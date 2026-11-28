"""Infer the first M9 guard-transfer phase from its opening addition; test the unresolved branch."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import gzip
import json
import lzma
from math import comb
import os
from pathlib import Path
import sys

from archive_exact_search import first_exact
from exact_receiver import exact_profile, toggle_path
from remote_incidence import changed, encoded
from replay import FIRST, HERE, LINE_PINS, PINS


def predict(initial, first, nodes, profile):
    """Only two nested states, the ordered tree and its stored ranks are input.

    The assumed program phase fills the second block of initially B/full rows
    with a lexically sorted new guard, using historical M9 primitive ordering.
    """
    roots = nodes[0]
    h = profile[str(roots[0])]
    q = profile["0"]
    labels = initial[0]
    k = len(labels)
    n = comb(h+q-2, h)
    assert all(profile[str(v)] == h for v in roots)
    assert len(roots) == 2*n and labels == list(range(k)) and k == 2*h+q-2
    assert [initial[v] for v in roots[:n]] == [list(s) for s in combinations(range(h+q-2), h)]
    assert initial[roots[n]] == list(range(h+q-2, k))
    assert all(initial[v] == labels for v in roots[n+1:])
    delta = changed(initial, first)
    assert len(delta) == 1
    v, x = delta[0]
    assert v == roots[n] and x in first[v] and x not in initial[v]
    remaining = labels[x:]
    needed = h+q-2
    assert len(remaining) >= needed
    if len(remaining) > needed:
        return None

    guard = list(combinations(remaining, h))
    assert len(guard) == n
    states = [initial]
    writes = []

    def toggle(vertex, label):
        current = states[-1][:]
        current[vertex] = sorted(set(current[vertex]) ^ {label})
        states.append(current)

    for i, desired in zip(roots[n:], guard):
        for new in sorted(set(desired) - set(states[-1][i])):
            toggle(i, new)
        for old in sorted(set(states[-1][i]) - set(desired)):
            holders = [j for j in nodes[i] if old in states[-1][j]]
            if holders:
                leaf, = holders
                occupied = {a for j in nodes[i] for a in states[-1][j]}
                new = min(set(states[-1][i])-occupied)
                writes.append((leaf, old, new))
                toggle(leaf, new)
                toggle(leaf, old)
            toggle(i, old)
    assert states[1] == first
    return states, writes


def guard_end(record):
    i = record["facts"]["parent_record"]["facts"]["guard_end"]
    assert record["path"][i] == record["facts"]["parent_record"]["facts"]["preliminary_path"][i]
    return record["facts"]["parent_boundaries"][i]


def goal_for_support(record, support, rotation=0, extra_slot=-1, dense=True):
    p, _, choices = record["identity"][1:]
    k, h, n = p["k"], p["h"], p["N"]
    guards = [list(s) for s in combinations(support, h)]
    dest = [(i+choices["shift"]) % (2*n) for i in range(n)]
    rest = [i for i in range(2*n) if i not in dest]
    outside = sorted(set(range(k))-set(support))
    goal = [list(range(k)) if dense else outside[:] for _ in range(2*n)]
    for j, i in enumerate(dest):
        goal[i] = guards[(j+rotation) % n]
    goal[rest[extra_slot]] = outside
    return goal


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    demo = args.demo.resolve()
    for name, pin in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest() == pin
    os.chdir(demo)
    sys.path.insert(0, str(demo))
    import universe
    import mechanisms
    import verifier

    raw = gzip.decompress((HERE/"original_m9.jsonl.gz").read_bytes()).splitlines(keepends=True)
    assert tuple(sha256(line).hexdigest() for line in raw) == LINE_PINS
    frozen = list(universe.m9({}))
    cases = [json.loads(line) for line in raw]
    count = 0
    identifiers = set()
    checksum = sha256()
    with lzma.open(HERE/"guard_onset_records.jsonl.xz", "wb" if args.write else "rb") as stream:
        def rerun(record, goal):
            name, p, initial, ch = record["identity"]
            case = {"identity": [name, p, initial, dict(ch, target=goal)]}
            result = mechanisms.produce(case)
            errors = verifier.verify_record(case, result)
            assert result["status"] == "PASS" and not errors, errors
            assert all(exact_profile(result["nested_path"][j], result["nodes"], result["targets"]) for j in (0, -1))
            nonlocal count
            line = encoded(result)
            checksum.update(line)
            identifiers.add(sha256(line).digest())
            count += 1
            if args.write:
                stream.write(line)
            else:
                assert stream.readline() == line
            return result

        for ordinal, (record, line) in enumerate(zip(cases, raw), FIRST):
            original, = [c for c in frozen if c["identity"] == record["identity"]]
            assert encoded(mechanisms.produce(original)) == line
            assert not verifier.verify_record(original, record)
            p = record["identity"][1]
            k, h, q = p["k"], p["h"], p["q"]
            nested, tree, targets = record["nested_path"], record["nodes"], record["targets"]
            forecast, writes = predict(nested[0], nested[1], tree, targets)
            end = guard_end(record)
            assert forecast == nested[:end+1]
            assert not verifier.verify_nested(forecast, tree, targets, k)
            assert len(writes) == sum(step["end"] <= end for step in record["facts"]["clearance"])
            counts, costs = Counter(), []
            exact_handoffs = Counter()
            for support in combinations(range(k), h+q-2):
                result = rerun(record, goal_for_support(record, support))
                observed = result["nested_path"]
                row, opening = changed(observed[0], observed[1])[0]
                assert row == tree[0][p["N"]] and opening == min(support)
                assert not result["facts"]["parent_record"]["facts"]["layers"]
                prediction = predict(observed[0], observed[1], tree, targets)
                if opening == h:
                    assert prediction[0] == forecast == observed[:guard_end(result)+1]
                else:
                    assert prediction is None
                counts[opening] += 1
                boundary = guard_end(result)
                costs.append(boundary)
                exact = exact_profile(observed[boundary], tree, targets)
                assert exact == set(range(h+q-2, k)).issubset(support)
                exact_handoffs[opening] += int(exact)
            assert counts == {x: comb(k-x-1, h+q-3) for x in range(h+1)}
            assert sum(exact_handoffs.values()) == comb(h+q-2, q-2)
            assert all(exact_handoffs[x] > 0 for x in range(h+1))
            # Vary the full endpoint and guard placement beyond the forecast horizon.
            support = list(range(h, k))
            for rotation, extra, dense in ((1, 0, True), (2, 1, True), (1, -1, False)):
                result = rerun(record, goal_for_support(record, support, rotation, extra, dense))
                assert forecast == result["nested_path"][:guard_end(result)+1]
            print(ordinal, "first label", h, "parent/nested moves", record["facts"]["parent_record"]["facts"]["guard_end"],
                  end, "leaf replacements", len(writes), "tight supports by opening", sorted(counts.items()),
                  "exact handoffs by opening", sorted(exact_handoffs.items()), "tight phase length range", [min(costs), max(costs)])

        small = cases[1]
        tree, profile, original_path = small["nodes"], small["targets"], small["nested_path"]
        for frame, expected in [(10, [(14, 4), (14, 2), (13, 2)]), (19, [(17, 4), (17, 2), (16, 2)]),
                                (23, [(1, 2)])]:
            levels, repairs = first_exact(original_path[frame], tree, profile, limit=3)
            assert levels[-1][2] == 1 and list(repairs[0]) == expected
            following = [changed(a, b)[0] for a, b in zip(original_path[frame:frame+len(expected)],
                                                             original_path[frame+1:frame+len(expected)+1])]
            assert (following == expected) == (frame == 19)
            print("Frozen frame", frame, "unique shortest toggles", expected, "historical toggles", following)
        # Score every unique exact repair within three moves in the smallest
        # original record. The verdict uses the current state and observed past.
        forecast, _ = predict(original_path[0], original_path[1], tree, profile)
        counts = Counter()
        for i, frame in enumerate(small["facts"]["parent_boundaries"]):
            if small["tau"][i] != profile["0"]-1:
                continue
            layers, candidates = first_exact(original_path[frame], tree, profile, limit=3)
            if not candidates or layers[-1][2] != 1:
                continue
            repair, = candidates
            expected = toggle_path(original_path[frame], repair)
            previous = changed(original_path[frame-1], original_path[frame])[0]
            v, label = previous
            if len(repair) == 1 and repair[0] == previous and label in original_path[frame][v] and v in tree[0]:
                verdict, reason = False, "reverse of last parent addition"
            elif frame+len(repair) < len(forecast):
                verdict = forecast[frame:frame+len(repair)+1] == expected
                reason = "opening-determined guard"
            else:
                raise AssertionError(("unclassified", frame))
            actual = original_path[frame:frame+len(repair)+1] == expected
            assert verdict == actual
            counts[reason, verdict] += 1
        assert counts == {("reverse of last parent addition", False): 5, ("opening-determined guard", False): 1,
                          ("opening-determined guard", True): 1}
        print("All seven unique repairs in the 3-move census:", dict(counts))
        # Both exact endpoints share all parameters and differ in one target incidence.
        goals = [[[0, 2], [0, 1], [0, 1], last, [1, 2], [3, 4]] for last in ([2, 3, 4], [3, 4])]
        assert changed(*goals) == [(3, 2)]
        keep, clear = [rerun(small, goal) for goal in goals]
        a, b = keep["nested_path"], clear["nested_path"]
        assert a[:18] == b[:18] and a[18] != b[18]
        assert changed(a[17], a[18]) == [(1, 2)]
        levels, repairs = first_exact(a[17], tree, profile, limit=3)
        moves, = repairs
        assert levels[-1] == (1761, 1, 1) and moves == ((17, 4), (17, 2), (16, 2))
        assert toggle_path(b[17], moves) == b[17:21]
        assert not exact_profile(a[20], tree, profile)
        print("One-target-incidence control: identical nested frames 0-17; one follows the sole three-edit repair, one bypasses it.")
        for h, q in ((2, 5), (4, 3)):
            case = universe.guard_case(h, q, 2*comb(h+q-2, h), 1, 1, "M9")
            result = rerun(case, case["identity"][3]["target"])
            path = result["nested_path"]
            prediction, writes = predict(path[0], path[1], result["nodes"], result["targets"])
            boundary = guard_end(result)
            assert prediction == path[:boundary+1]
            print("Additional geometry", (h, q), "first phase moves", boundary, "leaf replacements", len(writes))
        if not args.write:
            assert not stream.read(1)
    print("Control records", count, "distinct", len(identifiers), "uncompressed SHA-256", checksum.hexdigest())


if __name__ == "__main__":
    main()
