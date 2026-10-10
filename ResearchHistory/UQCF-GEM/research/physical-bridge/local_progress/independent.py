import itertools,json,pathlib,sys,functools,collections
@functools.lru_cache(None)
def minimum(roots):
    if not roots:return 0
    if any(not r for r in roots):return 99
    first=min(roots,key=len)
    return 1+min(minimum(tuple(r for r in roots if x not in r)) for x in first)
def tau(s):return minimum(tuple(sorted(tuple(sorted(r)) for r in s)))
def packed(s):return [sum(2**x for x in r) for r in s]
def frozen(s):return tuple(tuple(sorted(r)) for r in s)
def unpack(s):return [set(r) for r in s]
def native(s,hidden,f):return all(len(r)+(i in hidden)>=d for i,(r,d) in enumerate(zip(s,f))) and 3<=min(tau(s),1+tau([r for i,r in enumerate(s) if i not in hidden]))<=4
def fulltau(s,H):return min(tau(s),1+tau([r for i,r in enumerate(s) if i not in H]))
def family(n):
    N=n+5;f,g,h=n+2,n+3,n+4
    source=[{0,i+2} for i in range(n)]+[{1,i+2} for i in range(n)]+[{f,g,h},{f}];floors=[2]*(2*n)+[3,1]
    target=[{0,2} for _ in range(n)]+[{1,3} for _ in range(n)]+[{f,g,h},{f}]
    masks=[];Hs=[]
    for v in itertools.product((False,True),repeat=len(source)):
        H={i for i,b in enumerate(v) if b}
        if native(source,H,floors):masks.append(sum(2**i for i in H));Hs.append(H)
    # Reconstruct BFS by native legality over EVERY original admitted hidden mask.
    initial=frozen(source);seen={initial};queue=collections.deque([initial]);edges=[];reject=[]
    while queue:
        state=queue.popleft();a=unpack(state)
        for i in range(len(a)):
            for x in range(N):
                b=[r.copy() for r in a];b[i]^={x}
                ok=all(native(b,H,floors) for H in Hs)
                if ok:
                    edges.append([packed(a),i,x,packed(b)])
                    key=frozen(b)
                    if key not in seen:seen.add(key);queue.append(key)
                else:
                    H=set() if any(len(r)<d for r,d in zip(b,floors)) or tau(b)>4 else {j for j,r in enumerate(b) if x not in r}
                    assert native(source,H,floors) and native(a,H,floors) and not native(b,H,floors)
                    reject.append([packed(a),i,x,sum(2**j for j in H),fulltau(source,H),fulltau(a,H),fulltau(b,H)])
    states=sorted(packed(unpack(a)) for a in seen)
    for a in [unpack(k) for k in seen]+[target]:
        assert all(native(a,H,floors) for H in Hs)
    # Independent exact static allocation search with bitset demand coverage.
    original={frozenset(i for i,r in enumerate(source) if x in r) for x in range(N)}
    M=[j for j in original if j and not any(j<k for k in original)]
    cap=None
    for count in range(1,8):
        for assign in itertools.combinations_with_replacement(range(len(M)),count):
            if any(sum(i in M[j] for j in assign)<d for i,d in enumerate(floors)):continue
            candidate=[{x for x,j in enumerate(assign) if i in M[j]} for i in range(len(source))]
            if tau(candidate)<=4:cap=count;break
        if cap is not None:break
    assert cap==7
    return {'n':n,'source':packed(source),'floors':floors,'target':packed(target),'capacity':cap,'protected_masks':sorted(masks),'states':states,'edges':sorted(edges),'rejecting_toggles':sorted(reject),'absent_target_labels':list(range(4,n+2))}
def build():
    rows=[family(n) for n in (2,3,4,5)]
    return {'schema':'local-progress-v1','families':rows,'counts':{'families':4,'reachable_states':sum(len(r['states']) for r in rows),'directed_edges':sum(len(r['edges']) for r in rows),'protected_completions':sum(len(r['protected_masks']) for r in rows),'rejecting_toggles':sum(len(r['rejecting_toggles']) for r in rows),'protected_state_checks':sum((len(r['states'])+1)*len(r['protected_masks']) for r in rows)}}
def validate(actual,expected):
    def check(a,b):
        if type(a) is not type(b):raise ValueError('type')
        if isinstance(b,dict):
            if a.keys()!=b.keys():raise ValueError('keys')
            for k in b:check(a[k],b[k])
        elif isinstance(b,list):
            if len(a)!=len(b):raise ValueError('length')
            for x,y in zip(a,b):check(x,y)
        elif a!=b:raise ValueError('value')
    check(actual,expected)
if __name__=='__main__':
    expected=build();validate(json.loads(pathlib.Path(sys.argv[1]).read_text()),expected);print(json.dumps({'status':'PASS','complete_typed_reconstruction':True,**expected['counts']},sort_keys=True))
