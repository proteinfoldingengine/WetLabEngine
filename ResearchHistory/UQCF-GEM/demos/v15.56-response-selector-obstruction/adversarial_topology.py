"""v15.56 Task 25: adversarial topology-response discrimination.

Deterministically enumerate connected simple graphs on 6 vertices. Group by
degree sequence and Laplacian spectrum, reject isomorphic duplicates using an
exact permutation test, then compare localized-source response orbits. Response
distance is minimized over all source-preserving vertex permutations, so a
positive separation cannot be a labeling artifact.
"""
import itertools, numpy as np
N=6
ALL_EDGES=list(itertools.combinations(range(N),2))

def lap(edges):
 L=np.zeros((N,N))
 for i,j in edges: L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
 return L
def connected(edges):
 adj=[set() for _ in range(N)]
 for i,j in edges: adj[i].add(j);adj[j].add(i)
 seen={0}; stack=[0]
 while stack:
  for v in adj[stack.pop()]:
   if v not in seen: seen.add(v);stack.append(v)
 return len(seen)==N
def canon(edges):
 A=np.zeros((N,N),int)
 for i,j in edges:A[i,j]=A[j,i]=1
 best=None
 for p in itertools.permutations(range(N)):
  s=''.join(str(A[p[i],p[j]]) for i in range(N) for j in range(i+1,N))
  if best is None or s<best:best=s
 return best
def response(edges,source=0):
 L=lap(edges); J=np.zeros(N);J[source]=1;J-=J.mean()
 p=np.linalg.pinv(L,rcond=1e-13)@J;p-=p.mean();return p/np.linalg.norm(p)
def orbit_sep(a,b):
 pa=response(a); pb=response(b); best=1e9
 for tail in itertools.permutations(range(1,N)):
  p=(0,)+tail; best=min(best,np.linalg.norm(pa-pb[list(p)]))
 return best
def run():
 reps={}; deg={}; spec={}
 # trees suffice for degree-matched search; all connected graphs for cospectral
 for comb in itertools.combinations(ALL_EDGES,N-1):
  if not connected(comb):continue
  c=canon(comb)
  if c in reps:continue
  reps[c]=comb
  d=tuple(sorted([int(x) for x in np.diag(lap(comb))]))
  deg.setdefault(d,[]).append(comb)
 degree_pairs=[]
 for g in deg.values():
  if len(g)>1: degree_pairs.append((g[0],g[1]))
 # Known Laplacian-cospectral search across connected 6-node graphs.
 reps2={}
 for mask in range(1,1<<len(ALL_EDGES)):
  if mask.bit_count()<N-1:continue
  e=tuple(ALL_EDGES[i] for i in range(len(ALL_EDGES)) if mask>>i&1)
  if not connected(e):continue
  c=canon(e)
  if c in reps2:continue
  reps2[c]=e
  key=tuple(np.round(np.linalg.eigvalsh(lap(e)),9))
  spec.setdefault(key,[]).append(e)
 cos_pairs=[]
 for g in spec.values():
  if len(g)>1:cos_pairs.append((g[0],g[1]))
 ds=[orbit_sep(a,b) for a,b in degree_pairs]
 cs=[orbit_sep(a,b) for a,b in cos_pairs]
 # exact relabel null
 e=next(iter(reps.values())); p=(0,2,1,3,5,4)
 er=tuple(sorted((min(p[i],p[j]),max(p[i],p[j])) for i,j in e))
 return {"degree_matched_pair_count":len(ds),"cospectral_pair_count":len(cs),
 "min_degree_matched_response_separation":float(min(ds)) if ds else 0.,
 "min_cospectral_response_separation":float(min(cs)) if cs else 0.,
 "max_isomorphic_relabel_separation":float(orbit_sep(e,er))}
