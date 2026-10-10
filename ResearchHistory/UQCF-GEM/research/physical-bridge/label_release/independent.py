"""Set/representative-union reconstruction with independent state generation."""
import functools,itertools,json,pathlib,sys
def unpack(n):return frozenset(i for i in range(n.bit_length()) if n&(2**i))
def pack(s):return sum(2**x for x in s)
@functools.lru_cache(None)
def hit(s):
    candidates={frozenset()}
    for r in s:
        candidates={h|{x} for h in candidates for x in r}
        if not candidates:return 99
        candidates={h for h in candidates if not any(g<h for g in candidates)}
    return min(map(len,candidates),default=0)
def full(d,q,p):return tuple(r|({p} if i in unpack(q) else set()) for i,r in enumerate(d))
def qs(c,p):return [q for q in range(2**len(c)) if 3<=hit(full(c,q,p))<=4]
def valid(d,q,p,f):
    s=full(d,q,p);return all(len(r)>=a for r,a in zip(s,f)) and 3<=hit(s)<=4
def safe_core(c,d,p,f):
    if any(len(r)<a for r,a in zip(d,f)) or hit(tuple(d))>4:return False
    for x in range(p):
        selected=[set(c[i]) for i,r in enumerate(d) if x in r]
        if selected and not set.intersection(*selected):return False
    return True
def sources():
    result=[]
    for code in range(2**16):
        c=tuple(unpack((code//2**(4*i))%16) for i in range(4))
        if any(not r for r in c) or set.union(*(set(r) for r in c))!=set(range(4)) or not 3<=hit(c)<=4:continue
        f=list(map(len,c));masks=qs(c,4);pairs=[]
        footprints=[{i for i,r in enumerate(c) if x in r} for x in range(4)]
        for x in range(4):
            for y in range(4):
                if footprints[x]<footprints[y]:pairs.append([x,y])
        toggles=[];safe=[]
        for i in range(4):
            for x in range(4):
                d=list(c);d[i]=d[i]^{x};bad=[q for q in masks if not valid(d,q,4,f)];toggles.append([i,x,bad])
                if not bad:safe.append([i,x])
        if bool(pairs)!=bool(safe):raise ValueError('first-progress counterexample')
        releases=[]
        for kind,fl in [('saturated',f),('one-slack',[max(1,a-1) for a in f])]:
            for x in range(4):
                d=tuple(r-{x} for r in c);expected=all(len(r)>=a for r,a in zip(d,fl)) and hit(d)<=4
                bad=[q for q in masks if not valid(d,q,4,fl)]
                if expected!=(not bad):raise ValueError('extraction counterexample')
                releases.append([x,kind,expected,bad])
        result.append(dict(code=code,core=list(map(pack,c)),tau=hit(c),source_masks=masks,strict_pairs=pairs,safe_first_toggles=safe,toggles=toggles,release=releases))
    return result
def stages(c,M,a,d):
    # Generate configurations by explicit stage replacements rather than toggles.
    cur=list(c);out=[list(cur)];rem=sorted(M-({5} if 5 in M else set()))
    for i in rem:cur[i]=cur[i]-{5};out.append(list(cur))
    if 5 not in M:cur[5]=cur[5]|{5};out.append(list(cur))
    cur[5]=cur[5]-{d};out.append(list(cur))
    for i in range(3):cur[i]=cur[i]|{d};out.append(list(cur))
    for i in range(3):cur[i]=cur[i]-{a};out.append(list(cur))
    cur[5]=cur[5]|{a};out.append(list(cur))
    if 5 not in M:cur[5]=cur[5]-{5};out.append(list(cur))
    for i in rem:cur[i]=cur[i]|{5};out.append(list(cur))
    return [tuple(s) for s in out]
def loans():
    base=tuple(map(unpack,[1,1,1,2,4,24]));result=[];rejected=[];f=[1,1,1,1,1,2]
    for mask in range(1,64):
        M=unpack(mask);c=tuple(r|({5} if i in M else set()) for i,r in enumerate(base))
        if not 3<=hit(c)<=4:rejected.append([mask,hit(c)]);continue
        first=stages(c,M,0,3);second=stages(first[-1],M,3,0);path=first+second[1:];masks=qs(c,6)
        if len(set(first))!=len(first) or len(set(second))!=len(second) or path[-1]!=c:raise ValueError('renewal')
        for s in path:
            if not safe_core(c,s,6,f) or not all(valid(s,q,6,f) for q in masks):raise ValueError('loan counterexample')
        cost=2*3+2*len(M)+(0 if 5 in M else 4)
        if len(first)!=cost+1:raise ValueError('cost')
        result.append(dict(mask=mask,core=list(map(pack,c)),tau=hit(c),source_masks=masks,cost=cost,path=[list(map(pack,s)) for s in path],taus=[[hit(full(s,q,6)) for s in path] for q in masks]))
    return result,rejected
def controls():
    c=tuple(map(unpack,[3,1,4,8]));f=[2,1,1,1];masks=qs(c,4);safe=[];absent=[]
    for i in range(4):
        for x in range(4):
            d=list(c);d[i]=d[i]^{x}
            if all(valid(d,q,4,f) for q in masks):safe.append([i,x])
    for code in range(2**16):
        d=tuple(unpack((code//2**(4*i))%16) for i in range(4))
        if any(not r for r in d) or set.union(*(set(r) for r in d))==set(range(4)):continue
        if all(valid(d,q,4,f) for q in masks):absent.append(code)
    upper=tuple(map(unpack,[3,5,8,16,32]));gone=tuple(r-{0} for r in upper)
    return dict(nested_core=list(map(pack,c)),nested_safe_first=safe,nested_absent_states=absent,upper_core=list(map(pack,upper)),upper_removed=list(map(pack,gone)),upper_taus=[hit(upper),hit(gone)])
@functools.lru_cache(None)
def expected_json():
    loan,rejected=loans();d=dict(schema='existing-label-release-v1',sources=sources(),loans=loan,rejected_masks=rejected,controls=controls());return json.dumps(d,sort_keys=True,separators=(',',':'))
def validate(d):
    if json.dumps(d,sort_keys=True,separators=(',',':'))!=expected_json():raise ValueError('complete typed reconstruction mismatch')
    return True
if __name__=='__main__':validate(json.loads(pathlib.Path(sys.argv[1]).read_text()));print(json.dumps({'status':'PASS','method':'complete independent set/representative-union reconstruction'}))
