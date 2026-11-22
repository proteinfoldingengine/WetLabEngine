"""Review the frozen donor-read and phase-boundary evidence."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3',
 'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/verifier.py': '80a47f10231a086af161c4999c582fa038d064c7',
 'ResearchHistory/UQCF-GEM/demos/v16.45-binary-fork-unit-barrier/producer.py': 'e73a02ee05e11f0c6b041b783ba6ff9738271073',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/DONOR_READ.md': '8e455b165c5f8c174b09fafd8d358021079b8d53',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_donor_read.py': '130151a17ee347734e8251a47cb0f439b0dbdd82'}
QUESTION = 'Independently challenge this claim of a causal software write, including the original source and raw replay. Return a JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status as an independently reasoned string OPEN or DERIVED and proof_checks as an object with keys star, causal, fork and scope. Use one worked paragraph per key. Under star reconstruct both original paths up to the first B write, H, rank dependence and the common endpoint. Under causal analyze the in-place one-bit intervention, the third-index preparation difference, which receiver edit changes in each control, row 7 with the same preparation, both admissible exact-profile completions and distinct first acquisitions, admissibility versus normal form, and whether a fresh call or certificate was used between source and receiver. Under fork prove the cleanup-prefix rule and give the 1→17 witness and same-invocation non-interference argument. Under scope distinguish event provenance, batch launch, ordered palette, observability and physics. Return objections to the submitted claims in findings, missing_assumptions or counterexamples. Positive checks and rejecting controls supporting the claims belong in proof_checks. ACCEPTED requires all three objection arrays empty. Report worked checks for any verdict.'

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "donor_read_certificate.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    topics = ("star", "causal", "fork", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
