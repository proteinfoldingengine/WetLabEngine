"""v16.00: frozen-input precision audit; preserves v15.99 INVALID."""
import functools
import gzip
import hashlib
import importlib.util
import json
import pathlib
import sys
import numpy as np
import mpmath as mp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('middle99_precision',HERE.parent/'intermediate-eb-retention'/'gate.py')
V99=importlib.util.module_from_spec(spec);spec.loader.exec_module(V99)
V98=V99.V98;V97=V99.V97;V96=V99.V96
CASES=[(66,a,'overlap',o) for a in [1.,1/3,1/6] for o in ['reverse','contrast']]+[(77,1/6,'disjoint',o) for o in ['forward','reverse']]
PRECISIONS=[50,80];THRESHOLDS=['1e-9','1e-10','1e-11']


def exact_float(x):
    n,d=float(x).as_integer_ratio();return mp.mpf(n)/d
def exact_complex(z):return mp.mpc(exact_float(z.real),exact_float(z.imag))
def matrix(a):return mp.matrix([[exact_float(x) for x in row] for row in a])
def norm(a):return mp.sqrt(mp.fsum(abs(x)**2 for x in a))
def tr(a):return mp.fsum(a[i,i] for i in range(a.rows))
def coords(w):return mp.matrix([w[2,1],w[0,2],w[1,0]])
def skew(w):return (w-w.T)/2
def ns(x):return mp.nstr(x,mp.mp.dps)
def encoded(a):return [[ns(a[i,j]) for j in range(a.cols)] for i in range(a.rows)]
def decoded(a):return mp.matrix([[mp.mpf(x) for x in row] for row in a])
def hex_array(a):
    if np.ndim(a)==0:return float(a).hex()
    return [hex_array(x) for x in a]
def mp_inputs(arrays):return {'cs':[matrix(c) for c in arrays['cs']], 'sc':[matrix(c) for c in arrays['sc']], 'ds':[[matrix(c) for c in dd] for dd in arrays['ds']]}


def cofactor(a):
    c=mp.zeros(3)
    for i in range(3):
        for j in range(3):
            rows=[k for k in range(3) if k!=i];cols=[k for k in range(3) if k!=j]
            c[i,j]=(-1)**(i+j)*(a[rows[0],cols[0]]*a[rows[1],cols[1]]-a[rows[0],cols[1]]*a[rows[1],cols[0]])
    return c


def skew_basis():
    out=[]
    for i,j in [(2,1),(0,2),(1,0)]:
        b=mp.zeros(3);b[i,j]=1;b[j,i]=-1;out.append(b)
    return out


def spectrum(a):
    # Tall transpose avoids an unnecessary wide-matrix SVD. Singular values unchanged.
    sv=mp.svd_r(a.T if a.rows<a.cols else a,compute_uv=False)
    return [sv[i] for i in range(len(sv))]
def ranks_from(sv):return [sum(x>mp.mpf(t) for x in sv) for t in THRESHOLDS]


def edge(c,source):
    u,s,v=mp.svd_r(c);ref=spectrum(source)[0]
    if not (ref>0 and s[1]>mp.mpf('1e-9')*ref and s[2]<=mp.mpf('1e-11')*ref):raise ValueError('outside frozen rank-two numerical domain')
    partial=u[:,:2]*v[:2,:];r=partial+cofactor(partial);rawp=r.T*c;p=(rawp+rawp.T)/2
    basis=skew_basis();lin=mp.matrix(3,3)
    for k,b in enumerate(basis):
        col=coords(p*b+b*p)
        for j in range(3):lin[j,k]=col[j]
    pv,_=mp.eigsy(p)
    # Signed minimum and discarded support are diagnostics, never repaired or clipped.
    discarded=c-u[:,:2]*mp.diag([s[0],s[1]])*v[:2,:]
    res=max(norm(r.T*r-mp.eye(3)),abs(mp.det(r)-1),norm(r*p-c),norm(p-p.T))
    info={'C_singular_values':[ns(x) for x in s],'source_reference':ns(ref),'signed_minimum_P_eigenvalue':ns(pv[0]),'discarded_support_norm':ns(norm(discarded)),'arithmetic_identity_residual':ns(res)}
    return r,p,lin,res,info


