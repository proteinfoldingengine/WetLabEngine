"""Reproduce the original routed edits and their unique compatible grade presentations."""
import gzip
import hashlib
import itertools
import lzma
import json
import sys
from fractions import Fraction

import sympy as sp

import check_routed_chain as chain


X = chain.X
P = chain.P
B, C = 1, 2
PARENT, LEAF = 1, 7
UNIFORM = (1,) * len(X)
GROUND = (2,) * len(X)
SHIFTED = tuple(2 + int(v == LEAF) - int(v == PARENT) for v in X)
GRADES = {"unit": UNIFORM, "ground": GROUND, "shifted": SHIFTED}


def ancestor_sets(parents):
    sets = []
    for i in range(len(parents)):
        lineage = set()
        while i >= 0:
            lineage.add(i)
            i = parents[i]
        sets.append(lineage)
    return sets


ANCESTORS = ancestor_sets(P)


def independent_grade(carrier, source):
    """Use subtree-coordinate restriction and inversion, not retraction fibers."""
    c = {v: sum(g for i, g in enumerate(source) if v in ANCESTORS[i]) for v in carrier}
    return tuple(c[v] - sum(c[w] for w in carrier if P[w] == v) for v in carrier)


def initial(sources, masks, ambient):
    return tuple(sources.push(P, X, chain.view(mask), ambient) for mask in masks)


def family_on(sources, masks, values):
    return sources.glue_many(P, list(map(chain.view, masks)), values)


def overlap_checks(sources, views, grades):
    for left, right in itertools.combinations(range(len(views)), 2):
        common = tuple(sorted(set(views[left]) & set(views[right])))
        assert sources.push(P, views[left], common, grades[left]) == sources.push(P, views[right], common, grades[right])


def extend(sources, old, new, old_grade, holder, holder_grade):
    intersection = tuple(sorted(set(new) & set(holder)))
    assert tuple(sorted(set(old) | set(intersection))) == new
    common_grade = sources.push(P, holder, intersection, holder_grade)
    return sources.glue(P, old, intersection, old_grade, common_grade)


def edit(sources, old, new, grades):
    (actor,) = [i for i, (left, right) in enumerate(zip(old, new)) if left != right]
    bit = old[actor] ^ new[actor]
    assert bit > 1 and bit.bit_count() == 1
    site = bit.bit_length() - 1
    old_views, new_views = list(map(chain.view, old)), list(map(chain.view, new))
    assert set.union(*map(set, old_views)) == set.union(*map(set, new_views)) == set(X)
    y, z = old_views[actor], new_views[actor]
    if site in z:
        extensions = [extend(sources, y, z, grades[actor], view, grade)
                      for i, (view, grade) in enumerate(zip(old_views, grades)) if i != actor and site in view]
        assert extensions and all(value == extensions[0] for value in extensions)
        replacement = extensions[0]
        assert sources.push(P, z, y, replacement) == grades[actor]
    else:
        replacement = sources.push(P, y, z, grades[actor])
    output = list(grades)
    output[actor] = replacement
    overlap_checks(sources, new_views, output)
    return tuple(output)


def traverse(sources, full, ambient):
    live = initial(sources, full[0], ambient)
    overlap_checks(sources, list(map(chain.view, full[0])), live)
    all_grades = [live]
    for old, new in zip(full, full[1:]):
        live = edit(sources, old, new, live)
        all_grades.append(live)
    for masks, grades in zip(full, all_grades):
        assert tuple(independent_grade(chain.view(m), ambient) for m in masks) == grades
        assert family_on(sources, masks, grades) == ambient
    return all_grades


def original_paths(machine, atom, verifier):
    raw = (chain.DEMOS / chain.ARCHIVE).read_bytes()
    entry = json.loads(gzip.decompress(raw))["entries"][1]
    graph = entry["graph"]
    states = graph["states"]
    assert graph["parents"] == list(P) and states[14730] == chain.PREP
    results, events = {}, {}
    for name, actor, state_id, record_id in (
            ("delete_A", 0, 8, 2), ("delete_C", 2, 14725, 33), ("no_deletion", None, 14730, None)):
        views = list(map(chain.view, chain.PREP))
        if actor is not None:
            events[name] = atom.atomic(P, views, actor, 8)
            verifier.verify_atomic(events[name])
            views = events[name]["after"]
        start = [sum(1 << v for v in view) for view in views]
        assert start == states[state_id]
        profile = graph["attained_profiles"][graph["profile_ids"][state_id]]
        assert profile == [atom.tau_at(P, views, v) for v in X]
        path, _ = chain.trace_normalize(machine, start, profile)
        if record_id is not None:
            archived = entry["normalizations"][record_id]
            assert archived["state"] == state_id and archived["q"] == profile
            assert path == [states[i] for i in archived["path"]]
        results[name] = path if actor is None else [chain.PREP] + path
    low, high = results["delete_A"], results["delete_C"]
    embedded = atom.atomic(P, list(map(chain.view, low[2])), 2, 8)
    verifier.verify_atomic(embedded)
    assert embedded == events["delete_C"] and low[3] == high[1] and low[2] == high[0]
    assert low[4] == [259,63,199] and high[2] == [257,191,199]
    return results, embedded


