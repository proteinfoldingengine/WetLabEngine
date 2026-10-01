"""Independent support-set verifier; no producer imports or shared enumeration."""
from itertools import combinations,product,permutations
from functools import lru_cache
from coverage import verify_identities
L=();B=(L,L);T=(L,L,L);Q=(L,L,L,L)
TEMPLATES={'C':((B,L,L,L),((2,2),(3,2))), 'Z':((T,L,L,L),((3,3),)),
           'D':((B,B,B,L),((3,2,2,2),)), 'E':((Q,L),((2,2),(2,3))),
           'G':((Q,L,L,L),((2,3),(3,3)))}
class InterfaceNotPreserved(ValueError):pass
def frozen(t):return tuple(frozen(c) for c in t)
def topology(tree):
    children={};parent={};internal=[]
    def visit(t):
        if not isinstance(t,(tuple,list)) or len(t) not in (0,2,3,4):raise ValueError('tree scope')
        v=len(children);children[v]=[]
        if t:
            internal.append(v)
            for branch in t:
                c=visit(branch);children[v].append(c);parent[c]=v
        return v
    visit(tree);return children,parent,internal
def hitting(supports):
    if not supports or any(not s for s in supports):raise ValueError('empty child support')
    labels=sorted(set().union(*supports))
    for size in range(1,len(supports)+1):
        for choice in combinations(labels,size):
            if all(set(choice)&s for s in supports):return size
    raise ValueError('uncovered root')
@lru_cache(None)
def canonical_roots(widths,q,k):
    # Fixed-cardinality combinations are precisely the 1-before-0 bit order.
    if k<max(widths) or q not in range(1,len(widths)+1):return None
    for row in product(*(tuple(combinations(range(k),w)) for w in widths)):
        if hitting([set(s) for s in row])==q:return row
    return None
def root_feasible(widths,q,k):return canonical_roots(tuple(widths),q,k) is not None
@lru_cache(None)
def allocated_feasible(widths,q,k):
    # Recursive width cross-check: enumerate incidence allocations, with label
    # witnesses and exhaustive hitting tests, not producer bit-cover dynamics.
    if k<max(widths):return False
    d=len(widths);types=[tuple(i for i in range(d) if mask&(1<<i)) for mask in range(1,1<<d)]
    def allocate(pos,remaining,slots,columns):
        if not any(remaining):
            supports=[{j for j,C in enumerate(columns) if i in C} for i in range(d)]
            return hitting(supports)==q
        if pos==len(types) or slots==0:return False
        C=types[pos]
        for n in range(min(slots,*(remaining[i] for i in C))+1):
            left=tuple(x-n if i in C else x for i,x in enumerate(remaining))
            if max(left,default=0)>slots-n:continue
            if any(left[i] and not any(i in D for D in types[pos+1:]) for i in range(d)):continue
            if allocate(pos+1,left,slots-n,columns+(C,)*n):return True
        return False
    return allocate(0,widths,k,())
@lru_cache(None)
def minimum(widths,q):
    for m in range(max(widths),sum(widths)-(len(widths)-q)+1):
        if allocated_feasible(widths,q,m):return m
    raise ValueError('no finite width')
def model(tree,target,k,permutation='identity',mode='compact'):
    ch,parents,internal=topology(tree)
    if len(target)!=len(internal) or any(type(r)!=int or r not in range(1,len(ch[v])+1) for v,r in zip(internal,target)):raise ValueError('profile')
    goals=dict(zip(internal,target));width={}
    for v in reversed(range(len(ch))):
        sizes=tuple(width[c] for c in ch[v])
        width[v]=1 if not sizes else minimum(sizes,goals[v])
    if type(k)!=int or k<width[0]:raise ValueError('palette width')
    supports={}
    def fill(v,palette):
        supports[v]=set(palette)
        if not ch[v]:return
        sizes=tuple(width[c] for c in ch[v]);r=goals[v];offset=0
        if len(sizes)==4:
            roots=canonical_roots(sizes,r,width[v])
            assigned=[[palette[j] for j in root] for root in roots]
        else:
            assigned=[]
            for size in sizes:
                if r==1:labels=palette[:size]
                elif r==len(sizes):labels=palette[offset:offset+size]
                else:
                    selected={palette[j%width[v]] for j in range(offset,offset+size)}
                    labels=[x for x in palette if x in selected]
                assigned.append(labels);offset+=size
        for c,labels in zip(ch[v],assigned):fill(c,labels)
    fill(0,list(range(k)))
    def raw(ss):return [sum(1<<v for v,S in ss.items() if j in S) for j in range(k)]
    end=raw(supports)
    if permutation not in ('identity','reversal','cyclic') or mode not in ('compact','inflated'):raise ValueError('case mode')
    def relabel(x):return x if permutation=='identity' else k-1-x if permutation=='reversal' else (x+1)%k
    start={v:{relabel(x) for x in S} for v,S in supports.items()}
    if mode=='inflated':
        for v in range(1,len(ch)):
            for x in range(k):
                if x in start[v] or x not in start[parents[v]]:continue
                start[v].add(x)
                if any(hitting([start[c] for c in ch[u]])!=goals[u] for u in internal):start[v].remove(x)
    return width[0],raw(start),end