def solve_skew(r,p,lin,dc):
    q=r.T*dc-dc.T*r;wvec=mp.lu_solve(lin,coords(q));w=mp.zeros(3)
    for k,b in enumerate(skew_basis()):w+=wvec[k]*b
    res=max(norm(p*w+w*p-q),norm(w+w.T),norm(q+q.T))
    return w,res


def readout(inp):
    edges=[edge(c,sc) for c,sc in zip(inp['cs'][:5],inp['sc'][:5])];rs=[x[0] for x in edges]
    hs=[rs[0]*rs[1]*rs[2],rs[0]*rs[3]*rs[4]];K=mp.zeros(6,len(inp['ds']));J=mp.zeros(3,len(inp['ds']));res=max(x[3] for x in edges)
    for k,dd in enumerate(inp['ds']):
        dr=[]
        for (r,p,lin,_,_),dc in zip(edges,dd[:5]):
            w,err=solve_skew(r,p,lin,dc);dr.append(r*w);res=max(res,err)
        dh=[]
        for a,b,c in [(0,1,2),(0,3,4)]:dh.append(dr[a]*rs[b]*rs[c]+rs[a]*dr[b]*rs[c]+rs[a]*rs[b]*dr[c])
        for i in range(2):
            v=dh[i]*hs[i].T;res=max(res,norm(v+v.T));vec=coords(skew(v))
            for j in range(3):K[3*i+j,k]=vec[j]
        J[0,k]=tr(dh[0]);J[1,k]=tr(dh[1]);J[2,k]=tr(dh[0]*hs[1]+hs[0]*dh[1])
    ksv=spectrum(K);jsv=spectrum(J)
    record={'K':encoded(K),'J':encoded(J),'K_singular_values':[ns(x) for x in ksv],'J_singular_values':[ns(x) for x in jsv],
            'K_ranks':ranks_from(ksv),'J_ranks':ranks_from(jsv),'identity_residual':ns(res),'edges':[x[4] for x in edges]}
    record['finite']=all(bool(mp.isfinite(x)) for x in list(K)+list(J)+ksv+jsv+[res])
    return record,K,J


def exact_frames():
    gs=[]
    for w,x,y,z in V96.QUATS:
        n=w*w+x*x+y*y+z*z
        a=[[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)], [2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)], [2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]]
        gs.append(mp.matrix([[mp.mpf(v)/n for v in row] for row in a]))
    g6=mp.zeros(6)
    for i in range(3):
        for j in range(3):g6[i,j]=gs[0][i,j];g6[i+3,j+3]=gs[0][i,j]
    return gs,g6


def transport(inp,gs):
    action=lambda cs:[gs[i]*c*gs[j].T for c,(i,j) in zip(cs,V96.EDGES)]
    return {'cs':action(inp['cs']),'sc':action(inp['sc']),'ds':[action(dd) for dd in inp['ds']]}


@functools.lru_cache(maxsize=2)
def solver_controls(dps):
    with mp.workdps(dps):
        c=mp.diag([2,1,0]);r,p,lin,res,_=edge(c,c);responses=mp.zeros(3);err=res
        for k,b in enumerate(skew_basis()):
            w,e=solve_skew(r,p,lin,b*c);err=max(err,e,norm(w-b));v=coords(w)
            for j in range(3):responses[j,k]=v[j]
        null=mp.mpf(0)
        for i in range(3):
            for j in range(i,3):
                dc=mp.zeros(3);dc[i,j]=dc[j,i]=1;w,e=solve_skew(r,p,lin,dc);null=max(null,norm(w),e)
        rejected=False
        try:edge(mp.diag([1,0,0]),mp.diag([1,0,0]))
        except ValueError:rejected=True
        ranks=ranks_from(spectrum(responses));valid=err<=mp.mpf('1e-35') and null<=mp.mpf('1e-35') and ranks==[3,3,3] and rejected
        return {'precision_digits':dps,'positive_error':ns(err),'symmetric_null_error':ns(null),'positive_ranks':ranks,'rank_one_rejected':rejected,'valid':bool(valid)}


