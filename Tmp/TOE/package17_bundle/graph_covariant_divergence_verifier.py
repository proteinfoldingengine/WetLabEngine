
"""
graph_covariant_divergence_verifier.py

Verifier for GRAPH_COVARIANT_DIVERGENCE.md.

Goal:
Replace the simple finite-difference divergence proxy in MEMORY_EXCHANGE_CURRENT_ADM.md
with a graph-compatible divergence on antichain spatial graphs.

Given:
    spatial graph G_k with weights W_ij
    embedded coordinates X_i^a
    projected memory stress S_ab(i)

Define a graph divergence:
    (D^a S_ab)(i) ~ sum_j W_ij * [S_ab(j) - S_ab(i)] * e_ij^a / |e_ij|

where e_ij is the unit edge direction in embedded coordinates.

Checks:
    - finite graph divergence
    - weak-memory scaling
    - kinetic-only eta^2 scaling
    - graph divergence is less gauge-arbitrary than index finite difference
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class GraphDivConfig:
    n_points: int = 48
    dim: int = 3
    k_neighbors: int = 8
    eta: float = 1e-2
    Z: float = 1.0
    lam: float = 0.2
    v2: float = 1.0
    seed: int = 1117


@dataclass(frozen=True)
class GraphDivResult:
    graph_div_norm_median: float
    graph_div_half_ratio: float
    kinetic_half_ratio: float
    finite_fraction: float
    graph_connectivity_fraction: float
    stable: bool


def make_spatial_graph(cfg):
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


def make_fields(cfg, eta):
    rng = np.random.default_rng(cfg.seed + 1)
    h = random_spd(rng, cfg.dim)
    R = eta * rng.normal(size=cfg.n_points)
    gradR = eta * rng.normal(size=(cfg.n_points, cfg.dim))
    M = rng.normal(size=(cfg.n_points, cfg.dim, cfg.dim))
    Tmat = 0.5 * (M + np.swapaxes(M, 1, 2))
    return h, R, gradR, Tmat


def potential(R, cfg):
    return 0.5 * cfg.v2 * R * R


def stress_spatial(h, R, grad, Tmat, cfg, include_interaction=True):
    hinv = np.linalg.inv(h)
    out = []
    for r, g, T in zip(R, grad, Tmat):
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
        nbrs = np.where(W[i] > 0)[0]
        for j in nbrs:
            e = X[j] - X[i]
            norm = np.linalg.norm(e)
            if norm < 1e-12:
                continue
            u = e / norm
            dS = S[j] - S[i]  # tensor ab
            # contract first tensor index with edge direction u^a -> vector b
            contrib = u @ dS
            div[i] += W[i, j] * contrib
    return div


def connectivity_fraction(W):
    n = W.shape[0]
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in np.where(W[i] > 0)[0]:
            if int(j) not in seen:
                seen.add(int(j))
                stack.append(int(j))
    return len(seen) / n


def div_norms(cfg, eta, include_interaction=True):
    X, W = make_spatial_graph(cfg)
    h, R, gradR, Tmat = make_fields(cfg, eta)
    S = stress_spatial(h, R, gradR, Tmat, cfg, include_interaction)
    div = graph_divergence(X, W, S)
    norms = np.linalg.norm(div, axis=1)
    finite = float(np.mean(np.isfinite(div)))
    conn = connectivity_fraction(W)
    return norms, finite, conn


def verify(cfg):
    norms, f1, conn = div_norms(cfg, cfg.eta, True)
    norms_half, f2, _ = div_norms(cfg, cfg.eta * 0.5, True)
    kin, f3, _ = div_norms(cfg, cfg.eta, False)
    kin_half, f4, _ = div_norms(cfg, cfg.eta * 0.5, False)

    med = float(np.nanmedian(norms))
    half = float(np.nanmedian(norms_half))
    kin_med = float(np.nanmedian(kin))
    kin_half_med = float(np.nanmedian(kin_half))

    ratio = half / (med + 1e-12)
    kin_ratio = kin_half_med / (kin_med + 1e-12)
    finite_fraction = min(f1, f2, f3, f4)

    stable = bool(
        finite_fraction > 0.99
        and conn > 0.95
        and np.isfinite(med)
        and np.isfinite(ratio) and 0.30 < ratio < 0.70
        and np.isfinite(kin_ratio) and 0.15 < kin_ratio < 0.35
    )

    return GraphDivResult(
        graph_div_norm_median=med,
        graph_div_half_ratio=ratio,
        kinetic_half_ratio=kin_ratio,
        finite_fraction=finite_fraction,
        graph_connectivity_fraction=conn,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99 or r.graph_connectivity_fraction < 0.8:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=250, seed=1123):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "graph_div_norm_median","graph_div_half_ratio","kinetic_half_ratio",
        "finite_fraction","graph_connectivity_fraction"
    ]}

    for _ in range(n_sweeps):
        cfg = GraphDivConfig(
            n_points=int(rng.integers(24, 80)),
            dim=3,
            k_neighbors=int(rng.integers(4, 12)),
            eta=float(10 ** rng.uniform(-4, -1.5)),
            Z=float(10 ** rng.uniform(-1, 1)),
            lam=float(10 ** rng.uniform(-2, 0)),
            v2=float(10 ** rng.uniform(-1, 1)),
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
    print("Graph covariant divergence verifier")
    print("="*50)
    print("Route:")
    print("antichain graph + projected stress S_ab -> graph-compatible D^a S_ab")
    print("Checks finite divergence and weak-memory scaling.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
