"""Replay common-grade P1 views through the original archive work gate."""

from collections import Counter
import hashlib
import importlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

from check_p1_grade_work import read_pinned, work_read


DEMOS = Path("ResearchHistory/UQCF-GEM/demos")
CORE = DEMOS / "v15.42-duality-covariant-transport-repair"
PINS = {
    CORE / "exact_algebra.py": "c67ea42b61321469f7735ce589f2e729b241666a",
    CORE / "operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    CORE / "fixtures.py": "9704660b4183f040c84a0734b52702258d1d42da",
    DEMOS / "v16.23-overlap-descent/PROOFS.md": "0c8223367caf4d81dd1fe5a33a4e94d092f1aac4",
}
SIDE = 5
AXIS = range(SIDE)
SITES = tuple(range(SIDE * SIDE))
ROOT = ()


def label(x, y):
    return x % SIDE + SIDE * (y % SIDE)


def load_original(out):
    pinned = {}
    identities = []
    for name in ("lineage.py", "engine.py", "response_geometry.py"):
        pinned[name], identity = read_pinned(name, out)
        identities.append(identity)
    for path, expected in PINS.items():
        data = path.read_bytes()
        blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        assert blob == expected, path
        name = "overlap_PROOFS.md" if path.suffix == ".md" else path.name
        (out / name).write_bytes(data)
        identities.append({"path": str(path), "blob": blob, "sha256": hashlib.sha256(data).hexdigest()})
    sys.path.insert(0, str(CORE.resolve()))
    for name in ("exact_algebra", "operational_complex", "fixtures"):
        module = importlib.import_module(name)
        assert Path(module.__file__).resolve() == (CORE / (name + ".py")).resolve()
        pinned[name] = module
    return pinned, identities


def sorted_masks(masks):
    return tuple(sorted(masks, key=lambda mask: (len(mask), tuple(sorted(mask)))))


def meet_closure(masks):
    catalog = set(masks)
    while True:
        expanded = catalog | {a & b for a, b in combinations(catalog, 2)}
        if expanded == catalog:
            return catalog
        catalog = expanded


