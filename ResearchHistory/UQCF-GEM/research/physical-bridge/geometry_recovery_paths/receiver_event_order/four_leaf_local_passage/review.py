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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/PASSAGE_SCOPE.md": "a67aa666d80095b458c0f7688bb2348950040399",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/RESULT.md": "68aa6879ab0edad588b0f7831befb852c45d434c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/SCOPE.md": "09a4fe4174bb76fd301a6765112fbb24da5a9065",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/replay.json": "ef56c3a67f0b76fc94cf9222d92bbda3c3fb9076",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/replay.py": "b35ebbb8dc78b0de2487df4da82201b39c3bf520",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/search.json": "fc426e7c06092528eced7923a1625e78d6ba970a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/search.py": "e039403589ea94b4783ef3e106f035e515e60ecb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/verification.json": "ec0c1a0f542dc97edac030170a4f7c425df29a03",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_leaf_local_passage/verify.py": "c21606a9c20e56ec67874c29235172c339f06d26",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"
}
QUESTION = """Independently adjudicate the flat-four-leaf result. Check the original R caller, primitive complement thinning, necessity of the next local loss at every chart in both arms, endpoint dependence, independence of order, onset and first-loss grades, ambiguity of earlier addressed prefixes, effects of equal q for all four q values, and impossibility of unequal pairs involving q=1 or 4. Verify the six-chart role and cover argument, row-work test, same-address example, all reported counts and original archived-path check. Detect any claim outside the supplied invocation and event. Separate the conditional program theorem from autonomous physical enactment. Use limitations for valid scope boundaries, not findings. On acceptance use literal empty lists for findings, missing_assumptions and counterexamples. Challenge substantive flaws and withhold acceptance if warranted."""
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
