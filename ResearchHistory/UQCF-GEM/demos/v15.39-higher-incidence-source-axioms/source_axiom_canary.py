from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
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


def audit() -> dict:
    actions, _ql = load_upstream()
    sizes = (5, 7, 9, 11)
    rows = [_source_protocol_for_size(actions, L) for L in sizes]
    protocol = {
        "source_carrier": "Q_PLUS_BOUNDARY_INCIDENCE_PROVENANCE",
        "all_B1_kappa_zero": all(r["all_B1_kappa_zero"] for r in rows),
        "generator_covariance_exact": all(r["generator_covariance_exact"] for r in rows),
        "source_additivity_exact": all(r["source_additivity_exact"] for r in rows),
        "source_reversal_exact": all(r["source_reversal_exact"] for r in rows),
        "closed_face_coarse_q_null": all(r["closed_face_coarse_q_null"] for r in rows),
        "closed_face_higher_incidence_source_nonnull": all(
            r["closed_face_higher_incidence_source_nonnull"] for r in rows
        ),
        "closed_face_kappa_multiple": (
            4 if all(r["closed_face_kappa_multiple"] == 4 for r in rows) else None
        ),
        "size_rows": rows,
    }
    return {
        "version": "v15.39",
        "base_sha": BASE_SHA,
        "source_protocol": protocol,
        "closed_face_null_reinterpreted_by_new_axiom": True,
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
