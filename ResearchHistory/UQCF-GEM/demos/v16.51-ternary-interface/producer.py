"""One ternary root; inherited binary normalization and exact interior role transport."""
from pathlib import Path
from itertools import product,combinations
import importlib.util
s=importlib.util.spec_from_file_location('v1650_binary',Path(__file__).resolve().parent.parent/'v16.50-recursive-binary-composition/producer.py')
binary=importlib.util.module_from_spec(s);s.loader.exec_module(binary)
L=();C=(L,L);D=(C,L);F=(C,C);T=(C,C,C);U=(C,D,F);TREES={'T':T,'U':U}
SCOPE='one ternary root over finite full binary child trees; repeated ternary composition unresolved'
def layout(t):
 nodes=[]
 def walk(t):
  i=len(nodes);nodes.append([]);nodes[i]=[walk(x) for x in t];return i
 walk(t);return nodes
def vertices(nodes,i):
 return [i]+[v for c in nodes[i] for v in vertices(nodes,c)]
def data(t,q):
 nodes=layout(t);internal=[i for i,c in enumerate(nodes) if c]
 if len(nodes[0])!=3 or any(len(c) not in (0,2) for c in nodes[1:]):raise ValueError('scope')
 if len(q)!=len(internal) or any(type(x)!=int or x not in ((1,2,3) if n==0 else (1,2)) for n,x in enumerate(q)):raise ValueError('target')
 target=dict(zip(internal,q));w={}
 for i in reversed(range(len(nodes))):
  a=[w[c] for c in nodes[i]]
  w[i]=1 if not a else max(a) if target[i]==1 else sum(a) if target[i]==len(a) else max(max(a),(sum(a)+1)//2)
 return nodes,target,w
def palettes(P,widths,r):
 if r==1:return [P[:w] for w in widths]
 if r==3:
  out=[];offset=0
  for w in widths:out.append(P[offset:offset+w]);offset+=w
  return out
 M=max(max(widths),(sum(widths)+1)//2);out=[];offset=0
 for w in widths:
  chosen={P[j%M] for j in range(offset,offset+w)};out.append([j for j in P if j in chosen]);offset+=w
 return out
def canonical(t,k,q,order=None):
 nodes,target,w=data(t,q);P=list(range(k)) if order is None else list(order)
 if len(P)!=k or set(P)!=set(range(k)) or k<w[0]:raise ValueError('palette')
 state=[1]*k
 for i,c in enumerate(nodes[0]):
  labels=palettes(P,[w[x] for x in nodes[0]],target[0])[i];vs=vertices(nodes,c);cq=[target[v] for v in vs if nodes[v]]
  raw=binary.canonical(t[i],len(labels),cq)
  for j,z in enumerate(raw):
   for n,v in enumerate(vs):
    if z>>n&1:state[labels[j]]|=1<<v
 return state
def root_hitting(roots):
 if set.intersection(*roots):return 1
 return 2 if any(a&b for a,b in combinations(roots,2)) else 3
def initial(t,k,q,perm,mode):
 nodes,target,w=data(t,q);base=canonical(t,k,q);state=[0]*k
 for j,z in enumerate(base):state[j if perm=='identity' else k-1-j if perm=='reversal' else (j+1)%k]=z
 if mode=='interface_and_binary_inflated':
  for c in nodes[0]:
   for j in range(k):
    if state[j]>>c&1:continue
    state[j]|=1<<c
    if root_hitting([{x for x,z in enumerate(state) if z>>v&1} for v in nodes[0]])!=q[0]:state[j]&=~(1<<c)
  for i in range(1,len(nodes)):
   if nodes[i] and target[i]==1:
    for c in nodes[i]:
     for j,z in enumerate(state):
      if z>>i&1:state[j]|=1<<c
 return state
def replace_role(current,nodes,child,x,y,path):
 vs=vertices(nodes,child)
 if any(current[y]>>v&1 for v in vs):raise ValueError('role destination occupied')
 used=[v for v in vs if current[x]>>v&1]
 for v in used:current[y]|=1<<v;path.append(current[:])
 for v in reversed(used):current[x]&=~(1<<v);path.append(current[:])
def transport_child(state,t,child,roles,desired,P,trace=None):
 trace=[] if trace is None else trace;nodes=layout(t);current=list(state);path=[current[:]];roles=list(roles)
 for i,y in enumerate(desired):
  if roles[i]==y:continue
  if y in roles:
   other=roles.index(y);hole=next(j for j in P if j not in roles)
   replace_role(current,nodes,child,roles[other],hole,path);roles[other]=hole
   trace.append({'kind':'local_hole','child':child,'label':hole})
  replace_role(current,nodes,child,roles[i],y,path);roles[i]=y
 return path
def _normalize(state,t,k,q,order=None,trace=None,_record=None):
 trace=[] if trace is None else trace;nodes,target,w=data(t,q);P=list(range(k)) if order is None else list(order)
 if len(P)!=k or set(P)!=set(range(k)):raise ValueError('ordered palette')
 current=list(state);path=[] if _record is None else _record;path.append(current[:]);children=nodes[0];r=target[0]
 def support(c):return [j for j in P if current[j]>>c&1]
 def change(j,c,add):
  if add:current[j]|=1<<c
  else:current[j]&=~(1<<c)
  path.append(current[:])
 chosen=();anchor=None
 if r==2:
  for i,j in combinations(range(3),2):
   overlap=[x for x in P if x in support(children[i]) and x in support(children[j])]
   if overlap:chosen=(i,j);anchor=overlap[0];break
  if not chosen:raise ValueError('no shared pair')
  trace.append({'kind':'anchor','pair':list(chosen),'label':anchor,'end':0})
 if r==1:
  for c in children:
   for j in P:
    if not current[j]>>c&1:change(j,c,True)
  trace.append({'kind':'root_expansion','end':len(path)-1})
 roles=[]
 for i,c in enumerate(children):
  labels=support(c)
  if r==2 and i in chosen and w[c]<k:labels=[anchor]+[j for j in labels if j!=anchor]
  vs=vertices(nodes,c);cq=[target[v] for v in vs if nodes[v]]
  raw=[sum(1<<n for n,v in enumerate(vs) if current[j]>>v&1) for j in labels]
  inner=binary.normalize(raw,t[i],len(labels),cq)
  region=sum(1<<v for v in vs)
  for rawstep in inner[1:]:
   for j in P:current[j]&=~region
   for n,j in enumerate(labels):
    for pos,v in enumerate(vs):
     if rawstep[n]>>pos&1:current[j]|=1<<v
   path.append(current[:])
  for j in labels[w[c]:]:change(j,c,False)
  roles.append(labels[:w[c]])
  trace.append({'kind':'child_normalization','child':c,'end':len(path)-1})
  if r==2 and w[c]==k:trace.append({'kind':'whole_palette_child','child':c,'end':len(path)-1})
 targets=palettes(P,[w[c] for c in children],r)
 if r==2:
  for i,c in enumerate(children):
   if w[c]==k:continue
   trace.append({'kind':'role_transport','child':c})
   for nxt in transport_child(current,t,c,roles[i],targets[i],P,trace)[1:]:current[:]=nxt;path.append(current[:])
  trace.append({'kind':'transport_complete','end':len(path)-1})
 if r==3:
  flat=[j for row in roles for j in row];owner=[c for c,row in zip(children,roles) for j in row]
  def replace(i,y):
   replace_role(current,nodes,owner[i],flat[i],y,path);flat[i]=y
  def cross(i,j):
   x,y=flat[i],flat[j];replace(i,y);replace(j,x)
  def swap(i,j):
   if owner[i]!=owner[j]:cross(i,j)
   else:
    pivot=next(n for n,c in enumerate(owner) if c!=owner[i]);cross(i,pivot);cross(j,pivot);cross(i,pivot)
  for i,y in enumerate(P[:len(flat)]):
   if flat[i]==y:continue
   if y in flat:swap(i,flat.index(y))
   else:replace(i,y)
   trace.append({'kind':'disjoint_transport','end':len(path)-1})
 return path
class ConstructionFailure(Exception):
 def __init__(self,original,path):super().__init__(str(original));self.path=path
 def __str__(self):return super().__str__()
def normalize(state,t,k,q,order=None,trace=None):
 attempted=[]
 try:return _normalize(state,t,k,q,order,trace,attempted)
 except Exception as exc:raise ConstructionFailure(exc,attempted) from exc
normalize_ternary=normalize
def specs():
 rows=[]
 for name,t in TREES.items():
  n=sum(bool(c) for c in layout(t))-1
  for inner in product((1,2),repeat=n):
   for r in (1,2,3):
    q=[r,*inner];M=data(t,q)[2][0]
    for k in (M,M+1):
     for perm in ('identity','reversal','cyclic'):
      for mode in ('compact','interface_and_binary_inflated'):rows.append({'tree':name,'q':q,'k':k,'permutation':perm,'mode':mode})
 return rows
def produce():
 cases=[]
 for spec in specs():
  t=TREES[spec['tree']];k=spec['k'];q=spec['q'];start=initial(t,k,q,spec['permutation'],spec['mode']);trace=[]
  try:path=normalize(start,t,k,q,trace=trace);failure=None
  except Exception as exc:path=getattr(exc,'path',[]);failure={'type':type(exc).__name__,'message':str(exc),'trace':trace}
  cases.append({'spec':spec,'width':data(t,q)[2][0],'start':start,'path':path,'failure':failure})
 return {'schema':1,'scope':SCOPE,'cases':cases}
