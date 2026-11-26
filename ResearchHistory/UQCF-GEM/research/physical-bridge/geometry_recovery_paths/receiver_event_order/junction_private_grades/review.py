"""Submit the private-grade acquisition proof to the pinned independent review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/SCOPE.md": "60faa83fa2b3760783707f372166af89b37bfb65",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/WORK_TEST.md": "c27e64d3832b25eb768b8396a495b0c4a481da66",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/RESULT.md": "5539100eeaedd7f1376af2aa8315ed1d643a58ef",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/check.py": "71dbfe729699add3571de33e77a85519dc8b46ba",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/verify.py": "3b9d22daba66ce5d0fcf4f72b485812c14a6c725",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/result.json": "6441240ba079d8998c5c2d30f0ae0c78ab6aad9d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_private_grades/verification.json": "bddfa8c3afad62fdab1ecffefa60ea0f2735a3be",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/junction_reachability/RESULT.md": "f1a0943b0c502745197978167d2d8aa05323ca3d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/endogenous_junction/historical.py": "b91756446ff6d3a50d3c63e4ce3d0862ac8c153b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b"
}
QUESTION = "Independently adjudicate junction_private_grades/RESULT.md as a bounded mathematical result. Challenge the two-state assertion for all single-incidence edits and the two band counts. Derive what a retained P1 does and does not determine, the matched eight preparations, independence of peers' priors and the full initial works, the signed change rule, the bare-S inversion and the unlabeled-leaf counterexample. Check the untouched ordered calls, including the meaning of 36/36, 33/36, and a return to the starting state. Distinguish a source-private retained contrast from a grade change only at a private fine address, a new source event, a compulsory invocation, and physical access. Verify the proofs or produce a concrete counterexample. The documents include a ledger generator, independent verifier and their output. Treat the preregistered guesses as hypotheses. Return a JSON object with verdict ACCEPTED, REVISE or FAIL; use arrays findings, missing_assumptions, counterexamples, limitations, and a proof_checks object with your own worked checks. On genuine acceptance keep findings, missing_assumptions and counterexamples empty, and put scope conditions and non-defects in limitations. For the conditional finite mathematical proposition report program_status DERIVED, REFUTED or OPEN. For the separate proposition that the state starts its own dynamics and the resulting record is operationally accessible physically report native_bridge_status DERIVED, REFUTED or OPEN. Judge these propositions independently."
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
