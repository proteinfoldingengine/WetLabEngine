"""Independent exact coefficient construction for differentiated holonomy."""
from __future__ import annotations
from fractions import Fraction
from operator_types import Operator
from exact_matrix import add, identity, matmul, zeros


def _gradients(complex_, directions=None):
    """At every label return the two rows of its centered-gradient stencil."""
    labels = complex_.labels
    positions = {label: j for j, label in enumerate(labels)}
    if len(positions) != len(labels): raise ValueError('duplicate labels')
    local = {label: {} for label in labels}
    direction = dict(zip(complex_.directed_edges, complex_.direction_classes, strict=True)) if directions is None else directions
    for (x, y), vector in direction.items():
        if vector in local[x]: raise ValueError('duplicate direction')
        local[x][vector] = y
    axes = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    gradients = {}
    for x in labels:
        rows = []
        for positive in axes:
            negative = tuple(-entry for entry in positive)
            if positive not in local[x] or negative not in local[x]:
                raise ValueError('missing opposite direction')
            row = [Fraction(0)] * len(labels)
            row[positions[local[x][positive]]] += Fraction(1, 2)
            row[positions[local[x][negative]]] -= Fraction(1, 2)
            rows.append(tuple(row))
        gradients[x] = tuple(rows)
    return gradients, direction


def derive_operator(carrier, presentation=None) -> Operator:
    complex_, baseline = carrier.complex, carrier.baseline
    labels, cycles = complex_.labels, complex_.cycles
    if (not baseline.flat or baseline.labels != labels or
            baseline.directed_edges != complex_.directed_edges):
        raise ValueError('baseline mismatch')
    transports = dict(baseline.transports)
    directions = dict(zip(complex_.directed_edges, complex_.direction_classes, strict=True))
    if presentation is not None:
        presentation.validate(complex_)
        gauges = dict(presentation.gauges)
        transports = {edge: matmul(matmul(gauges[edge[1]], value),
                                   tuple(zip(*gauges[edge[0]])))
                      for edge, value in transports.items()}
        directions = {edge: tuple(sum(gauges[edge[0]][i][j]*vector[j] for j in range(2))
                                  for i in range(2)) for edge, vector in directions.items()}
    gradients, directions = _gradients(complex_, directions)
    if len(transports) != len(baseline.transports): raise ValueError('duplicate transport')
    N = len(labels)
    columns = [[] for _ in range(4 * len(cycles))]
    for j, label in enumerate(labels):
        deltas = {}
        for x, y in complex_.directed_edges:
            p_xy, p_yx = transports[(x, y)], transports[(y, x)]
            # Only coefficient j is needed for this basis impulse. Contract
            # the reverse transport with that column directly; the remaining
            # N-1 stencil coefficients belong to the other basis iterations.
            h = tuple((gradients[x][a][j] +
                       sum(p_yx[a][r] * gradients[y][r][j] for r in range(2))) / 2
                      for a in range(2))
            direction = directions[(x, y)]
            b = tuple(tuple((Fraction((x == label) - (y == label), 2)
                             if a == b_index else Fraction(0)) +
                            (h[a] * direction[b_index] -
                             direction[a] * h[b_index]) / 2
                            for b_index in range(2)) for a in range(2))
            deltas[(x, y)] = matmul(p_xy, b)
        for face_index, cycle in enumerate(cycles):
            edges = tuple((cycle[i], cycle[(i + 1) % 4]) for i in range(4))
            total = zeros(2, 2)
            for slot in range(4):
                factors = tuple(deltas[edge] if slot == i else transports[edge]
                                for i, edge in enumerate(edges))
                ordered = identity(2)
                for factor in factors:
                    ordered = matmul(factor, ordered)
                total = add(total, ordered)
            for a in range(2):
                for b in range(2):
                    columns[4 * face_index + 2 * a + b].append(total[a][b])
    return Operator(labels, cycles, tuple(tuple(row) for row in columns))


def require_equal(actual: Operator, expected: Operator) -> Operator:
    if (type(actual) is not Operator or type(expected) is not Operator or
            actual.labels != expected.labels or actual.cycles != expected.cycles or
            len(actual.entries) != 4 * len(actual.cycles) or
            len(expected.entries) != 4 * len(expected.cycles) or
            any(len(row) != len(actual.labels) for row in actual.entries) or
            any(len(row) != len(expected.labels) for row in expected.entries) or
            actual.entries != expected.entries):
        raise ValueError('operator_mismatch')
    return actual
