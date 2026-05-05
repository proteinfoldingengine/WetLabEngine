
"""
micro_to_block_action_verifier.py

Verifier for MICRO_TO_BLOCK_ACTION.md.

Goal:
Test a first structural map from microscopic retained-memory/pruning parameters
to block-level memory-action constants:

    K_t, K_U, K_x, K_int

This verifier is not a proof of the microscopic law. It checks whether the
candidate map is internally stable and produces admissible block constants over
reasonable parameter ranges.

Candidate microscopic inputs:
    alpha_s, alpha_f: slow/fast memory persistence
    beta_s, beta_f: slow/fast innovation injection weights
    w_s, w_f: slow/fast sector weights
    c_s, c_f: closure fractions
    mu_G: geometry persistence
    I_s, I_f: stationary slow/fast innovation statistics
    epsilon_star: pruning threshold
    sigma_neighbor: neighbor-block loading mismatch scale
    rho_mat: matter-source loading strength

Candidate block constants:
    K_t   ~ 1 + memory inertia from persistence
    K_U   ~ (1-a) * K_t
    K_x   ~ sigma_neighbor^2 * K_t * overlap envelope
    K_int ~ rho_mat * K_t * coupling envelope
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class MicroParams:
    alpha_s: float
    alpha_f: float
    beta_s: float
    beta_f: float
    w_s: float
    w_f: float
    c_s: float
    c_f: float
    mu_G: float
    I_s: float
    I_f: float
    G_star: float
    sigma_neighbor: float
    rho_mat: float


@dataclass(frozen=True)
class BlockConstants:
    a: float
    b: float
    Lambda_star: float
    chi_star: float
    K_t: float
    K_U: float
    K_x: float
    K_int: float
    stable: bool


def normalize_pair(x: float, y: float) -> Tuple[float, float]:
    total = x + y
    if total <= 0:
        raise ValueError("pair cannot be normalized")
    return x / total, y / total


def derive_block_constants(p: MicroParams) -> BlockConstants:
    if not (0 <= p.alpha_s < 1 and 0 <= p.alpha_f < 1):
        raise ValueError("alpha_s and alpha_f must be in [0,1)")
    if not (p.beta_s >= 0 and p.beta_f >= 0):
        raise ValueError("beta values must be nonnegative")
    if not (p.mu_G > 0 and p.G_star > 0):
        raise ValueError("mu_G and G_star must be positive")
    if not (p.I_s >= 0 and p.I_f >= 0):
        raise ValueError("innovation statistics must be nonnegative")
    if not (p.sigma_neighbor >= 0 and p.rho_mat >= 0):
        raise ValueError("sigma_neighbor and rho_mat must be nonnegative")

    w_s, w_f = normalize_pair(p.w_s, p.w_f)
    c_s, c_f = normalize_pair(p.c_s, p.c_f)

    a = (w_s * p.alpha_s * c_s + w_f * p.alpha_f * c_f) / p.mu_G
    b = (w_s * p.beta_s * p.I_s + w_f * p.beta_f * p.I_f) / (p.mu_G * p.G_star)

    if not (0 <= a < 1 and b > 0):
        raise ValueError("derived loading map is not stable/physical")

    Lambda_star = b / (1 - a)
    chi_star = 1 / (1 + Lambda_star)
    overlap = chi_star * (1 - chi_star)

    # Candidate block constants.
    # K_t: persistence-induced memory inertia. Larger retained persistence means larger inertia.
    persistence_load = w_s * p.alpha_s + w_f * p.alpha_f
    K_t = 1.0 + persistence_load

    # K_U: restoring stiffness tied to stability margin.
    K_U = K_t * (1 - a)

    # K_x: local neighbor coherence penalty.
    K_x = K_t * overlap * p.sigma_neighbor**2

    # K_int: matter loading coupling.
    K_int = K_t * overlap * p.rho_mat

    stable = (
        K_t > 0
        and K_U > 0
        and K_x >= 0
        and K_int >= 0
        and 0 < chi_star < 1
    )

    return BlockConstants(a, b, Lambda_star, chi_star, K_t, K_U, K_x, K_int, stable)


def classify_micro(p: MicroParams, singular_cutoff: float = 1e8) -> Tuple[str, BlockConstants | None]:
    try:
        b = derive_block_constants(p)
    except ValueError:
        return "HARD_FAIL", None

    vals = [b.a, b.b, b.Lambda_star, b.chi_star, b.K_t, b.K_U, b.K_x, b.K_int]
    if any((not np.isfinite(v)) or abs(v) > singular_cutoff for v in vals):
        return "HARD_FAIL", b

    if not b.stable:
        return "HARD_FAIL", b

    if b.K_x == 0:
        return "SOFT_FAIL", b

    return "PASS", b


def run_sweep(n_sweeps: int = 100000, seed: int = 23) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    a_vals, b_vals, chi_vals = [], [], []
    Kt_vals, KU_vals, Kx_vals, Ki_vals = [], [], [], []

    for _ in range(n_sweeps):
        p = MicroParams(
            alpha_s=float(rng.uniform(0.0, 0.98)),
            alpha_f=float(rng.uniform(0.0, 0.98)),
            beta_s=float(10 ** rng.uniform(-3, 1)),
            beta_f=float(10 ** rng.uniform(-3, 1)),
            w_s=float(rng.uniform(0.05, 1.0)),
            w_f=float(rng.uniform(0.05, 1.0)),
            c_s=float(rng.uniform(0.05, 1.0)),
            c_f=float(rng.uniform(0.05, 1.0)),
            mu_G=float(rng.uniform(0.25, 2.0)),
            I_s=float(10 ** rng.uniform(-3, 0.5)),
            I_f=float(10 ** rng.uniform(-3, 0.5)),
            G_star=float(10 ** rng.uniform(-1, 1)),
            sigma_neighbor=float(10 ** rng.uniform(-3, 0.5)),
            rho_mat=float(10 ** rng.uniform(-4, 0.5)),
        )

        # Inject pathologies.
        roll = rng.random()
        if roll < 0.002:
            p = MicroParams(**{**p.__dict__, "mu_G": -1.0})
        elif roll < 0.004:
            p = MicroParams(**{**p.__dict__, "alpha_s": 1.05})
        elif roll < 0.006:
            p = MicroParams(**{**p.__dict__, "G_star": -1.0})
        elif roll < 0.008:
            p = MicroParams(**{**p.__dict__, "sigma_neighbor": 0.0})

        label, bc = classify_micro(p)
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"} and bc is not None:
            a_vals.append(bc.a)
            b_vals.append(bc.b)
            chi_vals.append(bc.chi_star)
            Kt_vals.append(bc.K_t)
            KU_vals.append(bc.K_U)
            Kx_vals.append(bc.K_x)
            Ki_vals.append(bc.K_int)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if chi_vals:
        out.update({
            "a_median": float(np.median(a_vals)),
            "b_median": float(np.median(b_vals)),
            "chi_median": float(np.median(chi_vals)),
            "chi_min": float(np.min(chi_vals)),
            "chi_max": float(np.max(chi_vals)),
            "K_t_median": float(np.median(Kt_vals)),
            "K_U_median": float(np.median(KU_vals)),
            "K_x_median": float(np.median(Kx_vals)),
            "K_int_median": float(np.median(Ki_vals)),
        })
    return out


def main() -> None:
    print("Micro-to-block action verifier")
    print("=" * 50)
    print("Candidate map:")
    print("a     = (w_s alpha_s c_s + w_f alpha_f c_f) / mu_G")
    print("b     = (w_s beta_s I_s + w_f beta_f I_f) / (mu_G G_star)")
    print("K_t   = 1 + w_s alpha_s + w_f alpha_f")
    print("K_U   = K_t * (1-a)")
    print("K_x   = K_t * chi*(1-chi) * sigma_neighbor^2")
    print("K_int = K_t * chi*(1-chi) * rho_mat")
    print()

    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
