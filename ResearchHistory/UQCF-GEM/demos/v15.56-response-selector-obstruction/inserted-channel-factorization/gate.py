"""v16.04 independent weight-block commutator/connected-direction audit."""
import argparse,gzip,hashlib,importlib.util,itertools,json,pathlib,subprocess,sys,traceback
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('finite1603_factor',HERE.parent/'finite-source-continuation/gate.py')
F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
G=F.G;R=F.R;E=F.E
CANDIDATES=[13,16,22,25,27,29,37,39,46,50,66,77]
AS=[1.,1/3,1/6];ARMS=['plane','isotropic'];PRECISIONS=[50,80]
PARENT_HEAD='850dc3538f04ce9efcb3e974fa04992bcb1cb150'

def verify_files(root,manifest):
    try:return bool(manifest) and all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
    except OSError:return False

def verdict(valid,confirmed):
    return 'INVALID' if not valid else ('FACTORIZATION_CONFIRMED' if confirmed else 'FACTORIZATION_NOT_CONFIRMED')

def lift(t,sites):
    """Explicit global index replacement, independent of G.groups/apply."""
    out=[]
    for j,w in enumerate(G.LABELS):
        col=4*w[sites[0]]+w[sites[1]]
        for a,b in itertools.product(range(4),repeat=2):
            c=t[4*a+b,col]
            if c!=0:
                ww=list(w);ww[sites[0]]=a;ww[sites[1]]=b
                out.append((G.INDEX[tuple(ww)],j,c))
    return out

def apply_entries(entries,x):
    y=mp.zeros(x.rows,x.cols)
    for i,j,c in entries:
        for k in range(x.cols):y[i,k]+=c*x[j,k]
    F.finite_matrix(y);return y

def weight_action(entries,x,a,weights=None):
    weights=G.WEIGHT if weights is None else weights
    y=mp.zeros(x.rows,x.cols);blocks={};opnorm={}
    for i,j,c in entries:
        u,v=weights[j],weights[i];key=(u,v);z=(a**u-a**v)*c
        if key not in blocks:blocks[key]=mp.zeros(x.rows,x.cols);opnorm[key]=mp.mpf(0)
        opnorm[key]+=abs(z)**2
        for k in range(x.cols):
            val=z*x[j,k];y[i,k]+=val;blocks[key][i,k]+=val
    F.finite_matrix(y)
    return y,{f'{u}->{v}':{'operator_norm':R.ns(mp.sqrt(opnorm[u,v])),'state_action_norm':R.ns(F.norm(b))} for (u,v),b in sorted(blocks.items())}

def connected(z,x):
    """Independent coefficient indexing, with both one-body product terms."""
    def moment(vec,items):
        w=[0]*4
        for site,axis in items:w[site]=axis
        return 4*vec[G.INDEX[tuple(w)],0]
    out=[]
    for i,j in G.V96.EDGES:
        d=mp.zeros(3)
        for a,b in itertools.product(range(1,4),repeat=2):
            d[a-1,b-1]=moment(x,[(i,a),(j,b)])-moment(x,[(i,a)])*moment(z,[(j,b)])-moment(z,[(i,a)])*moment(x,[(j,b)])
        F.finite_matrix(d);out.append(d)
    return out

def contract(cs,sc,bs,v,arm):return F.response(cs,sc,bs,arm,v)

def affine_contrast(cs,sc,bf,br,arm):
    jf,_,_=F.response(cs,sc,bf,arm);jr,_,_=F.response(cs,sc,br,arm)
    return jf-jr

def listnorm(xs):return mp.sqrt(mp.fsum(F.norm(x)**2 for x in xs))
def difference(xs,ys):return listnorm([x-y for x,y in zip(xs,ys)])

def load_parent(candidate):
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    if not verify_files(HERE.parent,manifest):raise ValueError('parent provenance mismatch')
    parent=json.loads(gzip.decompress((HERE.parent/f'finite-source-continuation/result-{candidate}.json.gz').read_bytes()))
    expected={(av,pair,arm,dps) for av in AS for pair in ['disjoint','overlap'] for arm in ARMS for dps in PRECISIONS}
    keys=[(r['a'],r['pair'],r['arm'],r['precision']) for r in parent['rows']]
    if not(parent['version']=='16.03' and parent['all_valid'] is True and parent['execution_head']==PARENT_HEAD and parent['candidate_index']==candidate and len(keys)==len(expected) and set(keys)==expected):raise ValueError('parent structure or identity invalid')
    return {(r['a'],r['arm'],r['precision']):r for r in parent['rows'] if r['pair']=='disjoint'}

