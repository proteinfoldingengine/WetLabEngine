"""Bit-mask producer. Complete typed universes; no sampled cases."""
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
 if not s:return 0
 if 0 in s:return 99
 u=functools.reduce(int.__or__,s);bits=[1<<i for i in range(u.bit_length()) if u>>i&1]
 for k in range(len(bits)+1):
  if any(all(a&sum(c) for a in s) for c in itertools.combinations(bits,k)):return k
 return 99
def source(q):return tuple([1|(1<<(i+1)) for i in range(q)]+[(1<<(q+1))-2,1<<(q+1)])
def columns(s,q):return tuple(sum(1<<i for i,a in enumerate(s) if a>>x&1) for x in range(q+2))
def safe(s,q,h):
 return all(a < (1<<(q+2)) for a in s) and all(a.bit_count()>=f for a,f in zip(s,[2]*q+[h,1])) and tau(s)<=4 and all(any(J&~K==0 for K in columns(source(q),q)) for J in columns(s,q))
def fulltau(s,m):return min(tau(s),1+tau(tuple(a for i,a in enumerate(s) if not m>>i&1)))
def release(q,p,J):return [[q,p+1]]+sum(([[r,p+1],[r,r+1],[q,r+1]] for r in J),[])
def route(s,ops):
 out=[tuple(s)]
 for i,x in ops:
  a=list(out[-1]);a[i]^=1<<x;out.append(tuple(a))
 return out
@functools.lru_cache(None)
def capacity(q,h):
 def compositions(n,k):
  if k==1:yield (n,);return
  for x in range(n+1):
   for rest in compositions(n-x,k-1):yield (x,)+rest
 V=sorted(v for n in range(q+3) for v in compositions(n,q+2) if v[-1]>=1 and sum(v[1:-1])>=h and all(v[0]+u>=2 for u in v[1:-1]))
 minimum=min(map(sum,V));assert minimum==min(q+2,h+3)
 return {'q':q,'h':h,'vectors':[list(v) for v in V],'minimum':minimum,'witness':list(min(v for v in V if sum(v)==minimum))}
@functools.lru_cache(None)
def bfs(q,h):
 layers=[[source(q)]];seen={source(q)}
 for d in range(4):
  nxt=set()
  for s in layers[-1]:
   for i in range(q+2):
    for x in range(q+2):
     a=list(s);a[i]^=1<<x;a=tuple(a)
     if a not in seen and safe(a,q,h):nxt.add(a)
  layers.append(sorted(nxt));seen.update(nxt)
 vacancies=[d for d,L in enumerate(layers) if any(0 in columns(s,q) for s in L)]
 assert min(vacancies)==4
 return {'q':q,'h':h,'layers':[[list(s) for s in L] for L in layers],'first_vacancy':min(vacancies)}
def relabel(s,pi):return tuple(sum(1<<pi[x] for x in range(len(pi)) if a>>x&1) for a in s)
def macro(q,s,pi,release_ops,reserve):
 ops=list(release_ops);cur=route(s,ops)[-1];unused=set(range(q+2));cycles=[]
 while unused:
  start=min(unused);c=[];x=start
  while x not in c:c.append(x);unused.remove(x);x=pi[x]
  cycles.append(c)
 def rename(a,b):
  nonlocal cur
  assert all(not z>>b&1 for z in cur)
  J=[i for i,z in enumerate(cur) if z>>a&1]
  new=[[i,b] for i in J]+[[i,a] for i in J];ops.extend(new);cur=route(cur,new)[-1]
 for c in cycles:
  if reserve in c or len(c)==1:continue
  rename(c[-1],reserve)
  for j in range(len(c)-2,-1,-1):rename(c[j],c[j+1])
  rename(reserve,c[0])
 c=next(c for c in cycles if reserve in c);j=c.index(reserve);c=c[j:]+c[:j]
 for k in range(len(c)-1,0,-1):rename(c[k],pi[c[k]])
 assert cur==relabel(route(s,release_ops)[-1],pi)
 ops.extend([[i,pi[x]] for i,x in release_ops[::-1]])
 assert route(s,ops)[-1]==relabel(s,pi)
 return ops

