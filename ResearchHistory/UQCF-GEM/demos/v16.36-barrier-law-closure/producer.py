from itertools import combinations,product
from collections import deque
import json
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
def loc(p,A,a,b,lim):
 q0=q(p,a)
 def dev(s):
  d=tuple(abs(u-v) for u,v in zip(q(p,s),q0));return (sum(d),max(d,default=0),sum(x>0 for x in d))
 allowed={s for s in A if all(x<=y for x,y in zip(dev(s),lim))}
 def reach(forbid):
  todo=deque([a]);seen={a}
  while todo:
   x=todo.popleft()
   if x==b:return True
   for y in A[x]:
    if y not in allowed:continue
    ch={i for i,(u,v) in enumerate(zip(q(p,y),q0)) if u!=v}
    if forbid in ch:continue
    if y not in seen:seen.add(y);todo.append(y)
  return False
 return [v for v in range(len(p)) if not reach(v)],allowed
def shapes(nmax):
 d={}
 def code(p):
  ch={v:[] for v in range(len(p))}
  for w in range(1,len(p)):ch[p[w]].append(w)
  def r(v):return '('+''.join(sorted(r(w) for w in ch[v]))+')'
  return r(0)
 for n in range(1,nmax+1):
  for z in product(*(range(i) for i in range(1,n))):
   p=(-1,)+z;d.setdefault(code(p),p)
 return sorted(d.values(),key=lambda x:(len(x),x))
def analyze(p,k,cap=None):
 S=covers(p,k)
 if cap is not None and len(S)>cap:return None,{'excluded':True,'states':len(S)}
 A=graph(S);G={}
 for s in S:G.setdefault(q(p,s),[]).append(s)
 pairs=[];ultra=0
 for q0,mem in G.items():
  un=set(mem);Cs=[]
  while un:
   s=un.pop();C={s};todo=deque([s])
   while todo:
    x=todo.popleft()
    for y in A[x]:
     if y in un and q(p,y)==q0:un.remove(y);C.add(y);todo.append(y)
   Cs.append(C)
  if len(Cs)<2:continue
  cache={a:exact(p,A,a) for a in mem};dist={}
  for i,j in combinations(range(len(Cs)),2):
   vals=[]
   for a in Cs[i]:
    for b in Cs[j]:
     z=cache[a][b];vals.append(z)
     L,allowed=loc(p,A,a,b,z);ranges=[sorted({q(p,s)[v] for s in allowed}) for v in L]
     pairs.append({'parents':list(p),'view_count':k,'q':list(q0),'components':[i,j],'a':[list(x) for x in a],'b':[list(x) for x in b],'B1':z[0],'Binf':z[1],'Bs':z[2],'candidate_signature':{'q':list(q0),'compulsory':L,'attainable':[ [v,r] for v,r in zip(L,ranges)]}})
   dist[i,j]=min(x[0] for x in vals)
  for i,j,l in combinations(range(len(Cs)),3):
   a=dist[min(i,j),max(i,j)];b=dist[min(j,l),max(j,l)];c=dist[min(i,l),max(i,l)]
   ultra += c>max(a,b) or a>max(b,c) or b>max(a,c)
 return pairs,{'excluded':False,'states':len(S),'ultra':ultra}
def produce(bound=4):
 pairs=[];excluded=[];uv=0
 for p in shapes(bound):
  for k in range(1,4):
   x,m=analyze(p,k);pairs+=x;uv+=m['ultra']
 groups={}
 for r in pairs:
  s=json.dumps(r['candidate_signature'],sort_keys=True);groups.setdefault(s,set()).add((r['B1'],r['Binf'],r['Bs']))
 collisions=[{'signature':json.loads(s),'barriers':[list(x) for x in sorted(v)]} for s,v in groups.items() if len(v)>1]
 # Gate E extension through five vertices, explicit resource exclusions
 ext_ultra=0;tested=0
 for p in shapes(5):
  if len(p)<5:continue
  for k in range(1,4):
   x,m=analyze(p,k,5000)
   if m['excluded']:excluded.append({'parents':list(p),'view_count':k,'states':m['states'],'reason':'EXCLUDED_RESOURCE'})
   else:tested+=1;ext_ultra+=m['ultra']
 outcome='FIBER_CONTEXT' if collisions else 'UNRESOLVED'
 return {'version':'16.36','gate_a':'RECONSTRUCTED','gate_b':'REPRODUCED','gate_c':{'collisions':collisions,'groups':len(groups)},'gate_d':outcome,'gate_e':{'tested_cases':tested,'excluded':excluded,'ultrametric_violations':ext_ultra,'scope':'BOUNDED'},'pairs':pairs}
if __name__=='__main__':
 d=produce();open('PRODUCTION.json','w').write(json.dumps(d,indent=2,sort_keys=True));print(json.dumps({k:d[k] for k in ('gate_d','gate_e')}))
