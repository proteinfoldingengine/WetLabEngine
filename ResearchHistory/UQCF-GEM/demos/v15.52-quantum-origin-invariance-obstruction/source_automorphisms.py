"""v15.52 Task 2: exhaustive finite source automorphism action."""
from itertools import permutations
def frozen_fixture(contract):
 return {"objects":["o0","o1","o2","o3"],
  "lineage":[(0,1),(2,3)],"dependency":[(0,1),(2,3)],
  "recoverability":[(0,1),(2,3)],
  "composition":[(0,1,1),(2,3,3)],
  "refinement":[((0,1),(2,3))],
  "disjoint_composition":[(0,2),(1,3)]}
def _map_pair(pair,p): return (p[pair[0]],p[pair[1]])
def preserves(contract,f,p):
 for k in ("lineage","dependency","recoverability","disjoint_composition"):
  orig=set(tuple(x) for x in f[k]); mapped=set(_map_pair(x,p) for x in f[k])
  if mapped!=orig:return False
 orig=set(tuple(x) for x in f["composition"]); mapped={(p[a],p[b],p[c]) for a,b,c in orig}
 if mapped!=orig:return False
 # refinement is an unordered pair of ordered paths
 orig={tuple(path) for path in f["refinement"][0]}
 mapped={_map_pair(path,p) for path in f["refinement"][0]}
 return mapped==orig
def bruteforce_preserving_permutations(contract,f):
 return tuple(p for p in permutations(range(len(f["objects"]))) if preserves(contract,f,p))
def enumerate_automorphisms(contract,f): return bruteforce_preserving_permutations(contract,f)
def object_orbits(f,autos):
 unseen=set(range(len(f["objects"]))); out=[]
 while unseen:
  x=min(unseen); orb=sorted({p[x] for p in autos}); out.append(tuple(orb)); unseen-=set(orb)
 return tuple(out)
