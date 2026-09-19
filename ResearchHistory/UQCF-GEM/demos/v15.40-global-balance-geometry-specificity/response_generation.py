from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib
import json
import sys

VectorQ = tuple[Fraction, ...]
SignedSupport = tuple[tuple[int, ...], ...]
REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space"
V1539 = REPO_ROOT / "ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms"
SPEC = REPO_ROOT / "docs/superpowers/specs/2026-09-19-v1540-global-balance-geometry-specificity-design.md"
BASE_SHA = "0f3e10602929dd0a148b195f32406efa52082070"
EVIDENCE = {
    "v15.39-source": (V1539 / "source_axiom_canary.py", "620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a"),
    "v15.39-results": (V1539 / "docs/RESULTS.json", "ac8eb10ed90360fee6dcc0f170f19fffd0d74116"),
    "representation_actions.py": (V1528 / "representation_actions.py", "7260147cd6ca47ec21634172b44b98de726904af"),
    "exact_linear.py": (V1528 / "exact_linear.py", "05cc1b8cfec70d501408377b5e44190b259a4514"),
    "v15.40-design": (SPEC, "5f75f9a7ba1df5b21715f775d26bedbedc07297f"),
}
GENERATORS = {
    "GLOBAL_BALANCE_COMPLETION": ((1, 0), (-1, 0), (0, 1), (0, -1)),
    "MATCHED_DIAGONAL_BALANCE": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    "MATCHED_STEP2_BALANCE": ((2, 0), (-2, 0), (0, 2), (0, -2)),
}
CONTROL_KEYS = ("DIRECT_INHERITANCE", "ONE_INCIDENCE_TRANSPORT", "MATCHED_DIAGONAL_BALANCE", "MATCHED_STEP2_BALANCE")
FAMILY_KEYS = ("GLOBAL_BALANCE_COMPLETION",) + CONTROL_KEYS


@dataclass(frozen=True)
class ResponseFamily:
    key: str
    labels: tuple[int, ...]
    sources: tuple[VectorQ, ...]
    responses: tuple[VectorQ, ...]


@dataclass(frozen=True)
class StructuralAudit:
    key: str
    connected: bool
    invertible_on_augmentation: bool
    translation_D4_covariant: bool
    valence_four: bool
    response_equations_exact: bool


def git_blob(path):
    raw = Path(path).read_bytes()
    return hashlib.sha1(f"blob {len(raw)}".encode() + bytes([0]) + raw).hexdigest()


@lru_cache(None)
def verify_evidence():
    verified = {}
    for key, (path, expected) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f"evidence drift: {key}: {actual}")
        verified[key] = actual
    inherited = json.loads((V1539 / "docs/RESULTS.json").read_text())
    if inherited["status"] != "AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL":
        raise AssertionError("v15.39 status drift")
    expected = {"GLOBAL_BALANCE_COMPLETION": "PRETIME_GLOBAL_ORGANIZATION_SURVIVES", "DIRECT_INHERITANCE": "STRUCTURAL_ONLY_LOCAL", "ONE_INCIDENCE_TRANSPORT": "STRUCTURAL_ONLY_LOCAL"}
    if any(inherited["candidate_verdicts"].get(key) != value for key, value in expected.items()):
        raise AssertionError("v15.39 candidate verdict drift")
    return verified


@lru_cache(None)
def load_upstream():
    verify_evidence()
    if str(V1528) not in sys.path:
        sys.path.insert(0, str(V1528))
    return importlib.import_module("representation_actions"), importlib.import_module("exact_linear")


def _scale(scale, vector):
    return tuple(Fraction(scale) * Fraction(value) for value in vector)


def _add(*vectors):
    return tuple(sum((Fraction(vector[i]) for vector in vectors), Fraction(0)) for i in range(len(vectors[0])))


def _int_matvec(matrix, vector):
    rows, columns = matrix.shape
    return tuple(sum((Fraction(int(matrix[i, j])) * Fraction(vector[j]) for j in range(columns)), Fraction(0)) for i in range(rows))


@lru_cache(None)
def _complex(L):
    if type(L) is not int or L not in (5, 7, 9, 11):
        raise ValueError("L must be one of 5, 7, 9, 11")
    return load_upstream()[0].load_frozen_complex(L)


