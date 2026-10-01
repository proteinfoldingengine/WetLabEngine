"""Independent complete graph identities and directed raw-state path audit."""
from itertools import combinations,product
from functools import lru_cache
import graph_verifier as graph
require=graph.require
DOMAIN=(((2,2,2,2),2),((2,2,2,2),3),((3,2,2,2),2),((2,3,2,2),2),((2,2,3,2),2),((2,2,2,3),2))
def structure(d):
 parents=[-1]
 def descend(i,v):
  if i+1<len(d):
   w=len(parents);parents.append(v);descend(i+1,w);leaves=d[i]-1
  else:leaves=d[i]
  for _ in range(leaves):parents.append(v)
 descend(0,0)
 return parents
def requirements(d,q):
 out=[0]*len(d)
 for i in range(len(d)-1,-1,-1):
  require(type(q[i]) is int and 1<=q[i]<=d[i],'admissible internal profile')
  if i==len(d)-1:out[i]=q[i]
  elif q[i]==d[i]:out[i]=d[i]-1+out[i+1]
  else:out[i]=max(q[i],out[i+1])
 return out
def canonical(d,k,q):
 parents=structure(d);m=requirements(d,q);require(k>=m[0],'palette feasibility');S=[set() for _ in parents];S[0]=set(range(k))
 for i in range(len(d)):
  P=sorted(S[i]);leaves=[v for v in range(1,len(parents)) if parents[v]==i and v>=len(d)]
  if i+1==len(d):colors=P[:q[i]]
  elif q[i]==d[i]:colors=P[:d[i]-1];S[i+1]=set(P[d[i]-1:d[i]-1+m[i+1]])
  else:colors=P[:q[i]];S[i+1]=set(P[:m[i+1]])
  for j,v in enumerate(leaves):S[v]={colors[j] if j<len(colors) else colors[0]}
 return tuple(sum(1<<v for v,A in enumerate(S) if j in A) for j in range(k))
@lru_cache(None)
def _raw_profile(state,d,k):
 parents=structure(d);n=len(parents)
 require(len(state)==k and all(type(x) is int and 0<=x<1<<n for x in state),'raw state representation')
 S=[{j for j in range(k) if state[j]>>v&1} for v in range(n)]
 require(S[0]==set(range(k)) and all(S[v] and S[v]<=S[parents[v]] for v in range(1,n)),'raw state admission')
 q=[]
 for v in range(n):
  children=[w for w in range(1,n) if parents[w]==v]
  q.append(next(z for z in range(1,k+1) if any(all(set(H)&S[w] for w in children) for H in combinations(range(k),z))) if children else 0)
 return tuple(q)
def raw_profile(state,d,k):return list(_raw_profile(tuple(state),tuple(d),k))
def raw_path_valid(path,d,k,q,start,end):
 if not isinstance(path,list) or not path:return False
 if path[0]!=list(start) or path[-1]!=list(end):return False
 try:
  for s in path:
   z=raw_profile(s,d,k)
   if len(q)!=len(z) or sum(abs(a-b) for a,b in zip(z,q))>1:return False
  return all(sum((a^b).bit_count() for a,b in zip(x,y))==1 for x,y in zip(path,path[1:]))
 except (ValueError,TypeError):return False
def corpus_specs():
 rows=[]
 families=[((2,2,2,2),list(product((1,2),repeat=4))),((3,2,3,2),list(product((1,2),repeat=4))),((2,)*8,[(1,)*8,(2,)*8,(1,2)*4])]
 for d,targets in families:
  for q in targets:
   bound=requirements(d,q)[0]
   for k in (bound,bound+1):
    for perm in ('identity','reversal','cyclic'):rows.append({'degrees':list(d),'q':list(q),'k':k,'permutation':perm})
 return rows
