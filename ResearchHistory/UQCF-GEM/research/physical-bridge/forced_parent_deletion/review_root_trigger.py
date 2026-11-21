"""Adjudicate the original root trigger after two native deletions using the pinned review client."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ROOT_TRIGGER.md": "967771b52c744c1e5b59da69b13b4881681abbc2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/DERIVATION.md": "d154a565a602ddb5bf1fef1fd36596be889205d0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_original_atomic.py": "d9750d2cd672304be5342cc46d1eb4d50bd8eb6f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/original_atomic_replay.json": "d7c0995e2dacdc48dc926726909c0f223edf1194",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/replay_root_trigger.py": "b9e5817a2a44c9b2010313d70f60a6d525c3e0b8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/root_trigger_replay.json": "0b91e925bb07d2e43db211fd5aef91b4bd701023",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md": "69ace252586ad0b323ca3c460304ead8da8fd917",
    "ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/evidence/PRODUCTION.json": "25e15faf44bb59c77cdd48abf7c8473395c1ae04",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md": "ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/pruning_record_bridge/ACCEPTED_DRAFT.md": "567589719e0fcb53caca534b3dfb17597707e096",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/view_local_pruning/REVIEWED_DRAFT.md": "2f2948e3e2d9c5ab405e49c988e3fed55f918d9b",
}
QUESTION = """Independently adjudicate the entire ROOT_TRIGGER.md including the original source-level
claims and both control anchors. Check the provenance of the trigger field in the archived
producer and independent verify_atomic, and the difference between the v16.26 local result
and unchanged global maximum. Verify enumeration, original campaign domain, label aliases,
neutral duplicate views and all six outputs. Check the historical byte replay and whether
the actual caller consumes per-event diagnostics or makes them available to an independent
owner. Try to disprove the conditional law on its exact domain; check all stated assumptions
and the historical comparison to the earlier five-vertex example. Inspect the appended code
and receipts rather than relying on prior acceptance. Distinguish progress in binding a
software output from the physical event/owner/read correspondence. Return JSON with verdict
ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations,
proof_checks and field native_bridge_status. An ACCEPTED verdict requires empty findings,
missing_assumptions and counterexamples. Give concrete repairs for any material defect.
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
