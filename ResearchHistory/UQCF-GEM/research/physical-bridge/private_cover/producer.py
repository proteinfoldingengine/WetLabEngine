"""Complete bitmask construction for private maximal footprints."""
import itertools as it,functools,hashlib,json,pathlib,sys
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def union(xs):return functools.reduce(int.__or__,xs,0)
def rows(C,n):return tuple(sum(1<<j for j,c in enumerate(C) if c>>i&1) for i in range(n))
@functools.lru_cache(None)
def tau(R):
 if not R:return 0
 if 0 in R:return 99
 U=union(R)
 for k in range(U.bit_count()+1):
  if any(all(r&union(t) for r in R) for t in it.combinations([1<<i for i in range(U.bit_length()) if U>>i&1],k)):return k
def hidden(R,m):return min(tau(R),1+tau(tuple(r for i,r in enumerate(R) if not m>>i&1)))
def maxima(C):return tuple(sorted(c for c in set(C) if c and not any(c!=d and c&~d==0 for d in C)))
def private(M):return all(m&~union(M[:i]+M[i+1:]) for i,m in enumerate(M))
def weak(n,k):
 if k==1:yield(n,);return
 for j in range(n+1):
  for tail in weak(n-j,k-1):yield(j,)+tail
def parts(V,E):
 adj=[set() for _ in V]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 left=set(range(len(V)));out=[]
 while left:
  todo=[min(left)];left.remove(todo[0])
  for a in todo:
   for b in sorted(adj[a]&left):left.remove(b);todo.append(b)
  out.append(sorted(todo))
 return sorted(out)
def lift(C,x,K,n):
 cur=list(C);S=[tuple(cur)];ops=[];old=cur[x]
 for i in range(n):
  if old>>i&1 and not K>>i&1:cur[x]^=1<<i;ops.append((i,x));S.append(tuple(cur))
 for i in range(n):
  if K>>i&1 and not old>>i&1:cur[x]^=1<<i;ops.append((i,x));S.append(tuple(cur))
 return ops,S
def count_graph(N,T,F,cover=True):
 def ok(C):return all(a.bit_count()>=f for a,f in zip(rows(C,len(F)),F)) and (not cover or tau(rows(C,len(F)))<=4)
 V=[]
 for v in weak(N,len(T)):
  C=tuple(t for t,c in zip(T,v) for _ in range(c))
  if ok(C):V.append(v)
 idx={v:i for i,v in enumerate(V)};E=[]
 for a,v in enumerate(V):
  for i,c in enumerate(v):
   if not c:continue
   for j in range(len(T)):
    if i==j:continue
    w=list(v);w[i]-=1;w[j]+=1;b=idx.get(tuple(w),-1)
    if b<=a:continue
    meet=tuple(t for h,(t,c) in enumerate(zip(T,v)) for _ in range(c-(h==i)))+(T[i]&T[j],)
    if ok(meet):E.append((a,b))
 E.sort();return V,E,parts(V,E)
def source_universe(fixture=False):
 if fixture:return [(9,10,4,1,8)]
 out=[]
 for k in (3,4):
  for S in range(1,8):
   M=tuple((1<<i)|(8 if S>>i&1 else 0) for i in range(3))+((16,) if k==4 else ())
   alphabet=[c for c in range(1,union(M)+1) if any(c&~m==0 for m in M)]
   out.extend(M+extra for extra in it.combinations_with_replacement(alphabet,2))
 return out
