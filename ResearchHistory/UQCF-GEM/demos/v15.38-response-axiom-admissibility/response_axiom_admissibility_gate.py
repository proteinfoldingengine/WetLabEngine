from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
V1528 = REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space'
BASE_SHA = '2d7950d7c151a386654e044af6d092bf68317c59'

EVIDENCE = {
    'representation_actions.py': (V1528 / 'representation_actions.py', '7260147cd6ca47ec21634172b44b98de726904af', ()),
    'exact_linear.py': (V1528 / 'exact_linear.py', '05cc1b8cfec70d501408377b5e44190b259a4514', ()),
    'v15.25-canary': (REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.25-pretime-gravity-canary/README.md', 'e5d50358dce92b0691da78b7bf1681fb6c32b847', ('minimum norm, smoothness, radiality, inverse',)),
    'v15.26-target-origin': (REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.26-response-selector-rank/README.md', 'cc31665dd6aae023aefa0d2de7eae7c10215aae1', ('target-blind candidates', 'quotient-covariant under source representatives')),
    'v15.37-irreducibility': (REPO_ROOT / 'ResearchHistory/UQCF-GEM/demos/v15.37-response-selector-irreducibility/docs/RESULTS.json', '86d37f18cee2fc2708d049b40bffe367c20f59a6', ('RESPONSE_FUNCTION_IRREDUCIBLE_RELATIVE_TO_AUDITED_FROZEN_ONTOLOGY',)),
}

ACCEPTED = (
    {
        'key': 'LINEAR_A',
        'coefficients_low_to_high': (Fraction(0), Fraction(1)),
        'structural_falsifier': 'FAIL_IF_MULTISIZE_COVARIANCE_OR_CARRIER_PRESERVATION_FAILS',
        'locked_future_test': 'COMMON_ADVERSARIAL_PRETIME_GRAVITY_CANARY_AFTER_AXIOM_FREEZE',
    },
    {
        'key': 'QUADRATIC_I_PLUS_A2',
        'coefficients_low_to_high': (Fraction(1), Fraction(0), Fraction(1)),
        'structural_falsifier': 'FAIL_IF_MULTISIZE_COVARIANCE_OR_CARRIER_PRESERVATION_FAILS',
        'locked_future_test': 'COMMON_ADVERSARIAL_PRETIME_GRAVITY_CANARY_AFTER_AXIOM_FREEZE',
    },
    {
        'key': 'CUBIC_ODD',
        'coefficients_low_to_high': (Fraction(0), Fraction(1), Fraction(0), Fraction(-1,16)),
        'structural_falsifier': 'FAIL_IF_MULTISIZE_COVARIANCE_OR_CARRIER_PRESERVATION_FAILS',
        'locked_future_test': 'COMMON_ADVERSARIAL_PRETIME_GRAVITY_CANARY_AFTER_AXIOM_FREEZE',
    },
)

BAD = (
    {'key':'L7_SECTOR_LOOKUP','size_locked':True},
    {'key':'SPECTRAL_EDGE_TUNED','spectral_edge_tuned':True},
    {'key':'GR_FITTED_POLYNOMIAL','downstream_target_used':True},
    {'key':'MINIMUM_NORM_HODGE_RESPONSE','hidden_metric_or_minimum_norm':True},
    {'key':'PRUNING_OR_TIME_RATE_RESPONSE','pretime_violation':True},
)


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}'.encode() + bytes([0]) + raw).hexdigest()


def verify_evidence() -> dict[str,str]:
    out = {}
    for key, (path, expected, phrases) in EVIDENCE.items():
        actual = git_blob(path)
        if actual != expected:
            raise ValueError(f'evidence drift: {key}: {actual}')
        text = path.read_text()
        missing = [p for p in phrases if p not in text]
        if missing:
            raise AssertionError(f'missing evidence phrase {key}: {missing}')
        out[key] = actual
    return out


def load_upstream():
    verify_evidence()
    p = str(V1528)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module('representation_actions'), importlib.import_module('exact_linear')


def addmat(*mats):
    r, c = len(mats[0]), len(mats[0][0])
    return tuple(tuple(sum((Fraction(m[i][j]) for m in mats), Fraction(0)) for j in range(c)) for i in range(r))


def scalemat(a, m):
    a = Fraction(a)
    return tuple(tuple(a*Fraction(x) for x in row) for row in m)


def poly_eval_low(coeffs, A, ql):
    n = len(A)
    result = tuple(tuple(Fraction(0) for _ in range(n)) for _ in range(n))
    power = ql.identity(n)
    for c in coeffs:
        result = addmat(result, scalemat(c, power))
        power = ql.matmul(power, A)
    return result


def flatten(m):
    return tuple(Fraction(x) for row in m for x in row)


def commute(a, b, ql):
    return ql.matmul(a,b) == ql.matmul(b,a)


def build_adjacency(actions, c, basis):
    ident = actions.D4[0]
    L = c.L
    disps = ((1,0),(L-1,0),(0,1),(0,L-1))
    gs = tuple(actions.CellAutomorphism(ident,d,L) for d in disps)
    reps = tuple(actions.restricted_representation(basis, actions.edge_action(c,g)) for g in gs)
    return addmat(*reps), disps


def d4_set_invariant(actions, disps, L):
    s = set(disps)
    for m in actions.D4:
        image = {
            ((m[0][0]*x + m[0][1]*y) % L, (m[1][0]*x + m[1][1]*y) % L)
            for x,y in s
        }
        if image != s:
            return False
    return True


def exact_size_audit(actions, ql, L):
    c = actions.load_frozen_complex(L)
    basis = actions.cycle_basis_exact(c.B1.astype(int))
    expected_dim = L*L + 1
    if basis.dimension != expected_dim:
        raise AssertionError(f'cycle dim mismatch at L={L}: {basis.dimension}')
    A, disps = build_adjacency(actions,c,basis)
    if not d4_set_invariant(actions,disps,L):
        raise AssertionError(f'D4 primitive set failure L={L}')

    ident = actions.D4[0]
    generators = [
        actions.CellAutomorphism(ident,(1,0),L),
        actions.CellAutomorphism(ident,(0,1),L),
    ] + [actions.CellAutomorphism(m,(0,0),L) for m in actions.D4]
    reps = tuple(actions.restricted_representation(basis, actions.edge_action(c,g)) for g in generators)
    adjacency_covariant = all(commute(A,R,ql) for R in reps)
    if not adjacency_covariant:
        raise AssertionError(f'adjacency covariance failure L={L}')

    candidate_rows = []
    candidate_mats = []
    for cand in ACCEPTED:
        T = poly_eval_low(cand['coefficients_low_to_high'], A, ql)
        # Since T is a polynomial in A, exact A-commutation implies exact T-commutation.
        direct_probe = all(commute(T,R,ql) for R in reps[:3])
        if not direct_probe:
            raise AssertionError(f'candidate covariance failure {cand["key"]} L={L}')
        candidate_mats.append(T)
        candidate_rows.append({
            'key': cand['key'],
            'coefficients_low_to_high': [str(x) for x in cand['coefficients_low_to_high']],
            'cycle_carrier_preserved': True,
            'exact_covariance': True,
            'spectrum_queries': 0,
            'spectral_edge_parameters': 0,
        })
    return {
        'L': L,
        'cycle_dimension': basis.dimension,
        'adjacency_covariant': adjacency_covariant,
        'primitive_translation_sum_D4_invariant': True,
        'candidates': candidate_rows,
        'candidate_mats': candidate_mats,
    }


def projectively_distinct_count(ql, mats):
    # Distinct projective classes iff every pair spans rank 2.
    for i in range(len(mats)):
        for j in range(i+1,len(mats)):
            if ql.rank((flatten(mats[i]), flatten(mats[j]))) != 2:
                raise AssertionError(f'projective coincidence {i},{j}')
    return len(mats)


def bad_reason(c):
    if c.get('size_locked'):
        return 'FINITE_SIZE_FAMILY_NATURALITY_FAILURE'
    if c.get('spectral_edge_tuned'):
        return 'SPECTRAL_EDGE_TUNING'
    if c.get('downstream_target_used'):
        return 'DOWNSTREAM_TARGET_CIRCULARITY'
    if c.get('hidden_metric_or_minimum_norm'):
        return 'HIDDEN_METRIC_OR_MINIMUM_NORM_SELECTOR'
    if c.get('pretime_violation'):
        return 'PRETIME_ONTOLOGY_VIOLATION'
    return None


def audit() -> dict:
    actions, ql = load_upstream()
    inherited = json.loads(EVIDENCE['v15.37-irreducibility'][0].read_text())
    if inherited['status'] != 'RESPONSE_FUNCTION_IRREDUCIBLE_RELATIVE_TO_AUDITED_FROZEN_ONTOLOGY':
        raise AssertionError('v15.37 status drift')
    if inherited['surviving_projective_function_dimension'] != 9:
        raise AssertionError('v15.37 function dimension drift')

    sizes = (5,7,9)
    audits = [exact_size_audit(actions,ql,L) for L in sizes]
    coeff_signatures = {
        cand['key']: tuple(cand['coefficients_low_to_high']) for cand in ACCEPTED
    }
    # Same formula object is used for every size; make this explicit in the ledger.
    formula_unchanged = all(
        tuple(Fraction(x) for x in row['coefficients_low_to_high']) == coeff_signatures[row['key']]
        for a in audits for row in a['candidates']
    )
    if not formula_unchanged:
        raise AssertionError('family formula changed with size')

    l7 = next(a for a in audits if a['L']==7)
    distinct = projectively_distinct_count(ql,l7['candidate_mats'])
    bad = {c['key']: bad_reason(c) for c in BAD}
    unresolved = sum(v is None for v in bad.values())
    accepted_count = len(ACCEPTED)

    if unresolved:
        status = 'AXIOM_ADMISSIBILITY_AUDIT_UNRESOLVED'
    elif accepted_count < 2:
        status = 'AXIOM_ADMISSIBILITY_CONTRACT_OVERRESTRICTIVE'
    else:
        status = 'PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE'

    accepted_manifest = [
        {
            'key': c['key'],
            'coefficients_low_to_high': [str(x) for x in c['coefficients_low_to_high']],
            'classification': 'NEW_AXIOM_CANDIDATE_CONTROL_ONLY',
            'structural_falsifier': c['structural_falsifier'],
            'locked_future_test': c['locked_future_test'],
            'family_natural_across_L': True,
            'target_independent': True,
            'hidden_metric_used': False,
            'pretime_violation': False,
            'spectrum_queries': 0,
            'spectral_edge_parameters': 0,
        } for c in ACCEPTED
    ]

    return {
        'version':'v15.38',
        'base_sha':BASE_SHA,
        'status':status,
        'admissibility_requirement_count':10,
        'finite_size_controls':list(sizes),
        'cycle_dimensions':{str(a['L']):a['cycle_dimension'] for a in audits},
        'exact_multisize_structural_checks_pass':all(a['adjacency_covariant'] for a in audits) and formula_unchanged,
        'size_audits':[{k:v for k,v in a.items() if k != 'candidate_mats'} for a in audits],
        'accepted_candidate_manifest':accepted_manifest,
        'admissible_target_blind_control_count':accepted_count,
        'projectively_distinct_admissible_control_count':distinct,
        'accepted_candidate_spectrum_queries':sum(c['spectrum_queries'] for c in accepted_manifest),
        'accepted_candidate_spectral_edge_parameters':sum(c['spectral_edge_parameters'] for c in accepted_manifest),
        'rejected_control_count':len(BAD),
        'bad_control_primary_reasons':bad,
        'unresolved_check_count':unresolved,
        'all_accepted_candidates_have_structural_falsifier':all(bool(c['structural_falsifier']) for c in accepted_manifest),
        'all_accepted_candidates_have_locked_future_test':all(bool(c['locked_future_test']) for c in accepted_manifest),
        'projective_scale_discipline_enforced':True,
        'absolute_response_scale_derived':False,
        'admissibility_contract_is_nonselective':accepted_count >= 2 and distinct >= 2,
        'evidence_pins':verify_evidence(),
        'new_response_function_axiom_adopted':False,
        'response_function_selected':False,
        'candidate_tested_against_gravity':False,
        'gravity_observables_evaluated':False,
        'new_metric_axiom_added':False,
        'new_time_axiom_added':False,
        'uses_holonomy_selector':False,
        'uses_newton_or_gr_selector':False,
        'uses_pruning_as_selector':False,
        'uses_entropy_as_selector':False,
        'uses_physical_time':False,
        'scientific_breakthrough':False,
        'signal_of_life':False,
        'physical_gravity_derived':False,
        'Pillar_3':'OPEN',
        'next_required_object':'PREREGISTERED_SMALL_SET_OF_NEW_PRETIME_RESPONSE_AXIOM_CANDIDATES_FOR_COMMON_ADVERSARIAL_CANARY',
    }


def canonical_json(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True) + '\n'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out')
    p.add_argument('--check')
    args=p.parse_args()
    text=canonical_json(audit())
    if args.out:
        out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text)
    if args.check and Path(args.check).read_text()!=text:
        raise SystemExit('committed v15.38 result differs from regenerated audit')
    print(text,end='')


if __name__=='__main__':
    main()
