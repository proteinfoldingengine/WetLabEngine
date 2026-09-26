"""Exact corrective audit of v15.56 Tasks 31-33.

This is an additional control, not a modification of the frozen experiments.
All matrix identities and feasibility ranks use fractions.Fraction. Float
output is restricted to reproducing the old normalized-ray diagnostic.

For a finite prefix tree and root-containing prefix-closed retained subtree:
    P L_f = L_c S
    C_c S G_f = G_c P C_f
where P sums source over ancestor-retraction fibers and S restricts potentials
to retained vertices. Raw J and balanced C_f J must not be conflated.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
from math import sqrt

CASES = (
    (((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)), ((),(0,),(1,))),
    (((),(0,),(0,0),(0,1),(0,0,0),(0,0,1)), ((),(0,),(0,0))),
    (((),(0,),(1,),(2,),(1,0),(1,1),(2,0)), ((),(0,),(1,),(2,))),
    (((),(0,),(1,),(0,0),(0,0,0),(1,0),(1,0,0)), ((),(0,),(1,),(0,0),(1,0))),
)


def zeros(n: int, m: int) -> list[list[F]]:
    return [[F(0) for _ in range(m)] for _ in range(n)]


def ones(n: int, m: int) -> list[list[F]]:
    return [[F(1) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> list[list[F]]:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(A, B):
    return [[x + y for x, y in zip(a, b)] for a, b in zip(A, B)]


def sub(A, B):
    return [[x - y for x, y in zip(a, b)] for a, b in zip(A, B)]


def scale(A, q):
    return [[F(q) * x for x in row] for row in A]


def mul(A, B):
    if len(A[0]) != len(B):
        raise ValueError('Matrix dimensions do not match')
    return [[sum((x*y for x,y in zip(row,col)), F(0))
             for col in zip(*B)] for row in A]


def flat(A):
    return [x for row in A for x in row]


def maxabs(A):
    return max(map(abs, flat(A)), default=F(0))


def rref(A, pivot_columns=None):
    """Exact elimination; augmented RHS is excluded from pivot search."""
    R = [[F(x) for x in row] for row in A]
    count = len(R[0]) if pivot_columns is None else pivot_columns
    pivots = []
    for col in range(count):
        row = len(pivots)
        pivot = next((i for i in range(row,len(R)) if R[i][col]), None)
        if pivot is None:
            continue
        R[row], R[pivot] = R[pivot], R[row]
        q = R[row][col]
        R[row] = [x/q for x in R[row]]
        for i in range(len(R)):
            if i != row and R[i][col]:
                q = R[i][col]
                R[i] = [x-q*y for x,y in zip(R[i], R[row])]
        pivots.append(col)
    return R, pivots


def rank(A):
    return len(rref(A)[1])


def unique_solution(A, b):
    n = len(A[0])
    R, piv = rref([list(row)+[val] for row,val in zip(A,b)], n)
    inconsistent = any(not any(row[:n]) and row[n] for row in R)
    if inconsistent or len(piv) != n:
        return len(piv), None
    x = [F(0)]*n
    for i,j in enumerate(piv):
        x[j] = R[i][n]
    return len(piv), x


def inverse(A):
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError('Inverse requires a square matrix')
    R, piv = rref([list(a)+e for a,e in zip(A,eye(n))], n)
    if len(piv) != n:
        raise ValueError('Singular matrix')
    return [row[n:] for row in R]


def center(n):
    return sub(eye(n), scale(ones(n,n), F(1,n)))


def green(L):
    n = len(L)
    U = scale(ones(n,n), F(1,n))
    return sub(inverse(add(L,U)), U)


def validate(keys):
    if not keys or any(not isinstance(k,tuple) for k in keys):
        raise ValueError('A nonempty tuple-address carrier is required')
    if any(any(type(x) is not int or x < 0 for x in k) for k in keys):
        raise ValueError('Branch tokens must be nonnegative integers')
    if len(set(keys)) != len(keys) or () not in keys:
        raise ValueError('Unique addresses and the root must be retained')
    if any(k and k[:-1] not in keys for k in keys):
        raise ValueError('Carrier must be prefix closed')


def laplacian(keys):
    validate(keys)
    idx = {k:i for i,k in enumerate(keys)}
    L = zeros(len(keys),len(keys))
    for j,k in enumerate(keys):
        if k:
            i = idx[k[:-1]]
            L[i][i] += 1; L[j][j] += 1
            L[i][j] -= 1; L[j][i] -= 1
    return L


def operators(fine, coarse):
    validate(fine); validate(coarse)
    if not set(coarse).issubset(fine):
        raise ValueError('Coarse carrier must be a subset of the fine carrier')
    n,m = len(fine),len(coarse)
    P,S = zeros(m,n),zeros(m,n)
    for j,k in enumerate(fine):
        v = max((v for v in coarse if k[:len(v)] == v), key=len)
        P[coarse.index(v)][j] = 1
    for i,v in enumerate(coarse):
        S[i][fine.index(v)] = 1
    Lf,Lc = laplacian(fine),laplacian(coarse)
    return dict(P=P, S=S, Lf=Lf, Lc=Lc, Gf=green(Lf), Gc=green(Lc),
                Cf=center(n), Cc=center(m))


def aggregation(fine, coarse, kind):
    d = operators(fine,coarse); P = d['P']
    A = zeros(len(coarse),len(fine))
    for i,v in enumerate(coarse):
        for j,k in enumerate(fine):
            if P[i][j]:
                if kind == 'COUNTING':
                    A[i][j] = F(1)
                elif kind == 'ABS_DEPTH':
                    A[i][j] = F(1,2**len(k))
                elif kind == 'FIBER_DEPTH':
                    A[i][j] = F(1,2**(len(k)-len(v)))
                else:
                    raise ValueError('Unknown diagnostic measure')
        mass = sum(A[i])
        A[i] = [x/mass for x in A[i]]
    return A


def ray_distance(x,y):
    x,y = list(map(float,flat(x))),list(map(float,flat(y)))
    nx,ny = sqrt(sum(v*v for v in x)),sqrt(sum(v*v for v in y))
    if not nx or not ny:
        return None  # A zero response has no projective ray.
    return sqrt(sum((u/nx-v/ny)**2 for u,v in zip(x,y)))


def analyze(fine, coarse):
    n,m = len(fine),len(coarse)
    if m < 2:
        raise ValueError('Projective aggregation classification requires at least two coarse vertices')
    d = operators(fine,coarse)
    P,S,Lf,Lc,Gf,Gc,Cf,Cc = [d[k] for k in ('P','S','Lf','Lc','Gf','Gc','Cf','Cc')]
    target = mul(Gc,P)
    balanced = mul(target,Cf)
    restricted = mul(mul(Cc,S),Gf)
    fiber_sizes = [int(sum(row)) for row in P]
    witness = mul(target,ones(n,1))
    centering_difference = sub(mul(P,Cf),mul(Cc,P))
    background = [[F(1,m)-F(b,n)] for b in fiber_sizes]

    # One fiber-local weight per fine vertex. Test the ENTIRE source space.
    cols = []
    for j in range(n):
        E = zeros(m,n)
        i = next(i for i in range(m) if P[i][j])
        E[i][j] = 1
        cols.append(flat(mul(mul(Cc,E),Gf)))
    raw_matrix = [list(row) for row in zip(*cols, [-x for x in flat(target)])]
    balanced_matrix = [list(row) for row in zip(*cols, [-x for x in flat(balanced)])]
    normalized_matrix = balanced_matrix + [list(row)+[F(0)] for row in P]
    rhs = [F(0)]*len(balanced_matrix) + [F(1)]*m
    rk,solution = unique_solution(normalized_matrix,rhs)
    if solution is None:
        raise ArithmeticError('Unexpected failure of normalized restriction theorem')
    weights,lam = solution[:-1],solution[-1]
    expected_weights = [sum(S[i][j] for i in range(m)) for j in range(n)]

    # An erased contrast remains in the full fine field, but not at retained vertices.
    lost = next((i for i,b in enumerate(fiber_sizes) if b>1), None)
    x = zeros(n,1)
    if lost is not None:
        inds = [j for j in range(n) if P[lost][j]]
        x[inds[0]][0],x[inds[1]][0] = F(1),F(-1)
    fx = mul(Gf,x)
    J = zeros(n,1); J[-1][0]=1
    old_response = mul(target,J)
    old_counting = mul(mul(mul(Cc,aggregation(fine,coarse,'COUNTING')),Gf),J)
    assert mul(P,Lf) == mul(Lc,S)
    assert restricted == balanced
    assert lam == 1 and weights == expected_weights
    return {
        'fine_count':n, 'coarse_count':m,
        'fine_keys':[list(k) for k in fine], 'coarse_keys':[list(k) for k in coarse],
        'fiber_sizes':fiber_sizes,
        'raw_constant_source_coarse_response':[str(z[0]) for z in witness],
        'raw_operator_rank':rank(raw_matrix),
        'raw_operator_nullity':n+1-rank(raw_matrix),
        'balanced_operator_nullity':n+1-rank(balanced_matrix),
        'boundary_identity_residual':str(maxabs(sub(mul(P,Lf),mul(Lc,S)))),
        'balanced_naturality_residual':str(maxabs(sub(restricted,balanced))),
        'centering_discrepancy_rank':rank(centering_difference),
        'centering_residual':str(maxabs(sub(centering_difference,mul(background,ones(1,n))))),
        'normalized_solution_unique':rk == n+1,
        'projective_scale':str(lam),
        'solved_weights':[str(w) for w in weights],
        'restriction_weights':[str(w) for w in expected_weights],
        'strictly_positive_solution':all(w>0 for w in weights),
        'nonnegative_solution':all(w>=0 for w in weights),
        'forgotten_source_pushforward':str(maxabs(mul(P,x))),
        'forgotten_fine_response':str(maxabs(fx)),
        'forgotten_restricted_response':str(maxabs(mul(mul(Cc,S),fx))),
        'kernel_invariance_counterexample':str(maxabs(mul(P,fx))),
        'old_counting_ray_mismatch':ray_distance(old_counting,old_response),
        'depth_aggregation_difference':str(maxabs(sub(aggregation(fine,coarse,'ABS_DEPTH'),
                                                    aggregation(fine,coarse,'FIBER_DEPTH')))),
    }


def run():
    return {
        'schema':'uqcf-v1556-pruning-consistency-audit-v1',
        'source_snapshot':'23b6b4487cad036870246af1b044f5ee41784c92',
        'arithmetic':'EXACT_RATIONAL; FLOAT_ONLY_FOR_LEGACY_RAY_DIAGNOSTIC',
        'distinct_task31_aggregation_operators':2,
        'fitted_parameters':False,
        'theorem':'P L_f = L_c S; C_c S G_f = G_c P C_f',
        'scope':'FINITE_PREFIX_TREES_AND_ROOT_CONTAINING_PREFIX_CLOSED_RETAINED_SUBTREES',
        'cases':[analyze(f,c) for f,c in CASES],
    }

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
