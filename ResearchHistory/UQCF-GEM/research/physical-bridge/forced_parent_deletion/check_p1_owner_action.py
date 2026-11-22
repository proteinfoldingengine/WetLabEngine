"""Replay original same-union pruning and the archived work comparison."""

import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

from check_p1_grade_work import work_read
from check_p1_meet_work_catalog import load_original


SCI = Path("ResearchHistory/UQCF-GEM")
ATOMIC = SCI / "demos/v16.26-consistency-increment-law"
ATOMIC_PINS = {
    "engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    "TYPE_AND_PROOF.md": "69ace252586ad0b323ca3c460304ead8da8fd917",
}
ROOT = ()
ROWS = tuple((i,) for i in range(5))
EDGE_PARENT = (5,)
PARENT = (6,)
T, U = (6, 0), (6, 1)
A, B = 0, 1
LABELS = tuple(range(25))


def load_atomic(out):
    modules, pins = {}, []
    for name, expected in ATOMIC_PINS.items():
        path = ATOMIC / name
        data = path.read_bytes()
        blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        assert blob == expected, path
        (out / ("atomic_" + name)).write_bytes(data)
        pins.append({"path": str(path), "blob": blob, "sha256": hashlib.sha256(data).hexdigest()})
        if path.suffix == ".py":
            spec = importlib.util.spec_from_file_location("v16_26_" + path.stem, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[path.stem] = module
    return modules, pins


def prepare(lineage, edges):
    base = (ROOT, *ROWS, EDGE_PARENT, PARENT)
    corners = tuple((i // 5, i % 5) for i in LABELS)
    edge_list = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    edge_keys = tuple((5, i) for i in range(len(edge_list)))
    common = lineage.Carrier("indexed-P1-owner-action-fixture", base + corners + edge_keys + (T, U))
    positions = {key: i for i, key in enumerate(common.keys)}
    parents = (-1, *(positions[key[:-1]] for key in common.keys[1:]))
    grade = ((1,) * (len(base) + len(corners))
             + tuple(1 if edge == (A, B) else 3 for edge in edge_list) + (2, 2))
    views = []
    for i in LABELS:
        x, y = i % 5, i // 5
        keys = set(base)
        keys.update(((y + dy) % 5, (x + dx) % 5) for dx, dy in product((0, 1), repeat=2))
        keys.update(key for edge, key in zip(edge_list, edge_keys, strict=True) if i not in edge)
        if i in (A, B):
            keys.update((T, U))
        views.append(tuple(sorted(positions[key] for key in keys)))
    return common, positions, parents, grade, tuple(views)


def check_refinement(event, before, parents, index, leaf):
    after = list(before)
    after[index] = tuple(v for v in before[index] if v != leaf)
    assert event["index"] == index and event["leaf"] == leaf and event["parent"] == parents[leaf]
    assert tuple(map(tuple, event["before"])) == before and tuple(map(tuple, event["after"])) == tuple(after)
    assert event["h_before"] == event["h_after"] == 3 and event["delta_h"] == 0
    return tuple(after)


def require_refusal(call, reason):
    try:
        call()
    except ValueError as error:
        assert str(error) == reason
    else:
        raise AssertionError(f"Expected {reason}")


def replay_events(original, before, parents, p, twins, common_corner):
    atomic, verify = original["engine"].atomic, original["verify"].verify_atomic
    records, episodes, local_cases = {}, {}, {}
    twin_set = set(twins.values())

    def call(name, state, owner, leaf, old_tau, new_tau):
        record = atomic(parents, state, owner, leaf)
        after = check_refinement(record, state, parents, owner, leaf)
        triggered = new_tau > old_tau
        assert (record["tau_before"], record["tau_after"], record["trigger"]) == (old_tau, new_tau, triggered)
        assert verify(record) == (0, triggered)
        records[name] = record
        return after

    assert all({i for i, view in enumerate(before) if leaf in view} == {A, B} for leaf in twin_set)
    for name, opposite in (("t", "u"), ("u", "t")):
        held, alternative = twins[name], twins[opposite]
        source = call(name + "_source", before, A, held, 1, 1)
        assert source[B] == before[B]
        require_refusal(lambda: atomic(parents, source, B, held), "same union")
        received = call(name + "_receiver", source, B, alternative, 1, 2)
        assert set(received[B]) & twin_set == {held}
        blind = call(name + "_source_only", source, A, alternative, 1, 1)
        assert blind[B] == before[B]
        for leaf in twin_set:
            require_refusal(lambda: atomic(parents, blind, B, leaf), "same union")
        unrelated = call(name + "_unrelated_receiver", source, B, common_corner, 3, 3)
        assert set(unrelated[B]) & twin_set == twin_set
        episodes[name] = (source, received, blind, unrelated)
        assert all(records[name + "_" + step]["parent"] == p for step in ("source", "receiver", "source_only"))

        subsets = (set(), {held}, {alternative}, twin_set)
        reachable = {
            (tuple(sorted(own_a)), tuple(sorted(own_b)))
            for own_a, own_b in product(subsets, repeat=2)
            if own_a <= (set(source[A]) & twin_set) and own_b <= (set(source[B]) & twin_set)
            and own_a | own_b == twin_set
        }
        observed = {(tuple(sorted(set(state[A]) & twin_set)), tuple(sorted(set(state[B]) & twin_set)))
                    for state in (source, received, blind)}
        assert reachable == observed and len(reachable) == 3
        local_cases[name] = sorted(reachable)

    assert episodes["t"][2] == episodes["u"][2]
    forged = {**records["t_receiver"], "trigger": False}
    require_refusal(lambda: verify(forged), "false certificate")
    return episodes, records, local_cases


def embed_grades(lineage, common, ambient, states, records):
    def prune(view):
        return lineage.Pruning(common, lineage.Carrier(common.genesis, tuple(common.keys[v] for v in view)))

    prunings = {view: prune(view) for state in states for view in state}
    for record in records.values():
        old = prune(tuple(record["before"][record["index"]]))
        new = prune(tuple(record["after"][record["index"]]))
        local = lineage.Pruning(old.coarse, new.coarse)
        assert old.then(local) == new
        assert local.aggregate(old.aggregate(ambient)) == new.aggregate(ambient)
    embedded = {}
    for view, projection in prunings.items():
        values = dict(zip(projection.coarse.keys, projection.aggregate(ambient), strict=True))
        embedded[view] = tuple(values.get(key, 0) for key in common.keys)
    return embedded


def expected_work(edges, source, receiver):
    def row(i, j):
        if i == j:
            return 0
        dx, dy = (i - j) % 5, (i // 5 - j // 5) % 5
        overlap = (2 - min(dx, 5 - dx)) * (2 - min(dy, 5 - dy))
        edge = frozenset((i, j))
        value = 8 - 2 * overlap + 9 * (6 if edge in edges else 8)
        if source and A in edge:
            value += 4 if B in edge else -4
        if receiver and B in edge:
            value += 4 if A in edge else -4
        return value

    return tuple(tuple(row(i, j) for j in LABELS) for i in LABELS)


def replay_work(common, embedded, states, original, edges):
    work, summaries = {}, {}
    for name, state in states.items():
        source = name != "before"
        receiver = name.endswith("_receiver")
        expected_edges = edges if not source else frozenset(
            e for e in edges if (A in e or (receiver and B in e)) and e != frozenset((A, B))
        )
        result = work_read(common, tuple(embedded[view] for view in state),
                           original["engine.py"], original["response_geometry.py"])
        assert result.work == expected_work(edges, source, receiver)
        assert original["response_geometry.py"].metric_passes(result)
        assert result.minimum == (54 if source else 58) and result.neighbors == expected_edges
        gate = original["operational_complex"].construct_operational_complex(
            result.labels, result.work, result.neighbors
        )
        assert gate.reason == ("degree_not_four" if source else None)
        summary = {
            "min_work": int(result.minimum), "min_edges": len(expected_edges),
            "edge_ab_work": int(result.work[A][B]), "gate": gate.status.value, "reason": gate.reason,
            "nearest_pairs": sorted(sorted(e) for e in result.neighbors),
        }
        if not source:
            assert gate.complex.tangent_rank == 2 and len(gate.complex.cycles) == 25
            for neighbors in gate.complex.adjacency:
                assert sorted(result.work[i][j] for i, j in combinations(neighbors, 2)) == [78] * 4 + [80] * 2
            summary.update({"faces": 25, "tangent_rank": 2, "neighbor_pair_work": [78] * 4 + [80] * 2})
        summaries[name] = summary
        work[name] = [list(map(int, row)) for row in result.work]
    assert work["t_source"] == work["u_source"] and work["t_receiver"] == work["u_receiver"]
    return work, summaries


def write_json(out, name, data):
    raw = (json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    (out / name).write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    original, pins = load_original(out)
    atomic, atomic_pins = load_atomic(out)
    lineage = original["lineage.py"]
    labels, _, edges = original["fixtures"].periodic_square_input(5)
    assert labels == LABELS and len(edges) == 50
    common, positions, parents, grade, before = prepare(lineage, edges)
    twins = {"t": positions[T], "u": positions[U]}
    parent = positions[PARENT]
    episodes, records, local_cases = replay_events(atomic, before, parents, parent, twins, positions[(0, 1)])
    states = {"before": before}
    for name, (source, received, _, _) in episodes.items():
        states.update({name + "_source": source, name + "_receiver": received})
    embedded = embed_grades(lineage, common, grade, states.values(), records)
    for name in twins:
        source, final = states[name + "_source"], states[name + "_receiver"]
        assert embedded[source[B]] == embedded[before[B]]
        at_parent = embedded[final[B]]
        assert at_parent[parent] == 3 and at_parent[twins[name]] == 2
        assert all(at_parent[idx] == 0 for n, idx in twins.items() if n != name)

    work, geometry = replay_work(common, embedded, states, original, edges)
    records_digest = write_json(out, "atomic_records.json", {"keys": common.keys, "records": records})
    work_digest = write_json(out, "work_tables.json", work)
    return {
        "source_pins": pins + atomic_pins,
        "vertices": len(common.keys), "view_count": len(before), "twin_addresses": twins,
        "source_index": A, "receiver_index": B, "parent": parent, "ambient_grade": grade,
        "comparison": geometry, "reachable_local_views": local_cases,
        "verified_records": {name: {k: d[k] for k in ("index", "leaf", "parent", "h_before", "h_after",
                                                       "tau_before", "tau_after", "trigger")}
                             for name, d in sorted(records.items())},
        "illegal_sole_owner_deletions_checked": 6,
        "false_trigger_rejected": True, "source_only_endpoints_equal": True,
        "receiver_own_grade_equal_immediately_after_source": True,
        "receiver_final_parent_grade": 3,
        "atomic_records_sha256": records_digest, "work_tables_sha256": work_digest,
    }


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), indent=2, sort_keys=True, allow_nan=False))
