
from __future__ import annotations
import numpy as np
from math import sqrt, pi, exp

def integrals(sigma, r):
    Is = sigma * sqrt(2/pi)
    If = Is * exp(-(r**2)/2)
    return Is, If

def sample_block(rng):
    ws = rng.uniform(0.05, 0.95); wf=1-ws
    alpha_s=rng.uniform(0,.99); alpha_f=rng.uniform(0,.99)
    c_s=rng.uniform(.05,1); c_f=rng.uniform(.05,1)
    mu_G=10**rng.uniform(-.2,.8)
    sigma=10**rng.uniform(-1,1)
    r=rng.uniform(0,4)
    Is, If = integrals(sigma, r)
    beta_s=10**rng.uniform(-3,1)
    beta_f=10**rng.uniform(-3,1)
    G_star=10**rng.uniform(-2,1)

    a=(ws*alpha_s*c_s+wf*alpha_f*c_f)/mu_G
    if not (0<=a<1): return None
    b=(ws*beta_s*Is+wf*beta_f*If)/(mu_G*G_star)
    if b<=0: return None
    q=b/(1-a)
    chi=1/(1+q)
    K_t=1+ws*alpha_s+wf*alpha_f
    K_U=K_t*(1-a)
    sigma_grad=10**rng.uniform(-3,.5)
    rho_mat=10**rng.uniform(-3,.5)
    K_x=K_t*chi*(1-chi)*sigma_grad**2
    K_int=K_t*chi*(1-chi)*rho_mat

    # Candidate derived asymmetry ratio from block terms:
    # underload penalty = restoring + interaction need + coherence deficit
    # overload penalty = restoring + geometry-normalized coherence pressure
    A = K_U + K_int + K_x
    B = K_U
    A_over_B = A/(B+1e-12)

    # Candidate internal critical loading scale from block fixed point and response factor
    q0 = q * (1 + K_int/(K_U+1e-12)) / (1 + K_x/(K_U+1e-12))

    return dict(q=q, chi=chi, a=a, b=b, K_U=K_U, K_x=K_x, K_int=K_int,
                A=A, B=B, A_over_B=A_over_B, q0=q0, sigma=sigma,
                eps_over_sigma=r, If_over_Is=If/Is, beta_s=beta_s, beta_f=beta_f,
                G_star=G_star)

def summarize(rows):
    if not rows: return {}
    hits=[x for x in rows if 7.5<=x["A_over_B"]<=9.5 and 2.75<=x["q0"]<=3.3]
    qhits=[x for x in rows if 2.75<=x["q"]<=3.3]
    def med(k, arr=rows):
        return float(np.median([x[k] for x in arr])) if arr else float("nan")
    def pct(k,p,arr=rows):
        return float(np.percentile([x[k] for x in arr],p)) if arr else float("nan")
    out={
        "valid_samples":len(rows),
        "joint_AoverB_q0_hits":len(hits),
        "joint_hit_rate_percent":100*len(hits)/len(rows),
        "q_target_hits":len(qhits),
        "q_target_hit_rate_percent":100*len(qhits)/len(rows),
        "A_over_B_median_all":med("A_over_B"),
        "A_over_B_p90_all":pct("A_over_B",90),
        "A_over_B_p99_all":pct("A_over_B",99),
        "q0_median_all":med("q0"),
        "q0_p90_all":pct("q0",90),
        "q_median_all":med("q"),
        "chi_median_all":med("chi"),
        "K_int_over_KU_median_all":med_ratio("K_int","K_U",rows),
        "K_x_over_KU_median_all":med_ratio("K_x","K_U",rows),
    }
    if hits:
        for k in ["A_over_B","q0","q","chi","K_U","K_x","K_int","beta_s","beta_f","G_star","eps_over_sigma","If_over_Is"]:
            out[f"joint_{k}_median"]=med(k,hits)
    if qhits:
        for k in ["A_over_B","q0","q","chi","K_U","K_x","K_int","beta_s","beta_f","G_star","eps_over_sigma","If_over_Is"]:
            out[f"qtarget_{k}_median"]=med(k,qhits)
    out["closure_class"]="DERIVED_REGION_FOUND" if out["joint_hit_rate_percent"]>=1 else ("RARE_OR_ABSENT" if hits else "NOT_FOUND")
    return out

def med_ratio(a,b,rows):
    vals=[x[a]/(x[b]+1e-12) for x in rows]
    return float(np.median(vals)) if vals else float("nan")

def run(n=150000, seed=2503):
    rng=np.random.default_rng(seed)
    rows=[]
    for _ in range(n):
        r=sample_block(rng)
        if r is not None and np.all(np.isfinite(list(r.values()))):
            rows.append(r)
    return summarize(rows)

def main():
    print("Asymmetry from block action verifier")
    print("="*50)
    print("Route:")
    print("block constants -> derived A/B and q0 -> check target asymmetry")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
