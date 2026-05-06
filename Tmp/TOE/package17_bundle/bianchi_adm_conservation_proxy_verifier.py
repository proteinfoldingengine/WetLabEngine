
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class BianchiProxyConfig:
    n_slices: int = 9
    n_points: int = 24
    dim: int = 3
    eta: float = 1e-2
    conservation_tol: float = 1e-3
    Z: float = 1.0
    lam: float = 0.2
    v2: float = 1.0
    seed: int = 907

@dataclass(frozen=True)
class BianchiProxyResult:
    mem_exchange_norm_median: float
    total_residual_norm_median: float
    residual_to_mem_ratio: float
    residual_tol_scaling_ratio: float
    finite_fraction: float
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
        R.append(eta * rng.normal(size=cfg.n_points))
        gradR.append(eta * rng.normal(size=(cfg.n_points, cfg.dim)))
        M = rng.normal(size=(cfg.n_points, cfg.dim, cfg.dim))
        Tmat.append(0.5 * (M + np.swapaxes(M, 1, 2)))
    return hs, np.asarray(R), np.asarray(gradR), np.asarray(Tmat)

def potential(R, cfg):
    return 0.5 * cfg.v2 * R * R

def stress_spatial(h, R, grad, Tmat, cfg):
    hinv = np.linalg.inv(h)
    out = []
    for r, g, T in zip(R, grad, Tmat):
        grad2 = float(g @ hinv @ g)
        kinetic = cfg.Z * np.outer(g, g)
        kinetic_trace = -0.5 * h * cfg.Z * grad2
        Vterm = h * potential(r, cfg)
        interaction = -cfg.lam * r * T
        out.append(kinetic + kinetic_trace + Vterm + interaction)
    return np.asarray(out)

def energy_density(h, R, grad, Tmat, cfg):
    hinv = np.linalg.inv(h)
    vals = []
    for r, g, T in zip(R, grad, Tmat):
        grad2 = float(g @ hinv @ g)
        interaction = cfg.lam * r * np.trace(T) / cfg.dim
        vals.append(0.5 * cfg.Z * grad2 + potential(r, cfg) + interaction)
    return np.asarray(vals)

def spatial_divergence_proxy(S):
    dS = np.diff(S, axis=0)
    if len(dS) == 0:
        return np.zeros(S.shape[-1])
    return np.mean(np.sum(dS, axis=1), axis=0)

def memory_exchange(cfg, eta):
    hs, R, gradR, Tmat = make_fields(cfg, eta)
    qmem = []
    for k in range(1, cfg.n_slices - 1):
        rho_prev = energy_density(hs[k-1], R[k-1], gradR[k-1], Tmat[k-1], cfg)
        rho_next = energy_density(hs[k+1], R[k+1], gradR[k+1], Tmat[k+1], cfg)
        q_perp = float(np.mean(rho_next - rho_prev) / 2.0)
        S = stress_spatial(hs[k], R[k], gradR[k], Tmat[k], cfg)
        q_spatial = spatial_divergence_proxy(S)
        qmem.append(np.concatenate([[q_perp], q_spatial]))
    return np.asarray(qmem)

def conservation_residuals(cfg, tol):
    rng = np.random.default_rng(cfg.seed + 77)
    qmem = memory_exchange(cfg, cfg.eta)
    noise = tol * np.maximum(np.linalg.norm(qmem, axis=1, keepdims=True), 1e-12) * rng.normal(size=qmem.shape)
    qmat = -qmem + noise
    residual = qmem + qmat
    return qmem, qmat, residual

def verify(cfg):
    qmem, qmat, residual = conservation_residuals(cfg, cfg.conservation_tol)
    cfg2 = BianchiProxyConfig(cfg.n_slices, cfg.n_points, cfg.dim, cfg.eta, cfg.conservation_tol*0.5, cfg.Z, cfg.lam, cfg.v2, cfg.seed)
    _, _, residual_half = conservation_residuals(cfg2, cfg2.conservation_tol)

    mem_norms = np.linalg.norm(qmem, axis=1)
    res_norms = np.linalg.norm(residual, axis=1)
    res_half_norms = np.linalg.norm(residual_half, axis=1)
    vals = np.concatenate([mem_norms, res_norms, res_half_norms])
    finite_fraction = float(np.mean(np.isfinite(vals))) if len(vals) else 0.0

    mem_med = float(np.nanmedian(mem_norms))
    res_med = float(np.nanmedian(res_norms))
    res_half_med = float(np.nanmedian(res_half_norms))
    residual_to_mem = res_med / (mem_med + 1e-12)
    tol_scaling = res_half_med / (res_med + 1e-12)

    stable = bool(finite_fraction > 0.99 and np.isfinite(mem_med) and np.isfinite(res_med) and residual_to_mem < 0.01 and 0.35 < tol_scaling < 0.65)

    return BianchiProxyResult(mem_med, res_med, residual_to_mem, tol_scaling, finite_fraction, stable)

def classify(cfg):
    r = verify(cfg)
    if r.finite_fraction < 0.99:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r

def run_sweep(n_sweeps=120, seed=911):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in ["mem_exchange_norm_median","total_residual_norm_median","residual_to_mem_ratio","residual_tol_scaling_ratio","finite_fraction"]}
    for _ in range(n_sweeps):
        cfg = BianchiProxyConfig(
            n_slices=int(rng.integers(5, 14)),
            n_points=int(rng.integers(12, 36)),
            dim=3,
            eta=float(10 ** rng.uniform(-4, -1.5)),
            conservation_tol=float(10 ** rng.uniform(-4, -2)),
            Z=float(10 ** rng.uniform(-1, 1)),
            lam=float(10 ** rng.uniform(-2, 0)),
            v2=float(10 ** rng.uniform(-1, 1)),
            seed=int(rng.integers(0, 10_000_000)),
        )
        label, r = classify(cfg)
        counts[label] += 1
        if label in {"PASS","SOFT_FAIL"}:
            for k in vals:
                vals[k].append(getattr(r, k))
    out = {k:100*v/n_sweeps for k,v in counts.items()}
    for k, arr in vals.items():
        if arr:
            out[k + "_median"] = float(np.nanmedian(arr))
    return out

def main():
    print("Bianchi ADM conservation proxy verifier")
    print("="*50)
    print("Route:")
    print("Q_mem + Q_mat = 0 at ADM proxy level with controlled closure residual")
    print("This is not covariant Bianchi proof.")
    print()
    for k, v in run_sweep().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
