"""Check all post-join histories of the frozen five-chart control."""
import argparse
from collections import Counter
from functools import cache
from hashlib import sha1, sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path
from unittest.mock import patch


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def pinned(path, expected):
    data = path.read_bytes()
    assert sha1(f"blob {len(data)}".encode() + b"\x00" + data).hexdigest() == expected
    return data


def module(path, name, identity):
    pinned(path, identity)
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows(charts, columns):
    return tuple((0,) + tuple(i for i, col in enumerate(columns, 1) if c in col)
                 for c in charts)


def as_rows(data):
    return tuple(map(tuple, data))


def reachable_by_columns(charts, start):
    """Independent construction using nonempty subsets of each holder column."""
    choices = []
    for v in range(1, 8):
        holders = [c for c, row in zip(charts, start) if v in row]
        choices.append([subset for n in range(1, len(holders) + 1)
                        for subset in combinations(holders, n)])
    states = {rows(charts, cols) for cols in product(*choices)}
    edges = {}
    for s in states:
        for t in states:
            if s == t or not all(set(b) <= set(a) for a, b in zip(s, t)):
                continue
            removed = [(i, v) for i, (a, b) in enumerate(zip(s, t)) for v in set(a) - set(b)]
            if len(removed) == 1:
                edges[s, *removed[0]] = t
    return states, edges


def native_graph(atom, verify, p, start):
    work, seen, events = [start], set(), {}
    while work:
        state = work.pop()
        if state in seen:
            continue
        seen.add(state)
        for i, row in enumerate(state):
            for leaf in row[1:]:
                try:
                    d = atom.atomic(p, state, i, leaf)
                except ValueError as ex:
                    assert str(ex) == "same union"
                    continue
                verify.verify_atomic(d)
                events[state, i, leaf] = d
                work.append(as_rows(d["after"]))
    return seen, events


def match_edges(states, events, reference_states, reference_edges):
    assert states == reference_states
    assert {e: as_rows(d["after"]) for e, d in events.items()} == reference_edges


def trace_successors(mod, build):
    # Interpose only after the genuine atom returns its ordinary certificate.
    reads = Counter()
    class ReadTrace(dict):
        def __getitem__(self, key):
            reads[key] += 1
            return super().__getitem__(key)
    original = mod.atomic
    def traced(*args):
        return ReadTrace(original(*args))
    with patch.object(mod, "atomic", traced):
        result = build()
    return result, dict(reads)


