"""Adjudicate the frozen equal-population atlas via the existing pinned model driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import subprocess
import sys

root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
path = root / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
data = path.read_bytes()
if sha1(b"blob " + str(len(data)).encode() + bytes(1) + data).hexdigest() != "0fd5a1c3965e5be4b874969b8ae8c715b9e43a2e":
    raise ValueError("Unexpected historical review driver")
spec = spec_from_file_location("frozen_model_review", path)
driver = module_from_spec(spec)
spec.loader.exec_module(driver)
driver.ROOT = root
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/RESULT.md': '58803841adba8e2fe12b249ce056047f19bd961b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/SCOPE.md': 'e5f0a47eac185a477a37464a656e4c6b56531571',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/rank_minor.json': '8e409f075e9eb915b1e8c801fa6928614d3ce695',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/replay.py': '242680255a216519dcfc04a3c32d69ccf0d47a57',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/results.json': 'db4f67068a9b80f715bada518c5f30278f5ea189',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/verification.json': 'e39a6f6cfa7a2b239a778f4f63cf381f36a82954',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_overlap/verify.py': 'c2acb1c949eb9a3f17d010d7ca5c752d2b5df4a0',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py': '45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py': 'b18f52109ccff9c7dc77542d3b8f3e5d5989102a'}
driver.QUESTION = 'Act as an independent mathematical referee for the frozen RESULT.md. Reconstruct why row sums fix the chart counts, why two kernel directions and one nonzero modular minor prove completeness and integer parameter bounds, and whether the histogram test really fixes all named exterior records. Try to break the non-relabel witness or its numerical comparison. Inspect the original push and glue_many code. Check the fixed-chart pushbacks, the two independent triple formulas, the sign in the root conversion, the claimed minimum of two scalar reads, the distinction between exhaustive finite computation and general proof, and the difference between joint observation and endogenous delivery. State what is supplied. P_math denotes the stated finite result. P_physical denotes an endogenous transition/receiver or physical interpretation. Return one JSON object with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status (independently DERIVED, REFUTED or OPEN), proof_checks with worked mathematical reasoning, limitations, and the arrays findings, missing_assumptions, counterexamples. On acceptance the final three arrays are empty. Report any actual defect even if this requires revision.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
