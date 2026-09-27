"""v15.76: finite powers of a frozen CPTP source; no fundamental time."""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('affine75_composition',HERE.parent/'affine-open-null'/'gate.py')
V75=importlib.util.module_from_spec(spec);spec.loader.exec_module(V75)
M=V75.M
S,KAPPA,ETA=.1,.01,1e-4
DEPTHS=[1,2,4,8]


def depth_coefficients(s,n):
    if n==0:return 1.,0.
    return (1-s)**n,n*s*(1-s)**(n-1)


def phi(z,b,y,a):return np.trace(z)*b+KAPPA*np.trace(a@z)*y


def power(z,b,y,a,n):
    out=z.copy()
    for _ in range(n):out=(1-S)*out+S*phi(out,b,y,a)
    return out


def closed(z,b,y,a,n):
    alpha,beta=depth_coefficients(S,n)
    return alpha*z+(1-alpha)*np.trace(z)*b+beta*KAPPA*np.trace(a@z)*y


def primary_verdict(valid,leakage,q,e):
    if not valid:return 'INVALID'
    if not all(x>1e-6 for x in leakage):return 'FROZEN_CHANNEL_FINITE_NULL_UNRESOLVED'
    if all(x<=1e-10 for x in q+e):return 'FROZEN_CHANNEL_FINITE_NULL_CONFIRMED'
    if any(x>=1e-6 and y>=1e-6 for x,y in zip(q,e)):return 'FROZEN_CHANNEL_FINITE_NULL_OBSTRUCTED'
    return 'FROZEN_CHANNEL_FINITE_NULL_UNRESOLVED'


def polar_domain(states):
    d=V75.density_diagnostics(states);sv=float('inf');pos=float('inf')
    for state in states:
        for c in M.correlations(state):
            _,p,s=M.polar(c);sv=min(sv,float(min(s)));pos=min(pos,float(np.linalg.eigvalsh((p+p.T)/2).min()))
    d.update(min_edge_singular=sv,min_positive_polar=pos)
    d['valid']=bool(d['valid'] and sv>=1e-4 and pos>0)
    return d


def final_report(r):
    out=M.V70.finalize_report(r)
    if out['verdict']=='INVALID':out['anchored_verdict']='INVALID'
    return out


