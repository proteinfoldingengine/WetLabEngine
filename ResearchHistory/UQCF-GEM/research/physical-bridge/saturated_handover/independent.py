"""Set-support reconstruction; never imports producer."""
import collections,functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def hit(roots):
 if not roots:return 0
 if any(not a for a in roots):return 99
 a=min(roots,key=len);return 1+min(hit(tuple(b for b in roots if x not in b)) for x in a)
def raw(roots):return tuple(sum(2**x for x in a) for a in roots)
def supports(state):return tuple(frozenset(x for x in range(a.bit_length()) if a&(2**x)) for a in state)
@functools.lru_cache(None)
def original(r):return tuple([frozenset([0,1,i+3]) for i in range(r)]+[frozenset([0,2,i+3]) for i in range(r)]+[frozenset(range(1,r+4)),frozenset([r+4])])
@functools.lru_cache(None)
def footprints(roots,N):return tuple(frozenset(i for i,a in enumerate(roots) if x in a) for x in range(N))
@functools.lru_cache(None)
def maxima(r):
 F=footprints(original(r),r+5);nonempty={f for f in F if f};actual={a for a in nonempty if not any(a<b for b in nonempty)}
 # Published type order follows the named original maximal donors.
 order=tuple(F[x] for x in [0,1,2]+list(range(3,r+3))+[r+4]);assert set(order)==actual and len(order)==len(actual);return order
def floor_values(r):return [len(a) for a in original(r)]
def gate(roots,r):return all(a<=frozenset(range(r+5)) for a in roots) and all(len(a)>=f for a,f in zip(roots,floor_values(r))) and hit(roots)<=4 and all(any(a<=b for b in maxima(r)) for a in footprints(roots,r+5))
def hidden_tau(roots,m):return min(hit(roots),1+hit(tuple(a for i,a in enumerate(roots) if not m&(2**i))))
def path(start,ops):
 cur=supports(start);out=[cur]
 for root,label in ops:changed=list(cur);changed[root]^=frozenset([label]);cur=tuple(changed);out.append(cur)
 return out
def operations(r,a,b,c):
 out=[[a,r+3],[b,r+3],[c,r+3],[a,a+3]]
 out.extend([r+i,a+3] for i in range(r) if i!=a);out.extend([[b,b+3],[r+a,b+3],[r+c,b+3],[r+c,c+3]]);out.extend([i,c+3] for i in range(r) if i!=c);out.extend([i,0] for i in range(2*r));return out
def assignment(v,r):
 assigned=[frozenset()]*(r+5-sum(v))
 for f,number in zip(maxima(r),v):assigned.extend([f]*number)
 return tuple(frozenset(x for x,f in enumerate(assigned) if i in f) for i in range(2*r+2))
@functools.lru_cache(None)
def vector_universe(r):
 M=maxima(r);V=[]
 for n in range(r+6):
  for multiset in itertools.combinations_with_replacement(range(len(M)),n):
   counts=collections.Counter(multiset);v=tuple(counts[j] for j in range(len(M)))
   if any(sum(v[j] for j,f in enumerate(M) if i in f)<bound for i,bound in enumerate(floor_values(r))):continue
   roots=assignment(v,r)
   if hit(roots)<=4:V.append(v)
 return sorted(V)
def partition(V,E):
 parent=list(range(len(V)))
 def find(a):
  while parent[a]!=a:a=parent[a]
  return a
 for e in E:parent[find(e['from'])]=find(e['to'])
 groups=collections.defaultdict(list)
 for i in range(len(V)):groups[find(i)].append(i)
 return sorted(groups.values())
