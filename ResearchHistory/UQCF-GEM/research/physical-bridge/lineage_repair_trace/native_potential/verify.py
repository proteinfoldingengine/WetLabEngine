"""Exact leaf-source Laplacian comparison on the preregistered three-node fixture."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
PARENT, LEAF, SIBLING = 0, 1, 2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matvec(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def laplacian(size, edges):
    matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for i, j in edges:
        matrix[i][i] += 1
        matrix[j][j] += 1
        matrix[i][j] -= 1
        matrix[j][i] -= 1
    return matrix


def centered(grade):
    average = sum(grade, F(0)) / len(grade)
    return [F(x) - average for x in grade]


def solve_with_parent_gauge(lap, source):
    # Replace the redundant parent equation by the gauge equation phi_p = 0.
    n = len(source)
    aug = [list(row) + [source[i]] for i, row in enumerate(lap)]
    aug[PARENT] = [F(i == PARENT) for i in range(n)] + [F(0)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for i in range(n):
            if i != col:
                multiplier = aug[i][col]
                aug[i] = [v - multiplier * w for v, w in zip(aug[i], aug[col])]
    potential = [row[-1] for row in aug]
    require(potential[PARENT] == 0 and matvec(lap, potential) == source,
            "Full ungauged native system failed its exact residual check")
    return potential


def contrast(a, b, positive, negative):
    return (b[positive] - b[negative]) - (a[positive] - a[negative])


def spell(vector):
    return [str(v) for v in vector]


def native_fixture():
    fine = laplacian(3, [(PARENT, LEAF), (PARENT, SIBLING)])
    coarse = laplacian(2, [(0, 1)])
    prune = [[1, 1, 0], [0, 0, 1]]
    grade_a, grade_b = [1, 0, 0], [0, 1, 0]
    source_a, source_b = centered(grade_a), centered(grade_b)
    require(matvec(prune, grade_a) == matvec(prune, grade_b) == [1, 0], "P1 split changed")
    delta = [b - a for a, b in zip(source_a, source_b)]
    require(matvec(fine, grade_b) == delta == [-1, 1, 0], "Leaf column sign changed")
    require(matvec(prune, delta) == [0, 0], "Leaf-parent contrast survived P1")
    a = solve_with_parent_gauge(fine, source_a)
    b = solve_with_parent_gauge(fine, source_b)
    y_a, y_b = matvec(prune, source_a), matvec(prune, source_b)
    c_a, c_b = solve_with_parent_gauge(coarse, y_a), solve_with_parent_gauge(coarse, y_b)
    require(c_a == [a[PARENT], a[SIBLING]] and c_b == [b[PARENT], b[SIBLING]],
            "Native potentials failed the actual restriction test")
    require(c_a == c_b and y_a == y_b, "Coarse native outputs distinguish equal native sources")
    fine_drop = contrast(a, b, LEAF, PARENT)
    retained_drop = contrast(a, b, PARENT, SIBLING)
    require((fine_drop, retained_drop) == (1, 0), "Oriented edge contrasts changed")
    a_shift = [v + F(11, 7) for v in a]
    b_shift = [v - F(5, 3) for v in b]
    require((contrast(a_shift, b_shift, LEAF, PARENT),
             contrast(a_shift, b_shift, PARENT, SIBLING)) == (fine_drop, retained_drop),
            "Gauge shifts changed an edge contrast")
    return {"order": ["parent", "leaf", "sibling"], "centered_a": spell(source_a),
            "centered_b": spell(source_b), "fine_potential_a": spell(a),
            "fine_potential_b": spell(b), "fine_leaf_minus_parent_contrast": str(fine_drop),
            "coarse_source_a_and_b_after_fine_centering": spell(y_a),
            "coarse_potential_a_and_b": spell(c_a),
            "retained_parent_minus_sibling_each": str(a[PARENT] - a[SIBLING]),
            "retained_parent_minus_sibling_contrast": str(retained_drop),
            "independent_gauge_shifts": ["11/7", "-5/3"]}


def archived_comparison():
    spec = importlib.util.spec_from_file_location("frozen_parent_verifier", HERE.parent / "verify.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    archived = verifier.load_source()
    tree = archived.build_kary_tree(1, 2)
    memory = np.tile([0.0, 1.0], (tree.n, 1))
    outcomes = []
    known = json.loads((HERE.parent / "verification.json").read_text())["p1"]
    for source, name in [(PARENT, "A"), (LEAF, "B")]:
        values = memory.copy()
        values[source, 0] = 1.0
        result = archived.seed_repair(values, memory, tree, np.array([SIBLING]), steps=1)
        require(verifier.rounded(result[PARENT]) == known["default_parent_" + name],
                "Computed parent differs from the already published replay")
        require(result[SIBLING, 0] == 0.0, "Protected sibling differs in the tested coordinate")
        outcomes.append(float(result[PARENT, 0] - result[SIBLING, 0]))
    delta = outcomes[1] - outcomes[0]
    require(delta < 0, "Expected negative relative repair contrast")
    return {"parent_minus_sibling_a": round(outcomes[0], 12),
            "parent_minus_sibling_b": round(outcomes[1], 12),
            "relative_contrast_b_minus_a": round(delta, 12),
            "identification": "first repair coordinate as scalar potential on unchanged addresses, supplied"}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "native": native_fixture(), "repair": archived_comparison(),
                      "native_receiver_delivery": "NOT_DERIVED"}, indent=2, sort_keys=True))
