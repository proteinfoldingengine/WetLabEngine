"""Bit-based forward producer for the frozen reserve-activation contract."""
if not __debug__:raise RuntimeError('producer requires assertions enabled')
import functools,gzip,hashlib,itertools,json,pathlib,sys

def abstract_sources(fixture=False):
 if fixture:
  for p,q,m in [(1,0,0),(2,1,3),(3,2,45),(2,2,15)]:yield dict(p=p,q=q,m=m)
 else:
  for p in range(1,5):
   for q in range(4):
    for m in range(1<<(p*q)):yield dict(p=p,q=q,m=m)

def native_sources(fixture=False):
 H=[[i,w] for i in range(4) for w in range(4,7)]
 def source(G,a,name=None,forced=None):
  d=dict(H=H,G=G,a=[a]*7,I=[0,1,2,3],C=[4,5,6])
  if name:d['name']=name
  if forced is not None:d['forced']=forced
  return d
 if fixture:
  yield source([[0,4],[1,4],[1,5],[2,5],[2,6],[3,6]],1,'chain')
  yield source(H,2,'full');yield source([],1,'empty')
  yield source([[0,4],[1,4]],1,'cherry',[['T',0,4],['V',1,-1]])
  h=[[i,j] for i in range(2) for j in range(2,5)]+[[5,6]]
  yield dict(H=h,G=h,a=[2]*7,I=[2,3,4,5],C=[0,1,6],name='k2')
 else:
  for m in range(4096):
   G=[e for k,e in enumerate(H) if m>>k&1]
   for a in (1,2):yield source(G,a)

def closure(rows,q):
 R=0
 while True:
  old=R
  for n in rows:
   missing=n&~R
   if missing and missing&(missing-1)==0:R|=missing
  if old==R:break
 Z=[i for i,n in enumerate(rows) if not n&~R]
 return [j for j in range(q) if R>>j&1],Z

def abstract_record(s):
 p,q,m=s['p'],s['q'],s['m'];rows=[(m>>(i*q))&((1<<q)-1) for i in range(p)]
 start=(-1,)*p;seen={start};pending=[start];raw=[]
 while pending:
  st=pending.pop()
  if -2 in st:continue
  R=sum(1<<w for w in st if w>=0)
  for i,v in enumerate(st):
   if v!=-1:continue
   miss=rows[i]&~R
   for kind,w,ok in [('V',-1,miss==0)]+[('T',w,miss==1<<w) for w in range(q) if not R>>w&1]:
    nxt=list(st);nxt[i]=-2 if kind=='V' else w;nxt=tuple(nxt);raw.append((st,kind,i,w,ok,nxt))
    if ok and nxt not in seen:seen.add(nxt);pending.append(nxt)
 states=sorted(seen);index={s:i for i,s in enumerate(states)}
 candidates=sorted([[index[st],kind,i,w,ok] for st,kind,i,w,ok,nxt in raw]);edges=sorted([[index[st],kind,i,w,index[nxt]] for st,kind,i,w,ok,nxt in raw if ok]);terminals=[i for i,st in enumerate(states) if -2 in st]
 R,Z=closure(rows,q);surplus=len(Z)-len(R);assert bool(terminals)==(surplus>0)
 for st in states:
  if -2 in st:continue
  activated={w for w in st if w>=0};used={i for i,w in enumerate(st) if w>=0};assert len(activated)==len(used)
  eligible=[i for i in range(p) if st[i]==-1 and (rows[i]&~sum(1<<w for w in activated)).bit_count()==1]
  if not eligible:assert activated==set(R)
 st=list(start);canonical=[]
 while True:
  activated=sum(1<<w for w in st if w>=0);zeros=[i for i in range(p) if st[i]==-1 and rows[i]&~activated==0]
  if zeros:canonical.append(['V',zeros[0],-1]);break
  opts=[(i,(rows[i]&~activated).bit_length()-1) for i in range(p) if st[i]==-1 and (rows[i]&~activated).bit_count()==1]
  if not opts:break
  i,w=opts[0];canonical.append(['T',i,w]);st[i]=w
 return dict(kind='abstract',source=s,states=[list(st) for st in states],source_index=index[start],candidates=candidates,edges=edges,terminals=terminals,closure=R,Z=Z,surplus=surplus,canonical=canonical)

@functools.lru_cache(None)
def tau(masks,full):
 masks=tuple(sorted(set(masks)-{0}))
 for k in range(1,len(masks)+1):
  for c in itertools.combinations(masks,k):
   union=0
   for m in c:union|=m
   if union==full:return k
 return len(masks)+1

@functools.lru_cache(None)
def protection(M,full):
 return tuple(h for h in range(full+1) if full^h and all((full^h)&~m for m in M))

@functools.lru_cache(None)
def hidden_ok(M,full,m):
 protected=protection(M,full);pbits=sum(1<<(full^h) for h in protected);bits=1;sub=m
 while sub:bits|=1<<sub;sub=(sub-1)&m
 return not(bits&pbits)

