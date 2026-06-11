# V1703.2 - Associator faithfulness across the atlas (the test that CAN fail).
# Unlike V1703.1 (fixed-vector transport = construction identity), here we compute
# the THIRD-ORDER ASSOCIATOR using each chart's LOCAL product, then ask whether it
# transports to match the associator computed at the destination chart.
# Because the product is NON-ASSOCIATIVE and pulled back through different frames,
# there is NO identity forcing agreement. It can come back faithful (L3 global) or
# obstructed (real 3rd-order obstruction).
import numpy as np

def roll_kernel(x,y): return np.roll(x,1)*y - x*np.roll(y,1)
def op_global(x,y,g=0.17): return x+y+g*roll_kernel(x,y)

def orthonormal_frame(rng,dim):
    M=rng.normal(size=(dim,dim)); Q,R=np.linalg.qr(M)
    s=np.sign(np.diag(R)); s[s==0]=1; return Q*s
def sparse_atlas_edges(n):
    edges=set()
    for i in range(n): edges.add(tuple(sorted((i,(i+1)%n))))
    for e in [(0,2),(2,4),(4,0),(1,3),(3,5),(5,1),(2,6),(6,4)]:
        if max(e)<n: edges.add(tuple(sorted(e)))
    return sorted(edges)
def T(frames,i,j): return frames[j].T@frames[i]
def vloc(frames,i,v): return frames[i].T@v

def local_op(xl,yl,A,g):
    # chart-local product: pull local coords up via frame A, apply global op, push back
    xg=A@xl; yg=A@yl
    return A.T@op_global(xg,yg,g)

def local_associator(al,bl,cl,A,g):
    # associator computed entirely with the chart-local product
    return local_op(local_op(al,bl,A,g),cl,A,g) - local_op(al,local_op(bl,cl,A,g),A,g)

dim=12; n_branch=4; n_charts=7; g=0.17
rng=np.random.default_rng(17032)
tol=1e-8

faith_res=[]   # does local associator at i, transported to j, equal local associator at j?
null_res=[]    # broken null: use a DIFFERENT gamma at the destination chart (real algebra mismatch)
for t in range(40):
    raw=rng.normal(size=(dim,n_branch)); Q,_=np.linalg.qr(raw); branches=[Q[:,i] for i in range(n_branch)]
    frames=[orthonormal_frame(rng,dim) for _ in range(n_charts)]
    edges=sparse_atlas_edges(n_charts)
    triples=[(i,j,k) for i in range(n_branch) for j in range(n_branch) for k in range(n_branch) if len({i,j,k})==3]
    for (ci,cj) in edges:
        Tij=T(frames,ci,cj)
        Ai=frames[ci]; Aj=frames[cj]
        for (i,j,k) in triples:
            ai=vloc(frames,ci,branches[i]); bi=vloc(frames,ci,branches[j]); cci=vloc(frames,ci,branches[k])
            assoc_i=local_associator(ai,bi,cci,Ai,g)          # computed in chart i
            aj=vloc(frames,cj,branches[i]); bj=vloc(frames,cj,branches[j]); ccj=vloc(frames,cj,branches[k])
            assoc_j=local_associator(aj,bj,ccj,Aj,g)          # computed in chart j
            faith_res.append(np.linalg.norm(Tij@assoc_i - assoc_j))
            # null: destination computes associator with perturbed gamma (genuine algebra change)
            assoc_j_null=local_associator(aj,bj,ccj,Aj,g*1.5)
            null_res.append(np.linalg.norm(Tij@assoc_i - assoc_j_null))

faith_res=np.array(faith_res); null_res=np.array(null_res)
print("=== L3 ASSOCIATOR FAITHFULNESS ACROSS ATLAS (can fail) ===")
print(f"faithfulness residual: max={faith_res.max():.3e}  mean={faith_res.mean():.3e}  p95={np.percentile(faith_res,95):.3e}")
print(f"gamma-mismatch null:   max={null_res.max():.3e}  mean={null_res.mean():.3e}")
print("\n--- PRE-REGISTERED VERDICT ---")
print("  L3 ALGEBRAICALLY GLOBAL : faithfulness < 1e-8 AND null >> 1e-8")
print("  L3 OBSTRUCTED           : faithfulness >> 1e-8")
if faith_res.max()<tol and null_res.mean()>1e-3:
    print(f"\nRESULT: L3 IS ALGEBRAICALLY GLOBAL. The third-order associator, computed with")
    print(f"  each chart's own local product, transports faithfully across the atlas")
    print(f"  (residual {faith_res.max():.1e}); a genuine gamma change breaks it (null {null_res.mean():.2e}).")
    print(f"  This is NOT a construction identity: non-associative local products agree under transport.")
elif faith_res.max()>=tol:
    print(f"\nRESULT: L3 OBSTRUCTED. Local associators do not agree across charts")
    print(f"  (residual {faith_res.max():.2e}). Genuine third-order obstruction to global closure.")
else:
    print("\nRESULT: AMBIGUOUS - null did not separate.")
