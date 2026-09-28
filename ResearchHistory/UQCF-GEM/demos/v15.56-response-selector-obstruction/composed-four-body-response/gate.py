"""v15.98: composition can expose weight-four information; order is a separate test."""
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
spec=importlib.util.spec_from_file_location('hidden97_composition',HERE.parent/'overlap-hidden-response'/'gate.py')
V97=importlib.util.module_from_spec(spec);spec.loader.exec_module(V97)
V96=V97.V96;V93=V97.V93;V75=V97.V75
THRESHOLDS=[1e-9,1e-10,1e-11];EPS=1e-4;ETA=1e-6;STRENGTH=.1
SITES={'A':(0,1),'B':(1,2),'D':(2,3)};PAIRS={'overlap':('A','B'),'disjoint':('A','D')}
LABELS=list(itertools.product(range(4),repeat=4));H_LABELS=list(itertools.product([1,2,3],repeat=4))

def word(lab):return V96.tensor([V96.PAULI[i] for i in lab])
HIDDEN=np.array([word(lab)/4 for lab in H_LABELS])
SOURCES={}
for name,(i,j) in SITES.items():
    p=V96.op(i,3);q=V96.op(i,1,j,1);ap=(p+q)/np.sqrt(2);am=(p-q)/np.sqrt(2)
    SOURCES[name]=np.array([np.eye(16),ap,am,ap@am])


def generator(z,key,lam=1,units=SOURCES):
    us=units[key]
    return (1+lam)/2*(us[1]@z@us[1].conj().T-z)+(1-lam)/2*(us[2]@z@us[2].conj().T-z)


def source(z,key):return sum(w*(u@z@u.conj().T) for w,u in zip(V97.V81.weights(1.,STRENGTH),SOURCES[key]))
def restrict(d,max_weight=2):return {w:c for w,c in d.items() if sum(a!=0 for a in w)<=max_weight and c!=0}
def clean(d):return {w:sp.expand(c) for w,c in d.items() if sp.expand(c)!=0}
def add(a,b,factor=1):
    out=dict(a)
    for w,c in b.items():out[w]=out.get(w,0)+factor*c
    return clean(out)


