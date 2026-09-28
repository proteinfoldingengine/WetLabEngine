"""v16.08: physically realized ordered CPTP paths, explicit normalized input control."""
import gzip,hashlib,importlib.util,json,pathlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stratum1607_paths',HERE.parent/'support-stratum-stability/gate.py')
S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
D=S.D;L=S.L;R=L.R;F=L.F;G=L.G
PARAM=sp.Symbol('s',real=True)

def density_certificate(rho):
 if rho.rows!=rho.cols or rho!=rho.H:raise ValueError('input must be exactly Hermitian')
 tr=sp.trace(rho)
 if tr.is_positive is not True:raise ValueError('nonpositive trace')
 lower=sp.eye(rho.rows);diag=sp.zeros(rho.rows)
 for i in range(rho.rows):
  for j in range(i):
   lower[i,j]=sp.expand((rho[i,j]-sum(lower[i,k]*sp.conjugate(lower[j,k])*diag[k,k] for k in range(j)))/diag[j,j])
  pivot=sp.expand(rho[i,i]-sum(lower[i,k]*sp.conjugate(lower[i,k])*diag[k,k] for k in range(i)))
  if pivot.is_Rational is not True or pivot<=0:raise ValueError('nonpositive or nonrational exact LDL pivot')
  diag[i,i]=pivot
 valid=all(sp.expand(x)==0 for x in lower*diag*lower.H-rho)
 if not valid:raise ValueError('LDL reconstruction failed')
 return {'trace':tr,'trace_defect':tr-1,'normalized_trace':sp.trace(rho/tr),'pivots':[diag[i,i] for i in range(rho.rows)],'valid':valid}

