"""Unrestricted breadth-first native move search on two checkpoints from original M9 record 2393447."""
import argparse
from collections import Counter
from functools import lru_cache
import gzip
from hashlib import sha256
from itertools import combinations
import json
import lzma
import os
from pathlib import Path
import sys

from exact_receiver import exact_profile, nearest_parents, toggle_path
from remote_incidence import changed, cover, encoded
from replay import FIRST, HERE, LINE_PINS, PINS


def first_exact(start, nodes, targets, limit=None):
    """Return path counts to the first exact layer, keeping one path per exact endpoint."""
    palette = tuple(start[0])
    internal = [(i, children, targets[str(i)]) for i, children in enumerate(nodes) if children]
    masks = tuple(sum(1 << x for x in support) for support in start)
    parent = {j: i for i, children in enumerate(nodes) for j in children}
    choices = [sum(1 << x for x in group)
               for n in range(1, len(palette)+1) for group in combinations(palette, n)]

    @lru_cache(maxsize=None)
    def rank(children):
        return next(c.bit_count() for c in choices if all(mask & c for mask in children))

    def deviation(state):
        return sum(abs(rank(tuple(state[j] for j in children)) - q) for _, children, q in internal)

    assert deviation(masks) == 1
    seen = {masks}
    frontier = {masks: (1, ())}
    layers = []
    while frontier:
        upcoming = {}
        exact = set()
        for state, (count, prefix) in frontier.items():
            for node, above in parent.items():
                locked = 0
                for j in nodes[node]:
                    locked |= state[j]
                for x in palette:
                    bit = 1 << x
                    value = state[node] ^ bit
                    if not value or locked & ~value or value & ~state[above]:
                        continue
                    nxt = state[:node] + (value,) + state[node+1:]
                    if nxt in seen:
                        continue
                    if nxt in upcoming:
                        ways, first = upcoming[nxt]
                        upcoming[nxt] = (ways+count, first)
                        continue
                    diff = deviation(nxt)
                    if diff > 1:
                        continue
                    upcoming[nxt] = (count, prefix + ((node, x),))
                    if not diff:
                        exact.add(nxt)
        wins = sum(upcoming[e][0] for e in exact)
        layers.append((len(upcoming), len(exact), wins))
        if exact:
            return layers, [upcoming[e][1] for e in sorted(exact)]
        if limit is not None and len(layers) >= limit:
            return layers, []
        seen.update(upcoming)
        frontier = upcoming
    raise ValueError("No exact endpoint is reachable")


def direct_restore(start, nodes, targets):
    """Certificate for one parent change and two necessary leaf changes, using only this state."""
    roots, q = nodes[0], targets["0"]
    h = [targets[str(v)] for v in roots]
    row_sets = [start[v] for v in roots]
    held = [set.union(*(set(start[j]) for j in nodes[v])) for v in roots]
    assert all(len(start[j]) == 1 for v in roots for j in nodes[v])
    assert len(cover(row_sets)) == len(cover(held)) == q-1
    possible = nearest_parents(row_sets, start[0], h, q)
    assert len(possible) == 1 and len(possible[0]) == 1
    (i, x), = possible[0]
    root = roots[i]
    leaf, = [j for j in nodes[root] if x in start[j]]
    spare, = set(start[root])-held[i]
    return ((leaf, spare), (leaf, x), (root, x))


