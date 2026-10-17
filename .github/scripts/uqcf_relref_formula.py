"""PRODUCER for the relational-reference admission screen: claimed closed forms only.

Implements exactly the formulas stated in ADMISSION.md section 2 (Theorem B, Corollary)
and the predicted commutant dimension. It is never imported by the checker.
"""
import numpy as np


def block_slices(dims):
    out, start = [], 0
    for n in dims:
        out.append(slice(start, start + n))
        start += n
    return out


def t_formula(dims, rho0, rho1, sigma):
    delta = rho1 - rho0
    total = 0.0
    for s in block_slices(dims):
        total += abs(np.trace(delta[s, s] @ sigma[s, s]).real)
    return 0.5 * total


def t_wrong_no_block_abs(dims, rho0, rho1, sigma):
    """Rejecting-control formula W1: absolute value outside the block sum."""
    delta = rho1 - rho0
    return 0.5 * abs(sum(np.trace(delta[s, s] @ sigma[s, s]).real for s in block_slices(dims)))


def reader(dims, rho0, rho1, sigma, flip=False):
    """E* = sum_i (P_i x P_i)(I + s_i F_i)/2 on H x H (first factor source, second reference)."""
    n = sum(dims)
    delta = rho1 - rho0
    e = np.zeros((n * n, n * n), dtype=complex)
    for s in block_slices(dims):
        sign = np.sign(np.trace(delta[s, s] @ sigma[s, s]).real)
        if flip:
            sign = -sign
        idx = range(s.start, s.stop)
        for p in idx:
            for q in idx:
                a = p * n + q
                e[a, a] += 0.5
                e[q * n + p, a] += 0.5 * sign  # F_i |p q> = |q p>
    return e


def corollary_value(rho0, rho1):
    d = rho1 - rho0
    return 0.25 * float(np.sum(np.abs(d) ** 2))


def predicted_commutant_dim(dims):
    m = len(dims)
    return sum(2 if n >= 2 else 1 for n in dims) + 4 * (m * (m - 1) // 2)
