"""v16.03: finite physical centers and analytic mixed polar derivatives."""
import argparse
import functools
import gzip
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import mpmath as mp
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ensemble102_finite',HERE.parent/'full-ensemble-precision/gate.py')
E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
G=E.G;R=E.R;V98=E.V98;V96=E.V96
norm=E.norm;ns=E.ns
CANDIDATES=[13,16,22,25,27,29,37,39,46,50,66,77]
STEPS=[4,5,6,7,8];PRECISIONS=[50,80];AS=[1.,1/3,1/6]

def finite_matrix(a):
    if not all(mp.isfinite(x) for x in a):raise ValueError('nonfinite matrix')

def classify(a):
    finite_matrix(a)
    if norm(a)<=mp.mpf('1e-35'):return 'null'
    if R.spectrum(a)[0]>mp.mpf('1e-9'):return 'active'
    return 'unresolved'

def adjudicate(valid,classes,continuation):
    if not valid:return 'INVALID','INVALID'
    primary='DISJOINT_CUBIC_RESPONSE_DETECTED' if 'active' in classes else ('DISJOINT_CUBIC_NUMERICAL_NULL' if classes and all(c=='null' for c in classes) else 'DISJOINT_CUBIC_UNRESOLVED')
    return primary,'FINITE_GRID_OVERLAP_RESPONSE_CONFIRMED' if continuation else 'FINITE_GRID_OVERLAP_RESPONSE_NOT_CONFIRMED'

class DomainError(ValueError):
    """Only an explicit violation of the frozen spectral domain."""

def checked_edge(c,source,arm):
    finite_matrix(c);finite_matrix(source)
    try:return E.edge(c,source,arm)
    except ValueError as exc:
        if str(exc).startswith('outside frozen'):raise DomainError(str(exc)) from exc
        raise

def agreement(current,previous=None,classification=False):
    groups=[current]+([] if previous is None else [previous]);ok=True;error=mp.mpf(0)
    for group in groups:
        ok=ok and (group[0] is None)==(group[1] is None)
        if all(x is not None for x in group):
            for x in group:finite_matrix(x)
            ok=ok and R.ranks_from(R.spectrum(group[0]))==R.ranks_from(R.spectrum(group[1]))
            if classification:ok=ok and classify(group[0])==classify(group[1])
    if previous is not None:
        for x,y in zip(current,previous):
            ok=ok and (x is None)==(y is None)
            if x is not None and y is not None:
                error=max(error,norm(x-y));ok=ok and R.ranks_from(R.spectrum(x))==R.ranks_from(R.spectrum(y))
                if classification:ok=ok and classify(x)==classify(y)
    return bool(ok),error

def mat(v):return sum((v[k]*b for k,b in enumerate(R.skew_basis())),mp.zeros(3))
def trace(a):return R.tr(a)
def loop(rs):return [rs[0]*rs[1]*rs[2],rs[0]*rs[3]*rs[4]]
def loop_d(rs,ds):
    return [ds[i]*rs[j]*rs[k]+rs[i]*ds[j]*rs[k]+rs[i]*rs[j]*ds[k] for i,j,k in [(0,1,2),(0,3,4)]]
def loop_mixed(rs,bs,vs,ms):
    out=[]
    for inds in [(0,1,2),(0,3,4)]:
        total=mp.zeros(3)
        for x in range(3):
            items=[ms[e] if pos==x else rs[e] for pos,e in enumerate(inds)];total+=items[0]*items[1]*items[2]
            for y in range(3):
                if x==y:continue
                items=[bs[e] if pos==x else vs[e] if pos==y else rs[e] for pos,e in enumerate(inds)];total+=items[0]*items[1]*items[2]
        out.append(total)
    return out

