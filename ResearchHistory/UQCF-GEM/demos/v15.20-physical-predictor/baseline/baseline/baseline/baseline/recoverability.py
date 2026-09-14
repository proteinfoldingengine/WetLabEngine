#!/usr/bin/env python3
"""v15.16: exact observable survival for SUPPLIED partial record pinching.

No time, entropy-production objective, actuality selector or new dynamics.
Masks refer to the completed encoding, not a chronological collapse sequence.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import coherent_records as old
TOL=1e-11
D=16
HASHES={'coherent_records.py':'fdf5367b11729fc1e2bfccd8d8daa2a0c7209049',
        'baseline/adaptive.py':'44a87e4cc5bcf531ef7798aadab5d9dbba3482cb',
        'baseline/vendor/v1513.py':'95d0303d617422d74e61ae017f0354233ec9454b',
        'baseline/vendor/__init__.py':'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'}


def verify_baseline() -> dict:
    for name,expected in HASHES.items():
        data=(ROOT/'baseline'/name).read_bytes()
        found=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        if found!=expected:raise ValueError(f'baseline changed: {name}')
    return dict(HASHES)


def masks() -> tuple[str,...]:return tuple(f'{i:04b}' for i in range(16))


def _mask(mask: str) -> int:
    if type(mask) is not str or len(mask)!=4 or any(c not in '01' for c in mask):
        raise ValueError('four binary mask digits in A1,A2,B1,B2 order required')
    return int(mask,2)


def _operator(a,dim):
    a=np.asarray(a,dtype=complex)
    if a.shape!=(dim,dim) or not np.all(np.isfinite(a)):
        raise ValueError(f'finite {dim}x{dim} operator required')
    return a


def _immutable(a):
    a=np.asarray(a)
    return np.frombuffer(a.tobytes(),dtype=a.dtype).reshape(a.shape)


@lru_cache(None,typed=True)
def encoding(schedule: int=0) -> np.ndarray:
    if type(schedule) is not int or not 0<=schedule<5:raise ValueError('schedule index 0..4 required')
    verify_baseline()
    return _immutable(old.encoding(old.prior.schedules()[schedule])[-1]['V'])


@lru_cache(None,typed=True)
def basis(schedule: int=0) -> np.ndarray:
    """Rows <b_r| are extracted from the frozen K_r=|r><b_r|, not fitted."""
    v=encoding(schedule)
    f=np.stack([v[r*D+r,:] for r in range(D)])
    remainder=v.copy()
    for r in range(D):remainder[r*D+r,:]=0
    if np.linalg.norm(remainder)>TOL or np.linalg.norm(f.conj().T@f-np.eye(D))>TOL:
        raise ArithmeticError('sharp complete measurement structure not certified')
    return _immutable(f)


def groups(mask: str) -> tuple[tuple[int,...],...]:
    n=_mask(mask)
    return tuple(tuple(r for r in range(D) if r&n==s) for s in sorted({r&n for r in range(D)}))


def keep_matrix(mask: str) -> np.ndarray:
    n=_mask(mask);v=np.arange(D)&n
    return v[:,None]==v[None,:]


def projectors(mask: str,schedule: int=0) -> tuple[np.ndarray,...]:
    f=basis(schedule)
    return tuple(f[list(g)].conj().T@f[list(g)] for g in groups(mask))


def fixture() -> np.ndarray:return old.prior.base.initial_state()


def reduce_input(a: np.ndarray,mask: str,schedule: int=0) -> np.ndarray:
    """Conditional expectation equivalent to partial pinching on this code."""
    a=_operator(a,D);f=basis(schedule)
    return f.conj().T@(keep_matrix(mask)*(f@a@f.conj().T))@f


def pinch_joint(a: np.ndarray,mask: str) -> np.ndarray:
    a=_operator(a,D*D)
    return (a.reshape(D,D,D,D)*keep_matrix(mask)[:,None,:,None]).reshape(D*D,D*D)


def observable_recoverable(a: np.ndarray,mask: str,schedule: int=0) -> bool:
    """All-input observable recoverability, not state-specific guessing."""
    a=_operator(a,D)
    if np.linalg.norm(a-a.conj().T)>TOL:raise ValueError('Hermitian observable required')
    return bool(np.linalg.norm(reduce_input(a,mask,schedule)-a)<=TOL*max(1.,np.linalg.norm(a)))


def distance(a,b) -> float:
    delta=np.asarray(a)-np.asarray(b)
    return float(np.abs(np.linalg.eigvalsh((delta+delta.conj().T)/2)).sum()/2)


def phase_pair(i: int,j: int,phase: complex=1,schedule: int=0) -> tuple[np.ndarray,np.ndarray]:
    if type(i) is not int or type(j) is not int or not 0<=i<j<D:raise ValueError('labels must satisfy 0<=i<j<16')
    if phase not in (1,1j):raise ValueError('real or imaginary phase witness required')
    f=basis(schedule);x=f[i].conj();y=f[j].conj()
    a=(x+phase*y)/np.sqrt(2);b=(x-phase*y)/np.sqrt(2)
    return np.outer(a,a.conj()),np.outer(b,b.conj())


def details(mask: str) -> dict:
    gs=groups(mask);dim=sum(len(g)**2 for g in gs)
    return {'mask':mask,'pinched_records':[e for e,b in zip(old.EVENTS,mask) if b=='1'],
            'blocks':[list(g) for g in gs],'block_ranks':[len(g) for g in gs],
            'hermitian_dimension':dim,'lost_hermitian_directions':D*D-dim,
            'center_dimension':len(gs),'surviving_unordered_pairs':sum(len(g)*(len(g)-1)//2 for g in gs),
            'keep_matrix':keep_matrix(mask).astype(int).tolist()}


def negative_control() -> dict:
    """Unsharp instrument: compressed effects are NOT orthogonal projectors."""
    k0=np.diag(np.sqrt([.8,.2]));k1=np.diag(np.sqrt([.2,.8]));v=np.vstack([k0,k1])
    q=[np.diag([1,1,0,0]),np.diag([0,0,1,1])];ps=[v.conj().T@x@v for x in q]
    rho=np.ones((2,2))/2
    compress=lambda r:sum(p@r@p for p in ps)
    out=sum(x@v@rho@v.conj().T@x for x in q)
    return {'status':'REJECTED_GENERALIZATION_TO_UNSHARP_INSTRUMENT',
            'intertwining_error':max(float(np.linalg.norm(x@v-v@p)) for x,p in zip(q,ps)),
            'naive_compressed_output_error':float(np.linalg.norm(out-v@compress(rho)@v.conj().T)),
            'compression_idempotence_error':float(np.linalg.norm(compress(compress(rho))-compress(rho))),
            'note':'The formula requires the certified sharp, range-invariant encoding; no new physical channel is adopted.'}


def verify_result(r: dict) -> None:
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(float,int)) and not isinstance(x,bool):
            if not np.isfinite(x):raise AssertionError('nonfinite verification value')
    finite(r)
    for k,v in r.items():
        if k.startswith('max_') and v>TOL:raise AssertionError((k,v))
    if r['phase_witness_cases']!=3840 or r['schedule_mask_cases']!=80:raise AssertionError('coverage mismatch')
    if r['negative_control']['intertwining_error']<.1:raise AssertionError('insensitive negative control')
    if r['actual_record_selected'] is not None or r['physical_duration'] is not None or r['new_physical_axioms']!=[]:
        raise AssertionError('claim boundary changed')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();rho=fixture();errors={k:0. for k in ('max_basis_unitarity_error','max_intertwining_error',
        'max_joint_route_error','max_decoder_error','max_shared_projector_error','max_record_probability_error',
        'max_phase_witness_error','max_union_composition_error')}
    cases=0
    for s in range(5):
        v=encoding(s);f=basis(s);c=v@rho@v.conj().T
        errors['max_basis_unitarity_error']=max(errors['max_basis_unitarity_error'],float(np.linalg.norm(f.conj().T@f-np.eye(D))))
        for mask in masks():
            cases+=1;out=pinch_joint(c,mask);e=reduce_input(rho,mask,s)
            errors['max_joint_route_error']=max(errors['max_joint_route_error'],float(np.linalg.norm(out-v@e@v.conj().T)))
            errors['max_decoder_error']=max(errors['max_decoder_error'],float(np.linalg.norm(v.conj().T@out@v-e)))
            errors['max_record_probability_error']=max(errors['max_record_probability_error'],float(np.max(abs(np.diag(f@e@f.conj().T)-np.diag(f@rho@f.conj().T)))))
            for inds,p,p0 in zip(groups(mask),projectors(mask,s),projectors(mask)):
                qv=np.zeros_like(v)
                for i in inds:qv[i*D:(i+1)*D]=v[i*D:(i+1)*D]
                errors['max_intertwining_error']=max(errors['max_intertwining_error'],float(np.linalg.norm(qv-v@p)))
                errors['max_shared_projector_error']=max(errors['max_shared_projector_error'],float(np.linalg.norm(p-p0)))
    pair_cases=0
    for mask in masks():
        for i,j in itertools.combinations(range(D),2):
            for phase in (1,1j):
                a,b=phase_pair(i,j,phase);expected=float(keep_matrix(mask)[i,j])
                errors['max_phase_witness_error']=max(errors['max_phase_witness_error'],abs(distance(a,b)-1),abs(distance(reduce_input(a,mask),reduce_input(b,mask))-expected))
                pair_cases+=1
    for a,b in itertools.product(masks(),repeat=2):
        union=f'{int(a,2)|int(b,2):04b}'
        errors['max_union_composition_error']=max(errors['max_union_composition_error'],float(np.linalg.norm(reduce_input(reduce_input(rho,a),b)-reduce_input(rho,union))))
    r={'version':'v15.16','status':'EXECUTED_CONDITIONAL_RECOVERABLE_OBSERVABLE_MAP',
       'schedule_mask_cases':cases,'phase_witness_cases':pair_cases,'union_composition_cases':256,
       **errors,'dimension_chain':[256,128,64,32,16],'phase_pair_chain':[120,56,24,8,0],
       'masks':[details(mask) for mask in masks()],'negative_control':negative_control(),
       'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
       'physical_entropy_law_derived':False,'physical_collapse_law_derived':False,'Pillar_3':'OPEN',
       'scientific_breakthrough':False,
       'scope':'Exact for the supplied sharp completed instrument and declared partial record pinching. Observable dimensions are not entropy, elapsed time or a law selecting pinching.'}
    verify_result(r)
    return r


def payload() -> dict:
    result=audit();f=basis();rho=fixture();rho_b=f@rho@f.conj().T
    return {'version':'v15.16','record_names':list(old.EVENTS),'audit':result,
            'basis_real':f.real.tolist(),'basis_imag':f.imag.tolist(),
            'fixture_in_record_basis_real':rho_b.real.tolist(),'fixture_in_record_basis_imag':rho_b.imag.tolist(),
            'note':'Mask toggles compare alternative supplied reductions of the SAME completed encoding. Untoggling is not physical recovery.'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True);data=payload()
    (args.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    (args.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    np.savez_compressed(args.out/'encoding_and_basis.npz',V=encoding(),basis=basis(),rho=fixture())
    print(json.dumps(data['audit'],indent=2,allow_nan=False))

if __name__=='__main__':main()
