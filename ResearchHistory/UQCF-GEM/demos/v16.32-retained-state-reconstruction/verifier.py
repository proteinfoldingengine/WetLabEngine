from itertools import combinations,product
import hashlib
ALLOWED=['tau','h','component_values']
def need(x,m):
 if not x:raise ValueError(m)
def checker_collision(a,b):return a==b
def tau(p,ys,v):
 U=set().union(*map(set,ys));K={w for w in U if w and p[w]==v}
 if not K:return 0
 return min(r for r in range(1,len(ys)+1) if any(K<=set().union(*(set(ys[i]) for i in S)) for S in combinations(range(len(ys)),r)))
def sig(p,ys):
 t=tuple(tau(p,ys,v) for v in range(len(p)));return {'tau':list(t),'h':max([1]+list(t)),'component_values':[list(x) for x in ((v,t[v]) for v in range(len(p)) if t[v])]}
def valid_views(p,ys):
 out=[]
 for y in ys:
  y=tuple(y);need(y and 0 in y and len(set(y))==len(y),'view');need(all(type(n)is int and 0<=n<len(p) for n in y),'identity');need(all(n==0 or p[n] in y for n in y),'prefix');out.append(y)
 return tuple(out)
def reachable(p,initial,final):
 rem=[(i,n) for i,(y,z) in enumerate(zip(initial,final)) for n in y if n not in z];out=[]
 for mask in range(1<<len(rem)):
  deleted={rem[j] for j in range(len(rem)) if mask>>j&1};ys=[];ok=True
  for i,y in enumerate(initial):
   q=tuple(n for n in y if (i,n) not in deleted)
   if any(n and p[n] not in q for n in q):ok=False;break
   ys.append(q)
  if ok and set().union(*map(set,ys))==set(range(len(p))):out.append(tuple(ys))
 return set(out)
def verify_collision(c):
 need(set(c)=={'parents','initial','final','left','right','signature'},'collision schema');p=tuple(c['parents']);I=valid_views(p,c['initial']);F=valid_views(p,c['final']);L=valid_views(p,c['left']);R=valid_views(p,c['right']);need(L!=R,'not distinct');rr=reachable(p,I,F);need(L in rr and R in rr,'not same interval/reachable');sl,sr=sig(p,L),sig(p,R);need(sl==sr==c['signature'],'false collision');return True
def verify_document(d):
 need(d.get('version')=='16.32','version');need(d.get('signature_fields')==ALLOWED,'signature fields');need(not any(x in d['signature_fields'] for x in ('state_mask','deletion_mask','incidence_bitmap','state_identity')),'tautological signature')
 cols=d.get('collisions');need(isinstance(cols,list),'collisions')
 for c in cols:verify_collision(c)
 if d.get('verdict')=='NONINJECTIVE':need(cols,'missing witness')
 if d.get('verdict')=='RECONSTRUCTIVE_ON_BOUNDED_CLASS':need(not cols,'contradiction')
 return {'execution_status':'COMPLETED','input_validity':'VALID','verdict':d['verdict'],'witnesses':len(cols)}
