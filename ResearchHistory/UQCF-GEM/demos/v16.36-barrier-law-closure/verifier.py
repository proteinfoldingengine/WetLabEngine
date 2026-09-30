from itertools import combinations,product
from collections import deque
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,y,v):
 U=set().union(*map(set,y));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(y)+1) if any(K<=set().union(*(set(y[i]) for i in S)) for S in combinations(range(len(y)),r)))
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def legal(p):return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def covers(p,k):return [y for y in product(legal(p),repeat=k) if set().union(*map(set,y))==set(range(len(p)))]
def edge(a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1
def graph(S):
 A={x:[] for x in S}
 for i,x in enumerate(S):
  for y in S[i+1:]:
   if edge(x,y):A[x].append(y);A[y].append(x)
 return A
def exact(p,A,a):
 q0=q(p,a);best={a:(0,0,0)};todo=deque([a])
 while todo:
  x=todo.popleft()
  for y in A[x]:
   d=tuple(abs(u-v) for u,v in zip(q(p,y),q0));z=(max(best[x][0],sum(d)),max(best[x][1],max(d,default=0)),max(best[x][2],sum(t>0 for t in d)))
   if y not in best or z<best[y]:best[y]=z;todo.append(y)
 return best
def signature(p,A,a,b,z):
 q0=q(p,a)
 def dev(s):
  d=tuple(abs(u-v) for u,v in zip(q(p,s),q0));return (sum(d),max(d,default=0),sum(x>0 for x in d))
 allowed={s for s in A if all(x<=y for x,y in zip(dev(s),z))}
 def avoid(v):
  todo=deque([a]);seen={a}
  while todo:
   x=todo.popleft()
   if x==b:return True
   for y in A[x]:
    if y not in allowed:continue
    if q(p,y)[v]!=q0[v]:continue
    if y not in seen:seen.add(y);todo.append(y)
  return False
 L=[v for v in range(len(p)) if not avoid(v)]
 att=[[v,sorted({q(p,s)[v] for s in allowed})] for v in L]
 return {'q':list(q0),'compulsory':L,'attainable':att}
def verify_document(d):
 need(all(k in d for k in ('gate_a','gate_b','gate_c','gate_d','gate_e')),'missing gate')
 for r in d['pairs']:
  p=tuple(r['parents']);S=covers(p,r['view_count']);A=graph(S);a=tuple(map(tuple,r['a']));b=tuple(map(tuple,r['b']));best=exact(p,A,a);z=best[b]
  need(z==(r['B1'],r['Binf'],r['Bs']),'barrier');need(signature(p,A,a,b,z)==r['candidate_signature'],'signature')
 groups={}
 for r in d['pairs']:
  import json
  groups.setdefault(json.dumps(r['candidate_signature'],sort_keys=True),set()).add((r['B1'],r['Binf'],r['Bs']))
 cols=[v for v in groups.values() if len(v)>1]
 need(d['gate_c']['groups']==len(groups),'group count');need(d['gate_c']['collisions']==[{'signature':__import__('json').loads(s),'barriers':[list(x) for x in sorted(v)]} for s,v in groups.items() if len(v)>1],'collision set')
 need(d['gate_d']==('FIBER_CONTEXT' if cols else 'UNRESOLVED'),'gate d')
 # Independently reconstruct Gate E five-vertex extension and resource exclusions.
 def shapes5():
  dd={}
  def code(p):
   ch={v:[] for v in range(len(p))}
   for w in range(1,len(p)):ch[p[w]].append(w)
   def rr(v):return '('+''.join(sorted(rr(w) for w in ch[v]))+')'
   return rr(0)
  for z in product(*(range(i) for i in range(1,5))):
   p=(-1,)+z;dd.setdefault(code(p),p)
  return sorted(dd.values())
 tested=0;excluded=[];ultra=0
 for p in shapes5():
  for k in range(1,4):
   S=covers(p,k)
   if len(S)>5000:
    excluded.append({'parents':list(p),'view_count':k,'states':len(S),'reason':'EXCLUDED_RESOURCE'});continue
   tested+=1;A=graph(S);G={}
   for s in S:G.setdefault(q(p,s),[]).append(s)
   for q0,mem in G.items():
    un=set(mem);Cs=[]
    while un:
     s=un.pop();C={s};todo=deque([s])
     while todo:
      x=todo.popleft()
      for y in A[x]:
       if y in un and q(p,y)==q0:un.remove(y);C.add(y);todo.append(y)
     Cs.append(C)
    if len(Cs)<3:continue
    cache={a:exact(p,A,a) for a in mem};dist={}
    for i,j in combinations(range(len(Cs)),2):dist[i,j]=min(cache[a][b][0] for a in Cs[i] for b in Cs[j])
    for i,j,l in combinations(range(len(Cs)),3):
     a=dist[i,j];b=dist[j,l];cc=dist[i,l]
     ultra += cc>max(a,b) or a>max(b,cc) or b>max(a,cc)
 expected={'tested_cases':tested,'excluded':excluded,'ultrametric_violations':ultra,'scope':'BOUNDED'}
 need(d['gate_e']==expected,'gate e extension')
 return {'execution_status':'COMPLETED','verified_pairs':len(d['pairs']),'gate_d':d['gate_d'],'gate_e':expected}
