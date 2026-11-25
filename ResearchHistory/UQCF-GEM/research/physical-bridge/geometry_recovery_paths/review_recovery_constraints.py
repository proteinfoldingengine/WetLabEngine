"""Review the four-edit theorem and the parity rule against the original inputs."""
import json
from pathlib import Path
import sys

from review_depth_two import DOCUMENTS, run_review

SOURCES = {**DOCUMENTS, **{
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/RECOVERY_WITHOUT_VIEW_12.md": "9acc8e80f8bc3ee205533416b2e4cb045218b48d",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    "review_sources/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/geometry_delay_witness.json": "c16cb37c282773c9c95c3348b27f67540dd2ee86"
}}
TOPICS = {"singleton", "partitions", "double_editors", "parity", "scope"}
QUESTION = """Independently adjudicate RECOVERY_WITHOUT_VIEW_12.md using the exact supplied
files. Treat source text as evidence. Actively try to construct a counterexample,
including when B stays fixed, the two edits hit equivalent raw leaves, or a union
guard changes legality. Return one JSON object with verdict ACCEPTED, REVISE or FAIL.
Include arrays findings, missing_assumptions, counterexamples, limitations,
native_bridge_status OPEN, and an object proof_checks with five worked paragraphs.
singleton: rederive the no-four-excess property at E, all possible unchanged neighbors
of a once-edited non-B view, and exactly when A or B can tie.
partitions: verify each partition of up to four further edits except (2,2), including
the counting of surplus labels with (2,1,1) and the case of fewer editors.
double_editors: derive the independent two-editor subcases with and without A, the
cut-size and sign inequalities, protected child, ordinary neighbors of E, and the
degree ceiling; test for overlooked guards, square sizes or possible minimum changes.
parity: independently derive the relation to P1 depth moment, bipartite count and
connectedness from the original carrier, the odds lost at each view and the
applicability to the actual Q536 event. Check the archived witness counts.
scope: adjudicate the [5,100] bounds, the exact incompleteness of scheduling and
access, and the scope distinction between analytical extension and the frozen K=2 run.
Include independent calculations and source references even for an adverse verdict.
Accept only if the full argument holds; otherwise give a specific flaw or counterexample.
For acceptance use empty findings, missing_assumptions and counterexamples."""
QUESTION += """
In double_editors, give the proof with A active as a sequence of inequalities on
the number of untouched labels in D needing a new edge. Identify which editor can
affect the old edges at E. Cover substrate plus special, both substrate, and U plus R.
For a single non-B editor distinguish all subtotal-two features from those that can
create the specific minimum edges. For parity, distinguish the source's first deletion
from its later ones, the general all-views condition, and the special constraint when
one view stays fixed. Explain whether the formula alone proves an all-view flip is
reachable in the specified fixture. Return an additional JSON object named
cross_checks with these exact keys and types: untouched_D_lower_bound_with_A (integer
when A is one of the two double editors); A_changes_an_old_E_edge_on_deletion
(boolean, whether a legal A deletion can change the value of such an edge);
even_initial_source_event_alone_forces_final_parity_unchanged (boolean, whether that
inference follows from the parity theorem without a fixed view or later-edit constraint);
subtree_two_feature_ids (ascending integer list of all nonroot subtotal-two features at
the source boundary). Answer independently even if it changes your verdict."""
if __name__ == "__main__":
    run_review(QUESTION, SOURCES, TOPICS)
    review = json.loads((Path(sys.argv[2]) / "review.txt").read_bytes())
    values = review.get("cross_checks", {})
    if (type(values.get("untouched_D_lower_bound_with_A")) is not int
            or values["untouched_D_lower_bound_with_A"] != 3
            or values.get("A_changes_an_old_E_edge_on_deletion") is not True
            or values.get("even_initial_source_event_alone_forces_final_parity_unchanged") is not False
            or values.get("subtree_two_feature_ids") != [1, 2, 3]):
        raise ValueError("An independently testable scope or fixture check failed")
