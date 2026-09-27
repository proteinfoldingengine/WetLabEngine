"""v15.77: active retained baseline, fixed source calibration per reference."""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('composition76_active',HERE.parent/'cptp-null-composition'/'gate.py')
V76=importlib.util.module_from_spec(spec);spec.loader.exec_module(V76)
V75=V76.V75
M=V76.M
S,KAPPA,ETA,DELTA=.1,.01,1e-4,.02
DEPTHS=[1,2,4,8]
K=np.zeros((3,3));K[0,1]=1/np.sqrt(2);K[1,0]=-1/np.sqrt(2)


def skew_lift(o):return np.sqrt(3)/8*np.einsum('k,kij->ij',(o@K).ravel(),M.PAIR[:9])


def adjudicate(valid,primary,secondary):
    if not valid:return 'INVALID','INVALID'
    return ('ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_CONFIRMED' if primary else 'ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_NOT_CONFIRMED',
            'EQUAL_NORM_SKEW_BASELINE_VISIBLE_CONFIRMED' if secondary else 'EQUAL_NORM_SKEW_BASELINE_VISIBLE_NOT_CONFIRMED')


def maximize(c,k,v):c[k]=max(c.get(k,0.),float(v))
def minimize(c,k,v):c[k]=min(c.get(k,float('inf')),float(v))


def extract(center,ys):
    raw=np.einsum('hij,kji->hk',ys,V75.OBS).real[None,:,:]
    q,e,sy=V75.V74.geometry_from_retained(center,raw)
    return q.reshape(len(ys),9).T,e.reshape(len(ys),9).T,sy


