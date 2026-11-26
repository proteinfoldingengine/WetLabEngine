"""Test the cover lemma on the native scalar receipts of small transitive star inputs."""
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
import json
import sys

spec=spec_from_file_location("atom",Path(sys.argv[1])/"v16.26-consistency-increment-law/engine.py")
atom=module_from_spec(spec)
spec.loader.exec_module(atom)


def as_views(n,supports):
    return [[0]+[i+1 for i,group in enumerate(supports) if p in group] for p in range(n)]


def witnesses(n, fixed):
    candidates=(frozenset(c) for k in range(1,n+1) for c in combinations(range(n),k))
    return {c for c in candidates if all(c&s for s in fixed)}


counts = dict(orbits=0, states=0, deletions=0, matching_endpoint_families=0)
for n in range(3,6):
    points=frozenset(range(n))
    for width in range(1,n):
        fixed=[frozenset((i+t)%n for t in range(width)) for i in range(n)]
        parents=[-1]+[0]*(len(fixed)+1)
        all_covers=witnesses(n,fixed)
        optimum=min(map(len,all_covers))
        counts["orbits"]+=1
        for k in range(1,n+1):
            for group in combinations(range(n),k):
                active=frozenset(group)
                views=as_views(n,[*fixed,active])
                assert atom.h(parents,views)==atom.tau_at(parents,views,0)==optimum
                counts["states"]+=1
                for p in group if k>1 else ():
                    result=atom.atomic(parents,views,p,len(fixed)+1)
                    assert result["h_before"]==result["h_after"]==optimum
                    assert result["tau_before"]==result["tau_after"]==optimum
                    assert result["delta_h"]==0 and result["trigger"] is False
                    counts["deletions"]+=1
        if any(s.isdisjoint(fixed[0]) for s in fixed):
            assert witnesses(n,[*fixed,fixed[0]])==witnesses(n,[*fixed,points-fixed[0]])==all_covers
            counts["matching_endpoint_families"]+=1
control=atom.atomic([-1,0,0],as_views(2,[{0},{0,1}]),0,2)
assert (control["tau_before"],control["tau_after"],control["delta_h"],control["trigger"])==(1,2,1,True)
print(json.dumps(dict(counts=counts,broken_symmetry_control=[1,2,1,True]),sort_keys=True))
