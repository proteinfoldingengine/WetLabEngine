"""Independent v16.29 verifier: Pruefer trees, direct subfamilies and full raw states."""
from collections import Counter
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import hashlib,json,lzma
HERE=Path(__file__).resolve().parent
ORIGIN='v16.29-common-genesis'
PARENT_SHA='daedbb1ac332aa8c8058700b9f3a6b0eaa2a9d0a3341918b42a6b0495ba94df4'
PARENT=HERE.parent/'v16.28-diamond-attribution-closure/evidence/FULL_CERTIFICATES.json.xz'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def equal(a,b,msg):
 need(json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':')),msg)

def tree(raw):
 need(isinstance(raw,(list,tuple)) and raw,'empty tree');p=tuple(raw)
 need(all(type(v)is int for v in p) and p[0]==-1,'parent type/root')
 need(all(0<=v<len(p) for v in p[1:]),'outside tree')
 for v in range(1,len(p)):
  visited=set()
  while v:
   need(v not in visited,'cyclic parent');visited.add(v);v=p[v]
 return p

def family(p,raw):
 need(isinstance(raw,(list,tuple)) and raw,'empty family');out=[]
 for y in raw:
  need(isinstance(y,(list,tuple)) and y and all(type(v)is int and 0<=v<len(p) for v in y),'view type')
  need(len(y)==len(set(y)) and 0 in y and all(v==0 or p[v] in y for v in y),'non-prefix/duplicate view');out.append(tuple(y))
 return tuple(out)

def delete(p,ys,event):
 need(isinstance(event,(list,tuple)) and len(event)==2 and all(type(v)is int for v in event),'event type')
 i,c=event;need(0<=i<len(ys) and 0<c<len(p) and c in ys[i],'event not retained')
 need(all(w==0 or p[w]!=c for w in ys[i]),'ancestor before descendant')
 nxt=tuple(tuple(v for v in y if not (j==i and v==c)) for j,y in enumerate(ys))
 need(set().union(*map(set,nxt))==set().union(*map(set,ys)),'union loss')
 return nxt

@lru_cache(None)
def minima(p,ys):
 U=frozenset().union(*map(frozenset,ys));out=[]
 for v in range(len(p)):
  kids=frozenset(w for w in U if w and p[w]==v)
  if not kids:out.append(0);continue
  for n in range(1,len(ys)+1):
   if any(kids<=frozenset().union(*(frozenset(ys[j]) for j in S)) for S in combinations(range(len(ys)),n)):
    out.append(n);break
  else:raise ValueError('uncovered children')
 return tuple(out)

def verify_case(c):
 required={'version','genesis','parents','before','events','states','profiles','heights','parent_pair','local_mixed','global_mixed','background','prediction','mechanism'}
 need(isinstance(c,dict) and required<=c.keys(),'missing certificate field')
 need(c['version']=='16.29' and c['genesis']==ORIGIN,'foreign origin')
 p=tree(c['parents']);ys=family(p,c['before']);ev=c['events']
 need(isinstance(ev,(list,tuple)) and len(ev)==2,'event pair');e,f=ev
 need(e!=f,'duplicate event')
 ye=delete(p,ys,e);yf=delete(p,ys,f);yef=delete(p,ye,f);need(yef==delete(p,yf,e),'actual square mismatch')
 states=[ys,ye,yf,yef]
 need(isinstance(c['states'],list) and len(c['states'])==4,'four stored states')
 for got,want in zip(c['states'],states):equal(family(p,got),want,'false stored state')
 q=[minima(p,s) for s in states];h=[max((1,)+a) for a in q];pp=[p[e[1]],p[f[1]]]
 for before,after,target in [(0,1,pp[0]),(0,2,pp[1]),(1,3,pp[1]),(2,3,pp[0])]:
  need(all(q[after][v]==q[before][v] for v in range(len(p)) if v!=target),'profile locality violated')
  need(q[after][target]-q[before][target] in (0,1),'local atomic bound')
  need(h[after]-h[before] in (0,1),'global atomic bound')
 local=[q[3][v]-q[1][v]-q[2][v]+q[0][v] for v in range(len(p))];glob=h[3]-h[1]-h[2]+h[0]
 B=max([1]+[q[0][v] for v in range(len(p)) if v not in pp])
 if pp[0]!=pp[1]:
  need(not any(local),'cross-parent local interaction');pred=-(h[1]-h[0])*(h[2]-h[0])
 else:
  a,b,c1,d=[x[pp[0]] for x in q]
  if B<=a:pred=d-b-c1+a
  elif B==a+1:pred=int((b,c1,d)==(a+1,a+1,a+2))
  else:pred=0
 need(glob==pred,'L2/L3 theorem contradiction')
 if glob and any(local):need([x for x in local if x]!=[] and all(x==glob for x in local if x),'transmitted sign contradiction')
 kind=('MAX_ONLY' if not any(local) else 'LOCAL_TRANSMITTED') if glob else ('LOCAL_MASKED' if any(local) else 'ZERO')
 for key,expected in [('profiles',[list(a) for a in q]),('heights',h),('parent_pair',pp),('local_mixed',local),('global_mixed',glob),('background',B),('prediction',pred),('mechanism',kind)]:equal(c[key],expected,'false '+key)
 return Counter({'diamonds':1,kind:1,'global_'+str(glob):1,'same_parent' if pp[0]==pp[1] else 'different_parent':1})

