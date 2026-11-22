"""Adjudicate the fixed-effect calibration interval using the pinned review client."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/owner_effect_calibration/ASSESSMENT.md": "9aae23b855d1fe250d2f08e65f3872a37fd555ea",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/owner_effect_calibration/verify.py": "28a0c50463375f1a6817f7f573b08319a81a4c5e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/owner_effect_calibration/verification.json": "421a3eb78e96e8996e2bc183bbccb2f9c2db4f27",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_boundary/RESULT.md": "a04f23b6f667cf61c32149b1f3bb6e0316e60377",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/receiver_delivery_boundary/CORRECTION_T249.md": "270d284991afda4d4bf998e1a1ac88d4d3d3d9db",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/REALIZATION_INVARIANT_OWNER_EFFECT_2026_11_07.md": "19a42f89bec7da2cfb701908ae12318f42e9b298",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/support_sector_correspondence/RESULT.md": "56f94465168a858b10885c94bdcf6fba6f1c81f4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/OWNER_HELD_EFFECT_ACTION_DIRECTIVE_2026_11_07.md": "7f1ef751ef4891753f4743993af1aa4053e04bf1"
}
QUESTION = """Independently challenge every claim in owner_effect_calibration/ASSESSMENT.md.
Reconstruct the exact interval for an arbitrary effect, including noncommuting compressions,
off-diagonal source blocks, entangled complements, one-dimensional visible spaces, overlapping
or touching endpoints and the hidden factor size. Check that independently chosen block
expectations preserve the same coherent source channel on all inputs, rather than just the
two preparations. Check the relationship to the previous RD-0/RD-2/RD-4 and T249 qubit result.
Recompute both exact effects and all fixed controls from the frozen code and output. Verify
the qubit example remains the SAME owner effect and source input pair under the explicit
hidden-space enlargement, and whether whole-interface acquisition is claimed. Determine
whether this criterion actually earns native access or only characterizes a supplied
calibration class. Do not mistake fixed-effect response for optimized interface response.
Return JSON with verdict ACCEPTED, REVISE or FAIL and arrays findings, missing_assumptions,
counterexamples, limitations, proof_checks and field native_bridge_status. ACCEPTED requires
empty findings, missing_assumptions and counterexamples. Explain each defect and a concrete
repair. Assess the exact source packet rather than relying on earlier review verdicts.
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
