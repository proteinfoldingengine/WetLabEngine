from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import sys
import numpy as np
import exact_linear as ql

BASELINE_BLOB = '99110f943550751645539c0c8a7339024d7fefd3'
REPO_ROOT = Path(__file__).resolve().parents[4]
BASELINE_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py')
D4 = (
    ((1,0),(0,1)), ((0,-1),(1,0)), ((-1,0),(0,-1)), ((0,1),(-1,0)),
    ((-1,0),(0,1)), ((1,0),(0,-1)), ((0,1),(1,0)), ((0,-1),(-1,0)),
)


def _git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def verify_baseline(path: Path | None = None, expected_blob: str = BASELINE_BLOB) -> str:
    p = (REPO_ROOT / BASELINE_REL) if path is None else Path(path)
    actual = _git_blob(p)
    if actual != expected_blob:
        raise ValueError(f'frozen v15.25 baseline changed: {actual}')
    return actual


def load_frozen_complex(L: int = 7, path: Path | None = None, expected_blob: str = BASELINE_BLOB):
    p = (REPO_ROOT / BASELINE_REL) if path is None else Path(path)
    verify_baseline(p, expected_blob)
    name = f'_v1528_frozen_canary_{hash(str(p)) & 0xffffffff:x}'
    spec = importlib.util.spec_from_file_location(name, p)
    if spec is None or spec.loader is None:
        raise ImportError(p)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.torus_complex(L)


@dataclass(frozen=True)
class SignedPermutation:
    image: tuple[int, ...]
    sign: tuple[int, ...]

    def validate(self) -> None:
        if len(self.image) != len(self.sign) or sorted(self.image) != list(range(len(self.image))):
            raise ValueError('not a permutation')
        if any(s not in (-1, 1) for s in self.sign):
            raise ValueError('signs must be ±1')

    def matrix_int(self) -> np.ndarray:
        self.validate()
        m = np.zeros((len(self.image), len(self.image)), dtype=int)
        for i, (j, s) in enumerate(zip(self.image, self.sign)):
            m[j, i] = s
        return m

    def apply(self, vector) -> tuple[Fraction, ...]:
        self.validate()
        if len(vector) != len(self.image):
            raise ValueError('vector dimension mismatch')
        out = [Fraction(0) for _ in self.image]
        for i, (j, s) in enumerate(zip(self.image, self.sign)):
            out[j] += Fraction(s) * Fraction(vector[i])
        return tuple(out)

    def compose(self, other: 'SignedPermutation') -> 'SignedPermutation':
        self.validate(); other.validate()
        if len(self.image) != len(other.image):
            raise ValueError('permutation dimension mismatch')
        image = tuple(self.image[other.image[i]] for i in range(len(self.image)))
        sign = tuple(other.sign[i] * self.sign[other.image[i]] for i in range(len(self.image)))
        return SignedPermutation(image, sign)


@dataclass(frozen=True)
class CellAutomorphism:
    matrix: tuple[tuple[int, int], tuple[int, int]]
    translation: tuple[int, int]
    L: int

    def __post_init__(self):
        if self.matrix not in D4 or type(self.L) is not int or self.L < 3:
            raise ValueError('invalid torus automorphism')
        if any(type(x) is not int for x in self.translation):
            raise ValueError('integer translation required')

    def apply_vertex(self, v: tuple[int, int]) -> tuple[int, int]:
        a = self.matrix
        return ((a[0][0]*v[0] + a[0][1]*v[1] + self.translation[0]) % self.L,
                (a[1][0]*v[0] + a[1][1]*v[1] + self.translation[1]) % self.L)

    def compose(self, other: 'CellAutomorphism') -> 'CellAutomorphism':
        if self.L != other.L:
            raise ValueError('different tori')
        a, b = self.matrix, other.matrix
        m = ((a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]),
             (a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]))
        bt = other.translation
        t = ((a[0][0]*bt[0] + a[0][1]*bt[1] + self.translation[0]) % self.L,
             (a[1][0]*bt[0] + a[1][1]*bt[1] + self.translation[1]) % self.L)
        return CellAutomorphism(m, t, self.L)


def torus_automorphisms(L: int = 7) -> tuple[CellAutomorphism, ...]:
    if type(L) is not int or L < 3:
        raise ValueError('L>=3 integer required')
    return tuple(CellAutomorphism(m, (tx, ty), L)
                 for m in D4 for tx in range(L) for ty in range(L))


def vertex_action(c, g: CellAutomorphism) -> SignedPermutation:
    if c.L != g.L:
        raise ValueError('automorphism/complex size mismatch')
    image = tuple(c.vertex_index[g.apply_vertex(v)] for v in c.vertices)
    return SignedPermutation(image, tuple(1 for _ in image))


