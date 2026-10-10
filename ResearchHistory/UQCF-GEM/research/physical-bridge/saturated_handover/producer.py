"""Independent bitmask producer for saturated handover and count quotient."""
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
 if not s:return 0
 if 0 in s:return 99
 u=functools.reduce(int.__or__,s);bits=[1<<i for i in range(u.bit_length()) if u>>i&1]
 for k in range(len(bits)+1):
  if any(all(a&sum(c) for a in s) for c in itertools.combinations(bits,k)):return k
 return 99
def source(r):return tuple([3|(1<<(i+3)) for i in range(r)]+[5|(1<<(i+3)) for i in range(r)]+[(1<<(r+4))-2,1<<(r+4)])
def floors(r):return [3]*(2*r)+[r+3,1]
def columns(s,N):return tuple(sum(1<<i for i,a in enumerate(s) if a>>x&1) for x in range(N))
def types(r):
 R=1<<(2*r);A=(1<<r)-1;B=A<<r
 return (A|B,A|R,B|R)+tuple((1<<i)|(1<<(r+i))|R for i in range(r))+(1<<(2*r+1),)
def generic_safe(s,F,M,N):return all(0<=a<(1<<N) for a in s) and all(a.bit_count()>=f for a,f in zip(s,F)) and tau(s)<=4 and all(any(J&~K==0 for K in M) for J in columns(s,N))
def safe(s,r):return generic_safe(s,floors(r),types(r),r+5)
def fulltau(s,m):return min(tau(s),1+tau(tuple(a for i,a in enumerate(s) if not m>>i&1)))
def route(s,ops):
 out=[tuple(s)]
 for i,x in ops:a=list(out[-1]);a[i]^=1<<x;out.append(tuple(a))
 return out
def release(r,a,b,c):
 assert len({a,b,c})==3
 return [[j,r+3] for j in (a,b,c)]+[[a,a+3]]+[[r+j,a+3] for j in range(r) if j!=a]+[[b,b+3],[r+a,b+3],[r+c,b+3],[r+c,c+3]]+[[j,c+3] for j in range(r) if j!=c]+[[j,0] for j in range(2*r)]
def canonical(v,r):
 foot=[0]*(r+5-sum(v))
 for count,J in zip(v,types(r)):foot.extend([J]*count)
 return tuple(sum(1<<x for x,J in enumerate(foot) if J>>i&1) for i in range(2*r+2))
@functools.lru_cache(None)
def capacity(r):
 def weak(n,k):
  if k==1:yield (n,);return
  for x in range(n+1):
   for rest in weak(n-x,k-1):yield (x,)+rest
 V=[]
 for n in range(r+6):
  for v in weak(n,r+4):
   t,a,b=v[:3];c=v[3:-1]
   if v[-1]<1 or a+b+sum(c)<r+3 or any(t+a+k<3 or t+b+k<3 for k in c):continue
   assert safe(canonical(v,r),r);V.append(v)
 V.sort();minimum=min(map(sum,V));assert minimum==r+4+(r==2)
 return {'r':r,'vectors':[list(v) for v in V],'minimum':minimum,'witness':list(min(v for v in V if sum(v)==minimum))}
def components(V,E):
 adj=[[] for _ in V]
 for e in E:adj[e['from']].append(e['to']);adj[e['to']].append(e['from'])
 unseen=set(range(len(V)));out=[]
 while unseen:
  seed=min(unseen);unseen.remove(seed);todo=[seed];part=[]
  for a in todo:
   part.append(a)
   for b in adj[a]:
    if b in unseen:unseen.remove(b);todo.append(b)
  out.append(sorted(part))
 return sorted(out)
