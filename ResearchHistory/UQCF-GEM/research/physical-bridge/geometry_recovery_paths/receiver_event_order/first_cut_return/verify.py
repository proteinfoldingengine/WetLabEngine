"""Reconstruct each legal first cut from the coordinate support and signed cut differences."""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
import json
from pathlib import Path
import runpy
import sys

here = Path(__file__).resolve().parent
provided = json.loads(Path(sys.argv[1]).read_text())
# The historical coordinate verifier has its own optional receipt argument.
argv = sys.argv
try:
    sys.argv = [str(here.parent / "symmetric_matched_event/verify.py")]
    with redirect_stdout(StringIO()):
        parent = runpy.run_path(sys.argv[0])
finally:
    sys.argv = argv
V, A, prior, chosen, delta = (parent[k] for k in ("V", "A", "prior", "chosen", "part_delta"))
neighbors = {p: chosen(p) for p in V}
images = Counter(parent["images"])


def number(p):
    return p[0] + 11 * p[1]


def encode(m):
    return hex(sum(1 << number(p) for p in m))


def first_case(first):
    reduced = first - {A}
    all_leaves = images.copy()
    all_leaves[first] -= 1
    all_leaves[reduced] += 1
    old = {p: prior(A, p) + delta(first, reduced, A, p) for p in V if p != A}
    remote = []
    for b in V:
        if b == A or b in neighbors[A] or neighbors[b] & neighbors[A]:
            continue
        if all(old[p] >= 0 and ((old[p] == 0) == (p in neighbors[b])) for p in old if p != b):
            remote.append(b)
    outcomes = []
    for j in [A, *remote]:
        for leaf, copies in all_leaves.items():
            changed = leaf ^ {j}
            def val(p, q):
                first_value = old[q] if p == A else old[p] if q == A else prior(p, q)
                return first_value + delta(leaf, changed, p, q)
            if not all(val(j, p) == 0 for p in neighbors[A]):
                continue
            if any(val(j, p) <= 0 for p in V if p != j and p not in neighbors[A]):
                continue
            if j == A and leaf == reduced:
                status = "prior carrier"
            else:
                swap = lambda p: j if p == A else A if p == j else p
                status = "admitted"
                for p in V:
                    neigh = [swap(q) for q in neighbors[swap(p)]]
                    pairs = {k: val(*k) for k in combinations(neigh, 2)}
                    tops = [set(k) for k, value in pairs.items() if value == max(pairs.values())]
                    if len(tops) != 2 or tops[0] & tops[1]:
                        status = "opposites_ambiguous"
                        break
            outcomes.append([number(j), encode(leaf), 1 if j not in leaf else -1, copies, status])
    return sorted(number(j) for j in remote), sorted(outcomes)


expected = {encode(m): m for m in images if A in m}
rows = provided["starts"]
assert len(rows) == len(expected) == 100 and {r["mask"] for r in rows} == expected.keys()
successes = {}
alternatives = Counter()
for row in rows:
    m = expected[row["mask"]]
    remote, outcomes = first_case(m)
    assert row["multiplicity"] == images[m] == 2
    assert row["possible_remote"] == remote and sorted(row["answers"]) == outcomes
    undos = [x for x in outcomes if x[0] == 0]
    assert undos == [[0, encode(m - {A}), 1, 1, "prior carrier"]]
    gains = [x for x in outcomes if x[-1] == "admitted"]
    if gains:
        only, = gains
        assert only[1:4] == [encode(m - {A}), 1, 1]
        successes[m] = only[0]
    alternatives.update(x[-1] for x in outcomes)

# Cross-check the unique source for a single leaf directly before a cut occurs.
leaf = parent["S1"]
cores = {p for p in leaf if neighbors[p] <= leaf}
centers = {p for p in cores if neighbors[p] <= cores}
active = {}
for p in leaf:
    translated = frozenset(((x-p[0]) % 11, (y-p[1]) % 11) for x, y in leaf)
    if translated in successes:
        b = successes[translated]
        active[p] = ((p[0]+b%11) % 11, (p[1]+b//11) % 11)
assert len(cores) == 5 and centers == set(active) == {A} and active[A] == (3, 3)
assert sorted(successes.values()) == [36, 41, 91, 96]
assert provided["consumer"] == [["prior", True, True, None], ["cut36", True, False, "degree_not_four"],
                               ["cut41", True, False, "degree_not_four"]]
print(json.dumps(dict(fixed_source_indexed=200, fixed_source_masks=100,
                      transferable_indexed=2*len(successes), transferable_masks=len(successes),
                      labels=sorted(successes.values()), degree_survivors=dict(alternatives),
                      full_one_hop_balls=len(cores), full_two_hop_balls=len(centers),
                      eligible_holders=len(active), total_holders=len(leaf)), sort_keys=True))
