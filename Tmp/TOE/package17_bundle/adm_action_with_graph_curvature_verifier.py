
"""
adm_action_with_graph_curvature_verifier.py

Verifier for ADM_ACTION_WITH_GRAPH_CURVATURE.md.

Goal:
Integrate measured lapse N_k and explicit spatial graph curvature R3_graph,k
into the ADM-like causal-slice action proxy.

Action:
    S_proxy^(N,R3) =
        sum_k N_k sqrt(det h_k) *
        (R3_graph,k + K_ab K^ab - K^2) * delta k

Main branch:
    N_k measured from causal rank/slice density
    N_a = 0
    R3_graph from Forman-style + Ollivier-overlap graph curvature
    K_ab finite difference with lapse

This is not full ADM/EH convergence.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ADMGraphConfig:
    n_events: int = 380
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 653


@dataclass(frozen=True)
class ADMGraphResult:
    n_slices: int
    lapse_median: float
    lapse_cv: float
    R3_graph_median: float
    action_graph_abs: float
    action_spectral_abs: float
    action_ratio: float
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


def laplacian_embedding(W, embed_dim=3):
    n = W.shape[0]
    deg = np.sum(W, axis=1)
    if np.sum(deg > 0) < embed_dim + 2:
        return None, None
    invsqrt = np.zeros_like(deg)
    mask = deg > 1e-12
    invsqrt[mask] = 1.0 / np.sqrt(deg[mask])
    L = np.eye(n) - invsqrt[:, None] * W * invsqrt[None, :]
    vals, vecs = np.linalg.eigh(L)
    idx = np.argsort(vals)
    return vecs[:, idx][:, 1:embed_dim+1], vals[idx]


def h_proxy_from_embedding(Xemb, W):
    diffs = []
    for i in range(W.shape[0]):
        for j in np.where(W[i] > 0)[0]:
            diffs.append(Xemb[j] - Xemb[i])
    if len(diffs) < Xemb.shape[1] + 3:
        return None
    D = np.asarray(diffs)
    C = np.cov(D.T)
    eig = np.linalg.eigvalsh(C)
    if np.min(eig) <= 1e-10:
        return None
    return np.linalg.inv(C)


def forman_curvature(W):
    deg = np.sum(W > 0, axis=1)
    vals = []
    edges = np.argwhere(np.triu(W > 0, k=1))
    for i, j in edges:
        wij = max(W[i, j], 1e-12)
        vals.append(float((4.0 - deg[i] - deg[j]) * wij))
    return np.asarray(vals), len(edges)


def ollivier_overlap_proxy(W):
    A = W > 0
    vals = []
    edges = np.argwhere(np.triu(A, k=1))
    for i, j in edges:
        Ni = set(np.where(A[i])[0])
        Nj = set(np.where(A[j])[0])
        union = len(Ni | Nj)
        if union == 0:
            continue
        vals.append(len(Ni & Nj) / union)
    return np.asarray(vals)


def R3_graph_proxy(W):
    fvals, edges = forman_curvature(W)
    ovals = ollivier_overlap_proxy(W)
    if edges == 0 or len(fvals) == 0 or len(ovals) == 0:
        return None
    return float(np.mean(ovals) + np.mean(fvals) / (edges + 1e-12))


def collect_rows(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 35))

    rows = []
    for d, sl in slices[:30]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        Xemb, eigvals = laplacian_embedding(W, embed_dim=cfg.spatial_dim)
        if Xemb is None:
            continue
        h = h_proxy_from_embedding(Xemb, W)
        if h is None:
            continue
        heig = np.linalg.eigvalsh(h)
        if np.min(heig) <= 1e-10:
            continue
        sign, logdet = np.linalg.slogdet(h)
        if sign <= 0 or not np.isfinite(logdet):
            continue

        positive = eigvals[eigvals > 1e-8] if eigvals is not None else np.array([])
        R3_spectral = float(np.median(positive[:min(6, len(positive))])) if len(positive) else 0.0
        R3_graph = R3_graph_proxy(W)
        if R3_graph is None or not np.isfinite(R3_graph):
            continue
        vol = float(np.sqrt(np.exp(logdet)))
        rows.append((d, len(sl), h, vol, R3_spectral, R3_graph))

    rows.sort(key=lambda z: z[0])
    return rows


def verify(cfg):
    rows = collect_rows(cfg)
    n = len(rows)
    if n < 4:
        return ADMGraphResult(n, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0, False)

    slice_sizes = np.asarray([r[1] for r in rows], dtype=float)
    vbar = np.median(slice_sizes) + 1e-12

    terms_graph = []
    terms_spectral = []
    lapses = []
    R3s = []

    for idx in range(1, n-1):
        d_prev, size_prev, h_prev, _, _, _ = rows[idx-1]
        d, size, h, vol, R3_spectral, R3_graph = rows[idx]
        d_next, size_next, h_next, _, _, _ = rows[idx+1]

        dt1 = max(1, d - d_prev)
        dt2 = max(1, d_next - d)
        local_density = (size_prev + size + size_next) / (3.0 * vbar)
        N = 1.0 / np.sqrt(local_density + 1e-12)
        lapses.append(N)
        R3s.append(R3_graph)

        hdot = ((h_next - h) / dt2 + (h - h_prev) / dt1) / 2.0
        Kcov = 0.5 * hdot / max(N, 1e-12)
        hinv = np.linalg.inv(h)
        Kmixed = hinv @ Kcov
        K_trace = float(np.trace(Kmixed))
        K_ab_Kab = float(np.trace(Kmixed @ Kmixed))

        scalar_graph = R3_graph + K_ab_Kab - K_trace**2
        scalar_spectral = R3_spectral + K_ab_Kab - K_trace**2

        terms_graph.append(N * vol * scalar_graph)
        terms_spectral.append(N * vol * scalar_spectral)

    vals = np.asarray(terms_graph + terms_spectral + lapses + R3s, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0

    graph_abs = float(np.nansum(np.abs(terms_graph)))
    spectral_abs = float(np.nansum(np.abs(terms_spectral)))
    ratio = graph_abs / (spectral_abs + 1e-12)

    lapse_median = float(np.nanmedian(lapses)) if lapses else np.nan
    lapse_cv = float(np.nanstd(lapses) / (abs(lapse_median) + 1e-12)) if lapses else np.nan
    R3_median = float(np.nanmedian(R3s)) if R3s else np.nan

    stable = bool(
        n >= 4
        and finite_fraction > 0.99
        and np.isfinite(lapse_median) and lapse_median > 0
        and np.isfinite(lapse_cv) and lapse_cv < 0.75
        and np.isfinite(R3_median) and abs(R3_median) < 100
        and np.isfinite(ratio) and 0.01 < ratio < 100.0
        and graph_abs < 1e7
    )

    return ADMGraphResult(n, lapse_median, lapse_cv, R3_median, graph_abs, spectral_abs, ratio, finite_fraction, stable)


def classify(cfg):
    r = verify(cfg)
    if r.n_slices < 4 or r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=50, seed=661):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in ["n_slices","lapse_median","lapse_cv","R3_graph_median","action_graph_abs","action_spectral_abs","action_ratio","finite_fraction"]}

    for _ in range(n_sweeps):
        cfg = ADMGraphConfig(
            n_events=int(rng.integers(260, 520)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 12)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = ADMGraphConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = ADMGraphConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = ADMGraphConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("ADM action with graph curvature verifier")
    print("="*50)
    print("Route:")
    print("measured lapse + explicit R3_graph -> ADM-like action proxy")
    print("main branch keeps N_a=0; not full ADM/EH convergence")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
