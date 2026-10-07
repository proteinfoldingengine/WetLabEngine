# Post-A12 dynamic residual: argument audit and scoped analytical closeout

Date: 2026-10-06 (America/Phoenix).
Disposition: ANALYTICALLY COMPLETE FOR DECLARED RESIDUAL-EDIT UPDATEABILITY.
Evidence: written mathematical proof and exact symbolic counterexample, with author-side whole-argument audit and immutable readback. Not independent peer review, proof-assistant certification, numerical PASS, or physical validation.

## Immutable record

Scope:
- commit 716ff49fe1b1105695945d3ee7e808a927820cfa
- blob f26ea86ac785de490ca78073770521840cbf68be
- POST_A12_DYNAMIC_RESIDUAL_SCOPE.md

Result:
- commit d1aeaeba5ddb6a6748a5a80cb69d5ab76fdf8db7
- blob 61a764852a94f389a9c4a017bf45dfcbb70ef2a6
- POST_A12_DYNAMIC_RESIDUAL_RESULT.md

Parent fixed-residual handover closeout remains ef317a97b72a869bd3c6ceb38a1bc8bb65375090.

## What is established

1. The old Boolean F_R table is not update-closed when a residual root changes. Two states can have the same palette, same labelled residual carrier/count, same floors, same prepared controlled roots, same F_R, same named active-root support and the same two primitive edits, yet the second edit is legal in one state and illegal in the other.
2. The exact retained replacement is the residual miss-count field
       M_R(H)=#{r:S_r intersect H=empty}, 1<=|H|<=4.
3. A declared residual edit S->S' updates every coordinate exactly by
       M'(H)=M(H)-1_{S misses H}+1_{S' misses H}.
   No other residual support is consulted.
4. F_R is derivable from the zero set of M_R, but the counterexample proves F_R does not retain enough multiplicity to update itself exactly.
5. With controlled-root supports retained explicitly:
       global pair witnesses = M_R(K)+controlled misses,
   and H is a global small cover iff M_R(H)=0 and H hits every controlled root.
   Therefore M_R plus the explicit controlled supports reconstructs exactly both target-four band tests.
6. Native syntax, original floor legality and the band can consequently be decided and the retained record updated for any DECLARED single-incidence edit of an explicit controlled root or a named residual root whose current support/floor is supplied and then tracked.
7. The theorem does not select a hidden residual root, discover its unretained support, or prove a terminating route to arbitrary endpoints.

## Audit against frozen obligations

| Obligation | Finding |
| --- | --- |
| F_R insufficiency | Satisfied by the same-record A/B construction on P={a,b,c,d,e}. Both starts and both first-addition states have tau=4; final A has tau=4 and final B tau=5. |
| Same declared input | Same residual slot identities/count, floors, controlled prepared state, active r0={a}, all-true F_R and edit sequence Add b then Del a. Hidden r2 differs only as allowed by the counterexample. |
| Exact M update | Follows by subtracting the named root's old miss indicator and adding its new miss indicator. Other residual contributions cancel identically. |
| F from M | F_R(U) is the existential zero-coordinate predicate over eligible H containing U and at least one additional label. |
| Lower reconstruction | For each pair K, residual missed roots are exactly M_R(K); explicit controlled missed roots add disjointly. |
| Upper reconstruction | H hits the residual family exactly at M_R(H)=0 and the full state exactly when it also hits each explicit controlled root. |
| Floors | Addition cannot violate a positive lower size floor; deletion requires |S|-1>=f for the active root. Controlled-root floors are checked from their explicit support/floor. |
| No hidden full-state read | Updates require only M plus the named active root support. No other S_r is consulted. Activation/discovery of a hidden root remains explicitly outside scope. |
| Edge cases | Empty R gives M=0; k=4 retains all nonempty H; saturated deletion is rejected locally; addition/deletion sparse formulas are explicit. |
| Compression/minimality | Correctly NOT claimed. Coordinate count and integer width are disclosed. |
| Route selection | Correctly NOT claimed. The theorem certifies supplied declared edits and updates the record only. |

## Counterexample details rechecked

State A residuals: {a},{a},{b}; State B: {a},{a},{c}; controlled anchors {d},{e}; guards {a,b,c} twice.

Before editing, A residuals have cover {a,b} and B residuals cover {a,c}. Any unordered pair U can be extended by the relevant two-set to size at most4; when U already equals that two-set, append a third palette label. Hence both F tables are all true.

The controlled anchors force d,e. A additionally forces a,b; B forces a,c. Both initial tau values are4.

After r0 becomes {a,b}, A still forces a,b and B still forces a,c, so both tau values remain4.

After deleting a from r0, A residuals {b},{a},{b} force a,b, giving tau4. B residuals {b},{a},{c} force a,b,c in addition to d,e, giving tau5. Final B has F({d,e})=0 because any residual cover containing d,e must also contain a,b,c and therefore has size5.

No computation is needed for these claims.

## Exact advancement

The fixed-residual theorem showed that existential residual-cover information is sufficient while residual roots never change.

This result shows why that information stops being sufficient and identifies the additional retained distinction required for exact one-root updates: MISS MULTIPLICITY, not merely existence of a residual cover.

The same miss-count field simultaneously supplies:
- pair-witness multiplicity for the lower bound;
- zero-miss cover status for the upper bound.

That unifies the retained certificate needed for declared dynamic residual edits.

## Remaining frontier

The next unresolved problem is SELECTION/COMPLETION, not updateability.

A broader controller must specify how it chooses a residual root and obtains/retains that root's current support without an undeclared global read, then prove that its legal choices terminate at a stated exact endpoint class.

A legitimate next theorem should therefore separate:
1. information initialization;
2. active-root identification/support access;
3. primitive legality;
4. retained-record update;
5. route selection;
6. termination/exact destination.

The present result closes items 3-4 once item2 supplies the named active root. It does not close items2,5-6.

Closed A12.1-A12.5, certified v16.54/v16.55 and accepted A11 sources remain unchanged. No A12.6, physical force, geometry, energy, GR/ADM, dark-matter replacement, continuum, observer field, physical nonlocality or fundamental time is inferred.
