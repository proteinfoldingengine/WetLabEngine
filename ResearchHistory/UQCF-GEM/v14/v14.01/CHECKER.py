#!/usr/bin/env python3
import json

from admissibility_audit import run_audit

result = run_audit()

assert result["seed"] == 1401
assert result["trials"] == 256
assert result["scales"] == [0.2, 0.5, 2.0, 5.0, 11.0]
assert result["graph"]["n"] == 5
assert result["graph"]["edge_count"] == 7
assert result["graph"]["cycle_dimension"] == 3
assert result["incidence_only_cycle_leakage_norm"] < 1e-12
assert result["minimum_weighted_operator_norm"] > 1e-8
assert result["max_relative_source_scaling_error"] < 2e-12
assert result["max_covariance_error"] < 2e-12
assert result["max_normalized_candidate_direction_separation"] > 1e-3
assert result["candidate_operator_span_rank"] >= 2
assert result["positive_control_reconstruction_error"] < 2e-12
assert result["gate_outcome"] in {"DERIVED", "NONUNIQUE", "NO_NATIVE_DEFORMATION"}
if result["gate_outcome"] != "DERIVED":
    assert result["branch_status"] == "STOPPED_PENDING_NEW_SOURCE_TO_HIGHER_INCIDENCE_AXIOM_OR_CALIBRATION"

print("V14_01_GLOBAL_ADMISSIBILITY_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