def response(cs,sc,bs,arm,v=None):
    """J[B] and its center directional derivative. B is held fixed."""
    ed=[checked_edge(c,s,arm) for c,s in zip(cs[:5],sc[:5])];rs=[x[0] for x in ed];hs=loop(rs)
    inv=[x[2]**-1 for x in ed];res=max(x[3] for x in ed)
    vs=[];pvs=[];wvs=[]
    if v is not None:
        for e,(r,p,lin,_,_) in enumerate(ed):
            q=r.T*v[e]-v[e].T*r;w=mat(inv[e]*R.coords(q));pv=r.T*v[e]-w*p
            res=max(res,norm(p*w+w*p-q),norm(pv-pv.T));wvs.append(w);pvs.append(pv);vs.append(r*w)
        hv=loop_d(rs,vs)
    j=mp.zeros(3,len(bs));t=mp.zeros(3,len(bs)) if v is not None else None
    for k,bb in enumerate(bs):
        dr=[];mixed=[]
        for e,(r,p,lin,_,_) in enumerate(ed):
            b=bb[e];q=r.T*b-b.T*r;w=mat(inv[e]*R.coords(q));dr.append(r*w)
            res=max(res,norm(p*w+w*p-q))
            if v is not None:
                qv=-wvs[e]*r.T*b-b.T*r*wvs[e]-pvs[e]*w-w*pvs[e]
                dw=mat(inv[e]*R.coords(qv));mixed.append(r*(wvs[e]*w+dw))
                res=max(res,norm(p*dw+dw*p-qv))
        hb=loop_d(rs,dr)
        vals=[trace(hb[0]),trace(hb[1]),trace(hb[0]*hs[1]+hs[0]*hb[1])]
        for i,z in enumerate(vals):j[i,k]=z
        if v is not None:
            hm=loop_mixed(rs,dr,vs,mixed)
            vals=[trace(hm[0]),trace(hm[1]),trace(hm[0]*hs[1]+hb[0]*hv[1]+hv[0]*hb[1]+hs[0]*hm[1])]
            for i,z in enumerate(vals):t[i,k]=z
    finite_matrix(j)
    if t is not None:finite_matrix(t)
    return j,t,res

def record(a):
    finite_matrix(a);s=R.spectrum(a)
    return {'matrix':R.encoded(a),'singular_values':[ns(x) for x in s],'ranks':R.ranks_from(s),'norm':ns(norm(a))}

def diagnostics(cs,sc,arm):
    return [checked_edge(c,s,arm)[4] for c,s in zip(cs[:5],sc[:5])]

def centered_derivative(center,y):return G.retained(center,center,y)['ds'][0]

def physical(v):
    z=np.array(G.reconstruct(v).tolist(),complex)
    return E.V99.V75.density_diagnostics(z[None])

