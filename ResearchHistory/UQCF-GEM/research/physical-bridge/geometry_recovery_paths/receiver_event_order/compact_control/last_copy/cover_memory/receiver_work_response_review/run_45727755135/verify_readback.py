import hashlib
import json
import lzma
from contextlib import ExitStack
from pathlib import Path
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
science = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent.parent / "receiver_work_response"
manifest = json.loads((here / "MANIFEST.json").read_bytes())
def digest(data):
    return hashlib.sha256(data).hexdigest()

with ExitStack() as stack:
    archives = {}
    for name, entry in manifest["archives"].items():
        path = here / (name + ".zip")
        assert path.stat().st_size == entry["bytes"]
        assert "sha256:" + digest(path.read_bytes()) == entry["digest"]
        archive = archives[name] = stack.enter_context(ZipFile(path))
        assert archive.testzip() is None
        if "SHA256SUMS" in archive.namelist():
            for row in archive.read("SHA256SUMS").decode().splitlines():
                expected, member = row.split(None, 1)
                assert digest(archive.read(member.strip())) == expected
    replay = archives["receiver-work-replay"]
    review = archives["receiver-work-review"]
    foundation = archives["receiver-work-foundation"]
    publication = archives["receiver-work-publication"]
    for name in ("review.txt", "response.json", "receipt.json"):
        assert review.read(name) == publication.read(name)
    receipt = json.loads(review.read("receipt.json"))
    assert json.loads(publication.read("publication_audit.json")) == {"audit": "PASS", **receipt}
    assert receipt["checkout_sha"] == receipt["workflow_sha"] == manifest["science_commit"]
    assert int(receipt["run_id"]) == manifest["run"] and int(receipt["attempt"]) == manifest["attempt"]
    assert receipt["model_returned"] == receipt["model_requested"] == "gemini-3.1-pro-preview"
    for key, name in (("response", "response.json"), ("request", "request.json"), ("prompt", "prompt.txt")):
        assert receipt[key + "_sha256"] == digest(review.read(name))
    request = json.loads(review.read("request.json"))
    assert request["contents"][0]["parts"][0]["text"].encode() == review.read("prompt.txt")
    parts = json.loads(review.read("response.json"))["candidates"][0]["content"]["parts"]
    written = "\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip().encode()
    assert written == review.read("review.txt")
    verdict = json.loads(written)
    assert verdict["verdict"] == "ACCEPTED" and verdict["native_bridge_status"] == "OPEN"
    assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
    assert verdict["check_values"] == {
        "changed_neighbor_pairs": 6, "local_maxima_twice": [4020, 4008, 3999],
        "receiver_source_work_after_times_four": [7988, 7976, 7967],
        "outer_legal_count": 32575, "only_non_source_command": [12, 2]
    }
    assert replay.read("raw.json") == publication.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert replay.read("result.json") == publication.read("result.json") == (science / "result.json").read_bytes()
    assert replay.read("RESULT.md") == (science / "RESULT.md").read_bytes()
    assert replay.read("check.py") == (science / "check.py").read_bytes()
    assert digest(replay.read("raw.json")) == json.loads(replay.read("result.json"))["raw_sha256"]
    assert foundation.read("workflow-head.txt").decode().strip() == manifest["science_commit"]
    assert foundation.read("inherited-head.txt").decode().strip() == manifest["historical_commit"]
    inherited = json.loads(foundation.read("VERIFICATION.json"))
    assert inherited["all_valid"] and json.loads(foundation.read("TEST_RECEIPT.json"))["passed"]
    assert json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == inherited["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", manifest["run"], receipt["model_returned"], verdict["verdict"], "native bridge", verdict["native_bridge_status"])
