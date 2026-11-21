"""Submit the frozen V1718/P1 interface argument to the standing reviewer."""
import hashlib
from pathlib import Path
import review_common_field

PATHS=[
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/V1718_P1_INTERFACE.md",
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_v1718_p1_interface.py",
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/PRUNING_COMPATIBLE_PATCH.md",
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/PRUNING_COMPATIBLE_PATCH_REVIEW.md",
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/V1718_LOOP_REVERSIBILITY.md",
 "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/V1718_LOOP_REVERSIBILITY_RESULT.md",
 "Tmp/TOE/Einstein_13_V1720 retained_bridge_core/v1718_complete.py",
 "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md",
 "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md",
]
QUESTION="""Independently adjudicate this corollary against the pinned V1718 source, the reviewed
P1-compatible alternating-bilinear classification, and the exact replay. Re-derive the argument
exchange between V1718 native_T and the cyclic wedge K. Check every basis image, the full-image
claim, and why an invertible output identification would pull the root total back to a forbidden
nonzero annihilating covector. Check that independent invertible input changes do not help.
Independently derive the T(x,0)=T(x,x)=x collision and its quantified consequence for a separately
additive source grade. Preserve the positive fixed-total source-to-loop result in its archived
scope. Challenge any extension to noninvertible quotients, restricted domains, event binding,
physical access, geometry or gravity. The replay is evidence; do not claim you executed it.
Return one JSON object with exactly these field types:
{"verdict":"ACCEPTED","findings":[],"missing_assumptions":[],"counterexamples":[],
"limitations":[],"proof_checks":{},"native_bridge_status":"OPEN"}.
For ACCEPTED keep the first three issue arrays empty and give substantive calculations as string
key-value pairs in proof_checks. Use REVISE or FAIL for a real defect."""

def blob(path):
    data=Path(path).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

if __name__=="__main__":
    replay=Path("handoff/replay.json")
    review_common_field.DOCUMENTS={p:blob(p) for p in PATHS}
    review_common_field.DOCUMENTS[str(replay)]=blob(replay)
    review_common_field.QUESTION=QUESTION
    review_common_field.main()
