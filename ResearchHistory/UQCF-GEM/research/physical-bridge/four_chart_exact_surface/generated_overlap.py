"""Run the two-visit experiment against the pinned v16.53 demo directory."""
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

demo = Path(sys.argv[1]).resolve()
for file, expected in {
    "producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "cover.py": "7680cbacb22eac984f5377ad0b679e95b4632785",
    "feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
    "coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
}.items():
    data = (demo / file).read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected
sys.path.insert(0, str(demo))
import producer
import verifier

leaf = ()
fork = (leaf, leaf)
inner = (fork, fork, fork)
tree = (inner, leaf, leaf, leaf)
profile = [3, 2, 1, 1, 1]
ordered = (0, 1, 2, 3)
roots = (2, 5, 8)
descendants = range(2, 11)
# Each tuple gives the support of the fork root and the common support of its two leaves.
forks = {"A": ((2,), (2,)), "B": ((2, 3), (2,)), "C": ((3,), (3,))}


def prepare(extra, names):
    supports = [ordered, (1, 2, 3) if extra else (2, 3)]
    for name in names:
        root, tips = forks[name]
        supports.extend((root, tips, tips))
    supports.extend(((0,), (1,), (2,)))
    return [sum(1 << i for i, s in enumerate(supports) if label in s) for label in ordered]


def holders(state, site):
    return {j for j, row in enumerate(state) if row & (1 << site)}


def candidates(state):
    return [(i, j, x) for i, j in combinations(range(3), 2)
            for x in sorted(holders(state, roots[i]) & holders(state, roots[j]))]


def edits(path):
    moves = []
    for before, after in zip(path, path[1:]):
        diff = [(j, a ^ b) for j, (a, b) in enumerate(zip(before, after)) if a != b]
        assert len(diff) == 1
        label, bit = diff[0]
        assert bit.bit_count() == 1
        moves.append((label, bit.bit_length() - 1, bool(after[label] & bit)))
    return moves


def capture(start, order):
    visits, clearances = [], []
    def watch(frame, event, result):
        local = frame.f_locals
        if frame.f_code is producer.normalize.__code__ and local["t"] == inner:
            outer = frame.f_back.f_locals
            if event == "call":
                visits.append(dict(index=len(outer["path"])-1, state=outer["current"][:],
                                   labels=list(outer["labels"])))
            elif event == "return":
                visits[-1]["moves"] = len(result) - 1
        if frame.f_code is producer._normalize.__code__ and local["t"] == inner and event == "return":
            visits[-1]["trace"] = list(local["trace"])
        if frame.f_code is producer.clear_role.__code__ and local["child"] == 1:
            if event == "call":
                clearances.append(dict(x=local["x"], y=local["y"], state=local["state"][:],
                                       offset=len(local["path"])-1))
            elif event == "return":
                c = clearances[-1]
                c["path"] = local["path"][c["offset"]:]
    previous = sys.getprofile()
    sys.setprofile(watch)
    try:
        path = producer.normalize(start, tree, 4, profile, order)
    finally:
        sys.setprofile(previous)
    return path, visits, clearances


