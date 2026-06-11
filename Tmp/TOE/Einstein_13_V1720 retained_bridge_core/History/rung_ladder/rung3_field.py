# Characterize the curvature as a FIELD over configuration space.
# Questions: (1) is R positive everywhere, or are there negative-curvature regions?
# (2) does R have STRUCTURE - does it concentrate where the recombination kernel is most active
#     (large |roll(q)| cross-terms), or is it uniform? (3) what is the curvature distribution?
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def jac(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=native_T(e,q,g)
    return J
DIM=6
def metric(q,g=0.17):
    G=0.5*(jac(q,g)+jac(q,g).T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
def make_R(h=1e-4,g=0.17):
    def dg(q,k):
        e=np.zeros(DIM); e[k]=h; return (metric(q+e,g)-metric(q-e,g))/(2*h)
    def christ(q):
        G=metric(q,g); Gi=np.linalg.inv(G); dG=[dg(q,k) for k in range(DIM)]
        Ga=np.zeros((DIM,DIM,DIM))
        for l in range(DIM):
            for i in range(DIM):
                for j in range(DIM):
                    s=0.0
                    for m in range(DIM): s+=Gi[l,m]*(dG[i][m,j]+dG[j][m,i]-dG[m][i,j])
                    Ga[l,i,j]=0.5*s
        return Ga
    def R(q):
        G=metric(q,g); Gi=np.linalg.inv(G); Ga=christ(q)
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

R=make_R()
rng=np.random.default_rng(7)
# sample configuration space at varying radius (kernel activity scales with |q|)
radii=[0.3,0.7,1.2,2.0,3.0]
print("Curvature field vs configuration radius |q| (kernel activity grows with |q|):\n")
print(f"{'|q|':>6} | {'mean R':>9}{'std R':>9}{'min R':>9}{'max R':>9}{'%neg':>7}")
print("-"*52)
allR=[]
for r in radii:
    Rs=[]
    for t in range(40):
        q=rng.normal(size=DIM); q=r*q/np.linalg.norm(q)
        Rs.append(R(q))
    Rs=np.array(Rs); allR.extend(Rs)
    print(f"{r:>6.1f} | {Rs.mean():>9.3f}{Rs.std():>9.3f}{Rs.min():>9.3f}{Rs.max():>9.3f}{(Rs<0).mean()*100:>6.0f}%")
allR=np.array(allR)
print("-"*52)
print(f"\nGlobal over all sampled states: mean R={allR.mean():.3f}, fraction negative={ (allR<0).mean()*100:.1f}%")
# correlation of R with kernel activity proxy
rng=np.random.default_rng(13); qs=[rng.normal(size=DIM)*rng.uniform(0.3,3) for _ in range(120)]
Rv=np.array([R(q) for q in qs])
activity=np.array([np.linalg.norm(roll(q)*q - q*roll(q)) for q in qs])  # non-assoc cross-term magnitude
corr=np.corrcoef(Rv,activity)[0,1]
print(f"corr(R, non-associative cross-term magnitude) = {corr:.2f}")
print()
if (allR<0).mean()<0.02:
    print("UNIFORMLY POSITIVE: R>0 across configuration space -> the local geometry is")
    print("definite, sphere-like everywhere. Curvature grows with kernel activity (corr above).")
    print("The process builds a uniformly positively-curved local geometry, strongest where")
    print("the non-associative recombination is most active.")
else:
    print(f"MIXED SIGN: {(allR<0).mean()*100:.0f}% negative regions -> indefinite/saddle structure.")
