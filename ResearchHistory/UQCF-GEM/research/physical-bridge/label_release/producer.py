"""Bit/subset production and exact native-completion checks."""
import functools,itertools,json,pathlib,sys
@functools.lru_cache(None)
def tau(s):
    if not s:return 0
    if 0 in s:return 99
    palette=0
    for r in s:palette|=r
    return min(h.bit_count() for h in range(palette+1) if h&palette==h and all(h&r for r in s))
def full(c,q,p):return tuple(r|((1<<p) if q>>i&1 else 0) for i,r in enumerate(c))
def masks(c,p):return [q for q in range(1<<len(c)) if 3<=tau(full(c,q,p))<=4]
def legal(c,q,p,f):
    s=full(c,q,p);return all(r.bit_count()>=a for r,a in zip(s,f)) and 3<=tau(s)<=4
def criterion(c,d,p,f):
    old=[sum(1<<i for i,r in enumerate(c) if r>>x&1) for x in range(p)]
    cur=[sum(1<<i for i,r in enumerate(d) if r>>x&1) for x in range(p)]
    return all(r.bit_count()>=a for r,a in zip(d,f)) and tau(tuple(d))<=4 and all(any(j&~k==0 for k in old) for j in cur)
def source_rows():
    out=[]
    for c in itertools.product(range(1,16),repeat=4):
        if c[0]|c[1]|c[2]|c[3]!=15 or not 3<=tau(c)<=4:continue
        f=[r.bit_count() for r in c];qs=masks(c,4)
        fp=[sum(1<<i for i,r in enumerate(c) if r>>x&1) for x in range(4)]
        pairs=[[x,y] for x in range(4) for y in range(4) if fp[x]!=fp[y] and fp[x]&~fp[y]==0]
        toggles=[];safe=[]
        for i in range(4):
            for x in range(4):
                d=list(c);d[i]^=1<<x;bad=[q for q in qs if not legal(d,q,4,f)]
                assert (not bad)==criterion(c,d,4,f)
                toggles.append([i,x,bad])
                if not bad:safe.append([i,x])
        assert bool(pairs)==bool(safe)
        release=[]
        for kind,fl in [('saturated',f),('one-slack',[max(1,x-1) for x in f])]:
            for x in range(4):
                d=[r&~(1<<x) for r in c]
                expected=all(r.bit_count()>=a for r,a in zip(d,fl)) and tau(tuple(d))<=4
                bad=[q for q in qs if not legal(d,q,4,fl)]
                assert expected==(not bad)
                release.append([x,kind,expected,bad])
        out.append(dict(code=sum(r<<(4*i) for i,r in enumerate(c)),core=list(c),tau=tau(c),source_masks=qs,strict_pairs=pairs,safe_first_toggles=safe,toggles=toggles,release=release))
    return sorted(out,key=lambda s:s['code'])
def macro(c,M,a,d):
    h=5;r=5;path=[list(c)];actions=[]
    removal=[i for i in range(6) if M>>i&1 and (i!=h or not M>>h&1)]
    actions.extend((i,r) for i in removal)
    if not M>>h&1:actions.append((h,r))
    actions.append((h,d));actions.extend((i,d) for i in range(3));actions.extend((i,a) for i in range(3));actions.append((h,a))
    if not M>>h&1:actions.append((h,r))
    actions.extend((i,r) for i in removal)
    cur=list(c)
    for i,x in actions:cur[i]^=1<<x;path.append(list(cur))
    return path
def loans():
    base=(1,1,1,2,4,24);out=[];rejected=[];f=[1,1,1,1,1,2]
    for M in range(1,64):
        c=tuple(r|(32 if M>>i&1 else 0) for i,r in enumerate(base))
        if not 3<=tau(c)<=4:rejected.append([M,tau(c)]);continue
        qs=masks(c,6);p1=macro(c,M,0,3);p2=macro(tuple(p1[-1]),M,3,0);path=p1+p2[1:]
        cost=6+2*M.bit_count()+(0 if M>>5&1 else 4)
        assert len(p1)==cost+1 and len(set(map(tuple,p1)))==len(p1) and len(set(map(tuple,p2)))==len(p2)
        assert path[-1]==list(c)
        for s in path:assert criterion(c,s,6,f)
        ts=[[tau(full(s,q,6)) for s in path] for q in qs]
        assert all(legal(s,q,6,f) for s in path for q in qs)
        out.append(dict(mask=M,core=list(c),tau=tau(c),source_masks=qs,cost=cost,path=path,taus=ts))
    return out,rejected
def controls():
    c=(3,1,4,8);f=[2,1,1,1];qs=masks(c,4);safe=[];absent=[]
    for i in range(4):
        for x in range(4):
            d=list(c);d[i]^=1<<x
            if all(legal(d,q,4,f) for q in qs):safe.append([i,x])
    for d in itertools.product(range(1,16),repeat=4):
        union=d[0]|d[1]|d[2]|d[3]
        if union!=15 and criterion(c,d,4,f):absent.append(sum(r<<(4*i) for i,r in enumerate(d)))
    upper=(3,5,8,16,32);gone=tuple(r&~1 for r in upper)
    return dict(nested_core=list(c),nested_safe_first=safe,nested_absent_states=absent,upper_core=list(upper),upper_removed=list(gone),upper_taus=[tau(upper),tau(gone)])
def produce():
    loan,rejected=loans();return dict(schema='existing-label-release-v1',sources=source_rows(),loans=loan,rejected_masks=rejected,controls=controls())
def counts(d):return dict(sources=len(d['sources']),first_progress_sources=sum(bool(s['safe_first_toggles']) for s in d['sources']),release_tests=sum(len(s['release']) for s in d['sources']),loan_masks=len(d['loans']),rejected_loan_masks=len(d['rejected_masks']),loan_completions=sum(len(s['source_masks']) for s in d['loans']),loan_slice_checks=sum(len(s['source_masks'])*len(s['path']) for s in d['loans']))
if __name__=='__main__':
    d=produce();pathlib.Path(sys.argv[1]).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(counts(d),sort_keys=True))
