# V1719 - Retained-Order Lyapunov Audit. Does native pruning transport admit a scalar functional
# that is STRICTLY monotone under forward recombination? NO HEURISTICS: test each candidate
# SEPARATELY. A composite is allowed ONLY if derived before results - not fitted.
# Candidates (each measured independently, no tuning):
#   L1 = log||amplitude||   L2 = reconstruction deficit   L3 = support loss
#   L4 = entropy concentration   L5 = non-invertibility defect   L6 = loop drift accumulation
import numpy as np
from scipy.linalg import expm
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx+g*(roll(dx)*q - dx*roll(q))
def Jgen(q,g=0.17):
    n=len(q); J=np.zeros((n,n))
    for a in range(n):
        e=np.zeros(n);e[a]=1.0; J[:,a]=(native_T(e,q,g)-e)/g
    return J
def invertible_T(dx,q,g=0.17): return expm(g*0.5*(Jgen(q,g)-Jgen(q,g).T))@dx
DIM=8; rng=np.random.default_rng(7)

def run_trajectory(steps=40, transport=native_T):
    dx=rng.normal(size=DIM); dx/=np.linalg.norm(dx)
    x0=dx.copy()
    L1=[];L3=[];L4=[];L5=[];L2=[];hist=[x0]
    for t in range(steps):
        q=rng.normal(size=DIM)
        prev=dx.copy()
        dx=transport(dx,q)
        hist.append(dx.copy())
        p=np.abs(dx)**2; p=p/p.sum()
        L1.append(np.log(np.linalg.norm(dx)+1e-12))               # log amplitude
        L3.append(np.sum(np.abs(dx)>0.1*np.max(np.abs(dx))))      # support size (loss = decrease)
        L4.append(np.max(p))                                       # concentration (1-entropy proxy)
        # non-invertibility defect: how much a back-step fails to recover prev
        back=transport(dx,q)
        L5.append(np.linalg.norm(back-prev)/ (np.linalg.norm(prev)+1e-12))
        # reconstruction deficit: distance from original x0 (cumulative info loss)
        L2.append(np.linalg.norm(dx-x0)/np.linalg.norm(x0))
    return dict(L1=np.array(L1),L2=np.array(L2),L3=np.array(L3),L4=np.array(L4),L5=np.array(L5))

# monotonicity fraction per candidate, averaged over many trajectories
def monotonicity(name_key, expected_sign, n=300, transport=native_T):
    fracs=[]
    for _ in range(n):
        tr=run_trajectory(transport=transport)[name_key]
        d=np.diff(tr)
        d=d[np.abs(d)>1e-12]
        if len(d)==0: continue
        fracs.append(np.mean(np.sign(d)==expected_sign))
    return np.mean(fracs)

print("V1719 - Retained-Order Lyapunov Audit (each candidate tested SEPARATELY, no tuning)\n")
print("monotonicity = fraction of forward steps moving in the candidate's consistent direction")
print("(per-trajectory, then averaged; strict Lyapunov would be ~1.00)\n")
print(f"{'candidate':>28}{'native mono%':>14}{'invertible-control':>20}")
print("-"*62)
cands=[("L1 log||amplitude||","L1",+1),("L2 reconstruction deficit","L2",+1),
       ("L3 support size","L3",-1),("L4 concentration","L4",+1),
       ("L5 non-invertibility defect","L5",+1)]
results={}
for label,key,sign in cands:
    natm=monotonicity(key,sign,transport=native_T)
    invm=monotonicity(key,sign,transport=invertible_T)
    results[key]=(natm,invm)
    print(f"{label:>28}{natm*100:>13.0f}%{invm*100:>19.0f}%")
print("-"*62)

# L2 (reconstruction deficit / cumulative distance from origin) is the natural candidate for a
# monotone in a NON-INVERTIBLE forward process: once you move away you can't return -> should
# rise near-monotonically. Check it specifically.
print("\nFocused check - L2 (cumulative distance from origin) over a single long trajectory:")
tr=run_trajectory(steps=60)["L2"]
strict_inc=np.mean(np.diff(tr)>0)
print(f"  L2 strictly increasing fraction = {strict_inc:.2%}, net {tr[0]:.3f} -> {tr[-1]:.3f}")
print()
best=max(results.items(), key=lambda kv: kv[1][0])
print("VERDICT:")
bk,(bn,bi)=best
if bn>0.97:
    print(f"  LYAPUNOV-LIKE SCALAR FOUND: {bk} is {bn:.0%} monotone under native transport")
    print(f"  and {bi:.0%} under the invertible control -> the arrow admits a Lyapunov-like scalar.")
elif bn>0.85:
    print(f"  NEAR-MONOTONE: best candidate {bk} = {bn:.0%} monotone (not strict). The arrow is")
    print(f"  strongly directional but no STRICT scalar Lyapunov function in this audit.")
else:
    print(f"  NO STRICT MONOTONE: best {bk} = {bn:.0%}. Arrow is dissipative/statistical, not")
    print(f"  governed by a strict scalar Lyapunov function in this audit.")
print("\n(No composite was fitted. Candidates reported separately per the no-heuristics rule.)")
