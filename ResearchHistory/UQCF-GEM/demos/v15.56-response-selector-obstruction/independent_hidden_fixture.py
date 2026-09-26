"""Stage A: freeze a new axial/cyclic base fixture. No hidden-response endpoint."""
import json, numpy as np
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)
P=[I,X,Y,Z]
def kron3(a,b,c): return np.kron(np.kron(a,b),c)
def op(a,b,c): return kron3(P[a],P[b],P[c])
def ptrace(rho,keep):
    keep=tuple(sorted(keep)); out=np.zeros((2**len(keep),2**len(keep)),complex)
    for a in range(8):
      ba=((a>>2)&1,(a>>1)&1,a&1)
      for b in range(8):
       bb=((b>>2)&1,(b>>1)&1,b&1)
       if all(ba[q]==bb[q] for q in range(3) if q not in keep):
        ia=sum(ba[q]<<(len(keep)-1-j) for j,q in enumerate(keep)); ib=sum(bb[q]<<(len(keep)-1-j) for j,q in enumerate(keep)); out[ia,ib]+=rho[a,b]
    return out
def expect(rho,site_ops):
    ids=[0,0,0]
    for q,k in site_ops.items(): ids[q]=k
    return np.trace(rho@op(*ids))
def corr(rho,i,j):
    # Preserve requested oriented edge (i,j), including wrap edge (2,0).
    C=np.zeros((3,3))
    for a in range(1,4):
      for b in range(1,4):
       C[a-1,b-1]=(expect(rho,{i:a,j:b})-expect(rho,{i:a})*expect(rho,{j:b})).real
    return C
def polar(C):
    u,s,vh=np.linalg.svd(C); O=u@vh
    if np.linalg.det(O)<0: u[:,-1]*=-1; O=u@vh
    return O,s
def angle(H): return float(np.arccos(np.clip((np.trace(H).real-1)/2,-1,1)))
def state(m,d,a):
    # cyclic U(1)-invariant Pauli ansatz; pair block [[d,-a,0],[a,d,0],[0,0,dz]]
    dz=d/2
    R=np.eye(8,dtype=complex)
    for q in range(3): R+=m*op(3 if q==0 else 0,3 if q==1 else 0,3 if q==2 else 0)
    for i,j in [(0,1),(1,2),(2,0)]:
      ids=[0,0,0]
      for aa,bb,c in [(1,1,d),(2,2,d),(3,3,dz),(1,2,-a),(2,1,a)]:
       ids=[0,0,0];ids[i]=aa;ids[j]=bb;R+=c*op(*ids)
    return R/8
def select():
  # Frozen lexicographic grid; response is nowhere computed.
  for m in [0.10,0.15,0.20]:
   for d in [0.08,0.12,0.16]:
    for a in [0.04,0.08,0.12]:
     r=state(m,d,a); mine=float(np.linalg.eigvalsh(r).min())
     if mine<0.03: continue
     Cs=[corr(r,*e) for e in [(0,1),(1,2),(2,0)]]
     cyc=float(max(np.linalg.norm(Cs[i]-Cs[0]) for i in range(1,3)))
     if cyc>1e-12: continue
     ps=[polar(c) for c in Cs]
     if min(x[1].min() for x in ps)<0.02: continue
     H=ps[0][0]@ps[1][0]@ps[2][0]; h=angle(H)
     if h<0.20: continue
     return dict(m=m,d=d,a=a,dz=d/2,min_eigenvalue=mine,holonomy_angle=h,
       pair_singular_min=float(min(x[1].min() for x in ps)),
       cyclic_pair_difference=cyc)
  raise RuntimeError("no admissible fixture")
def run():
  f=select(); return {"stage":"BASE_FIXTURE_FROZEN_NO_HIDDEN_RESPONSE","fixture":f,
    "parameter_grid_order":"m=[.10,.15,.20],d=[.08,.12,.16],a=[.04,.08,.12],lexicographic_first_admissible",
    "admissibility":{"min_eigenvalue":0.03,"min_pair_singular":0.02,"min_holonomy_angle":0.20,"max_cyclic_pair_difference":1e-12},
    "hidden_response_evaluated":False,"parameters_fit_to_response":0}
if __name__=="__main__": print(json.dumps(run(),indent=2,sort_keys=True))
