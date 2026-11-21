"""Reproduce the fixed C, free A overlap bounds and the original event-selection controls."""

import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path

from replay_original_atomic import NAMES, PARENTS, load_archived, permitted
from replay_root_trigger import views_for

BASE = Path(__file__).resolve().parents[3] / "demos"
FULL = tuple(range(len(PARENTS)))
TREE = (((), ()), ())
TARGET = [1, 2]
SOURCES = {
    "overlap": ("v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"),
    "counting": ("v16.24-consistency-order/engine.py", "666617d33bf8925699d0dc440565588a5e40e57e"),
    "refine": ("v16.25-pruning-refinement-closure/engine.py", "e9c576a2590c8e16812f1b3fa0436111e3648f1c"),
    "norm": ("v16.50-recursive-binary-composition/producer.py", "44eb38cc3dff9d121fc634cd38c597acfc3f04c6"),
    "norm_check": ("v16.50-recursive-binary-composition/verifier.py", "970bd7fbecb0d7d2fc488f2e30ba32065d76328e"),
}


def archived_source(key):
    path, expected = SOURCES[key]
    file = BASE / path
    data = file.read_bytes()
    header = b"blob " + str(len(data)).encode() + b"\0"
    assert hashlib.sha1(header + data).hexdigest() == expected, file
    spec = importlib.util.spec_from_file_location("archived_" + key, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first, *rest)


def source_views():
    engine = load_archived("engine", "c10ac57f988a439144e21898bd2b33ece0838a9b")
    verifier = load_archived("verify", "91cd1e507e955683e744fbdbb0745cac19d66cb3")
    initial = views_for("A")
    first = permitted(engine, verifier, initial)
    assert set(first) == {("A", "l"), ("B", "l")}
    mids, endpoints = {}, {}
    for (label, _), rec in first.items():
        middle = rec["after"]
        final = permitted(engine, verifier, middle)
        assert set(final) == {(label, "p")}
        endpoint = final[label, "p"]["after"]
        assert endpoint[2] == initial[2] == middle[2] == [0, 1, 3]
        mids[label], endpoints[label] = middle, endpoint
    assert endpoints["A"][0] == [0, 4] and endpoints["B"][0] == [0, 1, 2, 4]
    return initial, mids, endpoints


def project(overlap, counting, views, source):
    local = [counting.push(PARENTS, view, source) for view in views]
    assert local == [overlap.push(PARENTS, FULL, view, source) for view in views]
    return local


def integer_fiber(overlap, counting, endpoints, marginal):
    total = sum(marginal)
    outputs = {label: set() for label in endpoints}
    whole = []
    n_checked = 0
    for source in compositions(total, len(PARENTS)):
        n_checked += 1
        if counting.push(PARENTS, endpoints["A"][2], source) != marginal:
            continue
        whole.append(source)
        for label, views in endpoints.items():
            local = project(overlap, counting, views, source)
            assert overlap.glue_many(PARENTS, views, local, positive=True) == source
            union = sorted(set(views[0]) | set(views[2]))
            joint = overlap.glue(PARENTS, views[0], views[2], local[0], local[2], positive=True)
            assert joint == overlap.push(PARENTS, FULL, union, source)
            outputs[label].add(int(local[0][0]))
    b, u, v = marginal
    expected = {(s, t, u-t, v, b-s) for s in range(b+1) for t in range(u+1)}
    assert set(whole) == expected
    assert outputs["A"] == set(range(u+v, total+1))
    assert outputs["B"] == set(range(b+1))
    return {"assignments_screened": n_checked, "admitted_full_sources": whole,
            "possible_A_root": {i: sorted(s) for i, s in outputs.items()}}


