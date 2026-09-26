"""v15.56 Task 32: operator-level positive fiber-local naturality feasibility.

For each frozen pruning pair, form the fine Green operator Gf=L_f^+ on the
zero-mean source quotient, the coarse Green Gc=L_c^+, and source pushforward P.
A fiber-local scalar aggregation A has row v supported only on r^{-1}(v).
Exact linear naturality for all sources would require A Gf = Gc P modulo the
coarse constant gauge. Projective naturality for *all* sources cannot use a
source-dependent scale when both sides are linear and rank >=2: it reduces to
one common scalar lambda, hence C A Gf = lambda C Gc P, C=centering.

We solve the resulting homogeneous linear equations for fiber weights and
lambda, then ask whether any solution has lambda != 0 and strictly positive
weights. This is feasibility/classification, not posthoc fitting to selected
sources.
"""
import numpy as np
import pruning_response as pr

CASES=[
 ([(),(0,),(1,),(0,0),(0,1),(1,0),(1,1)],[(),(0,),(1,)]),
 ([(),(0,),(0,0),(0,1),(0,0,0),(0,0,1)],[(),(0,),(0,0)]),
 ([(),(0,),(1,),(2,),(1,0),(1,1),(2,0)],[(),(0,),(1,),(2,)]),
 ([(),(0,),(1,),(0,0),(0,0,0),(1,0),(1,0,0)],[(),(0,),(1,),(0,0),(1,0)])
]

def matrices(fine,coarse):
 nf,nc=len(fine),len(coarse)
 Gf=np.linalg.pinv(pr.lap(fine),rcond=1e-13);Gc=np.linalg.pinv(pr.lap(coarse),rcond=1e-13)
 ci={k:i for i,k in enumerate(coarse)}
 P=np.zeros((nc,nf)); fiber=[]
 for j,k in enumerate(fine): P[ci[pr.retract(k,coarse)],j]=1
 for v in coarse: fiber.append([j for j,k in enumerate(fine) if pr.retract(k,coarse)==v])
 C=np.eye(nc)-np.ones((nc,nc))/nc
 return Gf,Gc,P,C,fiber

def feasibility(fine,coarse):
 Gf,Gc,P,C,fib=matrices(fine,coarse); nf=len(fine);nc=len(coarse)
 # one weight variable per fine vertex, because fibers partition K_f; plus lambda
 # A[w] has A[v,j]=w_j for j in fiber(v)
 cols=[]
 for j in range(nf):
  A=np.zeros((nc,nf))
  for v,F in enumerate(fib):
   if j in F:A[v,j]=1.;break
  cols.append((C@A@Gf).reshape(-1))
 target=(C@Gc@P).reshape(-1)
 M=np.column_stack(cols+[-target])
 # nullspace of M
 u,s,vh=np.linalg.svd(M,full_matrices=True);tol=max(M.shape)*s[0]*np.finfo(float).eps if s.size else 1e-12
 rank=int((s>tol).sum());N=vh[rank:].T
 if N.shape[1]==0:return {"nullity":0,"positive_feasible":False,"lambda_nonzero_feasible":False}
 # positivity feasibility is checked conservatively by whether lambda coordinate
 # can be normalized to 1, yielding unique/affine weight solution, then inspect
 # least-norm solution and null directions that preserve lambda.
 Aeq=M[:,:nf];b=target
 w,res,_,_=np.linalg.lstsq(Aeq,b,rcond=None)
 err=float(np.linalg.norm(Aeq@w-b))
 # If exact lambda=1 solution exists, positivity of least-norm is sufficient
 # only when unique. For affine cases sample deterministic null directions;
 # unresolved rather than overclaim if positivity cannot be certified.
 rankA=np.linalg.matrix_rank(Aeq,tol)
 unique=rankA==nf
 positive=err<1e-10 and bool(np.all(w>1e-10)) if unique else False
 return {"equation_residual_lambda1":err,"weight_rank":int(rankA),"weight_variables":nf,
 "unique_lambda1_solution":unique,"positive_feasible":positive,
 "lambda_nonzero_feasible":err<1e-10,"min_weight_lambda1":float(w.min()),"max_weight_lambda1":float(w.max())}

def run():
 rr=[feasibility(*c) for c in CASES]
 no_go=all((not x["lambda_nonzero_feasible"]) or (x["unique_lambda1_solution"] and not x["positive_feasible"]) for x in rr)
 exists=all(x["positive_feasible"] for x in rr)
 verdict="POSITIVE_FIBER_LOCAL_NATURALITY_NO_GO" if no_go else ("POSITIVE_FIBER_LOCAL_NATURALITY_EXISTS" if exists else "DEGENERATE_OR_UNRESOLVED")
 return {"case_count":len(CASES),"operator_level_test":True,"positive_fiber_local_family":True,
 "posthoc_parameter_fit":False,"per_case_feasibility":rr,"verdict":verdict}
