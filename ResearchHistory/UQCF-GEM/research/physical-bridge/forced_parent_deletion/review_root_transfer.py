"""Review the measured profile and its downstream write."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROOT_TRANSFER.md': 'cf7ec7753a54e64ea1155703a3462b03c09675cc',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_root_transfer.py': 'ac9b02be76a38dc9291dfd3db95c815f178e6ceb'}
QUESTION = "Adversarially check this as a proposed dynamics, not a historical discovery. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations, native_bridge_status evaluating whether a physical bridge is derived, and a proof_checks object. Write a worked paragraph for each of four keys. Under termination prove the W−m bound for arbitrary arity including the duplicate within a minimum cover case. Under receiver derive both terminal sets and the root covector for C, accounting for role and scheduling freedoms. Under countermodel reconstruct the permitted rise and test C's entire history and endpoint. Under scope also check the parent-certificate connection to the original writer. Discuss whether an unconditional physical law, observer, or recreation of the ordered controller at 1488 follows. Under countermodel also adjudicate the two exact-profile components, the forced change in C, and the equal ten-state C histories. Use native_bridge_status as a string, OPEN or DERIVED, and justify that choice. Reserve findings, missing_assumptions, and counterexamples for unresolved objections to the submitted claims. A valid negative control belongs in proof_checks; positive observations and declared premises are not objections. ACCEPTED requires all three objection arrays empty. If any substantive objection remains, return REVISE or FAIL and explain it. Distinguish necessity of this particular guard from insufficiency of the unguarded rule. Flag false or overbroad claims. Return the calculations for any verdict."

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "transfer_certificate.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    if not all(isinstance(checks.get(k), str) and len(checks[k].split()) >= 10
               for k in ("termination", "receiver", "countermodel", "scope")):
        raise ValueError("The review did not supply four written mathematical checks")
