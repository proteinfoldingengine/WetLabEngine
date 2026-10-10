# Fully saturated crossed-block handover and exact first-vacancy count quotient

Date: 2026-10-10 UTC. Status: OPEN prospective analytical/scope freeze before new scientific execution. Integrated parent: 18343fd432e54ea4453a7b610b55689cfe7ed43c. No fully saturated result is accepted from a finite passing campaign alone.

## Inherited setting
Finite original labelled core C, N active existing labels, positive original floors, tau(C) in{3,4}, fixed disjoint hidden palettes. ALL original protected completions remain fixed. Inherited universal safety iff original floors, current coretau<=4 and every current footprint is contained in an ORIGINAL footprint. Supplied observation/access/addresses, source admission, finite script and actual committed changes remain assumptions. No new native primitive, hidden reads, fundamental time, dark-matter variable or inserted geometry.

## Family
For r>=2, private roots A_i,B_i (i=0..r-1), shared root R and singleton T. Existing labels b,u,v,c_0,...,c_{r-1},y,e, N=r+5. Source:
A_i={b,u,c_i}; B_i={b,v,c_i}; R={u,v,c_0,...,c_{r-1},y}; T={e}.
Every original floor is SATURATED:3 at each private root,r+3 at R,1 at T. Source coretau=3. u,v,e is an actual three-cover. T forces e; no other single label covers both all private roots and R, so no two-cover.

Original maximal footprints are D=all private roots (b); U=all A_i plus R (u); V=all B_i plus R (v); K_i={A_i,B_i,R} (c_i); E={T} (e). They form an antichain for r>=2. y's footprint{R} is nonmaximal, contained in U,V and every K_i; it is not contained in D or E. There are r+4 original maximal types. The original helper is already active and creates slack by allowed additions; no initial slack or absent label is supplied.

## Theorem1: ALL anchored certificates fail
Any original maximal-footprint donor must retain its entire footprint, hence has no anchored expansion. Only y can expand, to ONE containing maximal type U,V or K_i.
Removing any of u,v,c_i,y violates the saturated R floor: every other R donor already occupies R, and b/e cannot add R while retaining their original footprints. Removing e violates T, since no other donor can enter E retaining its nonempty source footprint.
Removing b requires replacing its incidence at EVERY private root. All other donors except y are maximal and cannot add any private incidence. No permitted expansion of y covers every private root. Thus b also has no anchored release. This is failure for every palette label, independent of upper-cover constraints.

## Theorem2: exact static active-label minimum
Let t,a,d,k_0,...,k_{r-1},z be nonnegative multiplicities of D,U,V,K_i,E. A dominated safe core may be expanded within ORIGINAL maximal containers, retaining absent labels. This keeps floors and an at-most-four cover and cannot increase the number of active labels. Conversely such maximal-type assignments with floors and an actual<=4 cover are safe. Constraints:
t+a+k_i>=3, t+d+k_i>=3 for eachi;
a+d+sum_i k_i>=r+3; z>=1.
R and T have disjoint allowable types, so any safe state needs at least r+4 active labels.
For r>=3, t=0,a=r,d=3,k_i=0,z=1 uses r+4 labels, meets every floor and has an actual U,V,E three-cover. Thus kappa=r+4=N-1.
For r=2, a hypothetical N-1=6 active state must have exactly5R labels and1T label, no D label. Every original R-maximal type covers exactly2private roots, so at most10 private incidences are available, while four floor3 roots require12. Hence kappa=N=7. The source itself attains7 (or expand y to U).
Thus r=2 admits safe changing additions but NO safe absent-label state; for r>=3 one static spare exists. No obstruction is inferred just from failure of a script.

## Theorem3: fully saturated first-vacancy construction
For r>=3 select three distinct indices a,beta,c. Use the following actual single toggles in the stated order:
1. Add y at A_a,A_beta,A_c (3 additions).
2. Delete c_a at A_a, then add it at every B_j with j!=a (r changes).
3. Delete c_beta at A_beta, then add it at B_a and B_c (3 changes).
4. Delete c_c at B_c, then add it at every A_j with j!=c (r changes).
5. Delete b at every A_i and B_i (2r changes).
Total achieved cost4r+6. This is NOT a globally minimal native-toggle claim.

Afterstep1, y stays inside U. c_a shrinks to{B_a,R}, then expands inside V. c_beta similarly stays inside V, with only its stated B incidences. c_c shrinks to{A_c,R}, then expands inside U. b only shrinks inside D. All footprints remain originally dominated. u,v,e never change and remain an actual3cover at every slice. The original hidden lower bound therefore survives, and every original protected full completion has EXACT tau3.

Floor accounting: step1 supplies the replacement at A_a,A_beta,A_c. Before c_c loses B_c, both c_a and c_beta have added B_c, raising its size from3 to5; its deletion leaves4. Other new donor incidences supply the remaining replacements for b. Immediately beforestep5 EVERY private root has size4; after removing b EVERY private root has size3, exactly its ORIGINAL floor. R and T never change. At B_c maximum surplus is2, elsewhere at most1 in this chosen order. No floor ever drops or relaxes.

At the endpoint, b is absent, every other original label is active at R or T, and all root cardinalities return to their original saturated values. This is the FIRST vacancy, arising on the final b deletion. Endpoint active countN-1=kappa. It is a concrete fully saturated, statically spare, ALL-anchored-failure nonmonotone positive family. No fixed-cost optimality, unbounded multi-reserve surplus or arbitrary upper-cover handover is newly proved; a persistent actual3cover is used.

