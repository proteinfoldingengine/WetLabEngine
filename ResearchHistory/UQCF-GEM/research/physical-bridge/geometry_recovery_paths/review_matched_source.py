"""Challenge the paired-event theorem against the frozen sources and actual paths."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/MATCHED_SOURCE_EVENTS_PLAN.md": "b9980c8a976bff973bf4a9d52f455b6d9b97abff",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/MATCHED_SOURCE_CONTROL_PLAN.md": "5636b3d6a53a129bb63fbb155fe667b504191ae9",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/MATCHED_SOURCE_EVENTS.md": "f13a35710ef82aed74dd2bd365d8c0f98c105a5b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_matched_source_events.py": "84562f7536ed8ccdcbfa2d7ea4223386935f5290",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/matched_source_certificate.json": "1a732a051e3a4a98876daeb7ef56ad2dfad1a538",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/single_pruning_consumer/RESULT.md": "35564832c886f90978b3bcefc777b70766f1d7fd",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2"
}
TOPICS = {"geometry", "cover", "execution", "palette", "causation"}
QUESTION = """Challenge MATCHED_SOURCE_EVENTS.md against the new plans, complete proof, checker, certificate and historical producer. Return one JSON object with verdict ACCEPTED, REVISE or FAIL; arrays findings, missing_assumptions, counterexamples and limitations; native_bridge_status OPEN. Use ACCEPTED with the three defect arrays empty only if the scoped argument stands. proof_checks must have exactly geometry, cover, execution, palette, causation. Write at least fifteen words of independent reasoning under each. Test the lower-minimum two-editor obstruction even if the intermediate minimum changed. Derive the private witnesses, strict/flat possibilities, minimality with at most three active charts, all 96 separating pairs and the difference between an archived program and new R inputs. Check genuine primitive completion, projection to chart 0 on each arm, canonical order, and the relabeling and stale-target controls. A normalized execution may use charts globally and the negative original arm supplies no delivered symbol. Consider whether any whole P1 value object enters the software, as distinct from mathematical comparability of unit grades.
Also provide exact_checks. Use the following exact keys and JSON value types:
geometry_eligible_sources (integer), geometry_possible_cross_sources (array of source leaf numbers), initial_atlases (integer), unordered_pairs (integer), separating_pairs (integer), distinct_r_inputs (integer counting all unique post-cut specimens), witness_targets (two integers in cut order [3,4]), witness_receiver_leaf_counts (same order, excluding the root), first_receiver_leaf (two leaf IDs), source_root_grade_transitions (two [before,after] integer arrays), receiver_root_at_completion (two integers), initially_blank_relabelled_final_leaf_counts (two integers following the originally blank chart, now at palette slot 3), witness_in_archived_campaign (boolean for whether either of these witness post-cut specimens occurred in producer.specs()), same_target_control_equal_endpoints (boolean), native_grade_object_read (boolean), stale_arm_completed (boolean). Try to falsify both the fixed-preparation claim and the identity/physics interpretation. Credit the older no-event versus one-event result separately. Do not equate an address-dependent first edit with a count difference at that first edit; count distinction is asserted at completion.
"""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    c = json.loads(Path(__file__).with_name("matched_source_certificate.json").read_bytes())
    geo, star, arms = c["original_geometry"], c["star_domain"], c["witness"]
    swapped, neutral = c["relabeled_control"], c["same_target_control"]
    checks = dict(geometry_eligible_sources=geo["source_menu"],
                  geometry_possible_cross_sources=geo["possible_cross_editor_sources"],
                  initial_atlases=star["preparations"], unordered_pairs=star["unordered_pairs"],
                  separating_pairs=star["separating_pairs"], distinct_r_inputs=star["unique_postcut_inputs"],
                  witness_targets=[a["q"] for a in arms],
                  witness_receiver_leaf_counts=[a["end"][0].bit_count()-1 for a in arms],
                  first_receiver_leaf=[a["first_receiver_leaf"] for a in arms],
                  source_root_grade_transitions=[a["source_unit_root"] for a in arms],
                  receiver_root_at_completion=[a["final_receiver_unit_root"] for a in arms],
                  initially_blank_relabelled_final_leaf_counts=[a["end"][3].bit_count()-1 for a in swapped],
                  witness_in_archived_campaign=any(a["archived_specimen"] for a in arms),
                  same_target_control_equal_endpoints=neutral[0]["end"]==neutral[1]["end"],
                  native_grade_object_read=any(a["p1_called_in_normalizer"] for a in arms),
                  stale_arm_completed=c["stale_target_control"]["completed_receiver_write"])
    evidence = json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    if json.dumps(evidence.get("exact_checks"),sort_keys=True) != json.dumps(checks,sort_keys=True):
        raise ValueError("Independent reviewer differs on an exact paired-history check")