def graph(r):
 V=[tuple(v) for v in capacity(r)['vectors']];index={v:i for i,v in enumerate(V)};M=(0,)+types(r);E=[]
 for vi,v in enumerate(V):
  counts=(r+5-sum(v),)+v;s=canonical(v,r);cols=columns(s,r+5)
  for i,number in enumerate(counts):
   if not number:continue
   for j in range(len(M)):
    if i==j:continue
    w=list(counts);w[i]-=1;w[j]+=1;w=tuple(w[1:])
    if w not in index or index[w]<=vi:continue
    x=cols.index(M[i]);ops=[[root,x] for root in range(2*r+2) if M[i]>>root&1 and not M[j]>>root&1]+[[root,x] for root in range(2*r+2) if M[j]>>root&1 and not M[i]>>root&1];S=route(s,ops);meet=S[(M[i]&~M[j]).bit_count()]
    if not safe(meet,r):continue
    assert all(safe(a,r) for a in S)
    assert tuple(columns(S[-1],r+5).count(J) for J in types(r))==w
    E.append({'from':vi,'to':index[w],'i':i,'j':j,'ops':ops,'states':[list(a) for a in S]})
 E.sort(key=lambda e:(e['from'],e['to']));C=components(V,E)
 prep=[[i,r+3] for i in range(r)];expanded=route(source(r),prep);assert all(safe(s,r) for s in expanded)
 source_counts=tuple(columns(expanded[-1],r+5).count(J) for J in types(r));start=index[source_counts];part=next(c for c in C if start in c);minimum=min(sum(V[i]) for i in part);assert minimum==capacity(r)['minimum']
 adj={i:[] for i in range(len(V))}
 for e in E:adj[e['from']].append(e['to']);adj[e['to']].append(e['from'])
 parent={start:None};todo=[start];target=None
 for node in todo:
  if sum(V[node])<r+5:target=node;break
  for other in sorted(adj[node]):
   if other not in parent:parent[other]=node;todo.append(other)
 witness=[]
 while target is not None:witness.append(target);target=parent[target]
 witness.reverse();assert bool(witness)==(r>=3)
 return {'r':r,'vertices':[list(v) for v in V],'edges':E,'components':C,'source_expansion_ops':prep,'source_expansion_states':[list(z) for z in expanded],'vacancy_path':witness,'source_vertex':start,'source_component':part,'component_minimum_active':minimum}
def relabel(s,pi):return tuple(sum(1<<pi[x] for x in range(len(pi)) if a>>x&1) for a in s)
def macro(N,s,pi,L,reserve):
 ops=list(L);cur=route(s,ops)[-1];unused=set(range(N));cycles=[]
 while unused:
  start=min(unused);c=[];x=start
  while x not in c:c.append(x);unused.remove(x);x=pi[x]
  cycles.append(c)
 def rename(a,b):
  nonlocal cur
  assert all(not z>>b&1 for z in cur);J=[i for i,z in enumerate(cur) if z>>a&1];new=[[i,b] for i in J]+[[i,a] for i in J];ops.extend(new);cur=route(cur,new)[-1]
 for c in cycles:
  if reserve in c or len(c)==1:continue
  rename(c[-1],reserve)
  for j in range(len(c)-2,-1,-1):rename(c[j],c[j+1])
  rename(reserve,c[0])
 c=next(c for c in cycles if reserve in c);j=c.index(reserve);c=c[j:]+c[:j]
 for k in range(len(c)-1,0,-1):rename(c[k],pi[c[k]])
 assert cur==relabel(route(s,L)[-1],pi);ops.extend([[i,pi[x]] for i,x in L[::-1]]);assert route(s,ops)[-1]==relabel(s,pi);return ops
def permutations():
 N=8;out=set();work=[0,3,4,5,6];cover=[1,2,7]
 for group in (work,cover):
  for image in itertools.permutations(group):
   pi=list(range(N))
   for a,b in zip(group,image):pi[a]=b
   out.add(tuple(pi))
 for a,b in itertools.combinations(range(N),2):
  pi=list(range(N));pi[a],pi[b]=pi[b],pi[a];out.add(tuple(pi))
 for shift in range(N):out.add(tuple((i+shift)%N for i in range(N)))
 return sorted(out)
