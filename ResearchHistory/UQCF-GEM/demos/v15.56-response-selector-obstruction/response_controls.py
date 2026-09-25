"""v15.56 Task 24: executable native response controls."""
import numpy as np

def lap(n, edges):
    L=np.zeros((n,n),float)
    for i,j in edges:
        L[i,i]+=1; L[j,j]+=1; L[i,j]-=1; L[j,i]-=1
    return L

def solve(L, source=0, amp=1.0):
    n=len(L); J=np.zeros(n); J[source]=amp; J-=J.mean()
    phi=np.linalg.pinv(L,rcond=1e-13)@J; phi-=phi.mean()
    return J,phi

def normray(x):
    n=np.linalg.norm(x); return x/n if n else x

def run():
    trees=[
      ("path6",6,[(0,1),(1,2),(2,3),(3,4),(4,5)]),
      ("star6",6,[(0,1),(0,2),(0,3),(0,4),(0,5)]),
      ("fork6",6,[(0,1),(1,2),(1,3),(3,4),(3,5)]),
      ("broom6",6,[(0,1),(1,2),(2,3),(3,4),(3,5)])
    ]
    residual=[]; scale=[]; nulls=[]; rays=[]
    for _,n,e in trees:
        L=lap(n,e); J,p=solve(L,0,1.0)
        residual.append(np.linalg.norm(L@p-J))
        _,p7=solve(L,0,7.0)
        scale.append(np.linalg.norm(normray(p7)-normray(p)))
        nulls.append(np.linalg.norm(np.linalg.pinv(L)@np.zeros(n)))
        rays.append(normray(p))
    # deterministic relabel control on fork
    _,n,e=trees[2]; L=lap(n,e); J,p=solve(L,0)
    perm=np.array([3,5,1,4,0,2]); P=np.eye(n)[perm]
    Lp=P@L@P.T; Jp=P@J; pp=np.linalg.pinv(Lp,rcond=1e-13)@Jp; pp-=pp.mean()
    rel=np.linalg.norm(pp-P@p)
    seps=[np.linalg.norm(rays[i]-rays[j]) for i in range(len(rays)) for j in range(i+1,len(rays))]
    return {
      "tree_count":len(trees),
      "max_poisson_residual":float(max(residual)),
      "max_relabeling_error":float(rel),
      "max_projective_scale_error":float(max(scale)),
      "max_null_response_norm":float(max(nulls)),
      "min_nonisomorphic_shape_separation":float(min(seps)),
      "pairwise_shape_separations":[float(x) for x in seps],
      "tree_names":[x[0] for x in trees]
    }
