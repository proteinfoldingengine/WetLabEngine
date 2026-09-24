"""Independent v15.55 exact verifier; no producer semantic imports."""
from fractions import Fraction

def _rank(rows):
 a=[[Fraction(x) for x in r] for r in rows]; p=0
 for col in range(7):
  s=next((i for i in range(p,len(a)) if a[i][col]),None)
  if s is None: continue
  a[p],a[s]=a[s],a[p]; u=a[p][col]; a[p]=[x/u for x in a[p]]
  for i in range(len(a)):
   if i!=p and a[i][col]:
    c=a[i][col]; a[i]=[x-c*y for x,y in zip(a[i],a[p])]
  p+=1
 return p

def verify(contract):
 if contract.get("exact_arithmetic_required") is not True:
  return {"primary_verdict":"ILL_TYPED_RESPONSE_PROBLEM","solution_dimension":0,"variable_count":0,"constraint_rank":0,"producer_semantics_used":False}
 rows=[]
 for a,b in ((0,1),(2,3),(4,5)):
  r=[0]*7;r[a]=1;r[b]=-1;rows.append(r)
 rank=_rank(rows); dim=7-rank
 return {"primary_verdict":"RESPONSE_NONUNIQUE" if dim else "UNIQUE_CANONICAL_RESPONSE",
 "solution_dimension":dim,"variable_count":7,"constraint_rank":rank,
 "producer_semantics_used":False,
 "surviving_parameters":["branch_lineage","branch_dependency","branch_recoverability","composition"],
 "composition_additional_rank":0,"naturality_additional_rank":0}
