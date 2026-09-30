from itertools import combinations,product
import json,hashlib
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def q(p,ys):return tuple(tau(p,ys,v) for v in range(len(p)))
def legal_views(p):
 out=[]
 for mask in range(1,1<<len(p),2):
  y=tuple(i for i in range(len(p)) if mask>>i&1)
  if all(v==0 or p[v] in y for v in y):out.append(y)
 return out
def covers(p,k):
 for ys in product(legal_views(p),repeat=k):
  if set().union(*map(set,ys))==set(range(len(p))):yield ys
def adjacent(p,a,b):
 dif=sum(len(set(x)^set(y)) for x,y in zip(a,b))
 if dif!=1:return False
 return q(p,a)==q(p,b)
def class_info(p,members):
 mins=[]
 for a in members:
  if not any(b!=a and all(set(y)<=set(x) for x,y in zip(a,b)) for b in members):mins.append(a)
 # graph connectivity by one-incidence q-preserving moves
 seen={members[0]};stack=[members[0]]
 while stack:
  a=stack.pop()
  for b in members:
   if b not in seen and adjacent(p,a,b):seen.add(b);stack.append(b)
 return mins,len(seen)==len(members)
def controls():
 p=(-1,0,0);inv={'parents':list(p),'before':[[0,1],[0,1,2]],'after':[[0],[0,1,2]]}
 vis={'parents':list(p),'before':[[0,1,2],[0,1],[0,2]],'after':[[0,1],[0,1],[0,2]]}
 return inv,vis
def small_document():
 d=produce(2); 
 # ensure a multiple-minimum class for adversarial mutation; use synthetic exact class if absent
 if not d['classes']:d['classes']=[{'parents':[-1,0,0],'q':[1,0,0],'members':[[[0,1],[0,2]],[[0,2],[0,1]]],'minima':[[[0,1],[0,2]],[[0,2],[0,1]]],'unique_minimum':False,'connected':False}]
 return d
def shapes(bound):
 d={}
 def code(p):
  ch={v:[] for v in range(len(p))}
  for w in range(1,len(p)):ch[p[w]].append(w)
  def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
  return rec(0)
 for n in range(1,bound+1):
  for z in product(*(range(i) for i in range(1,n))):
   p=(-1,)+z;d.setdefault(code(p),p)
 return list(d.values())
def produce(bound=4,maxviews=3):
 classes=[];total=nontriv=disc=multi=0;first_multi=None;dig=hashlib.sha256()
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   groups={}
   for ys in covers(p,k):groups.setdefault(q(p,ys),[]).append(ys)
   for qq,mem in groups.items():
    total+=1
    if len(mem)>1:
     nontriv+=1;mins,conn=class_info(p,mem);disc+=not conn;multi+=len(mins)>1
     rec={'parents':list(p),'view_count':k,'q':list(qq),'members':[[list(x) for x in y] for y in mem],'minima':[[list(x) for x in y] for y in mins],'unique_minimum':len(mins)==1,'connected':conn}
     if first_multi is None and len(mins)>1:first_multi=rec
     if len(classes)<30:classes.append(rec)
    dig.update((repr((p,k,qq,mem))+'\n').encode())
 return {'version':'16.33','bound':bound,'maxviews':maxviews,'classes_total':total,'nontrivial_classes':nontriv,'disconnected_classes':disc,'multiple_minima_classes':multi,'gate_b':'GENERATED_BY_LOCAL_MOVES' if disc==0 else 'COUNTEREXAMPLE','gate_c':'MULTIPLE_MINIMA' if multi else 'UNIQUE_MINIMAL','classes':classes,'first_multiple_minima':first_multi,'digest':dig.hexdigest()}
if __name__=='__main__':
 d=produce();open('PRODUCTION.json','w').write(json.dumps(d,indent=2,sort_keys=True));print(json.dumps({k:d[k] for k in ('classes_total','nontrivial_classes','disconnected_classes','multiple_minima_classes','gate_b','gate_c','digest')}))
