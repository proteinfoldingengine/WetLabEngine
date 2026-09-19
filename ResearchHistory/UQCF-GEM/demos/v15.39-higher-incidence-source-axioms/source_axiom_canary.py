from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space"
V1538 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.38-response-axiom-admissibility"
SPEC = REPO_ROOT / "docs/superpowers/specs/2026-09-19-v1539-higher-incidence-source-axioms-design.md"

BASE_SHA = "825b47b276c6a17df35e6620f6de6630a1d729e2"
CANDIDATE_KEYS = (
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "GLOBAL_BALANCE_COMPLETION",
)

EVIDENCE = {
    "representation_actions.py": (
        V1528 / "representation_actions.py",
        "7260147cd6ca47ec21634172b44b98de726904af",
    ),
    "exact_linear.py": (
        V1528 / "exact_linear.py",
        "05cc1b8cfec70d501408377b5e44190b259a4514",
    ),
    "v15.38-results": (
        V1538 / "docs/RESULTS.json",
        "9caa94fe6e700a6684fa9c899b37503a2736bece",
    ),
    "v15.39-design": (
        SPEC,
        "edabb9837d293f49ff78f007c31c3904bf04c3e5",
    ),
}


@dataclass(frozen=True)
class SourceOccurrence:
    face_index: int
    edge_index: int
    amplitude: Fraction


@dataclass(frozen=True)
class LiftedSource:
    delta: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    kappa: tuple[Fraction, ...]
    incidence_sign: int


@dataclass(frozen=True)
class CandidateResponse:
    key: str
    response: tuple[Fraction, ...]
    boundary_coordinates: tuple[Fraction, ...]
    boundary_sector: bool
    unique_response_ray: bool
    balance_equation_exact: bool


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


def verify_evidence() -> dict[str, str]:
    out = {}
    for key, (path, expected) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"evidence drift: {key}: {actual}")
        out[key] = actual
    inherited = json.loads((V1538 / "docs/RESULTS.json").read_text())
    if inherited["status"] != "PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE":
        raise AssertionError("v15.38 admissibility status drift")
    if inherited["response_function_selected"]:
        raise AssertionError("v15.38 unexpectedly selected a response")
    return out


def load_upstream():
    verify_evidence()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module("representation_actions"), importlib.import_module("exact_linear")


def _fraction(value) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("exact integer or Fraction amplitude required")
    return Fraction(value)


def _zero(n: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(0) for _ in range(n))


def _add(*vectors) -> tuple[Fraction, ...]:
    if not vectors:
        raise ValueError("at least one vector required")
    n = len(vectors[0])
    if any(len(v) != n for v in vectors):
        raise ValueError("vector dimension mismatch")
    return tuple(sum((Fraction(v[i]) for v in vectors), Fraction(0)) for i in range(n))


def _scale(a, vector) -> tuple[Fraction, ...]:
    a = Fraction(a)
    return tuple(a * Fraction(x) for x in vector)


def _int_matvec(matrix, vector) -> tuple[Fraction, ...]:
    vector = tuple(Fraction(x) for x in vector)
    rows, cols = matrix.shape
    if len(vector) != cols:
        raise ValueError("matrix/vector dimension mismatch")
    return tuple(
        sum((Fraction(int(matrix[i, j])) * vector[j] for j in range(cols)), Fraction(0))
        for i in range(rows)
    )


def source_lift(c, face_index: int, edge_index: int, amplitude) -> LiftedSource:
    if type(face_index) is not int or not 0 <= face_index < c.B2.shape[1]:
        raise ValueError("invalid face index")
    if type(edge_index) is not int or not 0 <= edge_index < c.B2.shape[0]:
        raise ValueError("invalid edge index")
    a = _fraction(amplitude)
    sigma = int(c.B2[edge_index, face_index])
    if sigma not in (-1, 1):
        raise ValueError("edge is not an occurrence in the selected face")

    delta = list(_zero(c.B1.shape[1]))
    delta[edge_index] = a
    delta = tuple(delta)
    q = _int_matvec(c.B1, delta)
    boundary = tuple(Fraction(int(c.B2[e, face_index])) for e in range(c.B2.shape[0]))
    kappa = _scale(a * sigma, boundary)
    return LiftedSource(delta, q, kappa, sigma)


