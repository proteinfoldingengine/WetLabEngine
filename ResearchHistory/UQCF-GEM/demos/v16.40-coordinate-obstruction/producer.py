"""Producer: nested supports, explicit adjacency, BFS paths and partitions."""
from itertools import combinations
from collections import deque
from functools import lru_cache
P=[-1,0,0,1,1,1,2,2,6,6]; K=3; Q=[1,3,2,0,0,0,2,0,0,0]
X=[335,599,167]; Z=[599,335,167]
NAMED=[[335,599,167],[335,855,167],[847,855,167],[591,855,167],[591,343,167],[591,351,167],[607,351,167],[599,351,167],[599,335,167]]

def build(p,k,q,named):
    n=len(p); full=(1<<k)-1; children=[[w for w in range(1,n) if p[w]==v] for v in range(n)]
    states=[]; support=[full]
    def visit(v):
        if v==n:
            states.append(tuple(sum(1<<i for i,s in enumerate(support) if s&(1<<j)) for j in range(k)));return
        sup=support[p[v]]
        for s in range(1,full+1):
            if s&sup==s:support.append(s);visit(v+1);support.pop()
    visit(1); states.sort()
    @lru_cache(None)
    def hit(family):
        if not family:return 0
        return min(s.bit_count() for s in range(1,full+1) if all(s&t for t in family))
    def profile(state):
        sup=[sum(1<<j for j,m in enumerate(state) if m&(1<<v)) for v in range(n)]
        return tuple(hit(tuple(sup[w] for w in ch)) for ch in children)
    profiles={}; unit=[]
    for s in states:
        z=profile(s)
        if sum(abs(a-b) for a,b in zip(q,z))<=1:profiles[s]=z;unit.append(s)
    index={s:i for i,s in enumerate(unit)};adj=[[] for _ in unit];edges=[]
    for i,s in enumerate(unit):
        for label in range(k):
            for v in range(1,n):
                t=list(s);t[label]^=1<<v;j=index.get(tuple(t))
                if j is not None and j>i:edges.append([i,j]);adj[i].append(j);adj[j].append(i)
    for row in adj:row.sort()
    edges.sort()
    def partition(allowed):
        unseen=set(allowed);parts=[]
        while unseen:
            seed=min(unseen);unseen.remove(seed);queue=[seed];part=[]
            for u in queue:
                part.append(u)
                for v in adj[u]:
                    if v in unseen:unseen.remove(v);queue.append(v)
            parts.append(sorted(part))
        return parts
    exact=[i for i,s in enumerate(unit) if list(profiles[s])==q]
    static=[[i for i,s in enumerate(unit) if all(profiles[s][w]==q[w] for w in range(n) if w!=v)] for v in range(n)]
    parts={'zero':partition(exact),'unit':partition(range(len(unit))),'static':[partition(a) for a in static]}
    maps=[{i:j for j,c in enumerate(part) for i in c} for part in [parts['unit']]+parts['static']]
    bfs={}
    def path(src,dst,which):
        key=(src,which)
        if key not in bfs:
            allowed=set(range(len(unit))) if which==0 else set(static[which-1]);prev={src:None};queue=deque([src])
            while queue:
                u=queue.popleft()
                for v in adj[u]:
                    if v in allowed and v not in prev:prev[v]=u;queue.append(v)
            bfs[key]=prev
        prev=bfs[key]
        if dst not in prev:return None
        walk=[dst]
        while walk[-1]!=src:walk.append(prev[walk[-1]])
        return walk[::-1]
    active={v for v,a in enumerate(q) if a>=2}; hull={0}
    for v in active:
        while v>=0:hull.add(v);v=p[v]
    critical=[v for v in hull if v and p[v] in active]
    def descendant(a,b):
        while b>=0:
            if a==b:return True
            b=p[b]
        return False
    sc=all(any(q[w]==k and k>=2 and descendant(v,w) for w in range(n)) for v in critical)
    def endpoint_full(a,b):return all(all(m&(1<<v) for m in unit[a]) and all(m&(1<<v) for m in unit[b]) for v in critical)
    pairs=[]
    for a,b in combinations(range(len(parts['zero'])),2):
        x,y=parts['zero'][a][0],parts['zero'][b][0];paths={};cuts={}
        for w in range(n+1):
            walk=path(x,y,w)
            if walk is not None:paths[str(w)]=walk
            else:cuts[str(w)]=[maps[w][x],maps[w][y]]
        connected='0' in paths
        pairs.append({'components':[a,b],'endpoints':[x,y],'paths':paths,'cuts':cuts,'SC':sc,'endpoint_full':endpoint_full(x,y),'primary':[1,1,1] if connected else None,'LEX':[1,1,1] if connected else None,'classification':'static_sufficient' if any(str(w) in paths for w in range(1,n+1)) else ('moving_required' if connected else 'unit_disconnected')})
    return {'schema':1,'domain':{'parents':p,'k':k,'q0':q},'admitted':[list(s) for s in states],'unit':[list(s) for s in unit],'unit_edges':edges,'partitions':parts,'pairs':pairs,'named_path':named}

def produce():return build(P,K,Q,NAMED)
