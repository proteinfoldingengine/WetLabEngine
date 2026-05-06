
from __future__ import annotations
import numpy as np

def chi(q): 
    return 1/(1+q)

def stability_cost(q, q0, A, B, C, D):
    # q is retained-memory loading b/(1-a)
    # Underload penalty: A/q
    # Overload penalty: B*q
    # Critical-band penalty: C*(log(q/q0))^2
    # Responsiveness penalty: D/(chi(1-chi))
    c = chi(q)
    return A/(q+1e-12) + B*q + C*(np.log((q+1e-12)/q0)**2) + D/(c*(1-c)+1e-12)

def find_min(A,B,C,D,q0):
    qs = np.logspace(-3,3,3000)
    F = stability_cost(qs,q0,A,B,C,D)
    i = int(np.argmin(F))
    return float(qs[i]), float(chi(qs[i])), float(F[i])

def run_sweep(n=100000, seed=2401, q_target_low=2.75, q_target_high=3.3):
    rng=np.random.default_rng(seed)
    vals=[]; hits=[]
    for _ in range(n):
        # q0 is a candidate internal critical-loading scale, not fixed to target;
        # sampled broadly to test whether selection band can emerge.
        A=10**rng.uniform(-1,1.5)       # underload cost
        B=10**rng.uniform(-1,1.5)       # overload cost
        C=10**rng.uniform(-2,1.0)       # band-lock stiffness
        D=10**rng.uniform(-4,-0.2)      # bridge responsiveness penalty
        q0=10**rng.uniform(-0.2,0.8)    # possible critical loading 0.63..6.3
        qopt, chiopt, fmin = find_min(A,B,C,D,q0)
        rec=(qopt,chiopt,A,B,C,D,q0,A/B)
        if np.all(np.isfinite(rec)):
            vals.append(rec)
            if q_target_low<=qopt<=q_target_high:
                hits.append(rec)
    arr=np.asarray(vals); harr=np.asarray(hits) if hits else np.empty((0,8))
    out={
        "valid_samples":len(vals),
        "target_band_hits":len(hits),
        "target_band_hit_rate_percent":100*len(hits)/max(len(vals),1),
        "selection_class":"STABILIZATION_PLAUSIBLE" if 100*len(hits)/max(len(vals),1)>=5 else ("RARE_STABILIZATION" if hits else "NOT_FOUND")
    }
    names=["qopt","chiopt","A","B","C","D","q0","A_over_B"]
    if len(vals):
        for i,nm in enumerate(names):
            out[nm+"_median_all"]=float(np.median(arr[:,i]))
    if len(hits):
        for i,nm in enumerate(names):
            out[nm+"_median_hits"]=float(np.median(harr[:,i]))
            out[nm+"_p10_hits"]=float(np.percentile(harr[:,i],10))
            out[nm+"_p90_hits"]=float(np.percentile(harr[:,i],90))
    return out

def main():
    print("Asymmetry selection principle verifier")
    print("="*50)
    print("Route:")
    print("underload + overload + critical-band + bridge-response penalties -> selected q=b/(1-a)")
    print("Tests intermediate-loading stabilization, not final derivation.")
    print()
    for k,v in run_sweep().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
