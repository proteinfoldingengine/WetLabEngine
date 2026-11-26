"""Read back the Actions ZIPs, exact review and both numerical streams."""
from contextlib import ExitStack
from hashlib import sha256
import json
import lzma
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile

here = Path(__file__).resolve().parent
science = here.parent.parent / "first_cut_return"
meta = json.loads((here / "MANIFEST.json").read_bytes())
digest = lambda content: sha256(content).hexdigest()
with ExitStack() as stack:
    data = {}
    for name, record in meta["archives"].items():
        archive = here / (name + ".zip")
        assert archive.stat().st_size == record["bytes"] and digest(archive.read_bytes()) == record["sha256"]
        z = data[name] = stack.enter_context(ZipFile(archive))
        assert z.testzip() is None
        if "SHA256SUMS" in z.namelist():
            for line in z.read("SHA256SUMS").decode().splitlines():
                expected, path = line.split(None, 1)
                assert digest(z.read(path.strip())) == expected
    review = data["first-cut-return-review"]
    publication = data["first-cut-return-publication"]
    foundation = data["first-cut-return-foundation"]
    for name in ("raw.json", "verification.json", "review.txt", "response.json", "receipt.json"):
        assert review.read(name) == publication.read(name)
    for name in ("RESULT.md", "ORBIT.md", "SCOPE.md", "probe.py", "verify.py", "review.py", "raw.json", "verification.json"):
        assert publication.read(name) == (science / name).read_bytes()
    regenerated = subprocess.check_output([sys.executable, "-B", str(science / "verify.py"), str(science / "raw.json")])
    assert regenerated == review.read("verification.json")
    receipt = json.loads(review.read("receipt.json"))
    assert receipt["checkout_sha"] == receipt["workflow_sha"] == meta["science"]
    assert int(receipt["run_id"]) == meta["run"] and int(receipt["attempt"]) == 1
    assert json.loads(publication.read("publication_audit.json")) == {"audit":"PASS", **receipt}
    for key, name in (("request","request.json"), ("response","response.json"), ("prompt","prompt.txt")):
        assert digest(review.read(name)) == receipt[key + "_sha256"]
    assert json.loads(review.read("request.json"))["contents"][0]["parts"][0]["text"].encode() == review.read("prompt.txt")
    response = json.loads(review.read("response.json"))
    answer = "\n".join(p["text"] for p in response["candidates"][0]["content"]["parts"] if "text" in p and not p.get("thought")).strip()
    assert answer.encode() == review.read("review.txt")
    verdict = json.loads(answer)
    assert (verdict["verdict"], verdict["program_status"], verdict["native_bridge_status"]) == ("ACCEPTED", "DERIVED", "OPEN")
    assert receipt["model_requested"] == "gemini-3.1-pro-preview" and response["modelVersion"] == receipt["model_returned"]
    assert all(verdict[k] == [] for k in ("findings","missing_assumptions","counterexamples"))
    assert foundation.read("SHA256SUMS") == publication.read("foundation-checksums.txt")
    assert foundation.read("workflow-head.txt").decode().strip() == meta["science"]
    assert foundation.read("inherited-head.txt").decode().strip() == meta["historical"]
    tests = json.loads(foundation.read("TEST_RECEIPT.json"))
    assert tests["passed"] and tests["tests_run"] == 22
    foundation_verify = json.loads(foundation.read("VERIFICATION.json"))
    assert foundation_verify["all_valid"] and json.loads(foundation.read("REPRODUCED_1615F.json"))["all_valid"]
    assert digest(lzma.decompress(foundation.read("certificates.json.xz"))) == foundation_verify["raw_certificate_sha256"] == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
print("PASS", meta["run"], receipt["model_returned"], verdict["verdict"])
