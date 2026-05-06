
from __future__ import annotations
import numpy as np
from math import sqrt, pi, exp

def integrals(sigma, r):
    Is = sigma * sqrt(2/pi)
    If = Is * exp(-(r**2)/2)
    return Is, If

def sample(rng, mode="broad"):
    ws = rng.uniform(0.05, 0.95); wf=1-ws
    alpha_s=rng.uniform(0,.99); alpha_f=rng.uniform(0,.99)
    c_s=rng.uniform(.05,1); c_f=rng.uniform(.05,1)
    mu_G=10**rng.uniform(-.2,.8)
    if mode=="memory_biased":
        beta_s=10**rng.uniform(-1,1.2); beta_f=10**rng.uniform(-1,1.2)
        G_star=10**rng.uniform(-2,.3)
        sigma=10**rng.uniform(0,1); r=rng.uniform(0,2)
    else:
        beta_s=10**rng.uniform(-3,1); beta_f=10**rng.uniform(-3,1)
        G_star=10**rng.uniform(-2,1)
        sigma=10**rng.uniform(-1,1); r=rng.uniform(0,4)
    Is, If = integrals(sigma, r)
    a=(ws*alpha_s*c_s+wf*alpha_f*c_f)/mu_G
    if not (0<=a<1): return None
    b=(ws*beta_s*Is+wf*beta_f*If)/(mu_G*G_star)
    if b<=0: return None
    q=b/(1-a)
    chi=1/(1+q)
    mem=ws*beta_s*Is+wf*beta_f*If
    gap=mu_G-(ws*alpha_s*c_s+wf*alpha_f*c_f)
    drive=mem/(G_star*gap+1e-12) if gap>0 else np.nan
    return {"q":q,"chi":chi,"a":a,"b":b,"G_star":G_star,"memory_input":mem,
            "eps_over_sigma":r,"If_over_Is":If/Is,"loading_drive":drive,
            "beta_s":beta_s,"beta_f":beta_f,"sigma":sigma}

def summarize(rows):
    hits=[x for x in rows if 2.75<=x["q"]<=3.3]
    near=[x for x in rows if 2.4<=x["q"]<=3.6]
    def med(k, arr=rows):
        return float(np.median([x[k] for x in arr])) if arr else float("nan")
    out={"valid_samples":len(rows),"target_hits_2p75_to_3p3":len(hits),
         "target_hit_rate_percent":100*len(hits)/max(len(rows),1),
         "near_hits_2p4_to_3p6":len(near),
         "near_hit_rate_percent":100*len(near)/max(len(rows),1),
         "q_median_all":med("q"),"chi_median_all":med("chi"),
         "loading_drive_median_all":med("loading_drive"),
         "G_star_median_all":med("G_star"),
         "memory_input_median_all":med("memory_input"),
         "eps_over_sigma_median_all":med("eps_over_sigma"),
         "If_over_Is_median_all":med("If_over_Is")}
    for name, arr in [("target",hits),("near",near)]:
        if arr:
            for k in ["q","chi","a","b","loading_drive","G_star","memory_input","eps_over_sigma","If_over_Is","beta_s","beta_f","sigma"]:
                out[f"{name}_{k}_median"]=med(k,arr)
    out["naturalness_class"]="NATURAL_ASYMMETRY" if out["target_hit_rate_percent"]>=5 else ("RARE_BUT_PRESENT" if hits else "NOT_FOUND")
    return out

def run(n=75000, seed=2309):
    rng=np.random.default_rng(seed)
    outs={}
    for mode in ["broad","memory_biased"]:
        rows=[]
        for _ in range(n):
            r=sample(rng, mode)
            if r is not None and np.all(np.isfinite(list(r.values()))):
                rows.append(r)
        s=summarize(rows)
        for k,v in s.items():
            outs[f"{mode}_{k}"]=v
    return outs

def main():
    print("Retained memory loading asymmetry verifier")
    print("="*50)
    print("Route:")
    print("explicit pruning integrals + micro-to-block loading -> q=b/(1-a) distribution")
    print()
    for k,v in run().items():
        print(f"{k}: {v}")

if __name__=="__main__":
    main()
