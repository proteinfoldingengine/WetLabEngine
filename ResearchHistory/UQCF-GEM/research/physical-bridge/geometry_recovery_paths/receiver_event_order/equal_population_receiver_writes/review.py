"""Adjudicate the frozen remote receiver write via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/RESULT.md': 'ee503bf7c374b4ff426388938fb6c56b5b0e3291',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/SCOPE.md': '45dc06b5ad4e4aa63b4ada5c113d50717a16a6a8',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/SOURCE_SCOPE.md': 'eed46358bc5136568e6d2af3f5fc935a8d21e341',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/replay.py': '96f4436608d080bc1f3441b3f3eb64560b0a7aab',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/results.json': '3ad90a58350dc9537360e906040fe81a0fdabda4',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/verification.json': '9d03f2c4075bd25172b3df1ab6f7b5697f2ed96f',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/verify.py': '49091e4fcfe67406e21c90d5ca934e50b77ed208',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py': '45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py': 'b18f52109ccff9c7dc77542d3b8f3e5d5989102a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/graph_producer.py': '6c8eca570cda82b64c0d06775672f33977be430a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3'}
driver.QUESTION = 'Independently adjudicate the frozen RESULT.md against the pre-execution scopes and attached source code. Try to refute the exact minimum of four from one original source modulo the two identical copies per support type. Verify the normalization, the equal-k inference, multiplicity bounds, independence of the direct small-count enumeration, proof that the 11-chart family contains every leaf and needs all its members, the actual source interventions and original normalizer and P1 calls, the triple-to-local-count mechanism, first gain and source-last collision. Be precise about paired endpoints versus intermediate geometry; active cover versus full atlas; conditional transient record versus endogenous scheduling and persistence. P_math concerns the stated fixture and conditional software result, P_physical concerns endogenous or physical delivery. Return one JSON object with verdict ACCEPTED, REVISE or FAIL, program_status and native_bridge_status (independently DERIVED, REFUTED or OPEN), proof_checks with specific reasoning, limitations, and the arrays findings, missing_assumptions, counterexamples. On acceptance the final three arrays are empty. Reject or request revision if warranted.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
