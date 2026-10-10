import itertools,functools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
    if not s:return 0
    if 0 in s:return 99
    union=0
    for a in s:union|=a
    bits=[1<<x for x in range(union.bit_length()) if union&(1<<x)]
    for k in range(len(bits)+1):
        for c in itertools.combinations(bits,k):
            if all(a&sum(c) for a in s):return k
def fp(s,N):return tuple(sum(1<<i for i,a in enumerate(s) if a&(1<<x)) for x in range(N))
def maxima(s,N):
    F=set(fp(s,N))-{0};return sorted(j for j in F if not any(j!=k and j&~k==0 for k in F))
def witness(s,f,r,N):
    F=fp(s,N);M=maxima(s,N);labels=[x for x in range(N) if x!=r]
    choices=[[j for j in M if F[x]&~j==0] for x in labels];out=[]
    for assignment in itertools.product(*choices):
        target=tuple(sum(1<<x for x,j in zip(labels,assignment) if j&(1<<i)) for i in range(len(s)))
        if all(a.bit_count()>=d for a,d in zip(target,f)) and tau(target)<=4:out.append(target)
    return min(out) if out else None
def release(s,t,r,N):
    if t is None:return None
    out=[]
    for x in range(N):
        if x==r:continue
        for i,(a,b) in enumerate(zip(s,t)):
            if b&(1<<x) and not a&(1<<x):out.append([i,x])
    out += [[i,r] for i,a in enumerate(s) if a&(1<<r)]
    return out
def slices(s,ops):
    a=list(s);out=[tuple(a)]
    for i,x in ops:a[i]^=1<<x;out.append(tuple(a))
    return out
def fulltau(s,q):return min(tau(tuple(s)),1+tau(tuple(a for i,a in enumerate(s) if not q&(1<<i))))
def qs(s,f):return [q for q in range(1<<len(s)) if 3<=fulltau(s,q)<=4]
def native(s,f,q):return all(a.bit_count()+bool(q&(1<<i))>=d for i,(a,d) in enumerate(zip(s,f))) and 3<=fulltau(s,q)<=4
def permute(s,p):return tuple(sum(1<<p[x] for x in range(len(p)) if a&(1<<x)) for a in s)
def middle(s,r,p):
    # Canonical cycles: increasing least member, reserve cycle last.
    a=list(s);out=[];seen=set();cycles=[]
    def move(x,y):
        assert all(not(v&(1<<y)) for v in a)
        loc=[i for i,v in enumerate(a) if v&(1<<x)]
        for i in loc:a[i]|=1<<y;out.append([i,y])
        for i in loc:a[i]&=~(1<<x);out.append([i,x])
    for x in range(len(p)):
        if x in seen:continue
        c=[];y=x
        while y not in seen:seen.add(y);c.append(y);y=p[y]
        if len(c)>1:cycles.append(c)
    for c in sorted(cycles,key=lambda c:(r in c,min(c))):
        if r in c:
            j=c.index(r);c=c[j:]+c[:j];move(c[-1],r)
            for k in range(len(c)-2,0,-1):move(c[k],c[k+1])
        else:
            move(c[-1],r)
            for k in range(len(c)-2,-1,-1):move(c[k],c[k+1])
            move(r,c[0])
    assert tuple(a)==permute(s,p)
    return out
def macro(s,f,r,p,N):
    t=witness(s,f,r,N);assert t is not None
    L=release(s,t,r,N);mid=middle(t,r,p);back=[[i,p[x]] for i,x in reversed(L)];ops=L+mid+back
    route=slices(s,ops);assert route[-1]==permute(s,p)
    protected=qs(s,f)
    assert all(native(a,f,q) for a in route for q in protected)
    return {'permutation':p,'release':L,'middle':mid,'restoration':back,'toggles':ops,'endpoint':list(route[-1]),'cost':len(ops),'slice_checks':len(route)*len(protected)}
def fixtures():
    return [('saturated',[3,5,8,16,96],[2,2,1,1,2],2,7,[0,2,5,6]),('multi_donor',[3,5,10,20,32],[2,2,2,2,1],0,6,[0,1,2,5]),('deletion_triangle',[3,5,6,8,16],[1]*5,2,5,[0,1,2,3])]