def float_inputs(rho,a,pair,order,bigU,rot_us,scale):
    base=V99.middle(rho[None],a)[0];sc=V97.correlations(base);center=V96.post(base[None],scale)[0];cs=V97.correlations(center)
    rotbase=V99.middle((bigU@rho@bigU.conj().T)[None],a)[0];rotsc=V97.correlations(rotbase)
    rotcenter=bigU@V96.post((bigU.conj().T@rotbase@bigU)[None],scale)[0]@bigU.conj().T;rotcs=V97.correlations(rotcenter)
    rot_h=bigU@V98.HIDDEN@bigU.conj().T;ys={};rys={};keys=V98.PAIRS[pair]
    for o,(first,second) in zip(['forward','reverse'],[keys,keys[::-1]]):
        ys[o]=V98.generator(V99.middle(V98.generator(V98.HIDDEN,first),a),second)
        rys[o]=V98.generator(V99.middle(V98.generator(rot_h,first,units=rot_us),a),second,units=rot_us)
    ys['contrast']=ys['forward']-ys['reverse'];rys['contrast']=rys['forward']-rys['reverse']
    ds=V98.connected_tangent(center,V96.post(ys[order],scale))
    td=bigU@V96.post(bigU.conj().T@rys[order]@bigU,scale)@bigU.conj().T
    rds=V98.connected_tangent(rotcenter,td)
    return {'cs':cs,'sc':sc,'ds':ds},{'cs':rotcs,'sc':rotsc,'ds':rds}


def adjudicate(valid,recovery):
    if not valid:return 'INVALID'
    return 'READOUT_ARITHMETIC_NOISE_CONFIRMED' if recovery else 'FROZEN_INPUT_RANK_RESIDUAL_PERSISTS'


