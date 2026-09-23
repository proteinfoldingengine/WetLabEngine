"""Reference oracle: parent transport and holonomy on every basis field."""
from __future__ import annotations
from fractions import Fraction
from dataclasses import replace
from operator_types import Operator


def reference_operator(carrier, presentation=None) -> Operator:
    from bootstrap import load_pinned_modules
    from pathlib import Path
    parent = load_pinned_modules(Path(__file__).resolve().parents[4])
    construct = parent['transport'].construct_transport
    holonomy = parent['holonomy'].linearized_holonomy
    complex_, baseline = carrier.complex, carrier.baseline
    labels, cycles = complex_.labels, complex_.cycles
    rows = [[] for _ in range(4 * len(cycles))]
    for j in range(len(labels)):
        field = tuple(Fraction(k == j) for k in range(len(labels)))
        transport = construct(complex_, baseline, field, presentation=presentation)
        presented = replace(baseline, transports=transport.baseline)
        for face_index, cycle in enumerate(cycles):
            matrix = holonomy(presented, transport, cycle)
            for a in range(2):
                for b in range(2):
                    rows[4 * face_index + 2 * a + b].append(matrix[a][b])
    return Operator(labels, cycles, tuple(tuple(row) for row in rows))
