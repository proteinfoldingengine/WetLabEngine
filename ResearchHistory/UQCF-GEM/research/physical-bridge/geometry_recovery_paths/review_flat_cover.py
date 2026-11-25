"""Independent whole-argument review of the source-cut and next-chart experiment."""
import json
from pathlib import Path
import sys

from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FLAT_COVER_NEXT_EDIT_PLAN.md": "2ac13493aeaca7974e93cd26f64e53e337709e63",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FLAT_COVER_NEXT_EDIT.md": "41ab8bfe37f0ef6a34ec0245bd23f7b1ad169220",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_flat_cover.py": "40955cd8b68a4ea8cd8798f3386750f6cda1d3a5",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_flat_cover.py": "a5fdc712a080a893731955c04afccc786f97104f",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/flat_cover_certificate.json": "c3ba80f43032bb450fa35814a8ea8639de7fe0e0",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py": "ffd513619d182abea2b31bd90c38e12784557bf3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/graph_producer.py": "6c8eca570cda82b64c0d06775672f33977be430a",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b"
}
TOPICS = {"next_chart", "controller", "enumeration", "erasures", "scope"}
QUESTION = """Review FLAT_COVER_NEXT_EDIT.md as a skeptical mathematician. Independently derive the
legal next edit identities from the four supports on each arm, the uniqueness of the next chart,
the freedom to order its two leaves, and the status of maximality. Identify what breaks the prior
symmetry. Compare the original graph's possibilities with the unmodified deterministic historical
writer actually called from a common pre-cut input. Inspect the original source and distinguish
choice of H in the controller from the time at which the visible minimum cover becomes unique.
Recover the positional counts over all distinct placements analytically. Check both independent
erasures, including reversing to the prior at fixed cover and the unrestricted double source cut.
Challenge any inference of an autonomous source choice, ongoing physical restriction, or physical
gravity. Name any erroneous counts, erroneous causal statements, missing assumption or counterexample.
Return precisely one JSON object. Supply verdict ACCEPTED, REVISE or FAIL, arrays findings,
missing_assumptions, counterexamples and limitations, native_bridge_status OPEN unless actually
derived, and proof_checks keyed next_chart, controller, enumeration, erasures, scope. Supply at least
fifteen words of worked reasoning in each proof check. ACCEPTED requires empty findings,
missing_assumptions and counterexamples. Include exact_checks. named_next_charts lists the two
required destination chart IDs in named source-leaf order 2,3. named_first_three_writes contains
the three [chart,leaf] pairs actually executed by original writer row 1349. distinct_starts is
the number of distinct chart-labeled/leaf-labeled preparations after ruling out orbit duplicates.
source_position_all gives four counts [first,second,last,absent] among those distinct starts.
source_followed_by_receiver_original is the count in the original fixed-blank-0/source-2 class.
opposite_flat_all counts actual source-cut positions at which the other marked source cut is still
legal while also preserving scalar cover. opposite_bound_all counts such positions where that
other cut preserves the bound cover. exact_additions_per_named_post is the number of legal
single-membership additions preserving the profile after either named source cut (one integer).
double_cut_cover and reverse_to_prior_cover are scalar cover sizes of the two joins."""
if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    reply = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    cert = json.loads(Path(__file__).with_name("flat_cover_certificate.json").read_bytes())
    stats = cert["all_labels"]
    named = cert["named"]
    expected = dict(named_next_charts=[a["receiver"] for a in named["arms"]],
                    named_first_three_writes=[[s["chart"], s["leaf"]] for s in named["writer"]["cleanup"]],
                    distinct_starts=stats["starts"],
                    source_position_all=[stats["source_" + label] for label in ("first", "second", "last", "absent")],
                    source_followed_by_receiver_original=cert["original"]["source_followed_by_receiver"],
                    opposite_flat_all=stats["opposite_flat"], opposite_bound_all=stats["opposite_keeps_bound"],
                    exact_additions_per_named_post=len(named["arms"][0]["exact_additions"]),
                    double_cut_cover=3, reverse_to_prior_cover=2)
    if json.dumps(reply.get("exact_checks"), sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Independent exact reconstruction disagrees with the certificate")

