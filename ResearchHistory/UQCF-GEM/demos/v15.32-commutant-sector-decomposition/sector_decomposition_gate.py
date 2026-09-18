from __future__ import annotations

from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space"
V1531 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.31-source-extension-minimality"
BASE_SHA = "d2b767c88a4bdb3d750d7bb696b29b4fbd34dca1"

UPSTREAM_PINS = {
    "v15.28/representation_actions.py": (
        V1528 / "representation_actions.py",
        "7260147cd6ca47ec21634172b44b98de726904af",
    ),
    "v15.28/exact_linear.py": (
        V1528 / "exact_linear.py",
        "05cc1b8cfec70d501408377b5e44190b259a4514",
    ),
    "v15.31/source_extension_gate.py": (
        V1531 / "source_extension_gate.py",
        "4a5be8970bad772eb0902a9f34f3499253a08bc9",
    ),
    "v15.31/RESULTS.json": (
        V1531 / "docs/RESULTS.json",
        "bec3ffbe08eb29e9e22738eec8104cd35bfbdb47",
    ),
}


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def verify_upstream_pins() -> dict[str, str]:
    out = {}
    for key, (path, expected) in UPSTREAM_PINS.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"upstream pin drift: {key}: {actual}")
        out[key] = actual
    return out


def load_upstream():
    verify_upstream_pins()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    actions = importlib.import_module("representation_actions")
    ql = importlib.import_module("exact_linear")
    return actions, ql


def signed_trace(action) -> int:
    return sum(
        int(s)
        for i, (j, s) in enumerate(zip(action.image, action.sign))
        if i == j
    )


def _identity(n: int):
    return tuple(
        tuple(Fraction(1 if i == j else 0) for j in range(n))
        for i in range(n)
    )


def _zero(n: int):
    return tuple(tuple(Fraction(0) for _ in range(n)) for _ in range(n))


def _add(*mats):
    n = len(mats[0])
    return tuple(
        tuple(sum((m[i][j] for m in mats), Fraction(0)) for j in range(n))
        for i in range(n)
    )


def _scale(s, mat):
    s = Fraction(s)
    return tuple(tuple(s * x for x in row) for row in mat)


def face_projectors(c):
    faces = c.faces
    n = len(faces)
    if n != 49:
        raise AssertionError("v15.32 is frozen to the inherited 7x7 face set")

    def matrix_for(kind):
        rows = []
        for i, (xi, yi) in enumerate(faces):
            row = []
            for j, (xj, yj) in enumerate(faces):
                if kind == "constant":
                    value = Fraction(1, 49)
                elif kind == "x":
                    value = Fraction(1, 7) if xi == xj else Fraction(0)
                elif kind == "y":
                    value = Fraction(1, 7) if yi == yj else Fraction(0)
                elif kind == "plus":
                    value = Fraction(1, 7) if (xi + yi) % 7 == (xj + yj) % 7 else Fraction(0)
                elif kind == "minus":
                    value = Fraction(1, 7) if (xi - yi) % 7 == (xj - yj) % 7 else Fraction(0)
                else:
                    raise KeyError(kind)
                row.append(value)
            rows.append(tuple(row))
        return tuple(rows)

    p0 = matrix_for("constant")
    px = matrix_for("x")
    py = matrix_for("y")
    pp = matrix_for("plus")
    pm = matrix_for("minus")
    ident = _identity(n)

    axis = _add(px, py, _scale(-2, p0))
    diagonal = _add(pp, pm, _scale(-2, p0))
    generic = _add(ident, _scale(-1, px), _scale(-1, py),
                   _scale(-1, pp), _scale(-1, pm), _scale(3, p0))
    augmentation = _add(ident, _scale(-1, p0))
    return {
        "constant": p0,
        "axis": axis,
        "diagonal": diagonal,
        "generic": generic,
        "augmentation": augmentation,
    }


