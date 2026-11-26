"""Validate the pinned source-holder workflow archives against the checked-in experiment."""
from contextlib import ExitStack
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
meta = json.loads((here / "MANIFEST.json").read_bytes())
science = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent.parent / "four_child_source_holder"
def digest(data):
    return sha256(data).hexdigest()

initial = meta["earlier_argument"]
path = here / "initial_argument.zip"
assert digest(path.read_bytes()) == initial["sha256"]
with ZipFile(path) as z:
    assert z.testzip() is None
    parts = json.loads(z.read("response.json"))["candidates"][0]["content"]["parts"]
    first = json.loads("\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip())
    assert first["verdict"] == "ACCEPTED" and first["native_bridge_status"] == "OPEN"
    assert len(first["findings"]) == 5 and not first["missing_assumptions"] and not first["counterexamples"]
    assert z.read("result.json") == (science / "result.json").read_bytes()
    assert z.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert json.loads(z.read("request.json"))["contents"][0]["parts"][0]["text"].encode() == z.read("prompt.txt")

with ExitStack() as stack:
    archives = {}
    for name, row in meta["archives"].items():
        path = here / (name + ".zip")
        assert path.stat().st_size == row["bytes"] and digest(path.read_bytes()) == row["sha256"]
        z = archives[name] = stack.enter_context(ZipFile(path))
        assert z.testzip() is None
        if "SHA256SUMS" in z.namelist():
            for line in z.read("SHA256SUMS").decode().splitlines():
                expected, member = line.split(None, 1)
                assert digest(z.read(member.strip())) == expected
    review = archives["source-holder-review"]
    published = archives["source-holder-publication"]
    foundation = archives["source-holder-foundation"]
    for key in ("receipt.json", "review.txt", "response.json", "raw.json", "result.json"):
        assert review.read(key) == published.read(key)
    assert review.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert review.read("result.json") == (science / "result.json").read_bytes()
    summary = json.loads(review.read("result.json"))
    assert summary["raw_sha256"] == digest(review.read("raw.json"))
    assert summary["deferred_cases"] == 8 and summary["positive_comparisons"] == 312
    assert summary["three_tip"]["acquiring_output_sets_disjoint"]
    assert summary["three_tip"]["original_caller_first_actions"] == [
        ["receiver acquires", "receiver acquires", 8],
        ["stop", "receiver acquires", 2], ["undo", "receiver acquires", 2]]
    assert sum(x[2] for x in summary["three_tip"]["bounded"]) == 71082
    receipt = json.loads(review.read("receipt.json"))
    assert published.read("foundation-checksums.txt") == foundation.read("SHA256SUMS")
    assert json.loads(published.read("publication_audit.json")) == {"audit": "PASS", **receipt}
    assert receipt["workflow_sha"] == receipt["checkout_sha"] == meta["verified_commit"]
    assert int(receipt["run_id"]) == meta["run"] and int(receipt["attempt"]) == 1
    assert receipt["model_requested"] == receipt["model_returned"] == "gemini-3.1-pro-preview"
    for key, name in (("request", "request.json"), ("response", "response.json"), ("prompt", "prompt.txt")):
        assert digest(review.read(name)) == receipt[key + "_sha256"]
    assert json.loads(review.read("request.json"))["contents"][0]["parts"][0]["text"].encode() == review.read("prompt.txt")
    parts = json.loads(review.read("response.json"))["candidates"][0]["content"]["parts"]
    answer = "\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip().encode()
    assert answer == review.read("review.txt")
    verdict = json.loads(answer)
    assert receipt["verdict"] == verdict["verdict"] == "ACCEPTED"
    assert verdict["native_bridge_status"] == "OPEN"
    assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
    assert foundation.read("workflow-head.txt").decode().strip() == meta["verified_commit"]
    assert foundation.read("inherited-head.txt").decode().strip() == meta["historical_commit"]
    assert json.loads(foundation.read("TEST_RECEIPT.json"))["passed"]
    verify = json.loads(foundation.read("VERIFICATION.json"))
    assert verify["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == verify["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", meta["run"], receipt["model_returned"], verdict["verdict"], "native bridge", verdict["native_bridge_status"])