def measurement(candidate):
    parents=load_parent(candidate);pinned,states,_=F.pinned()
    if not pinned:raise ValueError('inherited provenance invalid')
    state=states[candidate];rows=[];controls=[];previous={};valid=True;confirmed=True
    for dps in PRECISIONS:
      with mp.workdps(dps):
        data=E.laws(dps)
        metrics={k:mp.mpf(0) for k in ['lift','commutator','connected','global_covariance','response_covariance','precision','hidden_null','hidden_pair_equality','affine_null','identity_middle_null','weight_preserving_null','hessian_identity','parent_coefficient','direct_coefficient','sum_coefficient','retained_covariance']}
        ranks_ok=True
        def mx(k,x):
            if not mp.isfinite(x):raise ValueError('nonfinite residual '+k)
            metrics[k]=max(metrics[k],x)
        def stage(key,arr,global_vector=True):
            for x in arr:F.finite_matrix(x)
            mx('global_covariance' if global_vector else 'response_covariance',F.norm(arr[1]-(G.product_action(data['frames'],arr[0]) if global_vector else arr[0])))
            if dps==50:previous[key]=[x.copy() for x in arr]
            else:mx('precision',max(F.norm(x-y) for x,y in zip(arr,previous.pop(key))))
            return arr
        def response_stage(key,arr):
            nonlocal ranks_ok
            old=previous.get(key) if dps==80 else None
            ok,_=F.agreement(arr,old,classification=True);ranks_ok=ranks_ok and ok
            return stage(key,arr,False)
        rho=mp.matrix([[mp.mpc(R.exact_float(float.fromhex(v[0])),R.exact_float(float.fromhex(v[1]))) for v in row] for row in state['state_hex']])
        cv,imag=G.coefficients(rho);mx('lift',imag)
        sv=stage('state',[cv,G.product_action(data['frames'],cv)])
        h=mp.zeros(256,81)
        for k,w in enumerate(F.V98.H_LABELS):h[G.INDEX[w],k]=1
        hs=stage('hidden',[h,G.product_action(data['frames'],h)])
        entries=[{key:lift(data['source'][f][key],F.V98.SITES[key]) for key in ['A','D']} for f in [0,1]]
        def act(key,v,f):return G.apply(data['source'][f][key],F.V98.SITES[key],v)
        for f in [0,1]:
            for key in ['A','D']:
                for x in [sv[f],hs[f]]:mx('lift',F.norm(apply_entries(entries[f][key],x)-act(key,x,f)))
        first={key:stage(('first',key),[act(key,hs[f],f) for f in [0,1]]) for key in ['A','D']}
        for av in AS:
          a=R.exact_float(av);base=stage(('base',av),[G.middle(v,a) for v in sv]);ks={};blocks={}
          for key in ['A','D']:
            pairs=[weight_action(entries[f][key],sv[f],a) for f in [0,1]]
            ks[key]=stage(('commutator',av,key),[x[0] for x in pairs]);blocks[key]=[x[1] for x in pairs]
            for f in [0,1]:
                direct=act(key,base[f],f)-G.middle(act(key,sv[f],f),a);mx('commutator',F.norm(ks[key][f]-direct))
                for w,b in blocks[key][f].items():
                    if w.split('->')[0]==w.split('->')[1]:mx('weight_preserving_null',mp.mpf(b['operator_norm']))
                if av==1.:mx('identity_middle_null',F.norm(ks[key][f]))
          ys={}
          for order,one,two in [('forward','A','D'),('reverse','D','A')]:
            cut=stage(('cut',av,order),[G.middle(first[one][f],a) for f in [0,1]])
            ys[order]=stage(('second',av,order),[act(two,cut[f],f) for f in [0,1]])
            for f in [0,1]:
                for z in [hs[f],G.middle(hs[f],a),first[one][f],cut[f],act(two,G.middle(hs[f],a),f)]:mx('hidden_null',G.restrict_norm(z,2))
                mx('hidden_null',G.restrict_norm(ys[order][f],1))
          for arm in ARMS:
            prep=lambda x,f:G.product_action(data['preparation'][arm][f],x)
            centers=stage(('center',av,arm),[prep(base[f],f) for f in [0,1]])
            py={o:stage(('prepared_hidden',av,arm,o),[prep(ys[o][f],f) for f in [0,1]]) for o in ys}
            b={o:[[G.pair_moments(py[o][f],k) for k in range(81)] for f in [0,1]] for o in ys}
            pk={key:stage(('prepared_commutator',av,arm,key),[prep(ks[key][f],f) for f in [0,1]]) for key in ['A','D']}
            dv={key:[connected(centers[f],pk[key][f]) for f in [0,1]] for key in ['A','D']}
            gs,_=R.exact_frames()
            for key in ['A','D']:
                mx('retained_covariance',difference(dv[key][1],[gs[i]*v*gs[j].T for v,(i,j) in zip(dv[key][0],G.V96.EDGES)]))
                skey=('retained_direction',av,arm,key)
                if dps==50:previous[skey]=[[v.copy() for v in arr] for arr in dv[key]]
                else:
                    old=previous.pop(skey)
                    mx('precision',max(difference(x,y) for x,y in zip(dv[key],old)))
            for o in ys:
                for f in [0,1]:mx('hidden_null',G.restrict_norm(py[o][f],1))
            td=[];ta=[];tot=[];records=[]
            for f in [0,1]:
                cs=G.correlations(centers[f]);sc=G.correlations(base[f])
                mx('hidden_pair_equality',listnorm([x-y for xx,yy in zip(b['forward'][f],b['reverse'][f]) for x,y in zip(xx,yy)]))
                mx('affine_null',F.norm(affine_contrast(cs,sc,b['forward'][f],b['reverse'][f],arm)))
                directions={};contributions={};direction_norms={}
                for key in ['A','D']:
                    prepared=pk[key][f];v=dv[key][f]
                    mx('connected',difference(v,G.retained(centers[f],centers[f],prepared)['ds'][0]))
                    _,t,res=contract(cs,sc,b['forward'][f],v,arm);mx('hessian_identity',res)
                    contributions[key]=t;directions[key]=v
                    direction_norms[key]={'global':R.ns(F.norm(ks[key][f])),'prepared':R.ns(F.norm(prepared)),'connected':R.ns(listnorm(v))}
                t=contributions['D']-contributions['A'];F.finite_matrix(t)
                _,ts,res=contract(cs,sc,b['forward'][f],[x-y for x,y in zip(directions['D'],directions['A'])],arm)
                mx('sum_coefficient',F.norm(t-ts));mx('hessian_identity',res)
                direct=act('D',base[f],f)+G.middle(act('A',sv[f],f),a)-act('A',base[f],f)-G.middle(act('D',sv[f],f),a)
                vdirect=F.centered_derivative(centers[f],prep(direct,f))
                _,tcheck,res=contract(cs,sc,b['forward'][f],vdirect,arm)
                mx('direct_coefficient',F.norm(t-tcheck));mx('hessian_identity',res)
                old=R.decoded(parents[av,arm,dps]['cubic'][f]['matrix']);mx('parent_coefficient',F.norm(t-old))
                ranks_ok=ranks_ok and R.ranks_from(R.spectrum(t))==parents[av,arm,dps]['cubic'][f]['ranks'] and F.classify(t)==parents[av,arm,dps]['classification'][f]
                if av==1.:mx('identity_middle_null',F.norm(t))
                denom=F.norm(contributions['D'])+F.norm(contributions['A'])
                records.append({'frame':f,'T_D':F.record(contributions['D']),'T_A':F.record(contributions['A']),'T':F.record(t),'classifications':{k:F.classify(x) for k,x in [('T_D',contributions['D']),('T_A',contributions['A']),('T',t)]},'direction_norms':direction_norms,'cancellation_ratio':None if denom==0 else R.ns(F.norm(t)/denom),'edges':F.diagnostics(cs,sc,arm)})
                td.append(contributions['D']);ta.append(contributions['A']);tot.append(t)
            for key,arr in [('T_D',td),('T_A',ta),('T',tot)]:response_stage((av,arm,key),arr)
            rows.append({'candidate_index':candidate,'a':av,'arm':arm,'precision':dps,'frames':records,'blocks':blocks})
            print(f'candidate={candidate} precision={dps} a={av} arm={arm} complete',flush=True)
        limits={k:mp.mpf('1e-35') for k in metrics};limits['precision']=mp.mpf('1e-30')
        pv=bool(ranks_ok and all(v<=limits[k] for k,v in metrics.items()) and data['controls']['valid'] and data['isotropic_controls']['valid'])
        valid=valid and pv;confirmed=confirmed and metrics['parent_coefficient']<=limits['parent_coefficient'] and metrics['direct_coefficient']<=limits['direct_coefficient']
        controls.append({'precision':dps,'all_valid':pv,'ranks_and_classes_agree':bool(ranks_ok),'metrics':{k:R.ns(x) for k,x in metrics.items()},'limits':{k:R.ns(x) for k,x in limits.items()},'laws':data['controls'],'isotropic_laws':data['isotropic_controls']})
    valid=bool(valid and not previous and len(rows)==12)
    return {'version':'16.04','candidate_index':candidate,'all_valid':valid,'verdict':verdict(valid,confirmed),'factorization_confirmed':bool(confirmed),'parent_execution_head':PARENT_HEAD,'parent_gzip_sha256':hashlib.sha256((HERE.parent/f'finite-source-continuation/result-{candidate}.json.gz').read_bytes()).hexdigest(),'rows':rows,'controls':controls,'scope':'Specified commutator/connected-direction audit using inherited polar Hessian; no universal source law or gravity claim.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=int,choices=CANDIDATES,required=True);args=ap.parse_args()
    try:result=measurement(args.candidate)
    except Exception as exc:
        traceback.print_exc();result={'version':'16.04','candidate_index':args.candidate,'all_valid':False,'verdict':'INVALID','error':str(exc)}
    result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
    out=HERE/f'result-{args.candidate}.json.gz';out.write_bytes(gzip.compress((json.dumps(result,indent=2,allow_nan=False)+'\n').encode(),mtime=0))
    files=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py',out.name]
    (HERE/f'SHA256SUMS-{args.candidate}').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in files))
    print(json.dumps({k:result[k] for k in ['version','candidate_index','all_valid','verdict','execution_head']}));sys.exit(0 if result['all_valid'] else 2)
