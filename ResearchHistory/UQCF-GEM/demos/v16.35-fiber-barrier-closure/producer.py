from itertools import combinations,product
from collections import deque
import json
def tau(p,y,v):
 U=set().union(*map(set,y));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(y)+1) if any(K<=set().union(*(set(y[i]) for i in S)) for S in combinations(range(len(y)),r)))
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def legal(p):
 return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def covers(p,k):
 for y in product(legal(p),repeat=k):
  if set().union(*map(set,y))==set(range(len(p))):yield y
def edge(a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1
def barrier(p,states,a,b):
 q0=q(p,a);best={a:(0,0,0)};dq=deque([a])
 while dq:
  x=dq.popleft();bx=best[x]
  for y in states:
   if not edge(x,y):continue
   dy=tuple(abs(u-v) for u,v in zip(q(p,y),q0));cost=(max(bx[0],sum(dy)),max(bx[1],max(dy,default=0)),max(bx[2],sum(z>0 for z in dy)))
   if y not in best or cost<best[y]:best[y]=cost;dq.append(y)
 return best.get(b)
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
 bars=[];positive=0;pairs=0
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   states=list(covers(p,k));G={}
   for y in states:G.setdefault(q(p,y),[]).append(y)
   for q0,mem in G.items():
    for a,b in combinations(mem,2):
     # only record pairs disconnected at zero barrier
     z=barrier(p,states,a,b)
     if z and z[0]>0:
      positive+=1;pairs+=1
      if len(bars)<50:bars.append({'parents':list(p),'view_count':k,'a':[list(x) for x in a],'b':[list(x) for x in b],'q':list(q0),'B1':z[0],'Binf':z[1],'Bs':z[2]})
 return {'version':'16.35','bound':bound,'maxviews':maxviews,'positive_barriers':positive,'barrier_pairs':pairs,'barriers':bars}
if __name__=='__main__':
 d=produce();open('PRODUCTION.json','w').write(json.dumps(d,indent=2));print(json.dumps({k:d[k] for k in ('positive_barriers','barrier_pairs')}))
