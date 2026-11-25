"""Replay local full-mask departures and pair work in the archived four-child writer."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import lzma
from pathlib import Path
import sys
from unittest.mock import patch

from check_matched_source_events import (
    CHILDREN, CONTROL, FOUR, FOUR_PINS, HIST, LABELS, SOURCE, STAR, WITNESS,
    atlas, independent_census, members, specimen, state_masks, unit_grade,
)
from check_receiver_command import FIXTURE, PINS, SCI, hash_blob

FULL = 31  # Genesis root plus all four leaves.
PAIRS = tuple(combinations(LABELS, 2))
BLANK = 0


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_sources(root):
    import importlib.util

    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, root / path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    atom = SCI / "demos/v16.26-consistency-increment-law"
    lineage = SCI / "foundational-closure-verification/lineage.py"
    pins = {FOUR / (name + ".py"): ident for name, ident in FOUR_PINS.items()}
    pins.update({FIXTURE: PINS[FIXTURE], lineage: "e95e3e978779164dd91f09b80e3389247e6320c2",
                 atom / "engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
                 atom / "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3"})
    for path, ident in pins.items():
        require(hash_blob((root / path).read_bytes()) == ident, str(path))
    sys.path.insert(0, str(root / FOUR))
    import producer
    import verifier
    return (producer, verifier, load("passage_atoms", atom / "engine.py"),
            load("passage_atom_verify", atom / "verify.py"), load("passage_lineage", lineage),
            load("passage_geometry", FIXTURE))


def views(state):
    return [members(mask, range(5)) for mask in state]


def event_post(atom, verifier, before, source, leaf):
    event = atom.atomic(STAR, before, source, leaf)
    verifier.verify_atomic(event)
    return tuple(state_masks(event["after"]))


def run_writer(r, v, state):
    declared = specimen(views(state))
    with patch.object(r, "specs", return_value=[declared]):
        rec, = r.produce()["records"]
    require(rec["status"] == "ok" and rec["identity"] == declared and rec["start"] == list(state),
            "incomplete historical R invocation")
    v.path_check(r.Q, 4, rec["q"], rec["path"], rec["start"], rec["end"])
    return rec


def state_key(state):
    return ",".join(map(str, state))


def full_departures(path):
    result = [0] * 4
    for prev, after in zip(path, path[1:]):
        for j in LABELS:
            if prev[j] == FULL and after[j] != FULL:
                result[j] += 1
    return result


def measured(q, path):
    seen = [any(s[j] == FULL for s in path) for j in LABELS]
    together = any(all(mask == FULL for mask in s) for s in path)
    zero_work = any(all((s[i] ^ s[j]).bit_count() == 0 for i, j in PAIRS) for s in path)
    return [q, seen, together, zero_work, full_departures(path)]


def prediction(q, endpoint):
    crosses = q <= 2
    return [q, [crosses] * 4, crosses, crosses,
            [int(crosses and m != FULL) for m in endpoint]]


def relabel(before, chart_map, leaf_map):
    result = [None] * 4
    for old, view in enumerate(before):
        result[chart_map[old]] = sorted(0 if v == 0 else leaf_map[v-1] for v in view)
    return result


def trace_live(r, v, atom, atom_verify, lineage, geometry, start):
    """Read observer-only frame data at the exact in-place clear and guard call."""
    lift = r.lift_root_path.__code__
    source = Path(lift.co_filename).read_text().splitlines()
    line, = (i for i, s in enumerate(source, 1) if s.strip() == "current[x]&=~(1<<child)")
    guard_line, = (i for i, s in enumerate(source, 1)
                   if s.strip().startswith("if abs(coordinate(current,children)-targets[0])"))
    coordinate = r.coordinate
    clears, guard, objects = [], [], []

    def observe(frame, kind, arg):
        if frame.f_code is not lift:
            return None
        if kind == "line" and frame.f_lineno == line:
            scope = frame.f_locals
            obj, j, leaf = scope["current"], scope["x"], scope["child"]
            if obj[j] == FULL:
                clears.append([len(scope["path"]), j, leaf, list(obj)])
                objects.append(obj)
        return observe

    def verify_live(obj, current, snapshot):
        require(obj is current and obj == snapshot, "guard received a copy or stale state")

    sample = list(start)
    try:
        verify_live(sample.copy(), sample, sample.copy())
    except ValueError:
        pass
    else:
        raise AssertionError("equal-by-value false guard identity passed")

    def observe_guard(state, children):
        q = coordinate(state, children)
        caller = sys._getframe(1)
        if caller.f_code is lift and caller.f_lineno == guard_line:
            verify_live(state, caller.f_locals["current"], caller.f_locals["path"][-1])
            objects.append(state)
            guard.append([list(state), q])
        return q

    previous = sys.gettrace()
    try:
        with patch.object(r, "coordinate", observe_guard), patch.object(
                lineage.Pruning, "aggregate", side_effect=RuntimeError("P1 called")) as probe:
            try:
                unit_grade(lineage, views(start)[0])
            except RuntimeError as error:
                require(str(error) == "P1 called", "P1 interception")
            else:
                raise AssertionError("inactive P1 probe")
            probe.reset_mock()
            sys.settrace(observe)
            rec = run_writer(r, v, start)
            p1_calls = probe.call_count
    finally:
        sys.settrace(previous)
    path = rec["path"]
    require([row for row, _ in guard] == path[1:] and objects and
            all(obj is objects[0] for obj in objects), "incomplete guard trace")
    expected = []
    for i, (before, after) in enumerate(zip(path, path[1:]), 1):
        for j in LABELS:
            if before[j] == FULL and after[j] != FULL:
                leaf = (before[j] ^ after[j]).bit_length() - 1
                require(event_post(atom, atom_verify, views(before), j, leaf) == tuple(after),
                        "wrong source or local edit")
                expected.append([i, j, leaf, before])
    require(clears == expected, "departure missing from live clear")
    work, roots = [], []
    for s in path:
        raw = views(s)
        table = geometry.work_for(raw, [1] * 5)
        six = [table[i][j] for i, j in PAIRS]
        require(six == [(s[i] ^ s[j]).bit_count() for i, j in PAIRS], "work evaluator")
        work.append(six)
        roots.append([unit_grade(lineage, y)[0] for y in raw])
    return dict(q=rec["q"][0], after_source=list(start), end=path[-1], steps=len(path)-1,
                full_chart_deletions=clears, live_guard_cover=[q for _, q in guard],
                simultaneous_full_indices=[i for i, s in enumerate(path) if s == [FULL]*4],
                zero_work_indices=[i for i, w in enumerate(work) if not any(w)],
                minimum_total_pair_work=min(map(sum, work)), minimum_root_grades=list(map(min, zip(*roots))),
                live_guard_checked_every_edit=True, p1_calls_in_writer=p1_calls)


def direct_short_path(r, v, start, end):
    current = list(start)
    path = [current.copy()]
    for adding in (True, False):
        for j in LABELS:
            for leaf in CHILDREN:
                bit = 1 << leaf
                if bool(end[j] & bit) == adding and bool(current[j] & bit) != adding:
                    current[j] ^= bit
                    path.append(current.copy())
    peak = v.path_check(r.Q, 4, [2], path, list(start), list(end))
    require(peak == 0 and all(FULL not in s for s in path), "alternative path control")
    return path


def expected_domain():
    return {columns: [[leaf, prediction(q, end)] for leaf, q, end in moves]
            for columns, (_, moves) in independent_census().items()}


def write_json(file, value):
    file.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    r, verifier, atom, atom_verify, lineage, geometry = load_sources(args.source.resolve())
    paths = {}

    @lru_cache(maxsize=None)
    def replay(state):
        rec = run_writer(r, verifier, state)
        paths[state_key(state)] = rec["path"]
        return measured(rec["q"][0], rec["path"])

    domain = {}
    for columns in product(range(2, 16, 2), repeat=4):
        before = atlas(columns)
        domain[columns] = [[v, replay(event_post(atom, atom_verify, before, SOURCE, v))]
                           for v, col in enumerate(columns, 1)
                           if col & (1 << SOURCE) and col.bit_count() >= 2]
    require(domain == expected_domain(), "whole-chart enumeration or passage prediction differs")
    pairs = [(list(cols), a, b, ma[1] != mb[1]) for cols, moves in sorted(domain.items())
             for (a, ma), (b, mb) in combinations(moves, 2)]
    orbit = []
    for chart_map in permutations(LABELS):
        for leaf_map in permutations(CHILDREN):
            before = relabel(atlas(WITNESS), chart_map, leaf_map)
            arms = []
            for cut in (3, 4):
                state = event_post(atom, atom_verify, before, chart_map[SOURCE], leaf_map[cut-1])
                obs = replay(state)
                require(obs == prediction(3 if cut == 3 else 2, paths[state_key(state)][-1]),
                        "relabeled passage")
                require(state[chart_map[BLANK]] == 1, "blank receiver prior changed")
                arms.append(state_key(state))
            orbit.append([list(chart_map), list(leaf_map), *arms])

    def post(cols, leaf):
        return event_post(atom, atom_verify, atlas(cols), SOURCE, leaf)

    witness = [trace_live(r, verifier, atom, atom_verify, lineage, geometry, post(WITNESS, leaf))
               for leaf in (3, 4)]
    neutral = [replay(post(CONTROL, leaf)) for leaf in (3, 4)]
    require(neutral[0] == neutral[1], "same-target control differs")
    swapped = next(row for row in orbit if row[:2] == [[3, 1, 2, 0], [1, 2, 3, 4]])
    ends = [paths[key][-1][3] for key in swapped[2:]]
    require(ends == [1, 1], "terminal persistence control")
    alternative = direct_short_path(r, verifier, witness[1]["after_source"], witness[1]["end"])
    rows = [[list(cols), moves] for cols, moves in sorted(domain.items())]
    data = dict(preparations=rows, pairs=pairs, relabelings=orbit, paths=paths)
    payload = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (out/"all_chart_paths.json.xz").write_bytes(lzma.compress(payload))
    distribution = Counter(m[0] for moves in domain.values() for _, m in moves)
    report = dict(inherited=HIST, preparations=len(rows), arms=sum(distribution.values()), pairs=len(pairs),
                  separating_pairs=sum(row[3] for row in pairs), arms_by_cover=dict(distribution),
                  relabelings=len(orbit), unique_paths_stored=len(paths), witness_cut_order=[3,4],
                  witness=witness, same_target_control=neutral, swapped_blank_end_masks=ends,
                  exact_cover_two_detour=alternative, universe_sha256=sha256(payload).hexdigest())
    write_json(out/"all_chart_certificate.json", report)
    print(json.dumps({k: report[k] for k in ("preparations","arms","pairs","separating_pairs","relabelings",
                                             "unique_paths_stored","universe_sha256")}))


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Historical verifiers require assertions")
    main()
