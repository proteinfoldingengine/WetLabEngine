from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from exact_algebra import (
    add,
    identity,
    matmul,
    matvec,
    nullspace,
    rank,
    scale,
    solve_unique,
    transpose,
)
from operational_complex import (
    BaselineConnection,
    ConnectionStatus,
    Matrix2,
    OperationalComplex,
)


@dataclass(frozen=True)
class IsotropicLift:
    values: tuple[Matrix2, ...]
    field: tuple[Fraction, ...]
    invariant_dimension: int
    glues_equivariantly: bool
    status: ConnectionStatus
    reason: str | None


@dataclass(frozen=True)
class LinearizedConnection:
    delta_transports: tuple[tuple[tuple[int, int], Matrix2], ...]
    coefficient_rank: int
    augmented_rank: int
    nullity: int
    gauge_dimension: int
    residual_zero: bool
    unique_mod_gauge: bool
    metric_compatibility_exact: bool
    status: ConnectionStatus
    reason: str | None


def _matvec2(value: Matrix2, vector):
    return (
        value[0][0] * vector[0] + value[0][1] * vector[1],
        value[1][0] * vector[0] + value[1][1] * vector[1],
    )


def _symmetric_basis():
    zero = Fraction(0)
    one = Fraction(1)
    return (
        ((one, zero), (zero, zero)),
        ((zero, one), (one, zero)),
        ((zero, zero), (zero, one)),
    )


def _invariant_symmetric_space(actions):
    rows = []
    for action in actions:
        differences = tuple(
            add(matmul(transpose(action), matmul(form, action)), scale(-1, form))
            for form in _symmetric_basis()
        )
        for i in range(2):
            for j in range(2):
                rows.append(tuple(difference[i][j] for difference in differences))
    return nullspace(tuple(rows), ncols=3)


def construct_isotropic_lift(
    complex_: OperationalComplex, field
) -> IsotropicLift:
    if not isinstance(complex_, OperationalComplex):
        raise TypeError("OperationalComplex required")
    field = tuple(field)
    if len(field) != len(complex_.labels):
        raise ValueError("field dimension mismatch")
    if any(
        isinstance(value, bool) or not isinstance(value, (int, Fraction))
        for value in field
    ):
        raise TypeError("exact integer or Fraction field required")
    field = tuple(Fraction(value) for value in field)
    invariant = _invariant_symmetric_space(complex_.d4_actions)
    expected = (Fraction(1), Fraction(0), Fraction(1))
    canonical = len(invariant) == 1 and invariant[0] == expected
    if not canonical:
        return IsotropicLift(
            (),
            field,
            len(invariant),
            False,
            ConnectionStatus.NOT_IDENTIFIABLE,
            "isotropic_lift_not_unique",
        )
    unit = identity(2)
    values = tuple(scale(value, unit) for value in field)
    glues = all(
        matmul(transpose(action), matmul(unit, action)) == unit
        for action in complex_.d4_actions
    )
    return IsotropicLift(
        values,
        field,
        len(invariant),
        glues,
        ConnectionStatus.IDENTIFIABLE,
        None,
    )


def _edge_delta(edge, field_by_label, edge_index, coefficient=Fraction(0)):
    first, second = edge
    canonical = tuple(sorted(edge))
    direction = Fraction(1) if edge == canonical else Fraction(-1)
    low, high = canonical
    conformal = direction * (field_by_label[low] - field_by_label[high]) / 2
    unit = identity(2)
    turn = (
        (Fraction(0), -direction),
        (direction, Fraction(0)),
    )
    value = add(scale(conformal, unit), scale(coefficient, turn))
    return value, turn, edge_index[canonical]


def _closure_system(complex_: OperationalComplex, lift: IsotropicLift, edges):
    field_by_label = dict(zip(complex_.labels, lift.field))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    tangent = dict(zip(complex_.directed_edges, complex_.direction_classes))
    rows = []
    rhs = []
    for initial in complex_.cycles:
        oriented_cycles = (
            initial,
            (initial[0], initial[3], initial[2], initial[1]),
        )
        for cycle in oriented_cycles:
            vectors = tuple(
                tangent[(cycle[i], cycle[(i + 1) % 4])] for i in range(4)
            )
            constant = [
                sum(
                    (
                        field_by_label[cycle[i]] * vectors[i][component] / 2
                        for i in range(4)
                    ),
                    Fraction(0),
                )
                for component in range(2)
            ]
            coefficients = [
                [Fraction(0) for _edge in edges] for _component in range(2)
            ]
            for prefix in range(3):
                # Transports are stored in source-to-target order.  Thus the
                # repository's P_10 factor is the edge (x0, x1).
                edge = (cycle[prefix], cycle[prefix + 1])
                fixed, variable, index = _edge_delta(
                    edge, field_by_label, edge_index
                )
                for vector_index in range(prefix + 1, 4):
                    fixed_part = _matvec2(fixed, vectors[vector_index])
                    variable_part = _matvec2(variable, vectors[vector_index])
                    for component in range(2):
                        constant[component] += fixed_part[component]
                        coefficients[component][index] += variable_part[component]
            for component in range(2):
                rows.append(tuple(coefficients[component]))
                rhs.append(-constant[component])
    return tuple(rows), tuple(rhs)


