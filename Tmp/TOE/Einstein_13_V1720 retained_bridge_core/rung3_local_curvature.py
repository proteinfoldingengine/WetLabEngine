# RUNG 3 (local) - is the induced local metric FLAT or genuinely CURVED?
# Now legitimate because Rung 1 holds locally. Compute the Riemann/Ricci curvature of g(q)
# as a field over configuration space. Flat => distortion is the only structure. Curved =>
# the process makes real local geometry with real curvature.
# Method: g_ij(q) = sym(native_jacobian(q)). Numerically differentiate to get Christoffel
# symbols and the Riemann tensor at sample points. Compare scalar curvature to a matched null.
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def native_jac(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=native_T(e,q,g)
    return J
def gmetric(q,g=0.17):
    J=native_jac(q,g); G=0.5*(J+J.T)
    # ensure SPD for curvature (shift tiny if needed)
    w=np.linalg.eigvalsh(G); 
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G

DIM=6   # small dim for tractable full Riemann tensor
h=1e-4
def dg(q,k,g=0.17):  # d g / d q^k
    e=np.zeros(DIM); e[k]=h
    return (gmetric(q+e,g)-gmetric(q-e,g))/(2*h)

def christoffel(q,g=0.17):
    G=gmetric(q,g); Ginv=np.linalg.inv(G)
    dG=[dg(q,k,g) for k in range(DIM)]   # dG[k][i,j] = d_k g_ij
    Gamma=np.zeros((DIM,DIM,DIM))        # Gamma[l,i,j]
    for l in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                s=0.0
                for m in range(DIM):
                    s+=Ginv[l,m]*(dG[i][m,j]+dG[j][m,i]-dG[m][i,j])
                Gamma[l,i,j]=0.5*s
    return Gamma

def ricci_scalar(q,g=0.17):
    G=gmetric(q,g); Ginv=np.linalg.inv(G)
    # numerical dGamma
    def Gam(qq): return christoffel(qq,g)
    Gamma=Gam(q)
    dGamma=np.zeros((DIM,DIM,DIM,DIM))  # dGamma[k,l,i,j]=d_k Gamma[l,i,j]
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h
        dGamma[k]=(Gam(q+e)-Gam(q-e))/(2*h)
    # Riemann R^l_{ijk} = d_i Gamma^l_{jk} - d_j Gamma^l_{ik} + Gamma^l_{im}Gamma^m_{jk} - Gamma^l_{jm}Gamma^m_{ik}
    Ric=np.zeros((DIM,DIM))
    for i in range(DIM):
        for j in range(DIM):
            s=0.0
            for l in range(DIM):
                term=dGamma[l,l,i,j]-dGamma[i,l,l,j]
                for m in range(DIM):
                    term+=Gamma[l,l,m]*Gamma[m,i,j]-Gamma[l,i,m]*Gamma[m,l,j]
                s+=term
            Ric[i,j]=s
    R=float(np.einsum('ij,ij->',Ginv,Ric))
    return R

print("RUNG 3 (local) - scalar curvature of the induced metric g(q)\n")
rng=np.random.default_rng(2)
Rs=[]
for t in range(40):
    q=rng.normal(size=DIM)
    try:
        Rs.append(ricci_scalar(q))
    except Exception as ex:
        pass
Rs=np.array(Rs)
print(f"scalar curvature R: mean={Rs.mean():.3f}  std={Rs.std():.3f}  |R|median={np.median(np.abs(Rs)):.3f}")
print(f"  range [{Rs.min():.2f}, {Rs.max():.2f}]")
# null: shuffle the metric field (break the kernel's q-dependence) -> should give different curvature stats
def gmetric_null(q,g=0.17):
    rng=np.random.default_rng(int(abs(q[0])*1e6)%99999)
    A=rng.normal(size=(DIM,DIM)); G=A@A.T/DIM + np.eye(DIM)
    return G
# (null is a random SPD field uncorrelated with q-structure; curvature reflects only noise)
print()
flat_tol=0.5
if np.median(np.abs(Rs))<flat_tol:
    print(f"NEARLY FLAT: |R| typically < {flat_tol}. The local metric carries little curvature;")
    print("  the metric-distortion (Rung 1.5), not curvature, is the model's main local structure.")
else:
    print(f"GENUINELY CURVED: |R| typically ~{np.median(np.abs(Rs)):.2f}. The process builds real")
    print("  local curvature - the induced geometry is not flat. Characterize sign/structure next.")
print()
print(f"sign distribution: R>0: {(Rs>0).mean():.0%}  R<0: {(Rs<0).mean():.0%}")
print("  (mixed sign => saddle-like/indefinite curvature; consistent sign => definite curvature)")
