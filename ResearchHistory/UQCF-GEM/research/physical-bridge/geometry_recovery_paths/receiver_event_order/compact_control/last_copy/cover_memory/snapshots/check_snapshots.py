"""Check current geometry against every allowed history of the five-chart comparison."""
import argparse
from collections import Counter, defaultdict
from functools import cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAST = HERE.parents[1]
spec = spec_from_file_location("last_copy", LAST / "check.py")
prior = module_from_spec(spec)
spec.loader.exec_module(prior)
prior.pinned(LAST / "check.py", "c7b0586362e74c22612a9926f1d7135cf074dfb0")
CHARTS = "BAEFX"
PAIRS = tuple(combinations(range(5), 2))
NAMES = tuple(CHARTS[i] + CHARTS[j] for i, j in PAIRS)


def phase(s):
    a, b = 6 in s[1], 6 in s[0]
    assert a or b
    return "P" if a and b else "A" if b else "B"


@cache
def cover_size(s):
    # Direct incidence calculation, independent of the historical emitter.
    for n in range(1, 6):
        if any(set().union(*group) == set(range(8)) for group in combinations(s, n)):
            return n
    raise AssertionError("invalid cover")


def possible_records(start, states, edges):
    records = {s: set() for s in states}
    records[start].add("P")
    for (s, i, v), t in sorted(edges.items(), key=lambda e: -sum(map(len, e[0][0]))):
        assert records[s]
        if v == 6:
            assert records[s] == {"P"}
            records[t].add(CHARTS[i] + str(cover_size(t) - cover_size(s)))
        else:
            records[t].update(records[s])
    return records


def bins(observations, mask, own_root):
    out = defaultdict(set)
    for root, w, status in observations:
        key = ((root,) if own_root else ()) + tuple(w[i] for i in mask)
        out[key].add(status)
    return out


def classify_subsets(observations, own_root):
    good = []
    for size in range(11):
        for mask in combinations(range(10), size):
            if all(len(group) == 1 for group in bins(observations, mask, own_root).values()):
                good.append(mask)
    minimum = min(map(len, good))
    return {"minimum": minimum,
            "minimal_at_that_size": [[NAMES[i] for i in mask] for mask in good if len(mask) == minimum],
            "sufficient_subsets_by_size": dict(sorted(Counter(map(len, good)).items()))}


