"""16.13 local normal-sign orbits under proper endpoint frames."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback,itertools
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('response1612_gauge',HERE.parent/'continuous-response/gate.py');A=importlib.util.module_from_spec(q);q.loader.exec_module(A)
S=A.S;B=A.B;L=A.L;R=A.R;F=A.F;LAM=A.LAM;PARAM=sp.Symbol('t',real=True)
def cofactor_pair(c,n):return sp.expand(sp.trace(c.cofactor_matrix().T*n))
def first_two(c,v,w):
 first=cofactor_pair(c,v);second=sp.Integer(0)
 for j in range(3):
  m=c.copy();m[:,j]=w[:,j];second+=m.det()
 for i,j in itertools.combinations(range(3),2):
  m=c.copy();m[:,i]=v[:,i];m[:,j]=v[:,j];second+=m.det()
 return [sp.expand(first),sp.expand(second)]
def classify_pair(c,n):
 p=c*c.pinv();j=2*p-sp.eye(3);poly=sp.expand((c+PARAM*n).det());coeff=[poly.coeff(PARAM,i) for i in range(4)];flip=j.T*j==sp.eye(3) and j*c==c and j*n==-n;proper=flip and j.det()==1 and n!=sp.zeros(3);odd=coeff[1]!=0 or coeff[3]!=0
 classification='SO_SIGN_EQUIVALENT' if proper else 'SO_SIGN_DISTINGUISHED' if odd else 'INCOMPLETE'
 return {'P':p,'J':j,'J_det':j.det(),'flip_valid':bool(flip),'proper_flip':bool(proper),'coefficients':coeff,'alpha':coeff[1],'beta':coeff[2],'classification':classification}
def cofactor_numeric(m):
 out=mp.zeros(3)
 for i in range(3):
  for j in range(3):
   rr=[k for k in range(3) if k!=i];cc=[k for k in range(3) if k!=j];out[i,j]=(-1)**(i+j)*(m[rr[0],cc[0]]*m[rr[1],cc[1]]-m[rr[0],cc[1]]*m[rr[1],cc[0]])
 return out
def inner(a,b):return sum(a[i,j]*b[i,j] for i in range(3) for j in range(3))
def load_parent():
 manifest=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
 if not L.A.verify_files(HERE.parent,manifest):raise ValueError('source hash mismatch')
 r=json.loads(lzma.decompress((HERE.parent/'continuous-response/result.json.xz').read_bytes()));expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.12' and r['all_valid'] is True and r['execution_head']=='88109eeb3e7f60f73f433f5e0ed33938c943e205' and len(r['exact'])==144 and {key(x) for x in r['exact']}==expected):raise ValueError('parent identity/completeness')
 return r
def key(x):return x['candidate'],x['a'],x['arm'],x['order']
def audit():
 parent=load_parent();exact=[];pairs=[];rows=[];cache={};old={};metrics={k:mp.mpf(0) for k in ['stabilizer','frames','cofactor','determinant','amplitude','invariance','spectral_identity','cauchy_bound','precision']}
 for x in parent['exact']:
  c=B.decode(x['C']);n=B.decode(x['normal']);p=B.decode(x['left_projector']);q=B.decode(x['right_projector']);r=int(c.rank());k=int(n.rank());cl=classify_pair(c,n)
  if cl['P']!=p or (sp.eye(3)-p)*n*(sp.eye(3)-q)!=n or k!=x['normal_rank'] or not cl['flip_valid']:raise ValueError('parent normal/projector control')
  vc=list(map(B.decode,x['V_coefficients']));wc=list(map(B.decode,x['W_coefficients']));v=vc[0]+LAM*vc[1];w=sum((LAM**i*m for i,m in enumerate(wc)),sp.zeros(3));d1,d2=first_two(c,v,w);physical_first=sp.expand(d1-LAM*cl['alpha'])==0;physical_second=(sp.expand(d2-LAM**2*cl['beta'])==0) if r==1 else None
  cf=c.cofactor_matrix();norm2=sp.trace(n.T*n);cache[key(x)]=(c,n,cl,cf,norm2)
  exact.append({**{z:x[z] for z in ['candidate','a','arm','order']},'C':S.encode(c),'N':S.encode(n),'rank':r,'normal_rank':k,'P':S.encode(p),'J':S.encode(cl['J']),'J_determinant':str(cl['J_det']),'proper_flip':cl['proper_flip'],'classification':cl['classification'],'determinant_coefficients':[str(z) for z in cl['coefficients']],'cofactor':S.encode(cf),'alpha':str(cl['alpha']),'beta':str(cl['beta']),'normal_norm_squared':str(norm2),'cofactor_norm_squared':str(sp.trace(cf.T*cf)),'physical_determinant_s_coefficients':[str(d1),str(d2)],'physical_first_matches':bool(physical_first),'physical_second_matches_rank1':physical_second,'O_sign_equivalent':True})
 for candidate in L.CANDIDATES:
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    aft=cache[candidate,av,arm,'after'];bef=cache[candidate,av,arm,'before']
    if aft[0]!=bef[0]:raise ValueError('order baseline mismatch')
    pairs.append({'candidate':candidate,'a':av,'arm':arm,'normal_scaling':bool(bef[1]==a*aft[1]),'energy_scaling':bool(bef[4]==a*a*aft[4]),'after_energy':str(aft[4]),'before_energy':str(bef[4]),'energy_difference':str(aft[4]-bef[4]),'energy_distinguishes_order':bool(aft[4]!=bef[4]),'expected_distinction':av!=1.,'orientation_after':str(aft[2]['alpha']),'orientation_before':str(bef[2]['alpha'])})
 print('Completed exact gauge and physical-coefficient audit',flush=True)
 for precision in [80,120]:
  with mp.workdps(precision):
   gs,_=R.exact_frames()
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite control '+k)
    metrics[k]=max(metrics[k],x)
   det=A.A.det3
   for g in [gs[2],gs[3]]:mx('frames',max(F.norm(g.T*g-mp.eye(3)),abs(det(g)-1)))
   for ky,(c,n,cl,cof,norm2) in cache.items():
    cm=S.number_matrix(c);nm=S.number_matrix(n);jm=S.number_matrix(cl['J']);cfm=S.number_matrix(cof);coef=[L.numeric(z) for z in cl['coefficients']]
    for frame in [0,1]:
     left=mp.eye(3) if frame==0 else gs[2];right=mp.eye(3) if frame==0 else gs[3];cc=left*cm*right.T;nn=left*nm*right.T;jj=left*jm*left.T;cf=cofactor_numeric(cc);alpha=inner(cf,nn);cn=F.norm(cc);nnorm=F.norm(nn);cfn=F.norm(cf);sv=mp.svd_r(cc,compute_uv=False)
     mx('stabilizer',max(F.norm(jj.T*jj-mp.eye(3)),F.norm(jj*cc-cc),F.norm(jj*nn+nn),abs(det(jj)-L.numeric(cl['J_det']))));mx('cofactor',F.norm(cf-left*cfm*right.T));mx('determinant',max(abs(alpha-coef[1]),abs(det(cc+nn)-sum(coef)),abs(det(cc-nn)-sum((-1)**i*coef[i] for i in range(4)))));mx('amplitude',abs(nnorm**2-L.numeric(norm2)));mx('spectral_identity',abs(cfn-sv[0]*sv[1]));mx('cauchy_bound',max(mp.mpf(0),abs(alpha)-cfn*nnorm))
     normalized=abs(alpha)/(cn*cn*nnorm);ratio=sv[1]/sv[0];vals=[alpha,nnorm,cn,cfn,normalized,ratio]
     if frame==0:native=vals.copy()
     else:mx('invariance',max(abs(a-b) for a,b in zip(vals,native)))
     pk=ky,frame
     if precision==80:old[pk]=vals.copy()
     else:mx('precision',max(abs(a-b) for a,b in zip(vals,old.pop(pk))))
     rows.append({'candidate':ky[0],'a':ky[1],'arm':ky[2],'order':ky[3],'precision':precision,'frame':frame,'classification':cl['classification'],'C':R.encoded(cc),'N':R.encoded(nn),'J':R.encoded(jj),'alpha':R.ns(alpha),'normal_norm':R.ns(nnorm),'C_norm':R.ns(cn),'cofactor_norm':R.ns(cfn),'orientation_bound':R.ns(cfn*nnorm),'normalized_orientation_response':R.ns(normalized),'singular_values':[R.ns(z) for z in sv],'sigma2_over_sigma1':R.ns(ratio)})
   print('Completed precision',precision,flush=True)
 valid=bool(len(exact)==144 and len(pairs)==72 and len(rows)==576 and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()));scientific=all(x['classification']!='INCOMPLETE' and x['physical_first_matches'] and x['physical_second_matches_rank1'] is not False for x in exact) and all(x['normal_scaling'] and x['energy_scaling'] and x['energy_distinguishes_order']==x['expected_distinction'] for x in pairs)
 return {'version':'16.13','all_valid':valid,'verdict':'INVALID' if not valid else 'LOCAL_NORMAL_SIGN_GAUGE_CLASSIFIED' if scientific else 'GAUGE_SIGN_CLASSIFICATION_INCOMPLETE','exact':exact,'pairs':pairs,'rows':rows,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'gauge':'SO(3) x SO(3); O(3) reported separately','scope':'Sign orbit of local baseline-normal pair, not full source paths or a network invariant. Rank-two orientation witness collapses at rank-one boundary.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.13','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
