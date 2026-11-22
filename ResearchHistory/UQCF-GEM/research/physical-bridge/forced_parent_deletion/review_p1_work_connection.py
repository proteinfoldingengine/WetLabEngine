"""Review the one-address obstruction and the exact original downstream replay."""

import hashlib
from pathlib import Path

import review_common_field


BASE = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    BASE + "P1_WORK_CONNECTION.md": "c927a82fef384bdbc40bfa679cf2b2f404a98cb1",
    BASE + "check_p1_work_connection.py": "b155645e93753dcbf5312d2022b24b6cf3333975",
    BASE + "check_p1_grade_work.py": "b5f5dba8a1998811cc1b879d6bee12c06afe15e7",
    "handoff/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "handoff/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "handoff/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "handoff/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "handoff/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "handoff/application.py": "30348d71d366a751932ec2d58d18a9148d81ae83",
    "handoff/transport.py": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
    "handoff/holonomy.py": "bad3f06b291bb448a903b4f48344a9e54a633f68",
}
QUESTION = """Independently verify the scoped mathematical claims and inspect the exact archive source.
Derive the tree work metric for one-address equal-amplitude probes and retraction. Prove the
four-point contradiction for chordless squares and the collision control. Inspect the actual
degree and cycle gates, including the K5 control. Reconstruct both positive grade families,
their equal fine work, P1 parent output, identical retained fields, their distinct work tables,
the eight omitted minimum edges, joint terminal control and the torus neighbor/opposites tests.
Reconstruct the invariant 1 on the held face from the actual centered derivative, antisymmetric
edge term and loop product. Check that the full per-face control is faithful under the chosen
presentation and that the constant field is zero. Identify the supplied corner preparation,
retained label association and fixed event, and distinguish this actual numerical gate behavior
from a native preparation or physical receiver. Treat bounded replay as evidence and do not claim
you executed it. The original historical campaign remains outside this scope.
Return one JSON object with these exact field types: {"verdict":"ACCEPTED","findings":[],
"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},
"native_bridge_status":"OPEN"}. For ACCEPTED leave the first three arrays empty and use
substantive string values in proof_checks. Use REVISE or FAIL for any actual defect."""


if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
