"""Corrected mixed-orthogonality skew quotient theorem."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
import response_quotient_rank as R
import closed_form_hidden_response as C
import hidden_response_theorem as A

def first_holonomy(r,dr):
 Cs=[F.corr(r,*e) for e in G.EDGES];Os=[F.polar(c)[0] for c in Cs]
 dCs=[A.corr_tangent(r,dr,*e) for e in G.EDGES];dOs=[A.polar_derivative(Cs[i],dCs[i]) for i in range(3)]
 H=Os[0]@Os[1]@Os[2]
 dH=dOs[0]@Os[1]@Os[2]+Os[0]@dOs[1]@Os[2]+Os[0]@Os[1]@dOs[2]
 return H,dH

def source_state_tangent(r,p):
 L=G.herm_log(r);N=A.exp_frechet(L,p);return N-r*np.trace(N)

def skewcoords(W):return np.array([W[2,1],W[0,2],W[1,0]],float)

def run():
 rows=[];identity_ok=True;controls=True
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    qcols=[];maxid=maxsk=maxrec=0.
    for h in R.HB:
     H,He=first_holonomy(r,h)
     for p in R.PB:
      rs=source_state_tangent(r,p);_,Hs=first_holonomy(r,rs)
      Hes=R.K_for(r,h,p)
      cross=He.T@Hs+Hs.T@He
      ident=H.T@Hes+Hes.T@H+cross
      den=max(np.linalg.norm(Hes),np.linalg.norm(cross),1e-15)
      maxid=max(maxid,float(np.linalg.norm(ident)/den))
      Q=H.T@Hes+.5*cross
      maxsk=max(maxsk,float(np.linalg.norm(Q+Q.T)/max(np.linalg.norm(Q),1e-15)))
      rec=H@(Q-.5*cross)
      maxrec=max(maxrec,float(np.linalg.norm(rec-Hes)/max(np.linalg.norm(Hes),1e-15)))
      qcols.append(skewcoords((Q-Q.T)/2))
    QM=np.column_stack(qcols);s=np.linalg.svd(QM,compute_uv=False);rank=int(np.sum(s>s[0]*1e-10))
    identity_ok &= maxid<=1e-10 and maxsk<=1e-10
    controls &= maxrec<=1e-10
    rows.append({"m":m,"d":d,"a":a,"mixed_identity_residual":maxid,"corrected_skew_residual":maxsk,"reconstruction_error":maxrec,"corrected_rank":rank,"corrected_singular_values":s.tolist()})
 ranks=[x["corrected_rank"] for x in rows]
 verdict="INVALID" if not controls or len(rows)!=11 else ("MIXED_ORTHOGONALITY_IDENTITY_FAILS" if not identity_ok else ("CORRECTED_SKEW_QUOTIENT_THEOREM_VERIFIED" if all(x==3 for x in ranks) else "CORRECTED_SKEW_QUOTIENT_NONSURJECTIVE"))
 return {"fixture_count":len(rows),"directions_total":len(rows)*243,"ranks":ranks,"max_mixed_identity_residual":max(x["mixed_identity_residual"] for x in rows),"max_corrected_skew_residual":max(x["corrected_skew_residual"] for x in rows),"max_reconstruction_error":max(x["reconstruction_error"] for x in rows),"fitted_parameters":0,"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
