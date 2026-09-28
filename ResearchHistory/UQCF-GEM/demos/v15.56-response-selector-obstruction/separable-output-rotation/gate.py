"""v15.91: separable outputs and invariant retained rotational response."""
import functools
import gzip
import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('interference81_separable',HERE.parent/'source-component-interference'/'gate.py')
V81=importlib.util.module_from_spec(spec);spec.loader.exec_module(V81)
M=V81.M;V75=V81.V75
LABELS=list(itertools.product(range(4),repeat=3))
BASIS=np.array([M.F.op(*x)/np.sqrt(8) for x in LABELS]);WEIGHTS=np.array([sum(i!=0 for i in x) for x in LABELS])
ATTENUATIONS=[1.,1/3,1/6,0.];LAMBDAS=[-1.,0.,1.];U=.1;ETA=1e-4
EXPECTED=[13,16,22,25,27,29,37,39,46,50,66,77]
CODE_HASH='eb44b9214844384bb5962e973711bfe31dc3d0038877063540e0b238879236be'
GZIP_HASH='6ec462e269a8cfd81b8cbd9312a2b613e8c802434b28dd2b38d3cbce4f37217d'
JSON_HASH='14d1fdac212d7373bddd3f450269a0c39dd0ae0d7937fa9356fe1acc64c646fc'


def symbolic_certificate():
    a=sp.symbols('a',real=True);I=sp.eye(2);pauli=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    effects=[];prepared=[]
    for p in pauli:
        for s in [-1,1]:effects.append((I+s*p)/6);prepared.append((I+3*a*s*p)/2)
    zero=lambda m:all(sp.simplify(x)==0 for x in m)
    checks={'povm_sum':zero(sum(effects,sp.zeros(2))-I)}
    for i in range(2):
        for j in range(2):
            z=sp.zeros(2);z[i,j]=1
            out=sum((sp.trace(e*z)*t for e,t in zip(effects,prepared)),sp.zeros(2))
            checks['matrix_unit_'+str(i)+str(j)]=zero(out-a*z-(1-a)*sp.trace(z)*I/2)
    for k,t in enumerate(prepared):
        checks['trace_'+str(k)]=sp.simplify(sp.trace(t)-1)==0
        checks['det_'+str(k)]=sp.simplify(t.det()-(1-9*a*a)/4)==0
    x,y,m,dx,dy,dm=sp.symbols('x y m dx dy dm',real=True)
    checks['connected_scaling']=sp.expand(a*a*m-(a*x)*(a*y)-a*a*(m-x*y))==0
    checks['tangent_scaling']=sp.expand(a*a*dm-(a*dx)*(a*y)-(a*x)*(a*dy)-a*a*(dm-dx*y-x*dy))==0
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def depolarize(z,a):
    coeff=np.einsum('ij,kji->k',z,BASIS)
    return np.einsum('k,kij->ij',coeff*a**WEIGHTS,BASIS)


def depolarize_many(zs,a):
    coeff=np.einsum('hij,kji->hk',zs,BASIS)
    return np.einsum('hk,kij->hij',coeff*a**WEIGHTS[None,:],BASIS)


def tensor3(items):return np.kron(np.kron(items[0],items[1]),items[2])


def measure_prepare(a):
    I=np.eye(2);effects=[];prepared=[]
    for p in M.PAULI:
        for sign in [-1,1]:effects.append((I+sign*p)/6);prepared.append((I+3*a*sign*p)/2)
    choices=list(itertools.product(range(6),repeat=3))
    return np.array([tensor3([effects[k] for k in x]) for x in choices]),np.array([tensor3([prepared[k] for k in x]) for x in choices])


def probabilities(zs,effects):return np.einsum('hij,kji->hk',zs,effects)


def reconstruct(weights,prepared):return np.einsum('hk,kij->hij',weights,prepared)


def domain(rho,a):
    edges=[];valid=True
    for c in M.correlations(rho):
        u,s,vh=np.linalg.svd(c);det=float(np.linalg.det(u@vh));ok=det>0 and s.min()>=a*a*1e-4
        edges.append({'singular_values':s.tolist(),'polar_determinant':det,'floor':a*a*1e-4,'valid':bool(ok)});valid=valid and ok
    return {'valid':bool(valid),'edges':edges}


