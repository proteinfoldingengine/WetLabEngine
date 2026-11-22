"""Replay the frozen tree and patch comparisons and reconstruct the exact constraint ranks."""
import ast
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp


UQCF = "ResearchHistory/UQCF-GEM/"
V1641 = Path(UQCF + "demos/v16.41-unit-barrier-dichotomy")
V1642 = Path(UQCF + "demos/v16.42-overlapping-core-repair")
V1622 = Path(UQCF + "demos/v16.22-response-selection-closure/engine.py")
FCV = Path(UQCF + "foundational-closure-verification/lineage.py")
GEOMETRY = Path("Tmp/TOE/Einstein_13_V1720 retained_bridge_core")
V1712 = GEOMETRY / "v1712_rg.py"
V1713 = GEOMETRY / "v1713_shape_rg.py"
PINNED = {
    V1641 / "producer.py": "0ba44accc8f47359a8e5adfa9b6a5265dc3eb45d",
    V1641 / "verifier.py": "079b2189d4d06e583eeafd25860c2dba33ede673",
    V1642 / "producer.py": "980d34ec76370c2f220d29c1650ea8e010ce75a4",
    V1642 / "verifier.py": "3ed004d6748e36e72f765a22b5533ec187e954f9",
    V1622: "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    FCV: "e95e3e978779164dd91f09b80e3389247e6320c2",
    V1712: "bc4504edbde3bc35815959f7f52288a57dced81a",
    V1713: "db8828f17a1ae597ac09abc1a8ac23b3eb3b6676",
}
CASES = {
    "star": ((-1, 0, 0, 0, 0), (16, 4, 4)),
    "branching": ((-1, 0, 1, 1, 3), (7, 13, 8)),
    "chain": ((-1, 0, 1, 2, 3), (5, 20, 10)),
}
STARTS = ((21, 11), (29, 11))
LOADS = ((2, 3, 5, 7, 11), (3, 1, 2, 4, 8))


def git_blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def lineage_keys(parents):
    keys = [()]
    for child, parent in enumerate(parents[1:], start=1):
        keys.append(keys[parent] + (child,))
    return tuple(keys)


def actual_paths(root):
    path = root / V1642 / "producer.py"
    producer = load_module(path, "archived_normalizer")
    verifier = load_module(root / V1642 / "verifier.py", "archived_verifier")
    domain = ((0, 4),)
    result = producer.produce(domain=domain)
    verification = verifier.verify(result, domain=domain)
    assert verification["outcome"] == "FAMILY_THEOREM_VALIDATED"
    assert verification["normalizations"] == 50 and not verification["construction_failures"]
    entry, = result["entries"]
    graph = entry["graph"]
    profile, = graph["profiles"]
    parents = tuple(graph["parents"])
    assert parents == CASES["star"][0] and profile["q"] == [2, 0, 0, 0, 0]
    indices = {tuple(v): i for i, v in enumerate(graph["states"])}
    indexed_paths = {x["state"]: x["path"] for x in entry["normalizations"]}

    observations = []
    for initial in STARTS:
        events = []

        def track(frame, event, _):
            if event != "call" or frame.f_code.co_name != "setleaf" or frame.f_code.co_filename != str(path):
                return
            if frame.f_back.f_lineno == 29 and frame.f_locals["v"] == 2:
                masks = tuple(frame.f_locals["state"])
                assert frame.f_locals["target"] == 2
                events.append(masks)

        sys.setprofile(track)
        try:
            states = producer.normalization(parents, initial)
        finally:
            sys.setprofile(None)
        assert [indices[tuple(row)] for row in states] == indexed_paths[indices[initial]]
        at_call, = events
        assert states[-1] == [27, 29]
        observations.append({"initial": initial, "entry_masks": at_call, "path": states})
    assert [x["entry_masks"] for x in observations] == [(23, 9), (27, 13)]
    assert [bool(x["entry_masks"][1] & (1 << 2)) for x in observations] == [False, True]
    return parents, observations


def common_green_reads(lineage, green, parents, observations):
    keys = lineage_keys(parents)
    all_vertices = lineage.Carrier("four-leaf-star", keys)
    coarse = [
        tuple(i for i in range(len(keys)) if item["entry_masks"][1] & (1 << i))
        for item in observations
    ]
    common = sorted(set(coarse[0]).intersection(coarse[1]))
    assert common == [0, 3]
    reads = []
    projections = []
    for retained in coarse:
        keeper = lineage.Carrier(all_vertices.genesis, tuple(keys[i] for i in retained))
        push = lineage.Pruning(all_vertices, keeper)
        local_parents = (-1,) + tuple(retained.index(parents[i]) for i in retained[1:])
        inverse = green.root_laplacian(local_parents).inv()
        outputs = []
        initial_grades = []
        for load in LOADS:
            source = push.aggregate(load)
            initial_grades.append([int(sum(source)), int(source[retained.index(3)])])
            field = inverse * sp.Matrix(source[1:])
            outputs.append(str(field[retained.index(3) - 1]))
        reads.append(outputs)
        projections.append(initial_grades)
    assert projections == [[[28, 7], [18, 4]], [[28, 7], [18, 4]]]
    assert reads == [["7", "4"], ["7", "4"]]
    return {"common_vertices": common, "subtree_grades": projections, "edge_reads": reads}


