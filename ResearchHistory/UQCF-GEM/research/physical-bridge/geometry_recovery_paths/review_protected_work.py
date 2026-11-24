"""Challenge the conditional geometric theorem and the scope of the bystander's readout."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PROTECTED_WORK_PLAN.md": "f64f523b63f126ed2759594d3c48ce0e13325f36",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PROTECTED_WORK_EQUAL_SOURCE_PLAN.md": "ae98a8f3bd830d5809a7f8bf56fd583bc2e2e03c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/PROTECTED_WORK.md": "1df8c0b82e0212a2a5a3a23656956dce72f8cc28",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_protected_work.py": "51af9fc7b22d964a8d6927d5ccfc70dfa28cc453",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_protected_work.py": "84f1fcdc3a0d2f54a5eb624fd5506d43c4fdc825",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/protected_work_certificate.json": "17d577338d5b27617bddc91b02caa1770a15b4c5",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.25-pruning-refinement-closure/engine.py": "e9c576a2590c8e16812f1b3fa0436111e3648f1c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.33-consistency-quotient-kernel/verifier.py": "c6cf3143423da17c09bbdbbc2eab4800c91acc24"
}
TOPICS = {"fork", "geometry", "enumeration", "witness", "scope"}
QUESTION = """Adversarially challenge the complete argument in PROTECTED_WORK.md. Reconstruct the
two-cut classification for a general finite rooted cover. Check the characterization of terminal
chart masks, and whether actual third-chart P1 information is forced. For a unit-weight star
rederive both directions of the terminal work theorem, including an alternating simple incidence
path with multiholder leaves, the minimum chart count for recovering chart loads, and the
stronger all-stages statement only in the declared three-potentially-active, one-blank domain.
Distinguish equality under freely varying histories from the paired same-continuation calculation.
Independently derive the analytic count and the worked triangle collision. Test the equal-source
six-leaf example, actual cover excursions and positivity/separation of pair work as a metric,
and the difference between two sites competing for one address and one site choosing two leaves.
Check whether inspected v16.25 or v16.33 automatically schedules a cover-preserving deletion at
the old same-chart fork and whether allowing additions can undo the new source events. A work
entry involving a potential source is a relational observable. Challenge any stronger inference
of a newly stored singleton receiver record, an autonomous physical selection or gravity.
Return one JSON object with verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions,
counterexamples, limitations, native_bridge_status OPEN unless independently justified, and
proof_checks keyed fork, geometry, enumeration, witness, scope. Provide at least fifteen words of
independent worked reasoning under each key. ACCEPTED requires empty findings, missing_assumptions
and counterexamples. Give exact_checks with the following keys. all_events_pairs is the count
of unordered distinct same-start atom pairs in the entire designated-blank census. exclusive,
disjoint_work and terminal_collision are the counts for last-copy pairs, all-stages disjoint
geometries, and overlapping terminal work respectively. triangle_collision is the six work
values in order 01,02,03,12,13,23 of the two displayed terminal states. six_work gives two
integers at the fixed chart pair 2,1 in source actor order [1,3]. six_source_root is the common
[before,after] pair of source root grades in the six-leaf example. six_receiver_p1 is the entire
fixed local P1 value list at chart 2. six_reachable_cover_sizes contains the sorted distinct
sizes reachable after either six-leaf cut. same_site_two_cut_join and native_pruning_can_erase_last_owner
are booleans about the original two distinct same-chart cuts and about deletion-only
erasure of a protected last copy, respectively. Do not turn a negative physical status into a
rejection of a correctly scoped finite theorem."""
if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    reply = json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    cert = json.loads(Path(__file__).with_name("protected_work_certificate.json").read_bytes())
    n = cert["domain"]
    six = cert["six_leaf_equal_source"]
    triangle = cert["triangle"]
    sets = [{tuple(s["work"]) for s in a["states"] if s["terminal"]} for a in triangle["arms"]]
    expected = dict(all_events_pairs=n["event_pairs"], exclusive=n["conflicts"], disjoint_work=n["disconnected"],
                    terminal_collision=n["connected"], triangle_collision=list(min(sets[0] & sets[1])),
                    six_work=[a["states"][0]["work"][six["pair_index"]] for a in six["arms"]],
                    six_source_root=six["arms"][0]["source_root"], six_receiver_p1=six["arms"][0]["states"][0]["receiver_p1"],
                    six_reachable_cover_sizes=sorted({s["h"] for s in six["arms"][0]["states"]}),
                    same_site_two_cut_join=True, native_pruning_can_erase_last_owner=False)
    if json.dumps(reply.get("exact_checks"),sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Independent reconstruction differs from frozen checks")
