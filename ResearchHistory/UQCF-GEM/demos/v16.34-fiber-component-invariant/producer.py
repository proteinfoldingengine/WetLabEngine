from itertools import combinations,product
import json
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def mcovers(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return [()]
 t=tau(p,ys,v);return [S for S in combinations(range(len(ys)),t) if K<=set().union(*(set(ys[i]) for i in S))]
def signatures(p,ys):
 M=[];E=[];P=[]
 for v in range(len(p)):
  m=mcovers(p,ys,v);M.append([list(x) for x in m]);ess=set.intersection(*(set(x) for x in m)) if m else set()
  E.append(sorted((i,c) for i in ess for c in ys[i] if c and p[c]==v))
  P.append([sum(i in S for S in m) for i in range(len(ys))])
 return M,E,P
def control():
 p=(-1,0,0);ys=((0,1),(0,1,2));M,E,P=signatures(p,ys);return {'parents':list(p),'views':[list(x) for x in ys],'minimum_covers':M,'essential':[[list(x) for x in z] for z in E],'participation':P}
def legal(p):
 return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def covers(p,k):
 for y in product(legal(p),repeat=k):
  if set().union(*map(set,y))==set(range(len(p))):yield y
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def adj(p,a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1 and q(p,a)==q(p,b)
def components(p,mem):
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
def produce(bound=4,maxviews=3):
 comps=disc=0;stats={x:{'vary':0,'collide':0} for x in ('M','E','P')};witness={}
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   G={}
   for y in covers(p,k):G.setdefault(q(p,y),[]).append(y)
   for qq,mem in G.items():
    Cs=components(p,mem);comps+=len(Cs);disc+=len(Cs)>1
    vals=[]
    for C in Cs:
     rows=[]
     for y in C:
      M,E,P=signatures(p,y);rows.append((repr(M),repr(E),repr(P)))
     for j,n in enumerate(('M','E','P')):
      if len({r[j] for r in rows})>1:stats[n]['vary']+=1;witness.setdefault(n+'_vary',(p,next(iter(C))))
     vals.append(tuple({r[j] for r in rows} for j in range(3)))
    for j,n in enumerate(('M','E','P')):
     for a,b in combinations(range(len(Cs)),2):
      if vals[a][j]&vals[b][j]:stats[n]['collide']+=1;witness.setdefault(n+'_collide',(p,next(iter(Cs[a])),next(iter(Cs[b]))))
 verdict={n:('COMPLETE_INVARIANT' if s['vary']==0 and s['collide']==0 else 'PARTIAL_INVARIANT') for n,s in stats.items()}
 return {'version':'16.34','bound':bound,'maxviews':maxviews,'component_count':comps,'disconnected_fibers':disc,'stats':stats,'verdict':verdict,'witness_keys':sorted(witness)}
if __name__=='__main__':
 d=produce();open('PRODUCTION.json','w').write(json.dumps(d,indent=2,sort_keys=True));print(json.dumps(d))
