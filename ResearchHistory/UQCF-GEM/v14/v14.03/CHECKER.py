#!/usr/bin/env python3
import json
from pathlib import Path

from source_ray_audit import run_audit

result = run_audit()
expected = json.loads(Path(__file__).with_name("SUMMARY.json").read_text())

# Scientific thresholds remain independent of the frozen summary.
assert result["version"] == "v14.03"
assert result["seed"] == 1403
assert result["primary_sample_count"] == 128
assert result["survey"]["V_A"]["sample_count"] == 64
assert result["survey"]["V_B"]["sample_count"] == 64
assert result["max_tangent_hermiticity_residual"] < 2e-11
assert result["max_tangent_trace_abs"] < 2e-11
assert result["max_finite_difference_relative_error"] < 2e-7
assert result["max_base_boundary_formula_relative_error"] < 2e-9
assert result["max_projective_hidden_direction_drift"] < 2e-9
assert result["max_projective_boundary_relative_drift"] < 2e-9
assert result["max_projective_dual_ray_drift"] < 2e-9
assert result["max_support_coordinate_covariance_error"] < 2e-9
assert result["max_boundary_psd_residual"] < 2e-9
assert result["unresolved_numerical_count"] == 0
assert result["nonunique_contact_count"] == 0
assert result["identity_source_control"]["classification"] == "ZERO_PGRL_TANGENT"
assert result["hidden_active_control"]["classification"] == "NONZERO_HIDDEN_COMPONENT"
assert result["gate_outcome"] in {
    "PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY",
    "SOURCE_TO_BOUNDARY_NONUNIQUE",
    "NO_HIDDEN_SOURCE_CONTACT",
    "UNRESOLVED_NUMERICAL_SOURCE_LIFT",
}
assert result["provenance_source_ray_status"] in {
    "PROVENANCE_TO_SOURCE_RAY_DERIVED",
    "PROVENANCE_TO_SOURCE_RAY_UNDERIVED",
    "PROVENANCE_SOURCE_TYPE_MISMATCH",
}

# Frozen discrete scientific record.
assert result["version"] == expected["version"]
assert result["seed"] == expected["seed"]
assert result["gate_outcome"] == expected["gate_outcome"]
assert result["scientific_breakthrough"] == expected["scientific_breakthrough"]
assert result["Pillar_3"] == expected["Pillar_3"]
assert result["primary_sample_count"] == expected["primary_sample_count"]
assert result["zero_hidden_source_count"] == expected["zero_hidden_source_count"]
assert result["nonzero_hidden_contact_count"] == expected["nonzero_hidden_contact_count"]
assert result["simple_ray_contact_count"] == expected["simple_ray_contact_count"]
assert result["unresolved_numerical_count"] == expected["unresolved_numerical_count"]
assert result["nonunique_contact_count"] == expected["nonunique_contact_count"]
assert result["provenance_source_ray_status"] == expected["provenance_source_ray_status"]

for name in ("V_A", "V_B"):
    actual_s = result["survey"][name]
    frozen_s = expected["survey"][name]
    for key in (
        "sample_count",
        "support_dimension",
        "hidden_dimension",
        "zero_hidden_source_count",
        "nonzero_hidden_contact_count",
        "simple_ray_contact_count",
        "source_sha256",
    ):
        assert actual_s[key] == frozen_s[key], (name, key, actual_s[key], frozen_s[key])

for key in (
    "uses_full_support_state",
    "uses_full_hidden_kernel",
    "uses_visualization_section",
    "boundary_is_hidden_tangent_radial_contact_not_pgrl_crossing",
):
    assert result["construction"][key] == expected["construction"][key]

for control in ("identity_source_control", "hidden_active_control", "visible_only_tangent_control"):
    assert result[control]["classification"] == expected["controls"][control]["classification"]

# Frozen floating telemetry: allow harmless BLAS-level drift while rejecting scientific drift.
def close(actual, frozen):
    tol = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(float(frozen)))
    return abs(float(actual) - float(frozen)) <= tol

telemetry_map = {
    "max_tangent_hermiticity_residual": "max_tangent_hermiticity_residual",
    "max_tangent_trace_abs": "max_tangent_trace_abs",
    "max_finite_difference_relative_error": "max_finite_difference_relative_error",
    "max_base_boundary_formula_relative_error": "max_base_boundary_formula_relative_error",
    "max_projective_tangent_scaling_error": "max_projective_tangent_scaling_error",
    "max_projective_hidden_direction_drift": "max_projective_hidden_direction_drift",
    "max_projective_boundary_relative_drift": "max_projective_boundary_relative_drift",
    "max_projective_dual_ray_drift": "max_projective_dual_ray_drift",
    "max_support_coordinate_covariance_error": "max_support_coordinate_covariance_error",
    "max_boundary_psd_residual": "max_boundary_psd_residual",
    "max_hidden_projection_idempotence_error": "max_hidden_projection_idempotence_error",
}
for result_key, frozen_key in telemetry_map.items():
    assert close(result[result_key], expected["telemetry"][frozen_key]), (
        result_key,
        result[result_key],
        expected["telemetry"][frozen_key],
    )

control_float_keys = {
    "identity_source_control": ("tangent_norm",),
    "hidden_active_control": ("hidden_norm", "tangent_target_error"),
    "visible_only_tangent_control": ("hidden_norm", "tangent_target_error"),
}
for control, keys in control_float_keys.items():
    for key in keys:
        assert close(result[control][key], expected["controls"][control][key]), (
            control,
            key,
            result[control][key],
            expected["controls"][control][key],
        )

print("V14_03_PROJECTIVE_SOURCE_RAY_CHECKER_PASS")
print(json.dumps({
    "gate_outcome": result["gate_outcome"],
    "provenance_source_ray_status": result["provenance_source_ray_status"],
    "primary_sample_count": result["primary_sample_count"],
    "nonzero_hidden_contact_count": result["nonzero_hidden_contact_count"],
    "simple_ray_contact_count": result["simple_ray_contact_count"],
    "unresolved_numerical_count": result["unresolved_numerical_count"],
    "max_finite_difference_relative_error": result["max_finite_difference_relative_error"],
    "max_projective_hidden_direction_drift": result["max_projective_hidden_direction_drift"],
    "max_projective_boundary_relative_drift": result["max_projective_boundary_relative_drift"],
    "max_projective_dual_ray_drift": result["max_projective_dual_ray_drift"],
    "max_support_coordinate_covariance_error": result["max_support_coordinate_covariance_error"],
}, indent=2, sort_keys=True))
