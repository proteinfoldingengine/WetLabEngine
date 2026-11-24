"""Challenge the all-view all-length refinement theorem and the single-entry control."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SINGLE_VIEW_EXACT_RETURN.md": "00786d6d59fb5eef657d45e56935650c1ff802dd",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SINGLE_VIEW_EXACT_RETURN_PLAN.md": "550f17b11a90f6ccbd1ad39f2e54337a82992005",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/SINGLE_VIEW_SOURCE_PLAN.md": "c7ef429e8994743863e3f1ad93d915f2641f0128",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_single_view_returns.py": "3b7bb173d15bcc469f886e2050d2c01f56600085",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/single_view_returns_certificate.json": "24816b42f2c00c9790e2417c95ba0589074050b0",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/GEOMETRY_SELECTED_RECORD.md": "5db94e33376a4c904904c2ffc280078cc3544317",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/geometry_selected_record_certificate.json": "34fa8c957dec8b7433543553abb4c1d57db36b4a",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py": "3324c0b46e09120ae526338444a19070b692d049",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.25-pruning-refinement-closure/engine.py": "e9c576a2590c8e16812f1b3fa0436111e3648f1c",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c"
}
TOPICS = {"endpoint", "source", "all_editors", "admission_control", "scope"}
QUESTION = """Challenge the post-replay theorem SINGLE_VIEW_EXACT_RETURN.md on its
stated 25-view fixture. Rebuild the private-ancestor and zero-column arguments for
arbitrary single-view refinements. Reconstruct both source completions, exactly which
other view can change, the two possible partners, why there is no upper length
assumption, the permanence statement and both kinds of blind control. Test whether
the 13 single-entry witnesses justify exactly the stated necessity claim and whether
the full native carrier gate and unlabelled readout are being overinterpreted.
Examine the different algorithms and the timing of the two plans. Decline acceptance
with a concrete counterexample if necessary.

Return verdict ACCEPTED, REVISE or FAIL, native_bridge_status, proof_checks,
numeric_checks, and arrays findings, missing_assumptions, counterexamples, limitations.
Use OPEN literally for an open physical bridge. An ACCEPTED verdict requires the
first three defect arrays to be empty. Supply at least 15 words of reconstruction
in each proof_checks key: endpoint, source, all_editors, admission_control, scope.
Return exactly these numeric_checks keys: charts (integer), source_completions (the two
sorted arrays of removed raw leaf IDs at view 0 before any receiver edit, ordered by
their first ID), receiver (integer), resulting_choices (counts of different receiver
endpoints after sources 718 then 719), receiver_partners (ascending raw IDs),
admitted_single_changes (integer number of passing j among the tested 17),
sample_changed_pair (two chart labels of the representative 593 control),
sample_work (two integers giving the before and after value there).
Use limitations to record supplied event occurrence, work conservation and physical
address readout. No numerical fit, physical clock or general impossibility is claimed."""

if __name__ == "__main__":
    run_review(QUESTION, DOCUMENTS, TOPICS)
    data = json.loads(Path(__file__).with_name("single_view_returns_certificate.json").read_bytes())
    arms = [data["arms"][s] for s in ("718","719")]
    first = arms[0]
    expected = {"charts":len(first["checks"]),"source_completions":data["common_source"]["all_endpoints"],
                "receiver":first["exact"][0][0],"resulting_choices":[len(a["exact"]) for a in arms],
                "receiver_partners":sorted(row[1][1] for row in first["exact"]),
                "admitted_single_changes":sum(r["carrier"]=="accepted" for r in first["admission_only"]),
                "sample_changed_pair":[0,first["blind"]["j"]],"sample_work":[1992,1990]}
    verdict = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    if json.dumps(verdict.get("numeric_checks"),sort_keys=True) != json.dumps(expected,sort_keys=True):
        raise ValueError("All-view reviewer values differ from the evidence")
