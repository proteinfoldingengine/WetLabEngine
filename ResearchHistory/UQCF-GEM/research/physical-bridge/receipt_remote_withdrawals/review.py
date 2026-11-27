"""Adjudicate the withdrawal-language result via the existing pinned model driver."""
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
driver.DOCUMENTS = {'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/RESULT.md': '850ea88335e8fac7f67346de373f26120b6ef5d9',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/SCOPE.md': 'a4d373baab67ed834fafd4e79d742250a5c24915',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/replay.py': 'c27f3ca192c7d797177fa7cf5f6d706f083a8b3d',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/results.json': '072df9d75a74e7526f4cf011a431fcbfe0725944',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/verification.json': '551dac81982f6ad3a4ca60dbf8efc3c6160ecb3e',
 'ResearchHistory/UQCF-GEM/research/physical-bridge/receipt_remote_withdrawals/verify.py': 'a79c6a4d47d9adb5216a987d67b8f545bf0228e8',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py': 'c10ac57f988a439144e21898bd2b33ece0838a9b',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py': '91cd1e507e955683e744fbdbb0745cac19d66cb3',
 'review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/completion/evidence/historical-producer.log': '84ac51dc629da88adf84549a3c3a139f612c3cc6'}
driver.QUESTION = "Try to refute the iff theorem about a different chart's entire existential projected withdrawal language under arbitrary interleaving. Inspect the proof for a proper covered subtree, the internal-site case and the exact words lost. Check the four genuine receipts against both orderings. Distinguish computed counterfactuals, centrally saved fields, and participant retention. Check domains, event identity and global projection verification. No new physical or delivery mechanism is claimed. Return JSON with verdict ACCEPTED, REVISE, or FAIL; program_status and native_bridge_status independently DERIVED, REFUTED, or OPEN; and five string arrays proof_checks, limitations, findings, missing_assumptions, counterexamples. Report genuine defects candidly and use empty arrays for absent defects."
driver.main()
if sys.argv[1] == "audit":
    answer = json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if not answer.get("proof_checks") or not answer.get("limitations"):
        raise ValueError("The independent response lacks reasoning or scope")
    print("Argument status:", answer.get("program_status"), "physical status:", answer.get("native_bridge_status"))

    if answer.get("verdict") != "ACCEPTED" or answer.get("program_status") != "DERIVED" or answer.get("native_bridge_status") != "OPEN":
        raise ValueError("Independent review requires adjudication")
