from itertools import combinations,product
import json,hashlib
FIELDS=['tau','h','component_values']
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def signature(p,ys):
 t=tuple(tau(p,ys,v) for v in range(len(p)));h=max([1]+list(t))
 # component values are value-level closure data. Use the complete labeled parent-local profile,
 # which v16.31 proves reconstructs tau; do not include deletion/state identity.
 cv=tuple((v,t[v]) for v in range(len(p)) if t[v])
 return {'tau':list(t),'h':h,'component_values':[list(x) for x in cv]}
def code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def shapes(bound):
 d={}
 for n in range(1,bound+1):
  for q in product(*(range(i) for i in range(1,n))):
   p=(-1,)+q;d.setdefault(code(p),p)
 return list(d.values())
def legal(p):
 out=[]
 for mask in range(1,1<<len(p),2):
  y=tuple(i for i in range(len(p)) if mask>>i&1)
  if all(v==0 or p[v] in y for v in y):out.append(y)
 return out
def covers(p,maxviews=4):
 L=legal(p)
 for n in range(1,min(maxviews,len(L))+1):
  for ys in combinations(L,n):
   if set().union(*map(set,ys))==set(range(len(p))):yield ys
def reachable_states(p,initial,final):
 rem=[(i,n) for i,(y,z) in enumerate(zip(initial,final)) for n in y if n not in z]
 out=[]
 for mask in range(1<<len(rem)):
  deleted={rem[j] for j in range(len(rem)) if mask>>j&1};ys=[];ok=True
  for i,y in enumerate(initial):
   q=tuple(n for n in y if (i,n) not in deleted)
   if any(n and p[n] not in q for n in q):ok=False;break
   ys.append(q)
  if ok and set().union(*map(set,ys))==set(range(len(p))):out.append(tuple(ys))
 return sorted(set(out))
def endpoints(p,bound_events=5):
 L=legal(p)
 for init in covers(p):
  pools=[[z for z in L if set(z)<=set(y)] for y in init]
  for final in product(*pools):
   if set().union(*map(set,final))!=set(range(len(p))):continue
   r=sum(len(set(y)-set(z)) for y,z in zip(init,final))
   if r<=bound_events:yield init,final
def key(sig):return (tuple(sig['tau']),sig['h'],tuple(map(tuple,sig['component_values'])))
def produce(bound=4):
 intervals=states=profile_collisions=closed_collisions=0;first=None;digest=hashlib.sha256()
 for p in shapes(bound):
  for iid,(initial,final) in enumerate(endpoints(p)):
   ss=reachable_states(p,initial,final);states+=len(ss);intervals+=1;groups={}
   for s in ss:
    sg=signature(p,s);groups.setdefault(key(sg),[]).append(s)
   cols=[g for g in groups.values() if len(g)>1]
   profile_collisions+=sum(len(g)-1 for g in cols);closed_collisions+=sum(len(g)-1 for g in cols)
   if cols and first is None:
    g=cols[0];first={'parents':list(p),'initial':[list(x) for x in initial],'final':[list(x) for x in final],
     'left':[list(x) for x in g[0]],'right':[list(x) for x in g[1]],'signature':signature(p,g[0])}
   digest.update((repr((p,initial,final,[(s,key(signature(p,s))) for s in ss]))+'\n').encode())
 return {'version':'16.32','signature_fields':FIELDS,'bound':bound,'intervals':intervals,'states':states,
  'profile_collisions':profile_collisions,'closed_collisions':closed_collisions,'collisions':[] if first is None else [first],
  'verdict':'NONINJECTIVE' if first else 'RECONSTRUCTIVE_ON_BOUNDED_CLASS','digest':digest.hexdigest()}
def small_document():return produce(2)
if __name__=='__main__':
 d=produce(4);open('PRODUCTION.json','w').write(json.dumps(d,sort_keys=True,indent=2));print(json.dumps({k:d[k] for k in ('intervals','states','profile_collisions','closed_collisions','verdict','digest')}))
