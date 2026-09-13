import numpy as np


def paulis():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    return I, X, Y, Z


def kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def embed_local(op, site, n):
    I = np.eye(2, dtype=complex)
    return kron_all([op if k == site else I for k in range(n)])


def embed_pair(op_i, i, op_j, j, n):
    if i == j:
        raise ValueError("pair sites must differ")
    I = np.eye(2, dtype=complex)
    ops = []
    for k in range(n):
        if k == i:
            ops.append(op_i)
        elif k == j:
            ops.append(op_j)
        else:
            ops.append(I)
    return kron_all(ops)


def hermitian_exp(a):
    w, v = np.linalg.eigh((a + a.conj().T) / 2)
    w0 = w.max()
    ew = np.exp(w - w0)
    return (v * ew) @ v.conj().T, float(w0)


def hermitian_exp_normalized(a):
    e, _ = hermitian_exp(a)
    tr = np.trace(e).real
    if not np.isfinite(tr) or tr <= 0:
        raise ValueError("non-positive normalization")
    return e / tr


def hermitian_log(a, floor=1e-15):
    h = (a + a.conj().T) / 2
    w, v = np.linalg.eigh(h)
    if w.min() <= 0:
        if w.min() < -1e-12:
            raise ValueError("matrix is not positive semidefinite")
        w = np.maximum(w, floor)
    return (v * np.log(np.maximum(w, floor))) @ v.conj().T


def partial_trace(rho, keep, dims):
    keep = tuple(sorted(keep))
    n = len(dims)
    if rho.shape != (int(np.prod(dims)), int(np.prod(dims))):
        raise ValueError("rho shape does not match dims")
    arr = rho.reshape(tuple(dims) + tuple(dims))
    current_dims = list(dims)
    traced = [i for i in range(n) if i not in keep]
    for idx in sorted(traced, reverse=True):
        m = len(current_dims)
        arr = np.trace(arr, axis1=idx, axis2=idx + m)
        current_dims.pop(idx)
    d = int(np.prod(current_dims))
    return arr.reshape((d, d))


def raw_orthogonal_polar(c):
    u, _, vh = np.linalg.svd(np.asarray(c, dtype=float), full_matrices=False)
    return u @ vh


def proper_orthogonal_polar(c):
    u, _, vh = np.linalg.svd(np.asarray(c, dtype=float), full_matrices=False)
    o = u @ vh
    if np.linalg.det(o) < 0:
        u[:, -1] *= -1
        o = u @ vh
    return o


def so3_angle_audit(o):
    raw = float((np.trace(o) - 1.0) / 2.0)
    clipped = float(np.clip(raw, -1.0, 1.0))
    return {
        "raw_cos_argument": raw,
        "clipped_cos_argument": clipped,
        "clip_excess": float(abs(raw - clipped)),
        "angle": float(np.arccos(clipped)),
    }


def so3_angle(o):
    return so3_angle_audit(o)["angle"]


def symmetric_sqrt(a):
    w, v = np.linalg.eigh((a + a.T) / 2)
    w = np.maximum(w, 0.0)
    return (v * np.sqrt(w)) @ v.T
