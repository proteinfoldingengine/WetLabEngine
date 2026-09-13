#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

from canonical_neutral_reference_audit import adjudicate_gate, run_audit

# Adjudication must not infer an opposite result merely because verification fails.
assert adjudicate_gate(True, False) == "CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED"
assert adjudicate_gate(False, True) == "FROZEN_ONTOLOGY_IDENTIFIES_CANONICAL_GENERATOR_AS_SOURCE"
assert adjudicate_gate(False, False) == "V15_07_GATE_UNRESOLVED"
try:
    adjudicate_gate(True, True)
except ValueError:
    pass
else:
    raise AssertionError("mutually exclusive v15.07 adjudications must raise")

s = run_audit()

# Additional exact source-origin evidence added after the first GREEN audit.
# These reports make the semantic boundary explicit: PGRL acts at supplied
# states, Genesis/source anchoring is identity/compatibility structure, and
# neither rule defines sourcehood as neutral-reference-to-state preparation.
EXTRA_SOURCE_BINDINGS = {
    "ResearchHistory/UQCF-GEM/v13/v13.04/REPORT.md": "e857d81f58a540833a7672fe769b2a301bad4459",
    "ResearchHistory/UQCF-GEM/v13/v13.25/REPORT.md": "65847800d6c079803e7c18537ef57cdc7f87da25",
    "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md": "9917085b211ca0e1f4737082227f55097cc72b66",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


repo_root = Path(__file__).resolve().parents[4]
for rel, expected_sha in EXTRA_SOURCE_BINDINGS.items():
    assert git_blob_sha(repo_root / rel) == expected_sha, f"source-origin archive binding changed: {rel}"

# Scientific gates are enforced independently from frozen-value reproducibility.
assert s["version"] == "v15.07"
assert s["gate"] == "Canonical Neutral Reference / Relative-Density Generator Gate"
assert s["primary_outcome"] == "CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED"
assert s["secondary_outcome"] == "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED"
assert s["tertiary_outcome"] == "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY"
assert s["major_structural_result"] is True
assert s["scientific_breakthrough"] is False
assert s["Pillar_3"] == "OPEN"

neutral = s["canonical_neutral_reference"]
assert neutral["classification"] == "UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED"
assert neutral["all_commutant_nullities_one"] is True
assert neutral["max_commutant_residual"] < 1e-12
assert neutral["max_reference_tensor_error"] < 1e-12
assert neutral["max_unitary_invariance_error"] < 1e-12
assert neutral["tested_dimensions"] == [2, 3, 4, 5]

relative = s["relative_density_generator"]
assert relative["classification"] == "CANONICAL_RELATIVE_DENSITY_OPERATOR_IS_MULTIPLICATIVE"
assert relative["max_relative_operator_tensor_error"] < 1e-12
assert relative["max_log_tensor_additivity_error"] < 1e-11
assert relative["max_centered_log_identity_error"] < 1e-12
assert relative["max_local_frame_covariance_error"] < 1e-11
assert relative["generator_shape"] == "centered_log_rho"

endpoint = s["neutral_to_state_endpoint"]
assert endpoint["classification"] == "NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY"
assert endpoint["status"] == "CONDITIONAL_ON_SOURCE_AS_NEUTRAL_TO_STATE_PREPARATION_GENERATOR"
assert endpoint["max_endpoint_reconstruction_error"] < 1e-11
assert endpoint["max_generator_identity_error"] < 1e-11
assert endpoint["product_endpoint_error"] < 1e-11
assert endpoint["projective_generator_ray_selected"] is True
assert endpoint["absolute_generator_scale_selected"] is False

boundary = s["source_identification_boundary"]
assert boundary["classification"] == "CANONICAL_OPERATOR_GENERATOR_DOES_NOT_BY_ITSELF_DEFINE_THE_SOURCE"
assert boundary["same_state_multiple_valid_pgrl_generators"] is True
assert boundary["min_pairwise_global_source_ray_separation"] > 1e-2
assert boundary["canonical_generator_vs_v15_04_log_source_ray_residual"] < 1e-11
assert boundary["frozen_source_equals_neutral_relative_generator_axiom_found"] is False

claim = s["claim_boundary"]
assert claim["canonical_neutral_reference_derived"] is True
assert claim["canonical_multiplicative_local_operator_derived"] is True
assert claim["centered_log_generator_derived"] is True
assert claim["neutral_to_state_log_projective_ray_theorem"] is True
assert claim["log_generator_identified_as_physical_source"] is False
assert claim["new_source_semantics_needed"] is True
assert claim["downstream_gravity_used_as_selector"] is False
assert claim["entropy_or_time_used_as_selector"] is False
assert claim["Pillar_3_closed"] is False


def summary_view(live: dict) -> dict:
    frozen = live["frozen_dependency_audit"]
    n = live["canonical_neutral_reference"]
    r = live["relative_density_generator"]
    e = live["neutral_to_state_endpoint"]
    b = live["source_identification_boundary"]
    extended_bindings = dict(frozen["archive_bindings"])
    extended_bindings.update(EXTRA_SOURCE_BINDINGS)
    return {
        "version": live["version"],
        "gate": live["gate"],
        "primary_outcome": live["primary_outcome"],
        "secondary_outcome": live["secondary_outcome"],
        "tertiary_outcome": live["tertiary_outcome"],
        "major_structural_result": live["major_structural_result"],
        "scientific_breakthrough": live["scientific_breakthrough"],
        "Pillar_3": live["Pillar_3"],
        "frozen_dependency_audit": {
            "archive_bindings": extended_bindings,
            "archive_bindings_match_expected": frozen["archive_bindings_match_expected"],
            "classification": frozen["classification"],
            "source_semantics_rule_found": frozen["source_semantics_rule_found"],
            "v13_04_supplied_state_semantics": "PGRL acts at each supplied faithful state and does not prescribe the baseline-state origin",
            "v13_11_forces_P_equal_centered_log_rho": frozen["v13_11"]["forces_P_equal_centered_log_rho"],
            "v13_25_source_origin_scope": "Genesis/source anchoring plus source-current compatibility; no state-preparation source semantics",
            "v13_26_genesis_semantics": "Genesis anchoring is source-origin identity/compatibility and does not make origin an absolute source strength",
            "v15_04_a_of_r_selected": frozen["v15_04"]["a_of_r_selected"],
            "v15_05_log_selector_premise_frozen": frozen["v15_05"]["premise_was_frozen"],
            "v15_06_canonical_local_operator_question_answered": "Q_d(rho)=d*rho",
        },
        "canonical_neutral_reference": {
            "classification": n["classification"],
            "reference_formula": n["reference_formula"],
            "tested_dimensions": n["tested_dimensions"],
            "commutant_nullities": n["commutant_nullities"],
            "all_commutant_nullities_one": n["all_commutant_nullities_one"],
            "max_commutant_residual": n["max_commutant_residual"],
            "max_unitary_invariance_error": n["max_unitary_invariance_error"],
            "max_reference_tensor_error": n["max_reference_tensor_error"],
            "requires_basis_choice": n["requires_basis_choice"],
            "uses_entropy_or_time": n["uses_entropy_or_time"],
        },
        "relative_density_generator": {
            "classification": r["classification"],
            "relative_operator": r["relative_operator"],
            "multiplicative_law": r["multiplicative_law"],
            "additive_generator": r["additive_generator"],
            "centered_generator": r["centered_generator"],
            "generator_shape": r["generator_shape"],
            "max_relative_operator_tensor_error": r["max_relative_operator_tensor_error"],
            "max_log_tensor_additivity_error": r["max_log_tensor_additivity_error"],
            "max_centered_log_identity_error": r["max_centered_log_identity_error"],
            "max_local_frame_covariance_error": r["max_local_frame_covariance_error"],
            "uses_reference_beyond_frame_symmetry": r["uses_reference_beyond_frame_symmetry"],
        },
        "neutral_to_state_endpoint": {
            "classification": e["classification"],
            "status": e["status"],
            "max_endpoint_reconstruction_error": e["max_endpoint_reconstruction_error"],
            "max_generator_identity_error": e["max_generator_identity_error"],
            "product_endpoint_error": e["product_endpoint_error"],
            "absolute_generator_scale_selected": e["absolute_generator_scale_selected"],
            "projective_generator_ray_selected": e["projective_generator_ray_selected"],
            "premise_frozen_as_source_semantics": e["premise_frozen_as_source_semantics"],
        },
        "source_identification_boundary": {
            "classification": b["classification"],
            "frozen_source_equals_neutral_relative_generator_axiom_found": b["frozen_source_equals_neutral_relative_generator_axiom_found"],
            "same_state_multiple_valid_pgrl_generators": b["same_state_multiple_valid_pgrl_generators"],
            "candidate_generators": b["candidate_generators"],
            "pairwise_global_source_ray_separations": b["pairwise_global_source_ray_separations"],
            "min_pairwise_global_source_ray_separation": b["min_pairwise_global_source_ray_separation"],
            "min_finite_pgrl_output_eigenvalue": b["min_finite_pgrl_output_eigenvalue"],
            "max_finite_pgrl_trace_error": b["max_finite_pgrl_trace_error"],
            "canonical_generator_vs_v15_04_log_source_ray_residual": b["canonical_generator_vs_v15_04_log_source_ray_residual"],
        },
        "claim_boundary": live["claim_boundary"],
        "next_lawful_question": live["next_lawful_question"],
    }


def assert_archive_equal(actual, expected, path="$"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), f"{path}: expected dict"
        assert set(actual) == set(expected), f"{path}: key mismatch"
        for key in expected:
            assert_archive_equal(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        assert isinstance(actual, list), f"{path}: expected list"
        assert len(actual) == len(expected), f"{path}: length mismatch"
        for idx, (a_item, e_item) in enumerate(zip(actual, expected)):
            assert_archive_equal(a_item, e_item, f"{path}[{idx}]")
        return
    if isinstance(expected, bool) or expected is None or isinstance(expected, (str, int)):
        assert actual == expected, f"{path}: {actual!r} != {expected!r}"
        return
    if isinstance(expected, float):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), f"{path}: expected numeric"
        assert math.isfinite(float(actual)) and math.isfinite(expected), f"{path}: non-finite value"
        tolerance = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(expected))
        assert abs(float(actual) - expected) <= tolerance, (
            f"{path}: numeric mismatch {actual!r} vs {expected!r}, tol={tolerance}"
        )
        return
    raise TypeError(f"{path}: unsupported archive type {type(expected)!r}")

frozen_summary = json.loads(Path("SUMMARY.json").read_text())
assert_archive_equal(summary_view(s), frozen_summary)

print(json.dumps(s, indent=2, sort_keys=True))
