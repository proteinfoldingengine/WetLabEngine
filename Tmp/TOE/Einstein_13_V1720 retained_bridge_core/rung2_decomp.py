# Decompose the non-metricity tensor: trace (Weyl/dilation) vs traceless.
# The non-metricity tensor is Q_{kij} = nabla_k g_ij = d_k g_ij - Gamma^l_{ki} g_lj - Gamma^l_{kj} g_il
# computed with the NATIVE connection. Its decomposition:
#   Weyl (trace) part:  Q_k = (1/n) g^{ij} Q_{kij}   -> uniform length rescaling (dilation)
#   traceless part:     Q_{kij} - (Weyl reconstruction)  -> shape-distorting non-metricity
# If Q is mostly trace -> the geometry is WEYL (lengths rescale, angles preserved): a dilation
# geometry with clean physical meaning. If traceless dominates -> richer shear-type non-metricity.
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g): return dx + g*(roll(dx)*q - dx*roll(q))
def jac(q,g,Tf=native_T):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=Tf(e,q,g)
    return J
DIM=6
def metric(q,g):
    G=0.5*(jac(q,g)+jac(q,g).T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
h=1e-4
def native_connection(q,g):
    # Gamma_nat^l_{kj} = (d_k J)^l_j  (transport-induced connection, as in Rung 2)
    Ga=np.zeros((DIM,DIM,DIM))  # Ga[l,k,j]
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h
        dJ=(jac(q+e,g)-jac(q-e,g))/(2*h)
        Ga[:,k,:]=dJ
    return Ga

def nonmetricity_tensor(q,g):
    G=metric(q,g)
    Ga=native_connection(q,g)
    # dg[k][i,j] = d_k g_ij
    dg=[]
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h; dg.append((metric(q+e,g)-metric(q-e,g))/(2*h))
    Q=np.zeros((DIM,DIM,DIM))  # Q[k,i,j] = nabla_k g_ij
    for k in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                s=dg[k][i,j]
                for l in range(DIM):
                    s-=Ga[l,k,i]*G[l,j]+Ga[l,k,j]*G[i,l]
                Q[k,i,j]=s
    return Q,G

def decompose(q,g):
    Q,G=nonmetricity_tensor(q,g)
    Gi=np.linalg.inv(G)
    # Weyl (trace) vector: W_k = (1/n) g^{ij} Q_{kij}
    W=np.zeros(DIM)
    for k in range(DIM):
        W[k]=np.einsum('ij,ij->',Gi,Q[k])/DIM
    # Weyl reconstruction: Q^Weyl_{kij} = W_k g_ij
    Qweyl=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        Qweyl[k]=W[k]*G
    Qtraceless=Q-Qweyl
    return np.linalg.norm(Qweyl), np.linalg.norm(Qtraceless), np.linalg.norm(Q)

rng=np.random.default_rng(4)
print("Non-metricity decomposition: Weyl (trace/dilation) vs traceless (shear)\n")
print(f"{'g':>6} | {'||Q||':>8}{'Weyl':>9}{'traceless':>11} | {'Weyl%':>7}{'tless%':>7}")
print("-"*54)
for g in [0.05,0.1,0.17,0.25,0.35]:
    ws=[];ts=[];qs=[]
    for t in range(30):
        q=rng.normal(size=DIM)
        w,tl,qn=decompose(q,g); ws.append(w);ts.append(tl);qs.append(qn)
    w,tl,qn=np.median(ws),np.median(ts),np.median(qs)
    wp=100*w/qn; tp=100*tl/qn
    print(f"{g:>6.2f} | {qn:>8.3f}{w:>9.3f}{tl:>11.3f} | {wp:>6.0f}%{tp:>6.0f}%")
print("-"*54)
print()
# decide
ws=[];ts=[]
for t in range(40):
    q=rng.normal(size=DIM); w,tl,qn=decompose(q,0.17); ws.append(w/qn); ts.append(tl/qn)
wf=np.median(ws); tf=np.median(ts)
print(f"At g=0.17: Weyl fraction={wf:.2f}, traceless fraction={tf:.2f}")
if wf>0.7:
    print("=> WEYL-DOMINATED: the non-metricity is mostly a trace (dilation). Lengths rescale")
    print("   under transport, angles approximately preserved. The model builds a WEYL geometry")
    print("   (conformal-like): a clean, recognized non-metric structure where recombination")
    print("   acts as a local length-gauge (scale) field. This is the it-from-bit dilation.")
elif tf>0.7:
    print("=> TRACELESS-DOMINATED: shear-type non-metricity; transport distorts shape, not just")
    print("   scale. A richer (non-conformal) metric-affine geometry.")
else:
    print("=> MIXED: both trace and traceless parts are significant; full metric-affine connection")
    print("   with both dilation and shear non-metricity.")
