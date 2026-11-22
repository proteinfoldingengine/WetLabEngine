"""Trace a two-deletion recovery through the inherited work and geometry readers."""
from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import importlib.util
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import sys


U = Path("ResearchHistory/UQCF-GEM")
D = U / "demos"
CORE = D / "v15.42-duality-covariant-transport-repair"
APP = D / "v15.43-certified-response-geometry"
ATOM = D / "v16.26-consistency-increment-law"
WORK = D / "v15.40-global-balance-geometry-specificity/response_geometry.py"
PINS = {
    CORE / "exact_algebra.py": "c67ea42b61321469f7735ce589f2e729b241666a",
    CORE / "operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    CORE / "protocol_types.py": "e90a98d17baa6028f0d50a165f0b9d0046de13a2",
    CORE / "transport.py": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
    CORE / "holonomy.py": "bad3f06b291bb448a903b4f48344a9e54a633f68",
    APP / "projection.py": "f857f2cf1cd4c265c193121236af8e441b1f01dc",
    APP / "carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    APP / "application.py": "30348d71d366a751932ec2d58d18a9148d81ae83",
    U / "foundational-closure-verification/lineage.py": "e95e3e978779164dd91f09b80e3389247e6320c2",
    ATOM / "engine.py": "c10ac57f988a439144e21898bd2b33ece0838a9b",
    ATOM / "verify.py": "91cd1e507e955683e744fbdbb0745cac19d66cb3",
    WORK: "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
}
SIDE = 5
LABELS = tuple(range(25))
ALL = frozenset(LABELS)
A, B = 0, 12
T, ULEAF, R, CHILD, B_PRIVATE = 1, 2, 3, 4, 5
FACE = (3, 4, 9, 8)
MU = 1984


def numbered(x, y):
    return x % SIDE + SIDE * (y % SIDE)


