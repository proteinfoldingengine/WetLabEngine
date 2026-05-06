
"""
chi_target_parameter_regime_verifier.py

Verifier for CHI_TARGET_PARAMETER_REGIME.md.

Goal:
Find and characterize micro-to-block parameter regimes that produce:

    chi_target ≈ 0.2667

Given:
    chi* = 1/(1+Lambda*)
    Lambda* = b/(1-a)

Target:
    Lambda_target = (1-chi_target)/chi_target ≈ 2.7495

Loading map:
    a = (w_s alpha_s c_s + w_f alpha_f c_f)/mu_G
    b = (w_s beta_s I_s + w_f beta_f I_f)/(mu_G G_star)

Requirement:
    b = Lambda_target(1-a)

Checks:
    - target reachability
    - parameter positivity
    - 0 <= a < 1
    - b > 0
    - chi close to target
    - coefficient admissibility
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TargetConfig:
    chi_target: float = 0.2667
    tol: float = 5e-3
    seed: int = 1709


@dataclass(frozen=True)
class TargetResult:
    hit_rate: float
    chi_median: float
    lambda_median: float
    a_median: float
    b_median: float
    gstar_median: float
    beta_scale_median: float
    Z_R_median: float
    m_R2_median: float
    lambda_int_median: float
    finite_fraction: float
    stable: bool


def compute(ws, alpha_s, alpha_f, cs, cf, beta_s, beta_f, Is, If, mu_G, G_star, sigma_grad, rho_mat, dx_dt):
    wf = 1-ws
    a = (ws*alpha_s*cs + wf*alpha_f*cf)/mu_G
    b = (ws*beta_s*Is + wf*beta_f*If)/(mu_G*G_star)
    Lambda = b/(1-a) if abs(1-a) > 1e-12 else np.nan
    chi = 1/(1+Lambda) if np.isfinite(Lambda) else np.nan
    K_t = 1 + ws*alpha_s + wf*alpha_f
    K_U = K_t*(1-a)
    K_x = K_t*chi*(1-chi)*sigma_grad**2 if np.isfinite(chi) else np.nan
    K_int = K_t*chi*(1-chi)*rho_mat if np.isfinite(chi) else np.nan
    Z_R = (K_x/K_t)*dx_dt**2 if K_t != 0 and np.isfinite(K_x) else np.nan
    m_R2 = K_U/K_t if K_t != 0 else np.nan
    lam_int = K_int/K_t if K_t != 0 and np.isfinite(K_int) else np.nan
    return a,b,Lambda,chi,G_star,Z_R,m_R2,lam_int


def targeted_sample(rng, chi_target):
    Lambda_target = (1-chi_target)/chi_target

    ws = rng.uniform(0.05, 0.95)
    wf = 1 - ws
    alpha_s = rng.uniform(0.05, 0.98)
    alpha_f = rng.uniform(0.05, 0.98)
    cs = rng.uniform(0.05, 1.0)
    cf = rng.uniform(0.05, 1.0)
    mu_G = rng.uniform(0.8, 4.0)

    # Compute a first, reject if not stable.
    a = (ws*alpha_s*cs + wf*alpha_f*cf)/mu_G
    if not (0 <= a < 0.98):
        return None

    Is = 10**rng.uniform(-2, 1.0)
    If = 10**rng.uniform(-2, 1.0)

    # Choose a positive G_star and solve for beta scale to hit b target.
    G_star = 10**rng.uniform(-2, 1.0)
    target_b = Lambda_target*(1-a)
    mix = ws*Is + wf*If
    beta_scale = target_b * mu_G * G_star / (mix + 1e-12)

    # Allow slow/fast beta asymmetry while preserving approximate mixture.
    asym = rng.uniform(0.5, 2.0)
    beta_s = beta_scale * asym
    # solve beta_f roughly for mixture target
    beta_f = (target_b*mu_G*G_star - ws*beta_s*Is)/(wf*If + 1e-12)
    if beta_f <= 0:
        beta_f = beta_scale / asym

    sigma_grad = 10**rng.uniform(-3, 0.5)
    rho_mat = 10**rng.uniform(-3, 0.5)
    dx_dt = 10**rng.uniform(-1, 1)

    return ws, alpha_s, alpha_f, cs, cf, beta_s, beta_f, Is, If, mu_G, G_star, sigma_grad, rho_mat, dx_dt, beta_scale


def run_sweep(n_sweeps=50000, seed=1709, chi_target=0.2667, tol=5e-3):
    rng = np.random.default_rng(seed)
    hits = []
    all_valid = []

    for _ in range(n_sweeps):
        sample = targeted_sample(rng, chi_target)
        if sample is None:
            continue
        *params, beta_scale = sample
        a,b,Lambda,chi,G_star,Z_R,m_R2,lam_int = compute(*params)
        vals = np.array([a,b,Lambda,chi,G_star,Z_R,m_R2,lam_int])
        finite = np.all(np.isfinite(vals))
        stable = finite and 0 <= a < 1 and b > 0 and 0 < chi < 1 and m_R2 > 0 and Z_R >= 0 and lam_int >= 0
        if stable:
            all_valid.append((a,b,Lambda,chi,G_star,beta_scale,Z_R,m_R2,lam_int))
            if abs(chi-chi_target) <= tol:
                hits.append((a,b,Lambda,chi,G_star,beta_scale,Z_R,m_R2,lam_int))

    arr = np.asarray(hits if hits else all_valid, dtype=float)
    finite_fraction = float(np.mean(np.isfinite(arr))) if arr.size else 0.0
    hit_rate = len(hits)/max(len(all_valid),1)*100

    out = {
        "valid_samples": len(all_valid),
        "target_hits": len(hits),
        "hit_rate": hit_rate,
        "finite_fraction": finite_fraction,
    }
    if arr.size:
        names = ["a","b","Lambda","chi","G_star","beta_scale","Z_R","m_R2","lambda_int"]
        for i,n in enumerate(names):
            out[n+"_median"] = float(np.nanmedian(arr[:,i]))
            out[n+"_p10"] = float(np.nanpercentile(arr[:,i],10))
            out[n+"_p90"] = float(np.nanpercentile(arr[:,i],90))

    out["stable"] = bool(len(hits) > 0 and hit_rate > 80 and finite_fraction == 1.0)
    return out


def main():
    print("Chi target parameter regime verifier")
    print("="*50)
    print("Route:")
    print("chi_target -> Lambda_target -> constraints on a,b and micro-to-block parameters")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
