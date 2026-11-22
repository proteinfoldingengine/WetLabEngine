"""Run the original work, carrier and connection routines on matched P1 inputs."""

from fractions import Fraction as Q
import hashlib
import importlib
import json
from pathlib import Path
import sys

from check_p1_grade_work import read_pinned, prune, projected, work_read


DEMOS = Path("ResearchHistory/UQCF-GEM/demos")
CORE = DEMOS / "v15.42-duality-covariant-transport-repair"
APP = DEMOS / "v15.43-certified-response-geometry"
PINS = {
    CORE / "exact_algebra.py": "c67ea42b61321469f7735ce589f2e729b241666a",
    CORE / "operational_complex.py": "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c",
    CORE / "fixtures.py": "9704660b4183f040c84a0734b52702258d1d42da",
    CORE / "protocol_types.py": "e90a98d17baa6028f0d50a165f0b9d0046de13a2",
    CORE / "transport.py": "df552284c16d43bc876340fbc13fe91eb9ee6a00",
    CORE / "holonomy.py": "bad3f06b291bb448a903b4f48344a9e54a633f68",
    APP / "projection.py": "f857f2cf1cd4c265c193121236af8e441b1f01dc",
    APP / "carriers.py": "5cd286b014bb44025e16832ee91a6e6665291c8c",
    APP / "application.py": "30348d71d366a751932ec2d58d18a9148d81ae83",
}
SIDE = 5
LABELS = tuple(range(SIDE * SIDE))
SITES = tuple((i,) for i in LABELS)
ROOT, PARENT, FIRST, SECOND = (), (0,), (0, 0), (0, 1)


def load_connection(out):
    identities = []
    for path, expected in PINS.items():
        data = path.read_bytes()
        blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        assert blob == expected, path
        (out / path.name).write_bytes(data)
        identities.append({"path": str(path), "blob": blob, "sha256": hashlib.sha256(data).hexdigest()})
    sys.path[:0] = [str(APP.resolve()), str(CORE.resolve())]
    modules = {}
    for path in PINS:
        module = importlib.import_module(path.stem)
        assert Path(module.__file__).resolve() == path.resolve(), path
        modules[path.stem] = module
    return modules, identities


def label(x, y):
    return (x % SIDE) + SIDE * (y % SIDE)


def corners(x, y):
    return (label(x, y), label(x + 1, y), label(x + 1, y + 1), label(x, y + 1))


def grade_family(tree, support, active_child):
    result = []
    for square in support:
        injected = {active_child if i == 0 else SITES[i] for i in square}
        grade = tuple(Q(5 - 4 * int(key == ROOT) + int(key in injected)) for key in tree.keys)
        assert min(grade) >= 1 and sum(grade) == 5 * len(tree.keys)
        result.append(grade)
    return tuple(result)


def exact_work(support, child_term):
    return tuple(tuple(Q(len(a ^ b) + child_term * int((0 in a) != (0 in b))) for b in support) for a in support)


def field_at_sites(tree, grade, background, engine):
    index = {key: i for i, key in enumerate(tree.keys)}
    parent = (-1, *(index[key[:-1]] for key in tree.keys[1:]))
    balance = tuple(a - b for a, b in zip(grade, background, strict=True))
    assert sum(balance) == 0
    values = engine.root_laplacian(parent).inv() * engine.sp.Matrix(balance[1:])
    return tuple(Q(str(values[index[site] - 1])) for site in SITES)


def payload(read, module):
    edges = tuple(sorted(tuple(sorted(edge)) for edge in read.neighbors))
    return module.Payload(SIDE, Q(1), read.labels, read.work, edges, ())


def rejection(build, data, expected):
    try:
        build(data)
    except ValueError as error:
        assert str(error) == expected, str(error)
        return str(error)
    raise AssertionError(f"carrier unexpectedly accepted, expected {expected}")


def independent_invariants(field):
    gx = {label(x, y): (field[label(x + 1, y)] - field[label(x - 1, y)]) / 2
          for x in range(SIDE) for y in range(SIDE)}
    gy = {label(x, y): (field[label(x, y + 1)] - field[label(x, y - 1)]) / 2
          for x in range(SIDE) for y in range(SIDE)}
    values = {}
    for x in range(SIDE):
        for y in range(SIDE):
            a, b, c, d = corners(x, y)
            omega = (gy[a] + gy[b] - gx[b] - gx[c] - gy[c] - gy[d] + gx[d] + gx[a]) / 4
            values[tuple(sorted((a, b, c, d)))] = omega**2
    return values


