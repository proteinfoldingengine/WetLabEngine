import numpy as np
from uqcf_demo.linalg import proper_orthogonal_polar, so3_angle
from uqcf_demo.quantum import build_default_model, state_at_lambda
from uqcf_demo.geometry import geometry_snapshot, finite_difference_geometry_jet


def test_proper_polar_is_so3():
    c = np.array([[0.2, -0.1, 0.3], [0.4, 0.7, -0.2], [-0.3, 0.1, 0.5]])
    o = proper_orthogonal_polar(c)
    assert np.allclose(o.T @ o, np.eye(3), atol=1e-12)
    assert abs(np.linalg.det(o) - 1.0) < 1e-12


def test_identity_rotation_has_zero_angle():
    assert so3_angle(np.eye(3)) < 1e-12


def test_geometry_snapshot_has_symmetric_nonmetricity_and_cycles():
    model = build_default_model()
    rho = state_at_lambda(model, 0.15)
    snap = geometry_snapshot(model, rho)
    assert len(snap["edges"]) == len(model["edges"])
    for edge in snap["edges"]:
        assert np.allclose(edge["M"], edge["M"].T, atol=1e-12)
        assert np.allclose(edge["O"].T @ edge["O"], np.eye(3), atol=1e-10)
    assert len(snap["cycles"]) >= 2
    assert all(0.0 <= c["angle"] <= np.pi for c in snap["cycles"])


def test_finite_difference_geometry_jet_is_finite():
    model = build_default_model()
    jet = finite_difference_geometry_jet(model, 0.1, delta=1e-4)
    assert np.isfinite(jet["mean_dM_norm"])
    assert np.isfinite(jet["mean_dO_norm"])
    assert jet["mean_dM_norm"] >= 0
