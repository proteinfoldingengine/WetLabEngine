"""Submit the live receiver and continuous-caller proof through the frozen project review driver."""
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
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/receiver_source_trace/RESULT.md": "476610744fc00253f067803f492e6c7170357eb4",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py": "48f132d141167d9cd85ff79ec41720b5dca4f8bb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/source_trigger_and_receiver/check.py": "eb5d84c8d8c0936c5da1930602a287212ef114a8",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/source_trigger_and_receiver/live.py": "474826d1e4e5d3788a7f290a9f31e6d290f0210f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/source_trigger_and_receiver/RESULT.md": "f53fe7b5f107c7f354bca432895be99196fbdd2b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/source_trigger_and_receiver/result.json": "01ecc5003d91ce2794ffc778dc07ca7e62da61a6"
}
QUESTION = """Independently challenge the finite continuing-caller and nested matched-intervention claims in source_trigger_and_receiver/RESULT.md. Reconstruct the nine-vertex fixture, the root and two child targets, absence of an event flag, and the first C edit and unit P1 in each sample. Distinguish the five intervened or control histories from an endogenous choice of source event. Examine whether a test hook silently supplies a receiver, new launch, plan, or a write other than the actor bit. Check how a naturally invoked recursive call samples the remaining labels, the exact chart-order criterion and the all-orders no-event and double-withdrawal controls. Challenge the scope of the 132 continuous-run observations including temporal order, the claimed orbit of 72, the flat no-spare proof for any k and loss of identity at fixed target. Check the nested N cohort, frozen M diagnostic, the independent path/atom verifiers and what the v16.26 and v16.27 consumers actually do. Prefer actual counterexamples to impressions. Is physical or autonomously initiated delivery established? Are any conclusions stronger than the stated software boundary?

Return JSON with verdict ACCEPTED, REVISE, or FAIL. Include arrays findings, missing_assumptions, counterexamples and limitations, plus proof_checks with actual arguments for nested_pair, live_hook, ordering, controls, continuous_flat, spare_lemma and scope. For ACCEPTED without unresolved defects the first three arrays must be empty. Record positive checks in proof_checks and honest conditions in limitations. Report substantive errors with REVISE or FAIL and do not alter your scientific conclusions for any gate. native_bridge_status is whether a native informational event autonomously entails a physically accessible receiver consequence without supplying the dynamics, occurrence or access. Use OPEN if underived, DERIVED if established or REFUTED if impossible. That label is independent of the finite proof verdict."""
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
