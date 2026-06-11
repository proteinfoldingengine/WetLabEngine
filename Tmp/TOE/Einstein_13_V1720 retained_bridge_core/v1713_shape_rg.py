# V1713 - is the SHAPE of the non-metricity (shear/Weyl ratio) also an RG fixed point?
# V1712 showed ||Q|| is RG-invariant (magnitude fixed point). Now test whether the DECOMPOSITION
# - traceless(shear) vs trace(Weyl) fraction - is preserved under coupled coarse-graining.
# If yes: the non-metric geometry is a fixed point in SHAPE too -> a fully scale-invariant
# metric-affine structure (the shear character is intrinsic, not scale-dependent).
import numpy as np
def roll(v): return np.roll(v,1)
def native_T(dx,q,g=0.17): return dx + g*(roll(dx)*q - dx*roll(q))
def jac(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0; J[:,a]=native_T(e,q,g)
    return J
DIM=6; h=1e-4
def metric(q,g=0.17):
    G=0.5*(jac(q,g)+jac(q,g).T); w=np.linalg.eigvalsh(G)
    if w.min()<1e-6: G=G+(1e-6-w.min())*np.eye(len(q))
    return G
def conn(q,g=0.17):
    Ga=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h; Ga[:,k,:]=(jac(q+e,g)-jac(q-e,g))/(2*h)
    return Ga
def Qtensor(q,g=0.17):
    G=metric(q,g); Ga=conn(q,g)
    dg=[(metric(q+np.eye(DIM)[k]*h,g)-metric(q-np.eye(DIM)[k]*h,g))/(2*h) for k in range(DIM)]
    Q=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                s=dg[k][i,j]
                for l in range(DIM): s-=Ga[l,k,i]*G[l,j]+Ga[l,k,j]*G[i,l]
                Q[k,i,j]=s
    return Q,G
def shear_weyl_fracs(q,g=0.17):
    Q,G=Qtensor(q,g); Gi=np.linalg.inv(G)
    W=np.array([np.einsum('ij,ij->',Gi,Q[k])/DIM for k in range(DIM)])
    Qweyl=np.zeros((DIM,DIM,DIM))
    for k in range(DIM): Qweyl[k]=W[k]*G
    Qtl=Q-Qweyl
    nq=np.linalg.norm(Q)+1e-12
    return np.linalg.norm(Qweyl)/nq, np.linalg.norm(Qtl)/nq
def rg_step(states,g=0.17):
    new=[]
    for b in range(0,len(states)-1,2):
        qa,qb=states[b],states[b+1]
        new.append(qa+g*(native_T(qb,qa,g)-qb))
    return new

rng=np.random.default_rng(3)
states=[rng.normal(size=DIM) for _ in range(256)]
print("V1713 - shear/Weyl decomposition under RG flow\n")
print(f"{'block':>7}{'n':>6} | {'Weyl%':>8}{'shear%':>9}{'shear/Weyl':>12}")
print("-"*44)
level=0
ratios=[]
while len(states)>=2:
    sample=states[:min(len(states),40)]
    ws=[];ts=[]
    for q in sample:
        w,t=shear_weyl_fracs(q); ws.append(w); ts.append(t)
    wmean,tmean=np.median(ws),np.median(ts)
    ratios.append(tmean/wmean)
    print(f"{2**level:>7}{len(states):>6} | {wmean*100:>7.0f}%{tmean*100:>8.0f}%{tmean/wmean:>12.2f}")
    states=rg_step(states); level+=1
print("-"*44)
print(f"\nshear/Weyl ratio: {ratios[0]:.2f} (finest) -> {ratios[-1]:.2f} (coarsest)")
spread=np.std(ratios)/np.mean(ratios)
print(f"relative variation across scales = {spread:.2%}")
if spread<0.15:
    print("=> SHAPE IS ALSO RG-INVARIANT: shear/Weyl ratio is preserved under coarse-graining.")
    print("   The non-metric geometry is a fixed point in BOTH magnitude AND shape. The shear")
    print("   character is intrinsic and scale-free - a fully scale-invariant metric-affine")
    print("   structure. The geometry the recombination builds looks the SAME at every scale.")
else:
    print(f"=> SHAPE FLOWS: shear/Weyl ratio varies {spread:.0%} across scales. Magnitude is fixed")
    print("   but the non-metricity's character changes with scale - a running shape.")
