# A11.X7: incidence-derived guards replace the unavailable X5 target

Frozen scope: A11_X7_SCOPE.md at 11da7b687cac61a4b9639e83af3e6bd50c14455b.
Parent publication: 4c2b4007bb309a92f3200468c5d243e497d723cd.
Integrated dependencies: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Analytical theorem, no numerical evidence or implementation.

## 1. Native statements

Fix a finite ordered palette P of size k, r labelled root slots and a uniform ORIGINAL floor h with 1<=h<=k. Supports of every size at least h are allowed. A primitive adds or removes one incidence in one root. Fix feasible exact-q endpoints, q>=3. Temporary incidences and repeated toggles remain permitted.

**Lemma X7G (incidence-derived actual guard).** After exact uniform compaction of an exact-q state E, it has an actual (q-1)-guard on at most

N = floor(r*(k-h)/k)

existing labelled slots. The guard is the complete actual family of roots avoiding one maximum-incidence label. No guard of this size is assumed as input.

**Theorem X7 (uniform incidence criterion).** If 2N<=r, EVERY pair of feasible exact-q endpoints on this carrier admits a finite native path with hitting number in {q-1,q}, preserving all original floors, palette and labelled destination supports.

**Corollary X7H.** If 2h>=k, the criterion holds for every r; hence all feasible exact-q endpoints are connected on every uniform-floor carrier meeting this inequality. This is a sufficient condition, not a necessary threshold.

**Primary corollary X7T.** For k=7, r=12, h=3, EVERY pair of exact-four endpoints admits a finite path in {3,4}, including noncompact states of arbitrary allowed support size. N=floor(48/7)=6 and 2N=12. No cyclic endpoint hypothesis, X5 qualification, common anchor slot, supplied avoiding-triple guard, extra label or new slot is required.

The new ingredient is the availability of a small actual guard derived from exactness and incidence counting. The subsequent compatible-disjoint-guard handover, safe endpoint root permutation and upper-layer removal are inherited accepted tools, not recertified discoveries.

## 2. Exact compaction with an eligible next deletion

Choose a minimum hitting set H of E, of size q. For each support E_i, choose a retained h-subset D_i containing one actual label of E_i intersect H. Such a set exists since |E_i|>=h>=1 and H hits E_i. Delete all labels of E_i outside D_i, one incidence at a time.

Every primitive retains at least h labels and the chosen H label. Deletion cannot decrease hitting number and H remains a q-cover, so every intermediate is EXACT q. If the tuple is not yet compact, some root has an incidence outside its chosen D_i, giving the next deletion. The finite excess-incidence count sum_i(|E_i|-h) decreases by one at each primitive until completion. Original floors and slots do not change. Reversal restores every original noncompact support, in exact q.

Write E* for the compact tuple. It has exactly hr incidences on the fixed k-label palette, including labels unused by some or all roots.

## 3. Actual guard availability from a single omitted label

For any x in P, let d_x count actual roots of E* containing x, and set

I_x = {i : x not in E*_i}.

Suppose the actual family (E*_i : i in I_x) had a hitting set K of size at most q-2. Then K union {x} would hit EVERY root: K hits all roots avoiding x, while x hits every remaining root. Its size is at most q-1, contradicting tau(E*)=q. Thus this actual family has transversal at least q-1. It is nonempty under the feasible q>=3 hypothesis. Its supports still satisfy their original floor h and use only P minus {x}; allowing x in a proposed hitting set supplies no additional coverage.

The incidence identity sum_x d_x=hr guarantees a label x of degree at least ceil(hr/k). Choose a maximum-degree label, breaking ties by the given palette order. The number of roots avoiding it satisfies

|I_x| = r-d_x <= r-ceil(hr/k) = floor(r*(k-h)/k) = N.

This proves X7G. No approximate hitting number or external guard is introduced. The roots avoiding a SINGLE label are different from the roots avoiding an X5 anchor TRIPLE. X6's empty-target result therefore does not exclude this protection.

