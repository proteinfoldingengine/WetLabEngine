"""Exact rational response kernel certificates and independent replay validation."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from operator_types import Operator
from exact_matrix import Matrix, Reduction, shape, rref, nullspace, inverse, matmul, transpose, zeros, apply_matrix


@dataclass(frozen=True)
class KernelResult:
    rank: int
    nullity: int
    pivots: tuple[int, ...]
    null_basis: Matrix
    image_basis: Matrix
    projector: Matrix
    centered_basis: Matrix
    reduction: Reduction


def analyze_kernel(operator: Operator) -> KernelResult:
    a = operator.entries
    m, n = shape(a)
    if n != len(operator.labels): raise ValueError('operator shape')
    reduction = rref(a)
    pivots = reduction.pivots
    z = nullspace(a)
    width = n-len(pivots)
    image = tuple(tuple(row[j] for j in pivots) for row in a)
    centered = nullspace(a + (tuple(Fraction(1) for _ in range(n)),))
    if width:
        zt = transpose(z)
        gram = matmul(zt, z)
        projector = matmul(matmul(z, inverse(gram)), zt)
    else:
        projector = zeros(n, n)
    return KernelResult(len(pivots), width, pivots, z, image,
                        projector, centered, reduction)


def _independent_columns(matrix: Matrix, width: int) -> bool:
    """Independent elimination; deliberately does not invoke the reducer."""
    rows, columns = shape(matrix, width if not matrix else None)
    if columns != width: return False
    work = [list(row) for row in matrix]
    pivot_row = 0
    for col in range(columns):
        candidate = next((i for i in range(pivot_row, rows) if work[i][col]), None)
        if candidate is None: return False
        work[pivot_row], work[candidate] = work[candidate], work[pivot_row]
        for i in range(pivot_row+1, rows):
            if work[i][col]:
                factor = work[i][col] / work[pivot_row][col]
                work[i] = [x-factor*y for x,y in zip(work[i], work[pivot_row])]
        pivot_row += 1
    return True


def _check(operator: Operator, result: KernelResult) -> None:
    a = operator.entries
    m, n = shape(a)
    if n != len(operator.labels): raise ValueError('operator shape')
    r = result.reduction
    shape(r.reduced, ncols=n)
    if len(r.reduced) != m or type(r.pivots) is not tuple or type(r.operations) is not tuple:
        raise ValueError('invalid reduction')
    work = [list(row) for row in a]
    for op in r.operations:
        if type(op) is not tuple or not op: raise ValueError('invalid row operation')
        if op[0] == 'swap' and len(op) == 3:
            _, i, j = op
            if type(i) is not int or type(j) is not int or not (0 <= i < m and 0 <= j < m) or i == j:
                raise ValueError('invalid swap')
            work[i], work[j] = work[j], work[i]
        elif op[0] == 'scale' and len(op) == 3:
            _, i, factor = op
            if type(i) is not int or not 0 <= i < m or type(factor) is not Fraction or not factor:
                raise ValueError('invalid scale')
            work[i] = [factor*v for v in work[i]]
        elif op[0] == 'add' and len(op) == 4:
            _, i, j, factor = op
            if (type(i) is not int or type(j) is not int or not (0 <= i < m and 0 <= j < m)
                    or i == j or type(factor) is not Fraction):
                raise ValueError('invalid add')
            work[i] = [x+factor*y for x,y in zip(work[i], work[j])]
        else: raise ValueError('invalid row operation')
    if tuple(tuple(row) for row in work) != r.reduced: raise ValueError('replay mismatch')
    pivots = r.pivots
    if (any(type(p) is not int or not 0 <= p < n for p in pivots)
            or tuple(sorted(set(pivots))) != pivots or len(pivots) > m):
        raise ValueError('invalid pivots')
    for i, row in enumerate(r.reduced):
        if i < len(pivots):
            pivot = pivots[i]
            if row[pivot] != 1 or any(row[j] for j in range(pivot)):
                raise ValueError('not RREF')
        elif any(row): raise ValueError('not RREF')
    for pivot in pivots:
        if any(r.reduced[i][pivot] != Fraction(i == pivots.index(pivot)) for i in range(m)):
            raise ValueError('not RREF')
    if (type(result.rank) is not int or type(result.nullity) is not int
            or result.rank != len(pivots) or result.nullity != n-len(pivots)
            or result.pivots != pivots): raise ValueError('rank-nullity')
    free = tuple(j for j in range(n) if j not in pivots)
    expected_z = []
    for i in range(n):
        expected_z.append(tuple(Fraction(i == col) if i in free else
                                -r.reduced[pivots.index(i)][col] for col in free))
    shape(result.null_basis, ncols=len(free))
    if result.null_basis != tuple(expected_z): raise ValueError('null basis incomplete')
    shape(result.image_basis, ncols=len(pivots))
    if result.image_basis != tuple(tuple(row[j] for j in pivots) for row in a):
        raise ValueError('image basis')
    if len(result.image_basis) != m or not _independent_columns(result.image_basis, len(pivots)):
        raise ValueError('image dependence')
    # The recorded invertible operations prove every nonpivot column is
    # spanned by pivot columns; check this explicitly on original entries.
    for col in range(n):
        coefficients = tuple(r.reduced[i][col] for i in range(len(pivots)))
        if apply_matrix(result.image_basis, coefficients) != tuple(row[col] for row in a):
            raise ValueError('image span')
    for j in range(len(free)):
        if any(apply_matrix(a, tuple(row[j] for row in result.null_basis))):
            raise ValueError('null response')
    centered_dim = len(free) - bool(any(sum(row[j] for row in result.null_basis) for j in range(len(free))))
    shape(result.centered_basis, ncols=centered_dim)
    if len(result.centered_basis) != n or not _independent_columns(result.centered_basis, centered_dim):
        raise ValueError('centered independence')
    for j in range(centered_dim):
        vector = tuple(row[j] for row in result.centered_basis)
        if sum(vector) or any(apply_matrix(a, vector)):
            raise ValueError('centered response')
    shape(result.projector, ncols=n)
    p = result.projector
    if len(p) != n or transpose(p) != p or matmul(p, p) != p:
        raise ValueError('projector')
    if matmul(a, p) != zeros(m, n) or matmul(p, result.null_basis, right_ncols=len(free)) != result.null_basis:
        raise ValueError('projector kernel')


def verify_kernel(operator: Operator, result: KernelResult) -> bool:
    """Validate replay, RREF, bases and projection without invoking rref."""
    try:
        _check(operator, result)
    except (IndexError, TypeError, KeyError, ZeroDivisionError) as error:
        raise ValueError('invalid kernel certificate') from error
    return True
