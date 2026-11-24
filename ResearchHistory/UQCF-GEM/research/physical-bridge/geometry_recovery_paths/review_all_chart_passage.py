"""Submit the frozen all-chart passage and counterexample for independent challenge."""
from pathlib import Path
import json
import sys

from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ALL_CHART_PASSAGE_PLAN.md": "d9ff3a59246a5559a61257278675549c000d9639",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ALL_CHART_DELETION_CONTROL.md": "7a2b094869a83f00858fc26fcd82f439a00a467d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/ALL_CHART_PASSAGE.md": "300de2505be94e0cf2d4f1131a2828ef8f5eb9a6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_all_chart_passage.py": "dad3bf48b7605fc11c0d0e4ad071284ef652fd9b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_all_chart_passage.py": "aa64eec483455893b6194411cea2170c7d2c1be5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/all_chart_certificate.json": "b5daf87da96bcb3d719330bb7aeeb44fff7b227f",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2"
}
TOPICS = {"source", "passage", "geometry", "control", "ownership"}
QUESTION = """Independently challenge ALL_CHART_PASSAGE.md against the complete supplied sources,
executed data and controls. Derive why both cuts are legal, why equal unit source transfers give
different covering targets, and why the traced local edit survives every chart and leaf renaming.
Distinguish the full state of a single chart, simultaneous full occupancy, collective zero work,
a deletion from a full pre-state at a given chart, and durable local memory. Prove or refute the
6 min(weight) bound and test its sharpness for this witness. Check the alternative path step
by step, compare its restrictions to the actual branch, and look for overclaimed necessity.
Check q=1 separately. Challenge the transferred object, the effective identity tests, the scope
of the exhaustive comparison and independence of its methods. A global history, a source event,
a supplied normalizer invocation and a chart-local observation are distinct.
Return one JSON object containing verdict (ACCEPTED, REVISE or FAIL), findings, missing_assumptions,
counterexamples, limitations, native_bridge_status and proof_checks. The four issue fields are
arrays. ACCEPTED requires empty findings, missing_assumptions and counterexamples. Keep native
physical bridge OPEN unless demonstrated. Give at least fifteen words of worked reasoning for
each of the exact proof_checks keys source, passage, geometry, control, ownership.
Also return exact_checks as an object with cut order [leaf 3,leaf 4]. Its exact keys are
cover (two integers), completed_writer_edits (two integers), number_of_charts_deleting_from_full
(two integers), minimum_total_unit_work (two integers), swapped_blank_final_leaf_counts
(two integers excluding the root), alternate_path_edits (one integer),
relabellings (number of chart-permutation/leaf-permutation pairs of the named witness, one integer),
separating_source_pairs (out of 2646, one integer), writer_reads_p1 (boolean).
Treat documented limitations as limitations when the scoped theorem holds. Preserve objections
in a REVISE or FAIL response if any substantive error is found."""
if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    result = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    cert = json.loads(Path(__file__).with_name("all_chart_certificate.json").read_bytes())
    arms = cert["witness"]
    expected = dict(cover=[a["q"] for a in arms], completed_writer_edits=[a["steps"] for a in arms],
                    number_of_charts_deleting_from_full=[len({x[1] for x in a["full_chart_deletions"]}) for a in arms],
                    minimum_total_unit_work=[a["minimum_total_pair_work"] for a in arms],
                    swapped_blank_final_leaf_counts=[m.bit_count()-1 for m in cert["swapped_blank_end_masks"]],
                    alternate_path_edits=len(cert["exact_cover_two_detour"])-1,
                    relabellings=cert["relabelings"], separating_source_pairs=cert["separating_pairs"],
                    writer_reads_p1=any(a["p1_calls_in_writer"] for a in arms))
    if json.dumps(result.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Independent review differs on an exact scope check")