def check(root, fixture_path):
    cfg = json.loads(pinned(fixture_path, "806d2bc487e358f498cafa806226d1f658e98d26"))
    demos = root / "ResearchHistory/UQCF-GEM/demos"
    src = demos / "v16.26-consistency-increment-law"
    atom = module(src / "engine.py", "atom", cfg["engine_blob"])
    verify = module(src / "verify.py", "checker", cfg["verify_blob"])
    v27 = module(demos / "v16.27-increment-attribution-closure/engine.py",
                 "attrib", "48f132d141167d9cd85ff79ec41720b5dca4f8bb")
    p1 = module(demos / "v16.23-overlap-descent/engine.py",
                "p1", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    charts = cfg["charts"]
    p = (-1,) + (0,) * len(cfg["tip_holders"])
    full = tuple(range(len(p)))
    b, a = charts.index("B"), charts.index("A")
    initial = rows(charts, cfg["tip_holders"])
    paths, joins = [], []
    for seq in cfg["receipt_paths"]:
        state = initial
        path = []
        for step in seq:
            actor, leaf = cfg["edits"][step]
            d = atom.atomic(p, state, charts.index(actor), leaf)
            verify.verify_atomic(d)
            path.append(d)
            state = as_rows(d["after"])
        paths.append(path)
        joins.append(state)
    old_bits = [v27.event_map(path)[b, 5] for path in paths]
    assert old_bits == [0, 1] and joins[0] == joins[1]
    start = joins[0]
    assert start == rows(charts, ["X","EF","E","XF","F","AB","X"])
    reference_states, reference_edges = reachable_by_columns(charts, start)
    graphs = [native_graph(atom, verify, p, s) for s in joins]
    for states, events in graphs:
        match_edges(states, events, reference_states, reference_edges)
    assert graphs[0] == graphs[1]
    states, events = graphs[0]
    assert all((d["h_before"], d["h_after"], d["delta_h"], d["trigger"]) ==
               (4, 4, 0, False) for d in events.values())

    def local(state):
        return p1.push(p, full, state[b], cfg["fine_grade"])[0]
    def owner(state):
        return "".join(c for c, row in zip(charts, state) if 6 in row)
    assert all(local(s) == (7 if 6 in s[b] else 8) for s in states)
    # Repeat the ownership test immediately after the B event, before rejoining.
    early, early_certificates = {}, {}
    for path, bit in zip(paths, old_bits):
        after_probe = as_rows(path[2]["after"])
        assert (path[2]["index"], path[2]["leaf"]) == (b, 5)
        assert owner(after_probe) == "BA" and local(after_probe) == 7
        early[str(bit)] = {}
        early_certificates[str(bit)] = {}
        for first, second in ((a, b), (b, a)):
            d = atom.atomic(p, after_probe, first, 6)
            inc, triggered = verify.verify_atomic(d)
            s = as_rows(d["after"])
            expected = 1 - bit if first == a else 0
            assert (inc, triggered) == (expected, bool(expected))
            assert local(s) == (7 if first == a else 8)
            assert d["h_before"] == 3 + bit and d["h_after"] == 3 + bit + inc
            assert owner(s) == charts[second]
            # Finish the untouched source cuts. The sole holder stays fixed.
            for later in path[3:]:
                follow = atom.atomic(p, s, later["index"], later["leaf"])
                verify.verify_atomic(follow)
                s = as_rows(follow["after"])
            assert s == as_rows(events[start, first, 6]["after"])
            early[str(bit)][charts[first]] = dict(increment=inc, trigger=triggered,
                                                  height_after=d["h_after"], B_root=int(local(s)))
            early_certificates[str(bit)][charts[first]] = d
    for (s,i,v), target in reference_edges.items():
        if owner(s) != "BA":
            assert owner(target) == owner(s) and local(s) == local(target)
        if v == 6:
            assert owner(s) == "BA" and owner(target) == ("A" if i == b else "B")

    @cache
    def terminal_paths(s):
        following = [t for (before, _, _), t in reference_edges.items() if before == s]
        if not following:
            return Counter({owner(s): 1})
        return sum((terminal_paths(t) for t in following), Counter())
    terminal = sorted(states - {s for s, _, _ in reference_edges})
    counts = terminal_paths(start)
    assert len(states) == 27 and len(events) == 54 and len(terminal) == 8
    assert counts == {"B": 24, "A": 24}

    field_hits = {"factor": Counter(), "paths": Counter()}
    # Exercise actual historical consumers on every maximal suffix endpoint.
    for end in terminal:
        fac, fr = trace_successors(atom, lambda: atom.factor(p, start, end))
        enumerated, pr = trace_successors(v27.v26, lambda: v27.paths(p, start, end))
        assert verify.verify_factor(fac)
        assert set(fr) == set(pr) == {"after"}
        assert len(enumerated) == 6
        for path in enumerated:
            assert as_rows(path[-1]["after"]) == end
            s = start
            for d in path:
                assert d == events[s, d["index"], d["leaf"]]
                s = as_rows(d["after"])
            for prefix, old in zip(paths, old_bits):
                mapping = v27.event_map(prefix + path)
                assert mapping[b,5] == old and all(mapping[d["index"],d["leaf"]] == 0 for d in path)
        for tag, val in (("factor", fr), ("paths", pr)):
            field_hits[tag].update(val)

    false_probe = dict(paths[0][2], trigger=True)
    try:
        verify.verify_atomic(false_probe)
    except ValueError as ex:
        assert str(ex) == "false certificate"
    else:
        raise AssertionError("false probe accepted")
    incomplete = events.copy()
    incomplete.pop(next(iter(incomplete)))
    try:
        match_edges(states, incomplete, reference_states, reference_edges)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing transition accepted")
    for first, second in ((a, b), (b, a)):
        s = as_rows(events[start, first, 6]["after"])
        try:
            atom.atomic(p, s, second, 6)
        except ValueError as ex:
            assert str(ex) == "same union"
        else:
            raise AssertionError("last copy removed")
    suffix_certificates = [events[key] for key in sorted(events)]
    evidence = dict(immediately_after_probe=early_certificates, after_join=suffix_certificates)
    return dict(prior_bits=old_bits, joined_holders=["X","EF","E","XF","F","AB","X"],
                suffix_states=len(states), suffix_edges=len(events), terminal_states=len(terminal),
                immediate_race_by_old_bit_and_first_deleter=early,
                full_suffix_certificate_sha256=sha256(encoded(suffix_certificates)).hexdigest(),
                full_evidence_sha256=sha256(encoded(evidence)).hexdigest(),
                next_state_field_reads={k: dict(v) for k,v in field_hits.items()},
                terminal_path_counts_by_old_bit_and_B_root={
                    str(old): {"7": counts["B"], "8": counts["A"]} for old in old_bits},
                suffix_heights=[4], suffix_increments=[0], suffix_triggers=[False],
                retained_B_root_if_B_keeps_6=7, retained_B_root_if_A_keeps_6=8,
                controls=["flipped trigger rejected", "missing edge rejected",
                          "last-copy deletion rejected in both directions"]), evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--raw", type=Path, help="save all four early and 54 post-join certificates")
    args = parser.parse_args()
    result, evidence = check(args.checkout.resolve(), Path(__file__).resolve().parents[1] / "FIXTURE.json")
    if args.raw:
        args.raw.write_bytes(encoded(evidence))
    print(json.dumps(result, sort_keys=True, indent=2))
