"""Compare literal P1 mergers with the archived bracket response, exactly."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import sympy as sp
import check_bracket_ports as archived

ROOT = Path(__file__).resolve().parents[5]
N = archived.N
INDICES = tuple(range(N))
OUT, PROBE, COMPENSATOR = 3, 2, 10


def unit(i):
    return [Fraction(j == i) for j in INDICES]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def nonzero(a):
    return {i for i, x in enumerate(a) if x != 0}


def read_source():
    """Use the native definitions with immutable input and gate provenance."""
    src = archived.original_functions(ROOT / archived.HISTORICAL_PATH)
    base = src["build_base"]()
    inputs = [[Fraction(int(x)) for x in branch] for branch in base["branches"]]
    gates = {
        name: Fraction((i + 1) % 11 + 2, (2 * i + 1) % 7 + 3)
        for i, name in enumerate(base["gates"])
    }
    assert {k: float(v) for k, v in gates.items()} == base["gates"]
    assert all(np.array_equal(a, b) for a, b in zip(inputs, base["branches"]))

    def native(a, b, g):
        return list(src["recombine"](np.array(a, dtype=object), np.array(b, dtype=object), g))

    def operand(inner, grouping):
        b, c, d = inner
        if grouping == "B3":
            return native(native(b, c, gates["g23"]), d, gates["g234"])
        return native(b, native(c, d, gates["g34"]), gates["g234"])

    operands = {k: operand(inputs[1:], k) for k in ("B3", "B4")}
    for key, name in (("B3", archived.LEFT), ("B4", archived.RIGHT)):
        result = native(inputs[0], operands[key], gates["g1234r"])
        assert np.allclose(np.array(result, dtype=float), base["bracketings"][name], rtol=0, atol=1e-9)
    return native, operand, inputs[1:], operands, gates["g1234r"]


def mergers():
    return [(u, p) for u in INDICES for p in INDICES if p != u]


def push(v, removed, parent):
    return [v[j] + (v[removed] if j == parent else 0) for j in INDICES if j != removed]


def included(v, u, p):
    out = push(v, u, p)
    out.insert(u, Fraction(0))
    return out


def native_p1_basis_check():
    # Any ordered pair is admissible on a rooted star with the parent at its root.
    # Renumber that tree back into cyclic slots after using the actual P1 routine.
    source = ROOT / "ResearchHistory/UQCF-GEM/demos/v16.23-overlap-descent/engine.py"
    raw = source.read_bytes()
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"
    spec = importlib.util.spec_from_file_location("p1_source", source)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)

    tree = (-1,) + (0,) * (N - 1)
    for u, p in mergers():
        order = [p] + [j for j in INDICES if j != p]
        keep = tuple(j for j in INDICES if order[j] != u)
        for j in INDICES:
            x = unit(j)
            actual = engine.push(tree, INDICES, keep, tuple(x[t] for t in order))
            relabeled = dict(zip((order[k] for k in keep), actual))
            assert [relabeled[k] for k in INDICES if k != u] == push(x, u, p)
    return len(mergers()) * N


def jacobian_contrast(s, gamma):
    return [
        [gamma * (s[i] * int(j == (i - 1) % N) - s[(i + 1) % N] * int(j == i))
         for j in INDICES]
        for i in INDICES
    ]


def matches_target(delta, targets, gamma):
    exact = [name for name, target in targets.items() if delta == target]
    local = [name for name, target in targets.items() if gamma * delta[OUT] == gamma * target[OUT]]
    return exact, local


def direct_and_nested(operand, inputs, q, gamma):
    target = sub(q["B3"], q["B4"])
    targets = {"B4_to_B3": target, "B3_to_B4": [-x for x in target]}
    assert len(nonzero(target)) == 10
    assert sp.Matrix(jacobian_contrast(target, gamma)).rank() == 10

    direct = []
    for origin, destination in (("B3", "B4"), ("B4", "B3")):
        start, end = q[origin], q[destination]
        lost = sorted(nonzero(start) - nonzero(end))
        # Any removed nonzero address must end at zero. Each removed nonzero
        # address can change only itself and its final retraction target.
        assert len(nonzero(sub(end, start))) > 2 * len(lost)
        trials = []
        for u, p in mergers():
            after = included(start, u, p)
            delta = sub(after, start)
            assert sum(delta) == 0 and nonzero(delta) <= {u, p}
            trials.append({
                "deleted": u, "parent": p, "delta_support": len(nonzero(delta)),
                "exact_pair": after == end, "matches_site3_delta": delta[OUT] == end[OUT] - start[OUT],
            })
        direct.append({
            "origin": origin, "destination": destination,
            "candidates_for_deleted_nonzero_coordinates": lost, "trials": trials,
        })

    nested = []
    for grouping in ("B3", "B4"):
        for bit in range(3):
            trials = []
            for u, p in mergers():
                inner = [v.copy() for v in inputs]
                inner[bit] = included(inputs[bit], u, p)
                observed = sub(operand(inner, grouping), q[grouping])
                assert sum(observed) == 0

                # Test the direction with unit amplitude, independently of the
                # current leaf grade. Fixed brackets are affine in this input.
                changed = [v.copy() for v in inputs]
                changed[bit] = [x + y for x, y in zip(inputs[bit], sub(unit(p), unit(u)))]
                direction = sub(operand(changed, grouping), q[grouping])
                assert all(a == inputs[bit][u] * b for a, b in zip(observed, direction))
                assert len(nonzero(observed)) <= len(nonzero(direction)) <= 6
                full, local = matches_target(observed, targets, gamma)
                assert full == []
                trials.append({
                    "deleted": u, "parent": p,
                    "original_leaf_grade": str(inputs[bit][u]),
                    "unit_direction_support": len(nonzero(direction)),
                    "actual_support": len(nonzero(observed)),
                    "rank_upper_bound": len(nonzero(observed)),
                    "same_output3_response_directions": local,
                    "unit_leaf_transfer_at_output3": str(gamma * direction[OUT]),
                })
            nested.append({
                "fixed_grouping": grouping, "edited_inner_input": bit + 2,
                "max_support": max(t["actual_support"] for t in trials),
                "max_unit_support": max(t["unit_direction_support"] for t in trials),
                "trials": trials,
            })
    return direct, nested


def predicted_factor(q, u, p, same_law):
    a, b = (u - 1) % N, (u + 1) % N
    if p == a:
        entries = (u, b) if same_law else (b,)
    elif p == b:
        entries = (p, (p + 1) % N) if same_law else ((p + 1) % N,)
    else:
        entries = (u, b, (p + 1) % N) if same_law else (b, (p + 1) % N)
    return all(q[j] == 0 for j in entries)


def compare_mergers(native, operands, gamma):
    vectors = {**operands, "B3_minus_B4": sub(operands["B3"], operands["B4"])}
    report = {
        name: {"any_affine_factor": [], "coarse_cyclic_identity": [], "site3_any_factor": [],
               "site3_coarse_cyclic_identity": [], "site3_same_response_with_both_probe_sites": []}
        for name in vectors
    }
    records = []
    for u, p in mergers():
        keep = [j for j in INDICES if j != u]
        entry = {"deleted": u, "parent": p, "results": {}}
        for name, q in vectors.items():
            # For the contrast, R(x,s)-x is exactly the difference of the
            # two original R calls, including their constant offsets.
            fine = [push(native(unit(j), q, gamma), u, p) for j in INDICES]
            coarse_q = push(q, u, p)
            coarse = [native(push(unit(j), u, p), coarse_q, gamma) for j in INDICES]
            assert push(native([0] * N, q, gamma), u, p) == native([0] * (N - 1), coarse_q, gamma)
            arbitrary = fine[u] == fine[p]
            same = fine == coarse
            assert arbitrary == predicted_factor(q, u, p, False)
            assert same == predicted_factor(q, u, p, True)
            row = {"affine_factor": arbitrary, "coarse_cyclic_identity": same}
            for yes, k in ((arbitrary, "any_affine_factor"), (same, "coarse_cyclic_identity")):
                if yes:
                    report[name][k].append([u, p])
            if u != OUT:
                read = keep.index(OUT)
                fixed_site = all(f[read] == c[read] for f, c in zip(fine, coarse))
                fixed_site_factor = fine[u][read] == fine[p][read]
                assert fixed_site_factor == (u not in (PROBE, OUT) and p not in (PROBE, OUT))
                row["site3_fixed_row"] = fixed_site
                row["site3_any_factor"] = fixed_site_factor
                row["site3_balanced_probe_response"] = str(fine[PROBE][read] - fine[COMPENSATOR][read])
                row["site3_coarse_balanced_probe_response"] = str(coarse[PROBE][read] - coarse[COMPENSATOR][read])
                if fixed_site_factor:
                    report[name]["site3_any_factor"].append([u, p])
                if fixed_site:
                    report[name]["site3_coarse_cyclic_identity"].append([u, p])
                if fixed_site and u not in (PROBE, COMPENSATOR):
                    report[name]["site3_same_response_with_both_probe_sites"].append([u, p])
            entry["results"][name] = row
        records.append(entry)
    for name in operands:
        assert not report[name]["coarse_cyclic_identity"]
    assert len(report["B3"]["any_affine_factor"]) == 6
    assert len(report["B4"]["any_affine_factor"]) == 2
    assert report["B3_minus_B4"]["coarse_cyclic_identity"] == [[9, 10], [10, 9]]
    assert sorted(set(map(tuple, report["B3"]["any_affine_factor"])) &
                  set(map(tuple, report["B4"]["any_affine_factor"]))) == [(9, 10), (10, 9)]
    for name, counts in report.items():
        assert len(counts["site3_any_factor"]) == 90
        assert len(counts["site3_coarse_cyclic_identity"]) == (74 if name == "B3_minus_B4" else 73)
    for u, p in ((9, 10), (10, 9)):
        record = next(e for e in records if (e["deleted"], e["parent"]) == (u, p))
        for row, slope in (("B3", "-63"), ("B4", "-270"), ("B3_minus_B4", "207")):
            assert record["results"][row]["site3_coarse_balanced_probe_response"] == slope
        retained = [j for j in INDICES if j != u]
        s = push(vectors["B3_minus_B4"], u, p)
        matrix = sp.Matrix([
            [gamma * (s[i] * int(j == (i - 1) % len(retained))
                      - s[(i + 1) % len(retained)] * int(j == i))
             for j in range(len(retained))]
            for i in range(len(retained))
        ])
        assert matrix.rank() == 10
    return report, records


def verify_two_input_loss(native, gamma):
    # Show separately that two distinct fibre contrasts can affect the output,
    # with positive inputs and with equal totals within each comparison.
    for u, p in mergers():
        members = {u, p}
        direction = sub(unit(u), unit(p))
        base = [Fraction(2)] * N
        varied = [a + b / 2 for a, b in zip(base, direction)]
        assert push(base, u, p) == push(varied, u, p)
        w = next(j for j in members if (j + 1) % N not in members)
        y = [a + b for a, b in zip(base, unit((w + 1) % N))]
        x0, x1 = [push(native(x, [0] * N, gamma), u, p) for x in (base, varied)]
        assert x0 == x1
        # The unit change to y isolates the outgoing edge. At least one of
        # y and the constant background must expose the difference of x.
        deltas = [sub(push(native(varied, q, gamma), u, p),
                      push(native(base, q, gamma), u, p)) for q in (base, y)]
        assert any(sub(*deltas))
        t = next(j for j in INDICES if j not in members and (j + 1) % N in members)
        x = [a + b for a, b in zip(base, unit(t))]
        deltas = [sub(push(native(left, varied, gamma), u, p),
                      push(native(left, base, gamma), u, p)) for left in (base, x)]
        assert any(sub(*deltas))
    return 2 * len(mergers())


def summary(data, raw):
    return {
        "full_json_bytes": len(raw), "full_json_sha256": hashlib.sha256(raw).hexdigest(),
        "p1_basis_checks": data["p1_basis_checks"],
        "positive_two_input_loss_checks": data["positive_two_input_loss_checks"],
        "direct": [{
            "origin": d["origin"], "destination": d["destination"],
            "nonzero_coordinates_that_could_be_deleted": d["candidates_for_deleted_nonzero_coordinates"],
            "trials": len(d["trials"]), "full_matches": sum(t["exact_pair"] for t in d["trials"]),
            "single_read_matches": sum(t["matches_site3_delta"] for t in d["trials"]),
        } for d in data["direct"]],
        "nested": [{
            "grouping": n["fixed_grouping"], "edited_input": n["edited_inner_input"],
            "trials": len(n["trials"]), "max_support": n["max_support"],
            "max_unit_support": n["max_unit_support"],
            "single_read_matches": sum(bool(t["same_output3_response_directions"]) for t in n["trials"]),
            "nonzero_unit_transfer_at_chosen_read": sum(
                t["unit_leaf_transfer_at_output3"] != "0" for t in n["trials"]
            ),
        } for n in data["nested"]],
        "coarse_factorization": {
            arm: {
                field: rows if field in ("any_affine_factor", "coarse_cyclic_identity") else len(rows)
                for field, rows in result.items()
            } for arm, result in data["classification"].items()
        },
    }


def main():
    if not __debug__:
        raise ValueError("Run without optimization to enable all checks")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summarize", type=Path)
    args = parser.parse_args()
    if args.summarize:
        raw = args.summarize.read_bytes()
        print(json.dumps(summary(json.loads(raw), raw), indent=2, sort_keys=True))
        return
    native, operand, inputs, q, gamma = read_source()
    basis_checks = native_p1_basis_check()
    direct, nested = direct_and_nested(operand, inputs, q, gamma)
    classification, records = compare_mergers(native, q, gamma)
    print(json.dumps({
        "historical_source_blob": archived.PIN,
        "default_gamma": str(gamma),
        "ordered_leaf_parent_choices": len(mergers()),
        "p1_basis_checks": basis_checks,
        "positive_two_input_loss_checks": verify_two_input_loss(native, gamma),
        "direct": direct,
        "nested": nested,
        "coarse_comparisons": records,
        "classification": classification,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
