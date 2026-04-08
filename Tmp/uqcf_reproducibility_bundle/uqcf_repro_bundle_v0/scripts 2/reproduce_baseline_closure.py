#!/usr/bin/env python3
"""
Reproduce the baseline selector convergence result for the UQCF-GEM bridge.
Expected qualitative outcome:
- convergence to a single attractor near gamma ~ 0.273, W ~ 0.431, chi ~ 0.401
"""
import json, math
from pathlib import Path
import numpy as np
import pandas as pd

gamma_star_target = 0.26671093
chi_star_target   = 0.40117290
W_star_target     = 0.43062200
d_eff = 3.9
mu = 2.98
sig_w = 0.605
Q0 = 0.15

s = np.logspace(0, 4, 900)
ds = np.gradient(s)
ell2 = np.log2(s)
taus = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0], dtype=float)
w_shape = np.exp(-0.5 * ((ell2 - mu) / sig_w) ** 2)

def sigma_from_retained_diffusion(p, x_diff):
    lam = np.power(np.maximum(ell2, 1e-8), x_diff)
    expo = np.exp(-np.outer(taus, lam))
    P = expo @ (p * ds)
    valid = P > 1e-14
    x = np.log(taus[valid]); y = np.log(P[valid])
    slope, _ = np.polyfit(x, y, 1)
    D_spec = float(np.clip(-2.0 * slope, 0.0, 4.0))
    sigma = float(np.clip(0.58 + 0.22 * (D_spec / 4.0), 0.55, 0.80))
    return sigma

def W_from_chi(chi):
    m = 1.0 + chi
    C = np.power(s, -m)
    norm = np.sum(C * ds)
    p = C / norm
    shape_weight = float(np.sum(w_shape * p * ds))
    Q_shape = float(norm) * shape_weight
    eta = Q_shape / (Q0 + Q_shape)
    W = eta / (1.0 + eta)
    return W, p

def sigma_from_state(gamma, chi):
    W, p = W_from_chi(chi)
    x_diff = chi - (gamma / d_eff) / (d_eff - 0.8)
    sigma = sigma_from_retained_diffusion(p, x_diff)
    return sigma

def iterate_flow(gamma0, W0, chi0, ag=0.60, aW=0.45, ac=0.65, n_steps=120):
    gamma = float(gamma0); W = float(W0); chi = float(chi0)
    for _ in range(n_steps):
        chi_target = (1.0 - gamma / d_eff) * W
        W_target, _ = W_from_chi(chi)
        sigma = sigma_from_state(gamma, chi)
        gamma_target = 1.0 - sigma
        chi = chi + ac * (chi_target - chi)
        W = W + aW * (W_target - W)
        gamma = gamma + ag * (gamma_target - gamma)
    err = math.sqrt((gamma-gamma_star_target)**2 + (chi-chi_star_target)**2 + (W-W_star_target)**2)
    return {"gamma_final": gamma, "W_final": W, "chi_final": chi, "error_final": err}

def main():
    gammas0 = [0.10, 0.18, 0.27, 0.36, 0.50]
    Ws0     = [0.25, 0.35, 0.43, 0.55, 0.65]
    chis0   = [0.20, 0.30, 0.40, 0.50, 0.60]
    rows = [iterate_flow(g0, W0, chi0) for g0 in gammas0 for W0 in Ws0 for chi0 in chis0]
    df = pd.DataFrame(rows)
    out = Path(__file__).resolve().parents[1] / "reproduced" / "baseline_closure"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "baseline_flow_runs.csv", index=False)
    summary = {
        "mean_gamma_final": float(df["gamma_final"].mean()),
        "mean_W_final": float(df["W_final"].mean()),
        "mean_chi_final": float(df["chi_final"].mean()),
        "mean_error_final": float(df["error_final"].mean()),
    }
    (out / "baseline_flow_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
