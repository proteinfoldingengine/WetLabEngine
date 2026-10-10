"""Independent set-based reconstruction; no producer imports or case-list trust."""
import itertools,collections,functools,json,hashlib,pathlib,sys
def encode(f):return sum(2**i for i in f)
def decode(m):return frozenset(i for i in range(m.bit_length()) if m&2**i)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def roots(cols,n):return tuple(frozenset(x for x,c in enumerate(cols) if i in c) for i in range(n))
@functools.lru_cache(None)
def hit(R):
 if not R:return 0
 if any(not r for r in R):return 99
 return 1+min(hit(tuple(r for r in R if x not in r)) for x in min(R,key=len))
def hiddentau(R,mask):return min(hit(R),1+hit(tuple(r for i,r in enumerate(R) if i not in mask)))
def partition(V,E):
 parent=list(range(len(V)))
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,b in E:parent[find(b)]=find(a)
 groups=collections.defaultdict(list)
 for x in range(len(V)):groups[find(x)].append(x)
 return sorted(groups.values())
def vectors(N,K):
 out=[]
 for multiset in itertools.combinations_with_replacement(range(K),N):
  c=collections.Counter(multiset);out.append(tuple(c[i] for i in range(K)))
 return sorted(out)
def graph(N,T,F,needcover):
 def permitted(C):return all(len(r)>=f for r,f in zip(roots(C,len(F)),F)) and (not needcover or hit(roots(C,len(F)))<=4)
 V=[v for v in vectors(N,len(T)) if permitted(tuple(t for t,c in zip(T,v) for _ in range(c)))];E=[]
 for a,b in itertools.combinations(range(len(V)),2):
  delta=[(i,y-x) for i,(x,y) in enumerate(zip(V[a],V[b])) if x!=y]
  if len(delta)!=2 or sorted(d for _,d in delta)!=[-1,1]:continue
  i=next(i for i,d in delta if d==-1);j=next(i for i,d in delta if d==1)
  C=[t for h,(t,c) in enumerate(zip(T,V[a])) for _ in range(c-(h==i))]+[T[i]&T[j]]
  if permitted(C):E.append((a,b))
 return V,E,partition(V,E)
def native(C,x,dest,n):
 cur=list(C);ss=[tuple(encode(c) for c in cur)];ops=[]
 for i in sorted(C[x]-dest):cur[x]=cur[x]-{i};ops.append((i,x));ss.append(tuple(encode(c) for c in cur))
 for i in sorted(dest-C[x]):cur[x]=cur[x]|{i};ops.append((i,x));ss.append(tuple(encode(c) for c in cur))
 return ops,ss
def sources(fixture=False):
 if fixture:return [(9,10,4,1,8)]
 out=[]
 for k in (3,4):
  for s in range(1,8):
   shared=decode(s);M=[frozenset({i}|({3} if i in shared else set())) for i in range(3)]
   if k==4:M.append(frozenset({4}))
   subs=set()
   for m in M:
    for size in range(1,len(m)+1):subs.update(frozenset(t) for t in itertools.combinations(sorted(m),size))
   codes=sorted(map(encode,subs));prefix=tuple(map(encode,M))
   for a in codes:
    for b in codes:
     if a<=b:out.append(prefix+(a,b))
 return out