def case(C,mode,Foverride=None):
 n=union(C).bit_length();N=len(C);M=maxima(C);T=(0,)+M;k=len(M);R=rows(C,n)
 F=tuple(Foverride) if Foverride is not None else tuple(max(1,a.bit_count()-(mode=='slack')) for a in R)
 if not all(f>0 for f in F) or not private(M):raise ValueError('positive original floors and PRIVATE required')
 assert tau(R)==k and k in (3,4)
 B=tuple(sum(m>>i&1 for m in M) for i in range(n));G=tuple(max(0,f-b) for f,b in zip(F,B))
 V,E,P=count_graph(N,T,F);W,D,Q=count_graph(N-k,T,G,False)
 shifted=[(v[0],)+tuple(c-1 for c in v[1:]) for v in V];assert shifted==W and E==D and P==Q
 assert all(all(c>=1 for c in v[1:]) for v in V)
 for a,b in E:
  for i in range(1,k+1):
   if V[a][i]>V[b][i]:assert V[a][i]>=2
   if V[b][i]>V[a][i]:assert V[b][i]>=2
 masks=[m for m in range(1<<n) if 3<=hidden(R,m)<=4];allstates={C};slice_occ=0;jobs=[];reach_values=[]
 for A in it.product(*(tuple(i for i,c in enumerate(C) if c==m) for m in M)):
  U=tuple(i for i in range(N) if i not in A)
  def actual(v):
   c=list(C)
   for x,j in zip(U,v):c[x]=T[j]
   return tuple(c)
  def safe(c):return all(a.bit_count()>=f for a,f in zip(rows(c,n),F)) and tau(rows(c,n))<=4 and all(any(z&~m==0 for m in M) for z in c)
  L=[v for v in it.product(range(k+1),repeat=N-k) if safe(actual(v))];li={v:i for i,v in enumerate(L)};LE=[];records=[]
  for a,v in enumerate(L):
   for u,x in enumerate(U):
    for j in range(k+1):
     w=v[:u]+(j,)+v[u+1:];b=li.get(w,-1)
     if b<=a:continue
     meet=list(actual(v));meet[x]&=T[j]
     if not safe(tuple(meet)):continue
     LE.append((a,b))
     for start,end in ((a,b),(b,a)):
      ops,ss=lift(actual(L[start]),x,T[L[end][u]],n)
      assert all(safe(s) and all(s[x]==C[x] for x in A) for s in ss)
      records.append((start,end,ops,ss));allstates.update(ss);slice_occ+=len(ss)
  LE.sort();records.sort(key=lambda t:t[:2]);LP=parts(L,LE)
  def count(v):return tuple(v.count(j) for j in range(k+1))
  wi={w:i for i,w in enumerate(W)};projection=[wi[count(v)] for v in L]
  assert sorted(set(projection))==list(range(len(W)))
  projedges=sorted({tuple(sorted((projection[a],projection[b]))) for a,b in LE});assert projedges==D
  adj=[set() for _ in L];wadj=[set() for _ in W]
  for a,b in LE:adj[a].add(b);adj[b].add(a)
  for a,b in D:wadj[a].add(b);wadj[b].add(a)
  orbit=0
  for a in range(len(L)):
   assert {projection[b] for b in adj[a]}==wadj[projection[a]];orbit+=len(wadj[projection[a]])
  exp=[];sourceparts=[];renames=[];vacancies=[]
  for v in it.product(*(tuple(j for j,t in enumerate(T) if t and C[x]&~t==0) for x in U)):
   cur=C;ops=[];ss=[C]
   for x,j in zip(U,v):op,states=lift(cur,x,T[j],n);ops.extend(op);ss.extend(states[1:]);cur=states[-1]
   assert all(safe(s) and all(s[x]==C[x] for x in A) for s in ss)
   allstates.update(ss);slice_occ+=len(ss);start=li[v];lp=next(p for p in LP if start in p);wp=next(p for p in Q if projection[start] in p)
   assert sorted({projection[i] for i in lp})==wp;sourceparts.append(wp)
   vac=[i for i in lp if 0 in L[i]];targetvac=[[i for i in lp if L[i][u]==0] for u in range(len(U))]
   assert all(bool(t)==bool(vac) for t in targetvac);reach_values.append(bool(vac))
   exp.append((v,start,ops,ss,lp));vacancies.append((v,vac,targetvac))
   if vac:
    endpoint=actual(L[vac[0]]);free=next(x for x in U if endpoint[x]==0)
    for target in U:
     if endpoint[target]==0:rop=[];rss=[endpoint]
     else:
      op1,s1=lift(endpoint,free,endpoint[target],n);op2,s2=lift(s1[-1],target,0,n);rop=op1+op2;rss=s1+s2[1:]
     assert rss[-1][target]==0 and all(safe(s) and all(s[x]==C[x] for x in A) for s in rss)
     allstates.update(rss);slice_occ+=len(rss);renames.append((v,target,rop,rss))
  assert all(p==sourceparts[0] for p in sourceparts)
  jobs.append({'A':A,'U':U,'vertices':len(L),'edges':len(LE),'vertices_hash':digest(L),'edges_hash':digest(LE),'components_hash':digest(LP),'lifts_hash':digest(records),'expansions':len(exp),'expansions_hash':digest(exp),'source_component_hash':digest(sourceparts[0]),'vacancies_hash':digest(vacancies),'renames_hash':digest(renames),'rename_witnesses':len(renames),'orbit_lifts':orbit})
 assert len(set(reach_values))==1
 for c in sorted(allstates):
  assert all(a.bit_count()>=f for a,f in zip(rows(c,n),F)) and tau(rows(c,n))==k
  for m in masks:assert 3<=hidden(rows(c,n),m)<=4
 startcount=tuple(sum(1 for c in C if next(j for j,t in enumerate(T) if t and c&~t==0)==i) for i in range(k+1));vi=V.index(startcount);sourcepart=next(p for p in P if vi in p)
 assert bool(any(V[i][0]>0 for i in sourcepart))==reach_values[0]
 return {'source':C,'mode':mode,'floors':F,'maxima':M,'tau':k,'residual_floors':G,'vertices':len(V),'edges':len(E),'vertices_hash':digest(V),'edges_hash':digest(E),'components_hash':digest(P),'graph_hash':digest([W,D,Q]),'shifted_graph_hash':digest([shifted,E,P]),'source_component_hash':digest(sourcepart),'static_minimum':min(N-v[0] for v in V),'accessible_minimum':min(N-V[i][0] for i in sourcepart),'reachable':reach_values[0],'anchors':jobs,'hidden_states':len(allstates),'protected_masks':masks,'hidden_checks':len(allstates)*len(masks),'slice_occurrences':slice_occ}
