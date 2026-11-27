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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/post_gain_stock_normalization/RESULT.md": "1c74224733c021e3f019293ef95077776d9f5af0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/post_gain_stock_normalization/replay.py": "5a5aa40ca8546a86f48ad35377b7050d2a06fdeb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/post_gain_stock_normalization/expected.json": "c163db879a186475c6e6c4179cbcc9ea567eae94",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py": "1fe52278ce24fe01756eac666add9681e88318d5",
    "ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/producer.py": "44eb38cc3dff9d121fc634cd38c597acfc3f04c6"
}
d.QUESTION="Independently assess the complete program-level mathematical argument in RESULT.md and try to falsify it from the two pinned producers, exact replay and its controls. Check the masks, carrier, rooted supports, exact profile throughout each positive path, actual first-pair and ordered-label selection, old-label contraction, fixed reference through the intermediate phase, input custody and loss at the canonical endpoint. Consider whether target or diagnostic trace itself supplies the varying destination, whether the two fresh phases really omit an answer-bearing argument, and what the no-gain and reversed-order controls do and do not rule out. Distinguish a path computation from an actual listener, activation, state commitment, event provenance and independently available participant-owned retained readout. Classify the scope of the program proposition and the native bridge separately. Return JSON with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting, leave findings, missing_assumptions and counterexamples empty and state boundaries in limitations. Do not infer scientific novelty or a physical result."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
