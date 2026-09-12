import numpy as np
from .linalg import paulis, embed_local, embed_pair, hermitian_exp_normalized, hermitian_log, partial_trace


def default_edges():
    return [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (1, 4)]


def build_default_model(n=6, beta=0.72, source_scale=1.0):
    if n != 6:
        raise ValueError("default demo is frozen at n=6")
    _, X, Y, Z = paulis()
    edges = default_edges()
    H = np.zeros((2**n, 2**n), dtype=complex)
    Jx, Jy, Jz = 0.42, 0.37, 0.51
    for e, (i, j) in enumerate(edges):
        modulation = 1.0 + 0.07 * np.cos(0.9 * (e + 1))
        H += modulation * (
            Jx * embed_pair(X, i, X, j, n)
            + Jy * embed_pair(Y, i, Y, j, n)
            + Jz * embed_pair(Z, i, Z, j, n)
        )
    h = np.array([0.13, 0.08, 0.02, -0.03, -0.05, 0.01])
    for i in range(n):
        H += h[i] * embed_local(Z, i, n)
    rho0 = hermitian_exp_normalized(-beta * H)
    P = source_scale * (
        0.95 * embed_local(Z, 0, n)
        + 0.80 * embed_local(Z, 3, n)
        + 0.12 * embed_local(X, 0, n)
        - 0.08 * embed_local(X, 3, n)
    )
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    positions = np.c_[np.cos(angles), np.sin(angles)]
    return {
        "n": n,
        "beta": float(beta),
        "edges": edges,
        "H0": H,
        "rho0": rho0,
        "P": P,
        "positions": positions,
        "source_nodes": (0, 3),
    }


def state_from_logtilt(log_rho0, lam, P):
    return hermitian_exp_normalized(log_rho0 + float(lam) * P)


def state_at_lambda(model, lam):
    log_rho0 = hermitian_log(model["rho0"])
    return state_from_logtilt(log_rho0, lam, model["P"])


def one_site_reductions(rho, n):
    return [partial_trace(rho, [i], [2] * n) for i in range(n)]


def pair_reduction(rho, i, j, n):
    keep = sorted([i, j])
    out = partial_trace(rho, keep, [2] * n)
    if i <= j:
        return out
    s = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    return s @ out @ s.T


def pauli_expectations(rho1):
    _, X, Y, Z = paulis()
    return np.array([np.trace(rho1 @ a).real for a in (X, Y, Z)])


def logarithmic_mean(a, b, tol=1e-14):
    if abs(a - b) <= tol * max(1.0, abs(a), abs(b)):
        return 0.5 * (a + b)
    return (a - b) / (np.log(a) - np.log(b))


def bkm_covariance(rho, observables):
    h = (rho + rho.conj().T) / 2
    w, v = np.linalg.eigh(h)
    if w.min() <= 0:
        raise ValueError("BKM covariance requires faithful state")
    obs_eig = [v.conj().T @ a @ v for a in observables]
    means = np.array([np.trace(rho @ a).real for a in observables])
    L = np.empty((len(w), len(w)), dtype=float)
    for m in range(len(w)):
        for n in range(len(w)):
            L[m, n] = logarithmic_mean(float(w[m]), float(w[n]))
    K = np.zeros((len(observables), len(observables)), dtype=float)
    for a, A in enumerate(obs_eig):
        for b, B in enumerate(obs_eig):
            val = np.sum(L * A * B.T)
            K[a, b] = float(np.real(val)) - means[a] * means[b]
    return (K + K.T) / 2


def connected_correlation(pair_rho, rho_i, rho_j):
    _, X, Y, Z = paulis()
    ops = (X, Y, Z)
    ri = np.array([np.trace(rho_i @ a).real for a in ops])
    rj = np.array([np.trace(rho_j @ b).real for b in ops])
    C = np.zeros((3, 3), dtype=float)
    for a, A in enumerate(ops):
        for b, B in enumerate(ops):
            C[a, b] = np.trace(pair_rho @ np.kron(A, B)).real - ri[a] * rj[b]
    return C
