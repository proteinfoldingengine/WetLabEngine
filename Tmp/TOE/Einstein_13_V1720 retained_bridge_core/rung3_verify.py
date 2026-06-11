# Verify: is R~0.1 real curvature or a finite-difference artifact? Vary h; real curvature is
# h-stable, artifact tracks h. Also add a FLAT control (constant metric -> R must be ~0) to
# measure the scheme's noise floor, and a known-curved control (sphere metric -> known R>0).
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def native_jac(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=native_T(e,q,g)
    return J
DIM=6
def gmetric(q,g=0.17):
    J=native_jac(q,g); G=0.5*(J+J.T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
def make_ricci(metric_fn,h):
    def dg(q,k):
        e=np.zeros(DIM); e[k]=h; return (metric_fn(q+e)-metric_fn(q-e))/(2*h)
    def christ(q):
        G=metric_fn(q); Ginv=np.linalg.inv(G); dG=[dg(q,k) for k in range(DIM)]
        Ga=np.zeros((DIM,DIM,DIM))
        for l in range(DIM):
            for i in range(DIM):
                for j in range(DIM):
                    s=0.0
                    for m in range(DIM): s+=Ginv[l,m]*(dG[i][m,j]+dG[j][m,i]-dG[m][i,j])
                    Ga[l,i,j]=0.5*s
        return Ga
    def R(q):
        G=metric_fn(q); Ginv=np.linalg.inv(G); Ga=christ(q)
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
        return float(np.einsum('ij,ij->',Ginv,Ric))
    return R

# controls
def flat_metric(q): return np.eye(DIM)                      # R must be ~0 (noise floor)
def sphere_metric(q):                                        # conformally curved, known R>0
    f=1.0/(1.0+0.25*np.dot(q,q))**2
    return f*np.eye(DIM)

rng=np.random.default_rng(2)
qs=[rng.normal(size=DIM) for _ in range(20)]
print(f"{'h':>8} | {'native R':>10}{'flat R(floor)':>14}{'sphere R':>10}")
print("-"*46)
for h in [1e-3,3e-4,1e-4,3e-5]:
    Rn=make_ricci(gmetric,h); Rf=make_ricci(flat_metric,h); Rs=make_ricci(sphere_metric,h)
    vn=np.median([Rn(q) for q in qs]); vf=np.median([abs(Rf(q)) for q in qs]); vs=np.median([Rs(q) for q in qs])
    print(f"{h:>8.0e} | {vn:>10.4f}{vf:>14.2e}{vs:>10.4f}")
print("-"*46)
print("native R h-stable & >> flat floor => REAL curvature. tracks h or ~floor => artifact.")
print("sphere R should be stable positive (sanity that the scheme detects real curvature).")
