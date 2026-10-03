# A11.X21 — floor-compatible protection transplantation and complete mixed-floor repair

Scope: 92a0a2eda05bb6e0cbf61bedbbe52d37736fe622.
Parent analytical publication: 93ee269982201902fe0f365daf51b2b81e9a1fdd.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Analytical candidate for fresh independent WHOLE-ARGUMENT review.

## 1. Native setting and exact statements

Fix a finite ordered palette P with k labels, r labelled original slots and positive ORIGINAL floors a_i<=k. Each support is a subset of P of size at least its own a_i. A primitive adds or removes ONE incidence in ONE existing root. Temporary larger supports, background edits and repeated incidence changes remain native. Endpoints have transversal EXACTLY FOUR.

Write S=sum_i a_i and b=max_i a_i. A three-guard is an ACTUAL selected subfamily of existing roots with transversal at least three. No floor is strengthened or weakened by this proof.

**Lemma X21A (floor-compatible hub access).** Suppose a specified full exact-four tuple Q on the SAME carrier has an actual three-guard on m slots, and EVERY full hub support has size at least b. Compact an arbitrary exact-four endpoint E exactly to its own original floors, and let d be its maximum label degree. If d>=m-1, there is a finite native path E->Q with tau in {3,4}, restoring the SAME ORIGINAL FULL LABELLED hub Q. Thus every two endpoints satisfying this condition connect with complete original labelled/noncompact destination restoration. The endpoint-independent sufficient condition is ceil(S/k)>=m-1.

The condition on full hub supports supplies compatibility for every support-token assignment. It does not license arbitrary permutations of mixed compact supports. We deliberately do NOT compact the hub to the unequal original floors before aligning it.

**Theorem X21W (mixed-floor wide-palette repair).** For arbitrary positive original floors with maximum b>=2, EVERY exact-four pair has complete native{3,4} repair if

r>=b+3 and k>=3b+1.

There is NO degree or S/k hypothesis in this theorem: exact incidence access and accepted palette-room AE cover complementary alternatives. The exact hub has a minimum three-slot three-guard.

**Theorem X21H (mixed-floor small-guard module repair).** For arbitrary positive original floors with maximum b>=2, put t=ceil(b/4). EVERY exact-four pair has complete native{3,4} repair if

r>=8, k>=7t+b, and ceil(S/k)>=3.

An explicit eight-slot exact-four hub has an actual FOUR-slot three-guard. Every full hub token has size at least b. This extends the accepted X20 module without assuming equal endpoint floors.

**Theorem X21M (large-palette mixed-three/four closure).** For EVERY original floor profile a_i in {3,4}, EVERY exact-four pair has complete native{3,4} repair on each of these broad domains:
- k>=13, with ANY r;
- k=11 or12, with r>=8.

Each positive branch restores EVERY original labelled/noncompact destination. Feasibility of each parameter tuple is not asserted. Unrestricted mixed-three/four repair on smaller palettes and the omitted smaller arities is NOT claimed.

**Corollary X21L (cover-automatic extension).** At k>=13, EVERY exact-four pair has complete repair whenever each original floor is at most FOUR OR at least k-2. Arbitrarily many high-floor slots are allowed, with no whole-carrier incidence-budget condition.

These are complete root-level repair results, with a defect upper bound of one, not a positive minimum for every pair. Original A11 destination-directed universality, arbitrary mixed floors, higher targets and unrestricted nested repair remain open.

## 2. Why the original compatibility obstacle is real

Baseline OVERLAPPING_CLIQUE_EXCHANGE Lemma M implements any FULL exact endpoint support permutation whose final supports meet the destination floors. It does not say every permutation of unequal compact supports is admissible. A compact floor-three support cannot be assigned to an original floor-four slot.

Accepted X12/X20 accessibility avoids this issue under UNIFORM floors by compacting both endpoints before placing guard tokens. Applying that recipe unchanged to unequal floors is invalid.

Instead construct an exact hub whose full support tokens ALL fit ALL original slots. Its support sizes may exceed some original floors. The native carrier permits this. Keep those full supports throughout the permutation; compact only the arbitrary input endpoint to its OWN original floors. This is a proof device within the original carrier, not a change to the carrier or its floor vector.

