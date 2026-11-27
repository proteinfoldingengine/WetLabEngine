"""Audit the nested v16.53 writer. Argument is the pinned v16.53 demo directory."""
import hashlib
import json
import sys
from collections import Counter
from itertools import permutations
from pathlib import Path
from random import Random

demo = Path(sys.argv[1]).resolve()
for name, expected in {
    "producer.py": "0501a1b32c0a660646ff95ecbb8a37a8f2e04b80",
    "verifier.py": "54e23706c170d0bb82c1b78161290145b6b99af7",
    "coverage.py": "e90576a0285357f62ca2f9d9cac872b2a226e823",
    "feasibility.py": "9e995e21c9a477034a2fd4be615e28a2551b0bf9",
}.items():
    data = (demo / name).read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected
sys.path.insert(0, str(demo))
import producer
import verifier

alphabet = tuple(range(12))
peers = ("A", "B", "C")
branch_names = ("outer", "second", "third", "parent", *peers)
bases = {"A": (2,3,4), "B": (4,5,6), "C": (2,6,7)}
orders = tuple(permutations(range(3)))
fork = ((), (), ())
peer_tree = (fork, fork, fork)


def prepare(source, wide, traversal):
    # Types depend only on topology. Compute the hitting profile from the actual rows below.
    sites = {}
    sets = {}
    spec = {
        "outer": (alphabet, ("second", "source", "outer_leaf")),
        "second": (range(10), ("third", "key2", "second_leaf")),
        "third": (range(9), ("parent", "key3", "third_leaf")),
        "parent": (range(8), peers),
        "source": ((*source, 11), ()), "key2": ((2,), ()), "key3": ((3,), ()),
        "outer_leaf": ((10,), ()), "second_leaf": ((9,), ()), "third_leaf": ((8,), ()),
    }
    for peer, base in bases.items():
        tips = tuple(peer + str(i) for i in range(3))
        spec[peer] = (base, tips)
        labels = base if peer == wide else (base[0],) * 3
        spec.update({tip: ((j,), ()) for tip, j in zip(tips, labels)})

    def build(name):
        sites[name] = len(sites)
        support, children = spec[name]
        sets[sites[name]] = support
        if not children:
            return ()
        return tuple(build(children[i]) for i in traversal[branch_names.index(name)])

    tree = build("outer")
    state = [sum(1 << v for v, s in sets.items() if j in s) for j in alphabet]
    q = verifier.profile_check(tree, len(alphabet), state)
    nodes, targets, widths = producer.data(tree, q)
    assert all(producer.coordinate(state, nodes[v]) == h for v, h in targets.items())
    assert {p: widths[sites[p]] for p in peers} == {p: 3 if p == wide else 1 for p in peers}
    return tree, state, q, sites


def capture(tree, state, q, palette):
    visits = []
    def observe(frame, event, returned):
        if event != "return" or frame.f_code is not producer.normalize.__code__:
            return
        if frame.f_locals["t"] != peer_tree:
            return
        caller = frame.f_back
        end = len(returned) - 1
        labels = list(range(frame.f_locals["k"]))
        while caller is not None and caller.f_code is producer._normalize.__code__:
            end += len(caller.f_locals["path"]) - 1
            labels = [caller.f_locals["labels"][j] for j in labels]
            caller = caller.f_back.f_back
        visits.append((end - len(returned) + 1, end, labels))

    previous = sys.getprofile()
    sys.setprofile(observe)
    try:
        path = producer.normalize(state, tree, len(palette), q, order=palette)
    finally:
        sys.setprofile(previous)
    visit, = visits
    return path, visit


def at(state, site):
    return tuple(j for j, mask in enumerate(state) if mask & (1 << site))


def check_run(source, wide, traversal, palette):
    tree, start, q, sites = prepare(source, wide, traversal)
    path, (begin, end, local_order) = capture(tree, start, q, palette)
    selected = next(j for j in palette if j in source)
    assert local_order[:3] == [3, 2, selected]
    nodes = producer.layout(tree)
    bit = 1 << sites[wide]
    others = [p for p in peers if p != wide]
    other_region = sum(1 << v for p in others for v in producer.vertices(nodes, sites[p]))
    region = sum(1 << v for p in peers for v in producer.vertices(nodes, sites[p]))
    assert not (start[0] | start[1]) & region
    first = next(i for i in range(1, end + 1) if (path[i][0] | path[i][1]) & region)
    assert path[first][selected] ^ path[first-1][selected] == bit
    assert not any((s[0] | s[1]) & other_region for s in path[:end+1])
    assert at(path[end], sites[wide]) == tuple(sorted((2, 3, selected)))
    assert sum(bool(path[end][selected] & (1 << i)) for i in nodes[sites[wide]]) == 1
    assert {at(path[end], sites[p]) for p in others} == {(2,), (3,)}
    canonical = verifier.model(tree, q, len(palette))[2]
    endpoint = [canonical[palette.index(j)] for j in alphabet]
    peak = verifier.path_check(tree, len(palette), q, path, start, endpoint)
    return start, sites, q, endpoint, (first, end, len(path)-1, peak), selected


def scenarios():
    default = (orders[0],) * len(branch_names)
    yield default, alphabet
    yield default, alphabet[::-1]
    # Change the enumeration at exactly one vertex at a time.
    for node in range(len(branch_names)):
        for local in orders[1:]:
            setting = list(default)
            setting[node] = local
            yield tuple(setting), alphabet
    # Cross every order of the three candidate receivers with all orders of 0,1,2,3.
    # Order the other eight labels and the other vertices independently with a fixed seed.
    rng = Random(53178)
    for destination_order in orders:
        for prefix in permutations(range(4)):
            rest = iter(rng.sample(alphabet[4:], 8))
            priority = iter(prefix)
            slots = set(rng.sample(range(12), 4))
            palette = tuple(next(priority) if i in slots else next(rest) for i in range(12))
            setting = [rng.choice(orders) for _ in branch_names]
            setting[3] = destination_order
            yield tuple(setting), palette


