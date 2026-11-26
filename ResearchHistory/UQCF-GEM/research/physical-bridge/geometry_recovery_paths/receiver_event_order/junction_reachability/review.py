"""Submit the first binary leaf edit proof to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/historical.py": "b91756446ff6d3a50d3c63e4ce3d0862ac8c153b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/RESULT.md": "acbbf81afd405e9eee9e354f96f214d8694db2e7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/SCOPE.md": "bd21bd9e6b4c48805c8a5bb7d61317c70a894f8a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/PREPARATIONS.md": "3d3f6ae048618e021582f055561d5ed1c35d5c99",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/check.py": "772bd93b5dfe08d5cd9a935dc094392a1c5049f4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/RESULT.md": "f1a0943b0c502745197978167d2d8aa05323ca3d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/result.json": "9ca1f740d1a51e2a98b94cf1e69d47b3269323ec"
}
QUESTION = 'Independently challenge the mathematical and causal claims in junction_reachability/RESULT.md. Reconstruct the local leaf-cover argument, why the remote singleton handoff is or is not forced, the four regimes, and the distinction between the original preparation, P, the reached H and the selected F. Investigate counterexamples using ancestry, primitive moves, relabeling, and differences between exact-at-calls and exact at every edit. Verify whether a receiver role, an address, a net transfer, physical access or the occurrence of any leaf edit is necessary at each stated level. Check the outside recipient for the first edit at I and H separately. Check whether the 12/18/6 classification and the 2 vs 1900 counts are evidence at the claimed scope. Inspect the enumerator, DP, orbit comparison, independent primitives and shortest path arguments. Call out a real error even if the tests pass.\n\nGive separate worked answers to these two propositions. P_program is the finite conditional law and path counts in the stated primitive model plus the separately described outcomes of its ordered program on the 36 prepared starts. P_physical is that this initial information by itself starts a dynamics and produces an operationally accessible physical record. Explicitly state whether one entails the other. For each use DERIVED if established, REFUTED if impossible, OPEN if underived. Return JSON with program_status for P_program and native_bridge_status for P_physical. Return verdict ACCEPTED, REVISE or FAIL for the claims as bounded in the report; add findings, missing_assumptions, counterexamples, limitations, and a proof_checks object with worked checks of each proposition, the first event, exact geometry, distances/multiplicities, the two starts and reachability. If you accept with no unresolved defect leave findings, missing_assumptions and counterexamples empty, and record conditional scope in limitations. Draw your own conclusions regardless of any expected audit status.'
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
    answer = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if (answer.get("verdict"), answer.get("program_status"), answer.get("native_bridge_status")) != ("ACCEPTED", "DERIVED", "OPEN"):
        raise ValueError("Independent review requires adjudication")
