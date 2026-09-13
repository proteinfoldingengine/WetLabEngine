#!/usr/bin/env python3
import json
import math
from pathlib import Path

from rgcl_audit import run_audit

root = Path(__file__).resolve().parent
summary = json.loads((root / "SUMMARY.json").read_text())
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

frozen = summary["fresh_controls"]
assert frozen["seed"] == result["seed"]
assert frozen["trials"] == result["trials"]
assert frozen["scales"] == result["scales"]
assert frozen["candidate_count"] == result["candidate_count"]
for key in (
    "max_relative_linear_scaling_error",
    "max_normalized_direction_drift",
    "max_relative_bkm_quadratic_scaling_error",
    "max_relative_inverse_weight_positive_control_error",
    "minimum_baseline_candidate_norm",
):
    assert math.isclose(float(frozen[key]), float(result[key]), rel_tol=2e-14, abs_tol=2e-15), (
        key,
        frozen[key],
        result[key],
    )

assert summary["candidate_verdicts"] == result["candidate_verdicts"]
assert summary["adjudication"] == result["gate_outcome"]
assert summary["branch_status"] == result["source_to_gr_coupling_branch"]

print("V13_28_RGCL_PAIRING_AUDIT_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
