"""Review the measured profile and its downstream write."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROOT_TRANSFER.md': '71cc89f3ed18a57be425eaa178e088f8f0f9f6ac',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_root_transfer.py': '585fd6261a0a108c674a04a3e498c61c5b91379e'}
QUESTION = "Adversarially check this as a proposed dynamics, not a historical discovery. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations, native_bridge_status evaluating whether a physical bridge is derived, and a proof_checks object. Write a worked paragraph for each of four keys. Under termination prove the W−m bound for arbitrary arity including the duplicate within a minimum cover case. Under receiver derive both terminal sets and the root covector for C, accounting for role and scheduling freedoms. Under countermodel reconstruct the permitted rise and test C's entire history and endpoint. Under scope also check the parent-certificate connection to the original writer. Discuss whether an unconditional physical law, observer, or recreation of the ordered controller at 1488 follows. Flag false or overbroad claims. Return the calculations for any verdict."

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
