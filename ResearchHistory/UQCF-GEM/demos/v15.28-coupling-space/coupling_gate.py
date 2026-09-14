from __future__ import annotations
from dataclasses import dataclass, field, asdict
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import numpy as np
import representation_actions as actions
import coupling_solver as solver

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE_SHA = '700a4639010100a12b73882d530ac2c2bbf1f71e'
SELECTOR_BLOB = '623defd0d8284e5d9cba6d8f8679de698e5202bc'
SELECTOR_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/selector_rank.py')
INVENTORY_REL = Path('ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/REPRESENTATION_INVENTORY.json')

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

@dataclass(frozen=True)
class FrozenCouplingForm:
    candidate_key: str
    projective_basis_hash: str
    ambient_shape: tuple[int, int]
    exact_nonzero_entries: tuple[tuple[int, int, int, int], ...]
    scale_status: str = 'UNRESOLVED_NONPHYSICAL_IN_V15_28'


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


def _verify_v1404_ambiguity(record, repo_root=None):
    root = REPO_ROOT if repo_root is None else Path(repo_root)
    path = root / record.artifact_path
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text()
    required = (
        '14041', '14042', '14043',
        'Minimum pairwise support-source projective residual',
        'Maximum hidden-direction separation',
    )
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError('v14.04 ambiguity evidence missing: ' + ','.join(missing))
    return {'supplied_link_count': 3, 'inequivalent_supplied_links': True}


def audit_candidate(record):
    if record.key == 'source-quotient-q-control':
        return q_baseline_audit()
    if record.eligibility == 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK':
        return CandidateAudit(record.key, record.role, record.eligibility,
                              record.eligibility, None,
                              stop_reason=record.label_link_status)
    if record.eligibility == 'CONDITIONAL_ON_SUPPLIED_INTERTWINER':
        meta = _verify_v1404_ambiguity(record)
        return CandidateAudit(record.key, record.role, record.eligibility,
                              record.eligibility, None,
                              stop_reason=record.label_link_status,
                              metadata=meta)
    if record.eligibility == 'ARCHIVE_EVIDENCE_ONLY':
        return CandidateAudit(record.key, record.role, record.eligibility,
                              'ARCHIVE_EVIDENCE_ONLY', None,
                              stop_reason='NOT_A_COUPLING_CANDIDATE')
    if not record.action_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified action')
    if not record.label_link_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified target link')
    raise NotImplementedError(
        'new eligible physical carrier requires an approved representation-specific solver')


def audit_all_candidates(records=None):
    import representation_inventory as inv
    rows = inv.frozen_inventory(inv.REPO_ROOT) if records is None else records
    roles = {'PROVENANCE_CANDIDATE', 'NEGATIVE_CONTROL', 'PHYSICAL_CANDIDATE'}
    return tuple(audit_candidate(row) for row in rows if row.role in roles)


def adjudicate(candidates):
    eligible = [c for c in candidates if c.eligible_physical_candidate]
    ones = [c for c in eligible if c.dimension == 1]
    if not eligible:
        return 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK'
    if not ones and all(c.dimension == 0 for c in eligible):
        return 'PRETIME_COUPLING_SPACE_ZERO'
    if len(ones) == 1 and len(eligible) == 1:
        return 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE'
    return 'PRETIME_COUPLING_REMAINS_UNDERDETERMINED'


def freeze_unique_form(candidate: CandidateAudit) -> FrozenCouplingForm:
    if not candidate.eligible_physical_candidate or candidate.dimension != 1 or len(candidate.ambient_basis) != 1:
        raise ValueError('unique form requires one-dimensional eligible physical candidate')
    canon = solver.canonical_projective_matrix(candidate.ambient_basis[0])
    entries = tuple((i, j, int(x), 1)
                    for i, row in enumerate(canon) for j, x in enumerate(row) if x)
    return FrozenCouplingForm(candidate.key, solver.projective_hash(candidate.ambient_basis[0]),
                              (len(canon), len(canon[0]) if canon else 0), entries)


