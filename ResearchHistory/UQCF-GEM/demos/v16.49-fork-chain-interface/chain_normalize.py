"""Recursive compact-palette chain repair; complete finite and directed outputs."""
from itertools import combinations,product
import graph_producer as graph
from star_normalize import normalize as star
DOMAIN=(((2,2,2,2),2),((2,2,2,2),3),((3,2,2,2),2),((2,3,2,2),2),((2,2,3,2),2),((2,2,2,3),2))
def tree(degrees):
 code='('+'()'*degrees[-1]+')'
 for d in reversed(degrees[:-1]):code='('+code+'()'*(d-1)+')'
 return code
def need(d,q):
 if len(d)==1:return q[0]
 m=need(d[1:],q[1:]);return max(q[0],m) if q[0]<d[0] else d[0]-1+m
def pattern(d,k,q):
 supports=[set(range(k))]+[set() for _ in range(sum(d))]
 def fill(ds,qs,P,root):
  if len(ds)==1:
   for i in range(ds[0]):supports[root+1+i]={P[i] if i<qs[0] else P[0]}
   return
  child_size=sum(ds[1:])+1;l=ds[0]-1;m=need(ds[1:],qs[1:]);sat=qs[0]==ds[0]
  inner=P[l:l+m] if sat else P[:m];supports[root+1]=set(inner)
  fill(ds[1:],qs[1:],inner,root+1)
  for i in range(l):supports[root+1+child_size+i]={P[i] if i<(l if sat else qs[0]) else P[0]}
 fill(d,q,list(range(k)),0)
 return [sum(1<<v for v,S in enumerate(supports) if j in S) for j in range(k)]
def normalize(state,degrees,k,q):
 d=tuple(degrees);q=list(q[:len(d)]);current=list(state);path=[current[:]]
 if k==1:return path
 if len(d)==1:return star(current,d[0],k,q[0])
 size=sum(d[1:])+1;mask=(1<<size)-1;outer_vertices=list(range(size+1,sum(d)+1));l=d[0]-1;r=q[0]
 def change(j,v,add):
  if add:current[j]|=1<<v
  else:current[j]&=~(1<<v)
  path.append(current[:])
 def inner(P):
  view=[(current[j]>>1)&mask for j in P]
  for nxt in normalize(view,d[1:],len(P),q[1:])[1:]:
   for j,z in zip(P,nxt):current[j]=(current[j]&~(mask<<1))|(z<<1)
   path.append(current[:])
 def contract(P):
  for j in P[need(d[1:],q[1:]):]:change(j,1,False)
 if r<d[0]:
  h=next(t for t in range(1,k+1) if any(all(any(current[j]>>v&1 for j in H) for v in outer_vertices) for H in combinations(range(k),t)))
  view=[1|sum(((current[j]>>v)&1)<<(i+1) for i,v in enumerate(outer_vertices)) for j in range(k)]
  for nxt in star(view,l,k,h)[1:]:
   for j,z in enumerate(nxt):
    for i,v in enumerate(outer_vertices):current[j]=(current[j]&~(1<<v))|(((z>>(i+1))&1)<<v)
   path.append(current[:])
  for j in range(k):
   if not current[j]&2:change(j,1,True)
  if h==r-1:change(r-1,outer_vertices[r-1],True);change(0,outer_vertices[r-1],False)
  inner(list(range(k)));contract(list(range(k)));return path
 P=[j for j in range(k) if current[j]&2];inner(P);contract(P);roles=[]
 for v in outer_vertices:
  colors=[j for j in range(k) if current[j]>>v&1];roles.append(colors[0])
  for j in colors[1:]:change(j,v,False)
 roles+=P[:need(d[1:],q[1:])]
 def replace_inner(x,y):
  vertices=[v for v in range(1,size+1) if current[x]>>v&1]
  for v in vertices:change(y,v,True)
  for v in reversed(vertices):change(x,v,False)
 def replace(i,y):
  x=roles[i]
  if i<l:change(y,outer_vertices[i],True);change(x,outer_vertices[i],False)
  else:replace_inner(x,y)
  roles[i]=y
 def cross(i,o):
  x,y=roles[i],roles[o];replace_inner(x,y);v=outer_vertices[o]
  change(x,v,True);change(y,v,False);roles[i],roles[o]=y,x
 def swap(i,j):
  if i<l and j<l:
   x,y=roles[i],roles[j];u,v=outer_vertices[i],outer_vertices[j]
   change(y,u,True);change(x,v,True);change(x,u,False);change(y,v,False);roles[i],roles[j]=y,x
  elif i>=l and j>=l:cross(i,0);cross(j,0);cross(i,0)
  else:cross(i,j) if i>=l else cross(j,i)
 for i in range(len(roles)):
  if roles[i]==i:continue
  if i in roles:swap(i,roles.index(i))
  else:replace(i,i)
 return path
def corpus_specs():
 targets=[(d,q) for d in ((2,2,2,2),(3,2,3,2)) for q in product((1,2),repeat=4)]
 targets += [((2,)*8,q) for q in ((1,)*8,(2,)*8,(1,2)*4)]
 return [{'degrees':list(d),'q':list(q),'k':need(d,q)+extra,'permutation':perm} for d,q in targets for extra in (0,1) for perm in ('identity','reversal','cyclic')]
def produce(domain=DOMAIN,specs=None):
 entries=[]
 for d,k in domain:
  g=graph.build(tree(d),k);index={tuple(s):i for i,s in enumerate(g['states'])};paths=[]
  for rec in g['profiles']:
   for comp in rec['zero_components']:
    i=comp[0];q=rec['q']
    try:path=[index.get(tuple(z),-1) for z in normalize(g['states'][i],d,k,q)]
    except Exception:path=None
    paths.append({'state':i,'q':q,'path':path})
  entries.append({'degrees':list(d),'k':k,'graph':g,'normalizations':paths})
 corpus=[]
 for spec in (corpus_specs() if specs is None else specs):
  d=spec['degrees'];q=spec['q'];k=spec['k'];p=spec['permutation'];base=pattern(d,k,q);start=[0]*k
  for j in range(k):start[j if p=='identity' else k-1-j if p=='reversal' else (j+1)%k]=base[j]
  try:path=normalize(start,d,k,q)
  except Exception:path=None
  corpus.append({'spec':spec,'palette_requirement':need(d,q),'start':start,'path':path})
 return {'schema':1,'domain':[{'degrees':list(d),'k':k} for d,k in domain],'entries':entries,'corpus':corpus}
