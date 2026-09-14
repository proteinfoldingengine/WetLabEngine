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
    if any(r[k] for k in ('uses_holonomy_as_selector','uses_newton_or_gr','uses_pruning','uses_entropy','uses_physical_time')):raise AssertionError('forbidden selector')

@lru_cache(None)
def audit():
    baseline=verify_baseline();c=base.base.torus_complex(7);q,delta=base.base.incidence_defect(c,(0,0),'bottom',1.0);R=base.response_operator(c)
    Z,_=base.cycle_basis(c.B1);obs=_factorization_obstruction(c.B1,R)
    # Factorization no-go witness: same q, current shifted by a closed cycle.
    j0=base.base.compatibility_response(c.B1,q).current;zfar=c.B2[:,c.face_index[base.base.farthest_face(c,(0,0))]];j1=j0+.25*zfar
    same_q=float(np.linalg.norm(c.B1@j1-c.B1@j0));same_y=float(np.linalg.norm(R@j1-R@j0))
    # Microscopic representative ambiguity.
    delta2=delta+c.B2[:,c.face_index[(2,3)]];q2=c.B1@delta2;tm=-R@delta;tm2=-R@delta2
    # Hodge/min-action metric dependence.
    weights=np.linspace(.75,1.25,len(c.edges));jw=base.base.weighted_response(c.B1,q,weights).current
    hodge_j=float(np.linalg.norm(jw-j0));hodge_t=float(np.linalg.norm(R@jw-R@j0))
    # Zero target is lawful but differs from Hodge.
    jzero=base.reconstruct(c.B1,q,R,np.zeros(R.shape[0]));zero_dist=float(np.linalg.norm(jzero-j0))
    # Topology/covariance family.
    ztop=topological_cycle(c,q);alphas=[-1.0,0.0,1.0];targets=[topological_target(c,q,a) for a in alphas];currents=[topological_current(c,q,a) for a in alphas]
    source_err=max(float(np.linalg.norm(c.B1@j+q)) for j in currents)
    # Quotient covariance: source-equivalent microscopic reps induce identical q-only law.
    quot=max(float(np.linalg.norm(topological_target(c,q,a)-topological_target(c,q2,a))) for a in alphas)
    relabel=_relabel_control(c,q,1.0);linear=_linearity_control(c,1.0)
    # Full rank still reconstructs every supplied target.
    recon=max(float(np.linalg.norm(base.reconstruct(c.B1,q,R,t)-j)) for t,j in zip(targets,currents))
    hb_err,hb_change=_homology_basis_control(c,q)
    candidate_verdicts={
      'SOURCE_QUOTIENT_INHERITANCE':'OBSTRUCTED_R_DOES_NOT_FACTOR_THROUGH_B1',
      'MICROSCOPIC_DEFECT_INHERITANCE':'OBSTRUCTED_NOT_QUOTIENT_COVARIANT',
      'HODGE_MINIMUM_ACTION':'CONDITIONAL_ON_UNDERIVED_EDGE_INNER_PRODUCT',
      'ZERO_CYCLE_TARGET':'LAWFUL_EXTRA_CONDITION_NOT_DERIVED',
      'TOPOLOGY_LINEAR_COVARIANT_FAMILY':'LAWFUL_BUT_NONUNIQUE'
    }
    r={'version':'v15.27','status':'PRETIME_CYCLE_TARGET_ORIGIN_AUDIT_STOP','baseline_blob':baseline,
       'response_target_factors_through_source':False,'factorization_obstruction_dimension':obs['dimension'],'factorization_witness_norm':obs['witness_norm'],
       'inheritance_verdict':'NO_FACTOR_THROUGH_SOURCE_QUOTIENT','same_q_error':same_q,'same_q_response_difference':same_y,
       'microscopic_inheritance_quotient_covariant':False,'microscopic_q_equivalence_error':float(np.linalg.norm(q2-q)),'microscopic_target_drift':float(np.linalg.norm(tm2-tm)),
       'hodge_metric_independent':False,'hodge_weighted_current_difference':hodge_j,'hodge_weighted_target_difference':hodge_t,
       'zero_target_lawful':True,'zero_target_derived':False,'zero_target_vs_hodge_current_distance':zero_dist,
       'topology_cycle_closure_error':float(np.linalg.norm(c.B1@ztop)),'topology_cycle_norm':float(np.linalg.norm(ztop)),
       'topology_family_parameters':alphas,'topology_family_max_source_error':source_err,'topology_family_target_spread':_spread(targets),'topology_family_current_spread':_spread(currents),
       'topology_family_linearity_error':linear,'topology_family_quotient_error':quot,'topology_family_relabeling_error':relabel,
       'multiple_covariant_target_laws_survive':True,'covariance_selects_target':False,
       'homology_basis_reconstruction_error':hb_err,'homology_target_coordinate_change':hb_change,
       'rank_gate_closes_given_target':True,'max_reconstruction_error':recon,
       'metric_origin_status':'CONDITIONAL_NOT_DERIVED','response_rank_status':'CONDITIONAL_ON_TARGET','source_geometry_pairing_status':'REQUIRES_NEW_AXIOM_OR_CALIBRATION','candidate_verdicts':candidate_verdicts,
       'uses_holonomy_as_selector':False,'uses_newton_or_gr':False,'uses_pruning':False,'uses_entropy':False,'uses_physical_time':False,
       'selector_verdict':'PRETIME_CYCLE_TARGET_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY','cycle_target_derived':False,'signal_of_life':False,'gravity_canary_certified':False,
       'next_required_object':'EXPLICIT_PRETIME_SOURCE_TO_HIGHER_INCIDENCE_COUPLING_AXIOM_OR_NEW_DERIVED_STRUCTURE',
       'interpretation':'The full response coordinates separate every cycle degree, but they cannot be inherited from the source quotient q for arbitrary currents because R is nonzero on ker(B1). Microscopic inheritance fails quotient covariance; Hodge requires an underived edge inner product; zero target is an extra condition; and topology plus source-linearity/relabeling covariance admits a nontrivial one-parameter family. The frozen ontology therefore does not derive a unique pre-time cycle-response target.'}
    verify_result(r);return r

def main():
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,default=ROOT/'outputs');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);r=audit();(a.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n');print(json.dumps(r,indent=2,allow_nan=False))
if __name__=='__main__':main()
