"""Bitmask producer: exhaustive labelled graphs and marked-cover orbit quotients."""
import itertools as it, functools,json,hashlib,pathlib,sys

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rows(cols,n):return tuple(sum(1<<x for x,J in enumerate(cols) if J>>i&1) for i in range(n))
def columns(s,N):return tuple(sum(1<<i for i,a in enumerate(s) if a>>x&1) for x in range(N))
@functools.lru_cache(None)
def tau(s):
 if not s:return 0
 if 0 in s:return 99
 U=functools.reduce(int.__or__,s)
 for k in range(U.bit_count()+1):
  if any(all(a&sum(c) for a in s) for c in it.combinations([1<<x for x in range(U.bit_length()) if U>>x&1],k)):return k
 return 99
def full(s,m):return min(tau(s),1+tau(tuple(a for i,a in enumerate(s) if not m>>i&1)))
def covered(cols,H,roots):return functools.reduce(int.__or__,(cols[x] for x in H),0)==(1<<roots)-1
def target_empty(markers,counts,target_index):return (0 in markers or counts[0]>0) if target_index is None else markers[target_index]==0
def maxima(cols):return tuple(sorted(J for J in set(cols) if J and not any(J!=K and J&~K==0 for K in cols)))
def feasible(cols,F,M):return all(a.bit_count()>=f for a,f in zip(rows(cols,len(F)),F)) and tau(rows(cols,len(F)))<=4 and all(any(J&~K==0 for K in M) for J in cols)
def components(V,E):
 A=[[] for _ in V]
 for i,j in E:A[i].append(j);A[j].append(i)
 unseen=set(range(len(V)));out=[]
 while unseen:
  todo=[min(unseen)];unseen.remove(todo[0])
  for x in todo:
   for y in A[x]:
    if y in unseen:unseen.remove(y);todo.append(y)
  out.append(sorted(todo))
 return sorted(out)
def lift(cols,x,K,n):
 cur=list(cols);ops=[];states=[tuple(cur)];old=cur[x]
 for i in range(n):
  if old>>i&1 and not K>>i&1:ops.append([i,x]);cur[x]^=1<<i;states.append(tuple(cur))
 for i in range(n):
  if K>>i&1 and not old>>i&1:ops.append([i,x]);cur[x]^=1<<i;states.append(tuple(cur))
 return ops,states
def weak(n,k):
 if k==1:yield (n,);return
 for j in range(n+1):
  for rest in weak(n-j,k-1):yield (j,)+rest

@functools.lru_cache(None)
def quotient_universe(N,d,M,F):
 out=[];K=len(M)
 for marks in it.product(range(K),repeat=d):
  if functools.reduce(int.__or__,(M[j] for j in marks[:4]),0)!=15:continue
  for counts in weak(N-d,K):
   v=marks+tuple(j for j,c in enumerate(counts) for _ in range(c))
   if feasible(tuple(M[j] for j in v),F,M[1:]):out.append((marks,counts))
 return sorted(out)

def sources(fixture=False):
 if fixture:return [('A',(1,1,2,4,8))]
 out=[]
 for group,N,alphabet in [('A',4,range(1,7)),('B',5,(1,2,4))]:
  for c in it.combinations_with_replacement(alphabet,N):
   if functools.reduce(int.__or__,c)==7:out.append((group,c+(8,)))
 return out