def endpoint_controls(overlap, counting, endpoints):
    order = ["A", "B"]
    touch = [(0, 1, 0, 1, 2), (2, 1, 0, 1, 0)]
    for label, source in zip(order, touch):
        views = endpoints[label]
        local = project(overlap, counting, views, source)
        assert local[0][0] == 2 and local[2] == (2, 1, 1)
        assert overlap.glue_many(PARENTS, views, local, positive=True) == source
    # Rational interior points prevent reading the integer sweep as an interval proof.
    for label, a in [("A", Fraction(7, 2)), ("B", Fraction(3, 2))]:
        source = (a-3, 2, 0, 1, 5-a) if label == "A" else (a, 2, 0, 1, 2-a)
        views = endpoints[label]
        local = project(overlap, counting, views, source)
        assert local[0][0] == a and local[2] == (2, 2, 1)
        assert overlap.glue_many(PARENTS, views, local, positive=True) == source
    views = endpoints["A"]
    local = [(0, 5), (2, 2, 1), (2, 2, 1)]
    signed = overlap.glue_many(PARENTS, views, local)
    assert signed == (-3, 1, 1, 1, 5)
    for y, x in zip(views, local):
        assert overlap.push(PARENTS, FULL, y, signed) == x
    try:
        overlap.glue(PARENTS, views[0], views[2], local[0], local[2], positive=True)
    except ValueError as exc:
        assert str(exc) == "no nonnegative global source"
    else:
        raise AssertionError("Accepted incompatible nonnegative lift")
    return {"four_unit_touch_sources": touch, "common_A_root_at_touch": 2,
            "rational_interior_A_root": ["7/2", "3/2"], "local_only_vectors": local,
            "signed_union": [int(x) for x in signed], "positive_lift_rejected": True}


def normalizer_control(mids, endpoints):
    refine = archived_source("refine")
    norm = archived_source("norm")
    verifier = archived_source("norm_check")
    records = {}
    for label, views in mids.items():
        family = tuple(map(tuple, views))
        alternatives = set(refine.refinements(PARENTS, family))
        assert alternatives == {family, tuple(map(tuple, endpoints[label]))}
        before = [sum(1 << v for v in view) for view in views]
        path = norm.normalize(before, TREE, 3, TARGET)
        canonical = norm.canonical(TREE, 3, TARGET)
        assert verifier.path_check(TREE, 3, TARGET, path, before, canonical) == [0, 0, 0]
        assert all(verifier.profile_check(TREE, 3, row) == TARGET for row in path)
        moves = []
        for left, right in itertools.pairwise(path):
            [(i, v)] = [(i, v) for i in range(3) for v in FULL if (left[i] ^ right[i]) & (1 << v)]
            sign = "+" if right[i] & (1 << v) else "-"
            moves.append(f"{sign}{'ABC'[i]}({NAMES[v]})")
        assert moves[:2] == ["+B(d)", "+C(d)"] and f"-{label}(p)" not in moves
        assert len(moves) == {"A": 9, "B": 7}[label]
        records[label] = {"edits": moves, "endpoint_columns": path[-1], "refinement_options": len(alternatives)}
    assert records["A"]["endpoint_columns"] == records["B"]["endpoint_columns"] == [23, 11, 1]
    return records


def main():
    ov, ct = archived_source("overlap"), archived_source("counting")
    initial, mids, endpoints = source_views()
    ones = (1,) * 5
    initial_local = project(ov, ct, initial, ones)
    assert initial_local[0][0] == 1 and initial_local[2] == (2, 2, 1)
    exact_counting = {}
    for label in ("A", "B"):
        early = project(ov, ct, mids[label], ones)
        final = project(ov, ct, endpoints[label], ones)
        exact_counting[label] = [int(x) for x in (initial_local[0][0], early[0][0], final[0][0])]
    assert exact_counting == {"A": [1, 1, 4], "B": [1, 1, 1]}
    before_ranges = {}
    for stage, views in {"initial": initial, "after_A_leaf": mids["A"], "after_B_leaf": mids["B"]}.items():
        possible = {int(ct.push(PARENTS, views[0], source)[0])
                    for source in compositions(5, 5) if ct.push(PARENTS, views[2], source) == (2, 2, 1)}
        assert possible == {0, 1, 2}
        before_ranges[stage] = sorted(possible)
    result = {"pre_parent_integer_ranges": before_ranges, "fixed_C_marginal": [2, 2, 1], "ordered_full_vertices": list(NAMES),
              "integer_fiber": integer_fiber(ov, ct, endpoints, (2, 2, 1)),
              "equal_mass_fiber": integer_fiber(ov, ct, endpoints, (2, 1, 1)),
              "zero_mass_fiber": integer_fiber(ov, ct, endpoints, (0, 0, 0)),
              "canonical_counting_A_root": exact_counting,
              "controls": endpoint_controls(ov, ct, endpoints),
              "original_path_selectors": normalizer_control(mids, endpoints),
              "physical_event_and_A_grade_access": "OPEN"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
