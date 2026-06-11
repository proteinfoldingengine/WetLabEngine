# RUNG 1 (real) - do charts with their OWN local states induce metrics that AGREE on overlaps?
# This is the non-trivial consistency: g_i from native_jacobian(q_i), g_j from native_jacobian(q_j).
# On overlap, the transition map T_ij must carry g_i to g_j:  g_j =?= T_ij^{-T} g_i T_ij^{-1}.
# The mismatch is the real inconsistency. Null: random q-states with random transitions.
import numpy as np
def roll(v): return np.roll(v,1)
def orth(rng,d):
    M=rng.normal(size=(d,d)); Q,R=np.linalg.qr(M); s=np.sign(np.diag(R)); s[s==0]=1; return Q*s
def native_jacobian(q,g=0.17):
    n=len(q); J=np.eye(n)
    for a in range(n):
        e=np.zeros(n); e[a]=1.0
        J[:,a]=e+g*(roll(e)*q - e*roll(q))
    return J
def metric(q): J=native_jacobian(q); return 0.5*(J+J.T)

DIM=24; NCH=6
def consistency(seed, atlas_coupled=True):
    rng=np.random.default_rng(seed)
    frames=[orth(rng,DIM) for _ in range(NCH)]
    if atlas_coupled:
        # atlas: chart states are RELATED by the transitions (same underlying geometry, re-expressed)
        q0=rng.normal(size=DIM)
        qs=[frames[i]@q0 for i in range(NCH)]      # each chart sees the SAME q0 in its own frame
    else:
        qs=[rng.normal(size=DIM) for _ in range(NCH)]   # null: unrelated states per chart
    errs=[]
    for i in range(NCH):
        for j in range(i+1,NCH):
            gi=metric(qs[i]); gj=metric(qs[j])
            Tij=frames[j].T@frames[i]               # transition i->j
            Tinv=np.linalg.inv(Tij)
            gi_in_j = Tinv.T @ gi @ Tinv            # carry g_i into chart j
            errs.append(np.linalg.norm(gi_in_j-gj)/(np.linalg.norm(gj)+1e-12))
    return float(np.mean(errs))

atl=[consistency(s,True) for s in range(40)]
nul=[consistency(s,False) for s in range(40)]
print("RUNG 1 (real) - cross-chart metric consistency with LOCAL chart states\n")
print(f"atlas-coupled charts (same geometry re-expressed): mismatch = {np.mean(atl):.3e} +/- {np.std(atl):.0e}")
print(f"null (unrelated local states per chart):           mismatch = {np.mean(nul):.3e} +/- {np.std(nul):.0e}")
print()
print(f"ratio null/atlas = {np.mean(nul)/(np.mean(atl)+1e-18):.1f}")
print("-"*55)
if np.mean(atl)<1e-6 and np.mean(nul)>1e-3:
    print("RUNG 1 PASS (non-trivially): atlas-coupled charts induce a CONSISTENT single metric")
    print("  (mismatch ~0), while unrelated charts do NOT (large mismatch). The atlas structure")
    print("  specifically carries one coherent Riemannian metric. Real foundation. -> Rung 2.")
elif np.mean(atl)<1e-6 and np.mean(nul)<1e-3:
    print("PASS BUT TRIVIAL: even unrelated charts agree -> consistency is automatic, not atlas-specific.")
else:
    print(f"PARTIAL/FAIL: atlas mismatch {np.mean(atl):.2e} not ~0; the metric is not globally coherent.")
    print("  Characterize: the model has LOCAL metrics that do not glue into one global metric.")
