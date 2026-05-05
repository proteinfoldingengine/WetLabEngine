
"""
lorentzian_signature_map_verifier.py

Verifier for LORENTZIAN_SIGNATURE_MAP.md.

Goal:
Test a first structural Lorentzian signature reconstruction from block coordinates,
causal/time labels, and adjacency.

Candidate route:
    block coordinates with one time-like coordinate + spatial coordinates
    causal-oriented neighbor intervals
    signed interval target:
        ds^2 = -c_t^2 dt^2 + spatial_scale * ||dx||^2
    local least-squares fit of symmetric metric
    signature check: one negative eigenvalue, d-1 positive eigenvalues

This verifier does not prove causal-set emergence, diffeomorphism invariance,
or Einstein-Hilbert convergence. It only checks whether the addition of causal
orientation can support a stable local Lorentzian metric fit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np


@dataclass(frozen=True)
class LorentzConfig:
    n_points: int = 220
    dim: int = 4
    k_neighbors: int = 22
    time_noise: float = 0.02
    geometry_noise: float = 0.12
    spatial_scale_noise: float = 0.12
    seed: int = 53


@dataclass(frozen=True)
class LorentzResult:
    n_valid: int
    valid_fraction: float
    signature_fraction: float
    cond_median: float
    eig_median: tuple
    metric_variation: float
    stable_lorentzian: bool
    nondegenerate: bool


def generate_blocks(cfg: LorentzConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)

    # Coordinates: x[:,0] is time, x[:,1:] spatial.
    t = np.sort(rng.uniform(0, 1, size=cfg.n_points))
    spatial = rng.uniform(0, 1, size=(cfg.n_points, cfg.dim - 1))
    X = np.column_stack([t, spatial])

    # Positive geometry scale. Used for spatial part.
    G = rng.lognormal(mean=0.0, sigma=cfg.geometry_noise, size=cfg.n_points)

    # Local time scale / lapse-like positive factor.
    C = rng.lognormal(mean=0.0, sigma=cfg.time_noise, size=cfg.n_points)

    return X, G, C


def causal_neighbors(X: np.ndarray, k: int) -> np.ndarray:
    # Select nearest neighbors using spacetime coordinate proximity, excluding self.
    diff = X[:, None, :] - X[None, :, :]
    dist2 = np.sum(diff * diff, axis=-1)
    np.fill_diagonal(dist2, np.inf)
    return np.argsort(dist2, axis=1)[:, :k]


def metric_design_rows(dx: np.ndarray) -> np.ndarray:
    k, d = dx.shape
    cols = []
    for a in range(d):
        cols.append(dx[:, a] * dx[:, a])
    for a in range(d):
        for b in range(a + 1, d):
            cols.append(2 * dx[:, a] * dx[:, b])
    return np.column_stack(cols)


def coeffs_to_matrix(coeffs: np.ndarray, d: int) -> np.ndarray:
    M = np.zeros((d, d))
    idx = 0
    for a in range(d):
        M[a, a] = coeffs[idx]
        idx += 1
    for a in range(d):
        for b in range(a + 1, d):
            M[a, b] = M[b, a] = coeffs[idx]
            idx += 1
    return M


def estimate_local_lorentz_metric(X: np.ndarray, G: np.ndarray, C: np.ndarray, nbrs: np.ndarray, i: int) -> np.ndarray | None:
    xi = X[i]
    dx = X[nbrs[i]] - xi

    dt = dx[:, 0]
    dspatial2 = np.sum(dx[:, 1:] * dx[:, 1:], axis=1)

    # Signed interval target.
    c_local = 0.5 * (C[i] + C[nbrs[i]])
    g_local = 0.5 * (G[i] + G[nbrs[i]])
    targets = -(c_local**2) * (dt**2) + g_local * dspatial2

    A = metric_design_rows(dx)
    if A.shape[0] < A.shape[1]:
        return None

    try:
        coeffs, *_ = np.linalg.lstsq(A, targets, rcond=None)
    except np.linalg.LinAlgError:
        return None

    return coeffs_to_matrix(coeffs, X.shape[1])


def signature_counts(eig: np.ndarray, eps: float = 1e-8) -> Tuple[int, int, int]:
    n_neg = int(np.sum(eig < -eps))
    n_pos = int(np.sum(eig > eps))
    n_zero = len(eig) - n_neg - n_pos
    return n_neg, n_pos, n_zero


def verify_lorentzian(cfg: LorentzConfig, sample_points: int = 70) -> LorentzResult:
    X, G, C = generate_blocks(cfg)

    if not (np.all(G > 0) and np.all(C > 0)):
        return LorentzResult(0, 0.0, 0.0, np.inf, tuple(), np.inf, False, False)

    nbrs = causal_neighbors(X, cfg.k_neighbors)

    rng = np.random.default_rng(cfg.seed + 1)
    point_idx = rng.choice(cfg.n_points, size=min(sample_points, cfg.n_points), replace=False)

    metrics = []
    conds = []
    eigs = []
    sig_ok = 0

    for i in point_idx:
        M = estimate_local_lorentz_metric(X, G, C, nbrs, int(i))
        if M is None or not np.all(np.isfinite(M)) or not np.allclose(M, M.T, atol=1e-8):
            continue

        eig = np.linalg.eigvalsh(M)
        if np.min(np.abs(eig)) <= 1e-8:
            continue

        n_neg, n_pos, n_zero = signature_counts(eig)
        if n_zero != 0:
            continue

        cond = float(np.max(np.abs(eig)) / np.min(np.abs(eig)))
        if not np.isfinite(cond):
            continue

        metrics.append(M)
        conds.append(cond)
        eigs.append(eig)

        if n_neg == 1 and n_pos == cfg.dim - 1:
            sig_ok += 1

    if not metrics:
        return LorentzResult(0, 0.0, 0.0, np.inf, tuple(), np.inf, False, False)

    metrics_arr = np.asarray(metrics)
    mean_metric = np.mean(metrics_arr, axis=0)
    metric_variation = float(np.mean([np.linalg.norm(M - mean_metric) for M in metrics_arr]))

    valid_fraction = len(metrics) / len(point_idx)
    signature_fraction = sig_ok / len(metrics)
    cond_median = float(np.median(conds))
    eig_median = tuple(float(x) for x in np.median(np.asarray(eigs), axis=0))

    nondegenerate = bool(valid_fraction > 0.75 and signature_fraction > 0.8)
    stable_lorentzian = bool(nondegenerate and cond_median < 100 and metric_variation < 3.0)

    return LorentzResult(
        n_valid=len(metrics),
        valid_fraction=float(valid_fraction),
        signature_fraction=float(signature_fraction),
        cond_median=cond_median,
        eig_median=eig_median,
        metric_variation=metric_variation,
        stable_lorentzian=stable_lorentzian,
        nondegenerate=nondegenerate,
    )


def classify(cfg: LorentzConfig) -> Tuple[str, LorentzResult]:
    r = verify_lorentzian(cfg)
    if not r.nondegenerate:
        return "HARD_FAIL", r
    if not r.stable_lorentzian:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps: int = 250, seed: int = 59) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}

    valid_fracs = []
    sig_fracs = []
    conds = []
    variations = []

    for _ in range(n_sweeps):
        cfg = LorentzConfig(
            n_points=int(rng.integers(140, 280)),
            dim=4,
            k_neighbors=int(rng.integers(14, 30)),
            time_noise=float(rng.uniform(0.0, 0.2)),
            geometry_noise=float(rng.uniform(0.01, 0.5)),
            spatial_scale_noise=float(rng.uniform(0.01, 0.4)),
            seed=int(rng.integers(0, 10_000_000)),
        )

        # Inject underdetermined/noisy cases.
        roll = rng.random()
        if roll < 0.04:
            cfg = LorentzConfig(
                n_points=cfg.n_points,
                dim=4,
                k_neighbors=7,  # underdetermined for 4D symmetric metric (10 comps)
                time_noise=cfg.time_noise,
                geometry_noise=cfg.geometry_noise,
                spatial_scale_noise=cfg.spatial_scale_noise,
                seed=cfg.seed,
            )
        elif roll < 0.08:
            cfg = LorentzConfig(
                n_points=cfg.n_points,
                dim=4,
                k_neighbors=cfg.k_neighbors,
                time_noise=1.5,
                geometry_noise=1.5,
                spatial_scale_noise=cfg.spatial_scale_noise,
                seed=cfg.seed,
            )

        label, r = classify(cfg)
        counts[label] += 1

        if label in {"PASS", "SOFT_FAIL"}:
            valid_fracs.append(r.valid_fraction)
            sig_fracs.append(r.signature_fraction)
            conds.append(r.cond_median)
            variations.append(r.metric_variation)

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    if valid_fracs:
        out.update({
            "valid_fraction_median": float(np.median(valid_fracs)),
            "signature_fraction_median": float(np.median(sig_fracs)),
            "cond_median": float(np.median(conds)),
            "metric_variation_median": float(np.median(variations)),
            "valid_fraction_min": float(np.min(valid_fracs)),
        })
    return out


def main() -> None:
    print("Lorentzian signature map verifier")
    print("=" * 50)
    print("Candidate tested:")
    print("time-oriented coordinates + positive lapse/geometry scales + adjacency")
    print("-> signed interval relation")
    print("-> local symmetric metric estimate")
    print("-> signature check: one negative, three positive")
    print()

    results = run_sweep()
    print("Sweep results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