def response(green, sources, Y, g):
    total = sum(g)
    j = (g[0] - total,) + tuple(g[1:])
    local = sources.push(P, X, Y, j)
    parents = tuple(-1 if v == 0 else Y.index(P[v]) for v in Y)
    phi = green.candidate(parents) * sp.Matrix(len(Y) - 1, 1, list(local[1:]))
    laplacian = green.root_laplacian(parents)
    assert tuple(laplacian * phi) == tuple(local[1:])
    return dict(zip(Y, (0,) + chain.exact(phi))), int((laplacian * phi)[Y.index(PARENT) - 1])


def rejected_controls(sources, high):
    old, new = high[1:3]
    old_views, new_views = list(map(chain.view, old)), list(map(chain.view, new))
    B0, B1, C0 = old_views[B], new_views[B], old_views[C]
    shared = tuple(sorted(set(B1) & set(C0)))
    assert B1 == tuple(sorted(set(B0) | {LEAF})) and new_views[C] == C0
    for g, agrees in ((UNIFORM, False), (tuple(int(v == PARENT) for v in X), True)):
        bs, cs = (sources.push(P, X, y, g) for y in (B0, C0))
        by_vertex = dict(zip(B0, bs))
        zero_extension = tuple(by_vertex.get(v, 0) for v in B1)
        old_projection = sources.push(P, B1, B0, zero_extension)
        assert old_projection == bs
        assert (sources.push(P, B1, shared, zero_extension) == sources.push(P, C0, shared, cs)) == agrees
    original_family, muted_family = initial(sources, old, SHIFTED), initial(sources, new, GROUND)
    for i, (former, latter) in enumerate(zip(original_family, muted_family)):
        present = tuple(sorted(set(old_views[i]) - {LEAF}))
        assert sources.push(P, old_views[i], present, former) == sources.push(P, new_views[i], present, latter)
    assert original_family[C] != muted_family[C]
    assert sources.push(P, B1, B0, muted_family[B]) == original_family[B]
    overlap_checks(sources, new_views, muted_family)
    assert family_on(sources, new, muted_family) == GROUND

    small = (-1,0,1,1)
    supports = (0,1,2), (0,1,3)
    positive_marginal = (0,0,1)
    signed = sources.glue(small, *supports, positive_marginal, positive_marginal)
    assert signed == (0,-1,1,1)
    try:
        sources.glue(small, *supports, positive_marginal, positive_marginal, positive=True)
    except ValueError as exception:
        assert str(exception) == "no nonnegative global source"
    else:
        raise AssertionError("Incompatible nonnegative extension was accepted")
    return {"zero_extension_at_positive_leaf": "REJECTED_BY_OVERLAP",
            "zero_extension_at_zero_leaf": "ACCEPTED",
            "letting_C_change_preserves_old_B_but_can_erase_the_contrast": True,
            "only_signed_extension_in_fork_control": chain.exact(signed)}


def historical_fixed_chart(sources, paths):
    """Check archived FCV output on the rooted chart K={o,v1,v2,v7}."""
    root = chain.DEMOS.parent / "foundational-closure-verification"
    pins = {"lineage.py":"e95e3e978779164dd91f09b80e3389247e6320c2",
            "evidence/certificates.json.xz":"5ef9b521fa65b715c3583923857f952900b75ba0"}
    for path, pin in pins.items():
        data = (root / path).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest() == pin
    sys.path.insert(0,str(root))
    from lineage import Carrier, Pruning

    plain = lzma.decompress((root / "evidence/certificates.json.xz").read_bytes())
    assert hashlib.sha256(plain).hexdigest() == "21357bdc79429f9d4214024b125e75693609a2538a08a57037978b191ab432c6"
    example = json.loads(plain)["instances"][7]
    tag = "U1:((()()))"
    keys = ((), (0,), (0,0), (0,1))
    assert example["tag"] == tag and example["keys"] == list(map(list, keys))
    chart = (0,1,2,7)
    fine = Carrier(tag, keys)
    both = []
    g = (Fraction(1,4), Fraction(2,3), Fraction(3,20), Fraction(3,20), Fraction(3,20),
         Fraction(3,20), Fraction(3,20), Fraction(4,5), Fraction(1,4))
    assert sources.push(P, X, chart, g) == tuple(map(Fraction, ("1/2","2/3","3/4","4/5")))
    low = paths["delete_A"][-1]
    high = paths["delete_C"][-1]
    for ordinal, keep_mask, actual in ((11,7,low[B]), (13,15,high[B])):
        row = example["prunings"][ordinal]
        assert (row["src"],row["dst"]) == (15,keep_mask)
        kept_keys = tuple(k for i,k in enumerate(keys) if keep_mask & (1 << i))
        retained = tuple(v for i,v in enumerate(chart) if keep_mask & (1 << i))
        current_B = chain.view(actual)
        assert retained == tuple(v for v in chart if v in current_B)
        returned = Pruning(fine, Carrier(tag, kept_keys)).aggregate(tuple(map(Fraction, row["fiber_input"])))
        assert list(map(str, returned)) == row["fiber_output"]
        assert returned == sources.push(P, X, retained, g)
        assert returned[1] == sources.push(P, X, current_B, g)[1]
        both.append({"archive_pruning":ordinal, "inputs":row["fiber_input"], "outputs":row["fiber_output"]})
    assert [r["outputs"][1] for r in both] == ["22/15","2/3"]
    return {"projected_chart":chart,"FCV_archive_instance":7,"FCV_pruning_rows":both,
            "junction_contrast_high_minus_low":"-4/5",
            "historical_topology_match_is_separate_from_routing_invocation":True}


