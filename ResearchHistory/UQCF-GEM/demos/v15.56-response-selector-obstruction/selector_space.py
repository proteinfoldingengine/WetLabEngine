"""v15.56 exact selector-space analysis.

v15.55 leaves the response family Q^4 with basis
(lineage, dependency, recoverability, composition).

This module asks only what the already-earned structures act like on that
quotiented response space.  No downstream curvature behavior is inspected.

At the v15.55 quotient level:
- branch exchange has already been quotiented inside each paired coordinate;
- retained incidence/refinement preserves the four response types;
- composition compatibility constrains admissibility but supplies no map that
  exchanges or weights the four surviving types;
- v15.45 factorization acts downstream on a scalar field and supplies no
  canonical map from the four source-response coefficients into one another;
- Genesis Pin provenance/repair constraints preserve provenance classes but
  supply no relative normalization among these four response coordinates.

Therefore every *earned induced action currently defined on Q^4* is identity.
The exact common invariant subspace is Q^4 itself.  Since no earned
normalization exists, no canonical selector is certified.
"""
from fractions import Fraction

BASIS=("branch_lineage","branch_dependency","branch_recoverability","composition")
STRUCTURES=(
 "RETAINED_INCIDENCE_REFINEMENT",
 "COMPOSITION_COMPATIBILITY",
 "AUTOMORPHISM_NATURALITY",
 "V1545_RESPONSE_FACTORIZATION",
 "GENESIS_PIN_PROVENANCE_REPAIR",
)

def _eye(n=4):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def _rank_q(rows):
    if not rows:
        return 0
    a=[[Fraction(x) for x in r] for r in rows]
    p=0
    n=len(a[0])
    for col in range(n):
        s=next((i for i in range(p,len(a)) if a[i][col]),None)
        if s is None:
            continue
        a[p],a[s]=a[s],a[p]
        u=a[p][col]
        a[p]=[x/u for x in a[p]]
        for i in range(len(a)):
            if i!=p and a[i][col]:
                c=a[i][col]
                a[i]=[x-c*y for x,y in zip(a[i],a[p])]
        p+=1
        if p==len(a):
            break
    return p

def build_selector_action(contract):
    expected=list(STRUCTURES)
    if contract.get("exact_arithmetic_required") is not True:
        raise ValueError("exact_arithmetic_required")
    if contract.get("response_basis")!=list(BASIS):
        raise ValueError("response_basis")
    if contract.get("structures_checked")!=expected:
        raise ValueError("structures_checked")

    actions={name:_eye() for name in STRUCTURES}
    return {
      "schema":"uqcf-v1556-selector-action-v1",
      "scalar_field":"Q",
      "response_dimension":4,
      "basis":list(BASIS),
      "structures_checked":expected,
      "induced_actions":actions,
      "forbidden_inputs_used":[],
      "earned_normalization_rules":[],
      "action_scope":"V1555_QUOTIENT_RESPONSE_SPACE"
    }

def classify_selector_space(contract):
    a=build_selector_action(contract)
    # Invariance equations are (M-I)v=0 for every earned induced action.
    rows=[]
    I=_eye()
    for M in a["induced_actions"].values():
        for i in range(4):
            rows.append([M[i][j]-I[i][j] for j in range(4)])
    rank=_rank_q(rows)
    dim=4-rank
    earned_norm=bool(a["earned_normalization_rules"])

    if dim==0:
        verdict="NO_EARNED_SELECTOR"
    elif dim==1 and earned_norm:
        verdict="CANONICAL_SELECTOR_FOUND"
    elif dim>=1:
        verdict="SELECTOR_NONUNIQUE"
    else:
        verdict="ILL_TYPED_SELECTOR_PROBLEM"

    return {
      "schema":"uqcf-v1556-selector-result-v1",
      "primary_verdict":verdict,
      "invariant_dimension":dim,
      "constraint_rank":rank,
      "invariant_basis":[[1 if i==j else 0 for i in range(4)] for j in range(4)] if dim==4 else None,
      "earned_normalization":earned_norm,
      "earned_normalization_rules":a["earned_normalization_rules"],
      "structures_checked":a["structures_checked"],
      "forbidden_inputs_used":[],
      "scientific_interpretation":
        "CURRENT_EARNED_STRUCTURES_DO_NOT_DISTINGUISH_A_SELECTOR_IN_Q4"
        if verdict=="SELECTOR_NONUNIQUE" else verdict
    }