def pinned():
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    ok=all(hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
    raw=gzip.decompress((HERE/'PARENT_J.json.gz').read_bytes())
    ok=ok and hashlib.sha256(raw).hexdigest()=='bcc465fcc363106f77e2f856eeaa205721e164889c70d3f7b729f3e2cf4fe745'
    parent=json.loads(raw);ok=ok and parent['all_valid'] and parent['version']=='16.02'
    states=json.loads(gzip.decompress((HERE.parent/'overlap-holonomy-common-line/RESULT.json.gz').read_bytes()))['input_states']
    return ok,{r['candidate_index']:r for r in states},{(r['candidate_index'],r['a'],r['pair'],r['arm']):r for r in parent['rows']}

def measurement(candidate):
    pin,states,parent=pinned();state=states[candidate]
    z=np.array([[complex(float.fromhex(v[0]),float.fromhex(v[1])) for v in row] for row in state['state_hex']])
    phys=E.V99.V75.density_diagnostics(np.concatenate([z[None],z[None]+1e-4*V98.HIDDEN,z[None]-1e-4*V98.HIDDEN]))
    valid=bool(pin and phys['valid']);rows=[];prev={};classes=[];continuation=True
    controls={'pinned':bool(pin),'input_physicality':phys,'precisions':[]}
    for dps in PRECISIONS:
      with mp.workdps(dps):
        data=E.laws(dps);gs,_=R.exact_frames();metrics={k:mp.mpf(0) for k in ['global_covariance','stage_convergence','retained_covariance','response_covariance','response_convergence','derivative_identity','origin_parent','one_body_null','lower_pair_null','disjoint_B_null','a1_order_null','erasure','finite_hidden_identity','independent_hessian','hessian_symmetry']}
        rankok=True;domainok=True;physicalok=True;min_eig=1.;checks={arm:0 for arm in ['plane','isotropic']}
        def mx(k,v):metrics[k]=max(metrics[k],v)
        def stage(name,vs):
            for v in vs:finite_matrix(v)
            mx('global_covariance',norm(vs[1]-G.product_action(data['frames'],vs[0])))
            if dps==50:prev['stage',name]=vs
            else:
                old=prev.pop(('stage',name));mx('stage_convergence',max(norm(x-y) for x,y in zip(vs,old)))
            return vs
        def compare(name,arr):
            nonlocal rankok
            for a in arr:finite_matrix(a)
            mx('response_covariance',norm(arr[0]-arr[1]))
            old=None if dps==50 else prev.pop(('response',name),[None,None])
            agreed,err=agreement(arr,old,classification=(name[-1]=='T'))
            rankok=rankok and agreed;mx('response_convergence',err)
            if dps==50:prev['response',name]=arr
        rho=mp.matrix([[R.exact_complex(v) for v in row] for row in z]);cv,im=G.coefficients(rho)
        sv=stage('state',[cv,G.product_action(data['frames'],cv)])
        h=mp.zeros(256,81)
        for k,w in enumerate(V98.H_LABELS):h[G.INDEX[w],k]=1
        hs=stage('hidden',[h,G.product_action(data['frames'],h)])
        def act(key,v,f):return G.apply(data['source'][f][key],V98.SITES[key],v)
        firsts={key:stage('first-'+key,[act(key,hs[f],f) for f in [0,1]]) for key in V98.SITES}
        mx('lower_pair_null',max(G.restrict_norm(x,2) for vv in [hs]+list(firsts.values()) for x in vv))
        for av in AS:
          a=R.exact_float(av);base=stage(('base',av),[G.middle(v,a) for v in sv])
          sourcebase={key:stage(('sourcebase',av,key),[act(key,base[f],f) for f in [0,1]]) for key in V98.SITES}
          firststate={key:stage(('firststate',av,key),[G.middle(act(key,sv[f],f),a) for f in [0,1]]) for key in V98.SITES}
          for pair,keys in V98.PAIRS.items():
            outputs={};linear={};quadratic={}
            for order,(first,second) in zip(['forward','reverse'],[keys,keys[::-1]]):
                cut=stage(('cut',av,pair,order),[G.middle(firsts[first][f],a) for f in [0,1]])
                outputs[order]=stage(('double',av,pair,order),[act(second,cut[f],f) for f in [0,1]])
                mh=[G.middle(hs[f],a) for f in [0,1]]
                secondonly=[act(second,mh[f],f) for f in [0,1]]
                mx('finite_hidden_identity',max(G.restrict_norm(v,2) for vv in [mh,cut,secondonly] for v in vv))
                mx('finite_hidden_identity',max(G.restrict_norm(v,1) for v in outputs[order]))
                linear[order]=stage(('linear',av,pair,order),[firststate[first][f]+sourcebase[second][f] for f in [0,1]])
                quadratic[order]=stage(('quadratic',av,pair,order),[act(second,firststate[first][f],f) for f in [0,1]])
                mx('lower_pair_null',max(G.restrict_norm(x,2) for x in cut));mx('one_body_null',max(G.restrict_norm(x,1) for x in outputs[order]))
            for arm in ['plane','isotropic']:
                prep=lambda v,f:G.product_action(data['preparation'][arm][f],v)
                center=stage(('center',av,pair,arm),[prep(base[f],f) for f in [0,1]])
                ys={o:stage(('preparedhidden',av,pair,arm,o),[prep(outputs[o][f],f) for f in [0,1]]) for o in outputs}
                bs={o:[[G.pair_moments(ys[o][f],k) for k in range(81)] for f in [0,1]] for o in ys}
                lpre={o:[prep(linear[o][f],f) for f in [0,1]] for o in linear};qpre={o:[prep(quadratic[o][f],f) for f in [0,1]] for o in quadratic}
                c0=[G.correlations(v) for v in center];sc0=[G.correlations(v) for v in base]
                origin={};vs=[[x-y for x,y in zip(centered_derivative(center[f],lpre['forward'][f]),centered_derivative(center[f],lpre['reverse'][f]))] for f in [0,1]]
                row={'candidate_index':candidate,'a':av,'pair':pair,'arm':arm,'precision':dps,'origin':{},'finite':[]}
                for order in outputs:
                    arr=[]
                    for f in [0,1]:
                        j,_,err=response(c0[f],sc0[f],bs[order][f],arm);arr.append(j);mx('derivative_identity',err)
                    compare((av,pair,arm,order,'origin'),arr);origin[order]=arr
                    old=R.decoded(parent[candidate,av,pair,arm]['responses'][order])
                    mx('origin_parent',norm(arr[0]-old));row['origin'][order]=[record(v) for v in arr]
                oc=[origin['forward'][f]-origin['reverse'][f] for f in [0,1]]
                row['origin_contrast']=[record(v) for v in oc]
                if pair=='disjoint':
                    for f in [0,1]:mx('disjoint_B_null',max(norm(x-y) for xx,yy in zip(bs['forward'][f],bs['reverse'][f]) for x,y in zip(xx,yy)))
                    ts=[]
                    for f in [0,1]:
                        _,t,err=response(c0[f],sc0[f],bs['forward'][f],arm,vs[f]);ts.append(t);mx('derivative_identity',err)
                        # Mixed Hessian symmetry, on the strongest B column to avoid an empty control.
                        col=max(range(81),key=lambda k:sum(norm(x) for x in bs['forward'][f][k]))
                        _,tr,err=response(c0[f],sc0[f],[vs[f]],arm,bs['forward'][f][col]);mx('hessian_symmetry',norm(tr-t[:,col]));mx('derivative_identity',err)
                        delta=mp.mpf('1e-6')
                        try:
                            jp,_,ep=response([c+delta*v for c,v in zip(c0[f],vs[f])],sc0[f],bs['forward'][f],arm)
                            jm,_,em=response([c-delta*v for c,v in zip(c0[f],vs[f])],sc0[f],bs['forward'][f],arm)
                            err=norm((jp-jm)/(2*delta)-t)/max(mp.mpf(1),norm(t));mx('independent_hessian',err);checks[arm]+=1
                        except DomainError:row.setdefault('unavailable_hessian_stencils',[]).append(f)
                    compare((av,pair,arm,'T'),ts);row['cubic']=[record(v) for v in ts];row['classification']=[classify(v) for v in ts]
                    if av==1.:mx('a1_order_null',max(norm(v) for v in ts))
                    if av!=1. and dps==80:classes.append(row['classification'][0])
                for exponent in STEPS:
                    lam=mp.mpf(2)**(-exponent);finite={'lambda_exponent':exponent,'lambda':ns(lam),'orders':{}};arrays={}
                    for order in outputs:
                        fc=stage(('finitecenter',av,pair,arm,order,exponent),[base[f]+lam*linear[order][f]+lam**2*quadratic[order][f] for f in [0,1]])
                        pc=[center[f]+lam*lpre[order][f]+lam**2*qpre[order][f] for f in [0,1]]
                        for v in [fc[0],pc[0]]:
                            dg=physical(v);physicalok=physicalok and dg['valid'];min_eig=min(min_eig,dg['min_eigenvalue'])
                        inputs=[{'cs':G.correlations(pc[f]),'sc':G.correlations(fc[f]),'ds':bs[order][f]} for f in [0,1]]
                        mx('retained_covariance',G.input_distance(inputs[1],R.transport(inputs[0],gs)))
                        arr=[];recs=[];dom=[]
                        for f in [0,1]:
                            try:
                                j,_,err=response(inputs[f]['cs'],inputs[f]['sc'],bs[order][f],arm);mx('derivative_identity',err);arr.append(j);dom.append(True)
                                recs.append({'normalized_J':record(j),'physical_J':record(lam**2*j),'edges':diagnostics(inputs[f]['cs'],inputs[f]['sc'],arm),'correlations':[R.encoded(c) for c in inputs[f]['cs']]})
                            except DomainError as exc:
                                arr.append(None);dom.append(False);recs.append({'normalized_J':None,'domain_error':str(exc),'correlations':[R.encoded(c) for c in inputs[f]['cs']]})
                        domainok=domainok and dom[0]==dom[1]
                        key=(av,pair,arm,order,exponent)
                        if dps==50:prev['domain',key]=dom
                        else:domainok=domainok and prev.pop(('domain',key))==dom
                        if all(dom):compare(key,arr)
                        arrays[order]=arr;finite['orders'][order]=recs
                    if all(v is not None for arr in arrays.values() for v in arr):
                        dif=[arrays['forward'][f]-arrays['reverse'][f] for f in [0,1]];compare((av,pair,arm,'contrast',exponent),dif)
                        finite['normalized_contrast']=[record(v) for v in dif];finite['physical_contrast']=[record(lam**2*v) for v in dif]
                        if pair=='disjoint':
                            finite['cubic_normalized']=[record(v/lam) for v in dif];finite['remainder_norms']=[ns(norm(dif[f]/lam-ts[f])) for f in [0,1]]
                            if av==1.:mx('a1_order_null',max(norm(v) for v in dif))
                        else:
                            finite['remainder_norms']=[ns(norm(dif[f]-oc[f])) for f in [0,1]]
                            continuation=continuation and all(R.spectrum(v)[0]>mp.mpf('1e-9') for v in dif)
                    elif pair=='overlap':continuation=False
                    row['finite'].append(finite)
                rows.append(row)
                print(f'candidate={candidate} precision={dps} a={av} pair={pair} arm={arm} complete',flush=True)
        target=mp.zeros(256,1);target[0]=mp.mpf(1)/4
        mx('erasure',max(norm(G.middle(v,0)-target) for v in sv))
        mx('erasure',max(norm(G.middle(v,0)) for vv in firsts.values() for v in vv))
        limits={k:mp.mpf('1e-35') for k in metrics};limits.update(stage_convergence=mp.mpf('1e-30'),response_convergence=mp.mpf('1e-30'),origin_parent=mp.mpf('1e-30'),independent_hessian=mp.mpf('1e-5'),erasure=mp.mpf('1e-12'))
        mixture=[{'lambda':ns(mp.mpf(2)**(-e)),'weights':[ns(1-mp.mpf(2)**(-e)),ns(mp.mpf(2)**(-e))],'valid':bool(0<=mp.mpf(2)**(-e)<mp.mpf('0.5') and (1-mp.mpf(2)**(-e))+mp.mpf(2)**(-e)==1)} for e in STEPS]
        pv=bool(all(x['valid'] for x in mixture) and data['controls']['valid'] and data['isotropic_controls']['valid'] and rankok and domainok and physicalok and all(checks.values()) and all(mp.isfinite(v) and v<=limits[k] for k,v in metrics.items()))
        valid=valid and pv
        controls['precisions'].append({'precision':dps,'valid':pv,'metrics':{k:ns(v) for k,v in metrics.items()},'limits':{k:ns(v) for k,v in limits.items()},'rank_agreement':bool(rankok),'domain_agreement':bool(domainok),'physicality':bool(physicalok),'minimum_center_eigenvalue':min_eig,'independent_stencil_count':checks,'finite_mixture_weights':mixture,'source_preparation_controls':data['controls'],'isotropic_controls':data['isotropic_controls'],'laws_valid':bool(data['controls']['valid'] and data['isotropic_controls']['valid'])})
    verdict,cv=adjudicate(valid,classes,continuation)
    return {'version':'16.03','candidate_index':candidate,'all_valid':bool(valid),'verdict':verdict,'continuation_verdict':cv,'cubic_classes':classes,'finite_overlap_confirmed':bool(continuation),'rows':rows,'controls':controls,'erasure_response':None,'scope':'Specified finite source/preparation laws. Numerical cubic classification, no gravity or source-law selection.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=int,choices=CANDIDATES,required=True);args=ap.parse_args()
    result=measurement(args.candidate)
    result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
    raw=json.dumps(result,indent=2,allow_nan=False).encode()+b'\n';out=HERE/f'result-{args.candidate}.json.gz';out.write_bytes(gzip.compress(raw,mtime=0))
    files=['PREREGISTRATION.md','SOURCE_MANIFEST.json','test_gate.py','gate.py',out.name]
    (HERE/f'SHA256SUMS-{args.candidate}').write_text(''.join(hashlib.sha256((HERE/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in files))
    print(json.dumps({k:result[k] for k in ['version','candidate_index','all_valid','verdict','continuation_verdict']}));sys.exit(0 if result['all_valid'] else 2)
