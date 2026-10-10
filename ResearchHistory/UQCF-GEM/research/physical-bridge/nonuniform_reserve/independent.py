"""Independent nonuniform reconstruction: sets, multisets, explicit meets, union-find."""
import gzip,hashlib,importlib.util,itertools as it,json,pathlib,sys
from functools import lru_cache
sp=importlib.util.spec_from_file_location('set_primitives',pathlib.Path(__file__).resolve().parent.parent/'fingerprint_lock/independent.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
P=B.ROOTS;M=B.M;D=B.hashof
_reader=None;_records={};_seen=set()
def compare(key,value):
 key=json.dumps(key,separators=(',',':'))
 if _reader is None:_records[key]=value;return
 if key in _seen:return
 _seen.add(key);record=json.loads(next(_reader));assert record[0]==key,('order',key)
 assert json.loads(json.dumps(value))==record[1],('canonical identity',key)
def original(a):return tuple(m for m,n in zip(M,a) for _ in range(n))
def limits(g,a):return tuple(a[i]+a[j] if r in B.decode(g) else 1 for r,(i,j) in enumerate(P))
def starts(a):
 out=[];position=0
 for n in a:out.append(position);position+=n
 return out

def structure(g):
 edges={P[r] for r in B.decode(g)};ns=[tuple(v for v in range(5) if tuple(sorted((u,v))) in edges) for u in range(5)]
 sets=[]
 for mask in range(1,31):
  I=tuple(v for v in range(5) if mask&2**v)
  if set(it.combinations(I,2))&edges:continue
  N=tuple(sorted({v for u in I for v in ns[u]}))
  if len(N)<len(I):sets.append([I,N])
 sets.sort(key=lambda z:(len(z[0]),z[0]));cherries=[];triples=[]
 for i,h,j in it.permutations(range(5),3):
  if ns[i]==ns[j]==(h,):cherries.append((i,h,j))
 if min(map(len,ns))==1:
  for i,h,j,b,k in it.permutations(range(5)):
   I={i,j,k}
   if ns[i]!=(h,) or b not in ns[j] or any(set(e)<=I for e in edges):continue
   if {v for u in I for v in ns[u]}=={h,b}:triples.append((i,h,j,b,k))
 return dict(G=g,neighbors=ns,degrees=list(map(len,ns)),isolated=[u for u in range(5) if not ns[u]],independent=sets,cherries=sorted(cherries),triples=sorted(triples))

@lru_cache(64)
def universe(total,fs):
 vertices=[]
 for multiset in it.combinations_with_replacement(range(6),total):
  n=tuple(multiset.count(k) for k in range(6))
  if all(n[i+1]+n[j+1]>=bound for (i,j),bound in zip(P,fs)):vertices.append(n)
 vertices.sort();lookup={n:k for k,n in enumerate(vertices)};links=[]
 for u,n in enumerate(vertices):
  for removed in range(6):
   if not n[removed]:continue
   for added in range(6):
    if added==removed:continue
    target=tuple(n[k]-(k==removed)+(k==added) for k in range(6));v=lookup.get(target)
    if v is None:continue
    meet=n if removed==0 else tuple(n[k]-(k==removed) for k in range(6))
    counts=[meet[i+1]+meet[j+1]+int(removed and added and {removed-1,added-1}=={i,j}) for i,j in P]
    if any(x<bound for x,bound in zip(counts,fs)):continue
    occupied=sum(bool(x) for x in meet[1:]);assert occupied>=4 or occupied==3 and removed and added
    links.append((u,v,removed-1,added-1))
 links.sort();groups=B.partitions(vertices,links);minimum=total-max(n[0] for n in vertices)
 return dict(vertices=vertices,edges=links,components=groups,static=[n for n in vertices if total-n[0]==minimum])

def graph(g,a):
 fs=limits(g,a);total=sum(a);u=universe(total,fs);compare(['universe',total,fs],u)
 src=(0,)+a;index=u['vertices'].index(src);group=next(c for c in u['components'] if index in c)
 compare(['count',g,a],dict(universe=[total,fs],source=src,source_component=group))
 fp=B.cert(original(a),fs,B.decode(g));isolated=len(group)==1;assert fp==isolated==(min(structure(g)['degrees'])>=2)
 return dict(G=g,profile=list(a),original_floors=list(fs),source=list(src),vertices=len(u['vertices']),edges=len(u['edges']),components=len(u['components']),vertices_hash=D(u['vertices']),edges_hash=D(u['edges']),components_hash=D(u['components']),static_hash=D(u['static']),minimum=total-u['static'][0][0],source_component_hash=D(group),accessible_minimum=min(total-u['vertices'][k][0] for k in group),count_isolated=isolated,fingerprint=fp)

class Gate:
 def __init__(self,g,a):
  self.g=g;self.a=a;self.s=original(a);self.fs=limits(g,a);self.valid=set();self.occurrences=0;supports=B.supports(self.s);masks=[]
  for size in range(1,11):
   for exposed in it.combinations(range(10),size):
    common=set(range(sum(a)))
    for r in exposed:common.intersection_update(supports[r])
    if not common:masks.append(1023-sum(2**r for r in exposed))
  self.masks=sorted(masks)
 def check(self,c):
  c=tuple(c);self.occurrences+=1
  if c in self.valid:return
  validate(c,self.a,self.g);self.valid.add(c)
 def finish(self):
  h=hashlib.sha256();checks=0;exposures=[(mask,tuple(r for r in range(10) if not mask&2**r)) for mask in self.masks]
  for c in sorted(self.valid,key=B.encode):
   supports=B.supports(c);bits=B.encode(c);prefix=('['+json.dumps(bits,separators=(',',':'))+',').encode()
   for hidden,exposed in exposures:
    common=supports[exposed[0]]
    for r in exposed[1:]:
     common=common&supports[r]
     if not common:break
    assert not common;h.update(prefix+str(hidden).encode()+b']\n');checks+=1
  return dict(native_cores=len(self.valid),slice_occurrences=self.occurrences,hidden_masks=len(self.masks),hidden_checks=checks,hidden_hash=h.hexdigest())

def validate(c,a,g,fs=None):
 assert len(a)==5 and all(isinstance(n,int) and n>0 for n in a)
 assert len(c)==sum(a) and (fs is None or tuple(fs)==limits(g,a))
 assert all(not s or any(s<=m for m in M) for s in c)
 assert all(len(s)>=bound for s,bound in zip(B.supports(c),limits(g,a)))
 assert B.number(c)<=4
 return True

def parameters(kind,st,a,key,exclude=None):
 ns=st['neighbors']
 if kind=='isolated':target=key[0];assert not ns[target];changed=[target]
 elif kind=='cherry':
  i,h,j=key;assert len({i,h,j})==3 and ns[i]==ns[j]==(h,);target=j;changed=[i,j]
 else:
  assert kind=='triple';i,h,j,b,k=key;I={i,j,k}
  assert len(set(key))==5 and min(st['degrees'])==1 and ns[i]==(h,) and b in ns[j]
  assert not any(I&set(ns[v]) for v in I) and {v for u in I for v in ns[u]}=={h,b}
  target=k;changed=[i,j,k]
 single=sorted(v for v in changed if a[v]==1);assert len(single)<2
 excluded=single[0] if single else target;assert exclude is None or exclude==excluded
 off=starts(a);anchors=[off[v] for v in range(5) if v!=excluded];labels={v:off[v]+(v!=excluded) for v in changed}
 assert all(x<off[v]+a[v] for v,x in labels.items()) and not set(labels.values())&set(anchors)
 assert B.number(tuple(original(a)[x] for x in anchors))==4
 return excluded,target,anchors,labels

def route(kind,st,a,key,gate):
 excluded,target,anchors,labels=parameters(kind,st,a,key);source=gate.s;cur=list(source);ops=[];states=[B.encode(cur)];comp=[];gate.check(cur)
 def edit(x,r,add=False):
  if add:assert r not in cur[x];comp.append((len(ops),r))
  else:assert r in cur[x]
  cur[x]=cur[x]^{r};ops.append([x,r]);states.append(B.encode(cur));gate.check(cur);assert all(cur[z]==source[z] for z in anchors)
 def shrink(v,w):
  keep=P.index(tuple(sorted((v,w))))
  for r in sorted(cur[labels[v]]-{keep}):edit(labels[v],r)
 def add(v,x,y):edit(labels[v],P.index(tuple(sorted((x,y)))),True)
 if kind=='cherry':i,h,j=key;shrink(i,h);add(i,h,j)
 elif kind=='triple':
  i,h,j,b,k=key;shrink(i,h)
  if j in st['neighbors'][h]:add(i,h,j)
  if k in st['neighbors'][h]:add(i,h,k)
  shrink(j,b)
  if k in st['neighbors'][b]:add(j,b,k)
 for r in sorted(cur[labels[target]]):edit(labels[target],r)
 first=next(k for k,c in enumerate(states) if 0 in c);cost=4 if kind=='isolated' else 8 if kind=='cherry' else 10+int(key[2] in st['neighbors'][key[1]])+len(st['neighbors'][target])
 assert len(ops)==first==cost and sum(not s for s in cur)==1
 failures=[]
 for omit,root in comp:
  altered=list(source);bad=None
  for step,(x,r) in enumerate(ops):
   if step==omit:continue
   altered[x]=altered[x]^{r}
   if sum(root in s for s in altered)<gate.fs[root]:bad=step;break
  assert bad is not None and root in B.decode(st['G']);failures.append([omit,root,bad])
 compare(['route',kind,st['G'],a,key],dict(ops=ops,states=states,anchors=anchors,excluded_type=excluded,labels=sorted(labels.items()),omission_rejections=failures))
 donors=[] if kind=='isolated' else [key[0]] if kind=='cherry' else [key[0],key[2]]
 return dict(kind=kind,G=st['G'],profile=list(a),key=list(key),excluded_type=excluded,target_type=target,anchors=anchors,labels=sorted(labels.items()),ops=ops,cost=cost,first_absent=first,states_hash=D(states),final=list(B.encode(cur)),globally_optimal=kind=='isolated' or kind=='cherry' and not st['isolated'],singleton_donor=any(a[v]==1 for v in donors),omission_rejections=failures)

def lower():
 records=[]
 for r,e in enumerate(P):
  for k in sorted(set(range(5))-set(e)):
   for owner in e:
    possible=[]
    for size in range(4):
     for subset in it.combinations(sorted(M[owner]-{r}),size):possible.append(frozenset(subset)|{r})
    for footprint in sorted(possible,key=lambda z:sum(2**v for v in z)):
     loss=len(M[k]-footprint);gain=len(footprint-M[k]);assert loss>=3 and gain>=1
     records.append([r,k,owner,sum(2**v for v in footprint),loss,gain])
 assert len(records)==480;compare(['lower'],records)
 return dict(witnesses=480,records_hash=D(records),minimum_donor_toggles=min(z[-1]+z[-2] for z in records),minimum_total=8)

def controls():
 def reject(fn,*args):
  try:fn(*args)
  except AssertionError:return True
  return False
 g=B.HUB;a=(1,1,2,1,1);st=structure(g);source=original(a);assert parameters('cherry',st,a,(1,0,2))[0]==1
 upper=list(original((2,)*5))
 for r,owner in [(0,0),(7,4),(8,5),(9,6)]:upper=[s|{r} if x==owner else s-{r} for x,s in enumerate(upper)]
 assert all(any(s<=m for m in M) for s in upper) and all(len(s)>=f for s,f in zip(B.supports(upper),limits(B.LOCK,(2,)*5))) and B.number(tuple(upper))==5
 partial=sum(2**P.index(e) for e in ((0,1),(1,2),(2,3),(1,4),(3,4)));ps=structure(partial);key=(0,1,2,3,4);assert key in ps['triples']
 return dict(two_singleton_cherry=reject(parameters,'cherry',st,(1,)*5,(1,0,2)),insufficient_triple=reject(parameters,'triple',ps,(1,1,2,1,1),key),wrong_exclusion=reject(parameters,'cherry',st,a,(1,0,2),2),fresh_label=reject(validate,source+(frozenset({0}),),a,g),wrong_floor=reject(validate,source,a,g,(2,)*10),invalid_profile=reject(validate,source,(0,1,2,1,1),g),upper_violation=reject(validate,tuple(upper),(2,)*5,B.LOCK))

@lru_cache(None)
def reconstruct(fixture=False):
 partial=sum(2**P.index(e) for e in ((0,1),(1,2),(2,3),(1,4),(3,4)))
 gs=sorted({0,B.HUB,B.LOCK,B.LOCK|1,partial,1023}) if fixture else range(1024)
 profiles=[(1,)*5,(2,)*5,(1,1,2,1,2),(1,1,2,1,1)] if fixture else list(it.product((1,2),repeat=5))
 structures=[structure(g) for g in gs];cases=[];routes=[];summaries=[]
 for st in structures:
  g=st['G'];compare(['structure',g],st)
  for a in profiles:
   cherries=[key for key in st['cherries'] if a[key[0]]+a[key[2]]>=3]
   triples=[list(I) for I,N in st['independent'] if len(I)==3 and len(N)==2 and sum(a[v]>1 for v in I)>=2]
   witnesses=[]
   for I,N in st['independent']:
    if len([v for v in I if a[v]==1])>1:continue
    vector=[a[v]+(v in N)-(v in I) for v in range(5)]
    assert sum(vector)<sum(a) and len([n for n in vector if n>0])>=4 and all(vector[i]+vector[j]>=f for (i,j),f in zip(P,limits(g,a)))
    witnesses.append(dict(types=list(I),neighbors=list(N),vector=vector))
   compare(['witnesses',g,a],witnesses)
   cg=graph(g,a);static=cg['minimum']<sum(a);reachable=cg['accessible_minimum']<sum(a)
   assert static==bool(st['isolated'] or cherries or triples)==bool(witnesses)
   assert reachable==(static and min(st['degrees'])<=1)
   if static and not reachable:assert any(len(I)==3 and len(N)==2 and all(len(st['neighbors'][v])==2 for v in I) and sum(a[v]>1 for v in I)>=2 for I,N in st['independent'])
   cases.append(dict(G=g,profile=list(a),graph=cg,static_spare=static,reachable=reachable,fingerprint=cg['fingerprint'],isolated_types=st['isolated'],eligible_cherries=cherries,eligible_triples=triples,witnesses=witnesses))
   gate=Gate(g,a)
   for v in st['isolated']:routes.append(route('isolated',st,a,(v,),gate))
   for key in cherries:routes.append(route('cherry',st,a,key,gate))
   for key in st['triples']:
    if sum(a[v]>1 for v in (key[0],key[2],key[4]))>=2:routes.append(route('triple',st,a,key,gate))
   if gate.valid:
    compare(['native',g,a],dict(cores=sorted(B.encode(c) for c in gate.valid),masks=gate.masks));summaries.append(dict(G=g,profile=list(a),**gate.finish()))
 if not fixture:
  observed={(c['G'],tuple(c['profile'])) for c in cases if c['static_spare'] and not c['reachable']};expected=set()
  for I in it.combinations(range(5),3):
   N=tuple(sorted(set(range(5))-set(I)))
   edges=[e for e in P if len(set(e)&set(I))==1]
   for selected in (edges,edges+[N]):
    g=sum(2**P.index(e) for e in selected)
    expected.update((g,a) for a in profiles if len([v for v in I if a[v]>1])>=2)
  assert observed==expected and len(observed)==320
 low=lower();ctrl=controls();assert all(ctrl.values())
 counts=dict(structures=len(structures),profiles=len(profiles),graph_cases=len(cases),routes=len(routes),isolated_routes=sum(r['kind']=='isolated' for r in routes),cherry_routes=sum(r['kind']=='cherry' for r in routes),triple_routes=sum(r['kind']=='triple' for r in routes),singleton_donor_routes=sum(r['singleton_donor'] for r in routes),native_cores=sum(n['native_cores'] for n in summaries),slice_occurrences=sum(n['slice_occurrences'] for n in summaries),hidden_checks=sum(n['hidden_checks'] for n in summaries),lower_witnesses=480)
 return dict(schema='nonuniform-reserve-v1',fixture=fixture,structures=structures,profiles=[list(a) for a in profiles],cases=cases,routes=routes,native=summaries,lower_bound=low,controls=ctrl,counts=counts,**({'identities':_records} if fixture else {}))

def verify(data,fixture=False,identity_path=None):
 global _reader
 if not fixture:
  assert identity_path is not None
  assert hashlib.sha256(pathlib.Path(identity_path).read_bytes()).hexdigest()==data['identity_archive_sha256']
  _reader=gzip.open(identity_path,'rt');_seen.clear();reconstruct.cache_clear()
 try:
  expected=reconstruct(fixture)
  if not fixture:assert next(_reader,None) is None,'extra identity'
 finally:
  if _reader is not None:_reader.close();_reader=None
 if fixture:assert json.loads(json.dumps(data['identities']))==json.loads(json.dumps(expected['identities']))
 else:expected['identity_archive_sha256']=data['identity_archive_sha256']
 assert D(data)==D(expected),'complete universe mismatch';return True
if __name__=='__main__':
 data=json.loads(pathlib.Path(sys.argv[1]).read_text());verify(data,identity_path=sys.argv[1]+'.identities.jsonl.gz')
 result=dict(status='PASS',complete_independent_reconstruction=True,certificate_sha256=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(),counts=data['counts']);pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
