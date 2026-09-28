"""v15.97: source-origin mixed response of two overlapping retained loops."""
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
spec=importlib.util.spec_from_file_location('overlap96_response',HERE.parent/'overlap-holonomy-common-line'/'gate.py')
V96=importlib.util.module_from_spec(spec);spec.loader.exec_module(V96)
V93=V96.V93;V81=V96.V81;V75=V96.V75
THRESHOLDS=[1e-9,1e-10,1e-11];LAMBDAS=[-1.,0.,1.];STEPS=[1e-3,3e-4,1e-4];EPS=1e-4
UNITARIES=np.array([np.kron(u,np.eye(2)) for u in V81.UNITARIES])
HIDDEN_LABELS=[(a,b,c,0) for a,b,c in itertools.product([1,2,3],repeat=3)]+[(a,b,0,c) for a,b,c in itertools.product([1,2,3],repeat=3)]
FOUR_LABELS=list(itertools.product([1,2,3],repeat=4))
HIDDEN=np.array([V96.tensor([V96.PAULI[i] for i in lab])/4 for lab in HIDDEN_LABELS])
FOUR=np.array([V96.tensor([V96.PAULI[i] for i in lab])/4 for lab in FOUR_LABELS])


def generator(z,lam,unitaries=UNITARIES):
    return (1+lam)/2*(unitaries[1]@z@unitaries[1].conj().T-z)+(1-lam)/2*(unitaries[2]@z@unitaries[2].conj().T-z)


def source(z,lam,u):return sum(w*(v@z@v.conj().T) for w,v in zip(V81.weights(lam,u),UNITARIES))


def single(z):return np.einsum('...ij,naji->...na',z,V96.ONE).real
def pairs(z):return np.einsum('...ij,eabji->...eab',z,V96.PAIR).real
def correlations(z):
    one=single(z);pair=pairs(z)
    return np.stack([pair[...,e,:,:]-one[...,i,:,None]*one[...,j,None,:] for e,(i,j) in enumerate(V96.EDGES)],axis=-3)


def loop_derivative(rs,dr):
    hs=[];dhs=[]
    for a,b,c in [(0,1,2),(0,3,4)]:
        hs.append(rs[a]@rs[b]@rs[c])
        dhs.append(dr[a]@rs[b]@rs[c]+rs[a]@dr[b]@rs[c]+rs[a]@rs[b]@dr[c])
    return np.array(hs),np.array(dhs)


