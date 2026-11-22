"""Review the independently replayed two-view work records."""
import hashlib
import json
import sys
from pathlib import Path

import review_common_field

DOCUMENTS = {'ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py': '9128c24b695c1b539ac60dc93aeaf0bd4795c57b',
 'ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3',
 'ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py': 'e95e3e978779164dd91f09b80e3389247e6320c2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PAIR_WORK.md': '1615f0e5b4839957aaa256cb54b26955b5692d12',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/REMOTE_PAIR_WORK_CHECK_PLAN.md': '102ac544529b0e8031cafb38c4c79aaeac3bfd13',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_remote_pair_work.py': 'bd7e4bf120ac89e49dbb6b7e902ab900234e6b0a'}
QUESTION = 'Challenge the mathematical and implementation claims. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples and limitations, native_bridge_status OPEN or DERIVED, and four worked proof_checks paragraphs keyed copy, orders, blind, scope. On acceptance use empty arrays for findings, missing_assumptions and counterexamples, put positive observations in proof_checks and scope limits in limitations. For copy, derive the structural choice of donor and recipient and algebraic work gap using disjoint private sets and one shared leaf. For orders, reconstruct the first changes for all six orders including the controls that suppress the reference deletion, give the 2 of 3 and 0 of 9 counts, and check whether grades or hidden palette invalidate the one-sided test. For blind, trace the complete B,R mask word in row 232 with the alternate source assignment, distinguishing a true phase-boundary work gap from distinguishability from two projected histories. For scope, separate this exercised software interaction and uncalibrated geometric sign from autonomous physical origin and owner access. Use genuine objections if any. The plan discloses prior exploratory work. Certificate summary and complete code are included.'

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
    topics = ("copy", "orders", "blind", "scope")
    if isinstance(checks, dict):
        paragraphs = [checks.get(topic) for topic in topics]
    elif isinstance(checks, list) and len(checks) == len(topics):
        paragraphs = checks
    else:
        raise ValueError("Expected four worked checks")
    if not all(isinstance(p, str) and len(p.split()) >= 10 for p in paragraphs):
        raise ValueError("The review did not supply four written mathematical checks")
