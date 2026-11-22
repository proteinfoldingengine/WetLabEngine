"""Apply the existing pinned independent-review protocol to the lineage repair argument."""
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE.parent / "v1686_recombination_trace" / "review.py"
DRIVER_BLOB = "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/ASSESSMENT.md": "175be3a4733d3f322bfd35dfa811113c92466782",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/verify.py": "c5f7d59e9d968ffb9d2e3b756731fb2ad814d485",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/lineage_repair_trace/verification.json": "7de811bdb30043d6aa4a1914ba0ee0f52ee6b96c",
    "Tmp/TOE/retained_branch_identity_audit.py": "5032b156203183b33318e44f3c4492e5ac697503",
    "ResearchHistory/UQCF-GEM/foundational-closure-verification/PROOFS.md": "a21acad73c80cb748f2e42c244f6db53146c2bf2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/p1_receiver_location_resolution/RESULT.md": "4182ba347f8c11bad63315ffa6395c496ddfa498"
}
QUESTION = """Adjudicate the entire ASSESSMENT.md against the exact files below. Independently
try to break first arrival with arbitrary backgrounds, protected cuts, zero mean, coefficient
endpoints and multiple seed sites. Check exact-real normalization injectivity versus the
binary64 counterexample. Distinguish the initially equal parent in acquisition from its
deliberately changed fine state in the separate P1 factorization test. Prove or disprove the
one-parent iff for fixed common exterior inputs, the degree criterion and the stated numerical
split at s=13/20. Check what is user-supplied, whether this is an actual P1 event, and what
access and gravity claims the argument makes. Check the original callers and control scope.
Read the raw per-mask output and independent fixture implementation. A durable conclusion here
requires balancing the positive software same-row update and the limits on physical
identification. Return a JSON object with verdict ACCEPTED, REVISE or FAIL and arrays findings,
missing_assumptions, counterexamples, limitations, proof_checks, and field native_bridge_status.
ACCEPTED requires empty findings, missing_assumptions and counterexamples. State a concrete
repair for any substantive defect. A limitation already explicit in the argument is not a defect.
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
