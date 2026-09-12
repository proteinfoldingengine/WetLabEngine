import numpy as np
from .linalg import symmetric_sqrt


def represented_q(K, regularizer=1e-6):
    K = np.asarray(K, dtype=float)
    A = (K + K.T) / 2 + float(regularizer) * np.eye(K.shape[0])
    return np.linalg.inv(A)


def dewitt_diagnostic(q, X):
    q = np.asarray(q, dtype=float)
    X = (np.asarray(X, dtype=float) + np.asarray(X, dtype=float).T) / 2
    qi = np.linalg.inv(q)
    tr_q = float(np.trace(qi @ X))
    X_tf = X - (tr_q / q.shape[0]) * q
    norm_tf = float(np.trace(qi @ X_tf @ qi @ X_tf))
    return norm_tf - 0.5 * tr_q**2


def dewitt_controls(q):
    q = np.asarray(q, dtype=float)
    root = symmetric_sqrt(q)
    pure_trace = q.copy()
    traceless = root @ np.diag([1.0, -1.0, 0.0]) @ root
    return {
        "pure_trace": float(dewitt_diagnostic(q, pure_trace)),
        "traceless": float(dewitt_diagnostic(q, traceless)),
    }
