"""v15.62 exact symmetric-leakage null at the retained-observable layer."""
import importlib.util,json,pathlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ASYM=load(PARENT/'asymmetric-heldout-ensemble'/'gate.py','asym62')
EXPECTED=[13,16,22,25,27,29,37,39,46,50,66,77]
def sym_basis():
 out=[]
 for i in range(3):
  x=np.zeros((3,3));x[i,i]=1.;out.append(x)
 for i,j in [(0,1),(0,2),(1,2)]:
  x=np.zeros((3,3));x[i,j]=x[j,i]=1/np.sqrt(2);out.append(x)
 return out
def skew_basis():
 out=[]
 for i,j in [(0,1),(0,2),(1,2)]:
  x=np.zeros((3,3));x[i,j]=1/np.sqrt(2);x[j,i]=-1/np.sqrt(2);out.append(x)
 return out
SYM=sym_basis();SKEW=skew_basis()
def coeff(W):return np.array([np.sum(k*W) for k in SKEW])
def solve(P,Q):
 # P W + W P = Q on skew basis
 S=np.column_stack([coeff(P@k+k@P) for k in SKEW]);return sum(c*k for c,k in zip(np.linalg.solve(S,coeff(Q)),SKEW))
def rank_parent(A,parent):
 s=np.linalg.svd(A,compute_uv=False);return [int(np.sum(s>parent*r)) for r in [1e-9,1e-10,1e-11]]
def run_measurement():
 states=ASYM.select_states()
 if [x['candidate_index'] for x in states]!=EXPECTED:return {'verdict':'INVALID','rows':[]}
 rows=[];valid=True;confirmed=True
 for row in states:
  rho=row['rho'];Cs=[ASYM.F.corr(rho,*e) for e in ASYM.EDGES];edge=[]
  for C in Cs:
   O,svals,Vh=np.linalg.svd(C);R=O@Vh
   if np.linalg.det(R)<0:
    O[:,-1]*=-1;R=O@Vh
   P=R.T@C
   null_cols=[];pos_cols=[];leak=[];proj=[]
   for H in SYM:
    dC=R@H;Q=R.T@dC-dC.T@R;W=solve(P,Q);null_cols.append(coeff(W));leak.append(np.linalg.norm(dC));proj.append(np.linalg.norm(Q))
   for K in SKEW:
    dC=R@K;Q=R.T@dC-dC.T@R;W=solve(P,Q);pos_cols.append(coeff(W))
   N=np.column_stack(null_cols);A=np.column_stack(pos_cols);parent=np.linalg.svd(A,compute_uv=False)[0]
   nr=rank_parent(N,parent);pr=rank_parent(A,parent)
   ok=min(leak)>.5 and max(proj)/parent<=1e-12 and nr==[0,0,0] and pr==[3,3,3] and np.linalg.eigvalsh((P+P.T)/2).min()>0
   valid&=ok;confirmed&=ok
   edge.append({'min_leakage_norm':float(min(leak)),'max_projected_norm':float(max(proj)),'positive_parent_scale':float(parent),'symmetric_rank_sweep':nr,'positive_rank_sweep':pr})
  rows.append({'candidate_index':row['candidate_index'],'edges':edge,'symmetric_ranks':[x['symmetric_rank_sweep'][1] for x in edge],'positive_ranks':[x['positive_rank_sweep'][1] for x in edge]})
 verdict='INVALID' if not valid else ('SYMMETRIC_LEAKAGE_NULL_CONFIRMED' if confirmed else 'SYMMETRIC_LEAKAGE_NULL_FALSIFIED')
 return {'verdict':verdict,'rows':rows}
if __name__=='__main__':
 r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['verdict']=='SYMMETRIC_LEAKAGE_NULL_CONFIRMED' else 2)
