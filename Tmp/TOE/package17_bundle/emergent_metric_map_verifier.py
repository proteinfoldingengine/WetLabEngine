
"""
emergent_metric_map_verifier.py

Verifier for EMERGENT_METRIC_MAP.md.

Goal:
Test a first structural emergent-metric candidate from block geometry data.

This verifier does not prove GR, Lorentzian signature, or covariance.
It tests whether a stable non-degenerate local metric tensor can be reconstructed
from local block geometry data in a toy Euclidean/local-Riemannian setting.

The sweep is intentionally lightweight enough to run quickly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class MetricConfig:
    n_points: int = 180
    dim: int = 3
    k_neighbors: int = 12
    geometry_noise: float = 0.15
    anisotropy: float = 0.25
    seed: int = 41


@dataclass(frozen=True)
class MetricResult:
    n_valid: int
    valid_fraction: float
    cond_median: float
    eig_min_median: float
    eig_max_median: float
    metric_variation: float
    stable_metric: bool
    nondegenerate: bool


def generate_blocks(cfg: MetricConfig) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    X = rng.uniform(0, 1, size=(cfg.n_points, cfg.dim))
    base = 1.0 + cfg.anisotropy * X[:, 0]
    G = base * rng.lognormal(mean=0.0, sigma=cfg.geometry_noise, size=cfg.n_points)
    return X, G


def nearest_neighbors(X: np.ndarray, k: int) -> np.ndarray:
    diff = X[:, None, :] - X[None, :, :]
    dist2 = np.sum(diff * diff, axis=-1)
    np.fill_diagonal(dist2, np.inf)
    return np.argsort(dist2, axis=1)[:, :k]


def metric_design_rows(dx: np.ndarray) -> np.ndarray:
    # dx shape: (k, d). For d=3, returns [xx, yy, zz, 2xy, 2xz, 2yz].
    k, d = dx.shape
    cols = []
    for a in range(d):
        cols.append(dx[:, a] * dx[:, a])
    for a in range(d):
        for b in range(a + 1, d):
            cols.append(2 * dx[:, a] * dx[:, b])
    return np.column_stack(cols)


def coeffs_to_matrix(coeffs: np.ndarray, d: int) -> np.ndarray:
    M = np.zeros((d, d))
    idx = 0
    for a in range(d):
        M[a, a] = coeffs[idx]
        idx += 1
    for a in range(d):
        for b in range(a + 1, d):
            M[a, b] = M[b, a] = coeffs[idx]
            idx += 1
    return M


def estimate_local_metric(X: np.ndarray, G: np.ndarray, nbrs: np.ndarray, i: int) -> np.ndarray | None:
    xi = X[i]
    dx = X[nbrs[i]] - xi
    targets = 0.5 * (G[i] + G[nbrs[i]]) * np.sum(dx * dx, axis=1)
    A = metric_design_rows(dx)

    if A.shape[0] < A.shape[1]:
        return None

    try:
        coeffs, *_ = np.linalg.lstsq(A, targets, rcond=None)
    except np.linalg.LinAlgError:
        return None

    return coeffs_to_matrix(coeffs, X.shape[1])


def verify_metric(cfg: MetricConfig, sample_points: int = 60) -> MetricResult:
    X, G = generate_blocks(cfg)

    if not np.all(G > 0):
        return MetricResult(0, 0.0, np.inf, -np.inf, np.inf, np.inf, False, False)

    nbrs = nearest_neighbors(X, cfg.k_neighbors)

    rng = np.random.default_rng(cfg.seed + 1)
    point_idx = rng.choice(cfg.n_points, size=min(sample_points, cfg.n_points), replace=False)

    metrics = []
    conds = []
    eig_mins = []
    eig_maxs = []

    for i in point_idx:
        M = estimate_local_metric(X, G, nbrs, int(i))
        if M is None or not np.all(np.isfinite(M)) or not np.allclose(M, M.T, atol=1e-8):
            continue

        eig = np.linalg.eigvalsh(M)
        if np.min(eig) <= 1e-8:
            continue

        cond = float(np.max(eig) / np.min(eig))
        if not np.isfinite(cond):
            continue

        metrics.append(M)
        conds.append(cond)
        eig_mins.append(float(np.min(eig)))
        eig_maxs.append(float(np.max(eig)))

    if not metrics:
        return MetricResult(0, 0.0, np.inf, -np.inf, np.inf, np.inf, False, False)

    metrics_arr = np.asarray(metrics)
    mean_metric = np.mean(metrics_arr, axis=0)
    metric_variation = float(np.mean([np.linalg.norm(M - mean_metric) for M in metrics_arr]))

    valid_fraction = len(metrics) / len(point_idx)
    cond_median = float(np.median(conds))
    eig_min_median = float(np.median(eig_mins))
    eig_max_median = float(np.median(eig_maxs))

    nondegenerate = bool(valid_fraction > 0.8 and eig_min_median > 1e-6)
    stable_metric = bool(nondegenerate and cond_median < 50 and metric_variation < 2.0)

    return MetricResult(
        n_valid=len(metrics),
        valid_fraction=float(valid_fraction),
        cond_median=cond_median,
        eig_min_median=eig_min_median,
        eig_max_median=eig_max_median,
        metric_variation=metric_variation,
        stable_metric=stable_metric,
        nondegenerate=nondegenerate,
    )


def classify(cfg: MetricConfig) -> Tuple[str, MetricResult]:
    r = verify_metric(cfg)
    if not r.nondegenerate:
        return "HARD_FAIL", r
    if not r.stable_metric:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps: int = 300, seed: int = 43) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    valid_fracs = []
    conds = []
    variations = []

    for _ in range(n_sweeps):
        cfg = MetricConfig(
            n_points=int(rng.integers(90, 240)),
            dim=3,
            k_neighbors=int(rng.integers(8, 18)),
            geometry_noise=float(rng.uniform(0.01, 0.55)),
            anisotropy=float(rng.uniform(0.0, 0.8)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.03:
            cfg = MetricConfig(
                n_points=cfg.n_points,
                dim=3,
                k_neighbors=4,
                geometry_noise=cfg.geometry_noise,
                anisotropy=cfg.anisotropy,
                seed=cfg.seed,
            )
        elif roll < 0.06:
            cfg = MetricConfig(
                n_points=cfg.n_points,
                dim=3,
                k_neighbors=cfg.k_neighbors,
                geometry_noise=2.0,
                anisotropy=cfg.anisotropy,
                seed=cfg.seed,
            )

        label, r = classify(cfg)
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"}:
            valid_fracs.append(r.valid_fraction)
            conds.append(r.cond_median)
            variations.append(r.metric_variation)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if valid_fracs:
        out.update({
            "valid_fraction_median": float(np.median(valid_fracs)),
            "cond_median": float(np.median(conds)),
            "metric_variation_median": float(np.median(variations)),
            "valid_fraction_min": float(np.min(valid_fracs)),
        })
    return out


def main() -> None:
    print("Emergent metric map verifier")
    print("=" * 50)
    print("Candidate tested:")
    print("block coordinates + positive geometry weights + adjacency")
    print("-> local weighted distance relation")
    print("-> local symmetric metric estimate")
    print()
    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
