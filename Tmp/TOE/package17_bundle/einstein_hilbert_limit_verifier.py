
"""
einstein_hilbert_limit_verifier.py

Verifier for EINSTEIN_HILBERT_LIMIT.md.

Goal:
Test a controlled discrete-to-continuum action convergence:

    S_geom_disc = sum_cells sqrt(g_i) R_i dA
        -> S_cont = integral sqrt(g) R dA

Controlled 2D conformal metric:
    g_ij = exp(2 phi) delta_ij
    sqrt(g) = exp(2 phi)
    R = -2 exp(-2 phi) Laplacian(phi)

Therefore:
    sqrt(g) R = -2 Laplacian(phi)

On a periodic domain, integral Laplacian(phi) = 0.
That makes the raw EH-like action zero, which is a weak test.
So we also test absolute curvature action:
    A_abs = integral sqrt(g) |R|
and squared curvature diagnostic:
    A_R2 = integral sqrt(g) R^2

These are not Einstein-Hilbert itself, but they test discrete curvature-density convergence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class EHConfig:
    n: int = 64
    amp: float = 0.1
    kx: int = 2
    ky: int = 3
    noise: float = 0.0
    seed: int = 79


@dataclass(frozen=True)
class EHResult:
    n: int
    S_num: float
    S_exact: float
    S_abs_num: float
    S_abs_exact: float
    S_R2_num: float
    S_R2_exact: float
    rel_abs_error: float
    rel_R2_error: float
    stable: bool


def phi_field(X: np.ndarray, Y: np.ndarray, amp: float, kx: int, ky: int) -> np.ndarray:
    return amp * np.sin(2 * np.pi * kx * X) * np.sin(2 * np.pi * ky * Y)


def laplacian_phi_exact(X: np.ndarray, Y: np.ndarray, amp: float, kx: int, ky: int) -> np.ndarray:
    phi = phi_field(X, Y, amp, kx, ky)
    factor = -((2 * np.pi * kx) ** 2 + (2 * np.pi * ky) ** 2)
    return factor * phi


def periodic_laplacian(F: np.ndarray, dx: float, dy: float) -> np.ndarray:
    return (
        (np.roll(F, 1, axis=0) - 2 * F + np.roll(F, -1, axis=0)) / dx**2
        + (np.roll(F, 1, axis=1) - 2 * F + np.roll(F, -1, axis=1)) / dy**2
    )


def compute_action(cfg: EHConfig) -> EHResult:
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n
    x = np.linspace(0, 1, n, endpoint=False)
    y = np.linspace(0, 1, n, endpoint=False)
    dx = 1.0 / n
    dy = 1.0 / n
    dA = dx * dy
    X, Y = np.meshgrid(x, y, indexing="ij")

    phi_exact = phi_field(X, Y, cfg.amp, cfg.kx, cfg.ky)
    phi_num = phi_exact.copy()

    if cfg.noise > 0:
        phi_num = phi_num + rng.normal(0, cfg.noise, size=phi_num.shape)

    lap_num = periodic_laplacian(phi_num, dx, dy)
    lap_exact = laplacian_phi_exact(X, Y, cfg.amp, cfg.kx, cfg.ky)

    sqrtg_num = np.exp(2 * phi_num)
    sqrtg_exact = np.exp(2 * phi_exact)

    R_num = -2 * np.exp(-2 * phi_num) * lap_num
    R_exact = -2 * np.exp(-2 * phi_exact) * lap_exact

    # EH-like curvature density.
    S_num = float(np.sum(sqrtg_num * R_num) * dA)
    S_exact = float(np.sum(sqrtg_exact * R_exact) * dA)

    # Non-topological convergence diagnostics.
    S_abs_num = float(np.sum(sqrtg_num * np.abs(R_num)) * dA)
    S_abs_exact = float(np.sum(sqrtg_exact * np.abs(R_exact)) * dA)

    S_R2_num = float(np.sum(sqrtg_num * R_num**2) * dA)
    S_R2_exact = float(np.sum(sqrtg_exact * R_exact**2) * dA)

    rel_abs_error = abs(S_abs_num - S_abs_exact) / (abs(S_abs_exact) + 1e-12)
    rel_R2_error = abs(S_R2_num - S_R2_exact) / (abs(S_R2_exact) + 1e-12)

    stable = bool(np.isfinite(S_num) and rel_abs_error < 0.05 and rel_R2_error < 0.1)

    return EHResult(
        n=n,
        S_num=S_num,
        S_exact=S_exact,
        S_abs_num=S_abs_num,
        S_abs_exact=S_abs_exact,
        S_R2_num=S_R2_num,
        S_R2_exact=S_R2_exact,
        rel_abs_error=float(rel_abs_error),
        rel_R2_error=float(rel_R2_error),
        stable=stable,
    )


def classify(cfg: EHConfig) -> Tuple[str, EHResult]:
    r = compute_action(cfg)
    if not all(np.isfinite(v) for v in [r.S_num, r.S_abs_num, r.S_R2_num]):
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def refinement_test() -> Dict[str, float]:
    out = {}
    for n in [24, 32, 48, 64, 96, 128, 192]:
        r = compute_action(EHConfig(n=n, amp=0.1, kx=2, ky=3, noise=0.0, seed=101))
        out[f"abs_rel_err_n{n}"] = r.rel_abs_error
        out[f"R2_rel_err_n{n}"] = r.rel_R2_error
    return out


def run_sweep(n_sweeps: int = 300, seed: int = 83) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    abs_errs = []
    r2_errs = []

    for _ in range(n_sweeps):
        cfg = EHConfig(
            n=int(rng.choice([32, 48, 64, 96, 128])),
            amp=float(rng.uniform(0.02, 0.25)),
            kx=int(rng.integers(1, 5)),
            ky=int(rng.integers(1, 5)),
            noise=float(rng.uniform(0.0, 0.002)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.05:
            cfg = EHConfig(n=16, amp=cfg.amp, kx=6, ky=6, noise=cfg.noise, seed=cfg.seed)
        elif roll < 0.10:
            cfg = EHConfig(n=cfg.n, amp=cfg.amp, kx=cfg.kx, ky=cfg.ky, noise=0.03, seed=cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"}:
            abs_errs.append(r.rel_abs_error)
            r2_errs.append(r.rel_R2_error)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if abs_errs:
        out.update({
            "abs_rel_error_median": float(np.median(abs_errs)),
            "R2_rel_error_median": float(np.median(r2_errs)),
            "abs_rel_error_max": float(np.max(abs_errs)),
            "R2_rel_error_max": float(np.max(r2_errs)),
        })
    return out


def main() -> None:
    print("Einstein-Hilbert limit verifier")
    print("=" * 50)
    print("Controlled 2D conformal metric:")
    print("g_ij = exp(2 phi) delta_ij")
    print("EH-like density sqrt(g) R = -2 Laplacian(phi)")
    print("Also testing absolute curvature and R^2 convergence diagnostics.")
    print()

    print("Refinement test:")
    for k, v in refinement_test().items():
        print(f"{k}: {v}")

    print("\nSweep results:")
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
