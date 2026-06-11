# RUNG 2 - the non-metricity: how far does the native recombination transport depart from the
# Levi-Civita connection of the induced metric? The difference is a tensor (the model's real
# geometric content). Two connections:
#   Gamma_LC   : Levi-Civita of g(q) (metric-compatible, gave us the curvature)
#   Gamma_nat  : native recombination transport's connection (metric-distorting, Rung 1.5)
# Non-metricity Q = Gamma_nat - Gamma_LC. Characterize its size, scaling with g, and whether
# it is structure-specific (vs associative null).
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g): return dx + g*(roll(dx)*q - dx*roll(q))
def assoc_T(dx,q,g):  return dx + g*(roll(dx)+dx)
def jac(q,g,Tf):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=Tf(e,q,g)
    return J
DIM=6
def metric(q,g,Tf):
    G=0.5*(jac(q,g,Tf)+jac(q,g,Tf).T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
h=1e-4
def christoffel_LC(q,g,Tf):
    def gm(x): return metric(x,g,Tf)
    G=gm(q); Gi=np.linalg.inv(G)
    dG=[]
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h; dG.append((gm(q+e)-gm(q-e))/(2*h))
    Ga=np.zeros((DIM,DIM,DIM))
    for l in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                Ga[l,i,j]=0.5*sum(Gi[l,m]*(dG[i][m,j]+dG[j][m,i]-dG[m][i,j]) for m in range(DIM))
    return Ga
def christoffel_native(q,g,Tf):
    # connection of the native transport: Gamma^l_{ij} from how the transport map varies.
    # native transport along direction j changes a vector; the connection coefficients are
    # the derivative of the transport Jacobian. Gamma_nat^l_{ij} = d_j J^l_i (transport-induced).
    def J(x): return jac(x,g,Tf)
    Ga=np.zeros((DIM,DIM,DIM))
    for j in range(DIM):
        e=np.zeros(DIM); e[j]=h
        dJ=(J(q+e)-J(q-e))/(2*h)     # d_j of transport Jacobian
        Ga[:,:,j]=dJ
    return Ga

def nonmetricity(q,g,Tf):
    Q=christoffel_native(q,g,Tf)-christoffel_LC(q,g,Tf)
    return np.linalg.norm(Q)

rng=np.random.default_rng(5)
qs=[rng.normal(size=DIM) for _ in range(30)]
print("RUNG 2 - non-metricity Q = ||Gamma_native - Gamma_LC|| (departure from ordinary geometry)\n")
print(f"{'g':>6} | {'native Q':>10}{'assoc Q':>10} | Q/g")
print("-"*38)
gs=[0.0,0.05,0.1,0.17,0.25,0.35,0.5]
natQ=[]
for g in gs:
    qn=np.median([nonmetricity(q,g,native_T) for q in qs])
    qa=np.median([nonmetricity(q,g,assoc_T) for q in qs])
    natQ.append(qn)
    print(f"{g:>6.2f} | {qn:>10.4f}{qa:>10.4f} | {qn/g if g>0 else float('nan'):>6.3f}")
print("-"*38)
gg=np.array(gs[1:]); QQ=np.array(natQ[1:])
slope=np.polyfit(np.log(gg),np.log(QQ),1)[0]
print(f"\nlog-log slope of Q vs g = {slope:.2f}")
print(f"Q at g=0 = {natQ[0]:.4f}")
print()
print("Interpretation:")
if natQ[0]<1e-6:
    print(f" Non-metricity VANISHES in the associative limit and scales ~g^{slope:.1f}.")
    print(" => the departure from ordinary (metric-compatible) geometry is SOURCED by the")
    print("    non-associativity. The native transport's refusal to preserve the metric IS")
    print("    the geometric signature of the it-from-bit recombination.")
print()
# compare scaling: curvature was ~g^2. Is non-metricity LOWER order (g^1)? That would mean
# non-metricity is the PRIMARY (leading) effect, curvature secondary.
print(f"Recall curvature R ~ g^2. Non-metricity Q ~ g^{slope:.1f}.")
if slope < 1.5:
    print(" Q is LOWER-order than R => non-metricity is the PRIMARY geometric effect;")
    print(" curvature is a higher-order consequence. The model's leading geometry is NON-METRIC.")
else:
    print(" Q and R similar order => non-metricity and curvature are co-leading.")
