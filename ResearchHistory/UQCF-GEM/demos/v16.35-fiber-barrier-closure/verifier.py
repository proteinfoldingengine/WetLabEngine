from itertools import combinations,product
from collections import deque
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,y,v):
 U=set().union(*map(set,y));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(y)+1) if any(K<=set().union(*(set(y[i]) for i in S)) for S in combinations(range(len(y)),r)))
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def legal(p):
 return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def edge(a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1
def exact(p,k,a,b):
 states=[y for y in product(legal(p),repeat=k) if set().union(*map(set,y))==set(range(len(p)))];q0=q(p,a);best={a:(0,0,0)};todo=[a]
 while todo:
  x=todo.pop(0)
  for y in states:
   if not edge(x,y):continue
   d=tuple(abs(u-v) for u,v in zip(q(p,y),q0));z=(max(best[x][0],sum(d)),max(best[x][1],max(d,default=0)),max(best[x][2],sum(t>0 for t in d)))
   if y not in best or z<best[y]:best[y]=z;todo.append(y)
 return best[b]
def verify_document(d):
 need(d['version']=='16.35','version')
 for c in d['barriers']:
  p=tuple(c['parents']);a=tuple(map(tuple,c['a']));b=tuple(map(tuple,c['b']));need(q(p,a)==q(p,b)==tuple(c['q']),'q endpoints');z=exact(p,c['view_count'],a,b);need(z==(c['B1'],c['Binf'],c['Bs']),'false barrier');need(z[0]>0,'not positive')
 return {'execution_status':'COMPLETED','verified_records':len(d['barriers'])}
