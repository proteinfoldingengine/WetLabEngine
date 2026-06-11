# RUNG 1.5 - does the NATIVE transport (not raw frame rotation) preserve the local metric?
# The metric g(q) = sym(native_jacobian(q)) is BUILT from the native kernel. The honest
# question: is the native transport metric-COMPATIBLE - does carrying g along a native edge
# p->q match the metric at q? If yes, the model glues itself (rung 1 completes). If no, the
# geometry is irreducibly local. Null: random transport of the same non-invertibility.
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def native_jacobian(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=native_T(e,q,g)
    return J
def metric(q): J=native_jacobian(q); return 0.5*(J+J.T)

DIM=24
# native transport as a linear map between charts p and q: the Jacobian of the edge map.
# metric-compatibility: g(p) =?= T_pq^T g(q) T_pq   (pullback of g(q) equals g(p))
def compat_error(p,q):
    Tpq=native_jacobian(q)            # linear native transport p->q uses state q
    gp=metric(p); gq=metric(q)
    pulled = Tpq.T @ gq @ Tpq
    return np.linalg.norm(pulled-gp)/(np.linalg.norm(gp)+1e-12)

def tb(p,q):  # non-invertibility of native edge, for matching the null
    x=np.ones(DIM)/np.sqrt(DIM)
    return np.linalg.norm(native_T(native_T(x,q),p)-x)/(np.linalg.norm(x)+1e-12)

def rand_compat(p,q,M,alpha):
    def Tr(dx): return dx+alpha*((M@dx)*q - dx*(M@roll(q)))
    n=DIM; J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=Tr(e)
    gp=metric(p); gq=metric(q)
    return np.linalg.norm(J.T@gq@J-gp)/(np.linalg.norm(gp)+1e-12)

nat=[];rnd=[]
rng=np.random.default_rng(3)
for t in range(120):
    p=rng.normal(size=DIM); q=rng.normal(size=DIM)
    nat.append(compat_error(p,q))
    # matched-noninvertibility random transport
    tgt=tb(p,q); M=rng.normal(size=(DIM,DIM)); M/=np.linalg.norm(M,2)
    def tbr(alpha):
        x=np.ones(DIM)/np.sqrt(DIM)
        Tr=lambda dx,s: dx+alpha*((M@dx)*s - dx*(M@roll(s)))
        return np.linalg.norm(Tr(Tr(x,q),p)-x)/(np.linalg.norm(x)+1e-12)
    al=np.linspace(0.02,3,40); va=[tbr(a) for a in al]; alpha=float(al[int(np.argmin(np.abs(np.array(va)-tgt)))])
    rnd.append(rand_compat(p,q,M,alpha))
nat=np.array(nat); rnd=np.array(rnd)
print("RUNG 1.5 - native transport metric-compatibility\n")
print(f"native transport compat error:  {nat.mean():.4f} +/- {nat.std():.4f}")
print(f"matched-random transport error: {rnd.mean():.4f} +/- {rnd.std():.4f}")
print(f"ratio random/native = {rnd.mean()/(nat.mean()+1e-12):.2f}")
print("-"*55)
if nat.mean()<0.05:
    print("GLUES: native transport is metric-compatible -> the connection that builds the")
    print("  metric also preserves it. Rung 1 COMPLETES self-consistently. -> Rung 2/3.")
elif nat.mean()<0.7*rnd.mean():
    print(f"PARTIAL: native preserves metric better than matched-random (ratio {rnd.mean()/nat.mean():.2f}).")
    print("  Structure-specific compatibility, not perfect. Characterize the residual.")
else:
    print("DOES NOT GLUE: native transport no better than random at preserving the metric.")
    print("  The geometry is IRREDUCIBLY LOCAL - local Riemannian metrics that do not")
    print("  transport compatibly. This is the model's actual structure: locally geometric,")
    print("  globally non-metric. A real finding about what this it-from-bit process builds.")
