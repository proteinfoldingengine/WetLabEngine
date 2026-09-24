from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from operational_complex import BaselineConnection, ConnectionStatus, OperationalComplex, construct_operational_complex, enumerate_baseline_connection
from projection import Payload


@dataclass(frozen=True)
class Carrier:
    complex: OperationalComplex
    baseline: BaselineConnection
    L: int
    scale: Fraction
    receipt: tuple[tuple[str, object], ...]


def _validate_payload(payload: Payload) -> None:
    if type(payload) is not Payload:
        raise ValueError("invalid_payload_type")
    if isinstance(payload.L, bool) or type(payload.L) is not int or payload.L < 1:
        raise ValueError("invalid_L")
    if type(payload.scale) is not Fraction or payload.scale <= 0:
        raise ValueError("invalid_scale")
    count = payload.L * payload.L
    if type(payload.labels) is not tuple or payload.labels != tuple(range(count)):
        raise ValueError("invalid_labels")
    if (type(payload.work) is not tuple or len(payload.work) != count or
            any(type(row) is not tuple or len(row) != count for row in payload.work)):
        raise ValueError("work_dimension")
    if any(type(value) is not Fraction for row in payload.work for value in row):
        raise ValueError("work_type")
    if any(payload.work[index][index] != 0 for index in range(count)):
        raise ValueError("work_diagonal")
    if any(payload.work[i][j] != payload.work[j][i]
           for i in range(count) for j in range(count)):
        raise ValueError("work_asymmetry")
    off_diagonal = tuple(payload.work[i][j]
                         for i in range(count) for j in range(i + 1, count))
    if not off_diagonal or any(value <= 0 for value in off_diagonal):
        raise ValueError("work_off_diagonal")
    if (type(payload.neighbors) is not tuple or
            any(type(edge) is not tuple or len(edge) != 2 or
                any(type(label) is not int for label in edge)
                for edge in payload.neighbors)):
        raise ValueError("neighbor_type")
    if payload.neighbors != tuple(sorted(set(payload.neighbors))):
        raise ValueError("neighbor_order")
    if any(not 0 <= first < second < count for first, second in payload.neighbors):
        raise ValueError("invalid_neighbor")
    minimum = min(off_diagonal)
    minimum_pairs = tuple((i, j) for i in range(count) for j in range(i + 1, count)
                          if payload.work[i][j] == minimum)
    if payload.neighbors != minimum_pairs:
        raise ValueError("neighbor_work_not_minimum")


def build_carrier(payload: Payload) -> Carrier:
    _validate_payload(payload)
    complex_audit = construct_operational_complex(
        payload.labels, payload.work,
        frozenset(frozenset(edge) for edge in payload.neighbors))
    if complex_audit.status is not ConnectionStatus.IDENTIFIABLE or complex_audit.complex is None:
        raise ValueError(complex_audit.reason or "complex_not_identifiable")
    complex_ = complex_audit.complex
    if complex_.tangent_rank != 2:
        raise ValueError("tangent_rank_not_two")
    baseline_audit = enumerate_baseline_connection(complex_)
    if baseline_audit.status is not ConnectionStatus.IDENTIFIABLE or baseline_audit.connection is None:
        raise ValueError(baseline_audit.reason or "baseline_not_identifiable")
    baseline = baseline_audit.connection
    if baseline.labels != complex_.labels or baseline.directed_edges != complex_.directed_edges:
        raise ValueError("baseline_carrier_mismatch")
    if baseline.gauge_orbit_count != 1:
        raise ValueError("baseline_orbit_not_unique")
    if not baseline.flat:
        raise ValueError("baseline_not_flat")
    receipt = (("status", complex_audit.status.value),
               ("complex_reason", complex_audit.reason),
               ("baseline_status", baseline_audit.status.value),
               ("baseline_reason", baseline_audit.reason),
               ("tangent_rank", complex_.tangent_rank),
               ("gauge_orbit_count", baseline.gauge_orbit_count),
               ("flat", baseline.flat))
    return Carrier(complex_, baseline, payload.L, payload.scale, receipt)
