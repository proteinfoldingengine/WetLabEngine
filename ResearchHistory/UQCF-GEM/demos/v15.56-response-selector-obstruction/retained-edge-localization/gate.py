"""v16.05: exact and numerical localization before the five-edge Hessian."""
import argparse,gzip,hashlib,importlib.util,itertools,json,pathlib,subprocess,sys,traceback
import mpmath as mp
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('factor1604_localization',HERE.parent/'inserted-channel-factorization/gate.py')
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
F=A.F;G=A.G;R=A.R;E=A.E;V=F.V98
CANDIDATES=A.CANDIDATES;AS=A.AS;ARMS=A.ARMS;PRECISIONS=A.PRECISIONS
PARENT_HEAD='1b14035ab727b1f07a40c01498f91ad7fd0f3aac'
SYMBOL=sp.Symbol('a',real=True)

def exact_coefficients(rho):
    out={}
    for w in G.LABELS:
        value=sp.expand(sum((sp.Integer(int(phase.real))+sp.I*int(phase.imag))*rho[col,row] for col,(row,phase) in enumerate(G.monomial(w)))/4)
        if value!=0:out[w]=value
    return out

def exact_middle(d,a):return V.clean({w:a**sum(x!=0 for x in w)*c for w,c in d.items()})
def exact_commutator(d,key,a):return V.add(V.exact_action(exact_middle(d,a),key),exact_middle(V.exact_action(d,key),a),-1)
def exact_prepare(d,arm):
    scale=[sp.Integer(1),sp.Rational(1,2),sp.Rational(1,2),sp.Integer(0)] if arm=='plane' else [sp.Integer(1)]+[sp.Rational(1,3)]*3
    return V.clean({w:c*sp.prod(scale[x] for x in w) for w,c in d.items()})

def exact_connected(z,x):
    def moment(d,items):
        w=[0]*4
        for site,axis in items:w[site]=axis
        return 4*d.get(tuple(w),0)
    out=[]
    for i,j in G.V96.EDGES:
        out.append(sp.Matrix(3,3,lambda a,b:sp.expand(moment(x,[(i,a+1),(j,b+1)])-moment(x,[(i,a+1)])*moment(z,[(j,b+1)])-moment(z,[(i,a+1)])*moment(x,[(j,b+1)]))))
    return out

def exact_localization(v):
    zeros=[all(sp.expand(x)==0 for x in edge) for edge in v]
    return {'retained_zero':all(zeros[:5]),'omitted_zero':zeros[5],'edge_zero':zeros}

def edge_norms(v):
    if len(v)!=6:raise ValueError('six edges required')
    for x in v:F.finite_matrix(x)
    return {'edges':[F.norm(x) for x in v],'retained':A.listnorm(v[:5]),'omitted':F.norm(v[5]),'complete':A.listnorm(v)}

def localize(retained,response):
    if not(mp.isfinite(retained) and mp.isfinite(response)) or min(retained,response)<0:raise ValueError('invalid localization norms')
    if retained<=mp.mpf('1e-35'):
        if response<=mp.mpf('1e-35'):return 'RETAINED_EDGE_NULL'
        raise ValueError('retained-null/readout-response contradiction')
    if response>mp.mpf('1e-9'):return 'READOUT_RESPONSE'
    if retained>mp.mpf('1e-9') and response<=mp.mpf('1e-35'):return 'READOUT_ANNIHILATION'
    return 'UNRESOLVED'

def rational_hex(v):return sp.Rational(*float.fromhex(v).as_integer_ratio())
def numeric(x):
    x=sp.cancel(x)
    if not x.is_Rational:raise ValueError('expected exact real rational')
    return mp.mpf(int(x.p))/int(x.q)
def numeric_vector(d):return mp.matrix([numeric(d.get(w,sp.Integer(0))) for w in G.LABELS])
def evaluate(v,av):
    a=sp.Rational(*av.as_integer_ratio())
    return [mp.matrix([[numeric(m[i,j].subs(SYMBOL,a)) for j in range(3)] for i in range(3)]) for m in v]

