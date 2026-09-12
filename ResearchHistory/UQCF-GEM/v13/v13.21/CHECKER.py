#!/usr/bin/env python3
import json, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
p=json.loads((root/"RATS_FROZEN_PROTOCOL.json").read_text())
a=json.loads((root/"ARCHITECTURE_AUDIT.json").read_text())
s=json.loads((root/"SUMMARY.json").read_text())
assert p["phase"]=="v13.21"
assert p["governance"]["no_target_dependent_continuation"] is True
assert p["governance"]["minimum_nested_levels"]>=4
assert p["canonical_recovery"]["map"].startswith("faithful-state Petz")
assert set(["I_h","gamma_h","mu_h","epsilon_h","eta_h","Lambda_h"]).issubset(p["telemetry"])
assert p["v13_20_information_score"]["value_bounded"]=="alpha_min >= 2*beta_max + 2"
assert p["direct_telemetry_score"]["value_bounded"]=="p_epsilon_min >= 1"
assert p["direct_telemetry_score"]["jet_local_bounded"]=="p_eta_min >= 1"
assert p["direct_telemetry_score"]["jet_context_bounded"]=="p_epsilon_min + lambda_min >= 2"
assert a["execution_status"].startswith("BLOCKED_")
assert s["execution"]["refinement_telemetry_generated"] is False
assert s["execution"]["protocol_frozen"] is True
assert s["status"]["scientific_breakthrough"] is False
sha=hashlib.sha256((root/"RATS_FROZEN_PROTOCOL.json").read_bytes()).hexdigest()
assert sha==s["protocol_sha256"]
print("V13_21_PROTOCOL_CHECKER_PASS")
print("protocol_sha256 =", sha)
print("execution_status =", a["execution_status"])
