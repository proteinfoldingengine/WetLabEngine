"""v16.07 exact normal-to-rank-stratum obstruction; no finite path is assumed."""
import gzip,hashlib,importlib.util,json,pathlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('domain1606_stratum',HERE.parent/'sixth-edge-domain/gate.py')
D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
L=D.L;R=L.R;F=L.F

def stratum(c,v):
 if c.shape!=(3,3) or v.shape!=(3,3) or any(not x.is_Rational for x in list(c)+list(v)):raise ValueError('exact rational 3x3 inputs required')
 cp=c.pinv();p=c*cp;q=cp*c;i=sp.eye(3);n=(i-p)*v*(i-q);t=p*v+v*q-p*v*q
 identities=[c*cp*c-c,cp*c*cp-cp,p-p.T,q-q.T,p*p-p,q*q-q,p*c-c,c*q-c,v-t-n,p*n,n*q]
 ok=all(x==sp.zeros(3) for x in identities)
 rank=int(c.rank());k=int(n.rank())
 return {'rank':rank,'normal_rank':k,'pseudoinverse':cp,'left':p,'right':q,'normal':n,'tangent':t,'normal_norm_squared':sp.expand(sum(x*x for x in n)),'identities_valid':ok,'jump_bound_squared':k,'classification':'FORCED_RANK_CHANGE' if k else 'TANGENT_COMPATIBLE_NOT_PATH_CERTIFIED'}

def verdict(valid,forced):
 if not valid or not forced:return 'INVALID'
 return 'SUPPORT_POLAR_DISCONTINUITY_FORCED' if all(forced) else ('NO_FIRST_ORDER_RANK_OBSTRUCTION' if not any(forced) else 'MIXED_SUPPORT_STABILITY')

def encode(m):return [[str(x) for x in row] for row in m.tolist()]
def number_matrix(m):return mp.matrix([[L.numeric(x) for x in row] for row in m.tolist()])

def audit():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('pinned hashes mismatch')
 parent6=json.loads(gzip.decompress((HERE.parent/'sixth-edge-domain/result.json.gz').read_bytes()))
 expected={(n,a,arm) for n in L.CANDIDATES for a in L.AS for arm in L.ARMS}
 if not(parent6['all_valid'] is True and parent6['version']=='16.06' and parent6['execution_head']=='dd7a023ac95de9a984b791a0de736f7f30174824'):raise ValueError('16.06 identity invalid')
 archived6={(x['candidate'],ev['a'],x['arm']):ev for x in parent6['exact'] for ev in x['evaluations']}
 if len(parent6['exact'])!=24 or sum(len(x['evaluations']) for x in parent6['exact'])!=72 or set(archived6)!=expected:raise ValueError('16.06 completeness')
 exact=[];rows=[];metrics={k:mp.mpf(0) for k in ['archive_C','archive_V','normal_covariance','projector_identity','normal_identity','precision']};previous={};valid=True
 for candidate in L.CANDIDATES:
  d,_,_=L.load_inputs(candidate)
  parent=json.loads(gzip.decompress((HERE.parent/f'retained-edge-localization/result-{candidate}.json.gz').read_bytes()))
  keys=[(r['a'],r['arm'],r['precision']) for r in parent['rows']]
  if not(parent['all_valid'] is True and parent['execution_head']=='24315bf18eed287f174f9b8e1e033fad55ea48f0' and parent['version']=='16.05' and parent['candidate_index']==candidate and len(keys)==12 and set(keys)=={(a,b,p) for a in L.AS for b in L.ARMS for p in L.PRECISIONS}):raise ValueError('16.05 identity/completeness')
  archived={(r['a'],r['arm'],r['precision']):r for r in parent['rows']}
  local={}
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio());base=L.exact_middle(d,a);direction=L.exact_commutator(d,'D',a)
   for arm in L.ARMS:
    z=L.exact_prepare(base,arm);x=L.exact_prepare(direction,arm);c=D.connected(z);v=L.exact_connected(z,x)[5];s=stratum(c,v)
    old=archived6[candidate,av,arm]
    if s['rank']!=old['rank'] or c!=sp.Matrix([[sp.Rational(y) for y in rr] for rr in old['matrix']]):raise ValueError('exact 16.06 mismatch')
    if av==1. and (v!=sp.zeros(3) or s['normal_rank']!=0):raise ValueError('identity-middle violation')
    valid=valid and s['identities_valid'];local[av,arm]=(c,v,s)
    exact.append({'candidate':candidate,'a':av,'arm':arm,'C':encode(c),'V':encode(v),**{k:encode(x) if isinstance(x,sp.MatrixBase) else str(x) if isinstance(x,sp.Basic) else x for k,x in s.items()}})
  for precision in L.PRECISIONS:
   with mp.workdps(precision):
    gs,_=R.exact_frames()
    def mx(k,x):
     if not mp.isfinite(x):raise ValueError('nonfinite residual')
     metrics[k]=max(metrics[k],x)
    for (av,arm),(c,v,s) in local.items():
     cm=number_matrix(c);vm=number_matrix(v);pm=number_matrix(s['left']);qm=number_matrix(s['right']);nm=number_matrix(s['normal'])
     rr=archived[av,arm,precision]
     if [f['frame'] for f in rr['frames']]!=[0,1]:raise ValueError('frame identity')
     for frame in [0,1]:
      left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3]
      cf=left*cm*right.T;vf=left*vm*right.T;p=left*pm*left.T;q=right*qm*right.T;n=(mp.eye(3)-p)*vf*(mp.eye(3)-q)
      f=rr['frames'][frame]
      mx('archive_C',F.norm(cf-R.decoded(f['origin_correlations'][5])));mx('archive_V',F.norm(vf-R.decoded(f['directions'][5])))
      mx('normal_covariance',F.norm(n-left*nm*right.T))
      mx('projector_identity',max(F.norm(p*p-p),F.norm(q*q-q),F.norm(p-p.T),F.norm(q-q.T),F.norm(p*cf-cf),F.norm(cf*q-cf)))
      mx('normal_identity',max(F.norm(p*n),F.norm(n*q),F.norm(vf-(p*vf+vf*q-p*vf*q)-n)))
      key=(candidate,av,arm,frame)
      if precision==50:previous[key]=n.copy()
      else:mx('precision',F.norm(n-previous.pop(key)))
      rows.append({'candidate':candidate,'a':av,'arm':arm,'precision':precision,'frame':frame,'C':R.encoded(cf),'V':R.encoded(vf),'left':R.encoded(p),'right':R.encoded(q),'normal':R.encoded(n),'normal_norm':R.ns(F.norm(n)),'exact_normal_norm':R.ns(mp.sqrt(L.numeric(s['normal_norm_squared']))),'exact_rank':s['rank'],'exact_normal_rank':s['normal_rank'],'classification':s['classification']})
  print('Audited candidate',candidate,flush=True)
 valid=bool(valid and len(exact)==72 and len(rows)==288 and not previous and L.V.exact_tables()[1] and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 forced=[x['normal_rank']>0 for x in exact if x['a']!=1.]
 return {'version':'16.07','all_valid':valid,'verdict':verdict(valid,forced),'exact':exact,'rows':rows,'metrics':{k:mp.nstr(v,50) for k,v in metrics.items()},'exact_transfer_reconstruction':L.V.exact_tables()[1],'EB_forced_count':sum(forced),'EB_case_count':len(forced),'scope':'Conditional obstruction for any differentiable matrix path realizing the frozen D direction; no physical path existence or alternative observable claimed.'}

if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.07','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
 (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json']
 (HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
 print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
