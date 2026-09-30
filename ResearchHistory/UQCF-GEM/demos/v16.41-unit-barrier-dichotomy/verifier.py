"""Independent increasing-parent trees, prefix-view states, subset covers and UF."""
from itertools import product,combinations
from functools import lru_cache,reduce
from collections import defaultdict
from math import factorial

def require(ok,message):
    if not ok:raise ValueError(message)

def tree_codes(leaves):
    out=set()
    for n in range(leaves+1,2*leaves):
        for tail in product(*(range(v) for v in range(1,n))):
            p=(-1,)+tail;ch=[[v for v in range(1,n) if p[v]==u] for u in range(n)]
            if sum(not c for c in ch)!=leaves or any(len(c)==1 for c in ch):continue
            def code(v):return '('+''.join(sorted(code(w) for w in ch[v]))+')'
            out.add(code(0))
    return sorted(out)

def decode(code):
    p=[]
    def subtree(i,parent):
        require(code[i]=='(','tree syntax');v=len(p);p.append(parent);i+=1
        while code[i]=='(':i=subtree(i,v)
        require(code[i]==')','tree syntax');return i+1
    require(subtree(0,-1)==len(code),'tree suffix');return p

def partition(allowed,adj):
    allowed=set(allowed);parent={v:v for v in allowed}
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    for x in sorted(allowed):
        for y in adj[x]:
            if y>x and y in allowed:
                a,b=find(x),find(y)
                if a!=b:parent[max(a,b)]=min(a,b)
    groups=defaultdict(list)
    for v in sorted(allowed):groups[find(v)].append(v)
    return sorted(groups.values(),key=lambda row:row[0])

def valid_walk(path,x,y,allowed,adj):
    return isinstance(path,list) and bool(path) and path[0]==x and path[-1]==y and all(type(v) is int and v in allowed for v in path) and all(b in adj[a] for a,b in zip(path,path[1:]))

def check_connection(pair,x,y,q,profiles,adj,mapping,allowed):
    """Same path/cut gate used by retained science and explicitly abstract controls."""
    nonunit=mapping[x]!=mapping[y]
    if not nonunit:
        require(valid_walk(pair['unit_path'],x,y,allowed,adj),'invalid unit path')
        require(pair['unit_cut'] is None and pair['unrestricted_path'] is None,'false unit cut')
        bounds={'B1':[1,1],'Binf':[1,1],'Bs':[1,1]};lex=[1,1,1]
    else:
        require(pair['unit_path'] is None and pair['unit_cut']==[mapping[x],mapping[y]],'missing/false complete cut')
        require(valid_walk(pair['unrestricted_path'],x,y,set(range(len(profiles))),adj),'invalid unrestricted path')
        costs=[[abs(a-b) for a,b in zip(q,profiles[i])] for i in pair['unrestricted_path']]
        bounds={'B1':[2,max(map(sum,costs))],'Binf':[1,max(max(c) for c in costs)],'Bs':[1,max(sum(v!=0 for v in c) for c in costs)]};lex=None
        require(bounds['B1'][1]>=2,'contradictory nonunit witness')
    require(pair['primary_bounds']==bounds and pair['LEX']==lex,'independent objectives')
    return nonunit

