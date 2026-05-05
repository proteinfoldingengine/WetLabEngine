
"""
order_only_metric_reconstruction_verifier.py

Verifier for ORDER_ONLY_METRIC_RECONSTRUCTION.md.

Goal:
Test whether causal-order data alone can reconstruct useful geometry proxies:
    - causal depth / longest-chain distance
    - interval-cardinality distance proxy
    - effective dimension proxy
    - embedding-quality proxy without using coordinates in the reconstruction

Important:
    Coordinates are used only to generate synthetic ground truth and evaluate correlation.
    The reconstruction itself uses only the causal relation matrix.

Candidate order-only proxies:
    chain_depth(i,j): longest causal chain length from i to j
    interval_size(i,j): number of events k such that i<k<j
    d_order(i,j): interval_size(i,j)^(1/D_est)

Evaluation:
    Compare order-only distance proxy with hidden proper-time-like tau from generator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class OrderMetricConfig:
    n_events: int = 320
    spatial_dim: int = 3
    c: float = 1.7
    retention_prob: float = 1.0
    seed: int = 151


@dataclass(frozen=True)
class OrderMetricResult:
    comparable_pairs: int
    sampled_pairs: int
    dim_estimate: float
    interval_tau_corr: float
    chain_tau_corr: float
    order_distance_tau_corr: float
    stable: bool


def generate_events(cfg: OrderMetricConfig):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    x = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    retained = rng.random(cfg.n_events) < cfg.retention_prob
    return t, x, retained


def build_causal_matrix(cfg: OrderMetricConfig, t, x, retained) -> np.ndarray:
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


def longest_chain_lengths(C: np.ndarray) -> np.ndarray:
    """Compute longest chain lengths for DAG ordered by index."""
    n = C.shape[0]
    L = np.zeros((n, n), dtype=np.int16)
    # Since edges only go forward, dynamic programming reverse over i.
    for i in range(n - 2, -1, -1):
        js = np.where(C[i])[0]
        for j in js:
            L[i, j] = max(L[i, j], 1)
            # paths i->j->k
            reachable_from_j = np.where(L[j] > 0)[0]
            if len(reachable_from_j):
                L[i, reachable_from_j] = np.maximum(
                    L[i, reachable_from_j],
                    1 + L[j, reachable_from_j]
                )
    return L


def transitive_closure_from_chain(L: np.ndarray) -> np.ndarray:
    return L > 0


def estimate_order_metric(cfg: OrderMetricConfig, max_pairs: int = 1600) -> OrderMetricResult:
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    L = longest_chain_lengths(C)
    closure = transitive_closure_from_chain(L)
    pairs = np.argwhere(closure)

    if len(pairs) < 80:
        return OrderMetricResult(len(pairs), 0, np.nan, np.nan, np.nan, np.nan, False)

    rng = np.random.default_rng(cfg.seed + 3)
    if len(pairs) > max_pairs:
        pairs = pairs[rng.choice(len(pairs), size=max_pairs, replace=False)]

    taus = []
    interval_sizes = []
    chain_lengths = []

    for i, j in pairs:
        dt = t[j] - t[i]
        dx = x[j] - x[i]
        tau2 = (cfg.c * dt) ** 2 - float(np.dot(dx, dx))
        if tau2 <= 1e-8:
            continue
        tau = np.sqrt(tau2) / cfg.c

        between = closure[i] & closure[:, j]
        size = int(np.sum(between))
        chain = int(L[i, j])

        if size <= 0 or chain <= 0:
            continue

        taus.append(tau)
        interval_sizes.append(size)
        chain_lengths.append(chain)

    if len(taus) < 80:
        return OrderMetricResult(len(np.argwhere(closure)), len(taus), np.nan, np.nan, np.nan, np.nan, False)

    taus = np.asarray(taus)
    interval_sizes = np.asarray(interval_sizes, dtype=float)
    chain_lengths = np.asarray(chain_lengths, dtype=float)

    # Estimate dimension order-only-ish from log interval size vs log chain length.
    # chain length is an order-only proxy for proper time.
    xlog = np.log(chain_lengths + 1.0)
    ylog = np.log(interval_sizes + 1.0)
    A = np.column_stack([xlog, np.ones_like(xlog)])
    slope, intercept = np.linalg.lstsq(A, ylog, rcond=None)[0]
    dim_est = float(slope)

    def corr(a, b):
        if np.std(a) < 1e-12 or np.std(b) < 1e-12:
            return np.nan
        return float(np.corrcoef(a, b)[0, 1])

    interval_tau_corr = corr(np.log(interval_sizes + 1.0), np.log(taus + 1e-12))
    chain_tau_corr = corr(chain_lengths, taus)

    # Order-only distance proxy from interval cardinality and estimated dimension.
    if np.isfinite(dim_est) and dim_est > 0.2:
        d_order = interval_sizes ** (1.0 / dim_est)
        order_distance_tau_corr = corr(d_order, taus)
    else:
        order_distance_tau_corr = np.nan

    stable = bool(
        np.isfinite(dim_est)
        and 0.5 < dim_est < 8.0
        and np.isfinite(order_distance_tau_corr)
        and order_distance_tau_corr > 0.55
        and np.isfinite(chain_tau_corr)
        and chain_tau_corr > 0.45
    )

    return OrderMetricResult(
        comparable_pairs=int(len(np.argwhere(closure))),
        sampled_pairs=len(taus),
        dim_estimate=dim_est,
        interval_tau_corr=interval_tau_corr,
        chain_tau_corr=chain_tau_corr,
        order_distance_tau_corr=order_distance_tau_corr,
        stable=stable,
    )


def classify(cfg: OrderMetricConfig) -> Tuple[str, OrderMetricResult]:
    r = estimate_order_metric(cfg)
    if not np.isfinite(r.dim_estimate) or r.sampled_pairs < 80:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps: int = 80, seed: int = 157) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    dims, od_corrs, ch_corrs, comps = [], [], [], []

    for _ in range(n_sweeps):
        cfg = OrderMetricConfig(
            n_events=int(rng.integers(160, 360)),
            spatial_dim=3,
            c=float(rng.uniform(1.0, 3.0)),
            retention_prob=float(rng.uniform(0.75, 1.0)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.05:
            cfg = OrderMetricConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.seed)
        elif roll < 0.10:
            cfg = OrderMetricConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            dims.append(r.dim_estimate)
            od_corrs.append(r.order_distance_tau_corr)
            ch_corrs.append(r.chain_tau_corr)
            comps.append(r.comparable_pairs)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if dims:
        out.update({
            "dim_estimate_median": float(np.median(dims)),
            "order_distance_tau_corr_median": float(np.nanmedian(od_corrs)),
            "chain_tau_corr_median": float(np.nanmedian(ch_corrs)),
            "comparable_pairs_median": float(np.median(comps)),
        })
    return out


def main() -> None:
    print("Order-only metric reconstruction verifier")
    print("=" * 50)
    print("Reconstruction uses only causal relation:")
    print("longest-chain distance, interval cardinality, order-distance proxy")
    print("Coordinates are used only for hidden evaluation correlation.")
    print()

    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
