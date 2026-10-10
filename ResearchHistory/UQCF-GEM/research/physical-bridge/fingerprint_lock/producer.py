"""Frozen fingerprint campaign: bit footprints, donor edges, BFS components."""
import gzip,hashlib,itertools as it,json,sys
from collections import deque
from functools import lru_cache
_writer=None
_seen=set()
_fixture_records={}
def emit(key,value):
 key=json.dumps(key,separators=(',',':'))
 if _writer is not None:
  if key not in _seen:
   _seen.add(key);_writer.write((json.dumps([key,value],separators=(',',':'))+'\n').encode())
 else:_fixture_records[key]=value
PAIRS=tuple(it.combinations(range(5),2))
K23=sum(1<<r for r,(i,j) in enumerate(PAIRS) if i<2<=j)
STAR=sum(1<<r for r,(i,j) in enumerate(PAIRS) if i==0)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def comps(total,k):
 if k==1:yield (total,);return
 for n in range(total+1):
  for rest in comps(total-n,k-1):yield (n,)+rest
@lru_cache(None)
def maxima():return tuple(sum(1<<r for r,e in enumerate(PAIRS) if i in e) for i in range(5))
def source(t):return tuple(m for m in maxima() for _ in range(t))
def floors(g,t):return tuple(2*t if g>>r&1 else 1 for r in range(10))
def rows(cols):return tuple(sum(1<<x for x,m in enumerate(cols) if m>>r&1) for r in range(10))
def tau(cols,roots=1023):
 for k in range(6):
  for sub in it.combinations(cols,k):
   union=0
   for m in sub:union|=m
   if union&roots==roots:return k
 return 6

def fingerprint(cols,fs,locked):
 rr=rows(cols);ms=tuple(m for m in set(cols) if m and not any(m!=n and m&n==m for n in cols))
 if any(rr[r].bit_count()!=fs[r] for r in range(10) if locked>>r&1):return False
 for c in cols:
  l=c&locked;owners=[m for m in ms if l&m==l]
  if not l or len(owners)!=1 or owners[0]&locked!=l:return False
 return True

def graph(g,t):
 fs=floors(g,t);vs=tuple(n for n in comps(5*t,6) if all(n[i+1]+n[j+1]>=fs[r] for r,(i,j) in enumerate(PAIRS)))
 index={n:k for k,n in enumerate(vs)};edges=[];adj=[[] for _ in vs]
 for a,n in enumerate(vs):
  for i in range(-1,5):
   if not n[i+1]:continue
   for j in range(-1,5):
    if j==i or (i==-1 and j==-1):continue
    if i!=-1 and not all(n[i+1]+n[l+1]>fs[PAIRS.index(tuple(sorted((i,l))))] for l in range(5) if l!=i and l!=j):continue
    v=list(n);v[i+1]-=1;v[j+1]+=1;v=tuple(v)
    assert v in index
    b=index[v];edges.append((a,b,i,j));adj[a].append(b);adj[b].append(a)
 edges=sorted(edges);seen=set();cc=[]
 for a in range(len(vs)):
  if a in seen:continue
  seen.add(a);todo=deque([a]);part=[]
  while todo:
   u=todo.popleft();part.append(u)
   for v in adj[u]:
    if v not in seen:seen.add(v);todo.append(v)
  cc.append(sorted(part))
 cc.sort();src=(0,)+(t,)*5;s=index[src];part=next(c for c in cc if s in c)
 degree=[sum(g>>r&1 for r,e in enumerate(PAIRS) if i in e) for i in range(5)]
 fp=fingerprint(source(t),fs,g);isolated=len(part)==1
 assert fp==isolated==(min(degree)>=2)
 minimum=min(5*t-n[0] for n in vs);capacities=[n for n in vs if 5*t-n[0]==minimum]
 emit(['count',g,t],dict(vertices=vs,edges=edges,components=cc,static=capacities,source_component=part))
 local=None
 if fp and g!=1023:
  r=next(r for r in range(10) if not g>>r&1);x=PAIRS[r][0]*t;c=list(source(t));c[x]^=1<<r
  assert rows(c)[r].bit_count()>=fs[r] and tau(c)==4
  local=[x,r]
 return dict(G=g,t=t,original_floors=list(fs),source=list(src),vertices=len(vs),edges=len(edges),components=len(cc),vertices_hash=digest(vs),edges_hash=digest(edges),components_hash=digest(cc),source_component_hash=digest(part),minimum=minimum,static_hash=digest(capacities),accessible_minimum=min(5*t-vs[a][0] for a in part),isolated=isolated,fingerprint=fp,local_deletion=local)

