"""Set-based independent reconstruction. Never imports the producer."""
import itertools,json,hashlib,functools,pathlib,sys

def serial(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(serial(x).encode()).hexdigest()
def support(mask):return frozenset(i for i in range(mask.bit_length()) if mask&(1<<i))
def number(S):return sum(1<<i for i in S)
def rootsets(footprints,n):return tuple(frozenset(j for j,F in enumerate(footprints) if i in F) for i in range(n))
@functools.lru_cache(None)
def hit(roots):
 roots=frozenset(roots)
 if not roots:return 0
 if frozenset() in roots:return 99
 first=min(roots,key=lambda a:(len(a),tuple(sorted(a))))
 return 1+min(hit(frozenset(R for R in roots if x not in R)) for x in first)
def fullhit(R,mask):return min(hit(frozenset(R)),1+hit(frozenset(S for i,S in enumerate(R) if i not in support(mask))))
def maxima(C):return tuple(sorted({F for F in C if F and not any(F<G for G in C)},key=number))
def iscover(C,H,n):return set().union(*(C[x] for x in H))==set(range(n))
def valid(C,f,M):
 R=rootsets(C,len(f));return all(len(S)>=a for S,a in zip(R,f)) and hit(frozenset(R))<=4 and all(any(F<=G for G in M) for F in C)
def partition(length,edges):
 parent=list(range(length))
 def root(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for a,b in edges:parent[root(a)]=root(b)
 parts={}
 for a in range(length):parts.setdefault(root(a),[]).append(a)
 return sorted(parts.values())
def native(C,x,destination,n):
 cur=list(C);out=[tuple(map(number,cur))];ops=[]
 for i in sorted(cur[x]-destination):cur[x]=cur[x]-{i};ops.append([i,x]);out.append(tuple(map(number,cur)))
 for i in sorted(destination-cur[x]):cur[x]=cur[x]|{i};ops.append([i,x]);out.append(tuple(map(number,cur)))
 return ops,out
def universe(fixture):
 if fixture:return [('A',(1,1,2,4,8))]
 out=[]
 # Multiplicity enumeration, distinct from multiset iterator used by producer.
 for group,n,alphabet in [('A',4,(1,2,3,4,5,6)),('B',5,(1,2,4))]:
  for counts in itertools.product(range(n+1),repeat=len(alphabet)):
   if sum(counts)!=n:continue
   v=tuple(a for a,c in zip(alphabet,counts) for _ in range(c))
   if set().union(*(support(a) for a in v))=={0,1,2}:out.append((group,v+(8,)))
 return sorted(out)

@functools.lru_cache(None)
def marked_graph(N,d,M,F):
 K=len(M);n=4
 Q=[]
 for marks in itertools.product(range(K),repeat=d):
  if set().union(*(M[j] for j in marks[:4]))!=set(range(n)):continue
  for rest in itertools.combinations_with_replacement(range(K),N-d):
   if valid(tuple(M[j] for j in marks+rest),F,M[1:]):Q.append((marks,tuple(rest.count(j) for j in range(K))))
 Q.sort();qi={v:i for i,v in enumerate(Q)}
 QE=set()
 # Direct canonical marked/unmarked transition generation with exact H meet.
 for a,(marks,counts) in enumerate(Q):
  seq=marks+tuple(j for j,c in enumerate(counts) for _ in range(c));actual=tuple(M[j] for j in seq)
  for x in range(N):
   for new in range(K):
    if new==seq[x]:continue
    w=seq[:x]+(new,)+seq[x+1:];key=(w[:d],tuple(w[d:].count(j) for j in range(K)));b=qi.get(key,-1)
    if b<=a:continue
    meet=list(actual);meet[x]=M[seq[x]]&M[new]
    if valid(tuple(meet),F,M[1:]) and iscover(tuple(meet),range(4),n):QE.add((a,b))
 return Q,sorted(QE)

def reconstruct_case(group,numbers,mode):
 C=tuple(map(support,numbers));N=len(C);n=4;R=rootsets(C,n);F=tuple(max(1,len(S)-int(mode=='slack')) for S in R[:3])+(1,);M=(frozenset(),)+maxima(C);K=len(M)
 V=[]
 for v in itertools.product(range(K),repeat=N):
  if valid(tuple(M[i] for i in v),F,M[1:]):V.append(v)
 index={v:i for i,v in enumerate(V)};col=[tuple(M[i] for i in v) for v in V];E=[];data=[];lifts=[];states={tuple(map(number,c)) for c in col};slices=0
 # Group by unchanged coordinates; compare all alternate donor types per bucket.
 for x in range(N):
  groups={}
  for i,v in enumerate(V):groups.setdefault(v[:x]+v[x+1:],[]).append(i)
  for bucket in groups.values():
   for a,b in itertools.combinations(bucket,2):
    meet=list(col[a]);meet[x]=col[a][x]&col[b][x]
    if not valid(tuple(meet),F,M[1:]):continue
    op,S=native(col[a],x,col[b][x],n);E.append((a,b));lifts.append([a,b,op,S]);data.append((a,b,tuple(meet),S));states.update(S);slices+=len(S)
 E.sort();lifts.sort(key=lambda a:(a[0],a[1]));data.sort(key=lambda a:(a[0],a[1]));parts=partition(len(V),E)
 expansion=tuple(next(j for j,Q in enumerate(M) if Q and P<=Q) for P in C);start=index[expansion];part=next(p for p in parts if start in p)
 expops=[];expstates=[numbers];cur=C
 for x,j in enumerate(expansion):
  op,S=native(cur,x,M[j],n);expops.extend(op);expstates.extend(S[1:]);cur=tuple(map(support,S[-1]))
 states.update(expstates);slices+=len(expstates);reach=[any(0 in V[i] for i in part)]+[any(V[i][x]==0 for i in part) for x in range(N)]
 covers=[];orbit=0;fixedslices=0
 for H in itertools.combinations(range(N),4):
  if not iscover(C,H,n):continue
  good=[i for i,c in enumerate(col) if iscover(c,H,n)];goodset=set(good);HE=[(a,b) for a,b,m,S in data if a in goodset and b in goodset and iscover(m,H,n)]
  for a,b,m,S in data:
   if a in goodset and b in goodset and iscover(m,H,n):
    assert all(iscover(tuple(map(support,s)),H,n) for s in S);fixedslices+=len(S)
  adjacency={i:[] for i in good}
  for a,b in HE:adjacency[a].append(b);adjacency[b].append(a)
  for target in range(-1,N):
   D=H+((target,) if target>=0 and target not in H else ());U=[x for x in range(N) if x not in D]
   def project(v):return tuple(v[x] for x in D),tuple(sum(v[x]==j for x in U) for j in range(K))
   Q,QE=marked_graph(N,len(D),M,F);qi={v:i for i,v in enumerate(Q)}
   assert Q==sorted({project(V[i]) for i in good})
   QE=sorted(QE);assert QE==sorted({tuple(sorted((qi[project(V[a])],qi[project(V[b])]))) for a,b in HE})
   qparts=partition(len(Q),QE);qs=qi[project(expansion)];qp=next(p for p in qparts if qs in p);qadj={i:set() for i in range(len(Q))}
   for a,b in QE:qadj[a].add(b);qadj[b].add(a)
   for i in good:
    targets={qi[project(V[j])] for j in adjacency[i]};assert targets==qadj[qi[project(V[i])]];orbit+=len(targets)
   vacancy=[]
   for i,(marks,counts) in enumerate(Q):
    absent=(0 in marks or counts[0]>0) if target<0 else marks[D.index(target)]==0
    if absent:vacancy.append(i)
   reachable=bool(set(vacancy)&set(qp));local={old:j for j,old in enumerate(good)};hp=partition(len(good),[(local[a],local[b]) for a,b in HE]);sp=next(p for p in hp if local[start] in p)
   assert sorted({qi[project(V[good[j]])] for j in sp})==qp
   rawvac=[i for i in good if (0 in V[i] if target<0 else V[i][target]==0)]
   assert sorted({qi[project(V[i])] for i in rawvac})==vacancy
   assert reachable==any((0 in V[good[j]]) if target<0 else V[good[j]][target]==0 for j in sp)
   covers.append({'H':H,'target':target,'D':D,'vertices':len(Q),'edges':len(QE),'vertices_hash':sha(Q),'edges_hash':sha(QE),'components_hash':sha(qparts),'source':qs,'source_component_hash':sha(qp),'vacancies_hash':sha(vacancy),'reachable':reachable})
 masks=[m for m in range(16) if 3<=fullhit(R,m)<=4]
 for s in states:
  Cnow=tuple(map(support,s));assert valid(Cnow,F,M[1:]);now=rootsets(Cnow,n)
  for mask in masks:assert 3<=fullhit(now,mask)<=4
 return {'group':group,'source':numbers,'mode':mode,'floors':F,'maxima':tuple(map(number,M[1:])),'vertices':len(V),'edges':len(E),'components':len(parts),'vertices_hash':sha(V),'edges_hash':sha(E),'components_hash':sha(parts),'source_vertex':start,'source_component_hash':sha(part),'reachable':reach,'lifts_hash':sha(lifts),'expansion_ops':expops,'expansion_states':expstates,'covers':covers,'slice_occurrences':slices,'fixed_cover_lift_slices':fixedslices,'orbit_edge_lifts':orbit,'hidden_states':len(states),'protected_masks':masks,'hidden_checks':len(states)*len(masks)}

def reconstruct_family(r,triple):
 N=r+6;n=2*r+3;R=[{0,1,i+3} for i in range(r)]+[{0,2,i+3} for i in range(r)]+[set(range(1,r+4)),{r+4},{r+5}];source=tuple(number(S) for S in R);C=tuple(frozenset(i for i,S in enumerate(R) if x in S) for x in range(N));F=tuple(map(len,R));M=maxima(C)
 anchored=[]
 for reserve in range(N):
  options=[(frozenset(),) if x==reserve else tuple(B for B in M if A<=B) for x,A in enumerate(C)]
  assert not any(valid(c,F,M) for c in itertools.product(*options));anchored.append(reserve)
 capacity=[]
 for count in range(N+1):
  for seq in itertools.combinations_with_replacement(range(len(M)),count):
   if valid(tuple(M[j] for j in seq),F,M):capacity.append(tuple(seq.count(j) for j in range(len(M))))
 minimum=min(map(sum,capacity));assert minimum==r+5+(r==2)
 covers=[H for H in itertools.combinations(range(N),4) if iscover(C,H,n)];assert all(r+4 in H and r+5 in H for H in covers)
 ops=[]
 if triple is None:ops=[(0,r+3)]
 else:
  a,b,c=triple
  ops.extend((j,r+3) for j in triple);ops.append((a,a+3));ops.extend((r+j,a+3) for j in range(r) if j!=a);ops.extend(((b,b+3),(r+a,b+3),(r+c,b+3),(r+c,c+3)));ops.extend((j,c+3) for j in range(r) if j!=c);ops.extend((j,0) for j in range(2*r));ops.extend(((2*r+1,0),(2*r+1,r+4)))
 states=[source];current=[set(S) for S in R]
 for root,x in ops:current[root].symmetric_difference_update({x});states.append(tuple(number(S) for S in current))
 masks=[m for m in range(1<<n) if 3<=fullhit(tuple(map(frozenset,R)),m)<=4]
 for s in states:
  roots=tuple(map(support,s));cnow=tuple(frozenset(i for i,A in enumerate(roots) if x in A) for x in range(N));assert valid(cnow,F,M) and hit(frozenset(roots))==4
  for mask in masks:assert 3<=fullhit(roots,mask)<=4
 if triple:
  assert len(ops)==4*r+8
  for s in states[:4*r+6]:assert set().union(*(support(a) for a in s))==set(range(N))
  assert all(0 not in support(a) for a in states[4*r+6]);assert all(r+4 not in support(a) for a in states[-1]);assert tuple(len(support(a)) for a in states[-1])==F
  last=tuple(frozenset(i for i,A in enumerate(map(support,states[-1])) if x in A) for x in range(N));assert last[0]=={2*r+1};failed=[H for H in covers if not iscover(last,H,n)];assert failed==covers
  for j,s in enumerate(states):
   H={1,2,r+4,r+5} if j<4*r+7 else {1,2,0,r+5};assert all(support(a)&H for a in s)
 else:failed=[]
 return {'r':r,'triple':triple,'source':source,'floors':F,'maxima':tuple(map(number,M)),'source_covers':covers,'anchored_failures':anchored,'capacity_vectors':len(capacity),'capacity_hash':sha(sorted(capacity)),'minimum_active':minimum,'ops':ops,'states':states,'failed_source_covers':failed,'protected_masks':masks,'hidden_checks':len(set(states))*len(masks)}

@functools.lru_cache(None)
def reconstruct(fixture=False):
 cases=[reconstruct_case(g,C,mode) for g,C in universe(fixture) for mode in ('saturated','slack')]
 families=[reconstruct_family(3,(0,1,2))] if fixture else [reconstruct_family(2,None)]+[reconstruct_family(r,t) for r in (3,4) for t in itertools.permutations(range(r),3)]
 counts={'sources':len(universe(fixture)),'cases':len(cases),'families':len(families),'vertices':sum(c['vertices'] for c in cases),'edges':sum(c['edges'] for c in cases),'cover_jobs':sum(len(c['covers']) for c in cases),'quotient_vertices':sum(q['vertices'] for c in cases for q in c['covers']),'quotient_edges':sum(q['edges'] for c in cases for q in c['covers']),'orbit_edge_lifts':sum(c['orbit_edge_lifts'] for c in cases),'native_slice_occurrences':sum(c['slice_occurrences'] for c in cases)+sum(len(f['states']) for f in families),'fixed_cover_lift_slices':sum(c['fixed_cover_lift_slices'] for c in cases),'hidden_checks':sum(c['hidden_checks'] for c in cases)+sum(f['hidden_checks'] for f in families)}
 return {'cases':cases,'families':families,'counts':counts}
def verify(data,fixture=False):
 expected=reconstruct(fixture)
 assert serial(data)==serial(expected),'Complete independently reconstructed identities differ'
 return True
if __name__=='__main__':
 d=json.loads(pathlib.Path(sys.argv[1]).read_text());verify(d);out={'status':'ACCEPTED','complete_identity_comparison':True,'counts':d['counts']};pathlib.Path(sys.argv[2]).write_text(json.dumps(out,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
