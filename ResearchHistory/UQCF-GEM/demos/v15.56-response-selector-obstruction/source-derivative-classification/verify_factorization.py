"""Algebraic verification of v15.61 regular-stratum rank classification."""
import numpy as np
rng=np.random.default_rng(1561)
def skew_basis():
 out=[]
 for i,j in [(0,1),(0,2),(1,2)]:
  x=np.zeros((3,3));x[i,j]=1/np.sqrt(2);x[j,i]=-1/np.sqrt(2);out.append(x)
 return out
B=skew_basis()
def coeff(x):return np.array([np.sum(b*x) for b in B])
def rand_rot():
 q,r=np.linalg.qr(rng.normal(size=(3,3)));q=q@np.diag(np.where(np.diag(r)<0,-1.,1.))
 if np.linalg.det(q)<0:q[:,0]*=-1
 return q
def syl(P,W):return P@W+W@P
def trial():
 O=rand_rot();u=rand_rot();vals=rng.uniform(.02,.4,3);P=u@np.diag(vals)@u.T
 # Matrix of Sylvester map on so(3).
 S=np.column_stack([coeff(syl(P,b)) for b in B])
 assert np.linalg.matrix_rank(S)==3
 # Arbitrary pre-Sylvester observable map Q: 3 x 27.
 Q=rng.normal(size=(3,27))
 E=np.linalg.solve(S,Q)
 assert np.linalg.matrix_rank(E)==np.linalg.matrix_rank(Q)
 # Exact polar-symmetric null: deltaC=O H with H symmetric => O-skew projection zero.
 H=rng.normal(size=(3,3));H=(H+H.T)/2;dC=O@H
 q=O.T@dC-dC.T@O
 assert np.linalg.norm(q)<1e-12
 # Nonzero retained leakage can therefore be rotationally invisible.
 assert np.linalg.norm(dC)>1e-6
 return np.linalg.cond(S)
conds=[trial() for _ in range(1000)]
print({"trials":1000,"all_pass":True,"max_sylvester_condition":max(conds),"median_sylvester_condition":float(np.median(conds))})
