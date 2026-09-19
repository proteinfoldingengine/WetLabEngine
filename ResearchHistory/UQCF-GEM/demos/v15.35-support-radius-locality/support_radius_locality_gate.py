from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space"
V1534 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.34-canonical-adjacency-commutant"
BASE_SHA = "e24b94fb1a0ca4c8eda33379f5a4ab3f4c360487"

EVIDENCE = {
    "representation_actions.py": (
        V1528 / "representation_actions.py",
        "7260147cd6ca47ec21634172b44b98de726904af",
        (),
    ),
    "exact_linear.py": (
        V1528 / "exact_linear.py",
        "05cc1b8cfec70d501408377b5e44190b259a4514",
        (),
    ),
    "v15.34-results": (
        V1534 / "docs/RESULTS.json",
        "105cf29c5288d5dd7ffc8ebaa8c67ff8b1de88fd",
        ("FULL_COMMUTANT_GENERATED_BY_CANONICAL_ADJACENCY_FUNCTION_UNSELECTED",),
    ),
    "v13.15-locality": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.15/REPORT.md",
        "f232b345e0bf3ab1ff03fdac354f504869b4be73",
        (
            "generic bounded-neighborhood QMAR: **NO-GO**",
            "Markov/commuting structure from ontology: **NOT DERIVED**",
        ),
    ),
    "v13.18-locality": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.18/REPORT.md",
        "bd1989fe36f3936a0065a9cd11291245917dbc03",
        (
            "ETL tangent locality: **CLOSED EXPLICIT / CONDITIONAL**",
            "O(||P|| sqrt(CMI))",
        ),
    ),
    "v15.03-source-locality": (
        REPO_ROOT / "docs/superpowers/specs/2026-09-13-v1503-graph-site-source-lift-design.md",
        "d7e7a081f1913a10cf545fbed5d5e0f6aade20fa",
        (
            "site-local source covariance/locality results",
            "conditional commuting-Markov locality theorem",
        ),
    ),
}


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


def verify_evidence() -> dict[str, str]:
    out = {}
    for key, (path, expected, phrases) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"evidence drift: {key}: {actual}")
        text = path.read_text()
        missing = [p for p in phrases if p not in text]
        if missing:
            raise AssertionError(f"missing evidence phrase {key}: {missing}")
        out[key] = actual
    return out


def load_upstream():
    verify_evidence()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module("representation_actions"), importlib.import_module("exact_linear")


def addmat(*mats):
    if not mats:
        raise ValueError("need matrices")
    r, c = len(mats[0]), len(mats[0][0])
    return tuple(
        tuple(sum((Fraction(m[i][j]) for m in mats), Fraction(0)) for j in range(c))
        for i in range(r)
    )


def scalemat(a, m):
    a = Fraction(a)
    return tuple(tuple(a * Fraction(x) for x in row) for row in m)


def lincomb(coeffs, mats):
    if len(coeffs) != len(mats):
        raise ValueError("coefficient/matrix mismatch")
    out = scalemat(0, mats[0])
    for c, m in zip(coeffs, mats):
        out = addmat(out, scalemat(c, m))
    return out


def flatten(m):
    return tuple(Fraction(x) for row in m for x in row)


def cyclic_l1(d, L=7):
    x, y = d
    return min(x % L, (-x) % L) + min(y % L, (-y) % L)


def d4_apply(m, d, L=7):
    x, y = d
    return (
        (m[0][0]*x + m[0][1]*y) % L,
        (m[1][0]*x + m[1][1]*y) % L,
    )


def displacement_orbits(actions, L=7):
    unseen = {(x, y) for x in range(L) for y in range(L)}
    rows = []
    while unseen:
        seed = min(unseen)
        orbit = frozenset(d4_apply(m, seed, L) for m in actions.D4)
        unseen -= orbit
        radii = {cyclic_l1(d, L) for d in orbit}
        if len(radii) != 1:
            raise ArithmeticError("D4 orbit changes graph radius")
        rows.append({
            "representative": min(orbit),
            "orbit": orbit,
            "radius": next(iter(radii)),
            "size": len(orbit),
        })
    rows.sort(key=lambda r: (r["radius"], r["representative"]))
    return rows