class Native:
 def __init__(self,t,g):
  self.t=t;self.g=g;self.s=source(t);self.fs=floors(g,t);self.original=rows(self.s);self.ms=maxima();self.cores=set();self.occurrences=0
  self.masks=[]
  for hidden in range(1024):
   exposed=[r for r in range(10) if not hidden>>r&1]
   common=(1<<(5*t))-1
   for r in exposed:common&=self.original[r]
   if exposed and not common:self.masks.append(hidden)
 def check(self,cols):
  cols=tuple(cols);self.occurrences+=1
  if cols in self.cores:return
  assert len(cols)==5*self.t
  assert all(c==0 or any(c&m==c for m in self.ms) for c in cols)
  rr=rows(cols);assert all(a.bit_count()>=f for a,f in zip(rr,self.fs))
  assert tau(cols)<=4
  self.cores.add(cols)
 def finish(self):
  h=hashlib.sha256();checks=0
  for cols in sorted(self.cores):
   rr=rows(cols);prefix=('['+json.dumps(cols,separators=(',',':'))+',').encode()
   # A hidden label yields 1+tau(exposed). Original masks exclude
   # exposed tau0/1. Domination prevents any new exposed singleton cover.
   # Core <=4 supplies the upper bound; actual exposed intersections supply >=3.
   for hidden in self.masks:
    common=(1<<(5*self.t))-1
    for r in range(10):
     if not hidden>>r&1:common&=rr[r]
    assert common==0
    h.update(prefix+str(hidden).encode()+b']\n');checks+=1
  return dict(native_cores=len(self.cores),slice_occurrences=self.occurrences,hidden_masks=len(self.masks),hidden_checks=checks,hidden_hash=h.hexdigest())

def target(t,g,vector):
 n=Native(t,g);cols=tuple(m for m,k in zip(maxima(),vector) for _ in range(k))+(0,)*(5*t-sum(vector));n.check(cols)
 assert tau(cols)==4
 absent=sum(c==0 for c in cols);same=all((c&g)==(s&g) for c,s in zip(cols,n.s))
 return dict(t=t,columns=list(cols),absent=absent,in_locked_component=same,**n.finish())

def raw(t):
 n=Native(t,K23);original=n.original;unlocked=[r for r in range(10) if not K23>>r&1];domains=[]
 for r in unlocked:
  bits=[x for x in range(5*t) if original[r]>>x&1]
  domains.append(tuple(sum(1<<x for k,x in enumerate(bits) if sub>>k&1) for sub in range(1,1<<len(bits))))
 # Enumerate actual four-label covers of the six locked roots.
 covers=[sum(1<<x for x in comb) for comb in it.combinations(range(5*t),4) if all(any(n.s[x]>>r&1 for x in comb) for r in range(10) if K23>>r&1)]
 accepted=[];columns={}
 for v in it.product(*domains):
  if not any(all(c&a for a in v) for c in covers):continue
  rr=list(original)
  for r,a in zip(unlocked,v):rr[r]=a
  cols=tuple(sum(1<<r for r,a in enumerate(rr) if a>>x&1) for x in range(5*t))
  assert all(cols);accepted.append(v);columns[v]=cols
 accepted.sort();index={v:a for a,v in enumerate(accepted)};edges=[]
 for a,v in enumerate(accepted):
  for k,r in enumerate(unlocked):
   for x in range(5*t):
    if original[r]>>x&1:
     w=list(v);w[k]^=1<<x;w=tuple(w)
     if w in index and a<index[w]:edges.append((a,index[w],x,r))
 edges.sort();h=hashlib.sha256()
 for v in accepted:
  cols=columns[v];removed=[(x,r) for x in range(5*t) for r in range(10) if n.s[x]>>r&1 and not cols[x]>>r&1]
  c=list(n.s);path=[tuple(c)];n.check(c)
  for x,r in removed:c[x]^=1<<r;n.check(c);path.append(tuple(c))
  assert tuple(c)==cols
  for state in reversed(path):n.check(state)
  emit(['lift',t,list(v)],[v,removed,path,list(reversed(path))])
  h.update(json.dumps([v,removed,path,list(reversed(path))],separators=(',',':')).encode()+b'\n')
 # Complete edge connectivity checked independently too.
 adj=[[] for _ in accepted]
 for a,b,*_ in edges:adj[a].append(b);adj[b].append(a)
 seen={0};todo=[0]
 while todo:
  for b in adj[todo.pop()]:
   if b not in seen:seen.add(b);todo.append(b)
 assert len(seen)==len(accepted)
 emit(['raw',t],dict(vertices=accepted,edges=edges,components=[list(range(len(accepted)))],cores=sorted(n.cores),hidden_masks=n.masks))
 return dict(t=t,candidates=len(domains[0])**4,vertices=len(accepted),edges=len(edges),components=1,vertices_hash=digest(accepted),edges_hash=digest(edges),components_hash=digest([list(range(len(accepted)))]),lifts_hash=h.hexdigest(),**n.finish())

