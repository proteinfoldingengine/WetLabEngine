"""Independent explicit-set reconstruction; never imports the producer."""
if not __debug__:
    raise RuntimeError("cover-static requires assertions enabled; optimized Python is unsupported")

import gzip
import hashlib
import itertools
import json
import pathlib
import sys
from functools import lru_cache


def subsets(items,maximum=None):
    items=list(items)
    for n in range(len(items)+1 if maximum is None else min(maximum,len(items))+1):
        yield from itertools.combinations(items,n)


def declarations(fixture=False):
    out=[]
    for family,k,removed,cycle in [('K4',4,None,False),('C5',5,None,True),('K5',5,None,False),
                                 ('K6-minus45',6,(4,5),False),('K5-minus34',5,(3,4),False)]:
        edges=sorted({tuple(sorted((u,(u+1)%k))) for u in range(k)}) if cycle else [e for e in itertools.combinations(range(k),2) if e!=removed]
        if family in ('K4','C5'):
            graphs=sorted(subsets(edges),key=lambda es:sum(2**edges.index(e) for e in es))
        else:
            graphs=[(),tuple(edges)]+[tuple(e for e in edges if v not in e) for v in range(k)]
            if family=='K5':
                cross=tuple(e for e in edges if (e[0]<2)!=(e[1]<2))
                graphs += [cross,tuple(sorted(cross+((0,1),)))]
        for graph in graphs:
            for profile in itertools.product((1,2),repeat=k):
                out.append(dict(family=family,H=[list(e) for e in edges],G=[list(e) for e in graph],a=list(profile)))
    if not fixture:
        assert len(out)==3072
        return out
    requests=[('essential0','K6-minus45',0,False),('duplicate0','K6-minus45',0,True),
              ('isolate4','K6-minus45',4,False),('isolate5','K6-minus45',5,False),
              ('nonminimum','K5-minus34',0,False),('locked','K5',None,True)]
    selected=[]
    for name,family,isolated,duplicate in requests:
        matches=[]
        for source in out:
            if source['family']!=family:continue
            wanted=[2]*5 if isolated is None else [1]*len(source['a'])
            if duplicate and isolated is not None:wanted[0]=2
            graph=[e for e in source['H'] if isolated not in e] if isolated is not None else [e for e in source['H'] if (e[0]<2)!=(e[1]<2)]
            if source['a']==wanted and source['G']==graph:matches.append(source)
        assert len(matches)==1
        selected.append(dict(matches[0],name=name))
    return selected


def hitting(footprints,H):
    roots=set(map(tuple,H))
    for n in range(len(footprints)+1):
        if any(set().union(*selection)>=roots for selection in itertools.combinations(footprints,n)):return n
    return len(footprints)+1


def original_stars(s):
    edges=set(map(tuple,s['H']))
    return [{e for e in edges if v in e} for v,a in enumerate(s['a']) for _ in range(a)]


def validate_source(s):
    a=s['a'];H=list(map(tuple,s['H']));G=list(map(tuple,s['G']))
    assert a and all(type(n) is int and n>0 for n in a)
    assert H==sorted(set(H)) and all(0<=u<v<len(a) for u,v in H)
    assert G==sorted(set(G)) and set(G)<=set(H)
    assert set().union(*(set(e) for e in H))==set(range(len(a)))
    assert hitting([{e for e in H if v in e} for v in range(len(a))],H) in (3,4)
    return True


def validate_cover(s,C):
    assert len(C)<=4 and list(C)==sorted(set(C)) and all(0<=v<len(s['a']) for v in C)
    assert all(set(e)&set(C) for e in s['H'])
    return True


def validate_endpoint(s,state):
    assert len(state)==sum(s['a'])
    original=original_stars(s);G=set(map(tuple,s['G']))
    assert all(any(f<=m for m in original) for f in state)
    for u,v in s['H']:
        floor=s['a'][u]+s['a'][v] if (u,v) in G else 1
        assert sum((u,v) in f for f in state)>=floor
    assert hitting(state,s['H'])<=4
    return True


@lru_cache(maxsize=128)
def all_counts(H,total,floors):
    k=max(itertools.chain.from_iterable(H))+1
    valid=[]
    # Stars-and-bars via multisets, including a distinguished empty slot.
    for tokens in itertools.combinations_with_replacement(range(k+1),total):
        n=tuple(tokens.count(v) for v in range(1,k+1))
        if any(n[u]+n[v]<bound for (u,v),bound in zip(H,floors)):continue
        occupied=[v for v in range(k) if n[v]>0]
        if any(all(set(e)&set(C) for e in H) for C in subsets(occupied,4)):valid.append(n)
    return sorted(valid)


