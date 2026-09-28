"""v15.92: fixed preparation affine span and regular polar obstruction."""
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
spec=importlib.util.spec_from_file_location('separable91_span',HERE.parent/'separable-output-rotation'/'gate.py')
V91=importlib.util.module_from_spec(spec);spec.loader.exec_module(V91)
V81=V91.V81;V75=V91.V75;M=V91.M
THRESHOLDS=[1e-9,1e-10,1e-11];ETA=1e-4;U=.1;LAMBDAS=[-1.,0.,1.]
CODE_HASH='fb3f26902f624c1a22008c015c4ea8216241eb4c99d89dddbf422f7481afc32d'
GZIP_HASH='1e38de1e7e1474e4d14546f722c3ab5013bf347fb02f72ab91bb43115a6da984'
JSON_HASH='9c848c70134adbb62e70c988dc35001834bccf3c78a0539b294e6ce60167bca9'


def exact_arms():
    I=sp.eye(2);P=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    arms={}
    for name,axes,T in [('isotropic',[0,1,2],sp.eye(3)/3),('plane',[0,1],sp.diag(sp.Rational(1,2),sp.Rational(1,2),0)),('line',[2],sp.diag(0,0,1))]:
        prepared=[(I+s*P[k])/2 for k in axes for s in [-1,1]]
        effects=[v/len(axes) for v in prepared]
        arms[name]=(T,sp.zeros(3,1),effects,prepared)
    arms['point']=(sp.zeros(3),sp.Matrix([0,sp.Rational(1,2),0]),[I],[(I+P[1]/2)/2])
    return P,arms


def symbolic_certificate():
    P,arms=exact_arms();checks={};zero=lambda m:all(sp.expand(x)==0 for x in m)
    for name,(T,t,effects,prepared) in arms.items():
        for i in range(2):
            for j in range(2):
                z=sp.zeros(2);z[i,j]=1
                v=sp.Matrix([sp.trace(p*z) for p in P]);action=sp.trace(z)*sp.eye(2)/2+sum(((T*v+t*sp.trace(z))[k]*P[k]/2 for k in range(3)),sp.zeros(2))
                mpout=sum((sp.trace(e*z)*tau for e,tau in zip(effects,prepared)),sp.zeros(2))
                checks[name+'_unit'+str(i)+str(j)]=zero(action-mpout)
        checks[name+'_effects']=zero(sum(effects,sp.zeros(2))-sp.eye(2))
        checks[name+'_trace']=all(sp.trace(v)==1 for v in prepared)
        checks[name+'_positive']=all(zero(v-v.H) and v[0,0]>=0 and v[1,1]>=0 and v.det()>=0 for v in prepared)
        vectors=[sp.Matrix([sp.trace(p*v) for p in P]) for v in prepared]
        checks[name+'_span']=sp.Matrix.hstack(*(v-vectors[0] for v in vectors)).rank()=={'isotropic':3,'plane':2,'line':1,'point':0}[name]
        comm=[sp.simplify(sp.trace((x*y-y*x).H*(x*y-y*x))) for x in prepared for y in prepared]
        checks[name+'_commutator']=max(comm)==(sp.Rational(1,2) if name in ['isotropic','plane'] else 0)
    T=sp.Matrix(3,3,lambda i,j:sp.Symbol('T'+str(i)+str(j)));S=sp.Matrix(3,3,lambda i,j:sp.Symbol('S'+str(i)+str(j)))
    A=sp.Matrix(3,3,lambda i,j:sp.Symbol('m'+str(i)+str(j)))
    vec=lambda prefix:sp.Matrix(sp.symbols(prefix+'0:3'))
    x,y,t,u=[vec(v) for v in ['x','y','t','u']]
    new=T*A*S.T+(T*x)*u.T+t*(S*y).T+t*u.T-(T*x+t)*(S*y+u).T
    residual=new-T*(A-x*y.T)*S.T
    for i in range(3):
        for j in range(3):checks['connected_'+str(i)+str(j)]=sp.expand(residual[i,j])==0
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def numeric_arms():
    _,exact=exact_arms();out={}
    convert=lambda x:np.array(x.tolist(),complex)
    for name,(T,t,effects,prepared) in exact.items():
        T=convert(T).real;t=convert(t).real.ravel();e=np.array([convert(x) for x in effects]);p=np.array([convert(x) for x in prepared])
        R=np.zeros((4,4));R[0,0]=1;R[1:,0]=t;R[1:,1:]=T
        choices=list(itertools.product(range(len(p)),repeat=3))
        glob_e=np.array([V91.tensor3([e[k] for k in c]) for c in choices]);glob_p=np.array([V91.tensor3([p[k] for k in c]) for c in choices])
        vectors=np.einsum('aij,kji->ak',p,np.array(M.PAULI)).real
        span=int(np.linalg.matrix_rank(vectors-vectors[0],tol=1e-12));comm=max(float(np.linalg.norm(x@y-y@x)**2) for x in p for y in p)
        out[name]={'T':T,'t':t,'R':V91.tensor3([R,R,R]),'effects':glob_e,'prepared':glob_p,'span':span,'commutator':comm}
    return out


