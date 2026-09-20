from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


@dataclass(frozen=True)
class SourceTarget:
    labels: tuple[int, ...]
    centered_sources: tuple[tuple[Fraction, ...], ...]
    neighbors: frozenset[frozenset[int]]


def construct_source_target(centered_sources, signed_support) -> SourceTarget:
    centered_sources = tuple(tuple(row) for row in centered_sources)
    if len(centered_sources) < 2:
        raise ValueError("at least two centered sources required")
    dimension = len(centered_sources[0])
    if dimension < 2 or len(centered_sources) != dimension:
        raise ValueError("square centered source family required")
    if any(len(row) != dimension for row in centered_sources):
        raise ValueError("centered source dimension mismatch")
    if any(
        isinstance(value, bool) or not isinstance(value, (int, Fraction))
        for row in centered_sources
        for value in row
    ):
        raise TypeError("exact integer or Fraction sources required")
    centered_sources = tuple(
        tuple(Fraction(value) for value in row) for row in centered_sources
    )
    if any(sum(row, Fraction(0)) != 0 for row in centered_sources):
        raise ValueError("sources must be centered")

    signed_support = tuple(tuple(row) for row in signed_support)
    if not signed_support or any(len(row) != dimension for row in signed_support):
        raise ValueError("signed support dimension mismatch")
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for row in signed_support
        for value in row
    ):
        raise TypeError("integer signed-support entries required")
    if any(value not in (-1, 0, 1) for row in signed_support for value in row):
        raise ValueError("signed-support entries must be -1, 0, or 1")
    if any(
        all(row[column] == 0 for row in signed_support)
        for column in range(dimension)
    ):
        raise ValueError("source label has no signed support")
    edges = set()
    for row in signed_support:
        incident = tuple(index for index, value in enumerate(row) if value)
        for first, second in combinations(incident, 2):
            edges.add(frozenset((first, second)))
    return SourceTarget(
        tuple(range(dimension)),
        centered_sources,
        frozenset(edges),
    )
