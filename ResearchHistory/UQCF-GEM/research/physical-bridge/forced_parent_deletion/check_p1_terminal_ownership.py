"""Check complete pruning in the original v16.26 transition graph."""
from collections import Counter
from functools import cache
import hashlib
import importlib.util
from itertools import combinations, product
import json
from math import prod
from pathlib import Path
import sys
from zipfile import ZipFile


SCI = Path("ResearchHistory/UQCF-GEM")
ATOMIC = SCI / "demos/v16.26-consistency-increment-law"
ARCHIVE = (SCI / "research/physical-bridge/forced_parent_deletion/p1_owner_action_evidence"
           / "p1-owner-action-replay.zip")
PINS = {"engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
        "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3"}


def pinned(path, expected):
    data = path.read_bytes()
    assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected
    return data


def module(name):
    path = ATOMIC / name
    pinned(path, PINS[name])
    spec = importlib.util.spec_from_file_location("p1_" + path.stem, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def family(raw):
    return tuple(map(tuple, raw))


def size(state):
    return sum(map(len, state))


def leaf_holders(parents, state):
    vertices = set().union(*state)
    leaves = sorted(vertices - {0} - {parents[v] for v in vertices if v})
    return {v: tuple(i for i, view in enumerate(state) if v in view) for v in leaves}


def hulls(parents, owners, n):
    views = [{0} for _ in range(n)]
    for leaf, who in owners.items():
        v = leaf
        while v:
            views[who].add(v)
            v = parents[v]
    return family(sorted(view) for view in views)


def small_cases(engine, verifier):
    rows = []
    for tree, parents in engine.shapes(4):
        for n in (1, 2, 3):
            states = [s for s in product(engine.legal(parents), repeat=n)
                      if len(set().union(*s)) == len(parents)]
            successors = {}
            for state in states:
                targets = []
                for i, view in enumerate(state):
                    for v in view:
                        if not v or any(parents[c] == v for c in view):
                            continue
                        try:
                            event = engine.atomic(parents, state, i, v)
                        except ValueError as error:
                            assert str(error) == "same union"
                            continue
                        verifier.verify_atomic(event)
                        targets.append(family(event["after"]))
                successors[state] = targets

            @cache
            def complete(state):
                moves = successors[state]
                if not moves:
                    return frozenset({state})
                return frozenset().union(*(complete(t) for t in moves))

            interfaces = {}
            for state in states:
                held = leaf_holders(parents, state)
                generated = {hulls(parents, dict(zip(held, owners, strict=True)), n)
                             for owners in product(*held.values())}
                assert generated == complete(state) and len(generated) == prod(map(len, held.values()))
                for i in range(n):
                    must = frozenset(v for v, h in held.items() if h == (i,))
                    may = frozenset(v for v, h in held.items() if i in h)
                    outputs = {
                        frozenset(set(z[i]) & held.keys()) for z in complete(state)}
                    assert all(must <= s <= may for s in outputs) and len(outputs) == 2 ** len(may - must)
                    key = (must, may)
                    assert key not in interfaces or interfaces[key] == outputs
                    interfaces[key] = outputs
            pairs = 0
            for ((m, p), a), ((k, q), b) in combinations(interfaces.items(), 2):
                assert a.isdisjoint(b) == bool((m - q) | (k - p))
                pairs += 1
            rows.append({"tree": tree, "indices": n, "states": len(states),
                         "moves": sum(map(len, successors.values())), "interface_pairs": pairs,
                         "sinks": sum(not z for z in successors.values())})
    return rows


def terminal_refusals(engine, parents, terminal):
    count = 0
    for i, view in enumerate(terminal):
        for v in view:
            if not v or any(parents[c] == v for c in view):
                continue
            try:
                engine.atomic(parents, terminal, i, v)
            except ValueError as error:
                assert str(error) == "same union"
                count += 1
            else:
                raise AssertionError("Terminal has an outgoing edge")
    return count


def fixture(engine, verifier):
    pinned(ARCHIVE, "f9d80670469339c36f1b0b7e21dce3e0b44e9c97")
    with ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        data = json.loads(archive.read("atomic_records.json"))
    keys = [tuple(k) for k in data["keys"]]
    records = data["records"]
    parents = tuple(records["t_source"]["parents"])
    a, b = 0, 1
    n = 25
    twins = {v for v, key in enumerate(keys) if len(key) == 2 and key[0] == 6}
    common = {}
    totals = {}
    witnesses = {}
    for arm in ("t", "u"):
        source = records[arm + "_source"]
        verifier.verify_atomic(source)
        after = family(source["after"])
        held = leaf_holders(parents, after)
        assert len(parents) == 85 and len(after) == n and len(twins) == 2 and size(after) == 1453
        assert Counter(map(len, held.values())) == {1: 1, 2: 1, 4: 25, 23: 50}
        fixed = source["leaf"]
        other, = twins - {fixed}
        assert held[fixed] == (b,) and held[other] == (a, b)
        corners = [v for v in held if keys[v][0] < 5]
        edges = [v for v in held if keys[v][0] == 5]
        edge_holders = [set(held[v]) for v in edges]
        assert len(corners) == 25 and len(edges) == 50
        # A row label covers at most two corners. No label covers all edge leaves.
        for row in range(5):
            assert max(sum(i in held[v] for v in corners if keys[v][0] == row)
                       for i in range(n)) == 2
        assert not set.intersection(*edge_holders)
        for focus in ("fewest", "most"):
            owners = {}
            for v in corners:
                row, col = keys[v]
                if focus == "fewest":
                    palette = [5 * row + offset for offset in (0, 2, 4)]
                    owners[v] = next(i for i in palette if i in held[v])
                else:
                    owners[v] = 5 * row + col
            if focus == "fewest":
                pair = next((i, j) for i, j in combinations(range(n), 2)
                            if all({i, j} & h for h in edge_holders))
                owners.update({v: next(i for i in pair if i in held[v]) for v in edges})
            else:
                # Match each index to its own distinct legal edge leaf.
                def place(i, seen):
                    for v in edges:
                        if i in held[v] and v not in seen:
                            seen.add(v)
                            if v not in owners or place(owners[v], seen):
                                owners[v] = i
                                return True
                    return False
                assert all(place(i, set()) for i in range(n))
                for v in edges:
                    owners.setdefault(v, held[v][0])
            for kind, last in (("shared_record", b), ("split_record", a)):
                assignment = {**owners, fixed: b, other: last}
                assert all(i in held[v] for v, i in assignment.items())
                end = hulls(parents, assignment, n)
                assert all(set(z) <= set(y) for y, z in zip(after, end, strict=True))
                assert set().union(*end) == set(range(len(parents)))
                assert terminal_refusals(engine, parents, end) == len(held)
                assert set(end[b]) & twins == ({fixed} if last == a else twins)
                if last == b:
                    assert focus not in common or common[focus] == end
                    common[focus] = end
                label = "_".join([arm, focus, kind])
                totals[label] = size(after) - size(end)
                witnesses[label] = end
    expected = {"fewest_shared_record": 1333, "fewest_split_record": 1332,
                "most_shared_record": 1300, "most_split_record": 1299}
    assert all(totals[arm + "_" + tag] == length for arm in ("t", "u") for tag, length in expected.items())
    k = 4**25 * 23**50
    # Moving the fork to the mandatory root removes the one-incidence length gap.
    root_star = ((0, 2), (0, 1, 2))
    controls = []
    for actor in (a, b):
        step = engine.atomic((-1, 0, 0), root_star, actor, 2)
        verifier.verify_atomic(step)
        end = family(step["after"])
        assert terminal_refusals(engine, (-1, 0, 0), end) == 2
        controls.append(end)
    assert controls[0] != controls[1]
    return ({"start_incidence": 1453, "vertices": 85, "views": n, "terminal_counts_per_arm": str(2*k),
             "shared_full_terminals": str(k), "strict_terminals_per_arm": str(k),
             "deletion_lengths": totals, "root_star_equal_length": 1}, witnesses)


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    engine, verifier = module("engine.py"), module("verify.py")
    rows = small_cases(engine, verifier)
    result, ends = fixture(engine, verifier)
    cert = json.dumps({"small_cases": rows, "full_witnesses": ends}, sort_keys=True, indent=2) + "\n"
    (out / "terminal_certificate.json").write_bytes(cert.encode())
    print(json.dumps({"grammar": "v16.26 deletion-only", "small": {
        key: sum(r[key] for r in rows) for key in ("states", "moves", "sinks", "interface_pairs")},
        "tree_shapes": len(rows)//3, "fixture": result,
        "certificate_sha256": hashlib.sha256(cert.encode()).hexdigest()}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