def run(checkout):
    cfg = json.loads(prior.pinned(LAST.parent / "FIXTURE.json",
                                  "806d2bc487e358f498cafa806226d1f658e98d26"))
    assert cfg["charts"] == CHARTS and cfg["fine_grade"] == [1] * 8
    uq = checkout / "ResearchHistory/UQCF-GEM"
    v26 = uq / "demos/v16.26-consistency-increment-law"
    atom = prior.module(v26 / "engine.py", "atom", cfg["engine_blob"])
    ver = prior.module(v26 / "verify.py", "ver", cfg["verify_blob"])
    p1 = prior.module(uq / "demos/v16.23-overlap-descent/engine.py",
                      "p1", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    geometry = prior.module(uq / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py",
                            "work", "3324c0b46e09120ae526338444a19070b692d049")
    p, all_sites = (-1,) + (0,) * 7, tuple(range(8))
    initial = prior.rows(CHARTS, cfg["tip_holders"])

    def advance(s, i, v):
        e = atom.atomic(p, s, i, v)
        ver.verify_atomic(e)
        return prior.as_rows(e["after"]), e

    def follow(s, seq):
        steps = []
        for owner, v in seq:
            s, e = advance(s, CHARTS.index(owner), v)
            steps.append(e)
        return s, steps

    @cache
    def reading(s):
        root = int(p1.push(p, all_sites, s[0], cfg["fine_grade"])[0])
        assert root == 9 - len(s[0])
        work = geometry.work_for(s, (1,) * 8)
        w = tuple(work[i][j] for i, j in PAIRS)
        assert w == tuple(sum((v in s[i]) != (v in s[j]) for v in range(1,8)) for i,j in PAIRS)
        return root, w

    observations, arm_history, evidence = [], {}, {}
    by_state, by_w, by_local = defaultdict(set), defaultdict(set), defaultdict(set)
    schedule_controls, response = {}, {}
    family_edges = {}
    for indexes in cfg["receipt_paths"]:
        source, _ = follow(initial, [cfg["edits"][k] for k in indexes[:2]])
        start, probe = advance(source, 0, 5)
        bit = probe["delta_h"]
        states, native = prior.native_graph(atom, ver, p, start)
        ref_states, edges = prior.reachable_by_columns(CHARTS, start)
        family_edges[bit] = edges
        prior.match_edges(states, native, ref_states, edges)
        records = possible_records(start, states, edges)
        arm_history[bit] = (start, records)
        assert (len(states),len(edges)) == (189,621)
        for key, dest in edges.items():
            s = key[0]
            assert native[key]["h_before"] == cover_size(s) and native[key]["h_after"] == cover_size(dest)
        keyed = []
        for s in sorted(states):
            root, w = reading(s)
            n_b = 8 - root
            n_e, n_x = w[1] - n_b, w[3] - n_b
            assert (n_e, n_x) == (len(s[2])-1, len(s[4])-1)
            if n_e == 0:
                assert bit == 0
            if n_x == 1:
                assert bit == 1
            if 3 not in s[2]:
                assert bit == 0
            if 1 not in s[4]:
                assert bit == 1
            if (root, w[0], w[1]) == (7,3,1):
                assert bit == 0 and records[s] == {"A1"}
            assert {label[0] for label in records[s]} == {phase(s)}
            observations.append((root, w, phase(s)))
            by_state[s].update(records[s])
            by_w[w].update(records[s])
            by_local[(root,w[:4])].update((bit,label) for label in records[s])
            keyed.append({"rows":s,"B_root":root,"work":w,"withdrawal_records":sorted(records[s])})
        # Progress for fixed editors B,E,X in any order, with A,F stationary.
        pending, seen, terminal = [start], set(), []
        while pending:
            s = pending.pop()
            if s in seen:
                continue
            seen.add(s)
            children = [t for (before, i, _),t in edges.items() if before == s and CHARTS[i] in "BEX"]
            if children:
                pending.extend(children)
            else:
                terminal.append(s)
        for s in terminal:
            assert (len(s[2])-1,len(s[4])-1) == ((0,2) if bit==0 else (1,1))
            root, w = reading(s)
            assert (w[1] - (8-root), w[3] - (8-root)) == ((0,2) if bit==0 else (1,1))
        assert len(terminal) == 1
        # Omitting the old B-at-5 probe preserves those exclusive exterior records.
        no_probe, _ = follow(source, [("E",2),("E",3)] if bit==0 else [("X",1),("X",4)])
        assert 5 in no_probe[0] and 6 in no_probe[0]
        r0, w0 = reading(no_probe)
        assert (w0[1]-(8-r0)==0 if bit==0 else w0[3]-(8-r0)==1)
        schedule_controls[str(bit)] = dict(states=len(seen), terminals=len(terminal),
                                          exterior_counts=[len(terminal[0][i])-1 for i in (2,4)])
        quiet_terminal = [s for s in states if s[1]==start[1] and
                          not any(before==s and i!=1 for before,i,_ in edges)]
        assert quiet_terminal and all((3 not in s[2],1 not in s[4])==(bit==0,bit==1)
                                      for s in quiet_terminal)
        schedule_controls[str(bit)]["source_quiescent_terminals"]=len(quiet_terminal)

        # Fixed addressed participant F is identified by the holder of 5 that
        # remains after B releases it. F has not acted in either source history.
        assert [CHARTS[i] for i,row in enumerate(source) if 5 in row] == ["B","F"]
        assert [CHARTS[i] for i,row in enumerate(start) if 5 in row] == ["F"]
        prep = (("E",2),("X",4))
        ready, prep_events = follow(start,prep)
        assert ready == follow(start,reversed(prep))[0]
        assert ready[3]==start[3]==(0,2,4,5)
        f_menu = lambda s, es: {v for before,i,v in es if before==s and i==3}
        assert f_menu(start,edges)=={2,4}
        rs, ne = prior.native_graph(atom,ver,p,ready)
        rs0, re = prior.reachable_by_columns(CHARTS,ready)
        prior.match_edges(rs,ne,rs0,re)
        removed = 4 if bit==0 else 2
        out_f = (0,2,5) if bit==0 else (0,4,5)
        assert f_menu(ready,re)=={removed}
        terms=rs-{before for before,_,_ in re}
        for s in rs:
            assert s[3] in (ready[3],out_f)
            grades=tuple(p1.push(p,all_sites,s[3],cfg["fine_grade"]))
            if s[3]==out_f:
                assert grades==(6,1,1) and not f_menu(s,re)
            else:
                assert grades==(5,1,1,1) and f_menu(s,re) <= {removed}
        assert all(t[3]==out_f for (s,i,v),t in re.items() if i==3 or s[3]==out_f)
        term_counts=Counter("record" if s[3]==out_f else "blank" for s in terms)
        assert (len(rs), len(re),term_counts)==(27,54,{"record":4,"blank":4})
        # A's remaining common F tip stays shared if A makes no further cut.
        qterm=[s for s in rs if s[1]==ready[1] and
               not any(before==s and i!=1 for before,i,_ in re)]
        assert qterm and all(s[3]==out_f for s in qterm)
        silent, sil = follow(ready, [("A",v) for v in ( (3,4) if bit==0 else (1,2) )])
        assert silent[3]==ready[3] and not f_menu(silent,re)
        # Without the B-at-5 withdrawal an identical F-at-5 write is available.
        no_B, c0 = follow(source,prep)
        decoy, c1 = advance(no_B,3,5)
        assert decoy[3]==(0,2,4)
        # This is the same F root as either informative first edit, and both
        # sources yield the same addressed F output after this common decoy.
        assert tuple(p1.push(p,all_sites,decoy[3],cfg["fine_grade"]))==(6,1,1)
        response[str(bit)] = dict(first_F_deletion=removed, retained_F=out_f,
                 source_quiescent_terminals=len(qterm),terminal_counts=dict(term_counts),
                 ready_F_incident=[reading(ready)[1][j] for j,pair in enumerate(PAIRS) if 3 in pair],
                 probe_F_incident=[reading(start)[1][j] for j,pair in enumerate(PAIRS) if 3 in pair])
        evidence[str(bit)] = dict(probe=probe, states=keyed, edges=[native[k] for k in sorted(native)],
                       preparation=prep_events, no_probe_decoy=c0+[c1],silent=silent,
                       silent_steps=sil)
    assert set(arm_history) == {0,1}
    assert evidence["0"]["silent"] == evidence["1"]["silent"]
    # Without the common preparation promise, even F's addressed state plus
    # the whole work table can mimic the opposite preparation's written state.
    out_of_protocol = ((0,), (0,3,6), (0,2), (0,4,5), (0,1,7))
    in_protocol = ((0,), (0,2,6), (0,3), (0,4,5), (0,1,7))
    assert out_of_protocol in arm_history[0][1] and in_protocol in arm_history[1][1]
    assert in_protocol in prior.reachable_by_columns(CHARTS,follow(arm_history[1][0],prep)[0])[0]
    assert out_of_protocol[3]==in_protocol[3] and reading(out_of_protocol)==reading(in_protocol)
    assert 2 in out_of_protocol[2]
    evidence["protocol_alias"] = dict(source_0=out_of_protocol, source_1=in_protocol,
                                      work=reading(in_protocol)[1])
    for k in ("ready_F_incident","probe_F_incident"):
        assert response["0"][k]==response["1"][k]
    # Pair every common successful non-F preparation. Actor and exact leaf
    # agree between arms, with no scheduling restriction at the separate tip 6.
    q=[(arm_history[0][0],arm_history[1][0])]
    seen_pairs=set()
    common_edges=separating=0
    while q:
        pair=q.pop()
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        cs=[{(i,v):t for (s,i,v),t in family_edges[bit].items() if s==pair[bit]}
            for bit in (0,1)]
        menus=[{v for i,v in c if i==3} for c in cs]
        prepared = not (2 in pair[0][2] or 4 in pair[0][4])
        assert all(menus) and (not (menus[0]&menus[1]))==prepared
        separating += int(prepared)
        for i,v in cs[0].keys() & cs[1].keys():
            if i!=3:
                common_edges+=1
                q.append((cs[0][i,v],cs[1][i,v]))
    assert (len(seen_pairs),common_edges,separating)==(12,20,3)

    # A can withdraw FIRST, with no observation or exterior-preparation phase.
    zero_start = arm_history[0][0]
    seq = (("A",6),("E",2),("E",3))
    for order in permutations(seq):
        s, hist = follow(zero_start, order)
        assert next(e["delta_h"] for e in hist if e["leaf"]==6) == 1
        root, w = reading(s)
        assert (root,w[0],w[1]) == (7,3,1)
    terminal, _ = follow(s, [("F",4),("X",4)])
    assert not any(len({i for i in range(5) if v in terminal[i]})>1 for v in range(1,8))
    assert reading(terminal)[1][:4] == (3,1,3,3)
    # Same current state and same source arm, but two different old increments.
    one_start = arm_history[1][0]
    a, first = follow(one_start,(("A",6),("X",1)))
    b, second = follow(one_start,(("X",1),("A",6)))
    assert a == b and (first[0]["delta_h"],second[1]["delta_h"]) == (0,1)
    # Cancellation in B's entire local geometric row, within one arm.
    shadow, _ = follow(zero_start,(("A",6),("A",4)))
    r, w = reading(zero_start)
    r2, w2 = reading(shadow)
    assert (r,w[:4]) == (r2,w2[:4]) and phase(zero_start) != phase(shadow)
    # For a passive B (unchanged 7), no one incident coordinate can certify A1.
    for j in range(4):
        pooled = defaultdict(set)
        for (r,w), labels in by_local.items():
            if r==7:
                pooled[w[j]].update(label for _,label in labels)
        assert all(v != {"A1"} for v in pooled.values())
    minimal = {mode: classify_subsets(observations, mode=="plus_B")
               for mode in ("work_only","plus_B")}
    assert minimal["work_only"]["minimal_at_that_size"] == [[n for n in NAMES if n!="BF"]]
    assert minimal["plus_B"]["minimal_at_that_size"] == [["BA","AE","AF","AX","EF","FX"]]
    def totals(d):
        return dict(sorted(Counter(",".join(sorted(v)) for v in d.values()).items()))
    assert totals(by_w) == {"P":97,"B0":97,"A0":18,"A1":27,"A0,A1":52}
    assert totals(by_state) == {"P":117,"B0":117,"A0":27,"A1":28,"A0,A1":62}
    return dict(arms=2, arm_states=378, distinct_states=len(by_state), metrics=len(by_w),
                geometry_record_sets=totals(by_w), atlas_record_sets=totals(by_state),
                minimum_fixed_coordinate_subsets=minimal, editor_controls=schedule_controls,
                six_orders_local_positive=6, F_response=response,
                paired_non_F_preparations=dict(states=12,edges=20,disjoint_menus=3),
                same_atlas_conflict={"arm":1,"first":first[0]["delta_h"],"second":second[1]["delta_h"]},
                evidence_sha256=sha256(prior.encoded(evidence)).hexdigest()), evidence


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout",type=Path)
    parser.add_argument("--raw",type=Path)
    args=parser.parse_args()
    result, raw = run(args.checkout.resolve())
    if args.raw:
        args.raw.write_bytes(prior.encoded(raw))
    print(json.dumps(result,sort_keys=True,indent=2))
