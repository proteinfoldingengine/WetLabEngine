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
QUESTION = """Independently challenge endogenous_junction/RESULT.md. In particular, reconstruct the (159,681,457) checkpoint, certify that the unmodified software chose its actual source and that suppressing the one bit reaches the claimed original guard. Check local tau, the global height delta, and immediate vs delayed uniqueness among both signs of incidence toggles. Explicitly examine the four shortest bypasses that retain S, and whether the controls preserve the receiver prior, parent target, downstream writer and admitted trajectory, including the difference between first return and later canonical completion. Verify the example's leaf exchange and the 24/48 ordering law, whether the unrevealed chart-rank discriminator is truly on addressed local observations, and what the persistence claim permits. Examine the earlier fixture, released N cases, one-binary rejecting controls, the exploratory provenance and the distinction between a state-forced deletion if pruning continues and autonomous physics. Look for a real counterexample and give a worked objection if warranted.

Return JSON with verdict ACCEPTED, REVISE, or FAIL. Include arrays findings, missing_assumptions, counterexamples and limitations, and a proof_checks object with worked checks for source, parent_guard, bypass, local_record, chart_order, stability and scope. For ACCEPTED without unresolved defects leave the first three arrays empty. Put positive reasoning in proof_checks, scope limitations in limitations. State actual defects with REVISE or FAIL. native_bridge_status is whether information alone autonomously establishes a physically accessible receiver distinction without supplying the dynamics, occurrence or access. Use OPEN if underived, DERIVED if established or REFUTED if impossible. This is distinct from the finite argument. Do not alter conclusions for an automated gate."""
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
