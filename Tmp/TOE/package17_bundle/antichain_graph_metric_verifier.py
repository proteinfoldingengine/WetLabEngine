
"""
antichain_graph_metric_verifier.py

Verifier for ANTICHAIN_GRAPH_METRIC.md.

Goal:
Test whether antichain spatial graphs can support a spatial metric candidate h_ab.

Route:
    causal order
      -> longest-chain depth
      -> rank antichain slices
      -> causal-profile adjacency graph on each slice
      -> graph Laplacian embedding
      -> local spatial metric proxy h_ab from embedded coordinates

Coordinates are used only for synthetic evaluation of embedding quality.
The reconstruction uses only causal order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np


@dataclass(frozen=True)
class GraphMetricConfig:
    n_events: int = 380
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    embed_dim: int = 3
    seed: int = 307


@dataclass(frozen=True)
class GraphMetricResult:
    n_slices_used: int
    median_slice_size: float
    median_embedding_corr: float
    median_stress: float
    median_metric_condition: float
    median_metric_rank: float
    stable: bool


def generate_events(cfg):
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


def rank_slices(depth, min_size=18):
    return [np.where(depth == d)[0] for d in np.unique(depth) if np.sum(depth == d) >= min_size]


def causal_profiles(closure, sl):
    profiles = []
    for i in sl:
        past = closure[:, i]
        future = closure[i, :]
        profiles.append(np.concatenate([past, future]).astype(float))
    return np.asarray(profiles)


def profile_weighted_adjacency(closure, sl, k):
    n = len(sl)
    if n < k + 2:
        return np.zeros((n, n), dtype=float)
    P = causal_profiles(closure, sl)
    norms = np.linalg.norm(P, axis=1) + 1e-12
    sim = (P @ P.T) / (norms[:, None] * norms[None, :])
    np.fill_diagonal(sim, -np.inf)

    W = np.zeros((n, n), dtype=float)
    for a in range(n):
        nbrs = np.argsort(sim[a])[-k:]
        for b in nbrs:
            if np.isfinite(sim[a, b]):
                W[a, b] = max(0.0, sim[a, b])
    W = np.maximum(W, W.T)
    return W


def laplacian_embedding(W, embed_dim=3):
    n = W.shape[0]
    deg = np.sum(W, axis=1)
    if np.sum(deg > 0) < embed_dim + 2:
        return None, None

    # Normalized Laplacian.
    invsqrt = np.zeros_like(deg)
    mask = deg > 1e-12
    invsqrt[mask] = 1.0 / np.sqrt(deg[mask])
    L = np.eye(n) - (invsqrt[:, None] * W * invsqrt[None, :])

    vals, vecs = np.linalg.eigh(L)
    idx = np.argsort(vals)
    vals = vals[idx]
    vecs = vecs[:, idx]

    # skip first constant mode
    usable = vecs[:, 1:embed_dim+1]
    return usable, vals


def pairwise_dist(X):
    diff = X[:, None, :] - X[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1))


def corr_flat(A, B):
    iu = np.triu_indices_from(A, k=1)
    a, b = A[iu], B[iu]
    mask = np.isfinite(a) & np.isfinite(b)
    if np.sum(mask) < 10 or np.std(a[mask]) < 1e-12 or np.std(b[mask]) < 1e-12:
        return np.nan
    return float(np.corrcoef(a[mask], b[mask])[0, 1])


def graph_shortest_dist(W):
    n = W.shape[0]
    D = np.full((n, n), np.inf)
    np.fill_diagonal(D, 0)
    # Convert weights to lengths.
    edges = W > 0
    lengths = np.where(edges, 1.0 / (W + 1e-9), np.inf)
    D = np.minimum(D, lengths)
    for k in range(n):
        D = np.minimum(D, D[:, [k]] + D[[k], :])
    return D


def metric_proxy_condition(Xemb, W):
    # Use local neighbor differences; covariance inverse proxy approximates metric shape.
    diffs = []
    for i in range(W.shape[0]):
        nbrs = np.where(W[i] > 0)[0]
        for j in nbrs:
            diffs.append(Xemb[j] - Xemb[i])
    if len(diffs) < Xemb.shape[1] + 2:
        return np.inf, 0
    D = np.asarray(diffs)
    C = np.cov(D.T)
    if C.ndim == 0 or C.shape[0] != Xemb.shape[1]:
        return np.inf, 0
    eig = np.linalg.eigvalsh(C)
    rank = int(np.sum(eig > 1e-8))
    if np.min(eig) <= 1e-10:
        return np.inf, rank
    cond = float(np.max(eig) / np.min(eig))
    return cond, rank


def verify(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 40))

    corrs, stresses, conds, ranks, sizes = [], [], [], [], []
    for sl in slices[:30]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        if np.sum(W > 0) == 0:
            continue
        Xemb, vals = laplacian_embedding(W, embed_dim=min(cfg.embed_dim, len(sl)-2))
        if Xemb is None:
            continue

        D_graph = graph_shortest_dist(W)
        D_emb = pairwise_dist(Xemb)
        finite = np.isfinite(D_graph)
        if np.mean(finite) < 0.8:
            continue
        # normalize graph and embedding distances for stress
        dg = D_graph[finite]
        de = D_emb[finite]
        dg = dg / (np.median(dg[dg > 0]) + 1e-12)
        de = de / (np.median(de[de > 0]) + 1e-12)
        stress = float(np.sqrt(np.mean((dg - de)**2)))

        D_hidden = pairwise_dist(x[sl])
        corr = corr_flat(D_emb, D_hidden)
        cond, rank = metric_proxy_condition(Xemb, W)

        if np.isfinite(corr):
            corrs.append(corr)
        if np.isfinite(stress):
            stresses.append(stress)
        if np.isfinite(cond):
            conds.append(cond)
        ranks.append(rank)
        sizes.append(len(sl))

    n_used = len(corrs)
    med_size = float(np.median(sizes)) if sizes else 0.0
    med_corr = float(np.nanmedian(corrs)) if corrs else float("nan")
    med_stress = float(np.nanmedian(stresses)) if stresses else float("nan")
    med_cond = float(np.nanmedian(conds)) if conds else float("inf")
    med_rank = float(np.nanmedian(ranks)) if ranks else 0.0

    stable = bool(
        n_used >= 2
        and med_size >= 18
        and np.isfinite(med_corr) and med_corr > 0.35
        and np.isfinite(med_stress) and med_stress < 1.25
        and np.isfinite(med_cond) and med_cond < 100
        and med_rank >= 2
    )

    return GraphMetricResult(n_used, med_size, med_corr, med_stress, med_cond, med_rank, stable)


def classify(cfg):
    r = verify(cfg)
    if r.n_slices_used < 1 or not np.isfinite(r.median_embedding_corr):
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=80, seed=313):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slices_used","median_slice_size","median_embedding_corr","median_stress","median_metric_condition","median_metric_rank"]}

    for _ in range(n_sweeps):
        cfg = GraphMetricConfig(
            n_events=int(rng.integers(240, 500)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            embed_dim=3,
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = GraphMetricConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, 3, cfg.seed)
        elif roll < 0.10:
            cfg = GraphMetricConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, 3, cfg.seed)
        elif roll < 0.13:
            cfg = GraphMetricConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, 3, cfg.seed)

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
    print("Antichain graph metric verifier")
    print("="*50)
    print("Route:")
    print("antichain causal-profile graph -> Laplacian embedding -> spatial metric proxy")
    print("Coordinates are used only for hidden embedding-quality evaluation.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
