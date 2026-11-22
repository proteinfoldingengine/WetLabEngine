"""Evaluate inherited work geometry on exact P1 source contrasts."""

from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


SOURCES = {
    "lineage.py": (
        "ResearchHistory/UQCF-GEM/foundational-closure-verification/lineage.py",
        "e95e3e978779164dd91f09b80e3389247e6320c2",
    ),
    "engine.py": (
        "ResearchHistory/UQCF-GEM/demos/v16.22-response-selection-closure/engine.py",
        "9b71ce47bbef83132f00270f8a9a19e7721864d6",
    ),
    "response_geometry.py": (
        "ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py",
        "9128c24b695c1b539ac60dc93aeaf0bd4795c57b",
    ),
}
ROOT, PARENT, REMOTE_PARENT, REFERENCE = (), (0,), (1,), (2,)
LOCAL_LEAF, REMOTE_LEAF = (0, 0), (1, 0)


def read_pinned(name, out):
    path, expected = SOURCES[name]
    data = Path(path).read_bytes()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    assert blob == expected
    (out / name).write_bytes(data)
    spec = importlib.util.spec_from_file_location("original_" + Path(name).stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, {"path": path, "blob": blob, "sha256": hashlib.sha256(data).hexdigest()}


def prune(lineage, fine, target):
    retained = lineage.Carrier(fine.genesis, tuple(key for key in fine.keys if key != target))
    return lineage.Pruning(fine, retained)


def shift(keys, base, positive, negative, value=F(1)):
    return tuple(x + value * (int(key == positive) - int(key == negative)) for x, key in zip(base, keys, strict=True))


def subtree_contrast(keys, first, second, v):
    return sum(a - b for key, a, b in zip(keys, first, second, strict=True) if key[:len(v)] == v)


def work_read(carrier, grades, engine, archive):
    keys = carrier.keys
    position = {key: i for i, key in enumerate(keys)}
    assert keys[0] == ROOT and len(set(map(sum, grades))) == 1
    parents = (-1, *(position[key[:-1]] for key in keys[1:]))
    green = engine.root_laplacian(parents).inv()
    reference = grades[0]
    responses = []
    for source in grades:
        balanced = tuple(a - b for a, b in zip(source, reference, strict=True))
        result = green * engine.sp.Matrix(balanced[1:])
        responses.append((F(0), *(F(str(value)) for value in result)))
    answer = archive.construct_response_geometry(tuple(range(len(grades))), grades, responses)
    for i, j in product(range(len(grades)), repeat=2):
        expected = sum(subtree_contrast(keys, grades[i], grades[j], v)**2 for v in keys[1:])
        assert answer.work[i][j] == expected
    return answer


def projected(pruning, grades):
    return tuple(pruning.aggregate(source) for source in grades)


def check_loss(pruning, grades, fine_work, retained_work):
    dropped = set(pruning.fine.keys) - set(pruning.coarse.keys)
    for i, j in product(range(len(grades)), repeat=2):
        expected = sum(subtree_contrast(pruning.fine.keys, grades[i], grades[j], v)**2 for v in dropped)
        assert fine_work.work[i][j] - retained_work.work[i][j] == expected


def result_row(result):
    return {"work": [[str(value) for value in row] for row in result.work],
            "minimum": str(result.minimum), "nearest_pairs": sorted(sorted(pair) for pair in result.neighbors),
            "separated": result.separated, "triangle": result.triangle}


def check_fixture(result, work, neighbor, archive):
    assert (result.work[0][1], result.work[0][2], result.work[1][2]) == work
    assert result.neighbors == frozenset((frozenset(neighbor),))
    assert archive.metric_passes(result)


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    lineage, lineage_pin = read_pinned("lineage.py", out)
    engine, engine_pin = read_pinned("engine.py", out)
    archive, archive_pin = read_pinned("response_geometry.py", out)
    keys = (ROOT, PARENT, REMOTE_PARENT, REFERENCE, LOCAL_LEAF, REMOTE_LEAF)
    fine = lineage.Carrier("same-Genesis-work-control", keys)
    fine_grade = (F(2),) * len(keys)
    third = shift(keys, fine_grade, REFERENCE, ROOT, F(5, 4))
    families = {
        "L": (fine_grade, shift(keys, fine_grade, LOCAL_LEAF, ROOT), third),
        "R": (fine_grade, shift(keys, fine_grade, REMOTE_LEAF, ROOT), third),
    }
    assert all(min(g) > 0 and sum(g) == 12 for family in families.values() for g in family)
    local = prune(lineage, fine, LOCAL_LEAF)
    remote = prune(lineage, fine, REMOTE_LEAF)
    assert local.ancestor(LOCAL_LEAF) == PARENT and remote.ancestor(REMOTE_LEAF) == REMOTE_PARENT
    operands = {"L": {}, "R": {}}
    short = (F(1), F(25, 16), F(41, 16))
    long = (F(2), F(25, 16), F(57, 16))
    for name, grades in families.items():
        initial = work_read(fine, grades, engine, archive)
        assert grades[1][fine.keys.index(PARENT)] == 2
        check_fixture(initial, long, (0, 2), archive)
        operands[name]["fine"] = result_row(initial)
        endpoints = []
        for event, first, last_leaf in (("local", local, REMOTE_LEAF), ("remote", remote, LOCAL_LEAF)):
            narrowed = projected(first, grades)
            after = work_read(first.coarse, narrowed, engine, archive)
            check_loss(first, grades, initial, after)
            changes = (event == "local" and name == "L") or (event == "remote" and name == "R")
            check_fixture(after, short if changes else long, (0, 1) if changes else (0, 2), archive)
            operands[name][event] = result_row(after)
            if event == "local":
                owner = narrowed[1][first.coarse.keys.index(PARENT)]
                assert owner == (5 if name == "L" else 4)
                operands[name][event]["owner_grade"] = str(owner)
            second = prune(lineage, first.coarse, last_leaf)
            final_grades = projected(second, narrowed)
            composite = first.then(second)
            assert final_grades == projected(composite, grades)
            final = work_read(second.coarse, final_grades, engine, archive)
            check_fixture(final, short, (0, 1), archive)
            check_loss(second, narrowed, after, final)
            check_loss(composite, grades, initial, final)
            endpoints.append(final)
            operands[name]["terminal_after_" + event] = result_row(final)
        assert endpoints[0] == endpoints[1]
    assert operands["L"]["fine"] == operands["R"]["fine"]
    assert operands["L"]["terminal_after_local"] == operands["R"]["terminal_after_local"]

    collapsed = (fine_grade, shift(keys, fine_grade, LOCAL_LEAF, PARENT))
    before = work_read(fine, collapsed, engine, archive)
    after = work_read(local.coarse, projected(local, collapsed), engine, archive)
    check_loss(local, collapsed, before, after)
    assert before.work[0][1] == 1 and after.work[0][1] == 0 and not after.separated
    assert projected(local, collapsed)[0] == projected(local, collapsed)[1]
    return {"source_pins": [lineage_pin, engine_pin, archive_pin], "fine_keys": keys,
            "local_deleted_leaf": LOCAL_LEAF, "local_owner": PARENT, "remote_deleted_leaf": REMOTE_LEAF,
            "families": operands, "within_fiber_control": {"fine": result_row(before), "coarse": result_row(after)}}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
