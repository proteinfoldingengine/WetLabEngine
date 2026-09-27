"""v15.75: fixed affine hidden response, with explicit CPTP controls."""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hamiltonian74_affine',HERE.parent/'hamiltonian-null-classification'/'gate.py')
V74=importlib.util.module_from_spec(spec);spec.loader.exec_module(V74)
M=V74.M
S,ETA,P_MIX,KAPPA=.1,1e-4,.37,.01
THETA=np.pi/4
G=np.concatenate([M.ONE,M.PAIR])/np.sqrt(8)
HIDDEN=np.array(M.HIDDEN)
OBS=np.concatenate([M.ONE,M.PAIR])


def choi(phi,d=8):
    blocks=[]
    for i in range(d):
        row=[]
        for j in range(d):
            z=np.zeros((d,d),complex);z[i,j]=1
            row.append(phi(z))
        blocks.append(row)
    return np.block(blocks)


def trace_output(j,d=8):return np.trace(j.reshape(d,d,d,d),axis1=1,axis2=3)


def cp_diagnostics(j):
    ev=np.linalg.eigvalsh((j+j.conj().T)/2)
    herm=float(np.linalg.norm(j-j.conj().T));tp=float(np.linalg.norm(trace_output(j)-np.eye(8)))
    return {'min_eigenvalue':float(ev.min()),'eigenvalues':ev.tolist(),'hermiticity_error':herm,'TP_error':tp,
            'valid':bool(ev.min()>=-1e-12 and herm<=1e-12 and tp<=1e-12)}


def density_diagnostics(states):
    ev=min(float(np.linalg.eigvalsh(z).min()) for z in states)
    tr=max(float(abs(np.trace(z)-1)) for z in states)
    he=max(float(np.linalg.norm(z-z.conj().T)) for z in states)
    return {'min_eigenvalue':ev,'trace_error':tr,'hermiticity_error':he,
            'valid':bool(ev>=-1e-12 and tr<=1e-12 and he<=1e-12)}


def adjudicate(valid,primary,secondary):
    if not valid:return 'INVALID','INVALID'
    return ('AFFINE_OPEN_NULL_RETAINED_CLOSED_CONFIRMED' if primary else 'AFFINE_RETAINED_NULL_NOT_EXCLUDED',
            'CPTP_POINTWISE_NULL_ONLY_CONFIRMED' if secondary else 'CPTP_POINTWISE_NULL_ONLY_NOT_CONFIRMED')


def finalize(report):
    result=M.V70.finalize_report(report)
    if result['verdict']=='INVALID':result['channel_verdict']='INVALID'
    return result


