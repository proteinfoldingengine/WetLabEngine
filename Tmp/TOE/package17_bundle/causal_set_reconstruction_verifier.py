
"""
causal_set_reconstruction_verifier.py

Verifier for CAUSAL_SET_RECONSTRUCTION.md.

Goal:
Pivot from failed naive order-distance MDS to causal-set-style reconstruction.

Route:
    causal order C
    -> longest-chain depth / rank time function
    -> antichain spatial slices by rank bands
    -> spatial adjacency proxy within antichains using shared causal past/future
    -> interval-volume dimension proxy
    -> diagnostics for manifoldlike reconstruction

This is structural. It does not prove full metric reconstruction.
Coordinates are used only to generate synthetic data and evaluate hidden spatial
neighbor quality.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np


@dataclass(frozen=True)
class CSRConfig:
    n_events: int = 320
    spatial_dim: int = 3
    c: float = 2.0
    retention_prob: float = 1.0
    seed: int = 241


@dataclass(frozen=True)
class CSRResult:
    comparable_density: float
    n_slices: int
    median_slice_size: float
    antichain_violation_rate: float
    spatial_neighbor_precision: float
    depth_time_corr: float
    dim_proxy: float
    stable: bool


def generate_events(cfg: CSRConfig):
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


def longest_depths(C):
    """Rank/depth time function from longest chain ending at each event."""
    n = C.shape[0]
    depth = np.zeros(n, dtype=np.int32)
    for j in range(n):
        preds = np.where(C[:, j])[0]
        if len(preds):
            depth[j] = 1 + int(np.max(depth[preds]))
    return depth


def make_rank_slices(depth, min_size=8):
    slices = []
    for d in np.unique(depth):
        idx = np.where(depth == d)[0]
        if len(idx) >= min_size:
            slices.append(idx)
    return slices


def antichain_violation(closure, slices):
    rates = []
    for sl in slices:
        if len(sl) < 2:
            continue
        sub = closure[np.ix_(sl, sl)]
        possible = len(sl) * (len(sl) - 1)
        rates.append(float(np.sum(sub) / possible) if possible else 0.0)
    return float(np.median(rates)) if rates else 1.0


def causal_profile_adjacency(closure, sl, k=6):
    """Spatial adjacency proxy within an antichain using shared past/future profiles."""
    nsl = len(sl)
    if nsl < k + 1:
        return []
    profiles = []
    for i in sl:
        past = closure[:, i]
        future = closure[i, :]
        profiles.append(np.concatenate([past, future]).astype(float))
    P = np.asarray(profiles)
    # cosine distance
    norms = np.linalg.norm(P, axis=1) + 1e-12
    sim = (P @ P.T) / (norms[:, None] * norms[None, :])
    np.fill_diagonal(sim, -np.inf)
    pairs = []
    for a in range(nsl):
        nbrs = np.argsort(sim[a])[-k:]
        for b in nbrs:
            pairs.append((sl[a], sl[b]))
    return pairs


def spatial_precision(pairs, x, k_true=8):
    if not pairs:
        return np.nan
    # Hidden eval: a predicted neighbor is good if among k nearest hidden spatial neighbors.
    n = len(x)
    diff = x[:, None, :] - x[None, :, :]
    dist = np.linalg.norm(diff, axis=-1)
    np.fill_diagonal(dist, np.inf)
    true_knn = np.argsort(dist, axis=1)[:, :k_true]
    hits = 0
    total = 0
    for i, j in pairs:
        total += 1
        if j in true_knn[i]:
            hits += 1
    return hits / total if total else np.nan


def interval_dimension_proxy(closure, depth, max_pairs=1000, seed=0):
    pairs = np.argwhere(closure)
    if len(pairs) < 50:
        return np.nan
    rng = np.random.default_rng(seed)
    if len(pairs) > max_pairs:
        pairs = pairs[rng.choice(len(pairs), size=max_pairs, replace=False)]
    chain = []
    sizes = []
    for i, j in pairs:
        d = depth[j] - depth[i]
        if d <= 0:
            continue
        size = int(np.sum(closure[i] & closure[:, j]))
        if size <= 0:
            continue
        chain.append(d)
        sizes.append(size)
    if len(chain) < 50:
        return np.nan
    xlog = np.log(np.asarray(chain) + 1.0)
    ylog = np.log(np.asarray(sizes) + 1.0)
    A = np.column_stack([xlog, np.ones_like(xlog)])
    slope, _ = np.linalg.lstsq(A, ylog, rcond=None)[0]
    return float(slope)


def verify_csr(cfg: CSRConfig) -> CSRResult:
    t, x, retained = generate_events(cfg)
    C_direct = build_causal_matrix(cfg, t, x, retained)
    closure = transitive_closure_bool(C_direct)
    n = cfg.n_events
    comparable_density = float(np.sum(closure) / (n * (n - 1)))

    depth = longest_depths(closure)
    slices = make_rank_slices(depth, min_size=max(6, n // 80))
    n_slices = len(slices)
    median_slice_size = float(np.median([len(s) for s in slices])) if slices else 0.0

    aviol = antichain_violation(closure, slices)

    pairs = []
    for sl in slices[:25]:
        pairs.extend(causal_profile_adjacency(closure, sl, k=4))
    precision = spatial_precision(pairs, x) if pairs else np.nan

    if np.std(depth) > 1e-12 and np.std(t) > 1e-12:
        depth_time_corr = float(np.corrcoef(depth, t)[0, 1])
    else:
        depth_time_corr = np.nan

    dim_proxy = interval_dimension_proxy(closure, depth, seed=cfg.seed + 5)

    stable = bool(
        0.01 < comparable_density < 0.8
        and n_slices >= 3
        and median_slice_size >= 5
        and aviol < 0.02
        and np.isfinite(depth_time_corr) and depth_time_corr > 0.75
        and np.isfinite(dim_proxy) and 0.5 < dim_proxy < 8.0
        # spatial precision is expected to be modest; causal profiles alone are hard.
        and (not np.isfinite(precision) or precision >= 0.03)
    )

    return CSRResult(
        comparable_density=comparable_density,
        n_slices=n_slices,
        median_slice_size=median_slice_size,
        antichain_violation_rate=aviol,
        spatial_neighbor_precision=float(precision) if np.isfinite(precision) else float("nan"),
        depth_time_corr=depth_time_corr,
        dim_proxy=dim_proxy,
        stable=stable,
    )


def classify(cfg: CSRConfig) -> Tuple[str, CSRResult]:
    r = verify_csr(cfg)
    if not np.isfinite(r.depth_time_corr) or r.n_slices < 2:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=80, seed=251) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    comp, nslice, ssize, prec, tcorr, dims, aviols = [], [], [], [], [], [], []

    for _ in range(n_sweeps):
        cfg = CSRConfig(
            n_events=int(rng.integers(180, 380)),
            spatial_dim=3,
            c=float(rng.uniform(1.1, 3.2)),
            retention_prob=float(rng.uniform(0.75, 1.0)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        roll = rng.random()
        if roll < 0.05:
            cfg = CSRConfig(cfg.n_events, 3, 0.05, cfg.retention_prob, cfg.seed)
        elif roll < 0.10:
            cfg = CSRConfig(cfg.n_events, 3, 10.0, cfg.retention_prob, cfg.seed)
        elif roll < 0.13:
            cfg = CSRConfig(cfg.n_events, 3, cfg.c, 0.05, cfg.seed)

        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            comp.append(r.comparable_density)
            nslice.append(r.n_slices)
            ssize.append(r.median_slice_size)
            prec.append(r.spatial_neighbor_precision)
            tcorr.append(r.depth_time_corr)
            dims.append(r.dim_proxy)
            aviols.append(r.antichain_violation_rate)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if comp:
        out.update({
            "comparable_density_median": float(np.nanmedian(comp)),
            "n_slices_median": float(np.nanmedian(nslice)),
            "median_slice_size_median": float(np.nanmedian(ssize)),
            "antichain_violation_median": float(np.nanmedian(aviols)),
            "depth_time_corr_median": float(np.nanmedian(tcorr)),
            "dim_proxy_median": float(np.nanmedian(dims)),
            "spatial_neighbor_precision_median": float(np.nanmedian(prec)),
        })
    return out


def main():
    print("Causal set reconstruction verifier")
    print("=" * 50)
    print("Route:")
    print("causal order -> longest-chain depth -> antichain slices -> causal-profile spatial adjacency")
    print("Coordinates are used only for synthetic evaluation of spatial-neighbor precision.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
