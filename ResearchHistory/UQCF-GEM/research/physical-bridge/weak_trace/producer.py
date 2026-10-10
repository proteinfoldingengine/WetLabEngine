"""Weak-trace producer; inherits the audited BIT count engine only."""
import gzip,hashlib,importlib.util,itertools as it,json,pathlib,sys
from functools import lru_cache
_spec=importlib.util.spec_from_file_location('fingerprint_bit',pathlib.Path(__file__).resolve().parent.parent/'fingerprint_lock/producer.py');B=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(B)
P=B.PAIRS;M=B.maxima();_writer=None;_seen=set();_records={}
def emit(key,value):
 k=json.dumps(key,separators=(',',':'))
 if _writer is None:_records[k]=value
 elif k not in _seen:_seen.add(k);_writer.write((json.dumps([k,value],separators=(',',':'))+'\n').encode())
B.emit=emit
D=B.digest
def edge(g,i,j):return bool(g>>P.index(tuple(sorted((i,j))))&1)
def structure(g):
 ns=[tuple(j for j in range(5) if j!=i and edge(g,i,j)) for i in range(5)];deg=[len(s) for s in ns]
 cycles=[]
 for tail in it.permutations(range(1,5)):
  c=(0,)+tail
  if c[1]<c[-1] and all(edge(g,c[k],c[(k+1)%5]) for k in range(5)):cycles.append(c)
 te=[]
 for tri in it.combinations(range(5),3):
  other=tuple(v for v in range(5) if v not in tri)
  if all(edge(g,a,b) for a,b in it.combinations(tri,2)) and edge(g,*other):te.append([tri,other])
 indep=[]
 for size in (3,4):
  for I in it.combinations(range(5),size):
   if any(edge(g,a,b) for a,b in it.combinations(I,2)):continue
   neigh=tuple(sorted(set().union(*(set(ns[i]) for i in I))))
   if len(neigh)<size:indep.append([I,neigh])
 isolated=[i for i,d in enumerate(deg) if not d]
 if not isolated:assert bool(cycles or te)!=bool(indep)
 cherries=[(i,ns[i][0],j) for i in range(5) for j in range(5) if i!=j and deg[i]==deg[j]==1 and ns[i]==ns[j]]
 triples=[]
 if min(deg)==1:
  for I,N in indep:
   if len(I)!=3 or len(N)!=2:continue
   for i in I:
    if deg[i]!=1:continue
    a=ns[i][0];b=next(v for v in N if v!=a)
    for j in I:
     if j!=i and b in ns[j]:k=next(v for v in I if v not in (i,j));triples.append((i,a,j,b,k))
 return dict(G=g,neighbors=ns,degrees=deg,isolated=isolated,cycles=cycles,triangle_edges=te,independent=indep,cherries=sorted(cherries),triples=sorted(triples))
def static_certificate(s,t):
 g=s['G'];n=[t]*5
 if s['isolated']:
  i=s['isolated'][0];n[i]-=1;return dict(kind='isolated',types=[i],vector=n)
 if t==1:return dict(kind='t1_no_isolate',types=[],vector=None)
 if s['cycles']:
  c=s['cycles'][0];w=[0]*10
  for i in range(5):w[P.index(tuple(sorted((c[i],c[(i+1)%5]))))]=1
  return dict(kind='cycle',weights_numerator=w,denominator=2,vector=None)
 if s['triangle_edges']:
  tri,pair=s['triangle_edges'][0];w=[0]*10
  for e in it.combinations(tri,2):w[P.index(e)]=1
  w[P.index(pair)]=2;return dict(kind='triangle_edge',weights_numerator=w,denominator=2,vector=None)
 I,N=max(s['independent'],key=lambda x:(len(x[0]),tuple(-i for i in x[0])))
 assert (len(I),len(N)) in ((4,1),(3,2))
 n=[1]*5
 for v in N:n[v]=2*t-1
 assert sum(n)<5*t and all(n[i]+n[j]>=f for (i,j),f in zip(P,B.floors(g,t)))
 return dict(kind='independent',types=list(I),neighbors=list(N),vector=n)

def validate(c,t,g,fs=None):
 assert len(c)==5*t and (fs is None or tuple(fs)==B.floors(g,t))
 assert all(not x or any(x&m==x for m in M) for x in c)
 assert all(r.bit_count()>=f for r,f in zip(B.rows(c),B.floors(g,t)))
 assert B.tau(c)<=4
 return True