For the primary target four, this supplies an actual witness for EVERY label pair K subset P: if K hit all the selected roots, it would be a two-cover of their family, contradicting the bound at least three. Therefore some selected labelled root misses K. This includes pairs inside any chosen anchor triple, pairs outside it, and mixed pairs. No separate capacities are assigned to overlapping pair systems.

## 4. Assign the two endpoint guards to disjoint existing slots

Compact A and C independently to A* and C*. Apply X7G at each exact-q tuple, obtaining actual guards on I and J_0 with m_A,m_C<=N. Their omitted labels may differ; no common label or X5 same-slot condition is needed.

The inequality 2N<=r gives r-m_A>=m_C. Consequently at least m_C existing slots lie outside I. Select a set J of that size outside I. Choose a root-support permutation pi of C* sending the guard tokens on J_0 bijectively to J and the other tokens to the remaining slots. Equal supports may be tracked as distinct labelled tokens.

Every compact support has size h and every ORIGINAL floor is h. Thus this entire endpoint permutation is admissible. The full permuted tuple C**=pi(C*) has hitting number EXACT q, and its actual guard on J has the same hitting number as the old guard on J_0.

Inherited OVERLAPPING_CLIQUE_EXCHANGE Lemma M realizes this permutation through a finite sequence of native root swaps in {q-1,q}. Its hypotheses hold: exact-q full endpoint, fixed labelled carrier, and each swapped support meets its destination's original floor. The token-fixing construction has an eligible swap whenever a destination token is misplaced and fixes at least one more slot. This is an endpoint operation at exact q; no bare inexact guard is assumed safely movable.

The root-permutation path will be REVERSED after the middle repair, restoring C*'s original labelled assignment. No palette label is relabelled, no root is created and no floor is weakened.

## 5. Install, hand over protection, and finish the exact destination

Construct a preliminary lower-guard path from A* to C**. First fix each root j in J to its destination support C**_j by the union bridge

current support -> current support union C**_j -> C**_j.

Decompose the bridge into individual additions of destination-only labels, followed by individual deletions of old-only labels. Additions preserve the old support's floor; every deletion stage contains the destination support of size h, so floors hold. Every requested label is present or absent as required. If a root is unfinished, its symmetric difference with the destination is nonempty, furnishing an eligible next primitive: add a missing destination label if any; otherwise delete an old-only label. No completed destination incidence is deleted.

During this first phase, the actual source guard on I remains unchanged because I and J are disjoint. It enforces tau>=q-1 regardless of changes in J. In particular at target four every pair is still missed by a FIXED actual source-guard root.

Once all J roots match C**, their actual destination guard is completely installed. Hold J fixed. Fix EVERY remaining root to C** through the same legal primitive union bridge. This includes the old source-guard slots I. The now-fixed destination guard protects tau>=q-1 throughout. At target four it supplies the missed-root witness for every label pair even while the old guard is removed.

At every middle primitive, the integer

D = sum_i |current support_i symmetric-difference C**_i|

decreases by one. Phase one processes J until its difference count is zero; phase two processes the rest. Any unfinished root has the eligible edit just described, so finite decrease is accompanied by next-move existence. The path terminates exactly at C**, with all original labelled destination tokens restored to their currently assigned slots.

Protection is renewed by actual completed installation of the destination guard before any source-guard root is edited. No return to exact q is required at the handover; a level q-1 state remains usable. Once installed, the new guard supports arbitrarily many subsequent legal root repairs without being modified. This is a complete terminating repair, not just one supplied safe exchange.

This is precisely the inherited AB construction, now unconditionally available in the declared parameter class because X7G supplies appropriately small guards at BOTH endpoints.

## 6. Preliminary upper levels and conversion to the one-unit band

The path in Section 5 is proved to maintain tau>=q-1. It is NOT asserted to stay at or below q. Coexisting guards can produce a larger hitting number. Nevertheless any k-h+1 labels hit every root of size at least h: the remaining palette has only h-1 labels and cannot contain an entire support. Hence the preliminary path is finite and lies between q-1 and k-h+1.

Apply accepted GENERAL_PARENT_CONNECTIVITY Theorem A to this actual finite lower path between EXACT-q endpoints A* and C**. Its fixed width-floor hypotheses are satisfied: all unions and support additions are native-permitted, roots stay nonempty and at their original floors, and both endpoints are exact q. The theorem removes upper excursions while retaining the endpoints and provides a finite primitive path with tau in {q-1,q}.

