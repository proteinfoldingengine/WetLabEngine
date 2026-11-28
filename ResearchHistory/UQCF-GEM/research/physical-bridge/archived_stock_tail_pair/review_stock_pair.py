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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_stock_tail_pair/FINDING.md":"38e79cc98698546b730070e266adae8335fbabc4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_stock_tail_pair/stock_tail_replay.py":"f2675bb3763828da8f80e7a6a1a3aac9926bbe37",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_stock_tail_pair/stock-tail-evidence.json":"e3307bff14e5a89a2357d132562568f679236f99",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_lift/inherited_nested_balance.py":"c7209533fe987cf4900b894bac707ce06c762837",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py":"ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py":"a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/verifier.py":"e19999dfd46cd134d8191a59da7b8bf2cdb74b43",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py":"0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py":"9e995e21c9a477034a2fd4be615e28a2551b0bf9"
}
d.QUESTION="Independently and adversarially assess the archived stock-pair argument in FINDING.md, its observed replay evidence and its exact checking code. Reconstruct the supplied versus derived distinctions including the starting receiver, differences in global preparation, generated shared suffix, local recipient/spare inference, and nested attachment. Explicitly look for false causality, ambiguous input provenance, and any conflicting interpretation of the stock verifier checks. Do not infer independent scientific reproduction from the included same-implementation controls. Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN; and proof_checks, limitations, findings, missing_assumptions and counterexamples string arrays. Give at least five substantive checks including exact values or an algebraic reconstruction, and at least three scoped limitations. If accepting the scoped mathematical/software argument, leave findings, missing_assumptions and counterexamples empty."
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert len(result.get("proof_checks", []))>=5 and len(result.get("limitations", []))>=3
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
