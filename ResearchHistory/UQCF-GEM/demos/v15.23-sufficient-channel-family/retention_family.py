#!/usr/bin/env python3
"""Classify all exact preprocessors of the supplied sharp event instruments.

Coefficient choices are diagnostic inputs, not a retention selector or time law.
The finite proof is in README; finite numerical samples do not prove completeness.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import event_sufficiency as old
TOL=1e-10
BLOB='0d6f625cc398ce1cd3e2edeac93156ad7b6c5f8e'


def verify_baseline() -> dict:
    raw=(ROOT/'baseline/event_sufficiency.py').read_bytes()
    digest=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if digest!=BLOB:raise ValueError('frozen v15.22 implementation changed')
    return {'event_sufficiency.py':digest,**{'baseline/'+k:v for k,v in old.verify_baseline().items()}}


def disk_samples() -> tuple[complex,...]:
    return (0j,)+tuple(radius*np.exp(1j*angle*np.pi/4) for radius in (.25,.5,.75,1.) for angle in range(8))


def binary(c: complex) -> np.ndarray:
    if isinstance(c,(bool,str)) or not isinstance(c,(int,float,complex,np.number)):
        raise ValueError('finite complex coefficient required')
    c=complex(c)
    if not np.isfinite([c.real,c.imag]).all() or abs(c)>1+1e-14:raise ValueError('coefficient must be inside the unit disk')
    return np.array([[1,c],[c.conjugate(),1]],complex)


def validate_correlation(c) -> np.ndarray:
    c=np.asarray(c,complex)
    if c.ndim!=2 or not c.shape[0] or c.shape[0]!=c.shape[1] or not np.isfinite(c).all():
        raise ValueError('finite nonempty square correlation matrix required')
    if np.linalg.norm(c-c.conj().T)>TOL or np.linalg.norm(np.diag(c)-1)>TOL:
        raise ValueError('Hermitian matrix with unit diagonal required')
    if np.linalg.eigvalsh(c).min() < -TOL:raise ValueError('correlation matrix is not positive semidefinite')
    return c


def projectors_checked(ps) -> tuple[np.ndarray,...]:
    ps=tuple(np.asarray(p,complex) for p in ps)
    if not ps:raise ValueError('nonempty projector resolution required')
    d=ps[0].shape[0] if ps[0].ndim==2 else 0
    if d==0 or any(p.shape!=(d,d) or not np.isfinite(p).all() for p in ps):raise ValueError('finite equal square projectors required')
    if any(np.linalg.norm(p-p.conj().T)>TOL or np.linalg.norm(p@p-p)>TOL or np.trace(p).real<.5 for p in ps):
        raise ValueError('nonzero orthogonal projections required')
    if np.linalg.norm(sum(ps)-np.eye(d))>TOL or any(np.linalg.norm(p@q)>TOL for i,p in enumerate(ps) for q in ps[i+1:]):
        raise ValueError('projectors must be disjoint and complete')
    return ps


def apply(a,ps,c) -> np.ndarray:
    ps=projectors_checked(ps);c=validate_correlation(c);a=np.asarray(a,complex)
    if c.shape!=(len(ps),len(ps)) or a.shape!=ps[0].shape or not np.isfinite(a).all():raise ValueError('operator or coefficient dimensions invalid')
    return sum((c[i,j]*p@a@q for i,p in enumerate(ps) for j,q in enumerate(ps)),np.zeros_like(a))


def channel_kraus(ps,c) -> tuple[np.ndarray,...]:
    ps=projectors_checked(ps);c=validate_correlation(c)
    if c.shape!=(len(ps),len(ps)):raise ValueError('one correlation label per projector required')
    vals,vecs=np.linalg.eigh(c)
    # Only roundoff-size negative eigenvalues can reach here; keep all positive ones.
    return tuple(sum((np.sqrt(value)*vecs[b,j]*p for b,p in enumerate(ps)),np.zeros_like(ps[0]))
                 for j,value in enumerate(vals) if value>0)


def fit_kraus(ks,ps) -> dict:
    ps=projectors_checked(ps);ks=tuple(np.asarray(k,complex) for k in ks)
    if not ks or any(k.shape!=ps[0].shape or not np.isfinite(k).all() for k in ks):raise ValueError('same-carrier finite Kraus list required')
    coefficients=np.array([[np.trace(p@k)/np.trace(p).real for p in ps] for k in ks])
    residual=max(float(np.linalg.norm(k-sum((a*p for a,p in zip(row,ps)),np.zeros_like(k)))) for k,row in zip(ks,coefficients))
    return {'central_residual':residual,'correlation':coefficients.T@coefficients.conj()}


def phase_pair(ps):
    ps=projectors_checked(ps)
    if len(ps)!=2:raise ValueError('binary witness required')
    vectors=[]
    for p in ps:
        _,v=np.linalg.eigh((p+p.conj().T)/2);vectors.append(v[:,-1])
    x,y=vectors
    return tuple(np.outer(z,z.conj()) for z in ((x+y)/np.sqrt(2),(x-y)/np.sqrt(2)))


def analyze_binary(c) -> dict:
    c=complex(c);binary(c)
    ps=old.effects(old.prior.start(),'A1');a,b=phase_pair(ps)
    aa,bb=(apply(r,ps,binary(c)) for r in (a,b))
    return {'real':float(c.real),'imag':float(c.imag),'modulus':float(abs(c)),
            'trace_distance':old.prior.base.distance(aa,bb),
            'linear_injective':c!=0,'cptp_reversible':bool(abs(abs(c)-1)<1e-12),
            'idempotent':bool(abs(c*c-c)<1e-12),
            'idempotence_coefficient_residual':float(abs(c*c-c)),
            'classification':'FULL_PINCHING' if c==0 else 'UNITARY_PHASE' if abs(abs(c)-1)<1e-12 else 'PARTIAL_DEPHASING'}


def idempotent_correlations(n: int):
    if type(n) is not int or not 1<=n<=4:raise ValueError('exhaustive enumeration restricted to 1..4 outcomes')
    pairs=list(itertools.combinations(range(n),2));result=[]
    for bits in itertools.product((0,1),repeat=len(pairs)):
        c=np.eye(n)
        for (i,j),bit in zip(pairs,bits):c[i,j]=c[j,i]=bit
        if np.linalg.eigvalsh(c).min()>=-TOL:result.append(c)
    return tuple(result)


def partition_audit() -> dict:
    cs=idempotent_correlations(4);counts={str(k):0 for k in range(1,5)}
    for c in cs:counts[str(int(round(np.linalg.matrix_rank(c,tol=TOL))))]+=1
    return {'boolean_candidates':64,'psd_partitions':len(cs),'partitions_by_blocks':counts,
            'local_bit_masks':4,'additional_partitions':len(cs)-4}


def batch(frame):
    ready=old.prior.enabled(frame)
    if len(ready)!=2:raise ValueError('two ready supplied events required')
    pa,pb=(old.effects(frame,e) for e in ready);ka,kb=(old.kraus(frame,e) for e in ready)
    ps=tuple(a@b for a in pa for b in pb)
    ks=tuple(b@a for a in ka for b in kb)
    projectors_checked(ps)
    return ps,ks


def negative_control() -> dict:
    f=old.prior.start();ps=old.effects(f,'A1');vals,v=np.linalg.eigh(ps[0]);x,y=v[:,-1],v[:,-2]
    u=np.eye(len(x))-2*np.outer(x,x.conj());z=(x+y)/np.sqrt(2);rho=np.outer(z,z.conj())
    k=old.kraus(f,'A1')[0];a=k@rho@k.conj().T;b=k@u@rho@u.conj().T@k.conj().T
    return {'probability_error':float(abs(np.trace(a)-np.trace(b))),
        'branch_state_distance':old.prior.base.distance(a/np.trace(a),b/np.trace(b)),
        'central_kraus_residual':fit_kraus([u],ps)['central_residual'],
        'status':'REJECTED_PROBABILITY_ONLY_PRESERVATION'}


@lru_cache(None)
def integration() -> dict:
    se=me=ce=0.;histories=steps=0
    for coefficient in (0.,.5,.5j,1.,-1.):
        for schedule in old.prior.schedules():
            for r in range(16):
                f=old.prior.start();ref=old.prior.run(schedule,f'{r:04b}')
                for i,event in enumerate(schedule,1):
                    w=old.sector(f);ps=old.effects(f,event)
                    transform=lambda a:w@apply(w.conj().T@a@w,ps,binary(coefficient))@w.conj().T
                    f=replace(f,rho=old.prior._frozen(transform(f.rho)),tau=old.prior._frozen(transform(f.tau)))
                    f=old.prior.advance(f,event,int(f'{r:04b}'[old.prior.EVENTS.index(event)]));g=ref[i]
                    se=max(se,old.prior.base.distance(f.rho,g.rho));me=max(me,abs(f.mass-g.mass));ce=max(ce,abs(f.conditional_weight-g.conditional_weight));steps+=1
                histories+=1
    return {'histories':histories,'branch_steps':steps,'max_state_error':se,'max_mass_error':me,'max_conditional_error':ce}


def verify_result(r: dict) -> None:
    needed={'version','status','event_channel_cases','branch_map_checks','max_branch_choi_error','max_kraus_fit_error',
      'max_tp_error','max_distance_formula_error','max_other_event_formula_error','open_alternative_checks',
      'common_identity_cases','batch_partition_cases','batch_branch_checks','max_batch_choi_error','disk','partitions',
      'negative_control','integration','actual_record_selected','physical_duration','new_physical_axioms',
      'physical_pruning_law_derived','scientific_breakthrough','Pillar_3'}
    if set(r)!=needed:raise AssertionError('audit schema mismatch')
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(int,float)) and not isinstance(x,bool) and not np.isfinite(x):raise AssertionError('nonfinite audit value')
    finite(r)
    counts={'event_channel_cases':1188,'branch_map_checks':2376,'open_alternative_checks':231,'common_identity_cases':7,'batch_partition_cases':105,'batch_branch_checks':420}
    if any(r[k]!=v for k,v in counts.items()):raise AssertionError('coverage mismatch')
    for k,v in r.items():
        if k.startswith('max_') and not 0<=v<TOL:raise AssertionError(k)
    for k in ('max_state_error','max_mass_error','max_conditional_error'):
        if not 0<=r['integration'][k]<TOL:raise AssertionError(k)
    if r['integration']['histories']!=400 or r['integration']['branch_steps']!=1600:raise AssertionError('integration coverage')
    if r['partitions']['psd_partitions']!=15 or r['negative_control']['branch_state_distance']<.1:raise AssertionError('sensitivity control')
    if r['actual_record_selected'] is not None or r['physical_duration'] is not None or r['new_physical_axioms']!=[] or r['physical_pruning_law_derived'] is not False:
        raise AssertionError('unsupported ontology claim')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();ec=bc=oc=ic=bpc=bbc=0;be=fe=te=oe=batch_error=0.
    samples=disk_samples()
    for frame in old.contexts().values():
        ready=old.prior.enabled(frame)
        for event in ready:
            ps=old.effects(frame,event);branches=old.kraus(frame,event);d=len(ps[0])
            for c in samples:
                ls=channel_kraus(ps,binary(c));fit=fit_kraus(ls,ps)
                fe=max(fe,fit['central_residual'],float(np.linalg.norm(fit['correlation']-binary(c))))
                te=max(te,float(np.linalg.norm(sum(l.conj().T@l for l in ls)-np.eye(d))))
                for k in branches:
                    be=max(be,float(np.linalg.norm(old.choi([k@l for l in ls])-old.choi([k]))));bc+=1
                ec+=1
        if len(ready)==2:
            pa=old.effects(frame,ready[0]);kb=old.kraus(frame,ready[1])[0];v,labels,_=old.joint_basis(frame)
            x,y=v[:,labels.index((0,0))],v[:,labels.index((1,0))]
            z=(x+y)/np.sqrt(2);rho=np.outer(z,z.conj());native=kb@rho@kb.conj().T
            for c in samples:
                out=kb@apply(rho,pa,binary(c))@kb.conj().T
                dist=old.prior.base.distance(native/np.trace(native),out/np.trace(out))
                oe=max(oe,abs(dist-abs(1-c)/2));oc+=1;ic+=int(dist<TOL)
            ps,ks=batch(frame)
            for corr in idempotent_correlations(4):
                ls=channel_kraus(ps,corr);bpc+=1
                for k in ks:
                    batch_error=max(batch_error,float(np.linalg.norm(old.choi([k@l for l in ls])-old.choi([k]))));bbc+=1
    disk=[analyze_binary(c) for c in samples]
    result={'version':'v15.23','status':'SUFFICIENT_CHANNELS_CLASSIFIED_BINARY_IDEMPOTENCE_SELECTS_PINCHING',
       'event_channel_cases':ec,'branch_map_checks':bc,'max_branch_choi_error':be,'max_kraus_fit_error':fe,'max_tp_error':te,
       'max_distance_formula_error':max(abs(r['trace_distance']-r['modulus']) for r in disk),
       'max_other_event_formula_error':oe,'open_alternative_checks':oc,'common_identity_cases':ic,
       'batch_partition_cases':bpc,'batch_branch_checks':bbc,'max_batch_choi_error':batch_error,
       'disk':disk,'partitions':partition_audit(),'negative_control':negative_control(),'integration':integration(),
       'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
       'physical_pruning_law_derived':False,'scientific_breakthrough':False,'Pillar_3':'OPEN'}
    verify_result(result);return result


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);r=audit()
    (args.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='disk'},indent=2,allow_nan=False))

if __name__=='__main__':main()
