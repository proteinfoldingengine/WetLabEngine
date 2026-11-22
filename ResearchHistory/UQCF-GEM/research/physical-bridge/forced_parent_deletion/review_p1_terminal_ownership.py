"""Adjudicate the unrestricted terminal-owner and path-length argument."""
from pathlib import Path
import hashlib
import review_common_field


DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/P1_TERMINAL_OWNERSHIP.md': '61ebdfebfe956fabcd3d03cf72c2dfc457f67437',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_p1_terminal_ownership.py': '4901c99544ca269115860c13e2d7b7dfd99bd501',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md': '69ace252586ad0b323ca3c460304ead8da8fd917',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/P1_OWNER_ACTION_RESULT.md': '3ad8d7583b877e9ba03b7657409f06cd3d35bbfa'}

QUESTION = """Reconstruct and attack the finite-tree terminal characterization, root-only and root-fork controls, the receiver interval and exact disjointness condition, and common-family source-only erasure. Independently compute all four extremal lengths and the endpoint counts. Check whether the nonroot fork forces an actual b write on every shortest complete run, establishes a physical selection principle, or merely identifies the outstanding selection and access premises. Distinguish incidence minimization from fewest deletions. Compare the enumerated and analytic scopes. Review the checker without claiming to have executed it. Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations, substantive proof_checks and native_bridge_status OPEN. For ACCEPTED the first three arrays must be empty."""


if __name__ == "__main__":
    raw = Path("handoff/replay.json").read_bytes()
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, "handoff/replay.json": blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
