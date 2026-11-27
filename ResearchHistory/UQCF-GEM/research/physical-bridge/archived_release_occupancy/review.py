from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import subprocess
import sys
root=Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())
path=root/"review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
data=path.read_bytes()
if sha1(b"blob "+str(len(data)).encode()+bytes(1)+data).hexdigest()!="0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Historical review driver identity mismatch")
spec=spec_from_file_location("pinned_review",path)
d=module_from_spec(spec)
spec.loader.exec_module(d)
d.ROOT=root
d.DOCUMENTS={
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/RESULT.md": "61f85e2d87b70a3a909b14a0dcc1b96e6f50bf96",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/expected.json": "c8b17c474baedca362b37fda6abfac3f11f875b2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/replay.py": "fbd0cd13a308479b5736bb9aea8421eaa5259207",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/rows-0.json": "8a7e0804428539be75d104246ef310c8066de490",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_release_occupancy/rows-1.json": "b04706d8994bc6e911b819d6add0776a42cbb9be",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43"
}
d.QUESTION="Independently reconstruct the programs and archive rows before judging the scoped argument. In your proof_checks state the complete initial pending tuples in both calls and their common residual menu; explicitly analyze whether the input endpoints already supply labels and addresses and which single decision remains computed from the live state. Confirm or reject the exact root profile, rejecting early-gain and restoration controls, and what each peer can infer from its complete stutter-compressed local word with no inter-row order. Check that the scope does not infer a P1 event, receiver-owned access, or physically enforced activity from the implementation. Respond in JSON with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN; request_menu_status SUPPLIED or DERIVED (meaning provenance of the candidate label/address menu, not provenance of the next choice); and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting, leave findings, missing_assumptions and counterexamples empty and state boundaries in limitations. Do not infer physical significance."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    assert result.get("request_menu_status") == "SUPPLIED", "Adjudicate menu provenance"
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