The compatibility observation was disclosed before proof development in A11_X21_SCOPE.md. The mechanism composes accepted M/O1/A rather than claiming a new local swap rule.

## 3. Exact source compaction and derived actual protection

At an arbitrary exact-four input E, choose an actual minimum four-label cover H_E. In each support choose a_i labels including one label of H_E that hits that root. This is possible since the root has size>=a_i and meets H_E. Delete all other incidences individually.

Each deletion preserves the ORIGINAL a_i floor. Deletion cannot lower tau; H_E still hits every root, so each intermediate tuple remains EXACT FOUR. Whenever excess remains, an incidence outside the chosen retained subset is an eligible next deletion. Total excess strictly decreases. Save this finite path's reverse, which restores every original incidence.

The resulting exact compact tuple E* has S ACTUAL incidences. Some actual label x has degree d>=ceil(S/k). Let I be ALL roots avoiding x, occupying r-d existing slots.

If I had a cover of at most two labels, append x to produce a cover of E* of at most three labels, contradicting exact four. Thus I is an ACTUAL three-guard. This covers every palette pair, not just pairs in an active hub palette. It is an endpoint exactness implication and is not reused at an arbitrary deficient prefix.

The condition d>=m-1 says there are at least m-1 existing slots OUTSIDE this actual source guard. It is a placement count attached to identified supports, not a total-coverage proxy for lower protection.

## 4. Full exact hub permutation on unequal original floors

Let J_0 be the specified m-slot actual guard of Q. Choose m-1 slots outside I and put that many distinct hub guard tokens there. Put the last guard token outside I too if another outside slot exists; otherwise put it in one I slot. Extend this injection to a bijection of ALL r hub tokens and slots. Equal supports may remain distinct tokens.

Every token has size>=b>=a_i at every destination, so the full permuted tuple Q' is legal at the ORIGINAL mixed floor vector. Support permutation preserves exact-four transversal. Its guard on J satisfies |I intersect J|<=1.

Here is the actual eligible permutation move, supplied by baseline M. Process slots in decreasing ORIGINAL floor order, with ordered tie-breaks. At an unfinished slot j, its desired token is in some unfixed slot i. The desired token fits j because the final full assignment is legal. The token currently in j has size>=a_j>=a_i, and so fits i. Swap those two FULL supports by expanding each to their union, then contracting each to its new support through individual incidences.

The union tuple has hitting number at least three: any cover of the two unions hits at least one original support, and adding one label from the other repairs it to a cover of the old exact-four tuple. During expansion every tuple contains the old endpoint; during contraction it contains the new exact-four endpoint; every tuple is contained in the union tuple. Hence all primitives have tau in {3,4}. Floors hold because expansion retains the original support and contraction retains the legal new one.

Each completed swap fixes another slot and moves no already fixed slot. Finite token-fixing progress supplies termination at Q'. Save the ENTIRE permutation path's reverse Q'->Q. This is a path between FULL EXACT FOUR tuples, not permutation of a bare level-three guard.

In this construction all hub tokens already fit all slots, but the decreasing-floor argument also checks the actual general M domain. No source floor-three token is assigned to a floor-four slot.

## 5. Every forbidden pair, primitive availability and renewed completion

Use the actual source guard I at E* and the actual destination guard J at Q'. Define the comparison family D on I union J:
- source support E*_i on I minus J;
- destination support Q'_j on J minus I;
- E*_s union Q'_s on the possible shared slot s.

If overlap is empty D contains the old guard. If there is one shared slot, take any palette pair K. If it misses an exclusive support, that actual support witnesses protection. Otherwise K meets all exclusive supports. The actual source guard forces K to miss E*_s and the actual destination guard forces it to miss Q'_s. It therefore misses their union. Thus EVERY pair has an actual missed support in D. Singletons and the empty set follow by padding inside P, possible since exact four implies k>=4.

