"""Adjudicate the historical trigger-fidelity result via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/ARCHIVE_SCOPE.md': '4c87b20ae3916678238ebe94a97a99eb124af867',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/RESULT.md': 'f81ee4afd591438f70a9b1a099f66b52f51d353f',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/SCOPE.md': '3d0a0c9871ca3adfb66a8a886ef482531ed05e42',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/TWO_CHART_SCOPE.md': 'e6417efdb89cdfcbe17344340f4109881d47ff4c',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/archived_profiles.py': '517d125e0d90944753cf42d3cf11802d535d7759',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/profiles.json': '835334d43cf668321513a3c20af1f652035632c1',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/replay.py': '65f90be50484981817a2b0b32ffdf971302849b8',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/results.json': 'cd0fa2569de146bb5340dc2220cba6081ce8e16a',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/verification.json': '6e294b207a936e9c0e9053464af0770452fb6e13',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_trigger_fidelity/verify.py': 'fa063119b672d1735ef76ca0f376e96c51d69920',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py': 'b18f52109ccff9c7dc77542d3b8f3e5d5989102a',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/evidence/PRODUCTION.json': '25e15faf44bb59c77cdd48abf7c8473395c1ae04',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-producer.log': '84ac51dc629da88adf84549a3c3a139f612c3cc6',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py': '48f132d141167d9cd85ff79ec41720b5dca4f8bb',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/PRODUCTION.json': '220e7644381df8e9f213a36a8f401bd18634cc69',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py': 'fc4a77fc4f01fce33fdb562423eca274cfb0c648'}
driver.QUESTION = 'Try to refute the topology classification in RESULT.md, its two-chart lower bound and constructed two- and three-chart converses, including ancestry of held descendants and conservation of the union. Verify the bounded fixed-position minimality claim including repeated starting views, local basis columns, whole paths versus distinct events, and the historical four-site/five-site scope. Check both archived v16.29 records against the live receipt fields, how indexing is transported, and whether membership is mistaken for same-provenance participant delivery. Evaluate the finite and general mathematical propositions and scientific scope separately from the participant handoff. Produce a JSON object. verdict must be exactly ACCEPTED, REVISE, or FAIL. program_status and native_bridge_status must independently be DERIVED, REFUTED, or OPEN. Include five arrays of strings: proof_checks, limitations, findings, missing_assumptions, counterexamples. Positive evidence goes in proof_checks, scope restrictions in limitations. The last three arrays describe unresolved defects or counterexamples to the claims as scoped; use [] when absent. Report genuine flaws candidly.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
