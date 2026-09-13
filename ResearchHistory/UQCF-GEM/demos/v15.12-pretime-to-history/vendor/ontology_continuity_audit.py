#!/usr/bin/env python3
"""v15.11: bounded continuity repair; no physical selector or clock is implemented.

Controls independently reconstruct finite examples. They are regression evidence,
not a proof of the physical interpretation of RAS, RCR, entropy, or time.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Callable, Sequence

import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1., -1.]).astype(complex)
PZ = [np.diag([1., 0.]), np.diag([0., 1.])]
TOL = 1e-12


def norm(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    h = np.asarray(a) - np.asarray(b)
    return float(np.sum(np.abs(np.linalg.eigvalsh((h+h.conj().T)/2)))/2)


def rotation(pauli: np.ndarray, extent: float) -> np.ndarray:
    """A finite group coordinate; extent has no elapsed-time interpretation."""
    return math.cos(extent/2)*I2 - 1j*math.sin(extent/2)*pauli


def pinch(a: np.ndarray, projectors: Sequence[np.ndarray]) -> np.ndarray:
    """Conditional expectation for a SUPPLIED orthogonal block decomposition."""
    a = np.asarray(a, dtype=complex)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.all(np.isfinite(a)):
        raise ValueError('finite square matrix required')
    ps = [np.asarray(p, dtype=complex) for p in projectors]
    if not ps or any(p.shape != a.shape or not np.all(np.isfinite(p)) for p in ps):
        raise ValueError('complete projectors with matching dimensions required')
    for p in ps:
        if norm(p-p.conj().T) > TOL or norm(p@p-p) > TOL:
            raise ValueError('Hermitian idempotent projectors required')
    if norm(sum(ps)-np.eye(a.shape[0])) > TOL:
        raise ValueError('projectors must resolve the identity')
    if any(norm(p@q)>TOL for i,p in enumerate(ps) for q in ps[i+1:]):
        raise ValueError('projectors must be mutually orthogonal')
    return sum((p@a@p for p in ps), np.zeros_like(a))


def select_record(rho: np.ndarray, projectors: Sequence[np.ndarray], record: int | None = None) -> np.ndarray:
    """RCR is supplied explicitly. No sampling, argmax, or preferred record."""
    if record is None or isinstance(record, bool) or not isinstance(record, int):
        raise ValueError('one record must be supplied explicitly; actuality is not derived')
    if not 0 <= record < len(projectors):
        raise ValueError('record out of range')
    rho = np.asarray(rho, dtype=complex)
    coarse = pinch(rho, projectors)
    if norm(rho-rho.conj().T)>TOL or abs(np.trace(rho)-1)>TOL or np.linalg.eigvalsh(rho).min() < -TOL:
        raise ValueError('normalized positive density matrix required')
    p = np.asarray(projectors[record], dtype=complex)
    selected = p@coarse@p
    weight = float(np.trace(selected).real)
    if weight <= 0:
        raise ValueError('a positive-weight record is required')
    return selected/weight


def entropy_diagnostic(rho: np.ndarray) -> float:
    """Ordinary von Neumann entropy, never a selector or physical-time definition."""
    vals = np.linalg.eigvalsh((rho+rho.conj().T)/2)
    if vals.min() < -TOL:
        raise ValueError('positive state required')
    vals = vals[vals > 0]
    return float(-np.sum(vals*np.log(vals)))


def motion_control() -> dict:
    rho = np.diag([.8, .2]).astype(complex)
    u, v = rotation(X, .7), rotation(Y, .43)
    moved = u@rho@u.conj().T
    return {
        'state_change': trace_distance(rho, moved),
        'inverse_error': norm(u.conj().T@moved@u-rho),
        'composition_error': norm(v@moved@v.conj().T-(v@u)@rho@(v@u).conj().T),
        'parameter_semantics': 'FINITE_TRANSFORMATION_EXTENT_NOT_TIME',
    }


def pruning_control() -> dict:
    plus, minus = (I2+X)/2, (I2-X)/2
    ep, em = pinch(plus,PZ), pinch(minus,PZ)
    rho = np.array([[.6,.17+.09j],[.17-.09j,.4]])
    out = pinch(rho,PZ)
    u = rotation(Y,.73)
    rotated_ps = [u@p@u.conj().T for p in PZ]
    units = [np.eye(4)[:,k].reshape(2,2) for k in range(4)]
    superop = np.column_stack([pinch(e,PZ).reshape(-1) for e in units])
    choi = sum((np.kron(e,pinch(e,PZ)) for e in units),np.zeros((4,4),complex))
    return {
        'input_trace_distance': trace_distance(plus,minus),
        'output_trace_distance': trace_distance(ep,em),
        'input_ranks': [int(np.linalg.matrix_rank(r)) for r in (plus,minus)],
        'output_ranks': [int(np.linalg.matrix_rank(r)) for r in (ep,em)],
        'channel_kernel_dimension': 4-int(np.linalg.matrix_rank(superop)),
        'idempotence_error': norm(pinch(out,PZ)-out),
        'trace_error': float(abs(np.trace(out)-np.trace(rho))),
        'minimum_choi_eigenvalue': float(np.linalg.eigvalsh(choi).min()),
        'covariance_error': norm(pinch(u@rho@u.conj().T,rotated_ps)-u@out@u.conj().T),
        'fixed_point_change': norm(pinch(np.diag([.6,.4]),PZ)-np.diag([.6,.4])),
        'repeat_change': norm(pinch(ep,PZ)-ep),
        'loss_scope': 'DISTINGUISHABILITY_ON_SUPPLIED_RETAINED_ALGEBRA',
    }


def record_control() -> dict:
    rho = np.array([[.6,.2],[.2,.4]],dtype=complex)
    return {
        'instrument_channel_error': norm(pinch(rho,PZ)-(rho+Z@rho@Z)/2),
        'projective_weights': [float(np.trace(p@rho).real) for p in PZ],
        'random_unitary_weights': [.5,.5],
        'actuality_selector': 'NONE__RECORD_MUST_BE_SUPPLIED',
    }


def refines(child: np.ndarray, parent: np.ndarray) -> bool:
    return norm(parent@child-child)<TOL and norm(child@parent-child)<TOL


def history_control() -> dict:
    fine = [np.diag(np.eye(4)[k]) for k in range(4)]
    coarse = [fine[0]+fine[1],fine[2]+fine[3]]
    records = [np.eye(4),*coarse,*fine]
    relation = {(i,j) for i,p in enumerate(records) for j,q in enumerate(records) if refines(q,p)}
    antisymmetric = all(i==j or (j,i) not in relation for i,j in relation)
    transitive = all((i,k) in relation for i,j in relation for jj,k in relation if jj==j)
    root_coarse_leaf = [(0,j,k) for j in (1,2) for k in range(3,7) if (0,j) in relation and (j,k) in relation]
    vec = np.array([1,2,3,4.],dtype=complex)
    rho = .8*np.outer(vec,vec.conj())/np.vdot(vec,vec).real+.2*np.eye(4)/4
    first = select_record(rho,coarse,0)
    sequential = select_record(first,fine,0)
    direct = select_record(rho,fine,0)
    ea = lambda a: pinch(a,[np.kron(p,I2) for p in PZ])
    eb = lambda a: pinch(a,[np.kron(I2,p) for p in PZ])
    orders = [p for p in itertools.permutations('abcd') if p.index('a')<p.index('b') and p.index('c')<p.index('d')]
    return {
        'antisymmetric': antisymmetric, 'transitive': transitive,
        'maximal_record_chains': len(root_coarse_leaf),
        'strict_record_rank_chain': [4,2,1],
        'incomparable_coarse_pair': ['A','B'] if (1,2) not in relation and (2,1) not in relation else [],
        'selective_composition_error': norm(sequential-direct),
        'independent_two_chain_linear_extensions': len(orders),
        'commuting_pruning_error': norm(ea(eb(rho))-eb(ea(rho))),
        'strict_order_derived_from': 'PROPER_PROJECTOR_INCLUSION__NOT_LOOP_COUNTER',
    }


def center_persistence_control() -> dict:
    """B={diag(T,T)} subset A=M2 direct-sum M2, yet Z(A) is not retained."""
    qa = np.diag([1.,1.,0.,0.]); qb = np.eye(4)-qa
    ea = lambda a: pinch(a,[qa,qb])
    def eb(a):
        avg = (a[:2,:2]+a[2:,2:])/2
        return np.kron(I2,avg)
    a = np.arange(16,dtype=float).reshape(4,4)
    return {
        'nested_expectation_error': norm(eb(ea(a))-eb(a)),
        'old_record_erasure_norm': norm(eb(qa)-qa),
        'old_center_dimension': 2, 'new_center_dimension': 1,
        'record_compatibility_condition': 'Z(A) subset B implies Z(A) subset Z(B); algebra inclusion alone is insufficient',
    }


def scope_control() -> dict:
    """Compare retained, classical-record, and full coherent-output descriptions."""
    plus,minus = (I2+X)/2,(I2-X)/2
    ancilla = np.diag([1.,0.])
    cnot = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)
    inputs = [np.kron(r,ancilla) for r in (plus,minus)]
    joint = [cnot@r@cnot.conj().T for r in inputs]
    def marginal(a):
        return np.trace(a.reshape(2,2,2,2),axis1=1,axis2=3)
    classical = [sum((np.kron(p@r@p,np.diag(np.eye(2)[k])) for k,p in enumerate(PZ)),np.zeros((4,4),complex)) for r in (plus,minus)]
    return {
        'retained_output_distance': trace_distance(marginal(joint[0]),marginal(joint[1])),
        'joint_output_distance': trace_distance(*joint),
        'joint_inverse_error': max(norm(cnot.conj().T@a@cnot-b) for a,b in zip(joint,inputs)),
        'classical_record_output_distance': trace_distance(*classical),
        'nonselective_entropy': entropy_diagnostic(pinch(plus,PZ)),
        'selected_entropy': entropy_diagnostic(select_record(plus,PZ,0)),
        'neutral_state_entropy': entropy_diagnostic(I2/2),
        'interpretation': 'A dilation is a mathematical control, not an added physical environment or a collapse law',
    }


def duration_control() -> dict:
    chain = [[4],[2,2],[2,1,1],[1,1,1,1]]
    def intervals(p):
        vals = np.array([sum(n**p for n in blocks) for blocks in chain],dtype=float)
        raw = np.log(vals[:-1]/vals[1:])
        return raw/raw[0]
    d2,d3 = intervals(2),intervals(3)
    return {'algebra_block_sizes': chain,'D2_normalized':d2.tolist(),'D3_normalized':d3.tolist(),
            'normalized_interval_separation':norm(d2-d3),'clock_selected':False}


def noninjective_cycle_control() -> dict:
    f = [1,0,0]
    return {'map':f,'injective':len(set(f))==len(f),'two_cycle_exists':f[0]==1 and f[1]==0,
            'scope':'Noninjectivity of a map on a nominal domain alone does not imply acyclic state succession'}


def verify_sources(manifest_path: Path, source_dir: Path | None = None) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for row in manifest['sources']:
        excerpt = row['excerpt']
        if hashlib.sha256(excerpt.encode()).hexdigest() != row['excerpt_sha256']:
            raise ValueError(f"excerpt digest mismatch: {row['name']}")
        if source_dir is not None:
            data = (source_dir/row['name']).read_bytes()
            if hashlib.sha256(data).hexdigest() != row['original_sha256']:
                raise ValueError(f"original digest mismatch: {row['name']}")
            lines = data.decode('utf-8').splitlines(keepends=True)
            a,b = row['original_lines_inclusive']
            if ''.join(lines[a-1:b]) != excerpt:
                raise ValueError(f"excerpt is not the declared original range: {row['name']}")
    return {'source_count':len(manifest['sources']), 'excerpt_hashes_valid':True,
            'original_bytes_checked':source_dir is not None,
            'verification_scope':'FULL_ORIGINALS_AND_EXCERPTS' if source_dir is not None else 'EXCERPTS_ONLY__FULL_ORIGINAL_DIGESTS_RECORDED'}


def adjudicate(checks_passed: bool) -> str:
    return 'CONTINUITY_RESTORED_CONDITIONAL_ORDINAL_ORDER_PRESERVED' if checks_passed else 'VERIFICATION_FAILED_NO_SCIENTIFIC_ADJUDICATION'


def run_audit() -> dict:
    m,p,r,h,c,s,d,n = (fn() for fn in (motion_control,pruning_control,record_control,history_control,center_persistence_control,scope_control,duration_control,noninjective_cycle_control))
    passed = (m['inverse_error']<TOL and m['composition_error']<TOL and m['state_change']>.1
              and abs(p['input_trace_distance']-1)<TOL and p['output_trace_distance']<TOL
              and p['channel_kernel_dimension']==2 and p['idempotence_error']<TOL
              and p['trace_error']<TOL and p['minimum_choi_eigenvalue']>=-TOL
              and p['covariance_error']<TOL and r['instrument_channel_error']<TOL
              and h['antisymmetric'] and h['transitive'] and h['maximal_record_chains']==4
              and h['selective_composition_error']<TOL and h['independent_two_chain_linear_extensions']==6
              and h['commuting_pruning_error']<TOL and c['nested_expectation_error']<TOL
              and c['old_record_erasure_norm']>.5 and s['retained_output_distance']<TOL
              and abs(s['joint_output_distance']-1)<TOL and s['joint_inverse_error']<TOL
              and d['normalized_interval_separation']>.05 and n['two_cycle_exists'])
    return {
        'version':'v15.11', 'title':'Ontology Continuity / Retained-Algebra and Actual-Record Reconciliation',
        'outcome':adjudicate(bool(passed)), 'numerical_controls_passed':bool(passed),
        'motion':m,'pruning':p,'records':r,'history':h,'record_persistence':c,
        'information_scope':s,'duration':d,'noninjectivity_boundary':n,
        'RAS':'EXISTING_EXPLICIT_PRIMITIVE_NOT_DERIVED',
        'RCR':'EXISTING_EXPLICIT_PRIMITIVE_NOT_DERIVED',
        'ordinal_time':'PRESERVED_CONDITIONAL_ON_RAS_RCR_AND_COMPATIBLE_STRICT_RECORD_REFINEMENT',
        'MCCC':'EARLIER_CONDITIONAL_CLOCK_BRIDGE_NOT_ADOPTED_OR_REDERIVED_HERE',
        'new_physical_axioms_adopted':[], 'physical_entropy_law_derived':False,
        'unconditional_metric_time_derived':False,'Pillar_3':'OPEN','scientific_breakthrough':False,
        'v15_10_correction':'FIXED_KNOWN_POTENTIAL_WEIGHT_MAP_RESULT_RETAINED__ARCHIVE_WIDE_ABSENCE_CLAIM_WITHDRAWN',
        'source_semantics_and_carrier_obstructions':'UNCHANGED_WITHIN_THEIR_AUDITED_PREMISES',
    }


def compare(actual, expected, path='root') -> None:
    if isinstance(expected,dict):
        if not isinstance(actual,dict) or set(actual)!=set(expected): raise AssertionError(path)
        for k in expected: compare(actual[k],expected[k],f'{path}.{k}')
    elif isinstance(expected,list):
        if not isinstance(actual,list) or len(actual)!=len(expected): raise AssertionError(path)
        for i,(a,b) in enumerate(zip(actual,expected)): compare(a,b,f'{path}[{i}]')
    elif type(expected) is float:
        if type(actual) not in (int,float) or not math.isfinite(actual) or not math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-12): raise AssertionError((path,actual,expected))
    elif type(actual) is not type(expected) or actual!=expected:
        raise AssertionError((path,actual,expected))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='compare fresh controls to frozen summary')
    parser.add_argument('--sources',type=Path,help='optional directory of original Library source bytes')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    report = run_audit()
    if not report['numerical_controls_passed']: raise SystemExit('verification failed')
    verification = verify_sources(base/'SOURCE_MANIFEST.json',args.sources)
    if args.check: compare(report,json.loads((base/'SUMMARY.json').read_text()))
    print(json.dumps({'audit':report,'source_verification':verification},indent=2,sort_keys=True,allow_nan=False))


if __name__=='__main__':
    main()
