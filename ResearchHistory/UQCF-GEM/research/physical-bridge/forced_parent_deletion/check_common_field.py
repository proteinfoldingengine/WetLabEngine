"""Exact Green responses and the historical O4 extension test on the anchored episode."""
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction

import sympy as sp

from check_passive_view import BASE, compositions, source_views, archived_source
from replay_original_atomic import NAMES, PARENTS


FULL = tuple(range(len(PARENTS)))
C = (0, 1, 3)


def load_green():
    file = BASE / "v16.22-response-selection-closure" / "engine.py"
    raw = file.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == "9b71ce47bbef83132f00270f8a9a19e7721864d6"
    spec = importlib.util.spec_from_file_location("archived_green", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def response(green, view, current):
    """Solve in the pinned root-zero potential coordinates."""
    assert sum(current) == 0 and len(view) == len(current)
    parents = (-1, *(view.index(PARENTS[v]) for v in view[1:]))
    laplacian = green.root_laplacian(parents)
    inverse = green.candidate(parents)
    assert laplacian * inverse == sp.eye(len(view) - 1)
    result = inverse * sp.Matrix(current[1:])
    return (0, *result)


def graded_field(green, overlap, view, source):
    x = overlap.push(PARENTS, FULL, view, source)
    return response(green, view, (x[0] - sum(x), *x[1:]))


def add(x, y):
    assert len(x) == len(y)
    return tuple(a + b for a, b in zip(x, y))


def gluable(overlap, a, phi_a, phi_c):
    try:
        union = overlap.glue_response(PARENTS, a, C, tuple(map(str, phi_a)), tuple(map(str, phi_c)))
    except ValueError as exc:
        if exc.args != ("incompatible response classes",):
            raise
        return False
    sites = sorted(set(a) | set(C))
    for view, potential in ((a, phi_a), (C, phi_c)):
        assert all(union[sites.index(v)] == val - potential[0] for v, val in zip(view, potential))
    return True


def clamped_modes(green, overlap, views):
    a = tuple(views[0])
    assert tuple(views[2]) == C
    j = tuple(sorted(set(a) & set(C)))
    _, _, restriction, _ = overlap.maps(PARENTS, C, j)
    _, _, _, extend_a = overlap.maps(PARENTS, a, j)
    coupling = int(1 in j)
    rank_free = len(C) - 1 - restriction.rank()
    assert rank_free == 2 - coupling
    baseline = (1,) * len(FULL)
    phi_a = graded_field(green, overlap, a, baseline)
    phi_c = graded_field(green, overlap, C, baseline)
    assert phi_c == (0, 3, 4) and gluable(overlap, a, phi_a, phi_c)
    assert gluable(overlap, a, (0,) * len(a), (0,) * len(C))
    grid_pass = free_pass = 0
    controls = {}
    for first, second in itertools.product((-1, 0, 1), repeat=2):
        current = (-first, first - second, second)
        delta = response(green, C, current)
        assert delta == (0, first, first + second)
        projected = overlap.push(PARENTS, C, j, current)
        clamped = gluable(overlap, a, phi_a, add(phi_c, delta))
        assert clamped == (all(x == 0 for x in projected)) == (coupling * first == 0)
        assert gluable(overlap, a, (0,) * len(a), delta) == clamped
        assert gluable(overlap, a, tuple(v + 7 for v in phi_a),
                       tuple(v - 4 for v in add(phi_c, delta))) == clamped
        paired = (0, *(extend_a * restriction * sp.Matrix(delta[1:])))
        assert gluable(overlap, a, add(phi_a, paired), add(phi_c, delta))
        grid_pass += int(clamped)
        free_pass += 1
        if (first, second) in ((1, 0), (0, 1)):
            key = "op_trial" if first else "pw_control"
            controls[key] = {"clamped": clamped, "C_current": list(current),
                             "C_increment": list(map(int, delta)), "free_A_increment": list(map(int, paired))}
    assert grid_pass == (3 if coupling else 9)
    return {"A_vertices": [NAMES[v] for v in a], "overlap_with_C": [NAMES[v] for v in j],
            "dimension_at_fixed_A": rank_free, "clamped_admitted_of_9": grid_pass,
            "free_A_admitted_of_9": free_pass, "controls": controls,
            "A_counting_potential": list(map(int, phi_a)), "C_counting_potential": list(map(int, phi_c))}


def shared_port(green, overlap, endpoints):
    fields = {label: set() for label in endpoints}
    n_admitted = n_comparisons = 0
    for source in compositions(5, len(FULL)):
        if overlap.push(PARENTS, FULL, C, source) != (2, 2, 1):
            continue
        n_admitted += 1
        assert graded_field(green, overlap, C, source) == (0, 3, 4)
        for label, views in endpoints.items():
            a = tuple(views[0])
            x = overlap.push(PARENTS, FULL, a, source)
            base = (x[0] - 5, *x[1:])
            fields[label].add(int(graded_field(green, overlap, a, source)[a.index(4)]))
            for drive in (-2, -1, 0, 1, 2):
                local = tuple(drive * (int(v == 4) - int(v == 0)) for v in a)
                phi = response(green, a, add(base, local))
                assert phi[a.index(4)] - phi[a.index(0)] == source[4] + drive
                n_comparisons += 1
    assert n_admitted == 9 and list(fields.values()) == [{0, 1, 2}, {0, 1, 2}]
    return {"admitted_ambient_sources": n_admitted, "signed_port_checks": n_comparisons,
            "possible_common_od_drops": {label: sorted(values) for label, values in fields.items()}}


def whole_cover(green, overlap, views):
    """Check every pair and the union for the same literal C intervention."""
    a, b, c = map(tuple, views)
    assert c == C
    base = (1,) * len(FULL)
    baseline = [graded_field(green, overlap, y, base) for y in (a, b, c)]
    drive = (-1, 1, 0)
    _, inclusion, _, harmonic = overlap.maps(PARENTS, FULL, C)
    injected = tuple(map(int, inclusion * sp.Matrix(drive)))
    assert injected == (-1, 1, 0, 0, 0)
    full_delta = response(green, FULL, injected)
    assert full_delta == (0, 1, 1, 1, 0)
    assert full_delta == (0, *(harmonic * sp.Matrix(response(green, C, drive)[1:])))
    shifted, records, frozen = [], {}, {}
    for label, y, field in zip("ABC", (a, b, c), baseline):
        pushed = overlap.push(PARENTS, FULL, y, injected)
        delta = response(green, y, pushed)
        assert delta == tuple(full_delta[v] for v in y)
        if label != "C":
            records[label] = {"view": [NAMES[v] for v in y], "projected_drive": list(map(int, pushed)),
                              "potential_increment": list(map(int, delta))}
            frozen[label] = gluable(overlap, y, field, add(baseline[2], response(green, C, drive)))
            assert frozen[label] == (1 not in y)
        shifted.append(add(field, delta))
    for s, t in itertools.combinations(range(3), 2):
        left, right = tuple(views[s]), tuple(views[t])
        pair = overlap.glue_response(PARENTS, left, right,
                                     tuple(map(str, shifted[s])), tuple(map(str, shifted[t])))
        pair_sites = tuple(sorted(set(left) | set(right)))
        remaining = 3 - s - t
        union = overlap.glue_response(PARENTS, pair_sites, tuple(views[remaining]), pair,
                                      tuple(map(str, shifted[remaining])))
        assert union == add(graded_field(green, overlap, FULL, base), full_delta)
    forced = [label for label in "AB" if not frozen[label]]
    return {"partners_forced_on_op": forced, "both_others_may_stay_fixed": all(frozen.values()),
            "fixed_C_drive": list(drive), "fixed_full_drive": list(injected),
            "full_potential_increment": list(map(int, full_delta)), "other_view_projections": records}


def loss_component(overlap, before, after, index, source):
    fine, coarse = tuple(before[index]), tuple(after[index])
    project, include, _, _ = overlap.maps(PARENTS, fine, coarse)
    _, into_full, _, _ = overlap.maps(PARENTS, FULL, fine)
    x = sp.Matrix(overlap.push(PARENTS, FULL, fine, source))
    lost = (sp.eye(len(fine)) - include * project) * x
    assert project * lost == sp.zeros(len(coarse), 1)
    return tuple(Fraction(str(value)) for value in into_full * lost)


def event_modes(green, overlap, initial, middle, endpoints):
    counting = (1,) * len(FULL)
    samples = [s for s in compositions(5, len(FULL))
               if overlap.push(PARENTS, FULL, C, s) == (2, 2, 1)]
    # No majority, zero subtotal and arbitrary signed sources probe the algebra's domain.
    extras = [(8, 1, -2, 3, 1), (4, -3, 1, 2, 0), (1, -3, 0, 1, 1),
              (0, Fraction(1, 2), 0, Fraction(1, 3), 0)]
    records = {}
    for index, label in enumerate("AB"):
        mid, end = middle[label], endpoints[label]
        for source in samples + extras:
            marginal = overlap.push(PARENTS, FULL, C, source)
            subtotal = marginal[1] + marginal[2]
            leaf = loss_component(overlap, initial, mid, index, source)
            parent = loss_component(overlap, mid, end, index, source)
            assert leaf == (0, -source[2], source[2], 0, 0)
            assert parent == (-subtotal, subtotal, 0, 0, 0)
            assert overlap.push(PARENTS, FULL, C, leaf) == (0, 0, 0)
            assert overlap.push(PARENTS, FULL, C, parent) == (-subtotal, subtotal, 0)
            modes = {}
            for owner, view in zip("ABC", map(tuple, end)):
                projected = overlap.push(PARENTS, FULL, view, parent)
                phi = response(green, view, projected)
                expected = tuple(subtotal if v in (1, 2, 3) else 0 for v in view)
                assert phi == expected
                modes[owner] = phi
            c_field = graded_field(green, overlap, C, source)
            assert c_field == (0, subtotal, subtotal + marginal[2])
            assert (c_field[1], c_field[2] - c_field[1]) == (subtotal, marginal[2])
            if source == counting:
                records[label] = {"first_lost_ambient": list(map(int, leaf)), "parent_lost_ambient": list(map(int, parent)),
                                  "endpoint_lost_potentials": {name: list(map(int, x)) for name, x in modes.items()},
                                  "unchanged_C_field": list(map(int, c_field)),
                                  "first_C_projection": [0, 0, 0], "second_C_projection": [-int(subtotal), int(subtotal), 0]}
    assert set(records) == {"A", "B"}
    return {"counting": records, "integer_sources_per_branch": len(samples),
            "signed_control_C_subtotals": [str(sum(overlap.push(PARENTS, FULL, C, s)[1:])) for s in extras]}


def main():
    green = load_green()
    overlap = archived_source("overlap")
    initial, middle, endpoints = source_views()
    stages = {"initial": initial, "after_A_leaf": middle["A"], "after_B_leaf": middle["B"],
              "after_A_parent": endpoints["A"], "after_B_parent": endpoints["B"]}
    rows = {key: clamped_modes(green, overlap, views) for key, views in stages.items()}
    endpoint_answer = {label: rows["after_" + label + "_parent"]["controls"]["op_trial"]["clamped"]
                       for label in ("A", "B")}
    assert endpoint_answer == {"A": True, "B": False}
    assert all(not rows[key]["controls"]["op_trial"]["clamped"] for key in list(stages)[:3])
    assert all(row["controls"]["pw_control"]["clamped"] for row in rows.values())
    assert add((2, 2, 1), (-1, 1, 0)) == (1, 3, 1)
    cover = {key: whole_cover(green, overlap, views) for key, views in stages.items()}
    assert [cover[k]["partners_forced_on_op"] for k in stages] == [["A", "B"]] * 3 + [["B"], ["A"]]
    assert all(not row["both_others_may_stay_fixed"] for row in cover.values())
    report = {"stages": rows, "common_A_port": shared_port(green, overlap, endpoints),
              "three_view_cover": cover,
              "event_loss": event_modes(green, overlap, initial, middle, endpoints),
              "C_counting_grade_after_unit_trial": [1, 3, 1], "C_vertices": [NAMES[v] for v in C],
              "clamp_grade_majority_used": False, "physical_delivery_status": "OPEN"}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
