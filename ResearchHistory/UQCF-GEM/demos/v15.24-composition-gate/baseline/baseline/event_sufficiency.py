#!/usr/bin/env python3
"""v15.22: exact event-specific retention versus a common ready-event channel.

The instruments and next-event schedules are supplied. No physical pruning law,
clock, entropy objective, or actual-outcome selector is inferred from sufficiency.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import adaptive as prior
TOL=1e-10
HASHES={'adaptive.py':'44a87e4cc5bcf531ef7798aadab5d9dbba3482cb',
        'vendor/v1513.py':'95d0303d617422d74e61ae017f0354233ec9454b',
        'vendor/__init__.py':'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'}


def verify_baseline() -> dict:
    for name,expected in HASHES.items():
        data=(ROOT/'baseline'/name).read_bytes()
        actual=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        if actual!=expected:raise ValueError('frozen source differs: '+name)
    return dict(HASHES)


def context_key(frame) -> str:
    return '|'.join(f'{e}={b}' for e,b in frame.records) or 'ROOT'


@lru_cache(None)
def contexts() -> dict:
    verify_baseline();result={}
    for schedule in prior.schedules():
        for r in range(16):
            for f in prior.run(schedule,f'{r:04b}'):
                key=context_key(f)
                if key in result:
                    if prior.base.distance(f.rho,result[key].rho)>TOL or abs(f.mass-result[key].mass)>TOL:
                        raise ArithmeticError('same realized context has inconsistent state')
                else:result[key]=f
    return result


def sector(frame) -> np.ndarray:
    """Isometry for the already-realized computational record sector."""
    inds=[r for r in range(16) if all(int(f'{r:04b}'[prior.EVENTS.index(e)])==b for e,b in frame.records)]
    if not inds:raise ValueError('empty realized record sector')
    return np.eye(16,dtype=complex)[:,inds]


def kraus(frame,event: str) -> tuple[np.ndarray,np.ndarray]:
    if event not in prior.enabled(frame):raise ValueError('event is not ready or is already realized')
    reads={e:dict(frame.records)[e] for e in prior.READS[event]}
    u=prior.instrument(event,reads);w=sector(frame)
    if np.linalg.norm((np.eye(16)-w@w.conj().T)@u@w)>TOL:
        raise ArithmeticError('supplied operation leaves the previous record sector')
    return tuple(w.conj().T@prior.base.projector(prior.EVENTS.index(event),b)@u@w for b in (0,1))


def effects(frame,event: str) -> tuple[np.ndarray,np.ndarray]:
    return tuple(k.conj().T@k for k in kraus(frame,event))


def retain(a: np.ndarray,ps) -> np.ndarray:
    a=np.asarray(a,complex);ps=tuple(np.asarray(p,complex) for p in ps)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or not np.isfinite(a).all() or not ps:
        raise ValueError('finite square operator and complete projectors required')
    if any(p.shape!=a.shape or not np.isfinite(p).all() for p in ps):raise ValueError('projector shape or finiteness')
    if any(np.linalg.norm(p-p.conj().T)>TOL or np.linalg.norm(p@p-p)>TOL for p in ps):raise ValueError('orthogonal projections required')
    if np.linalg.norm(sum(ps)-np.eye(len(a)))>TOL or any(np.linalg.norm(p@q)>TOL for i,p in enumerate(ps) for q in ps[i+1:]):
        raise ValueError('projectors must resolve identity without overlap')
    return sum((p@a@p for p in ps),np.zeros_like(a))


def choi(operators) -> np.ndarray:
    """Normalized input Choi; used to check the complete branch map."""
    operators=tuple(np.asarray(k,complex) for k in operators)
    if not operators or any(k.ndim!=2 or k.shape!=operators[0].shape or not np.isfinite(k).all() for k in operators):
        raise ValueError('finite equal-shaped nonempty Kraus operators required')
    d=operators[0].shape[1]
    return sum((np.outer(k.reshape(-1,order='F'),k.reshape(-1,order='F').conj())/d for k in operators))


def preprocess_frame(frame,event: str):
    """An alternative factorization of a specified event, not another actual event."""
    w=sector(frame);ps=effects(frame,event)
    rho=w@retain(w.conj().T@frame.rho@w,ps)@w.conj().T
    tau=w@retain(w.conj().T@frame.tau@w,ps)@w.conj().T
    return replace(frame,rho=prior._frozen(rho),tau=prior._frozen(tau))


def single_event_dimension(d: int) -> int:
    if type(d) is not int or d<2 or d%2:raise ValueError('positive even current-sector dimension required')
    return d*d//2


def joint_basis(frame):
    ready=prior.enabled(frame)
    if len(ready)!=2:raise ValueError('two ready events required')
    pa,pb=(effects(frame,e) for e in ready)
    d=pa[0].shape[0];vectors=[];labels=[];ranks=[]
    for a in (0,1):
        for b in (0,1):
            q=pa[a]@pb[b]
            if np.linalg.norm(q-q.conj().T)>TOL or np.linalg.norm(q@q-q)>TOL:
                raise ArithmeticError('ready effects do not form commuting projectors')
            vals,vecs=np.linalg.eigh((q+q.conj().T)/2)
            if np.max(np.minimum(abs(vals),abs(vals-1)))>TOL:raise ArithmeticError('unresolved joint projector')
            v=vecs[:,vals>.5];ranks.append(v.shape[1])
            vectors.extend(v.T);labels.extend([(a,b)]*v.shape[1])
    v=np.column_stack(vectors)
    if ranks!=[d//4]*4 or np.linalg.norm(v.conj().T@v-np.eye(d))>TOL:
        raise ArithmeticError('incomplete four-sector decomposition')
    return v,labels,ranks


def joint_certificate(frame) -> dict:
    ready=prior.enabled(frame);v,labels,ranks=joint_basis(frame);d=len(v)
    pa,pb=(effects(frame,e) for e in ready);error=0.
    # Within-A and within-B matrix units multiply to every current-sector unit.
    for i in range(d):
        for j in range(d):
            k=labels.index((labels[i][0],labels[j][1]))
            a=np.outer(v[:,i],v[:,k].conj());b=np.outer(v[:,k],v[:,j].conj())
            unit=np.outer(v[:,i],v[:,j].conj())
            error=max(error,float(np.linalg.norm(retain(a,pa)-a)),float(np.linalg.norm(retain(b,pb)-b)),float(np.linalg.norm(a@b-unit)))
    # A joint preprocessing is safe for a batch that actually executes BOTH,
    # not for either intermediate single-event output at the open frontier.
    batch_error=0.
    for ka in kraus(frame,ready[0]):
        for kb in kraus(frame,ready[1]):
            k=kb@ka;composed=[k@p@q for p in pa for q in pb]
            batch_error=max(batch_error,float(np.linalg.norm(choi(composed)-choi([k]))))
    return {'joint_ranks':ranks,'full_algebra_dimension':d*d,'matrix_units_checked':d*d,
            'max_multiplication_error':error,'two_event_batch_choi_error':batch_error,
            'common_preprocessor':'IDENTITY_ON_CURRENT_SECTOR'}


def integration_control() -> dict:
    se=me=ce=0.;steps=histories=0
    for schedule in prior.schedules():
        for r in range(16):
            reference=prior.run(schedule,f'{r:04b}');f=prior.start()
            for i,event in enumerate(schedule,1):
                before=f;f=preprocess_frame(f,event)
                if f.records!=before.records:raise ArithmeticError('preprocessing selected actuality')
                f=prior.advance(f,event,int(f'{r:04b}'[prior.EVENTS.index(event)]));g=reference[i]
                se=max(se,prior.base.distance(f.rho,g.rho));me=max(me,abs(f.mass-g.mass))
                ce=max(ce,abs(f.conditional_weight-g.conditional_weight));steps+=1
            histories+=1
    return {'histories':histories,'branch_steps':steps,'max_state_distance':se,
            'max_joint_mass_error':me,'max_conditional_error':ce,
            'scope':'Each event type and outcome remain supplied; only the factorization before that specified event changes.'}


def root_control() -> dict:
    f=prior.start();ready=prior.enabled(f);v,labels,_=joint_basis(f)
    x=v[:,labels.index((0,0))];y=v[:,labels.index((1,0))]
    plus=(x+y)/np.sqrt(2);minus=(x-y)/np.sqrt(2)
    rho=np.outer(plus,plus.conj());other=np.outer(minus,minus.conj())
    pa=effects(f,ready[0]);kb=kraus(f,ready[1])[0]
    native=kb@rho@kb.conj().T;wrong=kb@retain(rho,pa)@kb.conj().T
    native_other=kb@other@kb.conj().T;wrong_other=kb@retain(other,pa)@kb.conj().T
    chosen=next(k for k in kraus(f,ready[0]))
    return {'chosen_event':ready[0],'other_ready_event':ready[1],
            'matching_event_choi_error':float(np.linalg.norm(choi([chosen@p for p in pa])-choi([chosen]))),
            'event_map_parity_norm':float(np.linalg.norm(retain(prior.base.tensor_word('YYYY'),pa))),
            'wrong_event_probability_error':float(abs(np.trace(native)-np.trace(wrong))),
            'wrong_event_output_state_distance':prior.base.distance(native/np.trace(native),wrong/np.trace(wrong)),
            'unpruned_other_event_pair_distance':prior.base.distance(native,native_other),
            'prepruned_other_event_pair_distance':prior.base.distance(wrong,wrong_other),
            'input_state_real':rho.real.tolist(),'input_state_imag':rho.imag.tolist(),
            'interpretation':'The other event has the same probability but a different quantum output. Requiring the entire instrument is stronger than requiring its probabilities.'}


def verify_result(r: dict) -> None:
    needed={'version','status','contexts','nonterminal_contexts','terminal_contexts','single_ready_contexts','two_ready_contexts',
        'event_context_pairs','branch_maps_checked','matrix_unit_certificates','max_event_choi_error',
        'max_factorization_error','max_multiplication_certificate_error','max_two_event_batch_choi_error',
        'integration','root_control','common_preprocessor_at_two_ready','event_specific_rule_status',
        'cases','actual_record_selected','physical_duration','new_physical_axioms','physical_pruning_law_derived',
        'new_motion_law_derived','Pillar_3','scientific_breakthrough'}
    if set(r)!=needed:raise AssertionError('audit schema mismatch')
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(int,float)) and not isinstance(x,bool) and not np.isfinite(x):raise AssertionError('nonfinite result')
    finite(r)
    for k,n in [('contexts',45),('nonterminal_contexts',29),('terminal_contexts',16),('single_ready_contexts',22),
                ('two_ready_contexts',7),('event_context_pairs',36),('branch_maps_checked',72),('matrix_unit_certificates',448)]:
        if r[k]!=n:raise AssertionError('coverage: '+k)
    for k in ('max_event_choi_error','max_factorization_error','max_multiplication_certificate_error','max_two_event_batch_choi_error'):
        if not 0<=r[k]<TOL:raise AssertionError(k)
    if r['integration']['histories']!=80 or r['integration']['branch_steps']!=320:raise AssertionError('integration coverage')
    for k in ('max_state_distance','max_joint_mass_error','max_conditional_error'):
        if not 0<=r['integration'][k]<TOL:raise AssertionError(k)
    c=r['root_control']
    if c['wrong_event_probability_error']>TOL or abs(c['wrong_event_output_state_distance']-.5)>TOL:
        raise AssertionError('negative-control probability/state distinction')
    if abs(c['unpruned_other_event_pair_distance']-1)>TOL or c['prepruned_other_event_pair_distance']>TOL:
        raise AssertionError('distinguishability collision')
    if r['actual_record_selected'] is not None or r['physical_duration'] is not None or r['new_physical_axioms']!=[]:
        raise AssertionError('ontology boundary')
    if r['physical_pruning_law_derived'] is not False or r['new_motion_law_derived'] is not False:
        raise AssertionError('unsupported physical claim')


@lru_cache(None)
def audit() -> dict:
    rows=[];ce=fe=mu=be=0.;options=branches=units=0;single=two=terminal=0
    for key,f in contexts().items():
        ready=prior.enabled(f);d=sector(f).shape[1]
        if not ready:terminal+=1;continue
        row={'context':key,'records':dict(f.records),'ready':list(ready),'current_dimension':d,
             'fixed_next_event_algebra_dimension':single_event_dimension(d),'event_maps':[]}
        for e in ready:
            ks=kraus(f,e);ps=effects(f,e);local=0.
            for b,k in enumerate(ks):
                for c,p in enumerate(ps):fe=max(fe,float(np.linalg.norm(k@p-(k if b==c else np.zeros_like(k)))))
                local=max(local,float(np.linalg.norm(choi([k@p for p in ps])-choi([k]))));branches+=1
            ce=max(ce,local);options+=1
            row['event_maps'].append({'event':e,'complete_branch_choi_error':local})
        if len(ready)==2:
            cert=joint_certificate(f);row['common_channel']=cert;two+=1
            units+=cert['matrix_units_checked'];mu=max(mu,cert['max_multiplication_error']);be=max(be,cert['two_event_batch_choi_error'])
        else:
            single+=1;row['common_channel']={'common_preprocessor':'EVENT_SPECIFIC_CONDITIONAL_EXPECTATION',
                                           'sufficient_algebra_dimension':single_event_dimension(d)}
        rows.append(row)
    result={'version':'v15.22','status':'FIXED_EVENT_RETENTION_SUFFICIENT_OPEN_FRONTIER_REQUIRES_IDENTITY',
        'contexts':len(contexts()),'nonterminal_contexts':len(rows),'terminal_contexts':terminal,
        'single_ready_contexts':single,'two_ready_contexts':two,'event_context_pairs':options,
        'branch_maps_checked':branches,'matrix_unit_certificates':units,
        'max_event_choi_error':ce,'max_factorization_error':fe,'max_multiplication_certificate_error':mu,
        'max_two_event_batch_choi_error':be,'integration':integration_control(),'root_control':root_control(),
        'common_preprocessor_at_two_ready':'IDENTITY_ON_CURRENT_SECTOR',
        'event_specific_rule_status':'DERIVED_FROM_SUPPLIED_NEXT_INSTRUMENT_NOT_SELECTED_PHYSICS',
        'cases':rows,'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
        'physical_pruning_law_derived':False,'new_motion_law_derived':False,'Pillar_3':'OPEN','scientific_breakthrough':False}
    verify_result(result);return result


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    a=p.parse_args();result=audit();a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','root_control')},indent=2,allow_nan=False))

if __name__=='__main__':main()
