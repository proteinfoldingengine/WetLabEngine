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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/TERNARY_PREPARATION.md":"7fa945043d2f86a65726c573a21914d4fe1424ce",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/ternary_preparation.py":"7bd6321ac2ba3d458d28518dd71ebca7705af303",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/ternary_preparation_evidence.json":"f5f752f70dd64a50c12a7a67dcbe51aced3b9ed5",
    "ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/producer.py":"44eb38cc3dff9d121fc634cd38c597acfc3f04c6",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py":"1fe52278ce24fe01756eac666add9681e88318d5",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/verifier.py":"af727ef01d1b4bf7d0f61c61be51a2ffcdb77035",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/coverage.py":"973244d0eb8a48bcb2464870377139cf4e9870c6"
}
d.QUESTION="""Independently and adversarially assess the complete scoped argument in TERNARY_PREPARATION.md against the exact replay evidence and code. Develop the strongest positive form first, then challenge it. Reconstruct exactly: (i) why archived cases 2208/2209 start from the same canonical incidences except the generated node-1/label-3 addition, (ii) how the historical rank-preserving expansion scan and overlap normalizer choose the source edit, receiving branch and payload, (iii) whether frame 21 truly differs from the quiet state only inside the proper receiver subtree with the source, receiver parent and ranks restored, and (iv) whether a fresh unmodified normalizer call consumes that retained receiver state and emits eight receiver-confined edits while the quiet call emits zero. Check the alternative eligible node-9 placement and all reported archive/census counts.

Separate these claims sharply. The program-level claim may be DERIVED even though the expansion-mode invocation, sibling traversal/order, and fresh second call remain supplied. Do not call traversal order an observer, but do not infer an order-independent receiver when the six-order control denies one. No P1 contraction typing, event/state/record correspondence, physical provenance, custody/access, autonomous initiation, probability law, or persistent terminal receipt is established. The source edit is generated only conditional on the selected archived expansion mode. The restart demonstrates an available native consumer on the same nested incidence object; it does not recover historical execution position and need not match the archived suffix. Determine whether this result removes the previously supplied cross-family M5-to-M9 attachment at program level while leaving the P1-to-v16.51 correspondence open.

Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL; program_status and native_bridge_status each DERIVED, REFUTED or OPEN; and proof_checks, limitations, findings, missing_assumptions and counterexamples string arrays. Give at least eight substantive checks, including exact case/frame/node/label/edit values and an algebraic reconstruction of the complement formula, and at least five scoped limitations. If accepting the scoped mathematical/software argument, leave findings, missing_assumptions and counterexamples empty. Do not infer independent scientific reproduction merely from same-code replays."""
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert len(result.get("proof_checks", []))>=8 and len(result.get("limitations", []))>=5
    print("Program:",result.get("program_status"),"native bridge:",result.get("native_bridge_status"))
    if (result["verdict"],result.get("program_status"),result.get("native_bridge_status")) != ("ACCEPTED","DERIVED","OPEN"):
        raise ValueError("Independent assessment requires adjudication")
