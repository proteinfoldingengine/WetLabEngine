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
def covers(p,k):return [y for y in product(legal(p),repeat=k) if set().union(*map(set,y))==set(range(len(p)))]
def edge(a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1
def graph(states):
 A={x:[] for x in states}
 for i,x in enumerate(states):
  for y in states[i+1:]:
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
 return sorted(d.values(),key=lambda x:(len(x),x))
def canonical_records(bound,maxviews):
 records=[];statesN=edgesN=0;allconn=True
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   states=covers(p,k);A=graph(states);statesN+=len(states);edgesN+=sum(map(len,A.values()))//2
   seen={states[0]};dq=deque([states[0]])
   while dq:
    x=dq.popleft()
    for y in A[x]:
     if y not in seen:seen.add(y);dq.append(y)
   allconn &= len(seen)==len(states)
   G={}
   for s in states:G.setdefault(q(p,s),[]).append(s)
   for q0,mem in G.items():
    un=set(mem);Cs=[]
    while un:
     s=un.pop();C={s};dq=deque([s])
     while dq:
      x=dq.popleft()
      for y in A[x]:
       if y in un and q(p,y)==q0:un.remove(y);C.add(y);dq.append(y)
     Cs.append(C)
    if len(Cs)<2:continue
    cache={a:exact(p,A,a) for a in mem}
    for i,j in combinations(range(len(Cs)),2):
     for a in Cs[i]:
      for b in Cs[j]:
       z=cache[a][b];records.append((p,k,q0,a,b,z))
 return records,statesN,edgesN,allconn
def verify_path(c):
 p=tuple(c['parents']);P=[tuple(map(tuple,s)) for s in c['path']];a=tuple(map(tuple,c['a']));b=tuple(map(tuple,c['b']));need(P and P[0]==a and P[-1]==b,'path endpoints');need(all(edge(x,y) for x,y in zip(P,P[1:])),'illegal path');need(all(set().union(*map(set,s))==set(range(len(p))) for s in P),'changed union');q0=tuple(c['q']);ds=[tuple(abs(u-v) for u,v in zip(q(p,s),q0)) for s in P];z=(max(sum(d) for d in ds),max(max(d,default=0) for d in ds),max(sum(x>0 for x in d) for d in ds));need(z==(c['B1'],c['Binf'],c['Bs']),'path not claimed barrier');need(sorted({v for s in P for v,(u,w) in enumerate(zip(q(p,s),q0)) if u!=w})==c['changed_coordinates'],'localization')
def verify_document(d):
 need(d.get('version')=='16.35','version');need(all(x in d for x in ('gate_a','gate_b','gate_c','gate_d','gate_e')),'missing gate')
 rec,statesN,edgesN,conn=canonical_records(d['bound'],d['maxviews']);need((d['states'],d['edges'])==(statesN,edgesN),'false universe counts');need(d['gate_a']==('CONNECTED' if conn else 'COUNTEREXAMPLE'),'gate a')
 actual={(tuple(p),k,q0,a,b):z for p,k,q0,a,b,z in rec};published={}
 for c in d['barriers']:
  p=tuple(c['parents']);a=tuple(map(tuple,c['a']));b=tuple(map(tuple,c['b']));key=(p,c['view_count'],tuple(c['q']),a,b)
  if key not in actual:key=(p,c['view_count'],tuple(c['q']),b,a)
  need(key in actual,'foreign/omitted endpoint type');need(actual[key]==(c['B1'],c['Binf'],c['Bs']),'nonminimal barrier');verify_path(c);published[key]=actual[key]
 need(set(published)==set(actual),'omitted positive pair');need(d['positive_barriers']==len(actual),'false bulk count');need(d['gate_b']==('POSITIVE' if actual and all(z[0]>0 for z in actual.values()) else 'COUNTEREXAMPLE'),'gate b')
 # independently derive Gates C-E
 ranges=[];tri=ultra=0
 for p in shapes(d['bound']):
  for k in range(1,d['maxviews']+1):
   states=covers(p,k);A=graph(states);G={}
   for s in states:G.setdefault(q(p,s),[]).append(s)
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
     vals=[cache[a][b] for a in Cs[i] for b in Cs[j]]
     ranges.append({'parents':list(p),'view_count':k,'q':list(q0),'components':[i,j],'B1_range':[min(x[0] for x in vals),max(x[0] for x in vals)],'Binf_range':[min(x[1] for x in vals),max(x[1] for x in vals)],'Bs_range':[min(x[2] for x in vals),max(x[2] for x in vals)]});dist[i,j]=min(x[0] for x in vals)
    if len(Cs)>=3:
     for i,j,l in combinations(range(len(Cs)),3):
      dij=dist[min(i,j),max(i,j)];djl=dist[min(j,l),max(j,l)];dil=dist[min(i,l),max(i,l)]
      if dil>dij+djl or dij>dil+djl or djl>dij+dil:tri+=1
      if dil>max(dij,djl) or dij>max(dil,djl) or djl>max(dij,dil):ultra+=1
 gate_c='REPRESENTATIVE_INDEPENDENT' if all(x['B1_range'][0]==x['B1_range'][1] and x['Binf_range'][0]==x['Binf_range'][1] and x['Bs_range'][0]==x['Bs_range'][1] for x in ranges) else 'REPRESENTATIVE_DEPENDENT'
 need(d['component_ranges']==ranges,'false component ranges');need(d['gate_c']==gate_c,'gate c');need(d['gate_d']=={'triangle_violations':tri,'ultrametric_violations':ultra},'gate d');need(d['gate_e']=='CERTIFIED_PER_PATH_NOT_UNIVERSAL','gate e')
 return {'execution_status':'COMPLETED','input_validity':'VALID','states':statesN,'edges':edgesN,'positive_barriers':len(actual),'gate_a':d['gate_a'],'gate_b':d['gate_b'],'gate_c':gate_c,'gate_d':{'triangle_violations':tri,'ultrametric_violations':ultra},'gate_e':'CERTIFIED_PER_PATH_NOT_UNIVERSAL','component_ranges':len(ranges)}
