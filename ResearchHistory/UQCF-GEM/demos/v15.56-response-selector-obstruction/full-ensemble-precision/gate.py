"""v16.02 full ensemble; all historical implementations remain byte-identical."""
from fractions import Fraction
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
s=importlib.util.spec_from_file_location('global101_ensemble',HERE.parent/'global-input-precision'/'gate.py')
G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
R=G.V100;V99=R.V99;V98=G.V98;V96=G.V96;V97=V99.V97
ns=R.ns
def norm(a):
    value=R.norm(a)
    return value if mp.isfinite(value) else mp.inf
PRECISIONS=[50,80];ORDERS=['forward','reverse','contrast'];AS=[1.,1/3,1/6,0.]


def edge(c,source,arm):
    if arm=='plane':return R.edge(c,source)
    u,s,v=mp.svd_r(c);ref=R.spectrum(source)[0];r=u*v
    if not(ref>0 and all(x>mp.mpf('1e-9')*ref for x in s) and mp.det(r)>0):
        raise ValueError('outside frozen proper full-rank domain')
    rawp=r.T*c;p=(rawp+rawp.T)/2;lin=mp.zeros(3)
    for k,b in enumerate(R.skew_basis()):
        col=R.coords(p*b+b*p)
        for j in range(3):lin[j,k]=col[j]
    ev,_=mp.eigsy(p)
    res=max(norm(r.T*r-mp.eye(3)),abs(mp.det(r)-1),norm(r*p-c),norm(p-p.T),max(mp.mpf(0),-ev[0]))
    return r,p,lin,res,{'C_singular_values':[ns(x) for x in s],'source_reference':ns(ref),'full_polar_determinant':ns(mp.det(r)),'signed_minimum_P_eigenvalue':ns(ev[0]),'arithmetic_identity_residual':ns(res)}


@functools.lru_cache(maxsize=2)
def laws(dps):
    with mp.workdps(dps):
        old=G.laws(dps);ps=G.paulis();iso=[[],[]];cert=[];weights=[mp.mpf(1)/2]+[mp.mpf(1)/6]*3
        for site,(w,x,y,z) in enumerate(V96.QUATS):
            u=(w*ps[0]-mp.j*(x*ps[1]+y*ps[2]+z*ps[3]))/mp.sqrt(w*w+x*x+y*y+z*z)
            for frame,ops in enumerate([ps,[u*p*u.H for p in ps]]):
                t,c=G.transfer(list(zip(weights,ops)),1);iso[frame].append(t);cert.append(c)
        err=max(mp.mpf(v) for c in cert for v in c.values())
        return {**old,'preparation':{'plane':old['preparation'],'isotropic':iso},'isotropic_controls':{'maximum_residual':ns(err),'weight_sum_residual':ns(abs(sum(weights)-1)),'valid':bool(err<=mp.mpf('1e-35') and sum([Fraction(1,2)]+[Fraction(1,6)]*3)==1 and abs(sum(weights)-1)<=mp.mpf('1e-35') and min(weights)>=0)}}


def readout(inp,arm):
    edges=[edge(c,sc,arm) for c,sc in zip(inp['cs'][:5],inp['sc'][:5])];rs=[x[0] for x in edges]
    hs=[rs[0]*rs[1]*rs[2],rs[0]*rs[3]*rs[4]];K=mp.zeros(6,len(inp['ds']));J=mp.zeros(3,len(inp['ds']));res=max(x[3] for x in edges)
    for k,dd in enumerate(inp['ds']):
        dr=[]
        for (r,p,lin,_,_),dc in zip(edges,dd[:5]):
            w,err=R.solve_skew(r,p,lin,dc);dr.append(r*w);res=max(res,err)
        dh=[]
        for a,b,c in [(0,1,2),(0,3,4)]:dh.append(dr[a]*rs[b]*rs[c]+rs[a]*dr[b]*rs[c]+rs[a]*rs[b]*dr[c])
        for i in range(2):
            v=dh[i]*hs[i].T;res=max(res,norm(v+v.T));vec=R.coords(R.skew(v))
            for j in range(3):K[3*i+j,k]=vec[j]
        J[0,k]=R.tr(dh[0]);J[1,k]=R.tr(dh[1]);J[2,k]=R.tr(dh[0]*hs[1]+hs[0]*dh[1])
    ksv=R.spectrum(K);jsv=R.spectrum(J)
    record={'K':R.encoded(K),'J':R.encoded(J),'K_singular_values':[ns(x) for x in ksv],'J_singular_values':[ns(x) for x in jsv],
            'K_ranks':R.ranks_from(ksv),'J_ranks':R.ranks_from(jsv),'identity_residual':ns(res),'edges':[x[4] for x in edges]}
    record['loops']=[R.encoded(h) for h in hs]
    record['polar_links']=[R.encoded(r) for r in rs]
    record['finite']=all(bool(mp.isfinite(x)) for x in list(K)+list(J)+ksv+jsv+[res])
    return record,K,J