def verify_graph(g,k,selected=None):
    require(set(g)=={'code','parents','k','states','forward_moves','profile_ids','attained_profiles','profiles'},'graph membership')
    p=decode(g['code']);n=len(p);require(g['parents']==p and g['k']==k,'tree/domain')
    ch=[sum(1<<w for w in range(1,n) if p[w]==v) for v in range(n)];degrees=[c.bit_count() for c in ch]
    views=[m for m in range(1,1<<n,2) if all(not(m>>v&1) or m>>p[v]&1 for v in range(1,n))]
    states=[s for s in product(views,repeat=k) if reduce(int.__or__,s)==(1<<n)-1]
    require(g['states']==[list(s) for s in states],'complete admitted identities')
    @lru_cache(None)
    def cover(children,projections):
        if not children:return 0
        for size in range(1,k+1):
            for labels in combinations(range(k),size):
                if reduce(int.__or__,(projections[j] for j in labels))==children:return size
        raise ValueError('uncovered children')
    profiles=[tuple(cover(c,tuple(m&c for m in s)) for c in ch) for s in states];qs=sorted(set(profiles));qmap={q:i for i,q in enumerate(qs)}
    require(g['profile_ids']==[qmap[q] for q in profiles],'profile assignment')
    require(g['attained_profiles']==[list(q) for q in qs],'complete attained profile identities')
    tested=qs if selected is None else [tuple(selected)]
    require(all(q in qs for q in tested),'target profile attained')
    require([r['q'] for r in g['profiles']]==[list(q) for q in tested],'complete tested profiles')
    moves=[0]*len(states);adj=[[] for _ in states]
    for label in range(k):
        groups=defaultdict(list)
        for i,s in enumerate(states):groups[s[:label]+s[label+1:]].append((s[label],i))
        for group in groups.values():
            for (a,i),(b,j) in combinations(group,2):
                diff=a^b
                if diff>1 and diff&(diff-1)==0:
                    lo,hi=(i,j) if a<b else (j,i);v=diff.bit_length()-1
                    moves[lo]|=1<<(label*(n-1)+v-1);adj[i].append(j);adj[j].append(i)
    require(g['forward_moves']==moves,'complete primitive edges')
    for row in adj:row.sort()
    totals={'profiles':len(tested),'states':len(states),'edges':sum(m.bit_count() for m in moves),'components':0,'target_states':0,'pairs':0,'nonunit_pairs':0,'partition_pairs':0,'overlap_pairs':0,'adjacent_active_pairs':0,'construction_paths':0};all_nodes=set(range(len(states)))
    for rec,q in zip(g['profiles'],tested):
        require(set(rec)=={'q','partition_profile','adjacent_active','zero_components','unit_components','pairs'},'profile record membership')
        packed=list(q)==degrees;active=any(q[v]>=2 and q[p[v]]>=2 for v in range(1,n))
        require(type(rec['partition_profile']) is bool and type(rec['adjacent_active']) is bool and rec['partition_profile']==packed and rec['adjacent_active']==active,'profile classification')
        zero_nodes=[i for i,z in enumerate(profiles) if z==q]
        close={z for z in qs if sum(abs(a-b) for a,b in zip(q,z))<=1};allowed={i for i,z in enumerate(profiles) if z in close}
        zero=partition(zero_nodes,adj);unit=partition(allowed,adj);mapping={v:c for c,row in enumerate(unit) for v in row}
        require(rec['zero_components']==zero and rec['unit_components']==unit,'complete threshold partitions')
        if packed:
            require(len(zero_nodes)==factorial(k) and all(len(c)==1 for c in zero),'partition characterization')
            leaves=[v for v,d in enumerate(degrees) if d==0]
            descendants=[{i} for i in range(n)]
            for v in range(n-1,0,-1):descendants[p[v]]|=descendants[v]
            for i in zero_nodes:
                labels=[sum(1<<j for j,m in enumerate(states[i]) if m>>v&1) for v in leaves]
                require(all(s.bit_count()==1 for s in labels) and len(set(labels))==k,'leaf bijection')
                for v in range(n):
                    actual=sum(1<<j for j,m in enumerate(states[i]) if m>>v&1)
                    expected=reduce(int.__or__,(s for l,s in zip(leaves,labels) if l in descendants[v]),0)
                    require(actual==expected,'descendant partition support')
        wanted=list(combinations(range(len(zero)),2));require(len(rec['pairs'])==len(wanted),'complete pair count')
        totals['components']+=len(zero);totals['target_states']+=len(zero_nodes);totals['pairs']+=len(wanted)
        totals['partition_pairs' if packed else 'overlap_pairs']+=len(wanted)
        if active:totals['adjacent_active_pairs']+=len(wanted)
        for pair,(a,b) in zip(rec['pairs'],wanted):
            require(set(pair)=={'components','endpoints','unit_path','unit_cut','unrestricted_path','primary_bounds','LEX','construction'},'pair membership')
            x,y=zero[a][0],zero[b][0];require(pair['components']==[a,b] and pair['endpoints']==[x,y],'canonical pair identities')
            totals['nonunit_pairs']+=check_connection(pair,x,y,q,profiles,adj,mapping,allowed)
            if packed:
                require(valid_walk(pair['construction'],x,y,allowed,adj),'CONSTRUCTION_REFUTED');totals['construction_paths']+=1
            else:require(pair['construction'] is None,'unsupported construction claim')
    return dict(totals,code=g['code'],vertices=n)

def summarize(graphs):
    keys=['profiles','states','edges','components','target_states','pairs','nonunit_pairs','partition_pairs','overlap_pairs','adjacent_active_pairs','construction_paths'];totals={key:sum(g[key] for g in graphs) for key in keys}
    outcome='NONUNIT_WITNESS' if totals['nonunit_pairs'] else ('PARTITION_THEOREM_VALIDATED_BOUNDED_REMAINDER_UNIT' if totals['overlap_pairs'] else 'PARTITION_THEOREM_ONLY_NO_NONPARTITION_TEST')
    return {'status':'VERIFIED','outcome':outcome,'graphs':len(graphs),'totals':totals,'per_graph':graphs,'partition_theorem_scope':'all finite rooted no-unary trees with k=leaves and q=outdegree; see reviewed proof','universal_unit_barrier':'REFUTED_BY_NONUNIT_WITNESS' if totals['nonunit_pairs'] else 'UNRESOLVED','intrinsic_indecomposability':'NOT_CLAIMED'}

def verify(doc,leaves=4,k=4):
    directed=leaves==4 and k==4
    require(set(doc)=={'schema','domain','graphs','overlap'},'document membership');require(doc['schema']==1 and doc['domain']=={'leaves':leaves,'labels':k,'no_unary':True,'directed_overlap':directed},'frozen domain')
    require([g['code'] for g in doc['graphs']]==tree_codes(leaves),'complete canonical trees')
    records=[dict(verify_graph(g,k),campaign_role='canonical_core') for g in doc['graphs']]
    if directed:
        require(doc['overlap']['parents']==[-1,0,1,2,2,2,1,0],'directed overlap tree')
        records.append(dict(verify_graph(doc['overlap'],k,[2,2,2,0,0,0,0,0]),campaign_role='directed_overlap'))
    else:require(doc['overlap'] is None,'unexpected directed graph')
    return summarize(records)
