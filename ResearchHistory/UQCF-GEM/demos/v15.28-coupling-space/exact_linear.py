from __future__ import annotations
from fractions import Fraction
from typing import Iterable

MatrixQ = tuple[tuple[Fraction, ...], ...]
VectorQ = tuple[Fraction, ...]


def q(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def matrix(rows: Iterable[Iterable]) -> MatrixQ:
    rows = tuple(tuple(q(x) for x in row) for row in rows)
    if rows and len({len(r) for r in rows}) != 1:
        raise ValueError('ragged matrix')
    return rows


def shape(a: MatrixQ) -> tuple[int, int]:
    return (len(a), len(a[0]) if a else 0)


def identity(n: int) -> MatrixQ:
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative integer dimension required')
    return matrix(tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n)))


def transpose(a: MatrixQ) -> MatrixQ:
    a = matrix(a)
    r, c = shape(a)
    return tuple(tuple(a[i][j] for i in range(r)) for j in range(c))


def matmul(a: MatrixQ, b: MatrixQ) -> MatrixQ:
    a = matrix(a); b = matrix(b)
    ra, ca = shape(a); rb, cb = shape(b)
    if ca != rb:
        raise ValueError('matrix dimension mismatch')
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(ca)), Fraction(0))
                       for j in range(cb)) for i in range(ra))


def matvec(a: MatrixQ, v: Iterable) -> VectorQ:
    a = matrix(a); v = tuple(q(x) for x in v)
    r, c = shape(a)
    if len(v) != c:
        raise ValueError('matrix/vector dimension mismatch')
    return tuple(sum((a[i][j] * v[j] for j in range(c)), Fraction(0)) for i in range(r))


def trace(a: MatrixQ) -> Fraction:
    a = matrix(a); r, c = shape(a)
    if r != c:
        raise ValueError('trace requires square matrix')
    return sum((a[i][i] for i in range(r)), Fraction(0))


def rref(rows: Iterable[Iterable], ncols: int | None = None):
    dense = matrix(rows)
    cols = ncols if ncols is not None else (len(dense[0]) if dense else 0)
    if type(cols) is not int or cols < 0:
        raise ValueError('invalid column count')
    if dense and len(dense[0]) != cols:
        raise ValueError('explicit ncols does not match matrix width')
    sparse = [dict((j, v) for j, v in enumerate(row) if v) for row in dense]
    pivots = []
    r = 0
    for c in range(cols):
        p = next((k for k in range(r, len(sparse)) if sparse[k].get(c)), None)
        if p is None:
            continue
        sparse[r], sparse[p] = sparse[p], sparse[r]
        scale = sparse[r][c]
        sparse[r] = {j: v / scale for j, v in sparse[r].items()}
        for k in range(len(sparse)):
            if k == r or not sparse[k].get(c):
                continue
            f = sparse[k][c]
            for j, v in sparse[r].items():
                sparse[k][j] = sparse[k].get(j, Fraction(0)) - f * v
                if sparse[k][j] == 0:
                    del sparse[k][j]
        pivots.append(c)
        r += 1
        if r == len(sparse):
            break
    dense_out = tuple(tuple(row.get(j, Fraction(0)) for j in range(cols)) for row in sparse)
    return dense_out, tuple(pivots)


def rank(a: MatrixQ) -> int:
    return len(rref(a)[1])


def nullspace(a: MatrixQ) -> tuple[VectorQ, ...]:
    a = matrix(a); _, n = shape(a)
    rr, pivots = rref(a)
    pivot_row = {p: i for i, p in enumerate(pivots)}
    free = [j for j in range(n) if j not in pivot_row]
    basis = []
    for f in free:
        v = [Fraction(0) for _ in range(n)]
        v[f] = Fraction(1)
        for p, i in pivot_row.items():
            v[p] = -rr[i][f]
        basis.append(tuple(v))
    return tuple(basis)


def inverse(a: MatrixQ) -> MatrixQ:
    a = matrix(a); n, m = shape(a)
    if n != m:
        raise ValueError('inverse requires square matrix')
    aug = tuple(tuple(a[i][j] for j in range(n)) + tuple(Fraction(1 if i == j else 0) for j in range(n))
                for i in range(n))
    rr, pivots = rref(aug, ncols=2*n)
    if tuple(p for p in pivots if p < n) != tuple(range(n)):
        raise ValueError('singular matrix')
    left = tuple(tuple(rr[i][j] for j in range(n)) for i in range(n))
    if left != identity(n):
        raise ValueError('singular matrix')
    return tuple(tuple(rr[i][j] for j in range(n, 2*n)) for i in range(n))


def conjugate(a: MatrixQ, change: MatrixQ) -> MatrixQ:
    a = matrix(a); change = matrix(change)
    n, m = shape(a)
    if n != m or shape(change) != (n, n):
        raise ValueError('conjugation requires equal square matrices')
    return matmul(matmul(change, a), inverse(change))


def add(a: MatrixQ, b: MatrixQ) -> MatrixQ:
    a = matrix(a); b = matrix(b)
    if shape(a) != shape(b):
        raise ValueError('matrix dimension mismatch')
    return tuple(tuple(a[i][j] + b[i][j] for j in range(shape(a)[1])) for i in range(shape(a)[0]))


def scale(s, a: MatrixQ) -> MatrixQ:
    s = q(s); a = matrix(a)
    return tuple(tuple(s * x for x in row) for row in a)
