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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/FIXED_SOURCE.md": "e2fe118853bb88a70edb4271591ba02d1830b405",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/LOCAL_EVENT.md": "5a1fe3e2a7ef54a1cee46daa9bc9e98e1c4b13a8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/RESULT.md": "bc9f976e10d581558f67dd34a7494afb51b62f90",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/SCOPE.md": "8520a4429092cc0ba4e7527d765a08791ec6d770",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/orbit.json": "89502877e38aec790b2e65b1ed3a74e5eef9dc6f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/orbit.py": "e98440eda98ff2b8d4cdacc7f0626684b9edb92c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/replay.json": "c49deaadcd69dab57943dc9661a83a1cbeef575f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/replay.py": "487e7fc6a460488958406849a4ceedc63f8ba96b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/verification.json": "0b9a221c128e34d8c44da9f8a8d965c97d2abd94",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/star_contraction_record/verify.py": "98782ab3c4fc04dfd704d199acc3dcb2336c5ba4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py": "45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py": "ffd513619d182abea2b31bd90c38e12784557bf3"
}
QUESTION = """Independently adjudicate RESULT.md, especially retention versus acquisition and the two different source comparisons. Return exactly one JSON object. Check the original normalizer, lexicographic hitting-set argument, actual third-chart coverage (including nulls), matched P1 records, role of the supplied order, receiver-local first loss of U, the equal-work twin swap, phase erasure and terminal erasure of addressed differences. Assess separately P_math (conditional mathematical and program-trace results) and P_physical (autonomous initiation and physical access). Use verdict ACCEPTED, REVISE or FAIL; program_status for P_math and native_bridge_status for P_physical use DERIVED, REFUTED or OPEN. Put positive calculations in proof_checks, scope in limitations. An acceptance must have literal empty arrays findings, missing_assumptions, counterexamples. Challenge substantive defects and cite them in those arrays if any; do not presume success. Do not assume a numerical optimal 121-chart cover or a large historical execution. No claims about quantum states or gravity are to be adjudicated."""
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
