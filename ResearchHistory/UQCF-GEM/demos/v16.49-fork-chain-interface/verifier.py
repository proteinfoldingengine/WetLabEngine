"""Independent fork identity, palette feasibility, endpoint and whole-path audit."""
from itertools import combinations,product
from functools import lru_cache
import graph_verifier as graph
import chain_verifier as chain
require=graph.require
DOMAIN=(2,3)
LEFT=RIGHT=(2,2)
def structure(left,right):
 parents=[-1]
 for d in (left,right):
  offset=len(parents)
  for p in chain.structure(d):parents.append(0 if p==-1 else p+offset)
 return parents
def full_profile(left,right,t):
 require(len(t)==1+len(left)+len(right),'internal target length');q=[0]*len(structure(left,right));q[0]=t[0];off=2+sum(left)
 q[1:1+len(left)]=t[1:1+len(left)];q[off:off+len(right)]=t[1+len(left):];return q
def requirements(left,right,q):
 require(type(q[0]) is int and q[0] in (1,2),'binary parent profile')
 a=chain.requirements(left,q[1:])[0];b=chain.requirements(right,q[2+sum(left):])[0]
 return a,b,max(a,b) if q[0]==1 else a+b
def canonical(left,right,k,q):
 a,b,m=requirements(left,right,q);require(k>=m,'parent palette feasibility');parents=structure(left,right);S=[set() for _ in parents];S[0]=set(range(k));off=2+sum(left)
 palettes=[list(range(a)),list(range(b)) if q[0]==1 else list(range(a,a+b))]
 for d,offset,P in ((left,1,palettes[0]),(right,off,palettes[1])):
  local=chain.canonical(d,len(P),q[offset:]);n=sum(d)+1
  for v in range(n):S[offset+v]={P[j] for j in range(len(P)) if local[j]>>v&1}
 return tuple(sum(1<<v for v,z in enumerate(S) if j in z) for j in range(k))
@lru_cache(None)
def _profile(state,left,right,k):
 parents=structure(left,right);n=len(parents);require(len(state)==k and all(type(x) is int and 0<=x<1<<n for x in state),'raw representation')
 S=[{j for j in range(k) if state[j]>>v&1} for v in range(n)];require(S[0]==set(range(k)) and all(S[v] and S[v]<=S[parents[v]] for v in range(1,n)),'raw admission')
 q=[]
 for v in range(n):
  children=[w for w in range(1,n) if parents[w]==v]
  q.append(next(z for z in range(1,k+1) if any(all(set(H)&S[w] for w in children) for H in combinations(range(k),z))) if children else 0)
 return tuple(q)
def raw_profile(state,left,right,k):return list(_profile(tuple(state),tuple(left),tuple(right),k))
def raw_path_valid(path,left,right,k,q,start,end):
 if not isinstance(path,list) or not path or path[0]!=list(start) or path[-1]!=list(end):return False
 try:
  for s in path:
   z=raw_profile(s,left,right,k)
   if len(z)!=len(q) or sum(abs(a-b) for a,b in zip(z,q))>1:return False
  return all(sum((a^b).bit_count() for a,b in zip(x,y))==1 for x,y in zip(path,path[1:]))
 except (ValueError,TypeError):return False
def corpus_specs():
 rows=[]
 for t in product((1,2),repeat=5):
  q=full_profile(LEFT,RIGHT,t);m=requirements(LEFT,RIGHT,q)[2]
  for k in (m,m+1):
   for perm in ('identity','reversal','cyclic'):rows.append({'target':list(t),'k':k,'permutation':perm})
 return rows
def outcome(nonunit,failures):return 'NONUNIT_WITNESS' if nonunit else 'CONSTRUCTION_REFUTED' if failures else 'FORK_CHAIN_INTERFACE_VALIDATED'
def verify(doc,domain=DOMAIN,specs=None):
 specs=corpus_specs() if specs is None else specs
 require(set(doc)=={'schema','domain','entries','corpus'} and doc['schema']==1,'document membership')
 require(doc['domain']==list(domain) and [e['k'] for e in doc['entries']]==list(domain),'complete fork graph domain')
 rows=[];failures=[];parents=structure(LEFT,RIGHT)
 for e,k in zip(doc['entries'],domain):
  require(set(e)=={'k','graph','normalizations'},'entry membership');g=e['graph']
  require(g['parents']==parents,'canonical fork identity');row=graph.verify_graph(g,k)
  for q in g['attained_profiles']:require(requirements(LEFT,RIGHT,q)[2]<=k,'necessary fork palette bound')
  identities=[(c[0],r['q']) for r in g['profiles'] for c in r['zero_components']]
  require([(r['state'],r['q']) for r in e['normalizations']]==identities,'complete representative identities')
  index={tuple(s):i for i,s in enumerate(g['states'])}
  for r in e['normalizations']:
   require(set(r)=={'state','q','path'},'normalization membership');x=r['state'];q=r['q'];y=index.get(canonical(LEFT,RIGHT,k,q));path=r['path']
   require(y is not None and g['attained_profiles'][g['profile_ids'][y]]==q,'canonical admitted exact endpoint')
   valid=isinstance(path,list) and bool(path) and path[0]==x and path[-1]==y
   valid=valid and all(type(i) is int and 0<=i<len(g['states']) for i in path)
   if valid:
    valid=all(sum(abs(a-b) for a,b in zip(g['attained_profiles'][g['profile_ids'][i]],q))<=1 for i in path)
    valid=valid and all(sum((a^b).bit_count() for a,b in zip(g['states'][i],g['states'][j]))==1 for i,j in zip(path,path[1:]))
   if not valid:failures.append({'k':k,'state':x,'q':q})
  rows.append(dict(row,k=k,normalizations=len(identities),overlap_profiles=sum(r['q'][0]==1 for r in g['profiles']),disjoint_profiles=sum(r['q'][0]==2 for r in g['profiles'])))
 require([r['spec'] for r in doc['corpus']]==specs,'complete directed corpus identities');corpus=[]
 for i,(r,spec) in enumerate(zip(doc['corpus'],specs)):
  require(set(r)=={'spec','palette_requirement','start','path'},'corpus membership');k=spec['k'];q=full_profile(LEFT,RIGHT,spec['target']);m=requirements(LEFT,RIGHT,q)[2]
  require(r['palette_requirement']==m,'directed palette requirement');end=list(canonical(LEFT,RIGHT,k,q));p=spec['permutation']
  start=end[:] if p=='identity' else list(reversed(end)) if p=='reversal' else end[-1:]+end[:-1]
  require(r['start']==start and raw_profile(start,LEFT,RIGHT,k)==q,'directed starting state/profile')
  ok=raw_path_valid(r['path'],LEFT,RIGHT,k,q,start,end)
  if not ok:failures.append({'corpus_case':i,'spec':spec})
  corpus.append({'case':i,'target':spec['target'],'k':k,'permutation':p,'steps':len(r['path'])-1 if isinstance(r['path'],list) else None,'valid':ok})
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,failures),'per_graph':rows,'corpus':corpus,'construction_failures':failures,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'directed_cases':len(corpus),'profiles':sum(r['profiles'] for r in rows),'general_claim':'One binary parent with two internal-chain children admits total L1 excursion<=1 by reviewed interface composition; arbitrary branching is not covered.','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED'}
