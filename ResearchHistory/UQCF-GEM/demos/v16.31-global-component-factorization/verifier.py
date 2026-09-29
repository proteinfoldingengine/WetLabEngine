"""Independent retained verifier: Prufer coverage, legal paths, inclusion-exclusion.
No producer or inherited adjudicator imports. Missing evidence never succeeds.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations,permutations,product
from pathlib import Path
import hashlib,json,lzma
VERSION='16.31'
GENESIS='v16.31-frozen-common-genesis'
P=Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise ValueError(message)

def fields(d,keys,label):need(isinstance(d,dict) and set(keys)<=set(d),'missing '+label)
def integer(x):return type(x)is int

def same(a,b,label):
 try:ok=json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)
 except (TypeError,ValueError):ok=False
 need(ok,label)

def inputs(raw,before,after):
 need(isinstance(raw,(list,tuple)) and len(raw)>0,'parent carrier')
 p=tuple(raw);need(all(integer(v) for v in p),'parent scalar type')
 need(p[0]==-1 and all(0<=p[v]<len(p) for v in range(1,len(p))),'parent endpoints/root')
 for n in range(len(p)):
  seen=set();v=n
  while v!=0:
   need(v not in seen,'parent cycle');seen.add(v);v=p[v]
 def viewlist(rows):
  need(isinstance(rows,(list,tuple)) and len(rows)>0,'view family');ans=[]
  for row in rows:
   need(isinstance(row,(list,tuple)) and len(row)>0,'retained view')
   need(all(integer(n) and 0<=n<len(p) for n in row),'retained identity type')
   need(0 in row and len(set(row))==len(row),'root/duplicates')
   need(all(n==0 or p[n] in row for n in row),'prefix closure')
   ans.append(tuple(row))
  return tuple(ans)
 a,b=viewlist(before),viewlist(after)
 need(len(a)==len(b),'indexed endpoints');need(all(set(z)<=set(y) for y,z in zip(a,b)),'subset relation')
 need(set().union(*map(set,a))==set().union(*map(set,b)),'unchanged union')
 return p,a,b

@lru_cache(maxsize=150000)
def profile(p,ys):
 U=set().union(*map(set,ys));out=[]
 for v in range(len(p)):
  children={w for w in U if w and p[w]==v}
  if not children:out.append(0);continue
  best=None
  for k in range(1,len(ys)+1):
   if any(children<=set().union(*(set(ys[i]) for i in group)) for group in combinations(range(len(ys)),k)):
    best=k;break
  need(best is not None,'children not covered');out.append(best)
 return tuple(out)

def boolean_audit(values):
 need(isinstance(values,(list,tuple)) and len(values)>0,'Boolean values')
 size=len(values);need(size&(size-1)==0 and all(integer(x) for x in values),'Boolean cube scalar/size')
 k=(size-1).bit_length();mu=[]
 for s in range(size):
  mu.append(sum((-1)**(s.bit_count()-a.bit_count())*values[a] for a in range(size) if a&s==a))
 edges=[]
 for i,j in combinations(range(k),2):
  if any(values[a|1<<i|1<<j]-values[a|1<<i]-values[a|1<<j]+values[a]!=0 for a in range(size) if not a&(1<<i|1<<j)):
   edges.append([i,j])
 support_edges=set()
 for s,x in enumerate(mu):
  if x:support_edges.update(combinations([j for j in range(k) if s>>j&1],2))
 need(set(map(tuple,edges))==support_edges,'Mobius/pair graph disagreement')
 components=[];unseen=set(range(k))
 while unseen:
  block={min(unseen)}
  while True:
   bigger=block|{j for i,j in edges if i in block}|{i for i,j in edges if j in block}
   if bigger==block:break
   block=bigger
  components.append(sorted(block));unseen-=block
 for s in range(size):need(sum(mu[a] for a in range(size) if a&s==a)==values[s],'Mobius reconstruction')
 return {'mobius':mu,'edges':edges,'components':components}

def mask_of(ids):return sum(1<<j for j in ids)
def embed(s,ids):return mask_of(ids[k] for k in range(len(ids)) if s>>k&1)
def restrict(s,ids):return sum(1<<k for k,j in enumerate(ids) if s>>j&1)

def reconstruct(p,a,b):
 events=sorted((i,n) for i,y in enumerate(a) for n in y if n not in b[i]);m=len(events)
 need(m<=8,'independent verifier resource bound: at most eight events')
 # Explicit ancestor relations, then all actual legal leaf-deletion orders.
 ancestors={}
 for n in range(len(p)):
  s=set();u=p[n]
  while u!=-1:s.add(u);u=p[u]
  ancestors[n]=s
 pred=[mask_of(j for j,(k,w) in enumerate(events) if k==i and n in ancestors[w]) for i,n in events]
 U=set().union(*map(set,a));cover_cache={0:a};transition_cache={}
 def cover(s):
  if s not in cover_cache:
   deleted={events[j] for j in range(m) if s>>j&1}
   cover_cache[s]=tuple(tuple(n for n in y if (i,n) not in deleted) for i,y in enumerate(a))
  return cover_cache[s]
 def enabled(s,j):
  key=(s,j)
  if key not in transition_cache:
   i,n=events[j];ys=cover(s)
   okay=n in ys[i] and n!=0 and not any(w!=0 and p[w]==n for w in ys[i])
   if okay:okay=set().union(*map(set,cover(s|1<<j)))==U
   transition_cache[key]=okay
  return transition_cache[key]
 states={0};paths=0
 for order in permutations(range(m)):
  s=0;prefix=[0]
  for j in order:
   if not enabled(s,j):break
   s|=1<<j;prefix.append(s)
  else:
   need(cover(s)==b,'path final carrier');paths+=1;states.update(prefix)
 need(paths>0,'no complete legal deletion order')
 q={s:profile(p,cover(s)) for s in states}
 need(states=={s for s in range(1<<m) if all(not(s>>j&1) or pred[j]&s==pred[j] for j in range(m))},'ideal/path disagreement')
 return events,pred,q,paths

def verify_case(c):
 keys=('version','genesis','parents','before','after','events','predecessors','states','local','edges','edge_witnesses','product_states')
 fields(c,keys,'case fields');need(c['version']==VERSION and c['genesis']==GENESIS,'case provenance')
 p,a,b=inputs(c['parents'],c['before'],c['after']);events,pred,q,paths=reconstruct(p,a,b);m=len(events)
 same(c['events'],[list(e) for e in events],'event identities');same(c['predecessors'],pred,'predecessors')
 need(isinstance(c['states'],list),'states list');got={}
 for r in c['states']:
  need(isinstance(r,list) and len(r)==2 and integer(r[0]) and r[0] not in got,'state identifier')
  need(isinstance(r[1],list) and all(integer(x) for x in r[1]),'profile scalar types');got[r[0]]=tuple(r[1])
 need(got==q,'complete actual state/profile coverage')
 need(integer(c['product_states']) and c['product_states']==1<<m,'Cartesian candidate count')
 expected_vertices=sorted({p[n] for i,n in events});need(isinstance(c['local'],list),'local tables')
 tables={}
 for t in c['local']:
  fields(t,('vertex','event_ids','prelude','values','mobius','components'),'local table')
  need(integer(t['vertex']) and t['vertex'] not in tables,'local vertex type/duplicate');tables[t['vertex']]=t
 need(sorted(tables)==expected_vertices,'complete local table coverage')
 graph=set();diamonds=0
 for s in sorted(q):
  enabled=[j for j in range(m) if not(s>>j&1) and (s|1<<j) in q]
  for i,j in combinations(enabled,2):
   ef=s|1<<i|1<<j;need(ef in q,'enabled-pair closure');diamonds+=1
   d=tuple(q[ef][v]-q[s|1<<i][v]-q[s|1<<j][v]+q[s][v] for v in range(len(p)))
   if any(d):
    need(p[events[i][1]]==p[events[j][1]],'cross-parent local dependence')
    need(all(x==0 for v,x in enumerate(d) if v!=p[events[i][1]]),'wrong-parent mixed coordinate');graph.add((i,j))
 same(sorted(c['edges']),[list(e) for e in sorted(graph)],'complete full-history graph')
 cube_graph=set();cube_values=coefficients=components=higher=nonzero=0;factor_values={}
 for v,t in tables.items():
  ids=[j for j,(i,n) in enumerate(events) if p[n]==v];same(t['event_ids'],ids,'parent event identities')
  need(all(not(pred[j]&mask_of(ids)) for j in ids),'same-parent antichain')
  prelude=0
  for j in ids:prelude|=pred[j]
  need(integer(t['prelude']) and t['prelude']==prelude,'canonical prelude')
  truth=[]
  for localmask in range(1<<len(ids)):
   lifted=prelude|embed(localmask,ids);need(lifted in q,'illegal parent-cube lift')
   matching={prof[v] for s,prof in q.items() if restrict(s,ids)==localmask}
   need(matching=={q[lifted][v]},'global local-projection factorization');truth.append(q[lifted][v])
  same(t['values'],truth,'local truth table');need(truth[0]==q[0][v],'local baseline changed by prerequisites')
  ba=boolean_audit(truth);same(t['mobius'],ba['mobius'],'local Mobius coefficients')
  cube_graph.update((ids[i],ids[j]) for i,j in ba['edges'])
  expected=[]
  for block in ba['components']:
   glob=[ids[j] for j in block];vals=[truth[embed(s,block)]-truth[0] for s in range(1<<len(block))]
   expected.append({'event_ids':glob,'values':vals})
  need(isinstance(t['components'],list),'component records')
  same(sorted(t['components'],key=lambda x:x['event_ids']),expected,'normalized component factors')
  for s,prof in q.items():
   rec=truth[0]+sum(g['values'][restrict(s,g['event_ids'])] for g in expected)
   need(rec==prof[v],'full-history component reconstruction')
  cube_values+=len(truth);coefficients+=len(ba['mobius']);components+=len(expected)
  higher+=sum(x!=0 and s.bit_count()>=3 for s,x in enumerate(ba['mobius']))
  nonzero+=sum(any(g['values']) for g in expected);factor_values[v]=expected
 need(cube_graph==graph,'canonical cubes omitted a global graph edge')
 for v in range(len(p)):
  if v not in tables:need(all(prof[v]==q[0][v] for prof in q.values()),'unlisted changing coordinate')
 need(isinstance(c['edge_witnesses'],list),'edge witnesses');seen=set()
 for row in c['edge_witnesses']:
  need(isinstance(row,list) and len(row)==4 and all(integer(x) for x in row),'edge witness types')
  i,j,s,d=row;need((i,j) in graph and (i,j) not in seen and s in q,'edge witness identity');seen.add((i,j))
  need(not s&(1<<i|1<<j) and all((s|t) in q for t in (1<<i,1<<j,1<<i|1<<j)),'witness not enabled')
  v=p[events[i][1]];actual=q[s|1<<i|1<<j][v]-q[s|1<<i][v]-q[s|1<<j][v]+q[s][v]
  need(d==actual and d!=0,'false edge witness')
 need(seen==graph,'missing edge witness')
 return {'cases':1,'states':len(q),'paths':paths,'diamonds':diamonds,'graph_edges':len(graph),'parent_cube_values':cube_values,
         'mobius_coefficients':coefficients,'higher_order_nonzero':higher,'components':components,'nonzero_components':nonzero,
         'noncartesian_cases':int(len(q)<1<<m),'higher_order_cases':int(higher>0)}

def rooted_code(p):
 adj={v:[] for v in range(len(p))}
 for w in range(1,len(p)):adj[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in adj[v]))+')'
 return rec(0)

def shape_codes(bound):
 found=set()
 for n in range(1,bound+1):
  if n==1:found.add('()');continue
  for sequence in product(range(n),repeat=n-2):
   degree=[1+sequence.count(i) for i in range(n)];adj=[set() for _ in range(n)]
   for x in sequence:
    leaf=next(i for i,d in enumerate(degree) if d==1);adj[x].add(leaf);adj[leaf].add(x);degree[leaf]-=1;degree[x]-=1
   left=[i for i,d in enumerate(degree) if d==1];u,v=left;adj[u].add(v);adj[v].add(u)
   p=[-2]*n;p[0]=-1;stack=[0]
   while stack:
    v=stack.pop()
    for w in adj[v]:
     if p[w]==-2:p[w]=v;stack.append(w)
   found.add(rooted_code(tuple(p)))
 return sorted(found,key=lambda c:(len(c),c))

def decode(c):
 p=[];stack=[]
 for char in c:
  if char=='(':
   p.append(stack[-1] if stack else -1);stack.append(len(p)-1)
  else:stack.pop()
 return tuple(p)

def endpoint_keys(p):
 n=len(p);legal=[]
 for k in range(n):
  for rest in combinations(range(1,n),k):
   y=(0,)+rest
   if all(v==0 or p[v] in y for v in y):legal.append(y)
 legal.sort(key=lambda y:sum(1<<v for v in y));cap=4 if n<=4 else 3;full=set(range(n));out=set()
 for k in range(1,min(cap,len(legal))+1):
  for a in combinations(legal,k):
   if set().union(*map(set,a))!=full:continue
   for b in product(*[[z for z in legal if set(z)<=set(y)] for y in a]):
    if set().union(*map(set,b))==full and sum(len(y)-len(z) for y,z in zip(a,b))<=5:out.add((a,b))
 return out

def transport(p,a):
 pi=[0]+list(range(len(p)-1,0,-1));q=[-1]*len(p)
 for n in range(1,len(p)):q[pi[n]]=pi[p[n]]
 return tuple(q),tuple(tuple(pi[n] for n in reversed(y)) for y in reversed(a))

def check_transport(c,d):
 n=len(c['parents']);k=len(c['before']);pi=[0]+list(range(n-1,0,-1));new={tuple(e):j for j,e in enumerate(d['events'])}
 mapping=[new[(k-1-i,pi[v])] for i,v in c['events']]
 masks=lambda s:sum(1<<mapping[j] for j in range(len(mapping)) if s>>j&1)
 qd={s:q for s,q in d['states']}
 for s,q in c['states']:
  dest=[0]*n
  for v,x in enumerate(q):dest[pi[v]]=x
  same(qd[masks(s)],dest,'transported profile')
 same(sorted([sorted([mapping[i],mapping[j]]) for i,j in c['edges']]),sorted(d['edges']),'transported graph')
 dt={x['vertex']:x for x in d['local']}
 for t in c['local']:
  target=dt[pi[t['vertex']]];positions={j:h for h,j in enumerate(target['event_ids'])}
  need(masks(t['prelude'])==target['prelude'],'transported prerequisite cube')
  for s in range(len(t['values'])):
   dest=sum(1<<positions[mapping[j]] for h,j in enumerate(t['event_ids']) if s>>h&1)
   need(t['values'][s]==target['values'][dest] and t['mobius'][s]==target['mobius'][dest],'transported local coefficients')
  dest_components={tuple(g['event_ids']):g for g in target['components']}
  for g in t['components']:
   ids=sorted(mapping[j] for j in g['event_ids']);dest=dest_components[tuple(ids)]
   for s,x in enumerate(g['values']):
    a=sum(1<<ids.index(mapping[j]) for h,j in enumerate(g['event_ids']) if s>>h&1)
    need(x==dest['values'][a],'transported normalized factor')


def verify_document(doc,bound=5):
 fields(doc,('version','genesis','bound','instances'),'document sections')
 need(doc['version']==VERSION and doc['genesis']==GENESIS,'document origin')
 need(integer(bound) and 1<=bound<=5 and integer(doc['bound']) and doc['bound']==bound,'document bound')
 need(isinstance(doc['instances'],list),'instances');expected_codes=shape_codes(bound);lookup={}
 for inst in doc['instances']:
  fields(inst,('code','variant','parents','cases'),'shape instance');key=(inst['code'],inst['variant'])
  need(key not in lookup,'duplicate shape variant');lookup[key]=inst
 need(set(lookup)=={(c,v) for c in expected_codes for v in ('original','relabeled')},'complete shape coverage')
 totals={'original':Counter(),'relabeled':Counter()};details=[];transported=0
 for code in expected_codes:
  p=decode(code);keys=endpoint_keys(p);case_maps={}
  for variant in ('original','relabeled'):
   inst=lookup[(code,variant)];q=p if variant=='original' else transport(p,[(0,)])[0]
   same(inst['parents'],list(q),'actual transformed parent identities');expected=keys if variant=='original' else {(transport(p,a)[1],transport(p,b)[1]) for a,b in keys}
   need(isinstance(inst['cases'],list),'case array');seen={};counts=Counter()
   for c in inst['cases']:
    fields(c,('parents','before','after'),'endpoint')
    same(c['parents'],list(q),'foreign shape case');_,a,b=inputs(q,c['before'],c['after']);key=(a,b)
    need(key in expected and key not in seen,'unexpected/duplicate endpoint');seen[key]=c;counts.update(verify_case(c))
   need(set(seen)==expected,'complete endpoint coverage');case_maps[variant]=seen;totals[variant].update(counts)
   details.append({'code':code,'variant':variant,'vertices':len(p),'counts':dict(counts)})
  for (a,b),c in case_maps['original'].items():
   check_transport(c,case_maps['relabeled'][(transport(p,a)[1],transport(p,b)[1])]);transported+=1
 need(totals['original']==totals['relabeled'],'transported aggregate mismatch')
 return {'version':VERSION,'execution_status':'COMPLETED','input_validity':'VALID','proof_status':'G1-G8 plus independently reconstructed finite certificates',
         'scope':'full retained local-profile factorization, not Cartesian state or physical independence','shapes':len(expected_codes),
         'original':dict(totals['original']),'relabeled':dict(totals['relabeled']),'transported_cases':transported,'by_shape':details}

if __name__=='__main__':
 e=P/'evidence';raw=lzma.decompress((e/'FULL_CERTIFICATES.json.xz').read_bytes());doc=json.loads(raw)
 r=verify_document(doc,5);examples=json.loads((e/'EXAMPLES.json').read_text());r['examples']={k:verify_case(c) for k,c in examples.items()}
 r['raw_sha256']=hashlib.sha256(raw).hexdigest();(e/'VERIFICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:r[k] for k in ('execution_status','shapes','original','raw_sha256')}),flush=True)
