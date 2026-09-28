"""16.11 exact fixed-coherence boundary classification, including lambda=0."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('reversal1610_family',HERE.parent/'source-reversal/gate.py');T=importlib.util.module_from_spec(q);q.loader.exec_module(T)
B=T.B;P=T.P;L=T.L;S=T.S;R=T.R;F=T.F
LAM=sp.Symbol('lambda',real=True);LAMBDAS=[sp.Rational(-1,2),sp.Integer(0),sp.Rational(1,2)];STEPS=[32,128,192]
def det3(m):
 if m.rows!=3 or m.cols!=3:raise ValueError("expected 3x3 matrix")
 return m[0,0]*(m[1,1]*m[2,2]-m[1,2]*m[2,1])-m[0,1]*(m[1,0]*m[2,2]-m[1,2]*m[2,0])+m[0,2]*(m[1,0]*m[2,1]-m[1,1]*m[2,0])
def weights(s,lam):
 if not(0<=s<=1 and -1<=lam<=1):raise ValueError('outside CPTP rectangle')
 return [1-s,s*(1+lam)/2,s*(1-lam)/2]
def family_action(d,lam):
 plus=T.action(d,1);minus=T.action(d,-1)
 return L.V.add({w:(1+lam)*c/2 for w,c in plus.items()},minus,(1-lam)/2)
def paths(d,a,arm,lam):
 base=L.exact_middle(d,a);z=L.exact_prepare(base,arm)
 return z,{'after':L.exact_prepare(family_action(base,lam),arm),'before':L.exact_prepare(L.exact_middle(family_action(d,lam),a),arm)}
def zero_certificate(c,v,w):
 r=int(c.rank());rpoly=B.polynomial_rank(c+P.PARAM*v+P.PARAM**2*w)
 return {'certified':rpoly==r,'baseline_rank':r,'polynomial_rank':rpoly,'method':'exact polynomial minors in s'}
def continuum_bound(coefficients,r,k):
 if r+k==3:return {'certified':True,'upper_bound':3,'method':'ambient dimension for every fixed nonzero lambda'}
 if r+k==2 and all(m[i,2]==0 and m[2,i]==0 for m in coefficients for i in range(3)):return {'certified':True,'upper_bound':2,'method':'common plane coefficient identity for all lambda'}
 return {'certified':False,'upper_bound':None,'method':'no structural bound certified'}
def classify(valid,identities,zero,nonzero):
 if not valid:return 'INVALID'
 if not identities:return 'FAMILY_IDENTITIES_NOT_CONFIRMED'
 if not zero:return 'ZERO_COHERENCE_RANK_CHANGE'
 if not nonzero:return 'CONTINUUM_LIMIT_NOT_CERTIFIED'
 return 'THREE_COHERENCE_BOUNDARY_CLASSES_CERTIFIED'
def coefficients(m,degree):return [m.applyfunc(lambda t:sp.expand(t).coeff(LAM,i)) for i in range(degree+1)]
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hashes mismatch')
 r=json.loads(lzma.decompress((HERE.parent/'source-reversal/result.json.xz').read_bytes()));expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.10' and r['all_valid'] and r['execution_head']=='1e9a5e8029e53b09998f99b122a9df3324178b1b' and len(r['exact'])==144 and {(x['candidate'],x['a'],x['arm'],x['order']) for x in r['exact']}==expected):raise ValueError('parent identity/completeness')
 return {(x['candidate'],x['a'],x['arm'],x['order']):x for x in r['exact']}
def audit():
 parent=load_parent();source=T.source_certificate();cert=P.channel_certificate()
 if not(source['valid'] and cert['valid']):raise ValueError('channel certificate')
 ss,ll=sp.symbols('s lambda',real=True);ws=[1-ss,ss*(1+ll)/2,ss*(1-ll)/2]
 if sp.expand(sum(ws)-1)!=0:raise ValueError('weight identity')
 source['family_weights']=[str(x) for x in ws];source['lambda_interval']=[-1,1];source['nonnegativity_proof']='Each factor s, 1-s, 1+lambda, 1-lambda is nonnegative on the declared rectangle.'
 exact=[];pairs=[];rows=[];finite=[];densities=[];cache={};old={};metrics={k:mp.mpf(0) for k in ['polar','limit_identity','class_gap','covariance','precision','finite_polar','finite_covariance']}
 for candidate in L.CANDIDATES:
  raw,rho,_=L.load_inputs(candidate);dc=P.density_certificate(rho)
  if not(dc['valid'] and dc['normalized_trace']==1):raise ValueError('density certificate')
  d={w:c/dc['trace'] for w,c in raw.items()};densities.append({'candidate':candidate,'raw_trace':str(dc['trace']),'normalized_trace':str(dc['normalized_trace']),'positive':dc['valid']})
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    z,dirs=paths(d,a,arm,LAM)
    for order,x in dirs.items():
     key=candidate,av,arm,order;c,v,w,poly=P.connected_path(z,x);vc=coefficients(v,1);wc=coefficients(w,2)
     if (v-vc[0]-LAM*vc[1]).applyfunc(sp.expand)!=sp.zeros(3) or (w-sum((LAM**i*m for i,m in enumerate(wc)),sp.zeros(3))).applyfunc(sp.expand)!=sp.zeros(3):raise ValueError('unexpected polynomial degree')
     pp=parent[key]
     if c!=B.decode(pp['C']):raise ValueError('baseline mismatch')
     for sign,name in [(1,'plus'),(-1,'minus')]:
      if v.subs(LAM,sign)!=B.decode(pp[name]['V']) or w.subs(LAM,sign)!=B.decode(pp[name]['quadratic']):raise ValueError('endpoint parent mismatch')
     st=S.stratum(c,v.subs(LAM,1));n=((sp.eye(3)-st['left'])*v*(sp.eye(3)-st['right'])).applyfunc(sp.expand);np=st['normal']
     if not st['identities_valid'] or np!=B.decode(pp['plus']['normal']):raise ValueError('endpoint normal mismatch')
     identity=bool(n==LAM*np and np!=sp.zeros(3));zc=zero_certificate(c,vc[0],wc[0]);nc=continuum_bound([c,*vc,*wc],st['rank'],st['normal_rank']);good=identity and zc['certified'] and nc['certified'];cache[key]=(c,vc,wc,np,st,good)
     exact.append({'candidate':candidate,'a':av,'arm':arm,'order':order,'C':S.encode(c),'V_coefficients':[S.encode(m) for m in vc],'W_coefficients':[S.encode(m) for m in wc],'normal_coefficients':[S.encode(m) for m in coefficients(n,1)],'plus_normal':S.encode(np),'rank':st['rank'],'normal_rank':st['normal_rank'],'normal_identity':identity,'zero_certificate':zc,'nonzero_certificate':nc,'all_classes_certified':good})
    aft=cache[candidate,av,arm,'after'];bef=cache[candidate,av,arm,'before']
    if aft[0]!=bef[0]:raise ValueError('order baseline mismatch')
    if av==1. and aft[:3]!=bef[:3]:raise ValueError('identity middle mismatch')
    pairs.append({'candidate':candidate,'a':av,'arm':arm,'positive_normal_scale':B.positive_scale(aft[3],bef[3],a),'scale':str(a)})
  print('Symbolic family candidate',candidate,flush=True)
 for precision in [80,120]:
  with mp.workdps(precision):
   gs,_=R.exact_frames()
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite residual')
    metrics[k]=max(metrics[k],x)
   for key,(c,vc,wc,n,st,good) in cache.items():
    if not good:continue
    limits={}
    for lam in LAMBDAS:
     sign=int(sp.sign(lam));cm=S.number_matrix(c);nm=S.number_matrix(lam*n);k=st['normal_rank'] if sign else 0
     for frame in [0,1]:
      left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cm*right.T;nf=left*nm*right.T;uc=B.polar(cf,st['rank']);un=B.polar(nf,k);b=uc+un;limits[lam,frame]=b.copy()
      mx('polar',max(B.polar_error(cf,uc),B.polar_error(nf,un)));mx('limit_identity',F.norm(b*b.T*b-b));mx('class_gap',abs(F.norm(b-uc)**2-k))
      if frame==1:mx('covariance',F.norm(b-gs[2]*limits[lam,0]*gs[3].T))
      if precision==80:old[key,lam,frame]=b.copy()
      else:mx('precision',F.norm(b-old.pop((key,lam,frame))))
      rows.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'lambda':str(lam),'precision':precision,'frame':frame,'limit':R.encoded(b),'limit_rank':st['rank']+k,'determinant':R.ns(det3(b)),'gap_to_baseline':R.ns(F.norm(b-uc))})
     if precision==120:
      v=vc[0]+lam*vc[1];w=sum((lam**i*m for i,m in enumerate(wc)),sp.zeros(3))
      for step in STEPS:
       s=sp.Rational(1,2**step);ce=c+s*v+s*s*w;rank=int(ce.rank());cn=S.number_matrix(ce)
       for frame in [0,1]:
        left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cn*right.T;u=B.polar(cf,rank);mx('finite_polar',B.polar_error(cf,u))
        if frame==0:native=u.copy()
        else:mx('finite_covariance',F.norm(u-gs[2]*native*gs[3].T))
        finite.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'lambda':str(lam),'step_power':step,'frame':frame,'exact_rank':rank,'polar':R.encoded(u),'error_to_limit':R.ns(F.norm(u-limits[lam,frame]))})
    for frame in [0,1]:mx('class_gap',abs(F.norm(limits[LAMBDAS[2],frame]-limits[LAMBDAS[0],frame])**2-4*st['normal_rank']))
   print('Completed precision',precision,flush=True)
 count=sum(x['all_classes_certified'] for x in exact);valid=bool(len(exact)==144 and len(pairs)==72 and len(rows)==12*count and len(finite)==18*count and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()));identities=all(x['normal_identity'] for x in exact) and all(x['positive_normal_scale'] for x in pairs);zero=all(x['zero_certificate']['certified'] for x in exact);nonzero=all(x['nonzero_certificate']['certified'] for x in exact)
 return {'version':'16.11','all_valid':valid,'verdict':classify(valid,identities,zero,nonzero),'source_certificate':source,'density_certificates':densities,'exact':exact,'pairs':pairs,'rows':rows,'finite':finite,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'scope':'Full coherence interval, fixed lambda then s approaches zero; no uniform or joint-limit claim, and no source-selection law.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.11','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','DETERMINANT_REGRESSION.json','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
