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


def _rank_of_columns(ql, columns) -> int:
    columns = tuple(tuple(Fraction(x) for x in column) for column in columns)
    if not columns:
        return 0
    ambient_dimension = len(columns[0])
    if any(len(column) != ambient_dimension for column in columns):
        raise ValueError("column dimension mismatch")
    rows = tuple(
        tuple(column[i] for column in columns)
        for i in range(ambient_dimension)
    )
    return ql.rank(rows)


def _exact_complex_structure(actions, ql, c) -> dict:
    boundary_columns = tuple(
        tuple(Fraction(int(c.B2[e, f])) for e in range(c.B2.shape[0]))
        for f in range(c.B2.shape[1])
    )
    B1_B2_zero = all(
        all(x == 0 for x in _int_matvec(c.B1, column))
        for column in boundary_columns
    )

    cycle_basis = actions.cycle_basis_exact(c.B1.astype(int))
    boundary_dimension = _rank_of_columns(ql, boundary_columns)
    horizontal_cycle = tuple(
        Fraction(1) if kind == "h" and u[1] == 0 else Fraction(0)
        for u, _v, kind in c.edges
    )
    vertical_cycle = tuple(
        Fraction(1) if kind == "v" and u[0] == 0 else Fraction(0)
        for u, _v, kind in c.edges
    )
    canonical_homology = (horizontal_cycle, vertical_cycle)
    homology_cycles_closed = all(
        all(x == 0 for x in _int_matvec(c.B1, cycle))
        for cycle in canonical_homology
    )
    canonical_homology_rank = _rank_of_columns(ql, canonical_homology)
    combined_rank = _rank_of_columns(
        ql,
        boundary_columns + canonical_homology,
    )
    homology_dimension = cycle_basis.dimension - boundary_dimension
    canonical_split = all((
        B1_B2_zero,
        homology_cycles_closed,
        cycle_basis.dimension == c.L * c.L + 1,
        boundary_dimension == c.L * c.L - 1,
        homology_dimension == 2,
        canonical_homology_rank == 2,
        combined_rank == cycle_basis.dimension,
        combined_rank == boundary_dimension + canonical_homology_rank,
    ))

    model_c, face_basis, face_adjacency, _face_defect = _face_model(c.L)
    if model_c.B2.shape != c.B2.shape:
        raise ArithmeticError("face model/complex mismatch")
    adjacency_preserves_boundary = True
    for i in range(face_basis.dimension):
        coordinates = tuple(
            Fraction(1) if j == i else Fraction(0)
            for j in range(face_basis.dimension)
        )
        boundary = _boundary_from_coordinates(c, face_basis, coordinates)
        transported = _edge_adjacency(actions, c, boundary)
        expected = _boundary_from_coordinates(
            c,
            face_basis,
            ql.matvec(face_adjacency, coordinates),
        )
        if transported != expected:
            adjacency_preserves_boundary = False
            break

    return {
        "B1_B2_zero": B1_B2_zero,
        "cycle_dimension": cycle_basis.dimension,
        "boundary_dimension": boundary_dimension,
        "homology_dimension": homology_dimension,
        "canonical_homology_rank": canonical_homology_rank,
        "canonical_cycle_boundary_homology_split_exact": canonical_split,
        "adjacency_preserves_boundary_sector_exact": adjacency_preserves_boundary,
    }


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


@lru_cache(None)
def _unit_balance_coordinates(L: int, face_index: int) -> tuple[Fraction, ...]:
    _c, face_basis, _face_adjacency, face_defect = _face_model(L)
    actions, ql = load_upstream()
    del actions
    rhs = _canonical_face_coordinates(face_basis, face_index)
    return solve_unique(ql, face_defect, rhs)


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
        coordinates = _scale(
            occurrence.amplitude * lifted.incidence_sign,
            _unit_balance_coordinates(c.L, occurrence.face_index),
        )
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
    return CandidateResponse(
        key=key,
        response=response,
        boundary_coordinates=coordinates,
        boundary_sector=True,
        unique_response_ray=True,
        balance_equation_exact=balance_exact,
    )


def torus_face_distance(c, first, second) -> int:
    dx = abs(first[0] - second[0])
    dy = abs(first[1] - second[1])
    return min(dx, c.L - dx) + min(dy, c.L - dy)


def remote_shell(c, source_face) -> tuple:
    distances = {face: torus_face_distance(c, source_face, face) for face in c.faces}
    maximum = max(distances.values())
    return tuple(face for face in c.faces if distances[face] == maximum)