def invariants(hs):return np.array([np.trace(hs[0]),np.trace(hs[1]),np.trace(hs[0]@hs[1])])
def invariant_derivative(hs,dhs):return np.array([np.trace(dhs[0]),np.trace(dhs[1]),np.trace(dhs[0]@hs[1]+hs[0]@dhs[1])])
def skew(a):return (a-a.T)/2
def ranks(a):return [int(np.count_nonzero(np.linalg.svd(a,compute_uv=False)>t)) for t in THRESHOLDS]


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    I=sp.eye(2);X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1);ps=[X,Y,Z];kron=sp.kronecker_product
    P=kron(Z,I);Q=kron(X,X);ap=(P+Q)/sp.sqrt(2);am=(P-Q)/sp.sqrt(2);zero=lambda a:all(sp.simplify(v)==0 for v in a);checks={}
    checks['pauli_source_algebra']=P.H==P and Q.H==Q and P*P==sp.eye(4) and Q*Q==sp.eye(4) and zero(P*Q+Q*P)
    checks['source_unitaries']=all(zero(a.H-a) and zero(a*a-sp.eye(4)) for a in [ap,am])
    lam,u=sp.symbols('lambda u',real=True);plus=(1+sp.exp(-(1+lam)*u))/2;minus=(1+sp.exp(-(1-lam)*u))/2
    ws=[plus*minus,(1-plus)*minus,plus*(1-minus),(1-plus)*(1-minus)];target=[-1,(1+lam)/2,(1-lam)/2,0]
    checks['weight_derivative']=all(sp.simplify(sp.diff(w,u).subs(u,0)-t)==0 for w,t in zip(ws,target))
    labs=list(itertools.product(range(3),repeat=2));basis=[kron(ps[a],ps[b]) for a,b in labs]
    incoh=lambda h:(P*h*P+Q*h*Q)/2-h
    cross=lambda h:(P*h*Q+Q*h*P)/2
    one=[kron(p,I) for p in ps]+[kron(I,p) for p in ps]
    proj=lambda h:sp.Matrix([sp.simplify(sp.trace(o*h)/4) for o in one])
    checks['generator_split']=all(zero((1+lam)/2*(ap*h*ap-h)+(1-lam)/2*(am*h*am-h)-incoh(h)-lam*cross(h)) for h in basis)
    table={(0,0):kron(Z,I),(2,0):kron(X,I),(1,1):-kron(I,Z),(1,2):kron(I,Y)}
    checks['cross_leakage_table']=all(zero(proj(cross(h))-proj(table.get(lab,sp.zeros(4)))) for lab,h in zip(labs,basis))
    checks['incoherent_null']=all(zero(proj(incoh(h))) for h in basis)
    checks['local_hamiltonian_null']=all(zero(proj(-sp.I*(P*h-h*P))) for h in basis)
    checks['spectator_trace_and_TP']=all(sp.trace(p)==0 for p in ps) and all(zero(a.H*a-sp.eye(4)) for a in [ap,am])
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def response(cs,sc,ds,name):
    geom=V96.geometry(cs,sc,name)
    if not geom['domain']:return None,geom
    rs=np.array([e['R'] for e in geom['edges']]);ps=np.array([r.T@c for r,c in zip(rs,cs[:5])]);K=np.zeros((6,54));J=np.zeros((3,54));edge=np.zeros((5,3,54));res=0.
    for k,dc in enumerate(ds):
        dr=[]
        for e,(r,p,d) in enumerate(zip(rs,ps,dc[:5])):
            q,w=V93.tangent(r,p,d);dr.append(r@w);edge[e,:,k]=V93.coords(w)
            res=max(res,np.linalg.norm(p@w+w@p-q),np.linalg.norm(w+w.T))
        hs,dhs=loop_derivative(rs,dr)
        for i in range(2):
            tangent=dhs[i]@hs[i].T;res=max(res,np.linalg.norm(tangent+tangent.T));K[3*i:3*i+3,k]=V93.coords(skew(tangent))
        J[:,k]=invariant_derivative(hs,dhs)
    record={'K':K.tolist(),'J':J.tolist(),'K_singular_values':np.linalg.svd(K,compute_uv=False).tolist(),'J_singular_values':np.linalg.svd(J,compute_uv=False).tolist(),'K_ranks':ranks(K),'J_ranks':ranks(J),'edge_ranks':[ranks(e) for e in edge],'loop_ranks':[ranks(K[:3]),ranks(K[3:])],'family_ranks':[ranks(K[:,:27]),ranks(K[:,27:])],'loop_invariants':invariants(hs).tolist(),'loops':hs.tolist(),'identity_residual':float(res)}
    return record,geom


def finite_loops(outputs,centers,name):
    cs=correlations(outputs)[:,:5];sc=correlations(centers)[:,:5];left,sv,right=np.linalg.svd(cs);ref=np.linalg.svd(sc,compute_uv=False)[...,0]
    rr=left@right;det=np.linalg.det(rr);wanted=2 if name=='plane' else 3
    domain=np.ones(len(outputs),bool)
    for t in THRESHOLDS:domain &= np.all(np.sum(sv>t*ref[...,None],axis=-1)==wanted,axis=1)
    if name=='isotropic':domain &= np.all(det>0,axis=1)
    else:
        left=left.copy();left[..., :,2]*=det[...,None];rr=left@right
    if not np.all(domain):return None,None,domain.tolist()
    hs=np.stack([rr[:,0]@rr[:,1]@rr[:,2],rr[:,0]@rr[:,3]@rr[:,4]],axis=1)
    inv=np.stack([np.trace(hs[:,0],axis1=-2,axis2=-1),np.trace(hs[:,1],axis1=-2,axis2=-1),np.trace(hs[:,0]@hs[:,1],axis1=-2,axis2=-1)],axis=1)
    return hs,inv,domain.tolist()


