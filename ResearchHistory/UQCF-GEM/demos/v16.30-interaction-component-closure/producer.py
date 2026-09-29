from itertools import combinations,product
import json,hashlib
def need(x,m):
 if not x:raise ValueError(m)
def h(p,ys):
 U=set().union(*map(set,ys));vals=[1]
 for v in U:
  K={w for w in U if w and p[w]==v}
  if K:vals.append(tau(p,ys,v))
 return max(vals)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def square(p,ys,e,f):
 def dele(state,event):
  i,n=event;z=list(state);z[i]=tuple(x for x in z[i] if x!=n);return tuple(z)
 a=tuple(map(tuple,ys));b=dele(a,e);c=dele(a,f);d=dele(b,f);U=set().union(*map(set,a));need(all(set().union(*map(set,s))==U for s in (b,c,d)),'union')
 prof=lambda s:tuple(tau(p,s,v) for v in range(len(p)))
 P=[prof(s) for s in (a,b,c,d)];H=[h(p,s) for s in (a,b,c,d)];lm=tuple(P[3][v]-P[1][v]-P[2][v]+P[0][v] for v in range(len(p)))
 return {'parents':list(p),'views':[list(x) for x in a],'events':[list(e),list(f)],'profiles':[list(x) for x in P],'h':H,'local_mixed':list(lm),'global_mixed':H[3]-H[1]-H[2]+H[0]}
def control_max_only():return square((-1,0,0,1,1),[(0,1,2),(0,1,3,4),(0,2),(0,1,4)],(0,2),(1,4))
def control_masked():return square((-1,0,0,1,1),[(0,1,3,4),(0,1,3),(0,1,4),(0,2)],(0,3),(0,4))
def shape_code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def shapes(bound):
 d={}
 for n in range(1,bound+1):
  for q in product(*(range(i) for i in range(1,n))):
   p=(-1,)+q;d.setdefault(shape_code(p),p)
 return list(d.values())
def legal(p):
 return [tuple(i for i in range(len(p)) if mask>>i&1) for mask in range(1,1<<len(p),2) if all(v==0 or p[v] in tuple(i for i in range(len(p)) if mask>>i&1) for v in tuple(i for i in range(len(p)) if mask>>i&1))]
def current_events(p,ys):
 U=set().union(*map(set,ys));out=[]
 for i,y in enumerate(ys):
  for n in y:
   if n and not any(p[w]==n and w in y for w in y):
    z=list(ys);z[i]=tuple(x for x in y if x!=n)
    if set().union(*map(set,z))==U:out.append((i,n))
 return out
def small_document():
 c=control_masked();return {'version':'16.30','cases':[{'parents':c['parents'],'events':c['events'],'edges':[[c['events'][0],c['events'][1]]]}]}
def produce(bound=5):
 pair=edges=cross=0;digest=hashlib.sha256();controls={'max_only':control_max_only(),'masked':control_masked()}
 for p in shapes(bound):
  L=legal(p)
  for k in range(1,min(4,len(L))+1):
   for ys in combinations(L,k):
    if set().union(*map(set,ys))!=set(range(len(p))):continue
    ev=current_events(p,ys)
    for e,f in combinations(ev,2):
     try:q=square(p,ys,e,f)
     except ValueError:continue
     pair+=1
     if any(q['local_mixed']):edges+=1;cross+=p[e[1]]!=p[f[1]]
     digest.update((repr((p,ys,e,f,tuple(q['local_mixed'])))+'\n').encode())
 return {'version':'16.30','bound':bound,'pairs':pair,'local_edges':edges,'cross_parent_edges':cross,'digest':digest.hexdigest(),'controls':controls,'c5':'PAIRWISE_GRAPH_COMPLETE'}

if __name__=='__main__':
 d=produce(5);open('PRODUCTION.json','w').write(json.dumps(d,sort_keys=True,indent=2));print(json.dumps({k:d[k] for k in ('pairs','local_edges','cross_parent_edges','digest','c5')}))