def main():
    for path, pin in chain.PINS.items():
        raw = (chain.DEMOS/path).read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest() == pin
    sys.path.insert(0, str(chain.DEMOS / chain.OLD))
    machine = chain.module(chain.OLD+"producer.py", "replayed_grade_route")
    atom = chain.module(chain.ATOM+"engine.py", "grade_source_atom")
    verifier = chain.module(chain.ATOM+"verify.py", "grade_source_check")
    sources = chain.module("v16.23-overlap-descent/engine.py", "inherited_grade_overlap")
    green = chain.module("v16.22-response-selection-closure/engine.py", "inherited_grade_green")
    paths, embedded = original_paths(machine, atom, verifier)
    checked = 0
    traces, families = {}, {}
    for arm, path in paths.items():
        for vertex in X:
            traverse(sources, path, tuple(int(i == vertex) for i in X))
            checked += len(path)
        rows = {kind: traverse(sources, path, ambient) for kind, ambient in GRADES.items()}
        families[arm] = rows
        visible = []
        trace = []
        for step, state in enumerate(path):
            Y = chain.view(state[B])
            has_leaf = LEAF in Y
            carriers = [i for i, (u, v) in enumerate(zip(rows["ground"][step], rows["shifted"][step])) if u != v]
            assert carriers == [i for i, mask in enumerate(state) if mask & 1 << LEAF]
            visible.append("".join("ABC"[i] for i in carriers))
            coordinates = {}
            for key, ambient in GRADES.items():
                by_vertex = dict(zip(Y, rows[key][step][B]))
                phi, div = response(green, sources, Y, ambient)
                assert div == by_vertex[PARENT]
                if key == "unit":
                    assert [phi[1]-phi[0], phi[2]-phi[1]] == [7,5]
                    if has_leaf:
                        assert phi[LEAF]-phi[PARENT] == 1
                coordinates[key] = [int(by_vertex[PARENT]), int(by_vertex[LEAF]) if has_leaf else None]
            assert coordinates["unit"] == ([1,1] if has_leaf else [2,None])
            assert coordinates["ground"] == ([2,2] if has_leaf else [4,None])
            assert coordinates["shifted"] == ([1,3] if has_leaf else [4,None])
            trace.append({"masks":state,"B_at_v1_and_v7":coordinates,"contrast_holders":visible[-1]})
        assert visible[0] == "C" and visible[-1] == ("B" if arm == "delete_C" else "A")
        if arm == "delete_C":
            assert visible[1:4] == ["C","BC","B"]
            assert all(state[B] & (1 << LEAF) for state in path[2:])
        traces[arm] = trace
    assert checked == 306
    for key in GRADES:
        low, high = families["delete_A"][key], families["delete_C"][key]
        assert low[2:4] == high[:2]
    print(json.dumps({"original_paths":traces, "basis_family_states_checked":checked,
                      "same_embedded_and_high_source_record":embedded,
                      "different_next_writes_from_same_incidence_and_grades":{"continuing_low":"+A(v1)","fresh_high":"+B(v7)"},
                      "fixed_common_B_edges_unit_drop":{"o_to_v1":7,"v1_to_v2":5},
                      "rejecting_controls":rejected_controls(sources, paths["delete_C"]),
                      "separately_executed_historical_FCV_prunings":historical_fixed_chart(sources, paths),
                      "scope":"Compatible grade presentations on an unchanged rooted union. Native physical activation and access open."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
