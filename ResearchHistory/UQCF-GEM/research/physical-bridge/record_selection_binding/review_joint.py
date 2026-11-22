"""Independently review the retained-record/P1 joint-instrument theorem."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/JOINT_INSTRUMENT.md": "6bafbf6414f71cf97f3bd5822b50cc90e7a0f34f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/verify_joint.py": "81765366cec8945a0364c3b9e8a329d31e5c4621",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/joint_verification.json": "b88a0c9fd3bbb48d4cb929c823e640f047503fd2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/ASSESSMENT.md": "0f2159b84e00f6b5718eaa7ee01812767ad2fb18",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/record_selection_binding/verification.json": "3e41266a65f0d3f60a2a11d8f46e900907fe5c87",
    "ResearchHistory/UQCF-GEM/v15/v15.11/ontology_continuity_audit.py": "8871e50f19322adbb62f34ea3837ba8e6cb16c8b",
    "ResearchHistory/UQCF-GEM/v15/v15.11/REPORT.md": "255a62a329cc4ebb445122a8c5602df6e2dabc9c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/measurement_first_review/RESULT.md": "e8523368d50c366150221c5210ea6192534008d7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/p1_receiver_location_resolution/RESULT.md": "4182ba347f8c11bad63315ffa6395c496ddfa498",
}
QUESTION = """Independently challenge every claim in record_selection_binding/JOINT_INSTRUMENT.md.
Reconstruct the theorem on the full matrix space. Check whether the Q outcome probability and
conditional state really force its unnormalized branch, including q=0, and whether subtracting
that branch from C uniquely forces rho_uu*pi_p. Verify complete positivity, trace preservation,
all sixteen matrix-unit identities, both canonical preparations and all rejecting controls.
Look for a different two-outcome CP instrument satisfying the exact all-input contract. Distinguish
that theorem from weaker restricted-state or more-than-two-outcome contracts. Check carefully
whether the joint-instrument result legitimately removes a requirement that conditioning equal
pushforward, and whether it nevertheless inserts an event typing, reset action, outcome law,
receiver, access relation or physical probability interpretation. The old actual-record source,
P1 benchmark, direct equality screen and prior receiver boundary are exact evidence, not authority.
Return JSON with verdict ACCEPTED, REVISE or FAIL and arrays findings, missing_assumptions,
counterexamples, limitations and proof_checks, plus field native_bridge_status. ACCEPTED requires
empty findings, missing_assumptions and counterexamples. Explain every defect and concrete repair.
Do not upgrade the native bridge merely because the mathematical instrument exists.
"""


def main():
    data = DRIVER.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Independent review driver changed")
    spec = importlib.util.spec_from_file_location("frozen_review_driver", DRIVER)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.DOCUMENTS = DOCUMENTS
    driver.QUESTION = QUESTION
    driver.main()


if __name__ == "__main__":
    main()
