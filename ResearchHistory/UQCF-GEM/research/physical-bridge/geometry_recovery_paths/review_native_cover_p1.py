"""Challenge whether the strict successor imports an upstream P1 value at the receiver."""
import json
from pathlib import Path
import sys
from review_depth_two import run_review

DOCUMENTS = {
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_P1_PLAN.md": "dbf4456a7161aa46841b3a86391992ee95a1dfd7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_P1.md": "35b8259c37f8a50f1cf3446f9c07de865a1d18b7",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/check_native_cover_p1.py": "25b2ec7909889371e1d5dcf84bfd8bf97bf8eb64",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/native_cover_p1_certificate.json": "39f7abbd6dc07ede6c631ff81b7b7bddaa73a956",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/NATIVE_COVER_INCREMENT.md": "a52a3a45a97477586a7c1edef0ff851fffa9fc36",
    "ResearchHistory/UQCF-GEM/research/physical-bridge/geometry_recovery_paths/native_cover_increment_certificate.json": "236f51092ee4e1d5fbe0606af16b9c6c7ca4a01a",
    "review_sources/ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "review_sources/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py": "fc4a77fc4f01fce33fdb562423eca274cfb0c648"
}
TOPICS = {"objects","derivation","controls","call_path","scope"}
QUESTION = """Challenge NATIVE_COVER_P1.md as an original finite-fixture P1 provenance control.
Return verdict ACCEPTED, REVISE or FAIL. Return arrays findings, counterexamples,
missing_assumptions and limitations and native_bridge_status OPEN if unresolved.
Use ACCEPTED only if the scoped claims survive; then the first three arrays must be empty.
Return proof_checks with exactly objects, derivation, controls, call_path, scope; use at
least fifteen words of reconstruction per key. Check both sibling choices, direct versus
composed P1, which root receives which value, whether the surviving site already contained
the value and whether a common Genesis identifier suffices to compose the two charts.
Test the possibility that the numerical witness is merely stored in both charts before
the source. Scope the perturbations to fixed supports and distinguish the conditional
event selection from a physical writer. Return value_checks with exactly:
baseline_roots (two [before,after] arrays, source then receiver);
gains (three [source,receiver] arrays in order archive, source_plus_one, complement_plus_one);
surviving_x_at_B (same three cases, [before,after]); cross_composition (historical error
string); native_inputs (ordered array of raw Python argument names of atomic).
A numerical match alone does not suffice."""
if __name__=="__main__":
    run_review(QUESTION,DOCUMENTS,TOPICS)
    cert=json.loads(Path(__file__).with_name("native_cover_p1_certificate.json").read_text())
    first=cert["arms"]["718"]
    assert first["variations"]==cert["arms"]["719"]["variations"]
    vs=[first["variations"][k] for k in ("archived","source_plus_one","complement_plus_one")]
    expected=dict(baseline_roots=[vs[0]["root_a"],vs[0]["root_b"]],
                  gains=[v["gains"] for v in vs],surviving_x_at_B=[v["retained_x_at_b"] for v in vs],
                  cross_composition=first["typed_cross_composition"],native_inputs=cert["atom_parameters"])
    verdict=json.loads((Path(sys.argv[2])/"review.txt").read_text())
    if verdict.get("value_checks")!=expected:
        raise ValueError("The independent P1 object or sensitivity reconstruction disagrees")