def code(p):
 children={v:[] for v in range(len(p))}
 for w in range(1,len(p)):children[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in children[v]))+')'
 return rec(0)

def shape_codes(bound):
 found={'()'}
 for n in range(2,bound+1):
  for seq in product(range(n),repeat=n-2):
   deg=[seq.count(i)+1 for i in range(n)];adj=[set() for _ in range(n)]
   for v in seq:
    leaf=next(i for i in range(n) if deg[i]==1);adj[v].add(leaf);adj[leaf].add(v);deg[v]-=1;deg[leaf]-=1
   a,b=[i for i in range(n) if deg[i]==1];adj[a].add(b);adj[b].add(a)
   p=[-2]*n;p[0]=-1;todo=[0]
   while todo:
    v=todo.pop()
    for w in adj[v]:
     if p[w]==-2:p[w]=v;todo.append(w)
   found.add(code(p))
 return found

def all_inputs(p):
 L=[]
 for n in range(1,len(p)+1):
  for tail in combinations(range(1,len(p)),n-1):
   y=(0,)+tail
   if all(v==0 or p[v] in y for v in y):L.append(y)
 L.sort(key=lambda y:sum(1<<v for v in y));full=frozenset(range(len(p)))
 for k in range(1,min(4,len(L))+1):
  for ys in combinations(L,k):
   if frozenset().union(*map(frozenset,ys))!=full:continue
   candidates=[]
   for i,y in enumerate(ys):
    for v in y:
     if v and not any(w and p[w]==v for w in y):candidates.append((i,v))
   for e,f in combinations(candidates,2):
    remaining=[set(y) for y in ys];remaining[e[0]].remove(e[1]);remaining[f[0]].discard(f[1])
    if set().union(*remaining)==set(full):yield ys,(e,f)

def transport(p,ys,ev):
 pi={0:0,**{v:len(p)-v for v in range(1,len(p))}};q=[-1]*len(p)
 for v in range(1,len(p)):q[pi[v]]=pi[p[v]]
 a=tuple(tuple(pi[v] for v in reversed(y)) for y in reversed(ys));b=tuple((len(ys)-1-i,pi[v]) for i,v in ev)
 return tuple(q),a,b

def input_key(ys,ev):return (tuple(map(tuple,ys)),tuple(map(tuple,ev)))

