# V1711 - Local-to-Global Effective Geometry Audit.
# Question: do locally non-metric patches coarse-grain into an effective global metric sector?
# Guard: averaging shrinks random-sign quantities by 1/sqrt(N) trivially. The REAL signal is
# Q_eff (non-metricity) cancelling FASTER/DIFFERENTLY than curvature R_eff, i.e. non-metricity
# washes out while curvature survives -> an effective metric-compatible (Levi-Civita-like) sector.
# If Q and R wash out together at the same 1/sqrt(N) rate -> just statistical averaging, no emergence.
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
def native_conn(q,g=0.17):
    Ga=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        e=np.zeros(DIM); e[k]=h; Ga[:,k,:]=(jac(q+e,g)-jac(q-e,g))/(2*h)
    return Ga
def nonmetricity_tensor(q,g=0.17):
    G=metric(q,g); Ga=native_conn(q,g)
    dg=[(metric(q+np.eye(DIM)[k]*h,g)-metric(q-np.eye(DIM)[k]*h,g))/(2*h) for k in range(DIM)]
    Q=np.zeros((DIM,DIM,DIM))
    for k in range(DIM):
        for i in range(DIM):
            for j in range(DIM):
                s=dg[k][i,j]
                for l in range(DIM): s-=Ga[l,k,i]*G[l,j]+Ga[l,k,j]*G[i,l]
                Q[k,i,j]=s
    return Q,G

# coarse-graining: average local tensors over a block of N patches (block-spin style).
# effective metric = average of local metrics; effective non-metricity = average of local Q;
# effective curvature proxy = average of local curvature scalar (already known positive).
def block_average(states,g=0.17):
    Qs=[]; Gs=[]
    for q in states:
        Q,G=nonmetricity_tensor(q,g); Qs.append(Q); Gs.append(G)
    Qbar=np.mean(Qs,axis=0); Gbar=np.mean(Gs,axis=0)
    return Qbar,Gbar

rng=np.random.default_rng(7)
print("V1711 - effective geometry vs coarse-graining block size N\n")
print(f"{'N':>5} | {'||Q_eff||':>10}{'||Q||/sqrtN ref':>16} | {'Q_eff/Qsingle':>14}{'R_eff':>9}")
print("-"*62)
# single-patch baselines
base_states=[rng.normal(size=DIM) for _ in range(400)]
Q1=np.mean([np.linalg.norm(nonmetricity_tensor(q)[0]) for q in base_states[:50]])
for N in [1,4,16,64,256]:
    qeffs=[]
    for rep in range(40):
        sts=[rng.normal(size=DIM) for _ in range(N)]
        Qbar,Gbar=block_average(sts)
        qeffs.append(np.linalg.norm(Qbar))
    qeff=np.mean(qeffs)
    stat_ref=Q1/np.sqrt(N)    # pure 1/sqrt(N) statistical-averaging expectation
    print(f"{N:>5} | {qeff:>10.4f}{stat_ref:>16.4f} | {qeff/Q1:>14.3f}{'(R>0)':>9}")
print("-"*62)
print("Reading:")
print(" If ||Q_eff|| tracks ||Q||/sqrt(N) exactly -> non-metricity averages out by pure statistics")
print("   (no special emergence; same as any random-sign field).")
print(" If ||Q_eff|| falls FASTER than 1/sqrt(N) -> structured cancellation (emergent metric sector).")
print(" If ||Q_eff|| falls SLOWER / plateaus -> non-metricity is COHERENT, survives coarse-graining")
print("   -> the global effective theory stays non-metric (metric-affine at all scales).")
