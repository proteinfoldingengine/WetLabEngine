
"""
discrete_memory_action_verifier.py

Verifier for DISCRETE_MEMORY_ACTION.md.

Goal:
Connect a block-level discrete memory action to the continuum coefficient
scales used in COEFFICIENT_DERIVATION.md and CONTINUUM_LIMIT.md.

Discrete prototype:
    S_mem_disc =
        sum_n 1/2 K_t (Lambda_{n+1} - Lambda_n)^2
      + sum_<ij> 1/2 K_x (Lambda_i - Lambda_j)^2
      + sum_n U(Lambda_n)

Continuum identification under lattice spacings dt, dx:
    mu_R^2 ~ K_U / K_t
    Z0 ~ K_x * dx^(2-d) / K_t-like normalization, simplified as K_x * dx^2 / dt^2 proxy
    m_R^2 = mu_R^2(1-a)
    R_* = b/(1-a)

This verifier is structural, not a full covariant coarse-graining proof.
It checks positivity, stability, and scaling consistency of the discrete-to-continuum map.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class DiscreteParams:
    a: float
    b: float
    K_t: float
    K_x: float
    K_U: float
    K_int: float
    dt: float
    dx: float


@dataclass(frozen=True)
class ContinuumScales:
    Lambda_star: float
    chi_star: float
    mu_R2: float
    Z0: float
    lambda0: float
    m_R2: float
    stable: bool


def derive_scales(p: DiscreteParams) -> ContinuumScales:
    if not (0 <= p.a < 1):
        raise ValueError("stable loading requires 0 <= a < 1")
    if not (p.b > 0):
        raise ValueError("b must be positive")
    if not (p.K_t > 0 and p.K_x >= 0 and p.K_U > 0 and p.K_int >= 0):
        raise ValueError("K_t, K_U must be positive; K_x, K_int nonnegative")
    if not (p.dt > 0 and p.dx > 0):
        raise ValueError("dt and dx must be positive")

    Lambda_star = p.b / (1 - p.a)
    chi_star = 1 / (1 + Lambda_star)

    # Simplified structural continuum scaling.
    # K_t normalizes time-like memory inertia.
    mu_R2 = p.K_U / p.K_t
    Z0 = (p.K_x / p.K_t) * (p.dx / p.dt) ** 2
    lambda0 = p.K_int / p.K_t
    m_R2 = mu_R2 * (1 - p.a)

    stable = (m_R2 > 0) and (Z0 >= 0) and (lambda0 >= 0) and (0 < chi_star < 1)

    return ContinuumScales(
        Lambda_star=Lambda_star,
        chi_star=chi_star,
        mu_R2=mu_R2,
        Z0=Z0,
        lambda0=lambda0,
        m_R2=m_R2,
        stable=stable,
    )


def classify_discrete_map(p: DiscreteParams, singular_cutoff: float = 1e8) -> Tuple[str, ContinuumScales | None]:
    try:
        c = derive_scales(p)
    except ValueError:
        return "HARD_FAIL", None

    values = [c.Lambda_star, c.mu_R2, c.Z0, c.lambda0, c.m_R2]
    if any((not np.isfinite(v)) or abs(v) > singular_cutoff for v in values):
        return "HARD_FAIL", c

    if not c.stable:
        return "HARD_FAIL", c

    # If K_x=0, the local potential remains stable but the gradient penalty vanishes.
    # That is not fatal for decoupling, but it is a soft warning for spatial coherence.
    if c.Z0 == 0:
        return "SOFT_FAIL", c

    return "PASS", c


def run_sweep(n_sweeps: int = 100000, seed: int = 17) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    chi_vals = []
    mu_vals = []
    z_vals = []
    lam_vals = []
    m_vals = []

    for _ in range(n_sweeps):
        a = float(rng.uniform(0, 0.995))
        b = float(10 ** rng.uniform(-3, 1))

        K_t = float(10 ** rng.uniform(-2, 2))
        K_x = float(10 ** rng.uniform(-3, 2))
        K_U = float(10 ** rng.uniform(-3, 2))
        K_int = float(10 ** rng.uniform(-4, 1))
        dt = float(10 ** rng.uniform(-1, 1))
        dx = float(10 ** rng.uniform(-1, 1))

        # Inject pathologies.
        roll = rng.random()
        if roll < 0.002:
            a = 1.0 + rng.uniform(0, 0.2)
        elif roll < 0.004:
            b = -rng.uniform(0.001, 1)
        elif roll < 0.006:
            K_t = -rng.uniform(0.1, 10)
        elif roll < 0.008:
            K_U = -rng.uniform(0.1, 10)
        elif roll < 0.010:
            K_x = 0.0

        label, c = classify_discrete_map(DiscreteParams(a, b, K_t, K_x, K_U, K_int, dt, dx))
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"} and c is not None:
            chi_vals.append(c.chi_star)
            mu_vals.append(c.mu_R2)
            z_vals.append(c.Z0)
            lam_vals.append(c.lambda0)
            m_vals.append(c.m_R2)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if chi_vals:
        out.update({
            "chi_median": float(np.median(chi_vals)),
            "mu_R2_median": float(np.median(mu_vals)),
            "Z0_median": float(np.median(z_vals)),
            "lambda0_median": float(np.median(lam_vals)),
            "m_R2_median": float(np.median(m_vals)),
            "chi_min": float(np.min(chi_vals)),
            "chi_max": float(np.max(chi_vals)),
        })
    return out


def main() -> None:
    print("Discrete memory action verifier")
    print("=" * 50)
    print("Continuum scale map:")
    print("mu_R^2 = K_U / K_t")
    print("Z0     = (K_x / K_t) * (dx / dt)^2")
    print("lambda0= K_int / K_t")
    print("m_R^2  = mu_R^2 * (1-a)")
    print()

    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