def run_measurement():
    rows=[];refs=[];controls={};cases=0
    try:
        selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
        if indices!=M.EXPECTED:raise ValueError('frozen selector mismatch')
        hidden=np.array(M.HIDDEN);a=M.F.op(1,1,1);ah=np.array([np.trace(a@h) for h in hidden])
        active=M.LABELS.index((1,1,1));inactive=[i for i in range(27) if i!=active]
        units=[]
        for i in range(8):
            for j in range(8):
                u=np.zeros((8,8),complex);u[i,j]=1;units.append(u)
        physical_ok=True;cp_ok=True
        for reference in selected:
            rho=reference['rho'];cs0=M.correlations(rho);os0=np.array([M.polar(c)[0] for c in cs0])
            # These source tensors are calibrated once per reference, never per update.
            y=M.global_lift(rho);z=skew_lift(os0[0]);target_y=os0/np.sqrt(3)
            target_z=np.zeros((3,3,3));target_z[0]=np.sqrt(3)*os0[0]@K
            for tangent,target in [(y,target_y),(z,target_z)]:
                maximize(controls,'lift_identity_error',abs(np.trace(tangent)))
                maximize(controls,'lift_identity_error',np.linalg.norm(tangent-tangent.conj().T))
                maximize(controls,'lift_identity_error',np.linalg.norm(M.moments(tangent,M.ONE)))
                maximize(controls,'lift_identity_error',np.linalg.norm(np.einsum('ij,kji->k',tangent,hidden)))
                maximize(controls,'lift_norm_error',abs(np.linalg.norm(tangent)-np.sqrt(3/8)))
                maximize(controls,'lift_pair_error',np.linalg.norm(M.moments(tangent,M.PAIR).reshape(3,3,3)-target))
            maximize(controls,'A_moment_error',abs(np.trace(a@rho)))
            maximize(controls,'A_moment_error',abs(np.trace(a@y)))
            offsets={'fixed':np.zeros_like(rho),'active_symmetric':DELTA*y,'active_skew':DELTA*z}
            offset_pairs={'fixed':np.zeros((3,3,3)),'active_symmetric':DELTA*target_y,'active_skew':DELTA*target_z}
            gcoeff=np.einsum('ij,kji->k',y,V75.G).real
            refdata={'candidate_index':reference['candidate_index'],'Y_real':y.real.tolist(),'Y_imag':y.imag.tolist(),
                     'Z_real':z.real.tolist(),'Z_imag':z.imag.tolist(),'channels':{}}
            for name,offset in offsets.items():
                b=rho+offset
                maximize(controls,'A_moment_error',abs(np.trace(a@b)))
                baseline=V76.phi(rho,b,y,a)-rho
                baseline_coeff=np.einsum('ij,kji->k',baseline,V75.G).real
                baseline_norm=float(np.linalg.norm(baseline));baseline_ret=float(np.linalg.norm(baseline_coeff))
                maximize(controls,'baseline_field_error',np.linalg.norm(baseline-offset))
                qb,eb,sb=extract(rho,baseline[None,:,:]);maximize(controls,'sylvester',sb)
                if name!='fixed':
                    maximize(controls,'baseline_norm_error',abs(baseline_norm-DELTA*np.sqrt(3/8)))
                    maximize(controls,'baseline_norm_error',abs(baseline_ret-DELTA*np.sqrt(3/8)))
                if name=='active_skew':
                    maximize(controls,'skew_baseline_Q_error',abs(np.linalg.norm(qb)-2*np.sqrt(3)*DELTA))
                    minimize(controls,'skew_baseline_min_E',np.linalg.norm(eb))
                else:maximize(controls,'baseline_null_error',max(np.linalg.norm(qb),np.linalg.norm(eb)))
                pd=V75.density_diagnostics([b+KAPPA*y,b-KAPPA*y]);physical_ok=physical_ok and pd['valid']
                cp=V75.cp_diagnostics(V75.choi(lambda x:V76.phi(x,b,y,a)));cp_ok=cp_ok and cp['valid']
                channel={'baseline_norm':baseline_norm,'baseline_retained_norm':baseline_ret,
                         'baseline_Q_norm':float(np.linalg.norm(qb)),'baseline_E_norm':float(np.linalg.norm(eb)),
                         'prepared_states':pd,'Phi_Choi':cp,'power_Choi':[]}
                for u in units:
                    maximize(controls,'phi_square_error',np.linalg.norm(V76.phi(V76.phi(u,b,y,a),b,y,a)-np.trace(u)*b))
                    for n in DEPTHS:maximize(controls,'power_closed_error',np.linalg.norm(V76.power(u,b,y,a,n)-V76.closed(u,b,y,a,n)))
                    for n in [1,2,4]:
                        for m in [1,2,4]:maximize(controls,'composition_error',np.linalg.norm(V76.power(V76.power(u,b,y,a,m),b,y,a,n)-V76.closed(u,b,y,a,n+m)))
                for n in DEPTHS:
                    alpha,beta=V76.depth_coefficients(S,n)
                    cp=V75.cp_diagnostics(V75.choi(lambda x:V76.power(x,b,y,a,n)));cp_ok=cp_ok and cp['valid']
                    channel['power_Choi'].append({'depth':n,**cp})
                    center=V76.power(rho,b,y,a,n);ys=np.array([V76.power(h,b,y,a,n) for h in hidden])
                    maximize(controls,'center_closed_error',np.linalg.norm(center-(rho+(1-alpha)*offset)))
                    maximize(controls,'hidden_closed_error',np.max(np.linalg.norm(ys-(alpha*hidden+beta*KAPPA*ah[:,None,None]*y),axis=(-2,-1))))
                    coeff=np.einsum('hij,kji->kh',ys,V75.G).real
                    maximize(controls,'retained_closed_error',np.linalg.norm(coeff-beta*KAPPA*gcoeff[:,None]*ah[None,:].real))
                    maximize(controls,'active_leakage_error',abs(np.linalg.norm(coeff[:,active])-beta*KAPPA*np.sqrt(8)*np.linalg.norm(y)))
                    maximize(controls,'inactive_retained_norm',np.linalg.norm(coeff[:,inactive]))
                    q,e,sy=extract(center,ys);maximize(controls,'sylvester',sy)
                    cs=M.correlations(center);os=np.array([M.polar(c)[0] for c in cs]);pq=np.zeros((9,27));pe=np.zeros((9,27))
                    for edge in range(3):
                        predicted_c=cs0[edge]+(1-alpha)*offset_pairs[name][edge]
                        maximize(controls,'correlation_formula_error',np.linalg.norm(cs[edge]-predicted_c))
                        op,_,_=M.polar(predicted_c)
                        for hi in range(27):
                            dc=beta*KAPPA*ah[hi].real*os0[edge]/np.sqrt(3)
                            qp=op.T@dc-dc.T@op;wp=op.T@M.polar_derivative(predicted_c,dc)
                            pq[3*edge:3*edge+3,hi]=V75.V74.V73.skew_coords(qp)
                            pe[3*edge:3*edge+3,hi]=V75.V74.V73.skew_coords(wp)
                        dc=os[edge]@K;qc=os[edge].T@dc-dc.T@os[edge]
                        maximize(controls,'skew_control_Q_error',abs(np.linalg.norm(qc)-2))
                        minimize(controls,'skew_control_min_E',np.linalg.norm(M.polar_derivative(cs[edge],dc)))
                    maximize(controls,'closed_Q_error',np.linalg.norm(q-pq));maximize(controls,'closed_E_error',np.linalg.norm(e-pe))
                    physical=[center];shift=0.;hidden_shift=0.
                    for h in hidden:
                        for sign in [-1,1]:
                            input_state=rho+sign*ETA*h;out=V76.power(input_state,b,y,a,n);physical.extend([input_state,out])
                            oo=np.array([M.polar(c)[0] for c in M.correlations(out)])
                            shift=max(shift,float(np.linalg.norm(oo-os0)));hidden_shift=max(hidden_shift,float(np.linalg.norm(oo-os)))
                        cases+=1
                    dm=V76.polar_domain(physical);physical_ok=physical_ok and dm['valid']
                    leakage=float(np.linalg.norm(coeff));qn=float(np.linalg.norm(q));en=float(np.linalg.norm(e))
                    rec={'candidate_index':reference['candidate_index'],'channel':name,'depth':n,'alpha':alpha,'beta':beta,
                         'baseline_norm':baseline_norm,'baseline_retained_norm':baseline_ret,'retained_norm':leakage,
                         'Q_norm':qn,'E_norm':en,'Q_ratio':qn/leakage,'E_ratio':en/leakage,
                         'center_displacement':float(np.linalg.norm(center-rho)),'center_polar_drift':float(np.linalg.norm(os-os0)),
                         'max_endpoint_polar_shift_from_anchor':shift,'max_endpoint_polar_shift_from_output_center':hidden_shift,
                         'Q_map':q.tolist(),'E_map':e.tolist(),'retained_map':coeff.tolist(),'domain':dm}
                    rows.append(rec)
                refdata['channels'][name]=channel
            refs.append(refdata)
        fixed=[r for r in rows if r['channel']=='fixed'];active_rows=[r for r in rows if r['channel']=='active_symmetric'];skew_rows=[r for r in rows if r['channel']=='active_skew']
        fixed_ok=all(r['center_displacement']<=1e-12 and r['retained_norm']>1e-6 and r['Q_ratio']<=1e-10 and r['E_ratio']<=1e-10 and r['max_endpoint_polar_shift_from_anchor']<=1e-10 for r in fixed)
        controls['fixed_control_pass']=bool(fixed_ok)
        limits={k:1e-12 for k in controls if k not in ['skew_baseline_min_E','skew_control_min_E','fixed_control_pass']}
        limits.update(baseline_null_error=1e-10,sylvester=1e-10,closed_Q_error=1e-10,closed_E_error=1e-10)
        valid=physical_ok and cp_ok and fixed_ok and all(controls[k]<=v for k,v in limits.items())
        valid=valid and controls['skew_baseline_min_E']>1e-6 and controls['skew_control_min_E']>1e-6
        valid=valid and cases==3888 and len(rows)==144 and len(refs)==12 and all(len(rs)==48 for rs in [fixed,active_rows,skew_rows])
        primary=all(r['baseline_norm']>1e-6 and r['baseline_retained_norm']>1e-6 and r['center_displacement']>1e-6 and r['retained_norm']>1e-6 and r['Q_ratio']<=1e-10 and r['E_ratio']<=1e-10 and r['max_endpoint_polar_shift_from_anchor']<=1e-10 for r in active_rows)
        secondary=all(r['retained_norm']>1e-6 and r['Q_ratio']>=1e-6 and r['E_ratio']>=1e-6 for r in skew_rows)
        verdict,skew_verdict=adjudicate(valid,primary,secondary)
        report={'verdict':verdict,'skew_verdict':skew_verdict,'all_valid':bool(valid),'primary_pass':bool(primary),'skew_pass':bool(secondary),
                'candidate_indices':indices,'finite_cases':cases,'depths':DEPTHS,'s':S,'eta':ETA,'kappa':KAPPA,'delta':DELTA,
                'hidden_labels':M.LABELS,'controls':controls,'references':refs,'rows':rows}
        out=M.V70.finalize_report(report)
        if out['verdict']=='INVALID':out['skew_verdict']='INVALID'
        return out
    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
        return M.V70.finalize_report({'verdict':'INVALID','skew_verdict':'INVALID','all_valid':False,'error':str(exc),'controls':controls,'rows':rows})

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(2 if r['verdict']=='INVALID' else 0)
