"""v15.67 locate first float64 vs v15.66 high-precision semantic mismatch."""
import importlib.util,json,pathlib,numpy as np,mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V64=load(PARENT/'source-vector-field-null'/'gate.py','v64audit')
V66=load(PARENT/'polar-derivative-numerics'/'gate.py','v66audit')
CANDIDATE=13;T=1e-3;ETA=1e-4;mp.mp.dps=80

def frozen():
 row=[x for x in V64.ASYM.select_states() if x['candidate_index']==CANDIDATE][0]
 rho=row['rho'];Y,_=V64.target_Y(rho)
 sig=rho+ETA*V64.HIDDEN
 z64=V64.T(sig,rho,Y,T)
 # Reproduce v15.66's actual conversion path exactly: real parts only.
 zmp=V66.mp_state(rho)+mp.mpf(str(ETA))*V66.mp_state(V64.HIDDEN)+mp.mpf(str(T*ETA))*V66.mp_state(Y)
 return rho,Y,z64,zmp

def mp_to_complex(A):
 # v15.66 matrices are real mp matrices by construction.
 return np.array([[complex(float(A[i,j]),0.0) for j in range(A.cols)] for i in range(A.rows)])

def moments64(z):
 one=[];two=[]
 for q in range(3):
  for a in range(1,4):
   ids=[0,0,0];ids[q]=a;one.append(float(np.trace(z@V64.ASYM.F.op(*ids)).real))
 for e,(i,j) in enumerate(V64.ASYM.EDGES):
  for a in range(1,4):
   for b in range(1,4):
    ids=[0,0,0];ids[i]=a;ids[j]=b;two.append(float(np.trace(z@V64.ASYM.F.op(*ids)).real))
 return np.array(one),np.array(two)

def moments_mp(z):
 one=[];two=[]
 for q in range(3):
  for a in range(1,4):
   ids=[0,0,0];ids[q]=a;op=V66.mpmat(V64.ASYM.F.op(*ids))
   val=mp.fsum([z[r,k]*op[k,r] for r in range(8) for k in range(8)]);one.append(float(val))
 for e,(i,j) in enumerate(V64.ASYM.EDGES):
  for a in range(1,4):
   for b in range(1,4):
    ids=[0,0,0];ids[i]=a;ids[j]=b;op=V66.mpmat(V64.ASYM.F.op(*ids))
    val=mp.fsum([z[r,k]*op[k,r] for r in range(8) for k in range(8)]);two.append(float(val))
 return np.array(one),np.array(two)

def corr_from_moments(one,two):
 Cs=[];k=0
 for e,(i,j) in enumerate(V64.ASYM.EDGES):
  C=np.zeros((3,3))
  for a in range(3):
   for b in range(3):
    C[a,b]=two[k]-one[i*3+a]*one[j*3+b];k+=1
  Cs.append(C)
 return Cs

def pol64(C):
 u,s,vh=np.linalg.svd(C);O=u@vh
 if np.linalg.det(O)<0:u[:,-1]*=-1;O=u@vh
 return O

def mp_polar_from_float_C(C):
 M=mp.matrix([[mp.mpf(str(float(C[i,j]))) for j in range(3)] for i in range(3)])
 return np.array(V66.mp_polar(M).tolist(),dtype=float)

def audit():
 rho,Y,z64,zmp=frozen();zmp64=mp_to_complex(zmp)
 state_diff=float(np.max(np.abs(z64-zmp64)))
 state_imag=float(np.max(np.abs(z64.imag)))
 trace64=complex(np.trace(z64));tracemp=float(mp.fsum([zmp[i,i] for i in range(zmp.rows)]))
 eigmin=float(np.linalg.eigvalsh(z64).min())
 o64,t64=moments64(z64);omp,tmp=moments_mp(zmp)
 one_diff=float(np.max(np.abs(o64-omp)));two_diff=float(np.max(np.abs(t64-tmp)))
 C64=corr_from_moments(o64,t64);Cmp=corr_from_moments(omp,tmp)
 corr_diff=max(float(np.max(np.abs(a-b))) for a,b in zip(C64,Cmp))
 gram_rel=[];polar_diff=[];pol_diag=[]
 for a,b in zip(C64,Cmp):
  Ga=a.T@a;Gb=b.T@b;ea=np.linalg.eigvalsh(Ga);eb=np.linalg.eigvalsh(Gb)
  gram_rel.append(float(np.max(np.abs(ea-eb)/np.maximum(np.abs(ea),1e-300))))
  Oa=pol64(a);Ob=mp_polar_from_float_C(b);polar_diff.append(float(np.linalg.norm(Oa-Ob)))
  pol_diag.append({'det_float':float(np.linalg.det(Oa)),'det_mp':float(np.linalg.det(Ob)),'orth_float':float(np.linalg.norm(Oa.T@Oa-np.eye(3))),'orth_mp':float(np.linalg.norm(Ob.T@Ob-np.eye(3)))})
 if state_diff>1e-13:verdict='STATE_MISMATCH'
 elif max(one_diff,two_diff)>1e-13:verdict='MOMENT_MISMATCH'
 elif corr_diff>1e-13:verdict='CORRELATION_MISMATCH'
 elif max(gram_rel)>1e-12:verdict='GRAM_MISMATCH'
 elif max(polar_diff)>1e-11:verdict='POLAR_MISMATCH'
 else:verdict='PATHS_IDENTICAL_AT_FROZEN_CORNER'
 return {'verdict':verdict,'candidate_index':CANDIDATE,'eta':ETA,'t':T,'state_max_abs_diff':state_diff,'float_state_max_imag':state_imag,'trace_float_real':float(trace64.real),'trace_float_imag':float(trace64.imag),'trace_mp':tracemp,'float_min_eigenvalue':eigmin,'one_body_max_abs_diff':one_diff,'two_body_max_abs_diff':two_diff,'correlation_max_abs_diff':corr_diff,'gram_eigen_relative_diffs':gram_rel,'polar_frobenius_diffs':polar_diff,'polar_diagnostics':pol_diag}

if __name__=='__main__':
 try:
  r=audit();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0)
 except Exception as e:
  print(json.dumps({'verdict':'INVALID','error':repr(e)}));raise SystemExit(2)