def support_certificate():
    failed=[];count=0
    for w in G.LABELS:
        if w[2]!=0 and w[3]!=0:continue
        count+=1;k=exact_commutator({w:sp.Integer(1)},'D',SYMBOL)
        bad={v:c for v,c in k.items() if sum(x!=0 for x in v)<=1 or (sum(x!=0 for x in v)==2 and not(v[0]==v[1]==0))}
        if bad:failed.append({'input_word':list(w),'bad_outputs':[[list(v),str(c)] for v,c in bad.items()]})
    return {'basis_word_count':count,'confirmed':not failed,'failures':failed,'exact_transfer_reconstruction':V.exact_tables()[1]}

def load_inputs(candidate):
    manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
    if not A.verify_files(HERE.parent,manifest):raise ValueError('parent provenance mismatch')
    p=json.loads(gzip.decompress((HERE.parent/f'inserted-channel-factorization/result-{candidate}.json.gz').read_bytes()))
    expected={(av,arm,dps) for av in AS for arm in ARMS for dps in PRECISIONS}
    keys=[(r['a'],r['arm'],r['precision']) for r in p['rows']]
    if not(p['version']=='16.04' and p['all_valid'] is True and p['execution_head']==PARENT_HEAD and p['candidate_index']==candidate and len(keys)==12 and set(keys)==expected):raise ValueError('parent structure or identity invalid')
    for row in p['rows']:
        if [f['frame'] for f in row['frames']]!=[0,1]:raise ValueError('parent frames invalid')
    _,states,_=F.pinned();rec=states[candidate]
    rho=sp.Matrix([[rational_hex(v[0])+sp.I*rational_hex(v[1]) for v in row] for row in rec['state_hex']])
    return exact_coefficients(rho),rho,{(r['a'],r['arm'],r['precision']):r for r in p['rows']}

