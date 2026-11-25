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


def check_supplement(directory, science, label, certificate):
    info = json.loads((directory/(label+"_run.json")).read_bytes())
    assert info["conclusion"]=="success" and all(j["conclusion"]=="success" for j in info["jobs"])
    item, = info["archives"]
    archive = directory/(item["name"]+".zip")
    assert archive.stat().st_size==item["size"] and "sha256:"+digest(archive.read_bytes())==item["digest"]
    with ZipFile(archive) as z:
        check_manifest(z)
        assert z.read("workflow-head.txt").decode().strip()==info["head"]
        cert = z.read(certificate)
        assert cert==(science/certificate).read_bytes()
        raw = z.read("response.json")
        parts = json.loads(raw)["candidates"][0]["content"]["parts"]
        reply = json.loads("".join(p.get("text","") for p in parts if not p.get("thought",False)))
        assert reply==json.loads(z.read("review.txt"))
        assert reply["verdict"]=="ACCEPTED" and reply["native_bridge_status"]=="OPEN"
        assert all(reply[k]==[] for k in ("findings","counterexamples","missing_assumptions"))
        receipt = json.loads(z.read("receipt.json"))
        assert receipt["checkout_sha"]==receipt["workflow_sha"]==info["head"]
        assert str(info["run_id"])==receipt["run_id"]
        for f in ("request","response","prompt"):
            suffix=".txt" if f=="prompt" else ".json"
            assert digest(z.read(f+suffix))==receipt[f+"_sha256"]
        assert json.loads(z.read("request.json"))["contents"][0]["parts"][0]["text"].encode()==z.read("prompt.txt")
        assert json.loads(z.read("publication_audit.json"))=={"audit":"PASS",**receipt}
        markers=dict(l.split("_B64=",1) for l in (directory/(label+"_publication_readback.log")).read_text().splitlines())
        assert set(markers)=={"response.json","publication_audit.json"}
        for name, value in markers.items():
            assert base64.b64decode(value,validate=True)==z.read(name)
        result=dict(status="PASS",run=info["run_id"],head=info["head"],model=receipt["model_returned"],
                    raw_reply_sha256=digest(raw),certificate_sha256=digest(cert))
        if label=="field":
            errors=json.loads(z.read("numeric_errors.log"))
            assert set(errors)==set(json.loads(cert)["cases"])
            worst=max(value for row in errors.values() for value in row["maximum_absolute_errors"].values())
            assert worst<float(json.loads(cert)["tolerance"])
            result["largest_recorded_numeric_error"]=worst
        return result


def check_cover_p1(directory, science):
    return check_supplement(directory,science,"p1","native_cover_p1_certificate.json")