def _inventory_hash():
    import representation_inventory as inv
    path = REPO_ROOT / INVENTORY_REL
    actual = inv.git_blob_hash(path)
    expected = '28dd212b422a4f41d835ccbec79a35116e268ba1'
    if actual != expected:
        raise ValueError(f'committed representation inventory drift: {actual}')
    return actual


def _verify_result(r):
    required = {
        'version','status','base_sha','inventory_hash','q_control','candidates',
        'eligible_candidate_count','one_dimensional_candidate_count',
        'multi_dimensional_candidate_count','zero_dimensional_candidate_count',
        'blocked_candidate_count','unique_form_frozen','frozen_form','scale_resolved',
        'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
        'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
        'scientific_breakthrough','signal_of_life','gravity_canary_certified',
        'Pillar_3','next_required_object'
    }
    if set(r) != required:
        raise AssertionError('ledger schema mismatch')
    if r['q_control']['dimension'] != 3:
        raise AssertionError('q control dimension changed')
    if r['eligible_candidate_count'] == 0 and r['status'] != 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK':
        raise AssertionError('blocked verdict mismatch')
    for key in ('gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
                'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
                'signal_of_life','gravity_canary_certified'):
        if r[key]:
            raise AssertionError(f'forbidden claim/selector: {key}')
    if r['status'] != 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE' and r['scientific_breakthrough']:
        raise AssertionError('breakthrough without unique coupling form')


@lru_cache(None)
def audit():
    q_control = q_baseline_audit()
    candidates = audit_all_candidates()
    status = adjudicate(candidates)
    eligible = [c for c in candidates if c.eligible_physical_candidate]
    ones = [c for c in eligible if c.dimension == 1]
    multis = [c for c in eligible if c.dimension is not None and c.dimension > 1]
    zeros = [c for c in eligible if c.dimension == 0]
    blocked = [c for c in candidates if c.dimension is None]
    frozen = freeze_unique_form(ones[0]) if status == 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE' else None
    gravity_observables_evaluated = False
    scientific_breakthrough = bool(status == 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE' and frozen is not None and not gravity_observables_evaluated)
    result = {
        'version': 'v15.28',
        'status': status,
        'base_sha': BASE_SHA,
        'inventory_hash': _inventory_hash(),
        'q_control': q_control.as_dict(),
        'candidates': [c.as_dict() for c in candidates],
        'eligible_candidate_count': len(eligible),
        'one_dimensional_candidate_count': len(ones),
        'multi_dimensional_candidate_count': len(multis),
        'zero_dimensional_candidate_count': len(zeros),
        'blocked_candidate_count': len(blocked),
        'unique_form_frozen': frozen is not None,
        'frozen_form': asdict(frozen) if frozen is not None else None,
        'scale_resolved': False,
        'gravity_observables_evaluated': gravity_observables_evaluated,
        'uses_holonomy_selector': False,
        'uses_newton_or_gr': False,
        'uses_metric_selector': False,
        'uses_pruning': False,
        'uses_entropy': False,
        'uses_physical_time': False,
        'scientific_breakthrough': scientific_breakthrough,
        'signal_of_life': False,
        'gravity_canary_certified': False,
        'Pillar_3': 'OPEN',
        'next_required_object': 'CERTIFIED_PRETIME_PROVENANCE_TO_CYCLE_REPRESENTATION_LINK_OR_NEW_DERIVED_STRUCTURE',
    }
    _verify_result(result)
    return result


def write_results(path: Path, result=None):
    result = audit() if result is None else result
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n')


def main():
    parser = argparse.ArgumentParser(description='v15.28 gravity-blind coupling-space gate')
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent / 'outputs')
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    result = audit(); write_results(args.out / 'verification.json', result)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))

if __name__ == '__main__':
    main()
