
"""
coefficient_closure_from_micro_to_block_verifier.py

Verifier for COEFFICIENT_CLOSURE_FROM_MICRO_TO_BLOCK.md.

Uses the concrete slow/fast retained-memory recursion from MICRO_TO_BLOCK_ACTION.md:

    R_s[t+1] = alpha_s R_s[t] + beta_s |xi_t|
    R_f[t+1] = alpha_f R_f[t] + beta_f |xi_t| Theta(|xi_t|-eps*)
    M_t = w_s R_s[t] + w_f R_f[t]
    G[n+1] = mu_G G[n]
    Lambda[n+1] = a Lambda[n] + b

Then maps block constants to continuum coefficients.
"""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class MicroBlockParams:
    alpha_s: float
    alpha_f: float
    beta_s: float
    beta_f: float
    w_s: float
    w_f: float
    c_s: float
    c_f: float
    mu_G: float
    I_s: float
    I_f: float
    G_star: float
    sigma_grad: float
    rho_mat: float
    dx_dt: float
    eps_star: float


@dataclass(frozen=True)
class ClosureResult:
    a: float
    b: float
    Lambda_star: float
    chi_star: float
    K_t: float
    K_U: float
    K_x: float
    K_int: float
    Z_R: float
    m_R2: float
    V_quad: float
    lambda_int: float
    finite_fraction: float
    stable: bool


def compute(p: MicroBlockParams):
    try:
        a = (p.w_s*p.alpha_s*p.c_s + p.w_f*p.alpha_f*p.c_f) / p.mu_G
        b = (p.w_s*p.beta_s*p.I_s + p.w_f*p.beta_f*p.I_f) / (p.mu_G*p.G_star)

        Lambda_star = b/(1-a) if abs(1-a) > 1e-12 else np.nan
        chi_star = 1/(1+Lambda_star) if np.isfinite(Lambda_star) else np.nan

        K_t = 1 + p.w_s*p.alpha_s + p.w_f*p.alpha_f
        K_U = K_t*(1-a)
        K_x = K_t*chi_star*(1-chi_star)*(p.sigma_grad**2) if np.isfinite(chi_star) else np.nan
        K_int = K_t*chi_star*(1-chi_star)*p.rho_mat if np.isfinite(chi_star) else np.nan

        Z_R = (K_x/K_t)*(p.dx_dt**2) if K_t != 0 and np.isfinite(K_x) else np.nan
        m_R2 = K_U/K_t if K_t != 0 else np.nan
        V_quad = 0.5*m_R2 if np.isfinite(m_R2) else np.nan
        lambda_int = K_int/K_t if K_t != 0 and np.isfinite(K_int) else np.nan
    except Exception:
        a = b = Lambda_star = chi_star = K_t = K_U = K_x = K_int = Z_R = m_R2 = V_quad = lambda_int = np.nan

    vals = np.array([a,b,Lambda_star,chi_star,K_t,K_U,K_x,K_int,Z_R,m_R2,V_quad,lambda_int], dtype=float)
    finite_fraction = float(np.mean(np.isfinite(vals)))

    stable = bool(
        finite_fraction == 1.0
        and 0 <= a < 1
        and b > 0
        and Lambda_star > 0
        and 0 < chi_star < 1
        and K_t > 0
        and K_U > 0
        and K_x >= 0
        and K_int >= 0
        and Z_R >= 0
        and m_R2 > 0
        and lambda_int >= 0
    )

    return ClosureResult(a,b,Lambda_star,chi_star,K_t,K_U,K_x,K_int,Z_R,m_R2,V_quad,lambda_int,finite_fraction,stable)


def classify(p):
    r = compute(p)
    if r.finite_fraction < 1.0:
        return "HARD_FAIL", r
    if not r.stable:
        return "SOFT_FAIL", r
    return "PASS", r


def run_sweep(n_sweeps=100000, seed=1613):
    rng = np.random.default_rng(seed)
    counts = {"PASS":0, "SOFT_FAIL":0, "HARD_FAIL":0}
    vals = {k: [] for k in [
        "a","b","Lambda_star","chi_star","K_t","K_U","K_x","K_int","Z_R","m_R2","V_quad","lambda_int","finite_fraction"
    ]}

    for _ in range(n_sweeps):
        ws = rng.uniform(0.05, 0.95)
        wf = 1-ws
        p = MicroBlockParams(
            alpha_s=float(rng.uniform(0.0, 0.99)),
            alpha_f=float(rng.uniform(0.0, 0.99)),
            beta_s=float(10**rng.uniform(-3, 0.5)),
            beta_f=float(10**rng.uniform(-3, 0.5)),
            w_s=float(ws),
            w_f=float(wf),
            c_s=float(rng.uniform(0.05, 1.0)),
            c_f=float(rng.uniform(0.05, 1.0)),
            mu_G=float(10**rng.uniform(-0.2, 0.8)),
            I_s=float(10**rng.uniform(-3, 0.5)),
            I_f=float(10**rng.uniform(-3, 0.5)),
            G_star=float(10**rng.uniform(-1, 1)),
            sigma_grad=float(10**rng.uniform(-3, 0.5)),
            rho_mat=float(10**rng.uniform(-3, 0.5)),
            dx_dt=float(10**rng.uniform(-1, 1)),
            eps_star=float(10**rng.uniform(-4, -0.3)),
        )

        roll = rng.random()
        if roll < 0.01:
            p = MicroBlockParams(**{**p.__dict__, "mu_G": -abs(p.mu_G)})
        elif roll < 0.02:
            p = MicroBlockParams(**{**p.__dict__, "G_star": 0.0})
        elif roll < 0.04:
            p = MicroBlockParams(**{**p.__dict__, "mu_G": 0.01})

        label, r = classify(p)
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
    print("Coefficient closure from micro-to-block verifier")
    print("="*50)
    print("Route:")
    print("slow/fast retained-memory recursion -> loading map -> block constants -> continuum coefficients")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
