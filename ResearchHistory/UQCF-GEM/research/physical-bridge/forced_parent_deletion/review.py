"""Adjudicate the two consecutive native deletions using the pinned review client."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/DERIVATION.md": "d154a565a602ddb5bf1fef1fd36596be889205d0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/verify.py": "5182e1af19a5c0174a5cb8560b61795d22dc57bc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/verification.json": "d6a73b9ffe7e7c2d4cd78c2ae029719b1eb8bd1b",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/NATIVE_ADMISSIBILITY.md": "ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/source_withdrawal_completion/WORKING_CONSTRUCTION.md": "cc74a6d511439106a703c863c512cb0d3badeb13",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/first_pruning_own_view_review/RESULT.md": "5f4a3758cfc59b9a7d023d541a8765801254943b",
}
QUESTION = """Independently challenge the complete argument in forced_parent_deletion/DERIVATION.md.
Reconstruct the two global deletion histories without fixing the location, actor, or label.
Check the abstract local criterion at internal vertices and leaves, native arity, all
hitting profiles claimed, the two controls and the fixed indexed-owner comparisons.
Verify the finite state scope, edge counting convention, and correspondence between
the independent formula and the archived admission check. Try to construct a
counterexample that satisfies the exact same premises. Check how this differs from
a specified parent withdrawal and a response restricted to one palette index.
Separate forced destination conditional on two deletions from a physical law selecting
those events and from access to the retained parent's effect. Treat an openly supplied
scope restriction as a limitation, and an unacknowledged required premise as a defect.
Return JSON with verdict ACCEPTED, REVISE or FAIL and arrays findings, missing_assumptions,
counterexamples, limitations, proof_checks plus field native_bridge_status.
ACCEPTED requires empty findings, missing_assumptions and counterexamples. Give concrete
repairs for material defects and do not infer physical gravity or benchmark certification.
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
