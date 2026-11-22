"""Review the pinned P1 structural response through the existing review driver."""

import hashlib
from pathlib import Path

import review_common_field


DIRECTORY = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    DIRECTORY + "P1_ORDER_CURVATURE.md": "f5b3d260a2e0dc49f5efa8f9337278166f6f54e3",
    DIRECTORY + "check_p1_order_curvature.py": "34587438136b2cd39fce7bf019d76b244a6f4347",
    "handoff/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "handoff/spatial_graph_curvature_verifier.py": "c8043250f0a61077faabbc029ef7e248905f3f32",
}
QUESTION = """Independently reconstruct this bounded P1 leaf-removal argument from the pinned source.
Verify the shape and depth of the DAG input from inherited prefix incidence, the exact change of
the two profile columns, the Gram correction, normalization with epsilon, the neighbor-selection
guarantee including ties, and where the formal owner address enters. Calculate the matched fixture's
edge count, degree and curvature coefficient, held-edge values under both removals, the change to
the assembled scalar, and the sink-mask control. Inspect whether the replay checks the full
specified slice. Independently evaluate the grade-control pair with the original P1 code and verify
the reader factors through order for a fixed carrier. Distinguish that control from a grade-selected
event, and distinguish an owner-shaped numerical consequence from physical access or occurrence.
Read the replay evidence without claiming execution, and do not require a continuum claim, the
archive's full random campaign, or a new physical realization. Return one JSON object with exactly
these field types: {"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[],
"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}. For ACCEPTED keep the first three
issue arrays empty and give substantive proof_checks string key-value pairs. Use REVISE or FAIL if needed."""


if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