def build(n=7):
 D={k:[] for k in ['sources','primary','capacity','batch','bfs','permutations','renewal']};hidden=set();slices=0
 def check(q,h,states,cover=None,exact=True):
  nonlocal slices
  for s in states:
   assert safe(s,q,h) and (tau(s)==3 if exact else 3<=tau(s)<=4)
   if cover is not None:assert all(a&cover for a in s)
   hidden.add((q,s));slices+=1
 for q in range(2,n+1):
  s=source(q);M=columns(s,q);assert len(set(M))==q+2 and all(not(a!=b and a&~b==0) for a in M for b in M)
  for h in range(1,q+1):
   # Each donor has its unique original maximal container; no anchored expansion.
   assert all(not safe(tuple(a&~(1<<x) for a in s),q,h) for x in range(q+2))
   masks=[m for m in range(1<<(q+2)) if fulltau(s,m)==3]
   D['sources'].append({'q':q,'h':h,'source':list(s),'floors':[2]*q+[h,1],'footprints':list(M),'protected_masks':masks,'anchored_failures':list(range(q+2))})
   D['capacity'].append(capacity(q,h))
   if h==q:assert all(not safe(route(s,[[i,x]])[-1],q,h) for i in range(q+2) for x in range(q+2))
   for p,r in itertools.permutations(range(q),2):
    ops=release(q,p,[r]);states=route(s,ops);positive=h<=q-2
    if positive:
     survivor=next(i for i in range(q) if i not in (p,r));check(q,h,states,1|(1<<(survivor+1))|(1<<(q+1)));assert columns(states[-1],q)[r+1]==0
    elif h==q-1:check(q,h,states[:-1]);assert not safe(states[-1],q,h)
    else:assert not safe(states[1],q,h)
    D['primary'].append({'q':q,'h':h,'p':p,'r':r,'positive':positive,'ops':ops,'states':[list(a) for a in states]})
   if h<=q-2:
    for p in range(q):
     for m in range(1,q-h):
      for J in itertools.combinations([i for i in range(q) if i!=p],m):
       ops=release(q,p,J);states=route(s,ops);survivor=next(i for i in range(q) if i!=p and i not in J);check(q,h,states,1|(1<<(survivor+1))|(1<<(q+1)))
       assert len(ops)==1+3*m and all(columns(states[-1],q)[r+1]==0 for r in J)
       if m==q-h-1:assert sum(bool(a) for a in columns(states[-1],q))==capacity(q,h)['minimum']
       D['batch'].append({'q':q,'h':h,'p':p,'J':list(J),'ops':ops,'states':[list(a) for a in states]})
 D['bfs']=[bfs(q,h) for q,h in [(3,1),(4,1),(4,2)] if q<=n]
 for record in D['bfs']:
  for layer in record['layers']:check(record['q'],record['h'],map(tuple,layer),exact=False)
 s=source(3);L=release(3,0,[1]);r=2
 for pi in itertools.permutations(range(5)):
  ops=macro(3,s,pi,L,r);states=route(s,ops);check(3,1,states);D['permutations'].append({'pi':list(pi),'ops':ops,'states':[list(a) for a in states]})
 pairs=[((1,2,3,4,0),(4,0,1,2,3)),((2,0,1,4,3),(1,0,3,2,4)),((4,3,2,1,0),(1,2,3,4,0))]
 for pi,sigma in pairs:
  first=macro(3,s,pi,L,r);mid=relabel(s,pi);second=macro(3,mid,sigma,[[i,pi[x]] for i,x in L],pi[r]);ops=first+second;states=route(s,ops);check(3,1,states);assert states[-1]==relabel(mid,sigma)
  D['renewal'].append({'pi':list(pi),'sigma':list(sigma),'boundary':len(first),'ops':ops,'states':[list(a) for a in states]})
 hiddenchecks=0
 for q,s in hidden:
  for m in range(1<<(q+2)):
   if fulltau(source(q),m)==3:assert 3<=fulltau(s,m)<=4;hiddenchecks+=1
 D['control']={'source_tau':fulltau(source(3),20),'candidate_tau':fulltau((3,7,9,14,16),20),'mask':20};assert D['control']=={'source_tau':3,'candidate_tau':2,'mask':20}
 D['counts']={k:len(D[k]) for k in ['sources','primary','capacity','batch','bfs','permutations','renewal']};D['counts'].update(positive=sum(x['positive'] for x in D['primary']),route_and_bfs_slices=slices,unique_hidden_states=len(hidden),hidden_checks=hiddenchecks,capacity_vectors=sum(len(x['vectors']) for x in D['capacity']),bfs_layer_sizes=[[len(L) for L in x['layers']] for x in D['bfs']])
 return D
if __name__=='__main__':
 d=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(d['counts'],sort_keys=True))
