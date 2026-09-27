"""v15.81: source-component interference relative to a frozen P,Q decomposition."""
import importlib.util
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('signed80_interference',HERE.parent/'signed-cptp-tangents'/'gate.py')
V80=importlib.util.module_from_spec(spec);spec.loader.exec_module(V80)
V78=V80.V78;V75=V80.V75;M=V80.M
PP=M.F.op(3,0,0);QQ=M.F.op(1,1,0)
AP=(PP+QQ)/np.sqrt(2);AM=(PP-QQ)/np.sqrt(2)
UNITARIES=[np.eye(8),AP,AM,AP@AM]
LAMBDAS=[-1.,-.5,0.,.5,1.];DEPTHS=[1,2,4,8];STRENGTH=.1;ETA=1e-4
THRESHOLDS=[1e-9,1e-10,1e-11]


def dissipator(a,z):return a@z@a-.5*(a@a@z+z@a@a)
def cross(z):return .5*(PP@z@QQ+QQ@z@PP)
def generator(lam,z):return .5*(dissipator(PP,z)+dissipator(QQ,z))+lam*cross(z)


def weights(lam,u):
    plus=(1+np.exp(-(1+lam)*u))/2;minus=(1+np.exp(-(1-lam)*u))/2
    return np.array([plus*minus,(1-plus)*minus,plus*(1-minus),(1-plus)*(1-minus)])


def retained_factor(lam,u):return float(np.exp(-u)*np.sinh(lam*u))
def channel(lam,u,z):return sum(w*a@z@a.conj().T for w,a in zip(weights(lam,u),UNITARIES))
def retained(ys):return np.einsum('hij,rji->rh',ys,V75.G)
def extract(rho,ys):return V78.V77.extract(rho,ys)


def describe(a,reference):
    sv=np.linalg.svd(a,compute_uv=False)
    return {'norm':float(np.linalg.norm(a)),'reference':float(reference),'singular_values':sv.tolist(),
            'ranks':[int(np.count_nonzero(sv>t*reference)) for t in THRESHOLDS]}


def leading(a):return float(np.linalg.svd(a,compute_uv=False)[0])


def polar_domain(rho):
    rows=[];valid=True
    for c in M.correlations(rho):
        u,s,vh=np.linalg.svd(c);det=float(np.linalg.det(u@vh))
        ok=bool(det>0 and s.min()>=1e-4);valid=valid and ok
        rows.append({'singular_values':s.tolist(),'polar_determinant':det,'valid':ok})
    return {'valid':bool(valid),'edges':rows}


def adjudicate(valid,primary,finite):
    if not valid:return 'INVALID','INVALID'
    return ('MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED' if primary else 'MATCHED_COMPONENT_INTERFERENCE_RESPONSE_NOT_CONFIRMED',
            'FINITE_COMPONENT_INTERFERENCE_WINDOW_CONFIRMED' if finite else 'FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED')


