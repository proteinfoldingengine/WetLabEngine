"""v15.99: retained response through a specified intermediate EB channel."""
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
spec=importlib.util.spec_from_file_location('composition98_middle',HERE.parent/'composed-four-body-response'/'gate.py')
V98=importlib.util.module_from_spec(spec);spec.loader.exec_module(V98)
V97=V98.V97;V96=V98.V96;V93=V98.V93;V75=V98.V75
AS=[1.,1/3,1/6,0.];EB_AS=AS[1:];ORDERS=['forward','reverse','contrast']
WEIGHTS=np.array([sum(k!=0 for k in w) for w in V98.LABELS])
HIDDEN=V98.HIDDEN;EPS=1e-4;ETA=1e-6;STRENGTH=.1


def middle(zs,a):return V96.post(np.asarray(zs),a**WEIGHTS)
def exact_middle(d,a):return V98.clean({w:c*a**sum(k!=0 for k in w) for w,c in d.items()})
def maxabs(z):return float(np.max(np.abs(z)))
def relative(x,y):return float(np.linalg.norm(x-y)/max(1.,np.linalg.norm(y)))


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    a=sp.symbols('a',real=True);ps=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)];ident=sp.eye(2)
    es=[(ident+s*p)/6 for p in ps for s in [-1,1]];ts=[(ident+s*3*a*p)/2 for p in ps for s in [-1,1]]
    zero=lambda z:all(sp.simplify(v)==0 for v in z)
    units=[]
    for i,j in itertools.product(range(2),repeat=2):
        z=sp.zeros(2);z[i,j]=1;units.append(z)
    checks={'local_measure_prepare_identity':all(zero(sum((sp.trace(e*z)*t for e,t in zip(es,ts)),sp.zeros(2))-a*z-(1-a)*sp.trace(z)*ident/2) for z in units)}
    checks['positive_complete_certificate']=zero(sum(es,sp.zeros(2))-ident) and all(zero(e-e.H) and e[0,0]>=0 and e[1,1]>=0 and e.det()>=0 for e in es)
    for val in [sp.Rational(1,3),sp.Rational(1,6),sp.Integer(0)]:
        for t in ts:
            z=t.subs(a,val);checks['positive_complete_certificate']=checks['positive_complete_certificate'] and zero(z-z.H) and sp.trace(z)==1 and z[0,0]>=0 and z[1,1]>=0 and z.det()>=0
    m,x,y=sp.symbols('m x y',real=True)
    checks['connected_baseline_scaling']=sp.expand(a**2*m-(a*x)*(a*y)-a**2*(m-x*y))==0
    weights=True;scaling=True;lower=True;commuting=True
    for w in V98.H_LABELS:
        d={w:sp.Integer(1)}
        for keys in V98.PAIRS.values():
            ordered=[]
            for first,second in [keys,keys[::-1]]:
                one=V98.exact_action(d,first);whole=V98.exact_action(exact_middle(one,a),second);old=V98.exact_action(one,second)
                for weight in [0,1,2,4]:
                    sector={v:c for v,c in one.items() if sum(k!=0 for k in v)==weight}
                    weights=weights and not V98.restrict(V98.exact_action(sector,second))
                scaling=scaling and V98.restrict(whole)==V98.clean({v:a**3*c for v,c in V98.restrict(old).items()})
                lower=lower and all(not V98.restrict(z) for z in [exact_middle(d,a),exact_middle(one,a),V98.exact_action(exact_middle(d,a),second)]) and not V98.restrict(whole,1)
                ordered.append(V98.restrict(whole))
            if keys==V98.PAIRS['disjoint']:commuting=commuting and ordered[0]==ordered[1]
    checks['only_weight_three_pair_contribution']=weights;checks['retained_mixed_cubic_scaling']=scaling
    checks['lower_pair_and_mixed_one_body_null']=lower
    checks['complete_erasure_pauli_basis']=all(exact_middle({w:1},sp.Integer(0))==({w:1} if w==(0,0,0,0) else {}) for w in V98.LABELS)
    checks['disjoint_retained_contrast_null']=commuting
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


@functools.lru_cache(maxsize=3)
def measure_prepare(a):
    es=[(np.eye(2)+s*p)/6 for p in V96.PAULI[1:] for s in [-1,1]]
    ts=[(np.eye(2)+s*3*a*p)/2 for p in V96.PAULI[1:] for s in [-1,1]]
    choices=list(itertools.product(range(6),repeat=4))
    return np.array([V96.tensor([es[k] for k in c]) for c in choices]),np.array([V96.tensor([ts[k] for k in c]) for c in choices])


