"""Recursive arity2/3 fixed-root repair with exact-interior role transport."""
from itertools import product,combinations
L=();B=(L,L);T=(L,L,L);A=(T,L,L)
TREES={'A':A,'F':(T,T,L),'G':(T,T,T),'H':(A,T,B),'J':((T,L),(L,T),T)}
SCOPE='finite rooted ordered trees with internal arity two or three; higher arity unresolved'
def layout(t):
 nodes=[]
 def walk(t):
  i=len(nodes);nodes.append([]);nodes[i]=[walk(x) for x in t];return i
 walk(t);return nodes
def vertices(nodes,i):
 return [i]+[v for c in nodes[i] for v in vertices(nodes,c)]
def data(t,q):
 nodes=layout(t);internal=[i for i,c in enumerate(nodes) if c]
 if any(len(c) not in (0,2,3) for c in nodes):raise ValueError('scope')
 if len(q)!=len(internal) or any(type(x)!=int or x not in range(1,len(nodes[internal[n]])+1) for n,x in enumerate(q)):raise ValueError('target')
 target=dict(zip(internal,q));w={}
 for i in reversed(range(len(nodes))):
  a=[w[c] for c in nodes[i]]
  w[i]=1 if not a else max(a) if target[i]==1 else sum(a) if target[i]==len(a) else max(max(a),(sum(a)+1)//2)
 return nodes,target,w
def palettes(P,widths,r):
 if r==1:return [P[:w] for w in widths]
 if r==len(widths):
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
 state=[0]*k
 def fill(v,labels):
  for j in labels:state[j]|=1<<v
  if nodes[v]:
   child_palettes=palettes(labels,[w[c] for c in nodes[v]],target[v])
   for c,assigned in zip(nodes[v],child_palettes):fill(c,assigned)
 fill(0,P);return state

def coordinate(state,children):
 # Dynamic program over child-incidence bit covers, separate from verifier subset enumeration.
 full=(1<<len(children))-1;best={0:0}
 for z in state:
  cover=sum(1<<i for i,c in enumerate(children) if z>>c&1)
  for mask,cost in list(best.items()):
   joint=mask|cover;best[joint]=min(best.get(joint,len(children)+1),cost+1)
 return best.get(full,len(children)+1)
def initial(t,k,q,perm,mode):
 nodes,target,w=data(t,q);base=canonical(t,k,q);state=[0]*k
 if perm not in ('identity','reversal','cyclic') or mode not in ('compact','inflated'):raise ValueError('case mode')
 for j,z in enumerate(base):state[j if perm=='identity' else k-1-j if perm=='reversal' else (j+1)%k]=z
 if mode=='inflated':
  parents={c:v for v,cs in enumerate(nodes) for c in cs}
  for v in range(1,len(nodes)):
   for j in range(k):
    if state[j]>>v&1 or not state[j]>>parents[v]&1:continue
    state[j]|=1<<v
    if any(coordinate(state,nodes[u])!=r for u,r in target.items()):state[j]&=~(1<<v)
 return state
def replace_role(current,nodes,child,x,y,path):
 vs=vertices(nodes,child)
 if any(current[y]>>v&1 for v in vs):raise ValueError('role destination occupied')
 used=[v for v in vs if current[x]>>v&1]
 for v in used:current[y]|=1<<v;path.append(current[:])
 for v in reversed(used):current[x]&=~(1<<v);path.append(current[:])
def transport_child(state,t,child,roles,desired,P,trace=None):
 trace=[] if trace is None else trace;nodes=layout(t);current=list(state);path=[current[:]];roles=list(roles)
 try:
  for i,y in enumerate(desired):
   if roles[i]==y:continue
   if y in roles:
    other=roles.index(y);hole=next(j for j in P if j not in roles)
    replace_role(current,nodes,child,roles[other],hole,path);roles[other]=hole
    trace.append({'kind':'local_hole','child':child,'label':hole})
   replace_role(current,nodes,child,roles[i],y,path);roles[i]=y
 except Exception as exc:raise ConstructionFailure(exc,path) from exc
 return path
def _normalize(state,t,k,q,order=None,trace=None,_record=None):
 trace=[] if trace is None else trace;nodes,target,w=data(t,q);P=list(range(k)) if order is None else list(order)
 if len(P)!=k or set(P)!=set(range(k)):raise ValueError('ordered palette')
 current=list(state);path=[] if _record is None else _record;path.append(current[:]);children=nodes[0]
 if not children:return path
 r=target[0];middle=(len(children)==3 and r==2)
 def support(c):return [j for j in P if current[j]>>c&1]
 def change(j,c,add):
  if add:current[j]|=1<<c
  else:current[j]&=~(1<<c)
  path.append(current[:])
 chosen=();anchor=None
 if middle:
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
  if middle and i in chosen and w[c]<k:labels=[anchor]+[j for j in labels if j!=anchor]
  vs=vertices(nodes,c);cq=[target[v] for v in vs if nodes[v]]
  raw=[sum(1<<n for n,v in enumerate(vs) if current[j]>>v&1) for j in labels]
  failure=None
  try:inner=normalize(raw,t[i],len(labels),cq)
  except ConstructionFailure as exc:inner=exc.path;failure=exc
  region=sum(1<<v for v in vs)
  for rawstep in inner[1:]:
   for j in P:current[j]&=~region
   for n,j in enumerate(labels):
    for pos,v in enumerate(vs):
     if rawstep[n]>>pos&1:current[j]|=1<<v
   path.append(current[:])
  if failure is not None:raise failure
  for j in labels[w[c]:]:change(j,c,False)
  roles.append(labels[:w[c]])
  trace.append({'kind':'child_normalization','child':c,'end':len(path)-1})
  if middle and w[c]==k:trace.append({'kind':'whole_palette_child','child':c,'end':len(path)-1})
 targets=palettes(P,[w[c] for c in children],r)
 if middle:
  for i,c in enumerate(children):
   if w[c]==k:continue
   trace.append({'kind':'role_transport','child':c})
   failure=None
   try:transport=transport_child(current,t,c,roles[i],targets[i],P,trace)
   except ConstructionFailure as exc:transport=exc.path;failure=exc
   for nxt in transport[1:]:current[:]=nxt;path.append(current[:])
   if failure is not None:raise failure
  trace.append({'kind':'transport_complete','end':len(path)-1})
 if r==len(children):
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
 def __init__(self,original,path):
  super().__init__(str(original));self.path=path;self.original=getattr(original,'original',original)
 def __str__(self):return super().__str__()
def normalize(state,t,k,q,order=None,trace=None):
 attempted=[]
 try:return _normalize(state,t,k,q,order,trace,attempted)
 except Exception as exc:raise ConstructionFailure(exc,attempted) from exc
def specs():
 rows=[]
 for name,t in TREES.items():
  nodes=layout(t);arities=[len(c) for c in nodes if c]
  for profile in product(*(range(1,d+1) for d in arities)):
   q=list(profile);M=data(t,q)[2][0]
   for k in (M,M+1):
    for perm in ('identity','reversal','cyclic'):
     for mode in ('compact','inflated'):rows.append({'tree':name,'q':q,'k':k,'permutation':perm,'mode':mode})
 return rows
def produce():
 cases=[]
 for spec in specs():
  t=TREES[spec['tree']];k=spec['k'];q=spec['q'];trace=[];start=None;path=[];phase='start'
  try:
   start=initial(t,k,q,spec['permutation'],spec['mode']);phase='normalization'
   path=normalize(start,t,k,q,trace=trace);failure=None
  except Exception as exc:
   original=getattr(exc,'original',exc);path=getattr(exc,'path',[])
   category='construction' if isinstance(original,(ValueError,AssertionError)) else 'incomplete'
   failure={'phase':phase,'type':type(exc).__name__,'original_type':type(original).__name__,'category':category,'message':str(original),'trace':trace}
  cases.append({'spec':spec,'width':data(t,q)[2][0],'start':start,'path':path,'failure':failure})
 return {'schema':1,'scope':SCOPE,'kind':'campaign','cases':cases}