def controls(fixture=False):
 out=[]
 for k in ((3,) if fixture else (3,4)):
  for s in ((3,) if fixture else range(1,8)):
   M=tuple((1<<i)|(8 if s>>i&1 else 0) for i in range(3))+((16,) if k==4 else ())
   n=union(M).bit_length();F=tuple(a.bit_count() for a in rows(M,n));V,E,P=count_graph(k,(0,)+tuple(sorted(M)),F)
   assert len(V)==1 and not E and V[0][0]==0
   out.append({'maxima':M,'vertices':V,'edges':E,'reachable':False})
 assert not private((3,5,6))
 return out
def boundary():
 positives=[];rejections=[]
 for k in (3,4):
  C=(9,10,4)+((16,) if k==4 else ())+(1,8);n=k+1;F=tuple(r.bit_count() for r in rows(C,n));A=tuple(range(k))
  c=list(C);S=[C];ops=[(3,k),(3,k+1)]
  for i,x in ops:c[x]^=1<<i;S.append(tuple(c))
  masks=[m for m in range(1<<n) if 3<=hidden(rows(C,n),m)<=4]
  for c in S:
   assert all(r.bit_count()>=f for r,f in zip(rows(c,n),F)) and tau(rows(c,n))==k
   assert all(c[x]==C[x] for x in A) and all(any(z&~m==0 for m in maxima(C)) for z in c)
   for m in masks:assert 3<=hidden(rows(c,n),m)<=4
  assert all(S[0]) and all(S[1]) and S[2][k+1]==0
  positives.append({'k':k,'source':C,'floors':F,'anchors':A,'ops':ops,'states':S,'protected_masks':masks,'hidden_checks':len(S)*len(masks)})
  source=C[:k];floors=tuple(r.bit_count() for r in rows(source,n));meet=list(source);meet[0]&=source[1]
  assert rows(tuple(meet),n)[0].bit_count()<floors[0]
  rejections.append({'k':k,'source':source,'floors':floors,'donor':0,'destination':source[1],'meet':meet,'private_root':0,'rejected':True})
 return {'positives':positives,'private_loss':rejections}
def build(fixture=False):
 cases=[case(c,mode) for c in source_universe(fixture) for mode in ('saturated','slack')]
 counts={'sources':len(source_universe(fixture)),'cases':len(cases),'anchor_jobs':sum(len(c['anchors']) for c in cases),'expansions':sum(j['expansions'] for c in cases for j in c['anchors']),'vertices':sum(c['vertices'] for c in cases),'edges':sum(c['edges'] for c in cases),'labelled_vertices':sum(j['vertices'] for c in cases for j in c['anchors']),'labelled_edges':sum(j['edges'] for c in cases for j in c['anchors']),'orbit_lifts':sum(j['orbit_lifts'] for c in cases for j in c['anchors']),'rename_witnesses':sum(j['rename_witnesses'] for c in cases for j in c['anchors']),'hidden_checks':sum(c['hidden_checks'] for c in cases),'slice_occurrences':sum(c['slice_occurrences'] for c in cases),'reachable_cases':sum(c['reachable'] for c in cases)}
 b=boundary();counts['hidden_checks']+=sum(x['hidden_checks'] for x in b['positives']);counts['slice_occurrences']+=sum(len(x['states']) for x in b['positives'])
 return {'cases':cases,'controls':controls(fixture),'boundary':b,'counts':counts}
if __name__=='__main__':
 d=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(d['counts'],sort_keys=True))
