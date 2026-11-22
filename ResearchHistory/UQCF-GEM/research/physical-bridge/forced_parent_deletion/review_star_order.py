"""Review the frozen star ordering theorem and matched events."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3',
 'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/verifier.py': '80a47f10231a086af161c4999c582fa038d064c7',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/STAR_ORDER.md': 'c37e1e3941d1c127a41f17259017306641359634',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/STAR_ORDER_CHECK_PLAN.md': 'e19cf047c16d68de78e7747429dd1de31aaa3873',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_star_order.py': '83a30ac071b1f268bdfa52d31e908e4e8650d048'}
QUESTION = "Adversarially check the star ordering theorem and independently reconstruct the original examples and enumeration scope. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status string OPEN or DERIVED, and proof_checks as an object with keys precedence, same_event, coverage and scope. Give one worked paragraph under each key. In precedence show necessity and sufficiency of arrows, last among occupied roles, inserting B, and why other recoloring cannot write to a last-ranked B when m>q. In same_event calculate the first masks and counts for the three- and four-view cases, distinguish causal contribution from occurrence, and test the unique cover. In coverage review the exact both-sides-blank definition, the 258 one-start exceptions and whether the formula was checked using all original paths. In scope identify what structure supplies, what still depends on the caller's rank, and what can be claimed about physics. Use objection arrays only for unresolved objections to the claims. Include positive checks and valid negative controls in proof_checks. ACCEPTED requires all three objection arrays empty. Supply the worked proof checks for any verdict."

if __name__ == "__main__":
    documents = dict(DOCUMENTS)
    for name in ("replay.json", "star_order_certificate.json"):
        path = Path("handoff") / name
        raw = path.read_bytes()
        documents[str(path)] = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = documents
    review_common_field.QUESTION = QUESTION
    review_common_field.main()

    response = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    checks = response.get("proof_checks", {})
    topics = ("precedence", "same_event", "coverage", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