def prepare_views(lineage, squares, vertical, horizontal, catalog):
    fine = lineage.Carrier("common-Genesis-meet-work-fixture", (ROOT, *((i,) for i in SITES)))
    grade = (1,) * len(fine.keys)
    prunes = {
        mask: lineage.Pruning(
            fine, lineage.Carrier(fine.genesis, (ROOT, *((i,) for i in sorted(mask))))
        )
        for mask in set(catalog) | set(vertical) | set(horizontal)
    }
    square_grades = {}
    for i, mask in enumerate(squares):
        target = prunes[mask].coarse
        v, h = prunes[vertical[i % SIDE]], prunes[horizontal[i // SIDE]]
        from_vertical, from_horizontal = lineage.Pruning(v.coarse, target), lineage.Pruning(h.coarse, target)
        assert v.then(from_vertical) == h.then(from_horizontal) == prunes[mask]
        square_grades[mask] = from_vertical.aggregate(v.aggregate(grade))
        assert square_grades[mask] == from_horizontal.aggregate(h.aggregate(grade))

    embedded = {}
    for mask, prune in prunes.items():
        direct = prune.aggregate(grade)
        projected = square_grades.get(mask, direct)
        assert projected == direct
        retained = dict(zip(prune.coarse.keys, projected, strict=True))
        embedded[mask] = tuple(retained.get(key, 0) for key in fine.keys)
        assert embedded[mask] == (len(grade) - len(mask), *(int(i in mask) for i in SITES))
    return fine, embedded


def evaluate(masks, grade_view, fine, original, expected_edges, expected_min, expected_reason):
    work = work_read(fine, tuple(grade_view[mask] for mask in masks),
                     original["engine.py"], original["response_geometry.py"])
    assert original["response_geometry.py"].metric_passes(work)
    for i, j in product(range(len(masks)), repeat=2):
        assert work.work[i][j] == len(masks[i] ^ masks[j])
    assert work.minimum == expected_min
    assert work.neighbors == expected_edges
    geometry = original["operational_complex"].construct_operational_complex(
        work.labels, work.work, work.neighbors
    )
    assert geometry.reason == expected_reason
    degrees = Counter(label for edge in work.neighbors for label in edge)
    cert = {
        "masks_in_label_order": [sorted(mask) for mask in masks],
        "nearest_pairs": sorted(sorted(pair) for pair in work.neighbors),
        "views": len(masks),
        "minimum": int(work.minimum),
        "nearest_edge_count": len(work.neighbors),
        "degree_counts": dict(Counter(degrees[i] for i in work.labels)),
        "separated_metric": True,
        "unordered_pair_count": work.pair_count,
        "gate_status": geometry.status.value,
        "gate_reason": geometry.reason,
    }
    if expected_reason is None:
        assert geometry.status.value == "IDENTIFIABLE"
        complex_ = geometry.complex
        assert complex_.tangent_rank == 2 and len(complex_.cycles) == 25
        for neighbors in complex_.adjacency:
            pairs = sorted(work.work[a][b] for a, b in combinations(neighbors, 2))
            assert pairs == [6, 6, 6, 6, 8, 8]
        cert.update({"tangent_rank": complex_.tangent_rank, "face_count": len(complex_.cycles),
                     "neighbor_pair_works": [6, 6, 6, 6, 8, 8]})
    else:
        assert geometry.status.value == "NOT_IDENTIFIABLE" and geometry.complex is None
    return cert


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    original, pins = load_original(out)
    vertical = tuple(frozenset(label(x + dx, y) for dx in (0, 1) for y in AXIS) for x in AXIS)
    horizontal = tuple(frozenset(label(x, y + dy) for dy in (0, 1) for x in AXIS) for y in AXIS)
    squares = tuple(v & h for h in horizontal for v in vertical)
    strips = vertical + horizontal
    assert len(set(squares)) == 25 and len(set(strips)) == 10

    labels, _, expected_square_edges = original["fixtures"].periodic_square_input(SIDE)
    assert labels == SITES
    shared_sides = {squares[a] & squares[b] for a, b in expected_square_edges}
    assert shared_sides == set(expected_square_edges)
    assert len(shared_sides) == 50
    assert all(len(side) == 2 for side in shared_sides)
    one_side = squares[0] & squares[1]
    assert one_side == frozenset((1, 6))
    noncorner = (frozenset(),) + tuple(frozenset((i,)) for i in SITES) + sorted_masks(shared_sides)
    algebraic_closure = meet_closure(squares)
    assert len(algebraic_closure) == 101
    assert algebraic_closure == set(squares) | set(noncorner)
    closed = squares + noncorner
    position = {mask: i for i, mask in enumerate(closed)}
    closed_edge_masks = [(frozenset(), frozenset((i,))) for i in SITES]
    closed_edge_masks += [(frozenset((i,)), side) for side in shared_sides for i in side]
    closed_edges = frozenset(frozenset((position[a], position[b])) for a, b in closed_edge_masks)
    assert len(closed_edges) == 125
    assert all(sum(side < square for square in squares) == 2 for side in shared_sides)

    fine, prepared = prepare_views(original["lineage.py"], squares, vertical, horizontal, closed)
    added_side_edges = frozenset((frozenset((0, len(squares))), frozenset((1, len(squares)))))
    cases = {
        "squares_only": (squares, expected_square_edges, 4, None, {4: 25}),
        "including_strips": (
            squares + strips, expected_square_edges, 4, "degree_not_four", {4: 25, 0: 10}
        ),
        "including_one_side": (
            squares + (one_side,), added_side_edges, 2, "degree_not_four", {1: 2, 2: 1, 0: 23}
        ),
        "including_all_meets": (closed, closed_edges, 1, "degree_not_four", {0: 25, 2: 50, 5: 25, 25: 1}),
    }
    results = {}
    for name, (masks, edges, minimum, reason, degrees) in cases.items():
        result = evaluate(masks, prepared, fine, original, edges, minimum, reason)
        assert result["degree_counts"] == degrees
        results[name] = result
    return {
        "pinned_sources": pins,
        "ambient_grade": [1] * len(fine.keys),
        "ambient_leaf_count": len(SITES),
        "compositions_verified_in_both_orders": len(squares),
        "individual_shared_sides_that_lower_the_minimum": len(shared_sides),
        "cases": results,
    }


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
