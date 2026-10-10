import itertools,functools,json,pathlib,sys
@functools.lru_cache(None)
def minimum(family):
    if not family:return 0
    if any(not r for r in family):return 99
    pivot=min(family,key=len)
    return 1+min(minimum(tuple(r for r in family if x not in r)) for x in pivot)
def tau(s):return minimum(tuple(sorted(tuple(sorted(r)) for r in s)))
def decode(s):return [{x for x in range(max(s).bit_length()) if (a//2**x)%2} for a in s]
def pack(s):return [sum(2**x for x in r) for r in s]
def footprints(s,N):return [{i for i,r in enumerate(s) if x in r} for x in range(N)]
def fulltau(s,H):return min(tau(s),1+tau([r for i,r in enumerate(s) if i not in H]))
def admitted(s,f,H):return all(len(r)+(i in H)>=d for i,(r,d) in enumerate(zip(s,f))) and 3<=fulltau(s,H)<=4
def protected(s,f):
    return [q for q in range(2**len(s)) if admitted(s,f,{i for i in range(len(s)) if (q//2**i)%2})]
def stage(s,t,r,N):
    if t is None:return None
    return [[i,x] for x in range(N) if x!=r for i in range(len(s)) if x in t[i] and x not in s[i]]+[[i,r] for i,v in enumerate(s) if r in v]
def run(s,ops):
    a=[v.copy() for v in s];states=[pack(a)]
    for i,x in ops:a[i]^={x};states.append(pack(a))
    return states
def candidate_forms(s,r):
    # Entire donor-expanding three-label core universe, constructed rootwise.
    N=4;old=footprints(s,N);base=[v-{r} for v in s];labels=set(range(N))-{r}
    subsets=[set(c) for k in range(1,4) for c in itertools.combinations(sorted(labels),k)]
    choices=[[v for v in subsets if b<=v] for b in base];out=[]
    for candidate in itertools.product(*choices):
        F=footprints(candidate,N)
        if not all(any(j<=k for k in old) for j in F):continue
        maximal=all(not any(F[x]<k for k in old) for x in labels)
        out.append((candidate,tuple(map(len,candidate)),maximal))
    return out
def general_witness(s,f,r,N):
    # Independent direct footprint expansion for the non-four-label fixtures.
    old=footprints(s,N);allowed=[];labels=[x for x in range(N) if x!=r]
    for x in labels:
        possibilities=[]
        for q in range(1,2**len(s)):
            J={i for i in range(len(s)) if (q//2**i)%2}
            if old[x]<=J and any(J<=k for k in old) and not any(J<k for k in old):possibilities.append(J)
        allowed.append(possibilities)
    good=[]
    for assignment in itertools.product(*allowed):
        target=[{x for x,J in zip(labels,assignment) if i in J} for i in range(len(s))]
        if all(len(v)>=d for v,d in zip(target,f)) and tau(target)<=4:good.append(pack(target))
    return decode(min(good)) if good else None
def permute(s,p):return [{p[x] for x in v} for v in s]
def middle(s,r,p):
    # Independent permutation-orbit decomposition, then state-based rename execution.
    unused=set(range(len(p)));orbits=[]
    while unused:
        x=min(unused);orbit=[x];y=p[x]
        while y!=x:orbit.append(y);y=p[y]
        unused-=set(orbit)
        if len(orbit)>1:orbits.append(orbit)
    orbits=sorted(orbits,key=lambda v:(r in v,min(v)))
    a=[v.copy() for v in s];out=[]
    for orbit in orbits:
        if r in orbit:
            k=orbit.index(r);orbit=orbit[k:]+orbit[:k]
            renames=[(orbit[-1],r)]+[(orbit[j],orbit[j+1]) for j in range(len(orbit)-2,0,-1)]
        else:renames=[(orbit[-1],r)]+[(orbit[j],orbit[j+1]) for j in range(len(orbit)-2,-1,-1)]+[(r,orbit[0])]
        for x,y in renames:
            assert all(y not in v for v in a)
            roots=[i for i,v in enumerate(a) if x in v]
            for i in roots:a[i].add(y);out.append([i,y])
            for i in roots:a[i].remove(x);out.append([i,x])
    assert a==permute(s,p)
    return out
def macro(s,f,r,p,N):
    t=general_witness(s,f,r,N);assert t is not None
    L=stage(s,t,r,N);mid=middle(t,r,p);back=[[i,p[x]] for i,x in L[::-1]];ops=L+mid+back
    states=run(s,ops);Q=protected(s,f)
    for v in states:
        a=decode(v)
        for q in Q:assert admitted(a,f,{i for i in range(len(s)) if (q//2**i)%2})
    assert states[-1]==pack(permute(s,p))
    return {'permutation':p,'release':L,'middle':mid,'restoration':back,'toggles':ops,'endpoint':states[-1],'cost':len(ops),'slice_checks':len(states)*len(Q)}
def build():
    sources=[];rows=[];checks=0;steps=0
    for bits in itertools.product(range(1,16),repeat=4):
        s=decode(bits)
        if set.union(*s)!=set(range(4)) or tau(s) not in(3,4):continue
        index=len(sources);sources.append(list(bits));forms=[candidate_forms(s,r) for r in range(4)]
        for mode in range(2):
            f=[len(a) if mode==0 else max(1,len(a)-1) for a in s];Q=protected(s,f)
            for r in range(4):
                safe=[c for c,size,m in forms[r] if all(a>=b for a,b in zip(size,f)) and tau(c)<=4]
                maximal=[c for c,size,m in forms[r] if m and all(a>=b for a,b in zip(size,f)) and tau(c)<=4]
                assert bool(safe)==bool(maximal)
                target=decode(min(pack(c) for c in maximal)) if maximal else None
                L=stage(s,target,r,4)
                if target is not None:
                    states=run(s,L);assert states[-1]==pack(target)
                    assert run(target,L[::-1])==states[::-1]
                    for a in states:
                        for q in Q:assert admitted(decode(a),f,{i for i in range(4) if (q//2**i)%2})
                    checks+=len(states)*len(Q);steps+=len(L)
                rows.append([index,mode,r,None if target is None else pack(target),L])
    fixture_defs=[('saturated',[{0,1},{0,2},{3},{4},{5,6}],[2,2,1,1,2],2,7,[0,2,5,6]),('multi_donor',[{0,1},{0,2},{1,3},{2,4},{5}],[2,2,2,2,1],0,6,[0,1,2,5]),('deletion_triangle',[{0,1},{0,2},{1,2},{3},{4}],[1]*5,2,5,[0,1,2,3])]
    fixtures=[]
    for name,s,f,r,N,subset in fixture_defs:
        routes=[]
        for images in itertools.permutations(subset):
            p=list(range(N))
            for x,y in zip(subset,images):p[x]=y
            routes.append(macro(s,f,r,p,N))
        p,q=routes[1]['permutation'],routes[-1]['permutation'];second=macro(permute(s,p),f,p[r],q,N);composed=[q[p[x]] for x in range(N)]
        assert second['endpoint']==pack(permute(s,composed))
        fixtures.append({'name':name,'source':pack(s),'floors':f,'reserve':r,'palette':N,'subset':subset,'protected_masks':protected(s,f),'permutations':routes,'renewal':{'first':p,'second':q,'second_route':second,'composed':composed}})
    negatives=[]
    for name,s,f,N in [('isolated',[{0,3},{0,4},{0,5},{1,3},{1,4},{1,5},{2}],[2]*6+[1],6),('local_progress',[{0,2},{0,3},{0,4},{1,2},{1,3},{1,4},{5,6,7},{5}],[2]*6+[3,1],8)]:
        values=[general_witness(s,f,r,N) for r in range(N)];assert all(v is None for v in values)
        negatives.append({'name':name,'source':pack(s),'floors':f,'witnesses':values})
    s=[{0,3+i} for i in range(5)]+[{1 if i<3 else 2,3+i} for i in range(5)];c=[v-{0} for v in s];f=[1]*10
    assert all(len(v)>=d for v,d in zip(c,f)) and all(any(J<=K for K in footprints(s,8)) for J in footprints(c,8))
    assert general_witness(s,f,0,8) is None and tau(c)==5
    upper={'source':pack(s),'candidate':pack(c),'floors':f,'reserve':0,'candidate_tau':tau(c),'witness':None}
    fs=[{0,1},{0},{2},{3}];fc=[{0},{0},{2},{3}];ff=[2,1,1,1]
    assert general_witness(fs,ff,1,4) is None and tau(fc)==3 and not admitted(fc,ff,set())
    floor_control={'source':pack(fs),'candidate':pack(fc),'floors':ff,'reserve':1,'candidate_tau':tau(fc),'candidate_admitted':False,'witness':None}
    ds=[{0,3},{0,4},{0,5},{1,3},{1,4},{1,5},{2}];dc=[{0,3},{0,4},{0,3},{1,3},{1,4},{1,3},{2}];df=[2]*6+[1];H={1,4,6}
    assert admitted(ds,df,H) and not admitted(dc,df,H) and tau(dc)==3 and all(len(a)>=d for a,d in zip(dc,df))
    assert any(not any(J<=K for K in footprints(ds,6)) for J in footprints(dc,6))
    domination_control={'source':pack(ds),'candidate':pack(dc),'floors':df,'reserve':5,'hidden_mask':sum(2**i for i in H),'source_tau':fulltau(ds,H),'candidate_tau':fulltau(dc,H),'core_candidate_tau':tau(dc)}
    ac=[{0,3}]*3+[{1,4}]*3+[{2}]
    assert all(admitted(ac,df,{i for i in range(7) if (q//2**i)%2}) for q in protected(ds,df)) and general_witness(ds,df,5,6) is None
    assert any(not(a-{5})<=b for a,b in zip(ds,ac))
    anchor_control={'source':pack(ds),'candidate':pack(ac),'floors':df,'reserve':5,'candidate_admitted':True,'donor_inclusion':False,'witness':None}
    return {'schema':'anchored-release-v1','sources':sources,'primary':rows,'fixtures':fixtures,'negative':negatives,'upper_control':upper,'floor_control':floor_control,'domination_control':domination_control,'anchor_control':anchor_control,'counts':{'sources':len(sources),'primary_identities':len(rows),'positive_releases':sum(v[3] is not None for v in rows),'primary_release_toggles':steps,'primary_hidden_slice_checks':checks,'permutation_cases':sum(len(r['permutations']) for r in fixtures),'permutation_hidden_slice_checks':sum(p['slice_checks'] for r in fixtures for p in r['permutations']),'renewal_cases':len(fixtures)}}
def validate(a,b):
    if type(a)!=type(b):raise ValueError('type')
    if isinstance(b,dict):
        if a.keys()!=b.keys():raise ValueError('keys')
        for k in b:validate(a[k],b[k])
    elif isinstance(b,list):
        if len(a)!=len(b):raise ValueError('length')
        for x,y in zip(a,b):validate(x,y)
    elif a!=b:raise ValueError('value')
if __name__=='__main__':
    b=build();validate(json.loads(pathlib.Path(sys.argv[1]).read_text()),b);print(json.dumps({'status':'PASS','complete_typed_reconstruction':True,**b['counts']},sort_keys=True))