def run_measurement():
    controls={};rows=[];cases=0
    try:
        selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
        if indices!=M.EXPECTED:raise ValueError('frozen state identity mismatch')
        rho=selected[0]['rho'];y=M.global_lift(rho);a=M.F.op(1,1,1);hidden=np.array(M.HIDDEN)
        cs0=M.correlations(rho);os0=np.array([M.polar(c)[0] for c in cs0]);bloch=M.moments(rho,M.ONE).reshape(3,3)
        bases={'original':np.eye(8,dtype=complex)/8,'anchored':rho.copy()}
        units=[]
        for i in range(8):
            for j in range(8):
                z=np.zeros((8,8),complex);z[i,j]=1;units.append(z)
        keys=['identity_error','Y_norm_error','phi_square_error','power_closed_error','composition_error',
              'center_closed_error','hidden_closed_error','retained_closed_error','active_leakage_error','inactive_retained_norm',
              'correlation_formula_error','closed_Q_error','closed_E_error','sylvester','skew_control_error']
        controls={k:0. for k in keys};controls['skew_control_min_E']=float('inf')
        controls['Y_norm_error']=float(abs(np.linalg.norm(y)-np.sqrt(3/8)))
        controls['identity_error']=max(float(abs(np.trace(y))),float(np.linalg.norm(y-y.conj().T)),float(abs(np.trace(a@y))))
        cp_ok=True;domain_ok=True
        cp_rows=[];prepared=[]
        norm_y=float(np.linalg.norm(y));ah=np.array([np.trace(a@h) for h in hidden])
        active=M.LABELS.index((1,1,1));inactive=[i for i in range(27) if i!=active]
        gcoeff=np.einsum('ij,kji->k',y,V75.G).real
        k=np.zeros((3,3));k[0,1]=1/np.sqrt(2);k[1,0]=-1/np.sqrt(2)
        for name,b in bases.items():
            controls['identity_error']=max(controls['identity_error'],float(abs(np.trace(b)-1)),float(np.linalg.norm(b-b.conj().T)),float(abs(np.trace(a@b))))
            pd=V75.density_diagnostics([b+KAPPA*y,b-KAPPA*y]);prepared.append({'channel':name,**pd});domain_ok=domain_ok and pd['valid']
            cphi=V75.cp_diagnostics(V75.choi(lambda z:phi(z,b,y,a)));cp_ok=cp_ok and cphi['valid']
            cp_rows.append({'channel':name,'operation':'Phi',**cphi})
            for z in units:
                controls['phi_square_error']=max(controls['phi_square_error'],float(np.linalg.norm(phi(phi(z,b,y,a),b,y,a)-np.trace(z)*b)))
                for n in DEPTHS:controls['power_closed_error']=max(controls['power_closed_error'],float(np.linalg.norm(power(z,b,y,a,n)-closed(z,b,y,a,n))))
                for n in [1,2,4]:
                    for m in [1,2,4]:
                        controls['composition_error']=max(controls['composition_error'],float(np.linalg.norm(power(power(z,b,y,a,m),b,y,a,n)-closed(z,b,y,a,n+m))))
            for n in DEPTHS:
                alpha,beta=depth_coefficients(S,n)
                cp=V75.cp_diagnostics(V75.choi(lambda z:power(z,b,y,a,n)));cp_ok=cp_ok and cp['valid']
                cp_rows.append({'channel':name,'operation':'T_power','depth':n,**cp})
                center=power(rho,b,y,a,n);zs=np.array([power(h,b,y,a,n) for h in hidden])
                zclosed=alpha*hidden+beta*KAPPA*ah[:,None,None]*y
                controls['center_closed_error']=max(controls['center_closed_error'],float(np.linalg.norm(center-(b+alpha*(rho-b)))))
                controls['hidden_closed_error']=max(controls['hidden_closed_error'],float(np.max(np.linalg.norm(zs-zclosed,axis=(-2,-1)))))
                raw=np.einsum('hij,kji->hk',zs,V75.OBS).real[None,:,:]
                coeff=np.einsum('hij,kji->kh',zs,V75.G).real
                expected_coeff=beta*KAPPA*gcoeff[:,None]*ah[None,:].real
                controls['retained_closed_error']=max(controls['retained_closed_error'],float(np.linalg.norm(coeff-expected_coeff)))
                controls['active_leakage_error']=max(controls['active_leakage_error'],float(abs(np.linalg.norm(coeff[:,active])-beta*KAPPA*np.sqrt(8)*norm_y)))
                controls['inactive_retained_norm']=max(controls['inactive_retained_norm'],float(np.linalg.norm(coeff[:,inactive])))
                qv,ev,sy=V75.V74.geometry_from_retained(center,raw)
                q=qv.reshape(27,9).T;e=ev.reshape(27,9).T
                controls['sylvester']=max(controls['sylvester'],sy)
                center_cs=M.correlations(center);center_os=np.array([M.polar(c)[0] for c in center_cs])
                pred_q=np.zeros((9,27));pred_e=np.zeros((9,27))
                for edge,(i,j) in enumerate(M.EDGES):
                    predicted_c=alpha*cs0[edge]+alpha*(1-alpha)*np.outer(bloch[i],bloch[j]) if name=='original' else cs0[edge]
                    controls['correlation_formula_error']=max(controls['correlation_formula_error'],float(np.linalg.norm(center_cs[edge]-predicted_c)))
                    o,_,_=M.polar(predicted_c)
                    for hi in range(27):
                        dc=beta*KAPPA*ah[hi].real*os0[edge]/np.sqrt(3)
                        qp=o.T@dc-dc.T@o;wp=o.T@M.polar_derivative(predicted_c,dc)
                        pred_q[3*edge:3*edge+3,hi]=V75.V74.V73.skew_coords(qp)
                        pred_e[3*edge:3*edge+3,hi]=V75.V74.V73.skew_coords(wp)
                    oc=center_os[edge];dc=oc@k;qc=oc.T@dc-dc.T@oc
                    ec=M.polar_derivative(center_cs[edge],dc)
                    controls['skew_control_error']=max(controls['skew_control_error'],float(abs(np.linalg.norm(qc)-2)))
                    controls['skew_control_min_E']=min(controls['skew_control_min_E'],float(np.linalg.norm(ec)))
                controls['closed_Q_error']=max(controls['closed_Q_error'],float(np.linalg.norm(q-pred_q)))
                controls['closed_E_error']=max(controls['closed_E_error'],float(np.linalg.norm(e-pred_e)))
                physical=[center];max_anchor_shift=0.;max_output_shift=0.
                for h in hidden:
                    for sign in [-1,1]:
                        z=rho+sign*ETA*h;out=power(z,b,y,a,n);physical.extend([z,out])
                        oo=np.array([M.polar(c)[0] for c in M.correlations(out)])
                        max_anchor_shift=max(max_anchor_shift,float(np.linalg.norm(oo-os0)))
                        max_output_shift=max(max_output_shift,float(np.linalg.norm(oo-center_os)))
                    cases+=1
                pd=polar_domain(physical);domain_ok=domain_ok and pd['valid']
                leakage=float(np.linalg.norm(coeff));qn=float(np.linalg.norm(q));en=float(np.linalg.norm(e))
                rows.append({'channel':name,'depth':n,'alpha':alpha,'beta':beta,'retained_norm':leakage,'Q_norm':qn,'E_norm':en,
                             'Q_ratio':qn/leakage,'E_ratio':en/leakage,'Q_map':q.tolist(),'E_map':e.tolist(),'retained_map':coeff.tolist(),
                             'center_real':center.real.tolist(),'center_imag':center.imag.tolist(),
                             'center_displacement':float(np.linalg.norm(center-rho)),
                             'center_polar_drift':float(np.linalg.norm(center_os-os0)),
                             'max_endpoint_polar_shift_from_anchor':max_anchor_shift,
                             'max_endpoint_polar_shift_from_output_center':max_output_shift,'domain':pd})
        limits={k:1e-12 for k in keys};limits.update(sylvester=1e-10,closed_Q_error=1e-10,closed_E_error=1e-10)
        valid=cp_ok and domain_ok and all(controls[k]<=v for k,v in limits.items()) and controls['skew_control_min_E']>1e-6
        valid=valid and cases==216 and len(rows)==8 and len(cp_rows)==10
        original=[r for r in rows if r['channel']=='original'];anchored=[r for r in rows if r['channel']=='anchored']
        verdict=primary_verdict(valid,[r['retained_norm'] for r in original],[r['Q_ratio'] for r in original],[r['E_ratio'] for r in original])
        anchored_ok=all(r['retained_norm']>1e-6 and r['Q_ratio']<=1e-10 and r['E_ratio']<=1e-10 and r['center_displacement']<=1e-12 and r['max_endpoint_polar_shift_from_anchor']<=1e-10 for r in anchored)
        av='INVALID' if not valid else ('ANCHOR_FIXED_CPTP_COMPOSITION_NULL_CONFIRMED' if anchored_ok else 'ANCHOR_FIXED_CPTP_COMPOSITION_NULL_NOT_CONFIRMED')
        first_visible=next((r['depth'] for r in original if r['Q_ratio']>=1e-6 and r['E_ratio']>=1e-6),None)
        return final_report({'verdict':verdict,'anchored_verdict':av,'all_valid':bool(valid),'candidate_indices':indices,'anchor_candidate':indices[0],
                             'depths':DEPTHS,'finite_cases':cases,'s':S,'eta':ETA,'kappa':KAPPA,'hidden_labels':M.LABELS,
                             'first_tested_visible_depth':first_visible,'controls':controls,'prepared_states':prepared,'Choi_checks':cp_rows,
                             'Y_ref_real':y.real.tolist(),'Y_ref_imag':y.imag.tolist(),'rows':rows})
    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
        return final_report({'verdict':'INVALID','anchored_verdict':'INVALID','all_valid':False,'error':str(exc),'controls':controls,'rows':rows})

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(2 if r['verdict']=='INVALID' else 0)
