from itertools import combinations,product
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def qq(p,ys):return tuple(tau(p,ys,v) for v in range(len(p)))
def verify_move(d,invisible):
 p=tuple(d['parents']);a=tuple(map(tuple,d['before']));b=tuple(map(tuple,d['after']));need(set().union(*map(set,a))==set().union(*map(set,b)),'union');need(sum(len(set(x)^set(y)) for x,y in zip(a,b))==1,'not single incidence');need((qq(p,a)==qq(p,b))==invisible,'wrong invisibility');return True
def legal_views(p):
 out=[]
 for mask in range(1,1<<len(p),2):
  y=tuple(i for i in range(len(p)) if mask>>i&1)
  if all(v==0 or p[v] in y for v in y):out.append(y)
 return out
def covers(p,k):
 for ys in product(legal_views(p),repeat=k):
  if set().union(*map(set,ys))==set(range(len(p))):yield ys
def adjacent(p,a,b):return sum(len(set(x)^set(y)) for x,y in zip(a,b))==1 and qq(p,a)==qq(p,b)
def class_info(p,mem):
 mins=[a for a in mem if not any(b!=a and all(set(y)<=set(x) for x,y in zip(a,b)) for b in mem)]
 seen={mem[0]};stack=[mem[0]]
 while stack:
  a=stack.pop()
  for b in mem:
   if b not in seen and adjacent(p,a,b):seen.add(b);stack.append(b)
 return mins,len(seen)==len(mem)
def code(p):
 ch={v:[] for v in range(len(p))}
 for w in range(1,len(p)):ch[p[w]].append(w)
 def rec(v):return '('+''.join(sorted(rec(w) for w in ch[v]))+')'
 return rec(0)
def shapes(bound):
 d={}
 for n in range(1,bound+1):
  for z in product(*(range(i) for i in range(1,n))):
   p=(-1,)+z;d.setdefault(code(p),p)
 return list(d.values())
def reconstruct(bound,maxviews):
 allclasses=[];total=non=disc=multi=0
 for p in shapes(bound):
  for k in range(1,maxviews+1):
   groups={}
   for ys in covers(p,k):groups.setdefault(qq(p,ys),[]).append(ys)
   for qv,mem in groups.items():
    total+=1
    if len(mem)>1:
     non+=1;mins,conn=class_info(p,mem);disc+=not conn;multi+=len(mins)>1
     allclasses.append((p,qv,mem,mins,conn))
 return total,non,disc,multi,allclasses
def verify_class(c,expected=None):
 p=tuple(c['parents']);mem=[tuple(map(tuple,x)) for x in c['members']];need(len(mem)==len(set(mem)),'duplicate members');need(all(qq(p,x)==tuple(c['q']) for x in mem),'wrong q');mins,conn=class_info(p,mem);need([[list(x) for x in y] for y in mins]==c['minima'],'false minima');need(c['unique_minimum']==(len(mins)==1),'false unique');need(c['connected']==conn,'false connectivity')
 if expected is not None:need(set(mem)==set(expected),'omitted/foreign class member')
 return True
def verify_document(d):
 need(d['version']=='16.33','version');bound=d['bound'];mv=d['maxviews'];total,non,disc,multi,classes=reconstruct(bound,mv)
 need((d['classes_total'],d['nontrivial_classes'],d['disconnected_classes'],d['multiple_minima_classes'])==(total,non,disc,multi),'false bulk counts')
 lookup={(tuple(p),tuple(qv)):mem for p,qv,mem,mins,conn in classes}
 need(len(d['classes'])==min(30,len(classes)),'missing class records')
 for c in d['classes']:
  key=(tuple(c['parents']),tuple(c['q']));need(key in lookup,'unknown class');verify_class(c,lookup[key])
 if d['gate_b']=='COUNTEREXAMPLE':need(disc>0,'false gate b')
 if d['gate_c']=='MULTIPLE_MINIMA':need(multi>0 and d['first_multiple_minima'] is not None,'missing minima witness');verify_class(d['first_multiple_minima'],lookup[(tuple(d['first_multiple_minima']['parents']),tuple(d['first_multiple_minima']['q']))])
 return {'execution_status':'COMPLETED','input_validity':'VALID','classes_total':total,'nontrivial_classes':non,'disconnected_classes':disc,'multiple_minima_classes':multi,'gate_b':d['gate_b'],'gate_c':d['gate_c']}
