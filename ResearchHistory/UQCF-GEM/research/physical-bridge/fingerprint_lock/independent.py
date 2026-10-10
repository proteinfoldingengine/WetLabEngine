"""Independent full universe: root sets, multiset counts, indexed differences, union-find.
No producer imports; every declared identity is reconstructed before comparing."""
import gzip,hashlib,itertools,json,sys
from functools import lru_cache
_reader=None
_seen=set()
_fixture_records={}
def compare(key,value):
 key=json.dumps(key,separators=(',',':'))
 if _reader is not None:
  if key in _seen:return
  _seen.add(key);record=json.loads(next(_reader))
  assert record[0]==key,('identity order',key)
  assert json.loads(json.dumps(value))==record[1],('canonical identities before hashing',key)
 else:_fixture_records[key]=value
ROOTS=tuple((i,j) for i in range(5) for j in range(i+1,5))
LOCK=sum(2**r for r,e in enumerate(ROOTS) if e[0]<2<=e[1])
HUB=sum(2**r for r,e in enumerate(ROOTS) if 0 in e)
M=tuple(frozenset(r for r,e in enumerate(ROOTS) if i in e) for i in range(5))
def hashof(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def encode(c):return tuple(sum(2**r for r in s) for s in c)
def original(t):return tuple(s for s in M for _ in range(t))
def limits(g,t):return tuple(2*t if r in decode(g) else 1 for r in range(10))
def decode(n):return frozenset(k for k in range(n.bit_length()) if n&2**k)
def supports(c):return tuple(frozenset(x for x,s in enumerate(c) if r in s) for r in range(10))
def number(c,required=frozenset(range(10))):
 # Independent branch-and-bound hitting set solver on root supports.
 req=[frozenset(x for x,s in enumerate(c) if r in s) for r in required]
 if any(not a for a in req):return 6
 @lru_cache(None)
 def solve(todo):
  if not todo:return 0
  pivot=min(todo,key=len)
  return 1+min(solve(tuple(a for a in todo if x not in a)) for x in pivot)
 return solve(tuple(sorted(set(req),key=lambda a:(len(a),tuple(sorted(a))))))
def cert(c,f,k):
 ss=supports(c);maxs={a for a in c if a and not any(a<b for b in c)}
 if any(len(ss[r])!=f[r] for r in k):return False
 for a in c:
  trace=a&k;containers=[b for b in maxs if trace<=b]
  if not trace or len(containers)!=1 or containers[0]&k!=trace:return False
 return True

def partitions(vs,links):
 parent=list(range(len(vs)))
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,b,*_ in links:
  x,y=find(a),find(b)
  if x!=y:parent[y]=x
 groups={}
 for i in range(len(vs)):groups.setdefault(find(i),[]).append(i)
 return sorted(groups.values())

def countgraph(g,t):
 f=limits(g,t);vertices=[]
 # Multisets give a distinct source enumeration, including empty type0.
 for multi in itertools.combinations_with_replacement(range(6),5*t):
  n=tuple(multi.count(i) for i in range(6))
  if all(n[i+1]+n[j+1]>=f[r] for r,(i,j) in enumerate(ROOTS)):vertices.append(n)
 vertices.sort();lookup={n:a for a,n in enumerate(vertices)};links=[]
 for a,n in enumerate(vertices):
  # Indexed target identity changes; gates evaluated at explicit root meets.
  for removed in range(6):
   if n[removed]==0:continue
   for added in range(6):
    if removed==added:continue
    target=tuple(n[k]-(k==removed)+(k==added) for k in range(6));b=lookup.get(target)
    if b is None:continue
    if removed==0:meet=n
    else:meet=tuple(n[k]-(k==removed) for k in range(6))
    cover=frozenset()
    for i in range(5):
     if meet[i+1]:cover|=M[i]
    # Exact meet retains the singleton common pair for nonempty transfer.
    if removed and added:cover|=M[removed-1]&M[added-1]
    cardinalities=[meet[i+1]+meet[j+1]+int(removed and added and {removed-1,added-1}=={i,j}) for i,j in ROOTS]
    if not all(v>=bound for v,bound in zip(cardinalities,f)):continue
    assert cover==frozenset(range(10))
    # At least four unchanged maxima, or three + retained singleton suffice.
    occupied=sum(v>0 for v in meet[1:]);assert occupied>=4 or (occupied==3 and removed and added)
    links.append((a,b,removed-1,added-1))
 links.sort();groups=partitions(vertices,links);src=(0,)+(t,)*5;part=next(c for c in groups if lookup[src] in c)
 minimum=5*t-max(n[0] for n in vertices);best=[n for n in vertices if 5*t-n[0]==minimum]
 deg=[len([r for r,e in enumerate(ROOTS) if r in decode(g) and i in e]) for i in range(5)]
 fingerprint=cert(original(t),f,decode(g));isolated=len(part)==1;assert fingerprint==isolated==(min(deg)>=2)
 compare(['count',g,t],dict(vertices=vertices,edges=links,components=groups,static=best,source_component=part))
 local=None
 if fingerprint and len(decode(g))<10:
  r=min(set(range(10))-decode(g));x=ROOTS[r][0]*t;c=list(original(t));c[x]=c[x]-{r}
  assert len(supports(c)[r])>=f[r] and number(tuple(c))==4;local=[x,r]
 return dict(G=g,t=t,original_floors=list(f),source=list(src),vertices=len(vertices),edges=len(links),components=len(groups),vertices_hash=hashof(vertices),edges_hash=hashof(links),components_hash=hashof(groups),source_component_hash=hashof(part),minimum=minimum,static_hash=hashof(best),accessible_minimum=min(5*t-vertices[a][0] for a in part),isolated=isolated,fingerprint=fingerprint,local_deletion=local)

class Gate:
 def __init__(self,t,g):
  self.t=t;self.g=g;self.s=original(t);self.f=limits(g,t);self.original=supports(self.s);self.valid=set();self.occurrences=0
  # Enumerate exposed-root subsets, then translate to hidden identity.
  masks=[]
  for k in range(1,11):
   for exposed in itertools.combinations(range(10),k):
    intersection=set(range(5*t))
    for r in exposed:intersection.intersection_update(self.original[r])
    if not intersection:masks.append(1023-sum(2**r for r in exposed))
  self.masks=sorted(masks)
 def check(self,c):
  c=tuple(frozenset(s) for s in c);self.occurrences+=1
  if c in self.valid:return
  assert len(c)==5*self.t and all(not s or any(s<=m for m in M) for s in c)
  assert all(len(a)>=b for a,b in zip(supports(c),self.f))
  assert number(c)<=4;self.valid.add(c)
 def finish(self):
  h=hashlib.sha256();checks=0
  exposures=[(hidden,tuple(r for r in range(10) if not hidden&2**r)) for hidden in self.masks]
  for c in sorted(self.valid,key=encode):
   ss=supports(c);bits=encode(c);prefix=('['+json.dumps(bits,separators=(',',':'))+',').encode()
   for hidden,exposed in exposures:
    # Independent actual support intersections; terminate only once empty.
    common=ss[exposed[0]]
    for r in exposed[1:]:
     common=common&ss[r]
     if not common:break
    assert not common
    h.update(prefix+str(hidden).encode()+b']\n');checks+=1
  return dict(native_cores=len(self.valid),slice_occurrences=self.occurrences,hidden_masks=len(self.masks),hidden_checks=checks,hidden_hash=h.hexdigest())

def static_target(t):
 gate=Gate(t,LOCK);v=(2*t-1,2*t-1,1,1,1);c=tuple(m for m,k in zip(M,v) for _ in range(k))+(frozenset(),)*(t-1);gate.check(c)
 assert number(c)==4
 same=all((a&decode(LOCK))==(b&decode(LOCK)) for a,b in zip(c,gate.s))
 return dict(t=t,columns=list(encode(c)),absent=sum(not s for s in c),in_locked_component=same,**gate.finish())

def rawgraph(t):
 gate=Gate(t,LOCK);unlocked=sorted(set(range(10))-decode(LOCK));domain=[]
 for r in unlocked:
  choices=[]
  for k in range(1,len(gate.original[r])+1):
   for sub in itertools.combinations(sorted(gate.original[r]),k):choices.append(sum(2**x for x in sub))
  domain.append(sorted(choices))
 # Independent constraint solver: locked-compatible four covers as actual label sets.
 candidates4=[]
 for labels in itertools.combinations(range(5*t),4):
  if all(set(labels)&gate.original[r] for r in decode(LOCK)):candidates4.append(frozenset(labels))
 vertices=[];core={}
 for v in itertools.product(*domain):
  sets=tuple(decode(a) for a in v)
  if not any(all(labels&s for s in sets) for labels in candidates4):continue
  ss=list(gate.original)
  for r,s in zip(unlocked,sets):ss[r]=s
  c=tuple(frozenset(r for r in range(10) if x in ss[r]) for x in range(5*t))
  assert all(c);vertices.append(v);core[v]=c
 vertices.sort();lookup={v:a for a,v in enumerate(vertices)};links=[]
 # Enumerate adjacent pairs using root-support buckets with one coordinate omitted.
 for k,r in enumerate(unlocked):
  buckets={}
  for a,v in enumerate(vertices):buckets.setdefault(v[:k]+v[k+1:],[]).append((a,v[k]))
  for bucket in buckets.values():
   for (a,left),(b,right) in itertools.combinations(bucket,2):
    xor=left^right
    if xor and xor&(xor-1)==0:links.append((a,b,xor.bit_length()-1,r))
 links.sort();groups=partitions(vertices,links);assert len(groups)==1
 h=hashlib.sha256()
 for v in vertices:
  c=core[v];removed=sorted((x,r) for x,s in enumerate(gate.s) for r in s-c[x]);current=list(gate.s);path=[encode(current)];gate.check(current)
  for x,r in removed:current[x]=current[x]-{r};gate.check(current);path.append(encode(current))
  assert tuple(current)==c
  for state in reversed(path):gate.check(tuple(decode(s) for s in state))
  compare(['lift',t,list(v)],[v,removed,path,list(reversed(path))])
  h.update(json.dumps([v,removed,path,list(reversed(path))],separators=(',',':')).encode()+b'\n')
 compare(['raw',t],dict(vertices=vertices,edges=links,components=groups,cores=sorted(encode(c) for c in gate.valid),hidden_masks=gate.masks))
 return dict(t=t,candidates=len(domain[0])**4,vertices=len(vertices),edges=len(links),components=1,vertices_hash=hashof(vertices),edges_hash=hashof(links),components_hash=hashof(groups),lifts_hash=h.hexdigest(),**gate.finish())

def journey(t,pair=None,batch=False):
 gate=Gate(t,HUB);cur=list(gate.s);anchors=[i*t for i in range(1,5)];operations=[];states=[list(encode(cur))];gate.check(cur)
 def edit(x,r):
  cur[x]=cur[x]^{r};operations.append([x,r]);states.append(list(encode(cur)));gate.check(cur)
  assert all(cur[a]==M[i] for i,a in enumerate(anchors,1))
 moves=[]
 if batch:moves=[(i*t+k,i) for i in range(1,5) for k in range(1,t)]
 else:moves=[(i*t+1,i) for i in pair]
 for x,i in moves:
  for r in sorted(M[i]-M[0]):edit(x,r)
  for r in sorted(M[0]-M[i]):edit(x,r)
 donors=sorted(list(range(t))+[x for x,_ in moves])[:3*t-3] if batch else [0]
 for x in donors:
  for r in sorted(cur[x]):edit(x,r)
 first=next(k for k,c in enumerate(states) if 0 in c)
 assert len(operations)==(36*(t-1) if batch else 16) and (batch or first==16)
 assert sum(bool(s) for s in cur)==(2*t+3 if batch else 5*t-1)
 return dict(t=t,leaves=list(pair or []),anchors=anchors,ops=operations,states_hash=hashof(states),final=list(encode(cur)),first_absent=first,**gate.finish())

def boundaries():
 c=list(original(2))
 for pair,x in [((0,1),0),((2,3),4),((2,4),5),((3,4),6)]:
  r=ROOTS.index(pair)
  c=[s|{r} if k==x else s-{r} for k,s in enumerate(c)]
 assert number(tuple(c))==5 and all(len(s)>=f for s,f in zip(supports(c),limits(LOCK,2)))
 start=tuple(decode(x) for x in (9,10,4,1,2));end=tuple(decode(x) for x in (1,2,4,9,10));f=(2,2,1,2)+(0,)*6
 assert cert(start,f,frozenset((0,1,2)))
 ops=[(3,3),(4,3),(0,3),(1,3)];path=[encode(start)];cur=list(start)
 for x,r in ops:
  cur[x]=cur[x]^{r};assert number(tuple(cur),frozenset(range(4)))==3
  assert all(len(supports(cur)[r])>=f[r] for r in range(4));path.append(encode(cur))
 assert tuple(cur)==end and sum(len(a^b) for a,b in zip(start,end))==4
 oldmax={decode(i) for i in (9,10,4)}
 def validate(c,provided=f):
  assert len(c)==len(start) and provided==f
  assert all(not s or any(s<=m for m in oldmax) for s in c)
  assert all(a&frozenset((0,1,2))==b&frozenset((0,1,2)) for a,b in zip(c,start))
  assert all(len(supports(c)[r])>=f[r] for r in range(4)) and number(c,frozenset(range(4)))<=4
 def refused(c,provided=f):
  try:validate(c,provided)
  except AssertionError:return True
  return False
 masks=[]
 for hidden in range(16):
  exposed=frozenset(range(4))-decode(hidden)
  if min(number(start,frozenset(range(4))),1+number(start,exposed))>=3:masks.append(hidden)
 h=hashlib.sha256();checks=0
 for state in path+list(reversed(path)):validate(tuple(decode(x) for x in state))
 for state in sorted(set(path)):
  c0=tuple(decode(x) for x in state)
  for hidden in masks:
   exposed=frozenset(range(4))-decode(hidden)
   assert 3<=min(number(c0,frozenset(range(4))),1+number(c0,exposed))<=4
   h.update(json.dumps([state,hidden],separators=(',',':')).encode()+b'\n');checks+=1
 assert len(supports(tuple(decode(x) for x in path[1]))[3])==3
 compare(['join'],dict(states=path,reverse=list(reversed(path)),hidden_masks=masks))
 reject=dict(empty=not cert(original(1),limits(LOCK,1),frozenset()),nonunique=not cert(original(1),limits(HUB,1),decode(HUB)),incomplete=not cert(start,f,frozenset(range(4))),nonsaturated=not cert(start,(1,2,1,2)+(0,)*6,frozenset((0,1,2))),fresh_label=refused(start+(frozenset((0,)),)),floor_change=refused(start,(1,2,1,2)+(0,)*6),empty_original_label=not cert(start+(frozenset(),),f,frozenset((0,1,2))))
 assert all(reject.values())
 return dict(upper5=number(tuple(c)),upper5_columns=list(encode(c)),join_cost=4,join_ops=ops,join_states_hash=hashof(path),join_reverse_hash=hashof(list(reversed(path))),join_hidden_checks=checks,join_hidden_hash=h.hexdigest(),join_native_cores=len(set(path)),join_slice_occurrences=2*len(path),rejections=reject,locked_addition_safe=True)

@lru_cache(None)
def reconstruct(fixture=False):
 graphs=[countgraph(g,t) for g in ([0,LOCK,HUB,1023] if fixture else range(1024)) for t in ([1] if fixture else (1,2))]
 locked=[]
 for t in ([1] if fixture else range(1,6)):
  g=countgraph(LOCK,t);assert g['minimum']==4*t+1 and g['isolated'];z=static_target(t);assert z['absent']==t-1 and z['in_locked_component']==(t==1)
  assert all(any(r in decode(LOCK) for r in s) for s in original(t))
  locked.append(dict(t=t,minimum=g['minimum'],graph=g,target=z,anchored_rejections=[[x,min(s&decode(LOCK))] for x,s in enumerate(original(t))]))
 stars=[]
 for t in ([2] if fixture else range(1,6)):
  g=countgraph(HUB,t);assert g['minimum']==2*t+3
  assert all(s in M and any(r in decode(HUB) for r in s) for s in original(t))
  stars.append(dict(t=t,minimum=g['minimum'],graph=g,anchored_rejections=[[x,min(s&decode(HUB))] for x,s in enumerate(original(t))]))
 raws=[rawgraph(t) for t in ([1] if fixture else (1,2))]
 routes=[journey(t,(i,j)) for t in ([2] if fixture else range(2,6)) for i in range(1,5) for j in range(1,5) if i!=j]
 batches=[journey(t,batch=True) for t in ([2] if fixture else range(2,6))]
 native=raws+routes+batches+[c['target'] for c in locked]
 control=boundaries()
 counts=dict(graph_cases=len(graphs),raw_vertices=sum(c['vertices'] for c in raws),first_routes=len(routes),batches=len(batches),hidden_checks=sum(c['hidden_checks'] for c in native)+control['join_hidden_checks'],slice_occurrences=sum(c['slice_occurrences'] for c in native)+control['join_slice_occurrences'])
 return dict(schema='fingerprint-lock-v1',fixture=fixture,graphs=graphs,locked=locked,stars=stars,raw=raws,routes=routes,batches=batches,controls=control,counts=counts,**({'identities':_fixture_records} if fixture else {}))
def verify(data,fixture=False,identity_path=None):
 global _reader
 if not fixture:
  assert identity_path is not None,'Full canonical identities are mandatory'
  assert hashlib.sha256(open(identity_path,'rb').read()).hexdigest()==data['identity_archive_sha256']
  _reader=iter(gzip.open(identity_path,'rt'));_seen.clear();reconstruct.cache_clear()
 try:
  expected=reconstruct(fixture)
  if not fixture:assert next(_reader,None) is None,'Extra identity records'
 finally:
  if not fixture:
   _reader.close();_reader=None
 if not fixture:
  expected['identity_archive_sha256']=data['identity_archive_sha256']
 # Fixtures also compare their complete canonical records before digest checks.
 if fixture:assert json.loads(json.dumps(data['identities']))==json.loads(json.dumps(expected['identities']))
 assert hashof(data)==hashof(expected),'Complete universe/identity mismatch';return True
if __name__=='__main__':
 data=json.load(open(sys.argv[1]));verify(data,identity_path=sys.argv[1]+'.identities.jsonl.gz');out=dict(status='PASS',complete_independent_reconstruction=True,certificate_sha256=hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest(),counts=data['counts'])
 open(sys.argv[2],'w').write(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