def compose_sources(sources) -> LiftedSource:
    sources = tuple(sources)
    if not sources:
        raise ValueError("at least one lifted source required")
    return LiftedSource(
        _add(*(s.delta for s in sources)),
        _add(*(s.q for s in sources)),
        _add(*(s.kappa for s in sources)),
        0,
    )


def transform_occurrence(actions, c, occurrence: SourceOccurrence, g) -> SourceOccurrence:
    edge = actions.edge_action(c, g)
    face = actions.face_action(c, g)
    return SourceOccurrence(
        face.image[occurrence.face_index],
        edge.image[occurrence.edge_index],
        occurrence.amplitude * edge.sign[occurrence.edge_index],
    )


def _source_protocol_for_size(actions, L: int) -> dict:
    c = actions.load_frozen_complex(L)
    f0 = c.face_index[(0, 0)]
    loop = c.face_loops[(0, 0)]

    typed = []
    for edge_index, _loop_sign in loop:
        lifted = source_lift(c, f0, edge_index, Fraction(2, 3))
        typed.append(all(x == 0 for x in _int_matvec(c.B1, lifted.kappa)))

    identity = actions.D4[0]
    generators = (
        actions.CellAutomorphism(identity, (1, 0), L),
        actions.CellAutomorphism(identity, (0, 1), L),
        *(actions.CellAutomorphism(m, (0, 0), L) for m in actions.D4),
    )
    covariance = True
    for edge_index, _loop_sign in loop:
        occurrence = SourceOccurrence(f0, edge_index, Fraction(2, 3))
        lifted = source_lift(c, occurrence.face_index, occurrence.edge_index, occurrence.amplitude)
        for g in generators:
            transformed = transform_occurrence(actions, c, occurrence, g)
            lifted_transformed = source_lift(
                c,
                transformed.face_index,
                transformed.edge_index,
                transformed.amplitude,
            )
            covariance &= (
                actions.edge_action(c, g).apply(lifted.delta) == lifted_transformed.delta
                and actions.vertex_action(c, g).apply(lifted.q) == lifted_transformed.q
                and actions.edge_action(c, g).apply(lifted.kappa) == lifted_transformed.kappa
            )

    second_face = c.face_index[(1 % L, 2 % L)]
    second_edge = c.face_loops[(1 % L, 2 % L)][1][0]
    first = source_lift(c, f0, loop[0][0], Fraction(2, 3))
    second = source_lift(c, second_face, second_edge, Fraction(-5, 7))
    composed = compose_sources((first, second))
    additive = (
        composed.delta == _add(first.delta, second.delta)
        and composed.q == _add(first.q, second.q)
        and composed.kappa == _add(first.kappa, second.kappa)
    )

    reversed_first = source_lift(c, f0, loop[0][0], Fraction(-2, 3))
    reversal = (
        reversed_first.delta == _scale(-1, first.delta)
        and reversed_first.q == _scale(-1, first.q)
        and reversed_first.kappa == _scale(-1, first.kappa)
    )

    closed_parts = [
        source_lift(c, f0, edge_index, Fraction(loop_sign))
        for edge_index, loop_sign in loop
    ]
    closed = compose_sources(closed_parts)
    face_boundary = tuple(Fraction(int(c.B2[e, f0])) for e in range(c.B2.shape[0]))
    closed_q_null = all(x == 0 for x in closed.q)
    closed_kappa_four = closed.kappa == _scale(4, face_boundary)

    return {
        "L": L,
        "all_B1_kappa_zero": all(typed),
        "generator_covariance_exact": bool(covariance),
        "source_additivity_exact": additive,
        "source_reversal_exact": reversal,
        "closed_face_delta_is_B2_column": closed.delta == face_boundary,
        "closed_face_coarse_q_null": closed_q_null,
        "closed_face_higher_incidence_source_nonnull": any(closed.kappa),
        "closed_face_kappa_multiple": 4 if closed_kappa_four else None,
    }



def _primitive_translations(actions, L: int):
    identity = actions.D4[0]
    return tuple(
        actions.CellAutomorphism(identity, displacement, L)
        for displacement in ((1, 0), (L - 1, 0), (0, 1), (0, L - 1))
    )