def exhaustive_local():
    checked = 0
    for destination_order in orders:
        traversal = [orders[0]] * len(branch_names)
        traversal[3] = destination_order
        for wide in peers:
            tree, full, _, sites = prepare((0,), wide, traversal)
            region = producer.vertices(producer.layout(tree), sites["parent"])
            local = [sum(1 << i for i, v in enumerate(region) if full[j] & (1 << v)) for j in range(8)]
            q = verifier.profile_check(peer_tree, 8, local)
            wide_bit = 1 << region.index(sites[wide])
            other_bits = sum(1 << region.index(sites[p + suffix]) for p in peers if p != wide
                             for suffix in ("", "0", "1", "2"))
            for x in (0,1):
                prefix = (3,2,x)
                for rest in permutations(j for j in range(8) if j not in prefix):
                    path = producer.normalize(local, peer_tree, 8, q, prefix + rest)
                    # Both labels are already present at the local root (bit zero).
                    observed = next(s for s in path if (s[0] | s[1]) & ~1)
                    assert observed[x] == 1 | wide_bit and observed[1-x] == 1
                    assert not any((s[0] | s[1]) & other_bits for s in path)
                    assert path[-1][x] & wide_bit and not path[-1][1-x] & wide_bit
                    checked += 1
    assert checked == 4320
    print("All effective receiving palettes and candidate orders, isolated stock calls:", checked)


def main():
    exhaustive_local()
    settings = list(scenarios())
    totals = Counter()
    for index, (traversal, palette) in enumerate(settings):
        reference = None
        for wide in peers:
            arms = [check_run((x,), wide, traversal, palette) for x in (0,1)]
            a, b = arms
            source_bit = 1 << a[1]["source"]
            assert [x ^ y for x,y in zip(a[0], b[0])] == [source_bit, source_bit] + [0]*10
            assert a[2:4] == b[2:4] and (a[5], b[5]) == (0,1)
            if reference is not None:
                tips = {a[1][p+str(i)] for p in peers for i in range(3)}
                changed = set(v for v in a[1].values() if at(a[0], v) != at(reference, v))
                assert changed and changed <= tips
            reference = a[0]
            totals["matched pairs"] += 1
            for arm in arms:
                totals["verified whole paths"] += 1
                totals["unit-excursion paths"] += int(arm[4][-1] == 1)
            if index == 0:
                print("Default layout, wide peer", wide, "source 0/1 (first gain, return, final frame, peak)",
                      [arm[4] for arm in arms])
    print("Enumeration settings", len(settings), "counts", dict(totals))
    assert totals["matched pairs"] == 543 and totals["verified whole paths"] == 1086

    default = (orders[0],) * len(branch_names)
    # Same receiving subtree, with the inherited (3,2,0) priority directly varied.
    tree, full, _, sites = prepare((0,), "A", default)
    region = producer.vertices(producer.layout(tree), sites["parent"])
    local = [sum(1 << i for i, v in enumerate(region) if full[j] & (1 << v)) for j in range(8)]
    q = verifier.profile_check(peer_tree, 8, local)
    for prefix, expected_peers in [((0,3,2), {"A","B"}), ((3,2,0), {"A"}), ((3,2,4,0), set())]:
        palette = prefix + tuple(j for j in range(8) if j not in prefix)
        route = producer.normalize(local, peer_tree, 8, q, palette)
        canonical = verifier.model(peer_tree, q, 8)[2]
        verifier.path_check(peer_tree, 8, q, route, local, [canonical[palette.index(j)] for j in range(8)])
        holding = {p for p in peers if route[-1][0] & (1 << region.index(sites[p]))}
        assert holding == expected_peers
        print("Isolated receiver control, rank of label 0 (one-based)", palette.index(0)+1,
              "peers retaining it", sorted(holding))
    for palette in (alphabet, alphabet[::-1]):
        arm = check_run((0,1), "A", default, palette)
        assert arm[-1] == (0 if palette == alphabet else 1)
        assert arm[0][0] == arm[0][1]
        for x in (0, 1):
            tree, child, q, sites = prepare((x,), "A", default)
            diff = [a ^ b for a, b in zip(arm[0], child)]
            assert diff[1-x] == 1 << sites["source"] and sum(bit.bit_count() for bit in diff) == 1
            assert verifier.profile_check(tree, len(alphabet), arm[0]) == q
        print("Two-candidate source, first/last global label", palette[0], palette[-1],
              "actual first marker written to A", arm[-1])


def example_trace():
    arms = []
    for x in (0, 1):
        tree, start, q, sites = prepare((x,), "A", (orders[0],) * len(branch_names))
        path, (begin, end, labels) = capture(tree, start, q, alphabet)
        raw = json.dumps(path, separators=(",", ":")).encode()
        arms.append({"source": x, "profile": q, "local_palette": labels, "entry_frame": begin,
                     "return_frame": end, "raw_masks_through_return": path[:end+1],
                     "whole_path_frames": len(path), "final_masks": path[-1],
                     "whole_path_compact_json_sha256": hashlib.sha256(raw).hexdigest()})
    print(json.dumps({"wide_peer": "A", "sites": sites, "arms": arms}, separators=(",", ":")))


if __name__ == "__main__":
    if sys.argv[2:] == ["--trace"]:
        example_trace()
    else:
        main()
