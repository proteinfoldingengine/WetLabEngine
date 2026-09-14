from __future__ import annotations
from dataclasses import dataclass, field
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import sys
import numpy as np
import representation_actions as actions
import coupling_solver as solver

REPO_ROOT = Path(__file__).resolve().parents[4]
SELECTOR_BLOB = '623defd0d8284e5d9cba6d8f8679de698e5202bc'
SELECTOR_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/selector_rank.py')

@dataclass(frozen=True)
class CandidateAudit:
    key: str
    role: str
    eligibility: str
    status: str
    dimension: int | None
    orbit_dimension: int | None = None
    character_dimension: int | None = None
    ambient_basis: tuple = ()
    basis_hashes: tuple[str, ...] = ()
    stop_reason: str | None = None
    metadata: dict = field(default_factory=dict)

    @property
    def eligible_physical_candidate(self):
        return self.role == 'PHYSICAL_CANDIDATE' and self.eligibility == 'ELIGIBLE_EXACT_COUPLING_AUDIT'

    def as_dict(self):
        return {'key': self.key, 'role': self.role, 'eligibility': self.eligibility,
                'status': self.status, 'dimension': self.dimension,
                'orbit_dimension': self.orbit_dimension,
                'character_dimension': self.character_dimension,
                'basis_hashes': list(self.basis_hashes), 'stop_reason': self.stop_reason,
                'metadata': self.metadata}


def _signed_trace(a):
    return sum(s for i, (j, s) in enumerate(zip(a.image, a.sign)) if i == j)


def matrix_is_zero(m):
    return all(x == 0 for row in m for x in row)


def vector_is_zero(v):
    return all(x == 0 for x in v)


def left_multiply_B1(k, B1=None):
    if B1 is None:
        B1 = actions.load_frozen_complex(7).B1
    B = np.asarray(B1, int); tdim = len(k); sdim = len(k[0]) if k else 0
    if B.shape[1] != tdim:
        raise ValueError('B1/coupling mismatch')
    return tuple(tuple(sum((Fraction(int(B[r,i])) * Fraction(k[i][j]) for i in range(tdim)), Fraction(0))
                       for j in range(sdim)) for r in range(B.shape[0]))


def apply_to_constant(k):
    if not k:
        return ()
    return tuple(sum((Fraction(x) for x in row), Fraction(0)) for row in k)


def _selector_module():
    path = REPO_ROOT / SELECTOR_REL
    raw = path.read_bytes(); sha = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    if sha != SELECTOR_BLOB:
        raise ValueError('v15.26 selector-rank baseline changed')
    name = '_v1528_selector_rank'; spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module


def _response_coordinate_recovery(c, basis):
    module = _selector_module(); R = module.response_operator(c); zero = np.zeros(c.B1.shape[0])
    sources = actions.augmentation_basis(len(c.vertices)).columns[:3]; err = 0.0
    for K in basis:
        Kf = np.array([[float(x) for x in row] for row in K])
        for q in sources:
            qf = np.array([float(x) for x in q]); z = Kf @ qf
            err = max(err, float(np.linalg.norm(c.B1 @ z)))
            target = R @ z; recovered = module.reconstruct(c.B1, zero, R, target)
            err = max(err, float(np.linalg.norm(recovered - z)))
    return err


def _restricted_trace(basis, action):
    total = Fraction(0)
    for j, col in enumerate(basis.columns):
        total += basis.coordinates(action.apply(col))[j]
    return total


def _q_baseline_from_complex(c, verify_response=False):
    group = actions.torus_automorphisms(c.L)
    source_actions = {g: actions.vertex_action(c, g) for g in group}
    target_actions = {g: actions.edge_action(c, g) for g in group}
    space = solver.solve_signed_ambient(
        source_actions, target_actions,
        (tuple([1] * len(c.vertices)),),
        tuple(tuple(int(x) for x in row) for row in c.B1.astype(int)))
    source_chars = {}; target_chars = {}
    for g in group:
        cv = _signed_trace(source_actions[g]); ce = _signed_trace(target_actions[g])
        source_chars[g] = cv - 1
        target_chars[g] = ce - (cv - 1)
    character_dimension = solver.hom_dimension_from_character_values(source_chars, target_chars)
    if character_dimension != space.dimension:
        raise ArithmeticError('orbit and character dimensions disagree')
    source_basis = actions.augmentation_basis(len(c.vertices))
    cycle_basis = actions.cycle_basis_exact(c.B1.astype(int))
    for idx in (0,1,7,48,49,100,211,391):
        g = group[idx]
        if _restricted_trace(source_basis, source_actions[g]) != source_chars[g]:
            raise ArithmeticError('source character spot check failed')
        if _restricted_trace(cycle_basis, target_actions[g]) != target_chars[g]:
            raise ArithmeticError('cycle character spot check failed')
    status = ('EQUIVARIANT_COUPLING_SPACE_ZERO' if space.dimension == 0 else
              'EQUIVARIANT_COUPLING_UNIQUE_UP_TO_SCALE' if space.dimension == 1 else
              'EQUIVARIANT_COUPLING_MULTI_DIMENSIONAL')
    recovery_error = _response_coordinate_recovery(c, space.basis) if verify_response else None
    return CandidateAudit(
        'source-quotient-q-control', 'BASELINE_CONTROL', 'ELIGIBLE_EXACT_COUPLING_AUDIT',
        status, space.dimension, space.dimension, character_dimension, space.basis,
        tuple(solver.projective_hash(k) for k in space.basis), None,
        {'orbit_count': space.orbit_count, 'constraint_rank': space.constraint_rank,
         'character_spotcheck_exact': True,
         'response_coordinate_recovery_error': recovery_error})


@lru_cache(None)
def q_baseline_audit():
    return _q_baseline_from_complex(actions.load_frozen_complex(7), verify_response=True)
