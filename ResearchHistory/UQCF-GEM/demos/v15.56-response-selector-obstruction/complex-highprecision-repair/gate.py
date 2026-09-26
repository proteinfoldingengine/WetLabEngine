"""v15.68 complex-preserving 80-digit repair of v15.66."""
import importlib.util,json,pathlib,numpy as np,mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V64=load(PARENT/'source-vector-field-null'/'gate.py','v64c')
V66=load(PARENT/'polar-derivative-numerics'/'gate.py','v66c')
MP_DPS=80;FLOAT_TS=V66.FLOAT_TS;MP_TS=V66.MP_TS
mp.mp.dps=MP_DPS

def mpcmat(A):
 return mp.matrix([[mp.mpc(str(float(A[i,j].real)),str(float(A[i,j].imag))) for j in range(A.shape[1])] for i in range(A.shape[0])])

def mp_expect(rho,op_np):
 op=mpcmat(op_np)
 z=mp.fsum([rho[r,k]*op[k,r] for r in range(8) for k in range(8)])
 return mp.re(z)

def mp_corr(rho,e):
 i,j=V64.ASYM.EDGES[e];C=mp.matrix(3,3)
 for a in range(1,4):
  for b in range(1,4):
   ids=[0,0,0];ids[i]=a;ids[j]=b;ei=mp_expect(rho,V64.ASYM.F.op(*ids))
   ids1=[0,0,0];ids1[i]=a;mi=mp_expect(rho,V64.ASYM.F.op(*ids1))
   ids2=[0,0,0];ids2[j]=b;mj=mp_expect(rho,V64.ASYM.F.op(*ids2))
   C[a-1,b-1]=ei-mi*mj
 return C

def mp_polar(C):
 G=C.T*C;vals,Q=mp.eigsy(G);D=mp.diag([1/mp.sqrt(vals[i]) for i in range(3)])
 return C*Q*D*Q.T

def mp_to_np_complex(A):
 return np.array([[complex(float(mp.re(A[i,j])),float(mp.im(A[i,j]))) for j in range(A.cols)] for i in range(A.rows)])

def mp_to_np_real(A):
 return np.array([[float(A[i,j]) for j in range(A.cols)] for i in range(A.rows)])

def pol64(C):
 u,s,vh=np.linalg.svd(C);O=u@vh
 if np.linalg.det(O)<0:u[:,-1]*=-1;O=u@vh
 return O

def corner_mp(rho,Y,ie,jt,t):
 return mpcmat(rho)+ie*mp.mpf(str(V64.ETA))*mpcmat(V64.HIDDEN)+jt*ie*mp.mpf(str(V64.ETA*t))*mpcmat(Y)

def identity_gate():
 row=[x for x in V64.ASYM.select_states() if x['candidate_index']==13][0];rho=row['rho'];Y,_=V64.target_Y(rho)
 z64=V64.T(rho+V64.ETA*V64.HIDDEN,rho,Y,1e-3);zmp=corner_mp(rho,Y,1,1,1e-3)
 state=float(np.max(np.abs(z64-mp_to_np_complex(zmp))))
 one=[];two=[];onemp=[];twomp=[]
 for q in range(3):
  for a in range(1,4):
   ids=[0,0,0];ids[q]=a;op=V64.ASYM.F.op(*ids);one.append(float(np.trace(z64@op).real));onemp.append(float(mp_expect(zmp,op)))
 for i,j in V64.ASYM.EDGES:
  for a in range(1,4):
   for b in range(1,4):
    ids=[0,0,0];ids[i]=a;ids[j]=b;op=V64.ASYM.F.op(*ids);two.append(float(np.trace(z64@op).real));twomp.append(float(mp_expect(zmp,op)))
 one=np.array(one);two=np.array(two);onemp=np.array(onemp);twomp=np.array(twomp)
 md=max(float(np.max(np.abs(one-onemp))),float(np.max(np.abs(two-twomp))))
 C64=[];Cmp=[];k=0
 for e,(i,j) in enumerate(V64.ASYM.EDGES):
  A=np.zeros((3,3));B=np.zeros((3,3))
  for a in range(3):
   for b in range(3):
    A[a,b]=two[k]-one[i*3+a]*one[j*3+b];B[a,b]=twomp[k]-onemp[i*3+a]*onemp[j*3+b];k+=1
  C64.append(A);Cmp.append(B)
 cd=max(float(np.max(np.abs(a-b))) for a,b in zip(C64,Cmp))
 pd=max(float(np.linalg.norm(pol64(a)-mp_to_np_real(mp_polar(mp.matrix(b.tolist()))))) for a,b in zip(C64,Cmp))
 return {'pass':bool(state<=1e-13 and md<=1e-13 and cd<=1e-13 and pd<=1e-11),'state_diff':state,'moment_diff':md,'correlation_diff':cd,'polar_diff':pd}

def mp_measure(rho,Y,t):
 ro={}
 for ie in (-1,1):
  for jt in (-1,1):
   z=corner_mp(rho,Y,ie,jt,t);ro[(ie,jt)]=[mp_polar(mp_corr(z,e)) for e in range(3)]
 eta=mp.mpf(str(V64.ETA));tt=mp.mpf(str(t));ss=mp.mpf('0')
 for e in range(3):
  M=(ro[(1,1)][e]-ro[(1,-1)][e]-ro[(-1,1)][e]+ro[(-1,-1)][e])/(4*eta*tt)
  ss+=mp.fsum([M[i,j]**2 for i in range(3) for j in range(3)])
 return float(mp.sqrt(ss))

def run_measurement():
 ident=identity_gate()
 if not ident['pass']: return {'verdict':'INVALID','identity_gate':ident,'rows':[]}
 rows=[];analytic_ok=True;floor_ok=True;mp_ok=True
 for row in V64.ASYM.select_states():
  rho=row['rho'];Y,_=V64.target_Y(rho);an=V66.analytic(rho,Y);analytic_ok &= an<=1e-12
  fn=[];fm=[]
  for t in FLOAT_TS:
   a,b=V66.float_measure(rho,Y,t);fn.append(a);fm.append(b)
  tail=fn[-3:];floor=max(tail)/max(min(tail),1e-300);floor_ok &= floor<=10
  hm=[mp_measure(rho,Y,t) for t in MP_TS]
  ratio=fm[-1]/max(hm[-1],1e-300);good=hm[-1]<=1e-12 and ratio>=1e4;mp_ok &= good
  rows.append({'candidate_index':row['candidate_index'],'analytic_max_skew':an,'float_numerators':fn,'float_mixed_norms':fm,'float_tail_floor_factor':floor,'mp_mixed_norms':hm,'float_to_mp_ratio_at_min_t':ratio,'mp_min_t_pass':bool(good)})
 if not analytic_ok: verdict='ANALYTIC_FACTOR_INVALID'
 elif analytic_ok and floor_ok and mp_ok: verdict='NUMERICAL_CANCELLATION_CONFIRMED'
 elif analytic_ok and not mp_ok: verdict='ANALYTIC_NUMERIC_DISAGREEMENT'
 else: verdict='INVALID'
 return {'verdict':verdict,'identity_gate':ident,'mp_dps':MP_DPS,'float_amplitudes':FLOAT_TS,'mp_amplitudes':MP_TS,'rows':rows}

if __name__=='__main__':
 try:
  r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0)
 except Exception as e:
  print(json.dumps({'verdict':'INVALID','error':repr(e)}));raise SystemExit(2)