The finite LOWER schedule is actual O1:
1. Hold all I supports fixed. At each J-minus-I slot add missing Q' incidences, then delete old-only incidences after its destination support is present.
2. If s exists, add its missing destination incidences to reach E*_s union Q'_s, then delete old-only incidences. During this stage every I-union-J support is a subset of its corresponding D support. Any pair missed by D remains missed by the current support in that same existing slot.
3. Hold the fully installed J guard fixed while repairing every remaining original slot to its exact Q' support through its own union.

At preparation the unchanged source guard witnesses every forbidden pair. At handover the actual comparison family witnesses them. At final repair the installed destination guard witnesses them. This accounts for mixed anchor/residual pairs, pairs entirely inside a hub module, private labels and unused palette labels without separate fictitious capacity systems.

Each addition retains the current legal source support. Each deletion retains the complete legal destination support in that ORIGINAL slot. No incidence outside P is used and no simultaneous root/block change is a primitive.

At each unfinished scheduled root there is a missing destination incidence to add, or an old-only incidence to delete once the destination is present. That is an eligible next primitive by the floor and guard arguments above. The sum of differences from Q' decreases by ONE at each such primitive. The finite ordered phase/slot schedule terminates at the exact full Q'.

Renewal occurs BEFORE editing the remaining old-guard roots: all of the actual destination guard is already installed. The tuple can still carry hitting number three during this handover; exact four need not be restored after each intermediate stage. The restored destination guard is sufficient for every subsequent scheduled edit. No arbitrary safe-prefix completion is inferred.

## 6. Upper conversion, same full hub return and exact destination

The constructed middle schedule is finite and keeps tau>=3; its upper excursions can exceed four. Apply baseline GENERAL_PARENT_CONNECTIVITY Theorem A ONLY between its actual exact-four endpoints E*,Q'. The original carrier has fixed positive mixed floors and is closed under additions/unions, exactly A's domain. It gives a finite native{3,4} path between the SAME endpoints. The converted path can change the schedule; no path length, computational efficiency or destination-monotonicity property is inferred.

Append the saved reverse FULL exact hub permutation Q'->Q. Source compaction E->E* was already exact four. We have therefore reached the SAME ORIGINAL FULL LABELLED hub Q. No hub compaction reverse is needed, because the full hub was never compacted.

For arbitrary original exact endpoints A,C satisfying the lemma, independently construct A->Q and C->Q with their actual source compactions/guards/permutations. Reverse the complete second leg and concatenate at the identical exact tuple Q. This restores C*, followed by the saved destination compaction reverse, giving EVERY original labelled/noncompact support of C. Different source labels and different hub placements do not change the common full Q.

All joins are exact four. Repeat for any finite chain of endpoints in the proved class; no protection deficit accumulates. The exact-completion theorem is thus stronger than a local safe move or the existence of one supplied repeatable exchange. Sections3-6 prove X21A.

## 7. Max-floor wide hub and exhaustive incidence/palette alternatives

Let b>=2, r>=b+3 and k>=3b+1. Select disjoint existing label sets S_0,U,V of sizes b+1,b,b. Put ALL b-subsets of S_0 in the first b+1 slots, U and V in the next two, and duplicate one core support in every later original slot.

Every full hub support has size b and fits EVERY original slot. A singleton core label misses its own complementary b-root, while every pair of distinct core labels hits all core roots. The core has hitting number exactly two. The disjoint private roots each require one additional label, so the full hub Q has transversal EXACT FOUR. Supply two distinct core labels and one from each private root as an actual minimum four-cover.

ONE core root, U and V are three pairwise disjoint ACTUAL roots and have transversal three. They form the hub guard, m=3. Every palette pair misses at least one of these three supports. Extra palette labels and duplicate padding do not change these facts.

If k<S, exact input compaction has more than k incidences. Some label has degree at least two. X21A applies with m-1=2 and supplies complete access to this SAME full hub for every exact endpoint.

If k>=S, accepted PALETTE_SLACK_CONNECTIVITY Theorem AE applies at the ORIGINAL mixed floors, since S is their sum. It directly connects any exact-four endpoints; alternatively it connects them to Q. Its actual input compaction, unused-existing-label split, finite increasing active-label measure, full legal label permutation and upper conversion provide the complete path and restoration. It uses no extra labels. This alternative does not claim that the input has degree two.

