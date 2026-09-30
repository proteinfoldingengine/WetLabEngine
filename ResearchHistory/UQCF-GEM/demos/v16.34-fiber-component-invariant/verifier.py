from itertools import combinations
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def mc(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return [()]
 t=tau(p,ys,v);return [S for S in combinations(range(len(ys)),t) if K<=set().union(*(set(ys[i]) for i in S))]
def verify_state(c):
 p=tuple(c['parents']);ys=tuple(map(tuple,c['views']));M=[mc(p,ys,v) for v in range(len(p))];need(c['minimum_covers']==[[list(x) for x in z] for z in M],'minimum covers')
 ess=[];part=[]
 for v,m in enumerate(M):
  e=set.intersection(*(set(x) for x in m)) if m else set();ess.append(sorted([list((i,ch)) for i in e for ch in ys[i] if ch and p[ch]==v]));part.append([sum(i in S for S in m) for i in range(len(ys))])
 need(c['essential']==ess and c['participation']==part,'derived signature');return True
def legal(p):
 return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def adj(p,a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1 and q(p,a)==q(p,b)
def comps(p,mem):
 unseen=set(mem);out=[]
 while unseen:
  s=unseen.pop();C={s};st=[s]
  while st:
   a=st.pop()
   for b in list(unseen):
    if adj(p,a,b):unseen.remove(b);C.add(b);st.append(b)
  out.append(C)
 return out
def shapes(bound):
 from itertools import product
 d={}
 def code(p):
  ch={v:[] for v in range(len(p))}
  for w in range(1,len(p)):ch[p[w]].append(w)
  def r(v):return '('+''.join(sorted(r(w) for w in ch[v]))+')'
  return r(0)
 for n in range(1,bound+1):
  for z in product(*(range(i) for i in range(1,n))):
   p=(-1,)+z;d.setdefault(code(p),p)
 return d.values()
def reconstruct(bound,maxviews):
 from itertools import product
 cc=disc=0
 for p in shapes(bound):
  L=legal(p)
  for k in range(1,maxviews+1):
   G={}
   for y in product(L,repeat=k):
    if set().union(*map(set,y))==set(range(len(p))):G.setdefault(q(p,y),[]).append(y)
   for mem in G.values():
    C=comps(p,mem);cc+=len(C);disc+=len(C)>1
 return cc,disc
def verify_document(d):
 need(d['version']=='16.34','version');cc,disc=reconstruct(d['bound'],d['maxviews']);need((d['component_count'],d['disconnected_fibers'])==(cc,disc),'counts');return {'execution_status':'COMPLETED','component_count':cc,'disconnected_fibers':disc}
