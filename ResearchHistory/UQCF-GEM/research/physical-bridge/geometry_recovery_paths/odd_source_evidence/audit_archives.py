"""Validate downloaded run archives, logged model replies, and deterministic scientific bytes."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect_manifest(archive):
    for line in archive.read("SHA256SUMS").decode().splitlines():
        digest, filename = line.split("  ", 1)
        assert sha(archive.read(filename)) == digest, filename


def run(root, cert):
    runs = json.loads((root / "run_manifest.json").read_bytes())
    original_hash = "28b4892855331ac627986167f3882304e246b90d882df685e0917a3f6e404aa2"
    foundation_hash = "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
    results = {}
    for group, info in runs.items():
        directory = root / group
        for item in info["archives"]:
            raw = (directory / (item["name"] + ".zip")).read_bytes()
            assert len(raw) == item["size"] and "sha256:" + sha(raw) == item["digest"]
        with ZipFile(directory / "odd-source-foundation.zip") as foundation:
            inspect_manifest(foundation)
            assert sha(lzma.decompress(foundation.read("certificates.json.xz"))) == foundation_hash
            assert json.loads(foundation.read("VERIFICATION.json"))["all_valid"] is True
            assert json.loads(foundation.read("TEST_RECEIPT.json"))["passed"] is True
            assert foundation.read("workflow-head.txt").decode().strip() == info["sha"]
        with ZipFile(directory / "odd-source-replay.zip") as replay:
            inspect_manifest(replay)
            assert replay.read("odd_source_certificate.json") == cert
            assert sha(replay.read("original/geometry_repair_certificate.json")) == original_hash
            assert replay.read("science-head.txt").decode().strip() == info["sha"]
            if group == "third":
                partition = replay.read("WORK_PAIR_READBACK.json")
        with ZipFile(directory / "odd-source-review.zip") as review:
            raw = review.read("response.json")
            prompt = review.read("prompt.txt")
            request = json.loads(review.read("request.json"))
            assert request["contents"][0]["parts"][0]["text"].encode() == prompt
            response = json.loads(raw)
            answer = "".join(p.get("text", "") for p in response["candidates"][0]["content"]["parts"]
                             if not p.get("thought", False))
            verdict = json.loads(answer)
            if group == "first":
                assert verdict["verdict"] == "ACCEPTED" and verdict["findings"]
                assert "receipt.json" not in review.namelist()
                results[group] = "replay and foundation passed; review validator rejected"
                continue
            assert json.loads(review.read("review.txt")) == verdict
            receipt = json.loads(review.read("receipt.json"))
            assert sha(raw) == receipt["response_sha256"] and sha(prompt) == receipt["prompt_sha256"]
            assert receipt["workflow_sha"] == receipt["checkout_sha"] == info["sha"]
            assert receipt["run_id"] == str(info["run_id"])
            assert verdict["verdict"] == "ACCEPTED" and verdict["native_bridge_status"] == "OPEN"
            assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
        with ZipFile(directory / "odd-source-publication.zip") as publication:
            inspect_manifest(publication)
            assert publication.read("odd_source_certificate.json") == cert
            audit = publication.read("publication_audit.json")
            assert json.loads(audit) == {"audit": "PASS", **receipt}
            markers = dict(line.split("_B64=", 1) for line in
                           (directory / "publication_readback.log").read_text().splitlines())
            assert set(markers) == {"response.json", "publication_audit.json"}
            assert base64.b64decode(markers["response.json"], validate=True) == raw
            assert base64.b64decode(markers["publication_audit.json"], validate=True) == audit
            if group == "third":
                assert publication.read("WORK_PAIR_READBACK.json") == partition
                assert verdict["pair_checks"] == json.loads(partition)
        results[group] = "replay, foundation, raw review and fresh publication verified"
    return results


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    directory, certificate = map(Path, sys.argv[1:])
    print(json.dumps(run(directory, certificate.read_bytes()), indent=2))
