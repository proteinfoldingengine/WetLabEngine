#!/usr/bin/env python3
"""v15.17: fixed-retained-algebra descent of declared reversible motions.

No clock, entropy law or physical motion selector. All counterfactual routes
are explicitly distinguished from actually applying a map after pruning.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'baseline'))
import recoverability as old
D = 16
TOL = 1e-10
HASH = '0a01d2eea4f0114b119fbb7beaf4619775c0f9f6'


def verify_baseline() -> dict:
    data=(ROOT/'baseline/recoverability.py').read_bytes()
    digest=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if digest!=HASH: raise ValueError('v15.16 baseline changed')
    result={'recoverability.py':digest}
    result.update({'baseline/'+k:v for k,v in old.verify_baseline().items()})
    return result


def _matrix(a, *, unitary=False):
    a=np.asarray(a,dtype=complex)
    if a.shape!=(D,D) or not np.all(np.isfinite(a)):
        raise ValueError('finite 16x16 matrix required')
    if unitary and np.linalg.norm(a.conj().T@a-np.eye(D))>TOL:
        raise ValueError('unitary matrix required')
    return a


def exp_unitary(h, extent):
    h=_matrix(h)
    if np.linalg.norm(h-h.conj().T)>TOL or not np.isfinite(extent):
        raise ValueError('finite Hermitian generator and finite extent required')
    vals,vecs=np.linalg.eigh(h)
    return (vecs*np.exp(-1j*extent*vals))@vecs.conj().T


def frozen_motions() -> dict:
    """Reuse old finite operations as candidates; do not fit new laws."""
    b=old.old.prior.base
    return {'pretime':b._pretime_unitary(),
            'A1':b.event_unitary('A1'), 'A2':b.event_unitary('A2'),
            'B1':b.event_unitary('B1'),
            'B2_given_0':old.old.prior.instrument('B2',{'A1':0,'B1':0}),
            'B2_given_1':old.old.prior.instrument('B2',{'A1':1,'B1':0})}


def label_operator(word):
    f=old.basis()
    if type(word) is not str or len(word)!=4 or any(c not in 'IXYZ' for c in word):
        raise ValueError('four Pauli labels required')
    return f.conj().T@old.old.prior.base.tensor_word(word)@f


def control_unitary(name):
    if name=='within': return exp_unitary(label_operator('IIIY'),.37)
    if name=='mix': return exp_unitary(label_operator('YIII'),np.pi/4)
    if name=='swap': return label_operator('XIII')
    if name=='center': return exp_unitary(label_operator('ZIII'),.37)
    raise ValueError('unknown diagnostic control')


def _superoperator(u):
    u=_matrix(u,unitary=True); f=old.basis();b=f@u@f.conj().T
    return np.kron(b.conj(),b)


def leakage_matrix(u, mask):
    keep=old.keep_matrix(mask).reshape(-1,order='F')
    return _superoperator(u)*keep[:,None]*(~keep)[None,:]


def classify(u, mask):
    u=_matrix(u,unitary=True);keep=old.keep_matrix(mask).reshape(-1,order='F')
    g=_superoperator(u)
    leak=float(np.linalg.norm(g*keep[:,None]*(~keep)[None,:]))
    reverse=float(np.linalg.norm(g*(~keep)[:,None]*keep[None,:]))
    ps=old.projectors(mask)
    moved=[u@p@u.conj().T for p in ps]
    errors=np.array([[np.linalg.norm(p-q) for q in ps] for p in moved])
    assignment=np.argmin(errors,axis=1)
    normalizer_error=float(max(errors[i,j] for i,j in enumerate(assignment)))
    fixed=float(max(np.linalg.norm(p-q) for p,q in zip(ps,moved)))
    closed=leak<TOL
    normalizes=normalizer_error<TOL and len(set(assignment.tolist()))==len(ps)
    if closed!=normalizes: raise ArithmeticError('independent closure criteria disagree')
    status=('CLOSED_FIXED_RECORDS' if fixed<TOL else 'CLOSED_RECORD_PERMUTATION') if closed else 'NOT_CLOSED_ON_FIXED_ALGEBRA'
    return {'mask':mask,'closed':closed,'status':status,
            'discarded_to_retained_leakage':leak,'retained_to_discarded_leakage':reverse,
            'normalizer_error':normalizer_error,'fixed_record_error':fixed,
            'block_permutation':assignment.tolist() if closed else None}


def generator_preserves_records(h,mask):
    h=_matrix(h)
    if np.linalg.norm(h-h.conj().T)>TOL:raise ValueError('Hermitian generator required')
    return bool(np.linalg.norm(h-old.reduce_input(h,mask))<TOL*max(1,np.linalg.norm(h)))


def dimensions(mask):
    row=old.details(mask);z=row['center_dimension'];d=row['hermitian_dimension']
    return {'mask':mask,'generator_dimension_including_center':d,
            'central_generators_with_no_retained_action':z,
            'effective_continuous_motion_dimension':d-z,
            'scope':'Inner automorphism action on this fixed full-block algebra; not a clock or physical degree-of-freedom count.'}


def distance(a,b): return old.distance(a,b)


def collision_pair(u,mask):
    """An all-input failure certificate, not a fitted dynamics/record rule."""
    l=leakage_matrix(u,mask);best=None;value=0.
    keep=old.keep_matrix(mask)
    for i in range(D):
        for j in range(i+1,D):
            if keep[i,j]:continue
            for phase in (1,1j):
                # Difference of the orthogonal +/- input states.
                out=phase.conjugate()*l[:,i+D*j]+phase*l[:,j+D*i]
                size=float(np.linalg.norm(out))
                if size>value: value=size;best=(i,j,phase)
    if best is None or value<TOL:raise ValueError('no nonclosed-map collision witness')
    return old.phase_pair(*best)


def transport_error(u,mask):
    """All-input intertwiner P'_s U = U P_s, P'_s=U P_s U†."""
    u=_matrix(u,unitary=True)
    return float(max(np.linalg.norm((u@p@u.conj().T)@u-u@p) for p in old.projectors(mask)))


def controls():
    mask='1000';e=lambda r:old.reduce_input(r,mask)
    f=old.basis();r0=np.outer(f[0].conj(),f[0])
    within=control_unitary('within');mix=control_unitary('mix')
    a,b=old.phase_pair(0,8)
    move=lambda u,r:u@r@u.conj().T
    once=e(move(mix@mix,r0))
    repeated=e(move(mix,e(move(mix,r0))))
    return {'within_state_change':distance(move(within,r0),r0),
            'classifications':{name:classify(control_unitary(name),mask) for name in ('within','mix','swap','center')},
            'witness':{'same_retained_input_distance':distance(e(a),e(b)),
                       'move_then_retain_distance':distance(e(move(mix,a)),e(move(mix,b))),
                       'retain_then_move_then_retain_distance':distance(e(move(mix,e(a))),e(move(mix,e(b))))},
            'projection_cadence_distance':distance(once,repeated),
            'meaning':'Projection cadence changes the operation, not merely its display resolution. No recovery of discarded phase occurs.'}


def verify_result(r):
    def checkfinite(x):
        if isinstance(x,dict):
            for v in x.values():checkfinite(v)
        elif isinstance(x,list):
            for v in x:checkfinite(v)
        elif isinstance(x,(float,int)) and not isinstance(x,bool):
            if not np.isfinite(x):raise AssertionError('nonfinite result')
    checkfinite(r)
    if len(r['cases'])!=96 or sum(r['classification_counts'].values())!=96:raise AssertionError('coverage')
    if r['max_transport_error']>TOL:raise AssertionError('transport identity')
    for row in r['cases']:
        if row['closed']:
            if row['discarded_to_retained_leakage']>TOL:raise AssertionError('false closure')
        else:
            c=row['collision']
            if c['retained_input_distance']>TOL or c['unpruned_motion_output_distance']<1e-8:raise AssertionError('invalid collision')
    w=r['controls']['witness']
    if w['same_retained_input_distance']>TOL or abs(w['move_then_retain_distance']-1)>TOL or w['retain_then_move_then_retain_distance']>TOL:
        raise AssertionError('collision control')
    if abs(r['controls']['projection_cadence_distance']-.5)>TOL:raise AssertionError('cadence control')
    if r['physical_duration'] is not None or r['actual_record_selected'] is not None or r['new_physical_axioms']:
        raise AssertionError('claim boundary')


@lru_cache(None)
def audit():
    verify_baseline();rows=[];transport=0.
    counts={s:0 for s in ('CLOSED_FIXED_RECORDS','CLOSED_RECORD_PERMUTATION','NOT_CLOSED_ON_FIXED_ALGEBRA')}
    for name,u in frozen_motions().items():
        for mask in old.masks():
            row=classify(u,mask);row['motion']=name;counts[row['status']]+=1
            transport=max(transport,transport_error(u,mask))
            if not row['closed']:
                a,b=collision_pair(u,mask);e=lambda r:old.reduce_input(r,mask)
                row['collision']={'retained_input_distance':distance(e(a),e(b)),
                    'unpruned_motion_output_distance':distance(e(u@a@u.conj().T),e(u@b@u.conj().T)),
                    'actually_pruned_motion_output_distance':distance(e(u@e(a)@u.conj().T),e(u@e(b)@u.conj().T))}
            rows.append(row)
    r={'version':'v15.17','status':'EXECUTED_CONDITIONAL_RETAINED_MOTION_COMPARISON',
        'cases':rows,'classification_counts':counts,'max_transport_error':transport,
        'controls':controls(),'effective_motion_dimension_chain':[dimensions('1'*k+'0'*(4-k)) for k in range(5)],
        'physical_duration':None,'actual_record_selected':None,'new_physical_axioms':[],
        'new_physical_motion_law_derived':False,'physical_entropy_law_derived':False,'Pillar_3':'OPEN','scientific_breakthrough':False,
        'scope':'Fixed versus transported retained algebras, for supplied finite motions. Nonclosure is not invalid physics or recovered information; it blocks exact descent of UNPRUNED motion to a fixed quotient.'}
    verify_result(r);return r


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    a=p.parse_args();r=audit();a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'version':r['version'],'classification_counts':r['classification_counts'],'controls':r['controls']},indent=2))

if __name__=='__main__':main()
