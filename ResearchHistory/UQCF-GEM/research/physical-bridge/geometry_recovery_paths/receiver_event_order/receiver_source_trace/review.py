"""Submit the passive receiver source attribution proof through the frozen project review driver."""
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
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_source_holder/RESULT.md": "4df677da84c0d77cfc8b5b3a0f83f3121762b3cc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receiver_source_trace/RESULT.md": "476610744fc00253f067803f492e6c7170357eb4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receiver_source_trace/check.py": "ccb0c5235461a77e13a0ab700222f997eb1ad282",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receiver_source_trace/stars.py": "addcc3ec878418d5c646993c5dd6d796e589c78a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receiver_source_trace/result.json": "c07f9def7987c0aa63b63fafe837a02e81f6dd8e"
}
QUESTION = """Independently review receiver_source_trace/RESULT.md. Derive or refute the exact claim for the historical four-tip writer. Start with the two competing legal withdrawals of the SAME tip by A or P while C takes neither step, and separately the unchanged control. Test the starting inaccessibility, matching of ordinary command histories, the necessary and sufficient condition under arbitrary finite pruning before eventual invocation, and the stated all-priority failure witnesses. Look for a delayed path, admissible input, ordering or local observation in the stated class that invalidates an implication. Does the first local exit from three distinguish the active sources, and when is that first possible if the priority is undisclosed as opposed to fixed and known? Does the nonrobust construction establish equality of only C or of both non-source charts, in which comparison? Check the sufficiency argument and count 288/432, the one-chart trace factorization, the two-chart baseline, the matched-grade controls (which geometry is held fixed?), and whether the alternate verifier-legal path is a proper counterexample to a stronger inference. Distinguish an encoded source identity, an actual historical writer, autonomous initiation and physical access. Report any genuine ambiguity or overclaim in its substantive context.

Return JSON with verdict ACCEPTED, REVISE or FAIL. Include arrays findings, missing_assumptions, counterexamples and limitations, and a proof_checks object giving worked checks of competing_sources, immediate_marker, unknown_order, arbitrary_delays, converse, receiver_information, alternative_path and scope. The project uses findings for unresolved substantive defects. For ACCEPTED without unresolved defects, findings, missing_assumptions and counterexamples must each be empty JSON arrays. Put worked affirmative checks in proof_checks and finite-scope qualifications in limitations. State actual defects with REVISE or FAIL. native_bridge_status specifically concerns an informational withdrawal autonomously causing a physically accessible record at the receiver without externally providing the later procedure or access. Use OPEN if underived, DERIVED if established, REFUTED if impossibility was proved. This is separate from the verdict on the finite mathematics. Do not change your conclusions for automation."""
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
