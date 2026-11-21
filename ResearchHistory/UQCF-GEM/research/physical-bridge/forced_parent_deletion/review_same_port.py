"""Challenge the fixed-port comparisons and their caller boundaries."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_bracket_ports.py": "80e74e11ef3af58ff41d49e1838091342b5ac6bf",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_logical_record.py": "3b1f4fabc56ee38e9ebec500b36c81b67b123e30",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_paired_record.py": "42eafc9014d71d0efb2f92d54c6c2e46e09fd94c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/same_port/single.json": "16d909ebfc3a2d0f761644977cbf0af950a96c6b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/same_port/paired.json": "6aa5c0767992ce85706bc7ab4f666592546e819d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/same_port/bracket.json": "99eeb524d5f1536837b73f2777497178cc8e3c01",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/SAME_PORT_RESPONSE.md": "215e94d3ab8609c235b2103084358cb105690092",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECORD_RESPONSE_PROTOCOL.md": "3f5a150e0ed1c089762af45daa9aa5c753ef4038",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/BRACKET_PORT_PROTOCOL.md": "bc9dd46f64b08a7574b750406a6ded723db43838",
    "ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/recoverability.py": "0a01d2eea4f0114b119fbb7beaf4619775c0f9f6",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py": "bf0b84e3b3e627d7916a5fb1b46ab9bd5eba03e6",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/geometry.py": "bb2e5022e581e46cebcdc7294bab368c8be2ffe2",
    "ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/linalg.py": "28bdab47d7fc237beb96f7ed7dcc63bd707a652b",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/H4_rock_test/v1687_16.py": "090a03bf665b97d7784f688c8294a348ad20507f"
}
QUESTION = "Independently adjudicate SAME_PORT_RESPONSE.md. Derive the residue matrix from the original opposite-roll vector rule, default build_base seed and the two original bracketings. Verify the balanced fixed-port probe, both baselines, signed gains, exact cancellation, common-inner-gate and identical-state controls and rank claim. Verify whether the historical program freely chooses one bracketing or enumerates both. Reconstruct single and two record results from the sharp encoding, actual pinching and logarithmic mean convention for +/-1. Test the parity-sector formula and finite tilt curves, pinching after a tilt, normalized local filter, nonselective local maps, marginal BKM vs joint BKM, rank/faithfulness and both encoded-copy nulls. Distinguish a nonzero response within these program types from a physically activated gain, amplitude-consuming owner or a new gravitational observable, and look for an unsupported joint caller claim. The checks are bounded deterministic comparisons; no measurements are claimed. Give equations, concrete numbers and original-function checks in proof_checks. Return JSON with verdict ACCEPTED/REVISE/FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks and native_bridge_status. ACCEPTED requires empty findings/missing_assumptions/counterexamples. Do not claim to have executed the code."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