PAIRS=[((1,2,3,4,5,6,7,0),(7,0,1,2,3,4,5,6)),((0,2,1,3,4,5,6,7),(7,6,5,4,3,2,1,0)),((6,1,2,3,4,5,0,7),(0,2,7,3,4,5,6,1))]
def build(n=5):
 D={k:[] for k in ['sources','routes','capacity','graphs','permutations','renewal']};hidden=set();slices=0;script_slices=0;lift_slices=0
 def check(r,S,exact=False):
  nonlocal slices
  for s in S:assert safe(s,r) and (tau(s)==3 if exact else 3<=tau(s)<=4);hidden.add((r,s));slices+=1
 for r in range(2,n+1):
  s=source(r);f=floors(r);M=types(r);assert list(map(int.bit_count,s))==f and tau(s)==3
  assert all(any(J&~K==0 for K in M) for J in columns(s,r+5));masks=[m for m in range(1<<(2*r+2)) if fulltau(s,m)==3]
  # Every maximal donor is fixed; helper has exactly r+2 container choices.
  anchored=[]
  for reserve in range(r+5):
   choices=[[K for K in M if J&~K==0] if x!=reserve else [0] for x,J in enumerate(columns(s,r+5))]
   found=any(generic_safe(tuple(sum(1<<x for x,J in enumerate(v) if J>>i&1) for i in range(2*r+2)),f,M,r+5) for v in itertools.product(*choices));assert not found;anchored.append(reserve)
  D['sources'].append({'r':r,'source':list(s),'floors':f,'maxima':list(M),'protected_masks':masks,'anchored_failures':anchored});check(r,[s],True)
  if r==2:check(r,route(s,[[0,r+3]]),True)
  D['capacity'].append(capacity(r));g=graph(r);D['graphs'].append(g);check(r,list(map(tuple,g['source_expansion_states'])),True)
  for edge in g['edges']:S=list(map(tuple,edge['states']));check(r,S);lift_slices+=len(S)
  if r>=3:
   for a,b,c in itertools.permutations(range(r),3):
    ops=release(r,a,b,c);S=route(s,ops);check(r,S,True);script_slices+=len(S);assert len(ops)==4*r+6 and all(columns(z,r+5)[0] for z in S[:-1]) and columns(S[-1],r+5)[0]==0;assert all(sum(bool(J) for J in columns(z,r+5))==r+5 for z in S[:-1]);assert sum(bool(J) for J in columns(S[-1],r+5))==r+4
    assert list(map(int.bit_count,S[-1]))==f
    surplus=[max(z[i].bit_count()-f[i] for z in S) for i in range(2*r+2)];assert surplus[r+c]==2 and all(k<=1 for i,k in enumerate(surplus) if i!=r+c)
    assert all(all(z&(2|(4)|(1<<(r+4))) for z in st) for st in S)
    D['routes'].append({'r':r,'a':a,'b':b,'c':c,'ops':ops,'states':[list(z) for z in S],'maximum_surplus':surplus})
 s=source(3);L=release(3,0,1,2)
 for pi in permutations():
  ops=macro(8,s,pi,L,0);S=route(s,ops);check(3,S,True);D['permutations'].append({'pi':list(pi),'ops':ops,'states':[list(z) for z in S]})
 for pi,sigma in PAIRS:
  first=macro(8,s,pi,L,0);second=macro(8,relabel(s,pi),sigma,[[i,pi[x]] for i,x in L],pi[0]);ops=first+second;S=route(s,ops);check(3,S,True);D['renewal'].append({'pi':list(pi),'sigma':list(sigma),'boundary':len(first),'ops':ops,'states':[list(z) for z in S]})
 hiddenchecks=0;protected={r:[((1<<(2*r+2))-1)^m for m in range(1<<(2*r+2)) if fulltau(source(r),m)==3] for r in range(2,n+1)}
 for r,s in hidden:
  cols=columns(s,r+5)
  for outside in protected[r]:assert outside and not any(outside&~J==0 for J in cols);hiddenchecks+=1
 bad=list(source(3));bad[4]|=8;D['native_control']={'mask':166,'source_tau':fulltau(source(3),166),'candidate_tau':fulltau(tuple(bad),166)};assert D['native_control']['candidate_tau']==2
 singleton=(1,2,4);target=(2,1,4);count=columns(singleton,3);assert sorted(count)==sorted(columns(target,3));safe_first=sum(generic_safe(route(singleton,[[i,x]])[-1],[1]*3,(1,2,4),3) for i in range(3) for x in range(3));assert not safe_first;D['singleton_control']={'source':list(singleton),'target':list(target),'same_counts':True,'safe_first_toggles':safe_first}
 D['counts']={k:len(D[k]) for k in ['sources','routes','capacity','graphs','permutations','renewal']};D['counts'].update(capacity_vectors=sum(len(x['vectors']) for x in D['capacity']),count_vertices=sum(len(x['vertices']) for x in D['graphs']),count_edges=sum(len(x['edges']) for x in D['graphs']),count_components=sum(len(x['components']) for x in D['graphs']),all_slice_occurrences=slices,script_slices=script_slices,count_edge_lift_slices=lift_slices,unique_hidden_states=len(hidden),hidden_checks=hiddenchecks,component_minima=[x['component_minimum_active'] for x in D['graphs']]);return D
if __name__=='__main__':
 d=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(d['counts'],sort_keys=True))
