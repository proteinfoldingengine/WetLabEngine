"""v16.01: independently formed global operators at 50/80 digits."""
import functools
import gzip
import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys
import numpy as np
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('readout100_global',HERE.parent/'precision-readout-audit'/'gate.py')
V100=importlib.util.module_from_spec(spec);spec.loader.exec_module(V100)
V96=V100.V96;V98=V100.V98
LABELS=list(itertools.product(range(4),repeat=4));INDEX={w:i for i,w in enumerate(LABELS)}
WEIGHT=[sum(x!=0 for x in w) for w in LABELS];CASES=V100.CASES;PRECISIONS=[50,80]
norm=V100.norm;ns=V100.ns


@functools.lru_cache(maxsize=256)
def monomial(w):
    out=[]
    for col in range(16):
        row=col;phase=1+0j
        for site,p in enumerate(w):
            bit=(col>>(3-site))&1
            if p in [1,2]:row^=1<<(3-site)
            if p==2:phase*=1j if bit==0 else -1j
            if p==3:phase*=1 if bit==0 else -1
        out.append((row,phase))
    return out


def coefficients(rho):
    v=mp.zeros(256,1);imag=mp.mpf(0)
    for k,w in enumerate(LABELS):
        z=mp.fsum(mp.mpc(phase)*rho[col,row] for col,(row,phase) in enumerate(monomial(w)))/4
        imag=max(imag,abs(mp.im(z)));v[k]=z
    if imag>mp.mpf('1e-35'):raise ValueError('Hermitian Pauli coefficient imaginary residual exceeds frozen limit')
    return mp.matrix([mp.re(x) for x in v]),imag


def reconstruct(v):
    rho=mp.zeros(16)
    for k,w in enumerate(LABELS):
        for col,(row,phase) in enumerate(monomial(w)):rho[row,col]+=v[k]*mp.mpc(phase)/4
    return rho


