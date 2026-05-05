
"""
causal_slice_curvature_verifier.py

Verifier for CAUSAL_SLICE_CURVATURE.md.

Goal:
Estimate curvature-like diagnostics from slice-wise Lorentzian metrics assembled as:
    g_mu_nu(k) = diag(-N_k^2, h_ab(k))

This is a proxy verifier, not full Riemann/Ricci curvature.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SliceCurvConfig:
    n_events: int = 320
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 383


@dataclass(frozen=True)
class SliceCurvResult:
    n_metric_slices: int
    median_h_condition: float
    median_metric_velocity: float
    median_metric_acceleration: float
    median_log_volume_curvature: float
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
        return None
    invsqrt = np.zeros_like(deg)
    mask = deg > 1e-12
    invsqrt[mask] = 1.0 / np.sqrt(deg[mask])
    L = np.eye(n) - invsqrt[:, None] * W * invsqrt[None, :]
    vals, vecs = np.linalg.eigh(L)
    idx = np.argsort(vals)
    return vecs[:, idx][:, 1:embed_dim+1]


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


def collect_slice_metrics(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 35))

    metrics, ranks, conds, logvols = [], [], [], []

    for d, sl in slices[:30]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        Xemb = laplacian_embedding(W, embed_dim=cfg.spatial_dim)
        if Xemb is None:
            continue
        h = h_proxy_from_embedding(Xemb, W)
        if h is None:
            continue
        eig = np.linalg.eigvalsh(h)
        if np.min(eig) <= 1e-10:
            continue
        cond = float(np.max(eig) / np.min(eig))
        if not np.isfinite(cond) or cond > 1e4:
            continue
        sign, logdet = np.linalg.slogdet(h)
        if sign <= 0 or not np.isfinite(logdet):
            continue
        metrics.append(h)
        ranks.append(d)
        conds.append(cond)
        logvols.append(0.5 * float(logdet))

    return np.asarray(ranks), metrics, np.asarray(conds), np.asarray(logvols)


def verify(cfg):
    ranks, metrics, conds, logvols = collect_slice_metrics(cfg)
    n = len(metrics)
    if n < 4:
        return SliceCurvResult(n, np.inf, np.inf, np.inf, np.inf, 0.0, False)

    idx = np.argsort(ranks)
    ranks = ranks[idx]
    metrics = [metrics[i] for i in idx]
    conds = conds[idx]
    logvols = logvols[idx]

    velocities, accelerations, vol_curvs = [], [], []

    for i in range(n - 1):
        dt = max(1, ranks[i+1] - ranks[i])
        velocities.append(np.linalg.norm(metrics[i+1] - metrics[i]) / dt)

    for i in range(1, n - 1):
        dt1 = max(1, ranks[i] - ranks[i-1])
        dt2 = max(1, ranks[i+1] - ranks[i])
        v1 = (metrics[i] - metrics[i-1]) / dt1
        v2 = (metrics[i+1] - metrics[i]) / dt2
        accelerations.append(np.linalg.norm(v2 - v1) / max(1, (dt1 + dt2) / 2))
        vol_curvs.append(abs((logvols[i+1] - 2*logvols[i] + logvols[i-1]) / max(1, ((dt1+dt2)/2)**2)))

    vals = np.asarray(velocities + accelerations + vol_curvs, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0

    med_cond = float(np.median(conds)) if len(conds) else np.inf
    med_vel = float(np.nanmedian(velocities)) if velocities else np.inf
    med_acc = float(np.nanmedian(accelerations)) if accelerations else np.inf
    med_volcurv = float(np.nanmedian(vol_curvs)) if vol_curvs else np.inf

    stable = bool(
        n >= 4
        and finite_fraction > 0.99
        and np.isfinite(med_cond) and med_cond < 250
        and np.isfinite(med_vel) and med_vel < 250
        and np.isfinite(med_acc) and med_acc < 800
        and np.isfinite(med_volcurv) and med_volcurv < 40
    )

    return SliceCurvResult(n, med_cond, med_vel, med_acc, med_volcurv, finite_fraction, stable)


def classify(cfg):
    r = verify(cfg)
    if r.n_metric_slices < 3 or r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=40, seed=389):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_metric_slices","median_h_condition","median_metric_velocity","median_metric_acceleration","median_log_volume_curvature","finite_fraction"]}

    for _ in range(n_sweeps):
        cfg = SliceCurvConfig(
            n_events=int(rng.integers(260, 460)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = SliceCurvConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = SliceCurvConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = SliceCurvConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("Causal slice curvature verifier")
    print("="*50)
    print("Route:")
    print("slice Lorentzian metrics -> finite slice variation -> curvature proxies")
    print("This is not full Riemann/Ricci curvature.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
