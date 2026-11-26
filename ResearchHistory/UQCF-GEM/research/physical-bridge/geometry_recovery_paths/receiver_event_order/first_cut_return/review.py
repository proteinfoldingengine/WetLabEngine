"""Submit the first cut return study to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/RESULT.md": "799e6558b1dde66db08263bbf9afc6fd596d1b4a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/SCOPE.md": "9ed46c8ecd0a02839d7ad0f64c9c3c9f91789c1f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/ORBIT.md": "eb69ac686ef519d6404ac43595d2ae89d2f77b20",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/raw.json": "02b403782911892373dd747701e8f831bff6e2b6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/verification.json": "b4d603ac37cd64ebc3e0bba7b3c9bbcc1ebc2142",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/verify.py": "1d5358d7a3ecba71fcf545db8e45737e40145d2c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/first_cut_return/probe.py": "2520aba9e43f7f1c436c9345067c2484cc339d67",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/RESULT.md": "2daf9d691b19b8679374daebbafb9bf2f704159e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/verify.py": "65780a4c3374e49eacd44d47849430b6e5da4675",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/symmetric_matched_event/probe.py": "81014d679f411c78922e9c9de322ede5721b2fb6",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py": "2e75867e6aedb82ebe3d9c1f04733e2c0d33018a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/evaluate.py": "de3f568bb394ca34e127e4158e7ffd8c059b7595",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c"
}
QUESTION = "Challenge the bounded first_cut_return/RESULT.md. Check both actors including exact reversal, same-source grade restriction, coverage of the mutual edge in the distinct actor screen, necessity/sufficiency of the degree and opposite tests, the complete 968-index orbit and multiplicities after withdrawal, the 1-of-25 prospective result vs the exploratory radius-two description, whether chart positions can be derived once a leaf and one-edit non-undo restoration are specified, and whether either traced original component uses the irregular distance read to launch a write. Distinguish a finite criterion on a designed family from independent occurrence, physical access, or a scaling law. Return JSON with verdict ACCEPTED, REVISE or FAIL, program_status DERIVED, REFUTED or OPEN for the bounded mathematics, native_bridge_status DERIVED, REFUTED or OPEN for physical enactment. Include findings, missing_assumptions, counterexamples, limitations arrays and worked proof_checks. On acceptance leave the three defect arrays empty and put scope limitations in limitations. Draw independent conclusions."
QUESTION += """\n\nOutput contract: findings means exclusively outstanding defects. A confirmed result is never a finding in this interface. Put every successful calculation exclusively in proof_checks. If a defect remains, use REVISE or FAIL and describe it. An ACCEPTED object must contain exactly the following three literal fields: \\"findings\\": [], \\"missing_assumptions\\": [], \\"counterexamples\\": []. State all scientific reasoning freely in proof_checks and limitations. Validate this conditional schema before returning the object."""

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
    answer = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if (answer.get("verdict"), answer.get("program_status"), answer.get("native_bridge_status")) != ("ACCEPTED", "DERIVED", "OPEN"):
        raise ValueError("Independent review requires adjudication")
