from __future__ import annotations
import importlib.util, pathlib, sys
from functools import lru_cache
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v1525_base',ROOT/'baseline/pretime_gravity_canary.py')
base=importlib.util.module_from_spec(spec);sys.modules['v1525_base']=base;spec.loader.exec_module(base)
TOL=1e-10

def cycle_basis(B1):
    B1=np.asarray(B1,float)
    if B1.ndim!=2 or not np.isfinite(B1).all():raise ValueError('finite incidence required')
    _,s,vt=np.linalg.svd(B1,full_matrices=True);rank=int(np.sum(s>TOL))
    return vt[rank:].T,rank

def period_rows(c):
    H=np.zeros((2,c.B1.shape[1]))
    for e,(u,v,t) in enumerate(c.edges):
        if t=='h' and u[0]==0:H[0,e]=1
        if t=='v' and u[1]==0:H[1,e]=1
    return H

def response_operator(c):return np.vstack([c.B2.T,period_rows(c)])

def reconstruct(B1,q,R,target,particular=None):
    B1=np.asarray(B1,float);q=np.asarray(q,float);R=np.asarray(R,float);target=np.asarray(target,float)
    if B1.ndim!=2 or not np.isfinite(B1).all() or q.shape!=(B1.shape[0],) or not np.isfinite(q).all():raise ValueError('invalid source/incidence')
    if abs(float(q.sum()))>TOL:raise ValueError('neutral source required')
    if R.ndim!=2 or R.shape[1]!=B1.shape[1] or not np.isfinite(R).all() or target.shape!=(R.shape[0],) or not np.isfinite(target).all():raise ValueError('invalid response target')
    Z,_=cycle_basis(B1);RZ=R@Z
    if np.linalg.matrix_rank(RZ,tol=TOL)!=Z.shape[1]:raise ValueError('response operator does not resolve full cycle space')
    if particular is None:j0=np.linalg.lstsq(B1,-q,rcond=None)[0]
    else:
        j0=np.asarray(particular,float)
        if j0.shape!=(B1.shape[1],) or not np.isfinite(j0).all() or np.linalg.norm(B1@j0+q)>1e-8:raise ValueError('particular current must solve source equation')
    a=np.linalg.pinv(RZ,rcond=1e-13)@(target-R@j0);j=j0+Z@a
    if np.linalg.norm(B1@j+q)>1e-8 or np.linalg.norm(R@j-target)>1e-8:raise ArithmeticError('reconstruction failed')
    return j

def rank_summary(c):
    Z,rankB=cycle_basis(c.B1);Rf=c.B2.T;R=response_operator(c);sv=np.linalg.svd(R@Z,compute_uv=False)
    return {'rank_B1':rankB,'cycle_dimension':Z.shape[1],'face_boundary_rank':int(np.linalg.matrix_rank(c.B2,tol=TOL)),'homology_dimension':int(Z.shape[1]-np.linalg.matrix_rank(Rf@Z,tol=TOL)),'face_response_rank_on_cycle_space':int(np.linalg.matrix_rank(Rf@Z,tol=TOL)),'full_response_rank_on_cycle_space':int(np.linalg.matrix_rank(R@Z,tol=TOL)),'full_response_sigma_min':float(sv[-1])}

def current_residual(B,q,j):return float(np.linalg.norm(B@j+q))

