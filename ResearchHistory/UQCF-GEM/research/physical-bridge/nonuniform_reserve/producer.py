"""Nonuniform source producer: bits, compositions, donor gates, BFS."""
import gzip,hashlib,importlib.util,itertools as it,json,pathlib,sys
from collections import deque
from functools import lru_cache
sp=importlib.util.spec_from_file_location('bit_primitives',pathlib.Path(__file__).resolve().parent.parent/'fingerprint_lock/producer.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
P=B.PAIRS;M=B.maxima();D=B.digest
_writer=None;_records={};_seen=set()
def emit(key,value):
 k=json.dumps(key,separators=(',',':'))
 if _writer is None:_records[k]=value
 elif k not in _seen:_seen.add(k);_writer.write((json.dumps([k,value],separators=(',',':'))+'\n').encode())
def offsets(a):return [sum(a[:i]) for i in range(5)]
def source(a):return tuple(m for m,n in zip(M,a) for _ in range(n))
def floors(g,a):return tuple(a[i]+a[j] if g>>r&1 else 1 for r,(i,j) in enumerate(P))
def structure(g):
 ns=[tuple(j for j in range(5) if j!=i and g>>P.index(tuple(sorted((i,j))))&1) for i in range(5)]
 independent=[]
 for size in range(1,5):
  for I in it.combinations(range(5),size):
   N=tuple(sorted({v for i in I for v in ns[i]}))
   if not set(I)&set(N) and len(I)>len(N):independent.append([I,N])
 cherries=sorted((i,ns[i][0],j) for i in range(5) for j in range(5) if i!=j and len(ns[i])==len(ns[j])==1 and ns[i]==ns[j])
 triples=[]
 if min(map(len,ns))==1:
  for I,N in independent:
   if len(I)!=3 or len(N)!=2:continue
   for i in I:
    if len(ns[i])!=1:continue
    a=ns[i][0];b=next(v for v in N if v!=a)
    for j in I:
     if j!=i and b in ns[j]:triples.append((i,a,j,b,next(k for k in I if k not in (i,j))))
 return dict(G=g,neighbors=ns,degrees=list(map(len,ns)),isolated=[i for i in range(5) if not ns[i]],independent=independent,cherries=cherries,triples=sorted(triples))

@lru_cache(64)
def universe(total,fs):
 vs=tuple(n for n in B.comps(total,6) if all(n[i+1]+n[j+1]>=fs[r] for r,(i,j) in enumerate(P)))
 index={n:k for k,n in enumerate(vs)};edges=[];adj=[[] for _ in vs]
 for u,n in enumerate(vs):
  for i in range(-1,5):
   if not n[i+1]:continue
   for j in range(-1,5):
    if i==j:continue
    if i!=-1 and any(n[i+1]+n[k+1]<=fs[P.index(tuple(sorted((i,k))))] for k in range(5) if k not in (i,j)):continue
    v=list(n);v[i+1]-=1;v[j+1]+=1;v=tuple(v);assert v in index
    z=index[v];edges.append((u,z,i,j));adj[u].append(z);adj[z].append(u)
 groups=[];seen=set()
 for start in range(len(vs)):
  if start in seen:continue
  todo=deque([start]);seen.add(start);group=[]
  while todo:
   u=todo.popleft();group.append(u)
   for v in adj[u]:
    if v not in seen:seen.add(v);todo.append(v)
  groups.append(sorted(group))
 groups.sort();edges.sort();minimum=min(total-v[0] for v in vs);best=[v for v in vs if total-v[0]==minimum]
 return dict(vertices=vs,edges=edges,components=groups,static=best)

def graph(g,a):
 fs=floors(g,a);total=sum(a);u=universe(total,fs);emit(['universe',total,fs],u)
 src=(0,)+tuple(a);index=u['vertices'].index(src);part=next(c for c in u['components'] if index in c)
 emit(['count',g,a],dict(universe=[total,fs],source=src,source_component=part))
 fp=B.fingerprint(source(a),fs,g);isolated=len(part)==1
 assert fp==isolated==(min(structure(g)['degrees'])>=2)
 return dict(G=g,profile=list(a),original_floors=list(fs),source=list(src),vertices=len(u['vertices']),edges=len(u['edges']),components=len(u['components']),vertices_hash=D(u['vertices']),edges_hash=D(u['edges']),components_hash=D(u['components']),static_hash=D(u['static']),minimum=total-u['static'][0][0],source_component_hash=D(part),accessible_minimum=min(total-u['vertices'][k][0] for k in part),count_isolated=isolated,fingerprint=fp)

class Native:
 def __init__(self,g,a):
  self.g=g;self.a=a;self.s=source(a);self.fs=floors(g,a);self.cores=set();self.occurrences=0;rr=B.rows(self.s);self.masks=[]
  for hidden in range(1024):
   exposed=1023^hidden;common=(1<<len(self.s))-1
   for r in range(10):
    if exposed>>r&1:common&=rr[r]
   if exposed and not common:self.masks.append(hidden)
 def check(self,c):
  c=tuple(c);self.occurrences+=1
  if c in self.cores:return
  validate(c,self.a,self.g);self.cores.add(c)
 def finish(self):
  h=hashlib.sha256();checks=0
  for c in sorted(self.cores):
   rr=B.rows(c);intersections=[(1<<len(c))-1]*1024
   for exposed in range(1,1024):
    bit=exposed&-exposed;intersections[exposed]=intersections[exposed^bit]&rr[bit.bit_length()-1]
   prefix=('['+json.dumps(c,separators=(',',':'))+',').encode()
   for hidden in self.masks:
    assert intersections[1023^hidden]==0;h.update(prefix+str(hidden).encode()+b']\n');checks+=1
  return dict(native_cores=len(self.cores),slice_occurrences=self.occurrences,hidden_masks=len(self.masks),hidden_checks=checks,hidden_hash=h.hexdigest())

def validate(c,a,g,fs=None):
 assert len(a)==5 and all(isinstance(n,int) and n>=1 for n in a)
 assert len(c)==sum(a) and (fs is None or tuple(fs)==floors(g,a))
 assert all(not x or any(x&m==x for m in M) for x in c)
 assert all(r.bit_count()>=f for r,f in zip(B.rows(c),floors(g,a)))
 assert B.tau(c)<=4
 return True

def parameters(kind,s,a,key,exclude=None):
 if kind=='isolated':changed=(key[0],);target=key[0];assert target in s['isolated']
 elif kind=='cherry':assert tuple(key) in s['cherries'];changed=(key[0],key[2]);target=key[2]
 else:assert kind=='triple' and tuple(key) in s['triples'];changed=(key[0],key[2],key[4]);target=key[4]
 single=[v for v in changed if a[v]==1];assert len(single)<=1
 excluded=single[0] if single else target
 assert exclude is None or exclude==excluded
 off=offsets(a);anchors=[off[v] for v in range(5) if v!=excluded];labels={v:off[v]+int(v!=excluded) for v in changed}
 assert all(x<off[v]+a[v] for v,x in labels.items()) and not set(labels.values())&set(anchors)
 assert B.tau(tuple(source(a)[x] for x in anchors))==4
 return excluded,target,anchors,labels

def route(kind,s,a,key,n):
 excluded,target,anchors,labels=parameters(kind,s,a,key);c=list(n.s);ops=[];states=[tuple(c)];adds=[];n.check(c)
 def edit(x,r,add=False):
  if add:assert not c[x]>>r&1;adds.append((len(ops),r))
  else:assert c[x]>>r&1
  c[x]^=1<<r;ops.append([x,r]);states.append(tuple(c));n.check(c);assert all(c[z]==n.s[z] for z in anchors)
 def shrink(v,w):
  keep=P.index(tuple(sorted((v,w))))
  for r in range(10):
   if c[labels[v]]>>r&1 and r!=keep:edit(labels[v],r)
 def add(v,x,y):edit(labels[v],P.index(tuple(sorted((x,y)))),True)
 if kind=='cherry':i,h,j=key;shrink(i,h);add(i,h,j)
 elif kind=='triple':
  i,h,j,b,k=key;shrink(i,h)
  for v in (j,k):
   if v in s['neighbors'][h]:add(i,h,v)
  shrink(j,b)
  if k in s['neighbors'][b]:add(j,b,k)
 for r in range(10):
  if c[labels[target]]>>r&1:edit(labels[target],r)
 first=next(k for k,c0 in enumerate(states) if 0 in c0);cost=4 if kind=='isolated' else 8 if kind=='cherry' else 10+int(key[2] in s['neighbors'][key[1]])+s['degrees'][target]
 assert first==len(ops)==cost and sum(x==0 for x in c)==1
 bad=[]
 for omit,critical in adds:
  altered=list(n.s);failure=None
  for step,(x,r) in enumerate(ops):
   if step==omit:continue
   altered[x]^=1<<r
   if B.rows(altered)[critical].bit_count()<n.fs[critical]:failure=step;break
  assert failure is not None and s['G']>>critical&1;bad.append([omit,critical,failure])
 emit(['route',kind,s['G'],a,key],dict(ops=ops,states=states,anchors=anchors,excluded_type=excluded,labels=sorted(labels.items()),omission_rejections=bad))
 donor_types=() if kind=='isolated' else (key[0],) if kind=='cherry' else (key[0],key[2])
 return dict(kind=kind,G=s['G'],profile=list(a),key=list(key),excluded_type=excluded,target_type=target,anchors=anchors,labels=sorted(labels.items()),ops=ops,cost=cost,first_absent=first,states_hash=D(states),final=list(c),globally_optimal=kind=='isolated' or kind=='cherry' and not s['isolated'],singleton_donor=any(a[v]==1 for v in donor_types),omission_rejections=bad)

def lower():
 records=[]
 for r,(v,w) in enumerate(P):
  for k in range(5):
   if k in (v,w):continue
   for owner in (v,w):
    for sub in range(1024):
     if sub>>r&1 and sub&M[owner]==sub:
      loss=(M[k]&~sub).bit_count();gain=(sub&~M[k]).bit_count();assert loss>=3 and gain>=1;records.append([r,k,owner,sub,loss,gain])
 assert len(records)==480;emit(['lower'],records)
 return dict(witnesses=480,records_hash=D(records),minimum_donor_toggles=min(z[-1]+z[-2] for z in records),minimum_total=8)

def controls():
 def reject(fn,*args):
  try:fn(*args)
  except AssertionError:return True
  return False
 g=B.STAR;a=(1,1,2,1,1);st=structure(g);s=source(a)
 assert parameters('cherry',st,a,(1,0,2))[0]==1
 upper=list(source((2,)*5))
 for pair,x in [((0,1),0),((2,3),4),((2,4),5),((3,4),6)]:
  r=P.index(pair);upper=[v|1<<r if k==x else v&~(1<<r) for k,v in enumerate(upper)]
 assert all(any(v&m==v for m in M) for v in upper) and all(r.bit_count()>=f for r,f in zip(B.rows(upper),floors(B.K23,(2,)*5))) and B.tau(upper)==5
 partial=sum(1<<P.index(e) for e in ((0,1),(1,2),(2,3),(1,4),(3,4)));ps=structure(partial);key=(0,1,2,3,4);assert key in ps['triples']
 return dict(two_singleton_cherry=reject(parameters,'cherry',st,(1,)*5,(1,0,2)),insufficient_triple=reject(parameters,'triple',ps,(1,1,2,1,1),key),wrong_exclusion=reject(parameters,'cherry',st,a,(1,0,2),2),fresh_label=reject(validate,s+(1,),a,g),wrong_floor=reject(validate,s,a,g,(2,)*10),invalid_profile=reject(validate,s,(0,1,2,1,1),g),upper_violation=reject(validate,tuple(upper),(2,)*5,B.K23))

@lru_cache(None)
def build(fixture=False):
 partial=sum(1<<P.index(e) for e in ((0,1),(1,2),(2,3),(1,4),(3,4)))
 gs=sorted({0,B.STAR,B.K23,B.K23|1,partial,1023}) if fixture else range(1024)
 profiles=[(1,)*5,(2,)*5,(1,1,2,1,2),(1,1,2,1,1)] if fixture else list(it.product((1,2),repeat=5))
 structures=[structure(g) for g in gs];cases=[];routes=[];summaries=[]
 for st in structures:
  g=st['G'];emit(['structure',g],st)
  for a in profiles:
   eligible=lambda I:sum(a[v]==1 for v in I)<=1
   cherries=[key for key in st['cherries'] if eligible((key[0],key[2]))]
   triples=[list(I) for I,N in st['independent'] if len(I)==3 and len(N)==2 and eligible(I)]
   witnesses=[]
   for I,N in st['independent']:
    if eligible(I):
     vector=[a[v]-int(v in I)+int(v in N) for v in range(5)]
     assert sum(vector)<sum(a) and sum(v==0 for v in vector)<=1 and all(vector[i]+vector[j]>=f for (i,j),f in zip(P,floors(g,a)))
     witnesses.append(dict(types=list(I),neighbors=list(N),vector=vector))
   emit(['witnesses',g,a],witnesses)
   cg=graph(g,a);static=bool(st['isolated'] or cherries or triples);reachable=static and min(st['degrees'])<=1
   assert static==(cg['minimum']<sum(a)) and reachable==(cg['accessible_minimum']<sum(a)) and static==bool(witnesses)
   if static and not reachable:assert any(len(I)==3 and len(N)==2 and all(len(st['neighbors'][i])==2 for i in I) and eligible(I) for I,N in st['independent'])
   cases.append(dict(G=g,profile=list(a),graph=cg,static_spare=static,reachable=reachable,fingerprint=cg['fingerprint'],isolated_types=st['isolated'],eligible_cherries=cherries,eligible_triples=triples,witnesses=witnesses))
   n=Native(g,a)
   for i in st['isolated']:routes.append(route('isolated',st,a,(i,),n))
   for key in cherries:routes.append(route('cherry',st,a,key,n))
   for key in st['triples']:
    if eligible((key[0],key[2],key[4])):routes.append(route('triple',st,a,key,n))
   if n.cores:
    emit(['native',g,a],dict(cores=sorted(n.cores),masks=n.masks));summaries.append(dict(G=g,profile=list(a),**n.finish()))
 if not fixture:
  expected=set()
  for N in it.combinations(range(5),2):
   I=set(range(5))-set(N);cross=sum(1<<r for r,e in enumerate(P) if len(set(e)&set(N))==1)
   for extra in (0,1):
    g=cross|extra*(1<<P.index(N))
    for a in profiles:
     if sum(a[v]>1 for v in I)>=2:expected.add((g,tuple(a)))
  observed={(c['G'],tuple(c['profile'])) for c in cases if c['static_spare'] and not c['reachable']}
  assert observed==expected and len(expected)==320
 low=lower();ctrl=controls();assert all(ctrl.values())
 counts=dict(structures=len(structures),profiles=len(profiles),graph_cases=len(cases),routes=len(routes),isolated_routes=sum(r['kind']=='isolated' for r in routes),cherry_routes=sum(r['kind']=='cherry' for r in routes),triple_routes=sum(r['kind']=='triple' for r in routes),singleton_donor_routes=sum(r['singleton_donor'] for r in routes),native_cores=sum(n['native_cores'] for n in summaries),slice_occurrences=sum(n['slice_occurrences'] for n in summaries),hidden_checks=sum(n['hidden_checks'] for n in summaries),lower_witnesses=480)
 return dict(schema='nonuniform-reserve-v1',fixture=fixture,structures=structures,profiles=[list(a) for a in profiles],cases=cases,routes=routes,native=summaries,lower_bound=low,controls=ctrl,counts=counts,**({'identities':_records} if fixture else {}))
if __name__=='__main__':
 dest=sys.argv[1];identity=dest+'.identities.jsonl.gz'
 with open(identity,'wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as stream:_writer=stream;data=build()
 data['identity_archive_sha256']=hashlib.sha256(pathlib.Path(identity).read_bytes()).hexdigest();pathlib.Path(dest).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');print(json.dumps(data['counts'],sort_keys=True))
