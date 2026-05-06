
"""
memory_exchange_current_adm_verifier.py

Verifier for MEMORY_EXCHANGE_CURRENT_ADM.md.

Goal:
Project memory stress-energy exchange current into ADM-style components.

Continuum target:
    ∇^μ T^mem_{μν} = -Q_ν

ADM proxy components:
    Q_perp  = normal/energy exchange proxy from slice-to-slice change in memory energy density
    Q_a     = spatial/momentum exchange proxy from divergence of projected spatial stress S_ab^mem

Weak-memory expectations:
    Q_perp = O(eta) or O(eta^2), depending on interaction
    Q_a    = O(eta) or O(eta^2)
    halving eta should halve interaction-dominated exchange and quarter kinetic exchange

This is not covariant conservation closure.
It is a finite ADM-proxy exchange-current diagnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ExchangeConfig:
    n_slices: int = 9
    n_points: int = 32
    dim: int = 3
    eta: float = 1e-2
    Z: float = 1.0
    lam: float = 0.2
    v2: float = 1.0
    seed: int = 877


@dataclass(frozen=True)
class ExchangeResult:
    q_perp_norm_median: float
    q_spatial_norm_median: float
    q_total_half_ratio: float
    q_kinetic_half_ratio: float
    finite_fraction: float
    weak_suppression_fraction: float
    stable: bool


def random_spd(rng, dim):
    A = rng.normal(size=(dim, dim))
    return A.T @ A + dim * np.eye(dim)


def make_fields(cfg, eta):
    rng = np.random.default_rng(cfg.seed)
    hs, R, gradR, Tmat = [], [], [], []
    for k in range(cfg.n_slices):
        h = random_spd(rng, cfg.dim)
        if hs:
            h = 0.8 * hs[-1] + 0.2 * h
        hs.append(h)
        # fields across points in slice
        R.append(eta * rng.normal(size=cfg.n_points))
        gradR.append(eta * rng.normal(size=(cfg.n_points, cfg.dim)))
        M = rng.normal(size=(cfg.n_points, cfg.dim, cfg.dim))
        T = 0.5 * (M + np.swapaxes(M, 1, 2))
        Tmat.append(T)
    return hs, np.asarray(R), np.asarray(gradR), np.asarray(Tmat)


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


def energy_density(h, R, grad, Tmat, cfg, include_interaction=True):
    # simple memory energy density proxy:
    # rho = 1/2 Z |grad R|^2 + V(R) + lambda R tr(Tmat)/dim
    hinv = np.linalg.inv(h)
    vals = []
    for r, g, T in zip(R, grad, Tmat):
        grad2 = float(g @ hinv @ g)
        interaction = cfg.lam * r * np.trace(T) / cfg.dim if include_interaction else 0.0
        vals.append(0.5 * cfg.Z * grad2 + potential(r, cfg) + interaction)
    return np.asarray(vals)


def spatial_divergence_proxy(S):
    # Points are unordered; use nearest-index finite differences as a structural proxy.
    # Div_a S_ab ~ discrete difference along point index, averaged.
    dS = np.diff(S, axis=0)
    if len(dS) == 0:
        return np.zeros(S.shape[-1])
    # collapse derivative index to vector by summing first tensor index
    divs = np.sum(dS, axis=1)
    return np.mean(divs, axis=0)


def exchange_norms(cfg, eta, include_interaction=True):
    hs, R, gradR, Tmat = make_fields(cfg, eta)
    q_perp = []
    q_spatial = []
    for k in range(1, cfg.n_slices - 1):
        rho_prev = energy_density(hs[k-1], R[k-1], gradR[k-1], Tmat[k-1], cfg, include_interaction)
        rho_next = energy_density(hs[k+1], R[k+1], gradR[k+1], Tmat[k+1], cfg, include_interaction)
        # normal exchange proxy = time derivative of memory energy density
        qp = float(np.mean(rho_next - rho_prev) / 2.0)
        q_perp.append(abs(qp))

        S = stress_spatial(hs[k], R[k], gradR[k], Tmat[k], cfg, include_interaction)
        qa = spatial_divergence_proxy(S)
        q_spatial.append(np.linalg.norm(qa))

    vals = np.asarray(q_perp + q_spatial, dtype=float)
    finite = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0
    return np.asarray(q_perp), np.asarray(q_spatial), finite


def verify(cfg):
    qp, qs, f1 = exchange_norms(cfg, cfg.eta, include_interaction=True)
    qp_half, qs_half, f2 = exchange_norms(cfg, cfg.eta * 0.5, include_interaction=True)

    qp_kin, qs_kin, f3 = exchange_norms(cfg, cfg.eta, include_interaction=False)
    qp_kin_half, qs_kin_half, f4 = exchange_norms(cfg, cfg.eta * 0.5, include_interaction=False)

    q_total = np.nanmedian(np.concatenate([qp, qs]))
    q_total_half = np.nanmedian(np.concatenate([qp_half, qs_half]))
    q_kin = np.nanmedian(np.concatenate([qp_kin, qs_kin]))
    q_kin_half = np.nanmedian(np.concatenate([qp_kin_half, qs_kin_half]))

    total_ratio = float(q_total_half / (q_total + 1e-12))
    kinetic_ratio = float(q_kin_half / (q_kin + 1e-12))
    finite_fraction = min(f1, f2, f3, f4)

    weak_suppression_fraction = float(np.mean(np.concatenate([qp, qs]) < 0.1))

    stable = bool(
        finite_fraction > 0.99
        and np.isfinite(total_ratio) and 0.30 < total_ratio < 0.70
        and np.isfinite(kinetic_ratio) and 0.15 < kinetic_ratio < 0.35
        and weak_suppression_fraction > 0.75
    )

    return ExchangeResult(
        q_perp_norm_median=float(np.nanmedian(qp)),
        q_spatial_norm_median=float(np.nanmedian(qs)),
        q_total_half_ratio=total_ratio,
        q_kinetic_half_ratio=kinetic_ratio,
        finite_fraction=finite_fraction,
        weak_suppression_fraction=weak_suppression_fraction,
        stable=stable,
    )


def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=250, seed=881):
    rng = np.random.default_rng(seed)
    counts = {"PASS": 0, "SOFT_FAIL": 0, "HARD_FAIL": 0}
    vals = {k: [] for k in [
        "q_perp_norm_median","q_spatial_norm_median","q_total_half_ratio",
        "q_kinetic_half_ratio","finite_fraction","weak_suppression_fraction"
    ]}

    for _ in range(n_sweeps):
        cfg = ExchangeConfig(
            n_slices=int(rng.integers(5, 14)),
            n_points=int(rng.integers(16, 48)),
            dim=3,
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
    print("Memory exchange current ADM verifier")
    print("="*50)
    print("Route:")
    print("project ∇^μ T^mem_{μν} = -Q_ν into ADM normal/spatial exchange proxies")
    print("Checks finite exchange and weak-memory scaling.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
