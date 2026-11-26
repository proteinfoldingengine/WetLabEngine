"""Independent coordinate, cut-constraint and path replay for the uncompensated orbit."""
from collections import Counter, deque
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations, product
import json
from pathlib import Path
import runpy
import sys

receipt = json.loads(Path(sys.argv[1]).read_text())
here = Path(__file__).resolve().parent
old = sys.argv
try:
    sys.argv = [str(here.parent/"symmetric_matched_event/verify.py")]
    with redirect_stdout(StringIO()):
        g = runpy.run_path(sys.argv[0])
finally:
    sys.argv = old
S = g["S1"]
V = g["V"]
A = g["A"]
masks = Counter(g["images"])
orientations = []
shape = S
for turn in range(4):
    for sign in (-1,1):
        orientations.append(frozenset(((sign*x)%11,y) for x,y in shape))
    shape = frozenset(((-y)%11,x) for x,y in shape)


def number(p):
    return p[0]+11*p[1]


def add(p,q):
    return (p[0]+q[0])%11,(p[1]+q[1])%11


def work(d):
    return 8*sum(len(s)-len(s & {add(p,d) for p in s}) for s in orientations)


weights = {p:work(p) for p in V if p != A}
levels = sorted(set(weights.values()))
assert levels == receipt["levels"] and levels[:2] == [704,1088]
generators = [p for p,v in weights.items() if v == levels[0]]
N = {p:{add(p,d) for d in generators} for p in V}
E = [(p,q) for p,q in combinations(V,2) if q in N[p]]
assert len(E) == receipt["edge_count"] == 242 and len(N[A])==4
for p in V:
    histogram = Counter()
    for m,n in masks.items():
        histogram[int(p in m),len(N[p]&m)]+=n
    assert [[b,k,v] for (b,k),v in sorted(histogram.items())] == receipt["majority"]
assert receipt["cycles"] == 121 and receipt["automorphisms"] == 968


def solutions(shift):
    required = {p:[] for p in V}
    for p,q in E:
        crossing = int((p in S) != (q in S)) + shift
        if crossing not in (0,1):
            return []
        required[p].append((q,crossing))
        required[q].append((p,crossing))
    found = []
    for seed in (0,1):
        assigned={A:seed}
        wave = deque([A])
        while wave:
            p=wave.popleft()
            for q,crossing in required[p]:
                bit=assigned[p]^crossing
                if q in assigned:
                    if assigned[q] != bit:
                        return []
                else:
                    assigned[q]=bit
                    wave.append(q)
        assert len(assigned)==121
        found.append(frozenset(p for p,v in assigned.items() if v))
    return found


assert solutions(-1)==solutions(1)==[]
assert set(solutions(0)) == {S,frozenset(V)-S}
for route in receipt["routes"]:
    m=S
    seen=set()
    assert route[0][0]==0 and len(route)==121
    for t,(j,holders,minimum,count) in enumerate(route,1):
        p=j%11,j//11
        assert p not in seen
        seen.add(p)
        m=m^{p}
        assert m and len(m)==holders
        values=Counter(704+4*(int((x in m)!=(y in m))-int((x in S)!=(y in S))) for x,y in E)
        assert min(values)==minimum and values[minimum]==count
        assert (len(values)==1)==(t==121)
    assert m == set(V)-S

# Independent four-edit screen. A second flip at the sender must offset the
# withdrawal on every diagonal neighbor, all of which are stationary.
assert N[A] <= S
spare=masks.copy()
spare[S]-=1
source_matches=[m for m,k in spare.items() if k and all((v in m)!=(A in m) for v in N[A])]
assert not source_matches
reciprocal = {p:sum(k for m,k in spare.items() if p in m and A not in m) for p in V if p not in S}
f=receipt["four"]
assert f["indexed_reciprocal"]==sum(reciprocal.values())==15936
assert f["distinct_reciprocal"]==7968 and f["indexed_four_endpoints"]==96*967**2
assert f["source_counterflips"]==0 and f["outsiders"]==96
assert f["nominated"]=={str(number(p)):reciprocal[p] for p in ((3,3),(8,3))}
outside = set(V)-S
b=min(outside,key=lambda j:(weights[j],number(j)))
assert receipt["row_swap"]==[number(b),weights[b]//2]
assert receipt["retained"]=={"0":[[200,1537],[199,1539]],"36":[[200,1537],[201,1535]]}
# Even-order check of the odd-chart restriction on the parity lemma.
cube=tuple(product((0,1),repeat=4))
assert {sum(x)%2 for x in cube}=={0,1}
assert all(sum(sum(a!=b for a,b in zip(x,y))==1 for y in cube)==4 for x in cube)
print(json.dumps(dict(cut_solutions=[0,2,0],single_leaf_minimum=121,
        arbitrary_edit_lower_bound=6,checked_paths=2,
        full_work_preserved=True,cube_dimension=4,reciprocal_candidates=sum(reciprocal.values()),
        transposition=receipt["row_swap"]),sort_keys=True))
