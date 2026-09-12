#!/usr/bin/env python3
import json
from pathlib import Path

from uqcf_demo.simulation import default_config, run_telemetry

root = Path(__file__).resolve().parent
expected = json.loads((root / "EXPECTED_RESULTS.json").read_text())
data = run_telemetry(default_config(frames=expected["default_frames"]))
s = data["summary"]
t = expected["structural_thresholds"]

assert data["version"] == expected["version"]
assert s["min_state_eigenvalue"] > t["min_state_eigenvalue_gt"]
assert s["min_bkm_eigenvalue"] > t["min_bkm_eigenvalue_gt"]
assert s["max_source_balance_residual"] < t["max_source_balance_residual_lt"]
assert s["max_projective_direction_change"] < t["max_projective_direction_change_lt"]
assert s["pgrl_reparameterization_error"] < t["pgrl_reparameterization_error_lt"]
assert s["dewitt_pure_trace_control"] < t["dewitt_pure_trace_control_lt"]
assert s["dewitt_traceless_control"] > t["dewitt_traceless_control_gt"]
assert s["max_cycle_rank_deficit"] == t["max_cycle_rank_deficit_eq"]
assert s["projective_sigma_status"] == "RAY_ONLY__MAGNITUDE_NOT_DERIVED"
assert s["RGCL"] == "MISSING"
assert s["physical_Einstein_closure"] == "OPEN"

assert data["scientific_fingerprint"] == expected["scientific_fingerprint"], (
    data["scientific_fingerprint"],
    expected["scientific_fingerprint"],
)

print("V13_27_GRAVITY_PROGRESS_CHECKER_PASS")
print("scientific_fingerprint", data["scientific_fingerprint"])
print("telemetry_hash", data["telemetry_hash"])
print("reference_raw_telemetry_hash", expected["reference_raw_telemetry_hash"])
print("note", "raw telemetry hash is diagnostic; scientific fingerprint is the portable certification key")
