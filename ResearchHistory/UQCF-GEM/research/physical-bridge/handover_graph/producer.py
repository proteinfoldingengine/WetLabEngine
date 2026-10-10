import itertools,functools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
 if not s:return 0
 if 0 in s:return 99
 u=functools.reduce(int.__or__,s);bits=[1<<x for x in range(u.bit_length()) if u>>x&1]
 for k in range(len(bits)+1):
  if any(all(a&sum(c) for a in s) for c in itertools.combinations(bits,k)):return k
 return 99
def roots(v,n):return tuple(sum(1<<x for x,J in enumerate(v) if J>>i&1) for i in range(n))
def columns(s,N):return tuple(sum(1<<i for i,a in enumerate(s) if a>>x&1) for x in range(N))
def maxima(s,N):
 F=set(columns(s,N))-{0};return tuple(sorted(j for j in F if not any(j!=k and j&~k==0 for k in F)))
def gate(v,f,n):
 s=roots(v,n);return all(a.bit_count()>=b for a,b in zip(s,f)) and tau(s)<=4
def lift(v,w):
 differing=[x for x,(a,b) in enumerate(zip(v,w)) if a!=b];assert len(differing)==1
 x=differing[0];a,b=v[x],w[x]
 return [[i,x] for i in range(max(a,b).bit_length()) if a>>i&1 and not b>>i&1]+[[i,x] for i in range(max(a,b).bit_length()) if b>>i&1 and not a>>i&1]
def path_states(v,ops):
 a=list(v);out=[tuple(a)]
 for i,x in ops:a[x]^=1<<i;out.append(tuple(a))
 return out
def components(vertices,edges):
 adj={v:[] for v in vertices}
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 unseen=set(vertices);out=[]
 while unseen:
  seed=min(unseen);stack=[seed];unseen.remove(seed);part=[]
  while stack:
   a=stack.pop();part.append(a)
   for b in adj[a]:
    if b in unseen:unseen.remove(b);stack.append(b)
  out.append(sorted(part))
 return sorted(out)
def graph(M,f,N):
 n=len(f);V=sorted(v for v in itertools.product((0,)+tuple(M),repeat=N) if gate(v,f,n));VS=set(V);E=[]
 for v in V:
  for x in range(N):
   for J in (0,)+tuple(M):
    if J<=v[x]:continue
    w=v[:x]+(J,)+v[x+1:]
    if w not in VS:continue
    meet=v[:x]+(v[x]&J,)+v[x+1:]
    if gate(meet,f,n):E.append((v,w))
 return V,sorted(E),components(V,E)
def region(M,f,N):
 n=len(f);allowed=[J for J in range(1<<n) if any(J&~K==0 for K in M)]
 V=sorted(v for v in itertools.product(allowed,repeat=N) if gate(v,f,n));VS=set(V);E=[]
 for v in V:
  for x in range(N):
   for i in range(n):
    J=v[x]^(1<<i)
    if J<=v[x]:continue
    w=v[:x]+(J,)+v[x+1:]
    if w in VS:E.append((v,w))
 return V,sorted(E),components(V,E)
def expand(v,M):return tuple(0 if J==0 else next(K for K in M if J&~K==0) for J in v)
def equality(full,compressed,M):
 idx={v:i for i,c in enumerate(compressed) for v in c};mapped=[]
 for c in full:
  hit={idx[expand(v,M)] for v in c};assert len(hit)==1;mapped.append(next(iter(hit)))
 assert len(set(mapped))==len(full)==len(compressed)
 return mapped
def fulltau(v,q,n):
 s=roots(v,n);return min(tau(s),1+tau(tuple(a for i,a in enumerate(s) if not q>>i&1)))
def build():
 sources=[];cases=[];keys=set()
 for s in itertools.product(range(1,16),repeat=4):
  if functools.reduce(int.__or__,s)!=15 or tau(s) not in (3,4):continue
  i=len(sources);sources.append(list(s));M=maxima(s,4)
  for mode in (0,1):
   f=tuple(max(1,a.bit_count()-mode) for a in s);keys.add((M,f));cases.append((i,mode,M,f))
 protected={key:set() for key in keys}
 for i,mode,M,f in cases:
  v=columns(sources[i],4);protected[(M,f)].update(q for q in range(16) if 3<=fulltau(v,q,4)<=4)
 regions=[];index={};counts={'sources':len(sources),'floor_cases':len(cases),'regions':len(keys),'full_states':0,'full_edges':0,'compressed_vertices':0,'compressed_edges':0,'full_components':0,'compressed_components':0,'lifted_slice_checks':0,'nonmonotone_only_cases':0,'full_hidden_slice_checks':0}
 for M,f in sorted(keys):
  full,FE,FC=region(M,f,4);V,E,CC=graph(M,f,4);mapping=equality(FC,CC,M)
  Q=sorted(protected[(M,f)])
  for v in full:
   for q in Q:assert 3<=fulltau(v,q,4)<=4;counts['full_hidden_slice_checks']+=1
  for v,w in E:
   states=path_states(v,lift(v,w));assert states[-1]==w
   assert all(gate(a,f,4) and all(any(J&~K==0 for K in M) for J in a) for a in states)
   counts['lifted_slice_checks']+=len(states)
  index[(M,f)]=len(regions)
  regions.append({'maxima':list(M),'floors':list(f),'protected_masks_union':Q,'full_vertices':[list(v) for v in full],'full_components':[[list(v) for v in c] for c in FC],'vertices':[list(v) for v in V],'edges':[[list(a),list(b)] for a,b in E],'components':[[list(v) for v in c] for c in CC],'component_map':mapping})
  for k,val in [('full_states',len(full)),('full_edges',len(FE)),('compressed_vertices',len(V)),('compressed_edges',len(E)),('full_components',len(FC)),('compressed_components',len(CC))]:counts[k]+=val
 rows=[]
 for i,mode,M,f in cases:
  j=index[(M,f)];s=columns(sources[i],4);start=expand(s,M);component=next(c for c in regions[j]['components'] if list(start) in c);vacancy=any(0 in v for v in component)
  # Anchored class: expand source donors, drop one reserve, test vertex.
  anchored=False
  choices=[[K for K in M if J&~K==0] for J in s]
  for r in range(4):
   for v in itertools.product(*[([0] if x==r else choices[x]) for x in range(4)]):
    if gate(v,f,4):anchored=True;break
   if anchored:break
  counts['nonmonotone_only_cases']+=vacancy and not anchored
  rows.append([i,mode,j,vacancy,anchored,[q for q in range(16) if 3<=fulltau(s,q,4)<=4]])
 return {'schema':'maximal-handover-v1','sources':sources,'cases':rows,'regions':regions,'counts':counts}
if __name__=='__main__':
 data=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(data['counts'],sort_keys=True))
def reachable(M,f,start):
 seen={tuple(start)};todo=[tuple(start)];edges=[]
 for a in todo:
  for x in range(len(a)):
   for J in (0,)+tuple(M):
    if J==a[x]:continue
    b=a[:x]+(J,)+a[x+1:];meet=a[:x]+(J&a[x],)+a[x+1:]
    if not gate(b,f,len(f)) or not gate(meet,f,len(f)):continue
    edges.append((a,b))
    if b not in seen:seen.add(b);todo.append(b)
 return sorted(seen)
