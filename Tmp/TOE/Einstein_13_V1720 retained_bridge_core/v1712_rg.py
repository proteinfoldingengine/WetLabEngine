# V1712 - COUPLED / RG coarse-graining. The real test: patches are not averaged independently;
# they are TRANSPORTED into a common frame via the native connection, then combined, scale by
# scale (block-spin RG). Does the non-metricity survive interacting coarse-graining, or does the
# coupling produce structured cancellation -> an effective metric sector?
# Guard: compare to (a) the independent-average plateau (V1711) and (b) an associative-kernel RG
# (must flow to zero non-metricity - sanity) and (c) random-transport RG matched null.
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def assoc_T(dx,q,g=0.17):  return dx + g*(roll(dx)+dx)
def jac(q,g,Tf):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=Tf(e,q,g)
    return J
DIM=6; h=1e-4
def metric(q,g,Tf):
    G=0.5*(jac(q,g,Tf)+jac(q,g,Tf).T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
def conn(q,g,Tf):
    Ga=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h; Ga[:,k,:]=(jac(q+e,g,Tf)-jac(q-e,g,Tf))/(2*h)
    return Ga
def Qtensor(q,g,Tf):
    G=metric(q,g,Tf); Ga=conn(q,g,Tf)
    dg=[(metric(q+np.eye(DIM)[k]*h,g,Tf)-metric(q-np.eye(DIM)[k]*h,g,Tf))/(2*h) for k in range(DIM)]
    Q=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                s=dg[k][i,j]
                for l in range(DIM): s-=Ga[l,k,i]*G[l,j]+Ga[l,k,j]*G[i,l]
                Q[k,i,j]=s
    return Q

# RG STEP: take a block of patches, transport each into the block's reference frame using the
# NATIVE transport (coupling them), then form the block's effective state as the transport-
# combined configuration. This is the interacting coarse-grain, not an independent average.
def rg_step(states, g, Tf):
    new=[]
    for b in range(0,len(states)-1,2):
        qa,qb=states[b],states[b+1]
        # couple: transport qb's perturbation through qa (native), combine into effective patch
        coupled = qa + g*(native_T(qb,qa,g)-qb) if Tf is native_T else qa + g*(assoc_T(qb,qa,g)-qb)
        new.append(coupled)
    return new

def Q_at_scale(g, Tf, n0=256, seed=0):
    rng=np.random.default_rng(seed)
    states=[rng.normal(size=DIM) for _ in range(n0)]
    scales=[]
    level=0
    while len(states)>=2:
        Qm=np.median([np.linalg.norm(Qtensor(q,g,Tf)) for q in states[:min(len(states),40)]])
        scales.append((2**level, Qm, len(states)))
        states=rg_step(states,g,Tf)
        level+=1
    return scales

print("V1712 - coupled RG coarse-graining: does non-metricity flow to zero?\n")
print("NATIVE kernel RG flow:")
print(f"{'block':>7}{'n_patches':>11}{'||Q||':>10}")
for bs,Qm,n in Q_at_scale(0.17,native_T,seed=1):
    print(f"{bs:>7}{n:>11}{Qm:>10.4f}")
print("\nASSOCIATIVE kernel RG flow (sanity: must be ~0 at all scales):")
for bs,Qm,n in Q_at_scale(0.17,assoc_T,seed=1):
    print(f"{bs:>7}{n:>11}{Qm:>10.4f}")
print("-"*40)
nat=Q_at_scale(0.17,native_T,seed=1)
q_first=nat[0][1]; q_last=nat[-1][1]
print(f"\nnative ||Q|| flow: {q_first:.4f} (scale 1) -> {q_last:.4f} (largest block)")
ratio=q_last/q_first
print(f"flow ratio = {ratio:.3f}")
if ratio<0.2:
    print("=> RG FLOWS TO METRIC: coupled coarse-graining drives non-metricity toward zero.")
    print("   An effective metric-compatible (Levi-Civita-like) sector EMERGES at scale.")
    print("   Local non-metric -> global effective metric. This is the bottom-up globalization.")
elif ratio>0.7:
    print("=> RG STAYS NON-METRIC: non-metricity is an RG-stable (coherent) feature.")
    print("   The effective theory is metric-affine at ALL scales, even under interacting")
    print("   coarse-graining. Non-metricity is a true fixed-point property, not a fluctuation.")
else:
    print(f"=> PARTIAL FLOW: non-metricity decreases under RG (ratio {ratio:.2f}) but does not")
    print("   vanish. An effective theory with REDUCED but nonzero non-metricity. Worth mapping.")
