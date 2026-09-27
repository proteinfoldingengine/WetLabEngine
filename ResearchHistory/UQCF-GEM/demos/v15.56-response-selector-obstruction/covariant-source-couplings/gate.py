"""v15.79: a restricted covariant bilinear response class, not a CP-law class."""
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('covariance78_couplings',HERE.parent/'source-free-covariance'/'gate.py')
V78=importlib.util.module_from_spec(spec);spec.loader.exec_module(V78)
V75=V78.V75;V74=V75.V74;M=V78.M
LABELS=V78.LABELS
SLABELS=LABELS[1:];HLABELS=list(itertools.product(range(1,4),repeat=3))
RLABELS=[]
for site in range(3):
    for a in range(1,4):
        p=[0,0,0];p[site]=a;RLABELS.append(tuple(p))
for i,j in M.EDGES:
    for a in range(1,4):
        for b in range(1,4):
            p=[0,0,0];p[i]=a;p[j]=b;RLABELS.append(tuple(p))
RIDX=np.array([LABELS.index(p) for p in RLABELS]);HIDX=V78.HIDX
SUPPORTS=[tuple(c) for n in range(1,4) for c in itertools.combinations(range(3),n)]
TARGETS=[s for s in SUPPORTS if len(s)<3]
THRESHOLDS=[1e-9,1e-10,1e-11]


def local_tensor(source_vector,output_vector):
    ds=3 if source_vector else 1;do=3 if output_vector else 1
    t=np.zeros((do,ds,3))
    if not source_vector and output_vector:t[:,0,:]=np.eye(3)
    if source_vector and not output_vector:t[0,:,:]=np.eye(3)
    if source_vector and output_vector:
        for r,a,h in itertools.permutations(range(3)):
            t[r,a,h]=1 if (r,a,h) in [(0,1,2),(1,2,0),(2,0,1)] else -1
    return t


def generators():
    out=[]
    for n in np.eye(3):out.append(np.array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]]))
    return out


def local_classification():
    rows=[];max_res=0.;max_projector=0.
    for source in [False,True]:
        for output in [False,True]:
            ds=3 if source else 1;do=3 if output else 1;di=ds*3
            blocks=[]
            for j in generators():
                js=j if source else np.zeros((1,1));jo=j if output else np.zeros((1,1))
                ji=np.kron(js,np.eye(3))+np.kron(np.eye(ds),j)
                blocks.append(np.kron(jo,np.eye(di))-np.kron(np.eye(do),ji.T))
            a=np.concatenate(blocks);_,sv,vh=np.linalg.svd(a,full_matrices=False)
            ref=float(sv[0]);ranks=[int(np.count_nonzero(sv>t*ref)) for t in THRESHOLDS]
            null=vh[sv<=1e-10*ref].T;projector=null@null.T
            max_res=max(max_res,float(np.linalg.norm(a@null)))
            target=local_tensor(source,output).ravel();tn=float(np.linalg.norm(target))
            if tn:max_projector=max(max_projector,float(np.linalg.norm(projector-np.outer(target,target)/(tn*tn))))
            rows.append({'source_vector':source,'output_vector':output,'unknowns':do*di,
                         'ranks':ranks,'nullities':[do*di-r for r in ranks],
                         'singular_values':sv.tolist(),'kernel_projector':projector.tolist()})
    return rows,max_res,max_projector


def build_tensors():
    tensors=[];labels=[]
    for s in SUPPORTS:
        for t in TARGETS:
            if set(s)|set(t)!={0,1,2}:continue
            b=np.zeros((63,27,36));local=[local_tensor(q in s,q in t) for q in range(3)]
            for si,a in enumerate(SLABELS):
                if tuple(q for q,v in enumerate(a) if v)!=s:continue
                for ri,r in enumerate(RLABELS):
                    if tuple(q for q,v in enumerate(r) if v)!=t:continue
                    for hi,h in enumerate(HLABELS):
                        val=1.
                        for q in range(3):val*=local[q][r[q]-1 if q in t else 0,a[q]-1 if q in s else 0,h[q]-1]
                        b[si,hi,ri]=val
            k=len(set(s)&set(t));labels.append({'source_support':list(s),'target_support':list(t),'cross_count':k})
            tensors.append(b)
    return np.array(tensors),labels


