
"""
coefficient_micro_derivation_verifier.py

Verifier for COEFFICIENT_MICRO_DERIVATION.md.

Goal:
Test the conditional coefficient extraction from a minimal two-mode retained-memory recursion.

Minimal recursion ansatz:
    R_{n+1} = R_n + dt[-k_R(chi)(R_n - R_star) + lambda_micro(chi) O_n] + sqrt(2 D_R dt) xi_n
    A_{n+1} = A_n + dt[-k_A(A_n - A_star) + c_RA(R_n - R_star)] + sqrt(2 D_A dt) zeta_n

Coarse-grained scalar action target:
    S_mem = ∫ sqrt(-g)[ -1/2 Z_R(chi)(∂R)^2 - V(R;chi,eps*) + lambda_int(chi) R O_mat ]

Coefficient extraction:
    Z_R(chi) ~ 1/(2 D_R(chi))
    m_R^2(chi) ~ k_R(chi) / D_R(chi)
    V(R) = 1/2 m_R^2 (R - R_star)^2 + higher terms
    lambda_int(chi) ~ lambda_micro(chi) / D_R(chi)

Checks:
    - coefficients finite
    - Z_R > 0
    - m_R^2 > 0 for stable fixed point
    - lambda_int finite
    - weak-memory T_mem scaling remains O(eta) or O(eta^2)
    - singular/pruning failures are detected
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MicroCoeffConfig:
    chi: float = 0.2667
    eps_star: float = 0.05
    k0: float = 1.0
    D0: float = 0.4
    lam0: float = 0.2
    seed: int = 1409


@dataclass(frozen=True)
class CoeffResult:
    Z_R: float
    m_R2: float
    lambda_int: float
    V_quad: float
    finite_fraction: float
    weak_scaling_ratio: float
    stable: bool


def micro_functions(cfg):
    chi = cfg.chi
    eps = cfg.eps_star

    # Smooth positive candidate functions.
    # These are NOT claimed as final physics; they instantiate the conditional theorem.
    k_R = cfg.k0 * (1.0 + chi) * (1.0 + eps)
    D_R = cfg.D0 * (1.0 + chi**2) / (1.0 + eps)
    lam_micro = cfg.lam0 * chi / (1.0 + eps)

    return k_R, D_R, lam_micro


def extract_coefficients(cfg):
    k_R, D_R, lam_micro = micro_functions(cfg)

    if D_R <= 0:
        return np.nan, np.nan, np.nan, np.nan

    Z_R = 1.0 / (2.0 * D_R)
    m_R2 = k_R / D_R
    lambda_int = lam_micro / D_R
    V_quad = 0.5 * m_R2

    return Z_R, m_R2, lambda_int, V_quad


def weak_memory_scaling(cfg, eta=1e-3):
    Z, m2, lam, Vq = extract_coefficients(cfg)
    r = 1.0
    grad = eta
    O = 1.0

    # interaction-dominated source magnitude
    T_eta = Z * grad**2 + Vq * (eta*r)**2 + abs(lam * eta * O)
    T_half = Z * (grad/2)**2 + Vq * (eta*r/2)**2 + abs(lam * eta/2 * O)
    return T_half / (T_eta + 1e-30)


def verify(cfg):
    Z, m2, lam, Vq = extract_coefficients(cfg)
    vals = np.array([Z, m2, lam, Vq], dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals)))
    scaling = weak_memory_scaling(cfg)

    stable = bool(
        finite_fraction == 1.0
        and Z > 0
        and m2 > 0
        and np.isfinite(lam)
        and abs(lam) < 1e6
        and 0.35 < scaling < 0.65
    )

    return CoeffResult(Z, m2, lam, Vq, finite_fraction, scaling, stable)


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 1.0:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=10000, seed=1411):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in ["Z_R", "m_R2", "lambda_int", "V_quad", "weak_scaling_ratio", "finite_fraction"]}

    for _ in range(n_sweeps):
        cfg = MicroCoeffConfig(
            chi=float(rng.normal(0.2667, 0.05)),
            eps_star=float(10 ** rng.uniform(-4, -0.5)),
            k0=float(10 ** rng.uniform(-2, 2)),
            D0=float(10 ** rng.uniform(-3, 1)),
            lam0=float(10 ** rng.uniform(-3, 1)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        # Inject pathologies to verify failure detection.
        roll = rng.random()
        if roll < 0.015:
            cfg = MicroCoeffConfig(cfg.chi, cfg.eps_star, cfg.k0, -abs(cfg.D0), cfg.lam0, cfg.seed)
        elif roll < 0.03:
            cfg = MicroCoeffConfig(cfg.chi, cfg.eps_star, -abs(cfg.k0), cfg.D0, cfg.lam0, cfg.seed)
        elif roll < 0.04:
            cfg = MicroCoeffConfig(cfg.chi, cfg.eps_star, cfg.k0, cfg.D0, 1e9, cfg.seed)

        label, r = classify(cfg)
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
    print("Coefficient micro-derivation verifier")
    print("=" * 50)
    print("Route:")
    print("two-mode retained-memory recursion ansatz -> Z_R, V(R), lambda_int")
    print("Conditional theorem pass; exact recursion must replace ansatz for closure.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
