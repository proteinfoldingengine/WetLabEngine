
"""
chi_selection_from_block_action_verifier.py

Verifier for CHI_SELECTION_FROM_BLOCK_ACTION.md.

Goal:
Test whether a chi-selection functional can be constructed from the block action constants:

    K_U = K_t(1-a)
    K_x = K_t chi(1-chi) sigma_grad^2
    K_int = K_t chi(1-chi) rho_mat

Candidate block-derived selection energy:
    F_block(Lambda) =
        U_load(Lambda) + U_geom(Lambda) + U_resp(Lambda) + U_anchor(Lambda)

with:
    chi = 1/(1+Lambda)
    U_load  = A_block / Lambda
    U_geom  = B_block Lambda
    U_resp  = C_block / (chi(1-chi))
    U_anchor = S_block (Lambda - q_block)^2

Now derive coefficients from block objects:
    A_block ~ K_U + K_int
    B_block ~ K_U
    C_block ~ K_x + K_int
    q_block ~ b/(1-a) = Lambda_star_micro
    S_block ~ K_U/(1 + K_x + K_int)

This is not unique. It tests whether block-derived coefficients plausibly select target chi.
"""

from __future__ import annotations

import numpy as np


def chi_from_L(L):
    return 1/(1+L)


def find_min(A,B,C,S,q):
    Ls = np.logspace(-3, 3, 2000)
    chi = chi_from_L(Ls)
    F = A/(Ls+1e-12) + B*Ls + C/(chi*(1-chi)+1e-12) + S*(Ls-q)**2
    idx = int(np.argmin(F))
    return float(Ls[idx]), float(chi[idx])


def block_values(rng):
    # sample micro-to-block params, including target-ish and broad regimes
    ws = rng.uniform(0.05, 0.95)
    wf = 1-ws
    alpha_s = rng.uniform(0.0, 0.99)
    alpha_f = rng.uniform(0.0, 0.99)
    c_s = rng.uniform(0.05, 1.0)
    c_f = rng.uniform(0.05, 1.0)
    mu_G = 10**rng.uniform(-0.2, 0.8)

    a = (ws*alpha_s*c_s + wf*alpha_f*c_f)/mu_G
    if not (0 <= a < 1):
        return None

    # sample loading fixed point q directly across broad but physical range
    # This represents the micro-to-block fixed point b/(1-a).
    q = 10**rng.uniform(-1, 1)

    b = q*(1-a)
    chi_micro = 1/(1+q)

    K_t = 1 + ws*alpha_s + wf*alpha_f
    K_U = K_t*(1-a)

    sigma_grad = 10**rng.uniform(-3, 0.5)
    rho_mat = 10**rng.uniform(-3, 0.5)

    K_x = K_t*chi_micro*(1-chi_micro)*sigma_grad**2
    K_int = K_t*chi_micro*(1-chi_micro)*rho_mat

    # block-derived selection coefficients
    A = K_U + K_int
    B = K_U
    C = K_x + K_int
    S = K_U/(1 + K_x + K_int)

    return a,b,q,chi_micro,K_t,K_U,K_x,K_int,A,B,C,S


def run_sweep(n_sweeps=100000, seed=2113, chi_target=0.2667, tol=0.02):
    rng = np.random.default_rng(seed)
    vals = []
    hits = []
    for _ in range(n_sweeps):
        bv = block_values(rng)
        if bv is None:
            continue
        a,b,q,chi_micro,K_t,K_U,K_x,K_int,A,B,C,S = bv
        Lopt, chi_opt = find_min(A,B,C,S,q)
        rec = (Lopt, chi_opt, q, chi_micro, a,b,K_U,K_x,K_int,A,B,C,S)
        if np.all(np.isfinite(rec)):
            vals.append(rec)
            if abs(chi_opt-chi_target) <= tol:
                hits.append(rec)

    arr = np.asarray(vals)
    harr = np.asarray(hits) if hits else np.empty((0,13))
    hit_rate = 100*len(hits)/max(len(vals),1)

    names = ["Lambda_opt","chi_opt","q_block","chi_micro","a","b","K_U","K_x","K_int","A","B","C","S"]
    out = {
        "valid_samples": len(vals),
        "target_hits": len(hits),
        "hit_rate_percent": hit_rate,
        "selection_class": "BLOCK_SELECTION_PLAUSIBLE" if hit_rate >= 5 else ("RARE_BLOCK_SELECTION" if hits else "NOT_FOUND")
    }
    if len(vals):
        for i,n in enumerate(names):
            out[n+"_median_all"] = float(np.median(arr[:,i]))
    if len(hits):
        for i,n in enumerate(names):
            out[n+"_median_hits"] = float(np.median(harr[:,i]))
            out[n+"_p10_hits"] = float(np.percentile(harr[:,i],10))
            out[n+"_p90_hits"] = float(np.percentile(harr[:,i],90))
    return out


def main():
    print("Chi selection from block action verifier")
    print("="*50)
    print("Route:")
    print("block constants -> selection coefficients -> Lambda optimum")
    print("Tests block-derived plausibility, not unique derivation.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
