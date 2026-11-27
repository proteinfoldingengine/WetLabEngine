"""Replay the v16.51 writer on four matched source states. Argument: v16.51 demo directory."""
import gzip
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

demo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(demo))
pins = {
    demo / "producer.py": "1fe52278ce24fe01756eac666add9681e88318d5",
    demo / "verifier.py": "af727ef01d1b4bf7d0f61c61be51a2ffcdb77035",
    demo / "coverage.py": "973244d0eb8a48bcb2464870377139cf4e9870c6",
    demo.parent / "v16.50-recursive-binary-composition/producer.py": "44eb38cc3dff9d121fc634cd38c597acfc3f04c6",
}


def git_blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


for file, expected in pins.items():
    assert git_blob(file.read_bytes()) == expected

import producer
import verifier

tree = producer.T
profile = [2, 1, 1, 1]
alphabet = tuple(range(7))
blocks = ("source", "left", "right")
left = frozenset((0, 1, 4))
right = frozenset((2, 3, 5))


def prepare(markers, layout):
    roots = {"source": {6, *markers}, "left": left, "right": right}
    private = {"source": 6, "left": 4, "right": 5}
    supports = [alphabet]
    for block in layout:
        supports.extend((roots[block], {private[block]}, {private[block]}))
    return [sum(1 << site for site, holders in enumerate(supports) if label in holders)
            for label in alphabet]


def label_at(raw, site):
    return tuple(j for j, mask in enumerate(raw) if mask >> site & 1)


def check_corpus():
    doc = producer.produce()
    raw = (json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n").encode()
    archive = gzip.compress(raw, compresslevel=9, mtime=0)
    assert git_blob(archive[:9] + bytes([3]) + archive[10:]) == "571d38f08006b7023a65ec64cac77fe23e0db52a"
    counts = Counter()
    for case in doc["cases"]:
        counts["all"] += 1
        spec = case["spec"]
        if spec["q"][0] != 2:
            continue
        nodes, _, widths = producer.data(producer.TREES[spec["tree"]], spec["q"])
        roots = nodes[0]
        sets = {v: set(label_at(case["start"], v)) for v in roots}
        shared = [(a, b, j) for a, b in combinations(roots, 2) for j in sets[a] & sets[b]]
        if len(shared) == 1:
            counts["unique"] += 1
            a, b, _ = shared[0]
            counts["eligible_ends"] += sum(widths[v] == 1 and len(sets[v]) > 1 for v in (a, b))
    assert (counts["all"], counts["unique"], counts["eligible_ends"]) == (2592, 12, 0)
    print("Archive, unique initial pair/label, mixed width-one endpoints:",
          counts["all"], counts["unique"], counts["eligible_ends"])


def check_common_prior():
    for a, b in combinations(range(4), 2):
        common = prepare((a, b), blocks)
        assert verifier.profile_check(tree, 7, common) == profile
        for kept, removed in ((a, b), (b, a)):
            after = prepare((kept,), blocks)
            assert [x ^ y for x, y in zip(common, after)] == [2 if j == removed else 0 for j in alphabet]
            assert verifier.profile_check(tree, 7, after) == profile
    print("Exact common priors and alternative single-bit source cuts:", 6, 12)


def check_unresolved_choice():
    results = []
    for markers, layout, order in [
        ((0, 2), blocks, alphabet),
        ((0, 2), ("source", "right", "left"), alphabet),
        ((0, 1), blocks, alphabet),
        ((0, 1), blocks, alphabet[::-1]),
    ]:
        start = prepare(markers, layout)
        trace = []
        path = producer.normalize(start, tree, 7, profile, order=order, trace=trace)
        assert verifier.path_check(tree, 7, profile, path, start, producer.canonical(tree, 7, profile, order))[0] <= 1
        anchor = trace[0]
        peer, = {layout[i] for i in anchor["pair"]} - {"source"}
        results.append((peer, anchor["label"]))
    assert results == [("left", 0), ("right", 2), ("left", 0), ("left", 1)]
    print("Competing address and competing value controls:", results)


def check_writes():
    total = audited = receiver_first = private_address = 0
    for layout in permutations(blocks):
        roots = {name: 1 + 3 * i for i, name in enumerate(layout)}
        starts = [prepare((x,), layout) for x in range(4)]
        assert all(verifier.profile_check(tree, 7, start) == profile for start in starts)
        for index, order in enumerate(permutations(alphabet)):
            fallback = {key: next(x for x in order if x in labels)
                        for key, labels in (("left", left), ("right", right))}
            endpoints = []
            for x, start in enumerate(starts):
                trace = []
                path = producer.normalize(start, tree, 7, profile, order=order, trace=trace)
                address = "left" if x < 2 else "right"
                anchor = trace[0]
                assert anchor["kind"] == "anchor" and anchor["label"] == x
                assert {layout[i] for i in anchor["pair"]} == {"source", address}
                cut = max(e["end"] for e in trace if e["kind"] == "child_normalization")
                for name, root in roots.items():
                    kept = x if name in ("source", address) else fallback[name]
                    # In the stored integer masks all three sites have that label and only it.
                    region = 7 << root
                    assert all(mask & region == (region if label == kept else 0)
                               for label, mask in enumerate(path[cut]))
                private = 4 if address == "left" else 5
                for leaf in (roots[address] + 1, roots[address] + 2):
                    bit = 1 << leaf
                    first = next(frame for frame in path[1:cut+1]
                                 if any(frame[j] & bit for j in alphabet if j != private)
                                 or not frame[private] & bit)
                    assert set(label_at(first, leaf)) == {private, x}
                if fallback == {"left": 4, "right": 5}:
                    for name, label in (("left", 4), ("right", 5)):
                        expected_change = 7 << roots[name] if name == address else 0
                        assert start[label] ^ path[cut][label] == expected_change
                    private_address += 1
                endpoints.append(path[-1])
                total += 1
                if roots[address] < roots["source"]:
                    receiver_first += 1
                # Full stock path admission on a deterministic spread of palette orders.
                if index % 101 == 0 or index == 5039:
                    endpoint = producer.canonical(tree, 7, profile, order)
                    assert verifier.path_check(tree, 7, profile, path, start, endpoint)[0] <= 1
                    assert verifier.profile_check(tree, 7, path[cut]) == profile
                    audited += 1
                if layout == blocks and index == 0:
                    local = [label_at(vertex, roots[address] + 1) for vertex in path[:cut + 1]]
                    word = [label for i, label in enumerate(local) if i == 0 or label != local[i-1]]
                    print(f"Source {x}: {address} leaf through frame {cut}: {word}")
            assert all(end == endpoints[0] for end in endpoints)
    assert private_address == 13440
    print("Calls with both private labels first and only the addressed private row changed:", private_address)
    assert total == 120960 and receiver_first == total // 2 and audited == 1224
    print("Complete stock calls, full path-admission checks, receiver processed before source:",
          total, audited, receiver_first)


if __name__ == "__main__":
    check_corpus()
    check_common_prior()
    check_unresolved_choice()
    check_writes()
