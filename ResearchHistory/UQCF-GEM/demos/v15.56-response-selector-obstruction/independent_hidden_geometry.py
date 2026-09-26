"""Held-out independent hidden-completion -> holonomy-response gate."""
import json, numpy as np
from independent_hidden_fixture import I,X,Y,Z,P,op,state,corr,polar
FIX={"m":.10,"d":.08,"a":.04}
EDGES=[(0,1),(1,2),(2,0)]
def hidden_op():
 g=np.zeros((8,8),complex)
 for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:
  ids=[0,0,0];ids[i]=1;ids[j]=2;ids[k]=3;g+=op(*ids)
  ids=[0,0,0];ids[i]=2;ids[j]=1;ids[k]=3;g-=op(*ids)
 return g
G=hidden_op()
PZ=(op(3,0,0)+op(0,3,0)+op(0,0,3))/np.sqrt(3)
ID=np.eye(8)
def herm_log(r):
 w,v=np.linalg.eigh(r);return (v*np.log(w))@v.conj().T
def herm_exp(a):
 w,v=np.linalg.eigh((a+a.conj().T)/2);return (v*np.exp(w))@v.conj().T
def tilt(r,s,Q):
 e=herm_exp(herm_log(r)+s*Q);return e/np.trace(e)
def geom(r):
 Cs=[corr(r,*e) for e in EDGES]; Os=[polar(c)[0] for c in Cs];H=Os[0]@Os[1]@Os[2]
 return Cs,Os,H
def marginal_diff(a,b):
 # Pauli expectations through two-body order determine qubit marginals.
 vals=[]
 for q in range(3):
  for x in range(1,4): vals.append(abs(np.trace((a-b)@op(*([x if z==q else 0 for z in range(3)])))))
 for i,j in [(0,1),(1,2),(0,2)]:
  for x in range(1,4):
   for y in range(1,4):
    ids=[0,0,0];ids[i]=x;ids[j]=y;vals.append(abs(np.trace((a-b)@op(*ids))))
 return float(max(vals))
def jet(r,Q,eps=1e-5):
 hp=geom(tilt(r,eps,Q))[2];hm=geom(tilt(r,-eps,Q))[2];return (hp-hm)/(2*eps)
def choose_eta(r):
 for eta in [.003,.002,.001]:
  rh=r+eta*G
  if np.linalg.eigvalsh(rh).min()>=.01:return eta,rh
 raise RuntimeError("no eta")
def run():
 rb=state(**FIX);eta,rh=choose_eta(rb)
 Cb,Ob,Hb=geom(rb);Ch,Oh,Hh=geom(rh)
 vis=marginal_diff(rb,rh); pd=max(np.linalg.norm(Ob[i]-Oh[i]) for i in range(3)); hd=np.linalg.norm(Hb-Hh)
 jb=jet(rb,PZ);jh=jet(rh,PZ); gap=float(np.linalg.norm(jh-jb))
 # preregistered controls
 eta0=float(np.linalg.norm(jet(rb,PZ)-jet(rb,PZ)))
 idnull=max(float(np.linalg.norm(jet(rb,ID))),float(np.linalg.norm(jet(rh,ID))))
 rminus=rb-eta*G; sign_gap=float(np.linalg.norm((jet(rh,PZ)-jb)+(jet(rminus,PZ)-jb)))
 scale=float(np.linalg.norm(jet(rh,2*PZ)-2*jh))
 gates=vis<=1e-12 and pd<=1e-10 and hd<=1e-10 and np.linalg.eigvalsh(rh).min()>=.01
 controls=eta0<=1e-12 and idnull<=1e-8 and sign_gap<=5e-5 and scale<=5e-5
 verdict=("INDEPENDENT_HIDDEN_COMPLETION_GEOMETRY_SIGNAL" if gates and controls and gap>1e-6 else ("NULL" if gates and controls else "INVALID_FIXTURE"))
 return {"fixture":FIX,"eta":eta,"hidden_min_eigenvalue":float(np.linalg.eigvalsh(rh).min()),
 "max_proper_marginal_expectation_difference":vis,"initial_polar_transport_difference":pd,"initial_holonomy_difference":hd,
 "base_holonomy_jet_norm":float(np.linalg.norm(jb)),"hidden_holonomy_jet_norm":float(np.linalg.norm(jh)),
 "holonomy_jet_difference":gap,"controls":{"eta0":eta0,"identity_source":idnull,"hidden_sign_antisymmetry":sign_gap,"source_scale":scale},
 "matched_input_gates_pass":bool(gates),"controls_pass":bool(controls),"parameters_fit_to_response":0,"verdict":verdict}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