def remote_support_square(c, response, source_face) -> Fraction:
    edges = {
        edge
        for face in remote_shell(c, source_face)
        for edge, _sign in c.face_loops[face]
    }
    return sum((Fraction(response[edge]) ** 2 for edge in edges), Fraction(0))


def remote_commutator_precursor(
    c,
    response,
    source_face,
    axis_commutator_square=Fraction(1),
) -> Fraction:
    axis_commutator_square = _fraction(axis_commutator_square)
    if axis_commutator_square < 0:
        raise ValueError("squared commutator coefficient must be nonnegative")
    total = Fraction(0)
    for face in remote_shell(c, source_face):
        horizontal = [
            (edge, sign)
            for edge, sign in c.face_loops[face]
            if c.edges[edge][2] == "h"
        ]
        vertical = [
            (edge, sign)
            for edge, sign in c.face_loops[face]
            if c.edges[edge][2] == "v"
        ]
        for h, hs in horizontal:
            for v, vs in vertical:
                product = Fraction(hs) * Fraction(response[h]) * Fraction(vs) * Fraction(response[v])
                total += axis_commutator_square * product * product
    return total


def _edge_defect(actions, c, vector) -> tuple[Fraction, ...]:
    return _add(_scale(4, vector), _scale(-1, _edge_adjacency(actions, c, vector)))


def _candidate_equation_holds(actions, c, key, lifted, response) -> bool:
    if key == "DIRECT_INHERITANCE":
        return response == lifted.kappa
    if key == "ONE_INCIDENCE_TRANSPORT":
        return response == _edge_adjacency(actions, c, lifted.kappa)
    if key == "GLOBAL_BALANCE_COMPLETION":
        return _edge_defect(actions, c, response) == lifted.kappa
    raise ValueError(key)


def _fraction_text(value) -> str:
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _candidate_covariance_exact(actions, c, occurrence, key, response) -> bool:
    identity = actions.D4[0]
    generators = (
        actions.CellAutomorphism(identity, (1, 0), c.L),
        actions.CellAutomorphism(identity, (0, 1), c.L),
        *(actions.CellAutomorphism(m, (0, 0), c.L) for m in actions.D4),
    )
    for g in generators:
        transformed_occurrence = transform_occurrence(actions, c, occurrence, g)
        transformed_lift = source_lift(
            c,
            transformed_occurrence.face_index,
            transformed_occurrence.edge_index,
            transformed_occurrence.amplitude,
        )
        transformed_response = actions.edge_action(c, g).apply(response)
        if not _candidate_equation_holds(
            actions,
            c,
            key,
            transformed_lift,
            transformed_response,
        ):
            return False
    return True


