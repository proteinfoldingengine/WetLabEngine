"""Compare the original repair routine with graph distances and an exact P1 coefficient."""
from collections import deque
from fractions import Fraction
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[5]
SOURCE = "Tmp/TOE/retained_branch_identity_audit.py"
SOURCE_BLOB = "5032b156203183b33318e44f3c4492e5ac697503"
HORIZON = 5


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_source():
    path = ROOT / SOURCE
    raw = path.read_bytes()
    identity = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(identity == SOURCE_BLOB, "Historical source bytes changed")
    spec = importlib.util.spec_from_file_location("archived_lineage_repair", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fields(tree, source):
    memory = np.tile([0.0, 1.0], (tree.n, 1))
    low = memory.copy()
    high = memory.copy()
    high[source, 0] = 1.0
    return low, high, memory


def predicted_distances(parent, source, protected):
    # Independent edge construction. The tested operator uses its own adjacency().
    edges = [[] for _ in parent]
    for child, ancestor in enumerate(parent):
        if ancestor >= 0:
            edges[child].append(int(ancestor))
            edges[ancestor].append(child)
    distances = [None] * len(parent)
    queue = deque([source])
    distances[source] = 0
    while queue:
        vertex = queue.popleft()
        for other in edges[vertex]:
            if other not in protected and distances[other] is None:
                distances[other] = distances[vertex] + 1
                queue.append(other)
    return distances


def first_observed(module, tree, source, protected, strength=0.65):
    low, high, memory = fields(tree, source)
    seeds = np.asarray(sorted(protected), dtype=int)
    first = [None] * tree.n
    for step in range(HORIZON + 1):
        one = module.seed_repair(low, memory, tree, seeds, steps=step, strength=strength)
        two = module.seed_repair(high, memory, tree, seeds, steps=step, strength=strength)
        unequal = np.flatnonzero(np.any(one != two, axis=1))
        for vertex in unequal:
            if first[vertex] is None:
                first[vertex] = step
    return first


def arrival_checks(module):
    tree = module.build_kary_tree(depth=2, branch_factor=2)
    source = 3
    require(list(tree.parent) == [-1, 0, 0, 1, 1, 2, 2], "Tree fixture changed")
    other_vertices = [i for i in range(tree.n) if i != source]
    distances = {}
    counts = [0] * (HORIZON + 1)
    for size in range(len(other_vertices) + 1):
        for protected in combinations(other_vertices, size):
            expected = predicted_distances(tree.parent, source, protected)
            observed = first_observed(module, tree, source, protected)
            require(observed == expected, f"First arrival changed with protected rows {protected}")
            for step in observed:
                if step is not None:
                    counts[step] += 1
            key = ",".join(map(str, protected)) or "empty"
            distances[key] = observed
    clamped = first_observed(module, tree, source, {source})
    require(all(step is None for step in clamped), "Clamped source transmitted a distinction")
    zero = first_observed(module, tree, source, set(), strength=0.0)
    require(zero == [None, None, None, 0, None, None, None], "Zero-strength control propagated")
    require(distances["6"] == [2, 1, 3, 0, 2, 4, None], "Onward grandparent read changed")
    require(distances["1"] == zero, "Clamping the sole parent did not isolate the source")
    return {"seed_sets": len(distances), "row_first_arrivals_checked": len(distances) * tree.n,
            "row_sweep_comparisons": len(distances) * tree.n * (HORIZON + 1),
            "first_observed_by_sweep": counts,
            "never_observed_in_fixtures": len(distances) * tree.n - sum(counts),
            "protected_source": clamped, "zero_strength": zero,
            "row_order": list(range(tree.n)), "per_protected_set": distances}


def strategy_checks(module):
    tree = module.build_kary_tree(depth=1, branch_factor=2)
    seed_rows = {name: module.select_seeds(tree, name, 0.05, np.random.default_rng(0))
                 for name in ("root", "leaf")}
    sibling, = seed_rows["leaf"]
    source, = set(map(int, tree.leaves)) - {int(sibling)}
    parent = int(tree.parent[source])
    require(seed_rows["root"].tolist() == [parent], "The root selector changed")
    arrival = {name: first_observed(module, tree, source, set(rows))
               for name, rows in seed_rows.items()}
    require(arrival["root"][parent] is None and arrival["leaf"][parent] == 1,
            "Protection selector no longer reverses the parent verdict")
    return {"parent": parent, "source": source, "fraction": 0.05, "rng_seed": 0,
            "actual_seed_rows": {k: v.tolist() for k, v in seed_rows.items()},
            "first_observed": arrival}


def coarse_grades(x, p, u):
    coarse = x.copy()
    coarse[p] += coarse[u]
    return np.delete(coarse, u, axis=0)


def rounded(row):
    return [round(float(x), 12) for x in row]


def grade_checks(module):
    tree = module.build_kary_tree(depth=1, branch_factor=2)
    p, u, sibling = 0, 1, 2
    memory = np.tile([0.0, 1.0], (tree.n, 1))
    a, b = memory.copy(), memory.copy()
    a[p, 0] = 1.0
    b[u, 0] = 1.0
    seeds = np.array([sibling])
    coarse_a, coarse_b = coarse_grades(a, p, u), coarse_grades(b, p, u)
    require(np.array_equal(coarse_a, coarse_b), "P1 output differs across the split")
    d = int(np.count_nonzero(tree.parent == p))  # The nominated parent is the root.
    strength = Fraction(13, 20)
    coefficient = strength / d - (1 - strength)
    require(coefficient == Fraction(-1, 40), "Default coefficient changed")
    rows = [module.seed_repair(x, memory, tree, seeds, steps=1)[p] for x in (a, b)]
    for row, weight in zip(rows, (1 - strength, strength / d)):
        expected = np.array([float(weight), 1.0])
        expected /= np.linalg.norm(expected) + 1e-12
        require(np.allclose(row, expected, atol=5e-15, rtol=0), "Nonlinear parent row mismatch")
    gap = float(np.linalg.norm(rows[0] - rows[1]))
    require(gap > 0.01, "Default parent failed to resolve the two fine splits")
    tuned_strength = Fraction(d, d + 1)
    tuned = [module.seed_repair(x, memory, tree, seeds, steps=1,
                                strength=float(tuned_strength))[p] for x in (a, b)]
    require(np.allclose(tuned[0], tuned[1], atol=5e-15, rtol=0),
            "Degree-matched strength did not give equal parent rows within rounding")
    # Exercise the archive's real normalization with collinear binary64 inputs.
    saturation = []
    for size in (1e8, 2e8):
        x = a.copy()
        x[p] = (size, 0.0)
        saturation.append(module.seed_repair(x, memory, tree, seeds, steps=1, strength=0.0)[p])
    require(np.array_equal(saturation[0], saturation[1]), "Binary64 saturation control changed")
    return {"degree": d, "default_strength": str(strength), "coarse_field_both": coarse_a.tolist(),
            "difference_coefficient_B_minus_A": str(coefficient), "default_parent_A": rounded(rows[0]),
            "default_parent_B": rounded(rows[1]), "default_parent_L2_gap": round(gap, 12),
            "matched_strength": str(tuned_strength), "matched_parent_A": rounded(tuned[0]),
            "matched_parent_B": rounded(tuned[1]), "matched_max_allowed_roundoff": 5e-15,
            "saturation_distinct_input_sizes": [1e8, 2e8],
            "saturation_common_binary64_row": saturation[0].tolist()}


if __name__ == "__main__":
    archived = load_source()
    result = {"source": SOURCE, "source_blob": SOURCE_BLOB, "numpy": np.__version__,
              "horizon": HORIZON, "arrival": arrival_checks(archived),
              "actual_selectors": strategy_checks(archived), "p1": grade_checks(archived),
              "status": "PASS", "domain": "prescribed finite fixtures using archived repair",
              "native_delivery": "NOT_DERIVED"}
    print(json.dumps(result, indent=2, sort_keys=True))
