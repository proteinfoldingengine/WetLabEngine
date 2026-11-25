"""Recover the size of an actual withdrawal from surviving chart grades."""
import argparse
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LAST = HERE.parents[1]
spec = spec_from_file_location("last_copy", LAST / "check.py")
prior = module_from_spec(spec)
spec.loader.exec_module(prior)
prior.pinned(LAST / "check.py", "c7b0586362e74c22612a9926f1d7135cf074dfb0")


def load_sources(root, cfg):
    uq = root / "ResearchHistory/UQCF-GEM"
    demo = uq / "demos"
    a = demo / "v16.26-consistency-increment-law"
    atom = prior.module(a / "engine.py", "atom", cfg["engine_blob"])
    verify = prior.module(a / "verify.py", "verify", cfg["verify_blob"])
    p1 = prior.module(demo / "v16.23-overlap-descent/engine.py", "p1",
                      "b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    work = prior.module(uq / "research/physical-bridge/forced_parent_deletion/check_geometry_repair.py",
                        "work", "3324c0b46e09120ae526338444a19070b692d049")
    path = demo / "v15.40-global-balance-geometry-specificity/response_geometry.py"
    prior.pinned(path, "9128c24b695c1b539ac60dc93aeaf0bd4795c57b")
    spec = spec_from_file_location("response_geometry", path)
    geom = module_from_spec(spec)
    sys.modules[spec.name] = geom
    spec.loader.exec_module(geom)
    return atom, verify, p1, work, geom


def subtree(p, v):
    result = set()
    for site in range(len(p)):
        k = site
        while k >= 0 and k != v:
            k = p[k]
        if k == v:
            result.add(site)
    return result


def paired_work(work, geom, rows, totals):
    coords = [tuple(totals[v] if v in row else 0 for v in range(1, len(totals)))
              for row in rows]
    geometry = geom.construct_response_geometry(tuple(range(len(rows))), coords, coords)
    assert geometry.work == work.work_for(rows, [a*a for a in totals])
    return geometry


def swap_visibility(work, charts, states, edges, j):
    """Test when a legal withdrawal can expose or hide the swap in pair work."""
    def holders(state, site):
        return {name for name, row in zip(charts,state) if site in row}

    family = {}
    grades = []
    for u in (1,3):
        weights = [1]*8
        weights[5], weights[j] = u*u, (4-u)**2
        grades.append(weights)
    for s in states:
        h, k = holders(s,5), holders(s,j)
        assert h == {"F"}
        left, right = (work.work_for(s, w) for w in grades)
        equal = left == right
        assert equal == (h==k or h==set(charts)-k) == (k=={"F"})
        family[s] = (equal,"F" in k,len(k))
    lost = 0
    for (s,i,v),target in edges.items():
        equal, has_f, n = family[s]
        now_equal, now_has_f, _ = family[target]
        if equal:
            assert now_equal
        if not has_f:
            assert not now_has_f and not now_equal
        if now_equal and not equal:
            assert v==j and charts[i]!="F" and n==2
            lost += 1
    terminal = states-{s for s,i,v in edges}
    return dict(states=len(states),edges=len(edges), equal=sum(x[0] for x in family.values()),
                pending=sum(x[1] and x[2]==2 for x in family.values()),
                permanently_distinct=sum(not x[1] for x in family.values()),
                edges_hiding_swap=lost, terminals_equal=sum(family[s][0] for s in terminal),
                terminals_distinct=sum(not family[s][0] for s in terminal))


def small_tree_control(p1):
    trees = retained_rows = holder_checks = missing_checks = 0
    for n in range(2, 6):
        for parents in product(*(range(k) for k in range(1, n))):
            p = (-1,) + parents
            trees += 1
            full = tuple(range(n))
            values = tuple((-1)**i * (i+2) for i in full)
            for mask in range(1, 1 << n, 2):
                row = tuple(i for i in full if mask & (1 << i))
                if any(p[i] not in row for i in row if i):
                    continue
                retained_rows += 1
                local = p1.push(p, full, row, values)
                for v in full[1:]:
                    below = subtree(p, v)
                    if v in row:
                        assert sum(g for k, g in zip(row, local) if k in below) == sum(values[k] for k in below)
                        holder_checks += 1
                    else:
                        first = [2]*n
                        other = first.copy()
                        other[v] += 1
                        other[p[v]] -= 1
                        assert p1.push(p, full, row, first) == p1.push(p, full, row, other)
                        assert sum(first[k] for k in below)**2 != sum(other[k] for k in below)**2
                        missing_checks += 1
    return dict(ordered_parent_arrays=trees, retained_rows=retained_rows,
                holding_site=holder_checks, missing_site_counterexamples=missing_checks)


