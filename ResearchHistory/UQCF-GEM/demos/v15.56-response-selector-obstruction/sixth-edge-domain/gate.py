"""v16.06: exact baseline rank and inherited polar-domain audit; no loop extension."""
import gzip,hashlib,importlib.util,itertools,json,pathlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('localization1605_domain',HERE.parent/'retained-edge-localization/gate.py')
L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
R=L.R;F=L.F;E=L.E

def connected(d):
 def moment(items):
  w=[0]*4
  for i,j in items:w[i]=j
  return 4*d.get(tuple(w),0)
 return sp.Matrix(3,3,lambda i,j:sp.expand(moment([(2,i+1),(3,j+1)])-moment([(2,i+1)])*moment([(3,j+1)])))

def exact_record(c):
 return {'matrix':[[str(x) for x in row] for row in c.tolist()],'determinant':str(sp.factor(c.det())),'minors_2x2':[str(sp.factor(c.extract(i,j).det())) for i in itertools.combinations(range(3),2) for j in itertools.combinations(range(3),2)],'rank':int(c.rank())}

def domain(c,source,arm):
 F.finite_matrix(c);F.finite_matrix(source)
 sv=R.spectrum(c);ref=R.spectrum(source)[0]
 try:
  E.edge(c,source,arm);admitted=True;reason=None
 except ValueError as exc:
  if not str(exc).startswith('outside frozen'):raise
  admitted=False;reason=str(exc)
 return {'admitted':admitted,'reason':reason,'singular_values':[R.ns(x) for x in sv],'source_reference':R.ns(ref),'relative_singular_values':None if ref==0 else [R.ns(x/ref) for x in sv]}

def verdict(valid,decisions):
 if not valid or not decisions:return 'INVALID'
 return 'SIXTH_EDGE_ADMISSIBLE' if all(decisions) else ('SIXTH_EDGE_OUTSIDE_FROZEN_DOMAIN' if not any(decisions) else 'MIXED_DOMAIN')

def audit():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('pinned source hash mismatch')
 exact=[];rows=[];metrics={'archive_native':mp.mpf(0),'archive_transformed':mp.mpf(0),'precision':mp.mpf(0)};old={};decisions={};agree=True
 for candidate in L.CANDIDATES:
  d,_,_=L.load_inputs(candidate)
  parent=json.loads(gzip.decompress((HERE.parent/f'retained-edge-localization/result-{candidate}.json.gz').read_bytes()))
  expected={(a,arm,p) for a in L.AS for arm in L.ARMS for p in L.PRECISIONS}
  keys=[(r['a'],r['arm'],r['precision']) for r in parent['rows']]
  if not(parent['all_valid'] is True and parent['execution_head']=='24315bf18eed287f174f9b8e1e033fad55ea48f0' and parent['version']=='16.05' and parent['candidate_index']==candidate and len(keys)==12 and set(keys)==expected):raise ValueError('parent identity/completeness')
  polynomials={arm:connected(L.exact_prepare(L.exact_middle(d,L.SYMBOL),arm)) for arm in L.ARMS}
  source=connected(L.exact_middle(d,L.SYMBOL))
  for arm,c in polynomials.items():exact.append({'candidate':candidate,'arm':arm,'polynomial':exact_record(c),'evaluations':[{'a':av,**exact_record(c.subs(L.SYMBOL,sp.Rational(*av.as_integer_ratio())))} for av in L.AS]})
  for precision in L.PRECISIONS:
   with mp.workdps(precision):
    gs,_=R.exact_frames()
    for r in parent['rows']:
     if r['precision']!=precision:continue
     if [f['frame'] for f in r['frames']]!=[0,1]:raise ValueError('parent frames')
     av=r['a'];arm=r['arm'];c=L.evaluate([polynomials[arm]],av)[0];sc=L.evaluate([source],av)[0]
     for f in r['frames']:
      frame=f['frame'];actual=R.decoded(f['origin_correlations'][5]);pred=c if frame==0 else gs[2]*c*gs[3].T;ref=sc if frame==0 else gs[2]*sc*gs[3].T
      error=F.norm(actual-pred);key='archive_native' if frame==0 else 'archive_transformed';metrics[key]=max(metrics[key],error)
      key=(candidate,av,arm,frame)
      if precision==50:old[key]=actual.copy()
      else:metrics['precision']=max(metrics['precision'],F.norm(actual-old.pop(key)))
      rec=domain(actual,ref,arm);group=(candidate,av,arm)
      if group in decisions:agree=agree and decisions[group]==rec['admitted']
      decisions[group]=rec['admitted']
      rows.append({'candidate':candidate,'a':av,'arm':arm,'precision':precision,'frame':frame,'matrix':R.encoded(actual),'source_matrix':R.encoded(ref),'archive_agreement':R.ns(error),**rec})
  print('Audited candidate',candidate,flush=True)
 valid=len(rows)==288 and len(exact)==24 and len(decisions)==72 and not old and agree and all(mp.isfinite(v) and v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()) and L.V.exact_tables()[1]
 return {'version':'16.06','all_valid':bool(valid),'verdict':verdict(valid,list(decisions.values())),'exact':exact,'rows':rows,'metrics':{k:R.ns(v) for k,v in metrics.items()},'domain_agreement':bool(agree),'exact_transfer_reconstruction':L.V.exact_tables()[1],'admitted_frame_cases':sum(r['admitted'] for r in rows),'frame_case_count':len(rows),'scope':'Frozen baseline domain only; no loop response defined outside domain.'}

if __name__=='__main__':
 try:result=audit()
 except Exception:
  result={'version':'16.06','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
 (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json']
 (HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
 print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
