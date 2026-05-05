
"""
antichain_spatial_geometry_verifier.py

Verifier for ANTICHAIN_SPATIAL_GEOMETRY.md.

Goal:
Test whether antichain slices can support spatial adjacency and a spatial metric proxy.

Route:
    causal order
      -> longest-chain depth
      -> rank antichain slices A_k
      -> causal-profile similarity within A_k
      -> spatial adjacency graph
      -> graph-distance / local Laplacian diagnostics
      -> hidden spatial neighbor precision (evaluation only)

Coordinates are used only to generate synthetic causal data and evaluate hidden quality.
The reconstruction uses only causal order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np


@dataclass(frozen=True)
class AntichainConfig:
    n_events: int = 360
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 6
    seed: int = 271


@dataclass(frozen=True)
class AntichainResult:
    n_slices: int
    median_slice_size: float
    antichain_violation_rate: float
    neighbor_precision: float
    neighbor_recall_proxy: float
    graph_connectivity_fraction: float
    laplacian_rank_median: float
    stable: bool


def generate_events(cfg: AntichainConfig):
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


def transitive_closure_bool(A):
    R = A.copy()
    n = R.shape[0]
    for k in range(n):
        parents = R[:, k]
        if np.any(parents):
            R[parents] |= R[k]
    return R


def longest_depths(closure):
    n = closure.shape[0]
    depth = np.zeros(n, dtype=np.int32)
    for j in range(n):
        preds = np.where(closure[:, j])[0]
        if len(preds):
            depth[j] = 1 + int(np.max(depth[preds]))
    return depth


def rank_slices(depth, min_size=12):
    return [np.where(depth == d)[0] for d in np.unique(depth) if np.sum(depth == d) >= min_size]


def antichain_violation(closure, slices):
    vals = []
    for sl in slices:
        sub = closure[np.ix_(sl, sl)]
        denom = len(sl) * (len(sl)-1)
        vals.append(float(np.sum(sub) / denom) if denom else 0.0)
    return float(np.median(vals)) if vals else 1.0


def causal_profiles(closure, sl):
    profiles = []
    for i in sl:
        past = closure[:, i]
        future = closure[i, :]
        profiles.append(np.concatenate([past, future]).astype(float))
    return np.asarray(profiles)


def profile_adjacency(closure, sl, k):
    if len(sl) < k+1:
        return np.zeros((len(sl), len(sl)), dtype=bool)
    P = causal_profiles(closure, sl)
    norms = np.linalg.norm(P, axis=1) + 1e-12
    sim = (P @ P.T) / (norms[:, None] * norms[None, :])
    np.fill_diagonal(sim, -np.inf)
    A = np.zeros((len(sl), len(sl)), dtype=bool)
    for a in range(len(sl)):
        nbrs = np.argsort(sim[a])[-k:]
        A[a, nbrs] = True
    # symmetrize spatial adjacency
    return A | A.T


def hidden_precision_for_slice(A_local, sl, x, k_true=8):
    if len(sl) < 2:
        return np.nan, np.nan
    X = x[sl]
    dist = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
    np.fill_diagonal(dist, np.inf)
    true_knn = np.argsort(dist, axis=1)[:, :min(k_true, len(sl)-1)]
    hits = total = 0
    recall_hits = recall_total = 0
    for a in range(len(sl)):
        pred = np.where(A_local[a])[0]
        for b in pred:
            total += 1
            if b in true_knn[a]:
                hits += 1
        for b in true_knn[a]:
            recall_total += 1
            if A_local[a, b]:
                recall_hits += 1
    precision = hits / total if total else np.nan
    recall = recall_hits / recall_total if recall_total else np.nan
    return precision, recall


def connectivity_fraction(A):
    n = A.shape[0]
    if n == 0:
        return 0.0
    seen = set([0])
    stack = [0]
    while stack:
        i = stack.pop()
        for j in np.where(A[i])[0]:
            if j not in seen:
                seen.add(int(j))
                stack.append(int(j))
    return len(seen) / n


def laplacian_rank(A):
    n = A.shape[0]
    if n == 0:
        return 0
    deg = np.sum(A, axis=1)
    L = np.diag(deg) - A.astype(float)
    vals = np.linalg.eigvalsh(L)
    return int(np.sum(vals > 1e-8))


def verify(cfg: AntichainConfig) -> AntichainResult:
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(10, cfg.n_events // 50))
    aviol = antichain_violation(closure, slices)

    precisions, recalls, conns, ranks, sizes = [], [], [], [], []
    # Use central/mid slices when possible, avoids tiny edge slices.
    for sl in slices[:40]:
        A = profile_adjacency(closure, sl, cfg.k_profile_neighbors)
        p, r = hidden_precision_for_slice(A, sl, x)
        if np.isfinite(p):
            precisions.append(p)
        if np.isfinite(r):
            recalls.append(r)
        conns.append(connectivity_fraction(A))
        ranks.append(laplacian_rank(A))
        sizes.append(len(sl))

    n_slices = len(slices)
    med_size = float(np.median(sizes)) if sizes else 0.0
    precision = float(np.nanmedian(precisions)) if precisions else float("nan")
    recall = float(np.nanmedian(recalls)) if recalls else float("nan")
    conn = float(np.nanmedian(conns)) if conns else 0.0
    rank = float(np.nanmedian(ranks)) if ranks else 0.0

    stable = bool(
        n_slices >= 3
        and med_size >= 10
        and aviol < 0.02
        and np.isfinite(precision) and precision > 0.08
        and np.isfinite(recall) and recall > 0.05
        and conn > 0.75
        and rank >= med_size - 2  # near connected graph Laplacian rank n-1
    )

    return AntichainResult(n_slices, med_size, aviol, precision, recall, conn, rank, stable)


def classify(cfg: AntichainConfig):
    r = verify(cfg)
    if r.n_slices < 2 or r.median_slice_size < 5:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=100, seed=277):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slices","median_slice_size","antichain_violation_rate","neighbor_precision","neighbor_recall_proxy","graph_connectivity_fraction","laplacian_rank_median"]}

    for _ in range(n_sweeps):
        cfg = AntichainConfig(
            n_events=int(rng.integers(220, 480)),
            spatial_dim=3,
            c=float(rng.uniform(1.2, 3.0)),
            retention_prob=float(rng.uniform(0.8, 1.0)),
            k_profile_neighbors=int(rng.integers(4, 10)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = AntichainConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = AntichainConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = AntichainConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS","SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))

    out = {k: 100*v/n_sweeps for k,v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Antichain spatial geometry verifier")
    print("="*50)
    print("Route:")
    print("causal order -> rank antichains -> causal-profile adjacency -> spatial graph diagnostics")
    print("Coordinates are used only for hidden spatial-neighbor evaluation.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