def centered_source(L, face_index):
    count = L * L
    if type(face_index) is not int or not 0 <= face_index < count:
        raise ValueError("invalid face index")
    source = [Fraction(-1, count) for _ in range(count)]; source[face_index] += 1
    return tuple(source)


def signed_support_B2(L):
    matrix = _complex(L).B2
    return tuple(tuple(int(matrix[row, column]) for column in range(matrix.shape[1])) for row in range(matrix.shape[0]))


def B2_column(L, face_index):
    return tuple(Fraction(row[face_index]) for row in signed_support_B2(L))


def boundary_from_face_vector(L, vector):
    return _int_matvec(_complex(L).B2, vector)


def deterministic_permutation(L):
    count = L * L
    permutation = tuple((2 * index + 1) % count for index in range(count))
    if sorted(permutation) != list(range(count)):
        raise ArithmeticError("deterministic relabeling is not bijective")
    return permutation


def relabel_vector(vector, permutation):
    if len(vector) != len(permutation) or sorted(permutation) != list(range(len(permutation))):
        raise ValueError("invalid relabeling permutation")
    out = [Fraction(0)] * len(vector)
    for old, new in enumerate(permutation): out[new] = Fraction(vector[old])
    return tuple(out)


def relabel_family(family, permutation):
    count = len(family.labels); sources = [None] * count; responses = [None] * count
    for position, label in enumerate(family.labels):
        new = permutation[label]
        sources[new] = relabel_vector(family.sources[position], permutation)
        responses[new] = relabel_vector(family.responses[position], permutation)
    return ResponseFamily(family.key, tuple(range(count)), tuple(sources), tuple(responses))


def relabel_support_columns(support, permutation):
    rows = []
    for row in support:
        out = [0] * len(row)
        for old, new in enumerate(permutation): out[new] = row[old]
        rows.append(tuple(out))
    return tuple(rows)


@lru_cache(None)
def _permutations(L, key):
    actions, _ = load_upstream(); complex_ = _complex(L)
    return tuple(actions.face_action(complex_, actions.CellAutomorphism(actions.D4[0], displacement, L)) for displacement in GENERATORS[key])


def _adjacency_apply(L, key, vector):
    return _add(*(permutation.apply(vector) for permutation in _permutations(L, key)))


def inverse_on_augmentation(matrix):
    ql = load_upstream()[1]; inverse = ql.inverse(matrix); identity = ql.identity(len(matrix))
    if ql.matmul(matrix, inverse) != identity or ql.matmul(inverse, matrix) != identity:
        raise ArithmeticError("exact augmentation inverse verification failed")
    return inverse


def solve_with_verified_inverse(matrix, inverse, rhs):
    ql = load_upstream()[1]; solution = ql.matvec(inverse, rhs)
    if ql.matvec(matrix, solution) != tuple(rhs):
        raise ArithmeticError("exact solve verification failed")
    return solution


@lru_cache(None)
def _balance_model(L, key):
    actions, ql = load_upstream(); basis = actions.augmentation_basis(L * L)
    matrices = tuple(actions.restricted_representation(basis, p) for p in _permutations(L, key))
    adjacency = matrices[0]
    for matrix in matrices[1:]: adjacency = ql.add(adjacency, matrix)
    defect = ql.add(ql.scale(4, ql.identity(basis.dimension)), ql.scale(-1, adjacency))
    return basis, defect, inverse_on_augmentation(defect)


def _unit_response(L, key, source):
    if key == "DIRECT_INHERITANCE": return source
    if key == "ONE_INCIDENCE_TRANSPORT": return _adjacency_apply(L, "GLOBAL_BALANCE_COMPLETION", source)
    if key in GENERATORS:
        basis, defect, inverse = _balance_model(L, key)
        return basis.combine(solve_with_verified_inverse(defect, inverse, basis.coordinates(source)))
    raise ValueError(f"unknown response family: {key}")


@lru_cache(None)
def _unit_family(L, key):
    if key not in FAMILY_KEYS: raise ValueError(f"unknown response family: {key}")
    labels = tuple(range(L * L)); sources = tuple(centered_source(L, label) for label in labels)
    return ResponseFamily(key, labels, sources, tuple(_unit_response(L, key, source) for source in sources))


