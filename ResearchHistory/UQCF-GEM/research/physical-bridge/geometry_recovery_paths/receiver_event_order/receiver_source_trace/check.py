"""Check event attribution in original receiver traces, with and without an ordinary delay."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
import lzma
from math import factorial
from pathlib import Path

from stars import Archive, PALETTES, PRIORITIES, TIPS, compressed, decode, degree, holders, ordered


def tally(counter):
    return [list(key) + [n] for key, n in sorted(counter.items())]


def three_tip_baseline():
    ledger = Path(__file__).resolve().parent.parent / "four_child_source_holder/raw.json.xz"
    data = lzma.decompress(ledger.read_bytes())
    assert sha256(data).hexdigest() == "9473b97e395cfddfaf9e38e006ff0f10273dc1056ef5e54271163ac208c6f712"
    rows = json.loads(data)["three_tip_caller_paths"]
    paths = {q: [compressed(st[1] for st in path) for _, _, target, path in rows if target == q]
             for q in (1, 2)}
    results = {}
    for target, rivals in ((1, 2), (2, 1)):
        other = {hist[:i] for hist in paths[rivals] for i in range(1, len(hist) + 1)}
        decisions = Counter()
        for hist in paths[target]:
            step = next((i for i in range(1, len(hist)) if hist[:i + 1] not in other), -1)
            decisions[step] += 1
        results[str(target)] = dict(sorted(decisions.items()))
    assert set(degree(p[-1]) for p in paths[1]) == {0, 3}
    assert set(degree(p[-1]) for p in paths[2]) == {1, 2}
    assert len(rows) == 24
    return results


def immediate(ar, start, event, rival, source, witness, detail):
    """Check all priorities, physical receiver edit prefixes, both controls and hidden grades."""
    grade_setups = []
    for r in range(3):
        if r == source:
            continue
        for left, right in combinations(TIPS, 2):
            if start[r] & ((1 << left) | (1 << right)) or detail["tip"] in (left, right):
                continue
            if holders(start, left) != holders(start, right):
                continue
            arms = []
            for u, v in ((1, 3), (3, 1)):
                g = [1] * 5
                g[left], g[right] = u, v
                arms.append(tuple(g))
            for st in (start, event, rival):
                assert ar.work(st, arms[0]) == ar.work(st, arms[1])
            assert ar.grades(start[r], arms[0]) == ar.grades(start[r], arms[1])
            grade_setups.append((r, left, right, *arms))
    observed = defaultdict(set)
    vote = Counter()
    graded_pairs = defaultdict(set)
    for order in PRIORITIES:
        for palette in PALETTES:
            low = ordered(start, order, palette)
            high = ordered(event, order, palette)
            alternate = ordered(rival, order, palette)
            for r in range(3):
                if r == source:
                    continue
                index = palette.index(r)
                m = 4 - degree(start[r])
                hi_masks = ar.local(high, index)
                lo_masks = ar.local(low, index)
                ar.marker(high, index)
                ar.marker(low, index)
                assert hi_masks[1] != lo_masks[1]
                for tag, seq in (("high", hi_masks), ("low", lo_masks)):
                    prefix = tuple(decode(x, order) for x in seq[:m])
                    observed[r, tag].add(prefix)
                if r == witness:
                    rival_trace = ar.local(alternate, index)
                    ar.marker(alternate, index)
                    assert rival_trace[:m + 1] == lo_masks[:m + 1]
            for r, left, right, ga, gb in grade_setups:
                index = palette.index(r)
                high_prev, high_after = (decode(z, order) for z in ar.marker(high, index))
                null_prev, null_after = (decode(z, order) for z in ar.marker(low, index))
                for mask in (high_prev, null_prev, null_after):
                    assert ar.grades(mask, ga) != ar.grades(mask, gb)
                fresh = ar.grades(high_after, ga) != ar.grades(high_after, gb)
                assert fresh == bool(high_after & ((1 << left) | (1 << right)))
                vote[r, left, right] += fresh
                for arm, m1, m2 in (("source", high_prev, high_after),
                                    ("control", null_prev, null_after)):
                    for i, grade in enumerate((ga, gb)):
                        graded_pairs[r, left, right, arm, i].add((ar.grades(m1, grade), ar.grades(m2, grade)))
    for r in range(3):
        if r != source:
            assert observed[r, "high"] == observed[r, "low"]
            assert len(observed[r, "high"]) == factorial(4 - degree(start[r]))
    detail["grade_checks"] = [[r, a, b, vote[r, a, b], r == witness]
                              for r, a, b, _, _ in grade_setups]
    for r, a, b, _, _ in grade_setups:
        groups = [graded_pairs[r, a, b, arm, i] for arm in ("source", "control") for i in (0, 1)]
        assert all(a.isdisjoint(b) for a, b in combinations(groups, 2))


def compare_delays(ar, start, event, rival, source, tip, owner, witness, detail):
    """A matched delay can erase source identity when the owner has a second tip."""
    robust = degree(start[owner]) == 1
    arms = (("high", event, None), ("retained-incidence control", start, (source, tip)),
            ("competing release", rival, None))
    delays = {}
    for name, entry, forbidden in arms:
        counts = Counter()
        for z in ar.reachable(entry, forbidden):
            h = ar.height(z)
            counts[h] += 1
            for r in (owner, witness):
                if name == "competing release" and r == owner:
                    continue
                assert degree(z[r]) <= degree(start[r]) <= 2
                ar.marker(z, r)
        delays[name] = dict(sorted(counts.items()))
    assert set(delays["high"]) == {3}
    expected = {2} if robust else {2, 3}
    assert set(delays["competing release"]) == set(delays["retained-incidence control"]) == expected
    detail["delay_entries_by_cover"] = delays
    # For the two actual source alternatives the ordinary transition systems differ only at tip s.
    for z in ar.reachable(event):
        twin = list(z)
        twin[source] |= 1 << tip
        twin[owner] ^= 1 << tip
        twin = tuple(twin)
        assert twin in ar.reachable(rival) and ar.cuts(z).keys() == ar.cuts(twin).keys()
    if robust:
        return
    second, = [v for v in TIPS if v != tip and start[owner] & (1 << v)]
    private = next(v for v in TIPS if holders(start, v) == (witness,))
    n, e, a = start, event, rival
    clearing = []
    for j in holders(start, second):
        if j != owner:
            cmd = j, second
            n, e, a = (ar.cuts(row)[cmd] for row in (n, e, a))
            clearing.append(cmd)
    assert ar.height(n) == ar.height(e) == ar.height(a) == 3
    first_witness = None
    rival_matches = null_matches = 0
    for order in PRIORITIES:
        for palette in PALETTES:
            nr, er, alt = (ordered(st, order, palette) for st in (n, e, a))
            r, src = palette.index(witness), palette.index(source)
            same_rival = ar.local(er, r) == ar.local(alt, r)
            same_null = ar.other_charts(er, src) == ar.other_charts(nr, src)
            if order.index(private) < order.index(tip):
                assert same_rival
                if first_witness is None:
                    first_witness = [order, palette, [decode(x, order) for x in ar.local(er, r)]]
            if order.index(second) < order.index(tip):
                assert same_null
            rival_matches += same_rival
            null_matches += same_null
    detail["collision"] = {"other_tip": second, "outsider_private_tip": private, "delay_edits": clearing,
                           "entry_high_rival_control": [e, a, n], "rival_equal_out_of_144": rival_matches,
                           "null_joint_equal_out_of_144": null_matches, "rival_witness": first_witness}


def admissible_alternative(ar):
    start = (15, 9, 17)
    s = 3
    high = ar.cuts(start)[0, s]
    low = ar.cuts(start)[1, s]
    high_route = ar.route(high)
    for state in (high, low):
        for tip_order in PRIORITIES:
            native_order = ordered(state, tip_order, (0, 1, 2))
            for palette in PALETTES:
                native = ar.producer.normalize(list(native_order), ar.producer.Q, 3, [ar.height(state)], order=palette)
                renumbered = tuple(tuple(row[j] for j in palette) for row in native)
                assert renumbered == ar.route(ordered(state, tip_order, palette))
    path = [low]
    for st in high_route[1:]:
        shadow = (st[0] | (1 << s), st[1] & ~(1 << s), st[2])
        if shadow != path[-1]:
            path.append(shadow)
    assert compressed(st[2] for st in path) == ar.local(high, 2)
    end = ar.route(low)[-1]
    # Complete the comparison to the actual low canonical endpoint, retaining union throughout.
    for add in (True, False):
        for j in range(3):
            for tip in TIPS:
                flag = 1 << tip
                if bool(end[j] & flag) == add and bool(path[-1][j] & flag) != add:
                    st = list(path[-1])
                    st[j] ^= flag
                    path.append(tuple(st))
    assert path[-1] == end
    assert all(st[0] & (1 << s) and not st[1] & (1 << s) for st in path)
    ar.verifier.path_check(ar.producer.Q, 3, [2], list(map(list, path)), list(low), list(end))
    return {"start": start, "tip": s, "receiver": 2, "original_high": high_route,
            "original_low": ar.route(low), "alternative_low": path}


def run(ar):
    specs = [s for s in ar.verifier.expected_specs() if s[0] == "R"]
    assert specs == [s for s in ar.producer.specs() if s[0] == "R"]
    raw = []
    complete = {}
    source_rows = Counter()
    marker_counts, delay_counts, grade_counts = Counter(), Counter(), Counter()
    strong_counts, collision_counts = Counter(), Counter()
    entry_checks = 0
    for _, k, *roots in specs:
        if k != 3:
            continue
        st = tuple(ar.verifier.raw_roots(k, roots))
        if ar.height(st) in (2, 3):
            source_rows[ar.height(st)] += 1
            for j in range(3):
                key = (ar.height(st), j, st[j])
                trace = ar.local(st, j)
                assert complete.setdefault(key, trace) == trace
                if degree(st[j]) <= 2:
                    ar.marker(st, j)
                    entry_checks += 1
        if ar.height(st) != 2:
            continue
        for (source, tip), event in ar.cuts(st).items():
            if ar.height(event) != 3:
                continue
            owner, = [j for j in holders(st, tip) if j != source]
            witness, = set(range(3)) - {source, owner}
            rival = ar.cuts(st)[owner, tip]
            assert ar.height(rival) == 2 and st[witness] == event[witness] == rival[witness]
            assert {x for x in ar.cuts(event) if x[0] == witness} == {x for x in ar.cuts(rival) if x[0] == witness}
            detail = {"start": st, "source": source, "tip": tip, "other_holder": owner, "observer": witness}
            immediate(ar, st, event, rival, source, witness, detail)
            compare_delays(ar, st, event, rival, source, tip, owner, witness, detail)
            robust = degree(st[owner]) == 1
            strong_counts[robust, len(ar.reachable(event))] += 1
            for r in (owner, witness):
                marker_counts[degree(st[r]), r == owner] += 1
            for name, counts in detail["delay_entries_by_cover"].items():
                for h, n in counts.items():
                    delay_counts[robust, name, h] += n
            for _, _, _, survives, is_witness in detail["grade_checks"]:
                grade_counts[is_witness, survives] += 1
                assert robust
            if "collision" in detail:
                c = detail["collision"]
                collision_counts[c["rival_equal_out_of_144"], c["null_joint_equal_out_of_144"]] += 1
            raw.append(detail)
    control = admissible_alternative(ar)
    return {"three_tip_decisions": three_tip_baseline(), "R_rows": len(specs), "full_source_events": len(raw),
            "original_rows_per_target": dict(sorted(source_rows.items())),
            "complete_single_chart_trace_classes_per_target": dict(sorted(Counter(k[0] for k in complete).items())),
            "all_labelled_entry_state_chart_checks": entry_checks,
            "order_pairs_per_event": len(PRIORITIES) * len(PALETTES),
            "immediate_by_initial_degree_and_is_other_holder": tally(marker_counts),
            "robust_by_status_and_number_of_source_delay_states": tally(strong_counts),
            "event_entry_incidence_by_robust_arm_and_height": tally(delay_counts),
            "matched_grade_comparisons_by_bystander_and_retention_count": tally(grade_counts),
            "nonrobust_by_equal_rival_trace_count_and_equal_null_joint_trace_count": tally(collision_counts),
            "admissible_alternative": control}, {"events": raw,
            "complete_single_chart_trace_table": [list(key) + [trace] for key, trace in sorted(complete.items())]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_checkout", type=Path)
    parser.add_argument("--raw", type=Path)
    options = parser.parse_args()
    summary, raw = run(Archive(options.historical_checkout.resolve()))
    data = (json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n").encode()
    summary["raw_sha256"] = sha256(data).hexdigest()
    if options.raw:
        options.raw.write_bytes(data)
    print(json.dumps(summary, sort_keys=True, indent=2))