@functools.lru_cache(maxsize=1)
def run_measurement():
    f=HERE.parent/'intermediate-eb-retention';code=(f/'gate.py').read_bytes();gz=(f/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    oldraw=gzip.decompress((HERE.parent/'overlap-holonomy-common-line'/'RESULT.json.gz').read_bytes());inputs=json.loads(oldraw)
    pinned=hashlib.sha256(code).hexdigest()=='ba44a36fbef8923baf0b2c274fadc1dcc6b65c4f6bff848ff6c8ce0f6d32a56c' and hashlib.sha256(gz).hexdigest()=='84865667bf0a1987d919450eddf41751feb27ace640c99815592ebb65122eac9' and hashlib.sha256(raw).hexdigest()=='8107f3f6ac83b08ba9ff9490d56518a10ca823f9bd92a290adf418cc79d9ebbb' and hashlib.sha256(oldraw).hexdigest()=='99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e'
    pinned=pinned and not parent['all_valid'] and parent['verdict']==parent['erasure_verdict']=='INVALID' and parent['scaling_predicate'] and parent['erasure_predicate']
    archived={(r['candidate_index'],r['a'],r['pair']):r for r in parent['rows'] if r['arm']=='plane'}
    _,frames=V96.exact_frames();bigU=V96.tensor([np.array(u.tolist(),complex) for g,u in frames]);rot_us={key:np.array([bigU@u@bigU.conj().T for u in us]) for key,us in V98.SOURCES.items()};scale=V96.arms()['plane']['scale']
    states={r['candidate_index']:np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in r['state_hex']]) for r in inputs['input_states'] if r['candidate_index'] in [66,77]}
    physical=V99.V75.density_diagnostics(np.array(list(states.values())));state_roundtrip=True;max_imaginary=max(float(np.max(np.abs(z.imag))) for z in states.values())
    with mp.workdps(80):
        for z in states.values():
            state_roundtrip=state_roundtrip and all(complex(exact_complex(v))==complex(v) for v in z.flat)
    controls={'pinned_parent':bool(pinned),'state_roundtrip_exact':bool(state_roundtrip),'maximum_state_imaginary_entry':max_imaginary,'physicality':physical,'solver_controls':[solver_controls(p) for p in PRECISIONS]}
    valid=bool(pinned and state_roundtrip and physical['valid'] and all(x['valid'] for x in controls['solver_controls']));recovery=True;cases=[]
    maxima={'float_reproduction':0.,'arithmetic_identity':0.,'exact_frame_covariance':0.,'precision_convergence':0.}
    for idx,a,pair,order in CASES:
        frozen_native,frozen_rotated=float_inputs(states[idx],a,pair,order,bigU,rot_us,scale);old=archived[idx,a,pair]
        live=[];float_domain=True
        for arrays in [frozen_native,frozen_rotated]:
            rr,geom=V98.response(arrays['cs'],arrays['sc'],arrays['ds'],'plane');live.append(rr);float_domain=float_domain and geom['domain']
        nr,trr=live;oldn=old['responses'][order];oldt=old['transformed_responses'][order]
        error=float('inf');rank_reproduced=False
        if float_domain:
            error=max(float(np.linalg.norm(np.array(nr[k])-oldn[k])) for k in ['K','J'])
            error=max(error,*[float(np.linalg.norm(np.array(trr[k])-oldt[k])) for k in ['K_singular_values','J_singular_values']])
            rank_reproduced=all(nr[k]==oldn[k] and trr[k]==oldt[k] for k in ['K_ranks','J_ranks'])
        # A failed reproduction remains INVALID; the archived cases are never replaced.
        reproduction=bool(float_domain and error<=1e-9 and rank_reproduced)
        if np.isfinite(error):maxima['float_reproduction']=max(maxima['float_reproduction'],error)
        valid=valid and reproduction
        saved={'native':{k:hex_array(v) for k,v in frozen_native.items()},'transformed':{k:hex_array(v) for k,v in frozen_rotated.items()}}
        encoded_input=json.dumps(saved,sort_keys=True,separators=(',',':')).encode();prec_records={};metrics=[];case_recovery=True;case_valid=True;roundtrip=True
        expected=1 if idx==66 else 2
        for dps in PRECISIONS:
            with mp.workdps(dps):
                for arrays in [frozen_native,frozen_rotated]:
                    roundtrip=roundtrip and all(float(exact_float(x))==float(x) for arr in arrays.values() for x in arr.flat)
                native=mp_inputs(frozen_native);rotated=mp_inputs(frozen_rotated);gs,g6=exact_frames();exact=transport(native,gs)
                input_difference={k:float(mp.sqrt(mp.fsum(norm(x-y)**2 for x,y in zip(rotated[k],exact[k])))) for k in ['cs','sc']}
                input_difference['ds']=float(mp.sqrt(mp.fsum(norm(x-y)**2 for xd,yd in zip(rotated['ds'],exact['ds']) for x,y in zip(xd,yd))))
                results={};matrices={};failed=None
                for name,inp in [('native',native),('frozen_transformed',rotated),('exact_frame_control',exact)]:
                    try:
                        rr,k,j=readout(inp);results[name]=rr;matrices[name]=(k,j)
                    except ValueError as exc:failed=str(exc);results[name]={'error':failed}
                prec_records[str(dps)]=results
                if failed is not None:
                    case_valid=False;case_recovery=False;metrics.append({'precision_digits':dps,'error':failed});continue
                nK,nJ=matrices['native'];fK,fJ=matrices['frozen_transformed'];eK,eJ=matrices['exact_frame_control']
                ec=max(norm(eK-g6*nK),norm(eJ-nJ));fc=max(norm(fK-g6*nK),norm(fJ-nJ));identity=max(mp.mpf(rr['identity_residual']) for rr in results.values())
                control_ranks=all(results[name][key]==[expected]*3 for name in ['native','exact_frame_control'] for key in ['K_ranks','J_ranks'])
                recovered=all(results[name][key]==[expected]*3 for name in ['native','frozen_transformed'] for key in ['K_ranks','J_ranks']) and fc<=mp.mpf('1e-9')
                arithmetic_valid=identity<=mp.mpf('1e-35') and ec<=mp.mpf('1e-35') and control_ranks and all(rr['finite'] for rr in results.values())
                case_valid=case_valid and arithmetic_valid;case_recovery=case_recovery and recovered
                maxima['arithmetic_identity']=max(maxima['arithmetic_identity'],float(identity));maxima['exact_frame_covariance']=max(maxima['exact_frame_covariance'],float(ec))
                metrics.append({'precision_digits':dps,'identity_residual':ns(identity),'exact_frame_covariance':ns(ec),'frozen_input_covariance':ns(fc),'input_transport_difference':input_difference,'exact_control_ranks_valid':bool(control_ranks),'recovered':bool(recovered),
                                'ranks':{name:{k:rr[k] for k in ['K_ranks','J_ranks']} for name,rr in results.items()},'spectra':{name:{k:rr[k] for k in ['K_singular_values','J_singular_values']} for name,rr in results.items()}})
        convergence=0.;converged=True
        with mp.workdps(80):
            for name in ['native','frozen_transformed','exact_frame_control']:
                lo=prec_records['50'][name];hi=prec_records['80'][name]
                if 'error' in lo or 'error' in hi:converged=False;continue
                for k in ['K','J']:
                    diff=norm(decoded(lo[k])-decoded(hi[k]));convergence=max(convergence,float(diff));converged=converged and diff<=mp.mpf('1e-30') and lo[k+'_ranks']==hi[k+'_ranks']
        maxima['precision_convergence']=max(maxima['precision_convergence'],convergence)
        case_valid=bool(case_valid and converged and roundtrip and reproduction);valid=valid and case_valid;recovery=recovery and case_recovery
        cases.append({'candidate_index':idx,'a':a,'pair':pair,'order':order,'expected_native_rank':expected,'float_reproduction_error':error if np.isfinite(error) else None,'float_ranks_reproduced':bool(rank_reproduced),'float_native_ranks':{k:nr[k] for k in ['K_ranks','J_ranks']} if nr else None,'float_transformed_ranks':{k:trr[k] for k in ['K_ranks','J_ranks']} if trr else None,
                      'retained_inputs_hex':saved,'retained_inputs_sha256':hashlib.sha256(encoded_input).hexdigest(),'input_roundtrip_exact':bool(roundtrip),'precision_results':prec_records,'precision_metrics':metrics,'precision_convergence':convergence,'precision_converged':bool(converged),'all_valid':case_valid,'recovered':bool(case_recovery)})
    valid=bool(valid and len(cases)==8);controls['maxima']=maxima;controls['valid_case_count']=sum(c['all_valid'] for c in cases)
    return {'version':'16.00','all_valid':valid,'verdict':adjudicate(valid,recovery),'recovery_predicate':bool(recovery),'precision_digits':PRECISIONS,'rank_thresholds':THRESHOLDS,'controls':controls,'cases':cases,
            'scope':'Eight v15.99 failures only. Frozen retained input audit and prescribed exact-frame control, not a global source recomputation. v15.99 remains INVALID.'}


if __name__=='__main__':
    r=run_measurement();print(json.dumps(r,indent=2,allow_nan=False));sys.exit(0 if r['all_valid'] else 2)
