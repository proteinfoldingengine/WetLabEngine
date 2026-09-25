"""v15.56 Task 26: diagnose cospectral localized response by rooted Green data."""
import numpy as np
import adversarial_topology as at

def rooted_measure(L,s=0,tol=1e-7):
 w,U=np.linalg.eigh(L); out=[]
 used=np.zeros(len(w),bool)
 for i,x in enumerate(w):
  if used[i]:continue
  idx=np.where(np.abs(w-x)<tol)[0];used[idx]=True
  out.append((float(np.mean(w[idx])),float(np.sum(U[s,idx]**2))))
 return out
def run():
 a=at.run(); pair=[tuple(map(tuple,x)) for x in a["cospectral_pair_edges"]]
 L1,L2=at.lap(pair[0]),at.lap(pair[1])
 ev1,ev2=np.linalg.eigvalsh(L1),np.linalg.eigvalsh(L2)
 m1,m2=rooted_measure(L1),rooted_measure(L2)
 # same eigenvalue buckets for a cospectral pair
 ms=float(np.linalg.norm(np.array([x[1] for x in m1])-np.array([x[1] for x in m2])))
 G1,G2=np.linalg.pinv(L1,rcond=1e-13),np.linalg.pinv(L2,rcond=1e-13)
 J=np.zeros(6);J[0]=1;J-=J.mean()
 p1=G1@J; p1-=p1.mean()
 recon=np.linalg.norm(p1-G1[:,0]) # G1*1=0, so centered delta response is column 0
 return {
  "cospectral_pair_frozen":True,
  "cospectral_pair_edges":a["cospectral_pair_edges"],
  "max_global_spectrum_difference":float(np.max(np.abs(ev1-ev2))),
  "rooted_spectral_measure_separation":ms,
  "green_diagonal_separation":float(abs(G1[0,0]-G2[0,0])),
  "response_reconstruction_error":float(recon),
  "interpretation":"LOCALIZED_RESPONSE_IS_A_ROOTED_GREEN_COLUMN; GLOBAL_EIGENVALUES_ALONE_DO_NOT_FIX_SOURCE_RELATIVE_SPECTRAL_WEIGHTS"
 }