def exact_dimensions(lineage, parents):
    keys = lineage_keys(parents)
    n = len(keys)
    fine = lineage.Carrier("constraint-reconstruction", keys)
    pairs = list(combinations(range(n), 2))
    variables = {(v, *pair): i for i, (v, pair) in enumerate((v, p) for v in range(n) for p in pairs)}
    standard = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    push_rows = set()
    section_rows = set()
    retained_count = 0
    for size in range(n):
        for nonroot in combinations(range(1, n), size):
            retained = (0, *nonroot)
            if any(parents[j] not in retained for j in nonroot):
                continue
            target = lineage.Carrier(fine.genesis, tuple(keys[j] for j in retained))
            p = lineage.Pruning(fine, target)
            columns = [p.aggregate(u) for u in standard]
            assert all(sum(col) == 1 for col in columns)
            owner = [retained[col.index(1)] for col in columns]
            removed = sorted(set(range(n)) - set(retained))
            retained_count += 1
            for j in removed:
                for pair in combinations(retained, 2):
                    row = [0] * len(variables)
                    row[variables[(j, *pair)]] = 1
                    section_rows.add(tuple(row))
                # e_j - e_owner is a kernel vector of the original extensive pushforward.
                for i in range(n):
                    for v in retained:
                        row = [0] * len(variables)
                        for out, out_owner in enumerate(owner):
                            if out_owner != v:
                                continue
                            for k, weight in ((j, 1), (owner[j], -1)):
                                if k == i:
                                    continue
                                lo, hi = sorted((k, i))
                                row[variables[(out, lo, hi)]] += weight if k < i else -weight
                        if any(row):
                            push_rows.add(tuple(row))
    rank_p = sp.Matrix(sorted(push_rows)).rank()
    rank_both = sp.Matrix(sorted(push_rows | section_rows)).rank()
    return (retained_count, len(variables) - rank_p, len(variables) - rank_both)


def patch_checks(root):
    namespaces = {}
    path = root / V1712
    original = path.read_bytes()
    definitions = b"".join(original.splitlines(keepends=True)[:60])
    exec(compile(definitions, str(path), "exec"), namespaces)
    transport = namespaces["native_T"]
    write = namespaces["rg_step"]
    n = 6
    g = Fraction(17, 100)
    basis = np.eye(n, dtype=int).astype(object)
    gain_columns = []
    for i in range(n):
        left, right = basis[i], basis[(i - 1) % n]
        combined, = write([left, right], g, transport)
        delta = [(x - y) / g**2 for x, y in zip(combined, left)]
        assert delta == list(left)
        gain_columns.append(delta)
    left = np.array([Fraction(i + 1, i + 2) for i in range(n)], dtype=object)
    parallel, = write([left, left], g, transport)
    blank, = write([left, np.zeros(n, dtype=object)], g, transport)
    assert list(parallel) == list(blank) == list(left)
    image_rank = sp.Matrix(gain_columns).rank()
    assert image_rank == n
    for member in (V1712, V1713):
        tree = ast.parse((root / member).read_bytes())
        sources = [a.name for node in ast.walk(tree) if isinstance(node, ast.Import) for a in node.names]
        assert sources == ["numpy"] and not any(isinstance(node, ast.ImportFrom) for node in ast.walk(tree))
        assert any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                   and node.func.attr == "normal" for node in ast.walk(tree))
    return {"basis_image_rank": image_rank, "blank_parallel_outputs_equal": True}


def main(root):
    for member, expected in PINNED.items():
        assert git_blob((root / member).read_bytes()) == expected, member
    lineage = load_module(root / FCV, "archived_lineage")
    green = load_module(root / V1622, "archived_green")
    parents, observations = actual_paths(root)
    dimensions = {}
    for name, (shape, expected) in CASES.items():
        dimensions[name] = exact_dimensions(lineage, shape)
        assert dimensions[name] == expected
    return {
        "dimensions_retained_p1_p1_and_section": dimensions,
        "historical_observations": observations,
        "matched_common_port_control": common_green_reads(lineage, green, parents, observations),
        "patch_write": patch_checks(root),
        "source_blobs": {str(path): sha for path, sha in PINNED.items()},
    }


if __name__ == "__main__":
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[5]
    print(json.dumps(main(repo), sort_keys=True, indent=2))
