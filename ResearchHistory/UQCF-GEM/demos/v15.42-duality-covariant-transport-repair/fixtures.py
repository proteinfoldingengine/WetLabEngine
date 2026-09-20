from fractions import Fraction


def _validated_labels(L: int, labels: tuple[int, ...] | None) -> tuple[int, ...]:
    if isinstance(L, bool) or not isinstance(L, int) or L < 1:
        raise ValueError("L must be a positive integer")
    carrier = tuple(range(L * L)) if labels is None else tuple(labels)
    if len(carrier) != L * L:
        raise ValueError("labels must contain exactly L squared entries")
    if any(isinstance(label, bool) or not isinstance(label, int) for label in carrier):
        raise TypeError("integer labels required")
    if len(set(carrier)) != len(carrier):
        raise ValueError("labels must be a bijective carrier")
    return carrier


def periodic_square_input(
    L: int, labels: tuple[int, ...] | None = None
) -> tuple[tuple[int, ...], tuple[tuple[Fraction, ...], ...], frozenset[frozenset[int]]]:
    carrier = _validated_labels(L, labels)

    def position(x: int, y: int) -> int:
        return (x % L) + L * (y % L)

    edges = frozenset(
        frozenset((carrier[position(x, y)], carrier[position(x + dx, y + dy)]))
        for x in range(L)
        for y in range(L)
        for dx, dy in ((1, 0), (0, 1))
    )

    def distance(i: int, j: int) -> Fraction:
        ix, iy = i % L, i // L
        jx, jy = j % L, j // L
        dx = min((ix - jx) % L, (jx - ix) % L)
        dy = min((iy - jy) % L, (jy - iy) % L)
        return Fraction(dx * dx + dy * dy)

    work = tuple(
        tuple(distance(i, j) for j in range(L * L))
        for i in range(L * L)
    )
    return carrier, work, edges


def relabeled_edges(data, permutation) -> frozenset[frozenset[int]]:
    labels, _work, edges = data
    labels = tuple(labels)
    permutation = tuple(permutation)
    if len(permutation) != len(labels) or len(set(permutation)) != len(labels):
        raise ValueError("permutation must be a bijection of the carrier")
    if any(isinstance(label, bool) or not isinstance(label, int) for label in permutation):
        raise TypeError("integer labels required")
    replacement = dict(zip(labels, permutation))
    return frozenset(
        frozenset(replacement[label] for label in edge)
        for edge in edges
    )


def relabel_input(data, permutation):
    labels, work, _edges = data
    permutation = tuple(permutation)
    edges = relabeled_edges(data, permutation)
    return permutation, tuple(tuple(row) for row in work), edges
