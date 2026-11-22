"""Review the independently replayed inherited use of a receiver record."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECEIVER_RECOLORING.md': '95b7365e2ec58d41d6909e735c61fa2b32af315d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECEIVER_RECOLORING_CHECK_PLAN.md': '67455efe256f66070a8a780a78dc844f32be3458',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_receiver_recoloring.py': '1f11fc8c5450536b4d24f2982ce7141456be800e'}
QUESTION = 'Audit the inherited receiver-only mediation result and look for a counterexample. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status OPEN or DERIVED, and four worked proof_checks paragraphs keyed boundary, recolor, suppression, scope. On acceptance findings, missing_assumptions and counterexamples must be empty. Name objections in those fields if verdict is REVISE or FAIL. For boundary, reconstruct the active and silent orders from the original producer, calculate the full indexed difference at the copy boundary and derive the location of the common-grade contrast. For recolor, derive both first color vectors and effective edits in original rows 7 and 101, distinguish an attempted addition from an executed membership change, and explain the conditional B leaf deletion. For suppression, check why swapping one bit reproduces the other suffix, including whether earlier path or controller variables are read, and state what the script independently checks. For scope, test a B-blind realization against this software continuation and distinguish it from actual physical acquisition and numeric-grade consumption. Do the computations regardless of verdict.'

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json",):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    topics = ("boundary", "recolor", "suppression", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
