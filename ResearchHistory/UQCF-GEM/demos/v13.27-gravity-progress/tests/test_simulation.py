from uqcf_demo.simulation import run_telemetry, telemetry_hash, default_config
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


def test_claim_ledger_keeps_gravity_boundary_open():
    ledger = claim_ledger()
    states = {x["name"]: x["status"] for x in ledger}
    assert states["finite BKM/polar metric-affine geometry"] == "DERIVED"
    assert states["response-selected current witness"] == "CONDITIONAL"
    assert states["RGCL source-to-coframe coupling magnitude"] == "MISSING_LAW"
    assert states["physical Einstein closure"] == "MISSING_LAW"
