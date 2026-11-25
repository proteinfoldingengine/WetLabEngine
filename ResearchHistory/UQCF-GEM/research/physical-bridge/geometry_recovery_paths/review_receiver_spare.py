"""Challenge the transient receiver write and the status of its invocation."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_SPARE_PLAN.md": "37c8ab68ebc0d49d17cac8e94b0eb53668e900b4",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_SPARE_EQUAL_ROOT_PLAN.md": "68228213ebfc7100acc3aa7bab9c5a9a617903bc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_SPARE.md": "3bc2feaaaec1a444e96471b84646fd0353948d23",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_receiver_spare.py": "020b40f922eb0b59fdbce5aa7011f8e74578fe21",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_receiver_spare.py": "52d32c136b39d3b0a96857bc9715e91e39d4eff2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_spare_certificate.json": "c7c470331483fdbd8f6a417c89128a11f21d9c71",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py": "ffd513619d182abea2b31bd90c38e12784557bf3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.25-pruning-refinement-closure/engine.py": "e9c576a2590c8e16812f1b3fa0436111e3648f1c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c"
}
TOPICS = {"fork", "read", "controls", "orbit", "scope"}
QUESTION = """Challenge the finite claim in RECEIVER_SPARE.md by reconstructing it from the original
source and frozen records. Work the immediate four-cover example and both three-cover controls.
Distinguish the native last-copy fork, the legal commutation, default priority, and the one-call
source intervention. Verify the receiver's first edits, which subsequent owner test uses them,
and whether the code mutates an input, uses a global live list or stores a permanent record.
Check the grade-blind writer against actual P1 projections and the equal-root immediate comparison,
and challenge the meaning of matching the entire post-source work in a separate pair of grade
preparations. Check the carrier rejection and the common-spare legal alternative. Check the orbit
multiplicity, independent exact path verification, count categories, the distinction between the
original archived campaign and this new run, and whether a physical scheduling/ownership law follows.
Return one JSON object with verdict ACCEPTED, REVISE or FAIL; arrays findings, missing_assumptions,
counterexamples and limitations; native_bridge_status OPEN unless independently justified;
and proof_checks with exactly the keys fork, read, controls, orbit, scope, each containing at
least fifteen words of independent worked reasoning. ACCEPTED requires empty findings,
missing_assumptions and counterexamples. Provide exact_checks with precisely the following keys:
first_leaf is the pair of positive leaf numbers first added to chart 2 at cover four, in source
actor order [1,3]. later_owner_leaf3 is the pair of actual owner chart indices for leaf 3 at
canonical placement index i=2 in those same executions. equal_root_first is the pair of
receiver ROOT grades immediately after its first local edit under the supplementary common
equal-root grade. matched_work is the six-entry post-source work vector of the distinct-preparation
control, ordered 01,02,03,12,13,23. default_source is the chart index deleting 4 in the original
one-call run. paired is the total number of paired comparisons across the orbit. first_diff and
later_diff are respectively the total with different first edits and the total with equal first
edits but different subsequent receiver streams. native_pruning_exits is the number of admissible
v16.26 deletion atoms immediately after either marked source on the prepared four-cover example.
Compare the strongest plausible alternatives; do not reject a finite conditional result merely
because its physical-bridge status remains open."""
if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    reply = json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    cert = json.loads(Path(__file__).with_name("receiver_spare_certificate.json").read_bytes())
    named = cert["named"]
    arms = [r for r in named["primary"] if r["nuisance"] == 3]
    equal = [r for r in named["grade_controls"] if r["label"] == "equal_root"]
    matched = [r for r in named["grade_controls"] if r["label"] == "matched"]
    expected = dict(first_leaf=[r["receiver_edits"][0] for r in arms],
                    later_owner_leaf3=[r["trace"]["owner_reads"][2]["owners"][2] for r in arms],
                    equal_root_first=[r["first_receiver_edit"]["receiver_p1"][0] for r in equal],
                    matched_work=matched[0]["post"]["work"], default_source=named["one_call"][0]["actor"],
                    paired=cert["paired_histories"], first_diff=sum(r["first_differs"] for r in cert["counts"]),
                    later_diff=sum(r["later_differs"] for r in cert["counts"]), native_pruning_exits=0)
    if json.dumps(reply.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Independent review numerical reconstruction differs")
