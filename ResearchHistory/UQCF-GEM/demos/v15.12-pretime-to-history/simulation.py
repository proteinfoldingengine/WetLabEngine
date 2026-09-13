#!/usr/bin/env python3
"""v15.12 integrated conditional demonstrator. Display cadence is not a clock."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import numpy as np
from vendor.ontology_continuity_audit import pinch, select_record, trace_distance

ROOT=Path(__file__).resolve().parent
VENDOR_BLOB='8871e50f19322adbb62f34ea3837ba8e6cb16c8b'
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.diag([1.,-1.]).astype(complex)
TOL=1e-11


def verify_vendor() -> str:
    data=(ROOT/'vendor/ontology_continuity_audit.py').read_bytes()
    actual=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if actual!=VENDOR_BLOB:
        raise ValueError('v15.11 dependency differs from the frozen source')
    return actual


def kron(*ops: np.ndarray) -> np.ndarray:
    out=np.ones((1,1),complex)
    for op in ops: out=np.kron(out,op)
    return out


def initial_state() -> np.ndarray:
    """Supplied coherent reference |+++>; not identified with Genesis or vacuum."""
    v=np.ones(8,complex)/math.sqrt(8)
    return np.outer(v,v.conj())


def motion_generator(retained_bits: int) -> np.ndarray:
    """Declared illustrative Hermitian generators; no fitted force law."""
    if retained_bits==0:
        return .8*kron(Y,I,I)+.55*kron(Z,X,I)+.37*kron(I,Y,X)+.25*kron(X,I,Z)
    if retained_bits==1:
        return .9*kron(I,Y,I)+.4*kron(I,Z,X)+.35*kron(Z,X,Z)
    if retained_bits==2:
        return .9*kron(I,I,Y)+.3*kron(Z,I,X)+.25*kron(I,Z,Z)
    raise ValueError('only the three declared motion stages exist')


def unitary(generator: np.ndarray, extent: float) -> np.ndarray:
    """Finite transformation U(extent)=exp(-i extent G); extent is dimensionless."""
    generator=np.asarray(generator,complex)
    if not np.isfinite(extent) or generator.ndim!=2 or generator.shape[0]!=generator.shape[1]:
        raise ValueError('finite extent and square Hermitian generator required')
    if not np.all(np.isfinite(generator)) or np.linalg.norm(generator-generator.conj().T)>TOL:
        raise ValueError('finite Hermitian generator required')
    vals,vecs=np.linalg.eigh(generator)
    return (vecs*np.exp(-1j*extent*vals))@vecs.conj().T


def prefix_projector(prefix: str) -> np.ndarray:
    if not isinstance(prefix,str) or len(prefix)>3 or any(c not in '01' for c in prefix):
        raise ValueError('a prefix of at most three binary records is required')
    return np.diag([float(f'{k:03b}'.startswith(prefix)) for k in range(8)]).astype(complex)


def prefix_projectors(level: int) -> list[np.ndarray]:
    if type(level) is not int or not 0<=level<=3:
        raise ValueError('algebra level must be an integer from 0 through 3')
    return [np.eye(8,dtype=complex)] if level==0 else [prefix_projector(f'{k:0{level}b}') for k in range(2**level)]


def _validate(s: dict[str,Any],cadence: int) -> None:
    required={'schema_version','name','qubits','actual_records','record_semantics',
              'retained_algebra_semantics','pretime_extent','inter_record_extents',
              'motion_semantics','physical_duration','new_physical_axioms'}
    if not isinstance(s,dict) or set(s)!=required: raise ValueError('scenario keys must match the declared schema')
    if s['schema_version']!=1 or s['qubits']!=3: raise ValueError('this demonstrator has three supplied qubits')
    if s['physical_duration'] is not None: raise ValueError('no physical-duration input is admitted')
    if s['new_physical_axioms']!=[]: raise ValueError('no new physical axiom is adopted by this demo')
    records=s['actual_records']
    if not isinstance(records,list) or len(records)!=3 or any(type(r) is not int or r not in (0,1) for r in records):
        raise ValueError('three explicit binary RCR records are required; none will be chosen automatically')
    if not isinstance(s['inter_record_extents'],list) or len(s['inter_record_extents'])!=2:
        raise ValueError('two explicit inter-record extents are required')
    for extent in [s['pretime_extent'],*s['inter_record_extents']]:
        if type(extent) not in (int,float) or not math.isfinite(extent): raise ValueError('finite numerical extents are required')
    if type(cadence) is not int or cadence<2: raise ValueError('display cadence must be an integer >= 2')
    expected={
        'record_semantics':'EXPLICIT_ILLUSTRATIVE_RCR_INPUT_NOT_A_DERIVED_CHOICE',
        'retained_algebra_semantics':'SUPPLIED_COMPUTATIONAL_PREFIX_ALGEBRAS_NOT_A_DERIVED_SELECTOR',
        'motion_semantics':'ILLUSTRATIVE_REVERSIBLE_TRANSFORMATIONS_NOT_A_GRAVITY_LAW'}
    if any(s[k]!=v for k,v in expected.items()): raise ValueError('scenario may not relabel supplied inputs as derived laws')


@dataclass
class Frame:
    rho: np.ndarray
    phase: str
    label: str
    message: str
    record: str
    ordinal: int
    event_number: int
    algebra_level: int
    extent: float | None


@dataclass
class Trace:
    frames: list[Frame]
    events: list[dict[str,Any]]
    checks: dict[str,float]
    records: list[int]

    def summary(self) -> dict[str,Any]:
        return {'version':'v15.12','status':'EXECUTED_CONDITIONAL_DEMONSTRATOR',
                'supplied_records':self.records,'final_record':''.join(map(str,self.records)),
                'record_rank_chain':[8]+[e['record_rank'] for e in self.events],
                'events':self.events,'checks':self.checks,'physical_duration':None,
                'new_physical_axioms':[], 'physical_entropy_law_derived':False,
                'gravity_derived':False,'Pillar_3':'OPEN',
                'vendor_git_blob':VENDOR_BLOB,
                'claim':'An executed finite model conditional on a supplied carrier, reversible transforms, RAS, RCR and record-compatible refinement. No physical collapse selector or clock is derived.'}


def build_demo(scenario: dict[str,Any],cadence: int=20) -> Trace:
    _validate(scenario,cadence); verify_vendor()
    frames: list[Frame]=[]; events=[]
    reference=initial_state(); g0=motion_generator(0)
    record=''
    def append(rho,phase,label,message,level,extent=None,event=0,prefix=None):
        p=record if prefix is None else prefix
        frames.append(Frame(rho.copy(),phase,label,message,p,len(p),event,level,extent))
    def move(start,generator,extents,phase,label,message,level):
        last=start
        for extent in extents:
            u=unitary(generator,float(extent)); last=u@start@u.conj().T
            append(last,phase,label,message,level,float(extent))
        return last
    def hold(rho,phase,label,message,level,event,units):
        for _ in range(units*cadence): append(rho,phase,label,message,level,event=event)

    move(reference,g0,np.linspace(0,1.35,5*cadence),'pretime_forward',
         'PRE-TIME  /  REVERSIBLE CHANGE','Configurations change; no actual record is selected.',0)
    reverse=move(reference,g0,np.linspace(1.35,0,3*cadence),'pretime_reverse',
                 'PRE-TIME  /  RETURN ALONG THE INVERSE','The original coherent state is recovered. No temporal arrow is assigned.',0)
    current=move(reference,g0,np.linspace(0,scenario['pretime_extent'],3*cadence),'pretime_approach',
                 'PRE-TIME  /  APPROACH THE DECLARED EVENT','The upcoming algebra and actual record are scenario inputs, not predictions.',0)
    u=unitary(g0,1.35)
    inverse_error=float(np.linalg.norm(u.conj().T@(u@reference@u.conj().T)@u-reference))
    inverse_error=max(inverse_error,float(np.linalg.norm(reverse-reference)))

    for level,bit in enumerate(scenario['actual_records'],1):
        before=current.copy(); old_record=record; parent=prefix_projector(record)
        ps=prefix_projectors(level); previous_ps=prefix_projectors(level-1)
        coarse=pinch(before,ps)
        phase_ops=[I,I,I]; phase_ops[level-1]=Z
        phase_flip=kron(*phase_ops); partner=phase_flip@before@phase_flip.conj().T
        coarse_partner=pinch(partner,ps)
        weights=[float(np.trace(prefix_projector(record+str(b))@coarse).real) for b in (0,1)]
        record_index=int(record+str(bit),2)
        selected=select_record(before,ps,record_index)
        selected_partner=select_record(partner,ps,record_index)
        # Retain the classical outcome flag explicitly; it cannot recover erased phase.
        flag=lambda r: sum((np.kron(p@r@p,np.diag(np.eye(len(ps))[k])) for k,p in enumerate(ps)),np.zeros((8*len(ps),8*len(ps)),complex))
        new_record=record+str(bit); child=prefix_projector(new_record)
        event={
            'ordinal':level,'chosen_record':bit,'record_prefix':new_record,'parent_record':old_record,
            'selection_origin':'SUPPLIED_RCR','algebra_origin':'SUPPLIED_RAS',
            'record_rank':int(round(float(np.trace(child).real))),
            'algebra_dimension':sum(int(round(float(np.trace(p).real)))**2 for p in ps),
            'record_inclusion_error':float(np.linalg.norm(parent@child-child)),
            'nested_expectation_error':float(np.linalg.norm(pinch(pinch(reference,previous_ps),ps)-pinch(reference,ps))),
            'conditional_weights':weights,'chosen_conditional_weight':weights[bit],
            'idempotence_error':float(np.linalg.norm(pinch(coarse,ps)-coarse)),
            'witness_before':trace_distance(before,partner),
            'witness_after_ras':trace_distance(coarse,coarse_partner),
            'witness_with_classical_record':trace_distance(flag(before),flag(partner)),
            'witness_after_selected_record':trace_distance(selected,selected_partner),
            'event_semantics':'RAS and RCR exposed separately for inspection; no physical duration between views'}
        events.append(event)
        hold(coarse,f'ras_{level}',f'SUPPLIED RAS {level}  /  RETAINED DISTINCTIONS',
             'Cross-sector coherence is removed; actuality has not been selected by this map.',level,level,2)
        record=new_record
        hold(selected,f'rcr_{level}',f'SUPPLIED RCR {level}  /  ACTUAL RECORD {new_record}',
             'This actual record is explicitly provided. Its compatible descendants remain available.',level,level,3)
        current=selected
        if level<3:
            current=move(current,motion_generator(level),np.linspace(0,scenario['inter_record_extents'][level-1],4*cadence),
                         f'retained_motion_{level}',f'REVERSIBLE CHANGE  /  RECORD {record} PRESERVED',
                         'Motion continues inside the retained sector without adding a new record.',level)
    hold(current,'retained_history','RETAINED HISTORY  /  ORDINAL ORDER',
         'A compatible record chain is realized conditionally. No elapsed physical duration is derived.',3,3,3)
    checks={
        'pretime_reversal_error':inverse_error,
        'pretime_max_distance':max(trace_distance(f.rho,reference) for f in frames if f.phase.startswith('pretime')),
        'retained_record_motion_error':max(float(np.linalg.norm(prefix_projector(f.record)@f.rho@prefix_projector(f.record)-f.rho)) for f in frames),
        'maximum_trace_error':max(float(abs(np.trace(f.rho)-1)) for f in frames),
        'minimum_state_eigenvalue':min(float(np.linalg.eigvalsh((f.rho+f.rho.conj().T)/2).min()) for f in frames)}
    if checks['maximum_trace_error']>TOL or checks['minimum_state_eigenvalue'] < -TOL or checks['retained_record_motion_error']>TOL:
        raise ArithmeticError('integrated state-validity or retained-record invariant failed')
    return Trace(frames,events,checks,list(scenario['actual_records']))


def save_trace(trace: Trace,out: Path) -> None:
    out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(trace.summary(),indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(out/'states.npz',rho=np.stack([f.rho for f in trace.frames]),
                        phase=np.array([f.phase for f in trace.frames]),record=np.array([f.record for f in trace.frames]),
                        ordinal=np.array([f.ordinal for f in trace.frames]))
    view=[{'phase':f.phase,'label':f.label,'message':f.message,'record':f.record,'ordinal':f.ordinal,
           'event_number':f.event_number,'algebra_level':f.algebra_level,'extent':f.extent} for f in trace.frames]
    (out/'display_frames.json').write_text(json.dumps(view,indent=2,allow_nan=False)+'\n')


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',type=Path,default=ROOT/'scenario.json')
    parser.add_argument('--records',help='explicit three-bit RCR sequence; overrides the declared scenario')
    parser.add_argument('--cadence',type=int,default=20,help='display samples only; not a physical clock')
    parser.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=parser.parse_args()
    scenario=json.loads(args.scenario.read_text())
    if args.records is not None:
        if len(args.records)!=3 or any(c not in '01' for c in args.records): parser.error('--records requires three binary digits')
        scenario['actual_records']=[int(c) for c in args.records]
    trace=build_demo(scenario,args.cadence); save_trace(trace,args.out)
    print(json.dumps(trace.summary(),indent=2,allow_nan=False))

if __name__=='__main__': main()
