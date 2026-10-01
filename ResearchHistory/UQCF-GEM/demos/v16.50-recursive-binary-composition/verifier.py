"""Independent support-set corpus reconstruction and whole-profile path audit."""
from itertools import product
import json
L=();C=(L,L);F=(C,C);SHAPES={'N':(F,C),'D':(F,F)}
SCOPE='finite full binary trees; higher arity unresolved'
def topology(tree):
 children={};parent={};internal=[]
 def walk(t):
  v=len(children);children[v]=[]
  if t:
   internal.append(v)
   for branch in t:
    c=walk(branch);children[v].append(c);parent[c]=v
  return v
 walk(tree);return children,parent,internal
def model(tree,target,k,permutation='identity',mode='compact'):
 ch,parents,internal=topology(tree)
 if len(target)!=len(internal) or any(type(x)!=int or x not in (1,2) for x in target):raise ValueError('target')
 Q=dict(zip(internal,target));requirements={}
 def requirement(v):
  if not ch[v]:r=1
  else:
   a,b=[requirement(c) for c in ch[v]];r=(a+b if Q[v]==2 else max(a,b))
  requirements[v]=r;return r
 width=requirement(0)
 if type(k)!=int or k<width:raise ValueError('palette width')
 supports={}
 def assign(v,palette):
  supports[v]=set(palette)
  if ch[v]:
   a,b=ch[v];left=palette[:requirements[a]];right=palette[:requirements[b]] if Q[v]==1 else palette[requirements[a]:requirements[a]+requirements[b]]
   assign(a,left);assign(b,right)
 assign(0,list(range(k)))
 endpoint=[sum(1<<v for v,S in supports.items() if j in S) for j in range(k)]
 relabel=lambda j:j if permutation=='identity' else k-1-j if permutation=='reversal' else (j+1)%k
 start={v:{relabel(j) for j in S} for v,S in supports.items()}
 if mode=='overlap_inflated':
  for v in internal:
   if Q[v]==1:
    for c in ch[v]:start[c]=set(start[v])
 raw=[sum(1<<v for v,S in start.items() if j in S) for j in range(k)]
 return width,raw,endpoint
def profile_check(tree,k,raw):
 ch,parents,internal=topology(tree);n=len(ch)
 if not isinstance(raw,list) or len(raw)!=k or any(type(z)!=int or z<0 or z>=1<<n for z in raw):raise ValueError('state representation')
 sets=[{j for j,z in enumerate(raw) if z&(1<<v)} for v in range(n)]
 if sets[0]!=set(range(k)):raise ValueError('root changed')
 if any(not s for s in sets) or any(not sets[v]<=sets[p] for v,p in parents.items()):raise ValueError('state admission')
 # Independently solve the two-support hitting problem via explicit singleton search.
 return [1 if any(j in sets[ch[v][0]] and j in sets[ch[v][1]] for j in range(k)) else 2 for v in internal]
def path_check(tree,k,target,path,start,end):
 if not isinstance(path,list) or not path or path[0]!=start:raise ValueError('path start')
 peaks=[0,0,0]
 for i,raw in enumerate(path):
  now=profile_check(tree,k,raw);defects=[abs(x-y) for x,y in zip(now,target)]
  costs=[sum(defects),max(defects,default=0),sum(bool(x) for x in defects)]
  if costs[0]>1:raise ValueError('total excursion exceeds one')
  peaks=[max(a,b) for a,b in zip(peaks,costs)]
  if i and sum((a^b).bit_count() for a,b in zip(path[i-1],raw))!=1:raise ValueError('nonprimitive move')
 if profile_check(tree,k,path[0])!=target or path[-1]!=end or profile_check(tree,k,path[-1])!=target:raise ValueError('exact canonical endpoint')
 return peaks
def expected_specs():
 rows=[]
 for name in ('N','D'):
  n=5 if name=='N' else 7
  for q in product(range(1,3),repeat=n):
   # Compute width independently on sufficiently large palette before selecting the frozen values.
   M=model(SHAPES[name],list(q),2**n)[0]
   for k in range(M,M+2):
    for permutation in ('identity','reversal','cyclic'):
     for mode in ('compact','overlap_inflated'):rows.append({'tree':name,'q':list(q),'k':k,'permutation':permutation,'mode':mode})
 return rows
def verify(doc):
 if set(doc)!={'schema','scope','cases'} or doc['schema']!=1 or doc['scope']!=SCOPE:raise ValueError('schema/scope')
 rows=doc['cases'];wanted=expected_specs()
 if not isinstance(rows,list) or [r.get('spec') for r in rows]!=wanted:raise ValueError('canonical case identities')
 results=[]
 for index,r in enumerate(rows):
  if set(r)!={'spec','width','start','path'}:raise ValueError('record keys')
  s=r['spec'];tree=SHAPES[s['tree']];M,start,end=model(tree,s['q'],s['k'],s['permutation'],s['mode'])
  if r['width']!=M or r['start']!=start:raise ValueError('width/start')
  peaks=path_check(tree,s['k'],s['q'],r['path'],start,end)
  results.append({'case':index,'steps':len(r['path'])-1,'peaks':peaks})
 return {'status':'VERIFIED','outcome':'RECURSIVE_BINARY_INTERFACE_VALIDATED','cases':len(rows),'total_moves':sum(r['steps'] for r in results),'cases_with_unit_excursion':sum(r['peaks'][0]==1 for r in results),'construction_failures':[],'scope':SCOPE,'nonunit_witness':'NOT_CLAIMED','results':results}
