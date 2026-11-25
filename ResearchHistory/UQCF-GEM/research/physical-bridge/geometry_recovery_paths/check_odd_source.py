"""Replay the frozen odd-source construction against the archived recovery fixture."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha1, sha256
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import sys


FIXTURE = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py")
FIXTURE_BLOB = "3324c0b46e09120ae526338444a19070b692d049"


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def run(sources):
    os.chdir(sources)
    data = FIXTURE.read_bytes()
    assert sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == FIXTURE_BLOB
    sys.path.insert(0, str(FIXTURE.resolve().parent))
    import check_geometry_repair as f

    m = f.modules()
    features, target = f.fixture()
    parents, grades, support = map(tuple, zip(*features))
    labels = f.LABELS
    pairs = tuple(combinations(labels, 2))
    initial = f.initial_state(features)
    subtotal = list(grades)
    keys = [()]
    for v in range(1, len(parents)):
        keys.append(keys[parents[v]] + (v,))
    for v in range(len(parents) - 1, 0, -1):
        subtotal[parents[v]] += subtotal[v]
    squares = tuple(s * s for s in subtotal)
    assert [v for v, key in enumerate(keys) if len(key) >= 2] == [f.CHILD]
    assert support[f.CHILD] == {f.A}
    fine = m["lineage"].Carrier("odd-source-replay", tuple(keys))

    @lru_cache(None)
    def retained(row):
        keep = set(row)
        native_view = m["lineage"].Carrier(fine.genesis, tuple(keys[v] for v in row))
        native = m["lineage"].Pruning(fine, native_view).aggregate(grades)
        direct = dict.fromkeys(row, 0)
        for v, grade in enumerate(grades):
            while v not in keep:
                v = parents[v]
            direct[v] += grade
        assert tuple(direct[v] for v in row) == native
        moment = sum(len(keys[v]) * direct[v] for v in row)
        assert moment == sum(subtotal[v] for v in row if v)
        return direct[0], moment

    def legal_edit(rows, i, v, native=False):
        members = set(rows[i])
        assert v != 0 and v in members and all(parents[w] != v for w in members)
        assert any(v in row for j, row in enumerate(rows) if i != j)
        after = list(rows)
        after[i] = tuple(w for w in rows[i] if w != v)
        after = tuple(after)
        if native:
            event = m["atom"].atomic(parents, rows, i, v)
            m["verify"].verify_atomic(event)
            assert tuple(map(tuple, event["after"])) == after
        return after

    def work(rows):
        return f.work_for(rows, squares)

    def gate(table):
        minimum, edges = f.edges(table)
        exact = tuple(tuple(map(Fraction, row)) for row in table)
        payload = m["projection"].Payload(f.SIDE, Fraction(1), labels, exact, edges, ())
        try:
            carrier = m["carriers"].build_carrier(payload)
        except ValueError as exc:
            return {"accepted": False, "reason": str(exc), "minimum": minimum}, None
        return {"accepted": True, "receipt": dict(carrier.receipt), "minimum": minimum}, carrier

    def selected_cut(i):
        return frozenset((f.offset(i, 2, 1), f.offset(i, 2, 2)))

    sites, selected, cuts = [], [], tuple(map(selected_cut, labels))
    for i, cut in enumerate(cuts):
        vertices = [v for v in range(1, len(features)) if f.ALL - support[v] == cut]
        mass = sum(squares[v] for v in vertices)
        j, k = tuple(sorted(cut))
        ordinary_t = support[f.T]
        expected = 35 if cut & {f.A, f.B} else 32 + 6 * ((j in ordinary_t) != (k in ordinary_t))
        assert k in f.grid()[j] and mass == expected
        unit = min(v for v in vertices if parents[v] == 0 and grades[v] == subtotal[v] == 1)
        assert i not in cut and len(support[unit]) == 23
        sites.append(unit)
        selected.append({"view": i, "raw_leaf": unit, "absent_from": sorted(cut), "cut_mass": mass})

    def valid_sites(candidate):
        return (len(candidate) == len(labels) and len(set(candidate)) == len(labels)
                and all(v == min(w for w in initial[i] if w != 0 and parents[w] == 0
                                  and grades[w] == subtotal[w] == 1 and f.ALL - support[w] == cuts[i])
                        for i, v in enumerate(candidate)))

    assert valid_sites(sites)
    assert not valid_sites(sites[:-1])
    assert not valid_sites([sites[1], *sites[1:]])
    assert not valid_sites([sites[1], sites[0], *sites[2:]])
    assert len(set(cuts)) == len(labels)
    assert all(not (j in cuts[i] and i in cuts[j]) for i, j in pairs)

    initial_roots, initial_moments = map(tuple, zip(*(retained(row) for row in initial)))
    starting_work = work(initial)
    assert starting_work == target
    base_min, base_edges = f.edges(starting_work)
    neighbors = f.grid()
    assert set(base_edges) == {(i, j) for i, j in pairs if j in neighbors[i]}
    assert min(starting_work[i][j] - base_min for i, j in pairs if (i, j) not in base_edges) >= 4
    assert len({v % 2 for v in initial_moments}) == 1

    def endpoint(rows):
        table = work(rows)
        vectors = tuple(tuple(subtotal[v] if v in keep else 0 for v in range(1, len(features)))
                        for keep in map(set, rows))
        original = m["work"].construct_response_geometry(labels, vectors, vectors)
        assert original.work == table and m["work"].metric_passes(original)
        root, moment = map(tuple, zip(*(retained(row) for row in rows)))
        gain = [v - z for v, z in zip(root, initial_roots)]
        loss = [z - v for v, z in zip(moment, initial_moments)]
        assert gain == loss
        assert all((table[i][j] - moment[i] - moment[j]) % 2 == 0 for i, j in pairs)
        result, carrier = gate(table)
        result.update(root_grades=root, depth_moments=moment, increments=gain,
                      B_root=root[f.B], work_sha256=digest(table))
        return result, carrier

    start, base = endpoint(initial)
    assert base and base_min == 1984 and start["B_root"] == 242
    rows = initial
    prefixes = []
    for i, v in enumerate(sites):
        rows = legal_edit(rows, i, v, native=True)
        table = work(rows)
        result, carrier = gate(table)
        result["total_edits"] = i + 1
        assert all(table[i0][j0] == starting_work[i0][j0]
                   + (int(i0 <= i) * (1 - 2 * int(j0 in cuts[i0])))
                   + (int(j0 <= i) * (1 - 2 * int(i0 in cuts[j0]))) for i0, j0 in pairs)
        assert (carrier is not None) == (i == len(labels) - 1)
        prefixes.append(result)
        if i == f.A:
            odd_only = rows
    odd_end = rows
    odd, last = endpoint(odd_end)
    final_work = work(odd_end)
    for i, j in pairs:
        gain = final_work[i][j] - starting_work[i][j]
        assert gain in (0, 2)
        if j in neighbors[i] or neighbors[i] & neighbors[j]:
            assert gain == 2
    assert f.edges(final_work) == (1986, base_edges)
    for name in ("labels", "adjacency", "cycles", "directed_edges", "direction_classes",
                 "local_vectors", "tangent_rank", "d4_actions"):
        assert getattr(base.complex, name) == getattr(last.complex, name)
    assert base.baseline == last.baseline and odd["increments"] == [1] * len(labels)
    assert all(sum(v in row for row in odd_end) == 22 for v in sites)

    even_only = legal_edit(initial, f.A, f.T, native=True)
    even_end = legal_edit(even_only, f.B, f.ULEAF, native=True)
    even, _ = endpoint(even_end)
    cross1, _ = endpoint(legal_edit(odd_only, f.B, f.ULEAF, native=True))
    cross_rows, omitted = even_only, initial
    for i in labels[1:]:
        cross_rows = legal_edit(cross_rows, i, sites[i])
        omitted = legal_edit(omitted, i, sites[i])
    cross2, _ = endpoint(cross_rows)
    omitted_gate, _ = gate(work(omitted))
    assert not omitted_gate["accepted"]
    arms = {"odd_source_unit_schedule": odd, "even_source_B_U": even,
            "odd_source_B_U": cross1, "even_source_unit_schedule": cross2}
    assert [(r["accepted"], r["B_root"]) for r in (odd, even, cross1, cross2)] == [
        (True, 243), (True, 244), (False, 244), (False, 243)]
    assert even["minimum"] == 1984

    correction = min(v for v in odd_only[f.A] if v and parents[v] == 0 and subtotal[v] == 1
                     and len(support[v]) > 1)
    corrected = legal_edit(odd_only, f.A, correction, native=True)
    gain_a = initial_moments[f.A] - retained(corrected[f.A])[1]
    assert gain_a == 2 and corrected[1:] == initial[1:]
    corrected_gate, _ = gate(work(corrected))

    # For all collapse steps, check the exact leaf and same-union predicates.
    # Check both ends of each row's deletion list against the original event and verifier.
    collapse = odd_only
    representatives, counts = [], []
    for i in (1, 4):
        order = tuple(sorted(set(collapse[i]) - {0}, reverse=True))
        for k, v in enumerate(order):
            native = k in (0, len(order) - 1)
            collapse = legal_edit(collapse, i, v, native=native)
            if native:
                representatives.append([i, v])
        counts.append(len(order))
        assert collapse[i] == (0,)
    assert collapse[f.A] == odd_only[f.A] and collapse[f.B] == initial[f.B]
    assert (initial_moments[f.A] - retained(collapse[f.A])[1]) % 2 == 1
    collapse_work = work(collapse)
    collapse_gate, _ = gate(collapse_work)
    assert collapse_work[1][4] == 0 and collapse_gate["reason"] == "work_off_diagonal"

    return {"schema": "odd-source-root/1", "fixture_blob": FIXTURE_BLOB,
            "science_blobs": {str(k): v for k, v in f.PINS.items()},
            "vertices": len(features), "pairs": len(pairs), "sites": selected, "initial": start,
            "arms": arms, "odd_path_prefixes": prefixes, "first_return_further_edits": 24,
            "unit_path_graph_directions_baseline_identical": True,
            "pairwise_work_changes": dict(sorted(Counter(final_work[i][j] - starting_work[i][j]
                                                         for i, j in pairs).items())),
            "source_omitted": omitted_gate, "source_correction": {"leaf": correction,
            "source_loss": gain_a, "B_untouched": True, "gate": corrected_gate},
            "permanent_rejection": {"rows": [1, 4], "deletion_counts": counts,
            "native_representatives": representatives, "A_B_frozen": True, "work_1_4": 0,
            "gate": collapse_gate}, "corrupted_site_lists_rejected": ["missing", "duplicate", "swapped"]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    source_root, output = (Path(arg).resolve() for arg in sys.argv[1:])
    resource.setrlimit(resource.RLIMIT_AS, (1_500_000_000, 1_500_000_000))
    report = run(source_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    output.write_bytes(raw)
    print(json.dumps({"sha256": sha256(raw).hexdigest(), "bytes": len(raw),
                      "arms": {k: [v["accepted"], v["B_root"]] for k, v in report["arms"].items()}}))
