
"""
order_distance_embedding_verifier.py

Verifier for ORDER_DISTANCE_EMBEDDING.md.

Goal:
Test whether order-only distance proxies can support local embedding and
metric reconstruction.

Pipeline:
    causal relation C_ij
    -> longest-chain lengths L(i,j)
    -> interval cardinalities N(i,j)
    -> D_eff from log N vs log L
    -> order distance d_ord = N^(1/D_eff)
    -> local distance matrix
    -> classical MDS embedding
    -> local Euclidean metric quality / distance correlation

Important:
    Coordinates are used only to generate synthetic causal data and evaluate
    hidden geometric correlation. Reconstruction uses only C_ij-derived data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class EmbedConfig:
    n_events: int = 240
    spatial_dim: int = 3
    c: float = 1.8
    retention_prob: float = 1.0
    seed: int = 173


@dataclass(frozen=True)
class EmbedResult:
    comparable_pairs: int
    local_points: int
    dim_estimate: float
    embedding_stress: float
    hidden_distance_corr: float
    local_rank: int
    stable: bool


def generate_events(cfg: EmbedConfig):
    rng = np.random.default_rng(cfg.seed)
    t = np.sort(rng.uniform(0, 1, size=cfg.n_events))
    x = rng.uniform(0, 1, size=(cfg.n_events, cfg.spatial_dim))
    retained = rng.random(cfg.n_events) < cfg.retention_prob
    return t, x, retained


def build_causal_matrix(cfg: EmbedConfig, t, x, retained) -> np.ndarray:
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
    n = C.shape[0]
    L = np.zeros((n, n), dtype=np.int16)
    for i in range(n - 2, -1, -1):
        js = np.where(C[i])[0]
        for j in js:
            L[i, j] = max(L[i, j], 1)
            reachable = np.where(L[j] > 0)[0]
            if len(reachable):
                L[i, reachable] = np.maximum(L[i, reachable], 1 + L[j, reachable])
    return L


def estimate_dimension_and_order_dist(L: np.ndarray, max_pairs: int = 1200, seed: int = 0):
    closure = L > 0
    pairs = np.argwhere(closure)
    if len(pairs) < 80:
        return np.nan, None, pairs

    rng = np.random.default_rng(seed)
    sample = pairs
    if len(sample) > max_pairs:
        sample = sample[rng.choice(len(sample), size=max_pairs, replace=False)]

    chain = []
    sizes = []
    for i, j in sample:
        between = closure[i] & closure[:, j]
        size = int(np.sum(between))
        if size <= 0 or L[i, j] <= 0:
            continue
        chain.append(float(L[i, j]))
        sizes.append(float(size))

    if len(chain) < 80:
        return np.nan, None, pairs

    xlog = np.log(np.asarray(chain) + 1.0)
    ylog = np.log(np.asarray(sizes) + 1.0)
    A = np.column_stack([xlog, np.ones_like(xlog)])
    slope, _ = np.linalg.lstsq(A, ylog, rcond=None)[0]
    D_eff = float(slope)

    n = L.shape[0]
    Dmat = np.full((n, n), np.nan)
    if np.isfinite(D_eff) and D_eff > 0.2:
        for i, j in pairs:
            size = int(np.sum(closure[i] & closure[:, j]))
            if size > 0:
                d = size ** (1.0 / D_eff)
                Dmat[i, j] = Dmat[j, i] = d
    return D_eff, Dmat, pairs


def classical_mds(D: np.ndarray, embed_dim: int = 3):
    # D must be finite symmetric local distance matrix.
    n = D.shape[0]
    D2 = D ** 2
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ D2 @ J
    vals, vecs = np.linalg.eigh(B)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]
    vecs = vecs[:, idx]
    pos = np.maximum(vals[:embed_dim], 0)
    X = vecs[:, :embed_dim] * np.sqrt(pos)
    rank = int(np.sum(vals > 1e-8))
    return X, vals, rank


def pairwise_dist(X: np.ndarray) -> np.ndarray:
    diff = X[:, None, :] - X[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1))


def corr_flat(A: np.ndarray, B: np.ndarray):
    iu = np.triu_indices_from(A, k=1)
    a = A[iu]
    b = B[iu]
    mask = np.isfinite(a) & np.isfinite(b)
    if np.sum(mask) < 10 or np.std(a[mask]) < 1e-12 or np.std(b[mask]) < 1e-12:
        return np.nan
    return float(np.corrcoef(a[mask], b[mask])[0, 1])


def verify_embedding(cfg: EmbedConfig, local_points: int = 32) -> EmbedResult:
    t, x, retained = generate_events(cfg)
    C = build_causal_matrix(cfg, t, x, retained)
    L = longest_chain_lengths(C)
    D_eff, Dmat, pairs = estimate_dimension_and_order_dist(L, seed=cfg.seed + 4)

    if Dmat is None or not np.isfinite(D_eff):
        return EmbedResult(len(pairs), 0, np.nan, np.nan, np.nan, 0, False)

    # Choose an event with many comparable neighbors.
    finite_counts = np.sum(np.isfinite(Dmat), axis=1)
    center = int(np.argmax(finite_counts))
    candidates = np.where(np.isfinite(Dmat[center]))[0]
    if len(candidates) < local_points:
        return EmbedResult(len(pairs), len(candidates), D_eff, np.nan, np.nan, 0, False)

    # Select nearest order-distance neighbors.
    nearest = candidates[np.argsort(Dmat[center, candidates])[:local_points]]
    Dlocal = Dmat[np.ix_(nearest, nearest)]

    # Fill any missing pair distances using shortest finite fallback.
    finite_vals = Dlocal[np.isfinite(Dlocal)]
    if len(finite_vals) < local_points:
        return EmbedResult(len(pairs), len(nearest), D_eff, np.nan, np.nan, 0, False)
    fill = float(np.nanmedian(finite_vals))
    Dlocal = np.where(np.isfinite(Dlocal), Dlocal, fill)
    np.fill_diagonal(Dlocal, 0.0)

    Xemb, vals, rank = classical_mds(Dlocal, embed_dim=min(3, cfg.spatial_dim))
    Demb = pairwise_dist(Xemb)

    # Stress normalized.
    denom = np.sqrt(np.sum(Dlocal[np.triu_indices_from(Dlocal, k=1)] ** 2)) + 1e-12
    stress = float(np.sqrt(np.sum((Demb[np.triu_indices_from(Demb, k=1)] - Dlocal[np.triu_indices_from(Dlocal, k=1)]) ** 2)) / denom)

    # Hidden spatial/proper geometry correlation for evaluation only.
    Xtrue = x[nearest]
    Dtrue = pairwise_dist(Xtrue)
    hidden_corr = corr_flat(Demb, Dtrue)

    stable = bool(
        np.isfinite(stress)
        and stress < 0.45
        and np.isfinite(hidden_corr)
        and hidden_corr > 0.45
        and rank >= 2
        and 0.5 < D_eff < 8.0
    )

    return EmbedResult(
        comparable_pairs=int(len(pairs)),
        local_points=int(len(nearest)),
        dim_estimate=float(D_eff),
        embedding_stress=stress,
        hidden_distance_corr=hidden_corr,
        local_rank=rank,
        stable=stable,
    )


def classify(cfg: EmbedConfig) -> Tuple[str, EmbedResult]:
    r = verify_embedding(cfg)
    if not np.isfinite(r.dim_estimate) or r.local_points < 16 or not np.isfinite(r.embedding_stress):
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps: int = 60, seed: int = 179) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    dims, stress, corrs, ranks = [], [], [], []

    for _ in range(n_sweeps):
        cfg = EmbedConfig(
            n_events=int(rng.integers(160, 300)),
            spatial_dim=3,
            c=float(rng.uniform(1.3, 3.0)),
            retention_prob=float(rng.uniform(0.8, 1.0)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        roll = rng.random()
        if roll < 0.08:
            cfg = EmbedConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.seed)
        elif roll < 0.12:
            cfg = EmbedConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            dims.append(r.dim_estimate)
            stress.append(r.embedding_stress)
            corrs.append(r.hidden_distance_corr)
            ranks.append(r.local_rank)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if dims:
        out.update({
            "dim_estimate_median": float(np.median(dims)),
            "embedding_stress_median": float(np.median(stress)),
            "hidden_distance_corr_median": float(np.nanmedian(corrs)),
            "local_rank_median": float(np.median(ranks)),
        })
    return out


def main() -> None:
    print("Order-distance embedding verifier")
    print("=" * 50)
    print("Pipeline:")
    print("causal order -> chain/interval distances -> local MDS embedding -> metric proxy")
    print("Hidden coordinates are used only for evaluation correlation.")
    print()

    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
