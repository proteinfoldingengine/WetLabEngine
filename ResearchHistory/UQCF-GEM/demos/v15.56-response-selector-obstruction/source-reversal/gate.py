"""16.10 exact source reversal on frozen normalized physical paths."""
import pathlib,importlib.util,itertools,json,lzma,hashlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('boundary1609_reversal',HERE.parent/'boundary-polar-limits/gate.py');B=importlib.util.module_from_spec(q);q.loader.exec_module(B)
P=B.P;L=B.L;S=B.S;R=B.R;F=B.F
STEPS=[32,128,192]
def action(d,sign):
 if sign==1:return L.V.exact_action(d,'D',1)
 if sign==-1:return L.V.add({w:2*c for w,c in L.V.exact_action(d,'D',0).items()},L.V.exact_action(d,'D',1),-1)
 raise ValueError('source sign must be ±1')
def source_certificate():
 ps=[sp.eye(2),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)];basis={w:sp.kronecker_product(ps[w[0]],ps[w[1]]) for w in itertools.product(range(4),repeat=2)};checks=[]
 for sign in [-1,1]:
  u=(basis[3,0]+sign*basis[1,1])/sp.sqrt(2);checks.append(sp.simplify(u.H*u)==sp.eye(4))
  for w,h in basis.items():
   d=action({(0,0,*w):sp.Integer(1)},sign);recon=sum((c*basis[v[2:]] for v,c in d.items()),sp.zeros(4));checks.append((u*h*u.H-h-recon).applyfunc(sp.simplify)==sp.zeros(4))
 return {'valid':bool(all(checks)),'unitarity_checks':2,'direct_conjugation_columns':32,'source_weights':['1-s','s'],'s_interval':[0,1],'sites':list(L.V.SITES['D'])}
def paths(d,a,arm,sign):
 base=L.exact_middle(d,a);z=L.exact_prepare(base,arm)
 return z,{'after':L.exact_prepare(action(base,sign),arm),'before':L.exact_prepare(L.exact_middle(action(d,sign),a),arm)}
def reversal(plus,minus):return bool(plus!=sp.zeros(3) and minus==-plus)
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hashes mismatch')
 r=json.loads(lzma.decompress((HERE.parent/'boundary-polar-limits/result.json.xz').read_bytes()));expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.09' and r['all_valid'] and r['execution_head']=='b8bfa7cd3abf99884b6627ab2a42d0fa035154be' and len(r['exact'])==144 and {(x['candidate'],x['a'],x['arm'],x['order']) for x in r['exact']}==expected):raise ValueError('parent identity/completeness')
 return {(x['candidate'],x['a'],x['arm'],x['order']):x for x in r['exact']}