def check(directory, science):
    info = json.loads((directory / "run.json").read_bytes())
    assert info["conclusion"] == "success" and all(j["conclusion"]=="success" for j in info["jobs"])
    prefix = info["artifact_prefix"]
    for item in info["archives"]:
        data = (directory / (item["name"] + ".zip")).read_bytes()
        assert len(data) == item["size"] and "sha256:"+digest(data) == item["digest"]
    names = {
        "receiver-command": ["receiver_command_certificate.json"],
        "native-veto": ["native_receiver_veto_certificate.json","receiver_owner_certificate.json"],
        "receiver-record": ["reachable_receiver_certificate.json"],
        "geometry-selected": ["geometry_selected_record_certificate.json"],
        "single-view-return": ["single_view_returns_certificate.json"],
        "native-cover": ["native_cover_increment_certificate.json"],
        "source-gain": ["fixed_geometry_source_gain_certificate.json","fixed_geometry_source_gain_universe.json.xz"],
        "matched-source": ["matched_source_certificate.json","matched_source_universe.json.xz"],
        "cover-return": ["cover_return_certificate.json","cover_return_universe.json.xz"],
        "receiver-spare": ["receiver_spare_certificate.json","receiver_spare_universe.json.xz"],
        "protected-work": ["protected_work_certificate.json","protected_work_universe.json.xz"],
        "flat-cover": ["flat_cover_certificate.json","flat_cover_universe.json.xz"],
        "cover-member": ["cover_member_certificate.json","cover_member_universe.json.xz"],
        "receiver-prior": ["receiver_prior_certificate.json","receiver_prior_universe.json.xz"],
    }[prefix]
    with ZipFile(directory / (prefix+"-replay.zip")) as replay:
        check_manifest(replay)
        assert replay.read("science-head.txt").decode().strip() == info["head"]
        if prefix in {"cover-member", "flat-cover", "protected-work", "receiver-spare", "cover-return"}:
            assert replay.read("historical-head.txt").decode().strip() == info["inherited"]
        else:
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
    result = {"status":"PASS","run":info["run_id"],"head":info["head"],"model":receipt["model_returned"],
            "raw_reply_sha256":digest(raw),"archives":len(info["archives"]),
            "scientific_bytes":{name:digest((science/name).read_bytes()) for name in names}}
    if prefix == "native-cover":
        result["p1"] = check_cover_p1(directory,science)
    if prefix == "source-gain":
        cert=json.loads((science/names[0]).read_bytes())
        domain=lzma.decompress((science/names[1]).read_bytes())
        assert digest(domain)==cert["universe_sha256"]
        result["field"] = check_supplement(directory,science,"field","source_gain_field_certificate.json")
    if prefix == "matched-source":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["universe_sha256"]
        assert cert["star_domain"]["separating_pairs"] == 96
    if prefix == "cover-member":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["universe_sha256"]
        assert (cert["counts"]["equal_cover_separating"], cert["counts"]["pairs"]) == (108,2646)
        result["foundational_instances"] = evidence["coverage"]["instances"]
        result["archived_star_certificate_sha256"] = cert["archive_sha256"]
    if prefix == "cover-return":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["raw_sha256"]
        assert cert["arms"] == 2112 and cert["budget"]["arms"] == 81
        result.update(foundational_instances=evidence["coverage"]["instances"], primary_arms=cert["arms"],
                      budget_arms=cert["budget"]["arms"], archived_record_sha256=cert["archived_record"]["record_sha256"])
    if prefix == "receiver-spare":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["raw_sha256"]
        assert cert["priors"] == 8640 and cert["paired_histories"] == 25920
        result["foundational_instances"] = evidence["coverage"]["instances"]
        result["paired_histories"] = cert["paired_histories"]
    if prefix == "protected-work":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["raw_universe_sha256"]
        assert cert["domain"]["conflicts"] == 4116 and cert["domain"]["disconnected"] == 1212
        result["foundational_instances"] = evidence["coverage"]["instances"]
        result["archived_star_certificate_sha256"] = cert["archive_sha256"]
    if prefix == "flat-cover":
        cert = json.loads((science/names[0]).read_bytes())
        assert digest(lzma.decompress((science/names[1]).read_bytes())) == cert["universe_sha256"]
        assert cert["original"]["starts"] == 24 and cert["all_labels"]["starts"] == 288
        result["foundational_instances"] = evidence["coverage"]["instances"]
        result["archived_star_certificate_sha256"] = cert["archive_sha256"]
    if prefix == "receiver-prior":
        cert=json.loads((science/names[0]).read_bytes())
        domain=lzma.decompress((science/names[1]).read_bytes())
        assert digest(domain)==cert["universe_sha256"]
        with ZipFile(directory/(prefix+"-replay.zip")) as primary, ZipFile(directory/(prefix+"-publication.zip")) as comparison:
            for archive in (primary,comparison):
                errors=json.loads(archive.read("receiver_prior_numeric.log"))
                assert set(errors)=={"archive","swapped","factor_2_1"}
                assert all(0<=x<1e-8 for x in errors.values())
        failed=json.loads((directory/"original_failed_run.json").read_bytes())
        assert failed["conclusion"]=="failure"
        old=failed["original_archive"]
        previous=directory/old["local_name"]
        assert old["size"]==previous.stat().st_size and old["digest"]=="sha256:"+digest(previous.read_bytes())
        with ZipFile(previous) as failed_review:
            old_receipt=json.loads(failed_review.read("receipt.json"))
            assert old_receipt["checkout_sha"]==failed["head"]
            assert old_receipt["response_sha256"]==digest(failed_review.read("response.json"))
            old_checks=json.loads(failed_review.read("review.txt"))["exact_checks"]
            assert old_checks["eligible_next_per_case"]!=cert["legal"]
        result["preserved_failed_review"]=failed["run_id"]
    return result


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    print(json.dumps(check(*(Path(p).resolve() for p in sys.argv[1:])),indent=2,sort_keys=True))
