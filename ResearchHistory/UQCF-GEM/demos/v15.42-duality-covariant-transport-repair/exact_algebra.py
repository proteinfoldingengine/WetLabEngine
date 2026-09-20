from __future__ import annotations

from fractions import Fraction
from typing import Iterable

MatrixQ = tuple[tuple[Fraction, ...], ...]
VectorQ = tuple[Fraction, ...]


def _q(value) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("exact integer or Fraction required")
    return Fraction(value)


def matrix(rows: Iterable[Iterable]) -> MatrixQ:
    result = tuple(tuple(_q(value) for value in row) for row in rows)
    if result and len({len(row) for row in result}) != 1:
        raise ValueError("ragged matrix")
    return result


def shape(value: MatrixQ, ncols: int | None = None) -> tuple[int, int]:
    value = matrix(value)
    columns = len(value[0]) if value else (0 if ncols is None else ncols)
    if type(columns) is not int or columns < 0:
        raise ValueError("invalid column count")
    return len(value), columns


def identity(dimension: int) -> MatrixQ:
    if type(dimension) is not int or dimension < 0:
        raise ValueError("nonnegative integer dimension required")
    return tuple(
        tuple(Fraction(i == j) for j in range(dimension))
        for i in range(dimension)
    )


def transpose(value: MatrixQ, ncols: int | None = None) -> MatrixQ:
    value = matrix(value)
    rows, columns = shape(value, ncols)
    return tuple(tuple(value[i][j] for i in range(rows)) for j in range(columns))


def matmul(left: MatrixQ, right: MatrixQ) -> MatrixQ:
    left, right = matrix(left), matrix(right)
    left_rows, left_columns = shape(left)
    right_rows, right_columns = shape(right)
    if left_columns != right_rows:
        raise ValueError("matrix dimension mismatch")
    return tuple(
        tuple(
            sum(
                (left[i][k] * right[k][j] for k in range(left_columns)),
                Fraction(0),
            )
            for j in range(right_columns)
        )
        for i in range(left_rows)
    )


def matvec(value: MatrixQ, vector: Iterable) -> VectorQ:
    value = matrix(value)
    vector = tuple(_q(item) for item in vector)
    rows, columns = shape(value)
    if columns != len(vector):
        raise ValueError("matrix/vector dimension mismatch")
    return tuple(
        sum((value[i][j] * vector[j] for j in range(columns)), Fraction(0))
        for i in range(rows)
    )


def add(left: MatrixQ, right: MatrixQ) -> MatrixQ:
    left, right = matrix(left), matrix(right)
    if shape(left) != shape(right):
        raise ValueError("matrix dimension mismatch")
    rows, columns = shape(left)
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(columns))
        for i in range(rows)
    )


def scale(scalar, value: MatrixQ) -> MatrixQ:
    scalar, value = _q(scalar), matrix(value)
    return tuple(tuple(scalar * item for item in row) for row in value)


def rref(rows: Iterable[Iterable], ncols: int | None = None):
    dense = matrix(rows)
    columns = len(dense[0]) if dense else ncols
    if columns is None or type(columns) is not int or columns < 0:
        raise ValueError("empty matrix requires explicit nonnegative ncols")
    if dense and len(dense[0]) != columns:
        raise ValueError("explicit ncols does not match matrix width")
    sparse = [
        {column: value for column, value in enumerate(row) if value}
        for row in dense
    ]
    pivots = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (
                row
                for row in range(pivot_row, len(sparse))
                if sparse[row].get(column)
            ),
            None,
        )
        if selected is None:
            continue
        sparse[pivot_row], sparse[selected] = sparse[selected], sparse[pivot_row]
        pivot = sparse[pivot_row][column]
        sparse[pivot_row] = {
            key: value / pivot for key, value in sparse[pivot_row].items()
        }
        for row in range(len(sparse)):
            if row == pivot_row or not sparse[row].get(column):
                continue
            factor = sparse[row][column]
            for key, value in sparse[pivot_row].items():
                sparse[row][key] = sparse[row].get(key, Fraction(0)) - factor * value
                if sparse[row][key] == 0:
                    del sparse[row][key]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(sparse):
            break
    reduced = tuple(
        tuple(row.get(column, Fraction(0)) for column in range(columns))
        for row in sparse
    )
    return reduced, tuple(pivots)


def rank(value: MatrixQ, ncols: int | None = None) -> int:
    value = matrix(value)
    columns = len(value[0]) if value else ncols
    if columns is None:
        raise ValueError("empty matrix requires explicit nonnegative ncols")
    return len(rref(value, ncols=columns)[1])


def nullspace(value: MatrixQ, ncols: int | None = None) -> tuple[VectorQ, ...]:
    value = matrix(value)
    columns = len(value[0]) if value else ncols
    if columns is None:
        raise ValueError("empty matrix requires explicit nonnegative ncols")
    reduced, pivots = rref(value, ncols=columns)
    pivot_rows = {pivot: row for row, pivot in enumerate(pivots)}
    free = tuple(column for column in range(columns) if column not in pivot_rows)
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * columns
        vector[free_column] = Fraction(1)
        for pivot, row in pivot_rows.items():
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return tuple(basis)


def solve_unique(value: MatrixQ, rhs: VectorQ) -> VectorQ:
    value = matrix(value)
    rhs = tuple(_q(item) for item in rhs)
    rows, columns = shape(value)
    if rows != len(rhs):
        raise ValueError("matrix/right-hand-side dimension mismatch")
    augmented = tuple(row + (rhs_value,) for row, rhs_value in zip(value, rhs))
    reduced, pivots = rref(augmented, ncols=columns + 1)
    if columns in pivots:
        raise ValueError("inconsistent exact system")
    coefficient_pivots = tuple(pivot for pivot in pivots if pivot < columns)
    if coefficient_pivots != tuple(range(columns)):
        raise ValueError("nonunique exact system")
    solution = tuple(reduced[row][-1] for row in range(columns))
    if matvec(value, solution) != rhs:
        raise ArithmeticError("exact solve residual is nonzero")
    return solution
