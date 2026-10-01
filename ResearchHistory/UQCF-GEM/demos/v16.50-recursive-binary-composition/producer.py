"""Recursive fixed-root binary normalization with raw primitive paths."""
from itertools import product
L=();C=(L,L);F=(C,C);N=(F,C);D=(F,F)
TREES={'N':N,'D':D}
SCOPE='finite full binary trees; higher arity unresolved'
def layout(t):
 nodes=[]
 def visit(x):
  i=len(nodes);nodes.append([])
  if x:nodes[i]=[visit(x[0]),visit(x[1])]
  return i
 visit(t);return nodes
def data(t,q):
 nodes=layout(t);internal=[i for i,c in enumerate(nodes) if c]
 if len(q)!=len(internal) or any(x not in (1,2) for x in q):raise ValueError('target')
 target=dict(zip(internal,q));width={}
 for i in reversed(range(len(nodes))):
  if not nodes[i]:width[i]=1
  else:
   a,b=map(width.get,nodes[i]);width[i]=max(a,b) if target[i]==1 else a+b
 return nodes,target,width
def canonical(t,k,q,order=None):
 nodes,target,width=data(t,q);P=list(range(k)) if order is None else list(order)
 if len(P)!=k or set(P)!=set(range(k)) or k<width[0]:raise ValueError('palette')
 state=[0]*k
 def fill(i,labels):
  for j in labels:state[j]|=1<<i
  if nodes[i]:
   a,b=nodes[i];pa=labels[:width[a]];pb=labels[:width[b]] if target[i]==1 else labels[width[a]:width[a]+width[b]]
   fill(a,pa);fill(b,pb)
 fill(0,P);return state
def initial(t,k,q,perm,mode):
 nodes,target,width=data(t,q);base=canonical(t,k,q);state=[0]*k
 for j,z in enumerate(base):state[j if perm=='identity' else k-1-j if perm=='reversal' else (j+1)%k]=z
 if mode=='overlap_inflated':
  for i,children in enumerate(nodes):
   if children and target[i]==1:
    P=[j for j,z in enumerate(state) if z>>i&1]
    for child in children:
     for j in P:state[j]|=1<<child
 return state
def transport_roles(state,t,a,b,palette,rolesA,rolesB):
 current=list(state);path=[current[:]];nodes=layout(t)
 def subtree(i):
  out=[i]
  for c in nodes[i]:out+=subtree(c)
  return out
 def change(j,i,add):
  if add:current[j]|=1<<i
  else:current[j]&=~(1<<i)
  path.append(current[:])
 roles=list(rolesA)+list(rolesB);split=len(rolesA);regions=(subtree(a),subtree(b))
 def replace(i,y):
  x=roles[i];vertices=regions[0 if i<split else 1]
  if any(current[y]>>v&1 for v in vertices):raise ValueError('role destination occupied')
  used=[v for v in vertices if current[x]>>v&1]
  for v in used:change(y,v,True)
  for v in reversed(used):change(x,v,False)
  roles[i]=y
 def cross(i,j):
  x,y=roles[i],roles[j];replace(i,y);replace(j,x)
 def swap(i,j):
  if (i<split)!=(j<split):cross(i,j)
  else:
   pivot=split if i<split else 0;cross(i,pivot);cross(j,pivot);cross(i,pivot)
 for i,y in enumerate(palette[:len(roles)]):
  if roles[i]==y:continue
  if y in roles:swap(i,roles.index(y))
  else:replace(i,y)
 return path
def normalize(state,t,k,q,order=None):
 nodes,target,width=data(t,q);P=list(range(k)) if order is None else list(order)
 if len(P)!=k or set(P)!=set(range(k)):raise ValueError('ordered palette')
 current=list(state);path=[current[:]]
 def change(j,i,add):
  if add:current[j]|=1<<i
  else:current[j]&=~(1<<i)
  path.append(current[:])
 def support(i):return [j for j in P if current[j]>>i&1]
 def subtree(i):
  out=[i]
  for c in nodes[i]:out+=subtree(c)
  return out
 def recurse(i):
  if not nodes[i]:return
  palette=support(i);a,b=nodes[i]
  if target[i]==1:
   for c in (a,b):
    for j in palette:
     if not current[j]>>c&1:change(j,c,True)
  for c in (a,b):
   child_palette=support(c);recurse(c)
   for j in child_palette[width[c]:]:change(j,c,False)
  if target[i]==2:
   for nxt in transport_roles(current,t,a,b,palette,support(a),support(b))[1:]:
    current[:]=nxt;path.append(current[:])
 recurse(0);return path
def specs():
 rows=[]
 for name,t in TREES.items():
  count=sum(bool(c) for c in layout(t))
  for q in product((1,2),repeat=count):
   M=data(t,q)[2][0]
   for k in (M,M+1):
    for perm in ('identity','reversal','cyclic'):
     for mode in ('compact','overlap_inflated'):rows.append({'tree':name,'q':list(q),'k':k,'permutation':perm,'mode':mode})
 return rows
def produce():
 cases=[]
 for spec in specs():
  t=TREES[spec['tree']];k=spec['k'];q=spec['q'];start=initial(t,k,q,spec['permutation'],spec['mode'])
  try:path=normalize(start,t,k,q)
  except Exception as exc:path=None
  cases.append({'spec':spec,'width':data(t,q)[2][0],'start':start,'path':path})
 return {'schema':1,'scope':SCOPE,'cases':cases}
