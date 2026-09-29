"""16.14 complete simple-cycle response; no polar extension or selected loop."""
import pathlib,importlib.util,json,lzma,hashlib,subprocess,sys,traceback
import sympy as sp
import mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
q=importlib.util.spec_from_file_location('gauge1613_network',HERE.parent/'local-gauge-content/gate.py');A=importlib.util.module_from_spec(q);q.loader.exec_module(A)
S=A.S;B=A.B;L=A.L;R=A.R;F=A.F;T=A.A.A;LAM=A.LAM
EDGES=[(0,1),(1,2),(2,0),(1,3),(3,0),(2,3)]
CYCLES=[(0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,2,3),(0,1,3,2),(0,2,1,3)]
def expand(m):return m.applyfunc(sp.expand)
def inner(a,b):return sum(a[i,j]*b[i,j] for i in range(3) for j in range(3))
def edge(mats,i,j):
 if (i,j) in EDGES:return mats[EDGES.index((i,j))]
 return mats[EDGES.index((j,i))].T
def product(ms):
 out=ms[0]
 for m in ms[1:]:out=out*m
 return out

def trace(m):return sum(m[i,i] for i in range(3))
def cycle_trace(mats,cy):return trace(product([edge(mats,i,cy[(k+1)%len(cy)]) for k,i in enumerate(cy)]))
def cycle_derivative(c,v,cy):
 out=0
 for k in range(len(cy)):
  out+=trace(product([edge(v if j==k else c,i,cy[(j+1)%len(cy)]) for j,i in enumerate(cy)]))
 return out

def gradient(c,cy,target=5):
 out=sp.zeros(3)
 for i in range(3):
  for j in range(3):
   v=[sp.zeros(3) for _ in EDGES];v[target][i,j]=1;out[i,j]=cycle_derivative(c,v,cy)
 return out

def connected_edges(d):
 def mom(items):
  w=[0]*4
  for i,j in items:w[i]=j
  return 4*d.get(tuple(w),0)
 return [sp.Matrix(3,3,lambda a,b:sp.expand(mom([(i,a+1),(j,b+1)])-mom([(i,a+1)])*mom([(j,b+1)]))) for i,j in EDGES]
def key(x):return x['candidate'],x['a'],x['arm'],x['order']
def load_parent():
 if not L.A.verify_files(HERE.parent,json.loads((HERE/'SOURCE_MANIFEST.json').read_text())):raise ValueError('source hashes mismatch')
 r=json.loads(lzma.decompress((HERE.parent/'local-gauge-content/result.json.xz').read_bytes()))
 expected={(c,a,arm,o) for c in L.CANDIDATES for a in L.AS for arm in L.ARMS for o in ['after','before']}
 if not(r['version']=='16.13' and r['all_valid'] is True and r['execution_head']=='1a9d5d80f80385af2ba1771cadd21c5a4f8f976b' and len(r['exact'])==144 and {key(x) for x in r['exact']}==expected):raise ValueError('parent identity/completeness')
 r12=A.load_parent()
 return {key(x):x for x in r['exact']},{key(x):x for x in r12['exact']},r12

def normal_bound(g,p,q,n):return F.norm((mp.eye(3)-p)*g*(mp.eye(3)-q))*F.norm(n)

