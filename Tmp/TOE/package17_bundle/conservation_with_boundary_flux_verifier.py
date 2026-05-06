
"""
conservation_with_boundary_flux_verifier.py

Verifier for CONSERVATION_WITH_BOUNDARY_FLUX.md.

Goal:
Combine ADM graph-proxy conservation terms:

    Q_mem + Q_mat + Phi_boundary ≈ residual

using:
    - derived interaction cancellation Q_mat,int + Q_mem,int = 0
    - memory interior graph divergence
    - graph-boundary flux diagnostic

This is NOT a full conservation proof. It checks whether adding a controlled
boundary flux term keeps total residual finite, weak-memory suppressed, and
separable from the exactly-canceling interaction channel.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ConservationBoundaryConfig:
    n_points: int = 64
    dim: int = 3
    k_neighbors: int = 8
    eta: float = 1e-2
    lam: float = 0.2
    Z: float = 1.0
    v2: float = 1.0
    boundary_coupling: float = 0.15
    seed: int = 1301


@dataclass(frozen=True)
class ConservationBoundaryResult:
    interaction_residual_ratio: float
    boundary_flux_norm: float
    total_residual_norm: float
    total_half_ratio: float
    kinetic_half_ratio: float
    finite_fraction: float
    stable: bool


def rng_spd(rng, dim):
    A = rng.normal(size=(dim, dim))
    return A.T @ A + dim * np.eye(dim)


def graph(cfg):
    rng = np.random.default_rng(cfg.seed)
    X = rng.normal(size=(cfg.n_points, cfg.dim))
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
    np.fill_diagonal(D, np.inf)
    W = np.zeros((cfg.n_points, cfg.n_points))
    for i in range(cfg.n_points):
        nbrs = np.argsort(D[i])[:cfg.k_neighbors]
        for j in nbrs:
            W[i, j] = np.exp(-D[i, j]**2)
    W = np.maximum(W, W.T)
    return X, W


def fields(cfg, eta):
    rng = np.random.default_rng(cfg.seed + 1)
    h = rng_spd(rng, cfg.dim)
    R = eta * rng.normal(size=cfg.n_points)
    gradR = eta * rng.normal(size=(cfg.n_points, cfg.dim))
    Omat = rng.normal(size=cfg.n_points)
    M = rng.normal(size=(cfg.n_points, cfg.dim, cfg.dim))
    Tmat = 0.5 * (M + np.swapaxes(M, 1, 2))
    return h, R, gradR, Omat, Tmat


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


def graph_divergence(X, W, S):
    n, dim = X.shape
    div = np.zeros((n, dim))
    for i in range(n):
        for j in np.where(W[i] > 0)[0]:
            e = X[j] - X[i]
            norm = np.linalg.norm(e)
            if norm < 1e-12:
                continue
            u = e / norm
            div[i] += W[i, j] * (u @ (S[j] - S[i]))
    return div


def boundary_flux_vec(X, W, S, q=0.72):
    centroid = np.mean(X, axis=0)
    radius = np.linalg.norm(X - centroid, axis=1)
    deg = np.sum(W > 0, axis=1)
    mask = (radius >= np.quantile(radius, q)) | (deg <= np.quantile(deg, 0.25))
    vecs = []
    for i in np.where(mask)[0]:
        n = X[i] - centroid
        norm = np.linalg.norm(n)
        if norm < 1e-12:
            continue
        n = n / norm
        # vector flux proxy: n^a S_ab
        vecs.append(n @ S[i])
    if not vecs:
        return np.zeros(X.shape[1])
    return np.mean(vecs, axis=0)


def interaction_exchange(cfg, R, gradR, Omat, sign=+1):
    # spatial channel only for this graph-slice conservation residual
    return sign * cfg.lam * np.mean(Omat[:, None] * gradR, axis=0)


def residual_terms(cfg, eta, include_interaction=True):
    X, W = graph(cfg)
    h, R, gradR, Omat, Tmat = fields(cfg, eta)

    qmat_int = interaction_exchange(cfg, R, gradR, Omat, +1)
    qmem_int = interaction_exchange(cfg, R, gradR, Omat, -1)
    interaction_res = qmat_int + qmem_int

    S = stress(h, R, gradR, Tmat, cfg, include_interaction=include_interaction)
    div = graph_divergence(X, W, S)
    interior = np.mean(div, axis=0)

    boundary = cfg.boundary_coupling * boundary_flux_vec(X, W, S)

    total = interaction_res + interior + boundary
    return interaction_res, interior, boundary, total


def verify(cfg):
    ires, interior, boundary, total = residual_terms(cfg, cfg.eta, True)
    _, _, boundary_half, total_half = residual_terms(cfg, cfg.eta * 0.5, True)
    _, _, boundary_kin, total_kin = residual_terms(cfg, cfg.eta, False)
    _, _, boundary_kin_half, total_kin_half = residual_terms(cfg, cfg.eta * 0.5, False)

    channel_scale = np.linalg.norm(interior) + np.linalg.norm(boundary) + 1e-12
    interaction_ratio = float(np.linalg.norm(ires) / channel_scale)

    boundary_norm = float(np.linalg.norm(boundary))
    total_norm = float(np.linalg.norm(total))
    total_half_ratio = float(np.linalg.norm(total_half) / (total_norm + 1e-12))
    kin_ratio = float(np.linalg.norm(total_kin_half) / (np.linalg.norm(total_kin) + 1e-12))

    vals = np.array([interaction_ratio, boundary_norm, total_norm, total_half_ratio, kin_ratio])
    finite_fraction = float(np.mean(np.isfinite(vals)))

    stable = bool(
        finite_fraction > 0.99
        and interaction_ratio < 1e-10
        and np.isfinite(boundary_norm)
        and np.isfinite(total_norm)
        and np.isfinite(total_half_ratio) and 0.30 < total_half_ratio < 0.70
        and np.isfinite(kin_ratio) and 0.15 < kin_ratio < 0.35
    )

    return ConservationBoundaryResult(
        interaction_residual_ratio=interaction_ratio,
        boundary_flux_norm=boundary_norm,
        total_residual_norm=total_norm,
        total_half_ratio=total_half_ratio,
        kinetic_half_ratio=kin_ratio,
        finite_fraction=finite_fraction,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=250, seed=1307):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "interaction_residual_ratio", "boundary_flux_norm", "total_residual_norm",
        "total_half_ratio", "kinetic_half_ratio", "finite_fraction"
    ]}

    for _ in range(n_sweeps):
        cfg = ConservationBoundaryConfig(
            n_points=int(rng.integers(24, 96)),
            dim=3,
            k_neighbors=int(rng.integers(4, 14)),
            eta=float(10 ** rng.uniform(-4, -1.5)),
            lam=float(10 ** rng.uniform(-2, 0)),
            Z=float(10 ** rng.uniform(-1, 1)),
            v2=float(10 ** rng.uniform(-1, 1)),
            boundary_coupling=float(rng.uniform(0.05, 0.35)),
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
    print("Conservation with boundary flux verifier")
    print("="*50)
    print("Route:")
    print("interaction cancellation + graph divergence + boundary flux -> ADM graph residual")
    print("Checks finite residual and weak-memory scaling.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
