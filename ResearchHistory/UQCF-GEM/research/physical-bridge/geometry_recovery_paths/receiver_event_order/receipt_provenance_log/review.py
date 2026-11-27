"""Adjudicate the actual process-to-file custody of original receipts via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receipt_provenance_log/RESULT.md': '636247228ffc8cfeaf3adf32726423cc97a6d1eb',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receipt_provenance_log/SCOPE.md': 'e2cd39133d794014266f99e921c4ef9c1df4837d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receipt_provenance_log/replay.py': '8664983d4163530aa1fba63ce3f42cdf31a243a4',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receipt_provenance_log/results.json': 'db8c7b7c072e3d7f96750debd6dc85f384900cbe',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/COMMANDS.json': '3b560a00d8bacabc689f4703eca387ad819f2d3b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/EXECUTION.json': '31c961b7f86e36cc3c4a033ccf409305f89c2965',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/SHA256SUMS': '5b9073dda064590c14a067b5cd2e364ee7add0a6',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/WITNESS.json': '2d5c2eec7e5af4c5b975e4616d7d6caa3c194765',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-producer.log': '84ac51dc629da88adf84549a3c3a139f612c3cc6',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/producer.py': '4b171179d719372e855aa802b89e655496e4b6fa',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/run_campaign.py': 'da099fc328cde949e14ecb9afbd3d6217f6b7366',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py': '48f132d141167d9cd85ff79ec41720b5dca4f8bb'}
driver.QUESTION = 'Audit the campaign-custody claim in RESULT.md. Distinguish original in-process object identity, the verified subprocess-to-file route, the independently reconstructed WITNESS.json, and any participant-owned reader. Check the historical source manifest, command and stdout, same-actor histories and different local priors, and the explicit limits of the text scan. A program_status of DERIVED concerns the historical campaign route; native_bridge_status concerns receipt delivery to a participant-owned state. Decide independently. Return a single JSON object with verdict (exactly one token ACCEPTED, REVISE, or FAIL), program_status and native_bridge_status (each exactly one token DERIVED, REFUTED, or OPEN) and exactly the five standard arrays of strings proof_checks, limitations, findings, missing_assumptions, counterexamples. Put positive checks in proof_checks and scope bounds in limitations. The last three arrays are for substantive unresolved defects, missing premises for the stated claims and actual counterexamples and should be empty if none. State substantive defects candidly.'
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))
