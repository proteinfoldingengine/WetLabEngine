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
V1532 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.32-commutant-sector-decomposition"
V1533 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.33-sector-weight-constraint-audit"
BASE_SHA = "04ad5d3cf24b7f051d714d61d2fe6d8da4fd8eec"

PINS = {
    "representation_actions.py": (V1528 / "representation_actions.py", "7260147cd6ca47ec21634172b44b98de726904af"),
    "exact_linear.py": (V1528 / "exact_linear.py", "05cc1b8cfec70d501408377b5e44190b259a4514"),
    "v15.32-results": (V1532 / "docs/RESULTS.json", "a6018895d996bb01d76918994ebd0519260a958d"),
    "v15.33-results": (V1533 / "docs/RESULTS.json", "5ff397efbb66851f4a9a602c417cafdf50e62757"),
}

FACTORS = (
    (1, -4),
    (1, -5, 6, -1),
    (1, 2, -8, -8),
    (1, 2, -1, -1),
)


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


def verify_pins() -> dict[str, str]:
    out = {}
    for key, (path, expected) in PINS.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"upstream pin drift: {key}: {actual}")
        out[key] = actual
    return out


def load_upstream():
    verify_pins()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module("representation_actions"), importlib.import_module("exact_linear")


def addmat(*mats):
    if not mats:
        raise ValueError("need matrices")
    r, c = len(mats[0]), len(mats[0][0])
    return tuple(tuple(sum((Fraction(m[i][j]) for m in mats), Fraction(0))
                       for j in range(c)) for i in range(r))


def scalemat(a, m):
    a = Fraction(a)
    return tuple(tuple(a * Fraction(x) for x in row) for row in m)


def zeromat(n):
    return tuple(tuple(Fraction(0) for _ in range(n)) for _ in range(n))


def poly_mul_desc(a, b):
    aa = list(reversed([Fraction(x) for x in a]))
    bb = list(reversed([Fraction(x) for x in b]))
    cc = [Fraction(0)] * (len(aa) + len(bb) - 1)
    for i, x in enumerate(aa):
        for j, y in enumerate(bb):
            cc[i+j] += x*y
    return tuple(reversed(cc))


def full_polynomial():
    p = (Fraction(1),)
    for f in FACTORS:
        p = poly_mul_desc(p, f)
    return tuple(int(x) if x.denominator == 1 else x for x in p)


def eval_poly_from_powers(coeffs_desc, powers):
    degree = len(coeffs_desc) - 1
    n = len(powers[0])
    out = zeromat(n)
    for i, coeff in enumerate(coeffs_desc):
        power = degree - i
        out = addmat(out, scalemat(coeff, powers[power]))
    return out


def is_zero_matrix(m):
    return all(x == 0 for row in m for x in row)


def rational_cubic_irreducible(f):
    if len(f) != 4 or f[0] != 1:
        raise ValueError("monic cubic required")
    const = abs(int(f[-1]))
    candidates = set()
    for d in range(1, const + 1):
        if const % d == 0:
            candidates |= {d, -d}
    for r in candidates:
        if sum(Fraction(c) * (Fraction(r) ** (3-i)) for i, c in enumerate(f)) == 0:
            return False
    return True


def poly_strip_asc(p):
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return tuple(q)


def poly_divmod_asc(a, b):
    a = list(poly_strip_asc(a)); b = list(poly_strip_asc(b))
    if len(b) == 1 and b[0] == 0:
        raise ZeroDivisionError
    q = [Fraction(0)] * max(1, len(a)-len(b)+1)
    while len(a) >= len(b) and any(a):
        k = len(a)-len(b)
        c = a[-1] / b[-1]
        q[k] += c
        for j in range(len(b)):
            a[k+j] -= c*b[j]
        while len(a) > 1 and a[-1] == 0:
            a.pop()
    return tuple(q), tuple(a)


def poly_gcd_desc(a, b):
    aa = tuple(reversed([Fraction(x) for x in a]))
    bb = tuple(reversed([Fraction(x) for x in b]))
    while not (len(bb) == 1 and bb[0] == 0):
        _q, rr = poly_divmod_asc(aa, bb)
        aa, bb = bb, rr
    lead = aa[-1]
    aa = tuple(x/lead for x in aa)
    return tuple(reversed(aa))


def restricted_adjacency(actions, ql, c, basis):
    ident = actions.D4[0]
    disps = ((1,0), (6,0), (0,1), (0,6))
    trans = tuple(actions.CellAutomorphism(ident, d, c.L) for d in disps)
    reps = [actions.restricted_representation(basis, actions.edge_action(c, g)) for g in trans]
    A = addmat(*reps)
    return A, trans, disps


def d4_set_invariance(actions, disps):
    s = set(disps)
    for m in actions.D4:
        image = {
            ((m[0][0]*x + m[0][1]*y) % 7,
             (m[1][0]*x + m[1][1]*y) % 7)
            for x, y in s
        }
        if image != s:
            return False
    return True


