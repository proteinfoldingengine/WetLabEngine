"""Independent review of a literal ancestry-to-recombination binding."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/CALLER_BINDING.md": "439d7c5a38af2ccec2692e12700bf12fca4e515e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/CALLER_BINDING_PROTOCOL.md": "9428341ca403b64f86009511b680bcfc578875b8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_caller_binding.py": "5f262e5a0d45ce9bb2e6aa02466f48599df749aa",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/caller_binding/result.json": "e5813fac380a54e68a0130c4756a89100973bde5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_bracket_ports.py": "80e74e11ef3af58ff41d49e1838091342b5ac6bf",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/H4_rock_test/v1687_16.py": "090a03bf665b97d7784f688c8294a348ad20507f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/TWO_PRUNES.md": "86c85ba5b65fe7d67388936348c2e8327578ad75"
}
QUESTION = "Return only a valid JSON object using this exact field-type contract. {\"verdict\":\"ACCEPTED\",\"findings\":[],\"missing_assumptions\":[],\"counterexamples\":[],\"limitations\":[],\"proof_checks\":{},\"native_bridge_status\":\"OPEN\"}. For ACCEPTED the first three issue arrays must be empty. Limitations is an array of strings and proof_checks is an object of strings. Independently reconstruct the seed constraints, the exact two residue classes, all four archived two-port pairs, and the six two-prune mask failures. Inspect the original source for the actual later audit calls and check the projection argument including the zero residual scenario. Distinguish enumerated internal consumption from physical event binding or owner access. Do not claim you ran code. Report only concrete defects in findings with REVISE if needed."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