def profile_check(tree,k,raw):
    ch,parents,internal=topology(tree);n=len(ch)
    if type(k)!=int or k<1 or not isinstance(raw,list) or len(raw)!=k or any(type(z)!=int or z<0 or z>=1<<n for z in raw):raise InterfaceNotPreserved('state representation')
    supports=[{j for j,z in enumerate(raw) if z&(1<<v)} for v in range(n)]
    if supports[0]!=set(range(k)):raise InterfaceNotPreserved('root changed')
    if any(not S for S in supports) or any(not supports[v]<=supports[p] for v,p in parents.items()):raise InterfaceNotPreserved('state admission')
    return [hitting([supports[c] for c in ch[v]]) for v in internal]
def path_check(tree,k,target,path,start,end):
    if not isinstance(path,list) or not path or path[0]!=start:raise InterfaceNotPreserved('path start')
    peak=0
    for i,raw in enumerate(path):
        profile=profile_check(tree,k,raw)
        if len(profile)!=len(target):raise ValueError('target length')
        cost=sum(abs(a-b) for a,b in zip(profile,target));peak=max(peak,cost)
        if cost>1:raise InterfaceNotPreserved('total excursion exceeds one')
        if i and sum((a^b).bit_count() for a,b in zip(raw,path[i-1]))!=1:raise InterfaceNotPreserved('nonprimitive move')
    if profile_check(tree,k,start)!=target or path[-1]!=end or profile_check(tree,k,end)!=target:raise InterfaceNotPreserved('exact canonical endpoint')
    return peak
def raw_roots(k,roots):return [1+sum(1<<(i+1) for i,A in enumerate(roots) if j in A) for j in range(k)]
@lru_cache(None)
def expected_specs(kind='campaign'):
    if kind=='canonical_admission_control':return [['CONTROL','canonical_q3']]
    if kind!='campaign':raise ValueError('kind')
    rows=[]
    for widths in product((1,2),repeat=4):
        for q in range(1,5):
            for k in range(1,5):rows.append(['F',list(widths),q,k])
    for k in (1,2,3):
        subsets=[[j for j in range(k) if bits&(1<<j)] for bits in range(1,1<<k)]
        for roots in product(subsets,repeat=4):rows.append(['R',k,*roots])
    for order in permutations(range(4)):rows.append(['R',4,*[[x] for x in order]])
    for name,(tree,profiles) in TEMPLATES.items():
        for profile in profiles:
            m=model(tree,list(profile),len(topology(tree)[0]))[0]
            for k in (m,m+1):
                for perm in ('identity','reversal','cyclic'):
                    for mode in ('compact','inflated'):rows.append(['N',name,list(profile),k,perm,mode])
    rows += [['M',name] for name in ('clearance_root_full','spare_current_bin','unsafe_q2','unsafe_q3')]
    return rows
def mechanism(name):
    if name=='clearance_root_full':
        return {'tree':(((),()),(),(),()),'k':4,'q':[3,2],'path':[[23,43,67,3],[23,43,71,3],[19,43,71,3],[17,43,71,3]],'expected_outcome':'exact_interior_clearance'}
    if name in ('unsafe_q2','unsafe_q3'):
        k=4 if name=='unsafe_q2' else 3;q=2 if k==4 else 3
        roots=[{0},{0},{1},{1}] if q==2 else [{0},{0},{1},{2}]
        path=[raw_roots(k,roots)]
        edits=[(1,0,2),(3,1,3)] if q==2 else [(2,1,0),(3,2,0)]
        for i,x,y in edits:
            roots[i].add(y);path.append(raw_roots(k,roots));roots[i].remove(x);path.append(raw_roots(k,roots))
        return {'tree':Q,'k':k,'q':[q],'path':path,'expected_outcome':'native_but_not_unit'}
    if name=='spare_current_bin':
        path=[[[0],[1,2],[],[]],[[0,1],[1,2],[],[]],[[0,1],[2],[],[]],[[0,1],[0,2],[],[]],[[1],[0,2],[],[]]]
        return {'capacities':[2,2,2,0],'start_cover':path[0],'target_cover':path[-1],'cover_path':path}
    raise ValueError('mechanism')
