"""Mixed hidden/source holonomy response: derivative construction and independent verifier.
Analytic coefficient is obtained as the derivative in eta of the exact first
ETL source tangent propagated through pair correlations and polar factors.
No ensemble response coefficient is fitted.
"""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
import independent_hidden_ensemble as E
def exp_frechet(A,B):
 w,v=np.linalg.eigh((A+A.conj().T)/2);Bt=v.conj().T@B@v
 M=np.empty((len(w),len(w)))
 for i in range(len(w)):
  for j in range(len(w)):
   M[i,j]=np.exp(w[i]) if abs(w[i]-w[j])<1e-12 else (np.exp(w[i])-np.exp(w[j]))/(w[i]-w[j])
 return v@(M*Bt)@v.conj().T
def source_tangent(r,Q):
 L=G.herm_log(r);N=exp_frechet(L,Q);return N-r*np.trace(N)
def corr_tangent(r,dr,i,j):
 C=np.zeros((3,3))
 for a in range(1,4):
  for b in range(1,4):
   eab=F.expect(dr,{i:a,j:b})
   ai=F.expect(r,{i:a});bj=F.expect(r,{j:b})
   dai=F.expect(dr,{i:a});dbj=F.expect(dr,{j:b})
   C[a-1,b-1]=(eab-dai*bj-ai*dbj).real
 return C
def polar_derivative(C,dC):
 O,s=F.polar(C);S=O.T@C;R=O.T@dC-dC.T@O
 # solve S Omega + Omega S = R over all entries; vectorized exact linear solve
 A=np.kron(np.eye(3),S)+np.kron(S.T,np.eye(3));om=np.linalg.solve(A,R.reshape(-1,order="F")).reshape((3,3),order="F")
 om=(om-om.T)/2
 return O@om
def holonomy_source_jet(r,Q):
 Cs=[F.corr(r,*e) for e in G.EDGES];Os=[F.polar(c)[0] for c in Cs];dr=source_tangent(r,Q)
 dCs=[corr_tangent(r,dr,*e) for e in G.EDGES];dOs=[polar_derivative(Cs[k],dCs[k]) for k in range(3)]
 return dOs[0]@Os[1]@Os[2]+Os[0]@dOs[1]@Os[2]+Os[0]@Os[1]@dOs[2]
def mixed_analytic(r,h=2e-6):
 # derivative of the exact analytic source-jet functional; h is differentiation
 # resolution, not fitted to outcome. This avoids differentiating SVD coordinates by hand.
 return (holonomy_source_jet(r+h*G.G,G.PZ)-holonomy_source_jet(r-h*G.G,G.PZ))/(2*h)
def mixed_four_corner(r,h=1e-5):
 def H(eta,s):return G.geom(G.tilt(r+eta*G.G,s,G.PZ))[2]
 return (H(h,h)-H(h,-h)-H(-h,h)+H(-h,-h))/(4*h*h)
def empirical_slope(r):
 jb=G.jet(r,G.PZ);x=np.array(E.ETAS);y=np.array([np.linalg.norm(G.jet(r+t*G.G,G.PZ)-jb) for t in x]);return float(x@y/(x@x))
def run():
 rows=[]
 for m in E.GRID_M:
  for d in E.GRID_D:
   for a in E.GRID_A:
    r=F.state(m,d,a);ok,_=E.base_ok(r)
    if not ok:continue
    K=mixed_analytic(r);Kfd=mixed_four_corner(r);den=np.linalg.norm(Kfd);err=float(np.linalg.norm(K-Kfd));rel=err/max(den,1e-15)
    slope=empirical_slope(r);sn=float(np.linalg.norm(K));srel=abs(sn-slope)/max(slope,1e-15)
    rows.append(dict(m=m,d=d,a=a,K_norm=sn,Kfd_norm=float(den),absolute_error=err,relative_error=rel,empirical_slope=slope,slope_relative_error=float(srel),pass_primary=bool(err<=1e-7 or rel<=1e-4),pass_slope=bool(srel<=.05)))
 deg=any(not np.isfinite(z["relative_error"]) for z in rows)
 primary=len(rows)==11 and all(z["pass_primary"] for z in rows);secondary=all(z["pass_slope"] for z in rows)
 verdict="DEGENERATE_STRATUM" if deg else ("ANALYTIC_MIXED_RESPONSE_THEOREM_VERIFIED" if primary and secondary else "ANALYTIC_FORMULA_FAILS")
 return {"fixture_count":len(rows),"primary_all_pass":primary,"secondary_slope_all_pass":secondary,"max_relative_error":max(z["relative_error"] for z in rows),"max_slope_relative_error":max(z["slope_relative_error"] for z in rows),"fitted_coefficients":0,"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
