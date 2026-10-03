# A11.X8: complete repair with incidence guards sharing at most one slot

Frozen scope: A11_X8_SCOPE.md at 8010f4e04b616d89cc2227cd53f7960a502d5af6.
Parent publication: 7b475d5c904fb5bbba1888b9944be98ee1ad74b1.
Inherited X7G candidate: 4e0eee45107e54d6059d00b846a666fd0cd6c00d.
Inherited O1 candidate: fa71695118731da7f0e17bf8a31f0142e4c76267.
Integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Analytical composition, no implementation or numerical campaign.

## 1. Exact statements

Fix finite ordered P of size k, r labelled slots, uniform ORIGINAL floor h, and feasible exact-q endpoints A,C with q>=3. Every support size at least h is permitted; a primitive toggles one incidence in one root. No extra labels or slots, weakened floors or simultaneous edits.

Put N=floor(r*(k-h)/k).

**Theorem X8.** If r>=2N-1, every such endpoint pair has a finite native path in {q-1,q}, restoring every original labelled destination support, including all noncompact incidences.

**Endpoint-sensitive form X8E.** Compact A and C exactly to uniform size h, retaining their respective supplied minimum covers. Let d_A,d_C be maximum label incidence degrees in the two compact tuples. If d_A+d_C>=r-1, the same conclusion holds for this pair, even if the universal sufficient inequality fails.

The new result is a checked composition of X7G actual small-guard availability with inherited O1. Neither the original O1 handover nor X7G is recertified or relabelled as a new discovery.

**Primary corollary.** Every exact-four endpoint pair on seven labels and uniform original floor three is connected in {3,4} for r=13,15,17, with no X5 guard or cyclic hypothesis.

| r | N=floor(4r/7) | 2N-1 | Disjoint X7 sufficient? | X8 sufficient? |
| --- | ---: | ---: | --- | --- |
| 13 | 7 | 13 | No | Yes |
| 15 | 8 | 15 | No | Yes |
| 17 | 9 | 17 | No | Yes |

X7 already closed r=12. Failure of either inequality is inconclusive; other accepted results and actual smaller guards still apply.

## 2. Exact endpoint preparation and actual guard hypotheses

At each endpoint, choose its minimum q-cover H. Retain an h-subset of each actual root containing an H label; delete all excess incidences individually. Floors hold and H remains a q-cover; deletion cannot decrease tau, so every compaction primitive is EXACT q. Whenever excess remains, a label outside the retained h-set supplies an eligible next deletion. The finite excess count strictly decreases. Reversal restores all original labels and supports.

Write A*,C* for the compact exact-q tuples. By accepted X7G, the actual family avoiding a maximum-incidence label is a (q-1)-guard: a cover with at most q-2 labels plus the omitted label would otherwise hit the full exact-q tuple. The two actual guards occupy index sets I,J_0 of sizes

m_A=r-d_A, m_C=r-d_C,
m_A,m_C<=N.

These families are nonempty and in fact contain at least q-1 roots, since choosing one label from each root would be a cover. They are existing labelled roots at their original floor. Their omitted labels can differ, and no common X5 anchor slot is required.

## 3. Place the destination guard with zero or one overlap

Either theorem hypothesis gives r>=m_A+m_C-1: the universal condition follows from m_A,m_C<=N; the endpoint-sensitive condition follows from

m_A+m_C-1=2r-d_A-d_C-1<=r.

Therefore at least m_C-1 slots lie outside I.

If at least m_C slots lie outside I, choose J disjoint from I. Otherwise exactly m_C-1 outside slots are available and one existing slot s in I completes J, with I intersect J={s}. The source guard is nonempty, so s exists. Every choice uses only existing indices.

Permute the root-support tokens of C* so its guard occupies J. Complete the token assignment arbitrarily on other existing slots. Equal supports may be tracked as distinct tokens. Uniform original floors h make the permutation admissible, and the full permuted tuple C** is exact q.

Accepted baseline OVERLAPPING_CLIQUE_EXCHANGE Lemma M supplies a finite native path from C* to C** in {q-1,q}. Every swap meets both destination floors, and its token-fixing schedule has an eligible swap whenever a destination is unfinished. The operation is on full exact-q endpoints, not on an unprotected bare guard at q-1. Its REVERSE is saved for final restoration of C*'s original labelled slots.

No palette permutation, added label or mixed-floor reassignment is assumed.

## 4. The actual shared-slot comparison guard

Let K=I intersect J. On I union J define actual-support comparison tuple D by

D_i=A*_i for i in I minus J,
D_j=C**_j for j in J minus I,
D_s=A*_s union C**_s if K={s}.

For K empty, D contains the fixed source guard, so tau(D)>=q-1.

For K={s}, suppose H with at most q-2 labels hit every support of D. H would hit every exclusive source support. Because the source guard on I needs at least q-1 hitting labels, H must MISS A*_s. Likewise H hits every exclusive destination support, so the destination guard forces H to MISS C**_s. H therefore misses their union D_s, contradicting that H hits D.

Thus tau(D)>=q-1. At target four, this statement supplies an actual missed support for EVERY label pair in the comparison tuple, including anchor-only, residual-only and mixed pairs. No assertion that the exclusive roots alone form a guard is needed.

This is exactly accepted GUARD_HANDOVER O1's argument and domain. It applies to these supplied actual guards on at most one shared index. It does NOT infer intersecting miss sets for two or more shared slots.

D is a comparison family of support sets, not an extra native slot or a simultaneous primitive. The construction below realizes its shared union by individual legal additions.

## 5. Prepare, hand over the shared root, and finish

Construct a finite preliminary path from A* to C** with tau>=q-1.

