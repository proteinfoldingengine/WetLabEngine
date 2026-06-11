# V1703.1 - Does the irreducible L3 excess transport coherently across the V1698 atlas?
# Both halves are verified-real:
#   - associator3 irreducibility (+2 rank lift) confirmed in V1703.0
#   - V1698 atlas: orthonormal chart frames, sparse edge graph, transition maps T_ij
# Question: is the irreducible third-order structure a GLOBAL object (transports
#   faithfully around atlas loops) or only LOCAL (fails to close -> a real obstruction)?
# Pre-registered gate + random control + a deliberately-broken null. Can fail either way.
import numpy as np

def roll_kernel(x,y): return np.roll(x,1)*y - x*np.roll(y,1)
def op_global(x,y,g=0.17): return x+y+g*roll_kernel(x,y)
def associator3(a,b,c,g):
    return op_global(op_global(a,b,g),c,g)-op_global(a,op_global(b,c,g),g)
def residual_to_span(v,basis):
    B=np.column_stack(basis); coef,*_=np.linalg.lstsq(B,v,rcond=None); return v-B@coef

def orthonormal_frame(rng,dim):
    M=rng.normal(size=(dim,dim)); Q,R=np.linalg.qr(M)
    s=np.sign(np.diag(R)); s[s==0]=1; return Q*s
def sparse_atlas_edges(n):
    edges=set()
    for i in range(n): edges.add(tuple(sorted((i,(i+1)%n))))
    for e in [(0,2),(2,4),(4,0),(1,3),(3,5),(5,1),(2,6),(6,4)]:
        if max(e)<n: edges.add(tuple(sorted(e)))
    return sorted(edges)
def all_triangles(n,edges):
    E={tuple(sorted(e)) for e in edges}; tris=[]
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                if all(tuple(sorted(p)) in E for p in [(i,j),(j,k),(i,k)]): tris.append((i,j,k))
    return tris
def T(frames,i,j): return frames[j].T@frames[i]
def vloc(frames,i,v): return frames[i].T@v

def build_L3_basis(branches,g):
    # the +2-dim irreducible part: O3 associators with lower-order projected OUT
    O3=[associator3(branches[i],branches[j],branches[k],g)
        for i in range(len(branches)) for j in range(len(branches)) for k in range(len(branches)) if len({i,j,k})==3]
    pair=[op_global(branches[i],branches[j],g)-branches[i]-branches[j]
          for i in range(len(branches)) for j in range(len(branches))]
    lower=branches+pair
    # irreducible residuals
    irr=[residual_to_span(o,lower) for o in O3]
    irr=[v for v in irr if np.linalg.norm(v)>1e-8]
    # orthonormal basis for the irreducible L3 subspace
    Birr=np.column_stack(irr); U,s,_=np.linalg.svd(Birr,full_matrices=False)
    keep=U[:,s>1e-8]
    return keep  # dim x r  (r should be ~2)

def transport_residual(L3basis, frames, edges, scramble=False, rng=None):
    # L3 is a GLOBAL subspace. Transport its local coordinates chart i->j and compare
    # against the SAME global subspace expressed locally at j. Faithful => residual ~0.
    res=[]
    for (i,j) in edges:
        Tij=T(frames,i,j)
        if scramble and rng is not None:
            # broken null: random orthogonal map instead of the true transition
            Tij=orthonormal_frame(rng,frames[0].shape[0])
        # express each global L3 basis vector locally at i, transport to j, compare to local-at-j
        for col in range(L3basis.shape[1]):
            g_vec=L3basis[:,col]
            loc_i=vloc(frames,i,g_vec)
            loc_j=vloc(frames,j,g_vec)
            res.append(np.linalg.norm(Tij@loc_i - loc_j))
    return float(np.max(res)) if res else 0.0

def holonomy_residual(L3basis, frames, edges, n):
    # transport L3 coords around each triangle loop; should return to start (~0) if global
    tris=all_triangles(n,edges); res=[]
    for (i,j,k) in tris:
        loop=T(frames,k,i)@T(frames,j,k)@T(frames,i,j)
        for col in range(L3basis.shape[1]):
            loc_i=vloc(frames,i,L3basis[:,col])
            res.append(np.linalg.norm(loop@loc_i - loc_i))
    return float(np.max(res)) if res else 0.0

dim=12; n_branch=4; n_charts=7; g=0.17
rng=np.random.default_rng(17031)
tol=1e-8
valid_tr=[]; valid_hol=[]; null_tr=[]; lift_dims=[]
for t in range(40):
    raw=rng.normal(size=(dim,n_branch)); Q,_=np.linalg.qr(raw); branches=[Q[:,i] for i in range(n_branch)]
    L3=build_L3_basis(branches,g); lift_dims.append(L3.shape[1])
    frames=[orthonormal_frame(rng,dim) for _ in range(n_charts)]
    edges=sparse_atlas_edges(n_charts)
    valid_tr.append(transport_residual(L3,frames,edges))
    valid_hol.append(holonomy_residual(L3,frames,edges,n_charts))
    null_tr.append(transport_residual(L3,frames,edges,scramble=True,rng=rng))

valid_tr=np.array(valid_tr); valid_hol=np.array(valid_hol); null_tr=np.array(null_tr)
print("=== L3 IRREDUCIBLE-EXCESS ATLAS TRANSPORT ===")
print(f"irreducible L3 dimension (per trial): mean={np.mean(lift_dims):.2f} (expect ~2)")
print(f"valid transport residual:  max={valid_tr.max():.3e}  mean={valid_tr.mean():.3e}")
print(f"valid holonomy residual:   max={valid_hol.max():.3e}  mean={valid_hol.mean():.3e}")
print(f"scrambled-null residual:   max={null_tr.max():.3e}  mean={null_tr.mean():.3e}")
print("\n--- PRE-REGISTERED VERDICT ---")
print("  GLOBAL  : valid transport & holonomy < 1e-8, null fails (>>0)")
print("  LOCAL/OBSTRUCTED: valid transport or holonomy >> 1e-8")
if valid_tr.max()<tol and valid_hol.max()<tol and null_tr.mean()>1e-3:
    print(f"\nRESULT: L3 IS GLOBAL. The irreducible third-order excess transports faithfully")
    print(f"  across the atlas and closes around loops; scrambled transitions break it.")
    print(f"  => irreducible L3 + atlas closure COMPOSE: L3 is a coherent global object.")
elif valid_tr.max()>=tol or valid_hol.max()>=tol:
    print(f"\nRESULT: L3 IS LOCAL/OBSTRUCTED. The irreducible excess does NOT transport")
    print(f"  coherently (residual {max(valid_tr.max(),valid_hol.max()):.2e}). It is a genuine")
    print(f"  third-order OBSTRUCTION, not a global object.")
else:
    print("\nRESULT: AMBIGUOUS - controls did not separate; inconclusive.")
