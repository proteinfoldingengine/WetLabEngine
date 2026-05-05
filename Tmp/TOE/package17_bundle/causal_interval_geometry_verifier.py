
"""
causal_interval_geometry_verifier.py

Verifier for CAUSAL_INTERVAL_GEOMETRY.md.

Goal:
Test whether causal intervals generated from update/time-ordered events contain
stable interval-volume scaling and dimension proxies.

Lightweight structural version:
    Events in d-dimensional spacetime: time + spatial_dim.
    Causal relation i -> j iff dt > 0 and spatial distance <= c*dt.
    For comparable pairs, interval size |I(i,j)| is counted.
    Estimate D by regressing:
        log(|I(i,j)| + 1) ~ D * log(tau_ij) + const

This verifier is structural. It does not prove continuum causal-set geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class IntervalConfig:
    n_events: int = 350
    spatial_dim: int = 3
    c: float = 1.0
    retention_prob: float = 1.0
    seed: int = 131


@dataclass(frozen=True)
class IntervalResult:
    comparable_pairs: int
    sampled_pairs: int
    dim_estimate: float
    r2: float
    median_interval_size: float
    max_interval_size: int
    stable: bool


def generate_events(cfg: IntervalConfig):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    x = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    retained = rng.random(cfg.n_events) < cfg.retention_prob
    return t, x, retained


def build_causal_matrix(cfg: IntervalConfig, t, x, retained) -> np.ndarray:
    n = cfg.n_events
    C = np.zeros((n, n), dtype=bool)
    for i in range(n):
        if not retained[i]:
            continue
        dt = t[i+1:] - t[i]
        dx = x[i+1:] - x[i]
        dist = np.linalg.norm(dx, axis=1)
        C[i, i+1:] = dist <= cfg.c * dt
    return C


def estimate_interval_dimension(cfg: IntervalConfig, max_pairs: int = 1200) -> IntervalResult:
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    pairs = np.argwhere(C)

    if len(pairs) < 50:
        return IntervalResult(len(pairs), 0, np.nan, 0.0, 0.0, 0, False)

    rng = np.random.default_rng(cfg.seed + 2)
    if len(pairs) > max_pairs:
        pairs = pairs[rng.choice(len(pairs), size=max_pairs, replace=False)]

    taus = []
    sizes = []

    # Direct interval count using C rows/cols. This is not full transitive closure;
    # it is a first direct-causal interval proxy and runs fast.
    for i, j in pairs:
        dt = t[j] - t[i]
        dx = x[j] - x[i]
        spatial2 = float(np.dot(dx, dx))
        tau2 = (cfg.c * dt) ** 2 - spatial2
        if tau2 <= 1e-8:
            continue
        tau = np.sqrt(tau2) / cfg.c

        between_time = (t > t[i]) & (t < t[j])
        reachable_from_i = np.linalg.norm(x - x[i], axis=1) <= cfg.c * (t - t[i])
        reaches_j = np.linalg.norm(x[j] - x, axis=1) <= cfg.c * (t[j] - t)
        between = between_time & reachable_from_i & reaches_j
        size = int(np.sum(between))
        if size <= 0:
            continue
        taus.append(tau)
        sizes.append(size)

    if len(taus) < 50:
        return IntervalResult(int(len(np.argwhere(C))), len(taus), np.nan, 0.0, 0.0, 0, False)

    xlog = np.log(np.asarray(taus))
    ylog = np.log(np.asarray(sizes) + 1.0)

    Areg = np.column_stack([xlog, np.ones_like(xlog)])
    slope, intercept = np.linalg.lstsq(Areg, ylog, rcond=None)[0]
    pred = slope * xlog + intercept
    ss_res = float(np.sum((ylog - pred) ** 2))
    ss_tot = float(np.sum((ylog - np.mean(ylog)) ** 2)) + 1e-12
    r2 = 1 - ss_res / ss_tot

    target_D = cfg.spatial_dim + 1
    stable = bool(np.isfinite(slope) and r2 > 0.35 and abs(slope - target_D) < 2.5)

    return IntervalResult(
        comparable_pairs=int(len(np.argwhere(C))),
        sampled_pairs=len(taus),
        dim_estimate=float(slope),
        r2=float(r2),
        median_interval_size=float(np.median(sizes)),
        max_interval_size=int(np.max(sizes)),
        stable=stable,
    )


def classify(cfg: IntervalConfig) -> Tuple[str, IntervalResult]:
    r = estimate_interval_dimension(cfg)
    if not np.isfinite(r.dim_estimate) or r.sampled_pairs < 50:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps: int = 80, seed: int = 137) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    dims = []
    r2s = []
    comps = []

    for _ in range(n_sweeps):
        cfg = IntervalConfig(
            n_events=int(rng.integers(180, 420)),
            spatial_dim=3,
            c=float(rng.uniform(1.0, 3.0)),
            retention_prob=float(rng.uniform(0.75, 1.0)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.05:
            cfg = IntervalConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.seed)
        elif roll < 0.10:
            cfg = IntervalConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.seed)
        elif roll < 0.13:
            cfg = IntervalConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            dims.append(r.dim_estimate)
            r2s.append(r.r2)
            comps.append(r.comparable_pairs)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if dims:
        out.update({
            "dim_estimate_median": float(np.median(dims)),
            "dim_estimate_min": float(np.min(dims)),
            "dim_estimate_max": float(np.max(dims)),
            "r2_median": float(np.median(r2s)),
            "comparable_pairs_median": float(np.median(comps)),
        })
    return out


def main() -> None:
    print("Causal interval geometry verifier")
    print("=" * 50)
    print("Test:")
    print("Build causal intervals I(i,j), count |I(i,j)|, estimate dimension from log interval-size scaling.")
    print()

    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
