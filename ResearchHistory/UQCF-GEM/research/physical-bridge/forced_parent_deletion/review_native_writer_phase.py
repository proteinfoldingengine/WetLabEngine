"""Review the independently replayed historical writer contexts."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.52-recursive-ternary-composition/producer.py': '90108c926299ca7cb66dca6acc4530bafcdb4a7e',
 'ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py': '0501a1b32c0a660646ff95ecbb8a37a8f2e04b80',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/NATIVE_WRITER_PHASE.md': '01eb0cf44125a834abfb7fdf2ddc02b014def90e',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/NATIVE_WRITER_PHASE_CHECK_PLAN.md': '19ca626e2b2a2d963110c9ae686a41528288e537',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_native_writer_phase.py': '969b8a5769096ebc745f1435a5d68ca1dd223771'}
QUESTION = 'Challenge this exact scope for historical v16.52 and v16.53, without treating the software as a physical writer. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status OPEN or DERIVED, and four worked proof_checks paragraphs keyed repeated_event, rising_event, local_history, scope. The strict validator requires, on acceptance, {"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[]}. Put supporting observations in proof_checks and genuine limits in limitations. Use REVISE or FAIL with concrete objections for errors. For repeated_event, calculate the relevant memberships from the mask transitions and explain why the before/later futures at view 2 differ even with the same initial preparation, target, and complete event. For rising_event, compute explicit root/inner covers before and after view 1 deletes vertex 5, and calculate the root grade 4 to 3 at the first receiver write on the early route. For local_history, check the complete matched event, the receiver-local prefix, the exact grade change 7 to 1, and how the saved anchor and recursive/role-transport phases distinguish the original runs. For scope, state exactly which candidate inputs are insufficient, how the original broader move grammar relates to the source deletion, and which physical links stay supplied. You have exact source, checker, plan and replay summary. Calculate the requested checks regardless of verdict.'

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
    topics = ("repeated_event", "rising_event", "local_history", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
