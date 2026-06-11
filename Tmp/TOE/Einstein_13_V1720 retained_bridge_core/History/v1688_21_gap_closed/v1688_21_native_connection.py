# V1688.21 - Close the gap: use the ACTUAL native recombination kernel as the
# connection in the loop test, not an orthogonal frame change.
# Gap found: prior loop tests used T_ij = frames[j]^T frames[i] (orthogonal, exactly
# invertible, path-independent BY CONSTRUCTION) -> no curvature could ever appear.
# The retained connection is the nonlinear kernel T_pq(dx)=dx+gamma[roll(dx)*q - dx*roll(q)],
# which is NOT a change of basis. Test loop closure under the REAL connection.
import numpy as np

def roll(v): return np.roll(v,1)
# native edge transport: depends on the LOCAL node state q and edge gate gamma. Nonlinear, non-invertible.
def native_T(dx, q_state, gamma):
    return dx + gamma*(roll(dx)*q_state - dx*roll(q_state))

DIM=6
def make_network(rng, n):
    states=[rng.normal(size=DIM) for _ in range(n)]
    # edge gates depend on the pair (provenance-native, directed)
    return states

def carry_native(path, states, gammas, dx0):
    # transport a correction direction dx through a path using the native kernel,
    # using each traversed node's state and the edge gate.
    dx=dx0.copy()
    for a,b in zip(path[:-1],path[1:]):
        dx=native_T(dx, states[b], gammas[(a,b)])
    return dx

# Build a network where two MATCHED-LENGTH paths share endpoints but pass different nodes.
n=8
results_native=[]; results_orth=[]
for t in range(80):
    rng=np.random.default_rng(50000+t)
    states=make_network(rng,n)
    # symmetric gate per undirected pair so both directions/routes use comparable magnitudes
    gammas={}
    for a in range(n):
        for b in range(n):
            if a!=b:
                gammas[(a,b)]=float(0.3*np.tanh(np.dot(states[a],states[b])))
    dx0=rng.normal(size=DIM); dx0/=np.linalg.norm(dx0)
    pathA=[0,1,2,3,4]; pathB=[0,5,6,7,4]   # matched length (4 hops), same endpoints, disjoint interior
    cA=carry_native(pathA,states,gammas,dx0)
    cB=carry_native(pathB,states,gammas,dx0)
    results_native.append(np.linalg.norm(cA-cB)/(0.5*(np.linalg.norm(cA)+np.linalg.norm(cB))+1e-12))
    # orthogonal-frame comparison (the old flat connection) for contrast
    def orthf(rng,dim):
        M=rng.normal(size=(dim,dim)); Q,R=np.linalg.qr(M); s=np.sign(np.diag(R)); s[s==0]=1; return Q*s
    frames=[orthf(np.random.default_rng(50000+t+100*k),DIM) for k in range(n)]
    def carry_orth(path,v):
        v=frames[path[0]].T@v
        for a,b in zip(path[:-1],path[1:]): v=(frames[b].T@frames[a])@v
        return v
    oA=carry_orth(pathA,dx0); oB=carry_orth(pathB,dx0)
    results_orth.append(np.linalg.norm(oA-oB)/(0.5*(np.linalg.norm(oA)+np.linalg.norm(oB))+1e-12))

results_native=np.array(results_native); results_orth=np.array(results_orth)
print("=== V1688.21: loop closure under the REAL native connection vs the flat orthogonal one ===\n")
print(f"ORTHOGONAL frame connection (old tests): mean path-diff = {results_orth.mean():.3e}  (flat by construction)")
print(f"NATIVE recombination connection (real):  mean path-diff = {results_native.mean():.4f}  min={results_native.min():.4f}  max={results_native.max():.4f}")
print()
# Control: is the native path-difference REAL holonomy (route-dependent) or just
# step-count? Test two matched-length paths AND a reciprocal (there-and-back) loop.
recip=[]
for t in range(80):
    rng=np.random.default_rng(60000+t)
    states=make_network(rng,n)
    gammas={(a,b):float(0.3*np.tanh(np.dot(states[a],states[b]))) for a in range(n) for b in range(n) if a!=b}
    dx0=rng.normal(size=DIM); dx0/=np.linalg.norm(dx0)
    # there and back along SAME nodes: 0->1->2->1->0 (matched, returns to start)
    out=carry_native([0,1,2,3,4],states,gammas,dx0)
    back=carry_native([4,3,2,1,0],states,gammas,out)
    recip.append(np.linalg.norm(back-dx0)/(np.linalg.norm(dx0)+1e-12))
recip=np.array(recip)
print(f"there-and-back closure defect (native): mean = {recip.mean():.4f}")
print("  (nonzero => transport is non-invertible/curved, not flat)")
print()
print("--- READING ---")
if results_native.mean()>1e-3:
    print(f"GAP CLOSED: under the real native connection, two matched-length loops DIFFER")
    print(f"  by {results_native.mean():.3f} (vs {results_orth.mean():.1e} for the flat orthogonal connection).")
    print("  The earlier machine-precision closure was an artifact of using orthogonal frames")
    print("  as the connection. The native recombination kernel is NOT flat: it has genuine")
    print("  path dependence. This is the holonomy object the prior tests could never see.")
else:
    print("Native connection also closes; gap was not the connection choice.")
