"""Derive shortest exact repairs of measured nested defects and check separate full M9 runs."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import lzma
import os
from pathlib import Path
import sys

from guard_completion import propose
from remote_incidence import BASE, add_source, changed, cover, encoded, registers
from replay import HERE, PINS

COMPACT = [[0, 2], [0, 2, 3, 6], [3, 6], [1, 3, 4, 5], [0, 3, 4, 7], [5, 7]]
PRIOR_STREAM = "completion_examples.jsonl.gz"


def exact_profile(state, nodes, targets):
    return all(len(cover([state[i] for i in nodes[int(v)]])) == q for v, q in targets.items())


def nearest_parents(rows, palette, floors, target):
    """Find all exact, floor-respecting endpoints within two parent flips, over every row."""
    start = [sum(1 << x for x in row) for row in rows]
    lower_covers, target_covers = [[sum(1 << x for x in v) for v in combinations(palette, size)]
                                   for size in (target-1, target)]
    for distance in (0, 1, 2):
        solutions = []
        for moves in combinations(product(range(len(rows)), palette), distance):
            masks = start[:]
            for i, x in moves:
                masks[i] ^= 1 << x
            if any(mask.bit_count() < floor for mask, floor in zip(masks, floors)):
                continue
            if any(all(m & c for m in masks) for c in lower_covers):
                continue
            if any(all(m & c for m in masks) for c in target_covers):
                solutions.append(moves)
        if solutions:
            return solutions
    return []


def toggle_path(start, moves):
    states = [start]
    for node, x in moves:
        state = states[-1][:]
        state[node] = sorted(set(state[node]) ^ {x})
        states.append(state)
    return states


def shortest_repairs(record, verifier):
    # Only the measured terminal state, tree and target profile enter this search.
    start = record["nested_path"][-1]
    nodes, targets = record["nodes"], record["targets"]
    roots, labels, q = nodes[0], start[0], targets["0"]
    floors = [targets[str(v)] for v in roots]
    leaves = [leaf for root in roots for leaf in nodes[root]]
    assert all(not nodes[v] and len(start[v]) == 1 for v in leaves)
    assert not verifier.verify_nested([start], nodes, targets, len(labels))
    assert len(cover([start[v] for v in roots])) == q-1
    held_sets = [set.union(*(set(start[v]) for v in nodes[root])) for root in roots]
    held_cover = cover(held_sets)
    assert len(held_cover) < q
    # Without withdrawing a held incidence, this cover hits every future parent.
    # Nonempty singleton leaves require another leaf move before that withdrawal.
    parents = nearest_parents([start[v] for v in roots], labels, floors, q)
    assert len(parents) == 1 and len(parents[0]) == 2
    parent_moves = [(roots[i], x) for i, x in parents[0]]
    end_parents = toggle_path(start, parent_moves)[-1]
    paths = []
    for v in roots:
        for child in nodes[v]:
            old, = start[child]
            for new in end_parents[v]:
                if new == old:
                    continue
                moves = [*parent_moves, (child, old), (child, new)]
                endpoint = toggle_path(start, moves)[-1]
                if not exact_profile(endpoint, nodes, targets):
                    continue
                # No supplied schedule. These are all shortest move orders and
                # leaf substitutions allowed by the two independent lower bounds.
                for order in permutations(moves):
                    states = toggle_path(start, order)
                    if not verifier.verify_nested(states, nodes, targets, len(labels)):
                        paths.append(dict(leaf=child, old=old, new=new, moves=order, states=states))
    assert paths and all(len(r["moves"]) == 4 for r in paths)
    return dict(held_cover=list(held_cover), parent_moves=parent_moves, paths=paths)


def subsets(pair):
    return [set(z) for n in (1, 2) for z in combinations(sorted(pair), n)]


def new_pairs():
    p, q, s, t = ({0, 2}, {3, 6}, {5, 7}, {1, 4})
    for aq, az, xp, xq, xs, xt in product(subsets(q), subsets(s), subsets(p), subsets(q), sorted(s), sorted(t)):
        a, x = t | aq | az, xp | xq | {xs, xt}
        rows = [sorted(z) for z in (p, p | q, q, a, x, s)]
        yield rows, add_source(rows, 4), (len(a), len(x))


def mapped(rows, sign, offset):
    return [sorted((offset+sign*x) % 8 for x in row) for row in rows]


def alternate(record, verifier):
    # Explicit longer repair confined to the row initially carrying {1,3,4,5}.
    start, nodes, targets = record["nested_path"][-1], record["nodes"], record["targets"]
    v, = [i for i in nodes[0] if start[i] == [1, 3, 4, 5]]
    a, = [i for i in nodes[v] if start[i] == [1]]
    b, = [i for i in nodes[v] if start[i] == [4]]
    moves = [(v, 6), (a, 3), (a, 1), (b, 6), (b, 4)] + [(v, x) for x in (1, 4, 5)]
    states = toggle_path(start, moves)
    assert not verifier.verify_nested(states, nodes, targets, 8)
    assert exact_profile(states[-1], nodes, targets)
    return dict(moves=moves, states=states)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", type=Path)
    parser.add_argument("--write", action="store_true", help="write the full record streams beside this script")
    args = parser.parse_args()
    demo = args.demo.resolve()
    for name, digest in PINS.items():
        assert sha256((demo/name).read_bytes()).hexdigest() == digest
    os.chdir(demo)
    sys.path.insert(0, str(demo))
    import mechanisms
    import universe
    import verifier

    digest = sha256()
    archive = HERE / "exact_receiver_records.jsonl.xz"
    count = 0
    with lzma.open(archive, "wb" if args.write else "rb") as stream:
        def save(data):
            nonlocal count
            line = encoded(data)
            if args.write:
                stream.write(line)
            else:
                assert stream.readline() == line
            count += 1
            digest.update(line)

        def stock(rows, goal):
            c = universe.case("M9", "native", 8, [2]*6, 3, rows,
                              dict(shift=0, reversal=0, target=goal), h=2, N=3)
            r = mechanisms.produce(c)
            errors = verifier.verify_record(c, r)
            assert r["status"] == "PASS" and not errors, errors
            assert exact_profile(r["nested_path"][0], r["nodes"], r["targets"])
            save(dict(kind="M9", record=r))
            return r

        originals = [json.loads(line) for line in gzip.open(HERE / PRIOR_STREAM, "rt")]
        for name, base in (("previous", BASE), ("compact", COMPACT)):
            pair = [propose(rows) for rows in (base, add_source(base, 4))]
            assert pair[0][1:] == pair[1][1:]
            band = [stock(a, g) for a, g, _ in pair]
            assert changed(band[0]["nested_path"][0], band[1]["nested_path"][0]) == [(1, 4)]
            assert changed(band[0]["nested_path"][-1], band[1]["nested_path"][-1]) == [(14, 0), (14, 4), (15, 0), (15, 4)]
            for arm, record in enumerate(band):
                if name == "previous":
                    assert record == originals[arm]
                assert not exact_profile(record["nested_path"][-1], record["nodes"], record["targets"])
                repair = shortest_repairs(record, verifier)
                paths = repair["paths"]
                assert {r["leaf"] for r in paths} == {(14, 15)[arm]}
                assert {r["old"] for r in paths} == {4}
                values = sorted({r["new"] for r in paths})
                assert values == ([2, 6] if name == "previous" else [3])
                assert len(paths) == 4*len(values)
                save(dict(kind="direct repair", fixture=name, arm=arm, **repair))
                if name == "compact":
                    path = alternate(record, verifier)
                    assert all(start[14:16] == path["states"][0][14:16] for start in path["states"])
                    save(dict(kind="eight-move alternative", arm=arm, **path))
                print(name, "source bit", arm, "held cover", repair["held_cover"], "parent moves", repair["parent_moves"],
                      "leaf", paths[0]["leaf"], "new labels", values, "legal shortest orders", len(paths))
            a, goal, order = pair[0]
            # Independent end-to-end M9 executions to the calculated exact endpoint.
            target = [z[:] for z in goal]
            for row, x in nearest_parents(goal, list(range(8)), [2]*6, 3)[0]:
                target[row] = sorted(set(target[row]) ^ {x})
            corrected = [stock(prep[0], target) for prep in pair]
            for arm, r in enumerate(corrected):
                assert exact_profile(r["nested_path"][-1], r["nodes"], r["targets"])
                endpoints = shortest_repairs(band[arm], verifier)["paths"]
                assert any(r["nested_path"][-1] == d["states"][-1] for d in endpoints)
                assert band[arm]["nested_path"][-1] not in r["nested_path"]
            assert registers(corrected[0], -1)[4] != registers(corrected[1], -1)[4]
            if name == "previous":
                for prep in pair:
                    idle_target = stock(prep[0], a)
                    assert exact_profile(idle_target["nested_path"][-1], idle_target["nodes"], idle_target["targets"])
                    assert registers(idle_target, -1)[4] == (0, 2)

        groups = {"exploratory": Counter(), "remaining": Counter(), "label controls": Counter()}
        widths = {(6, 4), (6, 6), (5, 6)}
        for first, second, shape in new_pairs():
            group = "exploratory" if shape in widths else "remaining"
            transforms = [(1, 0)]
            if group == "exploratory":
                transforms = list(product((1, -1), range(8)))
            for sign, offset in transforms:
                key = group if (sign, offset) == (1, 0) else "label controls"
                a, b = [mapped(r, sign, offset) for r in (first, second)]
                if a[0][:2] != b[0][:2]:
                    groups[key]["changed initial leaf"] += 1
                    continue
                pa, pb = propose(a), propose(b)
                assert pa is not None and pb is not None and pa[1:] == pb[1:]
                _, goal, order = pa
                i = order.index(4)
                k = set(mapped([[1, 4, 5, 7]], sign, offset)[0])
                edited = [z[:] for z in goal]
                edited[i] = sorted(set(goal[i])-k)
                assert len(cover(goal)) == 2 and len(cover(edited)) == 3
                predicted = not set(a[4][:2]).intersection(k)
                rr = [stock(x[0], edited) for x in (pa, pb)]
                assert len(changed(rr[0]["nested_path"][0], rr[1]["nested_path"][0])) == 1
                assert rr[0]["path"][-1] == rr[1]["path"][-1]
                assert all(exact_profile(r["nested_path"][-1], r["nodes"], r["targets"]) for r in rr)
                end = [registers(r, -1)[i] for r in rr]
                assert set(end[0]) == set(end[1])
                observed = end[0] != end[1]
                groups[key][("predicted " if predicted else "unpredicted ") + ("delivery" if observed else "no delivery")] += 1
        if not args.write:
            assert not stream.read(1)
    for k, v in groups.items():
        print(k, dict(sorted(v.items())))
    assert groups["exploratory"] == {"predicted delivery": 14, "unpredicted no delivery": 22}
    assert groups["remaining"] == {"predicted delivery": 112, "unpredicted no delivery": 176}
    assert groups["label controls"] == {"changed initial leaf": 360, "predicted no delivery": 62, "unpredicted no delivery": 118}
    print(count, "archive entries, uncompressed SHA-256", digest.hexdigest())


if __name__ == "__main__":
    main()
