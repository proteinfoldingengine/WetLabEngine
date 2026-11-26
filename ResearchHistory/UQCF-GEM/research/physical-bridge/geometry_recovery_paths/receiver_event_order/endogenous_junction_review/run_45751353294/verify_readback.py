"""Validate the pinned endogenous junction withdrawal workflow archives against the checked-in experiment."""
from contextlib import ExitStack
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
meta = json.loads((here / "MANIFEST.json").read_bytes())
science = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent.parent / "endogenous_junction"


def digest(data):
    return sha256(data).hexdigest()


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
    review = archives["endogenous-junction-review"]
    published = archives["endogenous-junction-publication"]
    foundation = archives["endogenous-junction-foundation"]
    for key in ("receipt.json", "review.txt", "response.json", "raw.json", "result.json"):
        assert review.read(key) == published.read(key)
    assert review.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert review.read("result.json") == (science / "result.json").read_bytes()
    original = archives["initial-review"]
    first_foundation = archives["initial-foundation"]
    for file in ("raw.json", "result.json"):
        assert original.read(file) == review.read(file)
    first_receipt = json.loads(original.read("receipt.json"))
    first = meta["initial_adjudication"]
    assert first_receipt["workflow_sha"] == first_receipt["checkout_sha"] == first["commit"]
    assert int(first_receipt["run_id"]) == first["run"]
    for tag, file in (("request", "request.json"), ("response", "response.json"), ("prompt", "prompt.txt")):
        assert digest(original.read(file)) == first_receipt[tag + "_sha256"]
    first_parts = json.loads(original.read("response.json"))["candidates"][0]["content"]["parts"]
    first_text = "\n".join(p["text"] for p in first_parts if "text" in p and not p.get("thought")).strip().encode()
    assert first_text == original.read("review.txt")
    first_verdict = json.loads(first_text)
    assert first_verdict["verdict"] == "ACCEPTED" and first_verdict["native_bridge_status"] == "DERIVED"
    assert any("initiat" in x.lower() for x in first_verdict["limitations"])
    assert first_foundation.read("workflow-head.txt").decode().strip() == first["commit"]
    assert first_foundation.read("inherited-head.txt") == foundation.read("inherited-head.txt")
    assert first_foundation.read("certificates.json.xz") == foundation.read("certificates.json.xz")
    summary = json.loads(review.read("result.json"))
    assert digest(review.read("raw.json")) == meta["raw_sha256"] == summary["raw_sha256"]
    assert summary["historical_campaign"] == ["VERIFIED", 2863, 34234]
    data = json.loads(review.read("raw.json"))
    assert len(data["released"]) == 96 and len(data["one_binary"]) == 3396
    extra = data["extension"]
    assert len(extra["presentations"]) == 432
    cases = [r for r in extra["presentations"] if r[5] == [2, 3, 2]]
    assert len(cases) == 72 and len({tuple(r[4]) for r in cases}) == 36
    assert sum(bool(r[10]) for r in cases) == 24
    records = extra["controls"]
    assert {(tuple(j["entry"]),j["chart"]) for j in records} == {
        (tuple(r[4]),c) for r in cases for c in (1,2)}
    for row in records:
        assert row["veto_guard"] == [1,1,2] and "exact parent" in row["veto_outcome"]
        assert len(row["base_guards"]) == len(row["base_calls"]) == 8
        assert row["base_calls"][-1][1] == [1,2]
        assert len(row["bypasses"]) == 4
        clean = [r for r in row["bypasses"] if r["clean_prior"]]
        assert len(clean) == 2
        for r in clean:
            assert r["cut_fields"] == [1,2,0,True] and r["source_kept"]
            assert r["closing_moves"] > 0 and not r["complete_at_first_return"]
            assert r["second_input"][1] == [0,1,2]
            assert r["receiver"][0] == row["live_receiver"][0]
            assert r["receiver"][-1] != row["live_receiver"][-1]
    assert summary["two_subtrees"]["clean_comparisons_by_ordinary_closure_size"] == [[1,2,288]]
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
    assert verdict["native_bridge_status"] == "OPEN" and verdict["program_status"] == "DERIVED"
    assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
    assert foundation.read("workflow-head.txt").decode().strip() == meta["verified_commit"]
    assert foundation.read("inherited-head.txt").decode().strip() == meta["historical_commit"]
    tests = json.loads(foundation.read("TEST_RECEIPT.json"))
    assert tests["passed"] and tests["tests_run"] == 22
    verify = json.loads(foundation.read("VERIFICATION.json"))
    assert verify["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == verify["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", meta["run"], receipt["model_returned"], verdict["verdict"], "native bridge", verdict["native_bridge_status"])
