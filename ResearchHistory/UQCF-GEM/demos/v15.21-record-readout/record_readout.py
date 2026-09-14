#!/usr/bin/env python3
"""v15.21: ensemble readout is not a single-copy adaptive quantum instrument.

Uses frozen v15.20 encoding and v15.14 instruments. No RCR is chosen or sampled.
The signed branch update is valid on the encoded image, NOT a CPTP extension.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import physical_predictor as pp
import adaptive
D=16
TOL=1e-10
BLOB='e48f19de7c74d9c7dcf917a66bf7b06138fd36eb'
I=np.eye(D,dtype=complex)


def verify_baseline() -> dict:
    raw=(ROOT/'baseline/physical_predictor.py').read_bytes()
    digest=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if digest!=BLOB: raise ValueError('frozen predictor changed')
    pp.verify_baseline()
    return {'predictor_git_blob':digest,'inherited_baseline_verified':True}


def encode(rho: np.ndarray) -> np.ndarray:
    return pp.apply_channel(rho,.5,0)


def history_operator(schedule,records: str) -> np.ndarray:
    """Prefix branch operator. Resolver sees realized reads only, not future bits."""
    adaptive.base.validate_records(records)
    if not isinstance(schedule,(list,tuple)) or len(set(schedule))!=len(schedule):
        raise ValueError('distinct declared prefix events required')
    realized={};k=I.copy()
    for e in schedule:
        if e not in adaptive.EVENTS or not set(adaptive.READS[e])<=set(realized):
            raise ValueError('missing realized prerequisite')
        u=adaptive.instrument(e,{r:realized[r] for r in adaptive.READS[e]})
        b=int(records[adaptive.EVENTS.index(e)])
        k=adaptive.base.projector(adaptive.EVENTS.index(e),b)@u@k
        realized[e]=b
    return k


def first_effect() -> np.ndarray:
    k=history_operator(('A1',),'0000')
    return k.conj().T@k


def eigenpair() -> tuple[np.ndarray,np.ndarray]:
    f=first_effect()
    return f/8,(I-f)/8


def readout_effect(c: float=0.) -> np.ndarray:
    if isinstance(c,bool) or not isinstance(c,(int,float)) or not math.isfinite(c):
        raise ValueError('finite real coefficient required')
    return 2*first_effect()-.5*I+c*pp.gamma()


def obstruction() -> dict:
    a,b=eigenpair();sa,sb=encode(a),encode(b);f=first_effect()
    d=pp.distance(sa,sb)
    return {'input_distance':pp.distance(a,b),'encoded_distance':d,
            'encoded_pair_minimum_eigenvalue':float(min(np.linalg.eigvalsh(s).min() for s in (sa,sb))),
            'native_encoded_probabilities':[float(np.trace(f@s).real) for s in (sa,sb)],
            'minimax_binary_probability_error':(1-d)/2,
            'decoded_effect_eigenvalue_range':[float(np.linalg.eigvalsh(readout_effect()).min()),float(np.linalg.eigvalsh(readout_effect()).max())],
            'all_extension_spectrum':'1/2 +/- sqrt(1+c^2), c real; no valid POVM effect exists',
            'contract':'All-input reproduction of the first binary record probability from one encoded copy; arbitrary POVM allowed.'}


def distribution_decoder() -> np.ndarray:
    return 2*np.eye(D)-np.ones((D,D))/D


@lru_cache(None)
def inputs() -> dict[str,np.ndarray]:
    result={'fixture':pp.fixture(),'maximally_mixed':I/D}
    schedule=adaptive.schedules()[0]
    for r in range(D):
        k=history_operator(schedule,f'{r:04b}')
        result[f'basis_{r:04b}']=k.conj().T@k
    return result


def history_distribution(rho: np.ndarray,schedule) -> dict:
    if tuple(schedule) not in adaptive.schedules():raise ValueError('permissible complete schedule required')
    sigma=encode(rho);p=[];q=[]
    for r in range(D):
        k=history_operator(schedule,f'{r:04b}')
        p.append(float(np.trace(k@rho@k.conj().T).real))
        q.append(float(np.trace(k@sigma@k.conj().T).real))
    return {'ideal':p,'raw':q,'decoded':(distribution_decoder()@q).tolist()}


def conditional(child: float,parent: float) -> float:
    if not np.isfinite([child,parent]).all() or parent<=1e-12:
        raise ValueError('positive resolved parent mass required; no outcome is selected')
    return float(child/parent)


def path_rows(rho: np.ndarray,schedule,records: str) -> list[dict]:
    sigma=encode(rho);rows=[];p0=q0=d0=1.
    for i,e in enumerate(schedule,1):
        k=history_operator(schedule[:i],records);h=k.conj().T@k
        rank=float(np.trace(h).real)
        p=float(np.trace(h@rho).real);q=float(np.trace(h@sigma).real)
        decoded=2*q-rank/D
        rows.append({'event':e,'prefix':list(schedule[:i]),'ideal_mass':p,'raw_mass':q,'decoded_mass':decoded,
                     'effect_trace':rank,'ideal_conditional':conditional(p,p0),
                     'raw_conditional':conditional(q,q0),'decoded_conditional':conditional(decoded,d0),
                     'naive_local_rescaling':2*conditional(q,q0)-.5})
        p0,q0,d0=p,q,decoded
    return rows


def signed_branch(sigma: np.ndarray,k: np.ndarray) -> np.ndarray:
    """Linear formula, NOT accepted as a physical map on arbitrary states."""
    reconstructed=2*sigma-np.trace(sigma)*I/D
    return pp.linear_map(k@reconstructed@k.conj().T,.5,0)


def formal_control() -> dict:
    err=0.;positivity=0.;count=0
    for s in adaptive.schedules():
        for r in range(D):
            rho=pp.fixture();record={}
            for e in s:
                u=adaptive.instrument(e,{j:record[j] for j in adaptive.READS[e]})
                bit=int(f'{r:04b}'[adaptive.EVENTS.index(e)])
                k=adaptive.base.projector(adaptive.EVENTS.index(e),bit)@u
                native=k@rho@k.conj().T
                left=signed_branch(encode(rho),k)
                right=pp.linear_map(native,.5,0)
                err=max(err,float(np.linalg.norm(left-right)))
                positivity=min(positivity,float(np.linalg.eigvalsh((left+left.conj().T)/2).min()))
                rho=native/np.trace(native);record[e]=bit;count+=1
    _,outside=eigenpair();k=history_operator(('A1',),'0000')
    negative=float(np.trace(signed_branch(outside,k)).real)
    return {'branch_updates_checked':count,'max_on_image_branch_error':err,'minimum_on_image_output_eigenvalue':positivity,
            'outside_image_negative_branch_weight_magnitude':-negative,
            'scope':'Exact signed computation on encoded inputs only; no positive all-state instrument extension.'}


def copy_error(n: int) -> float:
    """Exact equal-prior optimal discrimination error for the fixed pair.

    N identically prepared independent copies are an extra diagnostic resource,
    not a claim of cloned states or multiple physical actualities.
    """
    if type(n) is not int or not 1<=n<=100:raise ValueError('integer copy count 1..100 required')
    total=sum(math.comb(n,k)*.75**k*.25**(n-k) for k in range((n+1)//2))
    if n%2==0:total+=.5*math.comb(n,n//2)*.75**(n//2)*.25**(n//2)
    return float(total)


def verify_result(r: dict) -> None:
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(int,float)) and not isinstance(x,bool):
            if not np.isfinite(x):raise AssertionError('nonfinite result')
    finite(r)
    for name in ['max_decoded_joint_error','max_joint_noise_formula_error','max_decoded_conditional_error',
                 'max_branch_parity_output_norm','max_schedule_probability_error']:
        if r[name]>TOL:raise AssertionError(name)
    if r['full_history_probabilities_checked']!=1440 or r['fixture_conditional_checks']!=320:raise AssertionError('coverage')
    if abs(r['obstruction']['encoded_distance']-.5)>TOL or abs(r['obstruction']['minimax_binary_probability_error']-.25)>TOL:raise AssertionError('discrimination witness')
    if r['formal_control']['max_on_image_branch_error']>TOL or r['formal_control']['outside_image_negative_branch_weight_magnitude']<.1:raise AssertionError('signed map boundary')
    if r['max_naive_conditional_error']<.01:raise AssertionError('insensitive conditioning control')
    for name in ['physical_pruning_law_derived','single_copy_event_channel_derived']:
        if r[name] is not False:raise AssertionError('unsupported physical claim')
    if r['actual_record_selected'] is not None or r['physical_duration'] is not None or r['new_physical_axioms']!=[]:raise AssertionError('ontology boundary')


@lru_cache(None)
def audit() -> dict:
    baseline=verify_baseline();decoded=direct=noise=parity=schedule_error=0.;count=0
    for rho in inputs().values():
        reference=None
        for s in adaptive.schedules():
            row=history_distribution(rho,s);p,q,d=(np.array(row[k]) for k in ('ideal','raw','decoded'))
            decoded=max(decoded,float(np.max(abs(d-p))));direct=max(direct,float(np.max(abs(q-p))))
            noise=max(noise,float(np.max(abs(q-.5*p-1/32))))
            if reference is not None:schedule_error=max(schedule_error,float(np.max(abs(p-reference))))
            else:reference=p
            count+=D
    for s in adaptive.schedules():
        for i in range(1,5):
            for r in range(D):
                k=history_operator(s[:i],f'{r:04b}')
                parity=max(parity,float(np.linalg.norm(k@pp.gamma()@k.conj().T)))
    ce=naive=0.;n=0;worst=None
    for s in adaptive.schedules():
        for r in range(D):
            for row in path_rows(pp.fixture(),s,f'{r:04b}'):
                ce=max(ce,abs(row['decoded_conditional']-row['ideal_conditional']))
                delta=abs(row['naive_local_rescaling']-row['ideal_conditional'])
                if delta>naive:naive=delta;worst={'schedule':list(s),'records':f'{r:04b}',**row}
                n+=1
    result={'version':'v15.21','status':'ENSEMBLE_READOUT_PRESERVED_SINGLE_COPY_RECORD_INSTRUMENT_OBSTRUCTED',
            'baseline':baseline,'input_fixtures':18,'schedules':5,'full_history_probabilities_checked':count,
            'fixture_conditional_checks':n,'max_decoded_joint_error':decoded,'max_direct_joint_error':direct,
            'max_joint_noise_formula_error':noise,'max_branch_parity_output_norm':parity,
            'max_schedule_probability_error':schedule_error,'max_decoded_conditional_error':ce,
            'max_naive_conditional_error':naive,'worst_naive_conditional_example':worst,
            'obstruction':obstruction(),'formal_control':formal_control(),
            'joint_decode_formula':'p_r=2 q_r-1/16; q_r=p_r/2+1/32',
            'finite_copy_pair_error':[{'copies':n,'equal_prior_error':copy_error(n)} for n in (1,2,3,5,9,15)],
            'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
            'physical_pruning_law_derived':False,'single_copy_event_channel_derived':False,
            'Pillar_3':'OPEN','scientific_breakthrough':False,
            'scope':'Frozen same-carrier noisy predictor. Ensemble statistics and formal signed updates are not a universally valid single-copy quantum instrument or physical actuality selector.'}
    verify_result(result);return result


def payload() -> dict:
    cases=[]
    for name,rho in inputs().items():
        for index,s in enumerate(adaptive.schedules()):
            cases.append({'input':name,'schedule_index':index,'schedule':list(s),**history_distribution(rho,s)})
    return {'audit':audit(),'cases':cases,'fixture_paths':[{'schedule':list(s),'rows':path_rows(pp.fixture(),s,'1001')} for s in adaptive.schedules()]}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);result=payload()
    (a.out/'verification.json').write_text(json.dumps(result['audit'],indent=2,allow_nan=False)+'\n')
    (a.out/'replay_data.json').write_text(json.dumps(result,separators=(',',':'),allow_nan=False)+'\n')
    print(json.dumps(result['audit'],indent=2,allow_nan=False))

if __name__=='__main__':main()
