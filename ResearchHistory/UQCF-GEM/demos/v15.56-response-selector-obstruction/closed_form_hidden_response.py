"""Closed-form mixed response: no numerical eta/s derivative inside K_CF."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
import hidden_response_theorem as A

# Frechet log via divided differences
def log_frechet(r,B):
 w,v=np.linalg.eigh(r);Bt=v.conj().T@B@v;M=np.empty((8,8))
 for i in range(8):
  for j in range(8):
   M[i,j]=1/w[i] if abs(w[i]-w[j])<1e-12 else (np.log(w[i])-np.log(w[j]))/(w[i]-w[j])
 return v@(M*Bt)@v.conj().T

# second Frechet exp using 3x3 block upper triangular identity:
# exp([[L,A,0],[0,L,B],[0,0,L]])_13 gives ordered second term;
# symmetrize A,B. Matrix exponential is evaluated spectrally on a Hermitian
# dilation through a power series, avoiding scipy dependency.
def expm_series(M):
 # scaling/squaring Taylor; deterministic algebraic evaluation, no differentiation
 nrm=np.linalg.norm(M,ord=np.inf);q=max(0,int(np.ceil(np.log2(max(1,nrm)))));X=M/(2**q);R=np.eye(M.shape[0],dtype=complex);term=R.copy()
 for k in range(1,80):
  term=term@X/k;R=R+term
  if np.linalg.norm(term,ord=np.inf)<1e-16:break
 for _ in range(q):R=R@R
 return R
def d2exp(L,A1,B1):
 n=L.shape[0]
 def ordered(A,B):
  M=np.zeros((3*n,3*n),complex);M[:n,:n]=L;M[n:2*n,n:2*n]=L;M[2*n:,2*n:]=L;M[:n,n:2*n]=A;M[n:2*n,2*n:]=B
  return expm_series(M)[:n,2*n:]
 return ordered(A1,B1)+ordered(B1,A1)

def state_tangents(r):
 L=G.herm_log(r);Lp=log_frechet(r,G.G);N=A.exp_frechet(L,G.PZ);Neta=d2exp(L,Lp,G.PZ)
 ts=N-r*np.trace(N)
 tm=Neta-G.G*np.trace(N)-r*np.trace(Neta)
 return G.G,ts,tm

def corr_from_tangents(r,re,rs,res,i,j):
 def ex(x,ops):return F.expect(x,ops)
 C=F.corr(r,i,j);Ce=np.zeros((3,3));Cs=np.zeros((3,3));Ces=np.zeros((3,3))
 for aa in range(1,4):
  for bb in range(1,4):
   ai=ex(r,{i:aa});bj=ex(r,{j:bb});ae=ex(re,{i:aa});be=ex(re,{j:bb});ass=ex(rs,{i:aa});bs=ex(rs,{j:bb});aes=ex(res,{i:aa});bes=ex(res,{j:bb})
   Ce[aa-1,bb-1]=(ex(re,{i:aa,j:bb})-ae*bj-ai*be).real
   Cs[aa-1,bb-1]=(ex(rs,{i:aa,j:bb})-ass*bj-ai*bs).real
   Ces[aa-1,bb-1]=(ex(res,{i:aa,j:bb})-aes*bj-ae*bs-ass*be-ai*bes).real
 return C,Ce,Cs,Ces

def polar_all(C,Ce,Cs,Ces):
 O,_=F.polar(C);S=O.T@C
 def solve(R):
  M=np.kron(np.eye(3),S)+np.kron(S.T,np.eye(3));W=np.linalg.solve(M,R.reshape(-1,order="F")).reshape((3,3),order="F");return (W-W.T)/2
 We=solve(O.T@Ce-Ce.T@O);Ws=solve(O.T@Cs-Cs.T@O);Oe=O@We;Os=O@Ws
 Se=Oe.T@C+O.T@Ce
 # Differentiate R_s=O^T Cs-Cs^T O
 Res=Oe.T@Cs+O.T@Ces-Ces.T@O-Cs.T@Oe
 Wes=solve(Res-Se@Ws-Ws@Se)
 Oes=Oe@Ws+O@Wes
 return O,Oe,Os,Oes

def closed_K(r):
 re,rs,res=state_tangents(r);Q=[polar_all(*corr_from_tangents(r,re,rs,res,*e)) for e in G.EDGES]
 O=[q[0] for q in Q];E1=[q[1] for q in Q];S1=[q[2] for q in Q];M=[q[3] for q in Q]
 K=M[0]@O[1]@O[2]+O[0]@M[1]@O[2]+O[0]@O[1]@M[2]
 K+=E1[0]@S1[1]@O[2]+S1[0]@E1[1]@O[2]+E1[0]@O[1]@S1[2]+S1[0]@O[1]@E1[2]+O[0]@E1[1]@S1[2]+O[0]@S1[1]@E1[2]
 return K

def run():
 rows=[]
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    K=closed_K(r);Kc=A.mixed_analytic(r);Kfd=A.mixed_four_corner(r)
    ec=np.linalg.norm(K-Kc)/max(np.linalg.norm(Kc),1e-15);ef=np.linalg.norm(K-Kfd)/max(np.linalg.norm(Kfd),1e-15)
    rows.append(dict(m=m,d=d,a=a,relative_vs_computational=float(ec),relative_vs_four_corner=float(ef),K_norm=float(np.linalg.norm(K))))
 deg=any(not np.isfinite(z["relative_vs_four_corner"]) for z in rows);good=len(rows)==11 and all(z["relative_vs_computational"]<=1e-5 and z["relative_vs_four_corner"]<=1e-5 for z in rows)
 verdict="DEGENERATE_STRATUM" if deg else ("CLOSED_FORM_MIXED_RESPONSE_THEOREM_VERIFIED" if good else "CLOSED_FORM_FORMULA_FAILS")
 return {"fixture_count":len(rows),"max_relative_vs_computational":max(z["relative_vs_computational"] for z in rows),"max_relative_vs_four_corner":max(z["relative_vs_four_corner"] for z in rows),"fitted_coefficients":0,"numerical_derivative_inside_closed_form":False,"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
