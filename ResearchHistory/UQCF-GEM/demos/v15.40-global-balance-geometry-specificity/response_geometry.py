from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class ResponseGeometry:
    labels: tuple[int, ...]
    work: tuple[tuple[Fraction, ...], ...]
    minimum: Fraction
    neighbors: frozenset[frozenset[int]]
    symmetric: bool
    identity: bool
    separated: bool
    triangle: bool
    pair_count: int
    ordered_triple_count: int


def _exact_vector(vector, dimension=None):
    vector = tuple(vector)
    if dimension is not None and len(vector) != dimension:
        raise ValueError("inconsistent vector dimensions")
    if not vector:
        raise ValueError("nonempty vectors required")
    if any(isinstance(value, bool) or not isinstance(value, (int, Fraction)) for value in vector):
        raise TypeError("vectors require exact integer or Fraction entries")
    return tuple(Fraction(value) for value in vector)


def _subtract(left, right):
    return tuple(x - y for x, y in zip(left, right))


def _dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def construct_response_geometry(labels, sources, responses) -> ResponseGeometry:
    labels, sources, responses = tuple(labels), tuple(sources), tuple(responses)
    if len(labels) < 2:
        raise ValueError("at least two labels required")
    if len(set(labels)) != len(labels):
        raise ValueError("duplicate labels")
    if any(isinstance(label, bool) or not isinstance(label, int) for label in labels):
        raise TypeError("integer labels required")
    if len(sources) != len(labels) or len(responses) != len(labels):
        raise ValueError("family length mismatch")
    sources = tuple(_exact_vector(vector) for vector in sources)
    dimension = len(sources[0])
    if any(len(vector) != dimension for vector in sources):
        raise ValueError("inconsistent vector dimensions")
    responses = tuple(_exact_vector(vector, dimension) for vector in responses)
    count = len(labels)
    work = tuple(tuple(_dot(_subtract(sources[i], sources[j]), _subtract(responses[i], responses[j])) for j in range(count)) for i in range(count))
    identity = all(work[i][i] == 0 for i in range(count))
    symmetric = all(work[i][j] == work[j][i] for i in range(count) for j in range(count))
    separated = all(work[i][j] > 0 for i in range(count) for j in range(count) if i != j)
    triangle = all(work[i][k] <= work[i][j] + work[j][k] for i, j, k in product(range(count), repeat=3))
    minimum = min(work[i][j] for i in range(count) for j in range(i + 1, count))
    neighbors = frozenset(frozenset((labels[i], labels[j])) for i in range(count) for j in range(i + 1, count) if work[i][j] == minimum)
    return ResponseGeometry(labels, work, minimum, neighbors, symmetric, identity, separated, triangle, count * (count - 1) // 2, count**3)


def metric_passes(geometry: ResponseGeometry) -> bool:
    return all((geometry.symmetric, geometry.identity, geometry.separated, geometry.triangle))
