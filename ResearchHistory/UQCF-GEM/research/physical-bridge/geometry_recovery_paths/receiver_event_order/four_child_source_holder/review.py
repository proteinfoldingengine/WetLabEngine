"""Submit the source-holder and next-edit proof through the frozen project review driver."""
from hashlib import sha1
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
DRIVER = ROOT / "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/v1686_recombination_trace/review.py"
DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_source_holder/RESULT.md": "4df677da84c0d77cfc8b5b3a0f83f3121762b3cc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_source_holder/check.py": "5db2fbab992a55b7ca4105a28867001c96efb74b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_source_holder/source_star.py": "b4db512caa3b7d057eb1823b58946d4016f76079",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_source_holder/result.json": "526c3da661b3b3501f8bf19d1b08056601c29703",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py": "b18f52109ccff9c7dc77542d3b8f3e5d5989102a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_event_order/four_child_retained_grade_fork/RESULT.md": "2a8487e3ac1542954de3724299398315116eef9b"
}
QUESTION = """Independently challenge the complete next-move classification in four_child_source_holder/RESULT.md, including
the iff direction, a possible third-chart evasion regardless of its tip membership, and the assumed move alphabet.
Derive the two addressed output sets for the swapped grades using the historical P1 push. Can different choices of tip
across arms erase the distinction? Distinguish acquisition of the hidden grade, attribution to this event versus the
null preparation, autonomous initiation, stability after later moves, and physical access. Check the actual original
three-child caller and its idle and reversing controls. Verify the full-cover-jump lemma for other charts' command catalogues
and whether the designated later receiver must be the chart singled out immediately. Read the four-child complementary
algorithm: why is the original source undone in the eight cases? Challenge the exact-cover alternate paths, exhaustive
catalogues, shortest-path lower bound, side case with two forward restorations, and interpretation of child-order controls.
Check whether all claims are appropriately limited to the finite inherited inputs and specified interventions.

Return JSON with verdict ACCEPTED, REVISE or FAIL. Include arrays findings, missing_assumptions, counterexamples and
limitations, and a proof_checks object with worked entries classification, grades, caller, source_holder, paths, order and
scope. The project uses findings EXCLUSIVELY for unresolved substantive defects. Put affirmative or explanatory
observations in proof_checks. For an ACCEPTED result without unresolved defects, findings, missing_assumptions and
counterexamples must each be an empty JSON list. Any actual objection must still be stated with REVISE or FAIL.
native_bridge_status refers specifically to a source autonomously
necessitating a physically accessible receiver record without supplying an update occurrence or excluding undo/rest.
Use OPEN if underived, DERIVED if established, or REFUTED if impossibility was proved. This is separate from verdict on
the finite mathematics. Calculate for yourself the next-edit counts and sample P1 values. Do not modify your scientific
conclusions to meet automation requirements."""
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
