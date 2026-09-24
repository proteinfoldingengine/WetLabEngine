"""v15.55 exact finite response-space parameterization.

The present frozen data provide one scalar defect coordinate D but no earned
distinguished direction in the seven retained compatibility coordinates.
Therefore the most general Q-linear neutral response is eta(D)=D*c with
c in Q^7. Covariance under the retained diamond automorphism exchanges the
two middle branches, imposing paired coefficients. The remaining frozen
axioms add no normalization of c; classification must report that freedom.
"""
from fractions import Fraction

COORDS=("lineage_left","lineage_right","dependency_left","dependency_right",
        "recoverability_left","recoverability_right","composition")

def _rank_q(rows):
    a=[[Fraction(x) for x in r] for r in rows]
    p=0
    for col in range(len(a[0]) if a else 0):
        s=next((i for i in range(p,len(a)) if a[i][col]),None)
        if s is None: continue
        a[p],a[s]=a[s],a[p]
        u=a[p][col]; a[p]=[x/u for x in a[p]]
        for i in range(len(a)):
            if i!=p and a[i][col]:
                c=a[i][col]; a[i]=[x-c*y for x,y in zip(a[i],a[p])]
        p+=1
    return p

def build_constraint_system(contract):
    if contract.get("exact_arithmetic_required") is not True:
        raise ValueError("exact_arithmetic_required")
    # branch-swap covariance: c0=c1, c2=c3, c4=c5.
    rows=[]
    for a,b in ((0,1),(2,3),(4,5)):
        r=[0]*7; r[a]=1; r[b]=-1; rows.append(r)
    return {
      "schema":"uqcf-v1555-response-system-v1",
      "scalar_field":"Q",
      "coordinates":list(COORDS),
      "variable_count":7,
      "constraint_count":len(rows),
      "constraint_matrix":rows,
      "axioms_encoded":list(contract["axioms"]),
      "neutrality_homogeneous":True,
      "construction":"GENERAL_Q_LINEAR_NEUTRAL_MAP_PLUS_RETAINED_BRANCH_SWAP_COVARIANCE",
      "normalization_constraint_count":0
    }

def classify_exact(contract):
    s=build_constraint_system(contract)
    rank=_rank_q(s["constraint_matrix"])
    dim=s["variable_count"]-rank
    verdict="RESPONSE_NONUNIQUE" if dim>0 else "UNIQUE_CANONICAL_RESPONSE"
    return {
      "primary_verdict":verdict,
      "solution_dimension":dim,
      "variable_count":s["variable_count"],
      "constraint_rank":rank,
      "normalization_constraint_count":0,
      "interpretation":"AXIOMS_LEAVE_RESPONSE_FREEDOM" if dim else "AXIOMS_SELECT_SINGLE_RESPONSE"
    }
