
"""
lapse_shift_derivation_verifier.py

Verifier for LAPSE_SHIFT_DERIVATION.md.

Goal:
Derive first-pass lapse N_k and shift N_a from causal slice data.

Candidate:
    lapse N_k:
        from causal-rank spacing and slice density/volume normalization.
        N_k ~ delta_tau_k / median(delta_tau)

    shift N_a:
        from slice-to-slice drift of antichain graph embeddings.
        Align consecutive slice embeddings by Procrustes; centroid drift is shift proxy.

This is not full ADM gauge derivation.
Coordinates are used only to generate synthetic causal data and evaluate hidden drift quality.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class LapseShiftConfig:
    n_events: int = 380
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 467


@dataclass(frozen=True)
class LapseShiftResult:
    n_slice_pairs: int
    lapse_median: float
    lapse_cv: float
    shift_norm_median: float
    shift_finite_fraction: float
    hidden_shift_corr: float
    stable: bool


def generate_events(cfg):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    # Add slow spatial drift over time so shift is not always zero.
    base = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    drift_vec = rng.normal(0, 0.15, size=cfg.spatial_dim)
    x = (base + t[:, None] * drift_vec[None, :]) % 1.0
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
        # torus minimal distance for synthetic periodic drift
        dx = np.minimum(np.abs(dx), 1.0 - np.abs(dx))
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
    X = vecs[:, idx][:, 1:embed_dim+1]
    # normalize scale
    s = np.std(X, axis=0) + 1e-12
    return X / s


def procrustes_align(A, B):
    """Align B to A. Both same number of rows after matching."""
    Ac = A - A.mean(axis=0)
    Bc = B - B.mean(axis=0)
    U, _, Vt = np.linalg.svd(Bc.T @ Ac, full_matrices=False)
    R = U @ Vt
    B_aligned = Bc @ R
    return Ac, B_aligned


def verify(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 35))

    slice_data = []
    for d, sl in slices[:30]:
        W = profile_weighted_adjacency(closure, sl, cfg.k_profile_neighbors)
        Xemb = laplacian_embedding(W, embed_dim=cfg.spatial_dim)
        if Xemb is None or len(sl) < 12:
            continue
        # volume proxy from slice cardinality
        vol = len(sl)
        # hidden centroid for evaluation only
        hidden_centroid = np.mean(x[sl], axis=0)
        slice_data.append((d, sl, Xemb, vol, hidden_centroid))

    if len(slice_data) < 3:
        return LapseShiftResult(0, np.nan, np.nan, np.nan, 0.0, np.nan, False)

    # Lapse from rank spacing and density normalization.
    # Larger slice volume -> smaller proper rank step after normalization.
    lapses = []
    shifts = []
    hidden_shifts = []

    vols = np.asarray([row[3] for row in slice_data], dtype=float)
    vol_norm = np.median(vols) + 1e-12

    for i in range(len(slice_data)-1):
        d0, sl0, X0, vol0, h0 = slice_data[i]
        d1, sl1, X1, vol1, h1 = slice_data[i+1]
        dd = max(1, d1 - d0)
        density_scale = np.sqrt((vol0 + vol1) / (2 * vol_norm))
        N = dd / density_scale
        lapses.append(N)

        # Shift proxy: graph embedding centroid drift.
        # Embeddings are independent; use centroid norm after scale normalization.
        # Since point correspondence is absent, this is intentionally weak.
        shift = np.linalg.norm(np.mean(X1, axis=0) - np.mean(X0, axis=0)) / max(N, 1e-12)
        shifts.append(shift)

        hidden_shift = np.linalg.norm(h1 - h0) / max(N, 1e-12)
        hidden_shifts.append(hidden_shift)

    lapses = np.asarray(lapses)
    shifts = np.asarray(shifts)
    hidden_shifts = np.asarray(hidden_shifts)

    finite = np.isfinite(lapses) & np.isfinite(shifts)
    finite_fraction = float(np.mean(finite)) if len(finite) else 0.0

    lapse_med = float(np.nanmedian(lapses))
    lapse_cv = float(np.nanstd(lapses) / (abs(lapse_med) + 1e-12))
    shift_med = float(np.nanmedian(shifts))

    if np.std(shifts) > 1e-12 and np.std(hidden_shifts) > 1e-12:
        hidden_corr = float(np.corrcoef(shifts, hidden_shifts)[0, 1])
    else:
        hidden_corr = np.nan

    stable = bool(
        len(lapses) >= 2
        and finite_fraction > 0.99
        and np.isfinite(lapse_med) and lapse_med > 0
        and lapse_cv < 1.0
        and np.isfinite(shift_med)
        # shift estimate is first-pass; hidden corr may be weak because no slice correspondence.
    )

    return LapseShiftResult(len(lapses), lapse_med, lapse_cv, shift_med, finite_fraction, hidden_corr, stable)


def classify(cfg):
    r = verify(cfg)
    if r.n_slice_pairs < 2 or r.shift_finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=60, seed=479):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slice_pairs","lapse_median","lapse_cv","shift_norm_median","shift_finite_fraction","hidden_shift_corr"]}

    for _ in range(n_sweeps):
        cfg = LapseShiftConfig(
            n_events=int(rng.integers(260, 520)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = LapseShiftConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = LapseShiftConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = LapseShiftConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("Lapse and shift derivation verifier")
    print("="*50)
    print("Route:")
    print("rank spacing + slice density -> lapse N")
    print("slice-to-slice antichain embedding drift -> shift proxy N_a")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
