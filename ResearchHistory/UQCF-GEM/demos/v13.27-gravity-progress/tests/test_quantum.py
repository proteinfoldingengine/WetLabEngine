import numpy as np
from uqcf_demo.linalg import partial_trace, hermitian_log, paulis
from uqcf_demo.quantum import build_default_model, state_at_lambda, state_from_logtilt, one_site_reductions, bkm_covariance


def test_density_matrix_is_faithful_trace_one_and_hermitian():
    model = build_default_model()
    rho = state_at_lambda(model, 0.31)
    assert np.allclose(rho, rho.conj().T, atol=1e-12)
    assert abs(np.trace(rho).real - 1.0) < 1e-12
    assert np.linalg.eigvalsh(rho).min() > 0.0


def test_partial_trace_preserves_trace_and_dimensions():
    model = build_default_model()
    rho = state_at_lambda(model, 0.0)
    reduced = partial_trace(rho, keep=[0, 3], dims=[2] * model["n"])
    assert reduced.shape == (4, 4)
    assert abs(np.trace(reduced).real - 1.0) < 1e-12


def test_bkm_covariance_is_symmetric_psd():
    model = build_default_model()
    rho = state_at_lambda(model, 0.2)
    singles = one_site_reductions(rho, model["n"])
    _, X, Y, Z = paulis()
    K = bkm_covariance(singles[2], [X, Y, Z])
    assert np.allclose(K, K.T, atol=1e-12)
    assert np.linalg.eigvalsh(K).min() > -1e-11


def test_pgrl_reparameterization_is_exact():
    model = build_default_model()
    log_rho0 = hermitian_log(model["rho0"])
    lam = 0.37
    a = 4.2
    r1 = state_from_logtilt(log_rho0, lam, model["P"])
    r2 = state_from_logtilt(log_rho0, lam / a, a * model["P"])
    assert np.linalg.norm(r1 - r2, ord="fro") < 1e-12