def site_generator(j,site):
    d=np.zeros((4,4));d[1:,1:]=j
    factors=[d if q==site else np.eye(4) for q in range(3)]
    return np.kron(np.kron(factors[0],factors[1]),factors[2])


def covariance_error(b,action,infinitesimal=False):
    source=action[1:,1:];hidden=action[np.ix_(HIDX,HIDX)];ret=action[np.ix_(RIDX,RIDX)]
    lhs=np.einsum('or,cshr->csho',ret,b,optimize=True)
    if infinitesimal:
        rhs=np.einsum('cthr,ts->cshr',b,source,optimize=True)+np.einsum('cskr,kh->cshr',b,hidden,optimize=True)
    else:rhs=np.einsum('ctkr,ts,kh->cshr',b,source,hidden,optimize=True)
    return float(np.linalg.norm(lhs-rhs))


def describe(a,include_gram=True):
    sv=np.linalg.svd(a,compute_uv=False);ref=float(sv[0])
    r={'shape':list(a.shape),'norm':float(np.linalg.norm(a)),'singular_values':sv.tolist(),
       'ranks':[int(np.count_nonzero(sv>t*ref)) for t in THRESHOLDS],
       'smallest_to_largest':float(sv[-1]/ref)}
    if include_gram:r['Gram']=(a.T@a).tolist()
    return r


def maps(rho,b,weights_source,weights_hidden):
    raw=(np.sqrt(8)*np.eye(36))[None,:,:]
    q,e,sy=V74.geometry_from_retained(rho,raw)
    fq=q.reshape(36,9).T;fe=e.reshape(36,9).T
    qs=np.einsum('or,cshr->shoc',fq,b,optimize=True).reshape(15309,len(b))
    es=np.einsum('or,cshr->shoc',fe,b,optimize=True).reshape(15309,len(b))
    coeff=np.einsum('s,h,cshr->cr',weights_source,weights_hidden,b,optimize=True)
    dq,de,ds=V74.geometry_from_retained(rho,(np.sqrt(8)*coeff)[:,None,:])
    aq=np.einsum('s,h,shoc->oc',weights_source,weights_hidden,qs.reshape(63,27,9,len(b)),optimize=True)
    ae=np.einsum('s,h,shoc->oc',weights_source,weights_hidden,es.reshape(63,27,9,len(b)),optimize=True)
    return qs,es,max(sy,ds),float(np.max(np.abs(aq-dq))),float(np.max(np.abs(ae-de)))


def adjudicate(valid,primary,observable):
    if not valid:return 'INVALID','INVALID'
    return ('COVARIANT_SOURCE_COUPLING_CLASSIFICATION_CONFIRMED' if primary else 'COVARIANT_SOURCE_COUPLING_CLASSIFICATION_NOT_CONFIRMED',
            'COVARIANT_COUPLINGS_ENSEMBLE_NULL_EXCLUDED' if observable else 'COVARIANT_COUPLINGS_ENSEMBLE_NULL_NOT_EXCLUDED')


