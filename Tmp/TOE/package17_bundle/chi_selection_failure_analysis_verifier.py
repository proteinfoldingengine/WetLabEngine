
"""
chi_selection_failure_analysis_verifier.py

Verifier for CHI_SELECTION_FAILURE_ANALYSIS.md.

Goal:
Analyze why block-derived chi selection usually lands near chi≈0.49
instead of target chi≈0.2667.

From prior verifier:
    q_block_median_all ≈ 1.0069 -> chi_micro≈0.498
    Lambda_opt_median_all ≈ 1.0387 -> chi_opt≈0.4905

Hypothesis:
The block-derived functional contains an anchor term S(Lambda-q_block)^2.
If q_block is broadly centered near 1, optimum will also be near 1.
Target Lambda≈2.75 requires q_block and/or memory insufficiency pressure A/B
to shift upward.

This verifier:
    - samples block-derived coefficients
    - computes correlations between Lambda_opt and q_block, A/B, C, S
    - compares all-sample vs target-hit regimes
    - quantifies how much q_block needs to shift
"""

from __future__ import annotations
import numpy as np


def chi_from_L(L): return 1/(1+L)

def find_min(A,B,C,S,q):
    Ls = np.logspace(-3, 3, 2500)
    chi = chi_from_L(Ls)
    F = A/(Ls+1e-12)+B*Ls+C/(chi*(1-chi)+1e-12)+S*(Ls-q)**2
    i = int(np.argmin(F))
    return float(Ls[i]), float(chi[i])

def sample_block(rng):
    ws = rng.uniform(0.05, 0.95); wf=1-ws
    alpha_s = rng.uniform(0, .99); alpha_f=rng.uniform(0,.99)
    c_s=rng.uniform(.05,1); c_f=rng.uniform(.05,1)
    mu_G=10**rng.uniform(-.2,.8)
    a=(ws*alpha_s*c_s+wf*alpha_f*c_f)/mu_G
    if not (0<=a<1): return None
    q=10**rng.uniform(-1,1)
    b=q*(1-a)
    chi_micro=chi_from_L(q)
    K_t=1+ws*alpha_s+wf*alpha_f
    K_U=K_t*(1-a)
    sigma_grad=10**rng.uniform(-3,.5)
    rho_mat=10**rng.uniform(-3,.5)
    K_x=K_t*chi_micro*(1-chi_micro)*sigma_grad**2
    K_int=K_t*chi_micro*(1-chi_micro)*rho_mat
    A=K_U+K_int; B=K_U; C=K_x+K_int; S=K_U/(1+K_x+K_int)
    Lopt, chiopt = find_min(A,B,C,S,q)
    return dict(Lopt=Lopt, chiopt=chiopt, q=q, chi_micro=chi_micro, a=a, b=b,
                K_U=K_U, K_x=K_x, K_int=K_int, A=A, B=B, C=C, S=S, A_over_B=A/(B+1e-12))

def corr(x,y):
    x=np.asarray(x); y=np.asarray(y)
    if len(x)<3 or np.std(x)==0 or np.std(y)==0: return np.nan
    return float(np.corrcoef(x,y)[0,1])

def run_analysis(n=120000, seed=2203, chi_target=.2667, tol=.02):
    rng=np.random.default_rng(seed)
    rows=[]
    for _ in range(n):
        r=sample_block(rng)
        if r is not None and np.all(np.isfinite(list(r.values()))):
            rows.append(r)
    hits=[r for r in rows if abs(r["chiopt"]-chi_target)<=tol]
    target_L=(1-chi_target)/chi_target
    keys=["Lopt","chiopt","q","A_over_B","C","S","K_int","K_x","b","a"]
    out={
        "valid_samples": len(rows),
        "target_hits": len(hits),
        "hit_rate_percent": 100*len(hits)/max(len(rows),1),
        "target_Lambda": target_L,
    }
    for k in keys:
        vals=[r[k] for r in rows]
        hvals=[r[k] for r in hits]
        out[k+"_median_all"]=float(np.median(vals)) if vals else np.nan
        out[k+"_median_hits"]=float(np.median(hvals)) if hvals else np.nan
    out["corr_Lopt_q"]=corr([r["Lopt"] for r in rows],[r["q"] for r in rows])
    out["corr_Lopt_A_over_B"]=corr([r["Lopt"] for r in rows],[r["A_over_B"] for r in rows])
    out["corr_Lopt_C"]=corr([r["Lopt"] for r in rows],[r["C"] for r in rows])
    out["corr_Lopt_S"]=corr([r["Lopt"] for r in rows],[r["S"] for r in rows])
    out["q_shift_factor_hits_vs_all"]=out["q_median_hits"]/out["q_median_all"]
    out["failure_mode"]="ANCHOR_CENTERED_NEAR_LAMBDA_1" if out["q_median_all"] < 1.5 and out["corr_Lopt_q"] > .5 else "MIXED"
    return out

def main():
    print("Chi selection failure analysis verifier")
    print("="*50)
    print("Route:")
    print("block-derived selection distribution -> failure mode diagnostics")
    print()
    for k,v in run_analysis().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