def _edge_adjacency(actions, c, vector) -> tuple[Fraction, ...]:
    return _add(*(
        actions.edge_action(c, g).apply(vector)
        for g in _primitive_translations(actions, c.L)
    ))


def _matrix_sum(ql, matrices):
    matrices = tuple(matrices)
    if not matrices:
        raise ValueError("at least one matrix required")
    out = matrices[0]
    for matrix in matrices[1:]:
        out = ql.add(out, matrix)
    return out


@lru_cache(None)
def _face_model(L: int):
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(L)
    basis = actions.augmentation_basis(len(c.faces))
    representations = tuple(
        actions.restricted_representation(basis, actions.face_action(c, g))
        for g in _primitive_translations(actions, L)
    )
    adjacency = _matrix_sum(ql, representations)
    defect = ql.add(
        ql.scale(4, ql.identity(basis.dimension)),
        ql.scale(-1, adjacency),
    )
    return c, basis, adjacency, defect


def _canonical_face_coordinates(basis, face_index: int) -> tuple[Fraction, ...]:
    count = basis.ambient_dimension
    if type(face_index) is not int or not 0 <= face_index < count:
        raise ValueError("invalid face index")
    full = [Fraction(-1, count) for _ in range(count)]
    full[face_index] += 1
    return basis.coordinates(tuple(full))


def _boundary_from_coordinates(c, basis, coordinates) -> tuple[Fraction, ...]:
    return _int_matvec(c.B2, basis.combine(coordinates))


def solve_unique(ql, matrix, rhs) -> tuple[Fraction, ...]:
    matrix = ql.matrix(matrix)
    rhs = tuple(Fraction(x) for x in rhs)
    n, m = ql.shape(matrix)
    if n != m or len(rhs) != n:
        raise ValueError("square system with matching right side required")
    augmented = tuple(tuple(matrix[i]) + (rhs[i],) for i in range(n))
    reduced, pivots = ql.rref(augmented, ncols=n + 1)
    coefficient_pivots = tuple(p for p in pivots if p < n)
    if coefficient_pivots != tuple(range(n)):
        raise ValueError("boundary defect operator is not invertible")
    solution = tuple(reduced[i][n] for i in range(n))
    if ql.matvec(matrix, solution) != rhs:
        raise ArithmeticError("exact solve verification failed")
    return solution


def candidate_response(actions, ql, c, occurrence: SourceOccurrence, key: str) -> CandidateResponse:
    if key not in CANDIDATE_KEYS:
        raise ValueError(f"unknown candidate: {key}")
    lifted = source_lift(
        c,
        occurrence.face_index,
        occurrence.edge_index,
        occurrence.amplitude,
    )
    model_c, face_basis, face_adjacency, face_defect = _face_model(c.L)
    if model_c.B2.shape != c.B2.shape:
        raise ArithmeticError("face model/complex mismatch")
    source_coordinates = _scale(
        occurrence.amplitude * lifted.incidence_sign,
        _canonical_face_coordinates(face_basis, occurrence.face_index),
    )

    if key == "DIRECT_INHERITANCE":
        coordinates = source_coordinates
        response = lifted.kappa
        balance_exact = False
    elif key == "ONE_INCIDENCE_TRANSPORT":
        coordinates = ql.matvec(face_adjacency, source_coordinates)
        response = _edge_adjacency(actions, c, lifted.kappa)
        balance_exact = False
    else:
        coordinates = solve_unique(ql, face_defect, source_coordinates)
        response = _boundary_from_coordinates(c, face_basis, coordinates)
        edge_defect_response = _add(
            _scale(4, response),
            _scale(-1, _edge_adjacency(actions, c, response)),
        )
        balance_exact = edge_defect_response == lifted.kappa
        if not balance_exact:
            raise ArithmeticError("ambient global-balance equation failed")

    reconstructed = _boundary_from_coordinates(c, face_basis, coordinates)
    boundary_sector = reconstructed == response
    if not boundary_sector:
        raise ArithmeticError("candidate left canonical boundary sector")
    if not any(response):
        raise ArithmeticError("candidate produced zero response")

    return CandidateResponse(
        key=key,
        response=response,
        boundary_coordinates=coordinates,
        boundary_sector=True,
        unique_response_ray=True,
        balance_equation_exact=balance_exact,
    )