def build():
    rows=[];sources=[];primary_checks=0;primary_steps=0
    for s in itertools.product(range(1,16),repeat=4):
        if __import__('functools').reduce(int.__or__,s)!=15 or tau(s) not in(3,4):continue
        sources.append(list(s))
        for mode in range(2):
            f=[a.bit_count() if mode==0 else max(1,a.bit_count()-1) for a in s]
            masks=qs(s,f)
            for r in range(4):
                t=witness(s,f,r,4);L=release(s,t,r,4)
                if t is not None:
                    path=slices(s,L);assert path[-1]==t
                    assert slices(t,L[::-1])==path[::-1]
                    # Restoration is the exact reverse, so has the same slice set.
                    assert all(native(a,f,q) for a in path for q in masks)
                    primary_checks+=len(path)*len(masks);primary_steps+=len(L)
                rows.append([len(sources)-1,mode,r,None if t is None else list(t),L])
    fix=[]
    for name,s,f,r,N,subset in fixtures():
        perm=[]
        for ordering in itertools.permutations(subset):
            p=list(range(N))
            for x,y in zip(subset,ordering):p[x]=y
            perm.append(macro(tuple(s),f,r,p,N))
        p,q=perm[1]['permutation'],perm[-1]['permutation'];c1=permute(s,p);r1=p[r]
        second=macro(c1,f,r1,q,N);composed=[q[p[x]] for x in range(N)]
        assert second['endpoint']==list(permute(s,composed))
        fix.append({'name':name,'source':s,'floors':f,'reserve':r,'palette':N,'subset':subset,'protected_masks':qs(s,f),'permutations':perm,'renewal':{'first':p,'second':q,'second_route':second,'composed':composed}})
    negatives=[]
    for name,s,f,N in [('isolated',[9,17,33,10,18,34,4],[2]*6+[1],6),('local_progress',[5,9,17,6,10,18,224,32],[2]*6+[3,1],8)]:
        negatives.append({'name':name,'source':s,'floors':f,'witnesses':[witness(tuple(s),f,r,N) for r in range(N)]})
        assert all(t is None for t in negatives[-1]['witnesses'])
    s=tuple([1|(1<<(3+i)) for i in range(5)]+[(2 if i<3 else 4)|(1<<(3+i)) for i in range(5)])
    candidate=tuple(a&~1 for a in s);f=[1]*10
    assert witness(s,f,0,8) is None and tau(candidate)==5
    upper={'source':list(s),'candidate':list(candidate),'floors':f,'reserve':0,'candidate_tau':tau(candidate),'witness':None}
    floor_s=(3,1,4,8);floor_c=(1,1,4,8);floor_f=[2,1,1,1]
    assert witness(floor_s,floor_f,1,4) is None and tau(floor_c)==3 and not native(floor_c,floor_f,0)
    floor_control={'source':list(floor_s),'candidate':list(floor_c),'floors':floor_f,'reserve':1,'candidate_tau':tau(floor_c),'candidate_admitted':False,'witness':None}
    dom_s=(9,17,33,10,18,34,4);dom_c=(9,17,9,10,18,10,4);dom_f=[2]*6+[1];q=82
    assert native(dom_s,dom_f,q) and not native(dom_c,dom_f,q) and tau(dom_c)==3 and all(a.bit_count()>=d for a,d in zip(dom_c,dom_f))
    assert any(not any(J&~K==0 for K in fp(dom_s,6)) for J in fp(dom_c,6))
    domination_control={'source':list(dom_s),'candidate':list(dom_c),'floors':dom_f,'reserve':5,'hidden_mask':q,'source_tau':fulltau(dom_s,q),'candidate_tau':fulltau(dom_c,q),'core_candidate_tau':tau(dom_c)}
    anchor_c=(9,9,9,18,18,18,4)
    assert all(native(anchor_c,dom_f,q) for q in qs(dom_s,dom_f)) and witness(dom_s,dom_f,5,6) is None
    assert any((a&~32)&~b for a,b in zip(dom_s,anchor_c))
    anchor_control={'source':list(dom_s),'candidate':list(anchor_c),'floors':dom_f,'reserve':5,'candidate_admitted':True,'donor_inclusion':False,'witness':None}
    return {'schema':'anchored-release-v1','sources':sources,'primary':rows,'fixtures':fix,'negative':negatives,'upper_control':upper,'floor_control':floor_control,'domination_control':domination_control,'anchor_control':anchor_control,'counts':{'sources':len(sources),'primary_identities':len(rows),'positive_releases':sum(r[3] is not None for r in rows),'primary_release_toggles':primary_steps,'primary_hidden_slice_checks':primary_checks,'permutation_cases':sum(len(r['permutations']) for r in fix),'permutation_hidden_slice_checks':sum(p['slice_checks'] for r in fix for p in r['permutations']),'renewal_cases':len(fix)}}
if __name__=='__main__':
    r=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(r['counts'],sort_keys=True))
