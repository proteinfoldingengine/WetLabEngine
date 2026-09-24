"""Independent compact candidate for the certified differentiated-holonomy operator."""
from __future__ import annotations
from fractions import Fraction
from evidence import Operator


def _det(left, right):
    return left[0] * right[1] - left[1] * right[0]


def compact_operator(carrier, presentation=None) -> Operator:
    if presentation is not None:
        raise ValueError("presentation_not_supported_in_task1")
    complex_ = carrier.complex
    labels, cycles = complex_.labels, complex_.cycles
    position = {label: i for i, label in enumerate(labels)}
    if len(position) != len(labels):
        raise ValueError("duplicate_labels")
    adjacency = {label: tuple(complex_.adjacency[position[label]]) for label in labels}
    directions = dict(zip(complex_.directed_edges, complex_.direction_classes, strict=True))
    rows = [[] for _ in range(4 * len(cycles))]
    eighth = Fraction(1, 8)
    for cycle_index, cycle in enumerate(cycles):
        if len(cycle) != 4:
            raise ValueError("non_square_face")
        d0 = directions[(cycle[0], cycle[1])]
        d1 = directions[(cycle[1], cycle[2])]
        orientation = _det(d0, d1)
        if orientation not in (Fraction(-1), Fraction(1)):
            raise ValueError("face_orientation")
        for label in labels:
            lap_sum = Fraction(0)
            for vertex in cycle:
                lap_sum += 4 * Fraction(vertex == label)
                lap_sum -= sum((Fraction(neighbor == label)
                                for neighbor in adjacency[vertex]), Fraction(0))
            chi = orientation * eighth * lap_sum
            values = (Fraction(0), -chi, chi, Fraction(0))
            for slot, value in enumerate(values):
                rows[4 * cycle_index + slot].append(value)
    return Operator(labels, cycles, tuple(tuple(row) for row in rows))


def verify_factorization(carrier, presentation=None, candidate=None):
    expected = compact_operator(carrier, presentation=presentation)
    actual = expected if candidate is None else candidate
    if (type(actual) is not Operator or actual.labels != expected.labels or
            actual.cycles != expected.cycles or actual.entries != expected.entries):
        raise ValueError("factorization_mismatch")
    return {"L": carrier.L, "scale": str(carrier.scale),
            "rows": len(expected.entries), "columns": len(expected.labels), "exact": True}
