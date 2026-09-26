"""SO(3) tangent-image and surjectivity gate."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
import response_quotient_rank as R

def base_H(r):
 Os=[F.polar(F.corr(r,*e))[0] for e in G.EDGES]
 return Os[0]@Os[1]@Os[2]

def skewcoords(W):
 return np.array([W[2,1],W[0,2],W[1,0]],float)

def run():
 rows=[];controls=True;tangent_all=True
 rng=np.random.default_rng(20260926)
 qg,_=np.linalg.qr(rng.normal(size=(27,27)));qp,_=np.linalg.qr(rng.normal(size=(9,9)));T=np.kron(qg,qp)
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    H=base_H(r);A=R.matrix(r)
    V=[];maxsym=0.;maxrec=0.
    for j in range(A.shape[1]):
     K=A[:,j].reshape(3,3);W=H.T@K
     sym=np.linalg.norm(W+W.T)/max(np.linalg.norm(W),1e-15);maxsym=max(maxsym,float(sym))
     Wsk=(W-W.T)/2;rec=np.linalg.norm(K-H@Wsk)/max(np.linalg.norm(K),1e-15);maxrec=max(maxrec,float(rec))
     V.append(skewcoords(Wsk))
    V=np.column_stack(V);s=np.linalg.svd(V,compute_uv=False);rank=int(np.sum(s>s[0]*1e-10))
    s2=np.linalg.svd(V@T,compute_uv=False);berr=float(np.linalg.norm(s2-s)/max(np.linalg.norm(s),1e-15))
    tang=maxsym<=1e-10;tangent_all &= tang;controls &= maxrec<=1e-10 and berr<=1e-8
    rows.append({"m":m,"d":d,"a":a,"max_tangency_symmetric_residual":maxsym,"max_reconstruction_error":maxrec,"projected_rank":rank,"projected_singular_values":s.tolist(),"basis_spectrum_error":berr})
 ranks=[x["projected_rank"] for x in rows]
 verdict="INVALID" if not controls or len(rows)!=11 else ("SO3_TANGENCY_FAILS" if not tangent_all else ("SO3_TANGENT_IMAGE_SURJECTIVE" if all(x==3 for x in ranks) else "SO3_TANGENT_IMAGE_NONSURJECTIVE"))
 return {"fixture_count":len(rows),"column_count_total":len(rows)*243,"projected_ranks":ranks,"max_tangency_residual":max(x["max_tangency_symmetric_residual"] for x in rows),"max_reconstruction_error":max(x["max_reconstruction_error"] for x in rows),"controls_pass":bool(controls),"fitted_parameters":0,"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