def run_measurement():
    c={};mx=lambda k,v:V78.V77.maximize(c,k,v)
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    domain=M.domain([r['rho'] for r in selected]);hidden=np.array(M.HIDDEN)
    for a in [PP,QQ,AP,AM]:
        mx('source_hermiticity',np.linalg.norm(a-a.conj().T));mx('source_unitarity',np.linalg.norm(a.conj().T@a-np.eye(8)))
    mx('anticommutation',np.linalg.norm(PP@QQ+QQ@PP))
    units=[]
    for i in range(8):
        for j in range(8):
            z=np.zeros((8,8),complex);z[i,j]=1;units.append(z)
    for z in units:mx('adjoint_commutation',np.linalg.norm(AP@AM@z@AM.conj().T@AP.conj().T-AM@AP@z@AP.conj().T@AM.conj().T))
    cy=np.array([cross(h) for h in hidden]);cb=retained(cy);cb_ref=leading(cb)
    control_components=[];components_ok=True
    for name,a,expected in [('P',PP,18),('Q',QQ,12)]:
        ys=np.array([dissipator(a,h) for h in hidden]);norms=np.linalg.norm(ys,axis=(-2,-1));active=norms>1e-12
        mx('component_active_norm',np.max(np.abs(norms[active]-2)))
        mx('component_retained',np.linalg.norm(retained(ys)))
        components_ok=components_ok and int(active.sum())==expected
        control_components.append({'component':name,'active_count':int(active.sum()),'hidden_norms':norms.tolist()})
    input_pd=V75.density_diagnostics([r['rho']+sign*ETA*h for r in selected for h in hidden for sign in [-1,1]])
    gamma_ok=True;cp_ok=True;curves={};channel_rows=[];generator_rows=[];finite_rows=[];primary=True;finite=True;cross_ok=True;outputs_ok=True
    def get_curve(lam,n):
        nonlocal cp_ok
        key=(lam,n)
        if key in curves:return curves[key]
        u=STRENGTH*n;w=weights(lam,u)
        cp=V75.cp_diagnostics(V75.choi(lambda z:channel(lam,u,z)))
        cp_ok=cp_ok and cp['valid'] and bool(np.min(w)>=-1e-12 and abs(w.sum()-1)<=1e-12)
        raw=V78.transfer(lambda z:channel(lam,u,z));mx('channel_PTM_imaginary',np.max(np.abs(raw.imag)))
        s=raw.real;gl=generator_cache[lam]['ptm'];values,vectors=generator_cache[lam]['eigh']
        expm=(vectors*np.exp(u*values)[None,:])@vectors.T
        # All computational matrix-unit columns and output entries at once.
        diff=V80.V@(s-expm)@V80.V.conj().T
        mx('channel_exponential',np.max(np.abs(diff)))
        ys=np.array([channel(lam,u,h) for h in hidden]);b=retained(ys);factor=retained_factor(lam,u)
        mx('finite_retained_formula',np.max(np.abs(b-factor*cb)))
        entry={'ptm':s,'hidden':ys,'retained':b,'factor':factor,'weights':w}
        curves[key]=entry;channel_rows.append({'lambda':lam,'depth':n,'strength':u,'weights':w.tolist(),'Choi':cp})
        return entry
    generator_cache={}
    for lam in LAMBDAS:
        gamma=.5*np.array([[1,lam],[lam,1.]])
        gamma_ok=gamma_ok and np.linalg.eigvalsh(gamma).min()>=-1e-12 and abs(np.trace(gamma)-1)<=1e-12 and np.max(np.abs(np.diag(gamma)-.5))<=1e-12
        for z in units:
            alt=.5*(1+lam)*dissipator(AP,z)+.5*(1-lam)*dissipator(AM,z)
            mx('generator_decomposition',np.max(np.abs(generator(lam,z)-alt)))
        raw=V78.transfer(lambda z:generator(lam,z));mx('generator_PTM_imaginary',np.max(np.abs(raw.imag)))
        gl=raw.real;mx('generator_PTM_symmetry',np.linalg.norm(gl-gl.T))
        j=V75.choi(lambda z:generator(lam,z));mx('generator_Choi_hermiticity',np.linalg.norm(j-j.conj().T));mx('generator_trace_annihilation',np.linalg.norm(V75.trace_output(j)))
        mx('conditional_Choi_trace',abs(np.trace(V80.P@j@V80.P)-8))
        ys=np.array([generator(lam,h) for h in hidden]);b=retained(ys)
        mx('generator_retained_formula',np.max(np.abs(b-lam*cb)))
        generator_cache[lam]={'ptm':gl,'eigh':np.linalg.eigh((gl+gl.T)/2),'hidden':ys,'retained':b}
    for lam in LAMBDAS:
        for n in DEPTHS:get_curve(lam,n)
        for n in [1,2,4]:
            for m in [1,2,4]:
                diff=get_curve(lam,n)['ptm']@get_curve(lam,m)['ptm']-get_curve(lam,n+m)['ptm']
                mx('composition',np.max(np.abs(V80.V@diff@V80.V.conj().T)))
    for rec in selected:
        rho=rec['rho'];cq,ce,sy=extract(rho,cy);mx('sylvester',sy)
        cross_ok=cross_ok and describe(cb,cb_ref)['ranks']==[12]*3 and describe(cq,leading(cq))['ranks']==[6]*3 and describe(ce,leading(ce))['ranks']==[6]*3
        for edge in [1,2]:
            for a in [cq,ce]:cross_ok=cross_ok and describe(a[edge*3:edge*3+3],leading(a[edge*3:edge*3+3]))['ranks']==[3]*3
        cross_ok=cross_ok and np.linalg.norm(cq[:3])<=1e-12*np.linalg.norm(cq) and np.linalg.norm(ce[:3])<=1e-12*np.linalg.norm(ce)
        for lam in LAMBDAS:
            data=generator_cache[lam];q,e,sy=extract(rho,data['hidden']);mx('sylvester',sy)
            recon=np.einsum('rh,rij->hij',lam*cb,V75.G);rq,re,rsy=extract(rho,recon);mx('sylvester',rsy)
            mx('geometry_Q_reconstruction',np.max(np.abs(q-rq)));mx('geometry_E_reconstruction',np.max(np.abs(e-re)))
            qr=float(np.linalg.norm(q-lam*cq)/np.linalg.norm(cq));er=float(np.linalg.norm(e-lam*ce)/np.linalg.norm(ce))
            metrics={'retained':describe(data['retained'],cb_ref),'Q':describe(q,leading(cq)),'E':describe(e,leading(ce))}
            if lam==0:
                ok=all(x['ranks']==[0]*3 for x in metrics.values()) and all(np.linalg.norm(x)<=1e-12*np.linalg.norm(y) for x,y in [(data['retained'],cb),(q,cq),(e,ce)])
            else:ok=metrics['retained']['ranks']==[12]*3 and metrics['Q']['ranks']==[6]*3 and metrics['E']['ranks']==[6]*3
            ok=ok and qr<=1e-10 and er<=1e-10;primary=primary and ok
            generator_rows.append({'candidate_index':rec['candidate_index'],'lambda':lam,**metrics,'Q_scaling_error':qr,'E_scaling_error':er,'pass':bool(ok)})
            for n in DEPTHS:
                curve=get_curve(lam,n);u=STRENGTH*n;center=channel(lam,u,rho);ys=curve['hidden'];b=curve['retained'];bref=retained_factor(1,u)
                pd=V75.density_diagnostics([center]+[center+sign*ETA*h for h in ys for sign in [-1,1]])
                outputs_ok=outputs_ok and pd['valid'];pol=polar_domain(center)
                row={'candidate_index':rec['candidate_index'],'lambda':lam,'depth':n,'strength':u,'factor':curve['factor'],
                     'density':pd,'polar_domain':pol,'retained':describe(b,bref*cb_ref),'Q':None,'E':None,'edges':None,'pass':False}
                if not pol['valid']:
                    finite=False;row['reason']='finite center outside frozen proper-polar domain';finite_rows.append(row);continue
                fq,fe,sy=extract(center,ys);mx('sylvester',sy);qc,ec,csy=extract(center,cy);mx('sylvester',csy)
                recon=np.einsum('rh,rij->hij',curve['factor']*cb,V75.G);rq,re,rsy=extract(center,recon);mx('sylvester',rsy)
                mx('geometry_Q_reconstruction',np.max(np.abs(fq-rq)));mx('geometry_E_reconstruction',np.max(np.abs(fe-re)))
                row['Q']=describe(fq,bref*leading(qc));row['E']=describe(fe,bref*leading(ec));row['edges']=[]
                if lam==0:
                    ok=all(row[key]['ranks']==[0]*3 for key in ['retained','Q','E']) and all(np.linalg.norm(x)<=1e-12*bref*np.linalg.norm(y) for x,y in [(b,cb),(fq,qc),(fe,ec)])
                else:ok=row['retained']['ranks']==[12]*3 and row['Q']['ranks']==[6]*3 and row['E']['ranks']==[6]*3
                for edge in range(3):
                    r=slice(3*edge,3*edge+3);edge_info={'edge':list(M.EDGES[edge])}
                    for key,a,ref in [('Q',fq,qc),('E',fe,ec)]:
                        scale=bref*leading(ref[r]) if edge else bref*leading(ref)
                        edge_info[key]=describe(a[r],scale)
                        if edge==0:ok=ok and np.linalg.norm(a[r])<=1e-12*bref*np.linalg.norm(ref)
                        elif lam!=0:ok=ok and edge_info[key]['ranks']==[3]*3
                    row['edges'].append(edge_info)
                row['pass']=bool(ok);finite=finite and ok;finite_rows.append(row)
    limits={k:1e-12 for k in ['source_hermiticity','source_unitarity','anticommutation','adjoint_commutation','component_active_norm','component_retained','generator_decomposition','generator_PTM_imaginary','generator_PTM_symmetry','generator_Choi_hermiticity','generator_trace_annihilation','generator_retained_formula','channel_PTM_imaginary','channel_exponential','composition','finite_retained_formula']}
    limits.update(conditional_Choi_trace=1e-11,sylvester=1e-10,geometry_Q_reconstruction=1e-10,geometry_E_reconstruction=1e-10)
    valid=(indices==M.EXPECTED and domain['valid'] and input_pd['valid'] and outputs_ok and gamma_ok and cp_ok and components_ok and cross_ok and all(c[k]<=v for k,v in limits.items()))
    c.update(Gamma_valid=bool(gamma_ok),CP_valid=bool(cp_ok),component_activity_valid=bool(components_ok),cross_control_valid=bool(cross_ok),finite_density_valid=bool(outputs_ok))
    verdict,fv=adjudicate(valid,primary,finite)
    report={'version':'15.81','candidate_indices':indices,'lambdas':LAMBDAS,'depths':DEPTHS,'strength':STRENGTH,'eta':ETA,
            'all_valid':bool(valid),'verdict':verdict,'finite_verdict':fv,'controls':c,'reference_domain':domain,'input_positivity':input_pd,
            'components':control_components,'channels':channel_rows,'generator_rows':generator_rows,'finite_rows':finite_rows,
            'domain_exits':[{'candidate_index':r['candidate_index'],'lambda':r['lambda'],'depth':r['depth']} for r in finite_rows if not r['polar_domain']['valid']]}
    report=M.V70.finalize_report(report)
    if not report['all_valid']:report['finite_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False))
    sys.exit(0 if result['all_valid'] else 2)
