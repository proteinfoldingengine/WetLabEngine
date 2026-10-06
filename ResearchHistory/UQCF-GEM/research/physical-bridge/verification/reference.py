"""Direct reference route: set-intersection transversal enumeration.

This module imports no certificate code and never obtains tau or legality from
W, C, A, D, supplied passing cases, or the primary universe generator.
Shared input encoding with certificate.py: tuple of integer support masks.
"""
from functools import lru_cache
from itertools import combinations, product
from math import inf
from typing import Iterable, Iterator

Roots = tuple[int, ...]
Move = tuple[str, int, int]
Identity = tuple[Roots, tuple[int, ...]]


def as_sets(p: int, roots: Roots) -> tuple[frozenset[int], ...]:
    if p < 0 or any(s < 0 or s >= 2 ** p for s in roots):
        raise ValueError('Invalid finite palette/support input')
    return tuple(frozenset(x for x in range(p) if (s // (2 ** x)) % 2)
                 for s in roots)


@lru_cache(maxsize=None)
def tau(p: int, roots: Roots) -> int | float:
    supports = as_sets(p, roots)
    for size in range(p + 1):
        for labels in combinations(range(p), size):
            h = frozenset(labels)
            if all(h.intersection(s) for s in supports):
                return size
    return inf


def apply(p: int, roots: Roots, move: Move) -> Roots:
    kind, i, x = move
    if kind not in ('add', 'del') or not 0 <= i < len(roots) or not 0 <= x < p:
        raise ValueError('Invalid incidence candidate')
    supports = list(as_sets(p, roots))
    if kind == 'add':
        if x in supports[i]:
            raise ValueError('Added incidence is already present')
        supports[i] = supports[i].union((x,))
    else:
        if x not in supports[i]:
            raise ValueError('Deleted incidence is absent')
        supports[i] = supports[i].difference((x,))
    return tuple(sum(2 ** label for label in s) for s in supports)


@lru_cache(maxsize=None)
def legal(p: int, roots: Roots, floors: tuple[int, ...], move: Move) -> bool:
    if len(roots) != len(floors) or any(f < 1 for f in floors):
        return False
    try:
        post = apply(p, roots, move)
    except ValueError:
        return False
    supports = as_sets(p, post)
    return all(len(s) >= f for s, f in zip(supports, floors)) and 3 <= tau(p, post) <= 4


def universe(p: int, m: int) -> Iterator[Identity]:
    """Reference construction: support tuples first, then their floor tuples."""
    supports = tuple(frozenset(c) for r in range(1, p + 1)
                     for c in combinations(range(p), r))
    for row in product(supports, repeat=m):
        roots = tuple(sum(2 ** x for x in s) for s in row)
        for floors in product(*(range(1, len(s) + 1) for s in row)):
            yield roots, tuple(floors)


def coverage_ok(observed: Iterable[Identity], expected: Iterable[Identity]) -> bool:
    actual, target = list(observed), list(expected)
    return (len(actual) == len(set(actual)) and len(target) == len(set(target))
            and set(actual) == set(target))