def check_run(extra, names, order, default=False):
    start = prepare(extra, names)
    path, visits, clearances = capture(start, order)
    # Relabel the independent verifier's canonical endpoint into the tested palette.
    expected = verifier.model(tree, profile, 4)[2]
    endpoint = [expected[order.index(i)] for i in ordered]
    peak = verifier.path_check(tree, 4, profile, path, start, endpoint)
    assert len(visits) == 2 and len(candidates(start)) == 2
    for visit in visits:
        state = visit["state"]
        assert state == path[visit["index"]]
        selection = visit["trace"][0]
        i, j = selection["pair"]
        label = visit["labels"][selection["label"]]
        assert (i, j, label) in candidates(state)
    second = visits[1]
    assert len(candidates(second["state"])) == 1
    assert all(t["end"] == 0 for t in second["trace"] if t["kind"] == "child_normalization")
    first = visits[0]
    first_end = path[first["index"] + first["moves"]]
    first_palette = [j for j in order if j in holders(start, 1)]
    assert [holders(first_end, site) for site in roots] == [
        {first_palette[0]}, {first_palette[1]}, {first_palette[0]}]
    changes = {}
    for c in clearances:
        x, y, state = c["x"], c["y"], c["state"]
        sites = [i for i in descendants if x in holders(state, i)]
        moves = edits(c["path"])
        assert moves == [(y, i, True) for i in sites] + [(x, i, False) for i in reversed(sites)]
        at = next(i for i, frame in enumerate(path) if frame == state and path[i:i+len(c["path"])] == c["path"])
        assert at + len(moves) < second["index"]
        assert edits(path[at+len(moves):at+len(moves)+2]) == [(x, 1, False)]
        if (x,y) != (2,0):
            continue
        peers = tuple(names[n] for n,r in enumerate(roots) if r in sites)
        assert len(sites) == 3 * len(peers)
        changes[(x,y)] = peers
        if default:
            # Test every unused local replacement under the identical pre-clearance holdings.
            spare = holders(state, 1) - set.union(*(holders(state, i) for i in descendants))
            assert spare == ({0,3} if extra else {0,1})
            for other in spare:
                alternate = [state[:]]
                producer.clear_role(state[:], producer.layout(tree), 1, x, other, alternate)
                assert edits(alternate) == [(other,i,True) for i in sites] + [(x,i,False) for i in reversed(sites)]
                assert all(verifier.profile_check(tree, 4, s)[1:] == profile[1:] for s in alternate)
            print("clearance", extra, "frames", at, at+len(moves), "receivers", peers,
                  "sites", sites, "available labels", sorted(spare))
    generated = candidates(second["state"])[0]
    assert (generated[0], generated[1]) == (0,2)
    # For some layouts the first/third named pairing already exists at entry.
    if default:
        assert not any((a,b)==(0,2) for a,b,x in candidates(start))
        assert changes[(2,0)] == (("B",) if extra else ("A","C"))
        assert generated[2] == int(extra)
        assert second["moves"] == (18 if extra else 0)
        assert peak == 1
        print("source bit", extra, "entry", start, "first and second input overlaps",
              candidates(start), [generated], "second visit frame", second["index"],
              "second visit edits", second["moves"], "endpoint", endpoint)
    return changes.get((2,0)), generated[2], second["moves"]


def check_canonical_overlaps():
    tested = 0
    for widths in product(range(1, 17), repeat=3):
        size = sum(widths)
        palette_size = max(max(widths), (size+1)//2)
        children = [set(a) for a in producer.palettes(list(range(palette_size)), widths, 2)]
        assert tuple(map(len, children)) == widths
        assert not set.intersection(*children) and len(set.union(*children)) == palette_size
        count = sum(len(a & b) for a, b in combinations(children, 2))
        assert count == size-palette_size
        assert (count == 1) == (widths == (1, 1, 1))
        if count == 1:
            assert children == [{0}, {1}, {0}]
        tested += 1
    print("Canonical ternary width triples checked:", tested)


def main():
    check_canonical_overlaps()
    total = Counter()
    default_pairs = []
    for names in permutations("ABC"):
        for order in permutations(ordered):
            before, after = (prepare(extra, names) for extra in (False, True))
            assert [a^b for a,b in zip(before, after)] == [0,2,0,0]
            outcomes = [check_run(extra, names, order, names==tuple("ABC") and order==ordered)
                        for extra in (False, True)]
            (a, x, m), (b, y, n) = outcomes
            total["paired comparisons"] += 1
            if a is not None and b is not None:
                total["both emit 2 to 0"] += 1
                if set(a) != set(b):
                    total["both emit 2 to 0 at different named receivers"] += 1
            total["second overlap labels differ"] += int(x != y)
            total["second edit counts differ"] += int(m != n)
            if order == ordered:
                default_pairs.append((names, a, b))
                assert a == (names[0], names[2]) and b == (names[1],)
    print("Default palette, transported peer names and cleared groups:", default_pairs)
    assert tuple(total[k] for k in ("paired comparisons", "both emit 2 to 0",
                                    "both emit 2 to 0 at different named receivers",
                                    "second overlap labels differ", "second edit counts differ")) == (144, 18, 6, 36, 36)
    print("All paired counts:", json.dumps(dict(total), sort_keys=True))


if __name__ == "__main__":
    main()
