"""v15.64 explicit normalized local source-vector-field symmetric null."""
import importlib.util,json,pathlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ASYM=load(PARENT/'asymmetric-heldout-ensemble'/'gate.py','asym64')
GL=load(PARENT/'global-symmetric-null-lift'/'gate.py','gl64')
EXPECTED=GL.EXPECTED;ETA=1e-4;TS=[1e-4,3e-4,1e-3]
HIDDEN=ASYM.F.op(1,1,1)/np.sqrt(8)
def hidden_marginal_norm():
 A1,Ap=GL.derivative_maps(np.eye(8)/8)
 y=np.array([np.trace(B@HIDDEN).real for B in GL.BASIS])
 return float(np.linalg.norm(np.concatenate([A1@y,Ap@y])))
def target_Y(rho):
 A1,Ap=GL.derivative_maps(rho);O=GL.rotations(rho)
 b=np.concatenate([np.zeros(9)]+[(O[e]@GL.H0).reshape(-1) for e in range(3)])
 A=np.vstack([A1,Ap]);y=np.linalg.lstsq(A,b,rcond=None)[0];Y=sum(c*B for c,B in zip(y,GL.BASIS))
 return Y,float(np.linalg.norm(A@y-b)/np.linalg.norm(b))
def alpha(sigma,rho):return float(np.trace(HIDDEN@(sigma-rho)).real/np.trace(HIDDEN@HIDDEN).real)
def X(sigma,rho,Y):return alpha(sigma,rho)*Y
def T(sigma,rho,Y,t):return sigma+t*X(sigma,rho,Y)
def rotations(sigma):return np.asarray(ASYM.G.geom(sigma)[1])
def skew_parent(rho):
 # Positive parent scale from an exact retained skew direction, converted through polar FD.
 O=rotations(rho);vals=[]
 eps=1e-6
 for e in range(3):
  C=ASYM.F.corr(rho,*ASYM.EDGES[e])
  for K in GL.load(PARENT/'symmetric-leakage-null'/'gate.py','sn64').SKEW:
   Cp=C+eps*(O[e]@K);Cm=C-eps*(O[e]@K)
   def pol(A):
    u,s,vh=np.linalg.svd(A);q=u@vh
    if np.linalg.det(q)<0:u[:,-1]*=-1;q=u@vh
    return q
   vals.append(np.linalg.norm((pol(Cp)-pol(Cm))/(2*eps)))
 return max(vals)
def rank_scaled(M,parent):
 s=np.linalg.svd(M,compute_uv=False);return [int(np.sum(s>parent*r)) for r in [1e-9,1e-10,1e-11]]
def run_measurement():
 states=ASYM.select_states()
 if [x['candidate_index'] for x in states]!=EXPECTED:return {'verdict':'INVALID','rows':[]}
 rows=[];okall=True
 for row in states:
  rho=row['rho'];Y,lift=target_Y(rho)
  # DX[h] centered check.
  fd=(X(rho+ETA*HIDDEN,rho,Y)-X(rho-ETA*HIDDEN,rho,Y))/(2*ETA)
  deriv=float(np.linalg.norm(fd-Y)/np.linalg.norm(Y))
  # Retained symmetric target and analytic skew projection.
  A1,Ap=GL.derivative_maps(rho);y=np.array([np.trace(B@Y).real for B in GL.BASIS]);O=GL.rotations(rho)
  one=float(np.linalg.norm(A1@y));proj=[]
  for e in range(3):
   d=(Ap[e*9:(e+1)*9]@y).reshape(3,3);proj.append(np.linalg.norm(O[e].T@d-d.T@O[e]))
  parent=skew_parent(rho)
  mineig=1.;worst_rank=[0,0,0]
  for t in TS:
   ro={}
   for ie in (-1,1):
    sig=rho+ie*ETA*HIDDEN
    for jt in (-1,1):
     z=T(sig,rho,Y,jt*t);mineig=min(mineig,float(np.linalg.eigvalsh(z).min()))
     if abs(np.trace(z)-1)>1e-12:okall=False
     ro[(ie,jt)]=rotations(z)
   M=(ro[(1,1)]-ro[(1,-1)]-ro[(-1,1)]+ro[(-1,-1)])/(4*ETA*t)
   # 9 x 1 rotational mixed column; effective rank either 0 or 1.
   col=np.concatenate([m.reshape(-1) for m in M])[:,None]
   rr=rank_scaled(col,parent);worst_rank=[max(a,b) for a,b in zip(worst_rank,rr)]
  ok=lift<=1e-10 and deriv<=1e-10 and one<=1e-12 and max(proj)/parent<=1e-10 and mineig>=-1e-12 and worst_rank==[0,0,0] and np.linalg.norm(Y)>1e-6
  okall&=ok
  rows.append({'candidate_index':row['candidate_index'],'Y_norm':float(np.linalg.norm(Y)),'lift_relative_residual':lift,'DX_hidden_relative_residual':deriv,'one_body_residual':one,'max_polar_skew_projection':float(max(proj)),'positive_parent_scale':float(parent),'min_finite_eigenvalue':mineig,'mixed_rank_sweep':worst_rank,'pass':bool(ok)})
 verdict='SOURCE_VECTOR_FIELD_NULL_REALIZED' if okall else 'SOURCE_VECTOR_FIELD_NULL_FALSIFIED'
 return {'verdict':verdict,'hidden_marginal_norm':hidden_marginal_norm(),'rows':rows}
if __name__=='__main__':
 r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['verdict']=='SOURCE_VECTOR_FIELD_NULL_REALIZED' else 2)
