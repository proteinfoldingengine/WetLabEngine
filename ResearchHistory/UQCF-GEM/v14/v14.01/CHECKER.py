#!/usr/bin/env python3
import json
from pathlib import Path

from admissibility_audit import run_audit

root = Path(__file__).resolve().parent
expected = json.loads((root / "SUMMARY.json").read_text())
result = run_audit()
frozen = expected["fresh_controls"]

assert result["version"] == expected["version"]
assert result["seed"] == frozen["seed"] == 1401
assert result["trials"] == frozen["trials"] == 256
assert result["scales"] == frozen["scales"] == [0.2, 0.5, 2.0, 5.0, 11.0]
assert result["graph"]["n"] == frozen["graph_n"] == 5
assert result["graph"]["edge_count"] == frozen["edge_count"] == 7
assert result["graph"]["cycle_dimension"] == frozen["cycle_dimension"] == 3

assert result["incidence_only_cycle_leakage_norm"] < 1e-12
assert result["minimum_weighted_operator_norm"] > 1e-8
assert result["max_relative_source_scaling_error"] < 2e-12
assert result["max_covariance_error"] < 2e-12
assert result["max_normalized_candidate_direction_separation"] > 1e-3
assert result["candidate_operator_span_rank"] >= 2
assert result["positive_control_reconstruction_error"] < 2e-12

# Bind stable scientific outputs to the frozen archive while allowing machine epsilon drift.
def close(a, b, atol=2e-12, rtol=2e-12):
    scale = max(abs(float(a)), abs(float(b)), 1.0)
    return abs(float(a) - float(b)) <= atol + rtol * scale

assert close(result["incidence_only_cycle_leakage_norm"], frozen["incidence_only_cycle_leakage_norm"])
assert close(result["max_relative_source_scaling_error"], frozen["max_relative_source_scaling_error"])
assert close(result["max_covariance_error"], frozen["max_covariance_error"])
assert close(result["max_normalized_candidate_direction_separation"], frozen["max_normalized_candidate_direction_separation"])
assert result["candidate_operator_span_rank"] == frozen["candidate_operator_span_rank"]
assert result["nonzero_trial_outputs"] == frozen["nonzero_trial_outputs"]
for name, value in frozen["candidate_operator_norms"].items():
    assert close(result["candidate_operator_norms"][name], value)

# Global positivity must not silently act as an untested selector.
pos = result["positivity_audit"]
assert pos["faithful_interior_common_epsilon"] > 0.0
assert pos["minimum_faithful_interior_margin"] > 0.0
assert pos["boundary_matrix_dimension"] == frozen["boundary_matrix_dimension"] == 4
assert pos["boundary_tangent_lineality_dimension"] == frozen["boundary_tangent_lineality_dimension"] == 9
assert pos["boundary_selector_classification"] == expected["positivity_selector_classification"]
assert close(pos["faithful_interior_common_epsilon"], frozen["faithful_interior_common_epsilon"])
assert close(pos["minimum_faithful_interior_margin"], frozen["minimum_faithful_interior_margin"])
assert close(result["positive_control_reconstruction_error"], frozen["positive_control_reconstruction_error"])

assert result["gate_outcome"] == expected["adjudication"] == "NONUNIQUE"
assert result["branch_status"] == expected["branch_status"]
assert result["Pillar_3"] == expected["Pillar_3"] == "OPEN"

print("V14_01_GLOBAL_ADMISSIBILITY_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
