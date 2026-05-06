
"""
chi_selection_principle_verifier.py

Verifier for CHI_SELECTION_PRINCIPLE.md.

Goal:
Test candidate selection principles that could prefer chi* ≈ 0.2667
(Lambda* ≈ 2.75) over the broad-sampling median chi ≈ 0.85.

Candidate principle:
Select Lambda by minimizing a balance functional combining:
    1. memory-loading mismatch / insufficient retained memory
    2. geometry-overloading / excessive memory domination
    3. coefficient coherence strength through chi(1-chi)
    4. target weak-memory compatibility

Minimal balance functional:
    F(Lambda; q, s) =
        A / Lambda
      + B * Lambda
      + C / [chi(1-chi) + eps]
      + S * (Lambda - q)^2

where:
    chi = 1/(1+Lambda)

This is not final physics.
It tests whether a simple variational balance can naturally select Lambda ≈ 2.75.

Checks:
    - optimum finite
    - optimum near target across a non-tiny parameter region
    - chi near 0.2667 possible without directly forcing b
"""

from __future__ import annotations

import numpy as np


def chi_from_L(L):
    return 1.0/(1.0+L)


def functional(L, A, B, C, S, q):
    chi = chi_from_L(L)
    return A/(L+1e-12) + B*L + C/(chi*(1-chi)+1e-12) + S*(L-q)**2


def find_min(A, B, C, S, q):
    # log grid for robustness
    Ls = np.logspace(-3, 3, 2000)
    F = functional(Ls, A, B, C, S, q)
    idx = int(np.argmin(F))
    return float(Ls[idx]), float(chi_from_L(Ls[idx])), float(F[idx])


def run_sweep(n_sweeps=100000, seed=2003, chi_target=0.2667, tol=0.02):
    rng = np.random.default_rng(seed)
    Lambda_target = (1-chi_target)/chi_target
    hits = []
    vals = []
    for _ in range(n_sweeps):
        # Candidate principle parameters; q is preferred loading from micro balance.
        A = 10**rng.uniform(-1, 1)       # penalty for too little memory
        B = 10**rng.uniform(-1, 1)       # penalty for too much memory
        C = 10**rng.uniform(-3, -0.2)    # coherence-coupling regularizer
        S = 10**rng.uniform(-2, 1)       # micro-balance anchoring
        q = 10**rng.uniform(-1, 1)       # natural loading balance scale

        Lopt, chi, fmin = find_min(A,B,C,S,q)
        if np.isfinite(Lopt) and np.isfinite(chi):
            rec = (Lopt, chi, A, B, C, S, q)
            vals.append(rec)
            if abs(chi-chi_target) <= tol:
                hits.append(rec)

    arr = np.asarray(vals)
    harr = np.asarray(hits) if hits else np.empty((0,7))
    hit_rate = 100*len(hits)/max(len(vals),1)

    out = {
        "valid_samples": len(vals),
        "target_hits": len(hits),
        "hit_rate_percent": hit_rate,
        "naturalness_class": "SELECTION_PLAUSIBLE" if hit_rate >= 5 else ("RARE_SELECTION" if len(hits)>0 else "NOT_FOUND"),
    }
    names = ["Lambda_opt","chi_opt","A","B","C","S","q"]
    if len(vals):
        for i,n in enumerate(names):
            out[n+"_median_all"] = float(np.median(arr[:,i]))
    if len(hits):
        for i,n in enumerate(names):
            out[n+"_median_hits"] = float(np.median(harr[:,i]))
            out[n+"_p10_hits"] = float(np.percentile(harr[:,i],10))
            out[n+"_p90_hits"] = float(np.percentile(harr[:,i],90))
    out["Lambda_target"] = Lambda_target
    return out


def main():
    print("Chi selection principle verifier")
    print("="*50)
    print("Route:")
    print("candidate balance functional -> selected Lambda* and chi*")
    print("This tests plausibility of a selection principle, not final derivation.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
