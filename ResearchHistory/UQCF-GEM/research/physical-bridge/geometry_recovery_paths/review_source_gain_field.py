"""Challenge the inherited field comparison on a kernel direction of the chartwise P1 map."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SOURCE_GAIN_FIELD_TRACE.md": "34edd95f3546a1ed80321cc86e98ab9934feac1a",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SOURCE_GAIN_FIELD_TRACE_PLAN.md": "9bb09323f1b928efaaf519a6b21369dc003bb8b6",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/FIXED_GEOMETRY_SOURCE_GAIN.md": "ed56c3c0e724388e477d3a3b1ab46fafae36d384",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_source_gain_field.py": "ec29e45221f6288b3eb2f19650720c86afb9ccea",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/source_gain_field_certificate.json": "738912249b1230a8b53dd0a013539a6203c070e0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/fixed_geometry_source_gain_certificate.json": "e12ccc36d90dc431d0f872076015ba15550a7937",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/pruning_response.py": "937325efc761d988d3cf34eb3378035a610e0773"
}
TOPICS={"source","fine_response","three_routes","caller","scope"}
QUESTION="""Adversarially reconstruct SOURCE_GAIN_FIELD_TRACE.md against the frozen plan, actual
historical v15.56 Task 30 program, exact input provenance, script and certificate. Return JSON with
verdict ACCEPTED, REVISE or FAIL, findings, missing_assumptions, counterexamples and limitations
as arrays, native_bridge_status OPEN when native receiver delivery and physical correspondence
remain open, and proof_checks. Use ACCEPTED only for the fully scoped result with empty first three
defect arrays. proof_checks must have exactly source, fine_response, three_routes, caller, scope.
Give at least fifteen words of reasoning per key. Show what the one-leaf P1 kernel does to the
fine solve, distinguish global centering and a measured difference, and derive all three
retained contrasts. Determine whether the direction change follows without fitting, what the
legacy four-case run actually consumes, which calls are reapplied on new inputs, which chart
owns the mathematical output and whether any observed execution uses it to write to chart 12.
Check the numerical tolerance and the scalar-discrepancy versus field-level claims. Do not treat
the counting-fiber mean as unique among physically admissible maps.

Return field_checks with exactly fine_keys, coarse_keys, old_example_count (integers);
legacy_verdict (string); lost_key (raw integer address array); mean_contrasts (five exact
rational strings in order archive, low5, high5, low17, high17); coarse_contrasts and
restricted_contrasts (five exact rational strings in each); unequal_nonroot_keys (two raw
address arrays demonstrating the projective claim); receiving_chart_of_mean (integer label of
the chart on which the averaged field is actually defined); observed_chart12_consumer
(boolean for the downstream use of this averaged field)."""
if __name__=="__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    c=json.loads(Path(__file__).with_name("source_gain_field_certificate.json").read_text())
    cases=[c["cases"][n] for n in ("archive","low5","high5","low17","high17")]
    expected=dict(fine_keys=c["fine_keys"],coarse_keys=c["coarse_keys"],old_example_count=c["legacy_examples"]["cases"],
                  legacy_verdict=c["legacy_examples"]["verdict"],lost_key=c["lost_key"],
                  mean_contrasts=[a["mean_root_contrast_change"] for a in cases],
                  coarse_contrasts=[a["coarse_root_contrast_change"] for a in cases],
                  restricted_contrasts=[a["restricted_root_contrast_change"] for a in cases],
                  unequal_nonroot_keys=c["nonroot_witness_keys"],receiving_chart_of_mean=0,
                  observed_chart12_consumer=False)
    v=json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if json.dumps(v.get("field_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent field comparison or caller provenance differs")
