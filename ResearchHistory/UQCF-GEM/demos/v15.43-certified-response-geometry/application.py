from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

from carriers import Carrier
from holonomy import curvature_invariant, linearized_holonomy
from protocol_types import TransportManifest
from transport import LinearizedTransport, construct_transport


ZERO = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))


@dataclass(frozen=True)
class FieldResult:
    transport: LinearizedTransport
    records: tuple[tuple[tuple[int, int, int, int],
                         tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
                         Fraction], ...]
    zero_count: int
    nonzero_count: int
    histogram: tuple[tuple[Fraction, int], ...]
    invariant_sum: Fraction


def evaluate_field(carrier: Carrier, values: tuple[Fraction, ...],
                   manifest: TransportManifest | None = None) -> FieldResult:
    if type(carrier) is not Carrier:
        raise ValueError("Carrier required")
    if (carrier.baseline.labels != carrier.complex.labels or
            carrier.baseline.directed_edges != carrier.complex.directed_edges):
        raise ValueError("baseline_carrier_mismatch")
    selected = TransportManifest.certified() if manifest is None else manifest
    try:
        selected.validate()
        transport = construct_transport(carrier.complex, carrier.baseline, values,
                                        manifest=selected)
    except (TypeError, ArithmeticError) as error:
        raise ValueError(str(error)) from None
    if not transport.metric_compatibility_exact or not transport.reversal_exact:
        raise ValueError("transport_identity_failure")
    if transport.manifest != TransportManifest.certified():
        raise ValueError("manifest differs from the approved v15.42 protocol")
    records = []
    for cycle in carrier.complex.cycles:
        matrix = linearized_holonomy(carrier.baseline, transport, cycle)
        invariant = curvature_invariant(matrix)
        if invariant < 0:
            raise ValueError("negative_curvature_invariant")
        if (matrix == ZERO) != (invariant == 0):
            raise ValueError("zero_invariant_mismatch")
        records.append((cycle, matrix, invariant))
    frozen_records = tuple(records)
    invariants = tuple(record[2] for record in frozen_records)
    histogram = tuple(sorted(Counter(invariants).items()))
    zero_count = sum(value == 0 for value in invariants)
    return FieldResult(transport, frozen_records, zero_count,
                       len(invariants) - zero_count, histogram,
                       sum(invariants, Fraction(0)))
