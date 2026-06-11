# V1720 - Entropy Production Audit (T1 ONLY). New arc, fresh start.
# Question: is there a STATE-DEFINED entropy whose production sigma = dS/step is sign-definite,
# pruning-sourced (zero in invertible control), zero at g=0, weakened in associative control,
# and scaling with g?  Entropy defined from the state's OWN structure - NOT from dissipation.
# FROZEN candidate entropies (chosen before running):
#   S_support       = -sum p_i log p_i,  p_i = |x_i|^2 / sum|x|^2     (Shannon of amplitude dist)
#   S_participation = log( (sum|x|^2)^2 / sum|x|^4 )                    (log participation number)
# FORBIDDEN: any S built from norm-change, loop drift, or forward/reverse error.
import numpy as np
from scipy.linalg import expm
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx+g*(roll(dx)*q - dx*roll(q))
def assoc_T(dx,q,g=0.17):  return dx + g*roll(dx)            # associative (linear shift), no cross-term
def Jgen(q,g=0.17):
    n=len(q); J=np.zeros((n,n))
    for a in range(n):
        e=np.zeros(n);e[a]=1.0; J[:,a]=(native_T(e,q,g)-e)/g
    return J
def invertible_T(dx,q,g=0.17): return expm(g*0.5*(Jgen(q,g)-Jgen(q,g).T))@dx
DIM=8

# state-defined entropies (independent of dissipation)
def S_support(x):
    p=np.abs(x)**2; s=p.sum()
    if s<1e-15: return 0.0
    p=p/s; return float(-np.sum(p*np.log(p+1e-15)))
def S_participation(x):
    a2=np.sum(np.abs(x)**2); a4=np.sum(np.abs(x)**4)
    if a4<1e-15: return 0.0
    return float(np.log((a2**2)/a4 + 1e-15))

def production(transport,g,Sfunc,steps=40,n=400,seed=0):
    rng=np.random.default_rng(seed)
    sigmas=[]   # per-step Delta S, pooled
    for _ in range(n):
        x=rng.normal(size=DIM); x/=np.linalg.norm(x)
        Sprev=Sfunc(x)
        for _ in range(steps):
            q=rng.normal(size=DIM)
            x=transport(x,q,g)
            Snew=Sfunc(x)
            sigmas.append(Snew-Sprev)
            Sprev=Snew
    sigmas=np.array(sigmas)
    return sigmas.mean(), np.mean(sigmas>0), sigmas.std()

print("V1720 - Entropy Production Audit (T1). sigma = mean Delta S per ordered step.\n")
for Sname,Sf in [("S_support",S_support),("S_participation",S_participation)]:
    print(f"=== {Sname} ===")
    print(f"{'condition':>26}{'mean sigma':>12}{'frac sigma>0':>14}")
    nat_m,nat_f,_=production(native_T,0.17,Sf)
    inv_m,inv_f,_=production(invertible_T,0.17,Sf)
    g0_m,g0_f,_=production(native_T,0.0,Sf)
    as_m,as_f,_=production(assoc_T,0.17,Sf)
    print(f"{'native (g=0.17)':>26}{nat_m:>12.5f}{nat_f:>14.3f}")
    print(f"{'invertible (master null)':>26}{inv_m:>12.5f}{inv_f:>14.3f}")
    print(f"{'g=0 flat':>26}{g0_m:>12.5f}{g0_f:>14.3f}")
    print(f"{'associative kernel':>26}{as_m:>12.5f}{as_f:>14.3f}")
    # g-sweep
    print(f"  g-sweep (native) mean sigma:")
    for g in [0.0,0.05,0.1,0.17,0.25,0.4]:
        m,f,_=production(native_T,g,Sf)
        print(f"     g={g:.2f}: sigma={m:+.5f}  frac>0={f:.3f}")
    print()

print("="*56)
print("T1 PASS requires: native sigma sign-definite (frac>0 far from 0.5),")
print("  invertible control sigma ~ 0, g=0 ~ 0, associative weakened, sigma scales with g.")
print("If native sigma ~ 0 or invertible control also nonzero -> NO pruning entropy production.")
