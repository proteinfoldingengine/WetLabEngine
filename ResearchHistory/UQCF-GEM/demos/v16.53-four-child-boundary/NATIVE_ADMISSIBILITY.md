# Native admissibility — four-child boundary

Documented before implementation or numerical execution. Analytical proof leads developed while framing this document are disclosed in SCOPE.md; this is not a claim that those leads were prospectively preregistered.

## Carrier and extension
Use the nonempty nested-support category of the accepted v16.52 interface. The new boundary is one ordered parent with FOUR children. Each child initially supplies the accepted interface on an arbitrary finite binary/ternary tree. A proof that joining returns the identical interface would support structural induction with arities 2,3,4; that consequence must be justified, not assumed.

For a finite nonempty ordered palette P, S_root=P. Every vertex has a nonempty support S_v subset P and every child support is contained in its parent. There are no weights, new labels outside P, extra native vertices, simultaneous moves, or physical interpretation.

At internal v, h_v is the minimum size of a label set intersecting every immediate child support. Candidate target q_v is an integer 1 through arity(v). A target profile and palette are EXACTLY ADMISSIBLE only if such a nested state with h_v=q_v exists. Membership in that integer range alone does not establish feasibility on a given palette. Infeasible palettes are excluded by a proved feasibility condition, never by filtering failed constructions.

A legal primitive adds or deletes ONE label incidence at ONE nonroot vertex, preserving nonemptiness, nesting and the fixed global root. Exactness is an endpoint condition; intermediate states remain natively admitted and need not have h=q.

The claimed path budget is sum over ALL internal vertices of |h_v-q_v| <=1 at every primitive. Leaf coordinates contribute zero. Root-support changes at an attached child are legal incidences, and their effect on the four-child parent must be checked. Child normalization can spend its unit only while the parent and all other subtrees are exact.

The independent scalar barriers B1, Binf and Bs keep their inherited meanings; no lexicographic surrogate replaces them. No fundamental time, dynamics, energy, metric, gravity, or dark-matter primitive is introduced.

## Feasibility language, without an assumed width formula
Let a_i be the proved minimum palette width for child i. The compact four-root feasibility question is whether four subsets A_i of a k-label palette, with |A_i|=a_i, have transversal number q. Its equivalence to native nested-state feasibility requires proof.

Use all 15 nonempty incidence regions C subset {1,2,3,4}, with integer multiplicity n_C>=0; root-only labels may occupy the empty region. Then |A_i|=sum over C containing i of n_C. The transversal number is the least number of available region types whose union is all four indices. Repeated labels of the same region type cannot improve a minimum cover. Region multiplicities determine capacity; region support determines the cover number. No ternary width recurrence is extrapolated.

## Decisive obligations
Return the SAME six interface clauses: exact palette feasibility; compact ordered canonical endpoint; finite fixed-root normalization with total excursion <=1; exact-interior role replacement; attached compact contraction; simultaneous label/order equivariance.

Separate:
1. failure of the old proof or a chosen construction;
2. a genuine impossibility of the specified interface;
3. a nonunit barrier, requiring admitted exact endpoints and a lower bound excluding EVERY unit path.

A finite search failure, timeout, or unsuccessful normalization does not establish 2 or 3.