@functools.lru_cache(maxsize=1)
def exact_tables():
    ps=[sp.eye(2),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    labs=list(itertools.product(range(4),repeat=2));basis={w:sp.kronecker_product(ps[w[0]],ps[w[1]]) for w in labs}
    p=basis[(3,0)];q=basis[(1,1)];ap=(p+q)/sp.sqrt(2);am=(p-q)/sp.sqrt(2);tables={};reconstruction=True
    for lam in [0,1]:
        table={}
        for w,h in basis.items():
            out=(sp.Rational(1+lam,2)*(ap*h*ap-h)+sp.Rational(1-lam,2)*(am*h*am-h)).applyfunc(sp.simplify)
            cs={v:sp.simplify(sp.trace(o*out)/4) for v,o in basis.items()};table[w]={v:c for v,c in cs.items() if c!=0}
            reconstructed=sum((c*basis[v] for v,c in table[w].items()),sp.zeros(4))
            reconstruction=reconstruction and all(sp.simplify(v)==0 for v in out-reconstructed)
        tables[lam]=table
    return tables,bool(reconstruction)


def exact_action(d,key,lam=1):
    table=exact_tables()[0][lam];i,j=SITES[key];out={}
    for w,c in d.items():
        for local,k in table[(w[i],w[j])].items():
            ww=list(w);ww[i],ww[j]=local;ww=tuple(ww);out[ww]=out.get(ww,0)+c*k
    return clean(out)


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    checks={'local_reconstruction':exact_tables()[1]}
    checks['single_source_pair_null']=all(not restrict(exact_action({w:1},key)) for w in H_LABELS for key in SITES)
    checks['double_one_body_null']=all(not restrict(exact_action(exact_action({w:1},a),b),1) for w in H_LABELS for keys in PAIRS.values() for a,b in [keys,keys[::-1]])
    w={(2,2,1,1):1};ab=restrict(exact_action(exact_action(w,'A'),'B'));ba=restrict(exact_action(exact_action(w,'B'),'A'))
    checks['overlap_witness']=ab=={(0,1,0,1):-1} and ba=={}
    checks['disjoint_full_commutation']=all(exact_action(exact_action({w:1},'A'),'D')==exact_action(exact_action({w:1},'D'),'A') for w in LABELS)
    checks['disjoint_activation_witness']=restrict(exact_action(exact_action({(1,1,1,1):1},'A'),'D'))=={(3,0,3,0):1}
    checks['incoherent_pair_null']=all(not restrict(exact_action(exact_action({w:1},a,la),b,lb)) for w in H_LABELS for keys in PAIRS.values() for a,b in [keys,keys[::-1]] for la,lb in [(0,1),(1,0),(0,0)])
    s,t=sp.symbols('s t',real=True);finite=True
    for w in H_LABELS:
        for keys in PAIRS.values():
            for a,b in [keys,keys[::-1]]:
                first=add({w:1},exact_action({w:1},a),s);whole=add(first,exact_action(first,b),t)
                expected={v:s*t*c for v,c in restrict(exact_action(exact_action({w:1},a),b)).items()}
                finite=finite and clean(restrict(whole))==clean(expected)
    checks['finite_polynomial_identity']=finite
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def describe(a):return {'norm':float(np.linalg.norm(a)),'singular_values':np.linalg.svd(a,compute_uv=False).tolist(),'ranks':V97.ranks(a)}


def leakage(ys):
    ds=V97.pairs(ys);out=[]
    for e,edge in enumerate(V96.EDGES):
        out.append({'edge':list(edge),'declared_geometry_edge':e<5,**describe(ds[:,e].reshape(81,9).T)})
    return out


def connected_tangent(center,ys):
    n=V97.single(center);dn=V97.single(ys);out=V97.pairs(ys).copy()
    for e,(i,j) in enumerate(V96.EDGES):out[:,e]-=dn[:,i,:,None]*n[j,None,:]+n[i,:,None]*dn[:,j,None,:]
    return out


def response(cs,sc,ds,arm):
    geom=V96.geometry(cs,sc,arm)
    if not geom['domain']:return None,geom
    rs=np.array([e['R'] for e in geom['edges']]);ps=np.array([r.T@c for r,c in zip(rs,cs[:5])]);K=np.zeros((6,len(ds)));J=np.zeros((3,len(ds)));edge=np.zeros((5,3,len(ds)));res=0.
    for k,dd in enumerate(ds):
        dr=[]
        for e,(r,p,d) in enumerate(zip(rs,ps,dd[:5])):
            q,w=V93.tangent(r,p,d);dr.append(r@w);edge[e,:,k]=V93.coords(w);res=max(res,np.linalg.norm(p@w+w@p-q),np.linalg.norm(w+w.T))
        hs,dhs=V97.loop_derivative(rs,dr)
        for i in range(2):
            v=dhs[i]@hs[i].T;res=max(res,np.linalg.norm(v+v.T));K[3*i:3*i+3,k]=V93.coords(V97.skew(v))
        J[:,k]=V97.invariant_derivative(hs,dhs)
    return {'K':K.tolist(),'J':J.tolist(),'K_ranks':V97.ranks(K),'J_ranks':V97.ranks(J),'K_singular_values':np.linalg.svd(K,compute_uv=False).tolist(),'J_singular_values':np.linalg.svd(J,compute_uv=False).tolist(),'edge_ranks':[V97.ranks(e) for e in edge],'loop_ranks':[V97.ranks(K[:3]),V97.ranks(K[3:])],'loops':hs.tolist(),'invariants':V97.invariants(hs).tolist(),'identity_residual':float(res)},geom


def adjudicate(valid,order,commuting):
    if not valid:return 'INVALID','INVALID'
    return ('COMPOSITION_ORDER_GEOMETRY_CONFIRMED' if order else 'COMPOSITION_ORDER_GEOMETRY_NOT_CONFIRMED','COMMUTING_COMPOSITION_ACTIVATION_CONFIRMED' if commuting else 'COMMUTING_COMPOSITION_ACTIVATION_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    f=HERE.parent/'overlap-hidden-response';code=(f/'gate.py').read_bytes();gz=(f/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    old=HERE.parent/'overlap-holonomy-common-line';oldraw=gzip.decompress((old/'RESULT.json.gz').read_bytes());inputs96=json.loads(oldraw)
    parent_ok=(hashlib.sha256(code).hexdigest()=='a27a98a29c5dce4f286bd445072297228af903a348ee274a9c6bb7d15c986439' and hashlib.sha256(gz).hexdigest()=='5d211fb43db6ddd101be6d31391554b4e6720f09626255e85cc01da76d3179bc' and hashlib.sha256(raw).hexdigest()=='a16af3868ed4a0d959dda97eaea9c79f02f2beb0aa996b175a233463b9381891' and hashlib.sha256(oldraw).hexdigest()=='99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e' and hashlib.sha256((old/'gate.py').read_bytes()).hexdigest()=='56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52' and parent['all_valid'] and parent['verdict']=='OVERLAP_HIDDEN_RESPONSE_CONFIRMED' and parent['planar_verdict']=='PLANAR_TWO_LOOP_RESPONSE_CONFIRMED')
    controls={k:0. for k in ['gram','trace','hermiticity','hidden_pair_null','individual_pair_null','one_body_null','incoherent_pair_null','source_unitarity','weight_sum','exact_coefficient_error','centering','geometry','derivative_identity','overlap_first_loop','commuting_order_null','linear_contrast','covariance','finite_channel_error','affine_K_error','affine_J_error']}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    physical={'min_eigenvalue':1.,'trace_error':0.,'hermiticity_error':0.,'count':0,'valid':True}
    def density(z):
        z=np.asarray(z).reshape(-1,16,16);d=V75.density_diagnostics(z);physical['min_eigenvalue']=min(physical['min_eigenvalue'],d['min_eigenvalue'])
        for key in ['trace_error','hermiticity_error']:physical[key]=max(physical[key],d[key])
        physical['count']+=len(z);physical['valid']=physical['valid'] and d['valid']
    mx('gram',np.linalg.norm(np.einsum('hij,kji->hk',HIDDEN,HIDDEN)-np.eye(81)));mx('trace',np.max(np.abs(np.trace(HIDDEN,axis1=1,axis2=2))));mx('hermiticity',np.max(np.abs(HIDDEN-HIDDEN.conj().transpose(0,2,1))));mx('hidden_pair_null',np.max(np.abs(V97.pairs(HIDDEN))))
    for key in SITES:
        mx('individual_pair_null',np.max(np.abs(V97.pairs(generator(HIDDEN,key)))))
        for u in SOURCES[key]:mx('source_unitarity',np.linalg.norm(u.conj().T@u-np.eye(16)))
    weights=V97.V81.weights(1,STRENGTH);mx('weight_sum',abs(weights.sum()-1))
    exact=symbolic_certificate();certs=[V97.symbolic_certificate(),V96.symbolic_certificate(),V96.V92.symbolic_certificate()]
    _,frames=V96.exact_frames();gs=[np.array(g.tolist(),float) for g,u in frames];bigU=V96.tensor([np.array(u.tolist(),complex) for g,u in frames]);g6=np.zeros((6,6));g6[:3,:3]=g6[3:,3:]=gs[0]
    rot_h=bigU@HIDDEN@bigU.conj().T;rot_us={key:np.array([bigU@u@bigU.conj().T for u in us]) for key,us in SOURCES.items()}
    ydata={};label_index={lab:i for i,lab in enumerate(LABELS)}
    for pair,keys in PAIRS.items():
        ys={};rys={}
        for order,(a,b) in zip(['forward','reverse'],[keys,keys[::-1]]):
            y=generator(generator(HIDDEN,a),b);ys[order]=y;rys[order]=generator(generator(rot_h,a,units=rot_us),b,units=rot_us)
            mx('one_body_null',np.max(np.abs(V97.single(y))))
            coeff=np.einsum('hij,kji->hk',y,V96.BASIS);pred=np.zeros((81,256))
            for i,w in enumerate(H_LABELS):
                for ww,c in exact_action(exact_action({w:1},a),b).items():pred[i,label_index[ww]]=float(c)
            mx('exact_coefficient_error',np.max(np.abs(coeff-pred)))
            for la,lb in [(0,1),(1,0),(0,0)]:mx('incoherent_pair_null',np.max(np.abs(V97.pairs(generator(generator(HIDDEN,a,la),b,lb)))))
        ys['contrast']=ys['forward']-ys['reverse'];rys['contrast']=rys['forward']-rys['reverse'];ydata[pair]=(ys,rys)
    armdata=V96.arms();rows=[];order_pass=True;comm_pass=True;rank_cov=True;comm_null=True;factor=((1-np.exp(-2*STRENGTH))/2)**2
    for rec in inputs96['input_states']:
        rho=np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in rec['state_hex']]);hidden_inputs=np.concatenate([rho[None]+EPS*HIDDEN,rho[None]-EPS*HIDDEN]);density(hidden_inputs)
        for pair,keys in PAIRS.items():
            ys,rys=ydata[pair]
            for arm,data in armdata.items():
                scale=data['scale'];center=V96.post(rho[None],scale)[0];cs=V97.correlations(center);sc=V97.correlations(rho);rotcenter=bigU@center@bigU.conj().T;rotcs=V97.correlations(rotcenter);rotsc=V97.correlations(bigU@rho@bigU.conj().T)
                responses={};rotresponses={};domain=True;baseline_edges=None;leaks={}
                for order in ['forward','reverse','contrast']:
                    posty=V96.post(ys[order],scale);ds=connected_tangent(center,posty);mx('centering',np.max(np.abs(ds-V97.pairs(posty))))
                    rr,geom=response(cs,sc,ds,arm);responses[order]=rr;mx('geometry',geom['residual']);baseline_edges=geom['edges']
                    td=bigU@V96.post(bigU.conj().T@rys[order]@bigU,scale)@bigU.conj().T
                    tr,tgeom=response(rotcs,rotsc,connected_tangent(rotcenter,td),arm);rotresponses[order]=tr;mx('geometry',tgeom['residual']);domain=domain and geom['domain'] and tgeom['domain']
                    for response_record in [rr,tr]:
                        if response_record is not None:
                            mx('derivative_identity',response_record['identity_residual'])
                            if pair=='overlap':mx('overlap_first_loop',np.linalg.norm(np.array(response_record['K'])[:3]))
                    if rr is not None and tr is not None:
                        mx('covariance',max(np.linalg.norm(np.array(tr['K'])-g6@np.array(rr['K'])),np.linalg.norm(np.array(tr['J'])-rr['J'])))
                        rank_cov=rank_cov and all(rr[key]==tr[key] for key in ['K_ranks','J_ranks'])
                    leaks[order]={'raw':leakage(ys[order]),'prepared':leakage(posty)}
                for records in [responses,rotresponses]:
                    if all(r is not None for r in records.values()):
                        for key in ['K','J']:
                            expected=np.array(records['forward'][key])-np.array(records['reverse'][key]);actual=np.array(records['contrast'][key]);mx('linear_contrast',np.linalg.norm(expected-actual))
                            if pair=='disjoint':
                                mx('commuting_order_null',max(np.linalg.norm(expected),np.linalg.norm(actual)));comm_null=comm_null and records['contrast'][key+'_ranks']==[0,0,0] and V97.ranks(expected)==[0,0,0]
                finite_checks={};affine_domains={}
                for order,(a,b) in zip(['forward','reverse'],[keys,keys[::-1]]):
                    intermediate=source(hidden_inputs,a);final=source(intermediate,b);outs=V96.post(final,scale)
                    for z in [intermediate,final,outs]:density(z)
                    dc=(V97.correlations(outs[:81])-V97.correlations(outs[81:]))/(2*EPS*factor);dy=connected_tangent(center,V96.post(ys[order],scale));err=float(np.linalg.norm(dc-dy)/max(1.,np.linalg.norm(dy)));mx('finite_channel_error',err)
                    affine=np.concatenate([rho[None]+ETA*ys[order],rho[None]-ETA*ys[order]]);prepared=V96.post(affine,scale);density(affine);density(prepared)
                    hs,iv,d=V97.finite_loops(prepared,affine,arm);affine_domains[order]=d;domain=domain and all(d)
                    check={'finite_channel_error':err,'affine_K_error':None,'affine_J_error':None}
                    rr=responses[order]
                    if rr is not None and hs is not None:
                        dh=(hs[:81]-hs[81:])/(2*ETA);jfd=((iv[:81]-iv[81:])/(2*ETA)).T;hh=np.array(rr['loops'])
                        kfd=np.array([np.concatenate([V93.coords(V97.skew(h[i]@hh[i].T)) for i in range(2)]) for h in dh]).T
                        for key,fd in [('K',kfd),('J',jfd)]:
                            arr=np.array(rr[key]);error=float(np.linalg.norm(fd-arr)/max(1.,np.linalg.norm(arr)));check['affine_'+key+'_error']=error;mx('affine_'+key+'_error',error)
                    finite_checks[order]=check
                if pair=='overlap':
                    kr=[3]*3 if arm=='isotropic' else [1]*3;jr=[2]*3 if arm=='isotropic' else [1]*3
                    passed=domain and all(r['contrast']['K_ranks']==kr and r['contrast']['J_ranks']==jr for r in [responses,rotresponses]);order_pass=order_pass and passed
                else:
                    kr=[6]*3 if arm=='isotropic' else [2]*3;jr=[3]*3 if arm=='isotropic' else [2]*3
                    passed=domain and all(r[o]['K_ranks']==kr and r[o]['J_ranks']==jr for r in [responses,rotresponses] for o in ['forward','reverse']);comm_pass=comm_pass and passed
                rows.append({'candidate_index':rec['candidate_index'],'pair':pair,'arm':arm,'all_domains':bool(domain),'baseline_edges':baseline_edges,'responses':responses,'transformed_responses':rotresponses,'leakage':leaks,'finite_checks':finite_checks,'affine_domains':affine_domains,'scientific_pass':bool(passed)})
    indices=[r['candidate_index'] for r in inputs96['input_states']];limits={k:1e-12 for k in controls}
    for k in ['geometry','derivative_identity','overlap_first_loop','commuting_order_null','linear_contrast','covariance']:limits[k]=1e-9
    limits.update(finite_channel_error=1e-7,affine_K_error=1e-5,affine_J_error=1e-5)
    valid=bool(parent_ok and indices==V96.EXPECTED and len(rows)==48 and exact['valid'] and all(c['valid'] for c in certs) and physical['valid'] and rank_cov and comm_null and weights.min()>=-1e-12 and all(v<=limits[k] for k,v in controls.items()))
    controls.update(parents_valid=bool(parent_ok),symbolic_certificate=exact,inherited_certificates=certs,physicality=physical,minimum_weight=float(weights.min()),rank_covariance_valid=bool(rank_cov),commuting_ranks_null=bool(comm_null),limits=limits)
    verdict,cv=adjudicate(valid,order_pass,comm_pass)
    report={'version':'15.98','all_valid':valid,'verdict':verdict,'commuting_verdict':cv,'order_predicate':bool(order_pass),'commuting_predicate':bool(comm_pass),'candidate_indices':indices,'hidden_count':81,'hidden_labels':H_LABELS,'controls':controls,'rows':rows,'scope':'Specified two-source origin mixed derivatives. Commuting activation and order-sensitive response are distinct; neither physical source-law selection nor gravity. Edge23 is not an unaffected spectator.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,(list,tuple)):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(report):report['all_valid']=False;report['verdict']=report['commuting_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