These two cases are exhaustive, proving X21W WITHOUT an incidence hypothesis. The hub has larger supports than some original floors, but this does not increase S: S is used only to count the source's actual original-floor compaction. We do not substitute the b*r hub incidence count for the source count.

This removes the uniform-original-floor assumption from the accepted wide-hub mechanism. Original floors remain in their own slots and are never reassigned.

## 8. Max-floor small-guard module without compact-token reassignment

Let b>=2,t=ceil(b/4), k>=7t+b and r>=8. Use the accepted X20 explicit complement pattern:

R1=4567, R2=2367, R3=2345, R4=1357, R5=1346, R6=1256, R7=1247.

Choose seven disjoint existing t-label blocks B1..B7, and an existing disjoint b-label private support V. Replace each index of R_j by its full block to form module support Q_j of size4t>=b. Slot8 is V; later slots duplicate a module support. Every full token fits every original floor.

For completeness, the complementary triples123,145,167,246,257,347,356 contain every index pair exactly once: the other-index pairs on triples containing1..7 are respectively
(23,45,67), (13,46,57), (12,47,56), (15,26,37), (14,27,36), (17,24,35), (16,25,34).
Each row partitions the six other indices. An actual complementary module root therefore misses every two-index set. The index set124 hits all module supports because it is not one of those triples. Thus the index module is EXACT THREE.

Projecting an actual cover of the fixed block module to its used block indices, and choosing an existing representative for a converse index cover, proves the actual module also has transversal three. This is a property of THIS hub, not a general clone/path equivalence. Pick representatives from B1,B2,B4 and one from V to supply a minimum four-cover of the full hub. Private disjointness raises the hub to EXACT FOUR.

The first three module roots have empty common intersection and a two-cover represented by indices2,6. Together with V they supply an ACTUAL FOUR-slot three-guard. For every palette pair using at most one module label, one of the first three roots is missed. A pair using two module labels misses V. Outside/private/unused labels are included in this classification.

If ceil(S/k)>=3, X21A supplies arbitrary exact endpoint access with m=4. Keep the supports of size4t and b throughout full exact token placement; do NOT shrink them to some original a_i before permutation. Native handover additions/deletions preserve the actual a_i in each slot, and full Q is restored. This proves X21H.

The uniform special case S=br was already accepted in X20H. The new conclusion concerns genuinely unequal original floors under the ACTUAL source incidence count S.

## 9. Broad mixed-three/four composition

Let every a_i belong to{3,4}.

### Palettes at least thirteen, every root count

If any original floor-four slot exists then b=4; otherwise uniform floor-three X15 already applies. For r>=7 and k>=13, X21W applies with b4. For uniform floor3 it also applies at r>=7, but X15 covers that class universally. The hub uses seven size-four supports; none of the original floors are changed.

For r=6, every label at an exact-four endpoint has degree at most THREE: x plus one label from each avoiding root is a cover of size at most7-d, so exact four forces d<=3. Compact exactly to the ORIGINAL mixed floors. Its incidence count S<=24<2k when k>=13. Apply accepted X15N with M3,D2,r6:
D<=M, S<=Dk, r6>=D+M+1=6.
The total slack is strict, so no saturated condition is needed.

X15's protected leveling supplies an actual above-two donor, below-two recipient and a row containing the former but missing the latter whenever excess remains. Pairs containing the added recipient meet at most D+M=5<6 roots; other pairs retain old missed-root witnesses. Finite excess decreases. The arrival need not be exact four.

Its strict incidence construction supplies a greedy transfer or full cycle, an existing cycle-row or OUTSIDE-row buffer, and restoration of the borrowed incidence. Every pair meets at most2D=4<6 roots in that middle construction. Completed macros reduce pending differences and renew degree/balance capacity. Saved destination leveling and compaction restoration yield a complete LOWER path between the ORIGINAL exact endpoints, then A gives the band. Original floors remain in place; no mixed token permutation is used in this six-slot branch.