def reconstruct_graph(r):
 V=vector_universe(r);M=(frozenset(),)+maxima(r);E=[]
 for ai,bi in itertools.combinations(range(len(V)),2):
  a,b=V[ai],V[bi];ca=(r+5-sum(a),)+a;cb=(r+5-sum(b),)+b;diff=[x-y for x,y in zip(ca,cb)]
  if sum(abs(x) for x in diff)!=2:continue
  i=diff.index(1);j=diff.index(-1);s=assignment(a,r);cols=footprints(s,r+5);label=cols.index(M[i]);meet=list(s)
  for root in M[i]-M[j]:meet[root]=meet[root]-frozenset([label])
  if not gate(tuple(meet),r):continue
  ops=[[root,label] for root in sorted(M[i]-M[j])]+[[root,label] for root in sorted(M[j]-M[i])];S=path(raw(s),ops);assert all(gate(z,r) for z in S);assert tuple(footprints(S[-1],r+5).count(f) for f in maxima(r))==b
  E.append({'from':ai,'to':bi,'i':i,'j':j,'ops':ops,'states':[list(raw(z)) for z in S]})
 C=partition(V,E);prep=[[i,r+3] for i in range(r)];expanded=path(raw(original(r)),prep);assert all(gate(s,r) for s in expanded);f=footprints(expanded[-1],r+5);source_counts=tuple(f.count(m) for m in maxima(r));start=V.index(source_counts);part=next(c for c in C if start in c)
 neighbors=collections.defaultdict(set)
 for edge in E:neighbors[edge['from']].add(edge['to']);neighbors[edge['to']].add(edge['from'])
 queue=collections.deque([start]);paths={start:[start]};witness=[]
 while queue:
  node=queue.popleft()
  if sum(V[node])<r+5:witness=paths[node];break
  for other in sorted(neighbors[node]):
   if other not in paths:paths[other]=paths[node]+[other];queue.append(other)
 return {'r':r,'vertices':[list(v) for v in V],'edges':E,'components':C,'source_expansion_ops':prep,'source_expansion_states':[list(raw(z)) for z in expanded],'vacancy_path':witness,'source_vertex':start,'source_component':part,'component_minimum_active':min(sum(V[i]) for i in part)}
def permutation_universe():
 out=set();identity=tuple(range(8))
 for roles in ([0,3,4,5,6],[1,2,7]):
  for perm in itertools.permutations(roles):
   d=dict(zip(roles,perm));out.add(tuple(d.get(i,i) for i in identity))
 out.update(tuple(b if i==a else a if i==b else i for i in identity) for a in identity for b in identity if a<b)
 out.update(tuple(identity[shift:]+identity[:shift]) for shift in identity);return sorted(out)