def mp_apply(zs,effects,prepared):
    probs=np.einsum('hij,kji->hk',zs,effects,optimize=True)
    return np.einsum('hk,kij->hij',probs,prepared,optimize=True),probs


def adjudicate(valid,scaling,erasure):
    if not valid:return 'INVALID','INVALID'
    return ('INTERMEDIATE_EB_RESPONSE_SCALING_CONFIRMED' if scaling else 'INTERMEDIATE_EB_RESPONSE_SCALING_NOT_CONFIRMED',
            'COMPLETE_INTERMEDIATE_ERASURE_POLAR_UNDEFINED_CONFIRMED' if erasure else 'COMPLETE_INTERMEDIATE_ERASURE_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    f=HERE.parent/'composed-four-body-response';code=(f/'gate.py').read_bytes();gz=(f/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    old=HERE.parent/'overlap-holonomy-common-line';oldraw=gzip.decompress((old/'RESULT.json.gz').read_bytes());inputs96=json.loads(oldraw)
    parent_ok=(hashlib.sha256(code).hexdigest()=='ddc0e59aee1db514e77728dd7788d43545f03cde40cb7a19b221e2e8b1733239' and hashlib.sha256(gz).hexdigest()=='20a117760c6f5a9ecac86e45c871411ab3ed64c59f48c42d79641202b6656c6d' and hashlib.sha256(raw).hexdigest()=='044fa85ad44c2edf5e1d8e0fa4c2410f44498d5edc2456c99633706b4c251b0e' and hashlib.sha256(oldraw).hexdigest()=='99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e' and hashlib.sha256((old/'gate.py').read_bytes()).hexdigest()=='56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52' and parent['all_valid'] and parent['verdict']=='COMPOSITION_ORDER_GEOMETRY_CONFIRMED' and parent['commuting_verdict']=='COMMUTING_COMPOSITION_ACTIVATION_CONFIRMED')
    parent_rows={(r['candidate_index'],r['pair'],r['arm']):r for r in parent['rows']}
    names=['gram','trace','hermiticity','hidden_pair_null','individual_pair_null','lower_pair_null','one_body_null','source_unitarity','weight_sum','mixed_pair_scaling','weight_three_pair_error','baseline_correlation_scaling','centering','middle_covariance','geometry','derivative_identity','baseline_polar_invariance','baseline_loop_invariance','overlap_first_loop','disjoint_retained_null','linear_contrast','covariance','finite_channel_error','affine_K_error','affine_J_error']
    controls={k:0. for k in names}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    physical={'min_eigenvalue':1.,'trace_error':0.,'hermiticity_error':0.,'count':0,'valid':True}
    def density(z):
        z=np.asarray(z).reshape(-1,16,16);d=V75.density_diagnostics(z);physical['min_eigenvalue']=min(physical['min_eigenvalue'],d['min_eigenvalue'])
        for key in ['trace_error','hermiticity_error']:physical[key]=max(physical[key],d[key])
        physical['count']+=len(z);physical['valid']=physical['valid'] and d['valid']
    mx('gram',np.linalg.norm(np.einsum('hij,kji->hk',HIDDEN,HIDDEN)-np.eye(81)));mx('trace',maxabs(np.trace(HIDDEN,axis1=1,axis2=2)));mx('hermiticity',maxabs(HIDDEN-HIDDEN.conj().transpose(0,2,1)));mx('hidden_pair_null',maxabs(V97.pairs(HIDDEN)))
    for key,us in V98.SOURCES.items():
        mx('individual_pair_null',maxabs(V97.pairs(V98.generator(HIDDEN,key))))
        for u in us:mx('source_unitarity',np.linalg.norm(u.conj().T@u-np.eye(16)))
    weights=V97.V81.weights(1,STRENGTH);mx('weight_sum',abs(weights.sum()-1))
    exact=symbolic_certificate();certs=[V98.symbolic_certificate(),V97.symbolic_certificate(),V96.symbolic_certificate(),V96.V92.symbolic_certificate()]
    # Independent, explicit 1296-outcome channel on a complete matrix-unit basis.
    units=np.eye(256,dtype=complex).reshape(256,16,16);channel_checks=[]
    for a in EB_AS:
        es,ts=measure_prepare(a);mp,_=mp_apply(units,es,ts)
        rec={'a':a,'outcome_count':len(es),'matrix_unit_count':256,'map_error':maxabs(mp-middle(units,a)),'effect_completeness_error':maxabs(es.sum(axis=0)-np.eye(16)),
             'effect_hermiticity_error':maxabs(es-es.conj().transpose(0,2,1)),'effect_min_eigenvalue':float(np.linalg.eigvalsh(es).min()),
             'preparation_trace_error':maxabs(np.trace(ts,axis1=1,axis2=2)-1),'preparation_hermiticity_error':maxabs(ts-ts.conj().transpose(0,2,1)),'preparation_min_eigenvalue':float(np.linalg.eigvalsh(ts).min())}
        rec['valid']=all(v>=-1e-12 if 'min_eigenvalue' in k else v<=1e-12 for k,v in rec.items() if 'error' in k or 'min_eigenvalue' in k);channel_checks.append(rec)
    _,frames=V96.exact_frames();gs=[np.array(g.tolist(),float) for g,u in frames];bigU=V96.tensor([np.array(u.tolist(),complex) for g,u in frames]);g6=np.zeros((6,6));g6[:3,:3]=g6[3:,3:]=gs[0]
    rot_h=bigU@HIDDEN@bigU.conj().T;rot_us={key:np.array([bigU@u@bigU.conj().T for u in us]) for key,us in V98.SOURCES.items()}
    ydata={};weight_audits=[]
    for a in AS:
        for pair,keys in V98.PAIRS.items():
            ys={};rys={}
            for order,(first,second) in zip(ORDERS,[keys,keys[::-1]]):
                firsty=V98.generator(HIDDEN,first);my=middle(firsty,a);y=V98.generator(my,second);ys[order]=y
                rys[order]=V98.generator(middle(V98.generator(rot_h,first,units=rot_us),a),second,units=rot_us)
                mx('middle_covariance',maxabs(middle(bigU@firsty@bigU.conj().T,a)-bigU@my@bigU.conj().T))
                for z in [middle(HIDDEN,a),my,V98.generator(middle(HIDDEN,a),second)]:mx('lower_pair_null',maxabs(V97.pairs(z)))
                mx('one_body_null',maxabs(V97.single(y)));mx('mixed_pair_scaling',maxabs(V97.pairs(y)-a**3*V97.pairs(V98.generator(firsty,second))))
                only3=V96.post(firsty,(WEIGHTS==3).astype(float));y3=V98.generator(middle(only3,a),second)
                mx('weight_three_pair_error',maxabs(V97.pairs(y-y3)))
                weight_audits.append({'a':a,'pair':pair,'order':order,'first_tangent_norm':float(np.linalg.norm(firsty)),'weight_three_norm':float(np.linalg.norm(only3)),'attenuated_weight_three_norm':float(np.linalg.norm(middle(only3,a))),'pair_reconstruction_error':maxabs(V97.pairs(y-y3))})
            ys['contrast']=ys['forward']-ys['reverse'];rys['contrast']=rys['forward']-rys['reverse'];ydata[a,pair]=(ys,rys)
    armdata=V96.arms();rows=[];centers=[];scaling_pass=True;erasure_pass=True;rank_cov=True;disjoint_null=True;factor=((1-np.exp(-2*STRENGTH))/2)**2
    for rec in inputs96['input_states']:
        idx=rec['candidate_index'];rho=np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in rec['state_hex']]);hidden_inputs=np.concatenate([rho[None]+EPS*HIDDEN,rho[None]-EPS*HIDDEN]);density(hidden_inputs)
        # Unique centers; no duplication across final preparations or pair/order labels.
        for a in EB_AS:
            es,ts=measure_prepare(a)
            for first in V98.SITES:
                sourcecenter=V98.source(rho,first);direct=middle(sourcecenter[None],a)[0];mp,probs=mp_apply(sourcecenter[None],es,ts);probs=probs[0]
                c={'candidate_index':idx,'a':a,'first_source':first,'probabilities':probs.real.tolist(),'imaginary_error':maxabs(probs.imag),'minimum_probability':float(probs.real.min()),'sum_error':float(abs(probs.sum()-1)),'reconstruction_error':maxabs(mp[0]-direct)}
                c['valid']=bool(c['imaginary_error']<=1e-12 and c['minimum_probability']>=-1e-12 and c['sum_error']<=1e-12 and c['reconstruction_error']<=1e-12);centers.append(c);density([sourcecenter,direct,mp[0]])
        for a in AS:
            base=middle(rho[None],a)[0];sc=V97.correlations(base);rotbase=middle((bigU@rho@bigU.conj().T)[None],a)[0];rotsc=V97.correlations(rotbase)
            mx('middle_covariance',maxabs(rotbase-bigU@base@bigU.conj().T));mx('baseline_correlation_scaling',maxabs(sc-a*a*V97.correlations(rho)));density([base,rotbase])
            for pair,keys in V98.PAIRS.items():
                ys,rys=ydata[a,pair]
                for arm,data in armdata.items():
                    parentrow=parent_rows[idx,pair,arm];scale=data['scale'];center=V96.post(base[None],scale)[0];cs=V97.correlations(center)
                    rotcenter=bigU@V96.post((bigU.conj().T@rotbase@bigU)[None],scale)[0]@bigU.conj().T;rotcs=V97.correlations(rotcenter)
                    responses={o:None for o in ORDERS};transformed={o:None for o in ORDERS};rotresponses={};leaks={};scaling={};domain=True;baseline_edges=None
                    erasure_error=max(maxabs(base-np.eye(16)/16),maxabs(center-np.eye(16)/16),maxabs(cs)) if a==0 else None
                    for order in ORDERS:
                        posty=V96.post(ys[order],scale);ds=V98.connected_tangent(center,posty);mx('centering',maxabs(ds-V97.pairs(posty)))
                        leaks[order]={'raw':V98.leakage(ys[order]),'prepared':V98.leakage(posty),'global_tangent_norm':float(np.linalg.norm(ys[order]))}
                        if a==0:
                            erasure_error=max(erasure_error,maxabs(ys[order]),maxabs(posty));continue
                        rr,geom=V98.response(cs,sc,ds,arm);responses[order]=rr;mx('geometry',geom['residual']);baseline_edges=geom['edges']
                        td=bigU@V96.post(bigU.conj().T@rys[order]@bigU,scale)@bigU.conj().T
                        tr,tgeom=V98.response(rotcs,rotsc,V98.connected_tangent(rotcenter,td),arm);rotresponses[order]=tr;mx('geometry',tgeom['residual']);domain=domain and geom['domain'] and tgeom['domain']
                        for rr0 in [rr,tr]:
                            if rr0 is not None:
                                mx('derivative_identity',rr0['identity_residual'])
                                if pair=='overlap':mx('overlap_first_loop',np.linalg.norm(np.array(rr0['K'])[:3]))
                        if rr is not None:
                            pr=parentrow['responses'][order];scaling[order]={k:relative(np.array(rr[k]),a*np.array(pr[k])) for k in ['K','J']}
                            scaling[order]['ranks_match']=all(rr[k+'_ranks']==pr[k+'_ranks'] for k in ['K','J'])
                            mx('baseline_loop_invariance',np.linalg.norm(np.array(rr['loops'])-pr['loops']))
                            for edge,oldedge in zip(geom['edges'],parentrow['baseline_edges']):mx('baseline_polar_invariance',np.linalg.norm(np.array(edge['R'])-oldedge['R']))
                        else:scaling[order]=None
                        if rr is not None and tr is not None:
                            cr=max(np.linalg.norm(np.array(tr['K'])-g6@np.array(rr['K'])),np.linalg.norm(np.array(tr['J'])-rr['J']));mx('covariance',cr)
                            same=all(rr[k]==tr[k] for k in ['K_ranks','J_ranks']);rank_cov=rank_cov and same
                            transformed[order]={'K_ranks':tr['K_ranks'],'J_ranks':tr['J_ranks'],'covariance_residual':float(cr),'ranks_match':bool(same)}
                    if a>0:
                        for records in [responses,rotresponses]:
                            if all(r is not None for r in records.values()):
                                for key in ['K','J']:
                                    expected=np.array(records['forward'][key])-np.array(records['reverse'][key]);actual=np.array(records['contrast'][key]);mx('linear_contrast',np.linalg.norm(expected-actual))
                                    if pair=='disjoint':
                                        mx('disjoint_retained_null',max(np.linalg.norm(expected),np.linalg.norm(actual)));disjoint_null=disjoint_null and records['contrast'][key+'_ranks']==[0,0,0] and V97.ranks(expected)==[0,0,0]
                    finite_checks={};affine_domains={}
                    for order,(first,second) in zip(ORDERS,[keys,keys[::-1]]):
                        firstout=V98.source(hidden_inputs,first);cut=middle(firstout,a);final=V98.source(cut,second);outs=V96.post(final,scale)
                        for z in [firstout,cut,final,outs]:density(z)
                        dc=(V97.correlations(outs[:81])-V97.correlations(outs[81:]))/(2*EPS*factor);dy=V98.connected_tangent(center,V96.post(ys[order],scale));err=relative(dc,dy);mx('finite_channel_error',err)
                        check={'finite_channel_error':err,'affine_K_error':None,'affine_J_error':None}
                        if a==0:
                            # Also check the unperturbed finite protocol center explicitly.
                            fc=V96.post(V98.source(middle(V98.source(rho,first)[None],a),second),scale)[0];density(fc)
                            erasure_error=max(erasure_error,maxabs(cut-np.eye(16)/16),maxabs(final-np.eye(16)/16),maxabs(outs-np.eye(16)/16),maxabs(fc-np.eye(16)/16),maxabs(V97.correlations(outs)))
                        else:
                            affine=np.concatenate([base[None]+ETA*ys[order],base[None]-ETA*ys[order]]);prepared=V96.post(affine,scale);density(affine);density(prepared)
                            hs,iv,d=V97.finite_loops(prepared,affine,arm);affine_domains[order]=d;domain=domain and all(d);rr=responses[order]
                            if rr is not None and hs is not None:
                                dh=(hs[:81]-hs[81:])/(2*ETA);jfd=((iv[:81]-iv[81:])/(2*ETA)).T;hh=np.array(rr['loops'])
                                kfd=np.array([np.concatenate([V93.coords(V97.skew(h[i]@hh[i].T)) for i in range(2)]) for h in dh]).T
                                for key,fd in [('K',kfd),('J',jfd)]:
                                    error=relative(fd,np.array(rr[key]));check['affine_'+key+'_error']=error;mx('affine_'+key+'_error',error)
                        finite_checks[order]=check
                    if a>0:
                        passed=domain and all(s is not None and s['ranks_match'] and s['K']<=1e-9 and s['J']<=1e-9 for s in scaling.values());scaling_pass=scaling_pass and passed
                        erasure=None
                    else:
                        erasure={'maximum_error':float(erasure_error),'correlation_ranks':[V97.ranks(c) for c in cs],'polar_readout':'undefined'}
                        passed=erasure_error<=1e-12 and all(r==[0,0,0] for r in erasure['correlation_ranks']) and all(r is None for r in responses.values());erasure_pass=erasure_pass and passed
                    rows.append({'candidate_index':idx,'a':a,'intermediate_entanglement_breaking':a<=1/3,'pair':pair,'arm':arm,'all_domains':bool(domain) if a>0 else None,'baseline_edges':baseline_edges,'responses':responses,'transformed_responses':transformed,'scaling':scaling,'leakage':leaks,'finite_checks':finite_checks,'affine_domains':affine_domains,'erasure':erasure,'scientific_pass':bool(passed)})
    indices=[r['candidate_index'] for r in inputs96['input_states']];limits={k:1e-12 for k in controls}
    for k in ['geometry','derivative_identity','baseline_polar_invariance','baseline_loop_invariance','overlap_first_loop','disjoint_retained_null','linear_contrast','covariance']:limits[k]=1e-9
    limits.update(finite_channel_error=1e-7,affine_K_error=1e-5,affine_J_error=1e-5)
    valid=bool(parent_ok and indices==V96.EXPECTED and len(rows)==192 and sum(r['a']>0 for r in rows)==144 and len(centers)==108 and exact['valid'] and all(c['valid'] for c in certs+channel_checks+centers) and physical['valid'] and rank_cov and disjoint_null and weights.min()>=-1e-12 and all(v<=limits[k] for k,v in controls.items()))
    controls.update(parents_valid=bool(parent_ok),symbolic_certificate=exact,inherited_certificates=certs,intermediate_channels=channel_checks,physicality=physical,minimum_source_weight=float(weights.min()),rank_covariance_valid=bool(rank_cov),disjoint_retained_ranks_null=bool(disjoint_null),limits=limits)
    verdict,ev=adjudicate(valid,scaling_pass,erasure_pass)
    report={'version':'15.99','all_valid':valid,'verdict':verdict,'erasure_verdict':ev,'scaling_predicate':bool(scaling_pass),'erasure_predicate':bool(erasure_pass),'candidate_indices':indices,'hidden_count':81,'a_values':AS,'controls':controls,'weight_audits':weight_audits,'intermediate_centers':centers,'rows':rows,'scope':'Specified intermediate EB channel and source laws. Positive attenuation preserves ranks; complete erasure has undefined polar readout. Disjoint retained contrast is not full protocol commutation. No physical law selection or gravity.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,(list,tuple)):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['erasure_verdict']='INVALID'
    return report


if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
