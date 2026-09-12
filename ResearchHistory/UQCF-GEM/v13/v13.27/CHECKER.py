#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent
s = json.loads((root / "SUMMARY.json").read_text())

assert s["version"] == "v13.27"

p = s["fresh_projective_source_controls"]
assert p["generic_current_trials"] >= 64
assert p["max_source_balance_residual"] < 1e-12
assert p["max_normalized_source_ray_direction_change"] < 1e-12
assert p["support_pattern_preserved"] is True

q = s["QMAR_parameterization_control"]
assert q["generic_linear_response_trials"] >= 64
assert q["max_reparameterized_increment_mismatch"] < 1e-12
assert q["max_response_scaling_identity_error"] < 1e-11
assert q["max_normalized_response_direction_change"] < 1e-12

t = s["tensor_completion_control"]
assert t["same_coupled_rho_j_projection_mismatch"] < 1e-12
assert t["different_full_tensor_frobenius_distance"] > 0.1

c = s["independent_geometric_calibration_positive_control"]
assert c["absolute_error"] < 1e-12

a = s["adjudication"]
assert a["RSCL_no_go_preserved"] is True
assert a["projective_source_ray_preserved"] is True
assert a["unique_nonzero_Sigma_obs_derived"] is False
assert a["QMAR_fixes_absolute_Sigma_magnitude"] is False
assert a["full_kappa_T_tensor_derived_from_retained_scalar_current"] is False
assert a["Einstein_or_ADM_residual_may_select_coupling"] is False
assert a["RGCL"] == "MISSING"

assert s["status"]["scientific_breakthrough"] is False
assert s["next_gate"]["version"] == "v13.28"

print("V13_27_CHECKER_PASS")
