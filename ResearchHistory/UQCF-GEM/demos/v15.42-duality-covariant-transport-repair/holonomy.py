"""Exact differentiated holonomy for the certified typed transport."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from exact_algebra import add, identity, matmul, scale, transpose
from operational_complex import BaselineConnection, Matrix2
from transport import LinearizedTransport

Edge = tuple[int, int]
Cycle = tuple[int, int, int, int]
ZERO = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))


@dataclass(frozen=True)
class CurvatureRecord:
    cycle: Cycle
    tangent: Matrix2
    cotangent: Matrix2
    invariant: Fraction


def _matrix(value) -> Matrix2:
    if type(value) is not tuple or len(value) != 2:
        raise ValueError('immutable 2 by 2 matrix required')
    result = []
    for row in value:
        if type(row) is not tuple or len(row) != 2:
            raise ValueError('immutable 2 by 2 matrix required')
        converted = []
        for item in row:
            if isinstance(item, bool) or not isinstance(item, (int, Fraction)):
                raise TypeError('exact integer or Fraction required')
            converted.append(Fraction(item))
        result.append(tuple(converted))
    return tuple(result)


def _cycle(value) -> Cycle:
    if type(value) is not tuple or len(value) != 4:
        raise ValueError('cycle must be an immutable oriented four-cycle')
    if any(isinstance(label, bool) or not isinstance(label, int) for label in value):
        raise TypeError('cycle labels must be integers')
    if len(set(value)) != 4:
        raise ValueError('cycle must contain four distinct vertices')
    return value


def reverse_cycle(cycle: Cycle) -> Cycle:
    cycle = _cycle(cycle)
    return (cycle[0], cycle[3], cycle[2], cycle[1])


def rotate_cycle(cycle: Cycle, steps: int) -> Cycle:
    cycle = _cycle(cycle)
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise TypeError('rotation steps must be an integer')
    if steps < 0 or steps > 3:
        raise ValueError('rotation steps must be between zero and three')
    return cycle[steps:] + cycle[:steps]


def _inputs(baseline, transport, cycle):
    if not isinstance(baseline, BaselineConnection):
        raise TypeError('BaselineConnection required')
    if not isinstance(transport, LinearizedTransport):
        raise TypeError('LinearizedTransport required')
    cycle = _cycle(cycle)
    if tuple(transport.baseline) != tuple(baseline.transports):
        raise ValueError('baseline and transport presentations are incompatible')
    if len(set(baseline.labels)) != len(baseline.labels):
        raise ValueError('baseline labels must be unique')
    if any(vertex not in set(baseline.labels) for vertex in cycle):
        raise ValueError('cycle vertex is absent from baseline carrier')
    edges = tuple((cycle[i], cycle[(i + 1) % 4]) for i in range(4))

    def mapping(values, name):
        try:
            pairs = tuple(values)
            result = dict(pairs)
        except (TypeError, ValueError):
            raise ValueError(f'malformed {name}') from None
        if len(result) != len(pairs):
            raise ValueError(f'duplicate {name} edge')
        for edge, matrix in pairs:
            if type(edge) is not tuple or len(edge) != 2:
                raise ValueError(f'malformed {name} edge')
            _matrix(matrix)
        missing = tuple(edge for edge in edges if edge not in result)
        if missing:
            raise ValueError(f'cycle edge missing from {name}')
        return result

    return (cycle, edges, mapping(baseline.transports, 'baseline'),
            mapping(transport.tangent_deltas, 'tangent deltas'),
            mapping(transport.cotangent_pullback_deltas, 'cotangent pullback deltas'))


def linearized_holonomy(baseline: BaselineConnection,
                         transport: LinearizedTransport,
                         cycle: Cycle) -> Matrix2:
    """Differentiate the four-factor product by degree-one polynomial recurrence."""
    _cycle_value, edges, matrices, deltas, _pullbacks = _inputs(
        baseline, transport, cycle)
    constant, coefficient = identity(2), ZERO
    for edge in edges:
        # (P + eps D)(C + eps K), truncated after degree one.
        coefficient = add(matmul(deltas[edge], constant),
                          matmul(matrices[edge], coefficient))
        constant = matmul(matrices[edge], constant)
    return coefficient


def cotangent_holonomy(baseline: BaselineConnection,
                        transport: LinearizedTransport,
                        cycle: Cycle) -> Matrix2:
    """Compose the stored per-edge pullbacks in their dual (right-product) order."""
    _cycle_value, edges, matrices, _deltas, pullback_deltas = _inputs(
        baseline, transport, cycle)
    constant, coefficient = identity(2), ZERO
    for edge in edges:
        pullback = transpose(matrices[edge])
        # (C + eps K)(P* + eps D*), preserving contravariant order.
        coefficient = add(matmul(coefficient, pullback),
                          matmul(constant, pullback_deltas[edge]))
        constant = matmul(constant, pullback)
    return coefficient


def curvature_invariant(value: Matrix2) -> Fraction:
    value = _matrix(value)
    if add(value, transpose(value)) != ZERO:
        raise ValueError('curvature matrix must have zero symmetric part')
    square = matmul(value, value)
    return -(square[0][0] + square[1][1]) / 2
