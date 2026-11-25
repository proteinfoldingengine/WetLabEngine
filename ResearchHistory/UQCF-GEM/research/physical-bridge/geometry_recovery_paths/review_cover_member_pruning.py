"""Challenge the minimum-cover membership argument and all three route controls."""
from pathlib import Path
import json
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_MEMBER_PRUNING_PLAN.md": "0dbbea57ef23fb65cc163d068983162a9995d8eb",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_MEMBER_ROUTE_CONTROL.md": "37dad77f185a176de9e070a066104b7efacf33dc",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_MEMBER_PRUNING.md": "b2877fe8f608f5c96ccf838a1d84e88fa4a353bd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_cover_member_pruning.py": "ace1c7e2d6c768a7072844a7a80a0236c620bf32",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_cover_member_pruning.py": "c6fa23826ca5326c2240d67dc08602123cd51e61",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/cover_member_certificate.json": "b4b5290e2ca51ea6370b0f7b17d77d33a0dda730",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/producer.py": "ffd513619d182abea2b31bd90c38e12784557bf3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.43-star-fiber-classification/verifier.py": "80a47f10231a086af161c4999c582fa038d064c7",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/construct.py": "284b8cc9305c14f3ff6f3693c67a2c61ea00e93e",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80"
}
TOPICS = {"terminal", "receiver", "census", "routes", "scope"}
QUESTION = """Independently challenge the frozen report COVER_MEMBER_PRUNING.md. Reconstruct the
terminal assignments under maximal fixed-cover and unrestricted native pruning for an arbitrary
finite star. Check necessity and sufficiency, minimal cover versus inclusion-minimal cover, and
what happens when chart names are permuted. Test the equal-scalar witness, where local membership
is stored, which program inputs and call boundaries are supplied, and which mask is actually read
by the old donor loop. Distinguish the first singleton state from the end of either full normalizer
and a possible lasting physical memory. Verify the two-cut join under both native orders. Try to
refute the 108 analytical count, including possible minimum covers excluding the source. Distinguish
counts of pairs from counts of eligible receivers. Compare the three same-endpoint routes of the
prior witness and the two different historical implementations. The 23 edits apply only to that
prior flat witness. Both scope and non-forcing are important. Return exactly one JSON object with
verdict ACCEPTED, REVISE or FAIL, arrays findings, missing_assumptions, counterexamples, limitations,
native_bridge_status OPEN unless derived, and proof_checks with keys terminal, receiver, census,
routes, scope. Give at least fifteen words of independent reasoning per key. ACCEPTED requires empty
findings, missing_assumptions and counterexamples. Preserve specific substantive objections.
Return exact_checks for the following keys. source_cover_after and source_root_after are lists of
two integers in cut order [1,2] for the new witness. receiver_leaves_after_cleanup is a two-element
list of lists of leaf IDs excluding root for those two original chart-order rows. archived_rows
gives their zero-based row IDs. pairs_separating, equal_cover_separating, receiver_incidences,
bare_forced_receiver_incidences and chart_leaf_relabelings are integer counts. route_edits and
route_minimum_work are three integers each, ordered [old v16.53 expand-and-contract, v16.39
constructor, direct seven-edit control] for the PRIOR same-endpoint witness. writer_reads_p1 is
a boolean for consumption of the numeric P1 grade object in the named historical writers."""
if __name__ == "__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    verdict=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    c=json.loads(Path(__file__).with_name("cover_member_certificate.json").read_bytes())
    a,b=c["witness"]
    n=c["counts"]
    routes=[c["same_endpoint_routes"][k] for k in ("v16.53","v16.39","direct")]
    expected=dict(source_cover_after=[z["source_height"][-1] for z in (a,b)],
                  source_root_after=[z["unit_roots_source_before_after_receiver_before_cleanup"][1] for z in (a,b)],
                  receiver_leaves_after_cleanup=[[v for v in range(1,5) if z["receiver_cleanup"] & (1<<v)] for z in (a,b)],
                  archived_rows=[z["star_record"]["archive_row"] for z in (a,b)],
                  pairs_separating=n["pairs_separating_empty_nonempty"],equal_cover_separating=n["equal_cover_separating"],
                  receiver_incidences=n["pair_receiver_incidences"],bare_forced_receiver_incidences=n["bare_forced_pair_receivers"],
                  chart_leaf_relabelings=n["relabelings"],route_edits=[len(z["path"])-1 for z in routes],
                  route_minimum_work=[z["minimum_work"] for z in routes],writer_reads_p1=False)
    if json.dumps(verdict.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent reconstruction disagrees on an exact reported check")
