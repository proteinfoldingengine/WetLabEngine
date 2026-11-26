"""Submit the star contraction study to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/GAIN_SCOPE.md": "d6a8f9dddde47d90333c1c57fb4f41c2f516ef1a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/LOCAL_SCOPE.md": "217ba0a319e8ebf56943920f4ceb4ab8ff8c8250",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/RESULT.md": "9084cbba492ed93a7d6107300eb6d83f42795e92",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/SCOPE.md": "54deafdf33eae107ba5e9982be4ee4a0c62a89e7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/census.json": "43bfd44a15de3e10ac1bb78339c5a79a54a77d5c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/census.py": "7f2a48b3eeb0deba54dcc61cb75d9aa772fef700",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/extension.json": "6d4c81aab95eb704aad9454f97470ecbd5db2476",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/extension.py": "4a0093f9fd0713d667002dfb7e6845b823487137",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/trace.json": "2173c2b0f682b56d9b35661b822cb548dd573d38",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/trace.py": "ec837bc2be16472e59229849f84b2b1ff65571a0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/verification.json": "df7f1a57df8d3abda6efcc24ed38ca441f04adc3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/order_free_star_receiver/verify.py": "dac795cd8cf3782c448f230fa77f0eb15d9a6609",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py": "ffd513619d182abea2b31bd90c38e12784557bf3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
QUESTION = """Independently check RESULT.md against the attached original code and independent enumerations. Return one JSON object. In particular test the theorem about the count at the first actual gain across contraction, palette substitution and final anchoring, the local collision construction for m>q, and the remote indistinguishability argument for the transitive orbit. Verify each optimum and both physical roles in the 5-by-5 preparation, case counting, unchanged and rising hitting number controls, the 1248 common novel addresses and all silent histories. Distinguish conditional mathematical behavior from a process that autonomously initiates a physical receiver transition. Use verdict ACCEPTED, REVISE or FAIL; assign program_status to the bounded mathematical result and native_bridge_status to physical enactment independently using DERIVED, REFUTED or OPEN. Use proof_checks for successful verifications and limitations for scope. Only an acceptance has findings, missing_assumptions, counterexamples all literal empty arrays. Challenge actual flaws. Do not treat a physical interpretation or a new payload value as established. The independent archive byte check is a separate workflow step."""
QUESTION += """
Output one JSON object with these REQUIRED top-level keys, in this order.
1. verdict -- your overall review decision. Choose exactly one string from ACCEPTED, REVISE, FAIL.
2. program_status -- the status of the finite mathematical claims. Choose exactly one string from DERIVED, REFUTED, OPEN.
3. native_bridge_status -- the status of autonomous physical enactment. Choose exactly one string from DERIVED, REFUTED, OPEN.
4. proof_checks -- a list of worked checks.
5. limitations -- a list of limitations.
6. findings -- a list of substantive issues.
7. missing_assumptions -- a list.
8. counterexamples -- a list.
Return all eight named keys in valid JSON. Judge the merits yourself. Do not replace verdict by program_status or put an overall review decision in a scientific status field."""
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
