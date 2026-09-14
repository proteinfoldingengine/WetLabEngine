#!/usr/bin/env python3
"""v15.24: batch sufficiency, no-signalling, and product composition differ.

No spacetime, locality law, random outcome or actual record is inferred. All
requirements are conditional tests on the inherited two-stream tensor factors.
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
import retention_family as old
E=old.old
P=E.prior
TOL=1e-10
BLOB='7c5a412c5f3925ad3656b08ccb035e9516ec108a'


def verify_baseline() -> str:
    raw=(ROOT/'baseline/retention_family.py').read_bytes()
    digest=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if digest!=BLOB:raise ValueError('v15.23 source changed')
    old.verify_baseline()
    return digest


def partitions() -> tuple[np.ndarray,...]:
    return tuple(c.astype(int) for c in old.idempotent_correlations(4))


def checked(c) -> np.ndarray:
    c=np.asarray(c)
    if c.shape!=(4,4) or not np.isfinite(c).all() or np.any(np.imag(c)!=0):
        raise ValueError('finite real 4x4 partition correlation required')
    if not np.all((c==0)|(c==1)) or not np.array_equal(c,c.T) or not np.all(np.diag(c)==1):
        raise ValueError('symmetric zero/one matrix with unit diagonal required')
    c=c.astype(int)
    if any(c[i,j] and c[j,k] and not c[i,k] for i,j,k in itertools.product(range(4),repeat=3)):
        raise ValueError('partition relation is not transitive')
    return c


def groups(c) -> list[list[int]]:
    c=checked(c);remaining=set(range(4));result=[]
    while remaining:
        g=np.flatnonzero(c[min(remaining)]).tolist();result.append(g);remaining-=set(g)
    return result


def code(c) -> str:
    gs=groups(c)
    return ''.join(str(next(k for k,g in enumerate(gs) if i in g)) for i in range(4))


def classify(c) -> dict:
    c=checked(c)
    # Non-signalling constrains local off-diagonal response at both remote values.
    ba=bool(c[0,2]!=c[1,3]);ab=bool(c[0,1]!=c[2,3])
    ca=old.binary(int(c[0,2]));cb=old.binary(int(c[0,1]))
    product=bool(np.array_equal(c,np.kron(ca,cb)))
    return {'partition':code(c),'groups':groups(c),'matrix':c.tolist(),
            'A_to_B':ab,'B_to_A':ba,'non_signalling':not(ab or ba),'product':product,
            'classification':'PRODUCT_LOCAL' if product else 'CORRELATED_NON_SIGNALLING' if not(ab or ba) else 'CROSS_INPUT_INFLUENCE'}


def contexts() -> tuple:
    return tuple(f for f in E.contexts().values() if len(P.enabled(f))==2)


def partial(a,da: int,db: int,keep: str) -> np.ndarray:
    a=np.asarray(a,complex)
    if a.shape!=(da*db,da*db) or not np.isfinite(a).all() or keep not in ('A','B'):
        raise ValueError('operator or retained factor invalid')
    q=a.reshape(da,db,da,db)
    return np.trace(q,axis1=1,axis2=3) if keep=='A' else np.trace(q,axis1=0,axis2=2)


def local_effects(frame):
    ready=P.enabled(frame)
    if len(ready)!=2 or not ready[0].startswith('A') or not ready[1].startswith('B'):
        raise ValueError('requires one ready event on each inherited stream')
    da=2**(2-sum(e.startswith('A') for e in frame.done))
    db=2**(2-sum(e.startswith('B') for e in frame.done))
    ea,eb=(E.effects(frame,e) for e in ready)
    aa=tuple(partial(a,da,db,'A')/db for a in ea)
    bb=tuple(partial(b,da,db,'B')/da for b in eb)
    old.projectors_checked(aa);old.projectors_checked(bb)
    if max(*(np.linalg.norm(x-np.kron(a,np.eye(db))) for x,a in zip(ea,aa)),
           *(np.linalg.norm(y-np.kron(np.eye(da),b)) for y,b in zip(eb,bb)))>TOL:
        raise ArithmeticError('inherited local-factor structure failed')
    return aa,bb


def no_signal_operator_error(frame,c) -> float:
    if not classify(c)['non_signalling']:raise ValueError('not a no-signalling candidate')
    aa,bb=local_effects(frame);da,db=len(aa[0]),len(bb[0]);ps,_=old.batch(frame)
    error=0.
    # Adjoint identities on ALL local matrix units certify both marginal channels
    # for arbitrary joint inputs, including entangled inputs and a reference.
    for keep,d,local,coefficient in [('A',da,aa,c[0,2]),('B',db,bb,c[0,1])]:
        for i,j in itertools.product(range(d),repeat=2):
            x=np.zeros((d,d),complex);x[i,j]=1
            y=old.apply(x,local,old.binary(int(coefficient)))
            lift=lambda z:np.kron(z,np.eye(db)) if keep=='A' else np.kron(np.eye(da),z)
            error=max(error,float(np.linalg.norm(old.apply(lift(x),ps,c)-lift(y))))
    return error


def _vectors(ps):
    result=[]
    for p in ps:
        _,v=np.linalg.eigh((p+p.conj().T)/2);result.append(v[:,-1])
    return result


def signalling_witness(frame,c,direction: str) -> dict:
    row=classify(c)
    if direction not in ('A_to_B','B_to_A') or not row[direction]:raise ValueError('no such influence in this map')
    aa,bb=local_effects(frame);av,bv=_vectors(aa),_vectors(bb)
    da,db=len(aa[0]),len(bb[0]);ps,_=old.batch(frame)
    plus=lambda v:(v[0]+v[1])/np.sqrt(2)
    keep='B' if direction=='A_to_B' else 'A'
    vectors=[np.kron(av[b],plus(bv)) if keep=='B' else np.kron(plus(av),bv[b]) for b in (0,1)]
    inputs=[np.outer(v,v.conj()) for v in vectors]
    outputs=[old.apply(r,ps,c) for r in inputs]
    local_in=[partial(r,da,db,keep) for r in inputs];local_out=[partial(r,da,db,keep) for r in outputs]
    lp=bb if keep=='B' else aa
    prob=max(float(abs(np.trace(p@(local_out[0]-local_out[1])))) for p in lp)
    preservation=max(float(abs(np.trace(p@(out-r)))) for r,out in zip(inputs,outputs) for p in ps)
    return {'direction':direction,'local_input_distance':P.base.distance(*local_in),
        'local_output_distance':P.base.distance(*local_out),'local_record_probability_change':prob,
        'complete_record_probabilities_changed_by_map':preservation,
        'scope':'Change only the other stream preparation in product inputs; the receiver input is identical. Full joint distributions need not agree between the two differently prepared inputs.'}


def phase_recipe(c) -> tuple:
    c=checked(c);key=code(c)
    recipes={
        '0000':((1.,0.,0.),),
        '0011':((.5,0.,0.),(.5,np.pi,0.)),
        '0101':((.5,0.,0.),(.5,0.,np.pi)),
        '0123':tuple((.25,a*np.pi,b*np.pi) for a,b in itertools.product((0,1),repeat=2)),
        '0110':((.5,0.,0.),(.5,np.pi,np.pi)),
        '0120':tuple((1/3,k*2*np.pi/3,-k*2*np.pi/3) for k in range(3)),
        '0112':tuple((1/3,k*2*np.pi/3,k*2*np.pi/3) for k in range(3))}
    if key not in recipes:raise ValueError('no no-communication phase-mixture certificate for this partition')
    return recipes[key]


def recipe_correlation(recipe) -> np.ndarray:
    result=np.zeros((4,4),complex)
    for weight,a,b in recipe:
        v=np.exp(1j*np.array([0,b,a,a+b]));result+=weight*np.outer(v,v.conj())
    return result


def phase_kraus(frame,c):
    aa,bb=local_effects(frame)
    return tuple(np.sqrt(w)*np.kron(aa[0]+np.exp(1j*a)*aa[1],bb[0]+np.exp(1j*b)*bb[1]) for w,a,b in phase_recipe(c))


def parity_correlation() -> np.ndarray:
    labels=np.array([0,1,1,0]);return (labels[:,None]==labels[None,:]).astype(int)


def parity_control() -> dict:
    f=P.start();aa,bb=local_effects(f);a,b=_vectors(aa),_vectors(bb)
    plus=lambda v:(v[0]+v[1])/np.sqrt(2)
    v=np.kron(plus(a),plus(b));rho=np.outer(v,v.conj());ps,_=old.batch(f)
    shared=old.apply(rho,ps,parity_correlation());independent=old.apply(rho,ps,np.eye(4))
    local=max(P.base.distance(partial(shared,4,4,k),partial(independent,4,4,k)) for k in ('A','B'))
    xx=lambda v:np.outer(v[0],v[1].conj())+np.outer(v[1],v[0].conj())
    obs=np.kron(xx(a),xx(b))
    return {'local_marginal_distance':local,'joint_state_distance':P.base.distance(shared,independent),
        'record_probability_difference':max(float(abs(np.trace(p@(shared-independent)))) for p in ps),
        'correlated_xx_expectation':float(np.trace(obs@shared).real),
        'independent_xx_expectation':float(np.trace(obs@independent).real),
        'interpretation':'Same local marginals and complete record probabilities, different joint retained coherence. The correlated map is a finite mixture of product local phase unitaries, not a sampled actual history.'}


@lru_cache(None)
def integration() -> dict:
    se=me=pe=0.;count=applications=0
    for c in partitions():
        for schedule in P.schedules():
            for r in range(16):
                script=f'{r:04b}';reference=P.run(schedule,script);f=P.start();i=0
                while i<4:
                    ready=P.enabled(f);batch_ready=len(ready)==2 and set(schedule[i:i+2])==set(ready)
                    width=2 if batch_ready else 1
                    if batch_ready:
                        w=E.sector(f);ps,_=old.batch(f)
                        transform=lambda a:w@old.apply(w.conj().T@a@w,ps,c)@w.conj().T
                        f=replace(f,rho=P._frozen(transform(f.rho)),tau=P._frozen(transform(f.tau)));applications+=1
                    for e in schedule[i:i+width]:f=P.advance(f,e,int(script[P.EVENTS.index(e)]))
                    i+=width
                    pe=max(pe,P.base.distance(f.rho,reference[i].rho))
                se=max(se,P.base.distance(f.rho,reference[-1].rho));me=max(me,abs(f.mass-reference[-1].mass));count+=1
    return {'batched_histories':count,'completed_batch_preprocessings':applications,
            'max_completed_boundary_state_error':pe,'max_final_state_error':se,'max_final_mass_error':me,
            'scope':'Preprocess only when both next scheduled events are a declared ready batch. Compare after the whole batch, not at its intermediate single-event output.'}


def verify_result(r: dict) -> None:
    expected={'version','status','partition_counts','context_partition_cases','non_signalling_context_cases',
      'signalling_context_cases','batch_branch_checks','shared_phase_context_cases','max_batch_choi_error',
      'max_non_signalling_operator_residual','max_phase_choi_error','max_phase_tp_error','max_tensor_factor_error',
      'open_frontier_identity_cases','max_identity_frontier_error','min_nonidentity_frontier_error',
      'partitions','contexts','parity_control','integration','actual_record_selected','physical_duration',
      'new_physical_axioms','physical_locality_derived','shared_random_outcome_sampled','Pillar_3'}
    if set(r)!=expected:raise AssertionError('audit schema mismatch')
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(float,int)) and not isinstance(x,bool) and not np.isfinite(x):raise AssertionError('nonfinite audit value')
    finite(r)
    counts={'context_partition_cases':105,'non_signalling_context_cases':49,'signalling_context_cases':56,
      'batch_branch_checks':420,'shared_phase_context_cases':49,'open_frontier_identity_cases':7}
    if any(r[k]!=v for k,v in counts.items()):raise AssertionError('coverage mismatch')
    if r['partition_counts']!={'total':15,'non_signalling':7,'product':4,'correlated_non_signalling':3,'signalling':8}:raise AssertionError('classification counts')
    for k,v in r.items():
        if k.startswith('max_') and not 0<=v<TOL:raise AssertionError(k)
    if r['min_nonidentity_frontier_error']<1e-4:raise AssertionError('insensitive full-instrument control')
    for row in r['contexts']:
        for w in row['witnesses']:
            if w['local_input_distance']>TOL or abs(w['local_output_distance']-.5)>TOL or w['local_record_probability_change']>TOL:raise AssertionError('signalling witness failed')
    integ=r['integration']
    if integ['batched_histories']!=1200 or integ['completed_batch_preprocessings']!=2160:raise AssertionError('integration coverage')
    if any(v>TOL for k,v in integ.items() if k.startswith('max_')):raise AssertionError('integration failed')
    if r['actual_record_selected'] is not None or r['physical_duration'] is not None or r['new_physical_axioms']!=[]:raise AssertionError('ontology boundary')
    if r['physical_locality_derived'] is not False or r['shared_random_outcome_sampled'] is not False:raise AssertionError('unsupported physical claim')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();cs=partitions();classes=[classify(c) for c in cs]
    rows=[];bc=ns=sig=shared=ident=0;be=ne=ce=te=fe=ie=0.;minerr=1e9
    for f in contexts():
        aa,bb=local_effects(f);ps,ks=old.batch(f);ready=P.enabled(f)
        fe=max(fe,*(float(np.linalg.norm(p-np.kron(a,b))) for p,(a,b) in zip(ps,itertools.product(aa,bb))))
        for c,cls in zip(cs,classes):
            ls=old.channel_kraus(ps,c);row={'context':E.context_key(f),'partition':cls['partition'],
              'classification':cls['classification'],'local_dimensions':[len(aa[0]),len(bb[0])],'witnesses':[]}
            for k in ks:be=max(be,float(np.linalg.norm(E.choi([k@l for l in ls])-E.choi([k]))));bc+=1
            if cls['non_signalling']:
                ne=max(ne,no_signal_operator_error(f,c));ns+=1
                local_ks=phase_kraus(f,c)
                ce=max(ce,float(np.linalg.norm(E.choi(local_ks)-E.choi(ls))))
                te=max(te,float(np.linalg.norm(sum(k.conj().T@k for k in local_ks)-np.eye(len(ps[0])))));shared+=1
            else:
                sig+=1
                row['witnesses']=[signalling_witness(f,c,key) for key in ('A_to_B','B_to_A') if cls[key]]
            frontier=max(float(np.linalg.norm(E.choi([k@l for l in ls])-E.choi([k]))) for e in ready for k in E.kraus(f,e))
            if cls['partition']=='0000':ident+=1;ie=max(ie,frontier)
            else:minerr=min(minerr,frontier)
            row['full_next_instrument_error']=frontier;rows.append(row)
    r={'version':'v15.24','status':'BATCH_RETENTION_NON_SIGNALLING_AND_PRODUCT_COMPOSITION_DISTINGUISHED',
      'partition_counts':{'total':15,'non_signalling':sum(c['non_signalling'] for c in classes),'product':sum(c['product'] for c in classes),
          'correlated_non_signalling':sum(c['non_signalling'] and not c['product'] for c in classes),'signalling':sum(not c['non_signalling'] for c in classes)},
      'context_partition_cases':len(rows),'non_signalling_context_cases':ns,'signalling_context_cases':sig,'batch_branch_checks':bc,
      'shared_phase_context_cases':shared,'max_batch_choi_error':be,'max_non_signalling_operator_residual':ne,
      'max_phase_choi_error':ce,'max_phase_tp_error':te,'max_tensor_factor_error':fe,
      'open_frontier_identity_cases':ident,'max_identity_frontier_error':ie,'min_nonidentity_frontier_error':minerr,
      'partitions':classes,'contexts':rows,'parity_control':parity_control(),'integration':integration(),
      'actual_record_selected':None,'physical_duration':None,'new_physical_axioms':[],
      'physical_locality_derived':False,'shared_random_outcome_sampled':False,'Pillar_3':'OPEN'}
    verify_result(r);return r


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    a=p.parse_args();r=audit();a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('partitions','contexts')},indent=2,allow_nan=False))

if __name__=='__main__':main()
