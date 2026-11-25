"""Run with python3 -B probe_return.py /path/to/WetLabEngine at e61d5b0e.

Use --full-prep to replay all 86 preliminary atoms and --full-orders to check
all 80 edges of the five-edit comparison through the archived emitter and verifier.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha1, sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations
import json
import lzma
import os
from pathlib import Path

BASE = Path("ResearchHistory/UQCF-GEM")
FIXTURE = BASE / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py"
P1 = BASE / "demos/v16.23-overlap-descent/engine.py"
V27 = BASE / "demos/v16.27-increment-attribution-closure/engine.py"
SOURCE, RECEIVER = 0, 12


def module(name, path, expected):
    data = path.read_bytes()
    assert sha1(f"blob {len(data)}".encode() + bytes([0]) + data).hexdigest() == expected
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def edited(rows, i, v):
    assert v and v in rows[i] and any(v in row for j, row in enumerate(rows) if j != i)
    return tuple(tuple(z for z in row if z != v) if j == i else row for j,row in enumerate(rows))


def archived_step(mods, p, rows, i, v):
    event = mods["atom"].atomic(p, rows, i, v)
    bit = mods["verify"].verify_atomic(event)
    after = tuple(map(tuple, event["after"]))
    assert after == edited(rows, i, v)
    return after, bit, event


def holdings(rows):
    who = defaultdict(set)
    for i, row in enumerate(rows):
        for v in row:
            who[v].add(i)
    return who


def prepare(f, mods, full_replay, p, initial):
    rows = initial
    seq = []
    for a,b in ((718,46),(1354,8)):
        who = holdings(rows)
        assert who[a] | who[b] == set(f.LABELS)
        common = sorted(who[a] & who[b])
        assert SOURCE not in common and RECEIVER not in common
        for i in common:
            for v in (a,b):
                assert v not in p and p[v] == 0
                if full_replay:
                    rows = archived_step(mods, p, rows, i, v)[0]
                else:
                    rows = edited(rows, i, v)
                seq.append((i,v))
    assert len(seq) == 86 and rows[0] == initial[0] and rows[12] == initial[12]
    return rows


def minimum_covers(p, rows):
    target = sum(1 << v for v in range(1, len(p)) if p[v] == 0)
    masks = [sum(1 << v for v in row if p[v] == 0) for row in rows]
    for size in range(1, len(rows)+1):
        found = []
        for group in combinations(range(len(rows)), size):
            covered = 0
            for j in group:
                covered |= masks[j]
            if covered == target:
                found.append(group)
        if found:
            return found
    raise AssertionError("uncovered root")


def totals(p, data):
    out = list(data)
    for v in reversed(range(1, len(data))):
        out[p[v]] += out[v]
    return out


def work(f, p, rows, fine):
    return f.work_for(rows, [t*t for t in totals(p,fine)])


def gate(f, mods, w):
    _, edges = f.edges(w)
    exact = tuple(tuple(map(F, row)) for row in w)
    payload = mods["projection"].Payload(5,F(1),f.LABELS,exact,edges,())
    try:
        return "accepted", mods["carriers"].build_carrier(payload)
    except ValueError as e:
        return str(e), None


def private_tips(rows, i):
    outside = set().union(*(set(row) for j,row in enumerate(rows) if i != j))
    return sorted(set(rows[i]) - outside)


def candidates(p, rows, covers):
    h = holdings(rows)
    receiver = set(rows[12])
    assert all(p[v] == 0 and v not in p for v in receiver if v)
    return {v: all(not ((set(c)-{12}) & h[v]) for c in covers)
            for v in receiver - {0} if len(h[v]) > 1}


def work_returns(p, rows, fine, arm):
    """Classify all nonempty one-chart returns using two exact row sums."""
    who = holdings(rows)
    others = set(range(len(rows))) - {12}
    monitors = {0,7,11,13,17}
    eligible = [v for v in rows[12] if v and len(who[v]) >= 2]
    assert all(v not in p for v in eligible)
    score = {v:(2*len(monitors & who[v])-5)*fine[v]**2 for v in eligible}
    nonpositive = {v for v in eligible if score[v] <= 0}
    if arm == "A":
        assert not nonpositive
        return []
    assert nonpositive == {718} and score[718] == -3
    others_possible = [v for v in eligible if v != 718 and score[v] <= 3]
    assert all(fine[v] == 1 and score[v] >= 1 and len(who[v]) >= 23 for v in others_possible)
    # The negative sum across all 24 partners is -22. Each possible positive
    # cut adds at least 20 to that same sum, so there must be exactly one.
    assert (2*len(who[718] & others)-24)*fine[718]**2 == -22
    pairs = [(718,v) for v in others_possible if who[v] & others == others - who[718]]
    assert sorted(pairs) == [(718,1301),(718,1302)]
    return sorted(pairs)


def single_classes(p, rows, fine):
    who = holdings(rows)
    s = set(rows[0])
    active_parents = {p[v] for v in s if v}
    group = Counter()
    for v in s - active_parents - {0}:
        if len(who[v]) > 1:
            assert p[v] == 0 and v not in p and fine[v] > 0
            group[fine[v],tuple(sorted(who[v]))] += 1
    return dict(legal=sum(group.values()), work_classes=len(group),
                work_matched_pairs=sum(k*(k-1)//2 for k in group.values()))


def calibration(fine):
    changed = list(fine)
    names = (163,164,47,48)
    assert tuple(changed[v] for v in names) == (5,3,1,1)
    for v,val in zip(names,(45,61,7,17)):
        changed[v] = F(val,13)
    assert changed[0] == fine[0] and sum(changed) == sum(fine)
    assert sum(changed[v]**2 for v in names[:2]) == 34
    assert sum(changed[v]**2 for v in names[2:]) == 2
    return tuple(changed)


def history_check(f, mods, p1, p, pre, fine, thorough, witness_path):
    v27 = module("v27", V27, "48f132d141167d9cd85ff79ec41720b5dca4f8bb")
    actions = ((0,718),(0,1355),(0,1304),(0,1354),(12,163))
    all_sites = tuple(range(len(p)))
    states, heights = {}, {}
    for mask in range(1 << len(actions)):
        row = pre
        for j,(i,v) in enumerate(actions):
            if mask & (1 << j):
                row = edited(row,i,v)
        states[mask] = row
        covers = minimum_covers(p,row)
        heights[mask] = len(covers[0])
        assert heights[mask] == 3 + int(mask & 24 == 24)
    key_orders = ((0,1,4,2,3),(2,3,4,0,1))
    need = set()
    for order in key_orders:
        mask=0
        for j in order:
            need.add((mask,j))
            mask |= 1 << j
    edges = {}
    for mask, state in states.items():
        for j,(i,v) in enumerate(actions):
            if mask & (1 << j):
                continue
            dest = mask | (1 << j)
            assert edited(state,i,v) == states[dest]
            delta = heights[dest] - heights[mask]
            if thorough or (mask,j) in need:
                after, bit, event = archived_step(mods,p,state,i,v)
                assert after == states[dest] and bit == (delta, bool(delta))
                edges[mask,j] = event
            else:
                # Sufficient columns for the archived attribution function.
                edges[mask,j] = dict(index=i,leaf=v,delta_h=delta)
    attributions = Counter()
    selected = {}
    for order in permutations(range(len(actions))):
        mask, path = 0,[]
        for j in order:
            path.append(edges[mask,j])
            mask |= 1 << j
        mapping = v27.event_map(path)
        assert set(mapping) == set(actions) and sum(mapping.values()) == 1
        last = 3 if order.index(3) > order.index(4) else 4
        assert mapping[actions[last]] == 1
        attributions[actions[last]] += 1
        if order in key_orders:
            selected[order] = path
    assert len(edges) == 80 and attributions == {(0,1354):60,(12,163):60}
    first, second = [selected[seq] for seq in key_orders]
    witness = v27.witness(p,pre,states[31],[first,second])
    assert witness["changed_events"] == [[0,1354],[12,163]]
    assert witness["path_a"][-1]["after"] == witness["path_b"][-1]["after"]
    raw = (json.dumps(witness, sort_keys=True, separators=(",",":")) + "\n").encode()
    if witness_path is not None:
        witness_path.write_bytes(lzma.compress(raw, preset=6))
    for data in (fine,calibration(fine)):
        all_w = []
        for a,b in zip(first,second):
            a_rows,b_rows = [tuple(map(tuple,row["after"])) for row in (a,b)]
            assert a_rows[12] == b_rows[12]
            assert all(a_rows[i] == b_rows[i] for i in range(1,25))
            assert p1.push(p,all_sites,a_rows[12],data) == p1.push(p,all_sites,b_rows[12],data)
            wa, wb = (work(f,p,row,data) for row in (a_rows,b_rows))
            assert wa[12] == wb[12]
            all_w.append(sum(wa[i][j] != wb[i][j] for i,j in combinations(f.LABELS,2)))
        assert all_w == [22,0,0,22,0]
    return dict(states=len(states), edges=len(edges), complete_orders=sum(attributions.values()),
                receiver_increment_orders=attributions[(12,163)], source_increment_orders=attributions[(0,1354)],
                assigned_to_receiver=[v27.event_map(seq)[(12,163)] for seq in (first,second)],
                archived_changed_events=witness["changed_events"],
                raw_witness_sha256=sha256(raw).hexdigest(), raw_witness_bytes=len(raw),
                matched_history_work_discrepancies=all_w,
                matched_history_receiver_work_discrepancies=[0]*5,final_height=heights[31])


def run(root, full_replay, full_orders, witness_path):
    os.chdir(root)
    f = module("fixture", FIXTURE, "3324c0b46e09120ae526338444a19070b692d049")
    fmods = f.modules()  # Also validates all 12 historical Git blobs.
    p1 = module("p1", P1, "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    features,target = f.fixture()
    p,fine,original = map(tuple,zip(*features))
    full = tuple(range(len(p)))
    initial = f.initial_state(features)
    pre = prepare(f, fmods, full_replay, p, initial)
    who = holdings(pre)
    all_charts = set(f.LABELS)
    expected = {718:{0,12},1355:all_charts-{12},1354:{0,1},1304:all_charts-{1},8:{12}}
    assert all(who[v] == owners for v,owners in expected.items())
    assert who[163] == who[164] == all_charts-{1,13}
    assert who[47] == who[48] == all_charts-{0,12}

    arms = {"A":(718,1355), "B":(1304,1354)}
    states, source_flags = {}, {}
    for key, moves in arms.items():
        state = pre
        history, flags = [pre], []
        for v in moves:
            state, bit, _ = archived_step(fmods,p,state,0,v)
            assert bit == (0,False)
            history.append(state)
            flags.append(bit)
        states[key], source_flags[key] = history, flags
    end = {k:s[-1] for k,s in states.items()}
    covers = {k:minimum_covers(p,s) for k,s in {"before":pre,**end}.items()}
    assert covers["before"] == covers["A"] == [(0,8,12),(0,12,13),(1,12,13)]
    assert covers["B"] == [(1,12,13)]
    experiments = {}
    for k, field in (("nominal",fine),("calibrated",calibration(fine))):
        w_init, w_pre = (work(f,p,s,field) for s in (initial,pre))
        assert w_init == w_pre == target
        w = {arm:[work(f,p,s,field) for s in states[arm]] for arm in arms}
        for t in range(3):
            assert w["A"][t][12] == w["B"][t][12]
        assert w["A"][-1] == w["B"][-1] == target
        assert sum(w["A"][1][i][j] != w["B"][1][i][j] for i,j in combinations(f.LABELS,2)) == 22
        assert all(s[12] == initial[12] for v in states.values() for s in v)
        prior = p1.push(p,full,pre[12],field)
        root = prior[pre[12].index(0)]
        source_root = p1.push(p,full,pre[0],field)[0]
        assert all(p1.push(p,full,s[0],field)[0] == source_root+n
                   for seq in states.values() for n,s in enumerate(seq))
        refs={}
        for key,row in (("before",pre), *end.items()):
            local = p1.push(p,full,row[12],field)
            assert local == prior
            tags = sorted((x,v) for v,x in zip(row[12],local) if v and x.denominator != 1)
            assert [v for x,v in tags] == ([163,164] if k=="calibrated" else [])
            refs[key] = [str(x) for x,v in tags]
        experiments[k] = dict(receiver_root=str(root), receiver_fractional_tip_grades=refs["before"],
                              exact_returns={arm:work_returns(p,s,field,arm) for arm,s in end.items()},
                              receiver_incident_01_to_12=[str(t[0][12]) for t in w["A"]],
                              postprobe={})
    known = {key:candidates(p,s,covers[key]) for key,s in {"before":pre,**end}.items()}
    common = sorted(known["A"].keys() & known["B"].keys())
    separators = [v for v in common if known["A"][v] != known["B"][v]]
    assert separators == [163,164]
    assert set(known["before"]) == set(known["B"])
    assert set(known["B"])-set(known["A"]) == {718}
    assert private_tips(pre,12) == private_tips(end["B"],12) == [5,8]
    assert private_tips(end["A"],12) == [5,8,718]

    receipts = {}
    for v in (163,164,1301):
        actual = {}
        checks = {}
        for arm,state in {"before":pre, **end}.items():
            after, bit, event = archived_step(fmods,p,state,12,v)
            assert bit == (int(known[arm][v]), known[arm][v])
            assert event["h_before"] == event["tau_before"] == 3
            assert event["h_after"] == event["tau_after"] == 3+bit[0]
            actual[arm] = after
            checks[arm] = list(bit)
            if v == 163:
                false_event = dict(event, trigger=not event["trigger"])
                try:
                    fmods["verify"].verify_atomic(false_event)
                except ValueError as e:
                    assert str(e) == "false certificate"
                else:
                    raise AssertionError("counterfeit certificate accepted")
        receipts[v] = checks
        assert actual["A"][12] == actual["B"][12]
        for k,field in (("nominal",fine),("calibrated",calibration(fine))):
            wa,wb = (work(f,p,actual[arm],field) for arm in arms)
            assert wa == wb
            ra,rb = (p1.push(p,full,actual[arm][12],field) for arm in arms)
            assert ra == rb
            experiments[k]["postprobe"][v] = dict(receiver_root=str(ra[0]), work_gate=gate(f,fmods,wa)[0])
    accepted, carrier = gate(f,fmods,target)
    assert accepted == "accepted"
    # Replay all actual short work-restoring receiver writes, and the
    # last-copy rejection of that same proposed cut in A.
    for x,y in work_returns(p,end["B"],fine,"B"):
        state=end["B"]
        for v in (x,y):
            state, _, _ = archived_step(fmods,p,state,12,v)
        assert work(f,p,state,fine) == target
        assert gate(f,fmods,work(f,p,state,fine)) == (accepted,carrier)
        assert p1.push(p,full,state[12],fine)[0] == 244
    try:
        fmods["atom"].atomic(p,end["A"],12,718)
    except ValueError as e:
        assert str(e) == "same union"
    else:
        raise AssertionError("last-copy cut accepted")
    return dict(prep_edits=86, preparation_sha256=sha256(json.dumps(pre,separators=(",",":")).encode()).hexdigest(),
                source_cuts=arms,source_receipts=source_flags,common_receiver_commands=len(common),
                distinguished_commands=separators,minimum_root_covers=covers, verified_receipts=receipts,
                raw_single_cut_classes=single_classes(p,pre,fine),experiments=experiments,
                order_test=history_check(f,fmods,p1,p,pre,fine,full_orders,witness_path))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("checkout", type=Path, help="historical WetLabEngine checkout")
    cli.add_argument("--full-prep", action="store_true")
    cli.add_argument("--full-orders", action="store_true")
    cli.add_argument("--witness", type=Path, help="write both complete native paths as XZ-compressed JSON")
    args = cli.parse_args()
    dest = args.witness.resolve() if args.witness is not None else None
    print(json.dumps(run(args.checkout.resolve(),args.full_prep,args.full_orders,dest),sort_keys=True,indent=2))