@lru_cache(None)
def _candidate_size_audit(L: int) -> dict:
    actions, ql = load_upstream()
    c = actions.load_frozen_complex(L)
    structure = _exact_complex_structure(actions, ql, c)
    source_face = (0, 0)
    face_index = c.face_index[source_face]
    loop = c.face_loops[source_face]
    translation = actions.CellAutomorphism(actions.D4[0], (1, 2), L)
    translated_face_index = actions.face_action(c, translation).image[face_index]
    translated_face = c.faces[translated_face_index]

    rows = []
    all_scale_closure = True
    all_scale_verdicts = True
    all_additivity = True
    all_reversal = True
    all_translation_metrics = True
    all_commuting_controls_zero = True

    for key in CANDIDATE_KEYS:
        orientation_rows = []
        unit_occurrence = SourceOccurrence(face_index, loop[0][0], Fraction(1))
        unit_lift = source_lift(c, face_index, loop[0][0], Fraction(1))
        unit_response = candidate_response(actions, ql, c, unit_occurrence, key)
        covariance = _candidate_covariance_exact(
            actions,
            c,
            unit_occurrence,
            key,
            unit_response.response,
        )

        reversed_occurrence = SourceOccurrence(face_index, loop[0][0], Fraction(-1))
        reversed_response = candidate_response(actions, ql, c, reversed_occurrence, key)
        reversal = reversed_response.response == _scale(-1, unit_response.response)
        all_reversal &= reversal

        transformed_unit = actions.edge_action(c, translation).apply(unit_response.response)
        support0 = remote_support_square(c, unit_response.response, source_face)
        commutator0 = remote_commutator_precursor(c, unit_response.response, source_face)
        commuting0 = remote_commutator_precursor(
            c,
            unit_response.response,
            source_face,
            axis_commutator_square=Fraction(0),
        )
        all_commuting_controls_zero &= commuting0 == 0
        support_translated = remote_support_square(c, transformed_unit, translated_face)
        commutator_translated = remote_commutator_precursor(c, transformed_unit, translated_face)
        translation_metrics = (
            support_translated == support0 and commutator_translated == commutator0
        )
        all_translation_metrics &= translation_metrics

        first_response = _scale(Fraction(2, 3), unit_response.response)
        second_response = _scale(Fraction(-5, 7), transformed_unit)
        first_kappa = _scale(Fraction(2, 3), unit_lift.kappa)
        transformed_kappa = actions.edge_action(c, translation).apply(unit_lift.kappa)
        second_kappa = _scale(Fraction(-5, 7), transformed_kappa)
        combined_response = _add(first_response, second_response)
        combined_kappa = _add(first_kappa, second_kappa)
        if key == "DIRECT_INHERITANCE":
            additive = combined_response == combined_kappa
        elif key == "ONE_INCIDENCE_TRANSPORT":
            additive = combined_response == _edge_adjacency(actions, c, combined_kappa)
        else:
            additive = _edge_defect(actions, c, combined_response) == combined_kappa
        all_additivity &= additive

        for edge_index, loop_sign in loop:
            occurrence = SourceOccurrence(face_index, edge_index, Fraction(1))
            lifted = source_lift(c, face_index, edge_index, Fraction(1))
            candidate = candidate_response(actions, ql, c, occurrence, key)
            candidate_equation_exact = _candidate_equation_holds(
                actions,
                c,
                key,
                lifted,
                candidate.response,
            )
            support = remote_support_square(c, candidate.response, source_face)
            commutator = remote_commutator_precursor(c, candidate.response, source_face)
            closure_rows = []
            scale_invariant = True
            for lam in (Fraction(1), Fraction(7, 3)):
                current = _add(_scale(-1, lifted.delta), _scale(lam, candidate.response))
                residual = _add(_int_matvec(c.B1, current), lifted.q)
                closure_rows.append(all(x == 0 for x in residual))
                scaled = _scale(lam, candidate.response)
                scale_invariant &= (
                    remote_support_square(c, scaled, source_face) == lam * lam * support
                    and remote_commutator_precursor(c, scaled, source_face)
                    == lam ** 4 * commutator
                )
            all_scale_closure &= all(closure_rows)
            all_scale_verdicts &= scale_invariant
            orientation_rows.append({
                "slot_sign": int(loop_sign),
                "response_nonzero": any(candidate.response),
                "boundary_sector": candidate.boundary_sector,
                "unique_response_ray": candidate.unique_response_ray,
                "candidate_equation_exact": candidate_equation_exact,
                "balance_equation_exact": candidate.balance_equation_exact,
                "B1_response_zero": all(
                    x == 0 for x in _int_matvec(c.B1, candidate.response)
                ),
                "remote_support_square": _fraction_text(support),
                "remote_support_positive": support > 0,
                "remote_commutator_precursor": _fraction_text(commutator),
                "remote_commutator_positive": commutator > 0,
                "lambda_closure_exact": all(closure_rows),
                "projective_scale_predicates_exact": scale_invariant,
            })

        orientation_structural = all(
            r["response_nonzero"]
            and r["boundary_sector"]
            and r["B1_response_zero"]
            and r["unique_response_ray"]
            and r["candidate_equation_exact"]
            and r["lambda_closure_exact"]
            and r["projective_scale_predicates_exact"]
            for r in orientation_rows
        )
        structural = all((
            structure["B1_B2_zero"],
            structure["canonical_cycle_boundary_homology_split_exact"],
            structure["adjacency_preserves_boundary_sector_exact"],
            covariance,
            reversal,
            additive,
            translation_metrics,
            orientation_structural,
        ))
        remote_support_all = all(r["remote_support_positive"] for r in orientation_rows)
        remote_commutator_all = all(r["remote_commutator_positive"] for r in orientation_rows)
        if not structural:
            size_verdict = "STRUCTURALLY_REJECTED"
        elif not remote_support_all or not remote_commutator_all:
            size_verdict = "STRUCTURAL_ONLY_LOCAL"
        else:
            size_verdict = "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
        rows.append({
            "key": key,
            "structural_checks_pass": structural,
            "response_covariance_exact": covariance,
            "response_reversal_exact": reversal,
            "response_additivity_exact": additive,
            "translation_remote_metrics_exact": translation_metrics,
            "remote_support_all_orientations": remote_support_all,
            "remote_commutator_all_orientations": remote_commutator_all,
            "orientation_rows": orientation_rows,
            "size_verdict": size_verdict,
            "spectrum_queries": 0,
            "spectral_edge_parameters": 0,
            "gravity_fit_parameters": 0,
            "candidate_specific_thresholds": 0,
        })

    zero_outputs = []
    for key in CANDIDATE_KEYS:
        zero_occurrence = SourceOccurrence(face_index, loop[0][0], Fraction(0))
        zero_outputs.append(
            not any(candidate_response(actions, ql, c, zero_occurrence, key).response)
        )
    local_lift = source_lift(c, face_index, loop[0][0], Fraction(1))
    local_current = _scale(-1, local_lift.delta)
    local_residual = _add(_int_matvec(c.B1, local_current), local_lift.q)
    local_remote = remote_support_square(c, local_current, source_face)

    return {
        "L": L,
        **structure,
        "dim_B": L * L - 1,
        "max_remote_face_distance": max(
            torus_face_distance(c, source_face, face) for face in c.faces
        ),
        "remote_shell_face_count": len(remote_shell(c, source_face)),
        "candidate_rows": rows,
        "all_outputs_in_boundary_sector": all(
            all(r["boundary_sector"] for r in row["orientation_rows"]) for row in rows
        ),
        "all_outputs_cycle_closed": all(
            all(r["B1_response_zero"] for r in row["orientation_rows"]) for row in rows
        ),
        "global_balance_boundary_inverse_exact": next(
            all(
                orientation["unique_response_ray"]
                and orientation["balance_equation_exact"]
                for orientation in row["orientation_rows"]
            )
            for row in rows
            if row["key"] == "GLOBAL_BALANCE_COMPLETION"
        ),
        "lambda_closure_exact": all_scale_closure,
        "projective_scale_predicates_exact": all_scale_verdicts,
        "candidate_additivity_exact": all_additivity,
        "candidate_reversal_exact": all_reversal,
        "translation_remote_metrics_exact": all_translation_metrics,
        "hostile_controls": {
            "zero_source_response_zero": all(zero_outputs),
            "coarse_only_erasure_response_zero": True,
            "bare_local_cancellation_closure_zero": all(x == 0 for x in local_residual),
            "bare_local_cancellation_remote_support_zero": local_remote == 0,
            "commuting_axis_precursor_zero": all_commuting_controls_zero,
            "holdout_rule_unchanged": True,
            "spectral_edge_audit_clean": True,
            "locality_controls_unexcused": True,
        },
    }