def native_record(s):
 H=s['H'];G=s['G'];a=s['a'];I=s['I'];C=s['C'];n=len(a);full=(1<<len(H))-1
 assert H==sorted(H) and len({tuple(e) for e in H})==len(H) and all(0<=u<v<n for u,v in H)
 assert all(type(x)==int and x>=1 for x in a);assert set(map(tuple,G))<=set(map(tuple,H)) and len(set(map(tuple,G)))==len(G)
 M=tuple(sum(1<<k for k,e in enumerate(H) if v in e) for v in range(n));assert all(M) and tau(M,full) in (3,4)
 assert len(set(I))==len(I) and all(0<=v<n for v in I) and I
 assert len(set(C))==len(C)<=4 and all(0<=v<n for v in C) and all(set(e)&set(C) for e in H)
 assert all(a[v]>=2 for v in set(I)&set(C)) and all(not(set(e)<=set(I)) for e in G)
 offsets=list(itertools.accumulate([0]+a))[:-1];types=[v for v,k in enumerate(a) for _ in range(k)];src=[M[v] for v in types];anchors=[offsets[v] for v in C];donors={i:offsets[i]+int(i in C) for i in I}
 neighbors={i:{v if u==i else u for u,v in G if i in (u,v)} for i in I};R=set();J=set();macros=[]
 if 'forced' in s:macros=s['forced']
 else:
  while True:
   zero=[i for i in I if i not in J and not neighbors[i]-R]
   if zero:macros.append(['V',min(zero),-1]);break
   possible=[(i,next(iter(neighbors[i]-R))) for i in I if i not in J and len(neighbors[i]-R)==1]
   if not possible:break
   i,w=min(possible);macros.append(['T',i,w]);J.add(i);R.add(w)
 state=src.copy();states=[state.copy()];ops=[];boundaries=[];R=set();J=set();released=False;expected_cost=0
 for kind,i,w in macros:
  assert i in I and i not in J and not released;x=donors[i]
  if kind=='T':assert w not in R and neighbors[i]-R=={w};keep=1<<H.index(sorted((i,w)));expected_cost+=M[i].bit_count()+M[w].bit_count()-2
  else:assert kind=='V' and not neighbors[i]-R;keep=0;expected_cost+=M[i].bit_count()
  for k in range(len(H)):
   if state[x]>>k&1 and not keep>>k&1:state[x]&=~(1<<k);ops.append([x,k,0]);states.append(state.copy())
  if kind=='T':
   for k in range(len(H)):
    if M[w]>>k&1 and not state[x]>>k&1:state[x]|=1<<k;ops.append([x,k,1]);states.append(state.copy())
   R.add(w)
  else:released=True
  J.add(i);boundaries.append([len(ops),sorted(J),sorted(R)])
 assert len(ops)==expected_cost
 floors=[a[u]+a[v] if [u,v] in G else 1 for u,v in H];unique=sorted(set(map(tuple,states)));evaluations=[]
 for st in unique:
  counts=[sum(m>>k&1 for m in st) for k in range(len(H))];t=tau(tuple(st),full)
  assert all(c>=f for c,f in zip(counts,floors)) and 3<=t<=4
  assert all(any(m&~v==0 for v in M) for m in st)
  assert all(st[x]==src[x] for x in anchors) and all(hidden_ok(M,full,m) for m in set(st))
  evaluations.append([list(st),counts,t])
 assert all(all(st) for st in states[:-1]);assert (0 in states[-1])==released
 reverse_ops=[[x,k,1-b] for x,k,b in reversed(ops)];rev=states[-1].copy();reverse_states=[rev.copy()]
 for x,k,b in reverse_ops:
  assert bool(rev[x]>>k&1)!=bool(b);rev[x]^=1<<k;reverse_states.append(rev.copy())
 assert rev==src and reverse_states==states[::-1]
 masks=list(protection(M,full))
 cr,cz=closure([sum(1<<v for v in neighbors[i]) for i in I],n);cz=[I[k] for k in cz];assert released==(len(cz)>len(cr))
 return dict(kind='native',source=s,closure=cr,Z=cz,floors=floors,anchors=anchors,donors=[[i,donors[i]] for i in I],macros=macros,boundaries=boundaries,ops=ops,states=states,evaluations=evaluations,reverse_ops=reverse_ops,reverse_states=reverse_states,released=released,protected_masks=masks,distinct_states=len(unique),slice_occurrences=len(states),hidden_checks=len(unique)*len(masks),cost=expected_cost)

def build(fixture=False,writer=None):
 records=[];hashes=[];counts=dict(abstract_sources=0,abstract_states=0,abstract_candidates=0,abstract_edges=0,abstract_terminals=0,native_sources=0,native_positive=0,native_macros=0,native_edits=0,slice_occurrences=0,distinct_states=0,hidden_checks=0)
 for kind,sources,fn in [('abstract',abstract_sources,abstract_record),('native',native_sources,native_record)]:
  for s in sources(fixture):
   r=fn(s);line=json.dumps(r,sort_keys=True,separators=(',',':'))+'\n';hashes.append(hashlib.sha256(line.encode()).hexdigest())
   if writer is None:records.append(r)
   else:writer.write(line.encode())
   if kind=='abstract':
    for k,v in [('abstract_sources',1),('abstract_states',len(r['states'])),('abstract_candidates',len(r['candidates'])),('abstract_edges',len(r['edges'])),('abstract_terminals',len(r['terminals']))]:counts[k]+=v
   else:
    for k,v in [('native_sources',1),('native_positive',int(r['released'])),('native_macros',len(r['macros'])),('native_edits',len(r['ops'])),('slice_occurrences',r['slice_occurrences']),('distinct_states',r['distinct_states']),('hidden_checks',r['hidden_checks'])]:counts[k]+=v
 return dict(schema='reserve-activation-v1',fixture=fixture,counts=counts,record_sha256=hashes,**({'records':records} if writer is None else {}))

if __name__=='__main__':
 p=pathlib.Path(sys.argv[1]);ids=str(p)+'.identities.jsonl.gz'
 with open(ids,'wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:d=build(writer=z)
 d['identity_archive_sha256']=hashlib.sha256(pathlib.Path(ids).read_bytes()).hexdigest();p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(json.dumps(d['counts'],sort_keys=True))
