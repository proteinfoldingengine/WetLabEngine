#!/usr/bin/env python3
"""v15.13: supplied independent events; execution schedules are not clocks.

The two local chains, their carrier, generators, retained algebras and outcomes
are illustrative inputs. This tests confluence, not a physical collapse law.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import numpy as np

EVENTS = ('A1','A2','B1','B2')
PAULIS = {'I':np.eye(2,dtype=complex), 'X':np.array([[0,1],[1,0]],complex),
          'Y':np.array([[0,-1j],[1j,0]],complex), 'Z':np.diag([1.,-1.]).astype(complex)}
TOL = 1e-11
BASE_COMMIT = 'c1b0582d15e0720e3e01989f7aa195ed89e6a62a'


def tensor_word(word: str) -> np.ndarray:
    out=np.ones((1,1),complex)
    for c in word: out=np.kron(out,PAULIS[c])
    return out


def unitary(generator: np.ndarray, extent: float) -> np.ndarray:
    h=np.asarray(generator,complex)
    if h.ndim!=2 or h.shape[0]!=h.shape[1] or not np.all(np.isfinite(h)) or not math.isfinite(extent):
        raise ValueError('finite square generator and extent required')
    if np.linalg.norm(h-h.conj().T)>TOL: raise ValueError('Hermitian generator required')
    vals,vecs=np.linalg.eigh(h)
    return (vecs*np.exp(-1j*extent*vals))@vecs.conj().T


def _seed() -> np.ndarray:
    v=np.ones(16,complex)/4
    return .9*np.outer(v,v.conj())+.1*np.eye(16)/16


def _pretime_unitary() -> np.ndarray:
    g=.39*tensor_word('ZIZI')+.27*tensor_word('IZIZ')+.17*tensor_word('YIII')
    return unitary(g,.9)


def initial_state() -> np.ndarray:
    u=_pretime_unitary()
    return u@_seed()@u.conj().T


def pretime_control() -> dict:
    u=_pretime_unitary(); rho=initial_state()
    shaped=rho.reshape(4,4,4,4)
    a=np.trace(shaped,axis1=1,axis2=3); b=np.trace(shaped,axis1=0,axis2=2)
    pt=shaped.transpose(0,3,2,1).reshape(16,16)
    return {'state_change':distance(rho,_seed()),
            'inverse_error':float(np.linalg.norm(u.conj().T@rho@u-_seed())),
            'product_state_residual':float(np.linalg.norm(rho-np.kron(a,b))),
            'partial_transpose_min_eigenvalue':float(np.linalg.eigvalsh(pt).min()),
            'extent_semantics':'FINITE_TRANSFORMATION_COORDINATE_NOT_TIME'}


def distance(a: np.ndarray,b: np.ndarray) -> float:
    d=a-b
    return float(np.abs(np.linalg.eigvalsh((d+d.conj().T)/2)).sum()/2)


@lru_cache(None)
def projector(qubit: int,bit: int) -> np.ndarray:
    if type(qubit) is not int or not 0<=qubit<4 or type(bit) is not int or bit not in (0,1):
        raise ValueError('qubit 0..3 and binary integer outcome required')
    word='I'*qubit+'Z'+'I'*(3-qubit)
    p=(np.eye(16)+(1 if bit==0 else -1)*tensor_word(word))/2
    p.setflags(write=False)
    return p


@lru_cache(None)
def event_unitary(event: str) -> np.ndarray:
    if event not in EVENTS: raise ValueError('undeclared event')
    g,extent={
      'A1':(.47*tensor_word('YIII')+.19*tensor_word('ZXII'),.65),
      'A2':(.41*tensor_word('IYII')+.17*tensor_word('ZXII'),.55),
      'B1':(.37*tensor_word('IIYI')+.23*tensor_word('IIZX'),-.45),
      'B2':(.43*tensor_word('IIIY')+.13*tensor_word('IIZX'),.70)}[event]
    u=unitary(g,extent); u.setflags(write=False)
    return u


def kraus(event: str,bit: int,*,coupled_control: bool=False) -> np.ndarray:
    if event not in EVENTS: raise ValueError('undeclared event')
    u=event_unitary(event)
    if coupled_control and event=='B1':
        # Deliberately violates independent support. NEVER a physical addition.
        u=unitary(tensor_word('XIXI'),.47)@u
    return projector(EVENTS.index(event),bit)@u


def validate_records(records: str) -> None:
    if not isinstance(records,str) or len(records)!=4 or any(c not in '01' for c in records):
        raise ValueError('supply four binary outcomes in A1,A2,B1,B2 order; none are chosen automatically')


def schedules() -> tuple[tuple[str,...],...]:
    return tuple(s for s in itertools.permutations(EVENTS)
                 if s.index('A1')<s.index('A2') and s.index('B1')<s.index('B2'))


def record_projector(done: tuple[str,...],records: str) -> np.ndarray:
    validate_records(records)
    p=np.eye(16,dtype=complex)
    for e in done:
        q=EVENTS.index(e); p=p@projector(q,int(records[q]))
    return p


def apply_selected(rho: np.ndarray,k: np.ndarray) -> tuple[np.ndarray,float]:
    rho=np.asarray(rho,complex); k=np.asarray(k,complex)
    if rho.shape!=(16,16) or k.shape!=(16,16) or not np.all(np.isfinite(rho)) or not np.all(np.isfinite(k)):
        raise ValueError('finite 16x16 matrices required')
    if np.linalg.norm(rho-rho.conj().T)>TOL or abs(np.trace(rho)-1)>TOL or np.linalg.eigvalsh(rho).min() < -TOL:
        raise ValueError('normalized positive state required')
    out=k@rho@k.conj().T; weight=float(np.trace(out).real)
    if not weight>0: raise ValueError('supplied outcome has zero probability')
    if weight>1+TOL: raise ValueError('selected map is not trace-nonincreasing on this state')
    return out/weight,weight


@dataclass
class Snapshot:
    done: tuple[str,...]
    rho: np.ndarray
    tau: np.ndarray
    mass: float
    conditional_weight: float
    record_rank: int
    event: str | None=None
    moved: np.ndarray | None=None
    coarse: np.ndarray | None=None
    witness_before: float=0.
    witness_after: float=0.


def run(schedule: tuple[str,...],records: str,*,coupled_control: bool=False) -> list[Snapshot]:
    validate_records(records)
    if not isinstance(schedule,(list,tuple)) or tuple(schedule) not in schedules():
        raise ValueError('execution order must respect supplied A1<A2 and B1<B2 dependencies')
    rho=initial_state(); tau=rho.copy(); done=[]
    frames=[Snapshot((),rho,tau,1.,1.,16)]
    for e in schedule:
        q=EVENTS.index(e); bit=int(records[q]); u=event_unitary(e)
        if coupled_control and e=='B1': u=unitary(tensor_word('XIXI'),.47)@u
        moved=u@rho@u.conj().T
        p0,p1=projector(q,0),projector(q,1)
        coarse=p0@moved@p0+p1@moved@p1
        phase=p0-p1; witness=phase@moved@phase
        reduced_witness=p0@witness@p0+p1@witness@p1
        k=projector(q,bit)@u
        rho,conditional=apply_selected(rho,k)
        tau=k@tau@k.conj().T; mass=float(np.trace(tau).real)
        done.append(e); ideal=tuple(sorted(done))
        frames.append(Snapshot(ideal,rho,tau,mass,conditional,16//(2**len(done)),e,moved,coarse,
                               distance(moved,witness),distance(coarse,reduced_witness)))
    return frames


def commutator_residual(*,coupled_control: bool=False) -> float:
    return max(float(np.linalg.norm(ka@kb-kb@ka))
               for a in ('A1','A2') for b in ('B1','B2') for x in (0,1) for y in (0,1)
               for ka,kb in [(kraus(a,x,coupled_control=coupled_control),kraus(b,y,coupled_control=coupled_control))])


def compare_schedules(records: str,*,coupled_control: bool=False) -> dict:
    seen={}; errors=[]; weights=[]; raw=[]; context={e:[] for e in EVENTS}
    trajectories=[run(s,records,coupled_control=coupled_control) for s in schedules()]
    for frames in trajectories:
        for f in frames:
            if f.event: context[f.event].append(f.conditional_weight)
            if f.done in seen:
                other=seen[f.done]
                errors.append(distance(f.rho,other.rho)); weights.append(abs(f.mass-other.mass))
                raw.append(float(np.linalg.norm(f.tau-other.tau)))
            else: seen[f.done]=f
    return {'ideal_count':len(seen),'max_shared_ideal_state_error':max(errors,default=0.),
            'max_shared_ideal_mass_error':max(weights,default=0.),
            'max_shared_ideal_subnormalized_error':max(raw,default=0.),
            'max_contextual_weight_change':max(max(v)-min(v) for v in context.values()),
            'final_mass_range':max(fs[-1].mass for fs in trajectories)-min(fs[-1].mass for fs in trajectories),
            'final_state_error':max(distance(fs[-1].rho,trajectories[0][-1].rho) for fs in trajectories),
            'contextual_weights':context}


def negative_control() -> dict:
    c=compare_schedules('1001',coupled_control=True)
    return {'classification':'DELIBERATELY_COUPLED_CONTROL_NOT_A_PHYSICAL_ADDITION',
            'cross_commutator':commutator_residual(coupled_control=True),
            'shared_ideal_state_error':c['max_shared_ideal_state_error'],
            'joint_mass_difference':c['final_mass_range'],
            'final_normalized_state_error':c['final_state_error']}


def audit() -> dict:
    rows=[compare_schedules(f'{k:04b}') for k in range(16)]
    norm_error=max(abs(sum(run(s,f'{k:04b}')[-1].mass for k in range(16))-1) for s in schedules())
    return {'version':'v15.13','status':'EXECUTED_CONDITIONAL_PARTIAL_ORDER_DEMONSTRATOR',
            'record_assignments':16,'schedules_per_assignment':6,'runs_checked':96,'ideals_per_assignment':9,
            'max_state_error':max(c['max_shared_ideal_state_error'] for c in rows),
            'max_mass_error':max(c['max_shared_ideal_mass_error'] for c in rows),
            'max_subnormalized_error':max(c['max_shared_ideal_subnormalized_error'] for c in rows),
            'max_contextual_weight_change':max(c['max_contextual_weight_change'] for c in rows),
            'joint_distribution_normalization_error':float(norm_error),
            'cross_stream_kraus_commutator':commutator_residual(),
            'pretime':pretime_control(),'negative_control':negative_control(),
            'physical_duration':None,'new_physical_axioms':[],'source_law_derived':False,
            'entropy_production_derived':False,'Pillar_3':'OPEN','scientific_breakthrough':False,
            'scope':'Carrier, instruments, local dependencies, and actual records supplied; only their computational interleaving is varied.'}


def _snapshot_json(f: Snapshot,records: str) -> dict:
    a=''.join(records[EVENTS.index(e)] for e in ('A1','A2') if e in f.done)
    b=''.join(records[EVENTS.index(e)] for e in ('B1','B2') if e in f.done)
    return {'done':list(f.done),'coordinates':[len(a),len(b)],'records':[a,b],
            'mass':f.mass,'conditional_weight':f.conditional_weight,'record_rank':f.record_rank,
            'event':f.event,'witness_before':f.witness_before,'witness_after':f.witness_after,
            'probabilities':np.diag(f.rho).real.tolist(),
            'rho_real':f.rho.real.tolist(),'rho_imag':f.rho.imag.tolist()}


def build_payload() -> dict:
    branches={}
    for k in range(16):
        r=f'{k:04b}'
        branches[r]=[{'schedule':list(s),'snapshots':[_snapshot_json(f,r) for f in run(s,r)]} for s in schedules()]
    return {'version':'v15.13','default_records':'1001','branches':branches,'audit':audit(),
            'notice':'Playback steps and lattice coordinates are display conventions, not duration, simultaneity or space.'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('outputs'))
    args=parser.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    payload=build_payload(); result=payload['audit']
    if max(result['max_state_error'],result['max_mass_error'],result['cross_stream_kraus_commutator'])>TOL:
        raise SystemExit('confluence verification failed; no positive adjudication')
    (args.out/'replay_data.json').write_text(json.dumps(payload,separators=(',',':'),allow_nan=False)+'\n')
    (args.out/'verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__': main()
