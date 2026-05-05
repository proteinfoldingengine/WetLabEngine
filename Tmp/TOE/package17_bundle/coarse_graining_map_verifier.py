
"""
coarse_graining_map_verifier.py

Verifier for COARSE_GRAINING_MAP.md.

Goal:
Test the first structural coarse-graining map:

    ({G_e}, {R_e}, {phi_e}) -> (g_mu_nu, R_eff, phi_eff)

with special focus on the critical identification:

    R_eff ~ Lambda = M/G

This verifier does not construct a Lorentzian metric from first principles.
It checks whether block-averaged geometry and memory variables can produce:
    - finite positive geometry scale G_block
    - finite retained-memory load M_block
    - stable loading scalar Lambda_block = M_block / G_block
    - finite scalar R_eff
    - stable block-to-block variance under coarse-graining

It also tests failure cases:
    - G_block <= 0
    - high variance/no stable block scalar
    - Lambda singularity
    - nonlocal dominance flag
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class CoarseGrainConfig:
    n_blocks: int = 256
    block_size: int = 32
    geometry_noise: float = 0.1
    memory_noise: float = 0.1
    nonlocal_strength: float = 0.0
    seed: int = 31


@dataclass(frozen=True)
class CoarseGrainResult:
    G_mean: float
    M_mean: float
    Lambda_mean: float
    Lambda_std: float
    Lambda_cv: float
    R_eff_mean: float
    R_eff_std: float
    stable_scalar: bool
    positive_geometry: bool
    nonlocal_ok: bool


def simulate_discrete_fields(cfg: CoarseGrainConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    n = cfg.n_blocks * cfg.block_size

    G = rng.lognormal(mean=0.0, sigma=cfg.geometry_noise, size=n)

    base_memory = 0.25 * G
    R_slow = base_memory + rng.normal(0, cfg.memory_noise, size=n)
    R_fast = 0.1 * base_memory + rng.normal(0, cfg.memory_noise * 0.5, size=n)
    M = np.clip(R_slow + R_fast, 0, None)

    if cfg.nonlocal_strength > 0:
        global_mode = cfg.nonlocal_strength * np.mean(M)
        M = M + global_mode

    phi = rng.normal(0, 1, size=n)

    return G, M, phi


def block_average(x: np.ndarray, block_size: int) -> np.ndarray:
    n_blocks = len(x) // block_size
    trimmed = x[: n_blocks * block_size]
    return trimmed.reshape(n_blocks, block_size).mean(axis=1)


def coarse_grain(cfg: CoarseGrainConfig) -> CoarseGrainResult:
    G, M, phi = simulate_discrete_fields(cfg)

    G_block = block_average(G, cfg.block_size)
    M_block = block_average(M, cfg.block_size)

    positive_geometry = bool(np.all(G_block > 0))
    if not positive_geometry:
        Lambda_block = np.full_like(G_block, np.nan)
    else:
        Lambda_block = M_block / G_block

    Lambda_mean = float(np.nanmean(Lambda_block))
    Lambda_std = float(np.nanstd(Lambda_block))
    Lambda_cv = float(Lambda_std / abs(Lambda_mean)) if abs(Lambda_mean) > 1e-12 else float("inf")

    R_eff_block = Lambda_block
    R_eff_mean = float(np.nanmean(R_eff_block))
    R_eff_std = float(np.nanstd(R_eff_block))

    stable_scalar = bool(np.isfinite(Lambda_cv) and Lambda_cv < 0.5)
    nonlocal_ok = bool(cfg.nonlocal_strength < 2.0)

    return CoarseGrainResult(
        G_mean=float(np.mean(G_block)),
        M_mean=float(np.mean(M_block)),
        Lambda_mean=Lambda_mean,
        Lambda_std=Lambda_std,
        Lambda_cv=Lambda_cv,
        R_eff_mean=R_eff_mean,
        R_eff_std=R_eff_std,
        stable_scalar=stable_scalar,
        positive_geometry=positive_geometry,
        nonlocal_ok=nonlocal_ok,
    )


def classify(cfg: CoarseGrainConfig) -> Tuple[str, CoarseGrainResult]:
    r = coarse_grain(cfg)

    if not r.positive_geometry:
        return "HARD_FAIL", r

    if not np.isfinite(r.Lambda_mean) or not np.isfinite(r.Lambda_cv):
        return "HARD_FAIL", r

    if not r.nonlocal_ok:
        return "HARD_FAIL", r

    if not r.stable_scalar:
        return "SOFT_FAIL", r

    return "PASS", r


def run_sweep(n_sweeps: int = 20000, seed: int = 37) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    lambda_means = []
    lambda_cvs = []
    r_stds = []

    for i in range(n_sweeps):
        cfg = CoarseGrainConfig(
            n_blocks=int(rng.integers(64, 512)),
            block_size=int(rng.choice([8, 16, 32, 64])),
            geometry_noise=float(rng.uniform(0.01, 0.75)),
            memory_noise=float(rng.uniform(0.01, 0.35)),
            nonlocal_strength=float(rng.uniform(0.0, 1.5)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.01:
            cfg = CoarseGrainConfig(
                n_blocks=cfg.n_blocks,
                block_size=cfg.block_size,
                geometry_noise=cfg.geometry_noise,
                memory_noise=2.0,
                nonlocal_strength=cfg.nonlocal_strength,
                seed=cfg.seed,
            )
        elif roll < 0.015:
            cfg = CoarseGrainConfig(
                n_blocks=cfg.n_blocks,
                block_size=cfg.block_size,
                geometry_noise=cfg.geometry_noise,
                memory_noise=cfg.memory_noise,
                nonlocal_strength=5.0,
                seed=cfg.seed,
            )

        label, r = classify(cfg)
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"}:
            lambda_means.append(r.Lambda_mean)
            lambda_cvs.append(r.Lambda_cv)
            r_stds.append(r.R_eff_std)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if lambda_means:
        out.update({
            "Lambda_mean_median": float(np.median(lambda_means)),
            "Lambda_cv_median": float(np.median(lambda_cvs)),
            "R_eff_std_median": float(np.median(r_stds)),
            "Lambda_mean_min": float(np.min(lambda_means)),
            "Lambda_mean_max": float(np.max(lambda_means)),
        })
    return out


def main() -> None:
    print("Coarse-graining map verifier")
    print("=" * 50)
    print("Map tested:")
    print("G_block = <G_e>_B")
    print("M_block = <M_e>_B")
    print("R_eff   = Lambda_block = M_block / G_block")
    print("phi_eff = <phi_e>_B [proxy only]")
    print()

    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