The inherited whole-footprint rename interface can move any prescribed occupied label into this absent b, leaving that prescribed label absent. For any release L, inherited arbitrary palette permutation followed by reversepi(L) reaches EXACTLYpi(C), restores every preparatory incidence in its prescribed image, fixes hidden incidences, and renews for finite sequences including permutations moving b. Costs2|L| plus achieved rename cost; no global optimality or native phase-free controller.

## Theorem4: exact count quotient for FIRST reserve availability
This lemma applies to the GENERAL inherited finite setting, not only the family. Let M={M_1,...,M_k} be the original inclusion-maximal nonempty footprints and M_0=empty. A count vertex n=(n_0,...,n_k), sum n_i=N, records actual label multiplicities of maximal types/empty. The associated core must meet original floors and possess an actual cover<=4. Hitting number and floor values depend on multiplicities/types, not label names.
An edge moves one existing label from typei to typej, i!=j,n_i>0: n'=n-e_i+e_j. Require that the MEET core, with the chosen donor footprint replaced by M_i intersection M_j, itself meets floors and admits<=4 actual cover. This criterion is evaluated with all other multiplicities unchanged; an intersection is not replaced by a containing maximum for the gate.

This is exactly the orbit projection of the inherited labelled maximal-assignment graph:
- Every labelled edge projects to this count edge because its meet has these multiplicities plus the actual intersection.
- From EVERY labelled assignment with counts n, a count edge lifts by choosing any label of typei. Its exact meet/floor/cover properties are invariant under relabelling. The inherited delete-to-meet/add-within-container path gives actual safe toggles.
- Any count path consequently lifts from the chosen source expansion; every labelled assignment path projects.
Choose any original-maximal expansion of the source retaining empty labels. Choice-independence of the inherited graph makes the source count component independent of this choice for the vacancy predicate.

A first absent label is reachable iff this source count component contains a vertex n_0>0. By the absent-label rename interface, the same yes/no answer decides reachability of ANY prescribed absent label, without claiming its native optimal cost. Thus the exact source-component minimum active count is min(N-n_0) over that component. Static minimum over ALL count vertices need not lie in the source component.

At most binomial(N+k,k) count vertices replace(k+1)^N labelled assignments. For fixedk this is polynomial inN; k may grow, so no general polynomial efficiency claim. Exhaustive edges/components may still be expensive. Counts do NOT decide exact labelled-target connectivity or optimal raw-toggle costs. Countercontrol: original singleton roots{a},{b},{c}, floors1, same count vector(1,1,1) for a/b-swapped targets, yet source has no safe first toggle and the exact swapped target is unreachable. Do not collapse this distinction.

## Prospective verification contract
1. Familyr=2..5: independently reconstruct complete source/floor/maximal/protected-one-hidden-mask identities and ALL anchored failures for every palette label. Verify all original floors equal source sizes, tau3 and actualu,v,e cover.
2. EVERY ordered triple of distinct indices for everyr=3..5; full4r+6 toggle identities/states, exact declared endpoint, FIRST vacancy at finaltoggle, all original floors and domination, fixed actual3cover, maximum private surplus2 atB_c and<=1elsewhere, final cardinalities exactly original, active countkappa. r2 has genuine safe helper additions but no static vacancy.
3. Independently enumerate EVERY nonnegative maximal-type multiplicity vector with total<=N for eachr=2..5; compare complete admissible-vector identities/canonical witnesses and kappa, not only formulas.
4. Reconstruct COMPLETE count-graph vertices, all unordered gated edges, every component, source count assignment and exact component minimum active count for everyr=2..5. Independently enumerate from the whole vector universe. Every count edge is concretely lifted on a canonical labelled assignment and every intermediate native slice checked; retain complete edge/lift identities. Source graph witness reaches vacancy whenr>=3; arbitraryq/generallemma are proof-based. Omitted vertices, edges, components or native lift identities must reject.
5. Deduplicate original-hidden checks only by exact(r,current-core) identity across source routes/count-edge lifts; retain all per-case route/lift identities and count occurrences separately. Independently reconstruct every original protected mask. Actual lower/upper bounds checked for all such onehidden masks; scripted routes exact3, generic count-edge lifts may3..4.
6. r3, fixed(a,beta,c)=(0,1,2), releaseb: exact prescribed permutation universe is the UNION of all120permutations of working roles{b,c0,c1,c2,y} fixing{u,v,e}, all28palette transpositions, all8full-palette cyclic shifts (identity included), and all6permutations of{u,v,e} fixing working roles. Independently compare complete FULL-palette permutation identities including deduplication, check exact restoration, and three renewed two-permutation sequences with explicit intermediatepi(C), secondpi(L), finalreverse-conjugate restoration; move b and original covering labels. No exhaustive8! claim.
7. Native rejecting control: adding c0 to B1 BEFORE deleting A0 violates original domination. r3 root orderA0,A1,A2,B0,B1,B2,R,T, hidden mask166 (complement of candidate footprint) gives original fulltau3 but candidatefulltau2. Preserve old floors/palette/renewal/fixed-cover controls and wrongoperation/omission rejection.
8. General count-quotient limitation control: singleton roots{a},{b},{c} floors1, same counts for exact swapped destination, all first toggles rejected. No exact-labelled-connectivity claim based only on equal counts.
9. Genuine localRED before implementation; independent implementations; all199inherited tests; exactevent-SHA CI and fresh byte reproduction; internal mathematical/code and separate publication audits; existing Gemini math and separate publication review integration; preserve all originalZIPs/fulljoblogs/rawresponses/manifests/input-output-hashes/retries; author reconciliation and immutable publication readback. CI alone is not scientific closeout.

No newly declared exploration occurs before this freeze. BroadC3/generalC4/nativeobserver-access-source-outcome-progress and arbitrary upper-cover handovers remain OPEN. PathA active; PathB closed. No numbered-stage/full-stack or physical GR certification.
