"""Submit the frozen V1718 analysis and inputs to the standing review driver."""

import hashlib
from pathlib import Path

import review_common_field


DIRECTORY = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    DIRECTORY + "V1718_LOOP_REVERSIBILITY.md": "7dc0a572f5afe9dfcd3ca67d3885e84c39047f78",
    DIRECTORY + "check_v1718_loop.py": "61c7f0c6f4c1924f3aff91fe0240c520ce17d233",
    "handoff/v1718_complete.py": "638e68d00762642d6b58f692e7a1747816752232",
}
QUESTION = """Independently rederive each claim against the pinned original V1718 Python source.
Check the loop order, exact fixed-total same-carrier comparison, determinant expansion and
scope of its similarity invariant, the polynomial invertibility result and exceptional rank
control. Compare the reverse attempt with the inverse of the actual forward matrix. Rebuild the
skew generator and verify why its norm-only probe can miss nonidentity. Recompute the conditional
first and squared-norm moments and check the conditions under which they iterate for this loop.
Distinguish distributional identification from sample recovery, expected squared norm from
sample mean norm, and the genuine numerical source-to-loop dataflow from a native pruning input
or receiver. Check the replay is faithful and no unexecuted or physical claim is attributed to it.
You can read the evidence but should not claim you ran the replay. Return one JSON object with
these exact field types: {"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],
"counterexamples":[],"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}.
For ACCEPTED keep the first three issue arrays empty and give substantive proof_checks string
key-value pairs. Use REVISE or FAIL for a flaw."""


if __name__ == "__main__":
    report = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(report)}\0".encode() + report).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
