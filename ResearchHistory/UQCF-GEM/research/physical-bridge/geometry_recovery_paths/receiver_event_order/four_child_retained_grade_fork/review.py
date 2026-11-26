"""Submit the four-child fork proof through the frozen project review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_retained_grade_fork/RESULT.md": "fe705089e381b06acecba2c57004c87e394b1217",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_retained_grade_fork/check.py": "4439c894cd46ca0c0ebbe31ff09ed00744d5bd93",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_retained_grade_fork/result.json": "4b5d341fbcf43a5546af3586ca5e52adfdb5b8aa",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = """Challenge the finite continuation-fork result in four_child_retained_grade_fork/RESULT.md using
the original producer, verifier and source atom. Inspect the 2-chart example. Identify what two
histories hold fixed, what is erased by removing repeated receiver masks, exactly what differs at the
shared state, whether both successors pass the original atomic rule, and how a fresh restart differs
from continuing an active path. Test whether the minimum-cover quantity is independently calculated
on each input or whether the original source operation has a direct dataflow link. Audit the
matched hidden-grade criterion, the independent historical path checks and all denominators,
including the 52 disjoint comparisons. State what the original R caller supplies. Distinguish
a deterministic single-valued selector from a multivalued move relation. Assess whether the stated
conditional memory requirement or a statement about physical ownership has been established.

Return one JSON object with verdict ACCEPTED, REVISE or FAIL, native_bridge_status, arrays findings,
missing_assumptions, counterexamples and limitations, and a proof_checks object with worked entries
example, source, history, campaign, and scope. Put any actual defect in findings. ACCEPTED assumes
no substantive defect. Do not change conclusions to satisfy a test."""
payload = DRIVER.read_bytes()
if sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() != "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Unexpected inherited review driver")
spec = spec_from_file_location("four_child_review_driver", DRIVER)
driver = module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT = ROOT
driver.DOCUMENTS = DOCUMENTS
driver.QUESTION = QUESTION
driver.main()
if sys.argv[1] == "audit":
    verdict = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if verdict.get("verdict") != "ACCEPTED" or verdict.get("native_bridge_status") != "OPEN":
        raise ValueError("Review requires scientific adjudication")