def kron(a,b):return mp.matrix([[a[i//b.rows,j//b.cols]*b[i%b.rows,j%b.cols] for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def paulis():return [mp.eye(2),mp.matrix([[0,1],[1,0]]),mp.matrix([[0,-mp.j],[mp.j,0]]),mp.matrix([[1,0],[0,-1]])]


def transfer(terms,k,generator=False):
    ps=paulis();basis=ps if k==1 else [kron(a,b) for a in ps for b in ps];d=2**k;t=mp.zeros(d*d);imag=mp.mpf(0);reconstruction=mp.mpf(0)
    for j,p in enumerate(basis):
        y=mp.zeros(d)
        for weight,u in terms:y+=weight*(u*p*u.H)
        if generator:y-=p
        for i,q in enumerate(basis):
            z=mp.fsum(q[a,b]*y[b,a] for a in range(d) for b in range(d))/d;imag=max(imag,abs(mp.im(z)));t[i,j]=z
        if imag>mp.mpf('1e-35'):raise ValueError('transfer coefficient imaginary residual exceeds frozen limit')
        rebuilt=mp.zeros(d)
        for i,q in enumerate(basis):t[i,j]=mp.re(t[i,j]);rebuilt+=t[i,j]*q
        reconstruction=max(reconstruction,norm(rebuilt-y))
    trace=norm(mp.matrix([[t[0,j]-(0 if generator else int(j==0)) for j in range(d*d)]]))
    return t,{'imaginary_residual':ns(imag),'basis_reconstruction':ns(reconstruction),'trace_residual':ns(trace)}


@functools.lru_cache(maxsize=None)
def groups(sites):
    rest=[i for i in range(4) if i not in sites];out=[]
    for env in itertools.product(range(4),repeat=len(rest)):
        indices=[]
        for local in itertools.product(range(4),repeat=len(sites)):
            w=[0]*4
            for i,x in zip(rest,env):w[i]=x
            for i,x in zip(sites,local):w[i]=x
            indices.append(INDEX[tuple(w)])
        out.append(indices)
    return out


def apply(t,sites,v):
    out=mp.zeros(256,v.cols)
    for inds in groups(tuple(sites)):
        block=mp.matrix([[v[i,j] for j in range(v.cols)] for i in inds]);result=t*block
        for k,i in enumerate(inds):
            for j in range(v.cols):out[i,j]=result[k,j]
    return out


def product_action(ts,v):
    for site,t in enumerate(ts):v=apply(t,(site,),v)
    return v


def middle(v,a):
    factors=[a**w for w in WEIGHT]
    return mp.matrix([[factors[i]*v[i,j] for j in range(v.cols)] for i in range(256)])


def restrict_norm(v,max_weight):return mp.sqrt(mp.fsum(abs(v[i,j])**2 for i,w in enumerate(WEIGHT) if w<=max_weight for j in range(v.cols)))


def unit(w):
    v=mp.zeros(256,1);v[INDEX[tuple(w)]]=1;return v


@functools.lru_cache(maxsize=2)
def laws(dps):
    with mp.workdps(dps):
        ps=paulis();us=[];frames=[];cert=[];unitarity=mp.mpf(0);frame_identity=mp.mpf(0);gs,_=V100.exact_frames()
        for site,(w,x,y,z) in enumerate(V96.QUATS):
            u=(w*ps[0]-mp.j*(x*ps[1]+y*ps[2]+z*ps[3]))/mp.sqrt(w*w+x*x+y*y+z*z);us.append(u)
            unitarity=max(unitarity,norm(u.H*u-mp.eye(2)),abs(mp.det(u)-1));t,c=transfer([(1,u)],1);frames.append(t);cert.append(c)
            target=mp.zeros(4);target[0,0]=1
            for i in range(3):
                for j in range(3):target[i+1,j+1]=gs[site][i,j]
            frame_identity=max(frame_identity,norm(t-target),norm(t.T*t-mp.eye(4)))
        ap=(kron(ps[3],ps[0])+kron(ps[1],ps[1]))/mp.sqrt(2);tn,c=transfer([(1,ap)],2,True);cert.append(c)
        unitarity=max(unitarity,norm(ap.H*ap-mp.eye(4)),norm(ap-ap.H),norm((tn+mp.eye(16)).T*(tn+mp.eye(16))-mp.eye(16)))
        src=[{},{}]
        for key,(i,j) in V98.SITES.items():
            src[0][key]=tn;u=kron(us[i],us[j]);rot=u*ap*u.H;tr,c=transfer([(1,rot)],2,True);src[1][key]=tr;cert.append(c)
            unitarity=max(unitarity,norm(rot.H*rot-mp.eye(4)),norm(rot-rot.H),norm((tr+mp.eye(16)).T*(tr+mp.eye(16))-mp.eye(16)))
        weights=[mp.mpf(1)/2,mp.mpf(1)/4,mp.mpf(1)/4];prep=[[],[]]
        f,c=transfer(list(zip(weights,ps[:3])),1);cert.append(c)
        for site,u in enumerate(us):
            prep[0].append(f);fr,c=transfer(list(zip(weights,[ps[0],u*ps[1]*u.H,u*ps[2]*u.H])),1);prep[1].append(fr);cert.append(c)
        maxerr=max([unitarity,frame_identity]+[mp.mpf(v) for c in cert for v in c.values()])
        controls={'local_certificates':cert,'unitarity':ns(unitarity),'frame_identity':ns(frame_identity),'weights':[ns(x) for x in weights],'maximum_residual':ns(maxerr),'valid':bool(maxerr<=mp.mpf('1e-35') and sum(weights)==1 and min(weights)>=0)}
        return {'frames':frames,'source':src,'preparation':prep,'controls':controls}


@functools.lru_cache(maxsize=2)
def witness_controls(dps):
    with mp.workdps(dps):
        data=laws(dps);err=mp.mpf(0)
        for av in [1.,1/3,1/6]:
            a=V100.exact_float(av)
            for w,second,target,sign in [((2,2,1,1),'B',(0,1,0,1),-1),((1,1,1,1),'D',(3,0,3,0),1)]:
                first=apply(data['source'][0]['A'],V98.SITES['A'],unit(w));y=apply(data['source'][0][second],V98.SITES[second],middle(first,a));expected=sign*a**3*unit(target)
                err=max(err,restrict_norm(y-expected,2))
        return {'precision_digits':dps,'maximum_error':ns(err),'valid':bool(err<=mp.mpf('1e-35') and data['controls']['valid'])}


def one(v,col):
    out=[]
    for site in range(4):
        arr=[]
        for axis in [1,2,3]:
            w=[0]*4;w[site]=axis;arr.append(4*v[INDEX[tuple(w)],col])
        out.append(mp.matrix(arr))
    return out


def pair_moments(v,col):
    out=[]
    for i,j in V96.EDGES:
        p=mp.zeros(3)
        for a in [1,2,3]:
            for b in [1,2,3]:
                w=[0]*4;w[i]=a;w[j]=b;p[a-1,b-1]=4*v[INDEX[tuple(w)],col]
        out.append(p)
    return out


def correlations(v):
    singles=one(v,0);pairs=pair_moments(v,0)
    return [p-singles[i]*singles[j].T for p,(i,j) in zip(pairs,V96.EDGES)]


def retained(base,center,y):
    singles=one(center,0);ds=[]
    for k in range(y.cols):
        dn=one(y,k);pairs=pair_moments(y,k)
        ds.append([p-dn[i]*singles[j].T-singles[i]*dn[j].T for p,(i,j) in zip(pairs,V96.EDGES)])
    return {'cs':correlations(center),'sc':correlations(base),'ds':ds}


def input_distance(a,b):
    return max([mp.sqrt(mp.fsum(norm(x-y)**2 for x,y in zip(a[k],b[k]))) for k in ['cs','sc']]+[mp.sqrt(mp.fsum(norm(x-y)**2 for xx,yy in zip(a['ds'],b['ds']) for x,y in zip(xx,yy)))])


def encode_inputs(a):return {'cs':[V100.encoded(c) for c in a['cs']],'sc':[V100.encoded(c) for c in a['sc']],'ds':[[V100.encoded(c) for c in dd] for dd in a['ds']]}
def decode_inputs(a):return {'cs':[V100.decoded(c) for c in a['cs']],'sc':[V100.decoded(c) for c in a['sc']],'ds':[[V100.decoded(c) for c in dd] for dd in a['ds']]}
def old_inputs(a):
    convert=lambda c:mp.matrix([[V100.exact_float(float.fromhex(v)) for v in row] for row in c])
    return {'cs':[convert(c) for c in a['cs']],'sc':[convert(c) for c in a['sc']],'ds':[[convert(c) for c in dd] for dd in a['ds']]}


def adjudicate(valid,recovered):
    if not valid:return 'INVALID'
    return 'GLOBAL_INPUT_PRECISION_RECOVERY_CONFIRMED' if recovered else 'GLOBAL_INPUT_PRECISION_RECOVERY_NOT_CONFIRMED'


@functools.lru_cache(maxsize=1)
def run_measurement():
    f=HERE.parent/'precision-readout-audit';code=(f/'gate.py').read_bytes();gz=(f/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    inputraw=gzip.decompress((HERE.parent/'overlap-holonomy-common-line'/'RESULT.json.gz').read_bytes());inputdata=json.loads(inputraw)
    pinned=hashlib.sha256(code).hexdigest()=='7eeead6262372ac6e57fc1a39d90775bd883227c017285997079c8fd70261fab' and hashlib.sha256(gz).hexdigest()=='ccebbb43faf27b7c5d8825e9b53571067ca40011c575618119f059550effa4a2' and hashlib.sha256(raw).hexdigest()=='7d2fcc55c51474f12ac596ca5321d6a8e22265560066d64ded61e945ffd0fd24' and hashlib.sha256(inputraw).hexdigest()=='99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e'
    pinned=pinned and parent['all_valid'] and parent['verdict']=='FROZEN_INPUT_RANK_RESIDUAL_PERSISTS' and len(parent['cases'])==8 and all(not c['recovered'] for c in parent['cases'])
    old={(c['candidate_index'],c['a'],c['pair'],c['order']):c for c in parent['cases']}
    states={r['candidate_index']:np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in r['state_hex']]) for r in inputdata['input_states'] if r['candidate_index'] in [66,77]}
    physical=V100.V99.V75.density_diagnostics(np.array(list(states.values())));valid=bool(pinned and physical['valid']);recovered=True
    cases=[{'candidate_index':idx,'a':a,'pair':pair,'order':order,'precision_results':{},'precision_metrics':[]} for idx,a,pair,order in CASES]
    controls={'pinned_parent':bool(pinned),'physicality':physical,'precisions':[]};previous_stages=None;maxconvergence=mp.mpf(0)
    for dps in PRECISIONS:
        with mp.workdps(dps):
            data=laws(dps);gs,g6=V100.exact_frames();stages={};stage_res={};null=mp.mpf(0);reconstruction=mp.mpf(0);imag=mp.mpf(0);roundtrip=True
            def stage(name,native,rotated):
                if name not in stages:
                    stages[name]=(native,rotated);stage_res[name]=norm(rotated-product_action(data['frames'],native))
                return stages[name]
            h=mp.zeros(256,81)
            for k,w in enumerate(V98.H_LABELS):h[INDEX[w],k]=1
            hs=stage('input_probes',h,product_action(data['frames'],h));null=max(null,*(restrict_norm(v,2) for v in hs))
            for key in V98.SITES:
                first=stage('first_'+key,*[apply(data['source'][frame][key],V98.SITES[key],hs[frame]) for frame in [0,1]])
                null=max(null,*(restrict_norm(v,2) for v in first))
            for idx,z in states.items():
                rho=mp.matrix([[V100.exact_complex(v) for v in row] for row in z]);roundtrip=roundtrip and all(complex(rho[i,j])==complex(z[i,j]) for i in range(16) for j in range(16));cv,im=coefficients(rho);imag=max(imag,im);reconstruction=max(reconstruction,norm(reconstruct(cv)-rho))
                stage('state_'+str(idx),cv,product_action(data['frames'],cv))
            def derivatives(a0,pair,order):
                a=V100.exact_float(a0);keys=V98.PAIRS[pair];ys={}
                for o,(first,second) in zip(['forward','reverse'],[keys,keys[::-1]]):
                    cutname='cut_'+str(a0)+'_'+first
                    if cutname not in stages:stage(cutname,*[middle(v,a) for v in stages['first_'+first]])
                    nulls=stages[cutname]
                    name='second_'+str(a0)+'_'+first+second
                    if name not in stages:stage(name,*[apply(data['source'][frame][second],V98.SITES[second],nulls[frame]) for frame in [0,1]])
                    ys[o]=stages[name]
                if order=='contrast':return stage('contrast_'+str(a0)+'_'+pair,*[ys['forward'][frame]-ys['reverse'][frame] for frame in [0,1]])
                return ys[order]
            for c,(idx,a0,pair,order) in zip(cases,CASES):
                a=V100.exact_float(a0);basekey='base_'+str(idx)+'_'+str(a0);centerkey='center_'+str(idx)+'_'+str(a0)
                if basekey not in stages:stage(basekey,*[middle(v,a) for v in stages['state_'+str(idx)]])
                if centerkey not in stages:stage(centerkey,*[product_action(data['preparation'][frame],stages[basekey][frame]) for frame in [0,1]])
                ys=derivatives(a0,pair,order);null=max(null,*(restrict_norm(v,1) for v in ys));pkey='prepared_'+str(a0)+'_'+pair+'_'+order
                if pkey not in stages:stage(pkey,*[product_action(data['preparation'][frame],ys[frame]) for frame in [0,1]])
                inputs=[retained(stages[basekey][frame],stages[centerkey][frame],stages[pkey][frame]) for frame in [0,1]]
                rc=input_distance(inputs[1],V100.transport(inputs[0],gs));ni=input_distance(inputs[0],old_inputs(old[idx,a0,pair,order]['retained_inputs_hex']['native']))
                results={};matrices={};identity=mp.mpf(0);failed=None
                for name,inp in zip(['native','transformed'],inputs):
                    try:
                        rr,k,j=V100.readout(inp);results[name]={'inputs':encode_inputs(inp),'response':rr};matrices[name]=(k,j);identity=max(identity,mp.mpf(rr['identity_residual']))
                    except ValueError as exc:failed=str(exc);results[name]={'error':failed}
                c['precision_results'][str(dps)]=results
                if failed is not None:valid=False;recovered=False;c['precision_metrics'].append({'precision_digits':dps,'error':failed});continue
                k,j=matrices['native'];kt,jt=matrices['transformed'];response_cov=max(norm(kt-g6*k),norm(jt-j));prior=old[idx,a0,pair,order]['precision_results']['80']['native'];ri=max(norm(k-V100.decoded(prior['K'])),norm(j-V100.decoded(prior['J'])))
                expected=1 if idx==66 else 2;rankok=all(results[n]['response'][key]==[expected]*3 for n in results for key in ['K_ranks','J_ranks'])
                pervalid=ni<=mp.mpf('1e-12') and ri<=mp.mpf('1e-9') and identity<=mp.mpf('1e-35') and all(results[n]['response']['finite'] for n in results)
                passed=rc<=mp.mpf('1e-35') and response_cov<=mp.mpf('1e-35') and rankok;valid=valid and pervalid;recovered=recovered and passed
                c['precision_metrics'].append({'precision_digits':dps,'native_input_identity':ns(ni),'native_response_identity':ns(ri),'retained_covariance':ns(rc),'response_covariance':ns(response_cov),'arithmetic_identity':ns(identity),'rank_recovered':bool(rankok),'valid':bool(pervalid),'recovered':bool(passed),
                    'ranks':{n:{key:results[n]['response'][key] for key in ['K_ranks','J_ranks']} for n in results}})
            for name,(native,rotated) in stages.items():
                if name.startswith('cut_'):null=max(null,restrict_norm(native,2),restrict_norm(rotated,2))
                if name.startswith('second_'):null=max(null,restrict_norm(native,1),restrict_norm(rotated,1))
            stage_cov=max(stage_res.values());wc=witness_controls(dps);sc=V100.solver_controls(dps)
            pvalid=data['controls']['valid'] and wc['valid'] and sc['valid'] and roundtrip and reconstruction<=mp.mpf('1e-35') and imag<=mp.mpf('1e-35') and null<=mp.mpf('1e-35')
            convergence=mp.mpf(0)
            if previous_stages is not None:
                for name,vs in stages.items():
                    for v,oldv in zip(vs,previous_stages[name]):convergence=max(convergence,norm(v-oldv))
                pvalid=pvalid and convergence<=mp.mpf('1e-30');maxconvergence=max(maxconvergence,convergence)
            previous_stages=stages;valid=valid and pvalid;recovered=recovered and stage_cov<=mp.mpf('1e-35')
            controls['precisions'].append({'precision_digits':dps,'laws':data['controls'],'witnesses':wc,'readout_controls':sc,'binary_state_roundtrip_exact':bool(roundtrip),'density_basis_reconstruction':ns(reconstruction),'density_coefficient_imaginary_residual':ns(imag),'hidden_null_residual':ns(null),'global_stage_covariance':ns(stage_cov),'stage_residuals':{k:ns(v) for k,v in stage_res.items()},'global_stage_precision_convergence':ns(convergence),'valid':bool(pvalid)})
    with mp.workdps(80):
        for c in cases:
            convergence=mp.mpf(0);converged=True
            for name in ['native','transformed']:
                lo=c['precision_results']['50'][name];hi=c['precision_results']['80'][name]
                if 'error' in lo or 'error' in hi:converged=False;continue
                convergence=max(convergence,input_distance(decode_inputs(lo['inputs']),decode_inputs(hi['inputs'])))
                for key in ['K','J']:
                    convergence=max(convergence,norm(V100.decoded(lo['response'][key])-V100.decoded(hi['response'][key])));converged=converged and lo['response'][key+'_ranks']==hi['response'][key+'_ranks']
            converged=converged and convergence<=mp.mpf('1e-30');valid=valid and converged;maxconvergence=max(maxconvergence,convergence)
            c['precision_convergence']=ns(convergence);c['precision_converged']=bool(converged);c['recovered']=all(m.get('recovered',False) for m in c['precision_metrics']);c['all_valid']=bool(converged and all(m.get('valid',False) for m in c['precision_metrics']))
        controls['maximum_precision_convergence']=ns(maxconvergence)
    valid=bool(valid and len(cases)==8);return {'version':'16.01','all_valid':valid,'verdict':adjudicate(valid,recovered),'recovery_predicate':bool(recovered),'precision_digits':PRECISIONS,'controls':controls,'cases':cases,
        'scope':'Eight end-to-end global precision comparisons, not full v15.99 recertification or upstream operation isolation. Historical v15.99 INVALID and v16.00 negative verdict preserved.'}


if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
