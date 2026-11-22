"""Review the exact pair-work identity and the matched P1 controls."""

import hashlib
from pathlib import Path

import review_common_field


DIRECTORY = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    DIRECTORY + "P1_GRADE_WORK.md": "d768dfbbd2164f4d0e46157f5bf61a4aa432c818",
    DIRECTORY + "check_p1_grade_work.py": "b5f5dba8a1998811cc1b879d6bee12c06afe15e7",
    "handoff/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "handoff/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "handoff/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
}
QUESTION = """Independently verify every scoped mathematical claim against the three original routines.
Derive the unit-tree work in subtree-drop coordinates, the exact decrement under P1, the
single-leaf magnitude and sign scope, and the rank bound and both-order decay. Check the depth
coefficient corollary from the displayed definition, separate from the unit-edge replay. Check
the three-pair tables, fine equality of the full work geometry, identical retained carrier with
distinct parent grades, neighbor switch, remote and terminal comparisons, and within-fiber
collapse. Check whether the original v15.40 evaluator actually computes the stated observables
and qualify the new calling interface. Separate the scalar work read from conserved fixed old-port
responses, and the abstract evaluator's equal outputs from physical receiver blindness. Confirm the
scope of physical selection, source event, and receiver access. Do not claim you executed the replay.
Return one JSON object with exactly these field types: {"verdict":"ACCEPTED","findings":[],
"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},
"native_bridge_status":"OPEN"}. For ACCEPTED the first three issue arrays are empty and proof_checks
has substantive string values. Use REVISE or FAIL for an actual defect."""


if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
