"""Adjudicate the full-atlas trigger and receiver results via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/CONTROL_SCOPE.md': 'bf447df17e4ab4d9636848cf0e51b2972337877e',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/RESULT.md': '3dd5ee69f4d6ee89654697cc6be07105dc60639a',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/SCOPE.md': '39753438dfd554067caae34fb423058c5992996d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/WRITER_SCOPE.md': '19dbe4217f92880daa578ea0395d06e1cbab16f2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/replay.py': '4119718fd5c9d5c1871f1d310d81b2bf72055847',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/results.json': '4072beef6317d94c5ab38d598d34cc9c260d68e0',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/verification.json': '5d1953856b8363dc4e9d30688b31084b47d27a3b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/verify.py': '5dc98bba0bf23c8830edb372a0051bf597b0734d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/writer.json': 'a75ebcd78539c41f6a811a15687892743e817d8b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/full_atlas_trigger_receivers/writer.py': '8e7a75a40a9be075a487b9e98bbb793cc5ef2bea',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/orbit_exchange/probe.py': '45eaeb0df71e6f6a5d9e205332f3bc015fcb4c8b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py': 'b18f52109ccff9c7dc77542d3b8f3e5d5989102a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/graph_producer.py': '6c8eca570cda82b64c0d06775672f33977be430a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py': 'ffd513619d182abea2b31bd90c38e12784557bf3'}
driver.QUESTION = 'Audit RESULT.md against the full prepared 121-chart orbit, the three calculation programs and historical operators. Try to refute the starting positive-event census, equal endpoint work, exact native trigger times, unique cover and receiver dependence, cross-history legality of the identical remote probe, protected completion theorem, attainable terminal counts, unrestricted merger obstruction and witness, and six full writer trajectories. In particular check that additions in late writer stages can erase the split which pure withdrawals cannot erase at cover number 12. Check what runs on all 121 charts directly versus the justified thirteen-chart restriction. The program proposition concerns the conditional mathematical and software results. The native-bridge proposition concerns spontaneous selection and initiation without supplying the common preparation, intervention or call; distinguish it from real receiver-dependent permissions and writes once invoked. Evaluate independently. Return a single JSON object with verdict (ACCEPTED, REVISE, FAIL), program_status and native_bridge_status (each DERIVED, REFUTED or OPEN), and five arrays of strings named proof_checks, limitations, findings, missing_assumptions and counterexamples. The last three arrays track unresolved defects, missing premises for the stated propositions and genuine counterexamples. Keep positive observations in proof_checks and explicit scope bounds in limitations. Use an empty array for any of the last three fields when there are none; substantive flaws should be identified and reported candidly.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