def json_equal(a,b):
    import json
    return json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)
def verify(doc):
    if not isinstance(doc,dict) or set(doc)!={'schema','kind','records'} or type(doc['schema'])!=int or doc['schema']!=1:raise ValueError('schema')
    kind=doc['kind'];rows=doc['records']
    if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows):raise ValueError('records')
    verify_identities([r.get('identity') for r in rows],expected_specs(kind))
    results=[]
    for row in rows:
        ident=row['identity'];family=ident[0]
        if row.get('status')!='ok':
            if row.get('category')=='construction':raise InterfaceNotPreserved('recorded construction failure')
            raise ValueError('INCOMPLETE: interrupted attempt')
        if family=='F':
            _,widths,q,k=ident;roots=canonical_roots(tuple(widths),q,k)
            wanted={'identity':ident,'status':'ok','feasible':roots is not None}
            if roots is not None:wanted['canonical_roots']=[list(A) for A in roots]
            if not json_equal(row,wanted):raise ValueError('feasibility/canonical record')
            results.append({'identity':ident,'feasible':roots is not None});continue
        if family=='M':
            expected=mechanism(ident[1]);wanted={'identity':ident,'status':'ok',**expected}
            if 'path' in expected:wanted.update(start=expected['path'][0],end=expected['path'][-1])
            if not json_equal(row,wanted):raise ValueError('mechanism metadata/path')
            if ident[1]=='spare_current_bin':
                prev=None
                for raw in row['cover_path']:
                    cover=[set(A) for A in raw]
                    if set.union(*cover)!={0,1,2} or any(len(A)>c for A,c in zip(cover,row['capacities'])):raise InterfaceNotPreserved('cover invariant')
                    if prev is not None and sum(len(a^b) for a,b in zip(cover,prev))!=1:raise InterfaceNotPreserved('cover primitive')
                    prev=cover
                results.append({'identity':ident,'outcome':'COVER_VERIFIED'});continue
            tree=row['tree'];k=row['k'];q=row['q'];path=row['path']
            for i,state in enumerate(path):
                profile=profile_check(tree,k,state)
                if i and sum((a^b).bit_count() for a,b in zip(state,path[i-1]))!=1:raise InterfaceNotPreserved('mechanism primitive')
                if ident[1]=='clearance_root_full':
                    if profile[1:]!=q[1:] or sum(abs(a-b) for a,b in zip(profile,q))>1:raise InterfaceNotPreserved('clearance interior')
                    if i<3 and [j for j,z in enumerate(state) if z&2]!=list(range(k)):raise InterfaceNotPreserved('clearance root')
            if ident[1].startswith('unsafe'):
                try:path_check(tree,k,q,path,path[0],path[-1])
                except InterfaceNotPreserved as exc:
                    if str(exc)!='total excursion exceeds one':raise
                else:raise InterfaceNotPreserved('unsafe unit path accepted')
            results.append({'identity':ident,'outcome':row['expected_outcome']});continue
        if family=='CONTROL':tree=Q;q=[3];k=3;start=end=[7,9,17]
        elif family=='R':
            k=ident[1];tree=Q;q=[hitting([set(A) for A in ident[2:]])];start=raw_roots(k,ident[2:]);end=model(tree,q,k)[2]
        elif family=='N':
            _,name,q,k,perm,mode=ident;tree=TEMPLATES[name][0];_,start,end=model(tree,q,k,perm,mode)
        else:raise ValueError('family')
        if set(row)!={'identity','status','tree','q','k','start','end','path'} or not json_equal([row['tree'],row['q'],row['k'],row['start'],row['end']],[tree,q,k,start,end]):raise ValueError('reconstructed metadata/start/endpoint')
        if family=='CONTROL' and row['path']!=[end]:raise ValueError('control singleton')
        peak=path_check(tree,k,q,row['path'],start,end)
        results.append({'identity':ident,'moves':len(row['path'])-1,'peak':peak})
    return {'status':'VERIFIED','kind':kind,'outcome':'FOUR_CHILD_INTERFACE_VALIDATED' if kind=='campaign' else 'CONTROL_VERIFIED','records':len(rows),'moves':sum(r.get('moves',0) for r in results),'nonunit_witness':'NOT_CLAIMED','results':results}
