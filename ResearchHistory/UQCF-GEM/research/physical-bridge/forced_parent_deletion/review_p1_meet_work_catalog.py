"""Independently review the common-grade work obstruction and bounded replay."""

import hashlib
from pathlib import Path

import review_common_field


BASE = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    BASE + "P1_MEET_WORK_CATALOG.md": "c2309176722e11442abc4289786e69ea4da787a5",
    BASE + "check_p1_meet_work_catalog.py": "5c817f67883f2d32d626ac426667b27914635a50",
    BASE + "check_p1_grade_work.py": "b5f5dba8a1998811cc1b879d6bee12c06afe15e7",
    "handoff/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "handoff/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "handoff/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "handoff/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "handoff/fixtures.py": "9704660b4183f040c84a0734b52702258d1d42da",
    "handoff/overlap_PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
}
QUESTION = """Independently adjudicate the pinned argument and replay. From FCV P1 and v16.23 O1/O3,
derive the formula for one common grade embedded via each view, and reconstruct its work from the
anchored inverse and v15.40 pairing. Check signed and zero subtotals and the meaning of separation.
Prove or refute the claim for both meet-closed and join-closed effective catalogs. Explicitly compute
the neighbor-pair ties at the lower endpoint of a comparable minimum edge in the two cases for a
second neighbor. Inspect the actual original v15.42 degree, face, and opposite gates. Check whether
the argument needs all neighbors across the catalog, a physical receiver, or any v15.43 input schema.
Independently reconstruct the four fixture catalogs, both FCV composition orders, full 101-view
classification, 125 minimum edges, degrees, and original 25-view neighbor-pair distances. In particular
check the 35-view fixture with intermediate strips and the two edges with one shared side. Critique
the source preparation, inherited eligibility, and operational ownership scope. Compare your independent
arithmetic to the recorded replay. Do not claim you ran the code or that this is a physical signal.
Return one JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions,
counterexamples, limitations, a proof_checks object with substantive string values, and
native_bridge_status OPEN. For ACCEPTED the first three arrays must be empty."""


if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