def powers_of(A, ql, max_power):
    n = len(A)
    powers = [ql.identity(n)]
    for _ in range(max_power):
        powers.append(ql.matmul(powers[-1], A))
    return tuple(powers)


def flatten(m):
    return tuple(Fraction(x) for row in m for x in row)


def audit() -> dict:
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(7)
    group = actions.torus_automorphisms(7)
    basis = actions.cycle_basis_exact(c.B1.astype(int))
    if basis.dimension != 50:
        raise AssertionError("cycle dimension changed")

    inherited32 = json.loads((V1532 / "docs/RESULTS.json").read_text())
    inherited33 = json.loads((V1533 / "docs/RESULTS.json").read_text())
    if inherited32["recovered_total_commutant_dimension"] != 10:
        raise AssertionError("v15.32 commutant dimension changed")
    if inherited33["frozen_constraint_rank"] != 0:
        raise AssertionError("v15.33 frontier changed")

    A, translations, disps = restricted_adjacency(actions, ql, c, basis)

    # Preservation is built into restricted_representation/coordinates; repeat directly
    # on every basis vector as a fail-closed check.
    preservation = True
    for col in basis.columns:
        out = tuple(Fraction(0) for _ in col)
        for g in translations:
            out = tuple(x+y for x, y in zip(out, actions.edge_action(c, g).apply(col)))
        try:
            basis.coordinates(out)
        except ValueError:
            preservation = False

    # The primitive translation set is conjugation-invariant under D4, hence its
    # group-algebra sum commutes with the full semidirect-product action.
    d4_invariant = d4_set_invariance(actions, disps)
    all_commute = d4_invariant and all(g.matrix in actions.D4 for g in group)

    powers = powers_of(A, ql, 10)
    p = full_polynomial()
    annih = is_zero_matrix(eval_poly_from_powers(p, powers))

    cubic_irred = all(rational_cubic_irreducible(f) for f in FACTORS[1:])
    pairwise_coprime = True
    for i, f in enumerate(FACTORS):
        for h in FACTORS[i+1:]:
            if poly_gcd_desc(f, h) != (Fraction(1),):
                pairwise_coprime = False

    omission_nonzero = []
    for omit in range(len(FACTORS)):
        q = (Fraction(1),)
        for i, f in enumerate(FACTORS):
            if i != omit:
                q = poly_mul_desc(q, f)
        omission_nonzero.append(not is_zero_matrix(eval_poly_from_powers(q, powers)))

    power_rank = ql.rank(tuple(flatten(m) for m in powers[:10]))
    degree = 10 if annih and cubic_irred and pairwise_coprime and all(omission_nonzero) else None
    full_generated = degree == 10 and power_rank == 10 and inherited32["recovered_total_commutant_dimension"] == 10

    if not preservation or not all_commute:
        status = "CANONICAL_ADJACENCY_AUDIT_UNRESOLVED"
    elif not full_generated:
        status = "CANONICAL_ADJACENCY_IS_PROPER_SUBALGEBRA"
    else:
        status = "FULL_COMMUTANT_GENERATED_BY_CANONICAL_ADJACENCY_FUNCTION_UNSELECTED"

    return {
        "version": "v15.34",
        "base_sha": BASE_SHA,
        "status": status,
        "group_order": len(group),
        "dim_Z": basis.dimension,
        "commutant_dimension": inherited32["recovered_total_commutant_dimension"],
        "primitive_translation_count": len(translations),
        "primitive_translation_sum_D4_invariant": d4_invariant,
        "adjacency_preserves_Z": preservation,
        "all_group_commutators_zero": all_commute,
        "minimal_polynomial_factors": [list(f) for f in FACTORS],
        "minimal_polynomial_coefficients": list(p),
        "cubic_factors_irreducible_over_Q": cubic_irred,
        "factors_pairwise_coprime": pairwise_coprime,
        "minimal_polynomial_annihilates_Z": annih,
        "all_proper_factor_omissions_fail": all(omission_nonzero),
        "proper_factor_omission_nonzero": omission_nonzero,
        "minimal_polynomial_degree": degree,
        "power_span_rank": power_rank,
        "full_commutant_generated_by_adjacency": full_generated,
        "rational_factor_degrees": [len(f)-1 for f in FACTORS],
        "rational_commutant_decomposition": [
            "Q",
            "Q[x]/(x^3-5x^2+6x-1)",
            "Q[x]/(x^3+2x^2-8x-8)",
            "Q[x]/(x^3+2x^2-x-1)",
        ],
        "splitting_field_sector_count": inherited32["splitting_field_sector_count"],
        "inherited_projective_weight_dimension": inherited33["surviving_projective_weight_dimension"],
        "adjacency_function_selected": False,
        "new_source_semantics_axiom_added": False,
        "new_sector_weight_selector_added": False,
        "low_degree_locality_assumed": False,
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
        "upstream_pins": verify_pins(),
        "next_required_object": (
            "TARGET_BLIND_PRINCIPLE_SELECTING_FUNCTION_OF_CANONICAL_ADJACENCY_OR_EXPLICIT_NEW_AXIOM"
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
        raise SystemExit("committed v15.34 result differs from regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
