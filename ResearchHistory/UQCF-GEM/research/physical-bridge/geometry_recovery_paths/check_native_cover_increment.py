"""Classify all one-cut changes in the native covering number on two archived preparations."""
import importlib.util
import json
import os
import sys
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path

from check_receiver_command import FIXTURE, PINS, hash_blob

HISTORICAL_CUT = Path("ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py")
SOURCE_SITES = (718, 719)
A = 0


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def membership(rows, size):
    holders = [set() for _ in range(size)]
    for i, row in enumerate(rows):
        for v in row:
            holders[v].add(i)
    return holders


def private_root_charts(parents, holders):
    return {next(iter(s)) for v, s in enumerate(holders) if parents[v] == 0 and len(s) == 1}


def extension(f, parents, grades, rows):
    """Choose the lexicographically first two compatible unit cuts for the prospective construction."""
    holders = membership(rows, len(parents))
    private = private_root_charts(parents, holders)
    groups = defaultdict(list)
    for v in range(6, len(parents)):
        if grades[v] == 1 and len(holders[v]) >= len(rows)-2:
            groups[tuple(sorted(f.ALL-holders[v]))].append(v)
    options = [(tuple(pair), vs[0]) for pair, vs in sorted(groups.items())
               if len(pair) == 2 and not set(pair) & {A, f.B}]
    for (left, u), (right, v) in combinations(options, 2):
        if set(left) & set(right):
            continue
        for d in left:
            for e in right:
                if not groups[(d,)] or not groups[(e,)]:
                    continue
                enlarged = private | {d, e}
                if len(enlarged) != len(private)+2:
                    continue
                if any(len(holders[w] & enlarged) < 2 for w in (f.T, f.ULEAF, f.R)):
                    continue
                # u was absent in left and v in right. Each ends up only in the other's missing pair.
                common = sorted(f.ALL-set(left)-set(right))
                swaps = [(i, w) for i in common for w in (u, v)]
                drop_d, = set(left)-{d}
                drop_e, = set(right)-{e}
                mates = [groups[(d,)][0], groups[(e,)][0]]
                steps = swaps + [(drop_d, v), (drop_d, mates[0]), (drop_e, u), (drop_e, mates[1])]
                return steps, dict(missing_pairs=[left,right], exchange_units=[u,v],
                                   new_private_charts=[d,e], complementary_units=mates)
    raise ValueError("No geometry-preserving extension of the proposed form")


def baseline_families(rows, parents):
    """Enumerate chart subsets from size one through minimum+one, without forcing private charts."""
    targets = sum(1 << v for v in range(1, len(parents)) if parents[v] == 0)
    masks = [sum(1 << v for v in row) & targets for row in rows]
    found = []
    for r in range(1, len(rows)+1):
        covers = []
        for sub in combinations(range(len(rows)), r):
            union = 0
            for i in sub:
                union |= masks[i]
            if union == targets:
                covers.append(sub)
        if covers:
            found.append(covers)
            if len(found) == 2:
                return found
    raise ValueError("No successive cover families")


def classify(rows, parents):
    """Evaluate every legal primitive using before-cover survival and a separate private-witness formula."""
    holders = membership(rows, len(parents))
    roots = [v for v in range(1,len(parents)) if parents[v]==0]
    assert {parents[v] for v in range(1,len(parents))} == {0, 3}
    assert [v for v in range(1,len(parents)) if parents[v]==3] == [4] and holders[4] == {A}
    priv = private_root_charts(parents, holders)
    assert all(priv & holders[v] for v in roots)
    minima, next_covers = baseline_families(rows, parents)
    assert list(map(set,minima)) == [priv]
    min_sets = list(map(set,minima))
    next_sets = list(map(set,next_covers))
    # Independent native menu from local-leaf constraints, as distinct from holder projections.
    native = set()
    for i, row in enumerate(rows):
        protected = {parents[v] for v in row if v}
        outside = set().union(*(set(r) for j,r in enumerate(rows) if j!=i))
        native.update((i,v) for v in row if v and v not in protected and v in outside)
    projected = {(i,v) for v in roots if len(holders[v])>=2 for i in holders[v]
                 if (v,i)!=(3,A)}
    assert native == projected
    strict, complete = [], []
    for i,v in sorted(native):
        rest = holders[v]-{i}
        surviving = [s for s in min_sets if s & rest]
        if not surviving:
            surviving = [s for s in next_sets if s & rest]
        predicted = ([priv] if priv & rest else [priv | {j} for j in sorted(rest)])
        assert {frozenset(s) for s in surviving} == {frozenset(s) for s in predicted}
        h_after = len(surviving[0])
        count = len(surviving)
        complete.append([i,v,h_after,count])
        if h_after != len(priv):
            strict.append(dict(editor=i, leaf=v, h_after=h_after, minimum_covers=count,
                               additional_charts=sorted(set.union(*surviving)-priv)))
    return dict(legal=len(native), h=len(priv), minimum_cover=sorted(priv),
                private_root_witnesses={str(i):[v for v in roots if holders[v]=={i}] for i in sorted(priv)},
                all_events_sha256=digest(complete), strict=strict)


