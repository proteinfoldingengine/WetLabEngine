
"""
spatial_graph_curvature_verifier.py

Verifier for SPATIAL_GRAPH_CURVATURE.md.

Goal:
Replace the spectral placeholder R3_proxy in ADM_ACTION_WITH_LAPSE.md with
explicit spatial graph curvature proxies on antichain slices.

Candidate estimators:
    1. Forman-Ricci curvature on unweighted/weighted graph edges
    2. Ollivier-style proxy via neighbor-overlap transport surrogate
    3. Scalar slice curvature = mean edge curvature / graph volume normalization

This is NOT continuum R^(3). It tests whether graph curvature estimates are finite,
stable, and structurally meaningful on antichain spatial graphs.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SpatialCurvConfig:
    n_events: int = 360
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 601


@dataclass(frozen=True)
class SpatialCurvResult:
    n_slices: int
    median_edges: float
    forman_median: float
    forman_iqr: float
    ollivier_proxy_median: float
    scalar_R3_median: float
    finite_fraction: float
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
    out = []
    for d in np.unique(depth):
        idx = np.where(depth == d)[0]
        if len(idx) >= min_size:
            out.append((int(d), idx))
    return out


def causal_profiles(closure, sl):
    return np.asarray([np.concatenate([closure[:, i], closure[i, :]]).astype(float) for i in sl])


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
    return np.maximum(W, W.T)


def forman_curvature(W):
    # Weighted Forman-like edge curvature with unit vertex weights:
    # F(e_ij) = w_ij * (2/w_ij - sum_{e_i~e} 1/sqrt(w_ij*w_i*) - sum_{e_j~e} ...)
    # Simplified finite proxy for positive weights.
    n = W.shape[0]
    deg = np.sum(W > 0, axis=1)
    vals = []
    edges = np.argwhere(np.triu(W > 0, k=1))
    for i, j in edges:
        wij = max(W[i, j], 1e-12)
        # unweighted classic proxy: 4 - deg(i) - deg(j)
        # weight-adjusted damping prevents huge values
        f = (4.0 - deg[i] - deg[j]) * wij
        vals.append(float(f))
    return np.asarray(vals), len(edges)


def ollivier_overlap_proxy(W):
    # Cheap Ollivier-like proxy:
    # curvature high when adjacent nodes have overlapping neighborhoods.
    # kappa_ij ~= Jaccard(N_i, N_j), centered by sparse baseline.
    n = W.shape[0]
    A = W > 0
    vals = []
    edges = np.argwhere(np.triu(A, k=1))
    for i, j in edges:
        Ni = set(np.where(A[i])[0])
        Nj = set(np.where(A[j])[0])
        union = len(Ni | Nj)
        inter = len(Ni & Nj)
        if union == 0:
            continue
        vals.append(inter / union)
    return np.asarray(vals)


def verify(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 35))

    all_forman = []
    all_olli = []
    scalar_R3 = []
    edge_counts = []

    for d, sl in slices[:30]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        if W.shape[0] < 8:
            continue
        fvals, edges = forman_curvature(W)
        ovals = ollivier_overlap_proxy(W)
        if edges < len(sl):
            continue
        if len(fvals) == 0 or len(ovals) == 0:
            continue

        # scalar R3 proxy: normalized mean of edge curvatures
        # combine Forman magnitude with overlap curvature to avoid pure degree artifact
        fmean = float(np.mean(fvals))
        omean = float(np.mean(ovals))
        R3 = omean + fmean / (edges + 1e-12)

        all_forman.extend(list(fvals))
        all_olli.extend(list(ovals))
        scalar_R3.append(R3)
        edge_counts.append(edges)

    vals = np.asarray(all_forman + all_olli + scalar_R3, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0

    if len(scalar_R3) == 0:
        return SpatialCurvResult(0, 0, np.nan, np.nan, np.nan, np.nan, 0.0, False)

    f = np.asarray(all_forman, dtype=float)
    o = np.asarray(all_olli, dtype=float)
    r = np.asarray(scalar_R3, dtype=float)

    forman_med = float(np.nanmedian(f))
    forman_iqr = float(np.nanpercentile(f, 75) - np.nanpercentile(f, 25))
    olli_med = float(np.nanmedian(o))
    r3_med = float(np.nanmedian(r))

    stable = bool(
        len(scalar_R3) >= 3
        and finite_fraction > 0.99
        and np.isfinite(forman_med)
        and np.isfinite(forman_iqr) and forman_iqr < 200
        and np.isfinite(olli_med) and 0 <= olli_med <= 1
        and np.isfinite(r3_med) and abs(r3_med) < 100
        and np.nanmedian(edge_counts) > 10
    )

    return SpatialCurvResult(
        n_slices=len(scalar_R3),
        median_edges=float(np.nanmedian(edge_counts)),
        forman_median=forman_med,
        forman_iqr=forman_iqr,
        ollivier_proxy_median=olli_med,
        scalar_R3_median=r3_med,
        finite_fraction=finite_fraction,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.n_slices < 2 or r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=60, seed=607):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in ["n_slices","median_edges","forman_median","forman_iqr","ollivier_proxy_median","scalar_R3_median","finite_fraction"]}

    for _ in range(n_sweeps):
        cfg = SpatialCurvConfig(
            n_events=int(rng.integers(260, 520)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 12)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = SpatialCurvConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = SpatialCurvConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = SpatialCurvConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))

    out = {k: 100*v/n_sweeps for k, v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Spatial graph curvature verifier")
    print("="*50)
    print("Route:")
    print("antichain spatial graph + h_ab proxy -> Forman/Ollivier-like R3 graph curvature proxy")
    print("This is not continuum R^(3), but replaces the pure spectral placeholder.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
