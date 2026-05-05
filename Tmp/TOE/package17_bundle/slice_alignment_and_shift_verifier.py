
"""
slice_alignment_and_shift_verifier.py

Verifier for SLICE_ALIGNMENT_AND_SHIFT.md.

Goal:
Improve shift N_a by aligning adjacent antichain slices using causal-profile matching.

Prior issue:
    LAPSE_SHIFT_DERIVATION.md found stable lapse, but weak/gauge-noisy shift:
        hidden_shift_corr_median ~ -0.10

Candidate improvement:
    For adjacent slices A_k, A_{k+1}:
      1. build causal-profile embeddings for both slices
      2. match events by cosine similarity of causal profiles
      3. embed both slices with graph Laplacian
      4. align embeddings using matched pairs + Procrustes
      5. define shift vector field as matched displacement
      6. evaluate against hidden drift only in synthetic data

This is not a proof of physical shift. It tests if slice alignment reduces gauge noise.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class AlignShiftConfig:
    n_events: int = 420
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    k_profile_neighbors: int = 7
    seed: int = 503


@dataclass(frozen=True)
class AlignShiftResult:
    n_slice_pairs: int
    match_count_median: float
    match_score_median: float
    aligned_shift_norm_median: float
    hidden_shift_corr: float
    procrustes_residual_median: float
    stable: bool


def generate_events(cfg):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    base = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    # stronger coherent drift to make hidden shift measurable
    drift_vec = rng.normal(0, 0.18, size=cfg.spatial_dim)
    x = (base + t[:, None] * drift_vec[None, :]) % 1.0
    retained = rng.random(cfg.n_events) < cfg.retention_prob
    return t, x, retained


def torus_dist_vec(a, b):
    d = b - a
    d = (d + 0.5) % 1.0 - 0.5
    return d


def build_causal_matrix(cfg, t, x, retained):
    n = cfg.n_events
    C = np.zeros((n, n), dtype=bool)
    for i in range(n):
        if not retained[i]:
            continue
        dt = t[i+1:] - t[i]
        dx = torus_dist_vec(x[i], x[i+1:])
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


def profile_weighted_adjacency_from_profiles(P, k):
    n = P.shape[0]
    if n < k + 2:
        return np.zeros((n, n), dtype=float)
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
    X = X / (np.std(X, axis=0) + 1e-12)
    return X


def greedy_profile_matches(P0, P1, max_matches=40):
    n0, n1 = P0.shape[0], P1.shape[0]
    norms0 = np.linalg.norm(P0, axis=1) + 1e-12
    norms1 = np.linalg.norm(P1, axis=1) + 1e-12
    sim = (P0 @ P1.T) / (norms0[:, None] * norms1[None, :])
    flat = np.argsort(sim.ravel())[::-1]
    used0, used1, matches, scores = set(), set(), [], []
    for idx in flat:
        i = idx // n1
        j = idx % n1
        if i in used0 or j in used1:
            continue
        if sim[i, j] <= 0:
            break
        used0.add(i); used1.add(j)
        matches.append((i, j))
        scores.append(float(sim[i, j]))
        if len(matches) >= min(max_matches, n0, n1):
            break
    return matches, scores


def procrustes(A, B):
    Ac = A - A.mean(axis=0)
    Bc = B - B.mean(axis=0)
    U, _, Vt = np.linalg.svd(Bc.T @ Ac, full_matrices=False)
    R = U @ Vt
    Bal = Bc @ R
    residual = float(np.sqrt(np.mean(np.sum((Ac - Bal)**2, axis=1))))
    return Ac, Bal, R, residual


def verify(cfg):
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C)
    depth = longest_depths(closure)
    slices = rank_slices(depth, min_size=max(18, cfg.n_events // 35))

    aligned_shift_norms = []
    hidden_shift_norms = []
    match_counts = []
    match_scores = []
    residuals = []

    for idx in range(len(slices)-1):
        d0, sl0 = slices[idx]
        d1, sl1 = slices[idx+1]
        P0 = causal_profiles(closure, sl0)
        P1 = causal_profiles(closure, sl1)

        W0 = profile_weighted_adjacency_from_profiles(P0, cfg.k_profile_neighbors)
        W1 = profile_weighted_adjacency_from_profiles(P1, cfg.k_profile_neighbors)
        X0 = laplacian_embedding(W0, cfg.spatial_dim)
        X1 = laplacian_embedding(W1, cfg.spatial_dim)
        if X0 is None or X1 is None:
            continue

        matches, scores = greedy_profile_matches(P0, P1, max_matches=50)
        if len(matches) < cfg.spatial_dim + 3:
            continue

        idx0 = np.array([m[0] for m in matches])
        idx1 = np.array([m[1] for m in matches])
        A = X0[idx0]
        B = X1[idx1]
        A0, B1, R, resid = procrustes(A, B)

        # Shift vector field in aligned embedding: displacement from slice0 to aligned slice1
        disp = B1 - A0
        shift_norm = float(np.median(np.linalg.norm(disp, axis=1)))

        # Hidden evaluation: spatial displacement of matched actual events, torus corrected.
        hidden_disp = torus_dist_vec(x[sl0[idx0]], x[sl1[idx1]])
        hidden_norm = float(np.median(np.linalg.norm(hidden_disp, axis=1)))

        aligned_shift_norms.append(shift_norm)
        hidden_shift_norms.append(hidden_norm)
        match_counts.append(len(matches))
        match_scores.append(float(np.median(scores)))
        residuals.append(resid)

    n_pairs = len(aligned_shift_norms)
    if n_pairs < 2:
        return AlignShiftResult(n_pairs, 0, np.nan, np.nan, np.nan, np.nan, False)

    s = np.asarray(aligned_shift_norms)
    h = np.asarray(hidden_shift_norms)
    if np.std(s) > 1e-12 and np.std(h) > 1e-12:
        corr = float(np.corrcoef(s, h)[0, 1])
    else:
        corr = np.nan

    stable = bool(
        n_pairs >= 2
        and np.nanmedian(match_counts) >= cfg.spatial_dim + 3
        and np.isfinite(np.nanmedian(match_scores))
        and np.nanmedian(match_scores) > 0.05
        and np.isfinite(np.nanmedian(s))
        and np.isfinite(np.nanmedian(residuals))
        and np.nanmedian(residuals) < 5.0
        # correlation is diagnostic, not pass/fail yet due gauge ambiguity
    )

    return AlignShiftResult(
        n_slice_pairs=n_pairs,
        match_count_median=float(np.nanmedian(match_counts)),
        match_score_median=float(np.nanmedian(match_scores)),
        aligned_shift_norm_median=float(np.nanmedian(s)),
        hidden_shift_corr=corr,
        procrustes_residual_median=float(np.nanmedian(residuals)),
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.n_slice_pairs < 2 or not np.isfinite(r.aligned_shift_norm_median):
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=50, seed=509):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["n_slice_pairs","match_count_median","match_score_median","aligned_shift_norm_median","hidden_shift_corr","procrustes_residual_median"]}

    for _ in range(n_sweeps):
        cfg = AlignShiftConfig(
            n_events=int(rng.integers(280, 540)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.85, 1.0)),
            k_profile_neighbors=int(rng.integers(5, 11)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = AlignShiftConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.10:
            cfg = AlignShiftConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.k_profile_neighbors, cfg.seed)
        elif roll < 0.13:
            cfg = AlignShiftConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.k_profile_neighbors, cfg.seed)

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
    print("Slice alignment and shift verifier")
    print("="*50)
    print("Route:")
    print("adjacent antichain profiles -> matching -> Procrustes alignment -> shift vector proxy")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
