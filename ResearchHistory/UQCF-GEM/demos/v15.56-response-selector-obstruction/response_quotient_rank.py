"""Closed-form response quotient rank over 27 hidden x 9 source directions."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G0
import independent_hidden_ensemble as E
import closed_form_hidden_response as C

# exact-weight-3 Pauli hidden basis
HB=[F.op(a,b,c) for a in range(1,4) for b in range(1,4) for c in range(1,4)]
# one-body source basis
PB=[]
for i in range(3):
 for a in range(1,4):
  ids=[0,0,0];ids[i]=a;PB.append(F.op(*ids))

def K_for(r,h,p):
 # reuse closed-form chain generalized from frozen G,P
 L=G0.herm_log(r);Lp=C.log_frechet(r,h);N=C.A.exp_frechet(L,p);Neta=C.d2exp(L,Lp,p)
 rs=N-r*np.trace(N);res=Neta-h*np.trace(N)-r*np.trace(Neta)
 Q=[]
 for e in G0.EDGES: Q.append(C.polar_all(*C.corr_from_tangents(r,h,rs,res,*e)))
 O=[q[0] for q in Q];Eh=[q[1] for q in Q];Sp=[q[2] for q in Q];M=[q[3] for q in Q]
 K=M[0]@O[1]@O[2]+O[0]@M[1]@O[2]+O[0]@O[1]@M[2]
 K+=Eh[0]@Sp[1]@O[2]+Sp[0]@Eh[1]@O[2]+Eh[0]@O[1]@Sp[2]+Sp[0]@O[1]@Eh[2]+O[0]@Eh[1]@Sp[2]+O[0]@Sp[1]@Eh[2]
 return K.real

def matrix(r):
 return np.column_stack([K_for(r,h,p).reshape(-1) for h in HB for p in PB])

def known_coeffs():
 # G_hidden in HB coordinates and Pz in PB coordinates
 cg=np.array([np.trace(h.conj().T@G0.G).real/8 for h in HB])
 cp=np.array([np.trace(p.conj().T@G0.PZ).real/8 for p in PB])
 return np.kron(cg,cp)

def run():
 rows=[];valid=True;kc=known_coeffs()
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    A=matrix(r);s=np.linalg.svd(A,compute_uv=False);rank=int(np.sum(s>s[0]*1e-10));nullity=243-rank
    recon=(A@kc).reshape(3,3);target=C.closed_K(r).real
    re=float(np.linalg.norm(recon-target)/max(np.linalg.norm(target),1e-15))
    # deterministic orthogonal basis changes represented by signed permutations;
    # right multiplication is orthogonal, so singular spectrum/rank invariant.
    rng=np.random.default_rng(20260926)
    qg,_=np.linalg.qr(rng.normal(size=(27,27)));qp,_=np.linalg.qr(rng.normal(size=(9,9)))
    T=np.kron(qg,qp);s2=np.linalg.svd(A@T,compute_uv=False)
    cov=float(np.linalg.norm(s2-s)/max(np.linalg.norm(s),1e-15))
    valid &= re<=1e-9 and cov<=1e-8
    rows.append({"m":m,"d":d,"a":a,"rank":rank,"nullity":nullity,"quotient_dimension":rank,"singular_values":s.tolist(),"reconstruction_error":re,"basis_spectrum_error":cov})
 ranks=[x["rank"] for x in rows]
 verdict="INVALID" if not valid or len(rows)!=11 else ("STRONG_COLLAPSE" if max(ranks)<=3 else ("PARTIAL_COLLAPSE" if max(ranks)<9 else "FULL_OUTPUT_RANK"))
 return {"fixture_count":len(rows),"input_tensor_dimension":243,"output_dimension":9,"ranks":ranks,"min_rank":min(ranks),"max_rank":max(ranks),"fitted_parameters":0,"controls_pass":bool(valid),"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