def apply_many(zs,R):
    coeff=np.einsum('hij,kji->hk',zs,V91.BASIS)
    return np.einsum('hk,kij->hij',coeff@R.T,V91.BASIS)


def edge_record(C,reference):
    u,s,vh=np.linalg.svd(C);ranks=[int(np.count_nonzero(s>t*reference)) for t in THRESHOLDS];mask=s>THRESHOLDS[1]*reference
    V=(u*mask[None,:])@vh;P=V.T@V;F=V@V.T
    error=max(float(np.linalg.norm(P@P-P)),float(np.linalg.norm(F@F-F)),float(np.linalg.norm(C-V@(V.T@C))))
    return {'correlation':C.tolist(),'singular_values':s.tolist(),'reference':float(reference),'ranks':ranks,'support_rank':int(mask.sum()),'support_polar':V.tolist(),'initial_projector':P.tolist(),'final_projector':F.tolist(),'support_residual':error}


def adjudicate(valid,span,noncommuting):
    if not valid:return 'INVALID','INVALID'
    return ('PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_CONFIRMED' if span else 'PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_NOT_CONFIRMED',
            'NONCOMMUTING_PREPARATIONS_INSUFFICIENT_CONFIRMED' if noncommuting else 'NONCOMMUTING_PREPARATIONS_INSUFFICIENT_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():return _run()


def _run():
    folder=HERE.parent/'separable-output-rotation';code=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    parents=(hashlib.sha256(code).hexdigest()==CODE_HASH and hashlib.sha256(gz).hexdigest()==GZIP_HASH and hashlib.sha256(raw).hexdigest()==JSON_HASH and parent['all_valid'] and
             parent['verdict']=='SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_CONFIRMED' and parent['zero_verdict']=='ZERO_ATTENUATION_POLAR_UNDEFINED_CONFIRMED')
    saved={(r['candidate_index'],r['lambda']):r for r in parent['rows'] if r['a']==1/3}
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected];hidden=np.array(M.HIDDEN);arms=numeric_arms()
    controls={};mx=lambda k,v:V81.V78.V77.maximize(controls,k,v)
    source_channels=[];composite=[];locals=[];rows=[];inputs=[];physical=[];source_tangents={};effect_min=1.;prob_min=1.;span_ok=True;noncommuting=True
    units=[]
    for i in range(8):
        for j in range(8):
            z=np.zeros((8,8),complex);z[i,j]=1;units.append(z)
    units=np.array(units)
    for name,a in arms.items():
        effects=a['effects'];prepared=a['prepared'];pd=V75.density_diagnostics(prepared)
        mx('effect_completeness',np.max(np.abs(effects.sum(axis=0)-np.eye(8))));mx('effect_hermiticity',np.max(np.abs(effects-effects.conj().transpose(0,2,1))))
        effect_min=min(effect_min,float(min(np.linalg.eigvalsh(e).min() for e in effects)))
        direct=apply_many(units,a['R']);weights=V91.probabilities(units,effects);rebuilt=V91.reconstruct(weights,prepared)
        mx('matrix_unit_reconstruction',np.max(np.abs(direct-rebuilt)))
        locals.append({'arm':name,'T':a['T'].tolist(),'t':a['t'].tolist(),'preparation_affine_dimension':a['span'],'max_squared_commutator_norm':a['commutator'],'outcomes':len(prepared),'prepared_states':pd})
    for lam in LAMBDAS:
        ys=np.array([V81.channel(lam,U,h) for h in hidden]);source_tangents[lam]=ys
        source_channels.append({'lambda':lam,**V75.cp_diagnostics(V75.choi(lambda z:V81.channel(lam,U,z)))})
        for name,a in arms.items():
            J=V75.choi(lambda z:apply_many(V81.channel(lam,U,z)[None],a['R'])[0]);composite.append({'lambda':lam,'arm':name,**V75.cp_diagnostics(J)})
    for rec in selected:
        rho=rec['rho'];candidate=rec['candidate_index'];inputs.extend([rho]+[rho+sign*ETA*h for h in hidden for sign in [-1,1]])
        for lam in LAMBDAS:
            center=V81.channel(lam,U,rho);ys=source_tangents[lam];zs=np.concatenate([center[None],ys]);source_C=np.array(M.correlations(center));one=M.moments(center,M.ONE).reshape(3,3)
            physical.extend([center]+[center+sign*ETA*h for h in ys for sign in [-1,1]])
            for name,a in arms.items():
                transformed=apply_many(zs,a['R']);out=transformed[0];outys=transformed[1:];T=a['T'];t=a['t'];C=np.array(M.correlations(out));outone=M.moments(out,M.ONE).reshape(3,3)
                physical.extend([out]+[out+sign*ETA*h for h in outys for sign in [-1,1]])
                w=V91.probabilities(zs,a['effects']);rebuilt=V91.reconstruct(w,a['prepared']);mx('center_tangent_reconstruction',np.max(np.abs(transformed-rebuilt)))
                mx('probability_imaginary',np.max(np.abs(w.imag)));mx('probability_sum',abs(w[0].sum()-1));mx('tangent_probability_sum',np.max(np.abs(w[1:].sum(axis=1))))
                pmin=float(min(w[0].real.min(),(w[0].real[None,:]+ETA*w[1:].real).min(),(w[0].real[None,:]-ETA*w[1:].real).min()));prob_min=min(prob_min,pmin)
                mx('affine_one_body',np.max(np.abs(outone-(one@T.T+t[None,:]))))
                formula=np.array([T@c@T.T for c in source_C]);mx('connected_identity',np.max(np.abs(C-formula)))
                edges=[edge_record(c,np.linalg.svd(old,compute_uv=False)[0]) for c,old in zip(C,source_C)]
                mx('support_residual',max(e['support_residual'] for e in edges))
                row={'candidate_index':candidate,'lambda':lam,'arm':name,'source_one_body':one.tolist(),'output_one_body':outone.tolist(),'source_correlations':source_C.tolist(),'edges':edges,'minimum_probability':pmin,'O':None,'Q':None,'E':None,'Q_map':None,'E_map':None}
                if name!='isotropic':
                    bound={'plane':2,'line':1,'point':0}[name];ok=all(all(k<=bound for k in e['ranks']) for e in edges)
                    if name=='point':row['connected_norm']=float(np.linalg.norm(C));ok=ok and row['connected_norm']<=1e-12
                    row['geometry_status']='SINGULAR_PREPARATION_SPAN' if ok else 'SPAN_BOUND_VIOLATION';span_ok=span_ok and ok
                    if name=='plane':noncommuting=noncommuting and ok and a['span']==2 and a['commutator']>=.1
                else:
                    dm=V91.domain(out,1/3);row['domain']=dm;regular=dm['valid'] and all(e['ranks']==[3]*3 for e in edges)
                    if not regular:row['geometry_status']='OUTSIDE_FROZEN_POLAR_DOMAIN';span_ok=False
                    else:
                        q,e,sy=V81.extract(out,outys);mx('sylvester',sy);O=np.array([M.polar(c)[0] for c in C]);old=saved[candidate,lam]
                        for key,value in [('Q',q),('E',e)]:
                            expected=np.array(old[key+'_map']);mx('parent_geometry_match',np.linalg.norm(value-expected)/max(1.,np.linalg.norm(expected)))
                        oldO=np.array([M.polar(np.array(c))[0] for c in old['correlations']]);mx('parent_geometry_match',np.linalg.norm(O-oldO)/max(1.,np.linalg.norm(oldO)))
                        em=V81.describe(e,old['E']['reference']);qm=V81.describe(q,old['Q']['reference'])
                        ok=em['ranks']==([0]*3 if lam==0 else [6]*3);span_ok=span_ok and ok
                        row.update(geometry_status='REGULAR',O=O.tolist(),Q=qm,E=em,Q_map=q.tolist(),E_map=e.tolist())
                rows.append(row)
    symbolic=symbolic_certificate();input_pd=V75.density_diagnostics(inputs);output_pd=V75.density_diagnostics(physical)
    limits={k:1e-12 for k in ['effect_completeness','effect_hermiticity','matrix_unit_reconstruction','center_tangent_reconstruction','probability_imaginary','probability_sum','tangent_probability_sum','affine_one_body','connected_identity']}
    limits.update(support_residual=1e-10,sylvester=1e-10,parent_geometry_match=1e-9)
    valid=(parents and indices==V91.EXPECTED and symbolic['valid'] and len(rows)==144 and len(composite)==12 and all(x['valid'] for x in source_channels+composite) and
           all(x['prepared_states']['valid'] for x in locals) and input_pd['valid'] and output_pd['valid'] and effect_min>=-1e-12 and prob_min>=-1e-12 and all(controls.get(k,0.)<=v for k,v in limits.items()))
    controls.update(parents_valid=bool(parents),symbolic_certificate=symbolic,input_physicality=input_pd,source_output_physicality=output_pd,minimum_effect_eigenvalue=effect_min,minimum_probability=prob_min)
    verdict,nv=adjudicate(valid,span_ok,noncommuting)
    report={'version':'15.92','candidate_indices':indices,'all_valid':bool(valid),'span_predicate':bool(span_ok),'noncommuting_predicate':bool(noncommuting),'verdict':verdict,'noncommuting_verdict':nv,
            'controls':controls,'local_channels':locals,'source_channels':source_channels,'composite_channels':composite,'rows':rows,
            'scope':'Preparation affine span bounds regular three-axis polar geometry; singular support transport remains defined; noncommutativity alone is insufficient; no source-law or gravity derivation.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['noncommuting_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
