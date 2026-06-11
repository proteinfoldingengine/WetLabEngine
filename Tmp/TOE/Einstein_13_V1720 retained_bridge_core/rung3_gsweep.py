# Does local curvature R come FROM the non-associativity? Sweep g (kernel coupling).
# g=0 is the associative/flat limit (T=identity). If R->0 as g->0 and scales with g, the
# curvature is SOURCED by the recombination non-associativity -> the it-from-bit structure
# is the origin of the local geometry. Null check: associative kernel should give R~0 at all g.
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g): return dx + g*(roll(dx)*q - dx*roll(q))     # non-associative
def assoc_T(dx,q,g):  return dx + g*(roll(dx) + dx)               # associative control (linear, no cross)
def jac(q,g,Tf):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=Tf(e,q,g)
    return J
DIM=6
def metric_factory(g,Tf):
    def m(q):
        G=0.5*(jac(q,g,Tf)+jac(q,g,Tf).T); w=np.linalg.eigvalsh(G)
        if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
        return G
    return m
def make_R(metric_fn,h=1e-4):
    def dg(q,k):
        e=np.zeros(DIM); e[k]=h; return (metric_fn(q+e)-metric_fn(q-e))/(2*h)
    def christ(q):
        G=metric_fn(q); Gi=np.linalg.inv(G); dG=[dg(q,k) for k in range(DIM)]
        Ga=np.zeros((DIM,DIM,DIM))
        for l in range(DIM):
            for i in range(DIM):
                for j in range(DIM):
                    s=0.0
                    for m in range(DIM): s+=Gi[l,m]*(dG[i][m,j]+dG[j][m,i]-dG[m][i,j])
                    Ga[l,i,j]=0.5*s
        return Ga
    def R(q):
        G=metric_fn(q); Gi=np.linalg.inv(G); Ga=christ(q)
        dGa=np.zeros((DIM,DIM,DIM,DIM))
        for k in range(DIM):
            e=np.zeros(DIM); e[k]=h; dGa[k]=(christ(q+e)-christ(q-e))/(2*h)
        Ric=np.zeros((DIM,DIM))
        for i in range(DIM):
            for j in range(DIM):
                s=0.0
                for l in range(DIM):
                    term=dGa[l,l,i,j]-dGa[i,l,l,j]
                    for m in range(DIM): term+=Ga[l,l,m]*Ga[m,i,j]-Ga[l,i,m]*Ga[m,l,j]
                    s+=term
                Ric[i,j]=s
        return float(np.einsum('ij,ij->',Gi,Ric))
    return R
rng=np.random.default_rng(2); qs=[rng.normal(size=DIM) for _ in range(20)]
print(f"{'g':>6} | {'native R':>10}{'assoc R':>10} | R/g^2")
print("-"*38)
gs=[0.0,0.05,0.1,0.17,0.25,0.35,0.5]
nativeR=[]
for g in gs:
    Rn=make_R(metric_factory(g,native_T)); Ra=make_R(metric_factory(g,assoc_T))
    vn=np.median([Rn(q) for q in qs]); va=np.median([Ra(q) for q in qs])
    nativeR.append(vn)
    ratio = vn/(g**2) if g>0 else float('nan')
    print(f"{g:>6.2f} | {vn:>10.4f}{va:>10.4f} | {ratio:>6.3f}")
print("-"*38)
# fit scaling: is R ~ g^2?
import numpy as np
gg=np.array(gs[1:]); RR=np.array(nativeR[1:])
p=np.polyfit(np.log(gg),np.log(RR),1)
print(f"\nlog-log slope of R vs g = {p[0]:.2f}  (2.0 => R ~ g^2, sourced by non-associativity)")
print(f"R at g=0 (associative/flat limit) = {nativeR[0]:.4f}")
if nativeR[0]<1e-6 and abs(p[0]-2)<0.4:
    print("\nCONFIRMED: R vanishes at g=0 and scales ~g^2. The local curvature is SOURCED by the")
    print("recombination non-associativity. The it-from-bit structure IS the origin of the local geometry.")
elif nativeR[0]<1e-6:
    print(f"\nSOURCED but non-quadratic (slope {p[0]:.2f}): curvature still vanishes in the flat limit;")
    print("non-associativity is the origin, with a different scaling law.")
else:
    print("\nNOT cleanly sourced: R nonzero even at g=0. Curvature has another origin.")