def _metric_compatibility(delta_transports, field_by_label):
    unit = identity(2)
    zero = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    return all(
        add(
            add(transpose(value), value),
            scale(field_by_label[edge[1]] - field_by_label[edge[0]], unit),
        )
        == zero
        for edge, value in delta_transports
    )


def solve_linearized_connection(
    complex_: OperationalComplex,
    baseline: BaselineConnection,
    lift: IsotropicLift,
) -> LinearizedConnection:
    if not isinstance(complex_, OperationalComplex):
        raise TypeError("OperationalComplex required")
    if not isinstance(baseline, BaselineConnection):
        raise TypeError("BaselineConnection required")
    if not isinstance(lift, IsotropicLift):
        raise TypeError("IsotropicLift required")
    if lift.status != ConnectionStatus.IDENTIFIABLE:
        return LinearizedConnection(
            (), 0, 0, 0, 0, False, False, False,
            ConnectionStatus.NOT_IDENTIFIABLE,
            lift.reason,
        )
    edges = tuple(sorted(tuple(sorted(edge)) for edge in complex_.neighbors))
    rows, rhs = _closure_system(complex_, lift, edges)
    coefficient_rank = rank(rows, ncols=len(edges))
    augmented = tuple(row + (value,) for row, value in zip(rows, rhs))
    augmented_rank = rank(augmented, ncols=len(edges) + 1)
    nullity = len(edges) - coefficient_rank
    gauge_dimension = 0
    consistent = coefficient_rank == augmented_rank
    unique_mod_gauge = consistent and nullity == gauge_dimension
    if not unique_mod_gauge:
        return LinearizedConnection(
            (),
            coefficient_rank,
            augmented_rank,
            nullity,
            gauge_dimension,
            False,
            False,
            False,
            ConnectionStatus.NOT_IDENTIFIABLE,
            "connection_not_identifiable",
        )
    solution = solve_unique(rows, rhs)
    residual_zero = matvec(rows, solution) == rhs
    field_by_label = dict(zip(complex_.labels, lift.field))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    delta_transports = tuple(
        (
            edge,
            _edge_delta(edge, field_by_label, edge_index, solution[edge_index[tuple(sorted(edge))]])[0],
        )
        for edge in complex_.directed_edges
    )
    metric_exact = _metric_compatibility(delta_transports, field_by_label)
    status = (
        ConnectionStatus.IDENTIFIABLE
        if residual_zero and metric_exact
        else ConnectionStatus.NOT_IDENTIFIABLE
    )
    return LinearizedConnection(
        delta_transports,
        coefficient_rank,
        augmented_rank,
        nullity,
        gauge_dimension,
        residual_zero,
        unique_mod_gauge and residual_zero and metric_exact,
        metric_exact,
        status,
        None if status == ConnectionStatus.IDENTIFIABLE else "exact_audit_failure",
    )


def differentiate_holonomy(
    baseline: BaselineConnection, perturbation, cycle
):
    cycle = tuple(cycle)
    if len(cycle) != 4 or len(set(cycle)) != 4:
        raise ValueError("four distinct cycle labels required")
    if isinstance(perturbation, LinearizedConnection):
        if not perturbation.unique_mod_gauge:
            raise ValueError("identifiable perturbation required")
        delta_by_edge = dict(perturbation.delta_transports)
    else:
        delta_by_edge = dict(perturbation)
    baseline_by_edge = dict(baseline.transports)
    edges = tuple((cycle[i], cycle[(i + 1) % 4]) for i in range(4))
    try:
        p0, p1, p2, p3 = tuple(baseline_by_edge[edge] for edge in edges)
        d0, d1, d2, d3 = tuple(delta_by_edge[edge] for edge in edges)
    except KeyError as error:
        raise ValueError("cycle edge missing from connection") from error
    return add(
        add(
            matmul(d3, matmul(p2, matmul(p1, p0))),
            matmul(p3, matmul(d2, matmul(p1, p0))),
        ),
        add(
            matmul(p3, matmul(p2, matmul(d1, p0))),
            matmul(p3, matmul(p2, matmul(p1, d0))),
        ),
    )
