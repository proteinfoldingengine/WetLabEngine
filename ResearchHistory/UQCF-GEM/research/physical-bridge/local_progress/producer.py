import itertools,json,pathlib,sys,functools,collections
@functools.lru_cache(None)
def tau(s):
    if not s:return 0
    if 0 in s:return 99
    active=0
    for r in s:active|=r
    bits=[1<<x for x in range(active.bit_length()) if active&(1<<x)]
    for k in range(len(bits)+1):
        for c in itertools.combinations(bits,k):
            if all(r&sum(c) for r in s):return k
def fp(s,N):return [sum(1<<i for i,r in enumerate(s) if r&(1<<x)) for x in range(N)]
def safe(s,f,old,N):return all(r.bit_count()>=v for r,v in zip(s,f)) and tau(s)<=4 and all(any(j&~o==0 for o in old) for j in fp(s,N))
def fulltau(s,q):return min(tau(s),1+tau(tuple(r for i,r in enumerate(s) if not q&(1<<i))))
def admitted(s,q,f):return all(r.bit_count()+bool(q&(1<<i))>=d for i,(r,d) in enumerate(zip(s,f))) and 3<=fulltau(s,q)<=4
def family(n):
    N=n+5;fbit=1<<(n+2);gb=1<<(n+3);hb=1<<(n+4)
    s=tuple([1|(1<<(i+2)) for i in range(n)]+[2|(1<<(i+2)) for i in range(n)]+[fbit|gb|hb,fbit]);floors=[2]*(2*n)+[3,1]
    target=tuple([5]*n+[10]*n+[fbit|gb|hb,fbit]);old=fp(s,N)
    qs=[q for q in range(1<<len(s)) if admitted(s,q,floors)]
    seen={s};pending=collections.deque([s]);edges=[];reject=[]
    while pending:
        a=pending.popleft()
        for i in range(len(a)):
            for x in range(N):
                b=list(a);b[i]^=1<<x;b=tuple(b)
                if safe(b,floors,old,N):
                    edges.append([list(a),i,x,list(b)])
                    if b not in seen:seen.add(b);pending.append(b)
                else:
                    q=0 if any(r.bit_count()<d for r,d in zip(b,floors)) or tau(b)>4 else ((1<<len(s))-1)^fp(b,N)[x]
                    assert admitted(s,q,floors) and admitted(a,q,floors) and not admitted(b,q,floors)
                    reject.append([list(a),i,x,q,fulltau(s,q),fulltau(a,q),fulltau(b,q)])
    states=sorted(seen)
    assert all(admitted(a,q,floors) for a in states+[target] for q in qs)
    # Explicit maximal-footprint incidence lower bound and attaining allocation.
    maximal=sorted({j for j in old if j and not any(j!=o and j&~o==0 for o in old)})
    sizes=[j.bit_count() for j in maximal if not j&(1<<(2*n))]
    assert max(sizes)==n and (4*n+n-1)//n+3==7
    return {'n':n,'source':list(s),'floors':floors,'target':list(target),'capacity':7,'protected_masks':qs,'states':[list(a) for a in states],'edges':sorted(edges),'rejecting_toggles':sorted(reject),'absent_target_labels':list(range(4,n+2))}
def build():
    rows=[family(n) for n in (2,3,4,5)]
    return {'schema':'local-progress-v1','families':rows,'counts':{'families':4,'reachable_states':sum(len(r['states']) for r in rows),'directed_edges':sum(len(r['edges']) for r in rows),'protected_completions':sum(len(r['protected_masks']) for r in rows),'rejecting_toggles':sum(len(r['rejecting_toggles']) for r in rows),'protected_state_checks':sum((len(r['states'])+1)*len(r['protected_masks']) for r in rows)}}
if __name__=='__main__':
    r=build();pathlib.Path(sys.argv[1]).write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(r['counts'],sort_keys=True))
