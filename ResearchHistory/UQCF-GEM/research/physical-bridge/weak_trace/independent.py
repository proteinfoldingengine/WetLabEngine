"""Independent weak-trace reconstruction using sets and the inherited set engine.
No producer import; source universes, certificates and edit paths are reconstructed.
"""
import gzip,hashlib,importlib.util,itertools as it,json,pathlib,sys
from functools import lru_cache
spec=importlib.util.spec_from_file_location('fingerprint_sets',pathlib.Path(__file__).resolve().parent.parent/'fingerprint_lock/independent.py')
B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
P=B.ROOTS;M=B.M;D=B.hashof
_reader=None;_records={};_seen=set()
def compare(key,value):
 key=json.dumps(key,separators=(',',':'))
 if _reader is None:_records[key]=value;return
 if key in _seen:return
 _seen.add(key);record=json.loads(next(_reader))
 assert record[0]==key,('record order',key,record[0])
 assert json.loads(json.dumps(value))==record[1],('full identities',key)
B.compare=compare

def structure(g):
 edges={P[r] for r in B.decode(g)}
 ns=[tuple(v for v in range(5) if tuple(sorted((u,v))) in edges) for u in range(5)]
 cycles=set()
 for c in it.permutations(range(5)):
  if c[0]!=0 or c[1]>c[-1]:continue
  if {tuple(sorted((c[k-1],c[k]))) for k in range(5)}<=edges:cycles.add(c)
 te=[];ind=[]
 for size in (3,4):
  for subset in it.combinations(range(5),size):
   internal=set(it.combinations(subset,2));outside=tuple(sorted(set(range(5))-set(subset)))
   if size==3 and internal<=edges and tuple(outside) in edges:te.append([subset,outside])
   if not internal&edges:
    neighbors=tuple(sorted({v for u in subset for v in ns[u]}))
    if len(neighbors)<size:ind.append([subset,neighbors])
 deg=list(map(len,ns));cherries=[];triples=[]
 for i,a,j in it.permutations(range(5),3):
  if ns[i]==ns[j]==(a,):cherries.append((i,a,j))
 if min(deg)==1:
  for i,a,j,b,k in it.permutations(range(5)):
   I={i,j,k};N={a,b}
   if ns[i]!=(a,) or b not in ns[j]:continue
   if any(set(e)<=I for e in edges):continue
   if {v for u in I for v in ns[u]}==N:triples.append((i,a,j,b,k))
 return dict(G=g,neighbors=ns,degrees=deg,isolated=[v for v in range(5) if not ns[v]],cycles=sorted(cycles),triangle_edges=te,independent=ind,cherries=sorted(cherries),triples=sorted(triples))

def static_certificate(s,t):
 if s['isolated']:
  i=min(s['isolated']);return dict(kind='isolated',types=[i],vector=[t-(v==i) for v in range(5)])
 if t==1:return dict(kind='t1_no_isolate',types=[],vector=None)
 if s['cycles']:
  c=s['cycles'][0];edges={tuple(sorted((c[k-1],c[k]))) for k in range(5)}
  return dict(kind='cycle',weights_numerator=[int(e in edges) for e in P],denominator=2,vector=None)
 if s['triangle_edges']:
  tri,pair=s['triangle_edges'][0]
  return dict(kind='triangle_edge',weights_numerator=[2 if e==pair else int(set(e)<=set(tri)) for e in P],denominator=2,vector=None)
 I,N=sorted(s['independent'],key=lambda z:(-len(z[0]),z[0]))[0]
 return dict(kind='independent',types=list(I),neighbors=list(N),vector=[2*t-1 if v in N else 1 for v in range(5)])

def parameters(kind,s,t,key,donors,anchors):
 assert t>1
 if kind=='cherry':
  i,a,j=key;assert i!=j and s['neighbors'][i]==s['neighbors'][j]==(a,)
  source_types=[i];target=j
 else:
  assert kind=='triple';i,a,j,b,k=key
  assert len(set(key))==5 and min(s['degrees'])==1
  assert s['neighbors'][i]==(a,) and b in s['neighbors'][j]
  I={i,j,k};assert not any(I&set(s['neighbors'][v]) for v in I)
  assert {v for u in I for v in s['neighbors'][u]}=={a,b}
  source_types=[i,j];target=k
 assert donors==[v*t+1 for v in source_types]
 assert anchors==[v*t for v in range(5) if v!=target]
 assert not set(donors)&set(anchors) and B.number(tuple(B.original(t)[x] for x in anchors))==4
 return True