def adjudicate(valid,scaling,erasure):
    if not valid:return 'INVALID','INVALID'
    return ('FULL_ENSEMBLE_EB_RESPONSE_SCALING_CONFIRMED' if scaling else 'FULL_ENSEMBLE_EB_RESPONSE_SCALING_NOT_CONFIRMED',
            'FULL_ENSEMBLE_ERASURE_POLAR_UNDEFINED_CONFIRMED' if erasure else 'FULL_ENSEMBLE_ERASURE_NOT_CONFIRMED')


def finite_probes(rho,a,pair,arm):
    """Independent float64 finite stencils retained at the original step sizes."""
    scale=V96.arms()[arm]['scale'];base=V99.middle(rho[None],a)[0]
    hidden=np.concatenate([rho[None]+V99.EPS*V98.HIDDEN,rho[None]-V99.EPS*V98.HIDDEN])
    factor=((1-np.exp(-2*V99.STRENGTH))/2)**2;out={}
    keys=V98.PAIRS[pair]
    for order,(first,second) in zip(ORDERS,[keys,keys[::-1]]):
        y=V98.generator(V99.middle(V98.generator(V98.HIDDEN,first),a),second)
        final=V96.post(V98.source(V99.middle(V98.source(hidden,first),a),second),scale)
        dc=(V97.correlations(final[:81])-V97.correlations(final[81:]))/(2*V99.EPS*factor)
        affine=np.concatenate([base[None]+V99.ETA*y,base[None]-V99.ETA*y]);prepared=V96.post(affine,scale)
        hs,iv,domains=V97.finite_loops(prepared,affine,arm)
        out[order]={'dc':dc,'dh':None if hs is None else (hs[:81]-hs[81:])/(2*V99.ETA),'J':None if iv is None else ((iv[:81]-iv[81:])/(2*V99.ETA)).T,'domain':bool(all(domains))}
    return out


def finite_errors(probe,inp,rr):
    ds=np.array([[np.array(dd.tolist(),float) for dd in d] for d in inp['ds']])
    errors={'finite_channel_error':V99.relative(probe['dc'],ds),'affine_K_error':None,'affine_J_error':None,'domain':probe['domain']}
    if probe['domain'] and rr is not None:
        hs=np.array(rr['loops'],float)
        kfd=np.array([np.concatenate([V99.V93.coords(V97.skew(h[i]@hs[i].T)) for i in range(2)]) for h in probe['dh']]).T
        errors['affine_K_error']=V99.relative(kfd,np.array(rr['K'],float))
        errors['affine_J_error']=V99.relative(probe['J'],np.array(rr['J'],float))
    errors['valid']=errors['finite_channel_error']<=1e-7 and all(errors[k] is None or errors[k]<=1e-5 for k in ['affine_K_error','affine_J_error'])
    return errors


def full_solver_controls():
    c=mp.diag([3,2,1]);r,p,lin,res,_=edge(c,c,'isotropic');err=res
    for b in R.skew_basis():
        w,e=R.solve_skew(r,p,lin,b*c);err=max(err,e,norm(w-b))
    rejected=False
    try:edge(mp.diag([3,2,-1]),c,'isotropic')
    except ValueError:rejected=True
    return {'maximum_error':ns(err),'improper_rejected':rejected,'valid':bool(err<=mp.mpf('1e-35') and rejected)}


