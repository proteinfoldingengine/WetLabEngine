"""Independent review of a literal ancestry-to-recombination binding."""
import hashlib
from pathlib import Path
import review_common_field
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/TWO_PRUNES.md": "86c85ba5b65fe7d67388936348c2e8327578ad75",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/TWO_PRUNE_PROTOCOL.md": "cd282cfa7792b16b6ea1813d93f4d68b4b40727a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_two_prunes.py": "cdaf30b09a4b7081bcbd4d189c7ecf8178496439",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/evidence/two_prunes/result.json": "ccc911176795fa3c50b9029ef80aa1f38828a846",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_bracket_ports.py": "80e74e11ef3af58ff41d49e1838091342b5ac6bf",
    "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/History/H4_rock_test/v1687_16.py": "090a03bf665b97d7784f688c8294a348ad20507f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/RECOMBINATION_P1.md": "dfdf1edda8b23946dd8d78cdeaaa2ee84b7e7104"
}
QUESTION = "Independently challenge TWO_PRUNES.md. Derive the two-edit domain counts and integer scaling at both groupings. Reconstruct the original B4 intermediate with the stated double merge, its shared site-3 slope and the baseline-subtracted second probe. Check that no full match and the scalar count are claims about the complete deterministic replay, and inspect whether the checker establishes them and tests the native functions. Distinguish code-domain admissibility, an ambiguity of a fixed scalar, and native physical selection. Do not claim you executed code. Return JSON with verdict ACCEPTED/REVISE/FAIL, findings, missing_assumptions, counterexamples, limitations, proof_checks and native_bridge_status. Give concrete numbers and exact equations."
if __name__ == "__main__":
    data=(Path(__file__).resolve().parent/"review_common_field.py").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="423357012a59a192b158204df03ffd9dbb4ee90e"
    review_common_field.DOCUMENTS=DOCUMENTS
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
