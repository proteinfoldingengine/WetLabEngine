"""Challenge the exact native potential comparison with the pinned review client."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parents[1] / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/native_potential/ASSESSMENT.md": "c9bf741e7926f19148a49b5c96c0f3e5d6c836f2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/native_potential/verify.py": "e4703df0f067ba19b482eca19f62d44eeaeee553",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/native_potential/verification.json": "e9e7536be8d5cd65fd0e91897c73f88f96da7072",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/ASSESSMENT.md": "175be3a4733d3f322bfd35dfa811113c92466782",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/verify.py": "c5f7d59e9d968ffb9d2e3b756731fb2ad814d485",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/verification.json": "7de811bdb30043d6aa4a1914ba0ee0f52ee6b96c",
    "Tmp/TOE/retained_branch_identity_audit.py": "5032b156203183b33318e44f3c4492e5ac697503",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/p1_receiver_location_resolution/RESULT.md": "4182ba347f8c11bad63315ffa6395c496ddfa498"
}
QUESTION = """Adjudicate native_potential/ASSESSMENT.md from first principles using the attached full
files. Check the elementary leaf column against the original P1/P4/P6 types, root gauge
and separate arbitrary shifts. Check the orientation, which quantity has unit difference,
whether the surviving reference potential can be nonzero in each case, and whether applying
fine centering before pruning is essential. Reconstruct the independent rational solutions.
Test the comparison between the two retained parent-minus-sibling readings in the archived
repair using the original function, monotonicity and the existing controls. Distinguish
conditional identification of a field, a mathematical potential on a fine edge and accessible
native delivery. Cover every assertion, check for overgeneralization to all gravity, all
representations, or every detector. Return JSON with verdict ACCEPTED, REVISE or FAIL,
arrays findings, missing_assumptions, counterexamples, limitations, proof_checks, and field
native_bridge_status. ACCEPTED requires empty findings, missing_assumptions and counterexamples.
Include concrete repairs for defects. The known split predates this rational replay.
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