def verify_document(doc,bound=5,include_parent=True):
 need(type(bound)is int and 1<=bound<=5 and type(include_parent)is bool,'verification bounds')
 need(isinstance(doc,dict) and {'version','genesis','tree_bound','view_bound','include_parent','parent_raw_sha256','parent','extension','examples'}<=doc.keys(),'document schema')
 equal([doc['version'],doc['genesis'],doc['tree_bound'],doc['view_bound'],doc['include_parent']],['16.29',ORIGIN,bound,4,include_parent],'document metadata')
 totals={'parent':{'original':Counter(),'relabeled':Counter()},'extension':{'original':Counter(),'relabeled':Counter()}}
 groups=doc['extension'];need(isinstance(groups,list),'extension list');seen={}
 for g in groups:
  need(isinstance(g,dict) and {'code','variant','parents','cases'}<=g.keys(),'group schema');p=tree(g['parents']);key=(g['code'],g['variant'])
  need(g['variant'] in ('original','relabeled') and code(p)==g['code'] and key not in seen,'shape identity/duplicate');seen[key]=g
 expected={(sc,v) for sc in shape_codes(bound) for v in ('original','relabeled')};need(set(seen)==expected,'complete shape coverage')
 for sc in shape_codes(bound):
  original=seen[(sc,'original')];p=tree(original['parents']);specs=list(all_inputs(p))
  for variant in ('original','relabeled'):
   g=seen[(sc,variant)];specs2=[(p,a,b) if variant=='original' else transport(p,a,b) for a,b in specs]
   q=p if variant=='original' else transport(p,[(0,)],[])[0];equal(g['parents'],list(q),'false metamorphic parent')
   expected_cases={input_key(a,b):(q,a,b) for q,a,b in specs2};need(len(expected_cases)==len(specs2),'duplicate enumerator')
   need(isinstance(g['cases'],list),'cases list');actual={}
   for c in g['cases']:
    r=verify_case(c);k=input_key(c['before'],c['events']);need(k in expected_cases and k not in actual,'unexpected/duplicate case')
    equal(c['parents'],g['parents'],'case carrier');actual[k]=c;totals['extension'][variant].update(r)
   need(set(actual)==set(expected_cases),'missing extension case')
 # Parent raw corpus is an immutable input, not an executable verifier or an outcome oracle.
 equal(doc['parent_raw_sha256'],PARENT_SHA if include_parent else None,'parent identity field')
 if include_parent:
  raw=lzma.decompress(PARENT.read_bytes());need(hashlib.sha256(raw).hexdigest()==PARENT_SHA,'parent bytes')
  old=json.loads(raw);provided={}
  for g in doc['parent']:
   k=(g['code'],g['variant']);need(k not in provided,'duplicate parent group');provided[k]=g
  need(set(provided)=={(g['code'],g['variant']) for g in old['instances']},'parent group coverage')
  for oldg in old['instances']:
   g=provided[(oldg['code'],oldg['variant'])];equal(g['parents'],oldg['parents'],'parent group carrier');expected_rows={}
   for ci,c in enumerate(oldg['cases']):
    vals=dict(c['states']);events=c['events']
    for di,(mask,j,k,mixed) in enumerate(c['diamonds']):
     a=tuple(tuple(v for v in y if not any(mask>>t&1 and events[t]==[i,v] for t in range(len(events)))) for i,y in enumerate(c['before']))
     hs=[vals[mask],vals[mask|(1<<j)],vals[mask|(1<<k)],vals[mask|(1<<j)|(1<<k)]]
     expected_rows[(ci,di)]=(a,[events[j],events[k]],hs,mixed)
   seenrows=set()
   for row in g['records']:
    need(isinstance(row,dict) and {'id','certificate'}<=row.keys(),'parent row');ident=row['id']
    need(isinstance(ident,list) and len(ident)==2 and all(type(x)is int for x in ident),'row identity');ident=tuple(ident)
    need(ident in expected_rows and ident not in seenrows,'parent row coverage');seenrows.add(ident);c=row['certificate'];a,ev,hs,mixed=expected_rows[ident]
    equal(c['parents'],g['parents'],'parent certificate carrier');equal(c['before'],a,'parent state');equal(c['events'],ev,'parent events');equal(c['heights'],hs,'parent scalar heights');equal(c['global_mixed'],mixed,'parent scalar diamond')
    totals['parent'][g['variant']].update(verify_case(c))
   need(seenrows==set(expected_rows),'missing parent diamond')
 else:equal(doc['parent'],[],'undeclared parent audit')
 # Controls are pinned admitted examples, not alternative source families.
 controls={
 'max_negative':([-1,0,0,1,1],[[0,1,2],[0,1,3,4],[0,2],[0,1,4]],[[0,2],[1,4]]),
 'max_positive':([-1,0,0,1,1,1],[[0,1,3,4,5],[0,1,3],[0,1,4],[0,2]],[[0,3],[0,4]]),
 'masked':([-1,0,0,1,1],[[0,1,3,4],[0,1,3],[0,1,4],[0,2]],[[0,3],[0,4]]),
 'transmitted_negative':([-1,0,0],[[0,1],[0,2],[0,1,2]],[[2,1],[2,2]]),
 'transmitted_positive':([-1,0,0],[[0,1,2],[0,1,2]],[[0,1],[1,2]]),
 'zero':([-1,0],[[0,1],[0,1],[0,1]],[[0,1],[1,1]])}
 need(isinstance(doc['examples'],dict) and set(doc['examples'])==set(controls),'example coverage');examples={}
 for name,(p,a,ev) in controls.items():
  c=doc['examples'][name];equal([c['parents'],c['before'],c['events']],[p,a,ev],'control inputs');examples[name]=dict(verify_case(c))
 for section in totals:
  equal(dict(totals[section]['original']),dict(totals[section]['relabeled']),'metamorphic summary disagreement')
 return {'version':'16.29','execution_status':'COMPLETED','input_validity':'VALID','proof_status':'written L1-L7 plus independently reconstructed exact finite cases','scope':'existing local counts and fixed global maximum; not a physical interaction law',
         'parent':{k:dict(v) for k,v in totals['parent'].items()},'extension':{k:dict(v) for k,v in totals['extension'].items()},'examples':examples,'extension_shapes':len(shape_codes(bound))}

if __name__=='__main__':
 e=HERE/'evidence';raw=lzma.decompress((e/'FULL_CERTIFICATES.json.xz').read_bytes());r=verify_document(json.loads(raw));r['raw_sha256']=hashlib.sha256(raw).hexdigest()
 (e/'VERIFICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
