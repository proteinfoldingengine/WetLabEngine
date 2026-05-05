
"""
causal_slice_lorentzian_metric_verifier.py

Verifier for CAUSAL_SLICE_LORENTZIAN_METRIC.md.

Goal:
Assemble a local Lorentzian metric candidate from:
    - causal rank / longest-chain depth as time
    - antichain graph Laplacian embedding as spatial coordinates
    - spatial metric proxy h_ab from neighbor covariance
    - lapse-like scale N

Candidate local ADM-like block metric:
    g_mu_nu =
        [ -N^2    0  ]
        [  0     h_ab ]

This verifier does not prove full Lorentzian geometry or curvature.
It checks:
    - rank time correlates with hidden time in synthetic data
    - antichain graph gives full-rank h_ab proxy
    - assembled g has signature (-,+,+,+)
    - condition numbers are controlled
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass(frozen=True)
class SliceLorentzConfig:
    n_events: int = 380
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 337


@dataclass(frozen=True)
class SliceLorentzResult:
    n_slices_used: int
    depth_time_corr: float
    median_h_rank: float
    median_h_condition: float
    signature_fraction: float
    median_g_condition: float
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


def rank_slices(depth, min_size=20):
    return [np.where(depth == d)[0] for d in np.unique(depth) if np.sum(depth == d) >= min_size]


def causal_profiles(closure, sl):
    profiles = []
    for i in sl:
        profiles.append(np.concatenate([closure[:, i], closure[i, :]]).astype(float))
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
                W[a, b] = max(0, sim[a, b])
    return np.maximum(W, W.T)


def laplacian_embedding(W, embed_dim=3):
    n = W.shape[0]
    deg = np.sum(W, axis=1)
    if np.sum(deg > 0) < embed_dim + 2:
        return None
    invsqrt = np.zeros_like(deg)
    mask = deg > 1e-12
    invsqrt[mask] = 1.0 / np.sqrt(deg[mask])
    L = np.eye(n) - (invsqrt[:, None] * W * invsqrt[None, :])
    vals, vecs = np.linalg.eigh(L)
    idx = np.argsort(vals)
    vecs = vecs[:, idx]
    return vecs[:, 1:embed_dim+1]


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
    h = np.linalg.inv(C)
    return h


def assemble_g(h, lapse=1.0):
    d = h.shape[0]
    g = np.zeros((d+1, d+1))
    g[0, 0] = -lapse**2
    g[1:, 1:] = h
    return g


def signature_ok(g):
    eig = np.linalg.eigvalsh(g)
    n_neg = int(np.sum(eig < -1e-8))
    n_pos = int(np.sum(eig > 1e-8))
    return n_neg == 1 and n_pos == g.shape[0]-1, eig


def verify(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)

    depth_time_corr = float(np.corrcoef(depth, t)[0, 1]) if np.std(depth) > 1e-12 else np.nan

    slices = rank_slices(depth, min_size=max(20, cfg.n_events // 35))
    h_ranks, h_conds, g_conds = [], [], []
    sigs = []

    for sl in slices[:35]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        Xemb = laplacian_embedding(W, embed_dim=cfg.spatial_dim)
        if Xemb is None:
            continue
        h = h_proxy_from_embedding(Xemb, W)
        if h is None:
            continue

        h_eig = np.linalg.eigvalsh(h)
        h_rank = int(np.sum(h_eig > 1e-8))
        h_cond = float(np.max(h_eig) / np.min(h_eig)) if np.min(h_eig) > 0 else np.inf

        # simple lapse from median depth step; normalized to 1 for now.
        g = assemble_g(h, lapse=1.0)
        ok, eig = signature_ok(g)
        g_abs = np.abs(eig)
        g_cond = float(np.max(g_abs) / np.min(g_abs)) if np.min(g_abs) > 1e-10 else np.inf

        h_ranks.append(h_rank)
        h_conds.append(h_cond)
        g_conds.append(g_cond)
        sigs.append(ok)

    n_used = len(h_ranks)
    sig_frac = float(np.mean(sigs)) if sigs else 0.0
    med_rank = float(np.median(h_ranks)) if h_ranks else 0.0
    med_h_cond = float(np.median(h_conds)) if h_conds else np.inf
    med_g_cond = float(np.median(g_conds)) if g_conds else np.inf

    stable = bool(
        n_used >= 2
        and np.isfinite(depth_time_corr) and depth_time_corr > 0.75
        and med_rank >= cfg.spatial_dim
        and sig_frac > 0.95
        and np.isfinite(med_h_cond) and med_h_cond < 100
        and np.isfinite(med_g_cond) and med_g_cond < 200
    )

    return SliceLorentzResult(n_used, depth_time_corr, med_rank, med_h_cond, sig_frac, med_g_cond, stable)


def classify(cfg):
    r = verify(cfg)
    if r.n_slices_used < 1 or not np.isfinite(r.depth_time_corr):
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=80, seed=347):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slices_used","depth_time_corr","median_h_rank","median_h_condition","signature_fraction","median_g_condition"]}

    for _ in range(n_sweeps):
        cfg = SliceLorentzConfig(
            n_events=int(rng.integers(240, 520)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = SliceLorentzConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = SliceLorentzConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = SliceLorentzConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("Causal slice Lorentzian metric verifier")
    print("="*50)
    print("Route:")
    print("longest-chain time + antichain spatial h_ab -> ADM-like block g_mu_nu")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
