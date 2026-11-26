"""Adjudicate the frozen square-geometry repair via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/equal_population_receiver_writes/verification.json': '9d03f2c4075bd25172b3df1ab6f7b5697f2ed96f',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/RECOVERY_SCOPE.md': 'a9acff1b5253ba0e56685e7da098f3f99e8c53d8',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/RESULT.md': 'de99780d9ab0495b0ab6ca1d87acc3c0b98868a4',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/SCOPE.md': '6eb2222a4fe7b94323bf88af216f1ce6351e15d9',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/replay.py': 'b75c7653282c0cd0264b6761d8bc75898363b4a1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/results.json': '14d4c184acfb065f80d4258975441854ee3e8da2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/verification.json': '518ec2f163f147b3cd74ff7b9acaab07eeb5671e',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/intrinsic_first_actor/verify.py': '5bce55160c77b0a36a1bbf9a8f5d8ee539cefe7b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py': '45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/exact_algebra.py': 'c67ea42b61321469f7735ce589f2e729b241666a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py': '8163beba8e52bc2a3a6d0c8cf59dd1257222f65c',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py': '5cd286b014bb44025e16832ee91a6e6665291c8c',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/projection.py': 'f857f2cf1cd4c265c193121236af8e441b1f01dc',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/graph_producer.py': '6c8eca570cda82b64c0d06775672f33977be430a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3',
 'review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py': '3324c0b46e09120ae526338444a19070b692d049'}
driver.QUESTION = 'Independently try to refute the finite mathematical claims and inspect the evidence in RESULT.md, SCOPE.md, and RECOVERY_SCOPE.md. Check the metric separation, the length-four common-actor argument, the opposite-pair necessary equalities, the exhaustive sufficiency step, parity at five, the six-step remote-first counterexample, the translation cover certificate for the original v16.26 trigger, the symmetry and normalizer scope, and source-priority census. Distinguish full holdings from the pair work alone. The mathematical proposition is the explicitly conditional classification; the physical proposition is whether these archived operations themselves initiate a particular update and deliver a new remote record. Shortest return is a supplied optimization criterion. Choose all verdicts independently. Return exactly one JSON object with verdict (ACCEPTED, REVISE or FAIL), program_status and native_bridge_status (each DERIVED, REFUTED or OPEN), and arrays proof_checks, limitations, findings, missing_assumptions, counterexamples. Each of the five arrays must be a JSON array of strings even for a single item. Report positive supporting calculations in proof_checks and scope limits in limitations. The final three arrays are reserved for unresolved defects, missing assumptions needed by the stated claims, or counterexamples to those claims. Use empty arrays there if none. For example the shape of an admissible response is {"verdict":"<assessment>","program_status":"<assessment>","native_bridge_status":"<assessment>","proof_checks":["<argument>"],"limitations":["<scope>"],"findings":[],"missing_assumptions":[],"counterexamples":[]}. Report any substantive defect candidly.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
