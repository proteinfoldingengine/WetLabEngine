"""Independent argument challenge for the post-replay one-sided local record corollary."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_RETAINED_STATE.md": "e9d3dde48d3164240c7c83b23da8a9409c3d836d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_RETAINED_STATE_PLAN.md": "2b2d3da3f42cae293c544023dfcff54dff925ed1",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_reachable_states.py": "8cc8a96622875cfc7798c71a567fd529e29590a4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/reachable_receiver_certificate.json": "8f1efb8711ea6c4933eea73b79b9966b61f81a9b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_RECEIVER_VETO.md": "bec8104c6e3b867dd8819358f4c7d7edecfdfe00",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/native_receiver_veto_certificate.json": "fe6597fbe42ef5f0738ce0f576014932ac7c3bee",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/coverage_protected_record/RESULT.md": "18a2c08afe2bb9d1ba2cbf046243c678a7064ee8"
}
TOPICS = {"necessity","realization","families","witness","scope"}
QUESTION = """Challenge RECEIVER_RETAINED_STATE.md as a post-replay analytical corollary
within its explicitly stated model and two-source alphabet. No human peer review or
physical access is claimed. Rebuild the proof for arbitrary allowed interleavings, all
target local subsets, exact containment of the two future state families, and whether a
successful rather than a refused receiver action can leave a persistent state. State which
source can be identified and which observations are still ambiguous. Check the unreduced
control, the unrelated successful edit, and the claim about root grade versus membership.
Recognize the earlier coverage mechanism; flag reachability, probability, scheduling or
gravity overclaims wherever supported. Return JSON with verdict ACCEPTED, REVISE or FAIL;
arrays findings, missing_assumptions, counterexamples, limitations; native_bridge_status;
proof_checks and numeric_checks. An ACCEPTED verdict must have empty first three defect
arrays. Place substantive limitations in limitations and reconstructions in proof_checks.
Use literal string OPEN for native_bridge_status if operational access is open. The five
proof_checks keys are necessity, realization, families, witness and scope, each with 15+
words of worked reasoning. For numeric_checks return the following exact fields: size
(integer receiver membership cardinality), exponents (array for balanced source 662 then
718), fixed (array of the fixed address arrays in that order), distinguishing_absence
(integer leaf), conclusive_source (integer source leaf when that absence is observed),
unreduced_exponents (array in the same order), unrelated_leaf (integer). A different
answer is welcome with a concrete objection. Do not condition on later full geometry
admission, add a reader or assign a probability to a reachable subset."""
if __name__ == "__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    data = json.loads(Path(__file__).with_name("reachable_receiver_certificate.json").read_bytes())
    p,q = (str(data[name]) for name in ("source_p","source_q"))
    orig,b = (data["preparations"][n] for n in ("original","balanced"))
    expected = {"size":b["view_12_size"],"exponents":[b["arms"][i]["free"] for i in (p,q)],
                "fixed":[b["arms"][i]["fixed"] for i in (p,q)],
                "distinguishing_absence":data["source_q"],"conclusive_source":data["source_p"],
                "unreduced_exponents":[orig["arms"][i]["free"] for i in (p,q)],
                "unrelated_leaf":data["unrelated_command"]}
    verdict=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    if json.dumps(verdict.get("numeric_checks"),sort_keys=True) != json.dumps(expected,sort_keys=True):
        raise ValueError("Reviewer state-family values differ from the readback")
