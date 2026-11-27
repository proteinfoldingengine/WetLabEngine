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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_generated_balance/replay_balance.py": "69ce389ee54050807ecf79f11e5a583171c91b7a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_generated_balance/expected.json": "cd54ffa510ce49d10f04c25e548300cb31cd3d4f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_generated_balance/FINDING.md": "06b4b158f3e834dd507acea72e51164657583eb3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_generated_balance/original-143.json": "790b6d8b6c5a21c35fcae5ea3e71c0c82ef49419",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/universe.py": "517ab8e20bc364c106e9a9b3ffaac23dc3a3b258"
}
d.QUESTION="Independently review the exact original M5 balancing archive interpretation in FINDING.md against the full raw row, producer, verifier, catalog and replay. Reconstruct the unique eligible directed moves at each completed boundary, scope of the continuation after the changed width, all relevant primitive cover/floor facts, the six necessarily newly changed rows and their invariance quantifier, and the exact row 11 trajectory including what is and is not retained. Audit the bypass-only primitive, the fresh encoded-start replay and equal canonical endpoint, and the independent complete grouping reconstruction. Distinguish actual recorded behavior from chance occurrence, native start/access and any stronger physical claim. Do not infer novelty. Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status each DERIVED, REFUTED or OPEN, and string arrays proof_checks, limitations, findings, missing_assumptions and counterexamples. If accepting the scoped program argument leave the last three arrays empty; separate stated scope limits from defects."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
