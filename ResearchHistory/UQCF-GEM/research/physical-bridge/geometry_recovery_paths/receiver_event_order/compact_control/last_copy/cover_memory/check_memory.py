"""Replay the two-holder cover-memory criterion. Python 3.11+ and SymPy."""
import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path

PARENT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("last_copy", PARENT / "check.py")
prior = module_from_spec(spec)
spec.loader.exec_module(prior)
prior.pinned(PARENT / "check.py", "c7b0586362e74c22612a9926f1d7135cf074dfb0")


def small_stars():
    results = {}
    for m in (2, 3, 4):
        masks = range(1, 1 << m)

        @cache
        def minimum(cols):
            return min(s.bit_count() for s in masks if all(s & t for t in cols))

        @cache
        def robust(other):
            # The contested tip has holders A=1 and B=2. Try both withdrawals.
            h = minimum((3,) + other)
            if (minimum((2,) + other) - h, minimum((1,) + other) - h) != (1, 0):
                return False
            for j, t in enumerate(other):
                if t.bit_count() < 2:
                    continue
                for k in range(m):
                    if t & (1 << k):
                        nxt = other[:j] + (t ^ (1 << k),) + other[j+1:]
                        if not robust(nxt):
                            return False
            return True

        total = passed = 0
        for size in range(4):
            for other in product(masks, repeat=size):
                outcome = robust(other)
                predicted = 1 in other and all(t & 2 == 0 for t in other)
                assert outcome == predicted
                total += 1
                passed += outcome
        results[str(m)] = dict(stars=total, fixed_orientation=passed)
    return results


