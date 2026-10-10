#!/usr/bin/env python3
"""Independent sets, representative-union covers and Cartesian partition reconstruction."""
import functools
import itertools
import json
import pathlib
import sys

@functools.lru_cache(None)
def cover(family):
    roots=[frozenset(r) for r in family]
    if any(not r for r in roots): return 99
    frontier={frozenset()}
    for root in roots:
        candidates={v|{x} for v in frontier for x in root}
        frontier={v for v in candidates if not any(w<v for w in candidates)}
    return min(map(len,frontier))

def tau(s): return cover(tuple(tuple(sorted(r)) for r in s))
def bits(s): return [sum(1<<x for x in r) for r in s]
def src(p,a=0,h=3): return [{a,5+j} for j in p]+[{1},{2},{h,4}]
def complete(s,q,u): return [r|({u} if (q//2**i)%2 else set()) for i,r in enumerate(s)]
def native(s,fl): return all(len(r)>=f for r,f in zip(s,fl)) and tau(s) in (3,4)

def schedule(p,d,r,a=0,h=3):
    m=len(p); vr=[i for i,j in enumerate(p) if j==r]; s=src(p,a,h); states=[bits(s)]
    operations=[(i,5+d,1) for i in vr]+[(i,5+r,0) for i in vr]+[(m+2,5+r,1),(m+2,h,0)]+[(i,h,1) for i in range(m)]+[(i,a,0) for i in range(m)]+[(m+2,a,1),(m+2,5+r,0)]+[(i,5+r,1) for i in vr]+[(i,5+d,0) for i in vr]
    original=src(p,a,h); n=max(p)+6
    old=[{i for i,root in enumerate(original) if x in root} for x in range(n)]
    for i,x,add in operations:
        if add:
            if x in s[i]: raise ValueError('duplicate add')
            s[i].add(x)
        else:
            if x not in s[i]: raise ValueError('absent delete')
            s[i].remove(x)
        fl=[2]*m+[1,1,2]
        if not native(s,fl): raise ValueError('core native')
        for y in range(n):
            footprint={j for j,root in enumerate(s) if y in root}
            if not any(footprint<=o for o in old): raise ValueError('original footprint')
        states.append(bits(s))
    if states[-1]!=bits(src(p,h,a)): raise ValueError('exact target')
    if len({tuple(v) for v in states})!=len(states): raise ValueError('ambiguous policy')
    return states

def decode(v): return [{i for i in range(max(v).bit_length()) if (b//2**i)%2} for b in v]

def controls():
    s=src((0,1)); f=[2,2,1,1,2]
    floor=[r.copy() for r in s]; floor[1].remove(6)
    mixed=[r.copy() for r in s]; mixed[-1].add(6)
    # exact target with reserve not yet returned to root1; removing donor then crosses floor
    cleanup=src((0,1),3,0); cleanup[1]={3}
    s3=src((0,1,2)); split=[r.copy() for r in s3]
    split[1]={0,5}; split[-1]={4,6}; split[0]={3,5}
    out={}
    for name,a,b,q,u,fl in [('floor_release',s,floor,0,7,f),('mixed_reserve',s,mixed,13,7,f),('split_apex',s3,split,0,8,[2,2,2,1,1,2]),('floor_cleanup',s,cleanup,0,7,f)]:
        aa=complete(a,q,u); bb=complete(b,q,u)
        out[name]={'source':bits(a),'candidate':bits(b),'q':q,'source_tau':tau(aa),'candidate_tau':tau(bb),'source_admitted':native(aa,fl),'candidate_admitted':native(bb,fl)}
        if not native(aa,fl) or native(bb,fl): raise ValueError(name)
    return out

def build():
    cases=[]; isolated=[]; count=checks=0
    for m in (2,3,4):
        canonical=[]
        for p in itertools.product(range(m),repeat=m):
            if p[0]==0 and all(p[i]<=1+max(p[:i]) for i in range(1,m)): canonical.append(p)
        for p in canonical:
            k=len(set(p)); n=k+5; fl=[2]*m+[1,1,2]; s=src(p)
            qs=[q for q in range(2**(m+3)) if native(complete(s,q,n),fl)]
            if k==1:
                rejects=[]
                for i in range(m+3):
                    for x in range(n):
                        candidate=[r.copy() for r in s]; candidate[i]=candidate[i]^{x}
                        unsafe=[q for q in qs if not native(complete(candidate,q,n),fl)]
                        if not unsafe: raise ValueError('not isolated')
                        rejects.append({'root':i,'label':x,'q':min(unsafe)})
                isolated.append({'m':m,'source':bits(s),'floors':fl,'protected_masks':qs,'rejecting_toggles':rejects}); continue
            for d,r in itertools.permutations(range(k),2):
                fw=schedule(p,d,r); rv=schedule(p,d,r,3,0); rows=[]
                sf=[decode(v) for v in fw]; sr=[decode(v) for v in rv]
                for q in qs:
                    tf=[tau(complete(v,q,n)) for v in sf]; tr=[tau(complete(v,q,n)) for v in sr]
                    if not all(t in (3,4) for t in tf+tr): raise ValueError('hidden band')
                    if len({tf[0],tf[-1],tr[0],tr[-1]})!=1: raise ValueError('endpoint tau')
                    rows.append({'q':q,'forward_tau':tf,'reverse_tau':tr}); count+=1; checks+=len(tf)+len(tr)
                cases.append({'partition':list(p),'donor':d,'reserve':r,'floors':fl,'forward':fw,'reverse':rv,'completions':rows})
    return {'schema':'saturated-transfer-v1','cases':cases,'isolated':isolated,'controls':controls(),'counts':{'cases':len(cases),'protected_completions':count,'slice_checks':checks,'isolated_sources':len(isolated),'rejecting_toggles':sum(len(r['rejecting_toggles']) for r in isolated),'native_controls':4}}

def validate(actual,expected=None):
    if expected is None: expected=build()
    def compare(a,b,path):
        if type(a) is not type(b): raise ValueError('type '+path)
        if isinstance(b,dict):
            if set(a)!=set(b): raise ValueError('members '+path)
            for k in b: compare(a[k],b[k],path+'/'+k)
        elif isinstance(b,list):
            if len(a)!=len(b): raise ValueError('length '+path)
            for i,(x,y) in enumerate(zip(a,b)): compare(x,y,path+'/'+str(i))
        elif a!=b: raise ValueError('value '+path)
    compare(actual,expected,'root')
    return {'status':'PASS','complete_typed_reconstruction':True,**expected['counts']}

if __name__=='__main__': print(json.dumps(validate(json.loads(pathlib.Path(sys.argv[1]).read_text())),sort_keys=True))
