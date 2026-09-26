"""Preregistered ensemble replication/scaling gate."""
import json,numpy as np
import independent_hidden_fixture as F
import independent_hidden_geometry as G
GRID_M=[.10,.15,.20];GRID_D=[.08,.12,.16];GRID_A=[.04,.08,.12];ETAS=[.001,.002,.003]
def base_ok(r):
 mine=float(np.linalg.eigvalsh(r).min());Cs=[F.corr(r,*e) for e in G.EDGES]
 cyc=max(np.linalg.norm(Cs[i]-Cs[0]) for i in (1,2));ps=[F.polar(c) for c in Cs]
 smin=min(x[1].min() for x in ps);H=ps[0][0]@ps[1][0]@ps[2][0];h=F.angle(H)
 return mine>=.03 and cyc<=1e-12 and smin>=.02 and h>=.20,dict(min_eigenvalue=mine,cyclic_pair_difference=float(cyc),pair_singular_min=float(smin),holonomy_angle=h)
def run():
 rows=[];bases=[]
 for m in GRID_M:
  for d in GRID_D:
   for a in GRID_A:
    rb=F.state(m,d,a);ok,meta=base_ok(rb)
    if ok:bases.append((m,d,a,rb,meta))
 allcontrols=True;allmatched=True
 for m,d,a,rb,meta in bases:
  jb=G.jet(rb,G.PZ); vals=[]
  for eta in ETAS:
   rh=rb+eta*G.G;mine=float(np.linalg.eigvalsh(rh).min())
   if mine<.01:continue
   _,Ob,Hb=G.geom(rb);_,Oh,Hh=G.geom(rh)
   vis=G.marginal_diff(rb,rh);pd=max(np.linalg.norm(Ob[i]-Oh[i]) for i in range(3));hd=np.linalg.norm(Hb-Hh)
   jh=G.jet(rh,G.PZ);D=float(np.linalg.norm(jh-jb));vals.append((eta,D))
   matched=vis<=1e-12 and pd<=1e-10 and hd<=1e-10;allmatched &= matched
   idn=max(np.linalg.norm(G.jet(rb,G.ID)),np.linalg.norm(G.jet(rh,G.ID)))
   scale=np.linalg.norm(G.jet(rh,2*G.PZ)-2*jh)
   ctrl=idn<=1e-7 and scale<=1e-5;allcontrols &= ctrl
   rows.append(dict(m=m,d=d,a=a,eta=eta,D=D,hidden_min_eigenvalue=mine,matched=bool(matched),controls=bool(ctrl)))
  if len(vals)==3:
   x=np.array([v[0] for v in vals]);y=np.array([v[1] for v in vals]);slope=float(x@y/(x@x));res=float(np.linalg.norm(y-slope*x)/np.linalg.norm(y))
   # sign control at .003
   rp=rb+.003*G.G;rm=rb-.003*G.G;sg=np.linalg.norm((G.jet(rp,G.PZ)-jb)+(G.jet(rm,G.PZ)-jb));allcontrols &= sg<=1e-5
   for z in rows:
    if (z["m"],z["d"],z["a"])==(m,d,a):z["scaling_slope"]=slope;z["scaling_relative_rms"]=res;z["sign_residual_003"]=float(sg)
 eligible=[b for b in bases if any(z["m"]==b[0] and z["d"]==b[1] and z["a"]==b[2] and z["eta"]==.003 for z in rows)]
 d3=[z["D"] for z in rows if z["eta"]==.003]; scale_fixtures={}
 for z in rows:
  if "scaling_relative_rms" in z:scale_fixtures[(z["m"],z["d"],z["a"])]=z["scaling_relative_rms"]
 scale_pass=sum(v<=.05 for v in scale_fixtures.values()); scale_frac=scale_pass/max(1,len(scale_fixtures))
 replication=len(bases)>=6 and len(d3)==len(bases) and all(x>1e-6 for x in d3) and float(np.median(d3))>1e-3
 controls=allcontrols and allmatched
 verdict="INVALID_ENSEMBLE" if not controls else ("ROBUST_LINEAR_HIDDEN_GEOMETRY_RESPONSE" if replication and scale_frac>=.9 else ("ROBUST_NONLINEAR_HIDDEN_GEOMETRY_RESPONSE" if replication else "ENSEMBLE_NULL"))
 return {"base_fixture_count":len(bases),"evaluated_rows":len(rows),"replication_pass":bool(replication),"median_D_003":float(np.median(d3)) if d3 else None,"min_D_003":float(min(d3)) if d3 else None,"max_D_003":float(max(d3)) if d3 else None,"scaling_eligible_count":len(scale_fixtures),"scaling_pass_count":scale_pass,"scaling_pass_fraction":scale_frac,"matched_inputs_all_pass":bool(allmatched),"controls_all_pass":bool(allcontrols),"parameters_fit_to_verdict":0,"verdict":verdict,"rows":rows}
if __name__=="__main__":print(json.dumps(run(),indent=2,sort_keys=True))
