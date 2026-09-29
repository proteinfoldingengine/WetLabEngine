"""16.15 independent reference-map and local-scalar interpretation gate."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('network1614_interpretation',HERE.parent/'closed-network-response/gate.py');A=importlib.util.module_from_spec(q);q.loader.exec_module(A)
B=A.B;S=A.S;L=A.L

def reference(c,cy,target=5):
 """Trace gradient from the complementary open chain (independent of basis differentiation)."""
 out=sp.zeros(3);e=A.EDGES[target]
 for k,i in enumerate(cy):
  j=cy[(k+1)%len(cy)]
  if (i,j)!=e and (j,i)!=e:continue
  rest=sp.eye(3)
  for offset in range(1,len(cy)):
   z=(k+offset)%len(cy);left=cy[z];right=cy[(z+1)%len(cy)]
   if (left,right) in A.EDGES:m=c[A.EDGES.index((left,right))]
   else:m=c[A.EDGES.index((right,left))].T
   rest=rest*m
  out+=rest.T if (i,j)==e else rest
 return out

def classify_references(hs,n):
 matrix=sp.Matrix([list(h) for h in hs]);rank=int(matrix.rank());response=[A.inner(h,n) for h in hs]
 return {'rank':rank,'classification':'STRUCTURAL_NORMAL_BLINDNESS' if rank==0 else 'DIRECTION_SPECIFIC_KERNEL' if all(x==0 for x in response) else 'NORMAL_COUPLED','response':response}
def projected_bounds(hs,n):
 nn=A.inner(n,n);hn=[A.inner(h,h) for h in hs];bounds=[x*nn for x in hn];responses=[A.inner(h,n)**2 for h in hs]
 return {'reference_norm_squared':hn,'bound_squared':bounds,'response_squared':responses,'valid':all(x<=y for x,y in zip(responses,bounds))}

def local_derivatives(c,v):
 gram=c.T*c;dg=c.T*v+v.T*c
 return [sp.expand(k*sp.trace(gram**(k-1)*dg)) for k in [1,2,3]]+[sp.expand(sum(c.cofactor(i,j)*v[i,j] for i in range(3) for j in range(3)))]
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hashes mismatch')
 binding=json.loads((HERE/'PARENT_BINDING.json').read_text());raw=(HERE.parent/'closed-network-response/result.json.xz').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=binding['result_xz_sha256']:raise ValueError('parent byte binding')
 r=json.loads(lzma.decompress(raw));expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.14' and r['all_valid'] is True and r['execution_head']==binding['execution_head'] and len(r['paths'])==144 and {A.key(x) for x in r['paths']}==expected and len(r['exact'])==1008 and len(r['pairs'])==504 and len(r['rows'])==12096):raise ValueError('parent identity/counts')
 return r

def audit():
 parent=load_parent();p13=json.loads(lzma.decompress((HERE.parent/'local-gauge-content/result.json.xz').read_bytes()));alpha={A.key(x):sp.Rational(x['alpha']) for x in p13['exact']};archived={(A.key(x),x['cycle']):x for x in parent['exact']};paths={A.key(x):x for x in parent['paths']};exact=[];local=[];pairs=[];loopchecks=[];cache={}
 for ky,x in paths.items():
  cs=list(map(B.decode,x['C']));vs=[list(map(B.decode,x[name])) for name in ['V0','V1']];n=B.decode(x['N']);p=B.decode(x['P']);q=B.decode(x['Q']);grads=[[reference(cs,cy,e) for e in range(6)] for cy in A.CYCLES];hs=[(sp.eye(3)-p)*g[5]*(sp.eye(3)-q) for g in grads];classification=classify_references(hs,n);bounds=projected_bounds(hs,n);totals=[]
  if not bounds['valid']:raise ValueError('exact Cauchy bound')
  for ci,gg in enumerate(grads):
   ar=archived[ky,ci];h=hs[ci];total=[sum(A.inner(g,v) for g,v in zip(gg,vv)) for vv in vs];normal=A.inner(h,n);six=[A.inner(gg[5],vv[5]) for vv in vs];tang=[six[0],six[1]-normal];other=[total[i]-six[i] for i in [0,1]]
   if gg[5]!=B.decode(ar['gradient']) or h!=B.decode(ar['normal_reference']) or normal!=sp.Rational(ar['normal'][1]):raise ValueError('reference mismatch')
   for name,value in [('total',total),('sixth_tangent',tang),('other_edges',other)]:
    if list(map(sp.Rational,ar[name]))!=value:raise ValueError('independent derivative mismatch '+name)
   totals.append(total)
  scalars=[[local_derivatives(c,v) for c,v in zip(cs,vv)] for vv in vs];ns=local_derivatives(cs[5],n)
  if ns[:3]!=[0,0,0] or ns[3]!=alpha[ky]:raise ValueError('normal scalar/cofactor mismatch')
  if classification['rank']>int((sp.eye(3)-p).rank()*(sp.eye(3)-q).rank()):raise ValueError('normal map rank dimension')
  exact.append({'candidate':ky[0],'a':ky[1],'arm':ky[2],'order':ky[3],'projected_bounds':{k:[str(t) for t in v] if isinstance(v,list) else v for k,v in bounds.items()},'normal_reference_rank':classification['rank'],'normal_dimension':int((sp.eye(3)-p).rank()*(sp.eye(3)-q).rank()),'classification':classification['classification'],'normal_responses':[str(t) for t in classification['response']],'normal_references':[S.encode(h) for h in hs],'normal_local_scalar_derivatives':[str(t) for t in ns],'normal_norm_squared':str(A.inner(n,n))})
  cache[ky]=(cs,vs,n,scalars,totals,classification)
 for candidate in L.CANDIDATES:
  for av in L.AS:
   for arm in L.ARMS:
    aft=cache[candidate,av,arm,'after'];bef=cache[candidate,av,arm,'before'];ident={'candidate':candidate,'a':av,'arm':arm};anylocal=False;oddlocal=False;zerolocal=False
    for e in range(6):
     for k,name in enumerate(['gram1','gram2','gram3','determinant']):
      delta=[aft[3][i][e][k]-bef[3][i][e][k] for i in [0,1]];nz=any(v!=0 for v in delta);anylocal|=nz;oddlocal|=delta[1]!=0;zerolocal|=delta[0]!=0
      local.append({**ident,'edge':e,'observable':name,'after':[str(aft[3][i][e][k]) for i in [0,1]],'before':[str(bef[3][i][e][k]) for i in [0,1]],'contrast':[str(t) for t in delta],'nonzero':nz})
    totals=[[x-y for x,y in zip(aa,bb)] for aa,bb in zip(aft[4],bef[4])];normal=[x-y for x,y in zip(aft[5]['response'],bef[5]['response'])];network=any(t!=0 for row in totals for t in row);normalcoupled=any(t!=0 for t in normal);energy=A.inner(aft[2],aft[2])-A.inner(bef[2],bef[2]);localamp=energy!=0
    if av==1. and (network or anylocal or normalcoupled or localamp):raise ValueError('identity-middle mismatch')
    for ci,(tot,norm) in enumerate(zip(totals,normal)):loopchecks.append({**ident,'cycle':ci,'total':[str(t) for t in tot],'normal':['0',str(norm)]})
    pairs.append({**ident,'local_scalar_distinguishes':bool(anylocal),'local_odd_coefficient_nonzero':bool(oddlocal),'local_zero_coherence_nonzero':bool(zerolocal),'network_distinguishes':bool(network),'network_normal_contribution':bool(normalcoupled),'normal_amplitude_distinguishes':bool(localamp),'normal_energy_contrast':str(energy),'first_order_network_beyond_chosen_local_scalars':bool(network and not anylocal),'claim':'BOTH_DISTINGUISH_NO_ADDITIONALITY_PROOF' if network and anylocal else 'NETWORK_FIRST_ORDER_SEPARATION_FROM_CHOSEN_LOCAL_SCALARS' if network else 'CHOSEN_NETWORK_FIRST_ORDER_NULL'})
 old={(x['candidate'],x['a'],x['arm'],x['cycle']):x for x in parent['pairs']}
 for x in loopchecks:
  y=old[x['candidate'],x['a'],x['arm'],x['cycle']]
  if x['total']!=y['total'] or x['normal']!=y['normal']:raise ValueError('independent order contrast mismatch')
 valid=bool(len(exact)==144 and len(local)==1728 and len(pairs)==72 and len(loopchecks)==504)
 verdict='NORMAL_REFERENCE_STRUCTURAL_OBSTRUCTION' if all(x['classification']=='STRUCTURAL_NORMAL_BLINDNESS' for x in exact) else 'ACTUAL_NORMAL_IN_REFERENCE_KERNEL' if all(x['classification']!='NORMAL_COUPLED' for x in exact) else 'NETWORK_NORMAL_COUPLING_CLASSIFIED'
 return {'version':'16.15','all_valid':valid,'verdict':verdict if valid else 'INVALID','exact':exact,'local_scalars':local,'pairs':pairs,'independent_loop_checks':loopchecks,'metrics':{},'physical_interpretation':'Conditional response of an explicitly specified CPTP source and connected-correlation readout. No emergent source law, transport, curvature, gravity, or preferred geometry follows. Only specified first-order local scalar family compared; amplitudes remain distinct information.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.15','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','PARENT_BINDING.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
