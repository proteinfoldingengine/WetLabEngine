"""v15.56 Task 30: executable fine-prune-coarse rooted-response comparison.

No parameters are fit.  Fine prefix trees are pruned to prefix-closed coarse
sets by ancestral retraction. Extensive sources are pushed forward by fiber
sum. Fine responses are aggregated by fiber mean (the canonical scalar
conditional expectation for counting measure) and compared projectively with
an independently solved coarse response.
"""
import numpy as np

def parent(k): return k[:-1] if len(k) else None
def lap(keys):
 idx={k:i for i,k in enumerate(keys)}; L=np.zeros((len(keys),len(keys)))
 for k in keys:
  p=parent(k)
  if p is not None and p in idx:
   i,j=idx[p],idx[k];L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
 return L
def retract(k,coarse):
 c=[x for x in coarse if len(x)<=len(k) and k[:len(x)]==x]
 return max(c,key=len)
def push(J,fine,coarse):
 out=np.zeros(len(coarse));ci={k:i for i,k in enumerate(coarse)}
 for x,k in zip(J,fine):out[ci[retract(k,coarse)]]+=x
 return out
def aggregate(phi,fine,coarse):
 out=np.zeros(len(coarse));cnt=np.zeros(len(coarse));ci={k:i for i,k in enumerate(coarse)}
 for x,k in zip(phi,fine):
  i=ci[retract(k,coarse)];out[i]+=x;cnt[i]+=1
 out/=cnt;out-=out.mean();return out
def solve(keys,J):
 L=lap(keys);j=J-J.mean();p=np.linalg.pinv(L,rcond=1e-13)@j;p-=p.mean();return p
def ray(x):
 n=np.linalg.norm(x);return x/n if n else x
def run():
 cases=[
  ([(),(0,),(1,),(0,0),(0,1),(1,0),(1,1)],[(),(0,),(1,)]),
  ([(),(0,),(0,0),(0,1),(0,0,0),(0,0,1)],[(),(0,),(0,0)]),
  ([(),(0,),(1,),(2,),(1,0),(1,1),(2,0)],[(),(0,),(1,),(2,)]),
  ([(),(0,),(1,),(0,0),(0,0,0),(1,0),(1,0,0)],[(),(0,),(1,),(0,0),(1,0)])
 ]
 mism=[];srcerr=[];raw=[]
 for fine,coarse in cases:
  J=np.zeros(len(fine));J[-1]=1.0
  pf=solve(fine,J);Jc=push(J,fine,coarse);pc=solve(coarse,Jc);pa=aggregate(pf,fine,coarse)
  m=float(np.linalg.norm(ray(pa)-ray(pc))) if np.linalg.norm(pa)*np.linalg.norm(pc)>0 else float(np.linalg.norm(pa-pc))
  mism.append(m);srcerr.append(abs(J.sum()-Jc.sum()));raw.append(m)
 mx=max(mism)
 if mx<1e-10: verdict="PROJECTIVE_NATURALITY"
 elif min(mism)>1e-6: verdict="SYSTEMATIC_MISMATCH"
 else: verdict="UNSTRUCTURED_FAILURE"
 return {"case_count":len(cases),"max_source_pushforward_error":float(max(srcerr)),
 "max_projective_response_mismatch":float(mx),"min_projective_response_mismatch":float(min(mism)),
 "per_case_projective_mismatch":raw,"verdict":verdict,"fitted_parameters":False,
 "fine_response_coarse_map":"RETRACTION_FIBER_MEAN"}
