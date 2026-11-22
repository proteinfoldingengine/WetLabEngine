"""Review the scoped two-child action and exact archived geometry replay."""

import hashlib
from pathlib import Path

import review_common_field


SCI = "ResearchHistory/UQCF-GEM/research/physical-bridge/"
BASE = SCI + "forced_parent_deletion/"
DOCUMENTS = {
    BASE + "P1_OWNER_ACTION.md": "9aee8fc5d5071648041dfa2fba28ed74ab715fd0",
    BASE + "check_p1_owner_action.py": "e2984b29bdc703a1153f6dbcbb2a61a0d440f815",
    BASE + "check_p1_meet_work_catalog.py": "5c817f67883f2d32d626ac426667b27914635a50",
    BASE + "check_p1_grade_work.py": "b5f5dba8a1998811cc1b879d6bee12c06afe15e7",
    SCI + "receiver_move_interface/RESULT.md": "0371d4a8aa66ce02ffbda084ad5dde93f1ec1136",
    "handoff/atomic_engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "handoff/atomic_verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "handoff/atomic_TYPE_AND_PROOF.md": "69ace252586ad0b323ca3c460304ead8da8fd917",
    "handoff/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "handoff/engine.py": "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    "handoff/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "handoff/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "handoff/fixtures.py": "9704660b4183f040c84a0734b52702258d1d42da",
}
QUESTION = """Independently review the scope of the proof and exact replay. Reconstruct the three
reachable local states after each source deletion using the inherited v16.26 same-union
pruning-only grammar. Check off-parent events, the source-only coalescing endpoints, and the
equivalence of tau_p=2 with the address-bearing receiver view. Prove who performs the forced
deletion and whether the original engine forces that completion. Contrast the previously
classified bare move domain with the new endpoint statement. Identify which of occurrence,
preparation, phase completion and physical receiver read remain supplied. Compare the two
local trigger sequences, global h, the owner-only observation, and an observation-blind
completion. No access, scheduler, or quantum carrier can be inserted by the reviewer.
Independently derive the fixture cover numbers, work values 58, 78, 80, added cut weights,
matched post-source and receiver work tables, and exact 50, 3 and 6 nearest pairs. Inspect
the original archive gate and the forced grade at the receiving parent and child. Compare
your calculations to the recorded replay. Treat the augmented layout as supplied and
do not claim you ran the code. The proof concerns the same mathematical event relation,
with no inference to physical gravity.
Return one JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions,
counterexamples, limitations, a proof_checks object with substantive string values, and
native_bridge_status OPEN. For ACCEPTED the first three arrays must be empty."""


if __name__ == "__main__":
    summary = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(summary)}\0".encode() + summary).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