def projector_checks(c, actions, ql):
    p = face_projectors(c)
    zero = _zero(49)
    names = ("axis", "diagonal", "generic")
    for name in names:
        if ql.matmul(p[name], p[name]) != p[name]:
            raise ArithmeticError(f"{name} projector not idempotent")
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if ql.matmul(p[a], p[b]) != zero or ql.matmul(p[b], p[a]) != zero:
                raise ArithmeticError(f"{a}/{b} projectors not orthogonal")
    if _add(p["axis"], p["diagonal"], p["generic"]) != p["augmentation"]:
        raise ArithmeticError("projectors do not resolve face augmentation")

    ranks = {name: ql.rank(p[name]) for name in names}
    if ranks != {"axis": 12, "diagonal": 12, "generic": 24}:
        raise ArithmeticError(f"unexpected projector ranks: {ranks}")

    group = actions.torus_automorphisms(c.L)
    for g in group:
        fa = actions.face_action(c, g)
        for name in names:
            mat = p[name]
            for i in range(49):
                for j in range(49):
                    if mat[fa.image[i]][fa.image[j]] != Fraction(fa.sign[i] * fa.sign[j]) * mat[i][j]:
                        raise ArithmeticError(f"{name} projector fails G-commutation")

    b2 = ql.matrix(tuple(tuple(int(x) for x in row) for row in c.B2.astype(int)))
    image_ranks = {}
    for name in names:
        image_ranks[name] = ql.rank(ql.matmul(b2, p[name]))
        if image_ranks[name] != ranks[name]:
            raise ArithmeticError(f"B2 not injective on {name}")

    if ql.rank(b2) != 48:
        raise ArithmeticError("unexpected B2 rank")

    return p, ranks, image_ranks


def homology_checks(c, actions, ql):
    h = tuple(Fraction(1 if kind == "h" else 0) for _u, _v, kind in c.edges)
    v = tuple(Fraction(1 if kind == "v" else 0) for _u, _v, kind in c.edges)
    b1 = ql.matrix(tuple(tuple(int(x) for x in row) for row in c.B1.astype(int)))
    if any(ql.matvec(b1, h)) or any(ql.matvec(b1, v)):
        raise ArithmeticError("uniform homology generators are not cycles")

    group = actions.torus_automorphisms(c.L)
    ident = ((1, 0), (0, 1))
    translations = tuple(g for g in group if g.matrix == ident)
    if len(translations) != 49:
        raise ArithmeticError("translation subgroup size changed")
    edge_orbits = set()
    for i in range(len(c.edges)):
        orbit = frozenset(actions.edge_action(c, g).image[i] for g in translations)
        edge_orbits.add(orbit)
        if any(actions.edge_action(c, g).sign[i] != 1 for g in translations):
            raise ArithmeticError("translation unexpectedly reverses edge")
    if len(edge_orbits) != 2:
        raise ArithmeticError("translation-fixed edge space is not two-dimensional")
    for g in translations:
        ea = actions.edge_action(c, g)
        if ea.apply(h) != h or ea.apply(v) != v:
            raise ArithmeticError("homology generators not translation fixed")

    b2 = tuple(tuple(Fraction(int(x)) for x in row) for row in c.B2.astype(int))
    augmented_rows = tuple(
        tuple(b2[e][f] for f in range(49)) + (h[e], v[e])
        for e in range(len(c.edges))
    )
    if ql.rank(augmented_rows) != 50:
        raise ArithmeticError("boundary plus homology direct sum failed")
    return h, v


def trace_projected_action(projector, action) -> Fraction:
    return sum(
        (Fraction(action.sign[i]) * projector[i][action.image[i]] for i in range(len(action.image))),
        Fraction(0),
    )


def sector_characters(c, actions, projectors):
    group = actions.torus_automorphisms(c.L)
    chars = {"homology": {}, "axis": {}, "diagonal": {}, "generic": {}}
    for g in group:
        fa = actions.face_action(c, g)
        chars["homology"][g] = Fraction(g.matrix[0][0] + g.matrix[1][1])
        for name in ("axis", "diagonal", "generic"):
            chars[name][g] = trace_projected_action(projectors[name], fa)

        total = sum((chars[name][g] for name in chars), Fraction(0))
        ez = signed_trace(actions.edge_action(c, g)) - (signed_trace(actions.vertex_action(c, g)) - 1)
        if total != ez:
            raise ArithmeticError("sector characters do not recover v15.31 cycle character")
    return chars