def channel_certificate():
 ps=[sp.eye(2),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
 u=(sp.kronecker_product(ps[3],ps[0])+sp.kronecker_product(ps[1],ps[1]))/sp.sqrt(2)
 unitary=sp.simplify(u.H*u)==sp.eye(4)
 prep={'plane':[sp.Rational(1,2),sp.Rational(1,4),sp.Rational(1,4),sp.Integer(0)],'isotropic':[sp.Rational(1,2)]+[sp.Rational(1,6)]*3}
 middle={str(av):[(1+3*sp.Rational(*av.as_integer_ratio()))/4]+[(1-sp.Rational(*av.as_integer_ratio()))/4]*3 for av in L.AS}
 weights=all(sum(w)==1 and all(x>=0 for x in w) for w in list(prep.values())+list(middle.values()))
 return {'valid':bool(unitary and weights and L.V.exact_tables()[1]),'unitary':unitary,'exact_transfer_reconstruction':L.V.exact_tables()[1],'preparation_weights':{k:[str(x) for x in w] for k,w in prep.items()},'middle_weights':{k:[str(x) for x in w] for k,w in middle.items()},'source_weights':['1-s','s'],'source_interval':[0,1]}

def path_directions(d,a,arm):
 base=L.exact_middle(d,a);z=L.exact_prepare(base,arm)
 return z,{'after':L.exact_prepare(L.V.exact_action(base,'D'),arm),'before':L.exact_prepare(L.exact_middle(L.V.exact_action(d,'D'),a),arm)}

def connected_path(z,x):
 c=D.connected(z);v=L.exact_connected(z,x)[5];poly=D.connected(L.V.add(z,x,PARAM));w=poly.applyfunc(lambda t:sp.expand(t).coeff(PARAM,2))
 if (poly-c-PARAM*v-PARAM**2*w).applyfunc(sp.expand)!=sp.zeros(3):raise ValueError('path differential/quadratic mismatch')
 return c,v,w,poly

def verdict(valid,forced):
 if not valid or not forced:return 'INVALID'
 return 'PHYSICAL_PATH_SUPPORT_DISCONTINUITY_FORCED' if all(forced) else ('NO_FIRST_ORDER_PHYSICAL_PATH_OBSTRUCTION' if not any(forced) else 'MIXED_PHYSICAL_PATH_STABILITY')

def archive(s):return {k:S.encode(v) if isinstance(v,sp.MatrixBase) else str(v) if isinstance(v,sp.Basic) else v for k,v in s.items()}

def audit():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hash mismatch')
 parent=json.loads(gzip.decompress((HERE.parent/'support-stratum-stability/result.json.gz').read_bytes()))
 expected={(n,a,arm) for n in L.CANDIDATES for a in L.AS for arm in L.ARMS};old={(x['candidate'],x['a'],x['arm']):x for x in parent['exact']}
 if not(parent['version']=='16.07' and parent['all_valid'] is True and parent['execution_head']=='fc08e122cd6b1949ba71b2582500c0724bb3ff1c' and len(parent['exact'])==72 and set(old)==expected):raise ValueError('parent identity/completeness')
 cert=channel_certificate();valid=cert['valid'];exact=[];rows=[];densities=[];law_controls=[];previous={}
 metrics={k:mp.mpf(0) for k in ['global_C','global_V','normal','covariance','projector','precision']}
 for candidate in L.CANDIDATES:
  raw,rho,_=L.load_inputs(candidate);dc=density_certificate(rho);tau=dc['trace'];densities.append({'candidate':candidate,**{k:[str(t) for t in v] if isinstance(v,list) else str(v) if isinstance(v,sp.Basic) else v for k,v in dc.items()}})
  valid=valid and dc['valid'] and dc['normalized_trace']==1
  inputs={'RAW':raw,'NORMALIZED':{w:c/tau for w,c in raw.items()}};local={}
  for representation,d in inputs.items():
   for av in L.AS:
    a=sp.Rational(*av.as_integer_ratio())
    for arm in L.ARMS:
     z,paths=path_directions(d,a,arm);rec={}
     for order,x in paths.items():
      c,v,w,poly=connected_path(z,x);st=S.stratum(c,v);valid=valid and st['identities_valid'];rec[order]=(c,v,w,poly,st)
      local[representation,av,arm,order]=rec[order]
      exact.append({'candidate':candidate,'representation':representation,'a':av,'arm':arm,'order':order,'C':S.encode(c),'V':S.encode(v),'quadratic':S.encode(w),'polynomial':S.encode(poly),**archive(st)})
     if av==1. and rec['after'][3]!=rec['before'][3]:raise ValueError('identity-middle path inequality')
     delta=rec['after'][1]-rec['before'][1];delta_n=rec['after'][4]['normal']-rec['before'][4]['normal']
     contrast=L.exact_connected(z,L.V.add(paths['after'],paths['before'],-1))[5]
     if delta!=contrast:raise ValueError('connected differential linearity failed')
     if representation=='RAW':
      previous_exact=old[candidate,av,arm];decode=lambda m:sp.Matrix([[sp.Rational(t) for t in rr] for rr in m])
      if rec['after'][0]!=decode(previous_exact['C']) or delta!=decode(previous_exact['V']) or delta_n!=decode(previous_exact['normal']) or int(delta_n.rank())!=previous_exact['normal_rank']:raise ValueError('RAW parent contrast mismatch')
  for precision in L.PRECISIONS:
   with mp.workdps(precision):
    laws=L.E.laws(precision);valid=valid and laws['controls']['valid'] and laws['isotropic_controls']['valid']
    if candidate==L.CANDIDATES[0]:law_controls.append({'precision':precision,'source_preparation':laws['controls'],'isotropic':laws['isotropic_controls']})
    gs,_=R.exact_frames()
    def mx(k,v):
     if not mp.isfinite(v):raise ValueError('nonfinite residual')
     metrics[k]=max(metrics[k],v)
    for representation,d in inputs.items():
     state=L.numeric_vector(d);states=[state,G.product_action(laws['frames'],state)]
     for av in L.AS:
      a=R.exact_float(av);bases=[G.middle(t,a) for t in states]
      def act(t,f):return G.apply(laws['source'][f]['D'],L.V.SITES['D'],t)
      dirs={'after':[act(t,f) for f,t in enumerate(bases)],'before':[G.middle(act(t,f),a) for f,t in enumerate(states)]}
      for arm in L.ARMS:
       centers=[G.product_action(laws['preparation'][arm][f],bases[f]) for f in [0,1]]
       for order in ['after','before']:
        derivs=[G.product_action(laws['preparation'][arm][f],dirs[order][f]) for f in [0,1]]
        c,v,_,_,st=local[representation,av,arm,order];cm=S.number_matrix(c);vm=S.number_matrix(v);pm=S.number_matrix(st['left']);qm=S.number_matrix(st['right']);nm=S.number_matrix(st['normal'])
        for frame in [0,1]:
         left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];p=left*pm*left.T;q=right*qm*right.T
         cf=G.correlations(centers[frame])[5];vf=L.A.connected(centers[frame],derivs[frame])[5];n=(mp.eye(3)-p)*vf*(mp.eye(3)-q)
         mx('global_C',F.norm(cf-left*cm*right.T));mx('global_V',F.norm(vf-left*vm*right.T));mx('normal',F.norm(n-left*nm*right.T))
         mx('projector',max(F.norm(p*p-p),F.norm(q*q-q),F.norm(p*cf-cf),F.norm(cf*q-cf)))
         if frame==0:native_n=n.copy()
         else:mx('covariance',F.norm(n-gs[2]*native_n*gs[3].T))
         key=(candidate,representation,av,arm,order,frame)
         if precision==50:previous[key]=(cf.copy(),vf.copy(),n.copy())
         else:mx('precision',max(F.norm(x-y) for x,y in zip((cf,vf,n),previous.pop(key))))
         rows.append({'candidate':candidate,'representation':representation,'a':av,'arm':arm,'order':order,'precision':precision,'frame':frame,'C':R.encoded(cf),'V':R.encoded(vf),'normal':R.encoded(n),'normal_norm':R.ns(F.norm(n)),'rank':st['rank'],'normal_rank':st['normal_rank'],'classification':st['classification']})
  print('Audited candidate',candidate,flush=True)
 forced=[x['normal_rank']>0 for x in exact if x['representation']=='NORMALIZED' and x['a']!=1.]
 valid=bool(valid and len(exact)==288 and len(rows)==1152 and len(forced)==96 and not previous and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 return {'version':'16.08','all_valid':valid,'verdict':verdict(valid,forced),'channel_certificate':cert,'density_certificates':densities,'exact':exact,'rows':rows,'metrics':{k:mp.nstr(v,50) for k,v in metrics.items()},'law_controls':law_controls,'physical_EB_forced_count':sum(forced),'physical_EB_case_count':len(forced),'scope':'NORMALIZED are exactly normalized physical CPTP paths; RAW are preserved nonunit-trace algebraic controls. Mixture parameter s is not fundamental time.'}

if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.08','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
 (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json']
 (HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
 print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
