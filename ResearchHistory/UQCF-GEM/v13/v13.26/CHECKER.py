#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent
s = json.loads((root / "SUMMARY.json").read_text())

assert s["version"] == "v13.26"

p = s["candidate_audit"]["PGRL_exponential_family_amplitude"]
assert p["max_state_mismatch"] < 1e-12
assert p["max_chain_rule_tangent_mismatch"] < 1e-8

r = s["candidate_audit"]["recoverability_response_normalization"]
assert r["max_reconstructed_current_change"] < 1e-12
assert r["max_sigma_scaling_identity_error"] < 1e-12

c = s["common_scale_control"]
assert c["max_source_balance_residual"] < 1e-12
assert c["max_coupled_product_error"] < 1e-12
assert c["max_normalized_source_direction_change"] < 1e-12

a = s["adjudication"]
assert a["protected_grading_derives_RSCL"] is False
assert a["PGRL_amplitude_derives_RSCL"] is False
assert a["Genesis_derives_RSCL"] is False
assert a["recoverability_response_derives_RSCL"] is False
assert a["RSCL"] == "IRREDUCIBLE_RELATIVE_TO_CURRENT_FROZEN_ONTOLOGY"
assert a["RSCL_origin_search"] == "STOP"
assert a["Einstein_or_ADM_residual_may_be_used_as_calibration_selector"] is False

assert s["status"]["scientific_breakthrough"] is False
assert s["next_gate"]["version"] == "v13.27"

print("V13_26_CHECKER_PASS")
