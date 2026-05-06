
"""
chi_naturalness_from_pruning_verifier.py

Verifier for CHI_NATURALNESS_FROM_PRUNING.md.

Goal:
Use explicit Gaussian pruning integrals to test whether chi* ≈ 0.2667
appears naturally across broad micro-to-block parameter regimes.

No targeted solving for b.
Instead sample:
    alpha_s, alpha_f, beta_s, beta_f, weights, c_s,c_f, mu_G, G_star,
    sigma_xi, eps_star/sigma_xi

Compute:
    I_s = sqrt(2/pi) sigma_xi
    I_f = I_s exp(-eps_star^2/(2 sigma_xi^2))
    a = (w_s alpha_s c_s + w_f alpha_f c_f)/mu_G
    b = (w_s beta_s I_s + w_f beta_f I_f)/(mu_G G_star)
    Lambda* = b/(1-a)
    chi* = 1/(1+Lambda*)

Naturalness metrics:
    hit rate near chi target
    log-distance to target Lambda
    regime distributions for hits
"""

from __future__ import annotations

import numpy as np
from math import sqrt, pi, exp


def integrals(sigma, eps):
    I_s = sigma * sqrt(2.0/pi)
    I_f = I_s * exp(-(eps**2)/(2*sigma**2))
    return I_s, I_f


def sample_once(rng):
    ws = rng.uniform(0.05, 0.95)
    wf = 1-ws
    alpha_s = rng.uniform(0.0, 0.99)
    alpha_f = rng.uniform(0.0, 0.99)
    c_s = rng.uniform(0.05, 1.0)
    c_f = rng.uniform(0.05, 1.0)
    mu_G = 10**rng.uniform(-0.2, 0.8)

    beta_s = 10**rng.uniform(-3, 1.0)
    beta_f = 10**rng.uniform(-3, 1.0)
    G_star = 10**rng.uniform(-2, 1.0)

    sigma = 10**rng.uniform(-1, 1.0)
    r = rng.uniform(0.0, 4.0)  # eps/sigma
    eps = r*sigma
    I_s, I_f = integrals(sigma, eps)

    a = (ws*alpha_s*c_s + wf*alpha_f*c_f)/mu_G
    if not (0 <= a < 1):
        return None

    b = (ws*beta_s*I_s + wf*beta_f*I_f)/(mu_G*G_star)
    if b <= 0:
        return None

    Lambda = b/(1-a)
    chi = 1/(1+Lambda)

    return {
        "chi": chi, "Lambda": Lambda, "a": a, "b": b,
        "ws": ws, "beta_s": beta_s, "beta_f": beta_f,
        "G_star": G_star, "sigma": sigma, "eps_over_sigma": r,
        "I_f_over_I_s": I_f/I_s, "mu_G": mu_G
    }


def run_sweep(n_sweeps=250000, seed=1901, chi_target=0.2667, tol=0.01):
    rng = np.random.default_rng(seed)
    valid = []
    hits = []
    Lambda_target = (1-chi_target)/chi_target

    for _ in range(n_sweeps):
        s = sample_once(rng)
        if s is None:
            continue
        valid.append(s)
        if abs(s["chi"] - chi_target) <= tol:
            hits.append(s)

    def med(key, arr):
        return float(np.median([x[key] for x in arr])) if arr else float("nan")
    def pctl(key, arr, p):
        return float(np.percentile([x[key] for x in arr], p)) if arr else float("nan")

    chi_vals = np.array([x["chi"] for x in valid])
    lam_vals = np.array([x["Lambda"] for x in valid])
    logdist = np.abs(np.log((lam_vals+1e-30)/Lambda_target))

    out = {
        "valid_samples": len(valid),
        "target_hits": len(hits),
        "hit_rate_percent": 100*len(hits)/max(len(valid),1),
        "chi_median_all": med("chi", valid),
        "chi_p10_all": pctl("chi", valid, 10),
        "chi_p90_all": pctl("chi", valid, 90),
        "Lambda_median_all": med("Lambda", valid),
        "logLambda_distance_median": float(np.median(logdist)) if len(logdist) else float("nan"),
        "hit_a_median": med("a", hits),
        "hit_b_median": med("b", hits),
        "hit_G_star_median": med("G_star", hits),
        "hit_beta_s_median": med("beta_s", hits),
        "hit_beta_f_median": med("beta_f", hits),
        "hit_eps_over_sigma_median": med("eps_over_sigma", hits),
        "hit_I_f_over_I_s_median": med("I_f_over_I_s", hits),
        "hit_sigma_median": med("sigma", hits),
        "naturalness_class": "NATURAL" if 100*len(hits)/max(len(valid),1) >= 5 else ("RARE_BUT_REACHABLE" if len(hits)>0 else "NOT_FOUND")
    }
    return out


def main():
    print("Chi naturalness from pruning verifier")
    print("="*50)
    print("Route:")
    print("broad pruning/noise sampling with explicit I_s,I_f -> chi* distribution")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
