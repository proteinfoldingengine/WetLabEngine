"""Publication/readback audit for the reviewed T-273 rank refinement."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

REVIEWED = "8921a58e3ec687b3c712b07a75746e5a392ef54b"
RUN_ID = 41524434282
ARTIFACT_ID = 13179825871
ZIP_SHA = "660efc5a5a54ca4c627fdaad0aaa8c2c0dc44f87c578260454e94b1888d1d5e4"
RESPONSE_SHA = "da31b55cefdc806fe8a34d343aef010f2d6c94bcb53463dd43b14a3ba96df9ce"
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
PREVIOUS = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
UQ = ROOT / "ResearchHistory" / "UQCF-GEM"
STAGE = UQ / "research" / "physical-bridge" / "constructive_candidates" / "t273_rank_refinement"
REVIEW = STAGE / "review" / "actions-41524434282"
OUT.mkdir(parents=True, exist_ok=True)
DETERMINISTIC = []

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write(name, obj, deterministic=True):
    target = OUT / name
    target.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    if deterministic:
        DETERMINISTIC.append(name)

def check(raw, record, label):
    assert len(raw) == record["bytes"], label + " byte count"
    assert sha(raw) == record["sha256"], label + " digest"

try:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert subprocess.check_output(["git", "merge-base", "--is-ancestor", REVIEWED, head], cwd=ROOT).returncode == 0

    receipt = json.loads((STAGE / "REVIEW_ARTIFACT_RECEIPT.json").read_text())
    assert receipt == {
        "review_run_id": RUN_ID,
        "review_attempt": 1,
        "reviewed_sha": REVIEWED,
        "artifact_id": ARTIFACT_ID,
        "artifact_zip_sha256": ZIP_SHA,
        "verdict": "ACCEPTED",
        "native_bridge_status": "NOT_DERIVED",
        "response_sha256": RESPONSE_SHA,
        "prompt_sha256": "10ceba6fe561a73f14909aa49f3a2fbda39b2ff4dd5ee5fb33d16b25d4489c21",
    }

    manifest = json.loads((REVIEW / "artifact_manifest.json").read_text())
    for name, record in manifest.items():
        check((REVIEW / name).read_bytes(), record, "review/" + name)

    docs = json.loads((REVIEW / "documents.json").read_text())
    prompt = (REVIEW / "prompt.txt").read_bytes()
    source_readback = {}
    for label, record in docs.items():
        path = ROOT / record["path"]
        raw = path.read_bytes()
        check(raw, record, label)
        reviewed_raw = subprocess.check_output(["git", "show", REVIEWED + ":" + record["path"]], cwd=ROOT)
        assert raw == reviewed_raw, label + " changed since review"
        assert raw in prompt, label + " absent from prompt"
        source_readback[label] = dict(record, current_sha256=sha(raw), reviewed_blob_equal=True)

    sys.path.insert(0, str(ROOT / ".github" / "scripts"))
    from uqcf_preparability_review import parse_response, accepted
    response = (REVIEW / "response.json").read_bytes()
    answer, verdict, model = parse_response(response)
    assert answer == (REVIEW / "review.txt").read_bytes()
    assert verdict == json.loads((REVIEW / "verdict.json").read_text())
    accepted(verdict)
    assert verdict["verdict"] == "ACCEPTED"
    assert verdict["native_bridge_status"] == "NOT_DERIVED"
    assert verdict["findings"] == []
    assert verdict["missing_assumptions"] == []
    assert verdict["counterexamples"] == []
    assert sha(response) == RESPONSE_SHA

    ident = json.loads((REVIEW / "review_identity.json").read_text())
    assert ident["science_sha"] == REVIEWED
    assert ident["workflow_sha"] == REVIEWED
    assert ident["run_id"] == str(RUN_ID)
    assert ident["run_attempt"] == "1"
    assert ident["model_requested"] == ident["model_returned"] == model == "gemini-3.1-pro-preview"
    assert ident["response_sha256"] == RESPONSE_SHA

    write("source-readback.json", source_readback)
    write("review-gate.json", {
        "status": "PASS",
        "review_run_id": RUN_ID,
        "reviewed_sha": REVIEWED,
        "artifact_id": ARTIFACT_ID,
        "artifact_zip_sha256": ZIP_SHA,
        "response_sha256": RESPONSE_SHA,
        "model": model,
        "verdict": verdict,
    })
    write("receipt.json", {
        "status": "PASS",
        "controller_sha": head,
        "reviewed_sha": REVIEWED,
        "review_run_id": RUN_ID,
        "publication_replay": PREVIOUS is not None,
        "native_bridge_status": "NOT_DERIVED",
        "scientific_breakthrough": False,
        "scope": "conditional rank theorem under SUPPLIED benchmark plus NEW TB",
    }, deterministic=False)

    if PREVIOUS:
        prior_manifest = json.loads((PREVIOUS / "artifact_manifest.json").read_text())
        for name, record in prior_manifest.items():
            check((PREVIOUS / name).read_bytes(), record, "previous/" + name)
        for name in DETERMINISTIC:
            assert (OUT / name).read_bytes() == (PREVIOUS / name).read_bytes(), "fresh replay mismatch: " + name
except Exception as exc:
    write("failure.json", {"status": "FAIL", "error_type": type(exc).__name__, "detail": str(exc)}, deterministic=False)
    raise
finally:
    write("artifact_manifest.json", {
        p.name: {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
        for p in sorted(OUT.iterdir())
        if p.is_file() and p.name != "artifact_manifest.json"
    }, deterministic=False)
