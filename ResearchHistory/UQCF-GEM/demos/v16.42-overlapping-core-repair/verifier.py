"""Independent domain/normal forms, complete inherited graph verifier, path checks."""
from pathlib import Path
import importlib.util
from itertools import combinations,permutations,product
from math import factorial
s=importlib.util.spec_from_file_location('v41_verifier',Path(__file__).resolve().parent.parent/'v16.41-unit-barrier-dichotomy/verifier.py');base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
require=base.require
DOMAIN=((0,3),(0,4),(0,5),(1,3),(1,4),(2,3))
def expected_parents(d,m):return [-1]+list(range(d))+[d]*m+list(reversed(range(d)))
def exact_identities(d,m):
 p=expected_parents(d,m);k=d+2;out=set()
 for sides in permutations(range(k),d):
  a,b=sorted(set(range(k))-set(sides))
  for word in product((1,2,3),repeat=m):
   if 1 not in word or 2 not in word:continue
   supports=[0]*len(p)
   for v,value in enumerate(word,d+1):supports[v]=((1<<a) if value&1 else 0)|((1<<b) if value&2 else 0)
   for v,j in zip(range(d+m+1,len(p)),sides):supports[v]=1<<j
   for v in range(len(p)-1,0,-1):supports[p[v]]|=supports[v]
   out.add(tuple(sum(1<<v for v,s in enumerate(supports) if s>>j&1) for j in range(k)))
 return out
def canonical(p,state,d,m):
 labels=[j for j,mask in enumerate(state) if mask>>d&1];require(len(labels)==2,'core palette saturation')
 a,b=labels;leaves=list(range(d+1,d+m+1));out=list(state)
 for v in leaves:
  out[a]&=~(1<<v);out[b]&=~(1<<v)
 for v in [leaves[0]]+leaves[2:]:out[a]|=1<<v
 for v in leaves[1:]:out[b]|=1<<v
 return tuple(out)
def path_valid(path,x,y,states,p,q,bound):
 if not isinstance(path,list) or not path or path[0]!=x or path[-1]!=y:return False
 if any(type(i)is not int or not 0<=i<len(states) for i in path):return False
 k=len(states[0]);children=[[v for v in range(1,len(p)) if p[v]==u] for u in range(len(p))]
 for i in path:
  state=states[i];cost=0
  for u,ch in enumerate(children):
   if not ch:continue
   hit=next(r for r in range(1,k+1) if any(all(any(state[j]>>v&1 for j in subset) for v in ch) for subset in combinations(range(k),r)))
   cost+=abs(hit-q[u])
  if cost>bound:return False
 return all(sum((a^b).bit_count() for a,b in zip(states[i],states[j]))==1 for i,j in zip(path,path[1:]))
def outcome(nonunit,failures):return 'NONUNIT_WITNESS' if nonunit else ('CONSTRUCTION_REFUTED' if failures else 'FAMILY_THEOREM_VALIDATED')
def verify(doc,domain=DOMAIN):
 require(set(doc)=={'schema','domain','entries'} and doc['schema']==1,'document membership')
 require(doc['domain']==[list(x) for x in domain] and [(e['d'],e['m']) for e in doc['entries']]==list(domain),'complete frozen family')
 results=[];failures=[]
 for e,(d,m) in zip(doc['entries'],domain):
  require(set(e)=={'d','m','graph','normalizations','constructions'},'entry membership');require(d>=0 and m>=3,'theorem domain')
  g=e['graph'];p=expected_parents(d,m);require(g['parents']==p,'canonical family identity');q=[2]*(d+1)+[0]*(d+m)
  counts=base.verify_graph(g,d+2,q);rec=g['profiles'][0];states=g['states'];index={tuple(s):i for i,s in enumerate(states)}
  target=sorted(v for row in rec['zero_components'] for v in row)
  require({tuple(states[i]) for i in target}==exact_identities(d,m),'complete independently derived exact identities')
  require(len(rec['zero_components'])==factorial(d+2)//2,'component formula')
  size=3**m-2*2**m+1;require(all(len(c)==size for c in rec['zero_components']),'fiber size formula')
  signatures=[]
  for comp in rec['zero_components']:
   sigs=set()
   for i in comp:
    st=states[i];sidevalues=[]
    for v in range(d+m+1,len(p)):
     labels=[j for j,mask in enumerate(st) if mask>>v&1];require(len(labels)==1,'side singleton saturation');sidevalues.append(labels[0])
    require(len(set(sidevalues))==d,'disjoint sides');sigs.add(tuple(sidevalues))
    require(canonical(p,st,d,m) in index,'canonical state admitted')
   require(len(sigs)==1,'component side assignment');signatures+=list(sigs)
  require(len(set(signatures))==len(signatures),'complete distinct side assignments')
  require([r['state'] for r in e['normalizations']]==target,'complete normalization identities')
  for r in e['normalizations']:
   require(set(r)=={'state','path'},'normalization membership');i=r['state'];y=index[canonical(p,states[i],d,m)]
   if not path_valid(r['path'],i,y,states,p,q,0):failures.append({'d':d,'m':m,'kind':'normalization','state':i})
  require([r['components'] for r in e['constructions']]==[r['components'] for r in rec['pairs']],'complete construction identities')
  for r,pair in zip(e['constructions'],rec['pairs']):
   require(set(r)=={'components','path'},'construction membership');x,y=pair['endpoints']
   if not path_valid(r['path'],x,y,states,p,q,1):failures.append({'d':d,'m':m,'kind':'exchange','components':r['components']})
  results.append(dict(counts,d=d,m=m,normalizations=len(target),theorem_paths=len(e['constructions'])))
 nonunit=sum(r['nonunit_pairs'] for r in results)
 return {'status':'VERIFIED','outcome':outcome(nonunit,failures),'per_graph':results,'construction_failures':failures,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in results),'theorem_paths':sum(r['theorem_paths'] for r in results),'general_claim':'Reviewed T(d,m) family only; not intrinsic indecomposability','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED'}