def pinned_inputs():
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    ok=all(hashlib.sha256((HERE.parent/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    objs={}
    for name,digest in [('global-input-precision','8308d457346e42755697228c4877db2b28eeedb93f6f3c9a16d551aa4449b7ba'),('intermediate-eb-retention','8107f3f6ac83b08ba9ff9490d56518a10ca823f9bd92a290adf418cc79d9ebbb'),('overlap-holonomy-common-line','99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e')]:
        raw=gzip.decompress((HERE.parent/name/'RESULT.json.gz').read_bytes());ok=ok and hashlib.sha256(raw).hexdigest()==digest;objs[name]=json.loads(raw)
    ok=ok and objs['global-input-precision']['all_valid'] and objs['global-input-precision']['verdict']=='GLOBAL_INPUT_PRECISION_RECOVERY_CONFIRMED' and objs['intermediate-eb-retention']['verdict']=='INVALID'
    parent=json.loads(gzip.decompress((HERE.parent/'composed-four-body-response'/'RESULT.json.gz').read_bytes()))
    states={rec['candidate_index']:np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in rec['state_hex']]) for rec in objs['overlap-holonomy-common-line']['input_states']}
    return bool(ok),states,{(r['candidate_index'],r['pair'],r['arm']):r for r in parent['rows']}


def retained_distance(a,b):return G.input_distance(a,b)


@functools.lru_cache(maxsize=1)
def run_measurement():
    pinned,states,parentrows=pinned_inputs()
    print('Replaying unmodified v15.99 physical/finite controls',file=sys.stderr,flush=True)
    legacy=V99.run_measurement();legacyraw=json.dumps(legacy,indent=2,allow_nan=False).encode()
    (HERE/'legacy-result.json.gz').write_bytes(gzip.compress(legacyraw,mtime=0))
    lc=legacy['controls'];old_ok=bool(lc['parents_valid'] and lc['symbolic_certificate']['valid'] and all(c['valid'] for c in lc['inherited_certificates']+lc['intermediate_channels']+legacy['intermediate_centers']) and lc['physicality']['valid'] and lc['disjoint_retained_ranks_null'] and lc['minimum_source_weight']>=-1e-12 and all(lc[k]<=lim for k,lim in lc['limits'].items()) and len(legacy['rows'])==192 and len(legacy['intermediate_centers'])==108)
    rows=[{'candidate_index':idx,'a':a,'pair':pair,'arm':arm,'precision_results':{}} for idx in states for a in AS for pair in V98.PAIRS for arm in ['plane','isotropic']]
    controls={'pinned_sources':pinned,'legacy_nonrank_controls_valid':old_ok,'legacy_verdict':legacy['verdict'],'legacy_rank_covariance_valid':lc['rank_covariance_valid'],'legacy_result_sha256':hashlib.sha256(legacyraw).hexdigest(),'legacy_physicality':lc['physicality'],'precisions':[]}
    valid=pinned and old_ok and list(states)==[13,16,22,25,27,29,37,39,46,50,66,77];scaling=True;erasure=True
    previous_stages=None;previous_inputs={};fd_cache={}
    for dps in PRECISIONS:
        with mp.workdps(dps):
            data=laws(dps);gs,g6=R.exact_frames();stages={};stage_finite=True;stage_error=mp.mpf(0);null=mp.mpf(0);reconstruction=mp.mpf(0);roundtrip=True;convergence=mp.mpf(0)
            retained_cov=mp.mpf(0);response_cov=mp.mpf(0);identity=mp.mpf(0);response_convergence=mp.mpf(0);retained_convergence=mp.mpf(0);algebra=mp.mpf(0);rankcov=True;converged=True;baseline_error=mp.mpf(0);erase_error=mp.mpf(0)
            def stage(key,vs):
                nonlocal stage_error,convergence,stage_finite
                stages[key]=vs;stage_finite=stage_finite and all(mp.isfinite(x) for v in vs for x in v);stage_error=max(stage_error,norm(vs[1]-G.product_action(data['frames'],vs[0])))
                if previous_stages is not None:
                    convergence=max(convergence,*(norm(v-o) for v,o in zip(vs,previous_stages[key])))
                return vs
            h=mp.zeros(256,81)
            for k,w in enumerate(V98.H_LABELS):h[G.INDEX[w],k]=1
            hs=stage('probes',[h,G.product_action(data['frames'],h)])
            firsts={key:stage('first_'+key,[G.apply(data['source'][f][key],V98.SITES[key],hs[f]) for f in [0,1]]) for key in V98.SITES}
            null=max(G.restrict_norm(v,2) for vs in [hs]+list(firsts.values()) for v in vs)
            ys={};prepared={}
            for a0 in AS:
                a=R.exact_float(a0)
                for pair,keys in V98.PAIRS.items():
                    for order,(first,second) in zip(ORDERS,[keys,keys[::-1]]):
                        cut=stage(f'cut_{a0}_{first}',[G.middle(v,a) for v in firsts[first]])
                        out=stage(f'second_{a0}_{pair}_{order}',[G.apply(data['source'][f][second],V98.SITES[second],cut[f]) for f in [0,1]])
                        null=max(null,*(G.restrict_norm(v,2) for v in cut),*(G.restrict_norm(v,1) for v in out));ys[a0,pair,order]=out
                    ys[a0,pair,'contrast']=stage(f'contrast_{a0}_{pair}',[ys[a0,pair,'forward'][f]-ys[a0,pair,'reverse'][f] for f in [0,1]])
                    for arm in ['plane','isotropic']:
                        for order in ORDERS:
                            prepared[a0,pair,arm,order]=stage(f'prepared_{a0}_{pair}_{arm}_{order}',[G.product_action(data['preparation'][arm][f],ys[a0,pair,order][f]) for f in [0,1]])
            for idx,z in states.items():
                rho=mp.matrix([[R.exact_complex(v) for v in row] for row in z]);roundtrip=roundtrip and all(complex(rho[i,j])==complex(z[i,j]) for i in range(16) for j in range(16))
                cv,im=G.coefficients(rho);reconstruction=max(reconstruction,im,norm(G.reconstruct(cv)-rho))
                sv=stage(f'state_{idx}',[cv,G.product_action(data['frames'],cv)])
                bases={};centers={}
                for a0 in AS:
                    bases[a0]=stage(f'base_{idx}_{a0}',[G.middle(v,R.exact_float(a0)) for v in sv])
                    for arm in ['plane','isotropic']:centers[a0,arm]=stage(f'center_{idx}_{a0}_{arm}',[G.product_action(data['preparation'][arm][f],bases[a0][f]) for f in [0,1]])
                for row in [r for r in rows if r['candidate_index']==idx]:
                    a0=row['a'];a=R.exact_float(a0);pair=row['pair'];arm=row['arm'];key=(idx,a0,pair,arm);pr=parentrows[idx,pair,arm]
                    result={'responses':{},'finite_checks':{},'scaling':{},'all_domains':True};ins={}
                    if a0==0:
                        target=mp.zeros(256,1);target[0]=mp.mpf(1)/4
                        err=max(*(norm(v-target) for v in bases[0]+centers[0,arm]),*(norm(v) for order in ORDERS for v in prepared[0,pair,arm,order]))
                        erase_error=max(erase_error,err);passed=err<=mp.mpf('1e-12')
                        result={'responses':None,'polar_readout':'undefined','maximum_erasure_error':ns(err),'scientific_pass':bool(passed)}
                        erasure=erasure and passed;row['precision_results'][str(dps)]=result;continue
                    if key not in fd_cache:fd_cache[key]=finite_probes(z,a0,pair,arm)
                    for order in ORDERS:
                        inputs=[G.retained(bases[a0][f],centers[a0,arm][f],prepared[a0,pair,arm,order][f]) for f in [0,1]]
                        valid=valid and all(mp.isfinite(v) for inp in inputs for m in inp['cs']+inp['sc']+[m for dd in inp['ds'] for m in dd] for v in m)
                        retained_cov=max(retained_cov,retained_distance(inputs[1],R.transport(inputs[0],gs)))
                        ikey=key+(order,)
                        if dps==50:previous_inputs[ikey]=inputs
                        else:
                            retained_convergence=max(retained_convergence,*(retained_distance(x,y) for x,y in zip(inputs,previous_inputs.pop(ikey))))
                        ins[order]=inputs;rr={};mat={}
                        for f,name in enumerate(['native','transformed']):
                            try:
                                record,k,j=readout(inputs[f],arm);rr[name]=record;mat[name]=(k,j)
                                identity=max(identity,mp.mpf(record['identity_residual']));valid=valid and record['finite']
                            except ValueError as exc:
                                rr[name]=None;result['all_domains']=False;result.setdefault('domain_errors',[]).append(str(exc))
                        result['responses'][order]=rr
                        if all(r is not None for r in rr.values()):
                            k,j=mat['native'];kt,jt=mat['transformed'];response_cov=max(response_cov,norm(kt-g6*k),norm(jt-j))
                            rankcov=rankcov and all(rr['native'][k0]==rr['transformed'][k0] for k0 in ['K_ranks','J_ranks'])
                            sr={k0:ns(norm(m-a*R.matrix(pr['responses'][order][k0]))/max(mp.mpf(1),norm(a*R.matrix(pr['responses'][order][k0])))) for k0,m in [('K',k),('J',j)]}
                            sr['ranks_match']=all(rr['native'][k0]==pr['responses'][order][k0] for k0 in ['K_ranks','J_ranks']);result['scaling'][order]=sr
                            baseline_error=max(baseline_error,*(norm(R.decoded(x)-R.matrix(y)) for x,y in zip(rr['native']['loops'],pr['responses'][order]['loops'])),*(norm(R.decoded(x)-R.matrix(e['R'])) for x,e in zip(rr['native']['polar_links'],pr['baseline_edges'])))
                            if pair=='overlap':algebra=max(algebra,norm(k[:3,:]),norm(kt[:3,:]))
                            if pair=='disjoint' and order=='contrast':
                                algebra=max(algebra,norm(k),norm(j),norm(kt),norm(jt));rankcov=rankcov and all(rr[n][q]==[0,0,0] for n in rr for q in ['K_ranks','J_ranks'])
                        if order!='contrast':
                            checks=finite_errors(fd_cache[key][order],inputs[0],rr['native']);result['finite_checks'][order]=checks;valid=valid and checks['valid'];result['all_domains']=result['all_domains'] and checks['domain']
                    for name in ['native','transformed']:
                        records=[result['responses'][o][name] for o in ORDERS]
                        if all(r is not None for r in records):
                            for q in ['K','J']:algebra=max(algebra,norm(R.decoded(records[0][q])-R.decoded(records[1][q])-R.decoded(records[2][q])))
                    if dps==80:
                        low=row['precision_results']['50'];converged=converged and low['all_domains']==result['all_domains']
                        for order in ORDERS:
                            for name in ['native','transformed']:
                                lo=low['responses'][order][name];hi=result['responses'][order][name]
                                if lo is None or hi is None:converged=converged and (lo is None)==(hi is None);continue
                                for q in ['K','J']:
                                    response_convergence=max(response_convergence,norm(R.decoded(lo[q])-R.decoded(hi[q])));converged=converged and lo[q+'_ranks']==hi[q+'_ranks']
                    passed=result['all_domains'] and len(result['scaling'])==3 and all(s['ranks_match'] and mp.mpf(s['K'])<=mp.mpf('1e-9') and mp.mpf(s['J'])<=mp.mpf('1e-9') for s in result['scaling'].values())
                    result['scientific_pass']=bool(passed);scaling=scaling and passed;row['precision_results'][str(dps)]=result
                print(f'precision={dps} candidate={idx} completed',file=sys.stderr,flush=True)
            wc=G.witness_controls(dps);sc=R.solver_controls(dps);fc=full_solver_controls()
            pvalid=bool(stage_finite and data['controls']['valid'] and data['isotropic_controls']['valid'] and wc['valid'] and sc['valid'] and fc['valid'] and roundtrip and all(v<=mp.mpf('1e-35') for v in [stage_error,null,reconstruction,retained_cov,response_cov,identity]) and all(v<=mp.mpf('1e-30') for v in [convergence,retained_convergence,response_convergence]) and algebra<=mp.mpf('1e-9') and baseline_error<=mp.mpf('1e-9') and rankcov and converged)
            controls['precisions'].append({'precision_digits':dps,'valid':pvalid,'global_covariance':ns(stage_error),'retained_covariance':ns(retained_cov),'response_covariance':ns(response_cov),'null_residual':ns(null),'density_reconstruction':ns(reconstruction),'exact_binary_roundtrip':bool(roundtrip),'identity_residual':ns(identity),'global_convergence':ns(convergence),'retained_convergence':ns(retained_convergence),'response_convergence':ns(response_convergence),'rank_covariance':bool(rankcov),'precision_rank_domain_agreement':bool(converged),'algebra_residual':ns(algebra),'baseline_invariance':ns(baseline_error),'erasure_residual':ns(erase_error),'laws':data['controls'],'isotropic':data['isotropic_controls'],'witnesses':wc,'readout':sc,'full_rank_solver':fc})
            valid=valid and pvalid;previous_stages=stages
    erasure=erasure and legacy['erasure_predicate'];valid=bool(valid and len(rows)==192)
    verdict,ev=adjudicate(valid,scaling,erasure)
    report={'version':'16.02','all_valid':valid,'verdict':verdict,'erasure_verdict':ev,'scaling_predicate':bool(scaling),'erasure_predicate':bool(erasure),'candidate_indices':list(states),'precision_digits':PRECISIONS,'hidden_count':81,'controls':controls,'rows':rows,'scope':'Full frozen ensemble under specified source/preparation laws. Historical INVALID preserved. No physical law selection or gravity derivation.'}
    (HERE/'result.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report


if __name__=='__main__':
    r=run_measurement();print(json.dumps({k:r[k] for k in ['version','all_valid','verdict','erasure_verdict']},indent=2));sys.exit(0 if r['all_valid'] else 2)