def construct(kind,s,t,key,native):
 g=s['G'];c=list(B.source(t));ops=[];states=[tuple(c)];adds=[]
 target=key[0] if kind=='isolated' else (key[2] if kind=='cherry' else key[4]);anchors=[v*t for v in range(5) if v!=target]
 if (t,g) not in native:native[t,g]=B.Native(t,g)
 n=native[t,g];n.check(c)
 if kind!='isolated':parameters(kind,s,t,key,[key[0]*t+1] if kind=='cherry' else [key[0]*t+1,key[2]*t+1],anchors)
 def toggle(x,r,addition=False):
  if addition:adds.append((len(ops),r))
  c[x]^=1<<r;ops.append([x,r]);states.append(tuple(c));n.check(c)
  assert all(c[a]==B.source(t)[a] for a in anchors)
 def shrink(v,keep):
  x=v*t+1
  for r in range(10):
   if c[x]>>r&1 and r!=keep:toggle(x,r)
 def add(v,a,b):toggle(v*t+1,P.index(tuple(sorted((a,b)))),True)
 if kind=='cherry':
  i,a,j=key;assert s['degrees'][i]==s['degrees'][j]==1 and s['neighbors'][i]==s['neighbors'][j]
  shrink(i,P.index(tuple(sorted((i,a)))));add(i,a,j)
 elif kind=='triple':
  i,a,j,b,k=key;assert tuple(key) in s['triples']
  shrink(i,P.index(tuple(sorted((i,a)))))
  if edge(g,a,j):add(i,a,j)
  if edge(g,a,k):add(i,a,k)
  shrink(j,P.index(tuple(sorted((j,b)))))
  if edge(g,b,k):add(j,b,k)
 else:assert target in s['isolated']
 x=target*t
 for r in range(10):
  if c[x]>>r&1:toggle(x,r)
 first=next(i for i,v in enumerate(states) if 0 in v)
 expected=4 if kind=='isolated' else 8 if kind=='cherry' else 10+int(edge(g,key[1],key[2]))+s['degrees'][target]
 assert first==len(ops)==expected and sum(m==0 for m in c)==1
 negatives=[]
 for omit,critical in adds:
  altered=list(B.source(t));failure=None
  for k,(label,r) in enumerate(ops):
   if k==omit:continue
   altered[label]^=1<<r
   if B.rows(altered)[critical].bit_count()<B.floors(g,t)[critical]:failure=k;break
  assert failure is not None and g>>critical&1
  negatives.append([omit,critical,failure])
 emit(['route',kind,g,t,list(key)],dict(ops=ops,states=states,anchors=anchors,omission_rejections=negatives))
 return dict(kind=kind,G=g,t=t,key=list(key),ops=ops,cost=len(ops),first_absent=first,anchors=anchors,states_hash=D(states),final=list(c),globally_optimal=(kind=='isolated' or kind=='cherry' and not s['isolated']),omission_rejections=negatives)

def lower():
 records=[]
 for r,(v,w) in enumerate(P):
  for k in range(5):
   if k in (v,w):continue
   for owner in (v,w):
    for sub in range(1024):
     if sub>>r&1 and sub&M[owner]==sub:
      lost=(M[k]&~sub).bit_count();gained=(sub&~M[k]).bit_count();assert lost>=3 and gained>=1
      records.append([r,k,owner,sub,lost,gained])
 emit(['lower'],records);assert len(records)==480
 return dict(witnesses=len(records),records_hash=D(records),minimum_donor_toggles=min(a[-1]+a[-2] for a in records),minimum_total=8)

def parameters(kind,s,t,key,donors,anchors):
 assert t>=2
 if kind=='cherry':
  assert tuple(key) in s['cherries'];types=(key[0],);target=key[2]
 else:
  assert kind=='triple' and tuple(key) in s['triples'];types=(key[0],key[2]);target=key[4]
 assert donors==[v*t+1 for v in types]
 assert anchors==[v*t for v in range(5) if v!=target]
 assert not set(donors)&set(anchors) and B.tau(tuple(B.source(t)[x] for x in anchors))==4
 return True