def reconstruct(s):
    validate_source(s)
    H=list(map(tuple,s['H']));G=list(map(tuple,s['G']));a=s['a'];k=len(a);total=sum(a)
    floor=[a[u]+a[v] if (u,v) in G else 1 for u,v in H]
    feasible=[list(n) for n in all_counts(tuple(H),total,tuple(floor))]
    minimum=min(sum(n) for n in feasible)
    independent=[];deficient=[]
    # Numeric membership order is part of the canonical format, not the enumeration algorithm.
    for I in sorted((c for c in subsets(range(k)) if c),key=lambda c:sum(2**v for v in c)):
        chosen=set(I)
        if any(set(e)<=chosen for e in G):continue
        neighbors=set().union(*(set(e)-chosen for e in G if set(e)&chosen))
        independent.append(list(I))
        if len(chosen)>len(neighbors):deficient.append(dict(I=list(I),N=sorted(neighbors)))
    cr=[];endpoints=[];original=original_stars(s)
    for C in subsets(range(k),4):
        if not all(set(e)&set(C) for e in H):continue
        validate_cover(s,C)
        eligible=[d['I'] for d in deficient if all(a[v]>1 or v not in C for v in d['I'])]
        direct=any(sum(n)<total and all(n[v]>=1 for v in C) for n in feasible)
        assert direct==bool(eligible)
        cr.append(dict(C=list(C),eligible=eligible,static=direct))
        for d in deficient:
            if d['I'] not in eligible:continue
            for choice in ('first','last'):
                labels_by_type=[];cursor=0
                for multiplicity in a:
                    labels_by_type.append(list(range(cursor,cursor+multiplicity)));cursor+=multiplicity
                anchors=[labels_by_type[v][0 if choice=='first' else -1] for v in C]
                counts=[a[v]-int(v in d['I'])+int(v in d['N']) for v in range(k)]
                state=[set() for _ in range(total)]
                for label in anchors:state[label]=original[label].copy()
                remaining=[label for label in range(total) if label not in anchors]
                slots=[v for v,n in enumerate(counts) for _ in range(n-int(v in C))]
                for label,v in zip(remaining,slots):state[label]={e for e in H if v in e}
                validate_endpoint(s,state)
                assert all(state[label]==original[label] for label in anchors)
                empty=sum(not footprint for footprint in state)
                assert empty==len(d['I'])-len(d['N'])
                bits=[sum(2**H.index(e) for e in footprint) for footprint in state]
                endpoints.append(dict(C=list(C),I=d['I'],N=d['N'],choice=choice,anchors=anchors,counts=counts,state=bits,empty=empty))
    masks=[];rootset=set(H);exposed_sets=[]
    for hidden in range(2**len(H)):
        exposed={e for r,e in enumerate(H) if not (hidden//(2**r))%2}
        if exposed and all(not exposed<=star for star in original):
            masks.append(hidden);exposed_sets.append(exposed)
    distinct=sorted({tuple(e['state']) for e in endpoints})
    # One bit per protected mask. Direct set inclusion constructs the complete
    # failure vector for each actual footprint; OR checks every declared pair.
    # Full endpoints contain original stars or empty, so equal footprints use
    # the same exact inclusion vector within this source, never a sampled mask.
    footprint_failures={}
    for bits in sorted({b for state in distinct for b in state}):
        footprint={e for r,e in enumerate(H) if (bits//2**r)%2}
        failures=0
        for index,exposed in enumerate(exposed_sets):
            if exposed<=footprint:failures |= 2**index
        footprint_failures[bits]=failures
    for state in distinct:
        assert all(footprint_failures[bits]==0 for bits in state)
    static=minimum<total
    assert static==any(c['static'] for c in cr)
    return dict(name=s.get('name',s['family']),source=s,floors=floor,feasible=feasible,minimum=minimum,
                minimizers=[n for n in feasible if sum(n)==minimum],independent=independent,deficient=deficient,
                covers=cr,static=static,endpoints=endpoints,distinct_endpoints=[list(c) for c in distinct],protected_masks=masks,
                hidden_checks=len(distinct)*len(masks))


def verify(data,fixture=False,identity_path=None):
    assert data['schema']=='cover-static-v1' and data['fixture']==fixture
    if identity_path is None:
        assert fixture,'Full verification requires canonical stream'
        iterator=iter(data['records']);handle=None
    else:
        try:handle=gzip.open(identity_path,'rt');iterator=iter(handle)
        except OSError as e:raise AssertionError('Missing identity stream') from e
    digests=[];counts=dict(sources=0,feasible_vectors=0,endpoint_occurrences=0,distinct_endpoints=0,hidden_checks=0)
    try:
        for s in declarations(fixture):
            expected=reconstruct(s)
            try:raw=next(iterator)
            except StopIteration as e:raise AssertionError('Truncated identity stream') from e
            actual=json.loads(raw) if isinstance(raw,str) else raw
            assert actual==expected,'Canonical source record mismatch'
            line=json.dumps(expected,sort_keys=True,separators=(',',':'))+'\n'
            digests.append(hashlib.sha256(line.encode()).hexdigest())
            counts['sources']+=1;counts['feasible_vectors']+=len(expected['feasible'])
            counts['endpoint_occurrences']+=len(expected['endpoints']);counts['distinct_endpoints']+=len(expected['distinct_endpoints'])
            counts['hidden_checks']+=expected['hidden_checks']
        sentinel=object();assert next(iterator,sentinel) is sentinel,'Extra identity record'
    except (OSError,EOFError,json.JSONDecodeError) as e:raise AssertionError('Invalid identity stream') from e
    finally:
        if handle is not None:handle.close()
    assert data['record_sha256']==digests and data['counts']==counts
    if identity_path is not None and 'identity_archive_sha256' in data:
        assert hashlib.sha256(pathlib.Path(identity_path).read_bytes()).hexdigest()==data['identity_archive_sha256']
    return True

if __name__=='__main__':
    source=pathlib.Path(sys.argv[1]);data=json.loads(source.read_text())
    verify(data,identity_path=str(source)+'.identities.jsonl.gz')
    result=dict(accepted=True,counts=data['counts'],certificate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                canonical_sha256=data['identity_archive_sha256'])
    pathlib.Path(sys.argv[2]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
