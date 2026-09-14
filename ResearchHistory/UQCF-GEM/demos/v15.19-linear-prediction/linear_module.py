#!/usr/bin/env python3
"""Linear observable prediction closure for the frozen v15.18 motion family.

A coordinate vector is not a physical reduced density matrix. No multiplication
closure, positive projection, entropy selector, clock or actual record is assumed.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import schur

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import completion as old
ZERO_TOL=1e-11
NONZERO_TOL=1e-8
CHECK_TOL=1e-9
BLOB='f50d12b46c72d564a4e69ebab38d477f147becba'

class AmbiguousRank(ValueError):
    """A singular value or spectral gap is unresolved by the declared gap."""


def verify_baseline():
    p=ROOT/'baseline/completion.py';data=p.read_bytes()
    blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if blob!=BLOB:raise ValueError('v15.18 completion source changed')
    return {'completion.py':blob,**{'baseline/'+k:v for k,v in old.verify_baseline().items()}}


@lru_cache(None)
def hermitian_basis(d):
    if type(d) is not int or d<1:raise ValueError('positive integer dimension required')
    h=[]
    for i in range(d):
        a=np.zeros((d,d),complex);a[i,i]=1;h.append(a)
    for i in range(d):
        for j in range(i+1,d):
            a=np.zeros((d,d),complex);a[i,j]=a[j,i]=1/np.sqrt(2);h.append(a)
            a=np.zeros((d,d),complex);a[i,j]=1j/np.sqrt(2);a[j,i]=-1j/np.sqrt(2);h.append(a)
    a=np.array(h);a.setflags(write=False);return a


def coordinates(a):
    a=np.asarray(a,complex)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or not np.isfinite(a).all():raise ValueError('finite square matrix required')
    return hermitian_basis(len(a)).reshape(len(a)**2,-1).conj()@a.reshape(-1)


def from_coordinates(c):
    c=np.asarray(c);d=int(round(np.sqrt(len(c))))
    if c.ndim!=1 or d*d!=len(c) or not np.isfinite(c).all():raise ValueError('finite square-length vector required')
    return np.einsum('k,kij->ij',c,hermitian_basis(d))


def _unitary(u):
    u=np.asarray(u,complex)
    if u.ndim!=2 or u.shape[0]!=u.shape[1] or not np.isfinite(u).all():raise ValueError('finite square unitary required')
    if np.linalg.norm(u.conj().T@u-np.eye(len(u)))>CHECK_TOL:raise ValueError('unitary required')
    return u


def exp_unitary(h,extent):
    h=np.asarray(h,complex)
    if h.ndim!=2 or h.shape[0]!=h.shape[1] or not np.isfinite(h).all() or not np.isfinite(extent):raise ValueError('finite Hermitian generator and extent required')
    if np.linalg.norm(h-h.conj().T)>CHECK_TOL:raise ValueError('Hermitian generator required')
    vals,vecs=np.linalg.eigh(h)
    return (vecs*np.exp(-1j*extent*vals))@vecs.conj().T


def adjoint_action(u):
    u=_unitary(u);d=len(u);b=hermitian_basis(d).reshape(d*d,d*d).T
    t=b.conj().T@np.kron(u.conj().T,u.T)@b
    if np.linalg.norm(t.imag)>CHECK_TOL:raise ArithmeticError('non-real Hermitian action')
    return t.real


def diagonal_seed(d):return np.eye(d*d)[:,:d]


def block_seed(blocks):
    keep=old.keep(blocks);d=len(keep);indices=list(range(d));index=d
    for i in range(d):
        for j in range(i+1,d):
            if keep[i,j]:indices.extend([index,index+1])
            index+=2
    return np.eye(d*d)[:,indices]


def _rank(s):
    if not np.isfinite(s).all():raise ArithmeticError('nonfinite singular values')
    bad=(s>ZERO_TOL)&(s<NONZERO_TOL)
    if bad.any():raise AmbiguousRank(f'singular value in gap: {s[bad].tolist()}')
    return int(np.sum(s>=NONZERO_TOL))


def orthogonal_columns(a):
    a=np.asarray(a)
    if a.ndim!=2 or not np.isfinite(a).all():raise ValueError('finite matrix required')
    q,s,_=np.linalg.svd(a,full_matrices=False);rank=_rank(s)
    return q[:,:rank],s


def minimal_module(units,seed):
    if not isinstance(units,(list,tuple)) or not units:raise ValueError('nonempty supplied unitary family required')
    units=[_unitary(u) for u in units];d=len(units[0]);seed=np.asarray(seed)
    if any(u.shape!=(d,d) for u in units) or seed.ndim!=2 or seed.shape[0]!=d*d or not np.isfinite(seed).all():raise ValueError('matching finite seed required')
    if np.iscomplexobj(seed) and np.linalg.norm(seed.imag)>ZERO_TOL:raise ValueError('seed must be real Hermitian coordinates')
    q,_=orthogonal_columns(seed.real);actions=[adjoint_action(u) for u in units]
    operators=[a for t in actions for a in (t,t.T)]
    history=[q.shape[1]];frontier=q.copy();minimum=1.;maximum_null=0.;rounds=[]
    for _ in range(d*d+1):
        if q.shape[1]==d*d:break
        images=np.concatenate([t@frontier for t in operators],axis=1)
        residual=images-q@(q.T@images)
        residual-=q@(q.T@residual)
        extra,s=orthogonal_columns(residual)
        rank=extra.shape[1]
        minimum=min(minimum,float(s[:rank].min())) if rank else minimum
        if rank<len(s):maximum_null=max(maximum_null,float(s[rank:].max()))
        rounds.append({'added_rank':rank,'max_discarded_singular_value':float(s[rank:].max()) if rank<len(s) else 0.,'min_retained_singular_value':float(s[:rank].min()) if rank else None})
        if not rank:break
        # Reorthogonalize after residual SVD; this never adds directions.
        extra-=q@(q.T@extra);extra=np.linalg.qr(extra,mode='reduced')[0]
        q=np.column_stack([q,extra]);frontier=extra;history.append(q.shape[1])
    else:raise ArithmeticError('finite closure did not stabilize')
    errors=[float(np.linalg.norm(t@q-q@(q.T@t@q))) for t in operators]
    ortho=float(np.linalg.norm(q.T@q-np.eye(q.shape[1])))
    if max(errors+[ortho])>CHECK_TOL:raise ArithmeticError(f'closure residual {max(errors+[ortho])}')
    seed_error=float(np.linalg.norm(seed-q@(q.T@seed)))
    return {'basis':q,'dimension':q.shape[1],'dimension_history':history,'rank_rounds':rounds,
            'max_closure_error':max(errors),'orthogonality_error':ortho,'seed_containment_error':seed_error,
            'smallest_retained_residual_sv':minimum,'largest_discarded_residual_sv':maximum_null}


def spectral_dimension(u,seed):
    """Independent single-unitary cyclic rank via adjoint eigenphase sectors."""
    u=_unitary(u);d=len(u);seed=np.asarray(seed,float)
    if seed.ndim!=2 or seed.shape[0]!=d*d or not np.isfinite(seed).all():raise ValueError('matching finite seed required')
    tri,v=schur(u,output='complex')
    off=float(np.linalg.norm(tri-np.diag(tri.diagonal())))
    if off>CHECK_TOL:raise ArithmeticError('unitary Schur decomposition not diagonal')
    vals=tri.diagonal();phases=(vals.conj()[:,None]*vals[None,:]).reshape(-1)
    ops=np.einsum('ak,aij->kij',seed,hermitian_basis(d))
    rotated=np.einsum('ai,kij,jb->kab',v.conj().T,ops,v).reshape(seed.shape[1],d*d).T
    unused=set(range(d*d));groups=[];ranks=[];null_max=0.;min_sv=1.;min_gap=2.
    while unused:
        i=min(unused);diff=abs(phases-phases[i]);uncertain=(diff>ZERO_TOL)&(diff<NONZERO_TOL)
        if uncertain.any():raise AmbiguousRank('adjoint eigenphase gap unresolved')
        group=[j for j in sorted(unused) if diff[j]<=ZERO_TOL];unused.difference_update(group)
        if (diff>=NONZERO_TOL).any():min_gap=min(min_gap,float(diff[diff>=NONZERO_TOL].min()))
        s=np.linalg.svd(rotated[group],compute_uv=False);rank=_rank(s)
        if rank:min_sv=min(min_sv,float(s[:rank].min()))
        if rank<len(s):null_max=max(null_max,float(s[rank:].max()))
        groups.append(group);ranks.append(rank)
    return {'dimension':sum(ranks),'eigenphase_sector_count':len(groups),'sector_ranks':ranks,
            'min_distinct_eigenphase_gap':min_gap,'smallest_retained_sv':min_sv,'largest_discarded_sv':null_max,
            'schur_offdiagonal_error':off}



def spectral_module(u,seed):
    """Cyclic span from real adjoint eigensectors, avoiding long Krylov chains.

    No rank tolerances change. Real planes join a phase and its conjugate;
    within each plane span{P seed, T P seed} is the complete cyclic span.
    """
    u=_unitary(u);d=len(u);seed=np.asarray(seed,float)
    if seed.ndim!=2 or seed.shape[0]!=d*d or not np.isfinite(seed).all():raise ValueError('matching finite seed required')
    tri,v=schur(u,output='complex');vals=tri.diagonal()
    if np.linalg.norm(tri-np.diag(vals))>CHECK_TOL:raise ArithmeticError('non-diagonal unitary Schur form')
    phases=(vals.conj()[:,None]*vals[None,:]).reshape(-1)
    hb=hermitian_basis(d).reshape(d*d,d*d).T
    eigenoperators=hb.conj().T@np.kron(v,v.conj())
    t=adjoint_action(u);unused=set(range(d*d));pieces=[];minimum=1.;nullmax=0.;ranks=[]
    while unused:
        index=min(unused);lam=phases[index]
        delta=abs(phases-lam);delta_bar=abs(phases-lam.conjugate())
        dist=np.minimum(delta,delta_bar)
        if ((dist>ZERO_TOL)&(dist<NONZERO_TOL)).any():raise AmbiguousRank('real eigensector gap unresolved')
        group=[j for j in sorted(unused) if delta[j]<=ZERO_TOL]
        conjugate=[j for j in sorted(unused) if delta_bar[j]<=ZERO_TOL]
        unused.difference_update(group+conjugate)
        e=eigenoperators[:,group]
        if abs(lam.imag)<=ZERO_TOL:
            proj=(e@e.conj().T).real
            candidates=proj@seed
            q,sing=orthogonal_columns(candidates);rank=q.shape[1]
            if rank:q=np.linalg.qr(proj@q,mode='reduced')[0]
        else:
            # A single complex eigenspace evolves by scalar lambda. Pair it
            # explicitly with its adjoint; do not infer the second real
            # direction by subtracting nearly aligned T-projected vectors.
            qsmall,sing=orthogonal_columns(e.conj().T@seed)
            r=qsmall.shape[1];rank=2*r
            qcomplex=e@qsmall
            q=np.column_stack([np.sqrt(2)*qcomplex.real,np.sqrt(2)*qcomplex.imag])
        if rank:
            pieces.append(q)
            accepted=rank if abs(lam.imag)<=ZERO_TOL else rank//2
            minimum=min(minimum,float(sing[:accepted].min()))
        else:accepted=0
        if accepted<len(sing):nullmax=max(nullmax,float(sing[accepted:].max()))
        ranks.append(rank)
    joined=np.column_stack(pieces);q=np.linalg.qr(joined,mode='reduced')[0]
    errors=[float(np.linalg.norm(a@q-q@(q.T@a@q))) for a in (t,t.T)]
    ortho=float(np.linalg.norm(q.T@q-np.eye(q.shape[1])))
    seederr=float(np.linalg.norm(seed-q@(q.T@seed)))
    if max(errors+[ortho,seederr])>CHECK_TOL:raise ArithmeticError('spectral span residual failed '+str(max(errors+[ortho,seederr])))
    return {'basis':q,'dimension':q.shape[1],'dimension_history':[seed.shape[1],q.shape[1]],
            'rank_rounds':[],'max_closure_error':max(errors),'orthogonality_error':ortho,
            'seed_containment_error':seederr,'smallest_retained_residual_sv':minimum,
            'largest_discarded_residual_sv':nullmax,'construction':'ADJOINT_REAL_EIGENSECTORS',
            'real_sector_ranks':ranks}


@lru_cache(None)
def _common_family_seed(family):
    return minimal_module(old.label_motions(family),diagonal_seed(16))


def family_module(family,mask):
    units=old.label_motions(family);seed=block_seed(old.old.old.groups(mask))
    if len(units)==1:return spectral_module(units[0],seed)
    # Every original algebra contains the full diagonal seed. Its invariant
    # module is a lower bound for every mask. Reusing it avoids unnecessary
    # ill-conditioned rediscovery; no extra observable is introduced.
    common=_common_family_seed(family)
    residual=seed-common['basis']@(common['basis'].T@seed)
    residual-=common['basis']@(common['basis'].T@residual)
    extra,sv=orthogonal_columns(residual)
    if extra.shape[1]:
        start=np.column_stack([common['basis'],extra])
        result=minimal_module(units,start)
    else:result=dict(common)
    result['dimension_history']=[seed.shape[1],result['dimension']]
    result['seed_containment_error']=float(np.linalg.norm(seed-result['basis']@(result['basis'].T@seed)))
    result['construction']='COMMON_DIAGONAL_CYCLIC_SEED_THEN_EXTENSION'
    return result

def state_features(rho,q):
    c=coordinates(rho)
    if np.linalg.norm(c.imag)>CHECK_TOL:raise ValueError('Hermitian state required')
    return q.T@c.real


def _prediction_check(units,seed,q):
    d=len(units[0]);psi=np.arange(1,d+1)+1j*np.arange(d,0,-1)
    psi=psi/np.linalg.norm(psi);rho=.83*np.outer(psi,psi.conj())+.17*np.eye(d)/d
    z=state_features(rho,q);transfers=[q.T@adjoint_action(u)@q for u in units]
    error=0.;minimum=1.
    # Deterministic finite compositions including inverses, not time steps.
    word=[(i%len(units),bool(i%3==0)) for i in range(12)]
    for i,inverse in word:
        u=units[i].conj().T if inverse else units[i]
        t=transfers[i].T if inverse else transfers[i]
        z=t.T@z;rho=u@rho@u.conj().T
        error=max(error,float(np.linalg.norm(z-state_features(rho,q))),float(np.linalg.norm(seed.T@q@z-seed.T@coordinates(rho).real)))
        # A projected representative is only coordinates: may be nonpositive.
        representative=from_coordinates(q@z)
        minimum=min(minimum,float(np.linalg.eigvalsh(representative).min()))
    return error,minimum


def controls():
    x=np.array([[0,1],[1,0]],complex);y=np.array([[0,-1j],[1j,0]]);z=np.diag([1.,-1.])
    u=exp_unitary(y,.31);q=minimal_module([u],diagonal_seed(2))['basis']
    projection=lambda a:from_coordinates(q@(q.T@coordinates(a)))
    choi=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            e=np.zeros((2,2));e[i,j]=1;choi+=np.kron(e,projection(e))
    a=(np.eye(2)+x)/2;b=(np.eye(2)-x)/2;pinch=lambda r:np.diag(np.diag(r))
    return {'qubit_linear_dimension':q.shape[1],'qubit_algebra_dimension':4,
            'multiplication_residual':float(np.linalg.norm(x@z-projection(x@z))),
            'qubit_projection_min_choi_eigenvalue':float(np.linalg.eigvalsh(choi).min()),
            'already_pruned_feature_distance':float(np.linalg.norm(state_features(pinch(a),q)-state_features(pinch(b),q))),
            'required_before_pruning_feature_distance':float(np.linalg.norm(state_features(a,q)-state_features(b,q))),
            'incomplete_diagonal_prediction_error':float(np.linalg.norm(diagonal_seed(2).T@adjoint_action(u)@(coordinates(a)-coordinates(pinch(a))))),
            'scope':'A non-CP linear expectation projection is not a supplied physical pruning channel.'}


@lru_cache(None)
def case(family,mask):
    units=old.label_motions(family);seed=block_seed(old.old.old.groups(mask))
    model=family_module(family,mask);q=model['basis'];spectral=spectral_dimension(units[0],seed) if len(units)==1 else None
    if spectral is not None and spectral['dimension']!=model['dimension']:raise ArithmeticError('independent cyclic rank disagrees')
    algebra=old.case(family,mask)['final_dimension']
    error,minimum=_prediction_check(units,seed,q)
    identity=coordinates(np.eye(16)).real
    row={k:v for k,v in model.items() if k!='basis'}
    row.update(family=family,mask=mask,initial_dimension=seed.shape[1],linear_dimension=model['dimension'],
               algebra_dimension=algebra,saved_vs_algebra=algebra-model['dimension'],
               spectral_dimension=spectral['dimension'] if spectral else None,spectral_check=spectral,
               prediction_error=error,minimum_projected_representative_eigenvalue=minimum,
               identity_containment_error=float(np.linalg.norm(identity-q@(q.T@identity))))
    return row,q



def parity_control():
    """Conserved direction already implicit in the fixed Pauli generators."""
    base=old.old.old.old.prior.base
    gamma=base.tensor_word('YYYY')
    f=old.old.old.basis();g=f@gamma@f.conj().T
    v=coordinates(g).real/4
    row,q=case('all_six','1111')
    complement=np.eye(256)-np.outer(v,v)
    comm=max(float(np.linalg.norm(u@gamma-gamma@u)) for u in old.input_motions('all_six'))
    # Each listed term is present in an unchanged generator or controller.
    # Two distinct nonidentity Pauli letters anticommute. An even count
    # across the tensor factors proves commutation, without numeric fitting.
    words=('ZIZI','IZIZ','YIII','ZXII','IYII','IIYI','IIZX','IIIY')
    terms=[]
    for w in words:
        antis=sum(c not in ('I','Y') for c in w)
        terms.append({'word':w,'anticommuting_factors':antis,'commutes_exactly':antis%2==0})
    rp=(np.eye(16)+g)/16;rm=(np.eye(16)-g)/16
    yp=np.array([1,1j])/np.sqrt(2);psi=yp
    for _ in range(3):psi=np.kron(psi,yp)
    rho0=np.outer(psi,psi.conj());rho=f@rho0@f.conj().T
    projected=from_coordinates(q@(q.T@coordinates(rho)))
    return {'operator':'Y tensor Y tensor Y tensor Y','pauli_terms':terms,
            'max_motion_commutator':comm,'module_dimension':row['linear_dimension'],
            'complement_projector_error':float(np.linalg.norm(q@q.T-complement)),
            'opposite_parity_state_distance':old.old.distance(rp,rm),
            'opposite_parity_feature_distance':float(np.linalg.norm(state_features(rp,q)-state_features(rm,q))),
            'opposite_parity_record_probability_difference':float(np.max(abs(np.diag(rp)-np.diag(rm)))),
            'projected_pure_state_min_eigenvalue':float(np.linalg.eigvalsh(projected).min()),
            'new_physical_law':False,
            'scope':'Conserved symmetry of the supplied finite toy generators. Linear expectation coordinates are not a physical density-matrix compression.'}

def verify_result(a):
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif type(x) is float and not np.isfinite(x):raise AssertionError('nonfinite result')
    finite(a)
    if len(a['cases'])!=112:raise AssertionError('coverage')
    for c in a['cases']:
        if not c['initial_dimension']<=c['linear_dimension']<=c['algebra_dimension']:raise AssertionError('dimension boundary')
        if c['family']!='all_six' and c['linear_dimension']!=c['spectral_dimension']:raise AssertionError('spectral crosscheck')
        if max(c['max_closure_error'],c['orthogonality_error'],c['seed_containment_error'],c['prediction_error'])>CHECK_TOL:raise AssertionError('residual failure')
    if a['max_prediction_error']>CHECK_TOL:raise AssertionError('prediction failure')
    if a['physical_duration'] is not None or a['actual_record_selected'] is not None or a['new_physical_axioms']!=[]:raise AssertionError('claim boundary')


@lru_cache(None)
def audit():
    verify_baseline();families=[*old.old.frozen_motions(),'all_six']
    rows=[case(family,mask)[0] for family in families for mask in old.old.old.masks()]
    a={'version':'v15.19','status':'EXECUTED_CONDITIONAL_LINEAR_PREDICTION_MODULE',
       'cases':rows,'max_prediction_error':max(r['prediction_error'] for r in rows),
       'max_closure_error':max(r['max_closure_error'] for r in rows),'controls':controls(),'parity':parity_control(),
       'physical_duration':None,'actual_record_selected':None,'new_physical_axioms':[],
       'physical_pruning_law_derived':False,'physical_entropy_law_derived':False,
       'GOSM_rederived':False,'Pillar_3':'OPEN','scientific_breakthrough':False,
       'scope':'Minimal invariant real Hermitian linear span for fixed observables and supplied finite unitary words. Not a CPTP reduction, time, entropy or actuality law.'}
    verify_result(a);return a


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs');args=p.parse_args()
    result=audit();args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({f:{r['mask']:(r['linear_dimension'],r['algebra_dimension']) for r in result['cases'] if r['family']==f} for f in [*old.old.frozen_motions(),'all_six']},indent=2))

if __name__=='__main__':main()
