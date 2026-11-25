"""Verify a coverage-dependent native deletion in two equally admitted preparations."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb
import os
from pathlib import Path
import resource
import sys

from check_receiver_command import FIXTURE, PINS, hash_blob, intervals


def run(sources):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path.insert(0, str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f

    m = f.modules()
    features, target = f.fixture()
    labels, a, b = f.LABELS, f.A, f.B
    parents, grades, holders = map(tuple, zip(*features))
    totals = list(grades)
    for v in range(len(features) - 1, 0, -1):
        totals[parents[v]] += totals[v]
    squares = tuple(x*x for x in totals)
    p, q = 662, 718
    c = set(labels) - holders[q]
    assert c == {8, 13} and set(labels) - holders[p] == {7, 12}
    r = min(v for v, h in enumerate(holders) if set(labels) - h == {a, b} and
            parents[v] == 0 and totals[v] == grades[v] == 1)
    assert sum(squares[v] for v, h in enumerate(holders) if set(labels)-h == {a,b}) == 33
    assert all(parents[v] == 0 and totals[v] == grades[v] == 1 for v in (p,q,r))
    others = sorted(holders[q] - {a,b})
    assert others == sorted(holders[r] - c) and len(others) == 21
    shared = [v for v in range(1,len(features)) if {a,b} <= holders[v]]
    sizes = Counter(len(holders[v]) for v in shared)
    assert all(v >= 6 and parents[v] == 0 and v not in parents for v in shared)
    assert set(sizes) == {23,24}

    initial = f.initial_state(features)
    keys = [()]
    for v in range(1,len(features)):
        keys.append(keys[parents[v]] + (v,))
    lin = m["lineage"]
    fine = lin.Carrier("coverage-receiver-veto",tuple(keys))
    pairs = list(combinations(labels, 2))

    def atom(rows, i, site):
        event = m["atom"].atomic(parents, rows, i, site)
        m["verify"].verify_atomic(event)
        after = tuple(map(tuple, event["after"]))
        assert all(row == (tuple(v for v in rows[i] if v != site) if k == i else rows[k])
                   for k, row in enumerate(after))
        return after

    @lru_cache(maxsize=None)
    def root(row):
        coarse = lin.Carrier(fine.genesis, tuple(keys[v] for v in row))
        native = lin.Pruning(fine, coarse).aggregate(grades)
        keep = set(row)
        result = 0
        for v, grade in enumerate(grades):
            while v not in keep:
                v = parents[v]
            if v == 0:
                result += grade
        assert result == native[0]
        return result

    def expected(edits):
        coverage = [set(row) for row in holders]
        children = [set() for _ in parents]
        for v in range(1,len(parents)):
            children[parents[v]].add(v)
        for i, v in edits:
            assert v != 0 and i in coverage[v] and len(coverage[v]) > 1
            assert all(i not in coverage[child] for child in children[v])
            coverage[v].remove(i)
        rows = tuple(tuple(v for v, h in enumerate(coverage) if i in h) for i in labels)
        menu = tuple(v for v, h in enumerate(coverage) if v and b in h and len(h) >= 2
                     and all(b not in coverage[w] for w in children[v]))
        return rows, menu

    def command_menu(rows):
        local = set(rows[b])
        outside = set().union(*(row for i,row in enumerate(rows) if i != b))
        retained_parents = {parents[v] for v in local}
        return tuple(sorted((local & outside) - retained_parents - {0}))

    def probe(rows):
        try:
            result = atom(rows,b,q)
        except ValueError as exc:
            assert str(exc) == "same union"
            return "same union", None
        return "accepted", result

    def table_for(rows, full_work=False):
        table = f.work_for(rows, squares)
        if full_work:
            data = tuple(tuple(totals[v] if v in keep else 0 for v in range(1,len(features)))
                         for keep in map(set, rows))
            geometry = m["work"].construct_response_geometry(labels, data, data)
            assert m["work"].metric_passes(geometry) and geometry.work == table
        return table

    def gate(table):
        minimum, edges = f.edges(table)
        payload = m["projection"].Payload(5,Fraction(1),labels,tuple(tuple(map(Fraction,row)) for row in table),edges,())
        try:
            carrier = m["carriers"].build_carrier(payload)
        except ValueError as exc:
            return str(exc), None
        assert carrier.baseline.flat and minimum > 0
        return "accepted", carrier

    prep_orders = {"original": [], "isolated": [(i,q) for i in others],
                   "balanced": [(i,v) for i in others for v in (q,r)]}
    before = table_for(initial,True)
    assert before == target and before[a][b] == 1998
    state0, carrier0 = gate(before)
    assert state0 == "accepted"
    root_a, root_b = root(initial[a]), root(initial[b])
    runs, prepared_tables = {}, {}
    untouched_menu = command_menu(initial)
    unrelated = min(v for v in untouched_menu if v not in (p,q,r) and
                    totals[v] == grades[v] == 1 and len(holders[v]) > 2)
    for name, prep in prep_orders.items():
        rows = initial
        for i,v in prep:
            rows = atom(rows,i,v)
        rebuilt, menu = expected(prep)
        assert rows == rebuilt and menu == command_menu(rows) == untouched_menu
        assert rows[a] == initial[a] and rows[b] == initial[b]
        table = table_for(rows,True)
        status, carrier = gate(table)
        prepared_tables[name] = table
        before_probe, before_return = probe(rows)
        assert table[a][b] == 1998 and before_probe == "accepted"
        assert root(before_return[b]) == 243
        assert (table == before) == (name != "isolated")
        assert (carrier == carrier0) == (name != "isolated")
        assert (status == "accepted") == (name != "isolated")
        actual_holders = sorted(i for i in labels if q in rows[i])
        assert actual_holders == (sorted(holders[q]) if name == "original" else [a,b])
        actual_r = sorted(i for i in labels if r in rows[i])
        assert actual_r == (sorted(c) if name == "balanced" else sorted(holders[r]))
        different = sum(table[i][j] != before[i][j] for i,j in pairs)
        outcomes = {}
        for source, pair_work in ((p,1997), (q,1999), (f.T,1994)):
            after = atom(rows,a,source)
            rebuilt, menu_after = expected(prep + [(a,source)])
            assert after == rebuilt and after[b] == rows[b] and root(after[b]) == root_b == 242
            assert root(after[a])-root_a == totals[source]
            assert command_menu(after) == menu_after
            removed = sorted(set(menu) - set(menu_after))
            blocked = source == q and name != "original"
            assert removed == ([q] if blocked else []) and set(menu_after) <= set(menu)
            if blocked:
                # Forge a claimed successful B deletion after B became the sole holder.
                false_event = dict(m["atom"].atomic(parents,rows,b,q))
                false_event["before"] = [list(row) for row in after]
                false_event["after"] = [list(row) for row in after]
                false_event["after"][b].remove(q)
                try:
                    m["verify"].verify_atomic(false_event)
                except ValueError as exc:
                    assert str(exc) == "union"
                else:
                    raise AssertionError("False success receipt passed the independent verifier")
            result, returned = probe(after)
            assert (result == "same union") == blocked
            returned_root = root(returned[b]) if returned is not None else None
            assert returned_root == (None if blocked else 243)
            other = atom(after,b,unrelated)
            assert root(other[b]) == 243
            after_table = table_for(after,full_work=(name != "original" and source != f.T))
            assert after_table[a][b] == pair_work
            after_status, _ = gate(after_table)
            outcomes[str(source)] = {"work_AB": pair_work, "A_root_gain": totals[source],
                                     "B_root": root_b, "lost_B_commands": removed,
                                     "B_menu_size": len(menu_after), "probe": result,
                                     "probe_returned_B_root": returned_root,
                                     "carrier": after_status}
        runs[name] = {"same_full_carrier_as_initial":carrier == carrier0,
                      "preparatory_edits":len(prep), "q_holders":actual_holders,
                      "r_holders":actual_r, "work_AB":table[a][b], "changed_work_pairs":different,
                      "geometry":status, "B_menu_size":len(menu), "B_root":root_b,
                      "before_source_probe":"accepted", "before_source_probe_returned_B_root":243,
                      "source_arms":outcomes}

    # Every minimum-size isolation omitting one real holder preserves BOTH command outcomes.
    omitted_controls = []
    for omitted in others:
        common = [(i,q) for i in others if i != omitted]
        pair_results = []
        rows, _ = expected(common)
        for source in (p,q):
            after = atom(rows,a,source)
            assert after == expected(common+[(a,source)])[0]
            status, _ = probe(after)
            assert status == "accepted"
            pair_results.append(status)
        omitted_controls.append([omitted,pair_results])

    # A set of remaining external holders supplies a Boolean guard. Enumerate every
    # labeled subset and independently compare each cardinality class with the binomial law.
    histogram = Counter()
    all_bits = (1 << len(others)) - 1
    for removed_bits in range(all_bits+1):
        remaining_bits = all_bits ^ removed_bits
        histogram[(removed_bits.bit_count(), not bool(remaining_bits))] += 1
    assert histogram == Counter({(k,k == 21):comb(21,k) for k in range(22)})

    # Deliberately omit one compensating deletion, and independently alter its cut weight.
    omitted_r = [e for e in prep_orders["balanced"] if e != (others[0],r)]
    wrong_rows, _ = expected(omitted_r)
    wrong_table = table_for(wrong_rows)
    assert wrong_table != before and gate(wrong_table)[0] != "accepted"
    balanced_rows, _ = expected(prep_orders["balanced"])
    bad_weights = tuple(4 if v == r else weight for v,weight in enumerate(squares))
    assert f.work_for(initial,bad_weights) != f.work_for(balanced_rows,bad_weights)
    try:
        m["atom"].atomic(parents,initial,7,p)
    except ValueError as exc:
        assert str(exc) == "leaf"
    else:
        raise AssertionError("The wrong-cut control must fail")
    assert len(untouched_menu) == 1305 and unrelated != q and len(others) == 21
    assert runs["balanced"]["source_arms"][str(p)]["carrier"] != "accepted"
    assert runs["balanced"]["source_arms"][str(q)]["carrier"] != "accepted"
    return {"schema":"receiver-veto/1", "source_blob":PINS[FIXTURE], "A":a, "B":b,
            "p":p, "q":q, "r":r, "other_holders":others, "unrelated_receiver_unit":unrelated,
            "shared_nonroot_by_initial_support":dict(sorted(sizes.items())),
            "B_commands_initial_intervals":intervals(untouched_menu),
            "arms":runs, "total_pairs":len(pairs), "initial_minimum":f.edges(before)[0],
            "prepared_work_tables":prepared_tables,
            "omitted_holder_controls":omitted_controls,
            "subset_count":sum(histogram.values()), "subsets_distinguishing":histogram[(21,True)],
            "subsets_by_count":[[k,histogram[k,k == 21]] for k in range(22)],
            "first_bound":21, "balanced_bound_unit_untouched_B":42,
            "controls":["one_holder_present","unrelated_B_command","historical_two_unit",
                        "one_compensator_omitted","unequal_cut_weight","wrong_cut_leaf","false_success_record"]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    sources, output = (Path(p).resolve() for p in sys.argv[1:])
    resource.setrlimit(resource.RLIMIT_AS, (1_500_000_000,1_500_000_000))
    report = run(sources)
    raw=(json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({"sha256":sha256(raw).hexdigest(),"bytes":len(raw),
                      "balanced":report["arms"]["balanced"],"r":report["r"]},sort_keys=True))
