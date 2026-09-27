"""v15.90: arbitrary-input negativity; normalized states throughout."""
import functools
import hashlib
import importlib.util
import json
import pathlib
import sys
import mpmath as mp
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('weakest89_inputs',HERE.parent/'weakest-direction-entanglement-bound'/'gate.py')
V89=importlib.util.module_from_spec(spec);spec.loader.exec_module(V89)
V88=V89.V88;V85=V89.V85;V84=V89.V84
num=V84.number;mat=V84.matrix;maximum=V84.maximum;kron=V85.kron
HASH89='760442f2d460af344aa9b1d6d8b1a0305894d301c1e1fddfd90d1cc478fb373c'


def symbolic_certificate():
    a,b,z,g,lam=sp.symbols('a b z g lam',real=True);I=sp.eye(2)
    k0=sp.diag(1,z);k1=sp.Matrix([[0,g],[0,0]]);v=sp.Matrix([a,0,0,b]);rho=v*v.H
    out=sum((sp.kronecker_product(I,k)*rho*sp.kronecker_product(I,k).H for k in [k0,k1]),sp.zeros(4))
    expected=sp.Matrix([[a*a,0,0,a*b*z],[0,0,0,0],[0,0,g*g*b*b,0],[a*b*z,0,0,z*z*b*b]])
    partial=V88.partial_input(out);pe=sp.Matrix([[a*a,0,0,0],[0,0,a*b*z,0],[0,a*b*z,g*g*b*b,0],[0,0,0,z*z*b*b]])
    zero=lambda m:all(sp.simplify(x)==0 for x in m)
    d=1-z*z+2*z;p=z/d;n=z*z/d;q=z*z;gamma=1-q
    checks={'kraus_output':zero(out-expected),'partial_output':zero(partial-pe),
            'characteristic_polynomial':sp.simplify((lam*sp.eye(4)-partial).det()-(lam-a*a)*(lam-z*z*b*b)*(lam*lam-g*g*b*b*lam-a*a*b*b*z*z))==0,
            'trace_preservation':zero((k0.H*k0+k1.H*k1-I).subs(g*g,1-z*z)),
            'negativity_stationary_quadratic':sp.simplify(n*n+gamma*p*n-q*p*(1-p))==0,
            'stationary_derivative':sp.simplify(gamma*n-q*(1-2*p))==0,
            'strict_ceiling_gap':sp.simplify(2-d-(1-z)**2)==0,
            'optimal_linear_limit':sp.limit(1/d,z,0,dir='+')==1}
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def apply_channel(T,t,rho):
    out=mp.zeros(4)
    for a in range(2):
        for b in range(2):
            block=mp.matrix([[rho[2*a+i,2*b+j] for j in range(2)] for i in range(2)])
            action=V85.affine(T,t,block)
            for i in range(2):
                for j in range(2):out[2*a+i,2*b+j]=action[i,j]
    return out


def negativity(rho):
    return sum(max(mp.mpf(0),-x) for x in mp.eighe(V88.partial_input(rho),eigvals_only=True))


def pure_input(p,phase):
    v=mp.matrix([mp.sqrt(1-p),0,0,phase*mp.sqrt(p)])
    return v*v.H,mp.diag([mp.sqrt(2*(1-p)),phase*mp.sqrt(2*p)])


def state_row(T,t,rho,delta,family,label,A=None):
    out=apply_channel(T,t,rho);G=V88.partial_input(out)
    ie=list(mp.eighe(rho,eigvals_only=True));oe=list(mp.eighe(out,eigvals_only=True));ge=list(mp.eighe(G,eigvals_only=True))
    n=sum(max(mp.mpf(0),-x) for x in ge);bound=min(delta,mp.mpf('.5'))
    ds=[V84.density(rho),V84.density(out)];errors=[maximum(G-G.H)]
    controls={};row={'family':family,'label':label,'matrix':mat(T),'shift':[num(x) for x in t],
                    'delta':num(delta),'input_eigenvalues':[num(x) for x in ie],'output_eigenvalues':[num(x) for x in oe],
                    'partial_eigenvalues':[num(x) for x in ge],'negativity':num(n),'uniform_bound':num(bound),
                    'uniform_slack':num(bound-n),'choi_ceiling':num(delta/2),'excess_over_choi_ceiling':num(n-delta/2),
                    'negative_partial_count':sum(x<-mp.mpf('1e-40') for x in ge),
                    'density_controls':[{k:num(v) for k,v in d.items()} for d in ds]}
    if A is not None:
        J=V85.choi(T,t);K=kron(A,V84.I);Ac=A.H.T;Kc=kron(Ac,V84.I)
        controls={'filter_output':maximum(out-K*J*K.H/2),
                  'filter_partial':maximum(G-Kc*V88.partial_input(J)*Kc.H/2),
                  'filter_normalization':abs(V84.tr(A*A.H)-2)}
        reference=A*A.H/2;schmidt=max(mp.eighe(reference,eigvals_only=True))
        lower=G+delta*kron(Ac*A.T,V84.I)/2
        controls['lower_hermiticity']=maximum(lower-lower.H)
        row.update({'schmidt_maximum':num(schmidt),'schmidt_slack':num(delta*schmidt-n),
                    'operator_bound_minimum':num(min(mp.eighe(lower,eigvals_only=True)))})
        errors.extend(controls.values())
    row['identity_controls']={k:num(v) for k,v in controls.items()}
    valid=all(V84.density_valid(d) for d in ds) and max(errors)<=mp.mpf('1e-45')
    return row,out,bool(valid),max(errors),ds


