"""Compare the historical execution path, reporting row and one-step recovery selector."""
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from hashlib import sha1, sha256
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import sys


SCI = Path("ResearchHistory/UQCF-GEM")
FIXTURE = SCI / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py"
DEMOS = SCI / "demos/v15.40-global-balance-geometry-specificity"
PINS = {
    FIXTURE: "3324c0b46e09120ae526338444a19070b692d049",
    DEMOS / "geometry_specificity_gate.py": "2e75867e6aedb82ebe3d9c1f04733e2c0d33018a",
    DEMOS / "response_generation.py": "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5",
    DEMOS / "response_geometry.py": "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    DEMOS / "incidence_target.py": "03c1f62279865aac396ea4b85f75a8d38c1629cf",
}


def hash_blob(raw):
    return sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def replace_source_entries(table, changes):
    result = [list(row) for row in table]
    for j, value in changes.items():
        result[0][j] = result[j][0] = value
    return tuple(map(tuple, result))


def intervals(values):
    spans = []
    for v in values:
        if spans and v == spans[-1][1] + 1:
            spans[-1][1] = v
        else:
            spans.append([v, v])
    return spans


def traced_candidates(f, features, rows, work, squares):
    # Inspect the actual accepted command identities at the immutable counter increment.
    recorded = []
    point = next(k for k, s in enumerate(FIXTURE.read_text().splitlines(), 1)
                 if s.strip() == "counts[i] += 1")
    function = f.degree_candidates.__code__

    def local(frame, event, arg):
        if event == "line" and frame.f_lineno == point:
            recorded.append((frame.f_locals["i"], frame.f_locals["v"]))
        return local

    def trace(frame, event, arg):
        return local if event == "call" and frame.f_code is function else None

    sys.settrace(trace)
    try:
        counts, candidates = f.degree_candidates(features, rows, work, squares)
    finally:
        sys.settrace(None)
    assert Counter(i for i, _ in recorded) == counts
    return sorted(recorded), sorted(candidates)


