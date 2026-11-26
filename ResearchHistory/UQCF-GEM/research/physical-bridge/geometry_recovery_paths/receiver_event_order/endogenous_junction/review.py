"""Submit the endogenous junction withdrawal result through the frozen project review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/source_trigger_and_receiver/RESULT.md": "f53fe7b5f107c7f354bca432895be99196fbdd2b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/RESULT.md": "acbbf81afd405e9eee9e354f96f214d8694db2e7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/check.py": "38684f6343a8b64adb837e1aeda78a718ab2f353",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/intervention.py": "de61f3dfa329c4d3e2eb749b89359277176ddd86",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/historical.py": "b91756446ff6d3a50d3c63e4ce3d0862ac8c153b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/result.json": "59aa3de5f1654891050126ce451daa54522e550e"
}
QUESTION = """Conduct an independent scientific re-examination of endogenous_junction/RESULT.md and its source. Check the entire finite construction, shortest bypass classification, matched receiver priors, reachability, one-binary controls, and one- vs two-call boundaries. A prior response conflated two levels of claim. Reconstruct the evidence yourself and give a separate worked verdict for each proposition, retaining any disagreement with the author:

1. P_program: starting the original ordered normalizer on the stated admitted input and target results, without intervention, in the indexed junction withdrawal and later source-sensitive local receiver record. Specify evidence, premises and the role of the matched alternatives.
2. P_physical: the initial informational structure alone suffices to initiate the dynamics, fix the operative order, and necessitate a record accessible to a physical receiver. Determine independently which hypotheses of this proposition, if any, have been derived, assumed, disproved or not addressed. Provide the theorem, original executable evidence, or missing implication for each. State whether P_program implies P_physical and give your reasoning. The distinction is operational, not terminological.

Also independently recompute the chronological order of clearance, parent withdrawal, binary re-read and exchange for (409,681,79). Specify which ranks are GLOBAL holders of S at the positive and alternate child reads, which LOCAL ranks the binary canonicalization targets, and which physical chart receives each leaf. Check the local vs global increment, the 24/48 split, the two addressed record sets, and persistence under ordinary withdrawals. State all real substantive objections.

Return JSON with verdict ACCEPTED, REVISE or FAIL on the stated scientific claims, findings, missing_assumptions, counterexamples and limitations arrays, and a proof_checks object giving worked checks including program, physical, chronology, gate, bypass, receiver and scope. For an ACCEPTED finite proof with no unresolved defects leave findings, missing_assumptions and counterexamples empty. Put conditional scope in limitations. Add program_status and native_bridge_status as DIFFERENT top-level fields. program_status applies only to P_program; native_bridge_status applies only to P_physical exactly as defined in item 2. In each field use DERIVED iff the specific proposition is established, REFUTED iff impossible, or OPEN if underived. Check that each field agrees with its own worked explanation. Do not change your scientific conclusions to meet the automation's expectations."""
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
    verdict = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if verdict.get("verdict") != "ACCEPTED" or verdict.get("native_bridge_status") != "OPEN":
        raise ValueError("Review requires scientific adjudication")
