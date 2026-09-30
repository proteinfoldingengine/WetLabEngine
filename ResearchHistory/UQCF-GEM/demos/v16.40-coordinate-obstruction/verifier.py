"""Independent prefix-view enumeration, subset covers and union-find cuts.
No producer imports or cached verification outcomes.
"""
from itertools import product, combinations
from functools import lru_cache
from collections import Counter,defaultdict
DOMAIN={'parents':[-1,0,0,1,1,1,2,2,6,6],'k':3,'q0':[1,3,2,0,0,0,2,0,0,0]}
NAMED=[[335,599,167],[335,855,167],[847,855,167],[591,855,167],[591,343,167],[591,351,167],[607,351,167],[599,351,167],[599,335,167]]

def require(ok,what):
    if not ok:raise ValueError(what)

def verify(doc,domain=None,named=None):
    domain=DOMAIN if domain is None else domain; named=NAMED if named is None else named
    require(set(doc)=={'schema','domain','admitted','unit','unit_edges','partitions','pairs','named_path'},'document membership')
    require(doc['schema']==1 and doc['domain']==domain,'frozen domain')
    p=domain['parents'];k=domain['k'];q=domain['q0'];n=len(p);total=(1<<n)-1
    views=[m for m in range(1,1<<n,2) if all(not(m>>v&1) or m>>p[v]&1 for v in range(1,n))]
    states=[s for s in product(views,repeat=k) if __import__('functools').reduce(int.__or__,s)==total]
    require(doc['admitted']==[list(s) for s in states],'complete admitted identities')
    child_masks=[sum(1<<v for v in range(1,n) if p[v]==u) for u in range(n)]
    @lru_cache(None)
    def cover(ch,projections):
        if ch==0:return 0
        for size in range(1,k+1):
            for labels in combinations(range(k),size):
                union=0
                for label in labels:union|=projections[label]
                if union==ch:return size
        raise ValueError('uncovered child')
    def profile(s):return [cover(ch,tuple(m&ch for m in s)) for ch in child_masks]
    nodes=[];zlist=[]
    for s in states:
        z=profile(s)
        if sum(abs(a-b) for a,b in zip(q,z))<=1:nodes.append(s);zlist.append(z)
    require(doc['unit']==[list(s) for s in nodes],'complete unit identities')
    edges=set()
    for label in range(k):
        groups=defaultdict(list)
        for i,s in enumerate(nodes):groups[s[:label]+s[label+1:]].append((s[label],i))
        for group in groups.values():
            for (a,i),(b,j) in combinations(group,2):
                diff=a^b
                if diff>1 and diff&(diff-1)==0:edges.add((min(i,j),max(i,j)))
    require(doc['unit_edges']==[list(e) for e in sorted(edges)],'complete primitive unit edges')
    def components(allowed):
        allowed=set(allowed);parent={i:i for i in allowed}
        def root(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for a,b in sorted(edges):
            if a in allowed and b in allowed:
                x,y=root(a),root(b)
                if x!=y:parent[max(x,y)]=min(x,y)
        groups=defaultdict(list)
        for i in sorted(allowed):groups[root(i)].append(i)
        return sorted(groups.values(),key=lambda c:c[0])
    exact=[i for i,z in enumerate(zlist) if z==q]
    statics=[[i for i,z in enumerate(zlist) if all(z[w]==q[w] for w in range(n) if w!=v)] for v in range(n)]
    parts={'zero':components(exact),'unit':components(range(len(nodes))),'static':[components(s) for s in statics]}
    require(doc['partitions']==parts,'complete cut partitions')
    maps=[{i:j for j,c in enumerate(part) for i in c} for part in [parts['unit']]+parts['static']]
    allowed=[set(range(len(nodes)))]+list(map(set,statics))
    desc=[{i} for i in range(n)]
    for v in range(n-1,0,-1):desc[p[v]]|=desc[v]
    active={v for v in range(n) if q[v]>=2};hull={v for v in range(n) if desc[v]&active}|{0}
    critical=[v for v in sorted(hull) if v and p[v] in active]
    sc=all(any(q[w]==k and k>=2 for w in desc[v]) for v in critical)
    def walk_valid(walk,a,b,w):
        return (isinstance(walk,list) and bool(walk) and walk[0]==a and walk[-1]==b and all(type(i) is int and i in allowed[w] for i in walk) and all((min(u,v),max(u,v)) in edges for u,v in zip(walk,walk[1:])))
    expected_pairs=list(combinations(range(len(parts['zero'])),2));require(len(doc['pairs'])==len(expected_pairs),'pair count')
    classifications=Counter();pairmap={}
    for rec,(a,b) in zip(doc['pairs'],expected_pairs):
        x,y=parts['zero'][a][0],parts['zero'][b][0]
        require(set(rec)=={'components','endpoints','paths','cuts','SC','endpoint_full','primary','LEX','classification'},'pair membership')
        require(rec['components']==[a,b] and rec['endpoints']==[x,y],'complete canonical pair identities')
        successful=[w for w in range(n+1) if maps[w][x]==maps[w][y]]
        require(set(rec['paths'])==set(map(str,successful)),'complete successful coordinates')
        require(set(rec['cuts'])==set(map(str,set(range(n+1))-set(successful))),'complete failed coordinates')
        for w in successful:require(walk_valid(rec['paths'][str(w)],x,y,w),'invalid attaining path')
        for w in set(range(n+1))-set(successful):require(rec['cuts'][str(w)]==[maps[w][x],maps[w][y]],'false cut reference')
        ef=all(all(m>>v&1 for m in nodes[x]+nodes[y]) for v in critical)
        require(type(rec['SC']) is bool and type(rec['endpoint_full']) is bool and rec['SC']==sc and rec['endpoint_full']==ef,'structural classification')
        barriers=[1,1,1] if 0 in successful else None
        require(rec['primary']==barriers and rec['LEX']==barriers,'independent scalar or LEX bounds')
        cls='static_sufficient' if any(w>0 for w in successful) else ('moving_required' if 0 in successful else 'unit_disconnected')
        require(rec['classification']==cls,'pair classification');classifications[cls]+=1;pairmap[(x,y)]=rec
    require(doc['named_path']==named,'frozen named candidate')
    index={s:i for i,s in enumerate(nodes)};ids=[index.get(tuple(s),-1) for s in named]
    require(ids[0] in exact and ids[-1] in exact,'named endpoint admission/profile')
    pair=pairmap.get(tuple(sorted([ids[0],ids[-1]])))
    require(pair is not None,'named distinct canonical components')
    candidate_valid=walk_valid(ids,ids[0],ids[-1],0)
    if any(int(w)>0 for w in pair['paths']):outcome='FIXED_COORDINATE_COUNTERPATH_FOUND'
    elif '0' in pair['paths'] and not pair['SC'] and not pair['endpoint_full']:outcome='MOVING_LOCATION_WITNESS_VALIDATED'
    elif '0' not in pair['paths']:outcome='UNIT_PATH_NOT_FOUND'
    else:outcome='INCOMPLETE'
    deviations=sorted({v for s in named for v,(a,b) in enumerate(zip(q,profile(s))) if a!=b}) if candidate_valid else None
    distance=sum((a^b).bit_count() for a,b in zip(named[0],named[-1]))
    return {'status':'VERIFIED','scope':'one fixed tree, k and q profile; complete admitted states and target component pairs','admitted_states':len(states),'prefix_views':len(views),'unit_states':len(nodes),'unit_edges':len(edges),'target_states':len(exact),'target_components':len(parts['zero']),'pairs':len(expected_pairs),'classifications':dict(sorted(classifications.items())),'SC_pairs':sum(r['SC'] for r in doc['pairs']),'endpoint_full_pairs':sum(r['endpoint_full'] for r in doc['pairs']),'outcome':outcome,'named':{'candidate_valid':candidate_valid,'moves':len(named)-1,'incidence_hamming':distance,'shortest_if_valid':candidate_valid and len(named)-1==distance,'deviation_coordinates':deviations,'static_success_coordinates':[int(w)-1 for w in pair['paths'] if int(w)>0],'primary':pair['primary'],'LEX':pair['LEX']},'universal_unit_barrier':'UNRESOLVED','indecomposable_fixed_coordinate':'UNRESOLVED'}
