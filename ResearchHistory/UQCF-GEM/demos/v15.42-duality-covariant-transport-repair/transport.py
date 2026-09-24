"""Exact tangent connection and its mechanical cotangent pullback.

The certified square substrate uses orthonormal unit direction classes, so its
metric in every permitted D4 presentation is the identity bilinear form.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from exact_algebra import add, identity, matmul, matvec, scale, solve_unique, transpose
from operational_complex import BaselineConnection, Matrix2, OperationalComplex, Vector2
from protocol_types import TransportManifest

Edge = tuple[int, int]


@dataclass(frozen=True)
class FramePresentation:
    gauges: tuple[tuple[int, Matrix2], ...]

    @classmethod
    def identity(cls, complex_: OperationalComplex) -> FramePresentation:
        return cls(tuple((label, identity(2)) for label in complex_.labels))

    def validate(self, complex_: OperationalComplex) -> bool:
        if type(self.gauges) is not tuple:
            raise TypeError('gauges must be an immutable tuple')
        labels = []
        for entry in self.gauges:
            if type(entry) is not tuple or len(entry) != 2:
                raise ValueError('each gauge must pair a label and a matrix')
            label, matrix = entry
            if type(label) is not int:
                raise TypeError('integer gauge label required')
            _validate_matrix(matrix)
            if matrix not in complex_.d4_actions:
                raise ValueError('gauge must be a certified D4 action')
            labels.append(label)
        if len(labels) != len(set(labels)) or set(labels) != set(complex_.labels):
            raise ValueError('gauges must contain each carrier label exactly once')
        return True


@dataclass(frozen=True)
class LinearizedTransport:
    manifest: TransportManifest
    baseline: tuple[tuple[Edge, Matrix2], ...]
    source_endomorphisms: tuple[tuple[Edge, Matrix2], ...]
    tangent_deltas: tuple[tuple[Edge, Matrix2], ...]
    cotangent_pullback_deltas: tuple[tuple[Edge, Matrix2], ...]
    metric_compatibility_exact: bool
    reversal_exact: bool


def _exact(value) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('exact integer or Fraction required')
    return Fraction(value)


def _validate_matrix(matrix: Matrix2) -> None:
    if type(matrix) is not tuple or len(matrix) != 2:
        raise ValueError('immutable 2 by 2 matrix required')
    for row in matrix:
        if type(row) is not tuple or len(row) != 2:
            raise ValueError('immutable 2 by 2 matrix required')
        for value in row:
            _exact(value)


def validate_exact_field(complex_: OperationalComplex, field: tuple[Fraction, ...]):
    if type(field) is not tuple:
        raise TypeError('field must be an immutable tuple')
    if len(field) != len(complex_.labels):
        raise ValueError('field must contain one scalar per carrier label')
    return dict(zip(complex_.labels, (_exact(value) for value in field)))


def _presented_data(complex_, baseline, presentation):
    presentation.validate(complex_)
    if baseline.labels != complex_.labels or baseline.directed_edges != complex_.directed_edges:
        raise ValueError('baseline carrier does not match the operational complex')
    gauges = dict(presentation.gauges)
    transports = {
        (x, y): matmul(gauges[y], matmul(p, transpose(gauges[x])))
        for (x, y), p in baseline.transports
    }
    directions = {
        (x, y): matvec(gauges[x], d)
        for (x, y), d in zip(complex_.directed_edges, complex_.direction_classes)
    }
    return transports, directions


def centered_derivatives(
    complex_: OperationalComplex, baseline: BaselineConnection,
    field: tuple[Fraction, ...], presentation: FramePresentation,
) -> tuple[tuple[int, Vector2], ...]:
    values = validate_exact_field(complex_, field)
    _, directions = _presented_data(complex_, baseline, presentation)
    metric = identity(2)
    axes = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    derivatives = []
    for label in complex_.labels:
        local = {}
        for (x, y), direction in directions.items():
            if x == label:
                if direction in local:
                    raise ValueError('direction must have a unique neighbor')
                local[direction] = y
        pairings = []
        for direction in axes:
            opposite = tuple(-value for value in direction)
            if direction not in local or opposite not in local:
                raise ValueError('missing opposite direction pair')
            pairings.append((values[local[direction]] - values[local[opposite]]) / 2)
        # Rows are d_i^T g; solve for the unique tangent gradient.
        rows = tuple(matvec(metric, direction) for direction in axes)
        derivatives.append((label, solve_unique(rows, tuple(pairings))))
    return tuple(derivatives)


def cotangent_pullback_delta(matrix: Matrix2) -> Matrix2:
    """Differentiate P*: T_y* -> T_x* mechanically as delta(P)^T."""
    _validate_matrix(matrix)
    return transpose(matrix)


def _outer(left: Vector2, right: Vector2) -> Matrix2:
    return tuple(tuple(a * b for b in right) for a in left)


def construct_transport(
    complex_: OperationalComplex, baseline: BaselineConnection,
    field: tuple[Fraction, ...], manifest: TransportManifest | None = None,
    presentation: FramePresentation | None = None,
) -> LinearizedTransport:
    manifest = TransportManifest.certified() if manifest is None else manifest
    manifest.validate()
    values = validate_exact_field(complex_, field)
    presentation = FramePresentation.identity(complex_) if presentation is None else presentation
    p, directions = _presented_data(complex_, baseline, presentation)
    q = dict(centered_derivatives(complex_, baseline, field, presentation))
    unit = identity(2)
    b, delta = {}, {}
    for x, y in complex_.directed_edges:
        endpoint = matvec(p[(y, x)], q[y])
        q_bar = tuple((a + c) / 2 for a, c in zip(q[x], endpoint))
        direction = directions[(x, y)]
        # Lowering with the certified identity metric preserves components.
        skew = scale(Fraction(1, 2), add(
            _outer(q_bar, matvec(unit, direction)),
            scale(-1, _outer(direction, matvec(unit, q_bar))),
        ))
        b[(x, y)] = add(scale((values[x] - values[y]) / 2, unit), skew)
        delta[(x, y)] = matmul(p[(x, y)], b[(x, y)])

    metric_exact = all(
        add(add(matmul(transpose(delta[(x, y)]), p[(x, y)]),
                matmul(transpose(p[(x, y)]), delta[(x, y)])),
            scale(values[y], matmul(transpose(p[(x, y)]), p[(x, y)])))
        == scale(values[x], unit)
        for x, y in complex_.directed_edges
    )
    reversal_exact = all(
        delta[(y, x)] == scale(-1, matmul(p[(y, x)], matmul(delta[(x, y)], p[(y, x)])))
        for x, y in complex_.directed_edges
    )
    if not metric_exact or not reversal_exact:
        raise ArithmeticError('exact differentiated metric or inverse identity failed')
    return LinearizedTransport(
        manifest,
        tuple((edge, p[edge]) for edge in complex_.directed_edges),
        tuple((edge, b[edge]) for edge in complex_.directed_edges),
        tuple((edge, delta[edge]) for edge in complex_.directed_edges),
        tuple((edge, cotangent_pullback_delta(delta[edge])) for edge in complex_.directed_edges),
        metric_exact, reversal_exact,
    )
