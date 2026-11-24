"""Classify every one-chart endpoint preserving all work, without a length bound."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

from check_receiver_command import FIXTURE, PINS, hash_blob


def identity(values):
    return sha256(json.dumps(values, separators=(",", ":")).encode()).hexdigest()


def possible_addresses(parents, rows, i):
    others = set().union(*(r for j, r in enumerate(rows) if j != i))
    fixed = set(rows[i]) - others
    for private in tuple(fixed):
        while private:
            private = parents[private]
            fixed.add(private)
    return set(rows[i]) - fixed - {0}


def classify_signed_columns(columns, labels, neighbors, a, b, i, shared):
    all_other = set(labels) - {i}

    def score(v, group):
        return sum(columns[v][j] for j in group)

    if i not in (a, b):
        subset = (neighbors | {a,b}) - {i} if i in neighbors else all_other
        lower = min((score(v, subset) for v in columns), default=None)
        assert lower is None or lower > 0
        return [], {"kind":"positive certificate","labels":sorted(subset),"minimum":lower}

    available = set(columns)
    notes = {}
    if i == b:
        projected = {v:score(v,neighbors) for v in available}
        assert {v for v in available if projected[v] < 0} == {shared}
        assert projected[shared] == -4 and projected[2] == 16
        available.remove(2)
        notes["eliminated_on_neighbors"] = 2
    totals = {v:score(v,all_other) for v in available}
    assert totals.pop(shared) == -22 and min(totals.values()) >= 20
    partners = [v for v,w in totals.items() if w == 22 and all(
        columns[v][j] == -columns[shared][j] for j in all_other)]
    notes.update(kind="one negative budget",negative=shared,budget=22,
                 positive_minimum=min(totals.values()),partners=sorted(partners))
    return sorted(tuple(sorted((shared,v))) for v in partners), notes


def independent_endpoints(parents, squares, rows, work, i, labels, neighbors):
    # Peel every removable local leaf; the survivors cannot disappear in any local history.
    outside = set().union(*(r for j,r in enumerate(rows) if j != i))
    row = set(rows[i])
    while True:
        parents_present = {parents[v] for v in row if v}
        layer = (row & outside) - parents_present - {0}
        if not layer:
            break
        row -= layer
    allowed = set(rows[i]) - row

    # Measure a single coordinate flip against each other row. Downward closure is
    # checked on final endpoints, so an internal flip can be used as a formal column.
    masks = [sum(1 << v for v in r if v) for r in rows]
    weights = defaultdict(int)
    for v in range(1,len(parents)):
        weights[squares[v]] |= 1 << v
    other = sorted(set(labels) - {i})
    cols = {}
    for v in allowed:
        candidate = masks[i] ^ (1 << v)
        col = []
        for j in other:
            xor = candidate ^ masks[j]
            col.append(sum(w * (xor & mask).bit_count() for w,mask in weights.items()) - work[i][j])
        cols[v] = tuple(col)

    # Interval elimination is valid for every subset. A selected term must be
    # offset by available terms of the opposite sign along every projection.
    all_indices = tuple(range(len(other)))
    subsets = [all_indices, tuple(k for k,j in enumerate(other) if j in neighbors),
               tuple(k for k,j in enumerate(other) if j in neighbors | {0,12})]
    subsets += [(k,) for k in all_indices]
    pool = set(cols)
    while pool:
        prior = pool.copy()
        for subset in subsets:
            projected = {v:sum(cols[v][k] for k in subset) for v in pool}
            pos = sum(x for x in projected.values() if x > 0)
            neg = -sum(x for x in projected.values() if x < 0)
            pool = {v for v,x in projected.items() if -pos <= x <= neg}
        if prior == pool:
            break
    total = {v:sum(cols[v]) for v in pool}
    neg = sorted(v for v,w in total.items() if w < 0)
    pos = sorted(v for v,w in total.items() if w > 0)
    # These bounds are certified from the data; the search has no input length cap.
    assert len(neg) + len(pos) == len(pool)
    ends = []
    for count in range(1,len(neg)+1):
        for negative in combinations(neg,count):
            budget = -sum(total[v] for v in negative)
            max_positive = min(len(pos), budget // min((total[v] for v in pos),default=budget+1))
            for length in range(1,max_positive+1):
                for positive in combinations(pos,length):
                    removed = negative + positive
                    if any(sum(cols[v][k] for v in removed) for k in all_indices):
                        continue
                    final = set(rows[i]) - set(removed)
                    if all(not v or parents[v] in final for v in final):
                        ends.append(tuple(sorted(removed)))
    return allowed, sorted(ends), len(pool)


def run(sources, certificate):
    os.chdir(sources)
    assert hash_blob(FIXTURE.read_bytes()) == PINS[FIXTURE]
    sys.path.insert(0,str(FIXTURE.parent.resolve()))
    import check_geometry_repair as f
    modules = f.modules()
    features, original = f.fixture()
    parents, grades, _ = map(tuple,zip(*features))
    sums = list(grades)
    for v in range(len(parents)-1,0,-1):
        sums[parents[v]] += sums[v]
    squares = [n*n for n in sums]
    a, b = f.A, f.B
    neighbors = f.grid()[b]
    history = json.loads(certificate)
    assert sha256(certificate).hexdigest() == "afa2a993f5a4fabc410df621b9377659fe6d98a1a3993a29990ea25a0abcf19b"
    initial = f.initial_state(features)
    sets = list(map(set,initial))
    counts = Counter(v for row in sets for v in row)
    for i,v in history["preparation"]:
        assert v in sets[i] and counts[v] > 1 and all(parents[u]!=v for u in sets[i])
        sets[i].remove(v)
        counts[v] -= 1
    common = tuple(tuple(sorted(row)) for row in sets)
    assert identity(common) == history["common_rows_digest"]
    out = {}

    def carrier(work):
        exact = tuple(tuple(map(Fraction,row)) for row in work)
        return modules["carriers"].build_carrier(modules["projection"].Payload(
            f.SIDE,Fraction(1),f.LABELS,exact,f.edges(work)[1],()))

    def factor(rows,i,removed):
        target = tuple(tuple(v for v in row if j!=i or v not in removed)
                       for j,row in enumerate(rows))
        event = modules["atom"].factor(parents,rows,target)
        assert modules["verify"].verify_factor(event)
        assert [(d["index"],d["leaf"]) for d in event["steps"]] == [(i,v) for v in sorted(removed,reverse=True)]
        return target

    # Classify A before the choice, so the source needs no minimum-length premise either.
    common_allowed = possible_addresses(parents,common,a)
    external = [j for j in f.LABELS if j != a]
    common_totals = {v:squares[v]*sum(1 if v in common[j] else -1 for j in external)
                     for v in common_allowed}
    negatives = {v:n for v,n in common_totals.items() if n < 0}
    assert negatives == {718:-22,719:-22}
    assert common_totals[f.T] == 56 and f.R not in common_allowed
    assert all(n > 44 or (n in (20,22) and squares[v]==1)
               for v,n in common_totals.items() if v not in negatives)
    single_missing_b = sorted(v for v,n in common_totals.items()
                              if n==22 and v not in common[b])
    assert single_missing_b == [history["source_mate"]]
    allowed, source_pairs, _ = independent_endpoints(parents,squares,common,original,a,f.LABELS,neighbors)
    assert allowed == common_allowed and source_pairs == [(718,1355),(719,1355)]

    for x,y in ((718,719),(719,718)):
        rows = factor(common,a,{x,history["source_mate"]})
        work = f.work_for(rows,squares)
        assert work == original
        holders = [set() for _ in parents]
        for i,row in enumerate(rows):
            for v in row:
                holders[v].add(i)
        per_view = []
        exact = []
        for i in f.LABELS:
            removable = possible_addresses(parents, rows, i)
            cols = {v:{j:squares[v]*(1 if j in holders[v] else -1)
                       for j in f.LABELS if j != i} for v in removable}
            predicted, proof = classify_signed_columns(cols, f.LABELS, neighbors, a,b,i,y)
            peeled, measured, pool = independent_endpoints(parents,squares,rows,work,i,f.LABELS,neighbors)
            assert peeled == removable and measured == predicted
            if i == a:
                assert f.R not in removable and f.CHILD not in removable and not measured
            if i == b:
                assert x not in removable and measured == [(y,1301),(y,1302)]
            for leaves in measured:
                target = factor(rows,i,set(leaves))
                assert f.work_for(target,squares) == original
                assert x in target[b] and y not in target[b]
                exact.append([i,list(leaves),identity(target[i])])
            per_view.append({"editor":i,"removable":len(removable),"removable_sha256":identity(sorted(removable)),
                             "inequality":proof,"pool_after_independent_elimination":pool,
                             "endpoints":[list(m) for m in measured]})
        assert {e[0] for e in exact} == {b}
        assert sum(len(v["endpoints"]) for v in per_view) == 2
        # Perturb only one A-to-j work entry using a legal alternative single-view pair.
        # Test every available unit support of this form and call the true full carrier gate.
        diagnostic = []
        for j in sorted(f.ALL - {a,b}):
            mates = [v for v in rows[a] if v and squares[v]==1 and f.ALL-holders[v]=={b,j}]
            if not mates:
                continue
            v = min(mates)
            trial = tuple(tuple(k for k in row if i!=a or k not in (y,v))
                          for i,row in enumerate(rows))
            assert trial[b] == common[b]
            table = f.work_for(trial,squares)
            changes = [(i,k,table[i][k]-work[i][k]) for i,k in combinations(f.LABELS,2)
                       if table[i][k] != work[i][k]]
            assert changes == [(a,j,-2)]
            try:
                carrier(table)
            except ValueError as exc:
                status = str(exc)
            else:
                status = "accepted"
            diagnostic.append({"j":j,"mate":v,"equivalent_mates":len(mates),"carrier":status})
        first = next((t for t in diagnostic if t["carrier"]=="accepted"),None)
        if first:
            blind = factor(rows,a,{y,first["mate"]})
            assert blind[b] == common[b] and carrier(f.work_for(blind,squares))
        out[str(x)] = {"checks":per_view,"exact":exact,"admission_only":diagnostic,"blind":first}
    assert out["718"]["admission_only"] == out["719"]["admission_only"]
    return {"schema":"all-one-chart-work-returns/1","mutable_editor":"unrestricted",
            "length_bound":None,"source_input_sha256":sha256(certificate).hexdigest(),
            "hist_fixture":PINS[FIXTURE],"arms":out,"common_source":{
                "all_endpoints":source_pairs,"negative_totals":negatives,
                "available_complement_units":single_missing_b,
                "subtotal_two_total":common_totals[f.T]}}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Enable assertions")
    sources, primary, dest = [Path(v).resolve() for v in sys.argv[1:]]
    data = run(sources,primary.read_bytes())
    raw = (json.dumps(data,sort_keys=True,indent=2)+"\n").encode()
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw)
    print(json.dumps({"sha256":sha256(raw).hexdigest(),"bytes":len(raw),
                      "arms":{s:{"exact":v["exact"],"blind":v["blind"]} for s,v in data["arms"].items()}}))
