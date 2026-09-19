from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class IncidenceTarget:
    labels: tuple[int, ...]
    neighbors: frozenset[frozenset[int]]
    degrees: tuple[int, ...]
    connected: bool
    distances: tuple[tuple[int | None, ...], ...]


def construct_incidence_target(signed_support) -> IncidenceTarget:
    rows = tuple(tuple(row) for row in signed_support)
    if not rows or not rows[0]:
        raise ValueError("nonempty signed support required")
    count = len(rows[0])
    if count < 2:
        raise ValueError("at least two face columns required")
    if any(len(row) != count for row in rows):
        raise ValueError("ragged signed support")
    if any(isinstance(value, bool) or not isinstance(value, int) for row in rows for value in row):
        raise TypeError("integer signed-support entries required")
    if any(value not in (-1, 0, 1) for row in rows for value in row):
        raise ValueError("signed-support entries must be -1, 0, or 1")
    if any(all(row[column] == 0 for row in rows) for column in range(count)):
        raise ValueError("face column has no support")
    edges = set()
    for row in rows:
        for first, second in combinations((i for i, value in enumerate(row) if value), 2):
            edges.add(frozenset((first, second)))
    neighbors = frozenset(edges)
    adjacency = [set() for _ in range(count)]
    for edge in neighbors:
        first, second = tuple(edge)
        adjacency[first].add(second); adjacency[second].add(first)
    distances = []
    for source in range(count):
        row = [None] * count; row[source] = 0; queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(adjacency[current]):
                if row[neighbor] is None:
                    row[neighbor] = row[current] + 1; queue.append(neighbor)
        distances.append(tuple(row))
    distances = tuple(distances)
    return IncidenceTarget(tuple(range(count)), neighbors, tuple(len(row) for row in adjacency), all(value is not None for row in distances for value in row), distances)
