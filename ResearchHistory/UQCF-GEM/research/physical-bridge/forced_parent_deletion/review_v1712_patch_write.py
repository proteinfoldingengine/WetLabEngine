"""Submit the archived patch update and replay to the standing reviewer."""

import hashlib
from pathlib import Path

import review_common_field


SCIENCE = "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/"
DOCUMENTS = {
    SCIENCE + "V1712_PATCH_WRITE.md": "24c93fc4c4ccd869b3efc1f47360202c3b0e7f4d",
    SCIENCE + "check_v1712_patch_write.py": "bca6e31df19a97c28e6df0a76549481857e7f96a",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1712_rg.py": "bc4504edbde3bc35815959f7f52288a57dced81a",
    "Tmp/TOE/Einstein 7/v1472_20_uci_candidate_package/v1472_20_uci_incident_adapter.py": "4926407e0694c1e049ca74feab1e5b38cc3c2ad6",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
}
QUESTION = """Independently reconstruct the proof and check all claims against the archived source.
Verify the same-input-port contrast and cyclic kernel, tensor indices, affine no-floor scope,
and Frobenius-norm and actual caller median arguments including all blind controls. Identify how
the fixture differs from the Gaussian caller and compare the exact written state with literal P1.
Reject any unsupported implication about physical access, event binding or a gravity signal.
The replay is evidence from the supplied GitHub job. Do not claim you ran it.
Return only one JSON object with exactly typed fields, in this form:
{"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[],"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}.
For ACCEPTED keep the first three issue arrays empty and give the explicit equations and control
outputs in proof_checks, as string key-value pairs. Use REVISE or FAIL for substantive defects.
"""


if __name__ == "__main__":
    replay = Path("handoff/replay.json")
    data = replay.read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    review_common_field.DOCUMENTS = {**DOCUMENTS, str(replay): blob}
    review_common_field.QUESTION = QUESTION
    review_common_field.main()
