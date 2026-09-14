#!/usr/bin/env python3
"""Minimal invariant *-algebra for supplied motions, not a new pruning law.

An enlargement is a requirement on information retained before pruning; it is
not an operation that reconstructs information from an already pruned output.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
from collections.abc import Sequence
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'baseline'))
import retained_motion as old
ZERO_TOL=1e-12
NONZERO_TOL=1e-9
CHECK_TOL=1e-10
BASE_SHA='a01f1ff5f1045bc701a97bfef44eab58cfc5b401'
BASE_BLOB='e3e8ac11cd5a856c66763faa071957fd9a220b42'

class AmbiguousSupport(ValueError):
    """Cannot adjudicate exact support with the preregistered numerical gap."""


def verify_baseline() -> dict:
    data=(ROOT/'baseline/retained_motion.py').read_bytes()
    digest=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if digest!=BASE_BLOB:raise ValueError('frozen v15.17 baseline differs')
    return {'retained_motion.py':digest,**{'baseline/'+k:v for k,v in old.verify_baseline().items()}}


def canonical(blocks: Sequence[Sequence[int]],dimension: int) -> list[list[int]]:
    if type(dimension) is not int or dimension<1:raise ValueError('positive dimension required')
    if not isinstance(blocks,(list,tuple)) or not blocks:raise ValueError('nonempty partition required')
    flat=[];out=[]
    for block in blocks:
        if not isinstance(block,(list,tuple)) or not block:raise ValueError('nonempty blocks required')
        if any(type(i) is not int for i in block):raise ValueError('integer labels required')
        flat.extend(block);out.append(sorted(block))
    if sorted(flat)!=list(range(dimension)):raise ValueError('partition must cover every label exactly once')
    return sorted(out,key=lambda g:g[0])


def contains(coarser,finer) -> bool:
    """The coarser partition represents the LARGER full-block algebra."""
    return all(any(set(g)<=set(h) for h in coarser) for g in finer)


def dimension(blocks) -> int:return sum(len(g)**2 for g in blocks)


def keep(blocks) -> np.ndarray:
    d=sum(map(len,blocks));blocks=canonical(blocks,d);a=np.zeros((d,d),bool)
    for g in blocks:a[np.ix_(g,g)]=True
    return a


def _unitaries(units,d):
    if not isinstance(units,(list,tuple)):raise ValueError('a finite list of unitaries required')
    out=[]
    for u in units:
        u=np.asarray(u,complex)
        if u.shape!=(d,d) or not np.all(np.isfinite(u)) or np.linalg.norm(u.conj().T@u-np.eye(d))>CHECK_TOL:
            raise ValueError('finite matching unitary matrices required')
        out.append(u)
    return out


def _supports(units):
    result=[];max_zero=0.;min_nonzero=1.
    for u in units:
        a=np.abs(u);uncertain=(a>ZERO_TOL)&(a<NONZERO_TOL)
        if uncertain.any():raise AmbiguousSupport(f'{uncertain.sum()} entries lie in the fixed support gap')
        if (a<=ZERO_TOL).any():max_zero=max(max_zero,float(a[a<=ZERO_TOL].max()))
        if (a>=NONZERO_TOL).any():min_nonzero=min(min_nonzero,float(a[a>=NONZERO_TOL].min()))
        result.append(a>=NONZERO_TOL)
    return result,{'max_discarded_entry':max_zero,'min_retained_entry':min_nonzero,
                   'zero_tolerance':ZERO_TOL,'nonzero_tolerance':NONZERO_TOL}


def normalizer_error(blocks,units) -> float:
    d=sum(map(len,blocks));blocks=canonical(blocks,d);units=_unitaries(units,d)
    ps=[np.diag([float(i in g) for i in range(d)]) for g in blocks]
    error=0.
    for u in units:
        costs=np.array([[np.linalg.norm(u@p@u.conj().T-q) for q in ps] for p in ps])
        assignment=np.argmin(costs,axis=1)
        error=max(error,float(max(costs[i,j] for i,j in enumerate(assignment))))
        if len(set(assignment.tolist()))!=len(blocks):error=max(error,1.)
    return error


def superoperator_leakage(blocks,units) -> float:
    k=keep(blocks).reshape(-1,order='F');error=0.
    for u in _unitaries(units,int(np.sqrt(len(k)))):
        c=np.kron(u.conj(),u)
        error=max(error,float(np.linalg.norm(c*k[:,None]*(~k)[None,:])))
    return error


def complete(initial,units) -> dict:
    d=sum(len(g) for g in initial) if isinstance(initial,(list,tuple)) else 0
    blocks=canonical(initial,d);units=_unitaries(units,d)
    directed=[x for u in units for x in (u,u.conj().T)]
    supports,support_info=_supports(directed)
    history=[blocks];merges=[]
    for round_id in range(d+1):
        parent=list(range(d))
        def root(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        def join(g):
            roots=sorted({root(int(i)) for i in g})
            for j in roots[1:]:parent[j]=roots[0]
            return len(roots)>1
        for g in blocks:join(g)
        for index,support in enumerate(supports):
            for block in blocks:
                # U† E_ij U, i,j in block, has all matrix-unit entries among
                # this row-support union. The old algebra includes E_kk.
                union=np.flatnonzero(np.any(support[block,:],axis=0)).tolist()
                if not union:raise ArithmeticError('unitary block has empty support')
                if join(union):
                    merges.append({'round':round_id+1,'motion_index':index//2,
                        'direction':'U' if index%2==0 else 'U_dagger',
                        'row_block':list(block),'column_support':union})
        next_blocks=canonical([[i for i in range(d) if root(i)==j]
                                for j in sorted({root(i) for i in range(d)})],d)
        if next_blocks==blocks:break
        blocks=next_blocks;history.append(blocks)
    else:raise ArithmeticError('finite partition completion failed to stabilize')
    normal=normalizer_error(blocks,units);leak=superoperator_leakage(blocks,units)
    if max(normal,leak)>CHECK_TOL:raise ArithmeticError('support completion fails independent operator closure')
    return {'initial_blocks':history[0],'final_blocks':blocks,'partition_history':history,
            'initial_dimension':dimension(history[0]),'final_dimension':dimension(blocks),
            'dimension_history':[dimension(p) for p in history],
            'added_hermitian_directions':dimension(blocks)-dimension(history[0]),
            'strict_completion_rounds':len(history)-1,'merge_witnesses':merges,
            'max_normalizer_error':normal,'max_superoperator_leakage':leak,'support':support_info}


def input_motions(family: str) -> list[np.ndarray]:
    motions=old.frozen_motions()
    if family=='all_six':return list(motions.values())
    if family not in motions:raise ValueError('unknown supplied motion family')
    return [motions[family]]


def label_motions(family: str) -> list[np.ndarray]:
    f=old.old.basis()
    return [f@u@f.conj().T for u in input_motions(family)]


@lru_cache(None)
def case(family: str,mask: str) -> dict:
    initial=[list(g) for g in old.old.groups(mask)]
    row=complete(initial,label_motions(family));row.update(family=family,mask=mask)
    row['initial_center_dimension']=len(row['initial_blocks'])
    row['final_center_dimension']=len(row['final_blocks'])
    row['old_center_preserved']=row['initial_blocks']==row['final_blocks']
    row['status']='UNCHANGED' if row['initial_dimension']==row['final_dimension'] else 'FULL_ALGEBRA_REQUIRED' if row['final_dimension']==256 else 'STRICT_PARTIAL_ENLARGEMENT'
    return row


def retain(rho: np.ndarray,blocks) -> np.ndarray:
    rho=np.asarray(rho,complex)
    if rho.shape!=(16,16) or not np.all(np.isfinite(rho)):raise ValueError('finite 16x16 operator required')
    f=old.old.basis()
    return f.conj().T@(keep(canonical(blocks,16))*(f@rho@f.conj().T))@f


def partitions(n: int):
    """All partitions for SMALL independent test cases only."""
    if type(n) is not int or not 1<=n<=6:raise ValueError('exhaustive helper limited to 1..6 labels')
    out=[[[0]]]
    for label in range(1,n):
        new=[]
        for p in out:
            new.append(p+[[label]])
            for j in range(len(p)):
                q=[list(g) for g in p];q[j].append(label);new.append(q)
        out=new
    return [canonical(p,n) for p in out]


def dense_witness(family: str) -> dict:
    """Direct certificate: E_ii (U† E_rr U) E_jj = q_ij E_ij.

    If every q_ij is nonzero, any algebra containing the diagonal units and
    this one conjugated projector is M_16. No inference from tiny zeros needed.
    """
    units=label_motions(family)
    candidate=max(((float(np.min(abs(u[row]))), index,row)
                   for index,u in enumerate(units) for row in range(16)))
    minimum,index,row=candidate
    if minimum<NONZERO_TOL:raise ValueError('no dense-row certificate in this family')
    u=units[index];q=np.outer(u[row].conj(),u[row]);error=0.
    for i in range(16):
        for j in range(16):
            ei=np.zeros((16,16));ej=ei.copy();ei[i,i]=1;ej[j,j]=1
            expected=np.zeros((16,16));expected[i,j]=1
            error=max(error,float(np.linalg.norm((ei@q@ej)/q[i,j]-expected)))
    return {'motion_index':index,'row_label':row,'minimum_row_amplitude':minimum,
            'minimum_projector_entry':float(np.min(abs(q))),
            'matrix_units_generated':256,'matrix_unit_reconstruction_error':error,
            'proof':'E_ii Q E_jj / Q_ij = E_ij for every i,j; all Q_ij are nonzero.'}


def controls() -> dict:
    u=old.control_unitary('mix');f=old.old.basis()
    completion=complete([list(g) for g in old.old.groups('1000')],[f@u@f.conj().T])
    a,b=old.old.phase_pair(0,8);e=lambda x:old.old.reduce_input(x,'1000')
    x=np.array([[0,1],[1,0]],complex);z=np.diag([1,-1]);i=np.eye(2)
    basis=np.stack([a.reshape(-1) for a in (i,x,z)],axis=1)/np.sqrt(2)
    product=(x@z).reshape(-1);residual=product-basis@(basis.conj().T@product)
    return {'mixing_completion_dimensions':completion['dimension_history'],
            'already_pruned_then_enlarged_distance':old.distance(retain(e(a),completion['final_blocks']),retain(e(b),completion['final_blocks'])),
            'kept_in_completed_algebra_distance':old.distance(retain(a,completion['final_blocks']),retain(b,completion['final_blocks'])),
            'linear_orbit_dimension':int(np.linalg.matrix_rank(basis)),
            'multiplicative_algebra_dimension':4,
            'linear_space_product_residual':float(np.linalg.norm(residual)),
            'scope':'Linear span {I,X,Z} is sufficient for a rotated Z expectation, but not closed under multiplication. Algebra minimality is a stronger requirement.'}


def verify_result(r: dict) -> None:
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(int,float)) and not isinstance(x,bool):
            if not np.isfinite(x):raise AssertionError('nonfinite audit value')
    finite(r)
    if len(r['cases'])!=112 or len({(c['family'],c['mask']) for c in r['cases']})!=112:raise AssertionError('incomplete coverage')
    if r['max_closure_error']>CHECK_TOL:raise AssertionError('closure failed')
    for row in r['cases']:
        if not contains(row['final_blocks'],row['initial_blocks']):raise AssertionError('not an enlargement')
        if max(row['max_normalizer_error'],row['max_superoperator_leakage'])>CHECK_TOL:raise AssertionError('unclosed candidate')
        if row['support']['max_discarded_entry']>ZERO_TOL or row['support']['min_retained_entry']<NONZERO_TOL:raise AssertionError('unresolved support')
    if r['physical_duration'] is not None or r['actual_record_selected'] is not None or r['new_physical_axioms']!=[]:raise AssertionError('claim boundary changed')
    if r['physical_pruning_law_derived'] or r['GOSM_derived']:raise AssertionError('unsupported physical claim')


@lru_cache(None)
def audit() -> dict:
    verify_baseline();families=[*old.frozen_motions(),'all_six']
    rows=[case(name,mask) for name in families for mask in old.old.masks()]
    summary={name:{key:sum(c['status']==key for c in rows if c['family']==name)
        for key in ('UNCHANGED','STRICT_PARTIAL_ENLARGEMENT','FULL_ALGEBRA_REQUIRED')} for name in families}
    r={'version':'v15.18','status':'EXECUTED_CONDITIONAL_MINIMAL_INVARIANT_ALGEBRA_COMPLETION',
       'scope_type':'MINIMAL_INVARIANT_UNITAL_STAR_ALGEBRA_FOR_SUPPLIED_MOTIONS',
       'cases':rows,'classification_by_family':summary,
       'max_closure_error':max(max(c['max_normalizer_error'],c['max_superoperator_leakage']) for c in rows),
       'controls':controls(),'full_algebra_certificate':dense_witness('pretime'),'physical_duration':None,'actual_record_selected':None,
       'new_physical_axioms':[],'physical_pruning_law_derived':False,'GOSM_derived':False,
       'Pillar_3':'OPEN','scientific_breakthrough':False,
       'numerical_scope':'Support gaps and operator residuals validate the computed partition; exact minimality follows for that support pattern. No symbolic proof of the input floating-point zeros is claimed.',
       'interpretation':'Information required BEFORE pruning to reproduce the supplied unpruned motions. No recovered information, new physical carrier, or replacement dynamics.'}
    verify_result(r);return r


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'outputs')
    args=p.parse_args();r=audit();args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'version':r['version'],'classification_by_family':r['classification_by_family'],
                      'max_closure_error':r['max_closure_error'],'controls':r['controls']},indent=2))

if __name__=='__main__':main()