def reconstruct_case(raw,mode):
 C=tuple(map(decode,raw));n=max(set().union(*C))+1;N=len(C);M=tuple(sorted({c for c in C if not any(c<d for d in C)},key=encode));T=(frozenset(),)+M;k=len(M);R=roots(C,n)
 assert all(m-set().union(*(t for t in M if t!=m)) for m in M)
 assert hit(R)==k and k in (3,4)
 F=tuple(max(1,len(r)-(mode=='slack')) for r in R);G=tuple(max(0,F[i]-sum(i in m for m in M)) for i in range(n))
 V,E,P=graph(N,T,F,True);W,D,Q=graph(N-k,T,G,False);shifted=[(v[0],)+tuple(c-1 for c in v[1:]) for v in V]
 assert (shifted,E,P)==(W,D,Q)
 for a,b in E:
  for i in range(1,k+1):
   if V[a][i]!=V[b][i]:assert min(V[a][i],V[b][i])>=1
 masks=[m for m in range(2**n) if 3<=hiddentau(R,decode(m))<=4];allstates={raw};occ=0;jobs=[];reach_values=[]
 choices=[tuple(x for x,c in enumerate(C) if c==m) for m in M]
 for A in itertools.product(*choices):
  U=tuple(x for x in range(N) if x not in A)
  def actual(v):
   cur=list(C)
   for x,j in zip(U,v):cur[x]=T[j]
   return tuple(cur)
  def permitted(cols):return all(len(r)>=f for r,f in zip(roots(cols,n),F)) and hit(roots(cols,n))<=4 and all(any(c<=m for m in M) for c in cols)
  def check(ss):
   for s in ss:
    cols=tuple(map(decode,s));assert permitted(cols) and all(cols[x]==C[x] for x in A)
  L=[v for v in itertools.product(range(k+1),repeat=N-k) if permitted(actual(v))];LE=[];records=[]
  for a,b in itertools.combinations(range(len(L)),2):
   differences=[u for u in range(len(U)) if L[a][u]!=L[b][u]]
   if len(differences)!=1:continue
   u=differences[0];x=U[u];meet=list(actual(L[a]));meet[x]&=T[L[b][u]]
   if not permitted(meet):continue
   LE.append((a,b))
   for start,end in ((a,b),(b,a)):
    op,ss=native(actual(L[start]),x,T[L[end][u]],n);check(ss);records.append((start,end,op,ss));allstates.update(ss);occ+=len(ss)
  records.sort(key=lambda t:t[:2]);LP=partition(L,LE)
  projection=[W.index(tuple(v.count(j) for j in range(k+1))) for v in L]
  assert set(projection)==set(range(len(W))) and sorted({tuple(sorted((projection[a],projection[b]))) for a,b in LE})==D
  orbit=0
  for a in range(len(L)):
   neighbors={projection[y if x==a else x] for x,y in LE if a in (x,y)}
   expected={y if x==projection[a] else x for x,y in D if projection[a] in (x,y)}
   assert neighbors==expected;orbit+=len(expected)
  exp=[];sourceparts=[];vacancies=[];renames=[]
  for v in itertools.product(*(tuple(j for j,t in enumerate(T) if C[x]<=t) for x in U)):
   cur=C;op=[];ss=[raw]
   for x,j in zip(U,v):o,s=native(cur,x,T[j],n);op+=o;ss+=s[1:];cur=tuple(map(decode,s[-1]))
   check(ss);allstates.update(ss);occ+=len(ss);start=L.index(v);lp=next(c for c in LP if start in c);wp=next(c for c in Q if projection[start] in c)
   assert sorted(set(projection[i] for i in lp))==wp;sourceparts.append(wp)
   vac=[i for i in lp if 0 in L[i]];targetvac=[[i for i in lp if L[i][u]==0] for u in range(len(U))];assert all(bool(t)==bool(vac) for t in targetvac)
   reach_values.append(bool(vac));exp.append((v,start,op,ss,lp));vacancies.append((v,vac,targetvac))
   if vac:
    endpoint=actual(L[vac[0]]);free=next(x for x in U if not endpoint[x])
    for target in U:
     if not endpoint[target]:rop=[];rss=[tuple(map(encode,endpoint))]
     else:
      op1,s1=native(endpoint,free,endpoint[target],n);op2,s2=native(tuple(map(decode,s1[-1])),target,frozenset(),n);rop=op1+op2;rss=s1+s2[1:]
     check(rss);assert rss[-1][target]==0;allstates.update(rss);occ+=len(rss);renames.append((v,target,rop,rss))
  assert all(p==sourceparts[0] for p in sourceparts)
  jobs.append({'A':A,'U':U,'vertices':len(L),'edges':len(LE),'vertices_hash':digest(L),'edges_hash':digest(LE),'components_hash':digest(LP),'lifts_hash':digest(records),'expansions':len(exp),'expansions_hash':digest(exp),'source_component_hash':digest(sourceparts[0]),'vacancies_hash':digest(vacancies),'renames_hash':digest(renames),'rename_witnesses':len(renames),'orbit_lifts':orbit})
 assert len(set(reach_values))==1
 for rawstate in sorted(allstates):
  r=roots(tuple(map(decode,rawstate)),n);assert all(len(a)>=f for a,f in zip(r,F)) and hit(r)==k
  for m in masks:assert 3<=hiddentau(r,decode(m))<=4
 assignment=[next(j for j,t in enumerate(T) if c<=t) for c in C];startcount=tuple(assignment.count(i) for i in range(k+1));start=V.index(startcount);sourcepart=next(p for p in P if start in p)
 assert any(V[i][0]>0 for i in sourcepart)==reach_values[0]
 return {'source':raw,'mode':mode,'floors':F,'maxima':tuple(map(encode,M)),'tau':k,'residual_floors':G,'vertices':len(V),'edges':len(E),'vertices_hash':digest(V),'edges_hash':digest(E),'components_hash':digest(P),'graph_hash':digest([W,D,Q]),'shifted_graph_hash':digest([shifted,E,P]),'source_component_hash':digest(sourcepart),'static_minimum':min(N-v[0] for v in V),'accessible_minimum':min(N-V[i][0] for i in sourcepart),'reachable':reach_values[0],'anchors':jobs,'hidden_states':len(allstates),'protected_masks':masks,'hidden_checks':len(allstates)*len(masks),'slice_occurrences':occ}
