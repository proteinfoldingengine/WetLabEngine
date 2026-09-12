import numpy as np
from uqcf_demo.quantum import build_default_model, state_at_lambda
from uqcf_demo.geometry import geometry_snapshot
from uqcf_demo.source_current import incidence_matrix, cycle_basis, balanced_source, minimum_norm_current, projective_direction, conditional_response_selected_current
from uqcf_demo.adm import represented_q, dewitt_diagnostic, dewitt_controls


def test_incidence_balance_and_cycle_nullspace():
    model = build_default_model()
    B = incidence_matrix(model["n"], model["edges"])
    raw = np.array([0.8, -0.1, 0.2, -0.7, 0.15, -0.35])
    s = balanced_source(raw)
    J = minimum_norm_current(B, s)
    Z = cycle_basis(B)
    assert np.linalg.norm(B @ J - s) < 1e-12
    assert np.linalg.norm(B @ Z) < 1e-12
    assert Z.shape[1] == len(model["edges"]) - (model["n"] - 1)


def test_projective_direction_is_scale_invariant():
    x = np.array([1.0, -2.0, 3.5, 0.2])
    d = projective_direction(x)
    for a in (0.1, 0.5, 2.0, 11.0):
        assert np.linalg.norm(projective_direction(a * x) - d) < 1e-12


def test_conditional_response_selection_preserves_balance():
    model = build_default_model()
    B = incidence_matrix(model["n"], model["edges"])
    s = balanced_source(np.array([0.7, -0.2, 0.1, -0.4, 0.25, -0.45]))
    y = np.linspace(-0.3, 0.4, len(model["edges"]))
    weights = np.linspace(1.0, 2.0, len(model["edges"]))
    out = conditional_response_selected_current(B, s, y, weights)
    assert np.linalg.norm(B @ out["J"] - s) < 1e-12
    assert out["cycle_rank"] == out["cycle_dim"]


def test_dewitt_trace_sign_controls():
    model = build_default_model()
    snap = geometry_snapshot(model, state_at_lambda(model, 0.05))
    q = represented_q(snap["metrics"][0])
    ctrl = dewitt_controls(q)
    assert ctrl["pure_trace"] < 0.0
    assert ctrl["traceless"] > -1e-12
    assert dewitt_diagnostic(q, q) < 0.0
