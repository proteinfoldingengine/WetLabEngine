"""Review the four-edit theorem and the parity rule against the original inputs."""
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
if __name__ == "__main__":
    run_review(QUESTION, SOURCES, TOPICS)
