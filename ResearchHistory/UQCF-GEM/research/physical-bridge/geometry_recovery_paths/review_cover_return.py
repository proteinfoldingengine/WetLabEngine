"""Adversarial review of the released address, receiver, timing and exact bypass cost."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_RETURN_WRITE_PLAN.md": "9ebcea4f55b773ce3d74bf32ae7b058a63a24819",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_RETURN_BUDGET_PLAN.md": "6ed00bf6c255c6f4e7e2cf763c571fbfcd7d660b",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/COVER_RETURN_WRITE.md": "63e09be0aa203bd2313f6c136246476d80022735",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_cover_return.py": "188f74f84dd95f063f1465f7cf0f724bb5b64eef",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_cover_return.py": "9354ebde4fe4c5cf03e92226c5a40dd10f1e4c98",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/cover_return_budget.py": "fd9002b32288b1762c7ad4ed3cbf0c8a1f021e4c",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/verify_cover_return_budget.py": "4b180415fbd74d35a6606d77536c38efbadeee5d",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/cover_return_certificate.json": "9c8dd30736b682269d8d3741f734d5e5e0121a46",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/model.py": "a4a6407990c36084ab3b6e8e7da9022a4f9d63a8",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py": "ab3541cba29d5e1ebd4fe6c56128daf020c1a81f",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/universe.py": "517ab8e20bc364c106e9a9b3ffaac23dc3a3b258",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.33-consistency-quotient-kernel/verifier.py": "c6cf3143423da17c09bbdbbc2eab4800c91acc24"
}
TOPICS = {"trigger", "uniqueness", "budget", "ordering", "scope"}
QUESTION = """Independently challenge COVER_RETURN_WRITE.md from the supplied native operations,
proof, finite universe definitions and receipts. Reconstruct the six-leaf activation control,
and distinguish the old protected mark from the mark that takes the initial cover to four.
Trace the exact cells read and changed by the forward and reverse M1 legs and the path returned.
On the new two- and three-chart-cover families, derive every legal single-incidence return,
testing the additional returns when private witnesses are weakened, re-acquisition at the source,
arbitrary chart order, and making no move. Generalize to N marks. Derive the minimum cost to first
return without the released leaf at R even with deletions allowed, by inspecting every kind of
covering pair, and check both constructive upper bounds. Determine exactly which marked sets a
receiver can have for budget strictly below that cost. Test the inference at the threshold and
at two edits with three possible source events. Compare the chronological packet after a source
cut to full-path clipping of the source and inverse. Inspect input provenance of the threshold,
historic campaign scope, label order and the lack of an endogenous physical scheduler. Return
one JSON object with verdict ACCEPTED, REVISE or FAIL, the arrays findings, missing_assumptions,
counterexamples and limitations, native_bridge_status OPEN unless independently justified, and
proof_checks with the five keys trigger, uniqueness, budget, ordering, scope. Provide at least
fifteen words of independent worked reasoning under each key. ACCEPTED needs empty findings,
missing_assumptions and counterexamples. Adverse findings should identify a concrete failing
claim. Return exact_checks with precisely these keys:
six_active is [source chart index, released leaf] for the only activating cut on the ORIGINAL
six-leaf prior in its original labels. primary_arms and budget_arms are the sizes of the two
separate comparison campaigns. q2_preserving and q3_preserving are the numbers of one-edit
returns per source arm which keep the marked source cut in the named TWO-private-leaves-per-anchor
examples. three_mark_bypass is the exact bypass distance for N=3,m=1,n=3. three_mark_records
is the ordered list of possible marked **leaf sets** as arrays of actual 1-based leaf numbers
for the release of leaf 1 and return within TWO edits in that example. Sort sets first by size,
then lexicographically. rebuilt_first_chart is the chart index performing the FIRST edit of
the clipped prior, marked cut, inverse cycle in the named canonical two-cover example.
no_source_input_scheduler is true if a physical automatic v16.26 to v16.54 invocation remains
unproved. Do not treat a correctly scoped open physical interpretation as a failure of the finite
calculation or the conditional general theorem."""
if __name__ == "__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    verdict=json.loads((Path(sys.argv[2])/"review.txt").read_bytes())
    cert=json.loads(Path(__file__).with_name("cover_return_certificate.json").read_bytes())
    six,=[row for row in cert["original_six"]["original"]["cuts"] if row["run"]["legs"][0]]
    three=next(r for r in cert["budget"]["projected"] if r["source"]==[3,1,3,1])
    sets=[[v for v in (1,2,3) if mask&(1<<(v-1))] for mask in three["all"][1]]
    two=cert["named"]["2"]["arms"][0]
    expected=dict(six_active=[six["actor"],six["v"]],primary_arms=cert["arms"],budget_arms=cert["budget"]["arms"],
                  q2_preserving=len(two["cut_kept"]),q3_preserving=len(cert["named"]["3"]["arms"][0]["cut_kept"]),
                  three_mark_bypass=next(i for i,v in enumerate(three["untouched_R"],1) if 0 in v),
                  three_mark_records=sorted(sets,key=lambda r:(len(r),r)),rebuilt_first_chart=(two["cycle"][0]-1)%4,
                  no_source_input_scheduler=True)
    if json.dumps(verdict.get("exact_checks"),sort_keys=True)!=json.dumps(expected,sort_keys=True):
        raise ValueError("Independent quantitative reconstruction differs from the frozen experiment")
