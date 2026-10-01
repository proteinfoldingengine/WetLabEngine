"""Native recursive arity2/3/4 repair, with guarded four-child root paths."""
from itertools import combinations,product,permutations
import feasibility

def layout(t):
    nodes=[]
    def walk(t):
        if len(t) not in (0,2,3,4):raise ValueError('scope')
        i=len(nodes);nodes.append([]);nodes[i]=[walk(c) for c in t];return i
    walk(t);return nodes
def vertices(nodes,i):return [i]+[v for c in nodes[i] for v in vertices(nodes,c)]
def data(t,q):
    nodes=layout(t);internal=[i for i,c in enumerate(nodes) if c]
    if len(q)!=len(internal) or any(type(r)!=int or r not in range(1,len(nodes[v])+1) for v,r in zip(internal,q)):raise ValueError('target')
    targets=dict(zip(internal,q));width={}
    for v in reversed(range(len(nodes))):
        sizes=tuple(width[c] for c in nodes[v])
        if not sizes:width[v]=1
        elif len(sizes)==4:width[v]=feasibility.minimum(sizes,targets[v])[0]
        elif targets[v]==1:width[v]=max(sizes)
        elif targets[v]==len(sizes):width[v]=sum(sizes)
        else:width[v]=max(max(sizes),(sum(sizes)+1)//2)
    return nodes,targets,width
def coordinate(state,children):
    full=(1<<len(children))-1;best={0:0}
    for z in state:
        mask=sum(1<<i for i,c in enumerate(children) if z&(1<<c))
        for old,cost in list(best.items()):
            joint=old|mask;best[joint]=min(best.get(joint,len(children)+1),cost+1)
    return best.get(full,len(children)+1)
class ConstructionFailure(Exception):
    def __init__(self,original,path):
        super().__init__(str(original));self.original=getattr(original,'original',original);self.path=[s[:] for s in path]
        self.category='construction' if isinstance(self.original,(ValueError,AssertionError)) else 'incomplete'
def clear_role(state,nodes,child,x,y,path):
    proper=vertices(nodes,child)[1:]
    if x==y or not state[x]&(1<<child) or not state[y]&(1<<child):raise ValueError('clearance root boundary')
    if any(state[y]&(1<<v) for v in proper):raise ValueError('destination used in proper descendants')
    used=[v for v in proper if state[x]&(1<<v)]
    for v in used:state[y]|=1<<v;path.append(state[:])
    for v in reversed(used):state[x]&=~(1<<v);path.append(state[:])
def lift_root_path(state,tree,q,root_path,order,trace):
    current=list(state);path=[current[:]]
    try:
        nodes,targets,width=data(tree,q);children=nodes[0];order=list(order)
        if len(children)!=4 or set(order)!=set(range(len(state))) or len(order)!=len(state):raise ValueError('lift dimensions')
        def roots():return [{j for j in order if current[j]&(1<<c)} for c in children]
        if not root_path or [set(A) for A in root_path[0]]!=roots():raise ValueError('root path start')
        for step in root_path[1:]:
            before=roots();after=[set(A) for A in step]
            if len(after)!=4 or any(not A<=set(order) for A in after):raise ValueError('root step domain')
            edits=[(i,j,j in after[i]) for i in range(4) for j in order if (j in before[i])!=(j in after[i])]
            if len(edits)!=1:raise ValueError('root step not primitive')
            i,x,add=edits[0];child=children[i]
            if any(len(A)<width[c] for A,c in zip(after,children)):raise ValueError('root deletion below minimum')
            if not add:
                proper=vertices(nodes,child)[1:]
                used={j for j in order if any(current[j]&(1<<v) for v in proper)}
                if proper and len(used)!=width[child]:raise ValueError('proper union not compact')
                if x in used:
                    y=next(j for j in order if j in before[i] and j not in used)
                    clear_role(current,nodes,child,x,y,path)
                    trace.append({'kind':'fixed_root_clearance','child':child,'x':x,'y':y})
                current[x]&=~(1<<child)
            else:current[x]|=1<<child
            path.append(current[:])
            if abs(coordinate(current,children)-targets[0])>1:raise ValueError('unguarded root path')
            if any(coordinate(current,nodes[v])!=r for v,r in targets.items() if v):raise ValueError('inexact interior lift')
    except Exception as exc:raise ConstructionFailure(exc,path) from exc
    return path

def palettes(P,widths,r):
 if len(widths)==4:
  _,roots=feasibility.minimum(tuple(widths),r)
  return [[P[j] for j in A] for A in roots]
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
 r=target[0]
 if len(children)==4 and r<4:return normalize_four(current,t,k,q,P,trace,path)
 middle=(len(children)==3 and r==2)
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
  try:
   require_exact_parent(current,nodes,r)
   trace.append({'kind':'recursive_call','child':c,'parent_exact':True})
   inner=normalize(raw,t[i],len(labels),cq)
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

def normalize(state,t,k,q,order=None,trace=None):
 attempted=[]
 try:return _normalize(state,t,k,q,order,trace,attempted)
 except Exception as exc:raise ConstructionFailure(exc,attempted) from exc

def require_exact_parent(state,nodes,q):
    if coordinate(state,nodes[0])!=q:raise ValueError('recursive call requires exact parent')

def normalize_four(current,t,k,q,P,trace,path):
    import cover
    nodes,targets,width=data(t,q);children=nodes[0];r=targets[0]
    def supports():return [{j for j in P if current[j]&(1<<c)} for c in children]
    def child_call(i):
        c=children[i];require_exact_parent(current,nodes,r)
        trace.append({'kind':'recursive_call','child':c,'parent_exact':True})
        labels=[j for j in P if current[j]&(1<<c)];vs=vertices(nodes,c)
        childq=[targets[v] for v in vs if nodes[v]]
        raw=[sum(1<<pos for pos,v in enumerate(vs) if current[j]&(1<<v)) for j in labels]
        failure=None
        try:inner=normalize(raw,t[i],len(labels),childq)
        except ConstructionFailure as exc:inner=exc.path;failure=exc
        region=sum(1<<v for v in vs)
        for step in inner[1:]:
            for j in P:current[j]&=~region
            for n,j in enumerate(labels):
                for pos,v in enumerate(vs):
                    if step[n]&(1<<pos):current[j]|=1<<v
            path.append(current[:])
        if failure is not None:raise failure
    for i in range(4):child_call(i)
    start=supports();target=[set(A) for A in palettes(P,[width[c] for c in children],r)]
    if r in (1,2):
        roots=[set(A) for A in start];root_path=[[set(A) for A in roots]]
        for i in range(4):
            for j in P:
                if j not in roots[i]:roots[i].add(j);root_path.append([set(A) for A in roots])
        for i in range(4):
            for j in P:
                if j not in target[i]:roots[i].remove(j);root_path.append([set(A) for A in roots])
        trace.append({'kind':'four_root_expand_contract','target':r})
    else:
        full=set(P);caps=[k-width[c] for c in children]
        complements=cover.reconfigure([full-A for A in start],[full-A for A in target],caps,P)
        root_path=[[full-B for B in step] for step in complements]
        trace.append({'kind':'four_root_cover','capacities':caps})
    failure=None
    try:lifted=lift_root_path(current,t,q,root_path,P,trace)
    except ConstructionFailure as exc:lifted=exc.path;failure=exc
    for step in lifted[1:]:current[:]=step;path.append(current[:])
    if failure is not None:raise failure
    for i in range(4):child_call(i)
    return path
