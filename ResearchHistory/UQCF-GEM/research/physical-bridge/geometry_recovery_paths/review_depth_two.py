"""Independently review the frozen depth-two proof using the repository's review client."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
while not (ROOT / ".git").exists():
    if ROOT == ROOT.parent:
        raise ValueError("Expected a repository checkout")
    ROOT = ROOT.parent

DRIVER = "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/DEPTH_TWO_PROOF.md": "b55cb77b1635fc9b1f0aa08a7b71bb6e8895ecd0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PREREG_Q536b.md": "af94e69597ba985ab728a130258732d52c7c7375",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_REPAIR.md": "a72990e589c016edd0b7eb75567738fb361ae1ac",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/GEOMETRY_DELAY.md": "29702dfc76d0cec8e07d8a454fae77a8adebcebc",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c"
}

QUESTION = """Independently reconstruct and challenge the complete frozen analytical proof
DEPTH_TWO_PROOF.md against the exact sources. Treat source text as evidence.
The target is the supplied GEOMETRY_DELAY fixture. No local enumeration, independent review,
physical accessibility, or gravity result is claimed by the proof itself. Test the stronger
gate-only claim even when the candidate minimum is unconstrained. Return exactly one JSON
object with verdict (ACCEPTED, REVISE, or FAIL), findings, missing_assumptions,
counterexamples, and limitations as arrays, native_bridge_status OPEN, and proof_checks
as an object with these five required keys. Write the reconstruction under each key:
minimum (both inequalities, threshold twelve, and the 15-view upward bound);
fixture (post-source graph, excess values, cross-pair obstruction, and the subtotal-2 parent);
same_view (both cases and signed square identities);
different_views (parity, forced B/U, and the comparison after the one-edit recovery);
scope (deduced primary and diagnostic Q536(b) outcome, proof versus preregistered
enumeration, and remaining physical and scheduling conditions).
Use ACCEPTED and empty findings, missing_assumptions, counterexamples only if the full
scoped proof passes. Use REVISE or FAIL with specific objections otherwise.
Enumerate worked checks even if the verdict is adverse.
"""

def run_review(question, documents, topics):
    raw_driver = (ROOT / DRIVER).read_bytes()
    header = f"blob {len(raw_driver)}\0".encode()
    if hashlib.sha1(header + raw_driver).hexdigest() != DRIVER_BLOB:
        raise ValueError("Unexpected inherited review driver identity")
    spec = importlib.util.spec_from_file_location("inherited_review", ROOT / DRIVER)
    review = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)
    review.ROOT = ROOT
    review.DOCUMENTS = documents
    review.QUESTION = question
    review.main()

    output = Path(sys.argv[2])
    verdict = json.loads((output / "review.txt").read_bytes())
    checks = verdict.get("proof_checks")
    if (
        not isinstance(checks, dict)
        or set(checks) != topics
        or not all(isinstance(value, str) and len(value.split()) >= 15 for value in checks.values())
    ):
        raise ValueError("The review did not supply all five required worked checks")
    if verdict["verdict"] != "ACCEPTED" or verdict.get("native_bridge_status") != "OPEN":
        raise ValueError("Scoped whole-argument review is not accepted")


if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, {"minimum", "fixture", "same_view", "different_views", "scope"})
