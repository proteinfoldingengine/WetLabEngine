from itertools import combinations,product
from collections import deque
import json,hashlib
def tau(p,y,v):
 U=set().union(*map(set,y));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(y)+1) if any(K<=set().union(*(set(y[i]) for i in S)) for S in combinations(range(len(y)),r)))
def q(p,y):return tuple(tau(p,y,v) for v in range(len(p)))
def legal(p):
 return [tuple(i for i in range(len(p)) if m>>i&1) for m in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if m>>i&1) for v in tuple(i for i in range(len(p)) if m>>i&1))]
def covers(p,k):
 return [y for y in product(legal(p),repeat=k) if set().union(*map(set,y))==set(range(len(p)))]
def edge(a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1
def graph(states):
 A={x:[] for x in states}
 for i,x in enumerate(states):
  for y in states[i+1:]:
   if edge(x,y):A[x].append(y);A[y].append(x)
 return A
def minimax(p,A,a):
 q0=q(p,a);best={a:(0,0,0)};prev={a:None};todo=deque([a])
 while todo:
  x=todo.popleft()
  for y in A[x]:
   d=tuple(abs(u-v) for u,v in zip(q(p,y),q0));z=(max(best[x][0],sum(d)),max(best[x][1],max(d,default=0)),max(best[x][2],sum(t>0 for t in d)))
   if y not in best or z<best[y]:best[y]=z;prev[y]=x;todo.append(y)
 return best,prev
def path(prev,b):
 out=[];x=b
 while x is not None:out.append(x);x=prev[x]
 return list(reversed(out))
def within(z,lim):return z[0]<=lim[0] and z[1]<=lim[1] and z[2]<=lim[2]
def localization(p,A,a,b,lim):
 q0=q(p,a)
 def dev(s):
  d=tuple(abs(u-v) for u,v in zip(q(p,s),q0));return (sum(d),max(d,default=0),sum(x>0 for x in d))
 allowed={s for s in A if within(dev(s),lim)}
 def reach(forbid=None,require=None):
  start=(a,False);todo=deque([start]);prev={start:None};target=None
  while todo:
   x,used=todo.popleft()
   if x==b and (require is None or used):target=(x,used);break
   for y in A[x]:
    if y not in allowed:continue
    changed={i for i,(u,v) in enumerate(zip(q(p,y),q0)) if u!=v}
    if forbid is not None and forbid in changed:continue
    st=(y,used or (require is not None and require in changed))
    if st not in prev:prev[st]=(x,used);todo.append(st)
  if target is None:return None
  out=[];z=target
  while z is not None:out.append(z[0]);z=prev[z]
  return list(reversed(out))
 compulsory=[];possible=[];alt=None
 for v in range(len(p)):
  avoid=reach(forbid=v);use=reach(require=v)
  if avoid is None:compulsory.append(v)
  if use is not None:
   possible.append(v)
   if alt is None and v not in compulsory:alt=use
 return compulsory,possible,reach(),alt
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
def produce(bound=4,maxviews=3):
 records=[];state_total=edge_total=sameq_pairs=0;all_connected=True;dig=hashlib.sha256();component_ranges=[];triangle_viol=ultra_viol=0
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   states=covers(p,k);A=graph(states);state_total+=len(states);edge_total+=sum(map(len,A.values()))//2
   # Gate A full graph connectivity
   seen={states[0]};dq=deque([states[0]])
   while dq:
    x=dq.popleft()
    for y in A[x]:
     if y not in seen:seen.add(y);dq.append(y)
   all_connected &= len(seen)==len(states)
   G={}
   for y in states:G.setdefault(q(p,y),[]).append(y)
   for q0,mem in G.items():
    # zero-q components
    un=set(mem);Cs=[]
    while un:
     s=un.pop();C={s};dq=deque([s])
     while dq:
      x=dq.popleft()
      for y in A[x]:
       if y in un and q(p,y)==q0:un.remove(y);C.add(y);dq.append(y)
     Cs.append(C)
    if len(Cs)<2:continue
    # exact all-pairs minimax
    paircost={};paths={}
    for ai,a in enumerate(mem):
     best,prev=minimax(p,A,a)
     for b in mem[ai+1:]:
      sameq_pairs+=1;paircost[(a,b)]=best[b];paths[(a,b)]=path(prev,b)
    # component pair ranges + records for every cross-component pair
    for ci,cj in combinations(range(len(Cs)),2):
     vals=[]
     for a in Cs[ci]:
      for b in Cs[cj]:
       key=(a,b) if (a,b) in paircost else (b,a);z=paircost[key];vals.append(z)
       pp=paths[key]; pp=pp if pp[0]==a else list(reversed(pp))
       changed=sorted({v for s in pp for v,(u,w) in enumerate(zip(q(p,s),q0)) if u!=w})
       comp,poss,canon,alt=localization(p,A,a,b,z)
       records.append({'parents':list(p),'view_count':k,'component_pair':[ci,cj],'a':[list(x) for x in a],'b':[list(x) for x in b],'q':list(q0),'B1':z[0],'Binf':z[1],'Bs':z[2],'changed_coordinates':changed,'path':[[list(x) for x in s] for s in pp],'compulsory_coordinates':comp,'possible_coordinates':poss,'localization':'FIXED' if comp==poss else 'PATH_DEPENDENT','canonical_minimax_path':[[list(x) for x in s] for s in canon],'alternative_path':None if alt is None else [[list(x) for x in s] for s in alt]})
     component_ranges.append({'parents':list(p),'view_count':k,'q':list(q0),'components':[ci,cj],'B1_range':[min(x[0] for x in vals),max(x[0] for x in vals)],'Binf_range':[min(x[1] for x in vals),max(x[1] for x in vals)],'Bs_range':[min(x[2] for x in vals),max(x[2] for x in vals)]})
    # Gate D on component minimum B1
    if len(Cs)>=3:
     dist={}
     for i,j in combinations(range(len(Cs)),2):
      vals=[]
      for a in Cs[i]:
       best,_=minimax(p,A,a)
       vals += [best[b][0] for b in Cs[j]]
      dist[i,j]=min(vals)
     for i,j,l in combinations(range(len(Cs)),3):
      dij=dist[min(i,j),max(i,j)];djl=dist[min(j,l),max(j,l)];dil=dist[min(i,l),max(i,l)]
      if dil>dij+djl or dij>dil+djl or djl>dij+dil:triangle_viol+=1
      if dil>max(dij,djl) or dij>max(dil,djl) or djl>max(dij,dil):ultra_viol+=1
   dig.update((repr((p,k,[(q(p,s),s) for s in states]))+'\n').encode())
 return {'version':'16.35','bound':bound,'maxviews':maxviews,'gate_a':'CONNECTED' if all_connected else 'COUNTEREXAMPLE','gate_b':'POSITIVE' if records and all(r['B1']>0 for r in records) else 'COUNTEREXAMPLE','gate_c':'REPRESENTATIVE_INDEPENDENT' if all(x['B1_range'][0]==x['B1_range'][1] and x['Binf_range'][0]==x['Binf_range'][1] and x['Bs_range'][0]==x['Bs_range'][1] for x in component_ranges) else 'REPRESENTATIVE_DEPENDENT','gate_d':{'triangle_violations':triangle_viol,'ultrametric_violations':ultra_viol},'gate_e':'FIXED' if records and all(r['localization']=='FIXED' for r in records) else ('PATH_DEPENDENT' if any(r['localization']=='PATH_DEPENDENT' for r in records) else 'NO_POSITIVE_PAIRS'),'states':state_total,'edges':edge_total,'same_q_pairs_in_disconnected_fibers':sameq_pairs,'positive_barriers':len(records),'barriers':records,'component_ranges':component_ranges,'digest':dig.hexdigest()}
if __name__=='__main__':
 d=produce();open('PRODUCTION.json','w').write(json.dumps(d,indent=2,sort_keys=True));print(json.dumps({k:d[k] for k in ('gate_a','gate_b','gate_c','gate_d','gate_e','states','edges','same_q_pairs_in_disconnected_fibers','positive_barriers','digest')}))
