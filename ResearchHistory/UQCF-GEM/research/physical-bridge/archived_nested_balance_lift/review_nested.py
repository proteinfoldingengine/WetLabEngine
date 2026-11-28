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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/FINDING.md": "a2c50c48fe9dd6c31a6f4c057a6ccb2218059666",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/inherited_nested_balance.py": "c7209533fe987cf4900b894bac707ce06c762837",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/expected.json": "b26ee5dc706a2d2ebac2ee00bafece18873ef71a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/m9-original-small.json": "f293de23f9d44315bce1128405dd9dd9d7474616",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/original-143.json": "790b6d8b6c5a21c35fcae5ea3e71c0c82ef49419",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py": "e19999dfd46cd134d8191a59da7b8bf2cdb74b43",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9"
}
d.QUESTION="Independently reconstruct and adversarially audit the historical-to-historical *new* nested composition in FINDING.md. Verify the identity separation (actual M5 and actual M9 vs new composition), byte-pinned historical clearance, exact original M9 nested control reconstruction, proposed compact-star prerequisites, global one-unit proof and explicit formula/path yielding receiver leaf 47’s retained label, parent deletion rejecting control, and the reached-state fresh-suffix limitation. Do not assume actual historical fusion, grade-contraction typing, endogenous startup or physical access. Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN; and proof_checks, limitations, findings, missing_assumptions and counterexamples string arrays. Give at least five explicit proof checks with your reconstruction (including actual frame boundaries and distinguishing controls) and three distinct limitation strings. If accepting the scoped mathematical/software argument leave findings, missing_assumptions and counterexamples empty. The auditor rejects a bare verdict."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert result.get("proof_checks") and result.get("limitations")
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
