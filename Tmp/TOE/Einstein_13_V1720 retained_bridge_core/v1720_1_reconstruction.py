# V1720.1 - Reconstruction Entropy Audit. The last allowed T1 candidate.
# w_i = normalized contribution of retained generator i to reconstructing the state, from
# PROJECTION coefficients onto a fixed retained generator basis. Independent of dissipation.
# S_recon = -sum w_i log w_i.  Same gates as V1720.
import numpy as np
from scipy.linalg import expm
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx+g*(roll(dx)*q - dx*roll(q))
def assoc_T(dx,q,g=0.17):  return dx + g*roll(dx)
def Jgen(q,g=0.17):
    n=len(q); J=np.zeros((n,n))
    for a in range(n):
        e=np.zeros(n);e[a]=1.0; J[:,a]=(native_T(e,q,g)-e)/g
    return J
def invertible_T(dx,q,g=0.17): return expm(g*0.5*(Jgen(q,g)-Jgen(q,g).T))@dx
DIM=8

# fixed retained generator basis: the roll-shifted unit directions (the kernel's own structure).
# reconstruction weights = squared projection coefficients onto this basis (orthonormal here),
# i.e. how the state distributes over the retained generators. Independent of any dissipation measure.
BASIS=np.eye(DIM)   # standard retained-coordinate generators; orthonormal
def S_recon(x):
    w=np.abs(BASIS.T@x)**2; s=w.sum()
    if s<1e-15: return 0.0
    w=w/s; return float(-np.sum(w*np.log(w+1e-15)))
# also the effective-reconstruction-support variant
def S_recon_eff(x):
    w=np.abs(BASIS.T@x)**2; s=w.sum()
    if s<1e-15: return 0.0
    w=w/s; return float(np.log(1.0/np.sum(w**2)+1e-15))

def production(transport,g,Sfunc,steps=40,n=400,seed=0):
    rng=np.random.default_rng(seed); sig=[]
    for _ in range(n):
        x=rng.normal(size=DIM); x/=np.linalg.norm(x); Sp=Sfunc(x)
        for _ in range(steps):
            q=rng.normal(size=DIM); x=transport(x,q,g); Sn=Sfunc(x); sig.append(Sn-Sp); Sp=Sn
    sig=np.array(sig); return sig.mean(), np.mean(sig>0)

print("V1720.1 - Reconstruction Entropy Audit (last T1 candidate)\n")
for Sname,Sf in [("S_recon",S_recon),("S_recon_eff",S_recon_eff)]:
    print(f"=== {Sname} ===")
    print(f"{'condition':>26}{'mean sigma':>12}{'frac sigma>0':>14}")
    for cname,tr,g in [("native (g=0.17)",native_T,0.17),("invertible (master null)",invertible_T,0.17),
                       ("g=0 flat",native_T,0.0),("associative kernel",assoc_T,0.17)]:
        m,f=production(tr,g,Sf); print(f"{cname:>26}{m:>12.5f}{f:>14.3f}")
    print("  g-sweep (native):", end=" ")
    for g in [0.0,0.1,0.17,0.25,0.4]:
        m,f=production(native_T,g,Sf); print(f"g{g:.2f}:{m:+.4f}", end="  ")
    print("\n")
print("="*56)
print("Same gates: sign-definite? invertible~0? assoc weakened? scales w/ g?")
print("If it fails like S_support/S_participation (assoc stronger, frac~0.5) -> T1 CLOSED NEGATIVE.")
