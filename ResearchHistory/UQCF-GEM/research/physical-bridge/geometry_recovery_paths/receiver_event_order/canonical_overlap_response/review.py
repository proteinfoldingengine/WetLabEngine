"""Submit the overlap response proof to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/RESULT.md": "ae78e254a372856d835e0d9e6f38425016e9f960",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/SCOPE.md": "5f9efecd4c7fb14e436e56a364d6c59e586c60ac",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/check.py": "0ff7078f3a356eb8b87144680b312a5aa3cba651",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/verify.py": "2cbd58e5fd5369c40d3f99d8284ab9d382ff7a3c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/verification.json": "06044453c61ee3a622d2e597fd0cc16757c1492a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/canonical_overlap_response/extract.py": "aa97822c38c6fd4eb04537165d1e537bb064f5ba",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/marked_branch_origin_review/run_45798072578/manifest.json": "617c5f2a7b81075e8ad5f9afadf1127e36d3255a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"
}
QUESTION = "Adversarially adjudicate this new conditional analytical composition and replay (NOT the previously reviewed archive's claim). Independently derive the cut response and the three stages of the overlap energy law. Verify whether the official v15.40 response constructor legally consumes those exact inputs, whether starting R and work truly match, and whether the historical standalone v16.53 run actually invoked the composition. Reconstruct the positive exact pair and the B-first negative control, ties and no-overlap case. Check the independent checker and distinguish a different edge incident on an anchored owner from non-isomorphism of unlabelled graphs. Look for hidden reader or a selected work threshold, confirm the source condition with matched action, and isolate the first outstanding premise for native R access. Return fields verdict (ACCEPTED, REVISE or FAIL), findings, missing_assumptions, counterexamples, limitations, proof_checks and separate program_status and native_bridge_status (DERIVED, REFUTED or OPEN). State actual defects; scoped limitations that do not refute the conditional claim belong in limitations. The workflow is replaying a fixed archive, not prospectively sampling. Do not trust author conclusions by default."
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
