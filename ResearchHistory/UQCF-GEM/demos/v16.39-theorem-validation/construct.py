"""Search-free implementation of the reviewed support-normalization proof."""
from itertools import combinations

def supports(p,k,state):return [sum(1<<j for j in range(k) if state[j]>>v&1) for v in range(len(p))]
def views(p,k,support):return [sum(1<<v for v in range(len(p)) if support[v]>>j&1) for j in range(k)]
def ancestors(p,v):
 out=[]
 while v>=0:out.append(v);v=p[v]
 return out
def classify(p,k,q,a,b):
 active={v for v,x in enumerate(q) if x>=2};sat={v for v in active if q[v]==k}
 H={0}|{u for v in active for u in ancestors(p,v)};ma=supports(p,k,a);mb=supports(p,k,b);full=(1<<k)-1
 edges=[]
 for w in sorted(H-{0}):
  u=p[w]
  if u in active:
   saturated=sorted(v for v in sat if w in ancestors(p,v))
   edges.append({'parent':u,'child':w,'saturated':saturated,'restricted':[ma[w]!=full,mb[w]!=full]})
 return {'sc':all(e['saturated'] for e in edges),'endpoint_full':all(not any(e['restricted']) for e in edges),'edges':edges}

def local_path(initial,target,k,r):
 if not initial:return [tuple(initial)]
 def shrink(sets):
  sets=list(sets);path=[tuple(sets)]
  cover=next(sum(1<<x for x in c) for c in combinations(range(k),r) if all(any(s>>x&1 for x in c) for s in sets))
  for i,s in enumerate(sets):
   keep=(s&cover)&-(s&cover)
   for j in range(k):
    bit=1<<j
    if sets[i]&bit and bit!=keep:sets[i]^=bit;path.append(tuple(sets))
  return sets,path
 current,path=shrink(initial);goal,tail=shrink(target)
 def recolor(i,new):
  old=current[i]
  if old!=new:
   current[i]|=new;path.append(tuple(current));current[i]=new;path.append(tuple(current))
 for old,new in zip(sorted(set(current)-set(goal)),sorted(set(goal)-set(current))):
  for i in range(len(current)):
   if current[i]==old:recolor(i,new)
 while current!=goal:
  used=set(current)
  if len(used)==r:i=next(i for i in range(len(current)) if current[i]!=goal[i])
  else:
   missing=set(goal)-used
   if len(used)!=r-1 or len(missing)!=1:raise ValueError('singleton repair invariant')
   i=next(i for i,x in enumerate(goal) if x in missing)
  recolor(i,goal[i])
 path.extend(reversed(tail[:-1]));return path

def build(p,k,q,a,b):
 c=classify(p,k,q,a,b)
 if not(c['sc'] or c['endpoint_full']):raise ValueError('outside sufficient condition')
 active={v for v,x in enumerate(q) if x>=2};H={0}|{u for v in active for u in ancestors(p,v)};full=(1<<k)-1
 sub={w:[v for v in range(len(p)) if w in ancestors(p,v)] for w in range(len(p))}
 roots=[w for w in range(1,len(p)) if w not in H and p[w] in H]
 def normalize(state):
  M=supports(p,k,state);path=[list(M)]
  def add(v,bit):M[v]|=bit;path.append(list(M))
  for w in sorted(H-{0}):
   if q[p[w]]>=2:
    if M[w]!=full:raise ValueError('restricted active skeleton edge')
   else:
    for j in range(k):
     if not M[w]>>j&1:add(w,1<<j)
  for w in roots:
   for v in sub[w][1:]:
    for j in range(k):
     if M[w]>>j&1 and not M[v]>>j&1:add(v,1<<j)
  return M,path
 M,path=normalize(a);target,tail=normalize(b);prefix=len(path)-1
 for u in sorted(H):
  children=[w for w in roots if p[w]==u]
  if not children:continue
  route=local_path([M[w] for w in children],[target[w] for w in children],k,q[u])
  for before,after in zip(route,route[1:]):
   changed=[i for i in range(len(children)) if before[i]!=after[i]]
   if len(changed)!=1:raise ValueError('local move count')
   i=changed[0];w=children[i];bit=before[i]^after[i]
   if bit.bit_count()!=1:raise ValueError('local incidence count')
   adding=bool(after[i]&bit)
   for v in (sub[w] if adding else list(reversed(sub[w]))):
    M[v]^=bit;path.append(list(M))
 if M!=target:raise ValueError('normalized endpoint mismatch')
 path.extend(reversed(tail[:-1]))
 return {'states':[views(p,k,x) for x in path],'zero_prefix':prefix,'zero_suffix':len(tail)-1}
