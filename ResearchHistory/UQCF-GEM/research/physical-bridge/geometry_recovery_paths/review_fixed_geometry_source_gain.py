"""Adversarial review of the fixed-work, identical-retained-source comparison."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FIXED_GEOMETRY_SOURCE_GAIN.md": "ed56c3c0e724388e477d3a3b1ab46fafae36d384",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FIXED_GEOMETRY_SOURCE_GAIN_PLAN.md": "5c32f5c6dd21157a2edae0b28c774bf6f3ec7b3c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FIXED_GEOMETRY_SOURCE_GAIN_LEMMA_PLAN.md": "db8ec236f4a9d6bc841277d6ce9f689493b5aa6d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_fixed_geometry_source_gain.py": "c8c31c46caa059a20b025ec3933498e3dbf7922e",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/fixed_geometry_source_gain_certificate.json": "e12ccc36d90dc431d0f872076015ba15550a7937",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_P1.md": "35b8259c37f8a50f1cf3446f9c07de865a1d18b7",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c"
}
TOPICS={"geometry","p1_fiber","all_editors","execution","scope"}
QUESTION="""Independently challenge the complete result in FIXED_GEOMETRY_SOURCE_GAIN.md
against the two frozen plans, original sources, code and certificate. Distinguish the
25-chart archived recovery operation from the previous 180-cut strict-covering example.
Return JSON with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions,
counterexamples and limitations, native_bridge_status OPEN if the physical numerical
consumer/receiver link remains open, and proof_checks. Accept only if the scoped results
survive the challenge; the first three defect arrays must then be empty. proof_checks
must have exactly geometry, p1_fiber, all_editors, execution, scope, each containing
at least fifteen words of reasoning. Reconstruct the signed difference of work, the full
preimage direction of the single-leaf P1 map, and the distinction between a retained
grade and a grade increment. Challenge the possibility of a new global working minimum,
a return with a second chart-0 cut and one with a different editor. Check that the
geometric proof for positive real weights and the software's rational input contract
are properly distinguished. Trace the observed object accepted by degree_candidates,
both stopping assertions and whether any candidate was returned before stopping.
Explain what it means that the source and receiver leaf grades were co-varied, and the
status of the expected singleton and caller invocation. Do not infer a gravitational wire.

Return exact_checks with the following fields and no other keys:
charts, legal (integers per preparation); matched_final_source_root (integer);
fiber_direction (two signed integer coefficients in order root, removed leaf when
the transferred grade is increased by one at fixed output);
old_a_neighbors and complement_neighbors (sorted chart arrays);
min_untouched_edges, max_absent_on_old_neighbors, squared_gap (integers);
success_pair (source and receiver grades, two integers); receiver_call ([chart,leaf]);
receiver_root_arc (two integers before,after at the original point);
exits ([original, low5, high5] using certificate strings);
candidates ([original list, low5 list, high5 value], using JSON null if the caller
stopped before returning a list); root_only_final_source_root (integer);
numeric_source_calls_before_receiver (number of original P1 aggregate calls before
the second verified native deletion); same_work_object (boolean)."""
if __name__=="__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    data=json.loads(Path(__file__).with_name("fixed_geometry_source_gain_certificate.json").read_text())
    obs=data["obstruction"]
    cases=data["cases"]
    logs=[cases[k]["trace"] for k in ("archive","low5","high5")]
    expected=dict(charts=data["charts"],legal=data["legal"],
                  matched_final_source_root=int(cases["archive"]["source_root"][1]),fiber_direction=[-1,1],
                  old_a_neighbors=obs["old_a_neighbors"],complement_neighbors=obs["complement_neighbors"],
                  min_untouched_edges=obs["untouched_minimum_edges_at_least"],
                  max_absent_on_old_neighbors=obs["max_missing_old_neighbors"],
                  squared_gap=obs["gap_to_neighbors"],success_pair=list(map(int,cases["archive"]["grades"][:2])),
                  receiver_call=logs[0]["verified"][1],receiver_root_arc=list(map(int,logs[0]["receiver_root"])),
                  exits=[l["exit"] for l in logs],candidates=[l.get("candidate_return") for l in logs],
                  root_only_final_source_root=int(cases["root_only"]["source_root"][1]),
                  numeric_source_calls_before_receiver=logs[0]["aggregate_before_second"],
                  same_work_object=logs[0]["same_work_object"])
    reply=json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if json.dumps(reply.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent numerical, control-flow or object reconstruction differs")
