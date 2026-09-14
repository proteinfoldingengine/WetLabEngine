from __future__ import annotations
import importlib.util, pathlib, sys, hashlib
from functools import lru_cache
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v1526_base',ROOT/'baseline/selector_rank.py')
base=importlib.util.module_from_spec(spec);sys.modules['v1526_base']=base;spec.loader.exec_module(base)
TOL=1e-10
# Local development baseline formatting hash. The published branch replaces this
# with the exact v15.26 Git blob and its canonical hash.
BASELINE_BLOB='623defd0d8284e5d9cba6d8f8679de698e5202bc'


def _git_blob(path:pathlib.Path)->str:
    raw=path.read_bytes();return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()

def verify_baseline()->str:
    actual=_git_blob(ROOT/'baseline/selector_rank.py')
    if actual!=BASELINE_BLOB:raise ValueError('frozen v15.26 selector source changed')
    return actual

def vertex_to_face_average(c):
    A=np.zeros((len(c.faces),len(c.vertices)),float)
    for f,(x,y) in enumerate(c.faces):
        corners=((x,y),((x+1)%c.L,y),(x,(y+1)%c.L),((x+1)%c.L,(y+1)%c.L))
        for v in corners:A[f,c.vertex_index[v]]+=.25
    return A

def _alpha(alpha):
    if isinstance(alpha,bool) or not isinstance(alpha,(int,float,np.number)) or not np.isfinite(alpha):raise ValueError('finite real alpha required')
    return float(alpha)

def topological_cycle(c,q):
    q=np.asarray(q,float)
    if q.shape!=(len(c.vertices),) or not np.isfinite(q).all():raise ValueError('finite vertex source required')
    return c.B2@vertex_to_face_average(c)@q

def topological_target(c,q,alpha):
    a=_alpha(alpha);z=topological_cycle(c,q)
    return a*(base.response_operator(c)@z)

def topological_current(c,q,alpha):
    return base.reconstruct(c.B1,np.asarray(q,float),base.response_operator(c),topological_target(c,q,alpha))

def _spread(xs):
    return max(float(np.linalg.norm(a-b)) for i,a in enumerate(xs) for b in xs[i+1:]) if len(xs)>1 else 0.0

def _factorization_obstruction(B1,R):
    Z,_=base.cycle_basis(B1);RZ=R@Z;sv=np.linalg.svd(RZ,compute_uv=False)
    return {'dimension':int(np.linalg.matrix_rank(RZ,tol=TOL)),'witness_norm':float(sv[-1]),'rank':int(np.linalg.matrix_rank(RZ,tol=TOL))}

def _relabel_control(c,q,alpha=1.0):
    A=vertex_to_face_average(c);R=base.response_operator(c);j=topological_current(c,q,alpha);t=topological_target(c,q,alpha)
    rng=np.random.default_rng(1527);pv=rng.permutation(len(c.vertices));pe=rng.permutation(len(c.edges));pf=rng.permutation(len(c.faces))
    B1p=c.B1[pv][:,pe];B2p=c.B2[pe][:,pf];Ap=A[pf][:,pv];qp=q[pv]
    Hp=base.period_rows(c)[:,pe];Rp=np.vstack([B2p.T,Hp]);zp=B2p@Ap@qp;tp=float(alpha)*(Rp@zp)
    jp=base.reconstruct(B1p,qp,Rp,tp)
    expected_t=np.concatenate([t[:len(c.faces)][pf],t[len(c.faces):]])
    return max(float(np.linalg.norm(jp-j[pe])),float(np.linalg.norm(tp-expected_t)))

def _linearity_control(c,alpha=1.0):
    q1,_=base.base.incidence_defect(c,(0,0),'bottom',.7);q2,_=base.base.incidence_defect(c,(3,2),'right',-.4)
    j12=topological_current(c,q1+q2,alpha);js=topological_current(c,q1,alpha)+topological_current(c,q2,alpha)
    t12=topological_target(c,q1+q2,alpha);ts=topological_target(c,q1,alpha)+topological_target(c,q2,alpha)
    return max(float(np.linalg.norm(j12-js)),float(np.linalg.norm(t12-ts)))

def _homology_basis_control(c,q):
    R=base.response_operator(c);j=base.base.compatibility_response(c.B1,q).current;t=R@j;H=base.period_rows(c)
    M=np.array([[1.,1.],[1.,2.]])
    R2=np.vstack([c.B2.T,M@H]);t2=np.concatenate([t[:len(c.faces)],M@t[len(c.faces):]])
    j2=base.reconstruct(c.B1,q,R2,t2)
    return float(np.linalg.norm(j2-j)),float(np.linalg.norm(t2[-2:]-t[-2:]))

def verify_result(r):
    needed={'version','status','baseline_blob','response_target_factors_through_source','factorization_obstruction_dimension','factorization_witness_norm','inheritance_verdict','same_q_error','same_q_response_difference','microscopic_inheritance_quotient_covariant','microscopic_q_equivalence_error','microscopic_target_drift','hodge_metric_independent','hodge_weighted_current_difference','hodge_weighted_target_difference','zero_target_lawful','zero_target_derived','zero_target_vs_hodge_current_distance','topology_cycle_closure_error','topology_cycle_norm','topology_family_parameters','topology_family_max_source_error','topology_family_target_spread','topology_family_current_spread','topology_family_linearity_error','topology_family_quotient_error','topology_family_relabeling_error','multiple_covariant_target_laws_survive','covariance_selects_target','homology_basis_reconstruction_error','homology_target_coordinate_change','rank_gate_closes_given_target','max_reconstruction_error','metric_origin_status','response_rank_status','source_geometry_pairing_status','candidate_verdicts','uses_holonomy_as_selector','uses_newton_or_gr','uses_pruning','uses_entropy','uses_physical_time','selector_verdict','cycle_target_derived','signal_of_life','gravity_canary_certified','next_required_object','interpretation'}
    if set(r)!=needed:raise AssertionError('audit schema mismatch')
    def finite(x):
        if isinstance(x,dict):
            for v in x.values():finite(v)
        elif isinstance(x,list):
            for v in x:finite(v)
        elif isinstance(x,(int,float)) and not isinstance(x,bool) and not np.isfinite(x):raise AssertionError('nonfinite result')
    finite(r)
    if r['response_target_factors_through_source'] is not False or r['factorization_obstruction_dimension']!=50:raise AssertionError('factorization theorem')
    for k in ('same_q_error','microscopic_q_equivalence_error','topology_cycle_closure_error','topology_family_max_source_error','topology_family_linearity_error','topology_family_quotient_error','topology_family_relabeling_error','homology_basis_reconstruction_error','max_reconstruction_error'):
        if r[k]>=TOL:raise AssertionError(k)
    if not r['multiple_covariant_target_laws_survive'] or r['covariance_selects_target']:raise AssertionError('covariance family')
    if r['selector_verdict']!='PRETIME_CYCLE_TARGET_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY':raise AssertionError('verdict')
    if r['cycle_target_derived'] or r['signal_of_life'] or r['gravity_canary_certified']:raise AssertionError('claim boundary')
    if any(r[k] for k in ('uses_holonomy_as_selector','uses_newton_or_gr','uses_pruning,'uses_entropy','uses_physical_time')):raise AssertionError('forbidden selector')
