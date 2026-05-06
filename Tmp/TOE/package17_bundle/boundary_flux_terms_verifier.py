
"""
boundary_flux_terms_verifier.py

Verifier for BOUNDARY_FLUX_TERMS.md.

Goal:
Add graph-boundary flux accounting to the ADM/Bianchi conservation branch.

Given:
    antichain spatial graph G=(V,E,W)
    embedded coordinates X
    projected memory stress S_ab(i)

Define:
    boundary nodes = low local graph density / low degree / convex hull proxy
    outward normal proxy n_i from centroid to boundary node
    flux_i = n_i^a S_ab(i) n_i^b
    total boundary flux = sum_i boundary_weight_i * flux_i

Checks:
    - finite boundary flux
    - weak-memory scaling O(eta)
    - kinetic-only scaling O(eta^2)
    - boundary fraction neither zero nor whole graph
    - flux remains suppressed in weak-memory regime

This is not continuum boundary integral closure.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class BoundaryFluxConfig:
    n_points: int = 64
    dim: int = 3
    k_neighbors: int = 8
    eta: float = 1e-2
    Z: float = 1.0
    lam: float = 0.2
    v2: float = 1.0
    boundary_quantile: float = 0.70
    seed: int = 1201


@dataclass(frozen=True)
class BoundaryFluxResult:
    boundary_fraction: float
    flux_abs_median: float
    flux_half_ratio: float
    kinetic_half_ratio: float
    finite_fraction: float
    stable: bool


def make_graph(cfg):
    rng = np.random.default_rng(cfg.seed)
    X = rng.normal(size=(cfg.n_points, cfg.dim))
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
    np.fill_diagonal(D, np.inf)
    W = np.zeros((cfg.n_points, cfg.n_points), dtype=float)
    for i in range(cfg.n_points):
        nbrs = np.argsort(D[i])[:cfg.k_neighbors]
        for j in nbrs:
            W[i, j] = np.exp(-D[i, j]**2)
    W = np.maximum(W, W.T)
    return X, W


def random_spd(rng, dim):
    A = rng.normal(size=(dim, dim))
    return A.T @ A + dim * np.eye(dim)


def fields(cfg, eta):
    rng = np.random.default_rng(cfg.seed + 1)
    h = random_spd(rng, cfg.dim)
    R = eta * rng.normal(size=cfg.n_points)
    gradR = eta * rng.normal(size=(cfg.n_points, cfg.dim))
    M = rng.normal(size=(cfg.n_points, cfg.dim, cfg.dim))
    Tmat = 0.5 * (M + np.swapaxes(M, 1, 2))
    return h, R, gradR, Tmat


def potential(R, cfg):
    return 0.5 * cfg.v2 * R * R


def stress(h, R, gradR, Tmat, cfg, include_interaction=True):
    hinv = np.linalg.inv(h)
    out = []
    for r, g, T in zip(R, gradR, Tmat):
        grad2 = float(g @ hinv @ g)
        kinetic = cfg.Z * np.outer(g, g)
        kinetic_trace = -0.5 * h * cfg.Z * grad2
        Vterm = h * potential(r, cfg)
        interaction = -cfg.lam * r * T if include_interaction else 0.0
        out.append(kinetic + kinetic_trace + Vterm + interaction)
    return np.asarray(out)


def boundary_nodes(X, W, q):
    deg = np.sum(W > 0, axis=1)
    centroid = np.mean(X, axis=0)
    radius = np.linalg.norm(X - centroid, axis=1)
    # boundary: high radius or low degree
    r_cut = np.quantile(radius, q)
    d_cut = np.quantile(deg, 0.25)
    mask = (radius >= r_cut) | (deg <= d_cut)
    return mask


def boundary_flux(cfg, eta, include_interaction=True):
    X, W = make_graph(cfg)
    h, R, gradR, Tmat = fields(cfg, eta)
    S = stress(h, R, gradR, Tmat, cfg, include_interaction)
    bmask = boundary_nodes(X, W, cfg.boundary_quantile)
    centroid = np.mean(X, axis=0)
    vals = []
    for i in np.where(bmask)[0]:
        n = X[i] - centroid
        norm = np.linalg.norm(n)
        if norm < 1e-12:
            continue
        n = n / norm
        vals.append(float(n @ S[i] @ n))
    vals = np.asarray(vals, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0
    return vals, float(np.mean(bmask)), finite_fraction


def verify(cfg):
    flux, bf, f1 = boundary_flux(cfg, cfg.eta, True)
    flux_half, _, f2 = boundary_flux(cfg, cfg.eta * 0.5, True)
    kin, _, f3 = boundary_flux(cfg, cfg.eta, False)
    kin_half, _, f4 = boundary_flux(cfg, cfg.eta * 0.5, False)

    med = float(np.nanmedian(np.abs(flux))) if len(flux) else np.nan
    half = float(np.nanmedian(np.abs(flux_half))) if len(flux_half) else np.nan
    kin_med = float(np.nanmedian(np.abs(kin))) if len(kin) else np.nan
    kin_half_med = float(np.nanmedian(np.abs(kin_half))) if len(kin_half) else np.nan

    ratio = half / (med + 1e-12)
    kin_ratio = kin_half_med / (kin_med + 1e-12)
    finite_fraction = min(f1, f2, f3, f4)

    stable = bool(
        finite_fraction > 0.99
        and 0.05 < bf < 0.80
        and np.isfinite(med)
        and med < 0.1
        and np.isfinite(ratio) and 0.30 < ratio < 0.70
        and np.isfinite(kin_ratio) and 0.15 < kin_ratio < 0.35
    )

    return BoundaryFluxResult(bf, med, ratio, kin_ratio, finite_fraction, stable)


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=250, seed=1207):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "boundary_fraction","flux_abs_median","flux_half_ratio",
        "kinetic_half_ratio","finite_fraction"
    ]}

    for _ in range(n_sweeps):
        cfg = BoundaryFluxConfig(
            n_points=int(rng.integers(24, 96)),
            dim=3,
            k_neighbors=int(rng.integers(4, 14)),
            eta=float(10 ** rng.uniform(-4, -1.5)),
            Z=float(10 ** rng.uniform(-1, 1)),
            lam=float(10 ** rng.uniform(-2, 0)),
            v2=float(10 ** rng.uniform(-1, 1)),
            boundary_quantile=float(rng.uniform(0.60, 0.85)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS", "SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))

    out = {k: 100 * v / n_sweeps for k, v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out


def main():
    print("Boundary flux terms verifier")
    print("="*50)
    print("Route:")
    print("graph boundary nodes + projected stress -> boundary flux proxy")
    print("Checks finite flux and weak-memory scaling.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