For r=5 accepted baseline F gives complete arbitrary-positive-floor exact-four repair including both strict and saturated alternatives. For r=4, exact four forces all four supports pairwise disjoint: a label shared by two, plus one label from each remaining root, would give a three-cover. Every feasible endpoint is therefore in protected J's domain, with its original mixed floors. For r<4, choosing one label per root proves exact-four infeasibility.

These branches exhaust ALL root counts at every k>=13 and prove the first part of X21M. This is a broad mixed-profile theorem, not a campaign or a claim each carrier is feasible.

### Eleven/twelve labels, at least eight roots

At k11,r>=8, S>=3r>=24>2k, so ceil(S/k)>=3. At k12,r>=9, S>=27>24 likewise. At k12,r8, any genuine profile containing a floor-four slot has S>=25>24; the sole excluded arithmetic case has all original floors3 and is already universally closed by X15. If all original floors4, X20U also already applies.

For b4, the module t1 requires7t+b=11 labels and eight slots. X21H therefore supplies complete repair on EVERY genuine mixed-three/four profile in these domains. Uniform cases remain inherited. This proves the second part of X21M.

No claim is made for k11/12 with the omitted small arities, or for general mixtures on k7..10. Some are already covered by accepted sufficient classes and must be checked individually before being labelled unresolved; the new theorem does not turn those tuples into an enumeration agenda.

## 10. Large cover-automatic supports and exact restoration

At k>=13, suppose each original floor is at most4 OR at least k-2. Retain the slots J with original floors below k-2; hold all other full-carrier slots B fixed.

At a full exact-four endpoint the retained family is EXACT FOUR: any retained cover of at most three can be extended to three labels, which hit every B root because each has complement size at most two. It would be a full three-cover, a contradiction. A full minimum four-cover also covers the retained family, giving the matching upper bound. Thus retained exact endpoint theorems are invoked only after this exactness proof. An empty retained family makes full exact four impossible.

The retained original floors are1..4. If one is1 use accepted X3; if one is2 use accepted X4; otherwise they are3/4 and X21M at k>=13 gives complete repair for every retained root count. No whole-carrier S condition is needed.

Lift this retained band path in the SAME existing slots while holding B fixed. A retained cover of size3 or4 hits every B root, so full transversal equals the retained value at every primitive. Every forbidden pair misses an actual retained root in the full carrier.

When the retained destination is exact four, repair each B support through its union with its ORIGINAL labelled destination: add missing incidences, then delete old-only incidences. Its floor>=k-2 makes it meet every three-set throughout; the retained exact-four family supplies the lower four bound and its minimum cover supplies the full upper four bound. These final restoration primitives therefore remain EXACT FOUR.

Each unfinished large support supplies a missing or excess incidence and decreases symmetric difference. This ends at every original support, not merely a projection. The lift is positive/sufficient only; unrestricted full safe paths need not project to retained band paths. No arbitrary mixed-floor token reassignment or negative projection argument occurs. This proves X21L through accepted X17L.

## 11. A genuine mixed control beyond whole-carrier degree repair

On P={1,...,13}, r7, take original floors

(4,4,4,4,4,4,3)

and full supports

2345,1345,1245,1235,1234,6789,10-11-12.

Here the last notation means the three labels{10,11,12}; label13 is unused. The first five roots are ALL four-subsets of the five-label core{1,...,5}, of hitting number two. The two private roots require one label each. Therefore the tuple is EXACT FOUR with supplied minimum cover{1,2,6,10}. Every root is already at its own floor, so its exact floor compaction is UNIQUE and equals itself.

Its total original incidence is S=27 and maximum degree is4. Any X15N application to this control must use M>=4 and satisfy r7>=D+M+1, forcing D<=2. But S27>2k26 contradicts S<=Dk. Thus NO whole-carrier X15N parameter choice applies. X14's r>=2D+2 also fails for any cap D>=4. The actual avoiding-label guard at label1 has exactly three disjoint roots2345,6789,{10,11,12}, so no avoiding-guard lower bound g>3 is valid for this control; X16R with g3 likewise fails its incidence budget.

