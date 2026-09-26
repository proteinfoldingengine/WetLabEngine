"""v15.66 analytic vs float64 vs 80-digit polar derivative adjudication."""
import importlib.util,json,pathlib,numpy as np,mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V64=load(PARENT/'source-vector-field-null'/'gate.py','v64num')
MP_DPS=80;FLOAT_TS=[1e-2,3e-3,1e-3,3e-4,1e-4,3e-5];MP_TS=[1e-3,3e-4,1e-4,3e-5]
mp.mp.dps=MP_DPS
def analytic(rho,Y):
 A1,Ap=V64.GL.derivative_maps(rho);y=np.array([np.trace(B@Y).real for B in V64.GL.BASIS]);O=V64.GL.rotations(rho);qs=[]
 for e in range(3):
  d=(Ap[e*9:(e+1)*9]@y).reshape(3,3);qs.append(float(np.linalg.norm(O[e].T@d-d.T@O[e])))
 return max(qs)
def float_measure(rho,Y,t):
 ro={};num=None
 for ie in (-1,1):
  sig=rho+ie*V64.ETA*V64.HIDDEN
  for jt in (-1,1):ro[(ie,jt)]=V64.rotations(V64.T(sig,rho,Y,jt*t))
 num=ro[(1,1)]-ro[(1,-1)]-ro[(-1,1)]+ro[(-1,-1)]
 return float(np.linalg.norm(num)),float(np.linalg.norm(num)/(4*V64.ETA*t))
def mpmat(A):return mp.matrix([[mp.mpf(str(float(A[i,j].real))) for j in range(A.shape[1])] for i in range(A.shape[0])])
def mp_polar(C):
 # symmetric eigendecomposition of C^T C
 G=C.T*C
 vals,Q=mp.eigsy(G)
 D=mp.diag([1/mp.sqrt(vals[i]) for i in range(3)])
 return C*Q*D*Q.T
def mp_corr(rho,e):
 i,j=V64.ASYM.EDGES[e];C=mp.matrix(3,3)
 # convert via exact observable traces evaluated at mp state
 for a in range(1,4):
  for b in range(1,4):
   ids=[0,0,0];ids[i]=a;ids[j]=b;op=mpmat(V64.ASYM.F.op(*ids))
   ei=mp.fsum([rho[r,k]*op[k,r] for r in range(8) for k in range(8)])
   ids1=[0,0,0];ids1[i]=a;o1=mpmat(V64.ASYM.F.op(*ids1));mi=mp.fsum([rho[r,k]*o1[k,r] for r in range(8) for k in range(8)])
   ids2=[0,0,0];ids2[j]=b;o2=mpmat(V64.ASYM.F.op(*ids2));mj=mp.fsum([rho[r,k]*o2[k,r] for r in range(8) for k in range(8)])
   C[a-1,b-1]=ei-mi*mj
 return C
def mp_state(A):return mpmat(A)
def mp_measure(rho_np,Y_np,t):
 rho=mp_state(rho_np);Y=mp_state(Y_np);h=mp_state(V64.HIDDEN);eta=mp.mpf(str(V64.ETA));tt=mp.mpf(str(t));ro={}
 # alpha(rho +/- eta h)= +/- eta because h HS-normalized.
 for ie in (-1,1):
  sig=rho+ie*eta*h
  for jt in (-1,1):
   z=sig+jt*tt*(ie*eta)*Y
   ro[(ie,jt)]=[mp_polar(mp_corr(z,e)) for e in range(3)]
 total=mp.mpf('0')
 for e in range(3):
  N=ro[(1,1)][e]-ro[(1,-1)][e]-ro[(-1,1)][e]+ro[(-1,-1)][e]
  M=N/(4*eta*tt);total+=mp.fsum([M[i,j]**2 for i in range(3) for j in range(3)])
 return float(mp.sqrt(total))
def run_measurement():
 rows=[];states=V64.ASYM.select_states();analytic_ok=True;floor_ok=True;mp_ok=True
 eps=np.finfo(float).eps
 for row in states:
  rho=row['rho'];Y,lift=V64.target_Y(rho);an=analytic(rho,Y);analytic_ok&=an<=1e-12
  fn=[];fm=[]
  for t in FLOAT_TS:
   a,b=float_measure(rho,Y,t);fn.append(a);fm.append(b)
  tail=fn[-3:];floor=max(tail)/max(min(tail),1e-300);floor_ok&=floor<=10
  hm=[mp_measure(rho,Y,t) for t in MP_TS]
  ratio=fm[-1]/max(hm[-1],1e-300);good=hm[-1]<=1e-12 and ratio>=1e4;mp_ok&=good
  rows.append({'candidate_index':row['candidate_index'],'analytic_max_skew':an,'float_numerators':fn,'float_mixed_norms':fm,'float_tail_floor_factor':floor,'mp_mixed_norms':hm,'float_to_mp_ratio_at_min_t':ratio,'mp_min_t_pass':bool(good)})
 if not analytic_ok:verdict='ANALYTIC_FACTOR_INVALID'
 elif analytic_ok and floor_ok and mp_ok:verdict='NUMERICAL_CANCELLATION_CONFIRMED'
 elif analytic_ok and not mp_ok:verdict='ANALYTIC_NUMERIC_DISAGREEMENT'
 else:verdict='INVALID'
 return {'verdict':verdict,'mp_dps':MP_DPS,'float_amplitudes':FLOAT_TS,'mp_amplitudes':MP_TS,'rows':rows}
if __name__=='__main__':
 try:r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0)
 except Exception as e:print(json.dumps({'verdict':'INVALID','error':repr(e)}));raise SystemExit(2)
