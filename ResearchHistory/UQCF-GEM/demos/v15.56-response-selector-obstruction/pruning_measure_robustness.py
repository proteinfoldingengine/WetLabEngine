"""v15.56 Task 31: robustness of pruning-response defect to fixed aggregation measures.

No weights are optimized. Three a-priori positive fiber measures are used:
uniform counting; depth attenuation 2^-depth; and retained-proximity
attenuation 2^-(depth-depth(root_of_fiber)). Each induces a normalized
conditional expectation on every retraction fiber. The same Task-30 cases,
source pushforward, and response equations are reused.
"""
import numpy as np
import pruning_response as pr

def agg(phi,fine,coarse,kind):
 out=np.zeros(len(coarse)); den=np.zeros(len(coarse)); ci={k:i for i,k in enumerate(coarse)}
 for x,k in zip(phi,fine):
  v=pr.retract(k,coarse); i=ci[v]
  if kind=="COUNTING": w=1.0
  elif kind=="ABS_DEPTH": w=2.0**(-len(k))
  elif kind=="FIBER_DEPTH": w=2.0**(-(len(k)-len(v)))
  else: raise ValueError(kind)
  out[i]+=w*x;den[i]+=w
 out/=den;out-=out.mean();return out

def run():
 cases=[
  ([(),(0,),(1,),(0,0),(0,1),(1,0),(1,1)],[(),(0,),(1,)]),
  ([(),(0,),(0,0),(0,1),(0,0,0),(0,0,1)],[(),(0,),(0,0)]),
  ([(),(0,),(1,),(2,),(1,0),(1,1),(2,0)],[(),(0,),(1,),(2,)]),
  ([(),(0,),(1,),(0,0),(0,0,0),(1,0),(1,0,0)],[(),(0,),(1,),(0,0),(1,0)])
 ]
 kinds=["COUNTING","ABS_DEPTH","FIBER_DEPTH"]; by={k:[] for k in kinds}; serr=[]
 for fine,coarse in cases:
  J=np.zeros(len(fine));J[-1]=1.;pf=pr.solve(fine,J);Jc=pr.push(J,fine,coarse);pc=pr.solve(coarse,Jc)
  serr.append(abs(J.sum()-Jc.sum()))
  for kind in kinds:
   pa=agg(pf,fine,coarse,kind)
   by[kind].append(float(np.linalg.norm(pr.ray(pa)-pr.ray(pc))))
 allm=[x for v in by.values() for x in v]
 if min(allm)>1e-6: verdict="ROBUST_DEFECT"
 elif any(min(v)<=1e-10 for v in by.values()): verdict="NATURALITY_RECOVERED_BY_ADMISSIBLE_MEASURE"
 else: verdict="MEASURE_DEPENDENT_DEFECT"
 return {"case_count":4,"aggregation_family_count":3,"aggregation_families":kinds,
 "per_family_mismatch":by,"global_min_mismatch":float(min(allm)),
 "global_max_mismatch":float(max(allm)),"max_source_pushforward_error":float(max(serr)),
 "verdict":verdict,"fitted_parameters":False}
