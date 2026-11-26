"""Count a specified family of equal-work records with the complete exterior fixed."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
from math import comb, prod
import json

# Original 11x11 coordinates from symmetric_matched_event/verify.py, centered at 0.
ARCHIVE = ((0,0),(0,1),(0,2),(0,9),(0,10),(1,0),(1,1),(1,10),(2,0),(2,8),
           (3,7),(3,9),(4,8),(7,3),(7,8),(8,2),(8,4),(8,7),(8,9),(9,0),(9,3),
           (9,8),(10,0),(10,1),(10,10))
S = tuple(((x+5)%11-5, (y+5)%11-5) for x,y in ARCHIVE)


def bit(p, x, y):
    return 1 << ((x % p) + p * (y % p))


def images(p):
    return [sum(bit(p, x+a, y+b) for x,y in S) for a,b in product(range(p), repeat=2)]


def region(p, side):
    # The derived axes are (1,1) and (1,-1) in archive coordinates.
    return sum(bit(p, u+v, u-v) for u,v in product(range(side), repeat=2))


def classes(templates, outside):
    blocks = defaultdict(list)
    for slot, mask in enumerate(templates):
        blocks[mask & outside].append(slot)
    return list(blocks.values())


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def chart_rows(columns, n):
    rows = [0] * n
    for index, col in enumerate(columns):
        marker = 1 << index
        for chart in bits(col):
            rows[chart] |= marker
    return rows


def work(rows):
    return [4 * (a ^ b).bit_count() for a,b in combinations(rows, 2)]


def assign(templates, blocks, full, choose_last):
    columns = templates.copy()
    for slots in blocks:
        k = len(slots)//2
        chosen = slots[-k:] if choose_last and k else slots[:k]
        selected = set(chosen)
        remaining = [i for i in slots if i not in selected]
        for index, (dest, src) in enumerate(zip(slots, chosen + remaining)):
            columns[dest] = templates[src] ^ (full if index < k else 0)
    return columns


def exact_fixture():
    p, n = 11, 121
    full = (1 << n) - 1
    templates = images(p)
    archive = list(templates)
    for swap, sx, sy in product((False,True), (1,-1), (1,-1)):
        if (swap,sx,sy) == (False,1,1):
            continue
        shape = [(sx*(y if swap else x), sy*(x if swap else y)) for x,y in S]
        archive.extend(sum(bit(p,x+a,y+b) for x,y in shape)
                       for a,b in product(range(p),repeat=2))
    assert len(archive) == 968 and len(set(archive)) == 484
    prior = chart_rows(archive, n)
    d = work(prior)
    assert {row.bit_count() for row in prior} == {200}
    assert len(d) == 7260
    # All ten archived levels in the sibling orbit_exchange/raw.json.
    assert sorted(set(d)) == [704,1088,1152,1216,1280,1312,1344,1376,1408,1472]
    for chart, row in enumerate(prior):
        near = {j for j,other in enumerate(prior) if 4*(row ^ other).bit_count() == 704}
        x, y = chart % p, chart // p
        assert near == {((x+a)%p) + p*((y+b)%p) for a,b in product((1,-1), repeat=2)}
        assert sum((row ^ other).bit_count() for other in prior) == 25*968+(121-50)*200
    summary = []
    for r in range(1, p):
        inside = region(p,r)
        blocks = classes(templates, full ^ inside)
        family = prod(comb(len(g), len(g)//2) for g in blocks)
        summary.append(dict(side=r, charts_inside=r*r, crossing_edges=4*r,
                            classes=len(blocks), named_class_sizes=dict(sorted(Counter(map(len,blocks)).items())),
                            profiles=family))
    # Select the smallest square with a positive result; use the last as a second control.
    witnesses = []
    for row in (next(item for item in summary if item['profiles'] > 1), summary[-1]):
        r = row['side']
        outside = full ^ region(p,r)
        blocks = classes(templates, outside)
        left = assign(templates, blocks, full, False) + archive[len(templates):]
        right = assign(templates, blocks, full, True) + archive[len(templates):]
        a, b = (chart_rows(cols,n) for cols in (left,right))
        assert work(a) == work(b) == d
        assert [m.bit_count() for m in left] == [m.bit_count() for m in right]
        assert all(a[i] == b[i] for i in bits(outside))
        count_delta = [y.bit_count()-x.bit_count() for x,y in zip(a,b)]
        assert any(count_delta) and all(v % 2 == 0 for v in count_delta)
        assert sum(count_delta) == 0
        additions = sum((y & ~x).bit_count() for x,y in zip(left,right))
        removals = sum((x & ~y).bit_count() for x,y in zip(left,right))
        assert additions == removals
        # Bare incidence path. Add before removing, with no outside writes.
        current = left.copy()
        for add in (True,False):
            for slot, target in enumerate(right):
                edits = target & ~current[slot] if add else current[slot] & ~target
                for chart in bits(edits):
                    assert not (outside >> chart) & 1
                    current[slot] ^= 1 << chart
                    assert current[slot] != 0
        assert current == right
        # A mismatched complement is invisible to work but violates a leaf total.
        bad_columns = left.copy()
        bad_columns[0] ^= full
        bad = chart_rows(bad_columns,n)
        assert work(bad) == d and bad_columns[0].bit_count() != left[0].bit_count()
        assert all(bad[i] != a[i] for i in bits(outside))
        bad = a.copy()
        bad[next(bits(outside))] ^= 1
        assert work(bad) != d
        witnesses.append(dict(side=r, leaf_sizes=dict(sorted(Counter(m.bit_count() for m in left).items())),
                              identical_exterior_rows=outside.bit_count(), interior_count_changes=sum(bool(v) for v in count_delta),
                              count_difference_histogram=dict(sorted(Counter(count_delta).items())),
                              additions=additions, removals=removals,
                              full_work_sha256=sha256(json.dumps(d,separators=(',',':')).encode()).hexdigest()))
    return summary,witnesses


def native_axes(p):
    overlaps = Counter()
    for swap,sx,sy in product((False,True),(1,-1),(1,-1)):
        coords = [(sx*(y if swap else x),sy*(x if swap else y)) for x,y in S]
        overlaps.update(((x-u)%p,(y-v)%p) for x,y in coords for u,v in coords)
    del overlaps[0,0]
    peak = max(overlaps.values())
    assert {q for q,h in overlaps.items() if h == peak} == {(a%p,b%p) for a,b in product((1,-1),repeat=2)}
    assert sorted(set(overlaps.values()),reverse=True)[:2] == [112,64]


def scaling(p):
    native_axes(p)
    side = 3*p//4
    half = p//2
    inv2 = (p+1)//2
    # Count the zero-exterior class directly from native template offsets.
    offsets = [((x+y)*inv2 % p,(x-y)*inv2 % p) for x,y in S]
    count = sum(all((u+a)%p < side and (v+b)%p < side for a,b in offsets)
                for u,v in product(range(p),repeat=2))
    guaranteed = max(0,side-half-8)**2
    assert count >= guaranteed
    inset_count = sum(all(1 <= (u+a)%p < side-1 and 1 <= (v+b)%p < side-1
                          for a,b in offsets)
                      for u,v in product(range(p),repeat=2))
    assert inset_count >= max(0,side-half-10)**2
    ways = comb(count,count//2)
    return dict(p=p, side=side, crossing_edges=4*side, exterior_charts=p*p-side*side,
                interior_translates=count, proved_minimum_translates=guaranteed,
                strictly_interior_translates=inset_count,
                floor_log2_profiles_from_interior_translates=ways.bit_length()-1)


if __name__ == "__main__":
    table,witnesses = exact_fixture()
    print(json.dumps(dict(squares=table,witnesses=witnesses,
                          scalable=[scaling(p) for p in (19,31,43,59,83,127,251)]),
                     indent=2,sort_keys=True))
