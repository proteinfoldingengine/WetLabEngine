"""Source-escape producer: bit submasks and exact union covers."""
if not __debug__:raise RuntimeError('source-escape requires assertions enabled')
import gzip,hashlib,itertools as it,json,pathlib,sys
from functools import lru_cache


def carrier(name):
 k={'K4':4,'C5':5,'K5':5,'K6-minus45':6,'K5-minus34':5,'K4-leaf':5,'K23-K2':7}[name]
 H=list(it.combinations(range(k),2))
 if name=='C5':H=[(0,1),(0,4),(1,2),(2,3),(3,4)]
 if name=='K6-minus45':H.remove((4,5))
 if name=='K5-minus34':H.remove((3,4))
 if name=='K4-leaf':H=sorted(list(it.combinations(range(4),2))+[(0,4)])
 if name=='K23-K2':H=[(u,v) for u in (0,1) for v in (2,3,4)]+[(5,6)]
 return k,H


def sources(fixture=False):
 if fixture:
  specs=[('pinned','K6-minus45','cross',[1,1,1,2,1,1]),('duplicate','K6-minus45','cross',[2,1,1,2,1,1]),('k2','K23-K2','full',[2]*7),('nonminimum','K5-minus34','isolate0',[1]*5),('star','K5','star',[1]*5),('locked','K5','cross',[2]*5),('leaf_empty','K4-leaf','empty',[1]*5),('leaf_full','K4-leaf','full',[1]*5)]
  out=[]
  for name,fam,kind,a in specs:
   k,H=carrier(fam)
   if kind=='full':G=H
   elif kind=='empty':G=[]
   elif kind=='isolate0':G=[e for e in H if 0 not in e]
   elif kind=='star':G=[e for e in H if 0 in e]
   elif fam=='K6-minus45':G=[(u,v) for u in (1,2) for v in (3,4,5)]
   else:G=[(u,v) for u in (0,1) for v in (2,3,4)]
   out.append(dict(family=fam,H=[list(e) for e in H],G=[list(e) for e in G],a=a,name=name))
  return out
 out=[]
 for fam in ('K4','C5','K5','K6-minus45','K5-minus34','K4-leaf','K23-K2'):
  k,H=carrier(fam)
  if fam in ('K4','C5','K4-leaf'):gs=[[e for r,e in enumerate(H) if g>>r&1] for g in range(1<<len(H))]
  elif fam=='K23-K2':gs=[H]
  else:
   gs=[[],H]+[[e for e in H if v not in e] for v in range(k)]
   if fam=='K5':
    cross=[(u,v) for u in (0,1) for v in (2,3,4)];gs += [cross,sorted(cross+[(0,1)])]
   if fam=='K6-minus45':gs += [[(u,v) for u in (1,2) for v in (3,4,5)]]
  for G in gs:
   for a in it.product((1,2),repeat=k):out.append(dict(family=fam,H=[list(e) for e in H],G=[list(e) for e in G],a=list(a)))
 return out


@lru_cache(maxsize=200000)
def tau(masks,full):
 masks=tuple(sorted(set(masks)-{0}))
 for n in range(len(masks)+1):
  for selection in it.combinations(masks,n):
   u=0
   for m in selection:u|=m
   if u==full:return n
 return len(masks)+1