def coefficients(x):return [sp.expand(x).coeff(LAM,i) for i in [0,1]]
def audit():
 parent,p12,physical=load_parent();paths=[];exact=[];pairs=[];rows=[];cache={};loopcache={};old={};metrics={k:mp.mpf(0) for k in ['exact_numeric','frame','moving_frame','bound','precision']}
 for candidate in L.CANDIDATES:
  raw,rho,_=L.load_inputs(candidate);dc=T.P.density_certificate(rho);d={w:c/dc['trace'] for w,c in raw.items()}
  for av in L.AS:
   a=sp.Rational(*av.as_integer_ratio())
   for arm in L.ARMS:
    z,dirs=T.paths(d,a,arm,LAM);cs=connected_edges(z);grads=[gradient(cs,cy) for cy in CYCLES]
    for order,x in dirs.items():
     ky=candidate,av,arm,order;pp=p12[ky];vs=L.exact_connected(z,x);v0=[expand(v.subs(LAM,0)) for v in vs];v1=[expand(v).applyfunc(lambda e:e.coeff(LAM,1)) for v in vs]
     if any(expand(v-vv-LAM*ww)!=sp.zeros(3) for v,vv,ww in zip(vs,v0,v1)):raise ValueError('derivative degree')
     n=B.decode(pp['normal']);p=B.decode(pp['left_projector']);qr=B.decode(pp['right_projector'])
     if cs[5]!=B.decode(pp['C']) or [v0[5],v1[5]]!=list(map(B.decode,pp['V_coefficients'])):raise ValueError('sixth-edge parent mismatch')
     if expand((sp.eye(3)-p)*vs[5]*(sp.eye(3)-qr))!=LAM*n:raise ValueError('normal identity')
     cache[ky]=(cs,v0,v1,n,grads)
     paths.append({'candidate':candidate,'a':av,'arm':arm,'order':order,'C':[S.encode(m) for m in cs],'V0':[S.encode(m) for m in v0],'V1':[S.encode(m) for m in v1],'N':S.encode(n),'P':S.encode(p),'Q':S.encode(qr),'normal_rank':int(n.rank()),'baseline_rank':int(cs[5].rank())})
     for ci,cy in enumerate(CYCLES):
      g=grads[ci];h=(sp.eye(3)-p)*g*(sp.eye(3)-qr);normal=inner(g,n);tot=coefficients(cycle_derivative(cs,vs,cy));six=coefficients(inner(g,vs[5]));tang=[six[0],six[1]-normal];other=[tot[k]-six[k] for k in [0,1]]
      if inner(h,n)!=normal:raise ValueError('projected reference mismatch')
      if sp.expand(cycle_derivative(cs,vs,tuple(reversed(cy)))-sum(LAM**k*v for k,v in enumerate(tot)))!=0:raise ValueError('reversal mismatch')
      row={'candidate':candidate,'a':av,'arm':arm,'order':order,'cycle':ci,'vertices':list(cy),'baseline':str(cycle_trace(cs,cy)),'total':[str(t) for t in tot],'normal':['0',str(normal)],'sixth_tangent':[str(t) for t in tang],'other_edges':[str(t) for t in other],'gradient':S.encode(g),'normal_reference':S.encode(h),'normal_reference_norm_squared':str(inner(h,h)),'normal_norm_squared':str(inner(n,n))}
      exact.append(row);loopcache[ky,ci]=(tot,[sp.Integer(0),normal],tang,other)
  print('Exact network candidate',candidate,flush=True)
 for candidate in L.CANDIDATES:
  for av in L.AS:
   for arm in L.ARMS:
    aft=cache[candidate,av,arm,'after'];bef=cache[candidate,av,arm,'before']
    if aft[0]!=bef[0]:raise ValueError('baseline mismatch')
    if av==1. and aft[1:3]!=bef[1:3]:raise ValueError('identity-middle mismatch')
    for ci in range(7):
     aa=loopcache[(candidate,av,arm,'after'),ci];bb=loopcache[(candidate,av,arm,'before'),ci];delta=[[sp.expand(x-y) for x,y in zip(u,v)] for u,v in zip(aa,bb)]
     if any(sp.expand(delta[0][i]-sum(delta[k][i] for k in [1,2,3]))!=0 for i in [0,1]):raise ValueError('decomposition mismatch')
     pairs.append({'candidate':candidate,'a':av,'arm':arm,'cycle':ci,**{k:[str(v) for v in vals] for k,vals in zip(['total','normal','sixth_tangent','other_edges'],delta)},'total_nonzero':any(x!=0 for x in delta[0]),'normal_nonzero':delta[1][1]!=0,'zero_coherence_total_nonzero':delta[0][0]!=0,'total_odd':delta[0][0]==0,'normal_odd':delta[1][0]==0})
 for precision in [80,120]:
  with mp.workdps(precision):
   gs,_=R.exact_frames();ks=[mp.matrix([[0,-i-1,2],[i+1,0,-3],[-2,3,0]]) for i in range(4)]
   def mx(k,x):
    if not mp.isfinite(x):raise ValueError('nonfinite '+k)
    metrics[k]=max(metrics[k],x)
   for ky,(cs,v0,v1,n,grads) in cache.items():
    cn=list(map(S.number_matrix,cs));v0n=list(map(S.number_matrix,v0));v1n=list(map(S.number_matrix,v1));nn=S.number_matrix(n);gn=list(map(S.number_matrix,grads));pm=S.number_matrix(B.decode(p12[ky]['left_projector']));qm=S.number_matrix(B.decode(p12[ky]['right_projector']))
    for lam in [-1,0,1]:
     vn=[x+lam*y for x,y in zip(v0n,v1n)];nv=[mp.zeros(3) for _ in EDGES];nv[5]=lam*nn
     for frame in [0,1]:
      ff=[mp.eye(3) for _ in range(4)] if frame==0 else gs
      cc=[ff[i]*m*ff[j].T for m,(i,j) in zip(cn,EDGES)];vv=[ff[i]*m*ff[j].T for m,(i,j) in zip(vn,EDGES)];nf=[ff[i]*m*ff[j].T for m,(i,j) in zip(nv,EDGES)];moving=[ff[i]*(m+ks[i]*b-b*ks[j])*ff[j].T for m,b,(i,j) in zip(vn,cn,EDGES)]
      for ci,cy in enumerate(CYCLES):
       total=cycle_derivative(cc,vv,cy);normal=cycle_derivative(cc,nf,cy);baseline=cycle_trace(cc,cy);target=loopcache[ky,ci];values=[baseline,total,normal];expected=[L.numeric(cycle_trace(cs,cy)),L.numeric(target[0][0]+lam*target[0][1]),L.numeric(lam*target[1][1])]
       mx('exact_numeric',max(abs(x-y) for x,y in zip(values,expected)));mx('moving_frame',abs(cycle_derivative(cc,moving,cy)-total));mx('bound',max(mp.mpf(0),abs(normal)-normal_bound(gn[ci],pm,qm,lam*nn)))
       pk=ky,lam,ci,frame
       if precision==80:old[pk]=values.copy()
       else:mx('precision',max(abs(x-y) for x,y in zip(values,old.pop(pk))))
       if frame==0:pass
       else:mx('frame',max(abs(x-y) for x,y in zip(values,expected)))
       rows.append({'candidate':ky[0],'a':ky[1],'arm':ky[2],'order':ky[3],'lambda':lam,'cycle':ci,'precision':precision,'frame':frame,'baseline':R.ns(baseline),'total':R.ns(total),'normal':R.ns(normal)})
   print('Completed numeric precision',precision,flush=True)
 valid=bool(len(paths)==144 and len(exact)==1008 and len(pairs)==504 and len(rows)==12096 and not old and all(v<=mp.mpf('1e-30' if k=='precision' else '1e-35') for k,v in metrics.items()))
 verdict='CLOSED_NETWORK_NORMAL_RESPONSE' if any(x['normal_nonzero'] for x in pairs if x['a']!=1.) else 'NETWORK_RESPONSE_WITHOUT_NORMAL' if any(x['total_nonzero'] for x in pairs) else 'CLOSED_NETWORK_FIRST_ORDER_NULL'
 return {'version':'16.14','all_valid':valid,'verdict':verdict if valid else 'INVALID','paths':paths,'exact':exact,'pairs':pairs,'rows':rows,'metrics':{k:mp.nstr(v,60) for k,v in metrics.items()},'source_certificate':physical['source_certificate'],'density_certificates':physical['density_certificates'],'scope':'First derivatives of all seven simple-cycle traces in the frozen six-edge model; no universal invariant or physical geometry claim.'}
if __name__=='__main__':
 try:result=audit()
 except Exception:result={'version':'16.14','all_valid':False,'verdict':'INVALID','error':traceback.format_exc()}
 result['execution_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();(HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');names=['PREREGISTRATION.md','SOURCE_MANIFEST.json','gate.py','test_gate.py','result.json'];(HERE/'SHA256SUMS').write_text(''.join(hashlib.sha256((HERE/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names));print(json.dumps({k:result[k] for k in ['all_valid','verdict']}));sys.exit(0 if result['all_valid'] else 2)