First fix each j in J minus I to C**_j through individual additions of destination-only labels and deletions of old-only labels. All roots on I remain unchanged and form the fixed source guard. A union-bridge addition contains the old support; every subsequent deletion contains the destination h-support, so floors hold.

If K={s}, expand A*_s to A*_s union C**_s one incidence at a time, then contract it to C**_s one incidence at a time. Exclusive source roots retain A*_i, and exclusive destination roots already have C**_j. At every shared primitive, the support tuple on I union J is componentwise contained in D. Shrinking supports cannot decrease transversal, so that actual subfamily has tau>=tau(D)>=q-1 throughout. Floors hold from the old support during expansion and the new support during contraction. At target four, the support missing a given pair in D has a current actual subset still missing that pair, proving all pair witnesses during the handover.

Now every root in J agrees with C**, giving the completed actual destination guard. Hold J fixed and repair every remaining root to its destination via the same primitive union bridge. The destination guard protects every subsequent edit, including changes to old source-guard roots.

For each unfinished root, a missing destination incidence is a legal next addition; if none remains, an old-only incidence is a legal next deletion. No finished destination incidence is removed. The integer

D_target=sum_i |current_i symmetric-difference C**_i|

strictly decreases by one at EACH middle primitive. Phase one finishes J minus I; the shared phase finishes s if present; phase three finishes the remaining slots. Every phase has an eligible edit whenever its target is unfinished. Thus progress is finite and reaches the EXACT tuple C**, not merely its hitting number.

Protection is renewed by the actual complete installation of J. Exact q need not reset at the handover; q-1 protection suffices to finish every subsequent root. This is complete repair, not just safety of one supplied exchange or arbitrary safe-prefix completion.

## 6. Upper excursions and original labelled restoration

The preliminary path has tau>=q-1, not necessarily tau<=q. At uniform floor h, every k-h+1 labels hit every root, so its upper bound is k-h+1. In the primary k7/h3/q4 class this is five. Do not report the preliminary {3,4,5} allowance as the final one-unit band.

Apply accepted GENERAL_PARENT_CONNECTIVITY Theorem A to the actual finite lower path between exact-q endpoints A* and C**. It preserves fixed palette, labelled slots and original floors, and removes upper excursions to produce a finite path in {q-1,q}. All its hypotheses have been furnished rather than inferred from endpoint counts alone.

Concatenate source exact compaction, the converted middle path, the reversed accepted endpoint root-permutation path from C** to C*, and destination reversed exact compaction. Each join is exact q and every component stays in {q-1,q}. The final configuration is the ORIGINAL C, restoring every labelled support and every noncompact incidence. This proves X8 and X8E.

The normalization is constructive in the inherited finite-path sense, not a new path-length efficiency claim or executed numerical certificate.

## 7. Nonvacuity and the seven-label remaining domain

Accepted X6 provides an explicit exact-four thirteen-slot state on seven labels with floor three. Filling two or four additional EXISTING slots with P gives exact-four states at r=15 or 17: P is redundant and meets the same floor. Thus the three primary carriers are feasible; the new theorem covers every endpoint on each, not just these illustrative states.

X8 neither reaches nor assumes X5 qualification. X6's target-existence threshold and X7's twelve-slot repair remain unchanged. Native connectivity is distinct from accessibility of a chosen X5 class.

At k=7,h=3,q=4, the X8 incidence criterion holds at every r from 4 through 13 and at r=15,17,19. This is an all-FEASIBLE-endpoints statement; it does not assert endpoint existence at every smaller r. The arithmetic follows directly from N=floor(4r/7). Accepted original uniform O1 bound uses binomial(5,3)=10 and therefore covers EVERY r>=19, regardless of failure of the incidence inequality at some larger r.

Consequently, within the seven-label uniform-floor-three target-four problem, any remaining universal carrier obligation is confined to r=14,16,18, before further exclusion of accepted endpoint classes. This is not an enumeration instruction, a claim every such carrier is wholly unresolved, or evidence of disconnection. Some endpoint pairs may satisfy X8E or earlier cyclic, symmetry, bridge or other conditions.

For example at r=14, maximum compact degrees d_A+d_C>=13 already suffice for that pair; analogous thresholds are fifteen at r=16 and seventeen at r=18. These are actual degree-input conditions, not universal average guarantees.

Larger palettes, arbitrary mixed floors and multiple-shared-slot guards remain outside this composition unless covered by other accepted results.

## 8. Scientific scope and dependencies

X8 removes ONE required disjoint guard slot from X7's incidence-derived sufficient budget. The same guard availability is retained; inherited O1 supplies the shared-root protection. This is incremental analytical progress, not a new fundamental handover principle or originality claim.

Frozen dependency domains:
- X7G: exact uniform compaction and actual single-label-avoiding guard availability, with at most N roots; no X7 disjoint criterion is imported where it fails.
- GUARD_HANDOVER O1: actual endpoint guards on index sets whose intersection has at most one slot. The comparison guard and every primitive are checked explicitly here; the prior independent receipt accepts its frozen source.
- Baseline M: native permutation of full exact endpoints with destination-compatible floors, supplied by uniform h.
- Baseline A: an actual finite lower path between exact-q endpoints on the original width-floor carrier, supplied in Section 5.

These are applicability checks, not recertification. No unchanged implementation or certificate is rerun. Original A11 universal destination-directed scheduling remains OPEN, since compaction, endpoint permutation and upper conversion can introduce temporary incidences and repeated changes relative to A,C. General native/nested universality remains OPEN; native lifting retains accepted child-interface conditions.

No numerical enumeration, campaign, scientific execution, implementation, tests, workflows, run IDs, numbered version, extra native primitive, geometry, fundamental time, physical implication or measured efficiency. Exact-source independent review and final immutable publication verification are required before completion is reported.