def restricted_translation(actions, c, basis, d):
    g = actions.CellAutomorphism(actions.D4[0], d, c.L)
    return actions.restricted_representation(basis, actions.edge_action(c, g))


def orbit_operators(actions, c, basis, rows):
    ops = []
    for row in rows:
        mats = [restricted_translation(actions, c, basis, d) for d in sorted(row["orbit"])]
        ops.append(addmat(*mats))
    return tuple(ops)


def powers(A, ql, n=9):
    out = [ql.identity(len(A))]
    for _ in range(n):
        out.append(ql.matmul(out[-1], A))
    return tuple(out)


def solve_change_of_basis(ql, power_mats, orbit_mats):
    power_rows = tuple(flatten(m) for m in power_mats)
    rr, pivots = ql.rref(power_rows)
    if len(pivots) != len(power_mats):
        raise ArithmeticError("power basis not independent")
    pivot_positions = pivots
    B = tuple(
        tuple(power_rows[k][pos] for k in range(len(power_mats)))
        for pos in pivot_positions
    )
    Binv = ql.inverse(B)
    coeff_rows = []
    exact = True
    for E in orbit_mats:
        ef = flatten(E)
        b = tuple(ef[pos] for pos in pivot_positions)
        coeff = ql.matvec(Binv, b)
        coeff_rows.append(coeff)
        if lincomb(coeff, power_mats) != E:
            exact = False
    return tuple(coeff_rows), exact


