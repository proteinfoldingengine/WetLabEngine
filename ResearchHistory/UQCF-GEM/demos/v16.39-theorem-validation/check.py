"""Independent support semantics, descendant classifier and union-find oracle."""
from itertools import combinations

def need(x,msg):
 if not x:raise ValueError(msg)
def profile(p,k,state):
 need(isinstance(state,list) and len(state)==k,'state shape')
 n=len(p);full=(1<<n)-1
 need(all(type(s) is int and 0<s<=full and s&1 for s in state),'view type/root')
 need(all(not(s>>v&1) or s>>p[v]&1 for s in state for v in range(1,n)),'prefix closure')
 need(all(any(s>>v&1 for s in state) for v in range(n)),'cover')
 out=[]
 for v in range(n):
  ch=[w for w in range(1,n) if p[w]==v]
  if not ch:out.append(0);continue
  out.append(next(r for r in range(1,k+1) if any(all(any(state[j]>>w&1 for j in C) for w in ch) for C in combinations(range(k),r))))
 return out
def classify(p,k,q,a,b):
 children=[[w for w in range(1,len(p)) if p[w]==v] for v in range(len(p))]
 def descendants(v):return {v}.union(*(descendants(w) for w in children[v]))
 edges=[]
 for u in range(len(p)):
  if q[u]<2:continue
  for w in children[u]:
   desc=descendants(w)
   if not any(q[v]>=2 for v in desc):continue
   sat=sorted(v for v in desc if q[v]==k and q[v]>=2)
   restricted=[not all(s>>w&1 for s in state) for state in (a,b)]
   edges.append({'parent':u,'child':w,'saturated':sat,'restricted':restricted})
 edges.sort(key=lambda e:e['child'])
 return {'sc':not any(not e['saturated'] for e in edges),'endpoint_full':not any(any(e['restricted']) for e in edges),'edges':edges}
def path_states(p,k,q,a,b,proof):
 need(isinstance(proof,dict) and set(proof)=={'states','zero_prefix','zero_suffix'},'path schema')
 states=proof['states'];need(isinstance(states,list) and states and states[0]==a and states[-1]==b,'path endpoints')
 pre=proof['zero_prefix'];suf=proof['zero_suffix']
 need(type(pre) is int and type(suf) is int and min(pre,suf)>=0 and pre+suf<len(states),'normalization lengths')
 for i,s in enumerate(states):
  row=profile(p,k,s);delta=[abs(x-y) for x,y in zip(row,q)]
  need(sum(delta)<=1,'nonunit construction width')
  if i<=pre or i>=len(states)-1-suf:need(row==q,'nonzero normalization')
  if i:need(sum((x^y).bit_count() for x,y in zip(states[i-1],s))==1,'illegal incidence move')
def reachable_union(edges,allowed,start):
 parent={x:x for x in allowed}
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,b in edges:
  if a in parent and b in parent:
   ra,rb=root(a),root(b)
   if ra!=rb:parent[rb]=ra
 if start not in parent:return []
 r=root(start);return sorted(x for x in allowed if root(x)==r)