def route(kind,s,t,key,gates):
 g=s['G'];source=B.original(t);cur=list(source);operations=[];states=[B.encode(cur)];compensations=[]
 target=key[0] if kind=='isolated' else key[-1]
 anchors=[v*t for v in range(5) if v!=target]
 if kind!='isolated':parameters(kind,s,t,key,[key[0]*t+1] if kind=='cherry' else [key[0]*t+1,key[2]*t+1],anchors)
 if (t,g) not in gates:gates[t,g]=B.Gate(t,g)
 gate=gates[t,g];gate.check(cur)
 def edit(x,r,add=False):
  if add:assert r not in cur[x];compensations.append((len(operations),r))
  else:assert r in cur[x]
  cur[x]=cur[x]^{r};operations.append([x,r]);states.append(B.encode(cur));gate.check(cur)
  assert all(cur[a]==source[a] for a in anchors)
 def shrink(v,w):
  retained=P.index(tuple(sorted((v,w))))
  for r in sorted(cur[v*t+1]-{retained}):edit(v*t+1,r)
 def add(v,a,b):edit(v*t+1,P.index(tuple(sorted((a,b)))),True)
 if kind=='isolated':assert not s['neighbors'][target]
 elif kind=='cherry':
  i,a,j=key;shrink(i,a);add(i,a,j)
 else:
  i,a,j,b,k=key;shrink(i,a)
  for endpoint in (j,k):
   if endpoint in s['neighbors'][a]:add(i,a,endpoint)
  shrink(j,b)
  if k in s['neighbors'][b]:add(j,b,k)
 for r in sorted(cur[target*t]):edit(target*t,r)
 first=next(k for k,c in enumerate(states) if 0 in c)
 assert first==len(operations) and sum(not z for z in cur)==1
 cost=4 if kind=='isolated' else 8 if kind=='cherry' else 10+int(key[2] in s['neighbors'][key[1]])+len(s['neighbors'][target])
 assert cost==len(operations)
 failures=[]
 for omit,r in compensations:
  altered=list(source);bad=None
  for step,(x,root) in enumerate(operations):
   if step==omit:continue
   altered[x]=altered[x]^{root}
   if sum(r in z for z in altered)<gate.f[r]:bad=step;break
  assert bad is not None and r in B.decode(g)
  failures.append([omit,r,bad])
 compare(['route',kind,g,t,list(key)],dict(ops=operations,states=states,anchors=anchors,omission_rejections=failures))
 return dict(kind=kind,G=g,t=t,key=list(key),ops=operations,cost=cost,first_absent=first,anchors=anchors,states_hash=D(states),final=list(B.encode(cur)),globally_optimal=kind=='isolated' or kind=='cherry' and not s['isolated'],omission_rejections=failures)

def lower():
 records=[]
 for r,e in enumerate(P):
  for k in sorted(set(range(5))-set(e)):
   for owner in e:
    possible=[]
    remaining=sorted(M[owner]-{r})
    for size in range(4):
     for subset in it.combinations(remaining,size):possible.append(frozenset(subset)|{r})
    for footprint in sorted(possible,key=lambda z:sum(2**v for v in z)):
     loss=len(M[k]-footprint);gain=len(footprint-M[k]);assert loss>=3 and gain>=1
     records.append([r,k,owner,sum(2**v for v in footprint),loss,gain])
 assert len(records)==480;compare(['lower'],records)
 return dict(witnesses=480,records_hash=D(records),minimum_donor_toggles=min(z[-1]+z[-2] for z in records),minimum_total=8)

def validate(c,t,g,fs=None):
 assert len(c)==5*t and (fs is None or tuple(fs)==B.limits(g,t))
 assert all(not z or any(z<=m for m in M) for z in c)
 assert all(len(z)>=f for z,f in zip(B.supports(c),B.limits(g,t)))
 assert B.number(c)<=4
 return True

def controls():
 t=2;g=B.HUB;s=B.original(t);st=structure(g);anchors=[0,2,6,8]
 def reject(fn,*args):
  try:fn(*args)
  except AssertionError:return True
  return False
 upper=list(s)
 for r in sorted(set(range(10))-B.decode(B.LOCK)):
  owner={0:0,7:4,8:5,9:6}[r]
  upper=[z|{r} if x==owner else z-{r} for x,z in enumerate(upper)]
 assert all(any(z<=m for m in M) for z in upper)
 assert all(len(z)>=f for z,f in zip(B.supports(upper),B.limits(B.LOCK,t))) and B.number(tuple(upper))==5
 bad_ind=structure(sum(1<<P.index(e) for e in ((0,1),(2,3),(2,4))))
 assert bad_ind['neighbors'][0]==(1,) and 3 in bad_ind['neighbors'][2] and 4 in bad_ind['neighbors'][2]
 assert parameters('cherry',st,t,(1,0,2),[3],anchors)
 return dict(fresh_label=reject(validate,s+(frozenset({0}),),t,g),changed_floor=reject(validate,s,t,g,(1,)*10),invalid_degree=reject(parameters,'cherry',st,t,(0,1,2),[1],anchors),invalid_independent=reject(parameters,'triple',bad_ind,t,(0,1,2,3,4),[1,5],[0,2,4,6]),invalid_donor=reject(parameters,'cherry',st,t,(1,0,2),[2],anchors),invalid_anchor=reject(parameters,'cherry',st,t,(1,0,2),[3],[0,1,2,3]),upper_violation=reject(validate,tuple(upper),t,B.LOCK))

