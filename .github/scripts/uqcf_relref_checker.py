"""INDEPENDENT CHECKER: numerical optimum over invariant effects.

Does not import the producer and uses no block, swap or Schur-Weyl structure. The symmetry
is given only as: block sizes of A (to build generators of U(A)) and, for each tensor
factor, a group label; factors sharing a label are acted on by the same group element.
"""
import numpy as np

RANK_CUTOFF = 1e-9


def lie_basis(dims):
    """Orthonormal real basis of block-diagonal anti-Hermitian matrices (Lie algebra of U(A))."""
    n = sum(dims)
    basis, start = [], 0
    for b in dims:
        idx = list(range(start, start + b))
        for p in idx:
            m = np.zeros((n, n), dtype=complex)
            m[p, p] = 1j
            basis.append(m)
        for i, p in enumerate(idx):
            for q in idx[i + 1:]:
                m = np.zeros((n, n), dtype=complex)
                m[p, q], m[q, p] = 1, -1
                basis.append(m / np.sqrt(2))
                m = np.zeros((n, n), dtype=complex)
                m[p, q], m[q, p] = 1j, 1j
                basis.append(m / np.sqrt(2))
        start += b
    return basis


def generators(dims, labels):
    n = sum(dims)
    eye = np.eye(n, dtype=complex)
    gens = []
    for label in sorted(set(labels)):
        for x in lie_basis(dims):
            total = 0
            for f, lab in enumerate(labels):
                factors = [x if g == f else eye for g in range(len(labels))]
                term = factors[0]
                for fac in factors[1:]:
                    term = np.kron(term, fac)
                if lab == label:
                    total = total + term
            gens.append(total)
    return gens


def commutant(dims, labels):
    gens = generators(dims, labels)
    d = gens[0].shape[0]
    eye = np.eye(d, dtype=complex)
    stacked = np.vstack([np.kron(eye, g.T) - np.kron(g, eye) for g in gens])  # row-major vec of M g - g M
    _, sv, vh = np.linalg.svd(stacked, full_matrices=True)
    sv = np.concatenate([sv, np.zeros(d * d - len(sv))])
    v = vh.conj().T
    cut = RANK_CUTOFF * sv.max()
    null = sv <= cut
    gap = float(sv[~null].min()) if (~null).any() else None
    basis = [v[:, k].reshape(d, d) for k in np.where(null)[0]]
    return basis, gens, {'dimension': len(basis), 'smallest_nonzero_singular_value': gap,
                         'largest_null_singular_value': float(sv[null].max()) if null.any() else None}


def optimum(basis, contrast):
    """max over invariant 0<=E<=I of Tr[E D] = Tr[(E_C D)_+] (HS projection onto the commutant)."""
    proj = sum(np.vdot(b, contrast) * b for b in basis)
    proj = 0.5 * (proj + proj.conj().T)
    w = np.linalg.eigvalsh(proj)
    return float(w[w > 0].sum())


def commutes(effect, gens, tol=1e-9):
    return max(float(np.abs(effect @ g - g @ effect).max()) for g in gens) <= tol


def value(effect, contrast):
    return float(np.trace(effect @ contrast).real)
