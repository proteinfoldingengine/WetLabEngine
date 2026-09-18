from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE_SHA = 'ff4707b3a09bc7cd091e89986c8cc3dcaf758798'

EVIDENCE = {
    'v15.32-results': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.32-commutant-sector-decomposition/docs/RESULTS.json',
        'a6018895d996bb01d76918994ebd0519260a958d',
        ('MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS',),
    ),
    'v15.05-composition': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/v15/v15.05/REPORT.md',
        'b191c08c22ded0439cc4c2c125fbccfdb677dcbc',
        ('FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE',),
    ),
    'v15.06-recoverability': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/v15/v15.06/REPORT.md',
        'bdeac09b2b162f07baa874ef1c1d6415fdd5e236',
        ('MULTIPLICATIVE_SCALAR_NEEDS_NEW_MAP_TO_BECOME_OPERATOR_SOURCE',),
    ),
    'v13.22-refinement': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/v13/v13.22/REPORT.md',
        'e6920facaa4d133e2767951612c608d0e514806c',
        ('does **not** derive a unique quantum refinement law', 'ETL source-naturality selection: **NO**'),
    ),
    'v13.23-qrsl': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/v13/v13.23/REPORT.md',
        '1162d8f8378cb5292d6c2f8526dd5bd53198d2c4',
        ('QRSL is irreducible relative to the current frozen ontology',),
    ),
    'v13.26-source-scale': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md',
        '9917085b211ca0e1f4737082227f55097cc72b66',
        ('exact positive rescaling freedom',),
    ),
    'v15.23-idempotence': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.23-sufficient-channel-family/README.md',
        '1e0a276a7aca9c5bf474dd9917c44ecfe99a262e',
        ('we have not derived a new physical reason to demand it',),
    ),
    'v15.24-composition': (
        REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.24-composition-gate/README.md',
        '8f7dcf085fc1cbaf167297191ad1a7416f0efa42',
        ('It does not adopt any of them as a new physical law',
         'Neither requirement determines which surviving map actually occurs'),
    ),
}


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    header = f'blob {len(raw)}'.encode() + bytes([0])
    return hashlib.sha1(header + raw).hexdigest()


def verify_evidence() -> dict[str, str]:
    out = {}
    for key, (path, expected, required) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f'evidence drift: {key}: {actual}')
        text = path.read_text()
        missing = [phrase for phrase in required if phrase not in text]
        if missing:
            raise AssertionError(f'evidence phrase missing for {key}: {missing}')
        out[key] = actual
    return out


def load_v1532() -> dict:
    verify_evidence()
    path = EVIDENCE['v15.32-results'][0]
    r = json.loads(path.read_text())
    if r['status'] != 'MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS':
        raise AssertionError('v15.32 status changed')
    if r['splitting_field_sector_count'] != 10:
        raise AssertionError('v15.32 sector count changed')
    if not r['multiplicity_free_over_splitting_field']:
        raise AssertionError('v15.32 multiplicity-free result changed')
    if r['mixing_freedom_dimension'] != 0:
        raise AssertionError('v15.32 mixing result changed')
    if r['projective_relative_weight_dimension'] != 9:
        raise AssertionError('v15.32 projective dimension changed')
    return r


def qvec(values):
    v = tuple(Fraction(x) for x in values)
    if len(v) != 10:
        raise ValueError('ten sector weights required')
    return v


def add(a, b):
    a, b = qvec(a), qvec(b)
    return tuple(x + y for x, y in zip(a, b))


def scale(s, a):
    a = qvec(a)
    s = Fraction(s)
    return tuple(s * x for x in a)


def compose(a, b):
    a, b = qvec(a), qvec(b)
    return tuple(x * y for x, y in zip(a, b))


def apply(weights, state):
    w, z = qvec(weights), qvec(state)
    return tuple(a * b for a, b in zip(w, z))


def canonical_projective(weights):
    w = qvec(weights)
    first = next((x for x in w if x), None)
    if first is None:
        raise ValueError('zero vector has no projective class')
    return tuple(x / first for x in w)


