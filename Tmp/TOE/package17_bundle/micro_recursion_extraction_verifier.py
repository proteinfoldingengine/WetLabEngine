
"""
micro_recursion_extraction_verifier.py

Verifier for MICRO_RECURSION_EXTRACTION.md.

Goal:
Given a candidate two-mode recursion in normalized affine form,

    R_{n+1} = a_R R_n + b_R A_n + c_R O_n + d_R + sigma_R xi_n
    A_{n+1} = a_A A_n + b_A R_n + d_A + sigma_A zeta_n

extract:
    k_R = (1 - a_R) / dt
    D_R = sigma_R^2 / (2 dt)
    lambda_micro = c_R / dt
    R_star from fixed point when O=0

and check whether extracted coefficients feed the coefficient map:

    Z_R = 1/(2D_R)
    m_R^2 = k_R/D_R
    lambda_int = lambda_micro/D_R

This verifier uses explicit affine recursion candidates.
It does not prove the production recursion unless real coefficients are supplied.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RecursionParams:
    a_R: float
    b_R: float
    c_R: float
    d_R: float
    sigma_R: float
    a_A: float
    b_A: float
    d_A: float
    sigma_A: float
    dt: float = 1.0


@dataclass(frozen=True)
class ExtractionResult:
    k_R: float
    D_R: float
    lambda_micro: float
    R_star: float
    A_star: float
    Z_R: float
    m_R2: float
    lambda_int: float
    stable_spectral_radius: float
    finite_fraction: float
    stable: bool


def fixed_point(p: RecursionParams):
    # Solve x = Mx + d for O=0.
    M = np.array([[p.a_R, p.b_R], [p.b_A, p.a_A]], dtype=float)
    d = np.array([p.d_R, p.d_A], dtype=float)
    A = np.eye(2) - M
    try:
        x = np.linalg.solve(A, d)
        return float(x[0]), float(x[1])
    except np.linalg.LinAlgError:
        return np.nan, np.nan


def extract(p: RecursionParams):
    k_R = (1.0 - p.a_R) / p.dt
    D_R = (p.sigma_R ** 2) / (2.0 * p.dt)
    lambda_micro = p.c_R / p.dt
    R_star, A_star = fixed_point(p)

    if D_R <= 0:
        Z_R = np.nan
        m_R2 = np.nan
        lambda_int = np.nan
    else:
        Z_R = 1.0 / (2.0 * D_R)
        m_R2 = k_R / D_R
        lambda_int = lambda_micro / D_R

    M = np.array([[p.a_R, p.b_R], [p.b_A, p.a_A]], dtype=float)
    try:
        rho = float(np.max(np.abs(np.linalg.eigvals(M))))
    except np.linalg.LinAlgError:
        rho = np.nan

    vals = np.array([k_R, D_R, lambda_micro, R_star, A_star, Z_R, m_R2, lambda_int, rho])
    finite_fraction = float(np.mean(np.isfinite(vals)))

    stable = bool(
        finite_fraction == 1.0
        and rho < 1.0
        and k_R > 0
        and D_R > 0
        and m_R2 > 0
        and abs(lambda_int) < 1e6
    )

    return ExtractionResult(
        k_R=k_R,
        D_R=D_R,
        lambda_micro=lambda_micro,
        R_star=R_star,
        A_star=A_star,
        Z_R=Z_R,
        m_R2=m_R2,
        lambda_int=lambda_int,
        stable_spectral_radius=rho,
        finite_fraction=finite_fraction,
        stable=stable,
    )


def classify(p):
    r = extract(p)
    if r.finite_fraction < 1.0:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=10000, seed=1511):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "k_R", "D_R", "lambda_micro", "R_star", "A_star",
        "Z_R", "m_R2", "lambda_int", "stable_spectral_radius", "finite_fraction"
    ]}

    for _ in range(n_sweeps):
        # Stable-biased affine recursion samples.
        a_R = float(rng.uniform(0.01, 0.99))
        a_A = float(rng.uniform(0.01, 0.99))
        b_R = float(rng.normal(0, 0.08))
        b_A = float(rng.normal(0, 0.08))
        c_R = float(rng.normal(0.05, 0.2))
        d_R = float(rng.normal(0, 0.2))
        d_A = float(rng.normal(0, 0.2))
        sigma_R = float(10 ** rng.uniform(-2, 0))
        sigma_A = float(10 ** rng.uniform(-2, 0))
        dt = float(10 ** rng.uniform(-2, 0))

        # Inject some known pathologies.
        roll = rng.random()
        if roll < 0.02:
            sigma_R = 0.0
        elif roll < 0.05:
            a_R = float(rng.uniform(1.0, 1.5))
        elif roll < 0.08:
            b_R = float(rng.uniform(0.8, 1.5))
            b_A = float(rng.uniform(0.8, 1.5))

        p = RecursionParams(a_R, b_R, c_R, d_R, sigma_R, a_A, b_A, d_A, sigma_A, dt)
        label, r = classify(p)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Micro recursion extraction verifier")
    print("=" * 50)
    print("Route:")
    print("affine two-mode recursion -> k_R, D_R, lambda_micro -> Z_R, V, lambda_int")
    print("This validates extraction mechanics; production recursion still required.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
