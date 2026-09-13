#!/usr/bin/env python3
"""v15.15: an explicit coherent dilation of the frozen v15.14 instruments.

Four diagnostic quantum record registers are SUPPLIED. Pinching is a declared
retained-description operation, not a derived collapse or actuality law.
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
import adaptive as prior

EVENTS=prior.EVENTS
D=16
N=D*D
TOL=1e-11
HASHES={'adaptive.py':'44a87e4cc5bcf531ef7798aadab5d9dbba3482cb',
        'vendor/v1513.py':'95d0303d617422d74e61ae017f0354233ec9454b',
        'vendor/__init__.py':'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'}


def verify_baseline() -> dict:
    for name,expected in HASHES.items():
        data=(ROOT/'baseline'/name).read_bytes()
        found=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        if found!=expected:raise ValueError(f'frozen baseline differs: {name}')
    return dict(HASHES)


def _readonly(a):
    a.setflags(write=False)
    return a


def bit(value,index):
    return (value>>(3-index))&1


@lru_cache(None)
def controller_gate(event: str, wrong: bool=False) -> np.ndarray:
    if event not in EVENTS:raise ValueError('undeclared event')
    gate=np.zeros((N,N),complex)
    for memory in range(D):
        # This is a quantum block-controlled operator, not a realized classical
        # record lookup. BOTH controller values coexist in the supplied gate.
        values={e:bit(memory,EVENTS.index(e)) for e in prior.READS[event]}
        if wrong and event=='B2':values['A1']=1-values['A1']
        u=prior.instrument(event,values)
        sl=slice(memory*D,(memory+1)*D)
        gate[sl,sl]=u
    return _readonly(gate)


@lru_cache(None)
def copy_gate(event: str) -> np.ndarray:
    if event not in EVENTS:raise ValueError('undeclared event')
    q=EVENTS.index(event)
    gate=np.zeros((N,N),complex)
    for memory,system in itertools.product(range(D),repeat=2):
        new_memory=memory^(bit(system,q)<<(3-q))
        gate[new_memory*D+system,memory*D+system]=1
    return _readonly(gate)


@lru_cache(None)
def event_gate(event: str,wrong: bool=False) -> np.ndarray:
    return _readonly(copy_gate(event)@controller_gate(event,wrong))


def encoding(schedule,wrong: bool=False) -> list[dict]:
    if not isinstance(schedule,(tuple,list)) or tuple(schedule) not in prior.schedules():
        raise ValueError('use a schedule compatible with the supplied write/read dependencies')
    w=np.eye(N,dtype=complex)
    out=[{'done':(),'event':None,'W':w.copy(),'V':w[:,:D].copy()}]
    done=[]
    for event in schedule:
        w=event_gate(event,wrong)@w
        done.append(event)
        out.append({'done':tuple(e for e in EVENTS if e in done),'event':event,
                    'W':w.copy(),'V':w[:,:D].copy()})
    return out


def branch_operator(schedule,records: str) -> np.ndarray:
    prior.base.validate_records(records)
    if not isinstance(schedule,(tuple,list)) or len(set(schedule))!=len(schedule):
        raise ValueError('distinct declared event prefix required')
    k=np.eye(D,dtype=complex); realized={}
    for event in schedule:
        if event not in EVENTS or not set(prior.READS[event])<=set(realized):
            raise ValueError('record-read prerequisites missing')
        u=prior.instrument(event,{e:realized[e] for e in prior.READS[event]})
        b=int(records[EVENTS.index(event)])
        k=prior.base.projector(EVENTS.index(event),b)@u@k
        realized[event]=b
    return k


def initial_joint(rho: np.ndarray) -> np.ndarray:
    rho=np.asarray(rho,complex)
    if rho.shape!=(D,D) or not np.all(np.isfinite(rho)) or np.linalg.norm(rho-rho.conj().T)>TOL:
        raise ValueError('finite Hermitian system density matrix required')
    if abs(np.trace(rho)-1)>TOL or np.linalg.eigvalsh(rho).min() < -TOL:
        raise ValueError('normalized positive system state required')
    out=np.zeros((N,N),complex);out[:D,:D]=rho
    return out


def pinch_records(rho: np.ndarray) -> np.ndarray:
    a=np.asarray(rho,complex)
    if a.shape!=(N,N) or not np.all(np.isfinite(a)):
        raise ValueError('finite 256x256 joint operator required')
    out=np.zeros_like(a)
    for r in range(D):
        sl=slice(r*D,(r+1)*D);out[sl,sl]=a[sl,sl]
    return out


def weights(a: np.ndarray) -> np.ndarray:
    return np.real(np.trace(a.reshape(D,D,D,D),axis1=1,axis2=3).diagonal())


def record_block_norms(a: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum(abs(a.reshape(D,D,D,D))**2,axis=(1,3)))


def memory_marginal(a: np.ndarray) -> np.ndarray:
    return np.trace(a.reshape(D,D,D,D),axis1=1,axis2=3)


def choi_difference(a: np.ndarray,b: np.ndarray) -> float:
    """Frobenius distance of normalized-input single-branch Choi blocks."""
    x=a.reshape(-1,order='F');y=b.reshape(-1,order='F')
    return float(np.linalg.norm(np.outer(x,x.conj())-np.outer(y,y.conj()))/D)


def _joint_trace_distance(a,b):
    delta=a-b
    return float(np.sum(np.abs(np.linalg.eigvalsh((delta+delta.conj().T)/2)))/2)


def echo_controls(stage: dict,rho: np.ndarray) -> dict:
    v,w=stage['V'],stage['W']; original=initial_joint(rho)
    coherent=v@rho@v.conj().T; classical=pinch_records(coherent)
    echoed=w.conj().T@coherent@w; pinched_echo=w.conj().T@classical@w
    memory=memory_marginal(coherent)
    return {'coherent_inverse_error':float(np.linalg.norm(echoed-original)),
            'pinched_inverse_distance':_joint_trace_distance(pinched_echo,original),
            'joint_record_offdiagonal_norm':float(np.linalg.norm(coherent-classical)),
            'memory_marginal_offdiagonal_norm':float(np.linalg.norm(memory-np.diag(memory.diagonal()))),
            'scope':'same declared inverse; global no-recovery conclusion uses a distinct-input witness, not this inverse attempt alone'}


def witness_controls(stage: dict) -> dict:
    v=stage['V']; plus=np.ones(2)/np.sqrt(2); minus=np.array([1.,-1.])/np.sqrt(2)
    vectors=[]
    for first in (plus,minus):
        p=first
        for _ in range(3):p=np.kron(p,plus)
        vectors.append(prior.base.event_unitary('A1').conj().T@p)
    states=[np.outer(p,p.conj()) for p in vectors]
    outputs=[v@r@v.conj().T for r in states]
    pinched=[pinch_records(r) for r in outputs]
    return {'input_distance':prior.base.distance(*states),
            'coherent_output_distance':_joint_trace_distance(*outputs),
            'pinched_output_distance':_joint_trace_distance(*pinched),
            'pinched_record_probability_error':float(np.max(np.abs(weights(outputs[0])-weights(outputs[1])))),
            'scope':'the declared full system plus classical record description loses this distinction; no common inverse on both inputs exists'}


def phase_control(stage: dict,rho: np.ndarray) -> dict:
    v=stage['V']; phases=np.exp(1j*np.arange(D)*.37)
    shifted=phases.repeat(D)[:,None]*v
    a=v@rho@v.conj().T;b=shifted@rho@shifted.conj().T
    return {'labeled_channel_error':max(choi_difference(v[r*D:(r+1)*D],shifted[r*D:(r+1)*D]) for r in range(D)),
            'coherent_state_distance':_joint_trace_distance(a,b),
            'scope':'record-sector phases are unobservable after record pinching; coherent dilations are not unique'}


def verify_result(r: dict) -> None:
    for key in ('max_branch_operator_error','max_labeled_choi_error','max_shared_encoding_error',
                'max_prior_state_error','max_prior_mass_error','max_deferred_pinching_error',
                'max_record_probability_error','max_distribution_normalization_error','max_isometry_error'):
        if not np.isfinite(r[key]) or r[key]>TOL:raise AssertionError((key,r[key]))
    w=r['distinguishability_witness'];echo=r['echo']
    if echo['coherent_inverse_error']>TOL or echo['pinched_inverse_distance']<.05:raise AssertionError('echo control failed')
    if abs(w['input_distance']-1)>TOL or abs(w['coherent_output_distance']-1)>TOL or w['pinched_output_distance']>TOL:raise AssertionError('distinguishability witness failed')
    if r['wrong_controller_control']['max_labeled_choi_error']<.01:raise AssertionError('negative control insensitive')
    if r['phase_control']['labeled_channel_error']>TOL or r['phase_control']['coherent_state_distance']<.01:raise AssertionError('phase control failed')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();rho=prior.base.initial_state()
    maxima={k:0. for k in ('max_branch_operator_error','max_labeled_choi_error','max_shared_encoding_error',
                'max_prior_state_error','max_prior_mass_error','max_deferred_pinching_error',
                'max_record_probability_error','max_distribution_normalization_error','max_isometry_error')}
    seen={};count=0;final_count=0
    for schedule in prior.schedules():
        stages=encoding(schedule);sequential=initial_joint(rho)
        for index,stage in enumerate(stages):
            v=stage['V'];done=stage['done']
            if done in seen:maxima['max_shared_encoding_error']=max(maxima['max_shared_encoding_error'],float(np.linalg.norm(v-seen[done])))
            else:seen[done]=v.copy()
            maxima['max_isometry_error']=max(maxima['max_isometry_error'],float(np.linalg.norm(v.conj().T@v-np.eye(D))))
            coherent=v@rho@v.conj().T; classical=pinch_records(coherent)
            if index:
                gate=event_gate(schedule[index-1]);sequential=pinch_records(gate@sequential@gate.conj().T)
            maxima['max_deferred_pinching_error']=max(maxima['max_deferred_pinching_error'],float(np.linalg.norm(sequential-classical)))
            maxima['max_record_probability_error']=max(maxima['max_record_probability_error'],float(np.max(abs(weights(coherent)-weights(classical)))))
            maxima['max_distribution_normalization_error']=max(maxima['max_distribution_normalization_error'],float(abs(weights(coherent).sum()-1)))
            for record in range(D):
                b=v[record*D:(record+1)*D]
                inactive=any(bit(record,q) for q,e in enumerate(EVENTS) if e not in done)
                k=np.zeros((D,D),complex) if inactive else branch_operator(schedule[:index],f'{record:04b}')
                maxima['max_branch_operator_error']=max(maxima['max_branch_operator_error'],float(np.linalg.norm(b-k)))
                maxima['max_labeled_choi_error']=max(maxima['max_labeled_choi_error'],choi_difference(b,k))
                if not inactive:count+=1
                if index==4:
                    final_count+=1;old=prior.run(schedule,f'{record:04b}')[-1]
                    tau=b@rho@b.conj().T;p=float(np.trace(tau).real)
                    if p<=0:raise AssertionError('supplied full-rank fixture branch must be positive')
                    maxima['max_prior_mass_error']=max(maxima['max_prior_mass_error'],abs(p-old.mass))
                    maxima['max_prior_state_error']=max(maxima['max_prior_state_error'],prior.base.distance(tau/p,old.rho))
    final=encoding(prior.schedules()[0])[-1]
    bad=encoding(prior.schedules()[0],True)[-1]['V']
    result={'version':'v15.15','status':'EXECUTED_CONDITIONAL_COHERENT_RECORD_COMPARISON',
            'schedules':5,'record_assignments':16,'final_branch_maps_compared':final_count,
            'prefix_branch_maps_compared':count,'common_ideals':len(seen),**maxima,
            'echo':echo_controls(final,rho),'distinguishability_witness':witness_controls(final),
            'phase_control':phase_control(final,rho),
            'wrong_controller_control':{'max_labeled_choi_error':max(choi_difference(final['V'][r*D:(r+1)*D],bad[r*D:(r+1)*D]) for r in range(D)),
                                        'status':'REJECTED_SWAPPED_CONTROLLER_COMPARISON'},
            'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
            'objective_collapse_derived':False,'physical_entropy_production_derived':False,
            'Pillar_3':'OPEN','scientific_breakthrough':False,
            'scope':'Equality of the supplied labeled instruments does not identify a physical collapse. Irreversibility is relative to explicitly pinched retained record blocks.'}
    verify_result(result)
    return result


def visual_payload() -> dict:
    rho=prior.base.initial_state();branches=[]
    for schedule in prior.schedules():
        frames=[]
        for stage in encoding(schedule):
            c=stage['V']@rho@stage['V'].conj().T; p=pinch_records(c)
            frames.append({'done':list(stage['done']),'event':stage['event'],
                           'coherent_blocks':record_block_norms(c).tolist(),
                           'pinched_blocks':record_block_norms(p).tolist(),
                           'record_probabilities':weights(c).tolist(),
                           'joint_offdiagonal_norm':float(np.linalg.norm(c-p))})
        branches.append({'schedule':list(schedule),'frames':frames})
    return {'version':'v15.15','branches':branches,'audit':audit(),
            'display_notice':'Checkpoint order is circuit composition, not elapsed physical time. No actual branch is selected.'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    payload=visual_payload()
    (args.out/'verification.json').write_text(json.dumps(payload['audit'],indent=2,allow_nan=False)+'\n')
    (args.out/'replay_data.json').write_text(json.dumps(payload,separators=(',',':'),allow_nan=False)+'\n')
    stages=encoding(prior.schedules()[0])
    np.savez_compressed(args.out/'quantum_encoding.npz',V=np.stack([s['V'] for s in stages]),W=stages[-1]['W'],rho=prior.base.initial_state())
    print(json.dumps(payload['audit'],indent=2,allow_nan=False))

if __name__=='__main__':main()