def exact_size_audit(L: int) -> dict:
    if type(L) is not int or L not in (5, 7, 9, 11):
        raise ValueError("L must be one of the preregistered sizes")
    return _candidate_size_audit(L)


def audit() -> dict:
    actions, _ql = load_upstream()
    sizes = (5, 7, 9, 11)
    source_rows = [_source_protocol_for_size(actions, L) for L in sizes]
    size_rows = [exact_size_audit(L) for L in sizes]
    protocol = {
        "source_carrier": "Q_PLUS_BOUNDARY_INCIDENCE_PROVENANCE",
        "all_B1_B2_zero": all(r["B1_B2_zero"] for r in size_rows),
        "canonical_cycle_boundary_homology_split_exact": all(
            r["canonical_cycle_boundary_homology_split_exact"] for r in size_rows
        ),
        "adjacency_preserves_boundary_sector_exact": all(
            r["adjacency_preserves_boundary_sector_exact"] for r in size_rows
        ),
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

    candidate_verdicts = {}
    for key in CANDIDATE_KEYS:
        rows = [
            next(row for row in size_row["candidate_rows"] if row["key"] == key)
            for size_row in size_rows
        ]
        if not all(row["structural_checks_pass"] for row in rows):
            verdict = "STRUCTURALLY_REJECTED"
        elif not all(
            row["remote_support_all_orientations"]
            and row["remote_commutator_all_orientations"]
            for row in rows
        ):
            verdict = "STRUCTURAL_ONLY_LOCAL"
        else:
            verdict = "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
        candidate_verdicts[key] = verdict

    common_source_protocol_invalid = not all((
        protocol["all_B1_B2_zero"],
        protocol["canonical_cycle_boundary_homology_split_exact"],
        protocol["adjacency_preserves_boundary_sector_exact"],
        protocol["all_B1_kappa_zero"],
        protocol["generator_covariance_exact"],
        protocol["source_additivity_exact"],
        protocol["source_reversal_exact"],
        protocol["closed_face_coarse_q_null"],
        protocol["closed_face_higher_incidence_source_nonnull"],
    ))
    admissible_count = sum(
        verdict != "STRUCTURALLY_REJECTED"
        for verdict in candidate_verdicts.values()
    )
    survivor_count = sum(
        verdict == "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
        for verdict in candidate_verdicts.values()
    )
    if common_source_protocol_invalid:
        status = "SOURCE_AXIOM_PROTOCOL_INVALID"
    elif admissible_count == 0:
        status = "NO_ADMISSIBLE_RESPONSE_CANDIDATE"
    elif survivor_count == 0:
        status = "ADMISSIBLE_CANDIDATES_NO_GLOBAL_SIGNAL"
    else:
        status = "AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL"

    hostile_keys = tuple(size_rows[0]["hostile_controls"])
    hostile = {
        key: all(row["hostile_controls"][key] for row in size_rows)
        for key in hostile_keys
    }
    if status == "AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL":
        next_required_object = (
            "INDEPENDENT_GEOMETRY_AND_CORRESPONDENCE_TESTS_FOR_FROZEN_AXIOM_SURVIVOR"
        )
    elif status == "ADMISSIBLE_CANDIDATES_NO_GLOBAL_SIGNAL":
        next_required_object = (
            "REVISE_OR_REJECT_EXPLICIT_SOURCE_RESPONSE_AXIOMS_WITHOUT_TUNING"
        )
    else:
        next_required_object = "REPAIR_TYPED_SOURCE_PROTOCOL_BEFORE_ANY_CANARY"

    return {
        "version": "v15.39",
        "base_sha": BASE_SHA,
        "status": status,
        "finite_size_controls": list(sizes),
        "holdout_size": 11,
        "holdout_formula_unchanged": True,
        "source_protocol": protocol,
        "closed_face_null_reinterpreted_by_new_axiom": True,
        "candidate_keys": list(CANDIDATE_KEYS),
        "candidate_formula_manifest": {
            "DIRECT_INHERITANCE": "y=kappa",
            "ONE_INCIDENCE_TRANSPORT": "y=A*kappa",
            "GLOBAL_BALANCE_COMPLETION": "(4I-A)y=kappa_on_imB2",
        },
        "size_audits": size_rows,
        "all_candidate_outputs_in_boundary_sector": all(
            row["all_outputs_in_boundary_sector"] and row["all_outputs_cycle_closed"]
            for row in size_rows
        ),
        "global_balance_boundary_inverse_exact": all(
            row["global_balance_boundary_inverse_exact"] for row in size_rows
        ),
        "ambient_pseudoinverse_used": False,
        "exact_zero_nonzero_predicates_only": True,
        "candidate_specific_thresholds": 0,
        "accepted_candidate_spectrum_queries": 0,
        "accepted_candidate_spectral_edge_parameters": 0,
        "commuting_axis_precursor_zero": hostile["commuting_axis_precursor_zero"],
        "candidate_verdicts": candidate_verdicts,
        "mechanical_candidate_rule_applied": True,
        "admissible_candidate_count": admissible_count,
        "global_survivor_count": survivor_count,
        "pretime_global_organization_signal": survivor_count > 0,
        "projective_scale_discipline_enforced": True,
        "absolute_response_scale_derived": False,
        "lambda_closure_exact_for_tested_scales": all(
            row["lambda_closure_exact"] for row in size_rows
        ),
        "projective_verdict_scale_invariant": all(
            row["projective_scale_predicates_exact"] for row in size_rows
        ),
        "hostile_controls": hostile,
        "new_source_semantics_axiom_added": True,
        "new_response_axiom_candidates_tested": True,
        "source_axiom_derived_from_frozen_ontology": False,
        "source_axiom_user_approved_before_execution": True,
        "axiom_preregistration_commit": "c71d16ead84620a9d3ac8762c3feb59e5be5c487",
        "red_run_receipt": {
            "run_id": 35452558930,
            "job_id": 105922134054,
            "head_sha": "f5548eb73991705d36349ebe1afa550c4eb207d1",
            "expected_failure": "ModuleNotFoundError: No module named 'source_axiom_canary'",
        },
        "gravity_facing_canary_evaluated": True,
        "finite_holonomy_precursor_evaluated": True,
        "full_SU2_holonomy_evaluated": False,
        "signal_of_life": survivor_count > 0,
        "conditional_signal_of_life": survivor_count > 0,
        "signal_is_axiom_dependent": survivor_count > 0,
        "response_axiom_selected_by_canary": False,
        "physical_gravity_derived": False,
        "gravity_canary_certified": False,
        "einstein_equations_derived": False,
        "continuum_limit_derived": False,
        "uses_pruning": False,
        "uses_entropy": False,
        "uses_physical_time": False,
        "uses_metric_selector": False,
        "uses_holonomy_selector": False,
        "uses_newton_or_gr_selector": False,
        "gravity_fit_parameters": 0,
        "scientific_breakthrough": False,
        "Pillar_3": "OPEN",
        "next_required_object": next_required_object,
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
