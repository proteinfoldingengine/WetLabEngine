"""v15.69 local-SU(2)^3 covariance of the symmetric-null construction."""
import importlib.util,json,pathlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;PARENT=HERE.parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V64=load(PARENT/'source-vector-field-null'/'gate.py','v64cov')
SEED=20260969;N_FRAMES=8;ETA=1e-4;T=1e-3
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.array([[1,0],[0,-1]],complex)
P=[X,Y,Z]

def kron3(a,b,c): return np.kron(np.kron(a,b),c)

def frames():
 rng=np.random.default_rng(SEED);out=[]
 for _ in range(N_FRAMES):
  us=[];rs=[]
  for __ in range(3):
   q=rng.normal(size=4);q=q/np.linalg.norm(q);w,x,y,z=q
   u=w*I-1j*(x*X+y*Y+z*Z)
   r=np.empty((3,3),float)
   for a in range(3):
    for b in range(3):
     r[a,b]=float((np.trace(P[a]@u@P[b]@u.conj().T)/2).real)
   us.append(u);rs.append(r)
  out.append((kron3(*us),rs))
 return out

def alpha_h(sigma,rho,h):
 return float(np.trace(h@(sigma-rho)).real/np.trace(h@h).real)

def source_step(sigma,rho,h,Ylift,st):
 return sigma+st*alpha_h(sigma,rho,h)*Ylift

def coeffs(A):
 return np.array([np.trace(B@A).real for B in V64.GL.BASIS])

def delta_cs(rho,Ylift):
 _,Ap=V64.GL.derivative_maps(rho);y=coeffs(Ylift)
 return [(Ap[9*e:9*(e+1)]@y).reshape(3,3) for e in range(3)]

def run_measurement():
 states=V64.ASYM.select_states();fr=frames();rows=[];okall=True
 maxes={'lift_rel':0.,'polar_cov':0.,'target_cov_rel':0.,'field_cov':0.,'null_rel':0.,'trace_err':0.};mineig=1.
 try:
  for row in states:
   rho=row['rho'];Y0,lift0=V64.target_Y(rho);O0=V64.GL.rotations(rho);d0=delta_cs(rho,Y0)
   for fi,(U,Rs) in enumerate(fr):
    rho1=U@rho@U.conj().T;h1=U@V64.HIDDEN@U.conj().T;Ytr=U@Y0@U.conj().T
    Y1,lift1=V64.target_Y(rho1);O1=V64.GL.rotations(rho1);d1=delta_cs(rho1,Y1)
    liftrel=float(np.linalg.norm(Y1-Ytr)/np.linalg.norm(Ytr))
    pc=[];tc=[];nr=[]
    for e,(i,j) in enumerate(V64.ASYM.EDGES):
     Oexp=Rs[i]@O0[e]@Rs[j].T;pc.append(float(np.linalg.norm(O1[e]-Oexp)))
     dexp=Rs[i]@d0[e]@Rs[j].T;tc.append(float(np.linalg.norm(d1[e]-dexp)/np.linalg.norm(dexp)))
     q=O1[e].T@d1[e]-d1[e].T@O1[e];nr.append(float(np.linalg.norm(q)/np.linalg.norm(d1[e])))
    fc=0.;te=0.;mi=1.
    for ie in (-1,1):
     sig=rho+ie*ETA*V64.HIDDEN;sig1=rho1+ie*ETA*h1
     for jt in (-1,1):
      z=source_step(sig,rho,V64.HIDDEN,Y0,jt*T)
      z1=source_step(sig1,rho1,h1,Y1,jt*T)
      fc=max(fc,float(np.linalg.norm(z1-U@z@U.conj().T)))
      te=max(te,float(abs(np.trace(z1)-1)))
      mi=min(mi,float(np.linalg.eigvalsh(z1).min()))
    caseok=(liftrel<=1e-9 and max(pc)<=1e-10 and max(tc)<=1e-9 and fc<=1e-11 and max(nr)<=1e-10 and te<=1e-12 and mi>=-1e-12 and lift0<=1e-10 and lift1<=1e-10)
    okall &= caseok
    maxes['lift_rel']=max(maxes['lift_rel'],liftrel);maxes['polar_cov']=max(maxes['polar_cov'],max(pc));maxes['target_cov_rel']=max(maxes['target_cov_rel'],max(tc));maxes['field_cov']=max(maxes['field_cov'],fc);maxes['null_rel']=max(maxes['null_rel'],max(nr));maxes['trace_err']=max(maxes['trace_err'],te);mineig=min(mineig,mi)
    rows.append({'candidate_index':row['candidate_index'],'frame_index':fi,'lift_relative_residual':liftrel,'polar_covariance_residual':max(pc),'target_covariance_relative_residual':max(tc),'vector_field_covariance_residual':fc,'null_relative_residual':max(nr),'min_finite_eigenvalue':mi,'pass':bool(caseok)})
  verdict='LOCAL_FRAME_COVARIANT_NULL_CONFIRMED' if okall else 'LOCAL_FRAME_COVARIANT_NULL_FALSIFIED'
  return {'verdict':verdict,'n_states':len(states),'n_frames':len(fr),'n_cases':len(rows),'maxima':maxes,'min_finite_eigenvalue':mineig,'rows':rows}
 except Exception as e:
  return {'verdict':'INVALID','n_states':len(states),'n_frames':len(fr),'error':repr(e),'rows':rows}

if __name__=='__main__':
 r=run_measurement();print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r['verdict']!='INVALID' else 2)