def image(roots,pi):return tuple(frozenset(pi[x] for x in a) for a in roots)
PAIRS=[([1,2,3,4,5,6,7,0],[7,0,1,2,3,4,5,6]),([0,2,1,3,4,5,6,7],[7,6,5,4,3,2,1,0]),([6,1,2,3,4,5,0,7],[0,2,7,3,4,5,6,1])]
def verify(D,n=5):
 hidden=set();slices=script_slices=lift_slices=0
 def check(r,S,exact=False):
  nonlocal slices
  for s in S:assert gate(s,r) and (hit(s)==3 if exact else 3<=hit(s)<=4),'unsafe slice';hidden.add((r,s));slices+=1
 assert [x['r'] for x in D['sources']]==list(range(2,n+1)),'source universe'
 for row in D['sources']:
  r=row['r'];s=original(r);assert row['source']==list(raw(s)) and row['floors']==floor_values(r);assert row['maxima']==[sum(2**i for i in f) for f in maxima(r)];assert row['protected_masks']==[m for m in range(2**(2*r+2)) if hidden_tau(s,m)==3]
  assert row['anchored_failures']==list(range(r+5))
  for reserve in range(r+5):
   choices=[([frozenset()] if x==reserve else [f for f in maxima(r) if old<=f]) for x,old in enumerate(footprints(s,r+5))]
   for choice in itertools.product(*choices):
    roots=tuple(frozenset(x for x,f in enumerate(choice) if i in f) for i in range(2*r+2));assert not gate(roots,r),'anchored positive'
  check(r,[s],True)
  if r==2:check(r,path(raw(s),[[0,r+3]]),True)
 assert [x['r'] for x in D['capacity']]==list(range(2,n+1)),'capacity universe'
 for row in D['capacity']:
  V=vector_universe(row['r']);assert row['vectors']==[list(v) for v in V],'complete vectors';minimum=min(map(sum,V));assert row['minimum']==minimum==row['r']+4+(row['r']==2);assert row['witness']==list(min(v for v in V if sum(v)==minimum))
 assert [x['r'] for x in D['graphs']]==list(range(2,n+1)),'graph universe'
 for row in D['graphs']:
  expected=reconstruct_graph(row['r']);assert row==expected,'complete graph vertices/edges/components/lifts';assert row['component_minimum_active']==row['r']+4+(row['r']==2)
  check(row['r'],list(map(supports,expected['source_expansion_states'])),True)
  for edge in expected['edges']:S=list(map(supports,edge['states']));check(row['r'],S);lift_slices+=len(S)
 ids=[(r,a,b,c) for r in range(3,n+1) for a in range(r) for b in range(r) for c in range(r) if len({a,b,c})==3];assert [(x['r'],x['a'],x['b'],x['c']) for x in D['routes']]==ids,'route universe'
 for row in D['routes']:
  r,a,b,c=(row[k] for k in ['r','a','b','c']);ops=operations(r,a,b,c);assert row['ops']==ops,'native operations';S=path(raw(original(r)),ops);assert row['states']==[list(raw(s)) for s in S];check(r,S,True);script_slices+=len(S)
  assert len(ops)==4*r+6 and all(0 in set().union(*s) for s in S[:-1]) and 0 not in set().union(*S[-1]);assert all(len(set().union(*s))==r+5 for s in S[:-1]);assert len(set().union(*S[-1]))==r+4;assert list(map(len,S[-1]))==floor_values(r)
  surplus=[max(len(s[i])-floor_values(r)[i] for s in S) for i in range(2*r+2)];assert row['maximum_surplus']==surplus;assert surplus[r+c]==2 and all(v<=1 for i,v in enumerate(surplus) if i!=r+c);assert all(all(a&{1,2,r+4} for a in s) for s in S)
 assert [x['pi'] for x in D['permutations']]==list(map(list,permutation_universe())),'permutation universe';L=operations(3,0,1,2)
 for row in D['permutations']:
  pi=row['pi'];S=path(raw(original(3)),row['ops']);assert row['states']==[list(raw(s)) for s in S];check(3,S,True);assert S[-1]==image(original(3),pi);assert row['ops'][:18]==L and row['ops'][-18:]==[[i,pi[x]] for i,x in L[::-1]]
 assert [(x['pi'],x['sigma']) for x in D['renewal']]==PAIRS,'renewal universe'
 for row in D['renewal']:
  pi,sigma=row['pi'],row['sigma'];ops=row['ops'];S=path(raw(original(3)),ops);assert row['states']==[list(raw(s)) for s in S];check(3,S,True);b=row['boundary'];PL=[[i,pi[x]] for i,x in L];assert S[b]==image(original(3),pi) and S[-1]==image(image(original(3),pi),sigma);assert ops[:18]==L and ops[b-18:b]==PL[::-1] and ops[b:b+18]==PL and ops[-18:]==[[i,sigma[x]] for i,x in PL[::-1]],'renewal restoration'
 protected={r:[frozenset(i for i in range(2*r+2) if not m&(2**i)) for m in range(2**(2*r+2)) if hidden_tau(original(r),m)==3] for r in range(2,n+1)};checks=0
 for r,s in hidden:
  f=footprints(s,r+5)
  for outside in protected[r]:assert outside and not any(outside<=a for a in f),'hidden lower bound';checks+=1
 bad=list(raw(original(3)));bad[4]|=8;assert D['native_control']=={'mask':166,'source_tau':hidden_tau(original(3),166),'candidate_tau':hidden_tau(supports(tuple(bad)),166)};assert not gate(supports(tuple(bad)),3)
 S=supports((1,2,4));T=supports((2,1,4));M=footprints(S,3);assert sorted(map(sorted,M))==sorted(map(sorted,footprints(T,3)))
 def singleton_gate(s):return all(s) and all(a<=frozenset(range(3)) for a in s) and hit(s)<=4 and all(any(a<=b for b in M) for a in footprints(s,3))
 first=sum(singleton_gate(path(raw(S),[[i,x]])[-1]) for i in range(3) for x in range(3));assert D['singleton_control']=={'source':[1,2,4],'target':[2,1,4],'same_counts':True,'safe_first_toggles':first} and first==0
 counts={k:len(D[k]) for k in ['sources','routes','capacity','graphs','permutations','renewal']};counts.update(capacity_vectors=sum(len(x['vectors']) for x in D['capacity']),count_vertices=sum(len(x['vertices']) for x in D['graphs']),count_edges=sum(len(x['edges']) for x in D['graphs']),count_components=sum(len(x['components']) for x in D['graphs']),all_slice_occurrences=slices,script_slices=script_slices,count_edge_lift_slices=lift_slices,unique_hidden_states=len(hidden),hidden_checks=checks,component_minima=[x['component_minimum_active'] for x in D['graphs']]);assert D['counts']==counts,'counts';return counts
if __name__=='__main__':
 d=verify(json.loads(pathlib.Path(sys.argv[1]).read_text()));result={'status':'ACCEPTED','complete_identity_comparison':True,'counts':d};pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