At k=7,h=3,q=4 the preliminary upper bound is FIVE, so only level five may need removal; its downward replacement bound is 5-2=3. This is an analytical construction, not an executed path-length or efficiency measurement. No supplied-record verification or finite search is used.

Concatenate A's exact compaction, the converted middle path, the reversed Lemma M path from C** to C*, and C's reversed exact compaction. Every piece respects the same native floor carrier, every join is exact q and every primitive stays in {q-1,q}. The final tuple is exactly the original C, including all labels, all labelled slots and every noncompact support incidence. This proves X7.

If 2h>=k, then 2r*(k-h)/k<=r and therefore 2N<=r, proving X7H.

## 7. What this resolves beyond X6 and existing classes

X6 remains fully valid: at seven labels and twelve floor-three slots, no exact-four state meets X5's entry condition at ANY slot. X7 does not reach that empty target. It replaces its protection with the single-label-avoiding guard forced by exact endpoint consistency.

For twelve compact triples, incidence count is 36. Some label belongs to at least six roots, leaving at most six actual roots that require at least three hitting labels. The resulting source and destination guards can be placed on disjoint halves of the EXISTING twelve slots using the accepted endpoint permutation. Native handover is therefore universally available on this carrier.

Accepted AA previously connected cyclic-core endpoints, not every arbitrary exact-four endpoint on the carrier. Accepted AB was conditional on actual compatible disjoint guards; the generic uniform-slot AC bound at h=3,q=4 is twenty (the earlier one-overlap refinement is nineteen), which alone does not settle twelve slots. X7G establishes the missing guard-size availability and closes all endpoints here without a cyclic classification. It does not merely rename an already covered cyclic example.

The same structural argument gives the general uniform incidence criterion. It is sufficient; failure of 2N<=r does not imply any obstruction. For example k=7,h=3,r=13 gives N=7 and fails this DISJOINT criterion; X5 target existence there remains distinct from accessibility, and other accepted results may still apply. No claim is made that a bound of six is optimal or that all seven-label slot counts are now solved.

General mixed floors and other parameter carriers stay outside this theorem unless independently covered by accepted results. No arbitrary mixed-floor root permutation is inferred from uniform admissibility. The same-slot requirement of X5 is neither weakened nor silently used; X7 is a different theorem with different guards.

## 8. Scientific and publication boundary

The actual new statement removes assumed small-guard availability within the declared uniform incidence class. Safety is enforced first by an unchanged source guard and then by an unchanged, fully installed destination guard. Existence of every next primitive and the decreasing symmetric-difference count establish complete middle repair; the inherited finite endpoint permutation, exact compaction reversal and upper-layer conversion establish full original destination restoration.

Frozen dependencies, checked for domain applicability only:
- GUARD_BUFFER_CONNECTIVITY AB: actual guards at two exact-q endpoints on disjoint compatible indices; supplied by X7G and the slot budget.
- OVERLAPPING_CLIQUE_EXCHANGE M: primitive endpoint root permutation with destination-compatible floors; supplied by uniform h.
- GENERAL_PARENT_CONNECTIVITY A: finite lower path with fixed palette/slots/floors and exact-q endpoints; explicitly constructed in Section 5.
Exact compaction and the averaging/guard lemma are proved here. No external mathematical design property, numerical classification, fitting or new native admissibility rule is used.

A11's universal ORIGINAL destination-directed question remains OPEN: compaction, endpoint token reassignment, restoration and upper-layer removal may involve temporary incidences and repeated toggles relative to the original endpoints. The middle's decreasing difference alone is not a directed schedule for the original A,C. General native/nested universality remains OPEN; any native lifting retains the accepted child-interface conditions and is not recertified here.

No new numerical campaign, scientific execution, implementation, tests, workflows, run IDs, numbered version, physical geometry, fundamental time, originality claim or measured efficiency. This is a completed analytical theorem contingent on its exact-source independent review, not merged implementation certification.