def run(root):
    cfg = json.loads(prior.pinned(LAST.parent / "FIXTURE.json", "806d2bc487e358f498cafa806226d1f658e98d26"))
    atom, verify, p1, work, geom = load_sources(root, cfg)
    charts = cfg["charts"]
    b, f = charts.index("B"), charts.index("F")
    initial = prior.rows(charts, cfg["tip_holders"])
    p = (-1,) + (0,)*7
    full = tuple(range(len(p)))
    evidence = []
    summary = {}
    for arm, path in enumerate(cfg["receipt_paths"]):
        start = initial
        events = []
        steps = [cfg["edits"][i] for i in path[:3]] + [("E",2), ("X",4), ("F",(4,2)[arm])]
        for name, v in steps:
            event = atom.atomic(p, start, charts.index(name), v)
            verify.verify_atomic(event)
            events.append(event)
            start = prior.as_rows(event["after"])
        probe = events[2]
        assert (probe["index"], probe["leaf"], probe["delta_h"]) == (b, 5, arm)
        before, after = (prior.as_rows(probe[k]) for k in ("before","after"))
        assert before[b] == (0,5,6) and start[f] == (0,(2,4)[arm],5)
        post_states, post_events = prior.native_graph(atom,verify,p,after)
        separate_states, post_edges = prior.reachable_by_columns(charts,after)
        prior.match_edges(post_states,post_events,separate_states,post_edges)
        visibility = swap_visibility(work,charts,post_states,post_edges,start[f][1])
        assert visibility == dict(states=189,edges=621,equal=63,pending=63,
            permanently_distinct=63,edges_hiding_swap=63,terminals_equal=12,terminals_distinct=12)
        states, edges = prior.native_graph(atom, verify, p, start)
        prior.match_edges(states, edges, *prior.reachable_by_columns(charts,start))
        assert (len(states), len(edges)) == (9,12)
        rows_checked = []
        for s in sorted(states):
            other_geometry = other_p1 = None
            samples = {}
            for u in (1,3):
                fine = [1]*8
                fine[5], fine[start[f][1]] = u, 4-u
                totals = [sum(fine[v] for v in subtree(p,k)) for k in full]
                current = paired_work(work, geom, s, totals)
                local = [p1.push(p, full, row, fine) for row in s]
                rest = tuple(y for i,y in enumerate(local) if i!=f)
                if other_geometry is not None:
                    assert (current,rest) == (other_geometry,other_p1)
                other_geometry, other_p1 = current,rest
                assert local[f] == (6,4-u,u) and [i for i,row in enumerate(s) if 5 in row] == [f]
                pre, post = [paired_work(work, geom, snap, totals).work for snap in (before,after)]
                delta = [[int(post[i][j]-pre[i][j]) for j in range(5)] for i in range(5)]
                amplitude = int(local[f][s[f].index(5)])
                predicted = [[0]*5 for _ in range(5)]
                for j in range(5):
                    if j!=b:
                        predicted[b][j] = predicted[j][b] = amplitude**2 * (1 if 5 in before[j] else -1)
                assert delta == predicted and delta[b] == [0,-u*u,-u*u,u*u,-u*u]
                # Use only contemporary chart grades, plus the old list of B addresses.
                minimal = []
                for i,row in enumerate(s):
                    if 6 not in row:
                        continue
                    assert i != f
                    union = tuple(sorted(set(row)|set(s[f])))
                    joint = p1.glue(p, s[f], row, local[f], local[i], positive=True)
                    past_b = p1.push(p, union, before[b], joint)
                    assert past_b == (9-u,u,1) == p1.push(p, full, before[b], fine)
                    minimal.append(charts[f]+charts[i])
                assert minimal
                trials = []
                for proposal in (1,3):
                    candidate = (9-proposal,proposal,1)
                    try:
                        p1.glue(p,s[f],before[b],local[f],candidate,positive=True)
                        trials.append(True)
                    except ValueError as exc:
                        assert str(exc) == "incompatible overlap sources"
                        trials.append(False)
                assert trials == [u==1, u==3]
                samples[str(u)] = dict(F=list(map(int,local[f])), former_B=list(map(int,past_b)),
                    current_B=list(map(int,local[b])), minimal_pairs=minimal, signed_B_row=delta[b],
                    proposals_1_3=trials, local_grades=[list(map(int,y)) for y in local],
                    earlier_work=[list(map(int,r)) for r in pre],
                    immediate_work=[list(map(int,r)) for r in post],
                    current_work=[list(map(int,r)) for r in current.work])
            rows_checked.append(dict(rows=s, cases=samples))
        evidence.append(dict(arm=arm, history=events, continuations=rows_checked))
        summary[str(arm)]=dict(states=len(states), ordinary_edges=len(edges), post_B_visibility=visibility,
                               cover_increment=probe["delta_h"],
                                possible_pairs=sorted({v for z in rows_checked for v in z["cases"]["1"]["minimal_pairs"]}))
    # Internal site, three holders before deletion including the actor, signed cancellation.
    parent = (-1,0,1,1,0)
    old = ((0,1),(0,1,2),(0,1,3),(0,4))
    cert = atom.atomic(parent,old,0,1)
    verify.verify_atomic(cert)
    new = prior.as_rows(cert["after"])
    internal = []
    for grades in ((1,2,3,5,1),(1,-2,-3,-5,1),(1,-2,3,-1,1)):
        totals = [sum(grades[v] for v in subtree(parent,k)) for k in range(5)]
        a,c = [paired_work(work,geom,rows,totals).work for rows in (old,new)]
        expected = [0,totals[1]**2,totals[1]**2,-totals[1]**2]
        assert [c[0][i]-a[0][i] for i in range(4)] == expected
        for row in new[1:3]:
            local = p1.push(parent,tuple(range(5)),row,grades)
            assert sum(g for k,g in zip(row,local) if k in subtree(parent,1)) == totals[1]
        internal.append(dict(subtree_total=totals[1],delta=expected))
    # Same two-level tree, same three legal edits, same total, unequal child splits.
    scales = []
    complement = ((0,1),(0,2),(0,2))
    assert paired_work(work,geom,complement,[5,1,3]) == paired_work(work,geom,complement,[5,3,1])
    changed = ((0,1),(0,2),(0,1,2))
    assert paired_work(work,geom,changed,[5,1,3]) != paired_work(work,geom,changed,[5,3,1])
    parent = (-1,0,1,1)
    all_sites = tuple(range(4))
    for left, right in ((2,2),(1,3)):
        fine = (1,1,left,right)
        totals = [sum(fine[v] for v in subtree(parent,k)) for k in all_sites]
        chart_state = (all_sites,all_sites)
        jumps = {}
        for site in (2,3,1):
            before_work = paired_work(work,geom,chart_state,totals).work
            e = atom.atomic(parent,chart_state,0,site)
            verify.verify_atomic(e)
            chart_state = prior.as_rows(e["after"])
            after_work = paired_work(work,geom,chart_state,totals).work
            jumps[site] = int(after_work[0][1]-before_work[0][1])
        assert jumps == {1:25, 2:left**2, 3:right**2}
        scales.append(dict(child_grades=[left,right], child_work=[jumps[2],jumps[3]],
                           parent_grade=fine[1], parent_work=jumps[1]))
    return dict(arms=summary, current_states_compared=18, paired_grade_cases=36,
                tree_controls=small_tree_control(p1), internal_site_controls=internal,
                branching_controls=scales,
                historical_B_work_rows={"1":[0,-1,-1,1,-1],"3":[0,-9,-9,9,-9]},
                raw_sha256=sha256(prior.encoded(evidence)).hexdigest()), evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--raw", type=Path)
    args = parser.parse_args()
    result, evidence = run(args.checkout.resolve())
    if args.raw:
        args.raw.write_bytes(prior.encoded(evidence))
    print(json.dumps(result,sort_keys=True,indent=2))