def jsonify_fraction(x):
    x = Fraction(x)
    return int(x) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def audit() -> dict:
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(7)
    basis = actions.cycle_basis_exact(c.B1.astype(int))
    if basis.dimension != 50:
        raise AssertionError("cycle dimension changed")

    inherited = json.loads((V1534 / "docs/RESULTS.json").read_text())
    if not inherited["full_commutant_generated_by_adjacency"]:
        raise AssertionError("v15.34 theorem changed")
    if inherited["commutant_dimension"] != 10:
        raise AssertionError("v15.34 commutant dimension changed")

    rows = displacement_orbits(actions, 7)
    if len(rows) != 10 or sum(r["size"] for r in rows) != 49:
        raise ArithmeticError("unexpected displacement orbit partition")

    expected = [
        ((0,0),0,1),
        ((0,1),1,4),
        ((0,2),2,4),
        ((1,1),2,4),
        ((0,3),3,4),
        ((1,2),3,8),
        ((1,3),4,8),
        ((2,2),4,4),
        ((2,3),5,8),
        ((3,3),6,4),
    ]
    observed = [(r["representative"], r["radius"], r["size"]) for r in rows]
    if observed != expected:
        raise ArithmeticError(f"unexpected canonical orbit table: {observed}")

    orbit_mats = orbit_operators(actions, c, basis, rows)
    orbit_rank = ql.rank(tuple(flatten(m) for m in orbit_mats))
    if orbit_rank != 10:
        raise ArithmeticError("orbit kernels do not span ten dimensions")

    A = orbit_mats[1]
    power_mats = powers(A, ql, 9)
    power_rank = ql.rank(tuple(flatten(m) for m in power_mats))
    if power_rank != 10:
        raise ArithmeticError("v15.34 power basis rank not reproduced")

    coeff_rows, reconstruction_exact = solve_change_of_basis(ql, power_mats, orbit_mats)
    change_rank = ql.rank(coeff_rows)
    if not reconstruction_exact or change_rank != 10:
        raise ArithmeticError("orbit/power change of basis failed")

    support_dims = {}
    support_proj = {}
    for R in range(7):
        mats = [m for m, row in zip(orbit_mats, rows) if row["radius"] <= R]
        d = ql.rank(tuple(flatten(m) for m in mats))
        support_dims[str(R)] = d
        support_proj[str(R)] = max(0, d-1)

    expected_support = {"0":1,"1":2,"2":4,"3":6,"4":8,"5":9,"6":10}
    if support_dims != expected_support:
        raise ArithmeticError(f"support filtration mismatch: {support_dims}")

    degree_dims = {
        str(k): ql.rank(tuple(flatten(m) for m in power_mats[:k+1]))
        for k in range(10)
    }
    expected_degree = {str(k): k+1 for k in range(10)}
    if degree_dims != expected_degree:
        raise ArithmeticError("polynomial degree filtration changed")

    mismatch = next(
        (R for R in range(7) if support_dims[str(R)] != degree_dims[str(R)]),
        None,
    )

    locality_ledger = [
        {
            "source": "v13.15 generic bounded-neighborhood QMAR",
            "classification": "GENERIC_HARD_RADIUS_NOT_DERIVED",
            "hard_radius_equation_count": 0,
        },
        {
            "source": "v13.15 commuting-Markov separator closure",
            "classification": "CONDITIONAL_LOCALITY_NOT_TYPED_TO_CURRENT_WEIGHT_ALGEBRA",
            "hard_radius_equation_count": 0,
        },
        {
            "source": "v13.18 CMI/source-conditioned jet locality",
            "classification": "APPROXIMATE_ERROR_LOCALITY_NOT_HARD_SUPPORT_CUTOFF",
            "hard_radius_equation_count": 0,
        },
        {
            "source": "v15.03 site-local source covariance",
            "classification": "SOURCE_LOCALITY_DOES_NOT_ENTAIL_RESPONSE_RADIUS",
            "hard_radius_equation_count": 0,
        },
    ]
    unresolved = 0
    hard_count = sum(x["hard_radius_equation_count"] for x in locality_ledger)
    frozen_R = None

    status = (
        "FROZEN_LOCALITY_SELECTS_HARD_RADIUS"
        if frozen_R is not None
        else "CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED"
    )

    orbit_table = []
    for row, coeff in zip(rows, coeff_rows):
        degree = max(i for i, x in enumerate(coeff) if x)
        orbit_table.append({
            "representative": list(row["representative"]),
            "radius": row["radius"],
            "size": row["size"],
            "polynomial_degree": degree,
            "polynomial_coefficients_low_to_high": [jsonify_fraction(x) for x in coeff],
        })

    return {
        "version": "v15.35",
        "base_sha": BASE_SHA,
        "status": status,
        "dim_Z": basis.dimension,
        "commutant_dimension": inherited["commutant_dimension"],
        "displacement_orbit_count": len(rows),
        "displacement_orbit_size_sum": sum(r["size"] for r in rows),
        "orbit_table": orbit_table,
        "orbit_basis_rank": orbit_rank,
        "orbit_polynomial_reconstruction_exact": reconstruction_exact,
        "orbit_to_power_change_rank": change_rank,
        "power_basis_rank": power_rank,
        "support_radius_dimensions": support_dims,
        "support_radius_projective_dimensions": support_proj,
        "polynomial_degree_filtration_dimensions": degree_dims,
        "support_radius_equals_polynomial_degree_filtration": mismatch is None,
        "first_radius_degree_mismatch": mismatch,
        "max_torus_graph_radius": 6,
        "locality_evidence_ledger": locality_ledger,
        "unresolved_locality_typing_count": unresolved,
        "frozen_hard_radius_selected": frozen_R,
        "frozen_hard_radius_constraint_count": hard_count,
        "surviving_response_dimension": inherited["commutant_dimension"],
        "surviving_projective_response_dimension": inherited["inherited_projective_weight_dimension"],
        "hard_radius_control_table": [
            {
                "radius": R,
                "response_dimension": support_dims[str(R)],
                "projective_dimension": support_proj[str(R)],
                "status": "NEW_HARD_RADIUS_ASSUMPTION_CONTROL_ONLY" if R < 6 else "FULL_FINITE_TORUS_SUPPORT",
            }
            for R in range(7)
        ],
        "evidence_pins": verify_evidence(),
        "new_source_semantics_axiom_added": False,
        "new_locality_axiom_added": False,
        "hard_radius_selected": False,
        "polynomial_degree_selected": False,
        "adjacency_function_selected": False,
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
            "TARGET_BLIND_TYPED_CONSTRAINT_ON_ADJACENCY_RESPONSE_FUNCTION_OR_"
            "EXPLICIT_PRETIME_RESPONSE_FUNCTION_AXIOM"
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
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    if args.check and Path(args.check).read_text() != text:
        raise SystemExit("committed v15.35 result differs from regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
