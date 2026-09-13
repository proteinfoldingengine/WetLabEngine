#!/usr/bin/env python3
import json

from rgcl_audit import run_audit

result = run_audit()

assert result["seed"] == 1328
assert result["trials"] == 256
assert result["scales"] == [0.2, 0.5, 2.0, 5.0, 11.0]
assert result["candidate_count"] == 4
assert result["max_relative_linear_scaling_error"] < 2e-12
assert result["max_normalized_direction_drift"] < 2e-12
assert result["max_relative_bkm_quadratic_scaling_error"] < 2e-12
assert result["max_relative_inverse_weight_positive_control_error"] < 2e-12
assert result["minimum_baseline_candidate_norm"] > 1e-6
assert result["candidate_verdicts"] == {
    "genesis_measure_support": "OBSTRUCTED",
    "pgrl_bkm": "OBSTRUCTED",
    "resa_solder_coframe": "OBSTRUCTED",
    "qmar_response_covariance": "OBSTRUCTED",
}
assert result["gate_outcome"] == "REQUIRES_NEW_AXIOM"
assert result["source_to_gr_coupling_branch"] == "STOPPED_PENDING_NEW_AXIOM_OR_INDEPENDENT_CALIBRATION"

print("V13_28_RGCL_PAIRING_AUDIT_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
