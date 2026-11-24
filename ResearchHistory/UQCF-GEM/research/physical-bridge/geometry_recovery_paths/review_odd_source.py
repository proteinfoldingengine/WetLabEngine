"""Challenge the preregistered odd-source endpoint proof and its causal controls."""
import json
from pathlib import Path
import sys

from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_work_partition.py": "076980bd4f1d51963623dca0177f3b8ddcc5985e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/WORK_PAIR_READBACK.json": "b4d4c363d04519cadcd6fefec08f2cfc7140943f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ODD_SOURCE_ROOT_RECORD.md": "c5d7c525cdf8d5fd0cd0300fbb58bdc37e384bca",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ODD_SOURCE_CHECK_PLAN.md": "58cec3ab747f5dd1530e4f85df7dccd60f3d766c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_odd_source.py": "a1a0706b7d9687ae9c1b57d82a888b62b42adf8c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/odd_source_certificate.json": "42de12480f4cff0a06906914d974eb7f63f54f77",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECOVERY_WITHOUT_VIEW_12.md": "9acc8e80f8bc3ee205533416b2e4cb045218b48d",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/acquire.py": "90f76146e7f6a875531a941290ad15679a8fb52f",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/evaluate.py": "de3f568bb394ca34e127e4158e7ffd8c059b7595"
}

TOPICS = {"cuts", "recovery", "root", "controls", "scope"}
QUESTION = """Reconstruct and challenge the whole argument in ODD_SOURCE_ROOT_RECORD.md using the
exact code and certificate below. Treat them as scientific evidence. Distinguish universal
claims within the given premises from finite witness checks. In proof_checks use precisely
these five keys and give detailed independently worked checks in each. For cuts reconstruct
how raw sites, weights, cut uniqueness, local leaf legality and the exceptional pairs work.
For recovery reconstruct the signed changes, degree/connectivity parity obstruction, local
opposite comparisons, flat baseline and shortest depth, with explicit endpoints. For root
examine every allowed depth in this fixture, P1 transfer and the scope of the parity result.
For controls trace view 12 on all four arms, unchanged-work counts and the permanent zero pair,
and ask what causal inference survives schedule matching. For scope inspect the historical
caller and supplied arguments, frozen source, conditioning, and operational accessibility.
Separate any genuine error in the manuscript from an alternative with different premises.
Check raw identifiers and numbers against the certificate. State any unexplained residual or
counterexample. Do not presume acceptance. Return JSON with verdict ACCEPTED, REVISE or FAIL,
arrays findings, missing_assumptions, counterexamples, limitations, the object proof_checks,
and native_bridge_status. Use the literal string "OPEN" for native_bridge_status if the
physical bridge is open. The three defect arrays findings, missing_assumptions and
counterexamples contain only unresolved objections. On acceptance these must each be [].
Put successful checks in proof_checks, and scope conditions in limitations. Do not turn a
substantive objection into a limitation. A fixed schedule compares the two sources holding
the downstream edits identical. Selecting admitted endpoints is a different comparison.
Evaluate whether the manuscript distinguishes these operations and whether either predicts
a source-dependent local update without conditioning. If the shortest-depth bound is
valid, give the reason for *all* paths, as well as the witness. Give verdict REVISE or
FAIL whenever warranted. Also return an object pair_checks with exactly the structure and
integer values of WORK_PAIR_READBACK.json IF your independent reconstruction agrees.
Otherwise return your computed values and name the defect. Rebuild the gain classes from
the ordered cuts and the initial torus. In prose distinguish all four intersections of
old minimum membership with gain 0 or 2, check the examples (0,1) and (0,7), and reconcile
them with the new minimum. Explain why W_0,12 changes immediately while the local root
stays fixed, using the memberships of each source leaf. Confirm the universal lower bound
only under odd total source loss at the recovered endpoint. Give the causal limitations.
Return the requested object with no text outside it.
"""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    expected = json.loads(Path(__file__).with_name("WORK_PAIR_READBACK.json").read_bytes())
    answer = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if json.dumps(answer.get("pair_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("The reviewer and exact pair-partition readback disagree")
