"""16.09 one-sided canonical polar limits on inherited physical paths."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback,itertools
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('physical1608_boundary',HERE.parent/'physical-channel-paths/gate.py');P=importlib.util.module_from_spec(q);q.loader.exec_module(P)
S=P.S;L=P.L;R=P.R;F=P.F
PRECISIONS=[80,120];STEPS=[8,32,64,128,192]
def decode(m):return sp.Matrix([[sp.Rational(x) for x in row] for row in m])
def polynomial_rank(c):
 if sp.expand(c.det())!=0:return 3
 if any(sp.expand(c.extract(i,j).det())!=0 for i in itertools.combinations(range(3),2) for j in itertools.combinations(range(3),2)):return 2
 return int(any(x!=0 for x in c))
def rank_certificate(c,v,w,r,k):
 if r+k==3:return {'certified':True,'upper_bound':3,'method':'ambient dimension'}
 if r+k==2 and all(m[i,2]==0 and m[2,i]==0 for m in [c,v,w] for i in range(3)):return {'certified':True,'upper_bound':2,'method':'exact common plane'}
 s=sp.Symbol('s');rank=polynomial_rank(c+s*v+s*s*w)
 return {'certified':rank==r+k,'upper_bound':rank,'method':'exact polynomial rank'}
def polar(c,rank):
 F.finite_matrix(c)
 if rank==0:return mp.zeros(c.rows,c.cols)
 u,sv,v=mp.svd_r(c)
 if not 0<rank<=min(c.rows,c.cols) or sv[rank-1]<=0:raise ValueError('invalid exact support rank')
 return u[:,:rank]*v[:rank,:]
def positive_scale(after,before,a):return bool(a>0 and before==a*after)
def pair_classification(scale,diffs):
 if len(diffs)!=4:return 'LIMIT_NOT_CERTIFIED'
 if scale:return 'EXACT_ORDER_AGREEMENT'
 if all(mp.mpf(x)>mp.mpf('1e-9') for x in diffs):return 'ORDER_LIMIT_DIFFERENCE_OBSERVED'
 if all(mp.mpf(x)<=mp.mpf('1e-35') for x in diffs):return 'NUMERICAL_AGREEMENT_ONLY'
 return 'UNRESOLVED'
def polar_error(c,u):
 h=u.T*c;ev,_=mp.eigsy((h+h.T)/2)
 return max(F.norm(u*u.T*u-u),F.norm(h-h.T),F.norm(u*h-c),max(mp.mpf(0),-ev[0]))
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('pinned hashes mismatch')
 parent=json.loads(lzma.decompress((HERE.parent/'physical-channel-paths/result.json.xz').read_bytes()))
 xs=[x for x in parent['exact'] if x['representation']=='NORMALIZED'];expected={(n,a,arm,o) for n in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(parent['version']=='16.08' and parent['all_valid'] is True and parent['execution_head']=='8739e9db7ce1cb2c4ae0a91600e20fb4a2e953f5' and len(xs)==144 and {(x['candidate'],x['a'],x['arm'],x['order']) for x in xs}==expected):raise ValueError('parent identity/completeness')
 return xs

def audit():
 xs=load_parent();exact=[];cache={};rows=[];finite=[];pairs=[];metrics={k:mp.mpf(0) for k in ['polar','support','limit_identity','covariance','precision','finite_polar','finite_covariance']};old={};limits={}
 for x in xs:
  c,v,w=map(decode,[x['C'],x['V'],x['quadratic']]);st=S.stratum(c,v);n=st['normal'];key=x['candidate'],x['a'],x['arm'],x['order']
  if n!=decode(x['normal']) or st['rank']!=x['rank'] or st['normal_rank']!=x['normal_rank'] or not st['identities_valid']:raise ValueError('parent normal mismatch')
  cert=rank_certificate(c,v,w,st['rank'],st['normal_rank']);cache[key]=(c,v,w,n,st,cert);exact.append({k:x[k] for k in ['candidate','a','arm','order','C','V','quadratic','normal','rank','normal_rank']}|{'rank_certificate':cert})
 for candidate in L.CANDIDATES:
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    after=cache[candidate,av,arm,'after'];before=cache[candidate,av,arm,'before']
    if after[0]!=before[0]:raise ValueError('order baseline mismatch')
    if av==1. and any(x!=y for x,y in zip(after[:3],before[:3])):raise ValueError('identity path mismatch')
    pairs.append({'candidate':candidate,'a':av,'arm':arm,'positive_normal_scale':positive_scale(after[3],before[3],a),'scale':str(a)})
 for precision in PRECISIONS:
  with mp.workdps(precision):
   gs,_=R.exact_frames()
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite residual')
    metrics[k]=max(metrics[k],x)
   for key,(c,v,w,n,st,cert) in cache.items():
    if not cert['certified']:continue
    cm,nm=S.number_matrix(c),S.number_matrix(n);nq=n.pinv()*n
    for frame in [0,1]:
     left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cm*right.T;nf=left*nm*right.T
     uc=polar(cf,st['rank']);un=polar(nf,st['normal_rank']);b=uc+un
     mx('polar',max(polar_error(cf,uc),polar_error(nf,un)))
     mx('support',max(F.norm(uc.T*uc-right*S.number_matrix(st['right'])*right.T),F.norm(un.T*un-right*S.number_matrix(nq)*right.T)))
     mx('limit_identity',F.norm(b*b.T*b-b))
     if frame==0:native=b.copy()
     else:mx('covariance',F.norm(b-gs[2]*native*gs[3].T))
     if precision==80:old[key,frame]=b.copy()
     else:mx('precision',F.norm(b-old.pop((key,frame))))
     limits[key,precision,frame]=b.copy()
     rows.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'precision':precision,'frame':frame,'baseline_polar':R.encoded(uc),'normal_polar':R.encoded(un),'limit':R.encoded(b),'limit_rank':st['rank']+st['normal_rank'],'determinant':R.ns(mp.det(b)),'baseline_gap':R.ns(F.norm(b-uc))})
    if precision==120:
     for step in STEPS:
      s=sp.Rational(1,2**step);ce=c+s*v+s*s*w;rank=int(ce.rank());cn=S.number_matrix(ce)
      for frame in [0,1]:
       left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cn*right.T;u=polar(cf,rank);mx('finite_polar',polar_error(cf,u))
       if frame==0:unative=u.copy()
       else:mx('finite_covariance',F.norm(u-gs[2]*unative*gs[3].T))
       finite.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'step_power':step,'frame':frame,'exact_rank':rank,'polar':R.encoded(u),'error_to_limit':R.ns(F.norm(u-limits[key,120,frame]))})
   print('Completed precision',precision,flush=True)
 for pair in pairs:
  key=pair['candidate'],pair['a'],pair['arm'];diffs=[]
  for precision in PRECISIONS:
   with mp.workdps(precision):
    for frame in [0,1]:
     a=limits.get(((*key,'after'),precision,frame));b=limits.get(((*key,'before'),precision,frame))
     if a is not None and b is not None:diffs.append(R.ns(F.norm(a-b)))
  if cache[(*key,'after')][5]['certified'] and cache[(*key,'before')][5]['certified'] and len(diffs)!=4:raise ValueError('missing order comparisons')
  pair['limit_differences']=diffs
  pair['classification']=pair_classification(pair['positive_normal_scale'],diffs)
  if pair['positive_normal_scale'] and any(mp.mpf(d)>mp.mpf('1e-35') for d in diffs):raise ValueError('exact equality/numerical contradiction')
 certified=sum(x['rank_certificate']['certified'] for x in exact);valid=bool(len(exact)==144 and len(pairs)==72 and len(rows)==4*certified and len(finite)==10*certified and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 verdict='INVALID' if not valid else 'LIMIT_NOT_CERTIFIED' if certified!=144 else 'COMMON_ORDER_BOUNDARY_LIMIT_CERTIFIED' if all(x['positive_normal_scale'] for x in pairs) else 'ORDER_LIMITS_NOT_FULLY_CERTIFIED'
 return {'version':'16.09','all_valid':valid,'verdict':verdict,'exact':exact,'pairs':pairs,'rows':rows,'finite':finite,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'scope':'One-sided limits for frozen normalized physical paths; no baseline canonical extension or source independence asserted.'}

if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.09','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
