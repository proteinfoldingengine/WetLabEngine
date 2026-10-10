import itertools,functools,json,pathlib,sys
@functools.lru_cache(None)
def cover(family):
 if not family:return 0
 if any(not a for a in family):return 99
 pivot=min(family,key=len)
 return 1+min(cover(tuple(a for a in family if x not in a)) for x in pivot)
def supports(v,n):return [frozenset(x for x,J in enumerate(v) if J//2**i%2) for i in range(n)]
def valid(v,f):
 R=supports(v,len(f));return all(len(a)>=d for a,d in zip(R,f)) and cover(tuple(R))<=4
def cols(s,N):return tuple(sum(2**i for i,r in enumerate(s) if r//2**x%2) for x in range(N))
def maximal(v):return tuple(sorted(J for J in set(v)-{0} if not any(J!=K and J|K==K for K in v)))
def partition(V,adj):
 pending=set(V);out=[]
 while pending:
  root=min(pending);component={root};todo=[root];pending.remove(root)
  for a in todo:
   for b in adj[a]:
    if b in pending:pending.remove(b);component.add(b);todo.append(b)
  out.append(sorted(component))
 return sorted(out)
@functools.lru_cache(None)
def all_four():
 out=[]
 for s in itertools.product(range(1,16),repeat=4):out.append((s,cols(s,4),tuple(a.bit_count() for a in s)))
 return out
def source_universe():
 return [list(s) for s,v,f in all_four() if set.union(*map(set,supports(v,4)))==set(range(4)) and 3<=cover(tuple(supports(v,4)))<=4]
def independently_region(M,f):
 V=[]
 for s,v,sizes in all_four():
  if all(a>=b for a,b in zip(sizes,f)) and all(any(J|K==K for K in M) for J in v):V.append(v)
 V=sorted(V);VS=set(V);adj={v:[] for v in V}
 for v in V:
  for x in range(4):
   for i in range(4):
    a=list(v);a[x]^=2**i;b=tuple(a)
    if b in VS:adj[v].append(b)
 return V,partition(V,adj)
def independently_graph(M,f):
 V=sorted(v for v in itertools.product([0]+list(M),repeat=4) if valid(v,f));adj={v:[] for v in V};E=[]
 for a,b in itertools.combinations(V,2):
  if sum(x!=y for x,y in zip(a,b))!=1:continue
  meet=tuple(x&y for x,y in zip(a,b))
  if valid(meet,f):E.append((a,b));adj[a].append(b);adj[b].append(a)
 return V,sorted(E),partition(V,adj)
def verify_region(record):
 M=tuple(record['maxima']);f=tuple(record['floors']);FV,FC=independently_region(M,f);V,E,C=independently_graph(M,f)
 assert record['full_vertices']==[list(v) for v in FV],'full vertex identities'
 assert record['full_components']==[[list(v) for v in c] for c in FC],'full components'
 assert record['vertices']==[list(v) for v in V],'compressed vertex identities'
 assert record['edges']==[[list(a),list(b)] for a,b in E],'edge identities'
 assert record['components']==[[list(v) for v in c] for c in C],'compressed components'
 idx={v:j for j,c in enumerate(C) for v in c};mapping=[]
 for component in FC:
  expansions=set()
  for v in component:
   chosen=tuple(0 if J==0 else min(K for K in M if J|K==K) for J in v);expansions.add(idx[chosen])
  assert len(expansions)==1;mapping.append(next(iter(expansions)))
 assert len(set(mapping))==len(FC)==len(C)
 assert record['component_map']==mapping
 # Every declared edge is lifted independently, and all original one-hidden completions
 # are checked for every source represented by this region later in verify().
 slices=0;FVS=set(FV)
 for a,b in E:
  x=next(i for i,(J,K) in enumerate(zip(a,b)) if J!=K);state=list(a)
  edits=[i for i in range(4) if a[x]//2**i%2 and not b[x]//2**i%2]+[i for i in range(4) if b[x]//2**i%2 and not a[x]//2**i%2]
  for i in [None]+edits:
   if i is not None:state[x]^=2**i
   assert valid(tuple(state),f)
   assert all(any(J|K==K for K in M) for J in state);slices+=1
  assert tuple(state)==b
 return {'full_states':len(FV),'full_edges':sum(sum(1 for x in range(4) for i in range(4) if tuple(v[j]^(2**i if j==x else 0) for j in range(4)) in FVS) for v in FV)//2,'compressed_vertices':len(V),'compressed_edges':len(E),'full_components':len(FC),'compressed_components':len(C),'lifted_slice_checks':slices}
def fullhit(v,q):
 R=supports(v,4);return min(cover(tuple(R)),1+cover(tuple(a for i,a in enumerate(R) if not q//2**i%2)))
def verify(data):
 sources=source_universe();assert data['sources']==sources,'source universe identities'
 keys=set();raw=[]
 for i,s in enumerate(sources):
  v=cols(s,4);M=maximal(v)
  for mode in (0,1):
   f=tuple(max(1,a.bit_count()-mode) for a in s);keys.add((M,f));raw.append((i,mode,M,f))
 protected={key:set() for key in keys}
 for i,mode,M,f in raw:
  protected[(M,f)].update(q for q in range(16) if 3<=fullhit(cols(sources[i],4),q)<=4)
 keys=sorted(keys);assert len(data['regions'])==len(keys),'region count'
 count={'sources':len(sources),'floor_cases':len(raw),'regions':len(keys),'full_states':0,'full_edges':0,'compressed_vertices':0,'compressed_edges':0,'full_components':0,'compressed_components':0,'lifted_slice_checks':0,'nonmonotone_only_cases':0,'full_hidden_slice_checks':0}
 for r,(M,f) in zip(data['regions'],keys):
  assert r['maxima']==list(M) and r['floors']==list(f),'region identities'
  for k,v in verify_region(r).items():count[k]+=v
  Q=sorted(protected[(M,f)]);assert r['protected_masks_union']==Q,'original protected masks'
  for v in r['full_vertices']:
   for q in Q:assert 3<=fullhit(v,q)<=4;count['full_hidden_slice_checks']+=1
 index={key:i for i,key in enumerate(keys)};rows=[]
 for i,mode,M,f in raw:
  j=index[(M,f)];v=cols(sources[i],4);start=tuple(min(K for K in M if J|K==K) for J in v)
  component=next(c for c in data['regions'][j]['components'] if list(start) in c);vacancy=any(0 in a for a in component)
  anchored=False
  for r in range(4):
   for candidate in data['regions'][j]['vertices']:
    if candidate[r]!=0:continue
    if all(x==r or v[x]|candidate[x]==candidate[x] for x in range(4)):anchored=True;break
   if anchored:break
  count['nonmonotone_only_cases']+=vacancy and not anchored;rows.append([i,mode,j,vacancy,anchored,[q for q in range(16) if 3<=fullhit(v,q)<=4]])
 assert data['cases']==rows,'case identities';assert data['counts']==count,'counts'
 return count
if __name__=='__main__':print(json.dumps(verify(json.loads(pathlib.Path(sys.argv[1]).read_text())),sort_keys=True))
