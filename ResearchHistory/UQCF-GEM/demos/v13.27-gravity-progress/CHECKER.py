#!/usr/bin/env python3
import json
from pathlib import Path

from uqcf_demo.simulation import default_config, run_telemetry

root = Path(__file__).resolve().parent
expected = json.loads((root / "EXPECTED_RESULTS.json").read_text())
data = run_telemetry(default_config(frames=expected["default_frames"]))
s = data["summary"]
t = expected["structural_thresholds"]

print("scientific_fingerprint_actual", data["scientific_fingerprint"])
print("telemetry_hash_actual", data["telemetry_hash"])
print("raw_polar_reflection_count", s["raw_polar_reflection_count"])
print("raw_polar_reflection_fraction", s["raw_polar_reflection_fraction"])
print("min_holonomy_raw_cos_argument", s["min_holonomy_raw_cos_argument"])
print("max_holonomy_raw_cos_argument", s["max_holonomy_raw_cos_argument"])
print("holonomy_clip_event_count", s["holonomy_clip_event_count"])
print("max_holonomy_clip_excess", s["max_holonomy_clip_excess"])
print("pi_holonomy_event_count", s["pi_holonomy_event_count"])
print("pi_holonomy_adjudication", s["pi_holonomy_adjudication"])

assert data["version"] == expected["version"]
assert s["min_state_eigenvalue"] > t["min_state_eigenvalue_gt"]
assert s["min_bkm_eigenvalue"] > t["min_bkm_eigenvalue_gt"]
assert s["max_source_balance_residual"] < t["max_source_balance_residual_lt"]
assert s["max_projective_direction_change"] < t["max_projective_direction_change_lt"]
assert s["pgrl_reparameterization_error"] < t["pgrl_reparameterization_error_lt"]
assert s["dewitt_pure_trace_control"] < t["dewitt_pure_trace_control_lt"]
assert s["dewitt_traceless_control"] > t["dewitt_traceless_control_gt"]
assert s["max_cycle_rank_deficit"] == t["max_cycle_rank_deficit_eq"]
assert s["raw_polar_reflection_count"] == t["raw_polar_reflection_count_eq"]
assert abs(s["raw_polar_reflection_fraction"] - t["raw_polar_reflection_fraction_eq"]) < 1e-12
assert s["holonomy_clip_event_count"] == t["holonomy_clip_event_count_eq"]
assert s["max_holonomy_clip_excess"] < t["max_holonomy_clip_excess_lt"]
assert s["pi_holonomy_event_count"] == t["pi_holonomy_event_count_eq"]
assert s["pi_holonomy_adjudication"] == expected["executed_summary"]["pi_holonomy_adjudication"]
assert s["projective_sigma_status"] == "RAY_ONLY__MAGNITUDE_NOT_DERIVED"
assert s["RGCL"] == "MISSING"
assert s["physical_Einstein_closure"] == "OPEN"

assert data["scientific_fingerprint"] == expected["scientific_fingerprint"], (
    data["scientific_fingerprint"],
    expected["scientific_fingerprint"],
)

print("V13_27_METHODS_OBSTRUCTION_CHECKER_PASS")
print("scientific_fingerprint", data["scientific_fingerprint"])
print("telemetry_hash", data["telemetry_hash"])
print("reference_raw_telemetry_hash", expected["reference_raw_telemetry_hash"])
print("note", "raw telemetry hash is diagnostic; scientific fingerprint is the portable certification key")