def hom_dimension(c1: dict, c2: dict) -> int:
    if set(c1) != set(c2) or not c1:
        raise ValueError("character domains differ")
    value = sum((c1[g] * c2[g] for g in c1), Fraction(0)) / len(c1)
    if value.denominator != 1:
        raise ArithmeticError("nonintegral Hom dimension")
    return int(value)


def sector_hom_matrix(chars):
    names = ("homology", "axis", "diagonal", "generic")
    matrix = {
        a: {b: hom_dimension(chars[a], chars[b]) for b in names}
        for a in names
    }
    expected_diag = {"homology": 1, "axis": 3, "diagonal": 3, "generic": 3}
    diag = {name: matrix[name][name] for name in names}
    cross_zero = all(matrix[a][b] == 0 for a in names for b in names if a != b)
    if diag != expected_diag or not cross_zero:
        raise ArithmeticError(f"unexpected sector Hom structure: {matrix}")
    if sum(diag.values()) != 10:
        raise ArithmeticError("sector End dimensions do not recover v15.31")
    return matrix, diag, cross_zero


def _d4_apply(m, k):
    return (
        (m[0][0] * k[0] + m[0][1] * k[1]) % 7,
        (m[1][0] * k[0] + m[1][1] * k[1]) % 7,
    )


def momentum_orbit_audit(actions):
    nonzero = {(x, y) for x in range(7) for y in range(7) if (x, y) != (0, 0)}
    unseen = set(nonzero)
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset(_d4_apply(m, seed) for m in actions.D4)
        orbits.append(orbit)
        unseen -= orbit
    if len(orbits) != 9 or set().union(*orbits) != nonzero:
        raise ArithmeticError("unexpected D4 momentum orbit decomposition")

    def classify(orbit):
        if any(x == 0 or y == 0 for x, y in orbit):
            return "axis"
        if any((x - y) % 7 == 0 or (x + y) % 7 == 0 for x, y in orbit):
            return "diagonal"
        return "generic"

    data = []
    lookup = {}
    for idx, orbit in enumerate(orbits):
        typ = classify(orbit)
        size = len(orbit)
        stabilizer = 8 // size
        row = {
            "representative": list(min(orbit)),
            "type": typ,
            "orbit_size": size,
            "stabilizer_size": stabilizer,
        }
        data.append(row)
        lookup[orbit] = idx

    summary = {}
    for typ in ("axis", "diagonal", "generic"):
        sizes = sorted(row["orbit_size"] for row in data if row["type"] == typ)
        summary[typ] = {"count": len(sizes), "orbit_sizes": sizes}

    expected = {
        "axis": {"count": 3, "orbit_sizes": [4, 4, 4]},
        "diagonal": {"count": 3, "orbit_sizes": [4, 4, 4]},
        "generic": {"count": 3, "orbit_sizes": [8, 8, 8]},
    }
    if summary != expected:
        raise ArithmeticError(f"unexpected orbit types: {summary}")

    # Multiplication by F_7^* is the exact Galois action on seventh-root
    # character labels. Count connected components of D4 orbits under it.
    orbit_index = {}
    for idx, orbit in enumerate(orbits):
        for point in orbit:
            orbit_index[point] = idx

    galois_groups_by_type = {}
    for typ in ("axis", "diagonal", "generic"):
        ids = {i for i, row in enumerate(data) if row["type"] == typ}
        remaining = set(ids)
        components = 0
        while remaining:
            start = min(remaining)
            seed = tuple(data[start]["representative"])
            component = set()
            for a in range(1, 7):
                p = ((a * seed[0]) % 7, (a * seed[1]) % 7)
                component.add(orbit_index[p])
            if not component <= ids:
                raise ArithmeticError("Galois scaling changed orbit type")
            remaining -= component
            components += 1
        galois_groups_by_type[typ] = components

    if galois_groups_by_type != {"axis": 1, "diagonal": 1, "generic": 1}:
        raise ArithmeticError("unexpected rational/Galois grouping")

    data = sorted(data, key=lambda r: (r["type"], r["representative"]))
    return data, summary, galois_groups_by_type


