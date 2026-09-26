"""Decompose the certified rank-three response image into canonical matrix sectors."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
import response_quotient_rank as R

def base_H(r):
 Os=[F.polar(F.corr(r,*e))[0] for e in G.EDGES];return Os[0]@Os[1]@Os[2]
def sectors(v,H):
 K=v.reshape(3,3);M=H.T@K
 tr=np.trace(M).real/3;T=tr*np.eye(3);W=(M-M.T)/2;S=(M+M.T)/2-T
 return T,W,S
def flat(X):return X.reshape(-1)
def rank(M):
 s=np.linalg.svd(M,compute_uv=False);return int(np.sum(s>s[0]*1e-10)) if s.size and s[0]>0 else 0
def run():
 rows=[];valid=True
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    A=R.matrix(r);H=base_H(r);U,s,_=np.linalg.svd(A,full_matrices=False);B=U[:,:3]
    PT=[];PW=[];PS=[];rec=0.
    for j in range(243):
     K=A[:,j].reshape(3,3);M=H.T@K;T,W,S=sectors(A[:,j],H)
     rec=max(rec,float(np.linalg.norm(M-(T+W+S))/max(np.linalg.norm(M),1e-15)))
    # project each image basis vector, then return to K-frame
    for q in range(3):
     T,W,S=sectors(B[:,q],H);PT.append(flat(H@T));PW.append(flat(H@W));PS.append(flat(H@S))
    PT=np.column_stack(PT);PW=np.column_stack(PW);PS=np.column_stack(PS)
    Pimg=B@B.T
    def leakage(X):
     return float(np.linalg.norm((np.eye(9)-Pimg)@X)/max(np.linalg.norm(X),1e-15))
    lt,lw,ls=leakage(PT),leakage(PW),leakage(PS)
    rt,rw,rs=rank(PT),rank(PW),rank(PS)
    energies=np.array([np.linalg.norm(PT)**2,np.linalg.norm(PW)**2,np.linalg.norm(PS)**2]);energies=energies/energies.sum()
    valid &= rec<=1e-12
    rows.append({"m":m,"d":d,"a":a,"trace_rank":rt,"skew_rank":rw,"symtr_rank":rs,"trace_energy_fraction":float(energies[0]),"skew_energy_fraction":float(energies[1]),"symtr_energy_fraction":float(energies[2]),"trace_image_leakage":lt,"skew_image_leakage":lw,"symtr_image_leakage":ls,"reconstruction_error":rec})
 # classify globally using exact-ish projector preservation threshold
 pure_skew=all(x["skew_image_leakage"]<=1e-10 and x["trace_energy_fraction"]<=1e-20 and x["symtr_energy_fraction"]<=1e-20 for x in rows)
 pure_sym=all(x["symtr_image_leakage"]<=1e-10 and x["trace_energy_fraction"]<=1e-20 and x["skew_energy_fraction"]<=1e-20 for x in rows)
 invariant_all=all(sum(v>0 for v in [x["trace_rank"],x["skew_rank"],x["symtr_rank"]])>=2 and all(z<=1e-10 for z in [x["trace_image_leakage"],x["skew_image_leakage"],x["symtr_image_leakage"]] if np.isfinite(z)) for x in rows)
 verdict="INVALID" if not valid or len(rows)!=11 else ("PURE_SKEW" if pure_skew else ("PURE_SYMMETRIC_TRACELESS" if pure_sym else ("MIXED_INVARIANT_DECOMPOSITION" if invariant_all else "IRREDUCIBLY_MIXED_IMAGE")))
 return {"fixture_count":len(rows),"fitted_parameters":0,"controls_pass":bool(valid),"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
