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
V1535 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.35-support-radius-locality"
BASE_SHA = "c549e093be355ca93fff5ac1c63d0c3a4452b6f7"

EVIDENCE = {
    "exact_linear.py": (
        V1528 / "exact_linear.py",
        "05cc1b8cfec70d501408377b5e44190b259a4514",
        (),
    ),
    "v15.35-results": (
        V1535 / "docs/RESULTS.json",
        "17a99eed9d9a36635b2fc47b79f8decf1e0ab52d",
        ("CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED",),
    ),
    "v15.05-composition": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v15/v15.05/REPORT.md",
        "b191c08c22ded0439cc4c2c125fbccfdb677dcbc",
        ("FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE",),
    ),
    "v15.06-recoverability": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v15/v15.06/REPORT.md",
        "bdeac09b2b162f07baa874ef1c1d6415fdd5e236",
        ("MULTIPLICATIVE_RECOVERABILITY_SCALAR_DOES_NOT_SELECT_LOCAL_SOURCE_LAW",),
    ),
    "v13.16-markov": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/v13/v13.16/REPORT.md",
        "cf2420b2545f801869a617092f4955b7a57ddc60",
        ("Exact quantum Markovity is **not** selected by the existing ontology.",),
    ),
    "v15.24-channels": (
        REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.24-composition-gate/README.md",
        "8f7dcf085fc1cbaf167297191ad1a7416f0efa42",
        ("It does not adopt any of them as a new physical law.",),
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


def load_ql():
    verify_evidence()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module("exact_linear")


def qvec(values):
    v = tuple(Fraction(x) for x in values)
    if len(v) != 10:
        raise ValueError("ten sector coordinates required")
    return v


def compose(a, b):
    a, b = qvec(a), qvec(b)
    return tuple(x*y for x, y in zip(a, b))


def semigroup_at(base, n):
    base = qvec(base)
    if type(n) is not int or n < 0:
        raise ValueError("nonnegative integer parameter required")
    return tuple(x**n for x in base)


def canonical_projective(v):
    v = qvec(v)
    first = next((x for x in v if x), None)
    if first is None:
        raise ValueError("zero vector")
    return tuple(x/first for x in v)


def exact_semigroup_witnesses():
    bases = (
        qvec((2,3,5,7,11,13,17,19,23,29)),
        qvec((3,5,7,11,13,17,19,23,29,31)),
        qvec((1,2,3,5,8,13,21,34,55,89)),
        qvec((2,4,3,9,5,25,7,49,11,121)),
        qvec((5,4,6,7,8,9,10,11,12,13)),
    )
    checks = []
    for b in bases:
        for m in range(5):
            for n in range(5):
                checks.append(compose(semigroup_at(b,m), semigroup_at(b,n)) == semigroup_at(b,m+n))
    return bases, all(checks)


def affine_rank(ql, points):
    points = tuple(qvec(p) for p in points)
    base = points[0]
    diffs = tuple(tuple(x-y for x,y in zip(p,base)) for p in points[1:])
    return ql.rank(diffs)


def cone_controls(ql):
    one = qvec((1,)*10)
    positive_points = [one]
    for i in range(10):
        p = list(one); p[i] = Fraction(2); positive_points.append(tuple(p))
    positive_dim = affine_rank(ql, positive_points)

    projective_points = [one]
    for i in range(1,10):
        p = list(one); p[i] = Fraction(2); projective_points.append(tuple(p))
    projective_dim = affine_rank(ql, projective_points)

    neg = qvec((-1,)*10)
    nonpositive = [neg]
    for i in range(10):
        p = list(neg); p[i] = Fraction(-2); nonpositive.append(tuple(p))
    contraction_dim = affine_rank(ql, nonpositive)
    return positive_dim, projective_dim, contraction_dim


def frozen_ledger():
    return [
        {
            "source": "v15.05 frozen composition",
            "class": "NONSELECTIVE_FAMILY_CLOSURE",
            "function_equation_rank": 0,
            "reason": "composition preserves arbitrary already-chosen response law",
        },
        {
            "source": "v15.06 recoverability multiplicativity",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "multiplicative scalar has no certified map to current cycle-response function",
        },
        {
            "source": "v13.16 Markov/recoverability",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "exact Markovity is not selected and recoverability acts on quantum state/channel data",
        },
        {
            "source": "v15.24 CPTP/no-signalling/product composition",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "quantum-channel operator algebra is not the certified cycle carrier",
        },
        {
            "source": "physical positivity/order on Z",
            "class": "TYPE_BLOCKED",
            "function_equation_rank": 0,
            "reason": "no frozen pointed cone, order unit, Choi structure or probability simplex is certified on Z",
        },
    ]


def audit() -> dict:
    ql = load_ql()
    inherited = json.loads((V1535 / "docs/RESULTS.json").read_text())
    if inherited["commutant_dimension"] != 10:
        raise AssertionError("inherited commutant dimension changed")
    if inherited["surviving_projective_response_dimension"] != 9:
        raise AssertionError("inherited projective function dimension changed")

    bases, semigroup_ok = exact_semigroup_witnesses()
    projective = {canonical_projective(b) for b in bases}
    positive_dim, positive_proj_dim, contraction_dim = cone_controls(ql)

    ledger = frozen_ledger()
    nonselective = sum(row["class"] == "NONSELECTIVE_FAMILY_CLOSURE" for row in ledger)
    blocked = sum(row["class"] == "TYPE_BLOCKED" for row in ledger)
    unresolved = sum(row["class"] == "UNRESOLVED" for row in ledger)
    actual = [row for row in ledger if row["class"] == "ACTUAL_FUNCTION_EQUATION"]
    rank = sum(row["function_equation_rank"] for row in actual)

    if unresolved:
        status = "ORDER_SEMIGROUP_AUDIT_UNRESOLVED"
    elif rank:
        status = "FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_REDUCE_FUNCTION"
    else:
        status = "FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_LEAVE_FUNCTION_UNSELECTED"

    return {
        "version": "v15.36",
        "base_sha": BASE_SHA,
        "status": status,
        "sector_count": inherited["commutant_dimension"],
        "continuous_semigroup_classification": "T_t=exp(t*g(A))_OVER_REAL_SPLITTING_FIELD",
        "continuous_semigroup_generator_dimension": 10,
        "projective_relative_generator_dimension": 9,
        "continuous_semigroup_control_is_frozen": False,
        "exact_rational_semigroup_witness_count": len(bases),
        "projectively_distinct_semigroup_witness_count": len(projective),
        "all_exact_semigroup_composition_checks_pass": semigroup_ok,
        "positive_cone_affine_dimension": positive_dim,
        "positive_projective_dimension": positive_proj_dim,
        "nonpositive_generator_cone_affine_dimension": contraction_dim,
        "sectorwise_positivity_is_frozen_physical_order_law": False,
        "contractive_semigroup_is_frozen_physical_law": False,
        "frozen_constraint_ledger": ledger,
        "nonselective_frozen_family_closure_count": nonselective,
        "type_blocked_frozen_candidate_count": blocked,
        "unresolved_typing_count": unresolved,
        "frozen_actual_function_equation_count": len(actual),
        "frozen_function_constraint_rank": rank,
        "surviving_projective_function_dimension": 9-rank,
        "evidence_pins": verify_evidence(),
        "new_source_semantics_axiom_added": False,
        "new_order_axiom_added": False,
        "new_semigroup_axiom_added": False,
        "response_generator_selected": False,
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
        "next_required_object": "NEW_TYPED_PRETIME_RESPONSE_PRINCIPLE_OR_EXPLICIT_RESPONSE_FUNCTION_AXIOM",
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + "\n"


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out")
    p.add_argument("--check")
    args=p.parse_args()
    text=canonical_json(audit())
    if args.out:
        out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text)
    if args.check and Path(args.check).read_text()!=text:
        raise SystemExit("committed v15.36 result differs from regenerated audit")
    print(text,end="")


if __name__=="__main__":
    main()
