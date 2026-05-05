
"""
adm_causal_slice_action_verifier.py

Verifier for ADM_CAUSAL_SLICE_ACTION.md.

Goal:
Build a first ADM-like action proxy from causal-slice geometry.

Inputs from prior seam:
    h_ab(k): antichain graph spatial metric proxy
    N_k: lapse (first pass N=1)
    N_a: shift (first pass zero)
    K_ab proxy: finite difference of h_ab across causal rank
    R3 proxy: graph/intrinsic spatial curvature placeholder via Laplacian roughness
    volume: sqrt(det h)

ADM-like proxy:
    S_proxy = sum_k N_k sqrt(det h_k) * (R3_proxy + K_ab K^ab - K^2) * dt

This is NOT full ADM or Einstein-Hilbert.
It checks whether the assembled action proxy is finite, stable, and not dominated by singular metrics.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ADMConfig:
    n_events: int = 340
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 431


@dataclass(frozen=True)
class ADMResult:
    n_slices: int
    action_proxy: float
    action_abs_proxy: float
    median_volume: float
    median_K_norm: float
    median_R3_proxy: float
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
                W[a, b] = max(0, sim[a, b])
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


def collect_slices(cfg):
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
        # Intrinsic curvature placeholder: low-frequency Laplacian spectral roughness.
        # In a flat uniform slice this should be finite and modest.
        positive = eigvals[eigvals > 1e-8] if eigvals is not None else np.array([])
        R3_proxy = float(np.median(positive[:min(6, len(positive))])) if len(positive) else 0.0
        rows.append((d, h, float(np.sqrt(np.exp(logdet))), R3_proxy))

    rows.sort(key=lambda z: z[0])
    return rows


def verify(cfg):
    rows = collect_slices(cfg)
    n = len(rows)
    if n < 4:
        return ADMResult(n, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0, False)

    action = []
    action_abs = []
    vols = []
    knorms = []
    r3s = []

    for idx in range(1, n-1):
        d_prev, h_prev, vol_prev, _ = rows[idx-1]
        d, h, vol, R3 = rows[idx]
        d_next, h_next, vol_next, _ = rows[idx+1]
        dt1 = max(1, d - d_prev)
        dt2 = max(1, d_next - d)

        hdot = ((h_next - h) / dt2 + (h - h_prev) / dt1) / 2.0
        # first pass N=1, shift=0: K_ab = 1/2 hdot_ab
        Kcov = 0.5 * hdot
        hinv = np.linalg.inv(h)
        Kmixed = hinv @ Kcov
        K_trace = float(np.trace(Kmixed))
        K_ab_Kab = float(np.trace(Kmixed @ Kmixed))
        K_norm = float(np.linalg.norm(Kmixed))

        density = vol * (R3 + K_ab_Kab - K_trace**2)
        action.append(density)
        action_abs.append(abs(density))
        vols.append(vol)
        knorms.append(K_norm)
        r3s.append(R3)

    vals = np.asarray(action + action_abs + vols + knorms + r3s, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0
    S = float(np.nansum(action))
    Sabs = float(np.nansum(action_abs))

    stable = bool(
        n >= 4
        and finite_fraction > 0.99
        and np.isfinite(S)
        and np.isfinite(Sabs)
        and Sabs < 1e5
        and np.nanmedian(vols) < 1e4
        and np.nanmedian(knorms) < 1e3
    )

    return ADMResult(
        n_slices=n,
        action_proxy=S,
        action_abs_proxy=Sabs,
        median_volume=float(np.nanmedian(vols)) if vols else np.nan,
        median_K_norm=float(np.nanmedian(knorms)) if knorms else np.nan,
        median_R3_proxy=float(np.nanmedian(r3s)) if r3s else np.nan,
        finite_fraction=finite_fraction,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.n_slices < 4 or r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=40, seed=439):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slices","action_proxy","action_abs_proxy","median_volume","median_K_norm","median_R3_proxy","finite_fraction"]}

    for _ in range(n_sweeps):
        cfg = ADMConfig(
            n_events=int(rng.integers(260, 460)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = ADMConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = ADMConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = ADMConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("ADM causal slice action verifier")
    print("="*50)
    print("Route:")
    print("h_ab sequence -> K_ab proxy + R3 proxy -> ADM-like action sum")
    print("This is not full ADM/EH convergence.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
