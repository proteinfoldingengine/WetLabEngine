"""Exact kernel certificates for A=(I+X)(I+Y)Delta/8 on a periodic square.

This algebraic domain is not a physical-carrier admissibility rule. No archive,
source field, floating spectrum, regulator, or fitted threshold enters here.
"""
from __future__ import annotations
from fractions import Fraction as Q
from hashlib import sha256
import json


def _period(L):
    if type(L) is not int or L < 3:
        raise ValueError('period_must_be_integer_at_least_three')
    return L


def _exact(value):
    if type(value) not in (int, Q):
        raise ValueError('exact_rational_required')
    return Q(value)


def _matrix(matrix):
    if not isinstance(matrix, (tuple, list)) or not matrix:
        raise ValueError('nonempty_rectangular_matrix_required')
    if any(not isinstance(row, (tuple, list)) for row in matrix):
        raise ValueError('matrix_rows_required')
    n = len(matrix[0])
    if not n or any(len(row) != n for row in matrix):
        raise ValueError('rectangular_matrix_required')
    return tuple(tuple(_exact(x) for x in row) for row in matrix)


def rational_rank(matrix):
    """Independent rational elimination, without numerical rank tolerances."""
    a = [list(row) for row in _matrix(matrix)]
    pivot = 0
    for col in range(len(a[0])):
        selected = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        unit = a[pivot][col]
        a[pivot] = [v/unit for v in a[pivot]]
        for i in range(pivot+1, len(a)):
            coefficient = a[i][col]
            if coefficient:
                a[i] = [u-coefficient*v for u,v in zip(a[i], a[pivot], strict=True)]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def apply(matrix, vector):
    a = _matrix(matrix)
    if not isinstance(vector, (tuple, list)) or len(vector) != len(a[0]):
        raise ValueError('vector_dimension')
    v = tuple(_exact(x) for x in vector)
    return tuple(sum((x*y for x,y in zip(row, v, strict=True)), Q(0)) for row in a)


def scalar_operator(L):
    """Rows index lower-left face corners; columns index (x,y) as x*L+y."""
    _period(L)
    n = L*L
    def index(x, y):
        return (x % L)*L + y % L
    rows = []
    for x in range(L):
        for y in range(L):
            row = [Q(0)]*n
            for dx,dy in ((0,0),(1,0),(1,1),(0,1)):
                a,b = x+dx, y+dy
                row[index(a,b)] += Q(1,2)
                for ex,ey in ((1,0),(-1,0),(0,1),(0,-1)):
                    row[index(a+ex,b+ey)] -= Q(1,8)
            rows.append(tuple(row))
    return tuple(rows)


def zero_modes(L):
    """Integer indices of the exact zeros; no approximate trigonometry."""
    _period(L)
    return [[k,l] for k in range(L) for l in range(L)
            if (k,l) == (0,0) or (L % 2 == 0 and (2*k == L or 2*l == L))]


def kernel_basis(L):
    """Rows are a rational basis: constant, X-alternating strips, Y strips.

    At even L the last Y strip is omitted to remove the unique checkerboard
    overlap. All nonconstant basis vectors are centered.
    """
    _period(L)
    basis = [[1]*(L*L)]
    if L % 2 == 0:
        basis += [[(-1)**x * int(y == b) for x in range(L) for y in range(L)]
                  for b in range(L)]
        basis += [[(-1)**y * int(x == a) for x in range(L) for y in range(L)]
                  for a in range(L-1)]
    return basis


def _digest(matrix):
    raw = json.dumps([[str(x) for x in row] for row in matrix],
                     separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return sha256(raw).hexdigest()


def spectral_certificate(L):
    _period(L)
    A = scalar_operator(L)
    rank = rational_rank(A)
    c = {'schema': 'uqcf-v1545-task3-spectral-v1', 'L': L,
         'domain': 'PERIODIC_SQUARE_FORMULA_NOT_PHYSICAL_ADMISSIBILITY',
         'rank': rank, 'nullity': L*L-rank, 'centered_nullity': L*L-rank-1,
         'centered_injective': L*L-rank == 1, 'zero_modes': zero_modes(L),
         'kernel_basis': kernel_basis(L), 'operator_sha256': _digest(A),
         'exact': True}
    verify_certificate(c)
    return c


def verify_certificate(c):
    """Check rank, annihilation, independence, completeness and mode count.

    This does not call spectral_certificate or trust its rank. Rank is freshly
    computed on the full scalar matrix, and all reported basis rows are tested.
    """
    keys = {'schema','L','domain','rank','nullity','centered_nullity',
            'centered_injective','zero_modes','kernel_basis','operator_sha256','exact'}
    if type(c) is not dict or set(c) != keys:
        raise ValueError('certificate_schema')
    L = _period(c['L'])
    if (c['schema'] != 'uqcf-v1545-task3-spectral-v1' or
        c['domain'] != 'PERIODIC_SQUARE_FORMULA_NOT_PHYSICAL_ADMISSIBILITY' or
        c['exact'] is not True):
        raise ValueError('certificate_scope')
    if any(type(c[k]) is not int for k in ('rank','nullity','centered_nullity')):
        raise ValueError('certificate_integer')
    A = scalar_operator(L)
    rank = rational_rank(A)
    nullity = L*L-rank
    if (c['rank'],c['nullity'],c['centered_nullity']) != (rank,nullity,nullity-1):
        raise ValueError('certificate_rank')
    if c['centered_injective'] is not (nullity == 1) or c['operator_sha256'] != _digest(A):
        raise ValueError('certificate_operator')
    modes = c['zero_modes']
    if (type(modes) is not list or any(type(p) is not list or len(p) != 2 or
            any(type(x) is not int for x in p) for p in modes) or
            modes != zero_modes(L) or len(modes) != nullity):
        raise ValueError('certificate_modes')
    b = c['kernel_basis']
    if (type(b) is not list or len(b) != nullity or any(type(v) is not list or
            len(v) != L*L or any(type(x) is not int for x in v) for v in b)):
        raise ValueError('certificate_basis_dimension')
    if b[0] != [1]*(L*L) or any(sum(v) != 0 for v in b[1:]):
        raise ValueError('certificate_centering')
    if rational_rank(b) != nullity or any(any(apply(A,v)) for v in b):
        raise ValueError('certificate_kernel')
    return True
