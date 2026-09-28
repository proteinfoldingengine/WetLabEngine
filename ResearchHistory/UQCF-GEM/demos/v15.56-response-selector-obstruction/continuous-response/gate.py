"""16.12: continuous weighted response and exact first-order Gram blindness."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('family1611_continuous',HERE.parent/'coherence-family/gate.py');A=importlib.util.module_from_spec(q);q.loader.exec_module(A)
B=A.B;S=A.S;L=A.L;R=A.R;F=A.F;LAM=A.LAM
PRECISIONS=[80,120];LAMBDAS=[-1,0,1];STEPS=[8,64]
def entry_bound(matrices):return sum((abs(x) for m in matrices for x in m),sp.Integer(0))
def gram_derivative(c,v):return c.T*v+v.T*c
def energy_coefficients(n,m):return [n.T*n,n.T*m+m.T*n,m.T*m]
def weighted_polar(c,rank):
 F.finite_matrix(c)
 if rank==0:return mp.zeros(3),mp.zeros(3),mp.zeros(3)
 left,sv,right=mp.svd_r(c)
 if not 0<rank<=3 or sv[rank-1]<=0:raise ValueError('invalid exact rank')
 u=left[:,:rank]*right[:rank,:];h=right[:rank,:].T*mp.diag([sv[i] for i in range(rank)])*right[:rank,:]
 return u,h,u*h

def classify(valid,scientific):
 if not valid:return 'INVALID'
 return 'CONTINUOUS_SIGNED_NORMAL_RESPONSE_CERTIFIED' if scientific else 'CONTINUOUS_RESPONSE_CRITERIA_NOT_CONFIRMED'
def expand(m):return m.applyfunc(sp.expand)
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hash mismatch')
 r=json.loads(lzma.decompress((HERE.parent/'coherence-family/result.json.xz').read_bytes()));expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.11' and r['all_valid'] is True and r['execution_head']=='12e477696c361f919c9c947db24503e9ac64153d' and len(r['exact'])==144 and {(x['candidate'],x['a'],x['arm'],x['order']) for x in r['exact']}==expected):raise ValueError('parent identity/completeness')
 if not(len(r['density_certificates'])==12 and all(x['positive'] and x['normalized_trace']=='1' for x in r['density_certificates']) and r['source_certificate']['valid']):raise ValueError('parent physical certificates')
 return r

def audit():
 parent=load_parent();exact=[];pairs=[];rows=[];cache={};old={};metrics={k:mp.mpf(0) for k in ['weighted_reconstruction','polar','normal_identity','energy_identity','gram_blindness','covariance','uniform_bound','precision']}
 for x in parent['exact']:
  key=x['candidate'],x['a'],x['arm'],x['order'];c=B.decode(x['C']);vc=list(map(B.decode,x['V_coefficients']));wc=list(map(B.decode,x['W_coefficients']));v=vc[0]+LAM*vc[1];w=sum((LAM**i*m for i,m in enumerate(wc)),sp.zeros(3));st=S.stratum(c,vc[0]+vc[1]);p=st['left'];q=st['right'];lp=sp.eye(3)-p;rq=sp.eye(3)-q;n=B.decode(x['plus_normal'])
  if not(st['identities_valid'] and n==st['normal'] and st['rank']==x['rank'] and st['normal_rank']==x['normal_rank']):raise ValueError('parent projector/normal mismatch')
  normal=expand(lp*v*rq);mc=[expand(lp*m*rq) for m in wc];m=sum((LAM**i*z for i,z in enumerate(mc)),sp.zeros(3));poly=c+A.P.PARAM*v+A.P.PARAM**2*w;kpoly=expand(lp*poly*rq)
  identity=normal==LAM*n and kpoly==expand(A.P.PARAM*LAM*n+A.P.PARAM**2*m)
  gd=expand(gram_derivative(c,v));blind=gd==expand(gram_derivative(c,v-normal))
  ec=list(map(expand,energy_coefficients(LAM*n,m)));energy=expand(kpoly.T*kpoly);energy_identity=energy==expand(sum((A.P.PARAM**(i+2)*z for i,z in enumerate(ec)),sp.zeros(3)))
  b_v=entry_bound(vc);b_w=entry_bound(wc);bound_valid=bool(b_v>=0 and b_w>=0 and b_v.is_Rational and b_w.is_Rational)
  cache[key]=(c,vc,wc,p,q,n,mc,b_v,b_w);exact.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'C':S.encode(c),'V_coefficients':[S.encode(z) for z in vc],'W_coefficients':[S.encode(z) for z in wc],'left_projector':S.encode(p),'right_projector':S.encode(q),'normal':S.encode(n),'normal_rank':int(n.rank()),'normal_norm_squared':str(sp.trace(n.T*n)),'M_coefficients':[S.encode(z) for z in mc],'gram_derivative_coefficients':[S.encode(expand(gram_derivative(c,z))) for z in vc],'normal_energy_coefficients':[S.encode(z) for z in ec],'uniform_bound_V':str(b_v),'uniform_bound_W':str(b_w),'normal_identity':bool(identity),'gram_first_order_blind':bool(blind),'energy_identity':bool(energy_identity),'bound_valid':bound_valid})
 for candidate in L.CANDIDATES:
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    aft=cache[candidate,av,arm,'after'];bef=cache[candidate,av,arm,'before']
    if aft[0]!=bef[0] or aft[3:5]!=bef[3:5]:raise ValueError('order baseline/projector mismatch')
    delta=aft[5]-bef[5];scale=bef[5]==a*aft[5];nonzero=delta!=sp.zeros(3)
    if av==1. and aft[:3]!=bef[:3]:raise ValueError('identity-middle polynomial mismatch')
    pairs.append({'candidate':candidate,'a':av,'arm':arm,'positive_normal_scale':bool(scale),'scale':str(a),'normal_contrast':S.encode(delta),'normal_contrast_norm_squared':str(sp.trace(delta.T*delta)),'nonzero':bool(nonzero),'expected_nonzero':av!=1.})
 print('Completed exact 144 families and 72 order pairs',flush=True)
 for precision in PRECISIONS:
  with mp.workdps(precision):
   gs,_=R.exact_frames()
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite residual '+k)
    metrics[k]=max(metrics[k],x)
   for key,(c,vc,wc,p,q,n,mc,bv,bw) in cache.items():
    cm=S.number_matrix(c);pm=S.number_matrix(p);qm=S.number_matrix(q);nm=S.number_matrix(n)
    for lam in LAMBDAS:
     v=vc[0]+lam*vc[1];w=sum((lam**i*m for i,m in enumerate(wc)),sp.zeros(3));m=sum((lam**i*z for i,z in enumerate(mc)),sp.zeros(3));vm=S.number_matrix(v);mm=S.number_matrix(m);actual_normal=expand((sp.eye(3)-p)*v*(sp.eye(3)-q));actual_nm=S.number_matrix(actual_normal);energy_coeff=list(map(S.number_matrix,energy_coefficients(actual_normal,m)))
     for step in STEPS:
      s=sp.Rational(1,2**step);sm=L.numeric(s);ce=c+s*v+s*s*w;rank=int(ce.rank());cn=S.number_matrix(ce);bound=sm*L.numeric(bv)+sm**2*L.numeric(bw)
      for frame in [0,1]:
       left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cn*right.T;cb=left*cm*right.T;pf=left*pm*left.T;qf=right*qm*right.T;nf=left*nm*right.T;mf=left*mm*right.T;vf=left*vm*right.T;actual_nf=left*actual_nm*right.T
       u,h,weighted=weighted_polar(cf,rank);mx('weighted_reconstruction',F.norm(weighted-cf));mx('polar',max(B.polar_error(cf,u),F.norm(h-u.T*cf)))
       ks=(mp.eye(3)-pf)*cf*(mp.eye(3)-qf)/sm;energy=ks.T*ks;mx('normal_identity',F.norm(ks-actual_nf-sm*mf));expected=right*(energy_coeff[0]+sm*energy_coeff[1]+sm**2*energy_coeff[2])*right.T;mx('energy_identity',F.norm(energy-expected));mx('gram_blindness',F.norm(cb.T*actual_nf+actual_nf.T*cb));mx('uniform_bound',max(mp.mpf(0),F.norm(cf-cb)-bound))
       values=(cf,weighted,ks,energy)
       if frame==0:native=tuple(z.copy() for z in values)
       else:mx('covariance',max(F.norm(values[i]-(gs[2]*native[i]*gs[3].T if i<3 else gs[3]*native[i]*gs[3].T)) for i in range(4)))
       pk=key,lam,step,frame
       if precision==80:old[pk]=tuple(z.copy() for z in values)
       else:mx('precision',max(F.norm(z-y) for z,y in zip(values,old.pop(pk))))
       rows.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'lambda':lam,'step_power':step,'precision':precision,'frame':frame,'exact_rank':rank,'C':R.encoded(cf),'weighted_polar':R.encoded(weighted),'K_over_s':R.encoded(ks),'normal_energy_over_s_squared':R.encoded(energy),'distance_to_baseline':R.ns(F.norm(cf-cb)),'uniform_bound':R.ns(bound),'signed_derivative_error':R.ns(F.norm(ks-lam*nf)),'energy_leading_error':R.ns(F.norm(energy-right*energy_coeff[0]*right.T))})
   print('Completed precision',precision,flush=True)
 valid=bool(len(exact)==144 and len(pairs)==72 and len(rows)==3456 and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 scientific=all(x['normal_identity'] and x['gram_first_order_blind'] and x['energy_identity'] and x['bound_valid'] and x['normal_rank']>0 for x in exact) and all(x['positive_normal_scale'] and x['nonzero']==x['expected_nonzero'] for x in pairs)
 return {'version':'16.12','all_valid':valid,'verdict':classify(valid,scientific),'exact':exact,'pairs':pairs,'rows':rows,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'source_certificate':parent['source_certificate'],'density_certificates':parent['density_certificates'],'scope':'Different continuous observables on the frozen sixth edge, not a repaired polar transport, source-selection law, or gravity derivation.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.12','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
