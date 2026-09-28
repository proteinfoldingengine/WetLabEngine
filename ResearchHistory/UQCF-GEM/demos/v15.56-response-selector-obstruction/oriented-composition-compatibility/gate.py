"""v15.94: completion multiplicativity versus intermediate support compatibility."""
import functools
import gzip
import hashlib
import importlib.util
import json
import pathlib
import sys
import numpy as np
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('oriented93_composition',HERE.parent/'oriented-rank-two-response'/'gate.py')
V93=importlib.util.module_from_spec(spec);spec.loader.exec_module(V93)
THRESHOLDS=[1e-9,1e-10,1e-11];TOL=1e-9
CODE_HASH='e12b740453761330add8f8d9694befa242e6b5c24bc9c6b49870d648b5c8725c'
GZIP_HASH='4c3e4d893c69f1a72a5409f905a1eafa81d4a0295b10439a0643ed21ba1dcc09'
JSON_HASH='540f46f32bf8f74ad2c4283870d14f36427b16d0155444546e7113cedd26cd2a'
LOOP_HASH='bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166'


def rank_info(x):
    sv=np.linalg.svd(x,compute_uv=False)
    return sv,[int(np.count_nonzero(sv>t)) for t in THRESHOLDS]


def complete(x):
    sv,ranks=rank_info(x)
    if ranks!=[2]*3:raise ValueError('proper completion requires frozen rank-two domain')
    u,s,vh=np.linalg.svd(x);v=u[:,:2]@vh[:2,:]
    return v+V93.cofactor(v)


def completion_residual(x,r):
    u,s,vh=np.linalg.svd(x);v=u[:,:2]@vh[:2,:];p=r.T@x
    return float(max(np.linalg.norm(r.T@r-np.eye(3)),abs(np.linalg.det(r)-1),np.linalg.norm(r@(v.T@v)-v),np.linalg.norm(p-p.T),max(0.,-np.linalg.eigvalsh((p+p.T)/2).min()),np.linalg.norm(r@p-x)))


def pair_diagnostic(a,b):
    product=a@b;sa,ra=rank_info(a);sb,rb=rank_info(b);s,ranks=rank_info(product)
    pa=a.T@a;qb=b@b.T;raw=float(np.trace((np.eye(3)-pa)@(np.eye(3)-qb)));bounded=float(np.clip(raw,0.,1.));c=float(np.sqrt(bounded))
    factor_error=float(max(np.linalg.norm(pa@pa-pa),np.linalg.norm((b.T@b)@(b.T@b)-b.T@b)))
    gap=float(np.linalg.norm(pa-qb));errors={'factor':factor_error,'spectrum':None,'projector_gap_formula':abs(gap*gap-2*(1-c*c)),'completion':0.,'discrepancy_formula':None}
    factor_valid=ra==[2]*3 and rb==[2]*3 and factor_error<=TOL
    row={'A':a.tolist(),'B':b.tolist(),'factor_ranks':[ra,rb],'factor_singular_values':[sa.tolist(),sb.tolist()],'raw_product':product.tolist(),'product_singular_values':s.tolist(),'product_ranks':ranks,
         'initial_A':pa.tolist(),'final_B':qb.tolist(),'normal_overlap_squared_raw':raw,'normal_overlap_squared_bounded':bounded,'c':c,'projector_gap':gap,
         'product_partial_isometry_defect':float(np.linalg.norm((product.T@product)@(product.T@product)-product.T@product)),
         'completion_product':None,'product_of_completions':None,'factor_completions':None,'discrepancy':None,'discrepancy_squared':None,'predicted_discrepancy_squared':None}
    if factor_valid:
        ar=complete(a);br=complete(b);row['factor_completions']=[ar.tolist(),br.tolist()]
        errors['completion']=max(completion_residual(a,ar),completion_residual(b,br))
        if ranks==[2]*3:
            errors['spectrum']=float(np.linalg.norm(s-np.array([1.,c,0.])))
            cr=complete(product);rr=ar@br;d=float(np.linalg.norm(cr-rr));pred=4*(1-c)
            errors['completion']=max(errors['completion'],completion_residual(product,cr));errors['discrepancy_formula']=abs(d*d-pred)
            row.update(completion_product=cr.tolist(),product_of_completions=rr.tolist(),discrepancy=d,discrepancy_squared=d*d,predicted_discrepancy_squared=pred)
    row['errors']=errors;row['valid']=bool(factor_valid and -1e-12<=raw<=1+1e-12 and all(v is None or v<=TOL for v in errors.values()))
    return row


