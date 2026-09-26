"""Locate the algebraic stage responsible for the certified 243->3 response collapse."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
import response_quotient_rank as R
import closed_form_hidden_response as C

def edge_data(r,h,p):
 L=G.herm_log(r);Lp=C.log_frechet(r,h);N=C.A.exp_frechet(L,p);Neta=C.d2exp(L,Lp,p)
 rs=N-r*np.trace(N);res=Neta-h*np.trace(N)-r*np.trace(Neta)
 return [C.polar_all(*C.corr_from_tangents(r,h,rs,res,*e)) for e in G.EDGES]

def rank(A):
 s=np.linalg.svd(A,compute_uv=False)
 return (int(np.sum(s>s[0]*1e-10)) if s.size and s[0]>0 else 0),s

def run():
 rows=[];valid=True
 rng=np.random.default_rng(20260926)
 qg,_=np.linalg.qr(rng.normal(size=(27,27)));qp,_=np.linalg.qr(rng.normal(size=(9,9)));T=np.kron(qg,qp)
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    edgecols=[[],[],[]];skcols=[[],[],[]];noncols=[[],[],[]];loopcols=[];skloopcols=[];maxrec=0.
    for h in R.HB:
     for p in R.PB:
      Q=edge_data(r,h,p);O=[q[0] for q in Q];Eh=[q[1] for q in Q];Sp=[q[2] for q in Q];M=[q[3] for q in Q]
      for e in range(3):
       edgecols[e].append(M[e].reshape(-1))
       W=O[e].T@M[e];Ws=(W-W.T)/2;Wn=W-Ws
       skcols[e].append((O[e]@Ws).reshape(-1));noncols[e].append((O[e]@Wn).reshape(-1))
      K=M[0]@O[1]@O[2]+O[0]@M[1]@O[2]+O[0]@O[1]@M[2]
      K+=Eh[0]@Sp[1]@O[2]+Sp[0]@Eh[1]@O[2]+Eh[0]@O[1]@Sp[2]+Sp[0]@O[1]@Eh[2]+O[0]@Eh[1]@Sp[2]+O[0]@Sp[1]@Eh[2]
      loopcols.append(K.reshape(-1))
      # replace only mixed edge M by its skew projection; cross terms unchanged
      MS=[]
      for e in range(3):
       W=O[e].T@M[e];MS.append(O[e]@((W-W.T)/2))
      Ks=MS[0]@O[1]@O[2]+O[0]@MS[1]@O[2]+O[0]@O[1]@MS[2]
      Ks+=Eh[0]@Sp[1]@O[2]+Sp[0]@Eh[1]@O[2]+Eh[0]@O[1]@Sp[2]+Sp[0]@O[1]@Eh[2]+O[0]@Eh[1]@Sp[2]+O[0]@Sp[1]@Eh[2]
      skloopcols.append(Ks.reshape(-1))
      maxrec=max(maxrec,float(np.linalg.norm(K-R.K_for(r,h,p))/max(np.linalg.norm(K),1e-15)))
    EA=[np.column_stack(x) for x in edgecols];SA=[np.column_stack(x) for x in skcols];NA=[np.column_stack(x) for x in noncols]
    direct=np.vstack(EA);LA=np.column_stack(loopcols);LS=np.column_stack(skloopcols)
    er=[rank(x)[0] for x in EA];sr=[rank(x)[0] for x in SA];nr=[rank(x)[0] for x in NA];dr,ds=rank(direct);lr,ls=rank(LA)
    skew_recon=float(np.linalg.norm(LS-LA)/max(np.linalg.norm(LA),1e-15))
    # basis covariance on spectra
    _,ds2=rank(direct@T);_,ls2=rank(LA@T)
    cov=max(float(np.linalg.norm(ds2-ds)/max(np.linalg.norm(ds),1e-15)),float(np.linalg.norm(ls2-ls)/max(np.linalg.norm(ls),1e-15)))
    valid &= maxrec<=1e-10 and cov<=1e-8
    rows.append({"m":m,"d":d,"a":a,"edge_ranks":er,"edge_skew_ranks":sr,"edge_nonskew_ranks":nr,"direct_sum_rank":dr,"loop_rank":lr,"skew_only_loop_reconstruction_error":skew_recon,"loop_reconstruction_error":maxrec,"basis_spectrum_error":cov})
 if not valid or len(rows)!=11: verdict="INVALID"
 elif all(max(x["edge_ranks"])<=3 and x["skew_only_loop_reconstruction_error"]<=1e-10 for x in rows): verdict="LOCAL_SYLVESTER_RANK3"
 elif all(x["direct_sum_rank"]>3 and x["loop_rank"]==3 for x in rows): verdict="LOOP_CANCELLATION_RANK3"
 elif all(x["loop_rank"]==3 and max(x["edge_ranks"])<9 for x in rows): verdict="HYBRID_POLAR_LOOP_REDUCTION"
 else: verdict="NO_STABLE_ORIGIN"
 return {"fixture_count":len(rows),"fitted_parameters":0,"controls_pass":bool(valid),"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