No original floor is1 or2, no root is cover-automatic at threshold11, and the profile is genuinely mixed, so X3/X4, the uniform universal X15/X20 conclusions and the X17/X20L automatic-profile reductions do not themselves establish universal repair of this profile.

X21M DOES establish complete repair for EVERY exact endpoint pair on this same carrier, regardless of whether either endpoint has the displayed modules, three disjoint guard roots or any input special structure. Its new max-floor hub has ALL private supports size4 and hence fits every original slot; it uses existing label13 as needed. The floor-three slot is allowed to have larger support during the path.

This control demonstrates removal of the whole-carrier incidence-budget and uniform-floor assumptions. It is not asserted to fail every older conditional guard construction: for particular endpoint pairs an actual O1/union bridge may already suffice. Its module shape is familiar from accepted results; the new content is guaranteed arbitrary endpoint access and full restoration at the MIXED ORIGINAL floor vector.

## 12. Consolidated discovery and inherited domains

The obstruction was not an inability to store protection at a mixed endpoint. It was that compact destination guard tokens could fail their reassigned slot floors. Creating FULL hub tokens that meet every original floor supplies compatible placement without changing any native floor.

The complete explanation has five distinct obligations:
1. create an exact-four hub and its actual three-guard, with a supplied minimum four-cover;
2. derive an actual input avoiding-label guard at an exact compact endpoint;
3. align full exact hub tokens using permitted swaps, with a proved outside-slot budget;
4. renew protection before editing remaining roots, supplying actual witnesses and eligible finite progress;
5. return to the same full hub and reverse the destination leg, restoring exact original labelled supports.

A small local certificate is not substituted for all five. The preliminary lower schedule and maximum-layer converted path are distinct. A restored level-three guard can sustain progress; exactness is required at the declared endpoints and full joins, not after every primitive.

Frozen dependency domains:
- Baseline exact compaction, maximum-layer A and arbitrary-positive-floor five-root F: GENERAL_PARENT_CONNECTIVITY.md at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
- Full exact endpoint-permutation M: OVERLAPPING_CLIQUE_EXCHANGE.md at that baseline; final support compatibility is explicitly supplied.
- Palette-room AE: PALETTE_SLACK_CONNECTIVITY.md at that baseline; applied only when k>=sum ORIGINAL floors.
- Protected J: PROTECTED_EXCHANGE.md at that baseline; exact-four r4 endpoints are proved protected.
- Actual one-overlap O1: GUARD_HANDOVER.md at parent93ee269982201902fe0f365daf51b2b81e9a1fdd; arbitrary positive floors, actual guards and exact endpoints supplied.
- X12's explicit wide module and X20's explicit complement module: read at the parent. Their support facts are restated; uniform input accessibility is not silently applied to mixed endpoints.
- X15S/L/N: read at the parent; six-slot branch checks strict S<2k, D2,M3 and r6. Inexact entries are used only for the explicit LOWER construction before full-path A.
- X17L: read at the parent; retained exact-four endpoints and full positive lift are proved before invocation. X3/X4 are used only when the retained original floor-one/two slot actually exists.

Accepted frozen sources are checked for applicability, not rewritten or recertified. X15/X20 universal uniform root closures remain unchanged. The scope discloses already-known reasoning; no originality or external design dependency is claimed.

Unrestricted mixed-three/four on remaining smaller domains, higher original floors outside sufficient classes, general higher targets, original A11 stricter destination-directed universality and unrestricted nested repair remain OPEN. Conditional root-to-child lifting retains the inherited exact-child interfaces and fixed-root clearance; no universal nested conclusion follows here. Use ordered repair/retained recoverability; no fundamental time, physical metric/energy/gravity or inserted geometry.

Analytical only. No numerical enumeration, scientific tests/workflows/run IDs, implementation, benchmark, numbered v16.55 certification or certified integration merge. Certified v16.54 and accepted separate efficiency baseline/design remain unchanged; runner implementation/fixture execution/measured speedup remain unstarted.
