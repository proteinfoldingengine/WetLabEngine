"""v15.63 global lifting of polar-symmetric retained leakage."""
import importlib.util,itertools,json,pathlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ASYM=load(PARENT/'asymmetric-heldout-ensemble'/'gate.py','asym63')
EXPECTED=[13,16,22,25,27,29,37,39,46,50,66,77];EDGES=ASYM.EDGES\ndef states():\n z=ASYM.select_states()\n if [x['candidate_index'] for x in z]!=EXPECTED: raise RuntimeError('state identity mismatch')\n return z
# HS-normalized nonidentity Pauli strings.
BASIS=[]
LABELS=[]
for ids in itertools.product(range(4),repeat=3):
 if ids==(0,0,0):continue
 op=ASYM.F.op(*ids)/np.sqrt(8);BASIS.append(op);LABELS.append(ids)
def expect_derivative(B,obs):return float(np.trace(B@obs).real)
def derivative_maps(rho):
 # rows: 9 one-body derivatives; 27 two-body raw expectation derivatives.
 A1=[];Ap=[]
 for q in range(3):
  for a in range(1,4):
   obs=ASYM.F.op(*([a if k==q else 0 for k in range(3)]));A1.append([expect_derivative(B,obs) for B in BASIS])
 for i,j in EDGES:
  for a in range(1,4):
   for b in range(1,4):
    ids=[0,0,0];ids[i]=a;ids[j]=b;obs=ASYM.F.op(*ids);Ap.append([expect_derivative(B,obs) for B in BASIS])
 return np.array(A1),np.array(Ap)
def sym_basis():
 out=[]
 for i in range(3):
  x=np.zeros((3,3));x[i,i]=1;out.append(x)
 for i,j in [(0,1),(0,2),(1,2)]:
  x=np.zeros((3,3));x[i,j]=x[j,i]=1/np.sqrt(2);out.append(x)
 return out
SYM=sym_basis();H0=np.eye(3)/np.sqrt(3)
def rotations(rho):
 out=[]
 for e in EDGES:
  C=ASYM.F.corr(rho,*e);u,s,vh=np.linalg.svd(C);O=u@vh
  if np.linalg.det(O)<0:u[:,-1]*=-1;O=u@vh
  out.append(O)
 return out
def solve(A,b):
 y,resrank,_,_=np.linalg.lstsq(A,b,rcond=None);rr=float(np.linalg.norm(A@y-b)/max(np.linalg.norm(b),1e-300))
 Y=sum(c*B for c,B in zip(y,BASIS))
 return {'relative_residual':rr,'coefficient_norm':float(np.linalg.norm(y)),'constraint_rank':int(np.linalg.matrix_rank(A)),'constraint_nullity':int(63-np.linalg.matrix_rank(A)),'trace_residual':float(abs(np.trace(Y))),'hermiticity_residual':float(np.linalg.norm(Y-Y.conj().T))},y
def single(A1,Ap,O,e,H):
 rows=np.vstack([A1,Ap[e*9:(e+1)*9]]);b=np.concatenate([np.zeros(9),(O[e]@H).reshape(-1)])
 return solve(rows,b)[0]
def simultaneous(A1,Ap,O):
 b=np.concatenate([np.zeros(9)]+[(O[e]@H0).reshape(-1) for e in range(3)])
 return solve(np.vstack([A1,Ap]),b)[0]
def run_measurement():
 states=ASYM.select_states()
 if [x['candidate_index'] for x in states]!=EXPECTED:return {'verdict':'INVALID','rows':[]}
 rows=[];all_single=True;all_sim=True
 for row in states:
  rho=row['rho'];A1,Ap=derivative_maps(rho);O=rotations(rho);sing=[]
  for e in range(3):
   sing.append([single(A1,Ap,O,e,H) for H in SYM])
  sim=simultaneous(A1,Ap,O)
  s_ok=all(z['relative_residual']<=1e-10 and z['trace_residual']<=1e-12 and z['hermiticity_residual']<=1e-12 for ee in sing for z in ee)
  m_ok=sim['relative_residual']<=1e-10 and sim['trace_residual']<=1e-12 and sim['hermiticity_residual']<=1e-12
  all_single&=s_ok;all_sim&=m_ok
  rows.append({'candidate_index':row['candidate_index'],'single_edge':sing,'simultaneous':sim,'single_all_feasible':s_ok,'simultaneous_feasible':m_ok})
 verdict='GLOBAL_SYMMETRIC_NULL_LIFT_EXISTS' if all_single and all_sim else ('PARTIAL_GLOBAL_LIFT_ONLY' if all_single else 'GLOBAL_LIFT_OBSTRUCTED')
 return {'verdict':verdict,'rows':rows}
if __name__=='__main__':
 r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0)