def offset(i, dx, dy):
    return numbered(i % SIDE + dx, i // SIDE + dy)


def grid():
    return {i: {offset(i,*d) for d in ((1,0),(-1,0),(0,1),(0,-1))} for i in LABELS}


def opposite(i, j):
    return i != j and any(offset(i,*d) == j for d in ((2,0),(-2,0),(0,2),(0,-2)))


def modules():
    for path, expected in PINS.items():
        raw = path.read_bytes()
        assert hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest() == expected, path
    sys.path[:0] = [str(APP.resolve()), str(CORE.resolve())]
    result = {n:importlib.import_module(n) for n in ("carriers","projection","application")}
    for label,path in (("lineage", U/"foundational-closure-verification/lineage.py"),
                       ("atom",ATOM/"engine.py"), ("verify",ATOM/"verify.py"), ("work",WORK)):
        spec = importlib.util.spec_from_file_location(label,path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[label] = module
        spec.loader.exec_module(module)
        result[label] = module
    return result


def fixture():
    neighbors = grid()
    others = ALL-{A,B}
    contains_t = {i:i not in neighbors[B] for i in others}

    def lower(j):
        if j in neighbors[A] or j in neighbors[B]:
            return 0
        return 20 if opposite(A,j) or opposite(B,j) else 8

    def mixed(i,j):
        return lower(j) + 4 * ((not contains_t[j]) if i == A else contains_t[j])

    def target(i,j):
        if {i,j} == {A,B}:
            return 14
        if i in (A,B):
            return mixed(i,j)
        if j in (A,B):
            return mixed(j,i)
        if j in neighbors[i]:
            return 0
        if opposite(i,j):
            (center,) = neighbors[i]&neighbors[j]
            cross = neighbors[center]-{i,j}
            root = cross&{A,B}
            if root:
                (special,) = root
                (partner,) = cross-{special}
                return mixed(special,partner)
            return 20
        return 8

    # Each entry describes the ambient parent, grade and initial indexed support.
    t = frozenset({A}|{j for j in others if contains_t[j]})
    u = frozenset({B}|{j for j in others if not contains_t[j]})
    r = frozenset({A}|{j for j in others if not contains_t[j]})
    features = [(-1,1,ALL), (0,2,t), (0,2,u), (0,1,r), (R,1,frozenset({A})), (0,1,frozenset({B}))]

    def substrate(i,j):
        if {i,j} == {A,B}:
            return 0
        if i in (A,B):
            return lower(j)-5
        if j in (A,B):
            return lower(i)-5
        return target(i,j)-12*(contains_t[i]!=contains_t[j])

    def parity(i):
        return int(i in (A,B))

    pairs = {}
    singleton = dict.fromkeys(LABELS, 1024)
    for i,j in combinations(LABELS,2):
        base = substrate(i,j)-parity(i)-parity(j)
        assert base % 2 == 0
        pairs[i,j] = 32-base//2
        singleton[i] -= pairs[i,j]
        singleton[j] -= pairs[i,j]

    def add_cut(cut, weight):
        assert weight > 0
        while weight:
            grade = isqrt(weight)
            if grade == 2:
                grade = 1
            features.append((0,grade,ALL-set(cut)))
            weight -= grade**2

    for pair, weight in pairs.items():
        add_cut(pair,weight)
    for i, weight in singleton.items():
        add_cut((i,),weight+parity(i))
    assert all(feature[1] != 2 for feature in features[6:])
    expected = tuple(tuple(0 if i==j else MU+target(i,j) for j in LABELS) for i in LABELS)
    return features,expected


def initial_state(features):
    return tuple(tuple(v for v,entry in enumerate(features) if i in entry[2]) for i in LABELS)


def work_for(state, squares):
    sets = [set(row) for row in state]
    return tuple(tuple(sum(squares[v] for v in a^b) for b in sets) for a in sets)


def edges(work):
    minimum = min(work[i][j] for i,j in combinations(LABELS,2))
    return minimum, tuple((i,j) for i,j in combinations(LABELS,2) if work[i][j]==minimum)


def degree_candidates(features, after, work, squares):
    """Exhaust the exact degree gate by row updates on every legal deletion."""
    supports = Counter(v for row in after for v in row)
    minimum, minimum_edges = edges(work)
    assert minimum == MU
    degrees = Counter(i for edge in minimum_edges for i in edge)
    members = set(minimum_edges)
    candidates, counts = [],Counter()
    state_sets = [set(s) for s in after]
    for i,row in enumerate(after):
        active_parents = {features[v][0] for v in row}
        for v in row:
            if v == 0 or v in active_parents or supports[v] < 2:
                continue
            counts[i] += 1
            changed = [work[i][j]+squares[v]*(1 if v in state_sets[j] else -1)
                       for j in LABELS if j!=i]
            # An untouched MU edge exists after each possible second deletion.
            assert any(i not in edge for edge in minimum_edges)
            if min(changed)<MU:
                continue
            new_degrees = degrees.copy()
            for j,value in zip((j for j in LABELS if i!=j),changed, strict=True):
                edge = (min(i,j),max(i,j))
                difference = int(value==MU)-int(edge in members)
                new_degrees[i] += difference
                new_degrees[j] += difference
            if all(new_degrees[j] == 4 for j in LABELS):
                candidates.append((i,v))
    return counts,candidates


def run(destination):
    m = modules()
    features,target = fixture()
    parents, grades, _ = map(tuple,zip(*features))
    subtotal = list(grades)
    for v in range(len(features)-1,0,-1):
        subtotal[parents[v]] += subtotal[v]
    squares = [x**2 for x in subtotal]
    initial = initial_state(features)

    def delete(state,i,v):
        event = m["atom"].atomic(parents,state,i,v)
        m["verify"].verify_atomic(event)
        after = tuple(map(tuple,event["after"]))
        expected = tuple(tuple(a for a in row if not (j==i and a==v)) for j,row in enumerate(state))
        assert after==expected
        return after, {key:val for key,val in event.items() if key not in ("parents","before","after")}

    after, source = delete(initial,A,T)
    work0 = work_for(initial,squares)
    assert work0 == target
    work1 = work_for(after,squares)
    count,candidates = degree_candidates(features,after,work1,squares)
    column_counts = Counter()
    for vertex, (_, _, support) in enumerate(features):
        if vertex == 0:
            continue
        holders = support - {A} if vertex == T else support
        if len(holders) >= 2:
            column_counts.update(holders - {A} if vertex == R else holders)
    assert column_counts == count and sum(count.values()) == 32575
    assert candidates == [(B,ULEAF)], candidates
    repaired, recipient = delete(after,*candidates[0])
    work2 = work_for(repaired,squares)
    for state,work in zip((initial,after,repaired),(work0,work1,work2),strict=True):
        coordinates = tuple(tuple(subtotal[v] if v in members else 0 for v in range(1,len(features)))
                            for members in map(set,state))
        # Edge divergence and edge difference form dual coordinates for the inherited work.
        constructed = m["work"].construct_response_geometry(LABELS,coordinates,coordinates)
        assert constructed.work == work and m["work"].metric_passes(constructed)

    keys = [()]
    for v in range(1,len(features)):
        keys.append(keys[parents[v]] + (v,))
    lin = m["lineage"]
    fine = lin.Carrier("recovery-test",tuple(keys))
    def retained_view(vertices):
        return lin.Carrier(fine.genesis,tuple(keys[v] for v in vertices))

    coarse0,coarse1 = retained_view(after[B]),retained_view(repaired[B])
    retained0 = lin.Pruning(fine,coarse0).aggregate(grades)
    retained1 = lin.Pruning(coarse0,coarse1).aggregate(retained0)
    assert retained1 == lin.Pruning(fine,coarse1).aggregate(grades)
    assert retained1[0]-retained0[0] == 2

    def observe(work):
        _, near = edges(work)
        exact = tuple(tuple(map(Fraction,row)) for row in work)
        p = m["projection"].Payload(SIDE,Fraction(1),LABELS,exact,near,())
        return m["carriers"].build_carrier(p)

    def must_reject(work):
        try:
            observe(work)
        except ValueError as exc:
            assert str(exc) == "degree_not_four"
        else:
            raise AssertionError("degree-four rejection expected")

    base = observe(work0)
    must_reject(work1)
    control_site = next(v for v in after[A] if v > B_PRIVATE)
    control, source_only = delete(after,A,control_site)
    assert control[B] == after[B]
    must_reject(work_for(control,squares))
    for denied_site, reason in ((R, "non-leaf"),(CHILD, "same union")):
        try:
            m["atom"].atomic(parents,after,A,denied_site)
        except ValueError as exc:
            assert str(exc) == reason
        else:
            raise AssertionError("forbidden deletion accepted")
    post = observe(work2)
    swap = {A:B,B:A}
    initial_graph = set(edges(work0)[1])
    assert set(edges(work2)[1]) == {tuple(sorted(swap.get(v,v) for v in edge)) for edge in initial_graph}
    assert ({k:post.complex.work[A][k] for k in ALL-{A,B}}
            == {k:base.complex.work[B][k] for k in ALL-{A,B}})
    field = tuple(Fraction(i==A)-Fraction(1,len(LABELS)) for i in LABELS)
    loops = []
    for carrier in (base,post):
        values = m["application"].evaluate_field(carrier,field)
        loops.append(next(v for face,_,v in values.records if set(face)==set(FACE)))
    def gauge_invariant(values):
        def derivative(i, dx, dy):
            return (values[offset(i, dx, dy)] - values[offset(i, -dx, -dy)]) / 2
        a, b, c, d = FACE
        gx = lambda i: derivative(i,1,0)
        gy = lambda i: derivative(i,0,1)
        curl = (gy(a)+gy(b)-gx(b)-gx(c)-gy(c)-gy(d)+gx(d)+gx(a))/4
        return curl**2

    assert loops == [gauge_invariant(field),gauge_invariant(tuple(field[swap.get(i,i)] for i in LABELS))]
    assert loops == [Fraction(1,64),0], loops
    for carrier in (base,post):
        flat = m["application"].evaluate_field(carrier,(Fraction(0),)*len(LABELS))
        assert flat.nonzero_count == 0
    report = {"fixture": features, "source":source, "receiver":recipient,
              "legal_next_deletions_by_index":dict(count),"degree_eligible_repair":candidates,
              "source_only_rejected":source_only,"constant_field_nonzero_loops":[0,0],
              "before_edges":edges(work0)[1],"source_edges":edges(work1)[1],"repair_edges":edges(work2)[1],
              "geometry_face":list(FACE),"invariant":[str(v) for v in loops],
              "work_tables":[work0,work1,work2],"B_root_grade":[str(retained0[0]),str(retained1[0])]}
    report["fixture"] = [(p,g,sorted(s)) for p,g,s in report["fixture"]]
    destination.mkdir(parents=True,exist_ok=True)
    raw = (json.dumps(report,sort_keys=True,indent=2)+"\n").encode()
    (destination/"geometry_repair_certificate.json").write_bytes(raw)
    return {"certificate_sha256":hashlib.sha256(raw).hexdigest(),"vertices":len(features),
            "legal_next_deletions":sum(count.values()),"choice":candidates, "face_invariant":report["invariant"],
            "receiver_root_grade":report["B_root_grade"]}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])),sort_keys=True,indent=2))
