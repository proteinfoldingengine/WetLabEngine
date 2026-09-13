#!/usr/bin/env python3
import json

from dual_normal_audit import run_audit

result = run_audit()

assert result["version"] == "v14.02"
assert result["seed"] == 1402
assert result["survey"]["V_A"]["sample_count"] == 64
assert result["survey"]["V_B"]["sample_count"] == 64
assert result["primary_sample_count"] == 128
assert result["construction"]["uses_full_hidden_kernel"] is True
assert result["construction"]["uses_visualization_section"] is False
assert result["typed_dual_control"] == "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE"
assert result["interior_control"]["classification"] == "NO_BOUNDARY_SELECTOR"
assert result["interior_control"]["minimum_center_eigenvalue"] > 0.0
assert result["synthetic_degenerate_control"]["classification"] == "NONUNIQUE_NORMAL_CONE"
assert result["synthetic_degenerate_control"]["projected_normal_span_rank"] >= 2
assert result["max_boundary_psd_residual"] < 2e-9
assert result["max_support_identity_relative_error"] < 2e-9
assert result["max_basis_invariance_relative_error"] < 2e-9
assert result["zero_projected_normal_count"] == 0
assert result["gate_outcome"] in {
    "CANONICAL_DUAL_RAY",
    "NONUNIQUE_NORMAL_CONE",
    "NO_BOUNDARY_SELECTOR",
    "UNRESOLVED_NUMERICAL_BOUNDARY",
}

print("V14_02_CONVEX_DUAL_NORMAL_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
