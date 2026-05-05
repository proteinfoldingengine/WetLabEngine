
"""
order_distance_failure_diagnostic.py

Diagnostic for ORDER_DISTANCE_EMBEDDING.md hard failure.

Goal:
Identify why naive order-distance embedding failed.

Hypotheses:
    H1: too few comparable pairs / local neighborhoods are sparse.
    H2: order-distance matrix has too many missing entries.
    H3: interval-cardinality distance violates metric properties.
    H4: MDS produces poor low-rank Euclidean embedding.
    H5: dimension proxy is unstable.
    H6: causal-order distances are timelike/partial-order quantities, not spatial metric distances.

This script runs targeted diagnostics and reports which failure modes dominate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass(frozen=True)
class DiagnosticConfig:
    n_events: int = 260
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    seed: int = 211


def generate_events(cfg: DiagnosticConfig):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    x = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    retained = rng.random(cfg.n_events) < cfg.retention_prob
    return t, x, retained


def build_causal_matrix(cfg, t, x, retained):
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


def longest_chain_lengths(C):
    n = C.shape[0]
    L = np.zeros((n, n), dtype=np.int16)
    for i in range(n - 2, -1, -1):
        js = np.where(C[i])[0]
        for j in js:
            L[i, j] = max(L[i, j], 1)
            reachable = np.where(L[j] > 0)[0]
            if len(reachable):
                L[i, reachable] = np.maximum(L[i, reachable], 1 + L[j, reachable])
    return L


def estimate_D_eff(L):
    closure = L > 0
    pairs = np.argwhere(closure)
    chain = []
    sizes = []
    for i, j in pairs[::max(1, len(pairs)//3000)]:
        size = int(np.sum(closure[i] & closure[:, j]))
        if size > 0 and L[i, j] > 0:
            chain.append(float(L[i, j]))
            sizes.append(float(size))
    if len(chain) < 50:
        return np.nan
    xlog = np.log(np.asarray(chain) + 1)
    ylog = np.log(np.asarray(sizes) + 1)
    A = np.column_stack([xlog, np.ones_like(xlog)])
    slope, _ = np.linalg.lstsq(A, ylog, rcond=None)[0]
    return float(slope)


def build_order_distance(L, D_eff):
    closure = L > 0
    n = L.shape[0]
    D = np.full((n, n), np.nan)
    if not np.isfinite(D_eff) or D_eff <= 0.2:
        return D
    pairs = np.argwhere(closure)
    for i, j in pairs:
        size = int(np.sum(closure[i] & closure[:, j]))
        if size > 0:
            d = size ** (1.0 / D_eff)
            D[i, j] = D[j, i] = d
    np.fill_diagonal(D, 0.0)
    return D


def triangle_violation_rate(D, sample_triples=5000, seed=0):
    rng = np.random.default_rng(seed)
    n = D.shape[0]
    violations = 0
    tested = 0
    for _ in range(sample_triples):
        i, j, k = rng.choice(n, size=3, replace=False)
        dij, djk, dik = D[i, j], D[j, k], D[i, k]
        if not (np.isfinite(dij) and np.isfinite(djk) and np.isfinite(dik)):
            continue
        tested += 1
        if dik > dij + djk + 1e-9:
            violations += 1
    return (violations / tested if tested else np.nan), tested


def local_missingness(D, k=32):
    finite_counts = np.sum(np.isfinite(D), axis=1) - 1
    if np.max(finite_counts) < k:
        return 1.0, int(np.max(finite_counts))
    center = int(np.argmax(finite_counts))
    candidates = np.where(np.isfinite(D[center]))[0]
    candidates = candidates[candidates != center]
    nearest = candidates[np.argsort(D[center, candidates])[:k]]
    local = D[np.ix_(nearest, nearest)]
    missing = np.mean(~np.isfinite(local))
    return float(missing), int(np.max(finite_counts))


def mds_negative_eigen_fraction(D, k=32):
    finite_counts = np.sum(np.isfinite(D), axis=1) - 1
    if np.max(finite_counts) < k:
        return np.nan, np.nan
    center = int(np.argmax(finite_counts))
    candidates = np.where(np.isfinite(D[center]))[0]
    candidates = candidates[candidates != center]
    nearest = candidates[np.argsort(D[center, candidates])[:k]]
    local = D[np.ix_(nearest, nearest)]
    finite_vals = local[np.isfinite(local)]
    if len(finite_vals) == 0:
        return np.nan, np.nan
    fill = float(np.nanmedian(finite_vals))
    local = np.where(np.isfinite(local), local, fill)
    np.fill_diagonal(local, 0)
    n = local.shape[0]
    J = np.eye(n) - np.ones((n, n))/n
    B = -0.5 * J @ (local**2) @ J
    eig = np.linalg.eigvalsh(B)
    neg_frac = float(np.mean(eig < -1e-8))
    pos_rank = int(np.sum(eig > 1e-8))
    return neg_frac, pos_rank


def run_diagnostic(n_runs=80, seed=223) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    comparable_density = []
    D_vals = []
    tri_rates = []
    tri_tests = []
    missing_rates = []
    max_neighbors = []
    neg_fracs = []
    pos_ranks = []

    for _ in range(n_runs):
        cfg = DiagnosticConfig(
            n_events=int(rng.integers(160, 340)),
            spatial_dim=3,
            c=float(rng.uniform(1.2, 3.2)),
            retention_prob=float(rng.uniform(0.8, 1.0)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        t, x, retained = generate_events(cfg)
        C = build_causal_matrix(cfg, t, x, retained)
        L = longest_chain_lengths(C)
        closure = L > 0
        comparable_density.append(float(np.sum(closure)/(cfg.n_events*(cfg.n_events-1))))
        D_eff = estimate_D_eff(L)
        D_vals.append(D_eff if np.isfinite(D_eff) else np.nan)
        Dmat = build_order_distance(L, D_eff)
        tri, tested = triangle_violation_rate(Dmat, seed=cfg.seed)
        tri_rates.append(tri)
        tri_tests.append(tested)
        miss, maxn = local_missingness(Dmat)
        missing_rates.append(miss)
        max_neighbors.append(maxn)
        neg, rank = mds_negative_eigen_fraction(Dmat)
        neg_fracs.append(neg)
        pos_ranks.append(rank)

    def nanmedian(xs):
        xs = np.asarray(xs, dtype=float)
        return float(np.nanmedian(xs)) if np.any(np.isfinite(xs)) else float("nan")

    return {
        "comparable_density_median": nanmedian(comparable_density),
        "D_eff_median": nanmedian(D_vals),
        "triangle_violation_rate_median": nanmedian(tri_rates),
        "triangle_tested_median": nanmedian(tri_tests),
        "local_missingness_median": nanmedian(missing_rates),
        "max_finite_neighbors_median": nanmedian(max_neighbors),
        "mds_negative_eigen_fraction_median": nanmedian(neg_fracs),
        "mds_positive_rank_median": nanmedian(pos_ranks),
    }


def main():
    print("Order-distance failure diagnostic")
    print("=" * 50)
    print("Diagnoses why naive order-distance MDS embedding hard-failed.")
    print()
    for k, v in run_diagnostic().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
