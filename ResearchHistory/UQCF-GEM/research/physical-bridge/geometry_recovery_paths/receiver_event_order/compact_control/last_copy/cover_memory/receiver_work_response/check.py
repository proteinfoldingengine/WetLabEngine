"""An exact receiver-input test of the historical 25-chart one-edit recovery."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha1, sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
import inspect
from math import lcm
import os
from pathlib import Path
import sys

import numpy as np

DEMO = Path("ResearchHistory/UQCF-GEM/demos")
REPAIR = Path("ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/check_geometry_repair.py")
SOURCE = 0
RECIPIENT = 12
SITE = 1
REPAIR_SITE = 2


def pinned(name, path, identity):
    data = path.read_bytes()
    assert sha1(f"blob {len(data)}".encode() + bytes([0]) + data).hexdigest() == identity, path
    spec = spec_from_file_location(name, path)
    obj = module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


def stored(x):
    if isinstance(x, Fraction):
        return x.numerator if x.denominator == 1 else str(x)
    raise TypeError(type(x))


def encoded(x):
    return (json.dumps(x, default=stored, sort_keys=True, separators=(",",":"))+"\n").encode()


def five_chart(p1, geom, op):
    """The preceding edge witness and the exact type obstruction on five labels."""
    rows = ((0,), (0,4,6), (0,2,3), (0,2,4,5), (0,1,4,7))
    p = (-1,)+(0,)*7
    atom = op["atom"]
    cert = atom.atomic(p,rows,3,2)
    op["verify"].verify_atomic(cert)
    out = []
    for state in (rows,tuple(map(tuple,cert["after"]))):
        pair = []
        for u in (1,3):
            grade = (4-u,1,1,1,1,u,1,1)
            loc = [p1.push(p,tuple(range(8)),row,grade) for row in state]
            coords = [tuple(dict(zip(row,y)).get(v,0) for v in range(1,8)) for row,y in zip(state,loc)]
            res = geom.construct_response_geometry(tuple(range(5)),coords,coords)
            assert geom.metric_passes(res)
            neighbors = sorted(j for j in range(5) if frozenset((1,j)) in res.neighbors)
            assert loc[1] == (8,1,1)
            pair.append(dict(incident_neighbors=neighbors, AF=res.work[1][3], minimum=res.minimum))
        out.append(pair)
    assert out[0][0]["incident_neighbors"] == out[0][1]["incident_neighbors"] == [0]
    assert [x["incident_neighbors"] for x in out[1]] == [[0,3],[0]]
    assert [[x["AF"] for x in state] for state in out] == [[3,11],[2,10]]
    # Independently of that metric, no five-label simple graph passes the original gate.
    core = sys.modules["operational_complex"]
    labels = tuple(range(5))
    pairs = list(combinations(labels,2))
    reasons = Counter()
    for mask in range(1<<len(pairs)):
        edges = frozenset(frozenset(e) for j,e in enumerate(pairs) if mask & (1<<j))
        W = tuple(tuple(Fraction(0 if i==j else 1 if frozenset((i,j)) in edges else 2)
                        for j in labels) for i in labels)
        audit = core.construct_operational_complex(labels,W,edges)
        assert audit.complex is None
        reasons[audit.reason]+=1
    assert reasons == {"degree_not_four":1023,"edge_cycle_count":1}
    return dict(before_after=out, rejected_five_label_graphs=dict(reasons))


def preparations(fixture):
    _,original = fixture
    base = list(original)
    lo,hi = base.copy(),base.copy()
    lo[1] = 1
    for i in (662,896,935,947):
        lo[i] = 2
    lo[1353] = 4
    lo[160:163] = [Fraction(k,7) for k in (41,5,3)]
    hi[1] = Fraction(5,2)
    for i in (660,894,933,945):
        hi[i:i+3] = [Fraction(9,2),Fraction(5 if i==660 else 7,2),Fraction(5 if i==660 else 1,2)]
    hi[1352:1356] = [Fraction(31,2),7,Fraction(1,2),Fraction(1,2)]
    return dict(nominal=base, one=lo, five_halves=hi)


def all_candidate_certificates(rows, parents, squares, W, labels, mu):
    """Independent complete search: trial-insert the changed row and remeasure all degrees."""
    sets = list(map(set,rows))
    frequency = Counter(v for values in sets for v in values)
    scale = lcm(*(Fraction(z).denominator for z in squares))
    wi = np.array([[int(a*scale) for a in row] for row in W],dtype=np.int64)
    cost = [int(a*scale) for a in squares]
    memberships = [tuple(v in held for held in sets) for v in range(len(parents))]
    upper = np.triu_indices(len(labels),1)
    cache = {}
    same_min = []
    four = []
    seen = 0
    for i,held in enumerate(sets):
        blocked = {parents[v] for v in held if v}
        for v in sorted(held):
            if v==0 or v in blocked or frequency[v]<2:
                continue
            seen+=1
            key = (i,memberships[v],cost[v])
            if key not in cache:
                shift = np.array([cost[v] if yes else -cost[v] for yes in memberships[v]])
                changed = wi[i]+shift
                changed[i] = 0
                M = wi.copy()
                M[i,:] = M[:,i] = changed
                minimum = M[upper].min()
                mask = M==minimum
                np.fill_diagonal(mask,False)
                degree_ok = bool(np.all(np.count_nonzero(mask,axis=1)==4))
                cache[key] = (minimum==mu*scale,degree_ok)
            threshold, degree_ok = cache[key]
            if degree_ok:
                four.append((i,v))
                if threshold:
                    same_min.append((i,v))
    return dict(legal=seen,degree_four=four,degree_four_at_original_minimum=same_min)


def trace_neighbor_comparison(core, legacy, payload, center):
    """Read the actual local maximum immediately after the original function computes it."""
    func = core.construct_operational_complex
    source, first = inspect.getsourcelines(func)
    at = first+next(i for i,line in enumerate(source) if "if len(maxima) != 2" in line)
    hits = []
    previous = sys.gettrace()

    def local(frame, event, arg):
        if event=="line" and frame.f_lineno==at and frame.f_locals["label"]==center:
            slots=frame.f_locals
            hits.append(dict(maximum=slots["maximum"], maxima=sorted(slots["maxima"]),
                             comparisons=sorted((i,j,w) for (i,j),w in slots["values"].items())))
        return local

    def monitor(frame, event, arg):
        return local if frame.f_code is func.__code__ else None

    try:
        sys.settrace(monitor)
        carrier=legacy.build_carrier(payload)
    finally:
        sys.settrace(previous)
    assert len(hits)==1
    return carrier,hits[0]


def audits(root):
    os.chdir(root)
    model = pinned("work_original",REPAIR,"3324c0b46e09120ae526338444a19070b692d049")
    op = model.modules()  # blob checks on all historical dependencies
    p1 = pinned("p1_work_inputs",DEMO/"v16.23-overlap-descent/engine.py","b18f52109ccff9c7dc77542d3b8f3e5d5989102a")
    five = five_chart(p1,op["work"],op)
    features,target = model.fixture()
    parents,base,holders = map(tuple,zip(*features))
    rows = model.initial_state(features)
    full = tuple(range(len(parents)))
    B = RECIPIENT
    pre_source = op["atom"].atomic(parents,rows,SOURCE,SITE)
    op["verify"].verify_atomic(pre_source)
    after = tuple(map(tuple,pre_source["after"]))
    receiver = op["atom"].atomic(parents,after,B,REPAIR_SITE)
    op["verify"].verify_atomic(receiver)
    repaired = tuple(map(tuple,receiver["after"]))
    nbors = tuple(sorted(j for i,j in model.edges(target)[1] if i==B))+tuple(sorted(i for i,j in model.edges(target)[1] if j==B))
    nbors = tuple(sorted(nbors))
    assert nbors == (7,11,13,17)
    masks = list(dict.fromkeys(frozenset(h) for h in holders if B not in h))
    U = set(model.LABELS)-{B}
    O = U-{SOURCE}-set(nbors)
    assert set(masks) == {frozenset(a) for a in [U, {SOURCE}|O, {SOURCE}|set(nbors), {SOURCE},
                                                  *(U-{i} for i in U)]} and len(masks)==28
    ref_values = None
    ref_inc = None
    ref_table = None
    proofs = {}
    report = {}
    legacy_geo = op["carriers"]
    from projection import Payload
    def graph_for(W,trace=False):
        mu,edges = model.edges(W)
        safe = tuple(tuple(map(Fraction,r)) for r in W)
        try:
            payload = Payload(5,Fraction(1),model.LABELS,safe,edges,())
            obj = legacy_geo.build_carrier(payload)
            if trace:
                twin,record = trace_neighbor_comparison(sys.modules["operational_complex"],legacy_geo,payload,B)
                assert twin==obj
                return "ADMITTED",edges,record
        except ValueError as err:
            return str(err), edges
        assert obj.baseline.flat and obj.complex.tangent_rank==2
        return "ADMITTED", edges

    for name,grade in preparations((parents,base)).items():
        assert len(grade)==len(parents) and min(grade)>0 and sum(grade)==3177 and grade[0]==1
        subtotal = list(grade)
        for v in range(len(parents)-1,0,-1):
            subtotal[parents[v]]+=subtotal[v]
        square = [x*x for x in subtotal]
        d = square[SITE] - 4
        localgrade = p1.push(parents,full,rows[B],grade)
        YR = p1.push(parents,full,after[B],grade)
        Y2 = p1.push(parents,full,repaired[B],grade)
        assert YR==localgrade and Y2[0]-YR[0]==2
        W0,W1,W2 = [model.work_for(s,square) for s in (rows,after,repaired)]
        status0,edges0,trace0 = graph_for(W0,True)
        status1,edges1 = graph_for(W1)
        status2,edges2 = graph_for(W2)
        assert status0=="ADMITTED" and edges0==model.edges(target)[1]
        if ref_values is None:
            ref_values,ref_table,ref_inc=Y2,W0,YR
        assert YR==ref_inc and Y2==ref_values
        for i in model.LABELS:
            for j in model.LABELS:
                inside = i!=j and i in nbors and j in nbors
                assert W0[i][j]==ref_table[i][j]-(2*d if inside else 0)
        for j in model.LABELS:
            assert W1[B][j]-W0[B][j]==(-square[SITE] if j==SOURCE else 0)
        assert W0[B] == ref_table[B]
        assert all(W1[SOURCE][j]==model.MU-d for j in nbors)
        assert min(W1[SOURCE][j] for j in model.LABELS if j!=SOURCE) == min(model.MU-d, model.MU+square[SITE])
        non_source = [i for i in model.LABELS if i!=SOURCE]
        assert [j for j in non_source if W0[B][j]==1984] == [j for j in non_source if W1[B][j]==1984] == list(nbors)
        enumeration = all_candidate_certificates(after,parents,square,W1,model.LABELS,model.MU)
        expected = [(B,REPAIR_SITE)] if d==0 else []
        others = [e for e in enumeration["degree_four"] if e[0]!=SOURCE]
        assert enumeration["legal"]==32575 and others==expected
        assert sorted(others)==sorted(e for e in enumeration["degree_four_at_original_minimum"] if e[0]!=SOURCE)
        # The historical scanner has an explicit threshold precondition. The higher
        # counterfactual runs below that threshold after the source cut.
        if min(W1[i][j] for i,j in combinations(model.LABELS,2))==model.MU:
            counts,candidates = model.degree_candidates(features,after,W1,square)
            assert sum(counts.values())==32575 and sorted(candidates)==sorted(enumeration["degree_four_at_original_minimum"])
            scanner = dict(called=True,candidates=candidates)
        else:
            assert d>0
            try:
                model.degree_candidates(features,after,W1,square)
            except AssertionError:
                scanner = dict(called=True,precondition="minimum != MU")
            else:
                raise AssertionError("historical precondition did not reject")
        if d==0:
            assert status2=="ADMITTED"
        else:
            assert status2=="degree_not_four"
        # Exhibit the 24 B distances, the six affected other distances and the
        # original minimum edges, without storing three redundant 25-by-25 matrices.
        nn_pairs = list(combinations(nbors,2))
        report[name] = dict(source_subtotal=subtotal[SITE], total=sum(grade), fine_Pin=grade[0],
            receiver_prior_sha256=sha256(encoded(YR)).hexdigest(),
            receiver_root_prior=YR[0], receiver_root_after_fixed_legal_cut=Y2[0],
            geometry_before=status0, geometry_after_source=status1, geometry_after_receiver=status2,
            own_row_sum_before=sum(W0[B]), own_row_sum_after=sum(W1[B]),
            source_pair_before=W0[B][SOURCE],source_pair_after=W1[B][SOURCE],
            neighbors_before=list(nbors),neighbors_after=[j for j in non_source if W1[B][j]==min(W1[i][k] for i,k in combinations(model.LABELS,2))],
            neighbor_pair_works=[W0[i][j] for i,j in nn_pairs], traced_local_maximum=trace0["maximum"],
            all_next_legal=enumeration["legal"],eligible_non_source=others, historical_scanner=scanner)
        proofs[name]=dict(fine_changes=[[i,grade[i]] for i in full if grade[i]!=base[i]],local_incident_before=W0[B],
            local_incident_after=W1[B],neighbor_pairs=[[i,j,W0[i][j]] for i,j in nn_pairs],
            original_constructor_trace=trace0,global_work_changed=[[i,j,W0[i][j]-ref_table[i][j]] for i,j in combinations(model.LABELS,2) if W0[i][j]!=ref_table[i][j]],
            post_edges=list(edges1), raw_candidates=enumeration["degree_four"],
            states=[dict(chart_edit=[c["index"],c["leaf"]],delta_h=c["delta_h"]) for c in (pre_source,receiver)])
    assert report["nominal"]["eligible_non_source"]==[(12,2)] and report["one"]["eligible_non_source"]==report["five_halves"]["eligible_non_source"]==[]
    # Reconstruct the exact rank test without relying on approximate singular values.
    import sympy as sp
    b=sp.Matrix([[int((B in h)!=(i in h)) for h in masks] for i in model.LABELS if i!=B])
    pairs=tuple(e for e in model.edges(target)[1] if B not in e)
    edge=sp.Matrix([[int((i in h)!=(j in h)) for h in masks] for i,j in pairs])
    null=b.col_join(edge).nullspace()
    totals={frozenset(holders[SITE]):1,frozenset(set(model.LABELS)-{B}):3,
            **{frozenset(set(model.LABELS)-{B,k}):-1 for k in nbors}}
    expected=sp.Matrix([totals.get(m,0) for m in masks])
    assert b.rank()==24 and len(null)==1 and null[0]/null[0][masks.index(frozenset(holders[SITE]))]==expected
    digest = sha256(encoded(proofs)).hexdigest()
    result=dict(five_chart=five,receiver=12,source=0,source_site=1,neighbor_pairs=list(combinations(nbors,2)),
        matrix_columns=len(masks),incident_rank=b.rank(),combined_rank=len(masks)-len(null),
        cases=report,raw_sha256=digest)
    return result,proofs


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_checkout",type=Path)
    parser.add_argument("--raw",type=Path)
    args = parser.parse_args()
    dest=args.raw.resolve() if args.raw else None
    result,raw=audits(args.historical_checkout.resolve())
    if dest:
        dest.write_bytes(encoded(raw))
    print(json.dumps(result,default=stored,sort_keys=True,indent=2))
