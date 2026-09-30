"""Complete core graphs from recursively assembled trees and nested supports."""
from itertools import combinations
from functools import lru_cache
from collections import deque

@lru_cache(None)
def codes(leaves):
    if leaves==1:return ('()',)
    choices=sorted((s,l) for l in range(1,leaves) for s in codes(l));out=set()
    def assemble(left,start,children):
        if left==0:
            if len(children)>=2:out.add('('+''.join(children)+')')
            return
        for i in range(start,len(choices)):
            s,l=choices[i]
            if l<=left:assemble(left-l,i,children+[s])
    assemble(leaves,0,[]);return tuple(sorted(out))

def parents(code):
    p=[];stack=[]
    for c in code:
        if c=='(':p.append(stack[-1] if stack else -1);stack.append(len(p)-1)
        else:stack.pop()
    return p

def proof_path(p,x,y):
    state=list(x);path=[list(state)];leaves=[v for v in range(len(p)) if v not in p[1:]]
    def label(v,s):return next(j for j,m in enumerate(s) if m>>v&1)
    def chain(v):
        row=[]
        while v>=0:row.append(v);v=p[v]
        return row
    for xleaf in leaves:
        target=label(xleaf,y)
        if label(xleaf,state)==target:continue
        yleaf=next(v for v in leaves if label(v,state)==target)
        a,b=label(xleaf,state),target;cx,cy=chain(xleaf),chain(yleaf);lca=next(v for v in cx if v in cy)
        px=list(reversed(cx[:cx.index(lca)]));py=list(reversed(cy[:cy.index(lca)]))
        for lab,vertices,add in [(a,py,True),(b,px,True),(a,list(reversed(px)),False),(b,list(reversed(py)),False)]:
            for v in vertices:
                if add:state[lab]|=1<<v
                else:state[lab]&=~(1<<v)
                path.append(list(state))
    if state!=list(y):raise ValueError('constructive endpoint')
    return path

def build(code,k,selected=None):
    p=parents(code);n=len(p);full=(1<<k)-1;children=[[w for w in range(1,n) if p[w]==v] for v in range(n)]
    states=[];supports=[full]
    def visit(v):
        if v==n:
            states.append(tuple(sum(1<<w for w,s in enumerate(supports) if s>>j&1) for j in range(k)));return
        for s in range(1,full+1):
            if s&supports[p[v]]==s:supports.append(s);visit(v+1);supports.pop()
    visit(1);states.sort();index={s:i for i,s in enumerate(states)}
    @lru_cache(None)
    def hit(family):
        if not family:return 0
        return min(s.bit_count() for s in range(1,full+1) if all(s&t for t in family))
    profiles=[]
    for state in states:
        sup=[sum(1<<j for j,m in enumerate(state) if m>>v&1) for v in range(n)]
        profiles.append(tuple(hit(tuple(sup[w] for w in ch)) for ch in children))
    qs=sorted(set(profiles));qindex={q:i for i,q in enumerate(qs)};profile_ids=[qindex[q] for q in profiles]
    moves=[];adj=[[] for _ in states]
    for i,s in enumerate(states):
        bits=0
        for label in range(k):
            for v in range(1,n):
                if s[label]>>v&1:continue
                t=list(s);t[label]|=1<<v;j=index.get(tuple(t))
                if j is not None:bits|=1<<(label*(n-1)+v-1);adj[i].append(j);adj[j].append(i)
        moves.append(bits)
    for row in adj:row.sort()
    def components(allowed):
        unseen=set(allowed);out=[]
        while unseen:
            seed=min(unseen);unseen.remove(seed);queue=[seed]
            for a in queue:
                for b in adj[a]:
                    if b in unseen:unseen.remove(b);queue.append(b)
            out.append(sorted(queue))
        return out
    def expansion(s):
        s=list(s);path=[tuple(s)]
        for v in range(1,n):
            for lab in range(k):
                if not s[lab]>>v&1:s[lab]|=1<<v;path.append(tuple(s))
        return path
    records=[]
    for qi,q in enumerate(qs):
        if selected is not None and list(q)!=selected:continue
        eligible={j for j,z in enumerate(qs) if sum(abs(a-b) for a,b in zip(q,z))<=1}
        exact=[i for i,z in enumerate(profile_ids) if z==qi];allowed={i for i,z in enumerate(profile_ids) if z in eligible}
        zero=components(exact);unit=components(allowed);groups={v:c for c,row in enumerate(unit) for v in row};pairs=[]
        packed=list(q)==[len(c) for c in children];previous_source=None;prev=None
        for a,b in combinations(range(len(zero)),2):
            x,y=zero[a][0],zero[b][0];connected=groups[x]==groups[y];walk=None;cut=None;unrestricted=None
            if connected:
                if previous_source!=x:
                    prev={x:None};queue=deque([x])
                    while queue:
                        u=queue.popleft()
                        for v in adj[u]:
                            if v in allowed and v not in prev:prev[v]=u;queue.append(v)
                    previous_source=x
                walk=[y]
                while walk[-1]!=x:walk.append(prev[walk[-1]])
                walk.reverse();bounds={'B1':[1,1],'Binf':[1,1],'Bs':[1,1]};lex=[1,1,1]
            else:
                cut=[groups[x],groups[y]];raw=expansion(states[x])[:-1]+list(reversed(expansion(states[y])));unrestricted=[index[s] for s in raw]
                costs=[[abs(u-v) for u,v in zip(q,profiles[i])] for i in unrestricted]
                bounds={'B1':[2,max(map(sum,costs))],'Binf':[1,max(max(c) for c in costs)],'Bs':[1,max(sum(v!=0 for v in c) for c in costs)]};lex=None
            constructive=[index[tuple(s)] for s in proof_path(p,states[x],states[y])] if packed else None
            pairs.append({'components':[a,b],'endpoints':[x,y],'unit_path':walk,'unit_cut':cut,'unrestricted_path':unrestricted,'primary_bounds':bounds,'LEX':lex,'construction':constructive})
        records.append({'q':list(q),'partition_profile':packed,'adjacent_active':any(q[v]>=2 and q[p[v]]>=2 for v in range(1,n)),'zero_components':zero,'unit_components':unit,'pairs':pairs})
    return {'code':code,'parents':p,'k':k,'states':[list(s) for s in states],'forward_moves':moves,'profile_ids':profile_ids,'attained_profiles':[list(q) for q in qs],'profiles':records}

OVERLAP_CODE='('+'('+'('+'()'*3+')'+'()'+')'+'()'+')'
OVERLAP_Q=[2,2,2,0,0,0,0,0]
def produce(leaves=4,k=4):
    directed=leaves==4 and k==4
    return {'schema':1,'domain':{'leaves':leaves,'labels':k,'no_unary':True,'directed_overlap':directed},'graphs':[build(c,k) for c in codes(leaves)],'overlap':build(OVERLAP_CODE,k,OVERLAP_Q) if directed else None}

