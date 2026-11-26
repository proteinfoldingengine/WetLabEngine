"""Submit the private-grade acquisition proof to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/SCOPE.md": "99b0b237cc2b081497c03a1b5a344fd84671d5e0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/RESULT.md": "c1eec6c220a415b98a6341a5ac2e69de055806fd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/check.py": "996a35ba7d729517d1a44cf78352b0b040fef5c0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/verify.py": "946f1b66c21346e283712e48f620cb9e015322c5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/production.json": "73d5cf6300e83499c4cb2c663daf8d0f59055346",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin/verification.json": "10076b90f2cfb70da154344bedca2ced2501972b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/historical.py": "b91756446ff6d3a50d3c63e4ce3d0862ac8c153b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"
}
QUESTION = "Independently evaluate the supplied marked_branch_origin analytical proof and bounded original executable replay. In your own reasoning reconstruct the two positive fine worlds, full prior equality, exact first-frontier completeness, unlabelled origin distinction versus true isomorphism, the receiver-only trace isomorphism, and evidence for retention, including no-op and inexact starts. Look for invalid scope or false claims of archive execution or reader ownership. Review the independent checker and provenance. The raw JSON has been reproduced in GitHub and is an artifact, not scored by its byte count. Identify the first remaining invocation/physical-owner premise separately. Return JSON with verdict ACCEPTED, REVISE or FAIL; arrays findings, missing_assumptions, counterexamples, limitations; and proof_checks with worked checks. On genuine acceptance keep findings, missing_assumptions and counterexamples empty, and put scope conditions and non-defects in limitations. Set program_status and native_bridge_status independently each to DERIVED, REFUTED or OPEN."
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
