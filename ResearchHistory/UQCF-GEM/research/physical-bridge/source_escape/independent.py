"""Independent source-escape reconstruction: sets and combination covers."""
if not __debug__:raise RuntimeError('source-escape requires assertions enabled')
import gzip,hashlib,itertools,json,pathlib,sys
from functools import lru_cache


def subsets(items):
 for size in range(len(items)+1):yield from itertools.combinations(items,size)


def definitions():
 complete=lambda n:list(itertools.combinations(range(n),2))
 return [('K4',4,complete(4)),('C5',5,[(0,1),(0,4),(1,2),(2,3),(3,4)]),('K5',5,complete(5)),
         ('K6-minus45',6,[e for e in complete(6) if e!=(4,5)]),('K5-minus34',5,[e for e in complete(5) if e!=(3,4)]),
         ('K4-leaf',5,sorted(complete(4)+[(0,4)])),('K23-K2',7,[(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(5,6)])]


def declarations(fixture=False):
 defs={name:(k,H) for name,k,H in definitions()}
 if fixture:
  requests=[('pinned','K6-minus45',[1,1,1,2,1,1],[(u,v) for u in (1,2) for v in (3,4,5)]),
            ('duplicate','K6-minus45',[2,1,1,2,1,1],[(u,v) for u in (1,2) for v in (3,4,5)]),
            ('k2','K23-K2',[2]*7,defs['K23-K2'][1]),('nonminimum','K5-minus34',[1]*5,[(u,v) for u,v in defs['K5-minus34'][1] if u!=0]),
            ('star','K5',[1]*5,[(0,v) for v in range(1,5)]),('locked','K5',[2]*5,[(u,v) for u in (0,1) for v in (2,3,4)]),
            ('leaf_empty','K4-leaf',[1]*5,[]),('leaf_full','K4-leaf',[1]*5,defs['K4-leaf'][1])]
  return [dict(family=family,H=[list(e) for e in defs[family][1]],G=[list(e) for e in G],a=a,name=name) for name,family,a,G in requests]
 out=[]
 for family,k,H in definitions():
  if family in ('K4','C5','K4-leaf'):graphs=sorted(subsets(H),key=lambda g:sum(2**H.index(e) for e in g))
  elif family=='K23-K2':graphs=[H]
  else:
   graphs=[[],H]+[[e for e in H if v not in e] for v in range(k)]
   if family=='K5':
    cross=[e for e in H if (e[0]<2)!=(e[1]<2)];graphs.extend([cross,sorted(cross+[(0,1)])])
   if family=='K6-minus45':graphs.append([e for e in H if e[0] in (1,2) and e[1] in (3,4,5)])
  for G in graphs:
   for a in itertools.product((1,2),repeat=k):out.append(dict(family=family,H=[list(e) for e in H],G=[list(e) for e in G],a=list(a)))
 assert len(out)==7360
 return out


@lru_cache(maxsize=200000)
def cover_number(footprints,roots):
 fs=[set(f) for f in footprints];target=set(roots)
 for size in range(len(fs)+1):
  for chosen in itertools.combinations(fs,size):
   if set().union(*chosen)>=target:return size
 return len(fs)+1


def hitting(state,H):
 footprints=tuple(sorted({tuple(sorted(f)) for f in state if f}))
 return cover_number(footprints,tuple(H))


def validate_source(s):
 H=list(map(tuple,s['H']));G=list(map(tuple,s['G']));a=s['a'];k=len(a)
 assert a and all(type(n) is int and n>=1 for n in a)
 assert H==sorted(set(H)) and all(0<=u<v<k for u,v in H)
 assert G==sorted(set(G)) and set(G)<=set(H)
 assert set(itertools.chain.from_iterable(H))==set(range(k))
 assert hitting([{e for e in H if v in e} for v in range(k)],H) in (3,4)
 return True


def validate_counts(s,n):
 validate_source(s);a=s['a'];H=list(map(tuple,s['H']));G=set(map(tuple,s['G']))
 assert len(n)==len(a) and all(type(x) is int and x>=0 for x in n) and sum(n)<sum(a)
 assert all(n[u]+n[v]>=(a[u]+a[v] if (u,v) in G else 1) for u,v in H)
 state=[{e for e in H if v in e} for v,count in enumerate(n) for _ in range(count)]
 assert hitting(state,H)<=4
 return True


def reconstruct(s):
 validate_source(s);H=list(map(tuple,s['H']));G=set(map(tuple,s['G']));a=s['a'];k=len(a)
 stars=[{e for e in H if v in e} for v in range(k)]
 types=[v for v,count in enumerate(a) for _ in range(count)];original=[stars[v].copy() for v in types]
 def bits(f):return sum(2**H.index(e) for e in f)
 src=[bits(f) for f in original]
 floor=[a[u]+a[v] if (u,v) in G else 1 for u,v in H]
 covers=[list(C) for C in subsets(list(range(k))) if len(C)<=4 and all(set(e)&set(C) for e in H)]
 B=[[C for C in covers if v not in C] for v in range(k)]
 traces=[[H.index(e) for e in H if e in G and v in e] for v in range(k)]
 V=[v for v in range(k) if not (stars[v]&G) and (a[v]>=2 or len(B[v])>0)]
 X=[]
 for v,w,z in itertools.permutations(range(k),3):
  first=tuple(sorted((v,w)));added=tuple(sorted((w,z)))
  if first in H and added in H and stars[v]&G <= {first} and (a[v]>=2 or B[v]):X.append([v,w,z])
 lock=all(len(stars[v]&G)>1 or (a[v]==1 and len(B[v])==0) for v in range(k))
 evaluations=[];evaluation_keys={}
 def evaluate(v,footprint):
  key=(v,tuple(sorted(footprint)))
  if key in evaluation_keys:return evaluation_keys[key]
  state=[f.copy() for f in original];state[types.index(v)]=set(footprint)
  counts=[sum(e in f for f in state) for e in H]
  palette=len(state)==sum(a) and all(f<=set(H) for f in state)
  domination=all(any(f<=star for star in stars) for f in state)
  hit=hitting(state,H);floors_ok=all(count>=bound for count,bound in zip(counts,floor))
  safe=palette and domination and floors_ok and hit<=4
  index=len(evaluations);evaluation_keys[key]=index;evaluations.append([v,bits(footprint),palette,domination,counts,hit,floors_ok,safe]);return index
 vacancies=[];candidates=[];direct=set()
 for x,v in enumerate(types):
  index=evaluate(v,set());safe=evaluations[index][-1];vacancies.append([x,v,index,safe])
  if safe:direct.add(('V',x,(),None))
  partials=sorted((set(F) for F in subsets(sorted(stars[v])) if F),key=bits)
  for F in partials:
   pre=evaluate(v,F)
   for added in H:
    if added in stars[v]:continue
    post=evaluate(v,F|{added});safe=evaluations[pre][-1] and evaluations[post][-1]
    candidates.append([x,v,bits(F),H.index(added),pre,post,safe])
    if safe:direct.add(('X',x,tuple(sorted(F)),added))
 predicted=set();routes=[];all_states=set();occurrences=0
 for x,v in enumerate(types):
  choices=[('V',None,None)] if v in V else []
  choices.extend(('X',w,z) for vv,w,z in X if vv==v)
  for kind,w,z in choices:
   kept=set() if kind=='V' else {tuple(sorted((v,w)))}
   added=None if kind=='V' else tuple(sorted((w,z)))
   predicted.add((kind,x,tuple(sorted(kept)),added))
   state=[f.copy() for f in original];slices=[[bits(f) for f in state]];ops=[]
   for edge in sorted(stars[v]-kept):
    state[x].remove(edge);ops.append([x,H.index(edge),0]);slices.append([bits(f) for f in state])
   if added is not None:state[x].add(added);ops.append([x,H.index(added),1]);slices.append([bits(f) for f in state])
   for index,serialized in enumerate(slices):
    decoded=[{edge for r,edge in enumerate(H) if (m//2**r)%2} for m in serialized]
    assert evaluations[evaluate(v,decoded[x])][-1]
    assert all(f==original[j] for j,f in enumerate(decoded) if j!=x)
    event=any(not f or not f<=original[j] for j,f in enumerate(decoded))
    assert event==(index==len(slices)-1)
    if kind=='X':assert all(decoded)
    all_states.add(tuple(serialized));occurrences+=1
   assert len(ops)==len(stars[v])
   routes.append(dict(kind=kind,label=x,type=v,w=w,z=z,ops=ops,states=slices,event_index=len(ops),cost=len(ops)))
 assert predicted==direct
 masks=[];exposed_sets=[]
 for hidden in range(2**len(H)):
  exposed={e for r,e in enumerate(H) if not (hidden//2**r)%2}
  if exposed and all(not exposed<=f for f in original):masks.append(hidden);exposed_sets.append(exposed)
 failures={}
 for code in {m for state in all_states for m in state}:
  f={e for r,e in enumerate(H) if (code//2**r)%2}
  failures[code]=any(exposed<=f for exposed in exposed_sets)
 for state in all_states:assert all(not failures[m] for m in state)
 assert not lock or not predicted
 return dict(source=s,floors=floor,covers=covers,B=B,traces=traces,V=V,X=X,cover_lock=lock,escape=bool(predicted),
             evaluations=evaluations,vacancies=vacancies,candidates=candidates,routes=routes,states=[list(st) for st in sorted(all_states)],
             slice_occurrences=occurrences,protected_masks=masks,hidden_checks=len(all_states)*len(masks))


def verify(data,fixture=False,identity_path=None):
 assert data['schema']=='source-escape-v1' and data['fixture']==fixture
 handle=None
 if identity_path is None:
  assert fixture,'Full verification requires canonical stream';iterator=iter(data['records'])
 else:
  try:handle=gzip.open(identity_path,'rt');iterator=iter(handle)
  except OSError as e:raise AssertionError('Missing canonical stream') from e
 counts=dict(sources=0,candidates=0,vacancy_candidates=0,routes=0,slice_occurrences=0,distinct_states=0,hidden_checks=0,escape_sources=0);hashes=[]
 try:
  for s in declarations(fixture):
   expected=reconstruct(s)
   try:raw=next(iterator)
   except StopIteration as e:raise AssertionError('Truncated canonical stream') from e
   actual=json.loads(raw) if isinstance(raw,str) else raw
   assert actual==expected,'Complete canonical record mismatch'
   line=json.dumps(expected,sort_keys=True,separators=(',',':'))+'\n';hashes.append(hashlib.sha256(line.encode()).hexdigest())
   increments={'sources':1,'candidates':len(expected['candidates']),'vacancy_candidates':len(expected['vacancies']),'routes':len(expected['routes']),'slice_occurrences':expected['slice_occurrences'],'distinct_states':len(expected['states']),'hidden_checks':expected['hidden_checks'],'escape_sources':int(expected['escape'])}
   for key,n in increments.items():counts[key]+=n
  marker=object();assert next(iterator,marker) is marker,'Extra canonical record'
 except (OSError,EOFError,json.JSONDecodeError) as e:raise AssertionError('Corrupt canonical stream') from e
 finally:
  if handle is not None:handle.close()
 assert counts==data['counts'] and hashes==data['record_sha256']
 if identity_path is not None and 'identity_archive_sha256' in data:assert hashlib.sha256(pathlib.Path(identity_path).read_bytes()).hexdigest()==data['identity_archive_sha256']
 return True

if __name__=='__main__':
 p=pathlib.Path(sys.argv[1]);data=json.loads(p.read_text());verify(data,identity_path=str(p)+'.identities.jsonl.gz')
 result=dict(accepted=True,counts=data['counts'],certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),canonical_sha256=data['identity_archive_sha256'])
 pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