@lru_cache(None)
def audit():
    c=base.torus_complex(7);q,delta=base.incidence_defect(c,(0,0),'bottom',1.0);R=response_operator(c);stats=rank_summary(c)
    jh=base.compatibility_response(c.B1,q).current;jlocal=-delta;far=base.farthest_face(c,(0,0));cycle=c.B2[:,c.face_index[far]];jshift=jh+0.25*cycle
    th=R@jh;tl=R@jlocal;ts=R@jshift
    rh=reconstruct(c.B1,q,R,th);rl=reconstruct(c.B1,q,R,tl);rs=reconstruct(c.B1,q,R,ts);rh2=reconstruct(c.B1,q,R,th,particular=jlocal)
    Z,_=cycle_basis(c.B1);face_rank=int(np.linalg.matrix_rank(c.B2.T@Z,tol=TOL));face_free=Z.shape[1]-face_rank
    stacked=np.vstack([c.B1,c.B2.T]);face_zero_nullity=c.B1.shape[1]-np.linalg.matrix_rank(stacked,tol=TOL)
    delta2=delta+c.B2[:,c.face_index[(2,3)]];q2=c.B1@delta2;micro_target=-R@delta;micro_target2=-R@delta2;micro=reconstruct(c.B1,q,R,micro_target)
    zero=np.zeros(R.shape[0]);jzero=reconstruct(c.B1,q,R,zero)
    rng=np.random.default_rng(1526);pv=rng.permutation(c.B1.shape[0]);pe=rng.permutation(c.B1.shape[1]);Bp=c.B1[pv][:,pe];B2p=c.B2[pe];Rp=np.vstack([B2p.T,period_rows(c)[:,pe]]);Zp,_=cycle_basis(Bp)
    sv0=np.sort(np.linalg.svd(R@Z,compute_uv=False));svp=np.sort(np.linalg.svd(Rp@Zp,compute_uv=False));perm_error=float(np.linalg.norm(sv0-svp))
    remote=lambda j:base.holonomy_defect(base.face_holonomy(c,j,far,.2,False))
    common=max(current_residual(c.B1,q,j) for j in (jh,jlocal,jshift,rh,rl,rs,jzero))
    return {'version':'v15.26','status':'PRETIME_RESPONSE_RANK_GATE_CLOSES_GIVEN_TARGET_TARGET_ORIGIN_OPEN',**stats,'face_response_residual_cycle_freedom':face_free,'face_zero_target_nullity':int(face_zero_nullity),'face_zero_target_not_unique':bool(face_zero_nullity==2),'hodge_reconstruction_error':float(np.linalg.norm(rh-jh)),'local_reconstruction_error':float(np.linalg.norm(rl-jlocal)),'cycle_shift_reconstruction_error':float(np.linalg.norm(rs-jshift)),'particular_section_invariance_error':float(np.linalg.norm(rh-rh2)),'hodge_vs_local_distance':float(np.linalg.norm(jh-jlocal)),'cycle_shift_vs_hodge_distance':float(np.linalg.norm(jshift-jh)),'max_common_source_residual':common,'hodge_remote_holonomy':remote(jh),'local_remote_holonomy':remote(jlocal),'cycle_shift_remote_holonomy':remote(jshift),'hodge_target_norm':float(np.linalg.norm(th)),'hodge_face_curl_norm':float(np.linalg.norm(c.B2.T@jh)),'hodge_period_target':(period_rows(c)@jh).tolist(),'local_target_norm':float(np.linalg.norm(tl)),'cycle_shift_target_norm':float(np.linalg.norm(ts)),'zero_full_target_current_distance_from_hodge':float(np.linalg.norm(jzero-jh)),'zero_full_target_remote_holonomy':remote(jzero),'microscopic_target_local_error':float(np.linalg.norm(micro-jlocal)),'microscopic_target_remote_holonomy':remote(micro),'equivalent_source_q_error':float(np.linalg.norm(q2-q)),'equivalent_source_target_difference':float(np.linalg.norm(micro_target2-micro_target)),'same_q_multiple_full_rank_targets':bool(np.linalg.norm(th-tl)>1e-4 and np.linalg.norm(th-ts)>1e-4),'rank_gate_closes_given_target':bool(stats['full_response_rank_on_cycle_space']==stats['cycle_dimension']),'rank_gate_supplies_target':False,'cycle_target_derived':False,'zero_target_is_additional_condition':True,'rank_gate_permutation_error':perm_error,'selector_verdict':'CYCLE_RESPONSE_TARGET_NOT_DERIVED','next_required_object':'PRETIME_SOURCE_TO_CYCLE_RESPONSE_TARGET_LAW','historical_response_rank_theorem':'CONSISTENT_WITH_V13_25_CONDITIONAL_RANK_RZ_CLOSURE','uses_metric_selector':False,'uses_pruning':False,'uses_entropy':False,'uses_physical_time':False,'fits_newton_or_gr':False,'physical_gravity_derived':False,'signal_of_life':False,'gravity_canary_certified':False,'interpretation':'Higher-incidence plus two homology-period response coordinates can resolve the complete cycle freedom without choosing an edge metric, but conservation/source data q do not supply their target values. Hodge, exact local cancellation, and cycle-shifted currents are all reconstructed exactly from different targets for the same q. The missing pre-time object is a source-to-cycle-response target law, not another pseudoinverse.'}

def main():
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,default=ROOT/'outputs');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);r=audit();(a.out/'verification.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n');print(json.dumps(r,indent=2,allow_nan=False))
if __name__=='__main__':main()
