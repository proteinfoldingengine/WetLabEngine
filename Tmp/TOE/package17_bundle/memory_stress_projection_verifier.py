
"""
memory_stress_projection_verifier.py

Verifier for MEMORY_STRESS_PROJECTION.md.

Goal:
Replace generic weak-memory source proxy S_ab^mem,k with a projected source
from the scalar-density memory stress tensor.

Scalar-density memory model:
    L_mem = -1/2 Z (∂R)^2 - V(R) + lambda R O_mat

Weak-memory regime:
    R_eff = eta * r

ADM spatial projection:
    S_ab^mem,k = projection of T_ij^mem onto spatial metric slice h_ab.
First simplified projection:
    T_ab^mem ~ Z ∂_a R ∂_b R
               - 1/2 h_ab Z |grad R|_h^2
               + h_ab V(R)
               - lambda R T_ab^mat

Checks:
    - finite projected source
    - O(eta) or O(eta^2) scaling
    - source remains small relative to Euler response scale
    - halving eta scales source appropriately
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MemStressConfig:
    n_slices: int = 9
    dim: int = 3
    eta: float = 1e-2
    Z: float = 1.0
    lam: float = 0.2
    v1: float = 0.0
    v2: float = 1.0
    seed: int = 809


@dataclass(frozen=True)
class MemStressResult:
    source_norm_median: float
    source_half_norm_median: float
    scaling_ratio: float
    kinetic_order_ratio: float
    finite_fraction: float
    small_source_fraction: float
    stable: bool


def random_spd(rng, dim):
    A = rng.normal(size=(dim, dim))
    return A.T @ A + dim * np.eye(dim)


def make_fields(cfg, eta):
    rng = np.random.default_rng(cfg.seed)
    hs = []
    R = []
    gradR = []
    Tmat = []
    for k in range(cfg.n_slices):
        h = random_spd(rng, cfg.dim)
        if hs:
            h = 0.75 * hs[-1] + 0.25 * h
        hs.append(h)

        # weak memory amplitude and spatial gradient
        r = rng.normal(0, 1)
        R.append(eta * r)
        g = eta * rng.normal(0, 1, size=cfg.dim)
        gradR.append(g)

        # simple positive matter spatial stress proxy
        M = rng.normal(size=(cfg.dim, cfg.dim))
        T = 0.5 * (M + M.T)
        Tmat.append(T)
    return hs, np.asarray(R), gradR, Tmat


def potential(R, cfg):
    return cfg.v1 * R + 0.5 * cfg.v2 * R * R


def projected_source(h, R, grad, Tmat, cfg):
    hinv = np.linalg.inv(h)
    grad2 = float(grad @ hinv @ grad)

    kinetic = cfg.Z * np.outer(grad, grad)
    kinetic_trace = -0.5 * h * cfg.Z * grad2
    Vterm = h * potential(R, cfg)
    interaction = -cfg.lam * R * Tmat

    return kinetic + kinetic_trace + Vterm + interaction


def source_norms(cfg, eta):
    hs, R, gradR, Tmat = make_fields(cfg, eta)
    norms = []
    kinetic_norms = []
    total_vals = []
    for h, r, g, T in zip(hs, R, gradR, Tmat):
        S = projected_source(h, r, g, T, cfg)
        norms.append(np.linalg.norm(S))

        hinv = np.linalg.inv(h)
        grad2 = float(g @ hinv @ g)
        K = cfg.Z * np.outer(g, g) - 0.5 * h * cfg.Z * grad2
        kinetic_norms.append(np.linalg.norm(K))
        total_vals.extend(list(S.ravel()))
    finite_fraction = float(np.mean(np.isfinite(total_vals))) if total_vals else 0.0
    return np.asarray(norms), np.asarray(kinetic_norms), finite_fraction


def verify(cfg):
    norms, kin, finite1 = source_norms(cfg, cfg.eta)
    norms_half, kin_half, finite2 = source_norms(cfg, cfg.eta * 0.5)

    med = float(np.nanmedian(norms))
    med_half = float(np.nanmedian(norms_half))
    scaling = med_half / (med + 1e-12)

    kin_med = float(np.nanmedian(kin))
    kin_half_med = float(np.nanmedian(kin_half))
    kinetic_order = kin_half_med / (kin_med + 1e-12)

    finite_fraction = min(finite1, finite2)

    # generic Euler scale from previous proxy median ~ O(1); require weak source < 0.1
    small_source_fraction = float(np.mean(norms < 0.1))

    # If v1=0, dominant interaction is O(eta), kinetic/potential O(eta^2).
    # Total scaling often ~0.5 when interaction dominates.
    # Kinetic-only should scale ~0.25.
    stable = bool(
        finite_fraction > 0.99
        and np.isfinite(scaling)
        and 0.35 < scaling < 0.65
        and np.isfinite(kinetic_order)
        and 0.15 < kinetic_order < 0.35
        and small_source_fraction > 0.8
    )

    return MemStressResult(
        source_norm_median=med,
        source_half_norm_median=med_half,
        scaling_ratio=scaling,
        kinetic_order_ratio=kinetic_order,
        finite_fraction=finite_fraction,
        small_source_fraction=small_source_fraction,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=300, seed=811):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "source_norm_median","source_half_norm_median","scaling_ratio",
        "kinetic_order_ratio","finite_fraction","small_source_fraction"
    ]}

    for _ in range(n_sweeps):
        cfg = MemStressConfig(
            n_slices=int(rng.integers(5, 14)),
            dim=3,
            eta=float(10 ** rng.uniform(-4, -1.5)),
            Z=float(10 ** rng.uniform(-1, 1)),
            lam=float(10 ** rng.uniform(-2, 0)),
            v1=0.0,
            v2=float(10 ** rng.uniform(-1, 1)),
            seed=int(rng.integers(0, 10_000_000)),
        )
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
    print("Memory stress projection verifier")
    print("="*50)
    print("Route:")
    print("scalar-density T_mu_nu^mem -> ADM spatial projection S_ab^mem,k")
    print("Checks weak-memory scaling and finite projected source.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
