"""Complete star graphs with constructive exact-fiber normal forms."""
from itertools import combinations
import graph_producer as graph
DOMAIN=tuple((m,k) for m in range(2,5) for k in range(2,5))+((5,2),(5,3))
def normalize(state,m,k,q):
 s=list(state);path=[list(s)]
 def change(j,v,add):
  if add:s[j]|=1<<v
  else:s[j]&=~(1<<v)
  path.append(list(s))
 def support(v):return [j for j in range(k) if s[j]>>v&1]
 H=next(h for h in combinations(range(k),q) if all(any(s[j]>>v&1 for j in h) for v in range(1,m+1)))
 for v in range(1,m+1):
  keep=next(j for j in H if s[j]>>v&1)
  for j in support(v):
   if j!=keep:change(j,v,False)
 for a,b in zip(sorted(set(H)-set(range(q))),sorted(set(range(q))-set(H))):
  leaves=[v for v in range(1,m+1) if s[a]>>v&1]
  for v in leaves:change(b,v,True)
  for v in leaves:change(a,v,False)
 def colors():return [support(v)[0] for v in range(1,m+1)]
 def recolor(i,b):
  a=support(i+1)[0]
  if a!=b:change(b,i+1,True);change(a,i+1,False)
 if m>q:
  for i in range(q):
   c=colors();a=c[i]
   if a==i:continue
   if c.count(a)==1:
    t=next(t for t in range(i+1,m) if c.count(c[t])>1);recolor(t,a)
   recolor(i,i)
  for i in range(q,m):recolor(i,0)
 elif k>q:
  for i in range(q):
   c=colors();a=c[i]
   if a==i:continue
   j=c.index(i);recolor(i,q);recolor(j,a);recolor(i,i)
 else:
  target=[1|(1<<(j+1)) for j in range(k)]
  path+=graph.proof_path([-1]+[0]*m,s,target)[1:]
 return path
