#!/usr/bin/env python3
"""v15.14: supplied record-read dependency, not a physical clock/collapse law."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
from types import MappingProxyType
from typing import Mapping
import numpy as np
from vendor import v1513 as base

ROOT=Path(__file__).resolve().parent
EVENTS=base.EVENTS
READS=MappingProxyType({'A1':(), 'A2':('A1',), 'B1':(), 'B2':('A1','B1')})
VENDOR_BLOB='95d0303d617422d74e61ae017f0354233ec9454b'
TOL=1e-11

class MissingRecord(ValueError):
    """The instrument is unavailable on this realized record prefix."""


def verify_vendor() -> str:
    data=(ROOT/'vendor/v1513.py').read_bytes()
    sha=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if sha!=VENDOR_BLOB: raise ValueError('v15.13 source hash mismatch')
    return sha


def edges() -> tuple[tuple[str,str],...]:
    return tuple((r,e) for e in EVENTS for r in READS[e])


def schedules() -> tuple[tuple[str,...],...]:
    return tuple(s for s in itertools.permutations(EVENTS)
                 if all(s.index(a)<s.index(b) for a,b in edges()))


def _frozen(a: np.ndarray) -> np.ndarray:
    # bytes-backed arrays prevent callers from re-enabling WRITEABLE.
    out=np.frombuffer(np.asarray(a,dtype=complex).tobytes(),dtype=complex).reshape(16,16)
    return out


@dataclass(frozen=True)
class Snapshot:
    records: tuple[tuple[str,int],...]
    rho: np.ndarray
    tau: np.ndarray
    mass: float
    conditional_weight: float
    event: str | None=None
    control_bit: int | None=None

    @property
    def done(self) -> tuple[str,...]:
        return tuple(e for e,_ in self.records)


def start() -> Snapshot:
    verify_vendor(); r=base.initial_state()
    return Snapshot((),_frozen(r),_frozen(r),1.,1.)


def missing(frame: Snapshot,event: str) -> tuple[str,...]:
    if event not in EVENTS: raise ValueError('undeclared event')
    return tuple(e for e in READS[event] if e not in frame.done)


def enabled(frame: Snapshot) -> tuple[str,...]:
    return tuple(e for e in EVENTS if e not in frame.done and not missing(frame,e))


def instrument(event: str, realized_reads: Mapping[str,int]) -> np.ndarray:
    """Only declared ALREADY REALIZED record values enter this resolver.

    B2's extra rotation is a supplied finite operation on the second B qubit:
    exp(-i s(a) Y_B2), s(0)=+0.6, s(1)=-0.6. It is not a fitted dynamics law.
    The actual B2 outcome is not an argument to the instrument resolver.
    """
    if event not in EVENTS: raise ValueError('undeclared event')
    if not isinstance(realized_reads,Mapping): raise ValueError('realized read mapping required')
    absent=set(READS[event])-set(realized_reads)
    if absent: raise MissingRecord(f'{event} requires realized records: {", ".join(sorted(absent))}')
    if set(realized_reads)!=set(READS[event]):
        raise ValueError('only declared realized read keys may be supplied')
    if any(type(v) is not int or v not in (0,1) for v in realized_reads.values()):
        raise ValueError('binary integer record values required')
    u=base.event_unitary(event)
    if event=='B2':
        extent=.6 if realized_reads['A1']==0 else -.6
        u=base.unitary(base.tensor_word('IIIY'),extent)@u
    return u


def advance(frame: Snapshot,event: str,outcome: int) -> Snapshot:
    if type(outcome) is not int or outcome not in (0,1): raise ValueError('supply the actual binary record')
    if event not in EVENTS: raise ValueError('undeclared event')
    if event in frame.done: raise ValueError('an actual record cannot be overwritten or repeated')
    if missing(frame,event):
        raise MissingRecord(f'{event} blocked: missing {", ".join(missing(frame,event))}')
    record=dict(frame.records)
    reads={e:record[e] for e in READS[event]}
    u=instrument(event,reads)
    k=base.projector(EVENTS.index(event),outcome)@u
    rho,conditional=base.apply_selected(frame.rho,k)
    tau=k@frame.tau@k.conj().T; mass=float(np.trace(tau).real)
    record[event]=outcome
    pairs=tuple((e,record[e]) for e in EVENTS if e in record)
    p=np.eye(16,dtype=complex)
    for e,b in pairs: p=p@base.projector(EVENTS.index(e),b)
    if np.linalg.norm(p@rho@p-rho)>TOL or abs(np.trace(rho)-1)>TOL or np.linalg.eigvalsh(rho).min() < -TOL:
        raise ArithmeticError('state or retained-record invariant failed')
    return Snapshot(pairs,_frozen(rho),_frozen(tau),mass,conditional,event,reads.get('A1') if event=='B2' else None)


def run(schedule: tuple[str,...],actual_records: str) -> tuple[Snapshot,...]:
    base.validate_records(actual_records)
    if not isinstance(schedule,(list,tuple)) or len(schedule)!=4 or set(schedule)!=set(EVENTS):
        raise ValueError('each of the four declared events must appear exactly once')
    f=start(); frames=[f]
    for event in schedule:
        # advance first tests realized availability; the complete script never
        # reaches the instrument resolver or readiness functions.
        f=advance(f,event,int(actual_records[EVENTS.index(event)])); frames.append(f)
    return tuple(frames)


def control_channel_distance() -> float:
    # Distinguish full labeled instrument channels, not merely Kraus phases.
    choi=[]
    for a in (0,1):
        u=instrument('B2',{'A1':a,'B1':0})
        blocks=[]
        for b in (0,1):
            k=base.projector(3,b)@u; v=k.reshape(-1,order='F')
            blocks.append(np.outer(v,v.conj()))
        choi.append(blocks)
    return float(np.sqrt(sum(np.linalg.norm(x-y)**2 for x,y in zip(*choi))))


def _unsafe_guess_run(records: str,guess: int) -> tuple[np.ndarray,float]:
    """Explicitly rejected bypass: use guessed A1 before A1 is realized."""
    rho=base.initial_state(); tau=rho.copy()
    for event in ('B1','B2','A1','A2'):
        # This deliberately violates the record-availability interface.
        u=instrument('B2',{'A1':guess,'B1':int(records[2])}) if event=='B2' else base.event_unitary(event)
        k=base.projector(EVENTS.index(event),int(records[EVENTS.index(event)]))@u
        rho,_=base.apply_selected(rho,k); tau=k@tau@k.conj().T
    return rho,float(np.trace(tau).real)


def guess_controls() -> list[dict]:
    rows=[]
    for guess in (0,1):
        errors=[]; distances=[]; guessed_mass=[]
        for k in range(16):
            records=f'{k:04b}'; correct=run(schedules()[0],records)[-1]
            wrong,weight=_unsafe_guess_run(records,guess)
            errors.append(abs(weight-correct.mass)); distances.append(base.distance(wrong,correct.rho)); guessed_mass.append(weight)
        rows.append({'status':'REJECTED_RECORD_GUESS_CONTROL','guessed_A1':guess,
                     'max_joint_mass_error':max(errors),'total_variation':float(sum(errors)/2),
                     'max_final_state_distance':max(distances),
                     'guessed_distribution_normalization_error':abs(sum(guessed_mass)-1)})
    return rows


def collect() -> dict[str,list[tuple[Snapshot,...]]]:
    return {f'{k:04b}':[run(s,f'{k:04b}') for s in schedules()] for k in range(16)}


def audit() -> dict:
    data=collect(); state=mass=raw=persist=traceerr=0.; mineig=1.; ideals=set()
    for runs in data.values():
        seen={}
        for frames in runs:
            for f in frames:
                ideals.add(f.done)
                traceerr=max(traceerr,float(abs(np.trace(f.rho)-1)))
                mineig=min(mineig,float(np.linalg.eigvalsh(f.rho).min()))
                if f.done in seen:
                    g=seen[f.done]
                    state=max(state,base.distance(f.rho,g.rho)); mass=max(mass,abs(f.mass-g.mass))
                    raw=max(raw,float(np.linalg.norm(f.tau-g.tau)))
                else: seen[f.done]=f
    norm=max(abs(sum(runs[i][-1].mass for runs in data.values())-1) for i in range(len(schedules())))
    # Permissible incomparable pairs must commute at each shared controller value.
    comm=0.
    incomparable=[('A1','B1'),('A2','B1'),('A2','B2')]
    for controller in (0,1):
        for a,b in incomparable:
            ua=instrument(a,{e:controller for e in READS[a]}); ub=instrument(b,{e:controller for e in READS[b]})
            for x,y in itertools.product((0,1),repeat=2):
                ka=base.projector(EVENTS.index(a),x)@ua; kb=base.projector(EVENTS.index(b),y)@ub
                comm=max(comm,float(np.linalg.norm(ka@kb-kb@ka)))
    rejected=0
    for s in itertools.permutations(EVENTS):
        try: run(s,'1001')
        except MissingRecord: rejected+=1
    result={'version':'v15.14','status':'EXECUTED_CONDITIONAL_RECORD_DEPENDENT_DEMONSTRATOR',
            'record_rule_status':'SUPPLIED_ILLUSTRATIVE_FEED_FORWARD','extra_record_read':['A1','B2'],
            'local_schedules_before_read':6,'valid_schedules_after_read':len(schedules()),
            'record_assignments':16,'runs_checked':sum(len(r) for r in data.values()),'ideals_per_assignment':len(ideals),
            'premature_permutations_rejected':rejected,'max_state_distance':state,'max_mass_error':mass,
            'max_subnormalized_error':raw,'max_trace_error':traceerr,'min_state_eigenvalue':mineig,
            'joint_distribution_normalization_error':float(norm),'max_incomparable_commutator':comm,
            'control_channel_choi_distance':control_channel_distance(),'guessed_record_controls':guess_controls(),
            'pretime_control':base.pretime_control(),'physical_duration':None,
            'physical_causality_derived':False,'physical_entropy_law_derived':False,'collapse_outcome_derived':False,
            'new_physical_axioms':[],'Pillar_3':'OPEN','scientific_breakthrough':False,
            'vendor_git_blob':verify_vendor(),
            'scope':'The record wire, finite controller values, carrier, RAS and RCR remain supplied. Readiness follows that declaration, not an externally imposed clock.'}
    if max(state,mass,raw,traceerr,norm,comm)>TOL or mineig < -TOL or rejected!=19:
        raise ArithmeticError('verification failed; no positive adjudication')
    return result


def snapshot_json(f: Snapshot) -> dict:
    return {'done':list(f.done),'records':dict(f.records),'enabled':list(enabled(f)),
            'blocked':{e:list(missing(f,e)) for e in EVENTS if e not in f.done and missing(f,e)},
            'mass':f.mass,'conditional_weight':f.conditional_weight,'event':f.event,'control_bit':f.control_bit,
            'record_rank':16//2**len(f.done),'probabilities':np.diag(f.rho).real.tolist(),
            'rho_real':f.rho.real.tolist(),'rho_imag':f.rho.imag.tolist()}


def payload() -> dict:
    return {'version':'v15.14','default_records':'1001','edges':[list(e) for e in edges()],
            'schedules':[list(s) for s in schedules()],
            'branches':{r:[{'snapshots':[snapshot_json(f) for f in fs]} for fs in runs] for r,runs in collect().items()},
            'audit':audit(),'display_warning':'Playback is not physical time. Dependencies and actual outcomes are supplied inputs.'}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out',type=Path,default=ROOT/'outputs')
    a=p.parse_args(); data=payload(); a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'replay_data.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n')
    (a.out/'verification.json').write_text(json.dumps(data['audit'],indent=2,allow_nan=False)+'\n')
    print(json.dumps(data['audit'],indent=2,allow_nan=False))

if __name__=='__main__': main()