def route(t,leaves=None,batch=False):
 n=Native(t,STAR);c=list(n.s);anchors=[i*t for i in range(1,5)];ops=[];states=[list(c)];n.check(c)
 def toggle(x,r):
  c[x]^=1<<r;ops.append([x,r]);states.append(list(c));n.check(c)
  assert all(c[a]==maxima()[i] for i,a in enumerate(anchors,1))
 def move(x,i):
  for r in range(10):
   if maxima()[i]>>r&1 and not maxima()[0]>>r&1:toggle(x,r)
  for r in range(10):
   if maxima()[0]>>r&1 and not maxima()[i]>>r&1:toggle(x,r)
 if batch:
  moved=[]
  for i in range(1,5):
   for k in range(1,t):x=i*t+k;move(x,i);moved.append(x)
  donors=sorted(list(range(t))+moved)[:3*t-3]
 else:
  for i in leaves:move(i*t+1,i)
  donors=[0]
 for x in donors:
  for r in range(10):
   if c[x]>>r&1:toggle(x,r)
 absent=[k for k,state in enumerate(states) if 0 in state]
 assert len(ops)==(36*(t-1) if batch else 16)
 assert sum(bool(m) for m in c)==(2*t+3 if batch else 5*t-1)
 if not batch:assert absent[0]==16
 return dict(t=t,leaves=list(leaves or []),anchors=anchors,ops=ops,states_hash=digest(states),final=list(c),first_absent=absent[0],**n.finish())

def controls():
 s=source(2);c=list(s)
 for r,who in [(PAIRS.index((0,1)),0),(PAIRS.index((2,3)),4),(PAIRS.index((2,4)),5),(PAIRS.index((3,4)),6)]:
  for x in range(10):c[x]=c[x]|1<<r if x==who else c[x]&~(1<<r)
 assert tau(c)==5 and all(a.bit_count()>=f for a,f in zip(rows(c),floors(K23,2)))
 # Generic four-root control uses padded ten-root representation ONLY for fingerprint predicate.
 a=(9,10,4,1,2);b=(1,2,4,9,10);fs=(2,2,1,2)+(0,)*6
 assert fingerprint(a,fs,7)
 path=[a];cur=list(a);ops=[(3,3),(4,3),(0,3),(1,3)]
 for x,r in ops:
  cur[x]^=1<<r;assert tau(cur,15)==3;assert all(rows(cur)[r].bit_count()>=fs[r] for r in range(4));path.append(tuple(cur))
 assert tuple(cur)==b and sum((x^y).bit_count() for x,y in zip(a,b))==4
 originalmax=(9,10,4)
 def guarded(c,current_floors=fs):
  assert len(c)==len(a) and current_floors==fs
  assert all(not x or any(x&m==x for m in originalmax) for x in c)
  assert all((x&7)==(y&7) for x,y in zip(c,a))
  assert all(rows(c)[r].bit_count()>=fs[r] for r in range(4)) and tau(c,15)<=4
  return True
 masks=[hidden for hidden in range(16) if min(tau(a,15),1+tau(a,15^hidden))>=3]
 hh=hashlib.sha256();join_checks=0
 for c0 in path+list(reversed(path)):
  guarded(c0)
 for c0 in sorted(set(path)):
  for hidden in masks:
   assert 3<=min(tau(c0,15),1+tau(c0,15^hidden))<=4
   hh.update(json.dumps([c0,hidden],separators=(',',':')).encode()+b'\n');join_checks+=1
 def rejected(c,f=fs):
  try:guarded(c,f)
  except AssertionError:return True
  return False
 fresh_rejected=rejected(a+(1,));floor_rejected=rejected(a,(1,2,1,2)+(0,)*6)
 assert not fingerprint(a+(0,),fs,7)
 # Source K=all four roots is saturated yet helper can safely gain rootx.
 assert rows(path[1])[3].bit_count()==3 and guarded(path[1])
 emit(['join'],dict(states=path,reverse=list(reversed(path)),hidden_masks=masks))
 incomplete=not fingerprint(a,fs,15);fresh=not any(1024&m==1024 for m in maxima())
 rejections=dict(empty=not fingerprint(source(1),floors(K23,1),0),nonunique=not fingerprint(source(1),floors(STAR,1),STAR),incomplete=incomplete,nonsaturated=not fingerprint(a,(1,2,1,2)+(0,)*6,7),fresh_label=fresh_rejected,floor_change=floor_rejected,empty_original_label=not fingerprint(a+(0,),fs,7))
 assert all(rejections.values())
 return dict(upper5=tau(c),upper5_columns=c,join_cost=4,join_ops=ops,join_states_hash=digest(path),join_reverse_hash=digest(list(reversed(path))),join_hidden_checks=join_checks,join_hidden_hash=hh.hexdigest(),join_native_cores=len(set(path)),join_slice_occurrences=2*len(path),rejections=rejections,locked_addition_safe=True)

