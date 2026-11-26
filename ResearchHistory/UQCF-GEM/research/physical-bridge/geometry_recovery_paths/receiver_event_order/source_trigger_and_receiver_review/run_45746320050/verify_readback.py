"""Validate the pinned live source-withdrawal workflow archives against the checked-in experiment."""
from contextlib import ExitStack
from hashlib import sha256
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
meta = json.loads((here / "MANIFEST.json").read_bytes())
science = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent.parent / "source_trigger_and_receiver"


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
    review = archives["live-receiver-source-review"]
    published = archives["live-receiver-source-publication"]
    foundation = archives["live-receiver-source-foundation"]
    for key in ("receipt.json", "review.txt", "response.json", "raw.json", "result.json"):
        assert review.read(key) == published.read(key)
    assert review.read("raw.json") == lzma.decompress((science / "raw.json.xz").read_bytes())
    assert review.read("result.json") == (science / "result.json").read_bytes()
    summary = json.loads(review.read("result.json"))
    assert digest(review.read("raw.json")) == meta["raw_sha256"] == summary["raw_sha256"]
    assert summary["original_campaign"] == ["VERIFIED", 2863, 34234]
    assert summary["flat"]["original_internal_raising_steps"] == 132
    assert summary["flat"]["original_post_source_bystander_writes"] == 0
    assert summary["flat"]["distinct_events_under_all_priorities"] == 72
    assert summary["controls"]["fixed_target_remote_withdrawal_observers"] == 30528
    assert summary["controls"]["nested_equal_target_rival_comparisons"] == 375
    records = json.loads(review.read("raw.json"))["live"]
    assert len({(tuple(r["order"]),tuple(r["palette"])) for r in records}) == len(records) == 144
    distinguish, underway = 0, 0
    for record in records:
        runs, order = record["runs"], record["palette"]
        a, b = runs["A"], runs["B"]
        middle = order.index("C") == 1
        assert (a["c_trace"] != b["c_trace"]) == middle
        assert (a["first_change"][0] != b["first_change"][0]) == middle
        assert runs[""]["c_trace"] in (a["c_trace"], b["c_trace"])
        assert runs["AB"]["c_trace"] == runs["BA"]["c_trace"]
        assert a["receipts"] == b["receipts"] == [[0, False, 2, 2]]
        assert a["first_two_P1"][0] == b["first_two_P1"][0]
        distinguish += middle
        underway += middle and a["prefix_edits"] == 2
    assert (distinguish, underway) == (48, 24)
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
    tests = json.loads(foundation.read("TEST_RECEIPT.json"))
    assert tests["passed"] and tests["tests_run"] == 22
    verify = json.loads(foundation.read("VERIFICATION.json"))
    assert verify["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == verify["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", meta["run"], receipt["model_returned"], verdict["verdict"], "native bridge", verdict["native_bridge_status"])
