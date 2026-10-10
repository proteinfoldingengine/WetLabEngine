#!/usr/bin/env python3
"""Exact bit-toggle enumerator; no floating point or hidden observation."""
import functools
import itertools
import json
import pathlib
import sys

@functools.lru_cache(None)
def tau(roots):
    if any(r==0 for r in roots): return 99
    active=0
    for r in roots: active |= r
    labels=[1<<i for i in range(active.bit_length()) if active & (1<<i)]
    for n in range(len(labels)+1):
        for chosen in itertools.combinations(labels,n):
            hit=sum(chosen)
            if all(r&hit for r in roots): return n
    raise AssertionError('no cover')

def partitions(m):
    def extend(p):
        if len(p)==m: yield tuple(p); return
        for j in range(max(p)+2): yield from extend(p+[j])
    yield from extend([0])

def source(p,apex=0,host=3):
    return [ (1<<apex)|(1<<(5+j)) for j in p]+[2,4,(1<<host)|16]

def path(p,d,r,apex=0,host=3):
    m=len(p); h=m+2; block=[i for i,j in enumerate(p) if j==r]
    s=source(p,apex,host); states=[s.copy()]
    def edit(i,x,add):
        bit=1<<x
        assert bool(s[i]&bit)!=add, 'invalid toggle'
        s[i]^=bit; states.append(s.copy())
    for i in block: edit(i,5+d,True)
    for i in block: edit(i,5+r,False)
    edit(h,5+r,True); edit(h,host,False)
    for i in range(m): edit(i,host,True)
    for i in range(m): edit(i,apex,False)
    edit(h,apex,True); edit(h,5+r,False)
    for i in block: edit(i,5+r,True)
    for i in block: edit(i,5+d,False)
    assert states[-1]==source(p,host,apex)
    return states

def footprints(s,n):
    return [sum(1<<i for i,b in enumerate(s) if b&(1<<x)) for x in range(n)]

def check_path(states,floors,n):
    original=footprints(states[0],n)
    assert len(set(map(tuple,states)))==len(states)
    for s in states:
        assert all(b.bit_count()>=f for b,f in zip(s,floors))
        assert tau(tuple(s))<=4
        assert all(any(j&~old==0 for old in original) for j in footprints(s,n))
    for a,b in zip(states,states[1:]):
        assert sum((x^y).bit_count() for x,y in zip(a,b))==1

def completed(s,q,u):
    return tuple(b | (u if q&(1<<i) else 0) for i,b in enumerate(s))

def admitted(s,floors):
    return all(b.bit_count()>=f for b,f in zip(s,floors)) and 3<=tau(tuple(s))<=4

def controls():
    p=(0,1); s=source(p); f=[2,2,1,1,2]; u=128
    floor=s.copy(); floor[1]^=64
    mixed=s.copy(); mixed[-1]|=64
    forward=path(p,0,1); cleanup=forward[-3].copy(); cleanup[1]^=32
    p3=(0,1,2); split=path(p3,0,1)[4].copy()
    # after release, host reserve added and D removed; transfer only root0 then delete its A
    split[0]|=8; split[0]^=1
    rows={}
    for name,src,cand,q,hidden,fl in [('floor_release',s,floor,0,u,f),('mixed_reserve',s,mixed,13,u,f),('split_apex',source(p3),split,0,256,[2,2,2,1,1,2]),('floor_cleanup',s,cleanup,0,u,f)]:
        a=completed(src,q,hidden); b=completed(cand,q,hidden)
        rows[name]={'source':src,'candidate':cand,'q':q,'source_tau':tau(a),'candidate_tau':tau(b),'source_admitted':admitted(a,fl),'candidate_admitted':admitted(b,fl)}
        assert rows[name]['source_admitted'] and not rows[name]['candidate_admitted'],name
    return rows

def build():
    cases=[]; isolated=[]; comps=checks=0
    for m in (2,3,4):
        for p in partitions(m):
            k=max(p)+1; n=k+5; u=1<<n; floors=[2]*m+[1,1,2]; s=source(p)
            qs=[q for q in range(1<<(m+3)) if admitted(completed(s,q,u),floors)]
            if k==1:
                rejects=[]
                for i in range(m+3):
                    for x in range(n):
                        cand=s.copy(); cand[i]^=1<<x
                        witness=next(q for q in qs if not admitted(completed(cand,q,u),floors))
                        rejects.append({'root':i,'label':x,'q':witness})
                isolated.append({'m':m,'source':s,'floors':floors,'protected_masks':qs,'rejecting_toggles':rejects})
                continue
            for d in range(k):
                for r in range(k):
                    if d==r: continue
                    fw=path(p,d,r); rv=path(p,d,r,3,0)
                    check_path(fw,floors,n); check_path(rv,floors,n)
                    completion=[]
                    for q in qs:
                        tf=[tau(completed(b,q,u)) for b in fw]
                        tr=[tau(completed(b,q,u)) for b in rv]
                        assert all(3<=t<=4 for t in tf+tr)
                        assert tf[0]==tf[-1]==tr[0]==tr[-1]
                        completion.append({'q':q,'forward_tau':tf,'reverse_tau':tr})
                        comps+=1; checks+=len(tf)+len(tr)
                    cases.append({'partition':list(p),'donor':d,'reserve':r,'floors':floors,'forward':fw,'reverse':rv,'completions':completion})
    return {'schema':'saturated-transfer-v1','cases':cases,'isolated':isolated,'controls':controls(),'counts':{'cases':len(cases),'protected_completions':comps,'slice_checks':checks,'isolated_sources':len(isolated),'rejecting_toggles':sum(len(r['rejecting_toggles']) for r in isolated),'native_controls':4}}

if __name__=='__main__':
    record=build(); pathlib.Path(sys.argv[1]).write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n'); print(json.dumps(record['counts'],sort_keys=True))