def run(sources, reference):
    os.chdir(sources)
    for path, pin in PINS.items():
        assert hash_blob(path.read_bytes()) == pin, path
    assert hash_blob(reference) == "42de12480f4cff0a06906914d974eb7f63f54f77"
    previous = json.loads(reference)
    sys.path[:0] = [str(FIXTURE.parent.resolve()), str(DEMOS.resolve())]
    import check_geometry_repair as f
    import geometry_specificity_gate as reporter

    m = f.modules()
    features, oldwork = f.fixture()
    parents, grades, holders = map(tuple, zip(*features))
    totals = list(grades)
    for v in range(len(features) - 1, 0, -1):
        totals[parents[v]] += totals[v]
    squares = tuple(n*n for n in totals)
    weight_masks = {}
    for v in range(1, len(features)):
        weight_masks[squares[v]] = weight_masks.get(squares[v], 0) | (1 << v)

    def distance(x, y):
        difference = x ^ y
        return sum(weight * (difference & mask).bit_count() for weight, mask in weight_masks.items())

    children = [set() for _ in parents]
    keys = [()]
    for v in range(1, len(parents)):
        children[parents[v]].add(v)
        keys.append(keys[parents[v]] + (v,))
    labels, a, b, u, mu = f.LABELS, f.A, f.B, f.ULEAF, f.MU
    pairs = list(combinations(labels, 2))
    initial = f.initial_state(features)
    grid_edges = [p for p in pairs if p[1] in f.grid()[p[0]]]
    target = reporter.construct_incidence_target([tuple((i == j) - (i == k) for i in labels)
                                                 for j, k in grid_edges])
    near_b = sorted(f.grid()[b])
    assert near_b == [7, 11, 13, 17]
    fine = m["lineage"].Carrier("receiver-command", tuple(keys))

    def root(row):
        coarse = m["lineage"].Carrier(fine.genesis, tuple(keys[v] for v in row))
        return int(m["lineage"].Pruning(fine, coarse).aggregate(grades)[0])

    def atom(rows, i, site):
        event = m["atom"].atomic(parents, rows, i, site)
        m["verify"].verify_atomic(event)
        return tuple(map(tuple, event["after"]))

    def full_gate(table):
        exact = tuple(tuple(map(Fraction, r)) for r in table)
        payload = m["projection"].Payload(5, Fraction(1), labels, exact, f.edges(table)[1], ())
        try:
            m["carriers"].build_carrier(payload)
        except ValueError as exc:
            return str(exc)
        return "accepted"

    raw_sites = [previous["sites"][0]["raw_leaf"], f.T, previous["sites"][1]["raw_leaf"]]
    assert raw_sites[0] == 662 and set(labels) - holders[raw_sites[2]] == {8, 13}
    names = ("unit_absent_B", "two_absent_B", "unit_present_B")
    results, states, legal_sets, reports = {}, {}, {}, {}
    for name, source in zip(names, raw_sites, strict=True):
        rows = atom(initial, a, source)
        # Reconstruct membership from raw coverage independent of the atom and selector.
        covers = [h - {a} if v == source else h for v, h in enumerate(holders)]
        members = [{v for v, cover in enumerate(covers) if i in cover} for i in labels]
        assert tuple(tuple(sorted(y)) for y in members) == rows
        raw = sorted((i, v) for v, cover in enumerate(covers) if v and len(cover) >= 2
                     for i in cover if not members[i].intersection(children[v]))
        masks = [sum(1 << v for v in y if v) for y in members]
        direct = tuple(tuple(distance(x, y) for y in masks) for x in masks)
        work = f.work_for(rows, squares)
        assert direct == work and min(work[i][j] for i, j in pairs) == mu
        native_raw, candidates = traced_candidates(f, features, rows, work, squares)
        assert native_raw == raw
        base_edges = [(i, j) for i, j in pairs if work[i][j] == mu]
        # Delete the editor from the graph. Residual degrees fix every required new tie.
        targets = {}
        for editor in labels:
            outside = Counter(k for p in base_edges if editor not in p for k in p)
            wanted = {j for j in labels if j != editor and outside[j] == 3}
            if len(wanted) == 4 and all(outside[j] in (3, 4) for j in labels if j != editor):
                targets[editor] = wanted
        independent = []
        for i, v in raw:
            if i not in targets:
                continue
            changed = masks[i] ^ (1 << v)
            if all((value := distance(changed, masks[j])) >= mu and
                   (value == mu) == (j in targets[i]) for j in labels if j != i):
                independent.append((i, v))
        assert candidates == independent
        assert candidates == ([(b, u)] if name == "two_absent_B" else [])
        agreed = lambda x, y: sorted(x) == raw and sorted(y) == independent
        assert not agreed(raw[1:], candidates) and not agreed(raw + [raw[0]], candidates)
        assert not agreed([(a, 0), *raw[1:]], candidates)
        assert not agreed(raw, [] if candidates else [(b, u)])
        after = atom(rows, b, u)
        after_table = f.work_for(after, squares)
        assert after[b] == tuple(v for v in initial[b] if v != u)
        assert rows[b] == initial[b] and root(rows[b]) == 242 and root(after[b]) == 244
        before_gate, after_gate = full_gate(work), full_gate(after_table)
        assert before_gate == "degree_not_four"
        assert after_gate == ("accepted" if name == "two_absent_B" else "degree_not_four")
        native_b = [v for i, v in raw if i == b]
        legal_sets[name] = native_b
        joined = {}
        for i in labels:
            joined[str(i)] = intervals(v for j, v in raw if j == i)
        results[name] = {"source": source, "W_0_12": work[a][b],
                         "W_0_E": [work[a][e] for e in near_b], "legal": len(raw),
                         "legal_by_view_intervals": joined, "legal_at_B": len(native_b),
                         "candidates": candidates, "N_0": [j for j in labels if work[a][j] == mu],
                         "N_12": [j for j in labels if work[b][j] == mu],
                         "root_before_and_after_B_U": [242, 244],
                         "native_carrier_before_and_after_B_U": [before_gate, after_gate]}
        assert work[a][b] == {"unit_absent_B": 1997, "two_absent_B": 1994, "unit_present_B": 1999}[name]
        states[name] = rows, work, after_table
        if name == "unit_present_B":
            continue
        vectors = tuple(tuple(totals[v] if v in keep else 0 for v in range(1, len(features)))
                        for keep in members)
        geom = reporter.construct_response_geometry(labels, vectors, vectors)
        assert geom.work == work
        def encode(g):
            comparison = reporter.compare_geometry(g, target)
            row = reporter._row(5, "supplied-retained-fixture", Fraction(1), False, labels,
                                g, target, comparison)
            return row["work"]["profile"][b], row["work"]["reconstruction_verified"]
        other_value = 1994 if name == "unit_absent_B" else 1997
        swapped = replace_source_entries(work, {b: other_value})
        altered = replace(geom, work=tuple(tuple(map(Fraction, row)) for row in swapped))
        reports[name] = {"genuine": encode(geom), "pair_swapped": encode(altered)}
        assert reports[name] == {"genuine": (str(work[a][b]), False), "pair_swapped": (str(other_value), False)}
        _, switched_candidates = f.degree_candidates(features, rows, swapped, squares)
        assert switched_candidates == candidates
        for editor, leaf in raw:
            change = 0
            if editor == a or editor == b:
                other = b if editor == a else a
                change = squares[leaf] if leaf in members[other] else -squares[leaf]
            low = 1994 + change - mu
            high = 1997 + change - mu
            assert (low < 0, low == 0) == (high < 0, high == 0)
    assert legal_sets[names[0]] == legal_sets[names[1]] == legal_sets[names[2]]

    unit_work, even_work = states[names[0]][1], states[names[1]][1]
    mask_records = []
    for name in names[:2]:
        rows, base, after = states[name]
        for bits in range(16):
            values = {e: (even_work if bits >> k & 1 else unit_work)[a][e] for k, e in enumerate(near_b)}
            for pair_value in (1994, 1997):
                mixed = replace_source_entries(base, {**values, b: pair_value})
                _, selected = f.degree_candidates(features, rows, mixed, squares)
                # Direct full edge and degree rebuild for precisely this hypothetical update.
                rebuilt = {(i,j): mixed[i][j] + after[i][j] - base[i][j] for i, j in pairs}
                minimum = min(rebuilt.values())
                degrees = Counter(v for p, val in rebuilt.items() if val == minimum for v in p)
                passes = all(degrees[v] == 4 for v in labels)
                assert minimum == mu and passes == ((b, u) in selected) == (bits == 15)
                mask_records.append({"background": name, "mask": bits, "W_0_12": pair_value,
                                     "candidate": passes})
    return {"schema": "receiver-command-trace/1", "fixture_blob": PINS[FIXTURE],
            "historic_report_blob": PINS[DEMOS / "geometry_specificity_gate.py"],
            "start_W_0_12": oldwork[a][b], "E": near_b, "arms": results, "reports": reports,
            "pair_swaps_preserve_all_one_step_thresholds": True,
            "same_legal_view_12_commands": True, "interventions": mask_records,
            "mask_trials": len(mask_records), "mask_passes": sum(r["candidate"] for r in mask_records),
            "record_control_rejections": ["missing", "duplicate", "substitution", "wrong_decision"]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    sources, previous, output = (Path(p).resolve() for p in sys.argv[1:])
    resource.setrlimit(resource.RLIMIT_AS, (1_500_000_000, 1_500_000_000))
    cert = run(sources, previous.read_bytes())
    raw = (json.dumps(cert, sort_keys=True, separators=(",", ":")) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({"bytes": len(raw), "sha256": sha256(raw).hexdigest(), "mask_passes": cert["mask_passes"],
                      "mask_trials": cert["mask_trials"], "candidates": {k: v["candidates"] for k, v in cert["arms"].items()}}))
