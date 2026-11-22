"""Adjudicate the root amount constrained by a passive view using the pinned review client."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/PASSIVE_VIEW.md": "77d62e7b64bc6430842800114f9d0d93febb05d0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_passive_view.py": "ee3aec59f61b9525ed7d45e32dc55d91e824e993",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/passive_view_results.json": "bd2a0cee233530acc671853e6443da4917c4f4cd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROOT_TRIGGER.md": "967771b52c744c1e5b59da69b13b4881681abbc2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_original_atomic.py": "d9750d2cd672304be5342cc46d1eb4d50bd8eb6f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_root_trigger.py": "b9e5817a2a44c9b2010313d70f60a6d525c3e0b8",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
    "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "ResearchHistory/UQCF-GEM/demos/v16.24-consistency-order/TYPE_AND_PROOF.md": "8c25e9501994bdc337e5cbbc8a4fc50a373d5140",
    "ResearchHistory/UQCF-GEM/demos/v16.24-consistency-order/engine.py": "666617d33bf8925699d0dc440565588a5e40e57e",
    "ResearchHistory/UQCF-GEM/demos/v16.25-pruning-refinement-closure/engine.py": "e9c576a2590c8e16812f1b3fa0436111e3648f1c",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/producer.py": "44eb38cc3dff9d121fc634cd38c597acfc3f04c6",
    "ResearchHistory/UQCF-GEM/demos/v16.50-recursive-binary-composition/verifier.py": "970bd7fbecb0d7d2fc488f2e30ba32065d76328e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/incidence_grade_realization/RESULT.md": "d9a0a5b43e5c029adf5926a9ec0b14fd135951c2",
}
QUESTION = """Review PASSIVE_VIEW.md as an independent adversary. The sole assigned grade marginal is C;
no map or shared joint completion is granted on A across the alternatives. Rebuild both
endpoint A,C intersections and exactly which inequalities follow from overlap or from
nonnegative joint realizability. Derive both ranges, explicit attainments, equality case,
initial/middle blindness of the half-total property, and the sharp threshold. Recompute
the counting marginal, two numerical ranges, common-unit special case, negative signed
control, integer domain and original normalizer/control outcome. Compare the actual
v16.23/v16.24 source types and October counting convention, including the distinct formal
owner and physical access assumptions. Inspect the supplied proof and sources; say exactly
where it fails if you have a counterexample.
Return JSON with verdict ACCEPTED, REVISE or FAIL and arrays findings, missing_assumptions,
counterexamples, limitations and proof_checks, and field native_bridge_status. ACCEPTED
requires empty findings, missing_assumptions and counterexamples. In proof_checks give
concrete reconstructed equations and control numbers. Include in limitations at least the
event-selection and independently usable physical grade assumptions. An unreasoned verdict
gives no evidence of inspection. Distinguish declared prerequisites from proof defects.
"""


def main():
    data = DRIVER.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != DRIVER_BLOB:
        raise ValueError("Independent review driver changed")
    spec = importlib.util.spec_from_file_location("frozen_review_driver", DRIVER)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.DOCUMENTS = DOCUMENTS
    driver.QUESTION = QUESTION
    driver.main()


if __name__ == "__main__":
    main()