def controls(fixture=False):
 out=[]
 for k in ((3,) if fixture else (3,4)):
  for s in ((3,) if fixture else range(1,8)):
   M=tuple(frozenset({i}|({3} if i in decode(s) else set())) for i in range(3))+((frozenset({4}),) if k==4 else ())
   n=max(set().union(*M))+1;F=tuple(len(r) for r in roots(M,n));V,E,P=graph(k,(frozenset(),)+tuple(sorted(M,key=encode)),F,True)
   assert len(V)==1 and not E and V[0][0]==0
   out.append({'maxima':tuple(map(encode,M)),'vertices':V,'edges':E,'reachable':False})
 triangle=tuple(map(decode,(3,5,6)));assert hit(roots(triangle,3))<len(triangle)
 return out
def boundary():
 positives=[];rejections=[]
 for k in (3,4):
  source=[frozenset({0,3}),frozenset({1,3}),frozenset({2})]
  if k==4:source.append(frozenset({4}))
  C=tuple(source+[frozenset({0}),frozenset({3})]);n=k+1;F=tuple(map(len,roots(C,n)));A=tuple(range(k))
  middle=list(C);middle[k]=middle[k]|{3};end=list(middle);end[k+1]=frozenset();S=[C,tuple(middle),tuple(end)];masks=[m for m in range(2**n) if 3<=hiddentau(roots(C,n),decode(m))<=4]
  for c in S:
   assert all(len(r)>=f for r,f in zip(roots(c,n),F)) and hit(roots(c,n))==k
   assert all(c[x]==C[x] for x in A) and all(any(z<=m for m in source) for z in c)
   for m in masks:assert 3<=hiddentau(roots(c,n),decode(m))<=4
  assert all(S[0]) and all(S[1]) and not S[2][k+1]
  positives.append({'k':k,'source':tuple(map(encode,C)),'floors':F,'anchors':A,'ops':[(3,k),(3,k+1)],'states':[tuple(map(encode,c)) for c in S],'protected_masks':masks,'hidden_checks':len(S)*len(masks)})
  F0=tuple(map(len,roots(source,n)));meet=list(source);meet[0]=source[0]&source[1];assert len(roots(meet,n)[0])<F0[0]
  rejections.append({'k':k,'source':tuple(map(encode,source)),'floors':F0,'donor':0,'destination':encode(source[1]),'meet':list(map(encode,meet)),'private_root':0,'rejected':True})
 return {'positives':positives,'private_loss':rejections}
def build(fixture=False):
 cases=[reconstruct_case(c,m) for c in sources(fixture) for m in ('saturated','slack')]
 counts={'sources':len(sources(fixture)),'cases':len(cases),'anchor_jobs':sum(len(c['anchors']) for c in cases),'expansions':sum(j['expansions'] for c in cases for j in c['anchors']),'vertices':sum(c['vertices'] for c in cases),'edges':sum(c['edges'] for c in cases),'labelled_vertices':sum(j['vertices'] for c in cases for j in c['anchors']),'labelled_edges':sum(j['edges'] for c in cases for j in c['anchors']),'orbit_lifts':sum(j['orbit_lifts'] for c in cases for j in c['anchors']),'rename_witnesses':sum(j['rename_witnesses'] for c in cases for j in c['anchors']),'hidden_checks':sum(c['hidden_checks'] for c in cases),'slice_occurrences':sum(c['slice_occurrences'] for c in cases),'reachable_cases':sum(c['reachable'] for c in cases)}
 b=boundary();counts['hidden_checks']+=sum(x['hidden_checks'] for x in b['positives']);counts['slice_occurrences']+=sum(len(x['states']) for x in b['positives'])
 return {'cases':cases,'controls':controls(fixture),'boundary':b,'counts':counts}
def verify(data,fixture=False):
 expected=build(fixture)
 assert json.loads(json.dumps(data))==json.loads(json.dumps(expected)),'complete independent reconstruction mismatch'
 return True
if __name__=='__main__':
 data=json.loads(pathlib.Path(sys.argv[1]).read_text());verify(data);result={'status':'ACCEPTED','complete_independent_reconstruction':True,'counts':data['counts'],'certificate_sha256':hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()};pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