@lru_cache(None)
def reconstruct(fixture=False):
 def graph(edges):return sum(2**P.index(tuple(sorted(e))) for e in edges)
 gs=sorted({0,B.HUB,B.LOCK,B.LOCK|1,graph([(0,1),(1,2),(2,3),(3,4),(4,0)]),graph([(0,1),(1,2),(2,3),(3,4)]),graph([(0,1),(0,2),(1,2),(3,4)])}) if fixture else range(1024)
 structures=[structure(g) for g in gs];cases=[]
 for s in structures:
  compare(['structure',s['G']],s)
  for t in ((1,2) if fixture else (1,2,3)):
   cg=B.countgraph(s['G'],t);static=cg['minimum']<5*t;reachable=cg['accessible_minimum']<5*t
   assert static==(bool(s['isolated']) if t==1 else bool(s['isolated'] or s['independent']))
   assert reachable==(bool(s['isolated']) if t==1 else static and min(s['degrees'])<=1)
   cert=static_certificate(s,t)
   if cert['vector'] is not None:
    v=cert['vector'];assert sum(v)<5*t and sum(n>0 for n in v)>=4
    assert all(v[a]+v[b]>=f for (a,b),f in zip(P,B.limits(s['G'],t)))
   if 'weights_numerator' in cert:
    w=cert['weights_numerator'];assert all(sum(w[r] for r in M[v])==2 for v in range(5))
    assert all(not weight or r in B.decode(s['G']) for r,weight in enumerate(w))
   cases.append(dict(G=s['G'],t=t,graph=cg,static_spare=static,reachable=reachable,fingerprint=cg['fingerprint'],isolated_types=s['isolated'],certificate=cert))
 if not fixture:
  forbidden=[]
  for N in it.combinations(range(5),2):
   cross=graph([e for e in P if len(set(e)&set(N))==1]);forbidden.extend((cross,cross+2**P.index(N)))
  for t in (2,3):assert sorted(forbidden)==[c['G'] for c in cases if c['t']==t and c['static_spare'] and not c['reachable']]
 gates={};routes=[]
 for s in structures:
  for t in ((1,2) if fixture else (1,2,3)):
   for i in s['isolated']:routes.append(route('isolated',s,t,(i,),gates))
  for t in ((2,) if fixture else (2,3,4,5)):
   for key in s['cherries']:routes.append(route('cherry',s,t,key,gates))
   for key in s['triples']:routes.append(route('triple',s,t,key,gates))
 summaries=[]
 for (t,g),gate in sorted(gates.items()):
  compare(['native',t,g],dict(cores=sorted(B.encode(c) for c in gate.valid),masks=gate.masks));summaries.append(dict(t=t,G=g,**gate.finish()))
 low=lower();ctrl=controls();assert all(ctrl.values())
 counts=dict(graph_cases=len(cases),structures=len(structures),routes=len(routes),isolated_routes=sum(r['kind']=='isolated' for r in routes),cherry_routes=sum(r['kind']=='cherry' for r in routes),triple_routes=sum(r['kind']=='triple' for r in routes),native_cores=sum(n['native_cores'] for n in summaries),slice_occurrences=sum(n['slice_occurrences'] for n in summaries),hidden_checks=sum(n['hidden_checks'] for n in summaries),lower_witnesses=low['witnesses'])
 return dict(schema='weak-trace-v1',fixture=fixture,structures=structures,cases=cases,routes=routes,native=summaries,lower_bound=low,controls=ctrl,counts=counts,**({'identities':_records} if fixture else {}))

def verify(data,fixture=False,identity_path=None):
 global _reader
 if not fixture:
  assert identity_path is not None
  assert hashlib.sha256(pathlib.Path(identity_path).read_bytes()).hexdigest()==data['identity_archive_sha256']
  _reader=gzip.open(identity_path,'rt');_seen.clear();reconstruct.cache_clear()
 try:
  expected=reconstruct(fixture)
  if not fixture:assert next(_reader,None) is None,'extra identities'
 finally:
  if _reader is not None:_reader.close();_reader=None
 if fixture:assert json.loads(json.dumps(data['identities']))==json.loads(json.dumps(expected['identities']))
 else:expected['identity_archive_sha256']=data['identity_archive_sha256']
 assert D(data)==D(expected),'complete reconstruction mismatch'
 return True
if __name__=='__main__':
 data=json.load(open(sys.argv[1]));verify(data,identity_path=sys.argv[1]+'.identities.jsonl.gz')
 result=dict(status='PASS',complete_independent_reconstruction=True,certificate_sha256=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(),counts=data['counts'])
 pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
