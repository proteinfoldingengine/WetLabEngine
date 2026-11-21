"""Exact bounded replay of leaf-loss support, unit Green response and old subtree totals.

Run: python check_loss_support.py [--max-vertices 5] [--output FILE].
Every admitted (X,M,h,V) is checked as a rational matrix identity, covering all
signed inputs. Enumeration is evidence only within the reported size bound.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import sympy as sp

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[3] / "demos"
COMMIT = "e7e01bab68ba5171dacd91333f98d208d810dac3"
SOURCES = {
    "green": ("v16.22-response-selection-closure/engine.py", "9b71ce47bbef83132f00270f8a9a19e7721864d6"),
    "pruning": ("v16.23-overlap-descent/engine.py", "b18f52109ccff9c7dc77542d3b8f3e5d5989102a"),
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def load_sources():
    for relative, expected in SOURCES.values():
        data = (BASE / relative).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(actual == expected, f"Historical Git blob mismatch: {relative}: {actual}")
    modules = {}
    for key, (relative, _) in SOURCES.items():
        spec = importlib.util.spec_from_file_location("loss_" + key, BASE / relative)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[key] = module
    return modules["green"], modules["pruning"]


def code(p, v=0):
    return "(" + "".join(sorted(code(p, w) for w in range(1, len(p)) if p[w] == v)) + ")"


def descendant(p, v, h):
    while v and v != h:
        v = p[v]
    return v == h


def views(p):
    return [tuple(v for v in range(len(p)) if mask & (1 << v))
            for mask in range(1, 1 << len(p), 2)
            if all(v == 0 or mask & (1 << p[v]) for v in range(len(p)) if mask & (1 << v))]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def passive_gluing_controls(green, pruning):
    p = (-1, 0, 1, 0, 0)
    X, U = (0, 1, 2, 3, 4), (0, 1, 2, 3)
    M, V, E = (0, 1, 3), (0, 1, 2), (0, 3)
    source = (2, -3, 5, 1)
    x_m, x_v = [pruning.push(p, U, y, source) for y in (M, V)]
    x_e = pruning.push(p, M, E, x_m)
    require(pruning.glue(p, M, V, x_m, x_v) == pruning.glue(p, E, V, x_e, x_v) == source,
            "Passive source changed on the same proper union")
    field = (0, *map(int, green.candidate(p[:4]) * sp.Matrix(source[1:])))
    cut = lambda view: tuple(field[i] for i in view)
    require(field == (0, 2, 7, 1), "Signed common-root-balanced field")
    require(pruning.glue_response(p, M, V, cut(M), cut(V)) ==
            pruning.glue_response(p, E, V, cut(E), cut(V)) == field, "Passive field changed")
    for ambient in ((2, -3, 5, 1, 0), (1, -3, 5, 1, 1)):
        require(pruning.push(p, X, U, ambient) == source, "Distinct ambient extensions control")
    # Independent arithmetic means on X and Y need not represent compatible fields.
    chain, full, y = (-1, 0, 1), (0, 1, 2), (0, 1)
    raw_y = pruning.push(chain, full, y, (1, 1, 1))
    require(raw_y == (1, 2), "Mean-centering example source")
    average_y = sum(raw_y) / len(y)
    y_drop = (green.candidate((-1, 0)) * sp.Matrix([raw_y[1] - average_y]))[0]
    require(y_drop == sp.Rational(1, 2), "Local mean-centered potential drop")
    unit_drop = (green.candidate((-1, 0)) * sp.Matrix([1]))[0]
    require(unit_drop == 1, "A balanced source dipole changes the field")
    return {"proper_union_before_and_after_source": list(source),
            "proper_union_before_and_after_potential": list(field), "old_M_coefficient": int(x_m[1]),
            "ambient_extensions_checked": 2, "mean_centered_ambient_drop": 0,
            "mean_centered_coarse_drop": str(y_drop), "unit_dipole_potential_drop": int(unit_drop)}


def run(bound=5):
    require(1 <= bound <= 5, "Finite bound must be 1..5")
    green, pruning = load_sources()
    trees = green.shapes(bound)
    independent_codes = {code((-1,) + tail) for n in range(1, bound + 1)
                         for tail in itertools.product(*(range(i) for i in range(1, n)))}
    require([code(p) for p in trees] == sorted(independent_codes, key=lambda s: (len(s), s)), "Shape universe mismatch")
    require(trees == pruning.shapes(bound), "Original shape enumerators disagree")
    expected_shapes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 9}
    require(dict(Counter(map(len, trees))) == {n: expected_shapes[n] for n in range(1, bound + 1)}, "Shape counts")

    @lru_cache(None)
    def unit_green(p, V):
        local = (-1,) + tuple(V.index(p[v]) for v in V[1:])
        G = green.candidate(local)
        L = green.root_laplacian(local)
        require(G == (L.inv() if len(V) > 1 else sp.zeros(0)), "Unit candidate is not original Green inverse")
        return G

    totals, by_size, shape_rows = Counter(), {}, []
    digest = hashlib.sha256()
    for p in trees:
        X = tuple(range(len(p)))
        retained = views(p)
        require(retained == pruning.subsets(p), "Retained-view universe mismatch")
        counts = Counter(shapes=1, retained_views=len(retained))
        for M in retained:
            for h in M[1:]:
                if any(p[v] == h for v in M[1:]):
                    continue
                counts["leaf_deletions"] += 1
                g, E = p[h], tuple(v for v in M if v != h)
                P_ME, I_EM, _, _ = pruning.maps(p, M, E)
                _, I_MX, _, _ = pruning.maps(p, X, M)
                loss_M = sp.eye(len(M)) - I_EM * P_ME
                loss_X = I_MX * loss_M
                for V in retained:
                    counts["triples"] += 1
                    counts["signed_basis_columns"] += len(M)
                    P_XV, _, _, _ = pruning.maps(p, X, V)
                    loss = P_XV * loss_X
                    expected = sp.zeros(len(V), len(M))
                    if h in V:
                        expected[V.index(h), M.index(h)] = 1
                        expected[V.index(g), M.index(h)] = -1
                        counts["retaining_triples"] += 1
                    else:
                        counts["blind_triples"] += 1
                    require(loss == expected, "Leaf-loss signed matrix identity")
                    require(all(sum(loss[:, j]) == 0 for j in range(len(M))), "Loss total not zero")

                    # Independently exercise original push(), rather than only its maps().
                    for j in range(len(M)):
                        basis = tuple(int(i == j) for i in range(len(M)))
                        pruned = pruning.push(p, M, E, basis)
                        residual = [basis[i] - (pruned[E.index(v)] if v in E else 0) for i, v in enumerate(M)]
                        extended = [residual[M.index(v)] if v in M else 0 for v in X]
                        pushed = pruning.push(p, X, V, extended)
                        require(list(map(str, pushed)) == list(map(str, loss[:, j])), "Original push disagrees with matrix")

                    response = sp.zeros(1, len(M)).col_join(unit_green(p, V) * loss[1:, :])
                    expected_response = sp.zeros(len(V), len(M))
                    descendants = [v for v in V if descendant(p, v, h)]
                    for v in descendants:
                        expected_response[V.index(v), M.index(h)] = 1
                    require(response == expected_response, "Unit Green support matrix identity")
                    for q in (-2, 0, 1, 3):
                        force = q * loss[:, M.index(h)]
                        field = q * response[:, M.index(h)]
                        nonzero = bool(q) and h in V
                        require(any(value != 0 for value in field) == nonzero, "Zero-amplitude support caveat")
                        require(max(map(abs, field), default=0) == (abs(q) if h in V else 0), "Sup norm bound")
                        require(sum(map(abs, field)) == abs(q) * len(descendants), "L1 response bound")
                        require(sum(map(abs, force)) == (2 * abs(q) if h in V else 0), "Dipole norm")
                        counts["amplitude_controls"] += 1

                    before_union, after_union = set(M) | set(V), set(E) | set(V)
                    require((before_union == after_union) == (h in V), "Other-view retention and coverage")
                    if before_union == set(X):
                        counts["covering_pairs"] += 1
                        if after_union == set(X):
                            counts["coverage_preserving_pairs"] += 1
                            require(h in V, "Coverage-preserving loss lacks another retaining view")

                    if h in V:
                        J = tuple(sorted(set(M) & set(V)))
                        P_MJ = pruning.maps(p, M, J)[0]
                        P_VJ = pruning.maps(p, V, J)[0]
                        source_coefficient = sp.zeros(1, len(M))
                        source_coefficient[0, M.index(h)] = 1
                        subtree_coefficient = sp.Matrix([[int(descendant(p, v, h)) for v in V]])
                        require(P_MJ[J.index(h), :] == source_coefficient, "h is not a leaf in intersection")
                        require(P_VJ[J.index(h), :] == subtree_coefficient, "Old subtree-total agreement identity")
                        # This exact constraint row proves q equals the old subtree total
                        # for every compatible signed pair; 0/1 coefficients prove
                        # 0 <= q <= total(z) when the existing V source z is nonnegative.
                        require(all(a in (0, 1) for a in subtree_coefficient), "Nonnegative total bound coefficients")
                        counts["compatibility_row_identities"] += 1
                    digest.update((canonical([list(p), list(M), h, list(V), list(map(str, loss)), list(map(str, response))]) + "\n").encode())
        totals.update(counts)
        by_size.setdefault(len(p), Counter()).update(counts)
        shape_rows.append({"shape": code(p), "parents": list(p), **dict(counts)})

    # h is a leaf only of M, and may have retained descendants in several receivers.
    p, X, M, h = (-1, 0, 1), (0, 1, 2), (0, 1), 1
    x, z = (1, 2), (1, 1, 1)
    require(pruning.push(p, X, M, z) == x, "Compatible covering example")
    receiver_controls = []
    for V in (X, M, (0,)):
        loss = pruning.push(p, X, V, (-2, 2, 0))
        field = sp.zeros(1, 1).col_join(unit_green(p, V) * sp.Matrix([str(a) for a in loss[1:]])) if len(V) > 1 else sp.zeros(1, 1)
        expected = [2 if descendant(p, v, h) else 0 for v in V]
        require(list(field) == expected, "Multiple-receiver descendant control")
        receiver_controls.append({"view": list(V), "loss": list(map(int, loss)), "unit_green": list(map(int, field))})
    return {"schema": 1, "status": "PASS", "source_commit": COMMIT,
            "sources": {k: {"path": p, "git_blob": s} for k, (p, s) in SOURCES.items()},
            "bound_vertices": bound, "totals": dict(totals),
            "by_size": {str(n): dict(c) for n, c in by_size.items()}, "shapes": shape_rows,
            "signed_identity_digest_sha256": digest.hexdigest(), "amplitudes_checked": [-2, 0, 1, 3],
            "compatible_cover_control": {"parents": list(p), "M": list(M), "x_M": list(x),
                                         "V": list(X), "z_V": list(z), "q": 2, "old_V_subtree_total": 2},
            "multiple_receiver_controls": receiver_controls,
            "passive_gluing_controls": passive_gluing_controls(green, pruning),
            "exactness": "Rational matrix identities cover all signed inputs on every enumerated triple; original push was also checked on every M basis column.",
            "bounds": "If h is retained, ||response||_infinity=|q| and ||response||_1=|q| times the number of retained descendants of h. Compatible nonnegative V grades give 0<=q<=their total.",
            "zero_caveat": "The projected loss and unit Green response are nonzero iff h is retained AND q!=0; zero q gives zero in every view.",
            "coverage": "For any indexed covering family, preserving its union after M loses h forces at least one other view to retain h. The finite pair identity was checked for every triple.",
            "scope": "Finite original-function replay through the stated vertex bound; no event selector, physical attainability, broad certification, or general proof from finite counts is claimed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-vertices", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = canonical(run(args.max_vertices)) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
