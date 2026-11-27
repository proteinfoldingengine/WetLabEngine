"""Inspect receipts emitted by the original campaigns and test tree constructions."""
from collections import Counter
from hashlib import sha1, sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import sys

D26 = 'v16.26-consistency-increment-law'
D27 = 'v16.27-increment-attribution-closure'
PINS = {D26:'c10ac57f988a439144e21898bd2b33ece0838a9b',
        D27:'48f132d141167d9cd85ff79ec41720b5dca4f8bb',
        'v16.23-overlap-descent':'b18f52109ccff9c7dc77542d3b8f3e5d5989102a'}


def pinned(path, expected):
    raw = path.read_bytes()
    assert sha1(b'blob '+str(len(raw)).encode()+bytes(1)+raw).hexdigest() == expected
    return raw


def module(path):
    spec = spec_from_file_location('frozen_'+path.parent.name, path)
    obj = module_from_spec(spec)
    sys.modules[spec.name] = obj
    spec.loader.exec_module(obj)
    return obj


def mask(row):
    return sum(1<<v for v in row)


def archived(v27, reference, log):
    v26 = v27.v26
    old_atom = v26.atomic
    missed = []
    def observe(p, ys, j, leaf):
        d = old_atom(p,ys,j,leaf)
        if int(d['trigger'])!=d['delta_h']:
            missed.append((p,tuple(map(mask,ys)),j,leaf))
        return d
    v26.atomic = observe
    try:
        assert v26.produce(5) == reference
    finally:
        v26.atomic = old_atom
    assert len(missed) == len(set(missed))
    counts = Counter(len(rows) for _,rows,_,_ in missed)
    old_paths = v27.paths
    events = Counter()
    digest = sha256()
    def trace_paths(p,ys,zs):
        paths = old_paths(p,ys,zs)
        words = []
        for path in paths:
            attr = v27.event_map(path)
            assert len(attr)==len(path)
            word = []
            for row in path:
                j,a,t = row['index'],row['leaf'],row['trigger']
                assert attr[j,a] == int(t)
                events[str(t)]+=1
                word.append((j,a,int(t)))
            words.append(tuple(word))
        digest.update((repr((p,tuple(map(mask,ys)),tuple(map(mask,zs)),sorted(words)))+'\n').encode())
        return paths
    v27.paths = trace_paths
    try:
        produced = v27.produce(4)
    finally:
        v27.paths = old_paths
    assert (json.dumps(produced,sort_keys=True)+'\n').encode() == log
    return dict(archived_shapes=len(reference['instances']),atoms=reference['atomic'],
                local_triggers=reference['triggers'],global_rises=reference['strict'],
                masked_by_charts=counts,masked_atoms=sorted(missed),
                endpoints=produced['endpoints'],paths=produced['paths'],path_event_occurrences=events,
                address_and_bit_path_digest=digest.hexdigest())


def ancestors(p,v):
    chain = {v}
    while p[v]>=0:
        v = p[v]
        chain.add(v)
    return chain


def construction(p):
    universe = set(range(len(p)))
    kids = {v:[i for i in universe if p[i]==v] for v in universe}
    branches = [v for v in sorted(universe) if len(kids[v])>=2]
    if len(branches)<2:
        return
    def below(v):
        return {w for w in universe if v in ancestors(p,w)}

    # Two charts suffice for independent branches, or if the upper branch
    # has two other children off the path to the lower target.
    for target in branches:
        for fixed in branches:
            if fixed==target or fixed in below(target):
                continue
            private = [v for v in kids[fixed] if target not in below(v)]
            if len(private)<2:
                continue
            x,y = kids[target][:2]
            a = universe - below(private[1]) - (below(x)-{x})
            b = universe - below(private[0]) - (below(y)-{y})
            return [a,b], [(0,x),(1,y)], target, fixed
    # Nested binary case. The third chart keeps the common pivot after both withdrawals.
    target,fixed = next((a,b) for a in branches for b in branches if a!=b and a in ancestors(p,b))
    w = next(v for v in kids[target] if fixed not in below(v))
    i,j = kids[fixed][:2]
    common = universe-(below(w)-{w})
    return [common-below(i),common-below(j),below(w)|ancestors(p,w)], [(0,w),(1,w)],target,fixed


def route(mod,p,rows,events):
    state=tuple(tuple(sorted(row)) for row in rows)
    path=[]
    for actor,leaf in events:
        d=mod.atomic(p,state,actor,leaf)
        path.append(d)
        state=tuple(map(tuple,d['after']))
    return path


def constructed(v27):
    shapes={}
    for code,p in v27.v26.shapes(7):
        c=construction(p)
        if c is None:
            shapes[code]=0
            continue
        rows,events,parent,frozen=c
        assert len(rows)==len({frozenset(s) for s in rows}) and set.union(*rows)==set(range(len(p)))
        paths=[route(v27.v26,p,rows,order) for order in (events,events[::-1])]
        assert paths[0][-1]['after']==paths[1][-1]['after']
        for path in paths:
            assert [d['trigger'] for d in path]==[False,True]
            assert [d['delta_h'] for d in path]==[0,0]
            assert all(d['h_before']==d['h_after']==2 and d['parent']==parent for d in path)
        assert v27.event_map(paths[0])==v27.event_map(paths[1])
        shapes[code]=len(rows)
    return shapes


def strong_control(v27,p1):
    p=(-1,0,0,1,1)
    rows=((0,1,2,3),(0,1,2,4),(0,2),(0,1,3))
    orders=(((0,2),(1,2),(0,3)),((0,3),(1,2),(0,2)))
    paths=[route(v27.v26,p,rows,order) for order in orders]
    assert paths[0][-1]['after']==paths[1][-1]['after']
    assert v27.event_map(paths[0])==v27.event_map(paths[1])
    assert v27.witness(p,rows,paths[0][-1]['after'],paths) is None
    columns=[]
    for path in paths:
        assert all(d['h_before']==d['h_after']==2 for d in path)
        d=path[1]
        prior,after=d['before'][1],d['after'][1]
        basis=[]
        for i in range(len(p)):
            v=tuple(int(j==i) for j in range(len(p)))
            b=p1.push(p,tuple(range(len(p))),prior,v)
            a=p1.push(p,tuple(range(len(p))),after,v)
            assert p1.push(p,prior,after,b)==a
            basis.append([list(map(int,b)),list(map(int,a))])
        columns.append(basis)
    assert columns[0]==columns[1]
    assert [p[1]['trigger'] for p in paths]==[True,False]
    return dict(orders=orders, basis_columns=columns[0], receipts=paths)


if __name__=='__main__':
    demos=Path(sys.argv[1])
    for name,h in PINS.items():
        pinned(demos/name/'engine.py',h)
    v27=module(demos/D27/'engine.py')
    p1=module(demos/'v16.23-overlap-descent/engine.py')
    ref=json.loads(pinned(demos/D26/'evidence/PRODUCTION.json','25e15faf44bb59c77cdd48abf7c8473395c1ae04'))
    log=pinned(demos/D27/'completion/evidence/historical-producer.log','84ac51dc629da88adf84549a3c3a139f612c3cc6')
    print(json.dumps(dict(archive=archived(v27,ref,log),tree_minima=constructed(v27),
                          fixed_position=strong_control(v27,p1)),sort_keys=True,indent=2))
