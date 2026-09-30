from itertools import combinations
def need(x,m):
 if not x:raise ValueError(m)
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def qq(p,ys):return tuple(tau(p,ys,v) for v in range(len(p)))
def verify_move(d,invisible):
 p=tuple(d['parents']);a=tuple(map(tuple,d['before']));b=tuple(map(tuple,d['after']));need(set().union(*map(set,a))==set().union(*map(set,b)),'union');diff=sum(len(set(x)^set(y)) for x,y in zip(a,b));need(diff==1,'not single incidence');same=qq(p,a)==qq(p,b);need(same==invisible,'wrong invisibility');return True
def verify_class(c):
 p=tuple(c['parents']);mem=[tuple(map(tuple,x)) for x in c['members']];need(len(mem)==len(set(mem)),'duplicate members');need(all(qq(p,x)==tuple(c['q']) for x in mem),'wrong q')
 mins=[a for a in mem if not any(b!=a and all(set(y)<=set(x) for x,y in zip(a,b)) for b in mem)]
 need([[list(x) for x in y] for y in mins]==c['minima'],'false minima');need(c['unique_minimum']==(len(mins)==1),'false unique minimum')
 return True
def verify_document(d):
 need(d['version']=='16.33','version')
 for c in d['classes']:verify_class(c)
 if d['gate_c']=='MULTIPLE_MINIMA':need(d['first_multiple_minima'] is not None,'missing witness');verify_class(d['first_multiple_minima'])
 return {'execution_status':'COMPLETED','gate_b':d['gate_b'],'gate_c':d['gate_c']}