def adjudicate(valid,response,zero):
    if not valid:return 'INVALID','INVALID'
    return ('SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_CONFIRMED' if response else 'SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_NOT_CONFIRMED',
            'ZERO_ATTENUATION_POLAR_UNDEFINED_CONFIRMED' if zero else 'ZERO_ATTENUATION_POLAR_UNDEFINED_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():return _run()


def _run():
    folder=HERE.parent/'source-component-interference';code=(folder/'gate.py').read_bytes();compressed=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(compressed);parent=json.loads(raw)
    parents=(hashlib.sha256(code).hexdigest()==CODE_HASH and hashlib.sha256(compressed).hexdigest()==GZIP_HASH and hashlib.sha256(raw).hexdigest()==JSON_HASH and
             parent['all_valid'] and parent['verdict']=='MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED' and parent['finite_verdict']=='FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED')
    archived={(r['candidate_index'],r['lambda']):r for r in parent['finite_rows'] if r['depth']==1 and r['lambda'] in LAMBDAS}
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected];hidden=np.array(M.HIDDEN)
    controls={};mx=lambda k,v:V81.V78.V77.maximize(controls,k,v)
    physical=[];input_physical=[];channels=[];source_channels=[];source_data={};rows=[];source_cases=[];response=True;zero_ok=True;archive_ranks=True
    units=[]
    for i in range(8):
        for j in range(8):
            z=np.zeros((8,8),complex);z[i,j]=1;units.append(z)
    units=np.array(units);effects,_=measure_prepare(0.);preps={};prep_diagnostics=[]
    mx('effect_completeness',np.max(np.abs(effects.sum(axis=0)-np.eye(8))))
    effect_min=float(min(np.linalg.eigvalsh(e).min() for e in effects))
    for a in ATTENUATIONS:
        if a>1/3:continue
        ee,pp=measure_prepare(a);preps[a]=pp;pd=V75.density_diagnostics(pp);prep_diagnostics.append({'a':a,**pd})
        reconstructed=reconstruct(probabilities(units,ee),pp);direct=depolarize_many(units,a)
        mx('matrix_unit_reconstruction',np.max(np.abs(reconstructed-direct)))
    for lam in LAMBDAS:
        ys=np.array([V81.channel(lam,U,h) for h in hidden]);source_data[lam]=ys
        source_channels.append({'lambda':lam,**V75.cp_diagnostics(V75.choi(lambda z:V81.channel(lam,U,z)))})
        for a in ATTENUATIONS:
            cp=V75.cp_diagnostics(V75.choi(lambda z:depolarize(V81.channel(lam,U,z),a)))
            channels.append({'lambda':lam,'a':a,**cp})
    min_probability=1.;max_probability_imag=0.
    for rec in selected:
        rho=rec['rho'];candidate=rec['candidate_index'];input_physical.extend([rho]+[rho+sign*ETA*h for h in hidden for sign in [-1,1]])
        base={}
        for lam in LAMBDAS:
            center=V81.channel(lam,U,rho);ys=source_data[lam];cs=np.array(M.correlations(center));dm=domain(center,1.)
            physical.extend([center]+[center+sign*ETA*y for y in ys for sign in [-1,1]])
            if dm['valid']:
                q,e,sy=V81.extract(center,ys);mx('sylvester',sy);os=np.array([M.polar(c)[0] for c in cs])
                for key,data in [('Q',q),('E',e)]:
                    saved=archived[candidate,lam][key];sv=np.linalg.svd(data,compute_uv=False)
                    mx('parent_metric_error',abs(np.linalg.norm(data)-saved['norm'])/max(1.,saved['norm']))
                    mx('parent_metric_error',np.max(np.abs(sv-saved['singular_values']))/max(1.,saved['singular_values'][0]))
                    archive_ranks=archive_ranks and V81.describe(data,saved['reference'])['ranks']==saved['ranks']
            else:q=e=os=None;response=False
            base[lam]={'center':center,'ys':ys,'C':cs,'domain':dm,'Q':q,'E':e,'O':os}
        plus=base[1.];cn=np.linalg.norm(plus['C']);qn=np.linalg.norm(plus['Q']) if plus['Q'] is not None else 1.;en=np.linalg.norm(plus['E']) if plus['E'] is not None else 1.
        qr=V81.leading(plus['Q']) if plus['Q'] is not None else 1.;er=V81.leading(plus['E']) if plus['E'] is not None else 1.
        for lam in LAMBDAS:
            b=base[lam];center=b['center'];ys=b['ys'];p=probabilities(np.concatenate([center[None],ys]),effects);pc=p[0];ph=p[1:]
            mx('probability_sum',abs(pc.sum()-1));mx('tangent_probability_sum',np.max(np.abs(ph.sum(axis=1))))
            max_probability_imag=max(max_probability_imag,float(np.max(np.abs(p.imag))))
            pmin=float(min(pc.real.min(),(pc.real[None,:]+ETA*ph.real).min(),(pc.real[None,:]-ETA*ph.real).min()));min_probability=min(min_probability,pmin)
            case_index=len(source_cases);source_cases.append({'candidate_index':candidate,'lambda':lam,'center_probabilities':pc.real.tolist(),'minimum_center_probe_probability':pmin,'domain':b['domain']})
            if lam!=0 and b['E'] is not None:response=response and np.linalg.norm(b['E'])>1e-6
            for a in ATTENUATIONS:
                out=depolarize(center,a);outys=depolarize_many(ys,a);cs=np.array(M.correlations(out))
                physical.extend([out]+[out+sign*ETA*y for y in outys for sign in [-1,1]])
                for obs,scale in [(M.ONE,a),(M.PAIR,a*a)]:
                    mx('moment_scaling',np.max(np.abs(np.einsum('hij,kji->hk',outys,obs)-scale*np.einsum('hij,kji->hk',ys,obs))))
                    mx('moment_scaling',np.max(np.abs(M.moments(out,obs)-scale*M.moments(center,obs))))
                if a<=1/3:
                    rebuilt=reconstruct(p,preps[a]);mx('center_tangent_reconstruction',np.max(np.abs(rebuilt-np.concatenate([out[None],outys]))))
                row={'candidate_index':candidate,'lambda':lam,'a':a,'source_case':case_index,'fully_separable_certificate':bool(a<=1/3),
                     'correlations':cs.tolist(),'correlation_norm':float(np.linalg.norm(cs)),'Q':None,'E':None,'Q_map':None,'E_map':None}
                if a==0:
                    err=max(float(np.linalg.norm(out-np.eye(8)/8)),float(np.linalg.norm(outys)),float(np.linalg.norm(cs)))
                    row.update(geometry_status='UNDEFINED_ZERO_CORRELATION',zero_error=err,pass_zero=bool(err<=1e-12));zero_ok=zero_ok and err<=1e-12;rows.append(row);continue
                dm=domain(out,a);row['domain']=dm
                if not dm['valid'] or not b['domain']['valid']:
                    response=False;row.update(geometry_status='OUTSIDE_FROZEN_POLAR_DOMAIN',pass_response=False);rows.append(row);continue
                q,e,sy=V81.extract(out,outys);mx('sylvester',sy);os=np.array([M.polar(c)[0] for c in cs])
                ce=float(np.linalg.norm(cs/(a*a)-b['C'])/cn);qe=float(np.linalg.norm(q/(a*a)-b['Q'])/qn);ee=float(np.linalg.norm(e-b['E'])/en);oe=float(np.linalg.norm(os-b['O']))
                qm=V81.describe(q,a*a*qr);em=V81.describe(e,er);ok=max(ce,qe,ee,oe)<=1e-9
                edges=[]
                for edge in range(3):
                    sl=slice(3*edge,3*edge+3);item={'edge':list(M.EDGES[edge]),'Q':V81.describe(q[sl],a*a*qr),'E':V81.describe(e[sl],er)}
                    if edge==0:ok=ok and np.linalg.norm(q[sl])<=1e-10*a*a*qr and np.linalg.norm(e[sl])<=1e-10*er
                    elif lam!=0:ok=ok and item['Q']['ranks']==[3]*3 and item['E']['ranks']==[3]*3
                    edges.append(item)
                if lam==0:ok=ok and qm['ranks']==[0]*3 and em['ranks']==[0]*3 and np.linalg.norm(q)<=1e-10*a*a*qn and np.linalg.norm(e)<=1e-10*en
                else:ok=ok and qm['ranks']==[6]*3 and em['ranks']==[6]*3
                response=response and ok;row.update(geometry_status='REGULAR',Q=qm,E=em,Q_map=q.tolist(),E_map=e.tolist(),edges=edges,
                    C_scaling_error=ce,Q_scaling_error=qe,E_invariance_error=ee,polar_factor_error=oe,pass_response=bool(ok));rows.append(row)
    physical_diag=V75.density_diagnostics(physical);input_diag=V75.density_diagnostics(input_physical);symbolic=symbolic_certificate()
    controls.update(parents_valid=bool(parents),archive_ranks_match=bool(archive_ranks),symbolic_certificate=symbolic,
                    minimum_effect_eigenvalue=effect_min,minimum_probability=min_probability,max_probability_imaginary=max_probability_imag,
                    prepared_states=prep_diagnostics,input_physicality=input_diag,source_output_physicality=physical_diag)
    limits={k:1e-12 for k in ['effect_completeness','matrix_unit_reconstruction','probability_sum','tangent_probability_sum','moment_scaling','center_tangent_reconstruction']}
    limits.update(parent_metric_error=1e-9,sylvester=1e-10)
    valid=(parents and indices==EXPECTED and symbolic['valid'] and archive_ranks and len(rows)==144 and all(x['valid'] for x in source_channels+channels+prep_diagnostics) and
           input_diag['valid'] and physical_diag['valid'] and effect_min>=-1e-12 and min_probability>=-1e-12 and max_probability_imag<=1e-12 and all(controls.get(k,0.)<=v for k,v in limits.items()))
    verdict,zv=adjudicate(valid,response,zero_ok)
    report={'version':'15.91','candidate_indices':indices,'source_strength':U,'eta':ETA,'attenuations':ATTENUATIONS,'lambdas':LAMBDAS,
            'all_valid':bool(valid),'response_predicate':bool(response),'zero_predicate':bool(zero_ok),'verdict':verdict,'zero_verdict':zv,
            'controls':controls,'source_channels':source_channels,'composite_channels':channels,'source_cases':source_cases,'rows':rows,
            'scope':'Fully separable outputs can preserve the specified polar rotational response; amplitudes shrink; no identity-anchored source flow or gravity law selected.',
            'sources':['https://arxiv.org/abs/quant-ph/0302032']}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['zero_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