def response_family(L, key, scale=Fraction(1)):
    if isinstance(scale, bool) or not isinstance(scale, (int, Fraction)): raise TypeError("exact scale required")
    scale = Fraction(scale)
    if scale <= 0: raise ValueError("positive projective scale required")
    family = _unit_family(L, key)
    return family if scale == 1 else ResponseFamily(key, family.labels, family.sources, tuple(_scale(scale, response) for response in family.responses))


def _graph_properties(L, key):
    count = L * L; neighbors = [set() for _ in range(count)]
    for permutation in _permutations(L, key):
        for old, new in enumerate(permutation.image): neighbors[old].add(new)
    seen = {0}; queue = deque([0])
    while queue:
        for neighbor in sorted(neighbors[queue.popleft()]):
            if neighbor not in seen: seen.add(neighbor); queue.append(neighbor)
    return len(seen) == count, all(len(row) == 4 for row in neighbors)


def _covariant(L, key):
    actions = load_upstream()[0]; expected = frozenset((x % L, y % L) for x, y in GENERATORS[key])
    return all(frozenset(((m[0][0]*x+m[0][1]*y)%L, (m[1][0]*x+m[1][1]*y)%L) for x, y in GENERATORS[key]) == expected for m in actions.D4)


def structural_audit(L, key):
    connected, valence = _graph_properties(L, key); basis, defect, inverse = _balance_model(L, key)
    equations = all(basis.combine(solve_with_verified_inverse(defect, inverse, basis.coordinates(centered_source(L, label)))) == _unit_response(L, key, centered_source(L, label)) for label in range(L * L))
    return StructuralAudit(key, connected, True, _covariant(L, key), valence, equations)


@lru_cache(None)
def generation_audit(L):
    actions, ql = load_upstream(); complex_ = _complex(L); support = signed_support_B2(L)
    matrix = tuple(tuple(Fraction(value) for value in row) for row in support)
    rank = ql.rank(matrix); nullspace = ql.nullspace(matrix)
    isomorphism = rank == L*L-1 and len(nullspace) == 1 and all(x == nullspace[0][0] for x in nullspace[0]) and all(boundary_from_face_vector(L, centered_source(L, face)) == B2_column(L, face) for face in range(L*L))
    structural = {key: structural_audit(L, key) for key in GENERATORS}
    covariance = True; additivity = True; orientation = True
    first, second = 0, complex_.face_index[(1 % L, 2 % L)]
    for key in FAMILY_KEYS:
        family = response_family(L, key)
        combined_source = _add(_scale(Fraction(2, 3), family.sources[first]), _scale(Fraction(-5, 7), family.sources[second]))
        combined_response = _unit_response(L, key, combined_source)
        additivity &= combined_response == _add(_scale(Fraction(2, 3), family.responses[first]), _scale(Fraction(-5, 7), family.responses[second]))
        for face in range(L * L):
            loop = complex_.face_loops[complex_.faces[face]]
            orientation &= len(loop) == 4 and all(support[edge][face] in (-1, 1) and support[edge][face] * support[edge][face] == 1 for edge, _sign in loop)
        automorphisms = (
            actions.CellAutomorphism(actions.D4[0], (1, 0), L),
            actions.CellAutomorphism(actions.D4[0], (0, 1), L),
            *(actions.CellAutomorphism(matrix_d4, (0, 0), L) for matrix_d4 in actions.D4),
        )
        for automorphism in automorphisms:
            image = actions.face_action(complex_, automorphism).image
            covariance &= all(relabel_vector(family.responses[label], image) == family.responses[image[label]] for label in range(L*L))
    return {
        "L": L, "evidence_verified": bool(verify_evidence()), "B2_rank": rank,
        "B2_kernel_constant_line": len(nullspace)==1 and all(x == nullspace[0][0] for x in nullspace[0]),
        "canonical_augmentation_isomorphism_exact": isomorphism,
        "all_response_equations_exact": all(item.response_equations_exact for item in structural.values()),
        "all_orientation_rays_exact": orientation,
        "all_additivity_exact": additivity,
        "all_translation_D4_covariance_exact": covariance and all(item.translation_D4_covariant for item in structural.values()),
        "matched_controls_structurally_admissible": all(all((structural[key].connected, structural[key].invertible_on_augmentation, structural[key].translation_D4_covariant, structural[key].valence_four, structural[key].response_equations_exact)) for key in ("MATCHED_DIAGONAL_BALANCE", "MATCHED_STEP2_BALANCE")),
        "structural_audits": {key: item.__dict__ for key, item in structural.items()},
    }