def run_measurement():
    controls={};rows=[];channel_rows=[];cases=0
    try:
        selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
        if indices!=M.EXPECTED:raise ValueError('frozen selector mismatch')
        controls['base_domain']=M.domain([r['rho'] for r in selected])
        fullbasis=np.concatenate([G,HIDDEN])
        gram=np.einsum('aij,bji->ab',fullbasis,fullbasis)
        controls['basis_gram_error']=float(np.linalg.norm(gram-np.eye(63)))
        retained=np.einsum('aij,kji->ak',G,OBS).real[:,None,:]
        hidden_retained=np.einsum('aij,kji->ak',HIDDEN,OBS).real[:,None,:]
        controls['sylvester']=0.;controls['hidden_output_Q_norm']=0.;controls['hidden_output_E_norm']=0.
        fq=[];fe=[];fqh=[];feh=[]
        for row in selected:
            q,e,sy=V74.geometry_from_retained(row['rho'],retained)
            qh,eh,sh=V74.geometry_from_retained(row['rho'],hidden_retained)
            controls['sylvester']=max(controls['sylvester'],sy,sh)
            controls['hidden_output_Q_norm']=max(controls['hidden_output_Q_norm'],float(np.linalg.norm(qh)))
            controls['hidden_output_E_norm']=max(controls['hidden_output_E_norm'],float(np.linalg.norm(eh)))
            rows.append({'candidate_index':row['candidate_index'],'Q':V74.summary(q),'E':V74.summary(e),'F_Q':q.tolist(),'F_E':e.tolist()})
            fq.append(q);fe.append(e);fqh.append(qh);feh.append(eh)
        qs=np.concatenate(fq);es=np.concatenate(fe)
        stacks={};expected=np.diag([0.]*36+[1.]*27)
        for name,a,hidden_maps in [('Q',qs,fqh),('E',es,feh)]:
            appended=np.concatenate([a,np.concatenate(hidden_maps)],axis=1)
            stats=V74.summary(a);ext=V74.summary(appended,stats['reference'])
            projector=V74.kernel_projector(appended,stats['reference'])
            stats.update(appended=ext,null_projector=projector.tolist(),projector_error=float(np.linalg.norm(projector-expected)))
            stacks[name]=stats
        # Freeze the reference lift ONCE, outside all state/channel input loops.
        yref=M.global_lift(selected[0]['rho']);a=M.F.op(1,1,1);ident=np.eye(8,dtype=complex)
        taup=ident/8+KAPPA*yref;taum=ident/8-KAPPA*yref
        mp=(ident+a)/2;mm=(ident-a)/2
        u=V74.V73.unitary(M.F.op(1,1,0),THETA)
        phis={'depolarizing':lambda z:np.trace(z)*ident/8,
              'entangling':lambda z:u@z@u.conj().T,
              'pointwise':lambda z:np.trace(z)*ident/8+KAPPA*np.trace(a@z)*yref}
        controls['prepared_states']=density_diagnostics([taup,taum])
        controls['Y_ref_norm_error']=float(abs(np.linalg.norm(yref)-np.sqrt(3/8)))
        controls['measure_prepare_error']=0.
        for i in range(8):
            for j in range(8):
                z=np.zeros((8,8),complex);z[i,j]=1
                controls['measure_prepare_error']=max(controls['measure_prepare_error'],float(np.linalg.norm(phis['pointwise'](z)-np.trace(mp@z)*taup-np.trace(mm@z)*taum)))
        channel_data={};channel_maps={};choi_ok=True
        for name,phi in phis.items():
            update=lambda z,f=phi:(1-S)*z+S*f(z)
            jp=choi(phi);jt=choi(update)
            cp=cp_diagnostics(jp);ct=cp_diagnostics(jt);choi_ok=choi_ok and cp['valid'] and ct['valid']
            ys=np.array([phi(h)-h for h in HIDDEN])
            raw=np.einsum('hij,kji->hk',ys,OBS).real[None,:,:]
            coeff=np.einsum('hij,kji->kh',ys,G).real
            channel_maps[name]=(ys,raw,coeff)
            channel_data[name]={'Phi_Choi':cp,'T_Choi':ct,'retained_coefficient_norm':float(np.linalg.norm(coeff)),
                                'retained_coefficients':coeff.tolist()}
            if name=='pointwise':controls['engineered_choi_error']=float(np.linalg.norm(jp-np.kron(ident,ident/8)-KAPPA*np.kron(a.T,yref)))
        controls.update(mixture_error=0.,hidden_secant_error=0.,direct_Q_error=0.,direct_E_error=0.)
        finite_min=1.;finite_trace=0.;finite_herm=0.;finite_ok=True
        point_q=[];point_e=[];positive_ok=True;null_ok=True
        for si,row in enumerate(selected):
            rho=row['rho'];state_maps={}
            for name,phi in phis.items():
                ys,raw,coeff=channel_maps[name]
                qv,ev,sy=V74.geometry_from_retained(rho,raw)
                q=qv.reshape(27,9).T;e=ev.reshape(27,9).T
                controls['sylvester']=max(controls['sylvester'],sy)
                controls['direct_Q_error']=max(controls['direct_Q_error'],float(np.max(np.abs(q-fq[si]@coeff))))
                controls['direct_E_error']=max(controls['direct_E_error'],float(np.max(np.abs(e-fe[si]@coeff))))
                state_maps[name]=(q,e)
                update=lambda z,f=phi:(1-S)*z+S*f(z)
                for hi,h in enumerate(HIDDEN):
                    plus=rho+ETA*h;minus=rho-ETA*h
                    tp=update(plus);tm=update(minus)
                    dd=density_diagnostics([plus,minus,tp,tm]);finite_ok=finite_ok and dd['valid']
                    finite_min=min(finite_min,dd['min_eigenvalue']);finite_trace=max(finite_trace,dd['trace_error']);finite_herm=max(finite_herm,dd['hermiticity_error'])
                    mix=update(P_MIX*plus+(1-P_MIX)*minus)-P_MIX*tp-(1-P_MIX)*tm
                    recovered=((tp-tm)/(2*ETA)-h)/S
                    controls['mixture_error']=max(controls['mixture_error'],float(np.linalg.norm(mix)))
                    controls['hidden_secant_error']=max(controls['hidden_secant_error'],float(np.linalg.norm(recovered-ys[hi])))
                    cases+=1
            entq,ente=state_maps['entangling'];depq,depe=state_maps['depolarizing'];pq,pe=state_maps['pointwise']
            unitq,unite=V74.summary(entq),V74.summary(ente)
            positive_ok=positive_ok and unitq['ranks']==[6]*3 and unite['ranks']==[6]*3
            nullq=float(np.linalg.norm(depq)/np.linalg.norm(entq));nulle=float(np.linalg.norm(depe)/np.linalg.norm(ente))
            null_ok=null_ok and nullq<=1e-12 and nulle<=1e-12
            point_q.append(pq);point_e.append(pe)
            channel_rows.append({'candidate_index':row['candidate_index'],'entangling_Q':unitq,'entangling_E':unite,
                                 'depolarizing_Q_relative':nullq,'depolarizing_E_relative':nulle,
                                 'pointwise_Q_norm':float(np.linalg.norm(pq)),'pointwise_E_norm':float(np.linalg.norm(pe)),
                                 'pointwise_Q_map':pq.tolist(),'pointwise_E_map':pe.tolist()})
        controls['finite_density']={'min_eigenvalue':finite_min,'trace_error':finite_trace,'hermiticity_error':finite_herm,'valid':bool(finite_ok)}
        leakage=channel_data['pointwise']['retained_coefficient_norm']
        secondary_metrics={'retained_norm':leakage,'anchor_Q_norm':float(np.linalg.norm(point_q[0])),
                           'anchor_E_norm':float(np.linalg.norm(point_e[0])),
                           'nonanchor_Q_norm':float(np.linalg.norm(np.concatenate(point_q[1:]))),
                           'nonanchor_E_norm':float(np.linalg.norm(np.concatenate(point_e[1:])))}
        secondary=leakage>1e-6 and all(secondary_metrics['anchor_'+k+'_norm']/leakage<=1e-10 and secondary_metrics['nonanchor_'+k+'_norm']/leakage>1e-6 for k in ['Q','E'])
        primary=all(d['ranks']==[36]*3 and d['appended']['ranks']==[36]*3 and d['projector_error']<=1e-8 for d in stacks.values())
        controls['per_state_rank9']=all(row[k]['ranks']==[9]*3 for row in rows for k in ['Q','E'])
        controls['entangling_rank6']=bool(positive_ok)
        controls['depolarizing_null']=bool(null_ok and channel_data['depolarizing']['retained_coefficient_norm']<=1e-12)
        limits={'basis_gram_error':1e-12,'sylvester':1e-10,'hidden_output_Q_norm':1e-12,'hidden_output_E_norm':1e-12,
                'Y_ref_norm_error':1e-12,'measure_prepare_error':1e-12,'engineered_choi_error':1e-12,
                'mixture_error':1e-12,'hidden_secant_error':1e-9,'direct_Q_error':1e-10,'direct_E_error':1e-10}
        valid=controls['base_domain']['valid'] and controls['prepared_states']['valid'] and finite_ok and choi_ok
        valid=valid and controls['per_state_rank9'] and positive_ok and controls['depolarizing_null'] and all(controls[k]<=v for k,v in limits.items())
        valid=valid and cases==972 and qs.shape==(108,36) and len(rows)==12 and len(channel_rows)==12
        verdict,channel_verdict=adjudicate(valid,primary,secondary)
        report={'verdict':verdict,'channel_verdict':channel_verdict,'all_valid':bool(valid),'primary_pass':bool(primary),'secondary_pass':bool(secondary),
                'candidate_indices':indices,'stack_shape':list(qs.shape),'finite_cases':cases,'rank_thresholds':V74.THRESHOLDS,
                's':S,'eta':ETA,'mixture_weight':P_MIX,'theta':THETA,'kappa':KAPPA,'anchor_candidate':indices[0],
                'Y_ref_real':yref.real.tolist(),'Y_ref_imag':yref.imag.tolist(),'hidden_labels':M.LABELS,
                'controls':controls,'states':rows,'stacked':stacks,'channels':channel_data,'channel_rows':channel_rows,'pointwise_metrics':secondary_metrics,
                'derived_operator_dimensions':{'rank':972,'nullity':729} if primary else None}
        return finalize(report)
    except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
        return finalize({'verdict':'INVALID','channel_verdict':'INVALID','all_valid':False,'error':str(exc),'controls':controls,'states':rows})

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(2 if r['verdict']=='INVALID' else 0)