def edge_action(c, g: CellAutomorphism) -> SignedPermutation:
    if c.L != g.L:
        raise ValueError('automorphism/complex size mismatch')
    lookup = {}
    for i, (u, v, _kind) in enumerate(c.edges):
        lookup[(u, v)] = (i, 1)
        lookup[(v, u)] = (i, -1)
    image, sign = [], []
    for u, v, _kind in c.edges:
        key = (g.apply_vertex(u), g.apply_vertex(v))
        if key not in lookup:
            raise ArithmeticError(f'transformed edge is not a cell edge: {key}')
        j, s = lookup[key]
        image.append(j); sign.append(s)
    result = SignedPermutation(tuple(image), tuple(sign)); result.validate(); return result


def face_action(c, g: CellAutomorphism) -> SignedPermutation:
    p1 = edge_action(c, g)
    b2 = c.B2.astype(int)
    lookup = {}
    for f in range(b2.shape[1]):
        col = tuple(int(x) for x in b2[:, f])
        lookup[col] = (f, 1)
        lookup[tuple(-x for x in col)] = (f, -1)
    p1m = p1.matrix_int()
    image, sign = [], []
    for f in range(b2.shape[1]):
        transformed = tuple(int(x) for x in (p1m @ b2[:, f]))
        if transformed not in lookup:
            raise ArithmeticError('transformed face boundary not found')
        j, s = lookup[transformed]
        image.append(j); sign.append(s)
    result = SignedPermutation(tuple(image), tuple(sign)); result.validate(); return result


@dataclass(frozen=True)
class SubspaceBasis:
    columns: tuple[tuple[Fraction, ...], ...]
    coordinate_indices: tuple[int, ...]

    def __post_init__(self):
        if len(self.columns) != len(self.coordinate_indices):
            raise ValueError('basis coordinate count mismatch')
        if self.columns:
            n = len(self.columns[0])
            if any(len(c) != n for c in self.columns):
                raise ValueError('basis column dimension mismatch')
            if len(set(self.coordinate_indices)) != len(self.coordinate_indices):
                raise ValueError('duplicate coordinate index')

    @property
    def ambient_dimension(self) -> int:
        return len(self.columns[0]) if self.columns else 0

    @property
    def dimension(self) -> int:
        return len(self.columns)

    def combine(self, coords) -> tuple[Fraction, ...]:
        coords = tuple(Fraction(x) for x in coords)
        if len(coords) != self.dimension:
            raise ValueError('coordinate dimension mismatch')
        out = [Fraction(0) for _ in range(self.ambient_dimension)]
        for a, col in zip(coords, self.columns):
            for i, x in enumerate(col):
                out[i] += a*x
        return tuple(out)

    def coordinates(self, vector) -> tuple[Fraction, ...]:
        v = tuple(Fraction(x) for x in vector)
        if len(v) != self.ambient_dimension:
            raise ValueError('ambient vector dimension mismatch')
        coords = tuple(v[i] for i in self.coordinate_indices)
        if self.combine(coords) != v:
            raise ValueError('vector not in subspace')
        return coords


def augmentation_basis(n: int) -> SubspaceBasis:
    if type(n) is not int or n < 2:
        raise ValueError('n>=2 required')
    cols = []
    for i in range(n-1):
        v = [Fraction(0) for _ in range(n)]
        v[i] = Fraction(1); v[-1] = Fraction(-1)
        cols.append(tuple(v))
    return SubspaceBasis(tuple(cols), tuple(range(n-1)))


def cycle_basis_exact(B1) -> SubspaceBasis:
    rows = ql.matrix(tuple(tuple(int(x) for x in row) for row in np.asarray(B1)))
    _rr, pivots = ql.rref(rows)
    n = len(rows[0]) if rows else 0
    free = tuple(i for i in range(n) if i not in pivots)
    cols = ql.nullspace(rows)
    if len(cols) != len(free):
        raise ArithmeticError('nullspace/free-column mismatch')
    basis = SubspaceBasis(cols, free)
    for col in cols:
        if any(ql.matvec(rows, col)):
            raise ArithmeticError('invalid cycle basis')
    return basis


def restricted_representation(basis: SubspaceBasis, action: SignedPermutation) -> ql.MatrixQ:
    if basis.ambient_dimension != len(action.image):
        raise ValueError('basis/action dimension mismatch')
    cols = [basis.coordinates(action.apply(col)) for col in basis.columns]
    d = basis.dimension
    return tuple(tuple(cols[j][i] for j in range(d)) for i in range(d))
