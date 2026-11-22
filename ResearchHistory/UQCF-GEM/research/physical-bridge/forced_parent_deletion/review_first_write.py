"""Adjudicate the source-conditioned first fork write on frozen code."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/producer.py': 'e73a02ee05e11f0c6b041b783ba6ff9738271073',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/star_normalize.py': 'd58cc9d1168d219b2869affd2d4ede889ebe579b',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/FIRST_WRITE.md': 'c566aa2a2291dec5e7a1d2474f4c4d2ebb260daf',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_first_write.py': '96af4b80c99093a0a8b7fa67a66477f7b7cd7327'}
QUESTION = 'Adversarially adjudicate the attached first-write proof, cases and original implementations. Return a JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status as an independently justified string OPEN or DERIVED, and a proof_checks object. Provide a worked paragraph for each key. Under source enumerate all valid immediate deletions and test local versus global conservation. Under grade derive the signs for removal and acquisition and distinguish first edit from terminal readout. Under writer inspect original normalizer sequencing, the two index orders, enumeration cardinality, and reorientation. Under phase reconstruct the actual three-index rise and its two distinct first writes and analyze the stored representative visits, whether they contain the source transition, and scope for physical launch, access, or gravity. Flag inaccurate deductions; the certificate records measured outputs. Keep positive observations and negative controls that support the claim in proof_checks. Reserve findings, missing_assumptions and counterexamples for unresolved objections to the submitted claim. ACCEPTED requires those three arrays empty. Report worked checks even when requesting revision.'

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "first_write_certificate.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    if not all(isinstance(checks.get(k), str) and len(checks[k].split()) >= 10
               for k in ("source", "grade", "writer", "phase")):
        raise ValueError("The review did not supply four written mathematical checks")