def replay(root):
    cfg = json.loads(prior.pinned(PARENT.parent / "FIXTURE.json",
                                  "806d2bc487e358f498cafa806226d1f658e98d26"))
    demos = root / "ResearchHistory/UQCF-GEM/demos"
    d = demos / "v16.26-consistency-increment-law"
    atom = prior.module(d / "engine.py", "atomic", cfg["engine_blob"])
    verifier = prior.module(d / "verify.py", "verifier", cfg["verify_blob"])
    p1 = prior.module(demos / "v16.23-overlap-descent/engine.py", "p1",
                      "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    charts = cfg["charts"]
    b, a = charts.index("B"), charts.index("A")
    p = (-1,) + (0,) * 7
    full = tuple(range(8))
    initial = prior.rows(charts, cfg["tip_holders"])

    def step(s, i, v):
        event = atom.atomic(p, s, i, v)
        verifier.verify_atomic(event)
        return prior.as_rows(event["after"]), event

    def holds(s, v):
        return tuple(i for i, row in enumerate(s) if v in row)

    def root_b(s):
        return int(p1.push(p, full, s[b], cfg["fine_grade"])[0])

    def coded(states, events, s):
        # Any pre-contest substate is reachable while preserving both copies:
        # it is a componentwise subview still covering the whole star.
        before = [t for t in states if 6 in t[a] and 6 in t[b]
                  and all(set(x) <= set(y) for x, y in zip(t, s))]
        assert before
        return all(events[t, a, 6]["delta_h"] == 1 and events[t, b, 6]["delta_h"] == 0
                   for t in before)

    report, raw, starts, continuations = {}, {}, {}, {}
    for seq in cfg["receipt_paths"]:
        state = initial
        for e in seq[:3]:
            who, tip = cfg["edits"][e]
            state, old = step(state, charts.index(who), tip)
        assert (old["index"], old["leaf"]) == (b, 5)
        bit = old["delta_h"]
        expected_move = ("E", 3) if bit == 0 else ("X", 1)
        all_states, all_events = prior.native_graph(atom, verifier, p, state)
        starts[bit] = state
        continuations[bit] = (all_states, all_events)
        ref_s, ref_e = prior.reachable_by_columns(charts, state)
        prior.match_edges(all_states, all_events, ref_s, ref_e)
        assert not coded(all_states, all_events, state)
        immediate = {(i, v): prior.as_rows(e["after"]) for (s, i, v), e in all_events.items()
                     if s == state and v != 6}
        enabling = [(charts[i], v) for (i, v), t in immediate.items() if coded(all_states, all_events, t)]
        assert enabling == [expected_move]
        mover, tip = enabling[0]
        prepared, setup = step(state, charts.index(mover), tip)
        assert holds(prepared, tip) == (a,) and prepared[b] == (0, 6)
        assert state[b] == prepared[b] and root_b(state) == root_b(prepared) == 7
        states, events = prior.native_graph(atom, verifier, p, prepared)
        ref_states, edges = prior.reachable_by_columns(charts, prepared)
        prior.match_edges(states, events, ref_states, edges)
        outgoing = {s: [] for s in states}
        races = []
        for (s, i, v), t in edges.items():
            outgoing[s].append((v, t))
            if v == 6:
                d = events[s, i, v]
                inc = d["delta_h"]
                assert inc == int(i == a) == int(6 in t[b])
                assert d["trigger"] == bool(inc) and root_b(t) == 8 - inc
                races.append(d)
            elif len(holds(s, 6)) == 1:
                assert holds(s, 6) == holds(t, 6) and root_b(s) == root_b(t)
        for s in states:
            menu = {v for (before, i, v) in events if before == s and i == b}
            assert menu == ({6} if len(holds(s, 6)) == 2 else set())
            if s[b] == (0, 6):
                assert p1.push(p, full, s[b], cfg["fine_grade"]) == (7, 1)
            else:
                assert s[b] == (0,) and p1.push(p, full, s[b], cfg["fine_grade"]) == (8,)

        @cache
        def finishes(s):
            if not outgoing[s]:
                return Counter({root_b(s): 1})
            return sum((finishes(t) for _, t in outgoing[s]), Counter())

        term = [s for s in states if not outgoing[s]]
        assert all(len(holds(s, 6)) == 1 and root_b(s) in (7, 8) for s in term)
        counts = finishes(prepared)
        assert (len(states), len(edges), len(races), len(term)) == (63, 165, 42, 12)
        assert counts == {7: 144, 8: 144}
        # Independent control: consume A's other possible holdings before
        # resolving 6. A and B then have identical rows and both increments vanish.
        erased = state
        for v in state[a]:
            if v not in (0, 6):
                erased, _ = step(erased, a, v)
        assert erased[a] == erased[b] == (0, 6)
        zero_controls = [step(erased, i, 6)[1] for i in (a,b)]
        assert all(not e["trigger"] and e["delta_h"] == 0 for e in zero_controls)
        # Same admissible editor set in both source histories; every possible
        # order runs until none of those editors has a remaining deletion.
        exterior = {}
        for size in range(4):
            for group in combinations("EFX", size):
                enabled = {charts.index(c) for c in group}
                pending, seen, ends = [state], set(), []
                while pending:
                    s = pending.pop()
                    if s in seen:
                        continue
                    seen.add(s)
                    nxt = [prior.as_rows(e["after"]) for (before,i,_),e in all_events.items()
                           if before == s and i in enabled]
                    if nxt:
                        pending.extend(nxt)
                    else:
                        ends.append(s)
                scores = [coded(all_states, all_events, s) for s in ends]
                other_a = [v for v in state[a] if v not in (0,6)]
                expected = any(set(holds(state,v)) - {a} <= enabled for v in other_a)
                assert ends and all(score == expected for score in scores)
                exterior["".join(group) or "none"] = dict(states=len(seen), terminals=len(ends),
                                                          all_encode=expected)
        summary = dict(unique_single_preparation=expected_move, candidates=len(immediate),
                       states=len(states), edges=len(edges), pre_contest_states=len(races)//2,
                       terminal_states=len(term), maximal_paths_by_B_root=dict(counts),
                       exterior_only_preparations=exterior,
                       contest_height_pairs=sorted({(e["h_before"],e["h_after"]) for e in races}))
        report[str(bit)] = summary
        raw[str(bit)] = dict(probe=old, preparation=setup, controls=zero_controls,
                             prepared_edges=[events[e] for e in sorted(events)])
    assert set(report) == {"0","1"}
    # Product of the two legal transition relations with the SAME event label
    # in both arms. Leave tip 6 untouched throughout this preparation search.
    pending = [(starts[0], starts[1])]
    paired, paired_edges = set(), []
    while pending:
        pair = pending.pop()
        if pair in paired:
            continue
        paired.add(pair)
        choices = []
        for bit, s in enumerate(pair):
            states, events = continuations[bit]
            assert not coded(states, events, s)
            choices.append({(i, v): prior.as_rows(d["after"])
                            for (before, i, v), d in events.items() if before == s and v != 6})
        for edit in choices[0].keys() & choices[1].keys():
            dest = tuple(choices[bit][edit] for bit in (0, 1))
            paired_edges.append((pair, edit, dest))
            pending.append(dest)
    assert (len(paired), len(paired_edges)) == (9, 12)
    return dict(historical=report, common_successful_preparation=dict(states=9, edges=12,
                states_with_robust_encoding_in_either_arm=0), independent_small_stars=small_stars(),
                raw_sha256=sha256(prior.encoded(raw)).hexdigest()), raw


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--raw", type=Path)
    args = parser.parse_args()
    result, raw = replay(args.checkout.resolve())
    if args.raw:
        args.raw.write_bytes(prior.encoded(raw))
    print(json.dumps(result, indent=2, sort_keys=True))
