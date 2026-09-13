#!/usr/bin/env python3
import json

from source_ray_audit import run_audit

result = run_audit()

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

print("V14_03_PROJECTIVE_SOURCE_RAY_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
