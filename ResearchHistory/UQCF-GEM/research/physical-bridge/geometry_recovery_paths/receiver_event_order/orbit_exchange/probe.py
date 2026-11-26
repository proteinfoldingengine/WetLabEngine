"""Pure grade-two support orbit: square admission, local majority, and complement paths."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

L = 11
charts = tuple(range(L * L))
pairs = tuple(combinations(charts, 2))
full = (1 << len(charts)) - 1


def point(x, y):
    return x % L + L * (y % L)


def shape(p, q):
    dx, dy = abs(p % L - q % L), abs(p // L - q // L)
    return tuple(sorted((min(dx, L-dx), min(dy, L-dy))))


def encode(group):
    return sum(1 << i for i in group)


def present(m, i):
    return (m >> i) & 1


def transform(p, swap, sx, sy, tx, ty):
    x, y = p % L, p // L
    if swap:
        x, y = y, x
    return point(sx*x+tx, sy*y+ty)


holder = frozenset(p for p in charts if shape(0, p) in ((0,0), (0,1), (1,1), (0,2))
                   or (shape(0, p) in ((2,3), (3,4)) and p != 36 and shape(p, 36) != (0,1)))
leaf = encode(holder)
orbit = [encode(transform(p, *t) for p in holder)
         for t in product((False, True), (-1, 1), (-1, 1), range(L), range(L))]
assert len(orbit) == 968 and len(set(orbit)) == 484 and orbit.count(leaf) == 2
rows = [encode(i for i, m in enumerate(orbit) if present(m, j)) for j in charts]
work = tuple(tuple(4*(v ^ w).bit_count() for w in rows) for v in rows)
levels = sorted({work[i][j] for i, j in pairs})
minimum = levels[0]
edges = tuple((i, j) for i, j in pairs if work[i][j] == minimum)
near = [frozenset(j for j in charts if work[i][j] == minimum) for i in charts]


def carrier(matrix):
    cheapest = min(matrix[i][j] for i, j in pairs)
    links = tuple((i,j) for i,j in pairs if matrix[i][j] == cheapest)
    exact = tuple(tuple(map(Fraction, row)) for row in matrix)
    return build_carrier(Payload(L, Fraction(1), charts, exact, links, ()))


def updated(i, j, mask):
    was = present(leaf, i) ^ present(leaf, j)
    now = present(mask, i) ^ present(mask, j)
    return work[i][j] + 4*(now-was)


def route(order):
    assert len(order) == len(set(order)) == len(charts) and order[0] == 0
    mask, results = leaf, []
    for step, chart in enumerate(order, 1):
        mask ^= 1 << chart
        assert mask != 0  # All other leaves keep their supports. The Pin is common.
        # Off-edge work remains above every old-edge work throughout.
        edge_work = [updated(i, j, mask) for i,j in edges]
        best = min(edge_work)
        count = edge_work.count(best)
        assert (count == len(edges)) == (step == len(charts))
        results.append([chart, mask.bit_count(), best, count])
    assert mask == full ^ leaf
    return results


def majority():
    profile = None
    for p in charts:
        counts = Counter((present(m,p),sum(present(m,n) for n in near[p])) for m in orbit)
        assert all((hits >= 2 if bit else hits <= 2) for bit, hits in counts)
        if profile is None:
            profile = counts
        assert profile == counts
    return [[b,n,c] for (b,n),c in sorted(profile.items())]


def counterleaf_test():
    # Any four-edit handoff needs one counterflip at each actor. The receiver
    # cannot be an original neighbor of 0 because all four already hold leaf.
    catalog = orbit.copy()
    catalog.remove(leaf)
    center_candidates = []
    for i, m in enumerate(catalog):
        sign = 1-2*present(m,0)
        if all(4 + 4*sign*(1-2*present(m,k)) == 0 for k in near[0]):
            center_candidates.append(i)
    assert not center_candidates
    reciprocal = {b: sum(present(m,b) and not present(m,0) for m in catalog)
                  for b in charts if b not in holder}
    return dict(outsiders=len(reciprocal), indexed_reciprocal=sum(reciprocal.values()),
                distinct_reciprocal=sum(reciprocal.values())//2,
                indexed_four_endpoints=len(reciprocal)*len(catalog)**2,
                source_counterflips=len(center_candidates), nominated={b:reciprocal[b] for b in (36,41)})


def read_p1():
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location("original_p1", demos/"v16.23-overlap-descent/engine.py")
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    which = orbit.index(leaf)
    parents = (-1,) + (0,)*len(orbit)
    ambient = tuple(range(len(parents)))
    grades = (1,) + (2,)*len(orbit)
    def record(mask):
        retained = (0,) + tuple(i+1 for i in range(len(orbit)) if present(mask,i))
        vals = mod.push(parents, ambient, retained, grades)
        return len(retained)-1, int(vals[0])
    expected = Counter()
    for j in charts:
        before = rows[j].bit_count()
        assert before == 200
        expected[(before, (rows[j]^(1<<which)).bit_count())] += 1
    records = {j:[record(rows[j]),record(rows[j] ^ (1<<which))] for j in (0,36)}
    assert records[0] == [(200,1537),(199,1539)] and records[36] == [(200,1537),(201,1535)]
    return records


if __name__ == "__main__":
    demos = Path(sys.argv[1]).resolve()
    sys.path[:0] = [str(demos/"v15.42-duality-covariant-transport-repair"),
                    str(demos/"v15.43-certified-response-geometry")]
    from carriers import build_carrier
    from projection import Payload
    assert levels[:2] == [704,1088] and near[0] <= holder
    assert all(shape(i,j) == (1,1) for i,j in edges) and all(len(n)==4 for n in near)
    initial = carrier(work)
    out = sorted(set(charts)-holder)
    others = sorted(holder-{0})
    orders = [[0,*out,*others], [0,*others[:-1],out[-1],others[-1],*reversed(out[:-1])]]
    traces = [route(order) for order in orders]
    complemented = tuple(tuple(updated(i,j,full^leaf) for j in charts) for i in charts)
    assert complemented == work and carrier(complemented).receipt == initial.receipt
    first = tuple(tuple(updated(i,j,leaf^1) for j in charts) for i in charts)
    try:
        carrier(first)
    except ValueError as e:
        assert str(e) == "degree_not_four"
    else:
        raise AssertionError("first cut admitted")
    # A genuine rewiring upper bound when other leaves may be edited.
    b = min(out,key=lambda j:(work[0][j],j))
    swap = [b if j==0 else 0 if j==b else j for j in charts]
    exchanged = tuple(tuple(work[i][j] for j in swap) for i in swap)
    assert (rows[0]^rows[b]).bit_count()*4 == work[0][b] and exchanged != work
    assert carrier(exchanged).baseline.flat
    print(json.dumps(dict(levels=levels, edge_count=len(edges), cycles=len(initial.complex.cycles),
                          automorphisms=len(initial.complex.metric_automorphisms), majority=majority(),
                          four=counterleaf_test(), routes=traces, retained=read_p1(),
                          row_swap=[b,work[0][b]//2]),sort_keys=True))
