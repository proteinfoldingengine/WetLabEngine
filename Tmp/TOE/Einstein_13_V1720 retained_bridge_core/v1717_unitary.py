# V1717 - Unitary / Complex Amplitude Audit. Is the interference real-signed-only, or does it
# have norm-conservation + phase/unitary structure? Each test has the associative control.
# DISCIPLINE: claim only what is measured. Norm conservation + skew generator => unitary-like.
# Norm NOT conserved => real signed interference, dissipative, NOT quantum-mechanical amplitudes.
import numpy as np
def roll(v): return np.roll(v,1)
def K_native(x,y): return roll(x)*y - x*roll(y)
def op(x,y,g=0.17): return x+y+g*K_native(x,y)
DIM=8
rng=np.random.default_rng(7)

# ---- TEST 1: norm conservation under recombination transport ----
# native transport T(dx)=dx+g(roll(dx)*q - dx*roll(q)). Does it preserve ||dx||?
def native_T(dx,q,g=0.17): return dx+g*(roll(dx)*q - dx*roll(q))
norms_before=[]; norms_after=[]
for _ in range(300):
    dx=rng.normal(size=DIM); q=rng.normal(size=DIM)
    nb=np.linalg.norm(dx); na=np.linalg.norm(native_T(dx,q))
    norms_before.append(nb); norms_after.append(na/nb)
print("TEST 1 - norm conservation under native transport:")
print(f"  ||T dx|| / ||dx|| = {np.mean(norms_after):.4f} +/- {np.std(norms_after):.4f}")
print(f"  (1.0 = norm-preserving/unitary-like; !=1 = dissipative/non-unitary)")

# ---- TEST 2: is the transport generator skew-symmetric (J^T = -J => exp(gJ) unitary)? ----
# linearize: T = I + g J(q). Is J(q) skew?
def Jgen(q,g=0.17):
    n=len(q); J=np.zeros((n,n))
    for a in range(n):
        e=np.zeros(n);e[a]=1.0
        J[:,a]=(native_T(e,q,g)-e)/g
    return J
skew=[]; symm=[]
for _ in range(100):
    q=rng.normal(size=DIM); J=Jgen(q)
    sk=0.5*(J-J.T); sy=0.5*(J+J.T)
    skew.append(np.linalg.norm(sk)); symm.append(np.linalg.norm(sy))
skew=np.array(skew); symm=np.array(symm)
print(f"\nTEST 2 - generator decomposition J = skew + symmetric:")
print(f"  ||skew|| = {skew.mean():.4f}   ||symmetric|| = {symm.mean():.4f}")
print(f"  skew fraction = {skew.mean()/(skew.mean()+symm.mean()):.3f}")
print(f"  (skew-dominated => unitary-like rotation; symmetric => dissipative/scaling)")

# ---- TEST 3: does exp(gJ_skew) approximate native transport? (unitary representability) ----
from scipy.linalg import expm
err_skew=[]; err_full=[]
for _ in range(60):
    q=rng.normal(size=DIM); J=Jgen(q); g=0.17
    Jsk=0.5*(J-J.T)
    Tnative=np.eye(DIM)+g*J
    Texp_skew=expm(g*Jsk)
    dx=rng.normal(size=DIM)
    err_skew.append(np.linalg.norm(Texp_skew@dx - Tnative@dx)/np.linalg.norm(Tnative@dx))
print(f"\nTEST 3 - does unitary exp(g*skew) reproduce native transport?")
print(f"  relative error ||exp(gJ_skew)dx - T_native dx|| = {np.mean(err_skew):.4f}")
print(f"  (small => native transport IS approximately unitary; large => it is not)")

# ---- TEST 4: history interference norm - do squared norms give STABLE endpoint weights (Born-like)? ----
import itertools
def histories(sources,g=0.17):
    outs=[]
    for perm in itertools.permutations(range(len(sources))):
        seq=[sources[i] for i in perm]; l=seq[0]
        for s in seq[1:]: l=op(l,s,g)
        outs.append(l)
    return outs
# Born-like test: is sum of |h|^2 conserved / stable vs sum of h then squared?
coh2=[]; cl2=[]
for _ in range(150):
    sources=[rng.normal(size=DIM) for _ in range(4)]
    H=histories(sources)
    coherent=np.linalg.norm(np.sum(H,axis=0))**2
    incoh=np.sum([np.linalg.norm(h)**2 for h in H])
    coh2.append(coherent); cl2.append(incoh)
print(f"\nTEST 4 - squared-norm (Born-like) structure:")
print(f"  |sum h|^2 / sum|h|^2 = {np.mean(np.array(coh2)/np.array(cl2)):.4f}")
print(f"  (this is just a diagnostic; Born rule requires probability normalization we do NOT claim)")

print("\n"+"="*58)
print("VERDICT LOGIC:")
nc=np.mean(norms_after); sf=skew.mean()/(skew.mean()+symm.mean())
if abs(nc-1)<0.05 and sf>0.7:
    print("UNITARY-LIKE: norm ~conserved AND generator skew-dominated => the interference has")
    print("  unitary-like (phase-rotation) structure. Quantum-mechanical-like amplitude dynamics begin.")
elif abs(nc-1)>0.1 or sf<0.5:
    print(f"REAL SIGNED ONLY: norm ratio {nc:.3f} (not 1), skew fraction {sf:.3f}. The interference is")
    print("  real signed cancellation, DISSIPATIVE/non-unitary - amplitude-LIKE but NOT quantum-")
    print("  mechanical amplitude dynamics. No phase/norm-conservation structure.")
else:
    print(f"PARTIAL: norm ratio {nc:.3f}, skew fraction {sf:.3f}. Mixed unitary/dissipative.")