def audit() -> dict:
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(7)
    group = actions.torus_automorphisms(c.L)
    if len(group) != 392:
        raise AssertionError("group order changed")

    projectors, ranks, boundary_ranks = projector_checks(c, actions, ql)
    homology_checks(c, actions, ql)
    chars = sector_characters(c, actions, projectors)
    hom_matrix, self_end, cross_zero = sector_hom_matrix(chars)
    orbit_rows, orbit_summary, galois_groups = momentum_orbit_audit(actions)

    char_hist = {
        name: {str(k): v for k, v in sorted(Counter(int(x) for x in chars[name].values()).items())}
        for name in chars
    }

    dims = {"homology": 2, "axis": ranks["axis"], "diagonal": ranks["diagonal"], "generic": ranks["generic"]}
    direct_sum = sum(dims.values()) == 50 and sum(boundary_ranks.values()) == 48
    if not direct_sum:
        raise ArithmeticError("sector dimensions do not sum to Z")

    splitting_count = 1 + len(orbit_rows)
    multiplicity_free = splitting_count == 10 and sum(row["orbit_size"] for row in orbit_rows) == 48
    if not multiplicity_free:
        status = "CANONICAL_MACRO_SECTORS_WITH_RESIDUAL_MULTIPLICITY"
        mixing_dim = 10 - splitting_count
    else:
        status = "MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS"
        mixing_dim = 0

    return {
        "version": "v15.32",
        "base_sha": BASE_SHA,
        "status": status,
        "group_order": len(group),
        "dim_Z": 50,
        "rational_macro_sector_count": 4,
        "rational_macro_sector_dimensions": dims,
        "projector_checks_exact": True,
        "projector_ranks": ranks,
        "boundary_image_ranks": boundary_ranks,
        "translation_fixed_homology_dimension": 2,
        "direct_sum_verified": direct_sum,
        "sector_character_histograms": char_hist,
        "sector_hom_dimension_matrix": hom_matrix,
        "sector_self_end_dimensions": self_end,
        "cross_sector_hom_zero": cross_zero,
        "recovered_total_commutant_dimension": sum(self_end.values()),
        "nonzero_momentum_orbit_count": len(orbit_rows),
        "momentum_orbits": orbit_rows,
        "momentum_orbits_by_type": orbit_summary,
        "galois_groups_by_type": galois_groups,
        "rational_boundary_macro_sector_count": 3,
        "splitting_field_sector_count": splitting_count,
        "splitting_field_sector_dimensions": [2] + sorted(row["orbit_size"] for row in orbit_rows),
        "multiplicity_free_over_splitting_field": multiplicity_free,
        "multiplicity_free_basis": (
            "ONE_TRANSLATION_CHARACTER_PER_FACE_MODE_PLUS_D4_ORBIT_LITTLE_GROUP_CLASSIFICATION"
        ),
        "residual_weight_dimension": splitting_count,
        "projective_relative_weight_dimension": splitting_count - 1,
        "mixing_freedom_dimension": mixing_dim,
        "unique_canonical_source_sector": splitting_count == 1,
        "upstream_pins": verify_upstream_pins(),
        "new_source_semantics_axiom_added": False,
        "coupling_solver_reopened": False,
        "gravity_observables_evaluated": False,
        "uses_holonomy_selector": False,
        "uses_newton_or_gr": False,
        "uses_metric_selector": False,
        "uses_pruning_as_selector": False,
        "uses_entropy_as_selector": False,
        "uses_physical_time": False,
        "scientific_breakthrough": False,
        "signal_of_life": False,
        "physical_gravity_derived": False,
        "Pillar_3": "OPEN",
        "next_required_object": (
            "INDEPENDENT_PRETIME_PRINCIPLE_FIXING_RELATIVE_WEIGHTS_OR_RELATIONS_"
            "AMONG_THE_10_MULTIPLICITY_FREE_SECTORS"
        ),
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out")
    p.add_argument("--check")
    args = p.parse_args()
    text = canonical_json(audit())
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    if args.check:
        if Path(args.check).read_text() != text:
            raise SystemExit("committed v15.32 result differs from regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
