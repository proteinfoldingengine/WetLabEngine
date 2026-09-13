import copy

from uqcf_demo.simulation import (
    run_telemetry,
    telemetry_hash,
    scientific_fingerprint,
    default_config,
)
from uqcf_demo.ledger import claim_ledger


def test_telemetry_is_deterministic_and_sensitive_to_source_scale():
    cfg = default_config(frames=5)
    a = run_telemetry(cfg)
    b = run_telemetry(cfg)
    assert telemetry_hash(a) == telemetry_hash(b)
    cfg2 = default_config(frames=5)
    cfg2["source_scale"] = 1.17
    c = run_telemetry(cfg2)
    assert telemetry_hash(a) != telemetry_hash(c)


def test_telemetry_structural_controls_pass():
    data = run_telemetry(default_config(frames=5))
    summary = data["summary"]
    assert summary["max_source_balance_residual"] < 1e-10
    assert summary["max_projective_direction_change"] < 1e-10
    assert summary["min_state_eigenvalue"] > 0
    assert summary["min_bkm_eigenvalue"] > -1e-9
    assert summary["dewitt_pure_trace_control"] < 0
    assert summary["dewitt_traceless_control"] >= -1e-10
    assert "toy_block_underdetermination_distance" in summary
    assert "tensor_completion_spatial_stress_distance" not in summary


def test_scientific_fingerprint_ignores_machine_epsilon_drift_but_not_physics():
    data = run_telemetry(default_config(frames=5))
    baseline = scientific_fingerprint(data)

    drifted = copy.deepcopy(data)
    drifted["summary"]["max_source_balance_residual"] += 3e-16
    drifted["summary"]["max_projective_direction_change"] += 2e-16
    drifted["summary"]["pgrl_reparameterization_error"] += 4e-16
    drifted["summary"]["min_bkm_eigenvalue"] += 8e-16
    drifted["summary"]["max_qmar_jet_norm"] -= 5e-14
    assert scientific_fingerprint(drifted) == baseline

    changed = copy.deepcopy(data)
    changed["summary"]["max_qmar_jet_norm"] += 0.1
    assert scientific_fingerprint(changed) != baseline


def test_claim_ledger_uses_rescoped_labels_and_keeps_gravity_boundary_open():
    ledger = claim_ledger()
    states = {x["name"]: x["status"] for x in ledger}
    assert states["finite BKM/polar relational geometry"] == "DERIVED"
    assert states["response-selected current witness"] == "CONDITIONAL"
    assert states["represented q=A^-1 DeWitt-like sign diagnostic"] == "CONDITIONAL"
    assert states["RGCL source-to-coframe coupling magnitude"] == "MISSING_LAW"
    assert states["physical Einstein closure"] == "MISSING_LAW"
    assert "represented q=A^-1 ADM-like sector" not in states
    assert "full spatial-stress completion" not in states
