"""Challenge the four-chart identity, calibrated receiver sufficiency and interventional controls."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_PRIOR_REPAIR.md": "ebe4c4c6e541187a52439bf86d97827873200ab2",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_PRIOR_REPAIR_PLAN.md": "585bb520e5408ced729719a1e63c09c35844af5c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECEIVER_PRIOR_FACTORIAL_PLAN.md": "5725f5f4eba6fd383f36b52c2677ae0e5ce93e1c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_receiver_prior_repair.py": "8017b7568d33e84b183b35b8a020737f472bd647",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/receiver_prior_certificate.json": "ba1265538882c44af8d46b7d01cae81b92da52d6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FIXED_GEOMETRY_SOURCE_GAIN.md": "ed56c3c0e724388e477d3a3b1ab46fafae36d384",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SOURCE_GAIN_FIELD_TRACE.md": "34edd95f3546a1ed80321cc86e98ab9934feac1a",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/pruning_response.py": "937325efc761d988d3cf34eb3378035a610e0773"
}
TOPICS={"four_point","prior_vs_acquisition","arbitrary_grades","factorial","field"}
QUESTION="""Challenge RECEIVER_PRIOR_REPAIR.md on the stated historical fixture against the
frozen plans, exact algorithm, certificates, historical caller and P1/mean implementations.
Reject or request revision if the scoped statements fail. Return JSON with verdict ACCEPTED,
REVISE or FAIL; arrays findings, missing_assumptions, counterexamples, limitations; and
native_bridge_status OPEN if delivery remains open. ACCEPTED requires the first three defect
arrays empty. proof_checks must have exactly four_point, prior_vs_acquisition,
arbitrary_grades, factorial, field. Write at least 15 words of actual reasoning per key.
In four_point derive the signed coefficient from cut indicators, eliminate all non-B terms
except T and explain which calibration belongs to whom. In arbitrary_grades show how both
grades are forced even for s²=14 or above the old circle and ordinary leaves of grade two.
Reconstruct the degree completion of each candidate star and show why the B editor can delete
only U. Verify the positive integer compensation signs and the equal-post-work control, as
well as the difference between a changed source field, writer consumption and receiver
prediction before a specified event. Try an uncalibrated receiver collision.
Return exact_checks with these precise keys: reference_quartet (ordered integer array),
quartet_count, reference_contrast, receiver_terms (integer count of nonzero B terms for
the reference quartet), eligible_next_per_case, calibrated_cases (integers);
passing_calls (the complete array of receiver repairs at archive);
factorial_executions (four arrays of actual repairs, in grade order [2,2],[2,1],[1,2],[1,1]);
factorial_balances (four integers for D in that order); same_post_work_at_s2 (boolean);
source_potential_change_on_swap (signed integer for potential at 160 minus potential at 161);
same_prior_at_B_on_swap (boolean); writer_uses_mean (boolean);
uncalibrated_true_vs_stale (two integers for the source square computed with actual vs
historically substituted geometry). Explicitly note that the known prior topology and the
fixed starting geometry and specified addressed event condition the theorem. Its numerical
representation alone does not grant physical access or execute a writer."""
if __name__=="__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    c=json.loads(Path(__file__).with_name("receiver_prior_certificate.json").read_text())
    cases=c["cases"]
    a=cases["archive"]
    four=[cases[k] for k in ("archive","factor_2_1","factor_1_2","factor_1_1")]
    control=cases["uncalibrated"]
    expected=dict(reference_quartet=c["reference_quartet"],quartet_count=c["quartet_count"],
                  reference_contrast=int(c["reference_contrast"]),receiver_terms=len(c["reference_receiver_terms"]),
                  eligible_next_per_case=c["legal"],calibrated_cases=sum(v["initial_work_matches"] for v in cases.values()),
                  passing_calls=a["actual"],factorial_executions=[x["actual"] for x in four],
                  factorial_balances=[int(v["ordinary_receiver_balance"]) for v in four],
                  same_post_work_at_s2=(a["post_work_sha256"]==four[1]["post_work_sha256"]),
                  source_potential_change_on_swap=int(c["source_mean_swap_contrast_change"]),
                  same_prior_at_B_on_swap=(a["receiver_prior_sha256"]==cases["swapped"]["receiver_prior_sha256"]),
                  writer_uses_mean=bool(a["mean_calls_in_writer"]),
                  uncalibrated_true_vs_stale=list(map(int,[control["source_square"],control["incorrect_if_old_geometry_substituted"]])))
    review=json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if json.dumps(review.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent reconstruction differs from the pre-event receiver tests")