def family_checkpoint(record):
    p = record["identity"][1]
    h, q, n = p["h"], p["q"], p["N"]
    a, g = range(h+q-2), list(range(h, 2*h+q-2))
    left = [list(v) for v in combinations(a, h)]
    right = [list(v) for v in combinations(g, h)]
    boundary = left + right[:-1] + [sorted(set(right[-1]) | {h+q-3})]
    i, = [i for i, vertex in enumerate(record["path"]) if vertex == boundary]
    assert len(left) == len(right) == n
    return i, record["facts"]["parent_boundaries"][i]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    args = parser.parse_args()
    demo = args.demo.resolve()
    for name, pin in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest() == pin
    os.chdir(demo)
    sys.path.insert(0, str(demo))
    import mechanisms
    import universe
    import verifier

    lines = gzip.decompress((HERE/"original_m9.jsonl.gz").read_bytes()).splitlines(keepends=True)
    assert tuple(sha256(line).hexdigest() for line in lines) == LINE_PINS
    catalog = list(universe.m9({}))
    for ordinal, line in enumerate(lines, FIRST):
        entry = json.loads(line)
        src, = [c for c in catalog if c["identity"] == entry["identity"]]
        assert encoded(mechanisms.produce(src)) == line
        assert not verifier.verify_record(src, entry)
        i, frame = family_checkpoint(entry)
        states = entry["nested_path"]
        moves = direct_restore(states[frame], entry["nodes"], entry["targets"])
        prediction = toggle_path(states[frame], moves)
        assert prediction == states[frame:frame+4]
        assert not verifier.verify_nested(prediction, entry["nodes"], entry["targets"], len(states[frame][0]))
        assert exact_profile(prediction[-1], entry["nodes"], entry["targets"])
        print("Original", ordinal, "parent/nested start", (i, frame), "unique shortest moves", moves)
    record = json.loads(lines[1])
    nodes, targets = record["nodes"], record["targets"]
    states = record["nested_path"]
    assert record["facts"]["parent_boundaries"][7] == 19
    # No subsequent state, target parent tuple, plan, acting node or label is
    # passed into first_exact. Compare the prediction to the archive afterward.
    layers, hits = first_exact(states[19], nodes, targets)
    expected = ((17, 4), (17, 2), (16, 2))
    assert hits == [expected] and layers[-1][2] == 1
    reconstructed = toggle_path(states[19], hits[0])
    assert reconstructed == states[19:23]
    assert not verifier.verify_nested(reconstructed, nodes, targets, 5)
    assert exact_profile(reconstructed[-1], nodes, targets)
    print("Original M9 ordinal", FIRST+1, "SHA-256", LINE_PINS[1])
    print("Frame 19. New states, exact endpoints, shortest exact paths at each distance:", layers)
    print("Sole shortest path (node, toggled label):", hits[0], "matches archived frames 20-22.")

    # Legal four-move repair elsewhere, matching the same target profile.
    alternative = toggle_path(states[19], [(10, 4), (12, 4), (12, 2), (10, 2)])
    assert not verifier.verify_nested(alternative, nodes, targets, 5)
    assert exact_profile(alternative[-1], nodes, targets)
    assert all(v[17] == states[19][17] for v in alternative)
    print("Four-move exact alternative: parent 10 and leaf 12; leaf 17 stays fixed.")

    control, next_moves = first_exact(states[23], nodes, targets)
    assert len(control) == 1
    assert states[22] in [toggle_path(states[23], s)[-1] for s in next_moves]
    assert not exact_profile(states[24], nodes, targets)
    print("Frame 23. Exact repairs in one move:", next_moves, "actual next change:", changed(states[23],states[24]))

    census = Counter()
    matches = []
    for i, frame in enumerate(record["facts"]["parent_boundaries"]):
        if record["tau"][i] != 2:
            continue
        outcome, exact = first_exact(states[frame], nodes, targets, limit=3)
        if not exact:
            census["no exact path within three"] += 1
            continue
        distance = len(outcome)
        actual = frame+distance < len(states) and exact_profile(states[frame+distance], nodes, targets)
        census[("unique" if outcome[-1][2] == 1 else "multiple") + (" followed" if actual else " bypassed")] += 1
        if actual and outcome[-1][2] == 1:
            matches.append((frame, distance))
    print("All root-defective parent boundaries in this original record, horizon three:", sorted(census.items()))
    print("Unique shortest paths followed, by (starting frame, distance):", matches)

    # Cross-check the independent endpoint proof on the compact continuing
    # experiment using only each initial state and its archived target profile.
    prior = []
    checked = 0
    with lzma.open(HERE / "exact_receiver_records.jsonl.xz", "rt") as stream:
        for line in stream:
            item = json.loads(line)
            if item["kind"] == "M9":
                prior.append(item["record"])
            if item["kind"] != "direct repair" or item["fixture"] != "compact":
                continue
            start = item["paths"][0]["states"][0]
            run, = [entry for entry in prior if entry["nested_path"][-1] == start]
            levels, first = first_exact(start, run["nodes"], run["targets"], limit=4)
            assert levels[-1] == (254645, 1, 4)
            assert toggle_path(start, first[0])[-1] == item["paths"][0]["states"][-1]
            print("Compact arm", item["arm"], "unrestricted BFS:", levels)
            checked += 1
            if checked == 2:
                break
    assert checked == 2


if __name__ == "__main__":
    main()