def audit():
 parent=load_parent();source=source_certificate();cert=P.channel_certificate()
 if not(source['valid'] and cert['valid']):raise ValueError('channel certificate')
 exact=[];rows=[];finite=[];cache={};densities=[];old={};metrics={k:mp.mpf(0) for k in ['polar','limit_identity','gap','covariance','precision','finite_polar','finite_covariance']}
 for candidate in L.CANDIDATES:
  raw,rho,_=L.load_inputs(candidate);dc=P.density_certificate(rho);d={w:c/dc['trace'] for w,c in raw.items()};densities.append({'candidate':candidate,'raw_trace':str(dc['trace']),'normalized_trace':str(dc['normalized_trace']),'positive':dc['valid']})
  if not(dc['valid'] and dc['normalized_trace']==1):raise ValueError('input certificate')
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    local={}
    for sign in [1,-1]:
     z,dirs=paths(d,a,arm,sign)
     for order,x in dirs.items():
      c,v,w,poly=P.connected_path(z,x);st=S.stratum(c,v)
      if not st['identities_valid']:raise ValueError('stratum identities')
      rc=B.rank_certificate(c,v,w,st['rank'],st['normal_rank']);local[sign,order]=(c,v,w,st,rc)
    for order in ['after','before']:
     key=candidate,av,arm,order;plus=local[1,order];minus=local[-1,order];p=parent[key]
     if any(x!=B.decode(p[k]) for x,k in zip(plus[:3],['C','V','quadratic'])) or plus[3]['normal']!=B.decode(p['normal']):raise ValueError('plus parent mismatch')
     if plus[0]!=minus[0] or plus[0]!=local[1,'after'][0]:raise ValueError('baseline mismatch')
     rev=reversal(plus[3]['normal'],minus[3]['normal']);cache[key]=(plus,minus,rev)
     exact.append({'candidate':candidate,'a':av,'arm':arm,'order':order,'C':S.encode(plus[0]),'rank':plus[3]['rank'],'reversal':rev,'plus':{'V':S.encode(plus[1]),'quadratic':S.encode(plus[2]),'normal':S.encode(plus[3]['normal']),'normal_rank':plus[3]['normal_rank'],'rank_certificate':plus[4]},'minus':{'V':S.encode(minus[1]),'quadratic':S.encode(minus[2]),'normal':S.encode(minus[3]['normal']),'normal_rank':minus[3]['normal_rank'],'rank_certificate':minus[4]},'predicted_gap_squared':4*plus[3]['normal_rank'] if rev else None})
    if av==1. and any(local[sign,'after'][:3]!=local[sign,'before'][:3] for sign in [1,-1]):raise ValueError('identity-order control')
  print('Exact candidate',candidate,flush=True)
 for precision in [80,120]:
  with mp.workdps(precision):
   gs,_=R.exact_frames()
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite residual')
    metrics[k]=max(metrics[k],x)
   for key,(plus,minus,rev) in cache.items():
    if not(plus[4]['certified'] and minus[4]['certified']):continue
    limits={}
    for frame in [0,1]:
     left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];out={}
     for name,data in [('plus',plus),('minus',minus)]:
      c,v,w,st,rc=data;cm=left*S.number_matrix(c)*right.T;nm=left*S.number_matrix(st['normal'])*right.T;uc=B.polar(cm,st['rank']);un=B.polar(nm,st['normal_rank']);b=uc+un
      mx('polar',max(B.polar_error(cm,uc),B.polar_error(nm,un)));mx('limit_identity',F.norm(b*b.T*b-b));limits[name,frame]=b.copy()
      if frame==1:mx('covariance',F.norm(b-gs[2]*limits[name,0]*gs[3].T))
      if precision==80:old[key,name,frame]=b.copy()
      else:mx('precision',F.norm(b-old.pop((key,name,frame))))
      out[name]=R.encoded(b)
     gap=F.norm(limits['plus',frame]-limits['minus',frame])
     if rev:mx('gap',abs(gap**2-4*plus[3]['normal_rank']))
     rows.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'precision':precision,'frame':frame,'limits':out,'gap':R.ns(gap),'gap_squared':R.ns(gap**2)})
    if precision==120:
     for name,data in [('plus',plus),('minus',minus)]:
      c,v,w,st,rc=data
      for step in STEPS:
       s=sp.Rational(1,2**step);ce=c+s*v+s*s*w;rank=int(ce.rank());cm=S.number_matrix(ce)
       for frame in [0,1]:
        left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cf=left*cm*right.T;u=B.polar(cf,rank);mx('finite_polar',B.polar_error(cf,u))
        if frame==0:native=u.copy()
        else:mx('finite_covariance',F.norm(u-gs[2]*native*gs[3].T))
        finite.append({'candidate':key[0],'a':key[1],'arm':key[2],'order':key[3],'source':name,'frame':frame,'step_power':step,'exact_rank':rank,'polar':R.encoded(u),'error_to_limit':R.ns(F.norm(u-limits[name,frame]))})
   print('Completed precision',precision,flush=True)
 count=sum(x['plus']['rank_certificate']['certified'] and x['minus']['rank_certificate']['certified'] for x in exact);valid=bool(len(exact)==144 and len(rows)==4*count and len(finite)==12*count and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 verdict='INVALID' if not valid else 'LIMIT_NOT_CERTIFIED' if count!=144 else 'SOURCE_DEPENDENT_BOUNDARY_LIMIT_CERTIFIED' if all(x['reversal'] for x in exact) else 'REVERSAL_NOT_UNIVERSAL'
 return {'version':'16.10','all_valid':valid,'verdict':verdict,'source_certificate':source,'density_certificates':densities,'exact':exact,'rows':rows,'finite':finite,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'scope':'Specified CPTP source reversal at a common normalized baseline; no universal source law.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.10','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
