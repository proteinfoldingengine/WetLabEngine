"""Replay source choices and enumerate every globally shortest return of exact work."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import sys

from check_receiver_command import FIXTURE, PINS, hash_blob
from verify_return_pairs import measured_pairs


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def holder_pairs(parents, rows, squares):
    n = len(rows)
    full = (1 << n) - 1
    cell = [0] * len(parents)
    for i, row in enumerate(rows):
        for v in row:
            cell[v] |= 1 << i
    recorded = set()
    for i, row in enumerate(rows):
        children = defaultdict(set)
        for v in row:
            if v:
                children[parents[v]].add(v)
        outside = full ^ (1 << i)
        seen = defaultdict(list)
        for v in row:
            holders = cell[v] & outside
            if not v or not holders:
                continue
            for u in seen[squares[v], outside ^ holders]:
                removed = {u, v}
                if not (children[v] - removed or children[u] - removed):
                    recorded.add((i, min(u, v), max(u, v)))
            seen[squares[v], holders].append(v)
    return sorted(recorded)


def run(sources):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path.insert(0, str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    native = f.modules()
    p29 = f.D / "v16.29-local-profile-closure/producer.py"
    assert hash_blob(p29.read_bytes()) == "fc4a77fc4f01fce33fdb562423eca274cfb0c648"
    spec = importlib.util.spec_from_file_location("profile29", p29)
    archive = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(archive)
    features, original_work = f.fixture()
    parents, grades, support = map(tuple, zip(*features))
    totals = list(grades)
    for v in range(len(parents) - 1, 0, -1):
        totals[parents[v]] += totals[v]
    squares = [s*s for s in totals]
    a, b, labels = f.A, f.B, f.ALL
    initial = f.initial_state(features)

    def work(rows):
        return f.work_for(rows, squares)

    def carrier(table):
        exact = tuple(tuple(map(Fraction, row)) for row in table)
        p = native["projection"].Payload(f.SIDE, Fraction(1), f.LABELS,
                                         exact, f.edges(table)[1], ())
        return native["carriers"].build_carrier(p)

    def cut(rows, i, v):
        return archive.cut(parents, rows, (i, v))

    def checked(rows, i, v):
        event = native["atom"].atomic(parents, rows, i, v)
        native["verify"].verify_atomic(event)
        after = tuple(map(tuple, event["after"]))
        assert after == cut(rows, i, v)
        return after

    def pairs(rows):
        first = holder_pairs(parents, rows, squares)
        second = measured_pairs(parents, rows, squares, work(rows))
        assert first == second
        return first

    keys = [()]
    for v in range(1, len(parents)):
        keys.append(keys[parents[v]] + (v,))
    lin = native["lineage"]
    fine = lin.Carrier("geometry-selected-record", tuple(keys))

    def local(rows):
        coarse = lin.Carrier(fine.genesis, tuple(keys[v] for v in rows[b]))
        return lin.Pruning(fine, coarse).aggregate(grades)

    def units_missing(missing):
        return [v for v in range(1, len(parents)) if parents[v] == 0 and
                squares[v] == 1 and labels - support[v] == missing]

    mates_a, mates_b = units_missing({b}), units_missing({a})
    exchanges = units_missing({a, b})
    q0 = 718
    eligible = [v for v in range(6, len(parents)) if squares[v] == 1 and
                {a, b} <= support[v] and len(support[v]) == len(labels) - 2]
    preferred = sorted((v for v in eligible if v != q0),
                       key=lambda v: (support[v] != support[q0], v))
    assert mates_a and mates_b and len(exchanges) >= len(mates_a)+1
    sparse = [q0] + preferred[:len(mates_a)]
    assert sparse[:2] == [718, 719]
    record_leaves = sparse[:2]
    before_geometry = carrier(original_work)
    assert work(initial) == original_work
    rows = initial
    preparation = []

    def switch(start, v, u):
        holders = [{i for i,y in enumerate(start) if site in y} for site in (v,u)]
        assert holders[0] | holders[1] == labels and squares[v] == squares[u]
        schedule = [(i, leaf) for i in sorted(holders[0] & holders[1]) for leaf in (v, u)]
        out = start
        for i, leaf in schedule:
            out = cut(out,i,leaf)
        assert work(out) == work(start)
        return out, schedule

    for v, u in zip(sparse, exchanges):
        rows, steps = switch(rows, v, u)
        assert len(steps) == 42 and rows[a] == initial[a] and rows[b] == initial[b]
        preparation.extend(steps)
    for v, u in zip(sparse[2:], mates_a):
        rows = cut(cut(rows,a,v),a,u)
        preparation.extend([(a,v),(a,u)])
        assert work(rows) == original_work
    removed_competitors = []
    while True:
        possible = holder_pairs(parents, rows, squares)
        foreign = [x for x in possible if x[0] not in (a,b)]
        if not foreign:
            break
        i, v, u = foreign[0]
        assert {u,v}.isdisjoint(record_leaves)
        rows = cut(cut(rows,i,v),i,u)
        preparation.extend([(i,v),(i,u)])
        removed_competitors.append([i,v,u])
        assert work(rows) == original_work
    common = rows
    assert common[b] == initial[b] and carrier(work(common)) == before_geometry
    source_mate, = [v for v in mates_a if v in common[a]]
    initial_pairs = pairs(common)
    expected_initial = sorted((i,min(x,y),max(x,y)) for i,ys in
                              ((a,[source_mate]),(b,mates_b)) for x in record_leaves for y in ys)
    assert initial_pairs == expected_initial
    original_B_grade = local(common)
    assert original_B_grade[0] == 242

    # A fresh cut exchange provides the same longer exact return in both arms.
    blind_r = next(v for v in exchanges if v not in exchanges[:len(sparse)])
    blind_q = next(v for v in eligible if v not in sparse)
    arms, source_work, final_rows = {}, {}, {}
    for x in record_leaves:
        y, = set(record_leaves) - {x}
        one = checked(common,a,x)
        after = checked(one,a,source_mate)
        assert after == cut(cut(common,a,source_mate),a,x)
        w1 = work(one)
        assert w1 != original_work and work(after) == original_work
        assert carrier(work(after)) == before_geometry and after[b] == common[b]
        # An exact one-step restoration can only undo the changed origin row.
        restorative = [pair for pair in initial_pairs if pair[0] == a and x in pair[1:]]
        assert restorative == [(a,min(x,source_mate),max(x,source_mate))]
        found = pairs(after)
        expected = sorted((b,min(y,t),max(y,t)) for t in mates_b)
        assert found == expected and len(found) == 2
        # Missing, repeated, substituted, wrong-editor and wrong-leaf candidate controls.
        impostors = [found[1:], found+[found[0]], [(a,v,u) for _,v,u in found],
                     sorted((b,min(x,t),max(x,t)) for t in mates_b),
                     [(b,found[0][1],f.B_PRIVATE),found[1]]]
        assert all(sorted(alternate) != expected for alternate in impostors)
        neighbor_set = f.grid()[b]
        dense_minima = []
        special = {}
        for v in after[b]:
            if v == 0:
                continue
            h = {i for i,row in enumerate(after) if i != b and v in row}
            if not h:
                continue
            nscore = squares[v] * (2 * len(h & neighbor_set) - len(neighbor_set))
            whole = squares[v] * (2 * len(h) - (len(labels)-1))
            if v in (y, f.ULEAF):
                special[v] = [nscore, whole]
            else:
                assert len(h) >= 22
                dense_minima.append([v,nscore,whole])
        assert special == {y:[-4,-22], f.ULEAF:[16,-64]}
        assert min(k[1] for k in dense_minima) >= 0 and min(k[2] for k in dense_minima) >= 20
        witnesses = []
        for _,v,u in found:
            for first, second in ((v,u),(u,v)):
                mid = checked(after,b,first)
                end = checked(mid,b,second)
                wm, we = work(mid), work(end)
                assert wm != original_work and we == original_work
                assert carrier(we) == before_geometry and x in end[b] and y not in end[b]
                assert local(end)[0] == 244
                final_rows[x,first==y,u] = end[b]
                witnesses.append({"commands":[[b,first],[b,second]],"membership":digest(end[b]),
                                  "root":244,"q_present":[v for v in record_leaves if v in end[b]],
                                  "work_path":[digest(t) for t in (original_work,w1,original_work,wm,we)]})
        try:
            checked(after,b,x)
        except ValueError as exc:
            assert str(exc) == "same union"
        else:
            raise AssertionError("The last holder removed its protected leaf")
        # Full carrier admission alone allows a two-edit historical alternative.
        weak1 = checked(after,a,f.T)
        weak2 = checked(weak1,b,f.ULEAF)
        weak_work = work(weak2)
        wk = carrier(weak_work)
        assert weak_work != original_work and weak2[b] == tuple(v for v in common[b] if v != f.ULEAF)
        assert local(weak2)[0] == 244 and set(record_leaves) <= set(weak2[b])
        # A genuine 42-step first return leaves both A and B idle throughout.
        target, steps = switch(after,blind_q,blind_r)
        assert len(steps) == 42 and {a,b}.isdisjoint(i for i,v in steps)
        assert target[a] == after[a] and target[b] == after[b]
        current = after
        prefix_hashes = []
        for i,v in steps:
            current = cut(current,i,v)
            prefix_hashes.append(digest(work(current)))
        assert current == target and digest(original_work) not in prefix_hashes[:-1]
        assert prefix_hashes[-1] == digest(original_work) and carrier(work(target)) == before_geometry
        source_work[x] = w1
        arms[str(x)] = {"source":[[a,x],[a,source_mate]],"minimal_returns":found,
                        "first_restorations":restorative,"witnesses":witnesses,
                        "row_bounds":{"dense_min_neighbor":min(k[1] for k in dense_minima),
                                      "dense_min_total":min(k[2] for k in dense_minima),
                                      "special":special},
                        "weaker_carrier":{"accepted":wk is not None,"work":digest(weak_work),
                                          "B_row":digest(weak2[b]),"root":244},
                        "long_return":{"cuts":steps,"prefix_work":prefix_hashes,
                                       "B_row":digest(target[b])}}
    x,y = record_leaves
    assert source_work[x] == source_work[y]
    def transpose(row):
        return tuple(sorted(y if v==x else x if v==y else v for v in row))
    for t in mates_b:
        for distinguished_first in (True,False):
            assert transpose(final_rows[x,distinguished_first,t]) == final_rows[y,distinguished_first,t]
    for w,z in zip(arms[str(x)]["witnesses"],arms[str(y)]["witnesses"],strict=True):
        assert w["work_path"] == z["work_path"] and w["membership"] != z["membership"]
    assert arms[str(x)]["long_return"] == arms[str(y)]["long_return"]
    assert arms[str(x)]["weaker_carrier"] == arms[str(y)]["weaker_carrier"]
    # Historical same-source diamond before a B edit.
    old,_ = switch(initial,718,46)
    p,q = 662,718
    joined = checked(checked(old,a,p),a,q)
    alternate = checked(checked(old,a,q),a,p)
    assert joined == alternate and joined[b] == old[b]
    return {"version":"geometry-selected-record/1","historical_fixture":PINS[FIXTURE],
            "original_work":digest(original_work),"unit_mates_at_A":mates_a,"unit_mates_at_B":mates_b,
            "exchange_leaves":list(zip(sparse,exchanges[:len(sparse)])),"source_mate":source_mate,
            "removed_competitors":removed_competitors,"preparation":preparation,
            "preparation_edits":len(preparation),"common_rows_digest":digest(common),
            "common_two_step_returns":initial_pairs,"B_root_before":242,
            "historical_diamond":digest(joined),"arms":arms,
            "identical_matched_work_paths":True,"indexed_address_required":True,
            "supplied":["preparation","source choice","occurrence of a shortest exact return"]}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Enable assertions")
    source, output = map(lambda p:Path(p).resolve(),sys.argv[1:])
    data = run(source)
    raw = (json.dumps(data,sort_keys=True,indent=2)+"\n").encode()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    print(json.dumps({"sha256":sha256(raw).hexdigest(),"bytes":len(raw),
                      "preparation_edits":data["preparation_edits"],
                      "common":data["common_two_step_returns"],
                      "source_arms":{x:z["minimal_returns"] for x,z in data["arms"].items()}}))
