"""Bit-mask producer. Count feasibility is enumerated independently of the criterion."""
if not __debug__:
    raise RuntimeError("cover-static requires assertions enabled; optimized Python is unsupported")

import gzip
import hashlib
import itertools as it
import json
import pathlib
import sys
from functools import lru_cache


def sources(fixture=False):
    families=[]
    for name,k in [('K4',4),('C5',5),('K5',5),('K6-minus45',6),('K5-minus34',5)]:
        H=list(it.combinations(range(k),2))
        if name=='C5': H=[(0,1),(0,4),(1,2),(2,3),(3,4)]
        if name=='K6-minus45': H.remove((4,5))
        if name=='K5-minus34': H.remove((3,4))
        if name in ('K4','C5'):
            gs=[[e for r,e in enumerate(H) if b>>r&1] for b in range(1<<len(H))]
        else:
            gs=[[],H]+[[e for e in H if v not in e] for v in range(k)]
            if name=='K5':
                cross=[(u,v) for u in (0,1) for v in (2,3,4)]
                gs.extend([cross,sorted(cross+[(0,1)])])
        for G in gs:
            for a in it.product((1,2),repeat=k):
                families.append(dict(family=name,H=[list(e) for e in H],G=[list(e) for e in G],a=list(a)))
    if not fixture:return families
    specs=[('essential0','K6-minus45',0,[1]*6),('duplicate0','K6-minus45',0,[2,1,1,1,1,1]),
           ('isolate4','K6-minus45',4,[1]*6),('isolate5','K6-minus45',5,[1]*6),
           ('nonminimum','K5-minus34',0,[1]*5),('locked','K5',None,[2]*5)]
    result=[]
    for name,family,v,a in specs:
        for s in families:
            if s['family']!=family or s['a']!=a:continue
            G=[e for e in s['H'] if v not in e] if v is not None else [[u,w] for u in (0,1) for w in (2,3,4)]
            if s['G']==G:result.append(dict(s,name=name));break
        else:raise AssertionError(name)
    return result


def compositions(total,k):
    if k==1:
        yield (total,);return
    for n in range(total+1):
        for tail in compositions(total-n,k-1):yield (n,)+tail


def covers(H,k):
    return [list(C) for size in range(1,min(k,4)+1) for C in it.combinations(range(k),size)
            if all(u in C or v in C for u,v in H)]


@lru_cache(maxsize=128)
def count_universe(H,total,fs):
    k=max(max(e) for e in H)+1
    cs=covers(H,k)
    good=[]
    for extended in compositions(total,k+1):
        n=extended[1:]
        if all(n[u]+n[v]>=f for (u,v),f in zip(H,fs)) and any(all(n[v] for v in C) for C in cs):
            good.append(n)
    return sorted(good)


def stars(H,k):return [sum(1<<r for r,e in enumerate(H) if v in e) for v in range(k)]


def protected(H,a):
    ms=stars(H,len(a));full=(1<<len(H))-1
    return [h for h in range(full+1) if (full^h) and all((full^h)&~m for m in ms)]


def endpoint(H,a,C,I,N,choice):
    ms=stars(H,len(a));offset=[sum(a[:v]) for v in range(len(a))]
    anchors=[offset[v]+(a[v]-1 if choice=='last' else 0) for v in C]
    n=[a[v]-(v in I)+(v in N) for v in range(len(a))]
    state=[0]*sum(a)
    for v,x in zip(C,anchors):state[x]=ms[v]
    labels=iter(x for x in range(sum(a)) if x not in anchors)
    for v in range(len(a)):
        for _ in range(n[v]-(v in C)):state[next(labels)]=ms[v]
    assert state.count(0)==len(I)-len(N)
    return dict(C=C,I=I,N=N,choice=choice,anchors=anchors,counts=n,state=state,empty=state.count(0))


def record(s):
    H=s['H'];G=s['G'];a=s['a'];k=len(a);total=sum(a)
    fs=[a[u]+a[v] if [u,v] in G else 1 for u,v in H]
    feasible=[list(n) for n in count_universe(tuple(map(tuple,H)),total,tuple(fs))]
    minimum=min(map(sum,feasible));cs=covers(H,k)
    indep=[];deficient=[]
    for b in range(1,1<<k):
        I=[v for v in range(k) if b>>v&1]
        if any(u in I and v in I for u,v in G):continue
        N=sorted({w for u,v in G for t,w in ((u,v),(v,u)) if t in I})
        indep.append(I)
        if len(I)>len(N):deficient.append(dict(I=I,N=N))
    cr=[];ep=[]
    for C in cs:
        eligible=[d['I'] for d in deficient if not any(a[v]==1 and v in C for v in d['I'])]
        direct=any(sum(n)<total and all(n[v] for v in C) for n in feasible)
        assert direct==bool(eligible)
        cr.append(dict(C=C,eligible=eligible,static=direct))
        for d in deficient:
            if d['I'] in eligible:
                for choice in ('first','last'):ep.append(endpoint(H,a,C,d['I'],d['N'],choice))
    static=minimum<total
    assert static==any(c['static'] for c in cr)
    masks=protected(H,a);full=(1<<len(H))-1
    protected_exposed=sum(1<<(full^h) for h in masks)
    distinct=sorted({tuple(e['state']) for e in ep})
    # Bit position E denotes the exact exposed root subset E. This tests all
    # endpoint/mask pairs simultaneously, without sampling or hashing.
    for state in distinct:
        bad=1  # exposed empty means the hidden label alone covers all roots
        for footprint in set(state):
            sub=footprint
            while sub:
                bad|=1<<sub;sub=(sub-1)&footprint
        assert not bad&protected_exposed
        assert all(sum(bool(m>>r&1) for m in state)>=f for r,f in enumerate(fs))
        assert any(__import__('functools').reduce(int.__or__,ss,0)==full for ss in it.combinations(state,4))
    return dict(name=s.get('name',s['family']),source=s,floors=fs,feasible=feasible,minimum=minimum,
                minimizers=[n for n in feasible if sum(n)==minimum],independent=indep,deficient=deficient,
                covers=cr,static=static,endpoints=ep,distinct_endpoints=[list(c) for c in distinct],protected_masks=masks,
                hidden_checks=len(distinct)*len(masks))


def build(fixture=False,writer=None):
    records=[];digests=[];counts=dict(sources=0,feasible_vectors=0,endpoint_occurrences=0,distinct_endpoints=0,hidden_checks=0)
    for s in sources(fixture):
        r=record(s);line=json.dumps(r,sort_keys=True,separators=(',',':'))+'\n'
        digests.append(hashlib.sha256(line.encode()).hexdigest())
        if writer is None:records.append(r)
        else:writer.write(line.encode())
        counts['sources']+=1;counts['feasible_vectors']+=len(r['feasible'])
        counts['endpoint_occurrences']+=len(r['endpoints']);counts['distinct_endpoints']+=len(r['distinct_endpoints'])
        counts['hidden_checks']+=r['hidden_checks']
    return dict(schema='cover-static-v1',fixture=fixture,counts=counts,record_sha256=digests,**({'records':records} if writer is None else {}))

if __name__=='__main__':
    dest=sys.argv[1];identity=dest+'.identities.jsonl.gz'
    with open(identity,'wb') as f:
        with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as stream:data=build(writer=stream)
    data['identity_archive_sha256']=hashlib.sha256(pathlib.Path(identity).read_bytes()).hexdigest()
    pathlib.Path(dest).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps(data['counts'],sort_keys=True))