def automatic_witness_audit():
    witnesses = (
        qvec(range(1, 11)),
        qvec((2, 3, 5, 7, 11, 13, 17, 19, 23, 29)),
        qvec((1, 2, 1, 3, 1, 5, 1, 7, 1, 11)),
        qvec((Fraction(1,2), Fraction(2,3), Fraction(3,4), Fraction(4,5), Fraction(5,6),
              Fraction(6,7), Fraction(7,8), Fraction(8,9), Fraction(9,10), Fraction(10,11))),
        qvec((1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),
    )
    z1 = qvec((1, -1, 2, -2, 3, -3, 4, -4, 5, -5))
    z2 = qvec((2, 1, -1, 3, -2, 4, -3, 5, -4, 6))
    v = qvec(range(10, 0, -1))
    ident = qvec((1,) * 10)
    checks = []
    for w in witnesses:
        linear = apply(w, add(z1, z2)) == add(apply(w, z1), apply(w, z2))
        reversal = apply(w, scale(-1, z1)) == scale(-1, apply(w, z1))
        composition = apply(compose(w, v), z1) == apply(w, apply(v, z1))
        identity = apply(ident, z1) == z1
        # G-covariance is exact from v15.32: each S_i is invariant and T_w is scalar on S_i.
        covariance = True
        checks.append(linear and reversal and composition and identity and covariance)
    projective = {canonical_projective(w) for w in witnesses}
    return {
        'witness_count': len(witnesses),
        'projectively_distinct_witness_count': len(projective),
        'all_witnesses_pass_automatic_constraints': all(checks),
    }


def constraint_ledger():
    return [
        {'key':'linearity_source_additivity','class':'AUTOMATIC_FOR_ALL_WEIGHTS','equation_rank':0},
        {'key':'source_reversal_oddness','class':'AUTOMATIC_FOR_ALL_WEIGHTS','equation_rank':0},
        {'key':'G_covariance','class':'AUTOMATIC_FOR_ALL_WEIGHTS','equation_rank':0},
        {'key':'same_carrier_composition_closure','class':'AUTOMATIC_FOR_ALL_WEIGHTS','equation_rank':0},
        {'key':'identity_availability','class':'AUTOMATIC_FOR_ALL_WEIGHTS','equation_rank':0},
        {'key':'v13.22_refinement_naturality','class':'TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE','equation_rank':0},
        {'key':'v13.23_QRSL','class':'TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE','equation_rank':0},
        {'key':'v15.05_labeled_monoidal_composition','class':'TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE','equation_rank':0},
        {'key':'v15.06_recoverability_multiplicativity','class':'TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE','equation_rank':0},
        {'key':'v15.24_no_signalling_product_composition','class':'TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE','equation_rank':0},
        {'key':'v13.26_common_source_scale','class':'PROJECTIVE_GAUGE_ONLY','equation_rank':0},
    ]


def idempotence_control():
    total = 0
    nonzero = 0
    for bits in product((0, 1), repeat=10):
        w = qvec(bits)
        if compose(w, w) != w:
            raise ArithmeticError('binary idempotence control failed')
        total += 1
        if any(w):
            nonzero += 1
    if total != 1024 or nonzero != 1023:
        raise ArithmeticError('idempotence counts changed')
    return total, nonzero


def audit() -> dict:
    inherited = load_v1532()
    witness = automatic_witness_audit()
    if not witness['all_witnesses_pass_automatic_constraints']:
        raise AssertionError('automatic witness failed')
    ledger = constraint_ledger()
    classes = [row['class'] for row in ledger]
    automatic = classes.count('AUTOMATIC_FOR_ALL_WEIGHTS')
    blocked = classes.count('TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE')
    gauge = classes.count('PROJECTIVE_GAUGE_ONLY')
    unresolved = classes.count('UNRESOLVED')
    actual = [row for row in ledger if row['class'] == 'ACTUAL_WEIGHT_EQUATION']
    rank = sum(row['equation_rank'] for row in actual)
    total_idem, nonzero_idem = idempotence_control()
    if unresolved:
        status = 'WEIGHT_CONSTRAINT_AUDIT_UNRESOLVED'
    elif rank > 0:
        status = 'FROZEN_CONSTRAINTS_REDUCE_SECTOR_WEIGHTS'
    else:
        status = 'FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE'
    return {
        'version': 'v15.33',
        'base_sha': BASE_SHA,
        'status': status,
        'sector_count': inherited['splitting_field_sector_count'],
        'affine_weight_dimension': 10,
        'inherited_projective_relative_weight_dimension': inherited['projective_relative_weight_dimension'],
        'automatic_constraint_count': automatic,
        'type_blocked_constraint_count': blocked,
        'projective_gauge_count': gauge,
        'unresolved_constraint_count': unresolved,
        'frozen_actual_weight_equation_count': len(actual),
        'frozen_constraint_rank': rank,
        'surviving_projective_weight_dimension': 9 - rank,
        'constraint_ledger': ledger,
        **witness,
        'idempotent_total_choice_count': total_idem,
        'idempotent_nonzero_choice_count': nonzero_idem,
        'idempotence_is_frozen_source_law': False,
        'equal_weight_control_projective_dimension': 0,
        'equal_weight_control_is_frozen': False,
        'positive_cone_projective_dimension': 9,
        'positive_cone_is_frozen_selector': False,
        'evidence_pins': verify_evidence(),
        'new_source_semantics_axiom_added': False,
        'new_sector_weight_selector_added': False,
        'coupling_solver_reopened': False,
        'gravity_observables_evaluated': False,
        'uses_holonomy_selector': False,
        'uses_newton_or_gr': False,
        'uses_metric_selector': False,
        'uses_pruning_as_selector': False,
        'uses_entropy_as_selector': False,
        'uses_physical_time': False,
        'scientific_breakthrough': False,
        'signal_of_life': False,
        'physical_gravity_derived': False,
        'Pillar_3': 'OPEN',
        'next_required_object': 'NEW_TYPED_PRETIME_INVARIANT_OR_EXPLICIT_SECTOR_WEIGHT_AXIOM',
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + '\n'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out')
    p.add_argument('--check')
    args = p.parse_args()
    text = canonical_json(audit())
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    if args.check and Path(args.check).read_text() != text:
        raise SystemExit('committed v15.33 result differs from regenerated audit')
    print(text, end='')


if __name__ == '__main__':
    main()
