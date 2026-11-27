"""Adjudicate the retained-record and ordering result via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/ARCHIVE_SCOPE.md': 'f30192fe50fa055f4ae1a3f8239ebe7148f35aa0',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/ORDER_SCOPE.md': '3c4f7e1e5bbba46c3c9496a75e40008eb549f1c1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/RESULT.md': 'd5666824a4f2ebeeff947276ac2a7ee79eb2bca2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/SCOPE.md': '710e38c37ff148b329ad7b81bbe97dad4fd272ab',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/archive_order.json': 'ac05f7650a06aa96ea9ecd90be1066f610f8b590',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/archive_order.py': '37bdc7a83e60dc8b0ba2b0bab1db1a447e53d3e2',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/replay.py': 'b0d8cf5fc252fc610f9d6a6cb0e6ad2978c8dcd9',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/results.json': '6a9a0029adacca2d4ea880c04a8057f4f55d2737',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/verification.json': '756cbe661fe37c1b56710ae078f4301427ec8a9b',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/retained_records_after_loop/verify.py': '37789d69d7f65e72c9bee5751b9db5e0b58c3eb7',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py': 'b18f52109ccff9c7dc77542d3b8f3e5d5989102a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/PRODUCTION.json': '220e7644381df8e9f213a36a8f401bd18634cc69'}
driver.QUESTION = 'Try to falsify the scoped mathematical and finite-computation claims in RESULT.md. Check the necessary-and-sufficient conditional snapshot criterion, internal sites, the minimum number of writes, the irreversibility/merger classification on the named star, which anonymous shape identifies which arm, exhaustive positive and erasing outcomes, and whether the source-last and no-source controls preserve what is claimed. Check the order argument for arbitrary withdrawal-only trees, including how union and ancestry are preserved. Check the archive identity and carefully distinguish the original archive square from the reconstructed matched path through it. The program_status field adjudicates ONLY the mathematical statements and bounded results just named: DERIVED if validated, REFUTED if contradicted, OPEN if unproved. Separately, native_bridge_status adjudicates whether a participant-owned causal delivery in which the source must precede the remote record is established. Do not equate the proof of a conditional distributed record with proof of delivery. Judge both independently. Return JSON with verdict ACCEPTED, REVISE, or FAIL, and program_status and native_bridge_status independently DERIVED, REFUTED, or OPEN. Include five string arrays proof_checks, limitations, findings, missing_assumptions, counterexamples. Give at least one specific limit on what evidence establishes in this model in limitations, even for a correct proof; scope limits are distinct from defects. Distinguish the anonymous remote chart signature from the all-chart one, with and without the supplied source boundary. Put affirmative findings in proof_checks; use findings only for substantive unresolved defects. ACCEPTED requires all three defect arrays empty. Give a counterexample or a specific missing fact if you find a defect.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))

    if answer.get("verdict") != "ACCEPTED" or answer.get("program_status") != "DERIVED" or answer.get("native_bridge_status") != "OPEN":
        raise ValueError("Independent review requires adjudication")