def controls():
 g=B.STAR;t=2;s=B.source(t);st=structure(g)
 def rejected(fn,*args):
  try:fn(*args)
  except AssertionError:return True
  return False
 upper=list(s)
 for pair,x in [((0,1),0),((2,3),4),((2,4),5),((3,4),6)]:
  r=P.index(pair);upper=[v|1<<r if k==x else v&~(1<<r) for k,v in enumerate(upper)]
 assert all(any(v&m==v for m in M) for v in upper)
 assert all(r.bit_count()>=f for r,f in zip(B.rows(upper),B.floors(B.K23,t))) and B.tau(upper)==5
 anchors=[v*t for v in range(5) if v!=2]
 bad_ind=structure(sum(1<<P.index(e) for e in ((0,1),(2,3),(2,4))))
 assert bad_ind['neighbors'][0]==(1,) and 3 in bad_ind['neighbors'][2] and 4 in bad_ind['neighbors'][2]
 assert parameters('cherry',st,t,(1,0,2),[3],anchors)
 return dict(fresh_label=rejected(validate,s+(1,),t,g),changed_floor=rejected(validate,s,t,g,(1,)*10),invalid_degree=rejected(parameters,'cherry',st,t,(0,1,2),[1],anchors),invalid_independent=rejected(parameters,'triple',bad_ind,t,(0,1,2,3,4),[1,5],[0,2,4,6]),invalid_donor=rejected(parameters,'cherry',st,t,(1,0,2),[2],anchors),invalid_anchor=rejected(parameters,'cherry',st,t,(1,0,2),[3],[0,1,2,3]),upper_violation=rejected(validate,tuple(upper),t,B.K23))

@lru_cache(None)
def build(fixture=False):
 cycle=sum(1<<P.index(tuple(sorted(e))) for e in [(0,1),(1,2),(2,3),(3,4),(4,0)])
 path=sum(1<<P.index(e) for e in [(0,1),(1,2),(2,3),(3,4)])
 tri=sum(1<<P.index(e) for e in [(0,1),(0,2),(1,2),(3,4)])
 gs=sorted({0,B.STAR,B.K23,B.K23|1,cycle,path,tri}) if fixture else range(1024)
 structures=[structure(g) for g in gs];cases=[]
 for s in structures:
  emit(['structure',s['G']],s)
  for t in ((1,2) if fixture else (1,2,3)):
   graph=B.graph(s['G'],t);static=bool(s['isolated']) or (t>=2 and bool(s['independent']));reachable=static and min(s['degrees'])<=1
   assert static==(graph['minimum']<5*t) and reachable==(graph['accessible_minimum']<5*t)
   cert=static_certificate(s,t)
   if cert['vector'] is not None:assert all(cert['vector'][a]+cert['vector'][b]>=f for (a,b),f in zip(P,B.floors(s['G'],t)))
   if 'weights_numerator' in cert:assert all(sum(cert['weights_numerator'][r] for r,e in enumerate(P) if v in e)==2 for v in range(5))
   cases.append(dict(G=s['G'],t=t,graph=graph,static_spare=static,reachable=reachable,fingerprint=graph['fingerprint'],isolated_types=s['isolated'],certificate=cert))
 if not fixture:
  forbidden=sorted({sum(1<<r for r,(a,b) in enumerate(P) if (a in N)!=(b in N))|extra*(1<<P.index(N)) for N in it.combinations(range(5),2) for extra in (0,1)})
  assert len(forbidden)==20
  for t in (2,3):assert [c['G'] for c in cases if c['t']==t and c['static_spare'] and not c['reachable']]==forbidden
 native={};routes=[]
 for s in structures:
  for t in ((1,2) if fixture else (1,2,3)):
   for i in s['isolated']:routes.append(construct('isolated',s,t,(i,),native))
  for t in ((2,) if fixture else (2,3,4,5)):
   for key in s['cherries']:routes.append(construct('cherry',s,t,key,native))
   for key in s['triples']:routes.append(construct('triple',s,t,key,native))
 summaries=[]
 for (t,g),n in sorted(native.items()):
  emit(['native',t,g],dict(cores=sorted(n.cores),masks=n.masks));summaries.append(dict(t=t,G=g,**n.finish()))
 low=lower();ctrl=controls();assert all(ctrl.values())
 counts=dict(graph_cases=len(cases),structures=len(structures),routes=len(routes),isolated_routes=sum(r['kind']=='isolated' for r in routes),cherry_routes=sum(r['kind']=='cherry' for r in routes),triple_routes=sum(r['kind']=='triple' for r in routes),native_cores=sum(n['native_cores'] for n in summaries),slice_occurrences=sum(n['slice_occurrences'] for n in summaries),hidden_checks=sum(n['hidden_checks'] for n in summaries),lower_witnesses=low['witnesses'])
 return dict(schema='weak-trace-v1',fixture=fixture,structures=structures,cases=cases,routes=routes,native=summaries,lower_bound=low,controls=ctrl,counts=counts,**({'identities':_records} if fixture else {}))
if __name__=='__main__':
 dest=sys.argv[1];identity=dest+'.identities.jsonl.gz'
 with open(identity,'wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as stream:_writer=stream;data=build()
 data['identity_archive_sha256']=hashlib.sha256(open(identity,'rb').read()).hexdigest();open(dest,'w').write(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps(data['counts'],sort_keys=True))