def case(group,C,mode):
 N=len(C);n=4;F=tuple(max(1,a.bit_count()-(mode=='slack')) for a in rows(C,n)[:3])+(1,);M=(0,)+maxima(C);K=len(M)
 V=[v for v in it.product(range(K),repeat=N) if feasible(tuple(M[j] for j in v),F,M[1:])];idx={v:i for i,v in enumerate(V)};cols=[tuple(M[j] for j in v) for v in V];E=[];edge_data=[];allstates=set(cols);lift_records=[];slice_occ=0
 for i,v in enumerate(V):
  for x in range(N):
   for j in range(K):
    w=v[:x]+(j,)+v[x+1:];b=idx.get(w,-1)
    if b<=i:continue
    meet=list(cols[i]);meet[x]&=M[j]
    if not feasible(tuple(meet),F,M[1:]):continue
    E.append((i,b));ops,S=lift(cols[i],x,M[j],n)
    assert all(feasible(s,F,M[1:]) for s in S)
    allstates.update(S);slice_occ+=len(S);lift_records.append([i,b,ops,S]);edge_data.append((i,b,x,tuple(meet),S))
 # Iteration order is vertex, donor, type; canonical edge/lift identities sorted.
 E.sort();lift_records.sort(key=lambda a:(a[0],a[1]));edge_data.sort(key=lambda a:(a[0],a[1]));parts=components(V,E)
 expansion=tuple(min(i for i,J in enumerate(M) if J and c&~J==0) for c in C);start=idx[expansion];part=next(p for p in parts if start in p)
 expcols=list(C);expops=[];expstates=[C]
 for x,j in enumerate(expansion):
  op,S=lift(tuple(expcols),x,M[j],n);expops.extend(op);expstates.extend(S[1:]);expcols=list(S[-1])
 allstates.update(expstates);slice_occ+=len(expstates)
 reach=[any(0 in V[i] for i in part)]+[any(V[i][x]==0 for i in part) for x in range(N)]
 covers=[];orbit_lifts=0;fixed_lift_slices=0
 for H in it.combinations(range(N),4):
  if not covered(C,H,n):continue
  HV=[i for i,c in enumerate(cols) if covered(c,H,n)];Hset=set(HV);HE=[(a,b) for a,b,x,meet,S in edge_data if a in Hset and b in Hset and covered(meet,H,n)]
  for a,b,x,meet,S in edge_data:
   if a in Hset and b in Hset and covered(meet,H,n):assert all(covered(c,H,n) for c in S);fixed_lift_slices+=len(S)
  for target in [-1]+list(range(N)):
   D=H+((target,) if target>=0 and target not in H else ());U=tuple(x for x in range(N) if x not in D)
   def key(v):return tuple(v[x] for x in D),tuple(sum(v[x]==j for x in U) for j in range(K))
   Q=sorted({key(V[i]) for i in HV});qi={v:i for i,v in enumerate(Q)};QE=sorted({tuple(sorted((qi[key(V[a])],qi[key(V[b])]))) for a,b in HE});Qparts=components(Q,QE);qstart=qi[key(expansion)];qpart=next(p for p in Qparts if qstart in p)
   # Derive quotient universe independently from marked products/count compositions.
   assert quotient_universe(N,len(D),M,F)==Q
   qadj={i:set() for i in range(len(Q))}
   for a,b in QE:qadj[a].add(b);qadj[b].add(a)
   hadj={i:set() for i in HV}
   for a,b in HE:hadj[a].add(b);hadj[b].add(a)
   for i in HV:
    actual={qi[key(V[j])] for j in hadj[i]};assert actual==qadj[qi[key(V[i])]];orbit_lifts+=len(actual)
   ti=None if target<0 else D.index(target);vac=[i for i,(marks,counts) in enumerate(Q) if target_empty(marks,counts,ti)];reachable=bool(set(vac)&set(qpart))
   hparts=components(HV,[(HV.index(a),HV.index(b)) for a,b in HE]);hsource=next(p for p in hparts if HV.index(start) in p)
   assert sorted({qi[key(V[HV[j]])] for j in hsource})==qpart
   rawvac=[i for i in HV if (0 in V[i] if target<0 else V[i][target]==0)]
   assert sorted({qi[key(V[i])] for i in rawvac})==vac
   rawreach=any((0 in V[HV[j]]) if target<0 else V[HV[j]][target]==0 for j in hsource);assert reachable==rawreach
   covers.append({'H':H,'target':target,'D':D,'vertices':len(Q),'edges':len(QE),'vertices_hash':digest(Q),'edges_hash':digest(QE),'components_hash':digest(Qparts),'source':qstart,'source_component_hash':digest(qpart),'vacancies_hash':digest(vac),'reachable':reachable})
 masks=[m for m in range(16) if 3<=full(rows(C,n),m)<=4]
 for s in sorted(allstates):
  assert feasible(s,F,M[1:])
  for m in masks:assert 3<=full(rows(s,n),m)<=4
 return {'group':group,'source':C,'mode':mode,'floors':F,'maxima':M[1:],'vertices':len(V),'edges':len(E),'components':len(parts),'vertices_hash':digest(V),'edges_hash':digest(E),'components_hash':digest(parts),'source_vertex':start,'source_component_hash':digest(part),'reachable':reach,'lifts_hash':digest(lift_records),'expansion_ops':expops,'expansion_states':expstates,'covers':covers,'slice_occurrences':slice_occ,'fixed_cover_lift_slices':fixed_lift_slices,'orbit_edge_lifts':orbit_lifts,'hidden_states':len(allstates),'protected_masks':masks,'hidden_checks':len(allstates)*len(masks)}

