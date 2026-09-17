from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528_DIR = REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space'
EXACT_LINEAR_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py')
ACTIONS_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py')
EXACT_LINEAR_BLOB = '05cc1b8cfec70d501408377b5e44190b259a4514'
ACTIONS_BLOB = '7260147cd6ca47ec21634172b44b98de726904af'


def _git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def _verify_inherited() -> None:
    expected = (
        (REPO_ROOT / EXACT_LINEAR_REL, EXACT_LINEAR_BLOB, 'exact_linear.py'),
        (REPO_ROOT / ACTIONS_REL, ACTIONS_BLOB, 'representation_actions.py'),
    )
    for path, blob, label in expected:
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = _git_blob(path)
        if actual != blob:
            raise ValueError(f'frozen v15.28 {label} changed: {actual} != {blob}')


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_INHERITED = None


def _inherited_modules():
    global _INHERITED
    if _INHERITED is None:
        _verify_inherited()
        exact = _load_module('exact_linear', REPO_ROOT / EXACT_LINEAR_REL)
        actions = _load_module('_v1529_frozen_representation_actions', REPO_ROOT / ACTIONS_REL)
        _INHERITED = (exact, actions)
    return _INHERITED


def load_frozen_complex(L: int = 7):
    _exact, actions = _inherited_modules()
    return actions.load_frozen_complex(L=L)


@dataclass(frozen=True)
class FiberRepresentative:
    edge_vector: tuple[int, ...]
    q: tuple[int, ...]

    def __post_init__(self) -> None:
        if any(type(x) is not int for x in self.edge_vector):
            raise ValueError('edge representative must be integral')
        if any(type(x) is not int for x in self.q):
            raise ValueError('coarse source quotient must be integral')


def apply_B1(edge_vector) -> tuple[int, ...]:
    c = load_frozen_complex()
    edge_vector = tuple(edge_vector)
    if len(edge_vector) != c.B1.shape[1]:
        raise ValueError('edge-vector dimension mismatch')
    if any(type(x) is not int for x in edge_vector):
        raise ValueError('integer edge vector required')
    return tuple(
        int(
            sum(
                int(c.B1[v, e]) * edge_vector[e]
                for e in range(c.B1.shape[1])
            )
        )
        for v in range(c.B1.shape[0])
    )


def root_fixture() -> FiberRepresentative:
    c = load_frozen_complex()
    # Exact incidence analogue of v15.25's
    # incidence_defect(c, face=(0,0), edge_slot='bottom', amplitude=1).
    edge_index = int(c.face_loops[(0, 0)][0][0])
    edge_vector = [0 for _ in range(c.B1.shape[1])]
    edge_vector[edge_index] = 1
    edge_vector = tuple(edge_vector)
    return FiberRepresentative(edge_vector, apply_B1(edge_vector))


def canonical_cycle_basis() -> tuple[tuple[int, ...], ...]:
    _exact, actions = _inherited_modules()
    c = load_frozen_complex()
    basis = actions.cycle_basis_exact(c.B1)
    out = []
    for column in basis.columns:
        integral = []
        for value in column:
            value = Fraction(value)
            if value.denominator != 1:
                raise ArithmeticError('inherited cycle basis is not integral')
            integral.append(int(value))
        vector = tuple(integral)
        if any(apply_B1(vector)):
            raise ArithmeticError('inherited cycle basis failed exact B1 kernel check')
        out.append(vector)
    return tuple(out)


def face_shift(
    rep: FiberRepresentative, face_index: int, coefficient: int
) -> FiberRepresentative:
    if type(face_index) is not int or type(coefficient) is not int:
        raise ValueError('integer face index and coefficient required')
    c = load_frozen_complex()
    if not 0 <= face_index < c.B2.shape[1]:
        raise ValueError('face index out of range')
    if len(rep.edge_vector) != c.B1.shape[1]:
        raise ValueError('representative dimension mismatch')
    boundary = tuple(int(c.B2[e, face_index]) for e in range(c.B2.shape[0]))
    shifted = tuple(
        rep.edge_vector[e] + coefficient * boundary[e]
        for e in range(len(rep.edge_vector))
    )
    result = FiberRepresentative(shifted, apply_B1(shifted))
    if result.q != rep.q:
        raise ArithmeticError('face boundary unexpectedly changed q')
    return result


def cycle_shift(
    rep: FiberRepresentative, cycle_vector
) -> FiberRepresentative:
    cycle_vector = tuple(cycle_vector)
    if len(cycle_vector) != len(rep.edge_vector):
        raise ValueError('cycle-vector dimension mismatch')
    if any(type(x) is not int for x in cycle_vector):
        raise ValueError('integer cycle vector required')
    if any(apply_B1(cycle_vector)):
        raise ValueError('cycle vector is not in ker(B1)')
    shifted = tuple(a + z for a, z in zip(rep.edge_vector, cycle_vector))
    result = FiberRepresentative(shifted, apply_B1(shifted))
    if result.q != rep.q:
        raise ArithmeticError('cycle shift unexpectedly changed q')
    return result


def same_coarse_source(a: FiberRepresentative, b: FiberRepresentative) -> bool:
    return a.q == b.q