@lru_cache(None)
def build(fixture=False):
 gs=[0,K23,STAR,1023] if fixture else range(1024);ts=[1] if fixture else [1,2]
 graphs=[graph(g,t) for g in gs for t in ts]
 locked=[];stars=[]
 for t in ([1] if fixture else range(1,6)):
  g=graph(K23,t);assert g['minimum']==4*t+1 and g['isolated']
  z=target(t,K23,(2*t-1,2*t-1,1,1,1));assert z['absent']==t-1 and z['in_locked_component']==(t==1)
  locked.append(dict(t=t,minimum=g['minimum'],graph=g,target=z,anchored_rejections=[[x,next(r for r in range(10) if s>>r&1 and K23>>r&1)] for x,s in enumerate(source(t))]))
 for t in ([2] if fixture else range(1,6)):
  g=graph(STAR,t);assert g['minimum']==2*t+3
  stars.append(dict(t=t,minimum=g['minimum'],graph=g,anchored_rejections=[[x,next(r for r in range(10) if s>>r&1 and STAR>>r&1)] for x,s in enumerate(source(t))]))
 raws=[raw(t) for t in ([1] if fixture else [1,2])]
 routes=[route(t,(i,j)) for t in ([2] if fixture else range(2,6)) for i in range(1,5) for j in range(1,5) if i!=j]
 batches=[route(t,batch=True) for t in ([2] if fixture else range(2,6))]
 natives=raws+routes+batches+[x['target'] for x in locked]
 control=controls()
 counts=dict(graph_cases=len(graphs),raw_vertices=sum(x['vertices'] for x in raws),first_routes=len(routes),batches=len(batches),hidden_checks=sum(x['hidden_checks'] for x in natives)+control['join_hidden_checks'],slice_occurrences=sum(x['slice_occurrences'] for x in natives)+control['join_slice_occurrences'])
 return dict(schema='fingerprint-lock-v1',fixture=fixture,graphs=graphs,locked=locked,stars=stars,raw=raws,routes=routes,batches=batches,controls=control,counts=counts,**({'identities':_fixture_records} if fixture else {}))
if __name__=='__main__':
 identity_path=sys.argv[1]+'.identities.jsonl.gz'
 with open(identity_path,'wb') as identity_file:
  with gzip.GzipFile(filename='',mode='wb',fileobj=identity_file,mtime=0) as stream:
   _writer=stream;data=build()
 data['identity_archive_sha256']=hashlib.sha256(open(identity_path,'rb').read()).hexdigest()
 open(sys.argv[1],'w').write(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps(data['counts'],sort_keys=True))