def outcome(nonunit,failures):return 'NONUNIT_WITNESS' if nonunit else 'CONSTRUCTION_REFUTED' if failures else 'CHAIN_INDUCTION_VALIDATED'
def verify(doc,domain=DOMAIN,specs=None):
 specs=corpus_specs() if specs is None else specs
 require(set(doc)=={'schema','domain','entries','corpus'} and doc['schema']==1,'document membership')
 require(doc['domain']==[{'degrees':list(d),'k':k} for d,k in domain],'complete graph domain')
 require([(e['degrees'],e['k']) for e in doc['entries']]==[(list(d),k) for d,k in domain],'complete graph identities')
 rows=[];failures=[]
 for e,(d,k) in zip(doc['entries'],domain):
  require(set(e)=={'degrees','k','graph','normalizations'},'entry membership');g=e['graph'];parents=structure(d)
  children=[[w for w in range(1,len(parents)) if parents[w]==v] for v in range(len(parents))]
  def code(v):return '('+''.join(sorted(code(w) for w in children[v]))+')'
  require(g['code']==code(0) and g['parents']==parents,'canonical chain identity')
  row=graph.verify_graph(g,k)
  for q in g['attained_profiles']:require(requirements(d,q)[0]<=k,'necessary compact-palette bound')
  identities=[(c[0],r['q']) for r in g['profiles'] for c in r['zero_components']]
  require([(r['state'],r['q']) for r in e['normalizations']]==identities,'complete representative identities')
  index={tuple(s):i for i,s in enumerate(g['states'])}
  for r in e['normalizations']:
   require(set(r)=={'state','q','path'},'normalization membership');x=r['state'];q=r['q'];y=index.get(canonical(d,k,q));path=r['path']
   require(y is not None and g['attained_profiles'][g['profile_ids'][y]]==q,'canonical admitted exact endpoint')
   valid=isinstance(path,list) and bool(path) and path[0]==x and path[-1]==y
   valid=valid and all(type(i) is int and 0<=i<len(g['states']) for i in path)
   if valid:
    valid=all(sum(abs(a-b) for a,b in zip(g['attained_profiles'][g['profile_ids'][i]],q))<=1 for i in path)
    valid=valid and all(sum((a^b).bit_count() for a,b in zip(g['states'][i],g['states'][j]))==1 for i,j in zip(path,path[1:]))
   if not valid:failures.append({'degrees':list(d),'k':k,'state':x,'q':q})
  rows.append(dict(row,degrees=list(d),k=k,normalizations=len(identities)))
 require([r['spec'] for r in doc['corpus']]==specs,'complete directed corpus identities')
 corpus_rows=[]
 for i,(r,spec) in enumerate(zip(doc['corpus'],specs)):
  require(set(r)=={'spec','palette_requirement','start','path'},'corpus membership');d=spec['degrees'];k=spec['k'];qi=spec['q'];q=qi+[0]*(sum(d)+1-len(d));m=requirements(d,qi)[0]
  require(r['palette_requirement']==m,'directed palette requirement');end=list(canonical(d,k,q));p=spec['permutation']
  start=end[:] if p=='identity' else list(reversed(end)) if p=='reversal' else end[-1:]+end[:-1]
  require(r['start']==start and raw_profile(start,d,k)==q,'directed starting state/profile')
  ok=raw_path_valid(r['path'],d,k,q,start,end)
  if not ok:failures.append({'corpus_case':i,'spec':spec})
  corpus_rows.append({'case':i,'degrees':d,'q':qi,'k':k,'permutation':p,'steps':len(r['path'])-1 if isinstance(r['path'],list) else None,'valid':ok})
 nonunit=sum(r['nonunit_pairs'] for r in rows)
 return {'status':'VERIFIED','outcome':outcome(nonunit,failures),'per_graph':rows,'corpus':corpus_rows,'construction_failures':failures,'nonunit_pairs':nonunit,'normalizations':sum(r['normalizations'] for r in rows),'directed_cases':len(corpus_rows),'profiles':sum(r['profiles'] for r in rows),'general_claim':'All finite internal chains admit total L1 excursion<=1 by independently reviewed compact-palette induction; arbitrary internal branching is not covered.','universal_unit_barrier':'REFUTED' if nonunit else 'UNRESOLVED'}
