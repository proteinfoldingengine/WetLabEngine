"""Fixed-root four-child primitives. Recursive joining is added after its RED."""
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