def run_measurement():
    c={};mx=lambda k,v:V78.V77.maximize(c,k,v)
    selected=M.V70.V64.ASYM.select_states();indices=[r['candidate_index'] for r in selected]
    zero=V74.control_fixture();domain=M.domain([r['rho'] for r in selected]+[zero])
    sources=np.array([M.F.op(*p) for p in SLABELS]);hidden=np.array(M.HIDDEN);ret=V75.G
    expected_h=np.array([M.F.op(*p)/np.sqrt(8) for p in HLABELS])
    expected_r=np.array([M.F.op(*p)/np.sqrt(8) for p in RLABELS])
    mx('basis_order',np.linalg.norm(hidden-expected_h));mx('basis_order',np.linalg.norm(ret-expected_r))
    for bs,scale in [(sources,8),(hidden,1),(ret,1)]:
        mx('basis_normalization',np.linalg.norm(np.einsum('aij,bji->ab',bs,bs)/scale-np.eye(len(bs))))
    local,lr,lp=local_classification();mx('local_kernel_residual',lr);mx('local_projector_error',lp)
    multiplicities={(int(r['source_vector']),int(r['output_vector'])):r['nullities'][1] for r in local}
    allowed=[]
    for s in SUPPORTS:
        for t in TARGETS:
            dim=int(np.prod([multiplicities[(int(q in s),int(q in t))] for q in range(3)]))
            if dim:allowed.append({'source_support':list(s),'target_support':list(t),'multiplicity':dim})
    scalar_dims=[int(np.prod([multiplicities[(0,int(q in t))] for q in range(3)])) for t in TARGETS]
    b,labels=build_tensors();flat=b.reshape(len(b),-1).T;expected_diag=np.array([27*2**x['cross_count'] for x in labels])
    mx('tensor_Gram_error',np.linalg.norm(flat.T@flat-np.diag(expected_diag)))
    for site in range(3):
        for j in generators():mx('generator_covariance',covariance_error(b,site_generator(j,site),True))
        for axis,angle in [(0,np.pi/7),(2,np.pi/5)]:
            j=generators()[axis];r=np.eye(3)+np.sin(angle)*j+(1-np.cos(angle))*(j@j)
            mx('finite_covariance',covariance_error(b,V78.site_action(r,site)))
    comm_weights=np.array([1. if x['cross_count']==1 else 0. for x in labels])
    jordan_weights=np.array([1. if x['cross_count']==0 else -1. if x['cross_count']==2 else 0. for x in labels])
    predicted_comm=np.einsum('c,cshr->shr',comm_weights,b)
    predicted_jordan=np.einsum('c,cshr->shr',jordan_weights,b)
    theta=np.pi/4
    for si,p in enumerate(sources):
        u=np.cos(theta/2)*np.eye(8)-1j*np.sin(theta/2)*p
        mx('unitarity',np.linalg.norm(u.conj().T@u-np.eye(8)))
        for hi,h in enumerate(hidden):
            comm=-.5j*(p@h-h@p)
            jordan=.5*(p@h+h@p)-np.trace(p@h)*np.eye(8)/8
            for tangent,pred,key in [(comm,predicted_comm[si,hi],'commutator_error'),(jordan,predicted_jordan[si,hi],'Jordan_error')]:
                mx('tangent_trace',abs(np.trace(tangent)));mx('tangent_hermiticity',np.linalg.norm(tangent-tangent.conj().T))
                coeff=np.einsum('ij,rji->r',tangent,ret)
                mx('imaginary_moments',np.max(np.abs(coeff.imag)));mx(key,np.max(np.abs(coeff-pred)))
            finite=np.einsum('ij,rji->r',u@h@u.conj().T,ret)
            mx('finite_unitary_error',np.max(np.abs(finite-np.sin(theta)*predicted_comm[si,hi])))
    for h in hidden:
        # Scalar source I gives zero commutator and a hidden-only Jordan output.
        for tangent in [np.zeros_like(h),h-np.trace(h)*np.eye(8)/8]:
            mx('identity_source_retained',np.linalg.norm(np.einsum('ij,rji->r',tangent,ret)))
    source_weights=np.array([(-1.)**j/(j+1) for j in range(63)])
    hidden_weights=np.array([(-1.)**j/(j+1) for j in range(27)])
    states=[];all_q=[];all_e=[]
    for rec in selected:
        q,e,sy,aq,ae=maps(rec['rho'],b,source_weights,hidden_weights)
        mx('sylvester',sy);mx('assembly_Q',aq);mx('assembly_E',ae)
        states.append({'candidate_index':rec['candidate_index'],'Q':describe(q),'E':describe(e)})
        all_q.append(q);all_e.append(e)
    sq=describe(np.concatenate(all_q));se=describe(np.concatenate(all_e))
    q,e,sy,aq,ae=maps(zero,b,source_weights,hidden_weights)
    mx('sylvester',sy);mx('assembly_Q',aq);mx('assembly_E',ae)
    mx('zero_one_body',np.linalg.norm(M.moments(zero,M.ONE)))
    mx('zero_correlations',np.linalg.norm(M.correlations(zero)-.04*np.eye(3)[None,:,:]))
    singles=np.array([i for i,x in enumerate(labels) if len(x['target_support'])==1]);pzero=np.zeros((len(b),len(b)));pzero[singles,singles]=1
    exceptional={};exception_ok=len(singles)==6
    for name,mat in [('Q',q),('E',e)]:
        d=describe(mat);_,sv,vh=np.linalg.svd(mat,full_matrices=False)
        null=vh[sv<=1e-10*sv[0]].T;pe=float(np.linalg.norm(null@null.T-pzero));rel=float(np.linalg.norm(mat[:,singles])/np.linalg.norm(mat))
        d.update(kernel_projector=(null@null.T).tolist(),expected_projector_error=pe,one_body_relative_norm=rel)
        exceptional[name]=d;exception_ok=exception_ok and d['ranks']==[12]*3 and pe<=1e-9 and rel<=1e-12
    bd=describe(flat);counts=[sum(x['multiplicity'] for x in allowed if len(x['source_support'])==w) for w in [1,2,3]]
    primary=(all(r['nullities']==[expected]*3 for r,expected in zip(local,[0,1,1,1]))
             and sum(x['multiplicity'] for x in allowed)==18 and counts==[3,9,6]
             and bd['ranks']==[18]*3 and int(np.count_nonzero(comm_weights))==9
             and int(np.count_nonzero(jordan_weights))==9 and scalar_dims==[0]*6)
    observable=sq['ranks']==[18]*3 and se['ranks']==[18]*3
    limits={k:1e-12 for k in ['basis_order','basis_normalization','local_kernel_residual','tensor_Gram_error','unitarity','tangent_trace','tangent_hermiticity','imaginary_moments','commutator_error','Jordan_error','finite_unitary_error','identity_source_retained','zero_one_body','zero_correlations']}
    limits.update(local_projector_error=1e-10,generator_covariance=1e-11,finite_covariance=1e-11,sylvester=1e-11,assembly_Q=1e-10,assembly_E=1e-10)
    valid=(indices==M.EXPECTED and domain['valid'] and len(ret)==36 and len(sources)==63 and len(hidden)==27 and exception_ok and all(c[k]<=v for k,v in limits.items()))
    c['exceptional_control_valid']=bool(exception_ok)
    verdict,obs=adjudicate(valid,primary,observable)
    report={'version':'15.79','candidate_indices':indices,'source_count':63,'hidden_count':27,
            'all_valid':bool(valid),'verdict':verdict,'observability_verdict':obs,'controls':c,'domain':domain,
            'classification':{'local':local,'allowed_pairs':allowed,'source_weight_counts':counts,
                              'scalar_source_multiplicities':scalar_dims,'tensor_labels':labels,'tensor_basis':bd,
                              'commutator_coefficients':comm_weights.tolist(),'Jordan_coefficients':jordan_weights.tolist()},
            'states':states,'stacked_Q':sq,'stacked_E':se,'zero_Bloch':exceptional}
    report=M.V70.finalize_report(report)
    if not report['all_valid']:report['observability_verdict']='INVALID'
    return report

if __name__=='__main__':
    result=run_measurement();print(json.dumps(result,indent=2,allow_nan=False))
    sys.exit(0 if result['all_valid'] else 2)
