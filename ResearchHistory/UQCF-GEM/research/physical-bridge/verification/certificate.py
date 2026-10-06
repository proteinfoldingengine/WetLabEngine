"""Certificate route for A12's frozen bounded verification.

No transversal oracle is imported. Integer masks represent supports; coordinates
are calculated from incidence. Cached field dictionaries are read-only by
convention: prediction always constructs new dictionaries, never mutates them.
"""
from functools import lru_cache
from itertools import combinations, product
from math import inf
from typing import Iterator

Roots = tuple[int, ...]
Move = tuple[str, int, int]
Fields = dict[str, dict[int, int]]


def validate(p: int, roots: Roots) -> None:
    if not isinstance(p, int) or p < 0:
        raise ValueError('Palette size must be a nonnegative integer')
    if any(not isinstance(s, int) or s < 0 or s >= (1 << p) for s in roots):
        raise ValueError('Support contains a label outside the palette')


@lru_cache(maxsize=None)
def indices(p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    pairs = tuple((1 << x) | (1 << y) for x, y in combinations(range(p), 2))
    covers = tuple(h for h in range(1 << p) if h.bit_count() <= 4)
    return pairs, covers


@lru_cache(maxsize=None)
def fields(p: int, roots: Roots) -> Fields:
    validate(p, roots)
    pairs, covers = indices(p)
    return {'W': {k: sum((s & k) == 0 for s in roots) for k in pairs},
            'C': {h: int(all(s & h for s in roots)) for h in covers}}


def syntax(p: int, roots: Roots, move: Move) -> bool:
    kind, i, x = move
    if kind not in ('add', 'del') or not 0 <= i < len(roots) or not 0 <= x < p:
        return False
    present = bool(roots[i] & (1 << x))
    return not present if kind == 'add' else present


def apply(p: int, roots: Roots, move: Move) -> Roots:
    if not syntax(p, roots, move):
        raise ValueError('Unavailable incidence syntax')
    _, i, x = move
    return roots[:i] + (roots[i] ^ (1 << x),) + roots[i + 1:]


def predict(p: int, roots: Roots, move: Move) -> Fields:
    if not syntax(p, roots, move):
        raise ValueError('Unavailable incidence syntax')
    kind, i, x = move
    bit, s = 1 << x, roots[i]
    old = fields(p, roots)
    if kind == 'add':
        w = {k: value - int(bool(k & bit) and not (s & k))
             for k, value in old['W'].items()}
        c = {h: int(bool(value) or (bool(h & bit) and not (s & h)
                  and all(roots[j] & h for j in range(len(roots)) if j != i)))
             for h, value in old['C'].items()}
    else:
        w = {k: value + int(bool(k & bit) and (s & k) == bit)
             for k, value in old['W'].items()}
        c = {h: int(bool(value) and (s & h) != bit)
             for h, value in old['C'].items()}
    return {'W': w, 'C': c}


def margin(p: int, roots: Roots, move: Move) -> int | float:
    if not syntax(p, roots, move):
        raise ValueError('Unavailable incidence syntax')
    kind, i, x = move
    bit, s = 1 << x, roots[i]
    old = fields(p, roots)
    if kind == 'add':
        return min((v for k, v in old['W'].items()
                    if (k & bit) and not (s & k)), default=inf)
    remaining = s & ~bit
    return sum(bool(v) and bool(remaining & h) for h, v in old['C'].items())


def protected(p: int, roots: Roots, floors: tuple[int, ...]) -> bool:
    if len(roots) != len(floors) or any(f < 1 or s.bit_count() < f
                                       for s, f in zip(roots, floors)):
        return False
    old = fields(p, roots)
    return p >= 2 and all(v >= 1 for v in old['W'].values()) and any(old['C'].values())


def legal(p: int, roots: Roots, floors: tuple[int, ...], move: Move) -> bool:
    """The candidate-margin iff is used ONLY on its protected-state domain."""
    if not syntax(p, roots, move):
        return False
    if not protected(p, roots, floors):
        raise ValueError('Candidate-margin legality requires a protected source state')
    kind, i, _ = move
    if kind == 'add':
        return margin(p, roots, move) >= 2
    return roots[i].bit_count() - 1 >= floors[i] and margin(p, roots, move) >= 1


def universe(p: int, m: int) -> Iterator[tuple[Roots, tuple[int, ...]]]:
    """Primary construction: Cartesian product of support/floor pairs."""
    options = tuple((s, f) for s in range(1, 1 << p)
                    for f in range(1, s.bit_count() + 1))
    for row in product(options, repeat=m):
        yield tuple(s for s, _ in row), tuple(f for _, f in row)