def measurement(candidate):
    d,rho,parents=load_inputs(candidate);cert=support_certificate()
    if not cert['exact_transfer_reconstruction']:raise ValueError('exact transfer reconstruction failed')
    k=exact_commutator(d,'D',SYMBOL)
    extra={w:c for w,c in d.items() if w[2]!=0 and w[3]!=0}
    extra_k=exact_commutator(extra,'D',SYMBOL)
    exact={};polynomials={}
    for arm in ARMS:
        z=exact_prepare(exact_middle(d,SYMBOL),arm);x=exact_prepare(k,arm)
        v=exact_connected(z,x);polynomials[arm]=v
        exact[arm]={**exact_localization(v),'direction_polynomials':[[[str(m[i,j]) for j in range(3)] for i in range(3)] for m in v],
                    'identity_middle_zero':all(sp.expand(y.subs(SYMBOL,1))==0 for m in v for y in m),
                    'commutator_one_body_zero':not V.restrict(x,1)}
    if not all(x['identity_middle_zero'] for x in exact.values()):raise ValueError('exact identity-middle control failed')
    rows=[];controls=[];previous={};valid=True
    for dps in PRECISIONS:
      with mp.workdps(dps):
        data=E.laws(dps);metrics={key:mp.mpf(0) for key in ['coefficient_identity','state_reconstruction','transfer_identity','commutator','exact_direction','global_covariance','retained_covariance','response_covariance','precision','hidden_null','hidden_pair_equality','hessian_identity','parent_response','parent_complete_norm','identity_middle_null']};ranks_ok=True
        def mx(key,value):
            if not mp.isfinite(value):raise ValueError('nonfinite residual '+key)
            metrics[key]=max(metrics[key],value)
        def stage(key,arr):
            for x in arr:F.finite_matrix(x)
            mx('global_covariance',F.norm(arr[1]-G.product_action(data['frames'],arr[0])))
            if dps==50:previous[key]=[x.copy() for x in arr]
            else:mx('precision',max(F.norm(x-y) for x,y in zip(arr,previous.pop(key))))
            return arr
        cv=numeric_vector(d);mrho=mp.matrix([[mp.mpc(numeric(sp.re(rho[i,j])),numeric(sp.im(rho[i,j]))) for j in range(16)] for i in range(16)])
        old,im=G.coefficients(mrho);mx('coefficient_identity',max(F.norm(cv-old),im));mx('state_reconstruction',F.norm(G.reconstruct(cv)-mrho))
        table=V.exact_tables()[0][1];tn=mp.zeros(16);labs=list(itertools.product(range(4),repeat=2))
        for j,w in enumerate(labs):
            for v,c in table[w].items():tn[labs.index(v),j]=numeric(c)
        mx('transfer_identity',F.norm(tn-data['source'][0]['D']))
        sv=stage('state',[cv,G.product_action(data['frames'],cv)])
        h=mp.zeros(256,81)
        for j,w in enumerate(V.H_LABELS):h[G.INDEX[w],j]=1
        hs=stage('hidden',[h,G.product_action(data['frames'],h)])
        def act(key,x,f):return G.apply(data['source'][f][key],V.SITES[key],x)
        first={key:stage(('first',key),[act(key,hs[f],f) for f in [0,1]]) for key in ['A','D']}
        entries=[A.lift(data['source'][f]['D'],V.SITES['D']) for f in [0,1]]
        for av in AS:
          a=R.exact_float(av);base=stage(('base',av),[G.middle(x,a) for x in sv])
          ks=stage(('D_commutator',av),[A.weight_action(entries[f],sv[f],a)[0] for f in [0,1]])
          for f in [0,1]:mx('commutator',F.norm(ks[f]-(act('D',base[f],f)-G.middle(act('D',sv[f],f),a))))
          ys={}
          for order,one,two in [('forward','A','D'),('reverse','D','A')]:
            cut=stage(('cut',av,order),[G.middle(first[one][f],a) for f in [0,1]])
            ys[order]=stage(('second',av,order),[act(two,cut[f],f) for f in [0,1]])
            for f in [0,1]:
                for x in [hs[f],G.middle(hs[f],a),first[one][f],cut[f],act(two,G.middle(hs[f],a),f)]:mx('hidden_null',G.restrict_norm(x,2))
                mx('hidden_null',G.restrict_norm(ys[order][f],1))
          for arm in ARMS:
            prep=lambda x,f:G.product_action(data['preparation'][arm][f],x)
            z=stage(('center',av,arm),[prep(base[f],f) for f in [0,1]])
            pk=stage(('prepared_D',av,arm),[prep(ks[f],f) for f in [0,1]])
            dirs=[A.connected(z[f],pk[f]) for f in [0,1]];gs,_=R.exact_frames()
            mx('retained_covariance',A.difference(dirs[1],[gs[i]*x*gs[j].T for x,(i,j) in zip(dirs[0],G.V96.EDGES)]))
            mx('exact_direction',A.difference(dirs[0],evaluate(polynomials[arm],av)))
            key=('directions',av,arm)
            if dps==50:previous[key]=[[x.copy() for x in v] for v in dirs]
            else:mx('precision',max(A.difference(x,y) for x,y in zip(dirs,previous.pop(key))))
            py={o:stage(('prepared_hidden',av,arm,o),[prep(ys[o][f],f) for f in [0,1]]) for o in ys}
            bs={o:[[G.pair_moments(py[o][f],j) for j in range(81)] for f in [0,1]] for o in ys}
            ts=[];frames=[];labels=[]
            for f in [0,1]:
                cs=G.correlations(z[f]);sc=G.correlations(base[f]);n=edge_norms(dirs[f])
                mx('hidden_pair_equality',A.listnorm([x-y for xx,yy in zip(bs['forward'][f],bs['reverse'][f]) for x,y in zip(xx,yy)]))
                for o in ys:mx('hidden_null',G.restrict_norm(py[o][f],1))
                _,t,res=A.contract(cs,sc,bs['forward'][f],dirs[f],arm);mx('hessian_identity',res)
                parent=parents[av,arm,dps]['frames'][f]
                mx('parent_response',F.norm(t-R.decoded(parent['T_D']['matrix'])))
                mx('parent_complete_norm',abs(n['complete']-mp.mpf(parent['direction_norms']['D']['connected'])))
                ranks_ok=ranks_ok and R.ranks_from(R.spectrum(t))==parent['T_D']['ranks'] and F.classify(t)==parent['classifications']['T_D']
                if av==1.:mx('identity_middle_null',max(F.norm(ks[f]),n['complete'],F.norm(t)))
                label=localize(n['retained'],F.norm(t));labels.append(label);ts.append(t)
                frames.append({'frame':f,'directions':[R.encoded(x) for x in dirs[f]],'norms':{key:[R.ns(x) for x in v] if isinstance(v,list) else R.ns(v) for key,v in n.items()},'T_D':F.record(t),'classification':F.classify(t),'localization':label,'origin_correlations':[R.encoded(x) for x in cs],'edges':F.diagnostics(cs,sc,arm)})
            key=('response',av,arm);old=previous.get(key) if dps==80 else None;ok,_=F.agreement(ts,old,classification=True);ranks_ok=ranks_ok and ok and labels[0]==labels[1]
            mx('response_covariance',F.norm(ts[0]-ts[1]))
            if dps==50:previous[key]=ts;previous[('labels',av,arm)]=labels
            else:
                mx('precision',max(F.norm(x-y) for x,y in zip(ts,previous.pop(key))));ranks_ok=ranks_ok and labels==previous.pop(('labels',av,arm))
            rows.append({'candidate_index':candidate,'a':av,'arm':arm,'precision':dps,'frames':frames})
            print(f'candidate={candidate} precision={dps} a={av} arm={arm} localization={labels[0]}',flush=True)
        limits={key:mp.mpf('1e-35') for key in metrics};limits['precision']=mp.mpf('1e-30')
        pv=bool(data['controls']['valid'] and data['isotropic_controls']['valid'] and ranks_ok and all(v<=limits[key] for key,v in metrics.items()))
        valid=valid and pv;controls.append({'precision':dps,'all_valid':pv,'ranks_and_localizations_agree':bool(ranks_ok),'metrics':{key:R.ns(v) for key,v in metrics.items()},'limits':{key:R.ns(v) for key,v in limits.items()},'laws':data['controls'],'isotropic_laws':data['isotropic_controls']})
    valid=bool(valid and not previous and len(rows)==12)
    eb=[f['localization'] for row in rows if row['precision']==80 and row['a']!=1. for f in row['frames']]
    exactzero=all(x['retained_zero'] for x in exact.values())
    verdict='INVALID' if not valid else ('EXACT_RETAINED_EDGE_LOCALIZATION_CONFIRMED' if exactzero and all(x=='RETAINED_EDGE_NULL' for x in eb) else 'LOCALIZATION_MIXED_OR_NOT_CONFIRMED')
    return {'version':'16.05','candidate_index':candidate,'all_valid':valid,'verdict':verdict,'parent_execution_head':PARENT_HEAD,'support_certificate':cert,'excluded_state_coefficients':[[list(w),str(c)] for w,c in extra.items()],'excluded_sector_commutator_zero':not extra_k,'excluded_sector_commutator':[[list(w),str(c)] for w,c in extra_k.items()],'exact':exact,'rows':rows,'controls':controls,'scope':'Localization for frozen states/sources/preparations and five-edge readout. No sixth-edge polar readout, universal source law or gravity claim.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=int,choices=CANDIDATES,required=True);args=ap.parse_args()
    try:r=measurement(args.candidate)
    except Exception as exc:
        traceback.print_exc();r={'version':'16.05','candidate_index':args.candidate,'all_valid':False,'verdict':'INVALID','error':str(exc)}
    r['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
    out=HERE/f'result-{args.candidate}.json.gz';out.write_bytes(gzip.compress((json.dumps(r,indent=2,allow_nan=False)+'\n').encode(),mtime=0))
    names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py',out.name]
    (HERE/f'SHA256SUMS-{args.candidate}').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
    print(json.dumps({key:r[key] for key in ['version','candidate_index','all_valid','verdict','execution_head']}));sys.exit(0 if r['all_valid'] else 2)
