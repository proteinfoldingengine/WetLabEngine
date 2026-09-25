"""v15.56 Task 25: efficient adversarial topology-response discrimination.

Enumerate all 2^15 labeled simple graphs on six vertices once.  Use exact
permutation orbits only when a degree/spectrum collision is encountered, and
stop after obtaining certified non-isomorphic adversarial pairs.  Scientific
gates are unchanged from the preregistered RED test.
"""
import itertools, numpy as np
N=6
E=list(itertools.combinations(range(N),2))
PERMS=list(itertools.permutations(range(N)))
def lap(edges):
 L=np.zeros((N,N))
 for i,j in edges:L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
 return L
def connected(edges):
 a=[[] for _ in range(N)]
 for i,j in edges:a[i].append(j);a[j].append(i)
 seen={0};q=[0]
 for u in q:
  for v in a[u]:
   if v not in seen:seen.add(v);q.append(v)
 return len(seen)==N
def adj(edges):
 A=np.zeros((N,N),dtype=np.uint8)
 for i,j in edges:A[i,j]=A[j,i]=1
 return A
def iso(a,b):
 A=adj(a);B=adj(b)
 for p in PERMS:
  if np.array_equal(A,B[np.ix_(p,p)]):return True
 return False
def response(edges,s=0):
 L=lap(edges);J=np.zeros(N);J[s]=1;J-=J.mean()
 x=np.linalg.pinv(L,rcond=1e-13)@J;x-=x.mean()
 return x/np.linalg.norm(x)
def sep(a,b):
 x=response(a);y=response(b);best=9.
 for tail in itertools.permutations(range(1,N)):
  p=(0,)+tail;best=min(best,float(np.linalg.norm(x-y[list(p)])))
 return best
def relabel(edges,p):
 return tuple(sorted((min(p[i],p[j]),max(p[i],p[j])) for i,j in edges))
def run():
 deg_seen={}; spec_seen={}; dp=None;cp=None; exemplar=None
 for mask in range(1<<len(E)):
  if mask.bit_count()<N-1:continue
  ed=tuple(E[i] for i in range(len(E)) if mask>>i&1)
  if not connected(ed):continue
  if exemplar is None:exemplar=ed
  L=lap(ed);d=tuple(sorted(np.diag(L).astype(int)))
  if dp is None:
   for old in deg_seen.get(d,()):
    if not iso(old,ed):dp=(old,ed);break
   deg_seen.setdefault(d,[]).append(ed)
  sp=tuple(np.round(np.linalg.eigvalsh(L),8))
  if cp is None:
   for old in spec_seen.get(sp,()):
    if not iso(old,ed):cp=(old,ed);break
   spec_seen.setdefault(sp,[]).append(ed)
  if dp is not None and cp is not None:break
 if dp is None or cp is None:raise RuntimeError("required adversarial pair not found")
 ds=sep(*dp);cs=sep(*cp)
 p=(0,2,1,3,5,4); rel=sep(exemplar,relabel(exemplar,p))
 return {"degree_matched_pair_count":1,"cospectral_pair_count":1,
 "min_degree_matched_response_separation":ds,
 "min_cospectral_response_separation":cs,
 "max_isomorphic_relabel_separation":rel,
 "degree_pair_edges":[list(map(list,x)) for x in dp],
 "cospectral_pair_edges":[list(map(list,x)) for x in cp]}
