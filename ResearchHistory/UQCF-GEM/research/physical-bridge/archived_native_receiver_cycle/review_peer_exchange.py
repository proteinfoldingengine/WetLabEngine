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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/PEER_EXCHANGE.md":"f52a07d7f2bd0283a0e9d4db37b75cbd577e1b9c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/peer_exchange.py":"dee24d24420efe7b4cebeeae839e3c26eb758a39",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/peer_exchange_results.json":"ff6f063983fdee3f1cdb225d1ef5f862e46eaea8",
    "ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/producer.py":"44eb38cc3dff9d121fc634cd38c597acfc3f04c6",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py":"1fe52278ce24fe01756eac666add9681e88318d5",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/verifier.py":"af727ef01d1b4bf7d0f61c61be51a2ffcdb77035",
    "ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/coverage.py":"973244d0eb8a48bcb2464870377139cf4e9870c6"
}
d.QUESTION="""Independently and adversarially assess the complete scoped mathematical and software argument in PEER_EXCHANGE.md against the exact code and replay evidence. Develop the strongest positive form first, then challenge it.

Reconstruct exactly: (i) original compact case 170, including frames 14, 18, 24, 30 and 36, the two direct exchanges 1->4 and 4->7, the relayed payload 3, the receiver-subtree leaf writes and both exact fresh restarts; (ii) the independent incidence/topology/ordered-target calculation that predicts all 22 edits from frame 14 without reading the trace, program counter, role array, next frame or branch indices; (iii) the direct saturated orientation theorem: with W roles and k=W labels, after the source half the duplicated desired label y, the unique absent outgoing x, the canonical owner of y and the other holder of y determine source, recipient and payload; and (iv) the archive reconstruction claim for the 890 direct saturated exchanges and the stated compact relay cases.

Challenge scope with the strongest adverse evidence. In original cases 176/177, verify whether the complete raw midpoint [7,907,113,1,1] and the stated worker-visible roles, owners and slots are identical while the next receiver payload differs (4 versus 3) because the enclosing exchange retains x. Check the k-label compact family: at fixed k and recipient placement, whether one midpoint admits k-3 realized next writes, so the retained incidence alone cannot determine the payload when k>W. Check the 210 interleavings and whether only the historical all-source-first order erases x below the root. State explicitly whether this refutes any universal state-only receiver-write claim while leaving the k=W theorem intact.

Separate status sharply. The program-level compact relay and saturated orientation theorem may be DERIVED. The new numerical family and census were exploratory rather than prospectively preregistered and cannot be promoted to a numbered/certified campaign merely by replay. The ordered tree, palette, target ranks, canonical target/priority order, normalization invocation and historical update law are inherited or supplied inputs. The source outgoing role label is not identified with an existing post-P_XY P1 retained-source record or the separate four campaign event receipts. No physical event/state/record correspondence, native occurrence, observer access, probability law, geometry, curvature or physical prediction is established. A fresh normalizer restart receives the whole tree and ranks; do not call it an observer or an independently justified physical receiver.

Return exactly one JSON object with verdict ACCEPTED, REVISE or FAIL; program_status, saturated_theorem_status and native_bridge_status each DERIVED, REFUTED or OPEN; and proof_checks, limitations, findings, missing_assumptions and counterexamples string arrays. Give at least twelve substantive proof checks with exact case/frame/branch/label/count values and an algebraic derivation of the k-W+1 missing-label formula. Give at least seven scoped limitations. Preserve the spare-label result as an adverse counterexample, not as a reason to reject the narrower saturated theorem. If accepting the scoped mathematical/software argument, findings and missing_assumptions should name only defects in that scoped argument; bridge limitations belong in limitations, and counterexamples should record the claimed adverse boundary. Do not infer independent scientific reproduction merely from same-code replays."""
d.main()
if sys.argv[1]=="audit":
    result=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    assert len(result.get("proof_checks", []))>=12 and len(result.get("limitations", []))>=7
    print("Program:",result.get("program_status"),"saturated theorem:",result.get("saturated_theorem_status"),"native bridge:",result.get("native_bridge_status"))
    expected=("ACCEPTED","DERIVED","DERIVED","OPEN")
    actual=(result["verdict"],result.get("program_status"),result.get("saturated_theorem_status"),result.get("native_bridge_status"))
    if actual != expected:
        raise ValueError(f"Independent assessment requires adjudication: {actual}")