def adjudicate(valid,full,plane):
    if not valid:return 'INVALID','INVALID'
    return ('OVERLAP_HIDDEN_RESPONSE_CONFIRMED' if full else 'OVERLAP_HIDDEN_RESPONSE_NOT_CONFIRMED','PLANAR_TWO_LOOP_RESPONSE_CONFIRMED' if plane else 'PLANAR_TWO_LOOP_RESPONSE_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    folder=HERE.parent/'overlap-holonomy-common-line';code=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    parents=(hashlib.sha256(code).hexdigest()=='56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52' and hashlib.sha256(gz).hexdigest()=='1102dd9da14f82cc44d958de15effe9b0553e3b6cf396deb1791f98a88527550' and hashlib.sha256(raw).hexdigest()=='99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e' and parent['all_valid'] and parent['verdict']=='OVERLAP_COMMON_LINE_OBSTRUCTION_CONFIRMED' and parent['planar_verdict']=='PLANAR_COMMON_LINE_PRESERVED')
    controls={k:0. for k in ['input_reconstruction','hidden_gram','hidden_trace','hidden_hermiticity','hidden_one','hidden_pair','generator_one','weight_four_null','hamiltonian_null','source_unitarity','weight_sum','mixed_connected','cross_leakage','geometry','derivative_identity','cross_loop','baseline_hidden','covariance','incoherent_norm','fd_K_final','fd_J_final']}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    physical={'min_eigenvalue':1.,'trace_error':0.,'hermiticity_error':0.,'count':0,'valid':True}
    def check_density(zs):
        z=np.asarray(zs).reshape(-1,16,16);d=V75.density_diagnostics(z);physical['min_eigenvalue']=min(physical['min_eigenvalue'],d['min_eigenvalue'])
        for k in ['trace_error','hermiticity_error']:physical[k]=max(physical[k],d[k])
        physical['valid']=physical['valid'] and d['valid'];physical['count']+=len(z)
    mx('hidden_gram',np.linalg.norm(np.einsum('hij,kji->hk',HIDDEN,HIDDEN)-np.eye(54)))
    mx('hidden_trace',np.max(np.abs(np.trace(HIDDEN,axis1=1,axis2=2))));mx('hidden_hermiticity',np.max(np.abs(HIDDEN-HIDDEN.conj().transpose(0,2,1))))
    mx('hidden_one',np.max(np.abs(single(HIDDEN))));mx('hidden_pair',np.max(np.abs(pairs(HIDDEN))))
    hamiltonian=V96.op(0,3);mx('hamiltonian_null',np.max(np.abs(pairs(-1j*(hamiltonian@HIDDEN-HIDDEN@hamiltonian)))))
    mx('source_unitarity',max(np.linalg.norm(u.conj().T@u-np.eye(16)) for u in UNITARIES))
    grid=sorted({0.,*[v for a in STEPS for v in [a,2*a]]});weight_min=1.
    for lam in LAMBDAS:
        mx('generator_one',np.max(np.abs(single(generator(HIDDEN,lam)))));mx('weight_four_null',np.max(np.abs(pairs(generator(FOUR,lam)))))
        for u in grid:
            w=V81.weights(lam,u);weight_min=min(weight_min,float(w.min()));mx('weight_sum',abs(w.sum()-1))
    exact=symbolic_certificate();frames_cert=V96.symbolic_certificate();prep_cert=V96.V92.symbolic_certificate()
    _,frames=V96.exact_frames();gs=[np.array(g.tolist(),float) for g,u in frames];bigU=V96.tensor([np.array(u.tolist(),complex) for g,u in frames]);rot_us=np.array([bigU@u@bigU.conj().T for u in UNITARIES]);rot_h=bigU@HIDDEN@bigU.conj().T
    g6=np.zeros((6,6));g6[:3,:3]=g6[3:,3:]=gs[0]
    armdata=V96.arms();selected=V96.M.V70.V64.ASYM.select_states();swap=V96.swap_matrix();rows=[];full=True;plane=True;null_valid=True;rank_cov=True
    for k,rec in enumerate(parent['input_states']):
        rho=np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in rec['state_hex']])
        rebuilt=(np.kron(selected[k]['rho'],np.eye(2)/2)+swap@np.kron(selected[(k+1)%12]['rho'],np.eye(2)/2)@swap.T)/2
        mx('input_reconstruction',np.linalg.norm(rho-rebuilt));inputs=np.concatenate([rho[None]+EPS*HIDDEN,rho[None]-EPS*HIDDEN]);check_density(inputs)
        for lam in LAMBDAS:
            lh=generator(HIDDEN,lam);rot_lh=generator(rot_h,lam,rot_us)
            for name,arm in armdata.items():
                scale=arm['scale'];T=arm['T'];center=V96.post(rho[None],scale)[0];tangents=V96.post(lh,scale);cs=correlations(center);sc=correlations(rho)
                # Direct mixed centering includes all terms, independently of the zero-moment simplification.
                ph=V96.post(HIDDEN,scale);lr=V96.post(generator(rho,lam)[None],scale)[0];n0=single(center);nh=single(ph);nl=single(lr);nlh=single(tangents);direct=pairs(tangents).copy()
                for e,(i,j) in enumerate(V96.EDGES):
                    direct[:,e]-=nlh[:,i,:,None]*n0[j,None,:]+n0[i,:,None]*nlh[:,j,None,:]+nh[:,i,:,None]*nl[j,None,:]+nl[i,:,None]*nh[:,j,None,:]
                ds=np.array([[T@c@T.T for c in d] for d in pairs(lh)]);mx('mixed_connected',np.max(np.abs(ds-direct)))
                mx('cross_leakage',max(np.linalg.norm(direct[:27,[0,3,4]]),np.linalg.norm(direct[27:,[0,1,2]])))
                response0,geom=response(cs,sc,direct,name);mx('geometry',geom['residual'])
                # Conjugate the preparation map itself, using transformed source/probe data.
                transformed=bigU@center@bigU.conj().T
                td=bigU@V96.post(bigU.conj().T@rot_lh@bigU,scale)@bigU.conj().T
                trho=bigU@rho@bigU.conj().T
                response1,geom1=response(correlations(transformed),correlations(trho),pairs(td),name);mx('geometry',geom1['residual'])
                if response0 is not None:
                    K=np.array(response0['K']);J=np.array(response0['J'])
                for rr in [response0,response1]:
                    if rr is not None:mx('derivative_identity',rr['identity_residual'])
                if response0 is not None and response1 is not None:
                    K1=np.array(response1['K']);J1=np.array(response1['J'])
                    mx('covariance',max(np.linalg.norm(K1-g6@K),np.linalg.norm(J1-J)))
                    rank_cov=rank_cov and all(response0[q]==response1[q] for q in ['K_ranks','J_ranks'])
                    mx('cross_loop',max(np.linalg.norm(K[:3,27:]),np.linalg.norm(K[3:,:27])))
                    if lam==0:
                        mx('incoherent_norm',max(np.linalg.norm(K),np.linalg.norm(J),np.linalg.norm(K1),np.linalg.norm(J1)))
                        null_valid=null_valid and all(rr[q]==[0,0,0] for rr in [response0,response1] for q in ['K_ranks','J_ranks'])
                finite={};finite_domains={}
                for u in grid:
                    centers=source(inputs,lam,u);outs=V96.post(centers,scale);check_density(centers);check_density(outs)
                    hs,iv,domain=finite_loops(outs,centers,name);finite_domains[str(u)]=domain
                    finite[u]=None if hs is None else ((hs[:54]-hs[54:])/(2*EPS),(iv[:54]-iv[54:])/(2*EPS))
                if finite[0.] is not None:mx('baseline_hidden',max(np.linalg.norm(finite[0.][0]),np.linalg.norm(finite[0.][1])))
                ladder=[];all_domains=bool(geom['domain'] and geom1['domain'] and all(all(d) for d in finite_domains.values()))
                for a in STEPS:
                    entry={'step':a,'K_error':None,'J_error':None}
                    if response0 is not None and all(finite[u] is not None for u in [0.,a,2*a]):
                        dH=(-3*finite[0.][0]+4*finite[a][0]-finite[2*a][0])/(2*a);jfd=((-3*finite[0.][1]+4*finite[a][1]-finite[2*a][1])/(2*a)).T;hs0=np.array(response0['loops'])
                        kfd=np.array([np.concatenate([V93.coords(skew(dh[i]@hs0[i].T)) for i in range(2)]) for dh in dH]).T
                        entry['K_error']=float(np.linalg.norm(kfd-K)/max(1.,np.linalg.norm(K)));entry['J_error']=float(np.linalg.norm(jfd-J)/max(1.,np.linalg.norm(J)))
                        if a==STEPS[-1]:mx('fd_K_final',entry['K_error']);mx('fd_J_final',entry['J_error'])
                    ladder.append(entry)
                if lam!=0:
                    kr=[6]*3 if name=='isotropic' else [2]*3;jr=[3]*3 if name=='isotropic' else [2]*3
                    passed=all_domains and all(rr['K_ranks']==kr and rr['J_ranks']==jr for rr in [response0,response1])
                    if name=='isotropic':full=full and passed
                    else:plane=plane and passed
                else:passed=None
                rows.append({'candidate_index':rec['candidate_index'],'lambda':lam,'arm':name,'all_domains':all_domains,'baseline_domain':geom['domain'],'transformed_domain':geom1['domain'],'baseline_edges':geom['edges'],'response':response0,'transformed_response':response1,'finite_domains':finite_domains,'finite_difference':ladder,'scientific_pass':passed})
    indices=[r['candidate_index'] for r in parent['input_states']]
    limits={k:1e-12 for k in controls}
    limits.update(input_reconstruction=1e-15,geometry=1e-9,derivative_identity=1e-9,cross_loop=1e-9,baseline_hidden=1e-9,covariance=1e-9,incoherent_norm=1e-9,fd_K_final=1e-4,fd_J_final=1e-4)
    valid=bool(parents and indices==V96.EXPECTED and len(rows)==72 and exact['valid'] and frames_cert['valid'] and prep_cert['valid'] and physical['valid'] and null_valid and rank_cov and weight_min>=-1e-12 and all(v<=limits[k] for k,v in controls.items()))
    controls.update(parents_valid=bool(parents),symbolic_certificate=exact,frame_certificate=frames_cert,preparation_certificate=prep_cert,physicality=physical,minimum_weight=weight_min,incoherent_ranks_valid=bool(null_valid),rank_covariance_valid=bool(rank_cov),limits=limits)
    verdict,pv=adjudicate(valid,full,plane)
    result={'version':'15.97','all_valid':valid,'verdict':verdict,'planar_verdict':pv,'full_predicate':bool(full),'plane_predicate':bool(plane),'candidate_indices':indices,'hidden_count':54,'weight_four_count':81,'hidden_labels':HIDDEN_LABELS,'controls':controls,'rows':rows,'scope':'Specified source-origin mixed response of pair-hidden probes; not hidden from corresponding three-site regions. Not continuous holonomy or physical source-law selection.'}
    def finite_data(x):
        if isinstance(x,dict):return all(finite_data(v) for v in x.values())
        if isinstance(x,(tuple,list)):return all(finite_data(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite_data(result):result['all_valid']=False;result['verdict']=result['planar_verdict']='INVALID'
    return result

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False));sys.exit(0 if result['all_valid'] else 2)