def family(r,triple):
 N=r+6;n=2*r+3;b=0;u=1;v=2;y=r+3;e=r+4;z=r+5
 S=tuple([3|(1<<(i+3)) for i in range(r)]+[5|(1<<(i+3)) for i in range(r)]+[(1<<(r+4))-2,1<<e,1<<z]);C=columns(S,N);F=tuple(a.bit_count() for a in S);M=maxima(C)
 anchored=[]
 for x in range(N):
  choices=[(0,) if j==x else tuple(K for K in M if J&~K==0) for j,J in enumerate(C)]
  assert not any(feasible(t,F,M) for t in it.product(*choices));anchored.append(x)
 cap=[]
 for total in range(N+1):
  for counts in weak(total,len(M)):
   cols=tuple(K for count,K in zip(counts,M) for _ in range(count))
   if feasible(cols,F,M):cap.append(counts)
 minimum=min(map(sum,cap));assert minimum==N-(r>=3)
 Hs=[H for H in it.combinations(range(N),4) if covered(C,H,n)];assert all(e in H and z in H for H in Hs)
 if triple is None:ops=[[0,y]]
 else:
  a,d,c=triple
  ops=[[j,y] for j in triple]+[[a,a+3]]+[[r+j,a+3] for j in range(r) if j!=a]+[[d,d+3],[r+a,d+3],[r+c,d+3],[r+c,c+3]]+[[j,c+3] for j in range(r) if j!=c]+[[j,b] for j in range(2*r)]+[[2*r+1,b],[2*r+1,e]]
 states=[S]
 for i,x in ops:t=list(states[-1]);t[i]^=1<<x;states.append(tuple(t))
 masks=[m for m in range(1<<n) if 3<=full(S,m)<=4]
 for s in states:
  col=columns(s,N);assert feasible(col,F,M) and tau(s)==4
  for m in masks:assert 3<=full(s,m)<=4
 if triple is not None:
  L=4*r+6;assert len(ops)==L+2 and all(all(columns(s,N)) for s in states[:L]);assert columns(states[L],N)[b]==0 and columns(states[-1],N)[e]==0 and columns(states[-1],N)[b]==1<<(2*r+1)
  assert tuple(a.bit_count() for a in states[-1])==F
  assert all(covered(columns(s,N),(u,v,e,z),n) for s in states[:L+2]);assert all(covered(columns(s,N),(u,v,b,z),n) for s in states[L+1:])
  failed=[H for H in Hs if not covered(columns(states[-1],N),H,n)];assert failed==Hs
 else:failed=[]
 return {'r':r,'triple':triple,'source':S,'floors':F,'maxima':M,'source_covers':Hs,'anchored_failures':anchored,'capacity_vectors':len(cap),'capacity_hash':digest(sorted(cap)),'minimum_active':minimum,'ops':ops,'states':states,'failed_source_covers':failed,'protected_masks':masks,'hidden_checks':len(set(states))*len(masks)}

def build(fixture=False):
 cases=[case(g,C,mode) for g,C in sources(fixture) for mode in ('saturated','slack')]
 families=[family(3,(0,1,2))] if fixture else [family(2,None)]+[family(r,t) for r in (3,4) for t in it.permutations(range(r),3)]
 counts={'sources':len(sources(fixture)),'cases':len(cases),'families':len(families),'vertices':sum(c['vertices'] for c in cases),'edges':sum(c['edges'] for c in cases),'cover_jobs':sum(len(c['covers']) for c in cases),'quotient_vertices':sum(q['vertices'] for c in cases for q in c['covers']),'quotient_edges':sum(q['edges'] for c in cases for q in c['covers']),'orbit_edge_lifts':sum(c['orbit_edge_lifts'] for c in cases),'native_slice_occurrences':sum(c['slice_occurrences'] for c in cases)+sum(len(f['states']) for f in families),'fixed_cover_lift_slices':sum(c['fixed_cover_lift_slices'] for c in cases),'hidden_checks':sum(c['hidden_checks'] for c in cases)+sum(f['hidden_checks'] for f in families)}
 return {'cases':cases,'families':families,'counts':counts}
if __name__=='__main__':
 d=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(d['counts'],sort_keys=True))
