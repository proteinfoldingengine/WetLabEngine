"""Audit original GitHub ZIPs and match the model response to the publication log."""
import base64
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def check_manifest(archive):
    for line in archive.read("SHA256SUMS").decode().splitlines():
        expected, name = line.split("  ",1)
        assert digest(archive.read(name)) == expected, name


def check(directory, science):
    info = json.loads((directory / "run.json").read_bytes())
    assert info["conclusion"] == "success" and all(j["conclusion"]=="success" for j in info["jobs"])
    prefix = info["artifact_prefix"]
    for item in info["archives"]:
        data = (directory / (item["name"] + ".zip")).read_bytes()
        assert len(data) == item["size"] and "sha256:"+digest(data) == item["digest"]
    names = ["receiver_command_certificate.json"] if prefix == "receiver-command" else [
             "native_receiver_veto_certificate.json","receiver_owner_certificate.json"]
    with ZipFile(directory / (prefix+"-replay.zip")) as replay:
        check_manifest(replay)
        assert replay.read("science-head.txt").decode().strip() == info["head"]
        assert replay.read("inherited-head.txt").decode().strip() == info["inherited"]
        assert digest(replay.read("original/geometry_repair_certificate.json")) == (
            "28b4892855331ac627986167f3882304e246b90d882df685e0917a3f6e404aa2")
        for name in names:
            assert replay.read(name) == (science/name).read_bytes()
    with ZipFile(directory / (prefix+"-foundation.zip")) as foundation:
        check_manifest(foundation)
        assert foundation.read("workflow-head.txt").decode().strip() == info["head"]
        assert foundation.read("inherited-head.txt").decode().strip() == info["inherited"]
        evidence = json.loads(foundation.read("VERIFICATION.json"))
        assert evidence["all_valid"] and evidence["coverage"]["instances"]==21
        assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == (
            "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6")
        assert json.loads(foundation.read("TEST_RECEIPT.json"))["passed"]
    with ZipFile(directory / (prefix+"-review.zip")) as review:
        raw, prompt = (review.read(n) for n in ("response.json","prompt.txt"))
        request = review.read("request.json")
        assert json.loads(request)["contents"][0]["parts"][0]["text"].encode() == prompt
        pieces = json.loads(raw)["candidates"][0]["content"]["parts"]
        parsed = json.loads("".join(p.get("text","") for p in pieces if not p.get("thought",False)))
        assert parsed == json.loads(review.read("review.txt"))
        assert parsed["verdict"] == "ACCEPTED" and parsed["native_bridge_status"] == "OPEN"
        assert all(parsed[k]==[] for k in ("findings","counterexamples","missing_assumptions"))
        receipt = json.loads(review.read("receipt.json"))
        assert receipt["checkout_sha"] == receipt["workflow_sha"] == info["head"]
        assert str(info["run_id"]) == receipt["run_id"]
        assert [digest(v) for v in (raw,prompt,request)] == [
            receipt[k+"_sha256"] for k in ("response","prompt","request")]
    with ZipFile(directory / (prefix+"-publication.zip")) as pub:
        check_manifest(pub)
        for name in names:
            assert pub.read(name) == (science/name).read_bytes()
        audit = pub.read("publication_audit.json")
        assert json.loads(audit) == {"audit":"PASS",**receipt}
        markers = dict(l.split("_B64=",1) for l in (directory/"publication_readback.log").read_text().splitlines())
        assert set(markers) == {"response.json","publication_audit.json"}
        assert base64.b64decode(markers["response.json"],validate=True) == raw
        assert base64.b64decode(markers["publication_audit.json"],validate=True) == audit
    return {"status":"PASS","run":info["run_id"],"head":info["head"],"model":receipt["model_returned"],
            "raw_reply_sha256":digest(raw),"archives":len(info["archives"]),
            "scientific_bytes":{name:digest((science/name).read_bytes()) for name in names}}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    print(json.dumps(check(*(Path(p).resolve() for p in sys.argv[1:])),indent=2,sort_keys=True))