def run(sources, history, *, invoke_original=True):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    assert hash_blob(HISTORICAL_CUT.read_bytes()) == "fc4a77fc4f01fce33fdb562423eca274cfb0c648"
    assert sha256(history).hexdigest() == "afa2a993f5a4fabc410df621b9377659fe6d98a1a3993a29990ea25a0abcf19b"
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    modules = f.modules()
    spec = importlib.util.spec_from_file_location("profile_producer", HISTORICAL_CUT)
    producer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(producer)
    features, original = f.fixture()
    parents, grades, _ = map(tuple,zip(*features))
    sums = list(grades)
    for v in range(len(sums)-1,0,-1):
        sums[parents[v]] += sums[v]
    squares = [n*n for n in sums]
    cut = lambda rows,i,v: producer.cut(parents,rows,(i,v))
    hist = json.loads(history)
    rows = f.initial_state(features)
    for i,v in hist["preparation"]:
        rows = cut(rows,i,v)
    assert digest(rows)==hist["common_rows_digest"] and f.work_for(rows,squares)==original
    extra, recipe = extension(f, parents, grades, rows)
    reinforced = rows
    for i,v in extra:
        reinforced = cut(reinforced,i,v)
    assert f.work_for(reinforced,squares)==original
    output = dict(charts=len(rows), vertices=len(parents), prior_steps=len(hist["preparation"]),
                  extra=extra, recipe=recipe, original_work_sha256=digest(original), states={}, historical_checks=[])
    def admission(work):
        payload = modules["projection"].Payload(f.SIDE, Fraction(1), f.LABELS,
                tuple(tuple(map(Fraction,r)) for r in work), f.edges(work)[1], ())
        try:
            modules["carriers"].build_carrier(payload)
        except ValueError as error:
            return str(error)
        return "accepted"

    assert admission(original)=="accepted"
    def check_atom(label, before, i, v, h0, h1):
        after = cut(before,i,v)
        if invoke_original:
            event = modules["atom"].atomic(parents,before,i,v)
            verified = modules["verify"].verify_atomic(event)
            assert verified == (h1-h0,h1>h0)
            assert (event["tau_before"],event["h_before"],event["tau_after"],event["h_after"])==(h0,h0,h1,h1)
            assert tuple(map(tuple,event["after"]))==after
            pair = [event["h_before"],event["h_after"]]
            tr = event["trigger"]
        else:
            old = baseline_families(before, parents)[0]
            new = baseline_families(after, parents)[0]
            pair = [len(old[0]),len(new[0])]
            kids = {w for w in range(1,len(parents)) if parents[w]==parents[v]}
            tr = all(not kids.issubset(set().union(*(after[j] for j in group))) for group in old)
        assert pair==[h0,h1] and tr==(h1>h0)
        output["historical_checks"].append(dict(label=label, index=i, leaf=v, h=pair,
                trigger=tr, delta_h=pair[1]-pair[0], before=digest(before), after=digest(after)))
        return after

    for name, common in (("original",rows),("reinforced",reinforced)):
        state = dict(common_rows_sha256=digest(common), arms={})
        output["states"][name] = state
        holds = membership(common,len(parents))
        assert all(holds[v]=={A,f.B} for v in SOURCE_SITES)
        joined = []
        for x,y in (SOURCE_SITES,tuple(reversed(SOURCE_SITES))):
            source = cut(common,A,x)
            case = classify(source,parents)
            arm = case
            state["arms"][str(x)] = arm
            unique_strict = [(r["editor"],r["leaf"]) for r in case["strict"] if r["minimum_covers"]==1]
            assert unique_strict==[(f.B,y)]
            if name=="reinforced":
                assert len(case["strict"])==1
            else:
                assert len(case["strict"])>1
            cost = case["h"]
            assert holds[x]-{A}=={f.B} and source[f.B]==common[f.B]
            arm["source"]=dict(cut=[A,x], b_unchanged=True, now_private_at_B=x)
            written = check_atom(name+"_record_"+str(x),source,f.B,y,cost,cost+1)
            source_work = f.work_for(source,squares)
            record_work = f.work_for(written,squares)
            arm["work_after_source_sha256"] = digest(source_work)
            arm["work_after_receiver_sha256"] = digest(record_work)
            arm["source_gate"] = admission(source_work)
            arm["receiver_gate"] = admission(record_work)
            arm["receiver_sites_after"]=[v for v in SOURCE_SITES if v in written[f.B]]
            post_record = membership(written, len(parents))
            assert arm["receiver_sites_after"]==[x] and post_record[x]=={f.B} and post_record[y]=={A}
            joined.append(cut(source,A,y))
            if name=="reinforced":
                idle = cut(source,A,hist["source_mate"])
                intermediate = cut(written,A,hist["source_mate"])
                closed = cut(intermediate,f.B,1301)
                stages = [idle, intermediate, closed]
                covers = [baseline_families(s,parents)[0] for s in stages]
                assert [len(fam[0]) for fam in covers]==[cost,cost+1,cost+1]
                assert all(len(fam)==1 for fam in covers)
                assert f.work_for(idle,squares)==f.work_for(closed,squares)==original
                assert idle[f.B]==common[f.B] and [v for v in SOURCE_SITES if v in closed[f.B]]==[x]
                arm["returned_geometry"]=dict(idle_tail=[[A,hist["source_mate"]]],
                        recording_tail=[[f.B,y],[A,hist["source_mate"]],[f.B,1301]],
                        idle_h=cost, recording_h=cost+1, both_work_sha256=digest(original),
                        both_gate=admission(original), idle_b_sites=list(SOURCE_SITES), recording_b_sites=[x])
            if name=="original" and x==SOURCE_SITES[0]:
                rival=next(r for r in case["strict"] if r["editor"]!=f.B)
                check_atom("original_strict_other_chart",source,rival["editor"],rival["leaf"],cost,cost+1)
            if name=="original":
                restored = cut(source,A,hist["source_mate"])
                assert f.work_for(restored,squares)==original
                blind = check_atom("historical_blind_sibling_"+str(x),restored,A,y,cost,cost)
                blind = check_atom("historical_blind_593_"+str(x),blind,A,593,cost,cost)
                changes = [[i,j,original[i][j],z] for i,row in enumerate(f.work_for(blind,squares))
                           for j,z in enumerate(row) if i<j and z!=original[i][j]]
                assert changes==[[0,6,1992,1990]] and blind[f.B]==common[f.B]
                arm["prior_blind"]=dict(cuts=[[A,y],[A,593]],h_values=[cost]*3,changed_work=changes)
        assert joined[0]==joined[1]
        state["source_order_diamond_sha256"]=digest(joined[0])
        if name=="reinforced":
            cost = case["h"]
            check_atom("reinforced_neutral_source_718",common,A,718,cost,cost)
            check_atom("reinforced_blind_sibling_719",cut(common,A,718),A,719,cost,cost)
            current = joined[0]
            post = membership(current,len(parents))
            core = private_root_charts(parents,post)
            assert core==set(case["minimum_cover"]) and all(s & core for v,s in enumerate(post) if parents[v]==0)
            candidates=[v for v,s in enumerate(post) if v>5 and grades[v]==1 and f.B not in s
                        and len(s & core)>0 and s-core and v not in SOURCE_SITES]
            witness = min(candidates,key=lambda v:(len(post[v]&core),v))
            removers=sorted(post[witness]&core)
            assert f.B not in removers
            delayed=[]
            for index,i in enumerate(removers):
                before=current
                current=cut(current,i,witness)
                after_holders=membership(current,len(parents))
                covers=baseline_families(current,parents)[0]
                last=index+1==len(removers)
                assert len(covers[0])==cost+int(last)
                if last:
                    assert check_atom("first_later_strict_other_chart",before,i,witness,cost,cost+1)==current
                delayed.append([i,witness,len(covers[0]),len(covers)])
                assert all(after_holders[v] for v in range(len(parents))) and current[f.B]==common[f.B]
            state["delayed_blind"]=dict(diamond_prefixes=[[[A,718],[A,719]],[[A,719],[A,718]]],
                    witness=witness, after_common_cuts=delayed, b_unchanged=True, endpoint_sha256=digest(current))
    # One raw source action and one raw response have the same work trajectory across preparations.
    for stage in ("work_after_source_sha256", "work_after_receiver_sha256"):
        hashes = {arm[stage] for state in output["states"].values() for arm in state["arms"].values()}
        assert len(hashes)==1
    return output


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Enable scientific assertions")
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources",type=Path)
    parser.add_argument("reference",type=Path)
    parser.add_argument("target",type=Path)
    parser.add_argument("--independent-covers",action="store_true",
                        help="Reconstruct historical event fields by independent subset enumeration")
    args = parser.parse_args()
    target = args.target.resolve()
    result = run(args.sources.resolve(),args.reference.read_bytes(),invoke_original=not args.independent_covers)
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:{x:[a["h"],a["legal"],len(a["strict"])] for x,a in s["arms"].items()}
                      for k,s in result["states"].items()},sort_keys=True))