def adjudicate(valid,bound,extension,constant):
    if not valid:return 'INVALID','INVALID','INVALID'
    return ('UNIVERSAL_INPUT_NEGATIVITY_BOUND_CONFIRMED' if bound else 'UNIVERSAL_INPUT_NEGATIVITY_BOUND_NOT_CONFIRMED',
            'CHOI_CEILING_EXTENSION_FALSIFIED' if extension else 'CHOI_CEILING_EXTENSION_NOT_FALSIFIED',
            'OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_CONFIRMED' if bound and constant else 'OPTIMAL_LINEAR_NEGATIVITY_CONSTANT_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    with mp.workdps(80):return _run()


def _run():
    data=(HERE.parent/'weakest-direction-entanglement-bound'/'RESULT.json').read_bytes();parent=json.loads(data)
    parents=(hashlib.sha256(data).hexdigest()==HASH89 and parent['all_valid'] and
             parent['verdict']=='WEAKEST_DIRECTION_NEGATIVITY_BOUND_CONFIRMED' and parent['sharpness_verdict']=='NEGATIVITY_BOUND_SHARPNESS_CONFIRMED')
    rows=[];channels=[];valids=[];errors=[];archive_errors=[];damping_delta_errors=[];ds=[];formulas=[];choi_matches=[];ratios=[]
    product=mp.zeros(4);product[2,2]=1
    for idx,saved in enumerate(parent['rows']):
        T=V84.real_matrix(saved['matrix']);t=mp.matrix([mp.mpf(x) for x in saved['shift']]);delta=mp.svd_r(T,compute_uv=False)[2]
        channel,e,g,checks=V88.channel_row(T,t);channels.append(channel);errors.extend(checks)
        archive_errors.append(max(V88.spectrum_error(e,[mp.mpf(x) for x in saved['choi_eigenvalues']]),V88.spectrum_error(g,[mp.mpf(x) for x in saved['partial_transpose_eigenvalues']]),abs(delta-mp.mpf(saved['minimum_singular_value'])),abs(mp.mpf(channel['normalized_choi_negativity'])-mp.mpf(saved['normalized_choi_negativity']))))
        pure_outputs={}
        for text in ['0','0.25','0.5']:
            p=mp.mpf(text);rho,A=pure_input(p,mp.j);r,out,valid,error,densities=state_row(T,t,rho,delta,'inherited_pure',str(idx)+':'+text,A)
            r.update({'parent_row':idx,'p':text,'phase':'i'});rows.append(r);valids.append(valid);errors.append(error);ds.extend(densities);pure_outputs[text]=out
            if text=='0.5':choi_matches.append(abs(mp.mpf(r['negativity'])-mp.mpf(saved['normalized_choi_negativity'])))
        rho,_=pure_input(mp.mpf('.25'),mp.j);mixed=(rho+product)/2
        r,out,valid,error,densities=state_row(T,t,mixed,delta,'inherited_mixed',str(idx)+':mixture')
        prodout=apply_channel(T,t,product);ds.append(V84.density(prodout))
        re=maximum(out-(pure_outputs['0.25']+prodout)/2);errors.extend([error,re]);valids.append(valid);ds.extend(densities)
        r.update({'parent_row':idx,'linear_reconstruction_error':num(re),'convexity_slack':num((negativity(pure_outputs['0.25'])+negativity(prodout))/2-mp.mpf(r['negativity']))});rows.append(r)
    for text in ['1','0.5','0.25','0.01','0.0001','0.000001','0']:
        q=mp.mpf(text);gamma=1-q;z=mp.sqrt(q);den=gamma+2*z;T=mp.diag([z,z,q]);t=mp.matrix([0,0,gamma]);delta=mp.svd_r(T,compute_uv=False)[2]
        channel,e,g,checks=V88.channel_row(T,t);channel['q']=text;channels.append(channel);errors.extend(checks);damping_delta_errors.append(abs(delta-q))
        k0=mp.diag([1,z]);k1=mp.matrix([[0,mp.sqrt(gamma)],[0,0]])
        for choice,p in [('choi',mp.mpf('.5')),('family_optimum',z/den)]:
            rho,A=pure_input(p,mp.mpf(1));r,out,valid,error,densities=state_row(T,t,rho,delta,'amplitude_damping',text+':'+choice,A)
            ko=sum((kron(V84.I,k)*rho*kron(V84.I,k).H for k in [k0,k1]),mp.zeros(4))
            ke=maximum(out-ko);errors.extend([error,ke]);valids.append(valid);ds.extend(densities)
            formula=(mp.sqrt(gamma*gamma*p*p+4*q*p*(1-p))-gamma*p)/2;predicted=q/2 if choice=='choi' else q/den
            fe=max(abs(mp.mpf(r['negativity'])-formula),abs(mp.mpf(r['negativity'])-predicted));formulas.append(fe)
            r.update({'q':text,'choice':choice,'p':num(p),'phase':'1','kraus_reconstruction_error':num(ke),'negativity_formula_error':num(fe)})
            if choice=='family_optimum' and q>0:
                ratio=mp.mpf(r['negativity'])/q;ratios.append(ratio);r['negativity_over_delta']=num(ratio)
            rows.append(r)
    symbolic=symbolic_certificate();inherited=V89.symbolic_certificate()
    valid=(parents and symbolic['valid'] and inherited['valid'] and inherited['check_count']==22 and len(rows)==114 and len(channels)==32 and
           all(valids) and all(V84.density_valid(d) for d in ds) and all(c['cp_class']=='CPTP' for c in channels) and
           max(errors+damping_delta_errors)<=mp.mpf('1e-45') and max(archive_errors)<=mp.mpf('1e-60'))
    bound=all(mp.mpf(r['uniform_slack'])>=-mp.mpf('1e-40') and r['negative_partial_count']<=1 and
              all(mp.mpf(r[k])>=-mp.mpf('1e-40') for k in ['schmidt_slack','operator_bound_minimum','convexity_slack'] if k in r) for r in rows)
    witnesses=[r for r in rows if r['family']=='amplitude_damping' and r['choice']=='family_optimum' and r['q'] in ['0.5','0.25']]
    formula_ok=max(formulas)<=mp.mpf('1e-45')
    extension=(len(witnesses)==2 and all(mp.mpf(r['excess_over_choi_ceiling'])>=mp.mpf('1e-4') for r in witnesses) and formula_ok and max(choi_matches)<=mp.mpf('1e-45'))
    constant=(formula_ok and len(ratios)==6 and all(b>a for a,b in zip(ratios,ratios[1:])) and ratios[-1]>=mp.mpf('.99'))
    verdict,ev,cv=adjudicate(valid,bound,extension,constant)
    report={'version':'15.90','precision_digits':80,'parent_hash':HASH89,'all_valid':bool(valid),
            'bound_predicate':bool(bound),'extension_falsified_predicate':bool(extension),'constant_predicate':bool(constant),
            'verdict':verdict,'extension_verdict':ev,'constant_verdict':cv,
            'controls':{'parents_valid':bool(parents),'symbolic_certificate':symbolic,'inherited_certificate':inherited,
                        'max_archive_error':num(max(archive_errors)),'max_identity_error':num(max(errors)),
                        'max_damping_delta_error':num(max(damping_delta_errors)),'max_damping_formula_error':num(max(formulas)),
                        'max_choi_input_negativity_error':num(max(choi_matches)),
                        'minimum_state_eigenvalue':num(min(d['minimum_eigenvalue'] for d in ds)),
                        'max_state_trace_error':num(max(d['trace'] for d in ds)),
                        'max_state_hermiticity_error':num(max(d['hermiticity'] for d in ds))},
            'channels':channels,'rows':rows,'scope':'Arbitrary-input qubit-channel negativity bound with optimal uniform linear coefficient, not pointwise sharpness, capacity or physical source-law selection.',
            'sources':['https://arxiv.org/abs/1412.5885']}
    def finite(a):
        if isinstance(a,dict):return all(finite(v) for v in a.values())
        if isinstance(a,list):return all(finite(v) for v in a)
        if isinstance(a,str):return a.lower() not in ['nan','inf','+inf','-inf']
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['extension_verdict']=report['constant_verdict']='INVALID'
    return report

if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
