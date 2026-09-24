"""Exact rectangular tuple matrices; zero-row operands require explicit width.

An empty tuple cannot encode its column count. Operations accepting an empty
operand expose its width as a keyword; every nonempty operand verifies its width.
"""
from __future__ import annotations
from fractions import Fraction

Matrix = tuple[tuple[Fraction, ...], ...]


def _dimension(value):
    if type(value) is not int or value < 0:
        raise ValueError('matrix shape')
    return value


def shape(matrix: Matrix, ncols: int | None = None) -> tuple[int, int]:
    if type(matrix) is not tuple or any(type(row) is not tuple for row in matrix):
        raise TypeError('matrix must be tuple rows')
    if not matrix and ncols is None:
        raise ValueError('matrix shape: zero-row width required')
    columns = len(matrix[0]) if matrix else _dimension(ncols)
    if ncols is not None and columns != _dimension(ncols):
        raise ValueError('matrix shape')
    if any(len(row) != columns for row in matrix):
        raise ValueError('matrix shape')
    if any(type(value) is not Fraction for row in matrix for value in row):
        raise TypeError('exact Fraction required')
    return len(matrix), columns


def zeros(rows: int, columns: int) -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(_dimension(columns)))
                 for _ in range(_dimension(rows)))


def identity(size: int) -> Matrix:
    _dimension(size)
    return tuple(tuple(Fraction(i == j) for j in range(size)) for i in range(size))


def transpose(matrix: Matrix, *, ncols: int | None = None) -> Matrix:
    rows, columns = shape(matrix, ncols)
    return tuple(tuple(matrix[i][j] for i in range(rows)) for j in range(columns))


def add(a: Matrix, b: Matrix, *, ncols: int | None = None,
        other_ncols: int | None = None) -> Matrix:
    a_shape = shape(a, ncols)
    b_shape = shape(b, other_ncols if other_ncols is not None else ncols)
    if a_shape != b_shape: raise ValueError('matrix shape')
    return tuple(tuple(a[i][j] + b[i][j] for j in range(a_shape[1]))
                 for i in range(a_shape[0]))


def matmul(a: Matrix, b: Matrix, *, left_ncols: int | None = None,
           right_ncols: int | None = None) -> Matrix:
    m, k = shape(a, left_ncols)
    k_other, n = shape(b, right_ncols)
    if k != k_other: raise ValueError('matrix shape')
    return tuple(tuple(sum((a[i][t] * b[t][j] for t in range(k)), Fraction(0))
                       for j in range(n)) for i in range(m))


def apply_matrix(matrix: Matrix, vector: tuple[Fraction, ...], *,
                 ncols: int | None = None) -> tuple[Fraction, ...]:
    m, n = shape(matrix, ncols)
    if type(vector) is not tuple or len(vector) != n:
        raise ValueError('matrix shape')
    if any(type(value) is not Fraction for value in vector):
        raise TypeError('exact Fraction required')
    return tuple(sum((matrix[i][j] * vector[j] for j in range(n)), Fraction(0))
                 for i in range(m))

from dataclasses import dataclass


@dataclass(frozen=True)
class Reduction:
    reduced: Matrix
    pivots: tuple[int, ...]
    operations: tuple[tuple, ...]


def rref(matrix: Matrix, *, ncols: int | None = None) -> Reduction:
    m, n = shape(matrix, ncols)
    rows = [list(row) for row in matrix]
    operations = []
    pivots = []
    cursor = 0
    for col in range(n):
        candidate = next((i for i in range(cursor, m) if rows[i][col]), None)
        if candidate is None: continue
        if candidate != cursor:
            rows[cursor], rows[candidate] = rows[candidate], rows[cursor]
            operations.append(('swap', cursor, candidate))
        factor = 1 / rows[cursor][col]
        rows[cursor] = [factor * v for v in rows[cursor]]
        operations.append(('scale', cursor, factor))
        for i in range(m):
            if i != cursor and rows[i][col]:
                factor = -rows[i][col]
                rows[i] = [x + factor*y for x, y in zip(rows[i], rows[cursor])]
                operations.append(('add', i, cursor, factor))
        pivots.append(col)
        cursor += 1
        if cursor == m: break
    return Reduction(tuple(tuple(row) for row in rows), tuple(pivots), tuple(operations))


def rank(matrix: Matrix, *, ncols: int | None = None) -> int:
    return len(rref(matrix, ncols=ncols).pivots)


def nullspace(matrix: Matrix, *, ncols: int | None = None) -> Matrix:
    _, n = shape(matrix, ncols)
    reduced = rref(matrix, ncols=n)
    free = tuple(col for col in range(n) if col not in reduced.pivots)
    columns = []
    for col in free:
        vector = [Fraction(0)] * n
        vector[col] = Fraction(1)
        for row, pivot in enumerate(reduced.pivots):
            vector[pivot] = -reduced.reduced[row][col]
        columns.append(vector)
    return tuple(tuple(column[i] for column in columns) for i in range(n))


def inverse(matrix: Matrix, *, ncols: int | None = None) -> Matrix:
    n, columns = shape(matrix, ncols)
    if n != columns: raise ValueError('matrix shape')
    if n == 0: return ()
    augmented = tuple(row + identity(n)[i] for i, row in enumerate(matrix))
    reduced = rref(augmented)
    if reduced.pivots[:n] != tuple(range(n)):
        raise ValueError('singular matrix')
    return tuple(row[n:] for row in reduced.reduced)