@functools.lru_cache(maxsize=1)
def symbolic_certificate():
    zero=lambda a:all(sp.simplify(x)==0 for x in a);checks={}
    for k,g in enumerate(V93.exact_frames()):checks['frame_'+str(k)]=zero(g.T*g-sp.eye(3)) and g.det()==1
    t=sp.Symbol('t',real=True);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);u=sp.Matrix([[c,0,s],[0,1,0],[-s,0,c]])
    p=sp.diag(1,1,0);q=u*p*u.T;x=q*p;v=u*p
    checks['plane_projectors']=zero(p*p-p) and zero(q*q-q) and sp.simplify(sp.trace(q))==2
    checks['product_polar_factorization']=zero(x-u*sp.diag(c,1,0))
    checks['product_gram']=zero(x.T*x-sp.diag(c*c,1,0))
    checks['support_partial_isometry']=zero(v*v.T*v-v) and zero(v.T*v-p)
    checks['proper_completion']=zero(v+v.cofactor_matrix()-u)
    checks['completion_discrepancy']=sp.simplify(sp.trace((u-sp.eye(3)).T*(u-sp.eye(3)))-4*(1-c))==0
    checks['projector_gap']=sp.simplify(sp.trace((p-q).T*(p-q))-2*(1-c*c))==0
    checks['matched_boundary']=zero(x.subs(t,0)-p) and zero(u.subs(t,0)-sp.eye(3))
    boundary=x.subs(t,1);rotation=u.subs(t,1)
    checks['rank_one_ambiguity']=boundary.rank()==1 and zero(rotation*boundary-boundary) and zero(rotation.T*rotation-sp.eye(3)) and rotation.det()==1 and not zero(rotation-sp.eye(3))
    return {'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'valid':bool(all(checks.values()))}


def fixtures():
    p=np.diag([1.,1.,0.]);u=np.array([[.6,0,.8],[0,1,0],[-.8,0,.6]]);u0=np.array([[0.,0,1],[0,1,0],[-1,0,0]])
    rows=[]
    for name,a,expected_c,rank,expected_d2 in [('matched',p,1.,2,0.),('tilted',u@p@u.T,.6,2,1.6),('rank_one',u0@p@u0.T,0.,1,None)]:
        r=pair_diagnostic(a,p);ok=r['valid'] and r['product_ranks']==[rank]*3 and abs(r['c']-expected_c)<=TOL
        if expected_d2 is None:
            rejected=False
            try:complete(a@p)
            except ValueError:rejected=True
            ok=ok and rejected and r['completion_product'] is None and r['discrepancy'] is None
            r['completion_rejected']=rejected
        else:ok=ok and abs(r['discrepancy_squared']-expected_d2)<=TOL
        r.update(name=name,fixture_pass=bool(ok));rows.append(r)
    return rows


def pair_covariance(a,b,gi,gj,gk,base):
    transformed=pair_diagnostic(gi@a@gj.T,gj@b@gk.T)
    error=max(np.linalg.norm(np.array(transformed['raw_product'])-gi@(a@b)@gk.T),abs(transformed['normal_overlap_squared_raw']-base['normal_overlap_squared_raw']),abs(transformed['projector_gap']-base['projector_gap']))
    same=transformed['product_ranks']==base['product_ranks']
    if transformed['completion_product'] is not None and base['completion_product'] is not None:
        error=max(error,np.linalg.norm(np.array(transformed['completion_product'])-gi@np.array(base['completion_product'])@gk.T),np.linalg.norm(np.array(transformed['product_of_completions'])-gi@np.array(base['product_of_completions'])@gk.T),abs(transformed['discrepancy']-base['discrepancy']))
    return {'residual':float(error),'transformed_product_ranks':transformed['product_ranks'],'transformed_discrepancy':transformed['discrepancy'],'transformed_valid':transformed['valid'],'same_rank_domain':bool(same),'valid':bool(transformed['valid'] and error<=TOL)}


def adjudicate(valid,obstruction,matched):
    if not valid:return 'INVALID','INVALID'
    return ('ORIENTED_COMPOSITION_OBSTRUCTED' if obstruction else 'ORIENTED_COMPOSITION_OBSTRUCTION_NOT_CONFIRMED',
            'MATCHED_SUPPORT_COMPOSITION_CONFIRMED' if matched else 'MATCHED_SUPPORT_COMPOSITION_NOT_CONFIRMED')


@functools.lru_cache(maxsize=1)
def run_measurement():
    folder=HERE.parent/'oriented-rank-two-response';code=(folder/'gate.py').read_bytes();gz=(folder/'RESULT.json.gz').read_bytes();raw=gzip.decompress(gz);parent=json.loads(raw)
    rawloop=(HERE.parent/'support-loop-composition'/'RESULT.json').read_bytes();oldloop=json.loads(rawloop)
    pins=(hashlib.sha256(code).hexdigest()==CODE_HASH and hashlib.sha256(gz).hexdigest()==GZIP_HASH and hashlib.sha256(raw).hexdigest()==JSON_HASH and hashlib.sha256(rawloop).hexdigest()==LOOP_HASH)
    parent_valid=(parent['all_valid'] and parent['verdict']=='ORIENTED_RANK_TWO_READOUT_CONFIRMED' and parent['response_verdict']=='PLANAR_ORIENTED_RESPONSE_CONFIRMED' and oldloop['all_valid'] and oldloop['crossing_verdict']=='SUPPORT_RESTRICTED_CROSSING_CONFIRMED' and oldloop['composition_verdict']=='SUPPORT_LOOP_COMPOSITION_OBSTRUCTED' and oldloop['core_verdict']=='LOSSLESS_LOOP_CORE_TRIVIAL')
    expected=[13,16,22,25,27,29,37,39,46,50,66,77]
    indices=all([r['candidate_index'] for r in parent['rows'] if r['lambda']==lam]==expected for lam in [-1,0,1])
    frames=[np.array(x.tolist(),float) for x in V93.exact_frames()];controls={k:0. for k in ['factor','spectrum','projector_gap_formula','completion','discrepancy_formula','archived_R','archived_loop_square','associativity','covariance']}
    def mx(k,v):controls[k]=max(controls[k],float(v))
    def absorb(r):
        for k,v in r['errors'].items():
            if v is not None:mx(k,v)
    rows=[];matched=True;measurements_valid=True
    for old in parent['rows']:
        vs=[np.array(e['V']) for e in old['edges']];rs=[]
        for v,e in zip(vs,old['edges']):
            rr=complete(v);rs.append(rr);mx('archived_R',np.linalg.norm(rr-np.array(e['R'])))
        pair_rows=[]
        for e in range(3):
            i,j,k=e,(e+1)%3,(e+2)%3;a,b=vs[e],vs[(e+1)%3];r=pair_diagnostic(a,b);absorb(r)
            cv=pair_covariance(a,b,frames[i],frames[j],frames[k],r);mx('covariance',cv['residual']);r['covariance']=cv
            ok=r['product_ranks']==[2]*3 and cv['transformed_product_ranks']==[2]*3 and r['projector_gap']<=TOL and r['discrepancy'] is not None and r['discrepancy']<=TOL
            r['path']=[k,j,i];r['matched_pass']=bool(ok);matched=matched and ok;measurements_valid=measurements_valid and r['valid'] and cv['valid'];pair_rows.append(r)
        x=(vs[0]@vs[1])@vs[2];other=vs[0]@(vs[1]@vs[2]);sv,ranks=rank_info(x);assoc=float(np.linalg.norm(x-other));mx('associativity',assoc)
        triple={'raw_product':x.tolist(),'singular_values':sv.tolist(),'ranks':ranks,'associativity_residual':assoc,'completion':None,'product_of_completions':None,'discrepancy':None,'covariance_residual':None}
        ok=False
        if ranks==[2]*3:
            rx=complete(x);rr=rs[0]@rs[1]@rs[2];d=float(np.linalg.norm(rx-rr));mx('completion',completion_residual(x,rx))
            g0,g1,g2=frames;trans=(g0@vs[0]@g1.T)@(g1@vs[1]@g2.T)@(g2@vs[2]@g0.T)
            _,tranks=rank_info(trans);cv=float(np.linalg.norm(trans-g0@x@g0.T));tr=None
            if tranks==[2]*3:
                tr=complete(trans);cv=max(cv,float(np.linalg.norm(tr-g0@rx@g0.T)))
            mx('covariance',cv)
            triple.update(completion=rx.tolist(),product_of_completions=rr.tolist(),discrepancy=d,covariance_residual=float(cv),transformed_ranks=tranks,transformed_completion=None if tr is None else tr.tolist());ok=d<=TOL and tranks==[2]*3
        triple['matched_pass']=bool(ok);matched=matched and ok
        rows.append({'candidate_index':old['candidate_index'],'lambda':old['lambda'],'pairs':pair_rows,'triple':triple})
    loop=np.array(oldloop['loop'],float);native=pair_diagnostic(loop,loop);absorb(native)
    native['covariance']=pair_covariance(loop,loop,frames[0],frames[0],frames[0],native);mx('covariance',native['covariance']['residual'])
    mx('archived_loop_square',np.linalg.norm(loop@loop-np.array(oldloop['powers'][1]['matrix'],float)))
    measurements_valid=measurements_valid and native['valid'] and native['covariance']['valid']
    obstruction=native['product_ranks']==[2]*3 and native['covariance']['transformed_product_ranks']==[2]*3 and native['discrepancy'] is not None and native['discrepancy']>=1e-6
    syn=fixtures();symbolic=symbolic_certificate()
    valid=bool(pins and parent_valid and indices and len(rows)==36 and symbolic['valid'] and all(x['fixture_pass'] for x in syn) and measurements_valid and all(v<=TOL for v in controls.values()))
    controls.update(parent_hashes_valid=bool(pins),parent_verdicts_valid=bool(parent_valid),candidate_indices_valid=bool(indices),symbolic_certificate=symbolic,measurements_valid=bool(measurements_valid),fixtures_valid=bool(all(x['fixture_pass'] for x in syn)))
    verdict,mv=adjudicate(valid,obstruction,matched)
    result={'version':'15.94','all_valid':valid,'verdict':verdict,'matched_verdict':mv,'obstruction_predicate':bool(obstruction),'matched_predicate':bool(matched),'controls':controls,'fixtures':syn,'planar_rows':rows,'native':native,
            'scope':'Rank-two partial-isometry factors, raw retained-map composition at a fixed slice; oriented completion need not preserve incompatible composition. No source-update composition or quantum recovery claim.'}
    def finite(x):
        if isinstance(x,dict):return all(finite(v) for v in x.values())
        if isinstance(x,list):return all(finite(v) for v in x)
        if isinstance(x,(int,float)):return bool(np.isfinite(x))
        return True
    if not finite(result):result['all_valid']=False;result['verdict']=result['matched_verdict']='INVALID'
    return result

if __name__=='__main__':
    report=run_measurement();print(json.dumps(report,indent=2,allow_nan=False));sys.exit(0 if report['all_valid'] else 2)