@lru_cache(None)
def _candidate_size_audit(L: int) -> dict:
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(L)
    face_index = c.face_index[(0, 0)]
    edge_index = c.face_loops[(0, 0)][0][0]
    occurrence = SourceOccurrence(face_index, edge_index, Fraction(1))
    rows = []
    for key in CANDIDATE_KEYS:
        response = candidate_response(actions, ql, c, occurrence, key)
        rows.append({
            "key": key,
            "boundary_sector": response.boundary_sector,
            "unique_response_ray": response.unique_response_ray,
            "nonzero_response": any(response.response),
            "B1_response_zero": all(x == 0 for x in _int_matvec(c.B1, response.response)),
            "balance_equation_exact": response.balance_equation_exact,
            "spectrum_queries": 0,
            "spectral_edge_parameters": 0,
            "gravity_fit_parameters": 0,
            "candidate_specific_thresholds": 0,
        })
    return {
        "L": L,
        "dim_B": L * L - 1,
        "candidate_rows": rows,
        "all_outputs_in_boundary_sector": all(r["boundary_sector"] for r in rows),
        "all_outputs_cycle_closed": all(r["B1_response_zero"] for r in rows),
        "global_balance_boundary_inverse_exact": next(
            r["balance_equation_exact"]
            for r in rows
            if r["key"] == "GLOBAL_BALANCE_COMPLETION"
        ),
    }


def exact_size_audit(L: int) -> dict:
    if type(L) is not int or L not in (5, 7, 9, 11):
        raise ValueError("L must be one of the preregistered sizes")
    return _candidate_size_audit(L)

def audit() -> dict:
    actions, _ql = load_upstream()
    sizes = (5, 7, 9, 11)
    source_rows = [_source_protocol_for_size(actions, L) for L in sizes]
    candidate_rows = [exact_size_audit(L) for L in sizes]
    protocol = {
        "source_carrier": "Q_PLUS_BOUNDARY_INCIDENCE_PROVENANCE",
        "all_B1_kappa_zero": all(r["all_B1_kappa_zero"] for r in source_rows),
        "generator_covariance_exact": all(r["generator_covariance_exact"] for r in source_rows),
        "source_additivity_exact": all(r["source_additivity_exact"] for r in source_rows),
        "source_reversal_exact": all(r["source_reversal_exact"] for r in source_rows),
        "closed_face_coarse_q_null": all(r["closed_face_coarse_q_null"] for r in source_rows),
        "closed_face_higher_incidence_source_nonnull": all(
            r["closed_face_higher_incidence_source_nonnull"] for r in source_rows
        ),
        "closed_face_kappa_multiple": (
            4 if all(r["closed_face_kappa_multiple"] == 4 for r in source_rows) else None
        ),
        "size_rows": source_rows,
    }
    return {
        "version": "v15.39",
        "base_sha": BASE_SHA,
        "finite_size_controls": list(sizes),
        "holdout_size": 11,
        "source_protocol": protocol,
        "closed_face_null_reinterpreted_by_new_axiom": True,
        "candidate_keys": list(CANDIDATE_KEYS),
        "candidate_formula_manifest": {
            "DIRECT_INHERITANCE": "y=kappa",
            "ONE_INCIDENCE_TRANSPORT": "y=A*kappa",
            "GLOBAL_BALANCE_COMPLETION": "(4I-A)y=kappa_on_imB2",
        },
        "candidate_size_audits": candidate_rows,
        "all_candidate_outputs_in_boundary_sector": all(
            row["all_outputs_in_boundary_sector"] and row["all_outputs_cycle_closed"]
            for row in candidate_rows
        ),
        "global_balance_boundary_inverse_exact": all(
            row["global_balance_boundary_inverse_exact"] for row in candidate_rows
        ),
        "ambient_pseudoinverse_used": False,
        "evidence_pins": verify_evidence(),
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    parser.add_argument("--check")
    args = parser.parse_args()
    text = canonical_json(audit())
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    if args.check and Path(args.check).read_text() != text:
        raise SystemExit("committed v15.39 result differs from regenerated audit")
    print(text, end="")


if __name__ == "__main__":
    main()
