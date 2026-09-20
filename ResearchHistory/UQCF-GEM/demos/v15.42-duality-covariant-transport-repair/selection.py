from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from exact_algebra import rank, solve_unique


@dataclass(frozen=True)
class ComponentSelectionAudit:
    solution: tuple[Fraction, ...] | None
    rank: int
    unknowns: int
    identifiable: bool


@dataclass(frozen=True)
class SelectionAudit:
    centered_stencil: ComponentSelectionAudit
    endpoint_average: ComponentSelectionAudit
    identifiable: bool


def _audit(
    equations: tuple[tuple[str, tuple[Fraction, ...], Fraction], ...],
    unknowns: int,
    drop: str | None,
) -> ComponentSelectionAudit:
    names = {name for name, _, _ in equations}
    if drop is not None and drop not in names:
        raise ValueError(f"unknown selection axiom: {drop}")
    active = tuple((row, rhs) for name, row, rhs in equations if name != drop)
    matrix = tuple(row for row, _ in active)
    rhs = tuple(value for _, value in active)
    matrix_rank = rank(matrix, ncols=unknowns)
    identifiable = matrix_rank == unknowns
    solution = solve_unique(matrix, rhs) if identifiable else None
    return ComponentSelectionAudit(solution, matrix_rank, unknowns, identifiable)


def audit_centered_stencil(drop: str | None = None) -> ComponentSelectionAudit:
    zero = Fraction(0)
    # constant_exact = odd_center + odd_endpoints.  Thus removing any one of
    # those three redundant rows retains rank three; removing affine_exact,
    # the normalization row, reduces the exact system to rank two.
    return _audit(
        (
            ("constant_exact", (Fraction(1), Fraction(1), Fraction(1)), zero),
            ("odd_center", (zero, Fraction(1), zero), zero),
            ("odd_endpoints", (Fraction(1), zero, Fraction(1)), zero),
            ("affine_exact", (Fraction(1), zero, Fraction(-1)), Fraction(1)),
        ),
        3,
        drop,
    )


def audit_endpoint_average(drop: str | None = None) -> ComponentSelectionAudit:
    # Both endpoint equations are independent, so either removal leaves rank one.
    return _audit(
        (
            ("constant_exact", (Fraction(1), Fraction(1)), Fraction(1)),
            ("endpoint_symmetry", (Fraction(1), Fraction(-1)), Fraction(0)),
        ),
        2,
        drop,
    )


def audit_selection() -> SelectionAudit:
    centered_stencil = audit_centered_stencil()
    endpoint_average = audit_endpoint_average()
    return SelectionAudit(
        centered_stencil,
        endpoint_average,
        centered_stencil.identifiable and endpoint_average.identifiable,
    )
