"""Verify the three saved workflow artifacts, the source grade ledger, and the raw review."""
from contextlib import ExitStack
from hashlib import sha256
from io import BytesIO
import json
import lzma
from pathlib import Path
import sys
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SCIENCE = HERE.parent.parent / "junction_private_grades"


def digest(data):
    return sha256(data).hexdigest()


def main():
    manifest = json.loads((HERE / "MANIFEST.json").read_bytes())
    with ExitStack() as stack:
        archives = {}
        for name, info in manifest["archives"].items():
            data = (HERE / (name + ".zip")).read_bytes()
            assert len(data) == info["bytes"] and digest(data) == info["sha256"]
            z = archives[name] = stack.enter_context(ZipFile(BytesIO(data)))
            assert z.testzip() is None
            if "SHA256SUMS" in z.namelist():
                for line in z.read("SHA256SUMS").decode().splitlines():
                    expected, member = line.split(None, 1)
                    assert digest(z.read(member.strip())) == expected
        foundation = archives["junction-private-grades-foundation"]
        review = archives["junction-private-grades-review"]
        publication = archives["junction-private-grades-publication"]
        for name in ("raw.json", "result.json", "verification.json", "review.txt", "receipt.json", "response.json"):
            assert review.read(name) == publication.read(name)
        for name in ("SCOPE.md", "WORK_TEST.md", "RESULT.md", "check.py", "verify.py", "review.py",
                     "verification.json", "result.json"):
            assert publication.read(name) == (SCIENCE / name).read_bytes()
        raw = review.read("raw.json")
        summary = json.loads(review.read("result.json"))
        assert raw == lzma.decompress((SCIENCE / "raw.json.xz").read_bytes())
        assert digest(raw) == manifest["raw_sha256"] == summary["raw_sha256"]
        # Reconstruct the population and all first-event edges from the archived ledger again.
        sys.path.insert(0, str(SCIENCE))
        from verify import rejection_checks, verify
        rows = json.loads(raw)
        recounted = verify(rows)
        recounted["rejecting_controls"] = rejection_checks(rows)
        assert recounted == json.loads(publication.read("verification.json"))
        assert len(rows) == 36 and all(row["first"]["step"] == 1 for row in rows)
        assert sum(row["first"]["bit_at_return"] for row in rows) == 33
        receipt = json.loads(review.read("receipt.json"))
        assert json.loads(publication.read("publication_audit.json")) == {"audit": "PASS", **receipt}
        assert receipt["workflow_sha"] == receipt["checkout_sha"] == manifest["verified_commit"]
        assert int(receipt["run_id"]) == manifest["run"] and int(receipt["attempt"]) == 1
        assert receipt["model_requested"] == "gemini-3.1-pro-preview" and receipt["model_returned"].startswith(receipt["model_requested"])
        for key, name in (("request", "request.json"), ("prompt", "prompt.txt"), ("response", "response.json")):
            assert digest(review.read(name)) == receipt[key + "_sha256"]
        request = json.loads(review.read("request.json"))
        assert request["contents"][0]["parts"][0]["text"].encode() == review.read("prompt.txt")
        parts = json.loads(review.read("response.json"))["candidates"][0]["content"]["parts"]
        answer = "\n".join(p["text"] for p in parts if "text" in p and not p.get("thought")).strip().encode()
        assert answer == review.read("review.txt")
        verdict = json.loads(answer)
        assert receipt["verdict"] == verdict["verdict"] == "ACCEPTED"
        assert verdict["program_status"] == "DERIVED" and verdict["native_bridge_status"] == "OPEN"
        assert all(verdict[k] == [] for k in ("findings", "missing_assumptions", "counterexamples"))
        assert foundation.read("SHA256SUMS") == publication.read("foundation-checksums.txt")
        assert foundation.read("workflow-head.txt").decode().strip() == manifest["verified_commit"]
        assert foundation.read("inherited-head.txt").decode().strip() == manifest["historical_commit"]
        tests = json.loads(foundation.read("TEST_RECEIPT.json"))
        assert tests["passed"] and tests["tests_run"] == 22
        fv = json.loads(foundation.read("VERIFICATION.json"))
        assert fv["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
        assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == fv["raw_certificate_sha256"]
        assert fv["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
    print("PASS", manifest["run"], "36 first acquisitions, 33 retained at return;", receipt["model_returned"], verdict["verdict"])


if __name__ == "__main__":
    main()