def record(s):
 H=s['H'];G=s['G'];a=s['a'];k=len(a);A=sum(a);full=(1<<len(H))-1
 M=[sum(1<<r for r,e in enumerate(H) if v in e) for v in range(k)]
 types=[v for v,n in enumerate(a) for _ in range(n)];src=[M[v] for v in types]
 fs=[a[u]+a[v] if [u,v] in G else 1 for u,v in H]
 cs=[list(C) for n in range(5) for C in it.combinations(range(k),n) if all(u in C or v in C for u,v in H)]
 B=[[C for C in cs if v not in C] for v in range(k)]
 traces=[[r for r,e in enumerate(H) if v in e and e in G] for v in range(k)]
 V=[v for v in range(k) if not traces[v] and (a[v]>1 or B[v])]
 X=[]
 for v in range(k):
  for w in range(k):
   edge=sorted((v,w))
   if edge not in H:continue
   r=H.index(edge)
   for z in range(k):
    if len({v,w,z})==3 and sorted((w,z)) in H and set(traces[v])<={r} and (a[v]>1 or B[v]):X.append([v,w,z])
 lock=all(len(traces[v])>=2 or a[v]==1 and not B[v] for v in range(k))
 evaluations=[];lookup={}
 def evaluate(v,m):
  key=(v,m)
  if key in lookup:return lookup[key]
  state=src.copy();state[types.index(v)]=m
  counts=[sum(bool(t>>r&1) for t in state) for r in range(len(H))]
  dom=all(any(t&star==t for star in M) for t in state)
  hit=tau(tuple(sorted(state)),full);palette=len(state)==A and all(0<=t<=full for t in state)
  floor_ok=all(c>=f for c,f in zip(counts,fs));safe=palette and dom and floor_ok and hit<=4
  i=len(evaluations);lookup[key]=i;evaluations.append([v,m,palette,dom,counts,hit,floor_ok,safe]);return i
 vacancies=[];candidates=[];observed=set()
 for x,v in enumerate(types):
  ev=evaluate(v,0);safe=evaluations[ev][-1];vacancies.append([x,v,ev,safe])
  if safe:observed.add(('V',x,0,-1))
  subsets=[];f=M[v]
  while f:subsets.append(f);f=(f-1)&M[v]
  for F in sorted(subsets):
   pre=evaluate(v,F)
   for r in range(len(H)):
    if M[v]>>r&1:continue
    post=evaluate(v,F|1<<r);ok=evaluations[pre][-1] and evaluations[post][-1]
    candidates.append([x,v,F,r,pre,post,ok])
    if ok:observed.add(('X',x,F,r))
 expected=set();routes=[];states=set();occ=0
 for x,v in enumerate(types):
  certificates=[('V',None,None)] if v in V else []
  certificates += [('X',w,z) for vv,w,z in X if vv==v]
  for kind,w,z in certificates:
   keep=0 if kind=='V' else 1<<H.index(sorted((v,w)))
   add=-1 if kind=='V' else H.index(sorted((w,z)))
   expected.add((kind,x,keep,add));state=src.copy();slices=[state.copy()];ops=[]
   for r in range(len(H)):
    if M[v]>>r&1 and not keep>>r&1:state[x]&=~(1<<r);ops.append([x,r,0]);slices.append(state.copy())
   if kind=='X':state[x]|=1<<add;ops.append([x,add,1]);slices.append(state.copy())
   for i,st in enumerate(slices):
    assert evaluations[evaluate(v,st[x])][-1]
    assert all(t==src[j] for j,t in enumerate(st) if j!=x)
    event=any(t==0 or t&~src[j] for j,t in enumerate(st))
    assert event==(i==len(slices)-1)
    if kind=='X':assert all(st)
    states.add(tuple(st));occ+=1
   assert len(ops)==M[v].bit_count()
   routes.append(dict(kind=kind,label=x,type=v,w=w,z=z,ops=ops,states=slices,event_index=len(ops),cost=len(ops)))
 assert observed==expected
 masks=[h for h in range(full+1) if full^h and all((full^h)&~m for m in M)]
 pbits=sum(1<<(full^h) for h in masks)
 failures={}
 for m in {m for st in states for m in st}:
  bits=1;sub=m
  while sub:bits|=1<<sub;sub=(sub-1)&m
  failures[m]=bits&pbits
 for st in states:assert not any(failures[m] for m in st)
 assert not lock or not expected
 return dict(source=s,floors=fs,covers=cs,B=B,traces=traces,V=V,X=X,cover_lock=lock,escape=bool(expected),
             evaluations=evaluations,vacancies=vacancies,candidates=candidates,routes=routes,states=[list(st) for st in sorted(states)],
             slice_occurrences=occ,protected_masks=masks,hidden_checks=len(states)*len(masks))


def build(fixture=False,writer=None):
 records=[];hashes=[];counts=dict(sources=0,candidates=0,vacancy_candidates=0,routes=0,slice_occurrences=0,distinct_states=0,hidden_checks=0,escape_sources=0)
 for s in sources(fixture):
  r=record(s);line=json.dumps(r,sort_keys=True,separators=(',',':'))+'\n';hashes.append(hashlib.sha256(line.encode()).hexdigest())
  if writer is None:records.append(r)
  else:writer.write(line.encode())
  for key,n in [('sources',1),('candidates',len(r['candidates'])),('vacancy_candidates',len(r['vacancies'])),('routes',len(r['routes'])),('slice_occurrences',r['slice_occurrences']),('distinct_states',len(r['states'])),('hidden_checks',r['hidden_checks']),('escape_sources',int(r['escape']))]:counts[key]+=n
 return dict(schema='source-escape-v1',fixture=fixture,counts=counts,record_sha256=hashes,**({'records':records} if writer is None else {}))

if __name__=='__main__':
 path=pathlib.Path(sys.argv[1]);ids=str(path)+'.identities.jsonl.gz'
 with open(ids,'wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as writer:data=build(writer=writer)
 data['identity_archive_sha256']=hashlib.sha256(pathlib.Path(ids).read_bytes()).hexdigest();path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');print(json.dumps(data['counts'],sort_keys=True))
