import numpy as np


def incidence_matrix(n, edges):
    B = np.zeros((n, len(edges)), dtype=float)
    for e, (i, j) in enumerate(edges):
        B[i, e] = -1.0
        B[j, e] = +1.0
    return B


def balanced_source(raw):
    raw = np.asarray(raw, dtype=float)
    return raw - np.mean(raw)


def cycle_basis(B, tol=1e-12):
    _, s, vh = np.linalg.svd(B, full_matrices=True)
    rank = int(np.sum(s > tol * max(B.shape) * (s[0] if len(s) else 1.0)))
    return vh[rank:].T.copy()


def minimum_norm_current(B, s):
    return np.linalg.pinv(B) @ np.asarray(s, dtype=float)


def conditional_response_selected_current(B, s, edge_response, weights=None):
    s = np.asarray(s, dtype=float)
    y = np.asarray(edge_response, dtype=float)
    J0 = minimum_norm_current(B, s)
    Z = cycle_basis(B)
    if weights is None:
        weights = np.ones(B.shape[1])
    R = np.diag(np.asarray(weights, dtype=float))
    if Z.shape[1] == 0:
        return {
            "J": J0,
            "J0": J0,
            "Z": Z,
            "cycle_dim": 0,
            "cycle_rank": 0,
            "response_residual": float(np.linalg.norm(R @ J0 - y)),
        }
    A = R @ Z
    rhs = y - R @ J0
    coeff, *_ = np.linalg.lstsq(A, rhs, rcond=None)
    J = J0 + Z @ coeff
    return {
        "J": J,
        "J0": J0,
        "Z": Z,
        "cycle_coeff": coeff,
        "cycle_dim": int(Z.shape[1]),
        "cycle_rank": int(np.linalg.matrix_rank(A, tol=1e-10)),
        "response_residual": float(np.linalg.norm(R @ J - y)),
    }


def projective_direction(x, tol=1e-15):
    x = np.asarray(x, dtype=float)
    n = float(np.linalg.norm(x))
    if n <= tol:
        return np.zeros_like(x)
    return x / n


def projective_scale_control(x, scales=(0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0)):
    ref = projective_direction(x)
    errs = [float(np.linalg.norm(projective_direction(a * x) - ref)) for a in scales]
    return {"scales": list(map(float, scales)), "max_direction_change": max(errs, default=0.0)}
