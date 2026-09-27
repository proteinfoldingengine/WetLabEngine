"""v15.72: preparation mixing of the unchanged memory-enriched null field."""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('memory71_mixture',HERE.parent/'memory-enriched-null'/'gate.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
H=M.HIDDEN[0]
ETA,DELTA,S=1e-4,1e-4,1e-3
WEIGHTS=[.25,.5,.75]
UNITARY=(np.eye(8)-1j*M.F.op(1,0,0))/np.sqrt(2)


def mixture_defect(fn,a,b,p):
    return p*fn(a)+(1-p)*fn(b)-fn(p*a+(1-p)*b)


def skew_coords(q):
    return np.array([(q[0,1]-q[1,0])/np.sqrt(2),
                     (q[0,2]-q[2,0])/np.sqrt(2),
                     (q[1,2]-q[2,1])/np.sqrt(2)])


def skew_column(rho,direction):
    one=M.moments(rho,M.ONE).reshape(3,3)
    done=M.moments(direction,M.ONE).reshape(3,3)
    dpair=M.moments(direction,M.PAIR).reshape(3,3,3)
    cols=[]
    for e,((i,j),c) in enumerate(zip(M.EDGES,M.correlations(rho))):
        dc=dpair[e]-np.outer(done[i],one[j])-np.outer(one[i],done[j])
        o=M.polar(c)[0]
        cols.extend(skew_coords(o.T@dc-dc.T@o))
    return np.asarray(cols)


def adjudicate(valid,normalized_defects,skew_pass):
    if not valid or not normalized_defects or not np.isfinite(normalized_defects).all():
        return 'INVALID','INVALID'
    obstructed=max(normalized_defects)>1e-6
    primary=('UNCONDITIONED_MIXTURE_AFFINITY_OBSTRUCTED' if obstructed
             else 'MIXTURE_AFFINITY_NOT_OBSTRUCTED_ON_PROBES')
    secondary=('PREPARATION_DEPENDENT_SKEW_CONFIRMED' if obstructed and skew_pass
               else 'PREPARATION_DEPENDENT_SKEW_NOT_CONFIRMED')
    return primary,secondary


def unitary(rho):
    return UNITARY@rho@UNITARY.conj().T


def rotation_difference(a,b):
    return max(float(np.linalg.norm(M.polar(ca)[0]-M.polar(cb)[0]))
               for ca,cb in zip(M.correlations(a),M.correlations(b)))


def measure(rho,v,label,index,p):
    a=rho+ETA*H+DELTA*v;b=rho-ETA*H-DELTA*v;r=p*a+(1-p)*b
    fa=M.field(a,H);fb=M.field(b,H);fr=M.field(r,H)
    j=p*fa+(1-p)*fb-fr
    ta=a+S*fa;tb=b+S*fb;tr=r+S*fr;pooled=p*ta+(1-p)*tb
    gap=pooled-tr
    normfactor=4*p*(1-p)*ETA*DELTA
    direction=j/normfactor
    column=skew_column(r,direction)
    identity=float(np.linalg.norm(gap-S*j))
    field_norm=float(np.linalg.norm(j))
    normalized=field_norm/normfactor
    memory_error=abs(p*M.memory(a,H)+(1-p)*M.memory(b,H)-M.memory(r,H))
    unitary_error=float(np.linalg.norm(mixture_defect(unitary,a,b,p)))
    unitary_activity=max(float(np.linalg.norm(unitary(x)-x)) for x in [a,b])
    hidden_only=float(np.linalg.norm(mixture_defect(lambda z:M.field(z,H),rho+ETA*H,rho-ETA*H,p)))
    visible_only=float(np.linalg.norm(mixture_defect(lambda z:M.field(z,H),rho+DELTA*v,rho-DELTA*v,p)))
    toy=mixture_defect(lambda z:M.memory(z,H)**2*v,a,b,p)
    expected_toy=4*p*(1-p)*ETA**2*v
    toy_norm=float(np.linalg.norm(toy))
    toy_error=float(np.linalg.norm(toy-expected_toy)/np.linalg.norm(expected_toy))
    approximation=None
    if p==.5:
        dy=M.lift_derivative(rho,v)
        approximation=float(np.linalg.norm(direction-dy)/max(1.,np.linalg.norm(dy)))
    branch_rotation=max(rotation_difference(a,ta),rotation_difference(b,tb))
    one_error=float(np.linalg.norm(M.moments(j,M.ONE)))
    trace_error=float(abs(np.trace(j)))
    dm=M.domain([rho,a,b,r,ta,tb,tr,pooled])
    valid=(dm['valid'] and abs(M.memory(rho,H))<=1e-12 and memory_error<=1e-12
           and identity<=1e-14 and one_error<=1e-12 and trace_error<=1e-12
           and unitary_error<=1e-12 and unitary_activity>1e-6
           and hidden_only<=1e-12 and visible_only<=1e-12
           and toy_error<=1e-8 and toy_norm>1e-10
           and (approximation is None or approximation<=1e-4))
    result={'candidate_index':index,'visible_label':list(label),'weight':p,
            'field_defect_norm':field_norm,'normalized_field_defect':normalized,
            'finite_update_gap_norm':float(np.linalg.norm(gap)),
            'finite_identity_error':identity,'memory_affinity_error':float(memory_error),
            'unitary_mixture_error':unitary_error,'unitary_activity':unitary_activity,
            'hidden_only_control':hidden_only,'visible_only_control':visible_only,
            'toy_norm':toy_norm,'toy_relative_error':toy_error,
            'midpoint_DY_verification_error':approximation,
            'individual_branch_rotation_change':branch_rotation,
            'J_one_body_residual':one_error,'J_trace_residual':trace_error,
            'polar_skew_column':column.tolist(),'domain':dm,
            'valid':bool(valid),'branch_null_pass':bool(branch_rotation<=1e-10)}
    result['valid']=bool(result['valid'] and M.finite_numbers(result))
    return result


def run_measurement():
    rows=[];rank_rows=[]
    try:
        states=M.V70.V64.ASYM.select_states()
        indices=[x['candidate_index'] for x in states]
        if indices!=M.EXPECTED:raise ValueError('state identity mismatch')
        for state in states:
            for p in WEIGHTS:
                group=[measure(state['rho'],v,label,state['candidate_index'],p)
                       for v,label in zip(M.VISIBLE,M.VISIBLE_LABELS)]
                rows.extend(group)
                matrix=np.column_stack([z['polar_skew_column'] for z in group])
                sv=np.linalg.svd(matrix,compute_uv=False)
                ranks=[int(np.sum(sv>sv[0]*tol)) for tol in [1e-9,1e-10,1e-11]]
                rank_rows.append({'candidate_index':state['candidate_index'],'weight':p,
                                  'common_pooled_base':bool(p==.5),
                                  'singular_values':sv.tolist(),'rank_sweep':ranks})
        valid=len(rows)==972 and len(rank_rows)==36 and all(z['valid'] for z in rows) and M.finite_numbers(rows+rank_rows)
        mid=[x for x in rank_rows if x['weight']==.5]
        skew_pass=len(mid)==12 and all(x['rank_sweep']==[9,9,9] for x in mid) and all(x['branch_null_pass'] for x in rows)
        verdict,secondary=adjudicate(valid,[x['normalized_field_defect'] for x in rows],skew_pass)
        return {'verdict':verdict,'skew_verdict':secondary,'all_valid':bool(valid),
                'candidate_indices':indices,'source_label':[1,1,1],'eta':ETA,'delta':DELTA,
                'source_strength':S,'mixture_weights':WEIGHTS,'rows':rows,'rank_rows':rank_rows,
                'numpy_version':np.__version__,'python_version':sys.version}
    except Exception as exc:
        return {'verdict':'INVALID','skew_verdict':'INVALID','all_valid':False,
                'error':repr(exc),'rows':rows,'rank_rows':rank_rows}


if __name__=='__main__':
    report=M.V70.finalize_report(run_measurement())
    if report['verdict']=='INVALID':report['skew_verdict']='INVALID'
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(2 if report['verdict']=='INVALID' else 0)