def single_address_controls(lineage, engine, archive, modules, retained):
    def probes(carrier, sites):
        return tuple(tuple(Q(5 + int(key == site) - int(key == ROOT)) for key in carrier.keys) for site in sites)

    build = modules["carriers"].build_carrier
    reads = work_read(retained, probes(retained, SITES), engine, archive)
    assert reads.minimum == 2 and len(reads.neighbors) == 300
    reject = rejection(build, payload(reads, modules["projection"]), "degree_not_four")
    small = lineage.Carrier("single-address-degree-control", (ROOT, *SITES[:5]))
    k5 = work_read(small, probes(small, SITES[:5]), engine, archive)
    assert k5.minimum == 2 and len(k5.neighbors) == 10
    complex_ = modules["operational_complex"].construct_operational_complex(k5.labels, k5.work, k5.neighbors)
    assert complex_.reason == "edge_cycle_count" and complex_.complex is None
    return {"25_rayed_star": reject, "5_rayed_degree_four_star": complex_.reason}


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    lineage, lineage_pin = read_pinned("lineage.py", out)
    engine, engine_pin = read_pinned("engine.py", out)
    archive, archive_pin = read_pinned("response_geometry.py", out)
    modules, extra_pins = load_connection(out)
    catalog_labels, _, archive_edges = modules["fixtures"].periodic_square_input(SIDE)
    assert catalog_labels == LABELS
    support = tuple(frozenset(corners(i % SIDE, i // SIDE)) for i in catalog_labels)
    fine = lineage.Carrier("periodic-grade-preparation-control", (ROOT, *SITES, FIRST, SECOND))
    cut = prune(lineage, fine, FIRST)
    last = prune(lineage, cut.coarse, SECOND)
    assert cut.ancestor(FIRST) == PARENT and last.ancestor(SECOND) == PARENT
    background = (Q(5),) * len(fine.keys)
    fine_work = {}
    effects = {}
    post = {}
    terminal_work = {}
    build = modules["carriers"].build_carrier
    proj = modules["projection"]
    for key, active_child in (("A", FIRST), ("B", SECOND)):
        grades = grade_family(fine, support, active_child)
        narrowed = projected(cut, grades)
        fine_work[key] = work_read(fine, grades, engine, archive)
        assert fine_work[key].work == exact_work(support, 1)
        assert archive.metric_passes(fine_work[key]) and len(fine_work[key].neighbors) == 42
        fine_rejection = rejection(build, payload(fine_work[key], proj), "degree_not_four")
        through = work_read(cut.coarse, narrowed, engine, archive)
        extra = int(active_child == SECOND)
        assert through.work == exact_work(support, extra)
        assert archive.metric_passes(through) and through.minimum == 4
        expected_field = tuple(Q(int(i in support[0])) for i in LABELS)
        before_field = field_at_sites(fine, grades[0], background, engine)
        after_field = field_at_sites(cut.coarse, narrowed[0], cut.aggregate(background), engine)
        assert before_field == after_field == expected_field
        assert grades[0][fine.keys.index(PARENT)] == 5
        after_grade = narrowed[0][cut.coarse.keys.index(PARENT)]
        assert after_grade == (11 if key == "A" else 10)
        terminal_grades = projected(last, narrowed)
        assert terminal_grades == projected(cut.then(last), grades)
        terminal_work[key] = work_read(last.coarse, terminal_grades, engine, archive)
        post[key] = through
        effects[key] = {"fine_edges": len(fine_work[key].neighbors), "fine_rejection": fine_rejection,
                        "post_edges": len(through.neighbors), "post_owner_grade": str(after_grade),
                        "fixed_field": list(map(str, after_field))}
    assert fine_work["A"] == fine_work["B"]
    assert terminal_work["A"] == terminal_work["B"] == post["A"]
    assert post["A"].neighbors == archive_edges and len(archive_edges) == 50
    cut_edges = frozenset(edge for edge in archive_edges if sum(0 in support[i] for i in edge) == 1)
    assert len(cut_edges) == 8 and fine_work["A"].neighbors == post["B"].neighbors == archive_edges - cut_edges
    effects["B"]["post_rejection"] = rejection(build, payload(post["B"], proj), "degree_not_four")

    approved = build(payload(post["A"], proj))
    assert approved.baseline.flat and approved.complex.tangent_rank == 2 and len(approved.complex.cycles) == 25
    evaluate = modules["application"].evaluate_field
    field = tuple(Q(value) for value in effects["A"]["fixed_field"])
    exact = evaluate(approved, field)
    actual_faces = {tuple(sorted(face)): invariant for face, matrix, invariant in exact.records}
    assert actual_faces == independent_invariants(field)
    fixed_face = tuple(sorted(corners(0, 0)))
    assert actual_faces[fixed_face] == 1
    constant = evaluate(approved, (Q(1),) * len(field))
    assert constant.zero_count == 25 and constant.invariant_sum == 0
    effects["A"]["post_acceptance"] = dict(approved.receipt)
    return {"source_pins": [lineage_pin, engine_pin, archive_pin, *extra_pins],
            "cases": effects, "same_initial_work_and_fixed_retained_field": True,
            "terminal_work_equal_after_second_pruning": True,
            "single_address_controls": single_address_controls(lineage, engine, archive, modules, cut.coarse),
            "cut_edges": sorted(sorted(edge) for edge in cut_edges),
            "loop": {"fixed_face": fixed_face, "fixed_face_invariant": str(actual_faces[fixed_face]),
                     "nonzero_count": exact.nonzero_count, "face_count": len(actual_faces),
                     "all_invariants": [[face, str(value)] for face, value in sorted(actual_faces.items())],
                     "constant_zero_count": constant.zero_count}}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1])), allow_nan=False, indent=2, sort_keys=True))
