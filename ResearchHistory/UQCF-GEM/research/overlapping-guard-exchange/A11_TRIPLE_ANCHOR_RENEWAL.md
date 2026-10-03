# A11.X5: triple-anchor renewal at saturated residual capacity

Frozen analytical candidate under A11_TRIPLE_ANCHOR_SCOPE.md. Fixed finite palette P, labelled root slots, ORIGINAL positive floors a_i, single-incidence moves, and all floor-permitted intermediate sizes. No numerical evidence or implementation is used.

## 1. The declared sufficient condition

**Theorem X5.** Let A and C have transversal exactly four on the same carrier. Suppose the same distinguished slot s has ORIGINAL floor a_s=3. At EACH endpoint E supply:

- a three-label subset T_E of E_s;
- a four-label hitting set H_E of E with T_E intersect H_E nonempty;
- the actual family M_E of all other roots disjoint from T_E, with transversal at least TWO on R_E=P minus T_E.

Then A and C admit a finite primitive path entirely in {3,4}, respecting all original floors, palette and slots and restoring every labelled destination support. Temporary incidences and repeated toggles are allowed.

The actual guard condition is equivalent to: for every x in R_E, some root of M_E misses x. Its positive supports are already subsets of R_E. It is NOT implied by the presence of a floor-three slot alone, and is not an assertion about all floor-three exact endpoints.

Dependencies: baseline GENERAL_PARENT_CONNECTIVITY.md Lemma C and OVERLAPPING_CLIQUE_EXCHANGE.md Lemma L, at integrated baseline 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f under ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/. X4's residual upper-band argument is used with its hypotheses verified below; X4's universal floor-two input condition is NOT invoked. The main theorem constructs the band directly; upper-excursion removal is unnecessary.

## 2. Exact compaction and alignment

At each endpoint delete from E_s every incidence outside the supplied T_E. At every deletion the floor three holds, H_E still hits the selected root, and all other roots are unchanged. Deletion cannot decrease transversal, while H_E still bounds it by four; every compaction primitive is exact four.

Use inherited Lemma L to align the compact triple to a common T={a,b,c} by a global palette permutation. The permutation is a finite word of transpositions; each completed stage is exact four and each primitive lies in {3,4}. Track the permuted four-cover H. No original slot or floor changes. Destination compaction/alignment will be reversed at the end.

Put R=P minus T and n=|R|. Let M be the aligned actual roots avoiding T. Their complementary blocks Q_i=R minus E_i cover R, so their residual transversal g is at least two. Since H meets T, H_R=H intersect R has size at most three and hits M. Thus g is two or three. In particular n>=2, H_R is nonempty, and M is nonempty. T and M occupy disjoint label sets, so their combined transversal is exactly 1+g>=3.

## 3. Common residual carrier and safe preparation

Define the SAME nonanchor index sets at both endpoints by ORIGINAL floors:

F={i not s: a_i<=n}, Z={i not s: a_i>n}, c_i=n-a_i for i in F.

Each c_i is nonnegative and at most n-1. M is a subset of F. Keep the triple root T and every actual M root fixed. For each i in F minus M move E_i to R by the union bridge E_i -> E_i union R -> R, decomposing additions and deletions individually. Expand each Z root to P. Both bridge endpoints meet original floors. Fixed T+M protects the lower bound three throughout.

The old four-cover H hits every expansion through the old support, every contraction through R and H_R, and every expanded Z root. It hits T. Therefore every preparation primitive also has transversal at most four.

At completion all F roots are inside R and all Z roots equal P. The F roots newly equal to R add no constraint to the nonempty residual cover of M. Residual transversal is still g in {2,3}. For ANY subsequent permitted residual tuple on F, with T fixed and Z=P, exact additivity gives full transversal 1+residual transversal. Original floors, labelled indices and the common residual carrier are identical for both endpoint preparations.

Coverage at either endpoint gives n<=sum_M |Q_i|<=sum_M c_i<=sum_F c_i. The two possible capacity regimes must be treated separately; strict slack is not assumed.

## 4. Strict slack: inherited owner transfers with a checked upper band

If sum_F c_i>=n+1, apply inherited Lemma C to the residual complementary covers of R. Zero capacities are allowed. For completeness, its extra upper-band obligation is as follows.

Remove duplicate block occurrences until each label has one owner. Block deletions are support additions, so residual transversal does not increase; element coverage keeps it at least two. At an owner partition, no bin can hold all n labels because c_i<=n-1. At least two bins are nonempty. Labels from different bins form a two-cover of all complementary supports; every singleton is missed at its owner. Thus residual transversal is exactly two.

Each owner transfer adds its label to the new block before deleting it from the old block. The sole duplicated-owner intermediate is one legal support deletion from a level-two partition and raises transversal by at most one: take an old two-cover and add any label of the still-positive edited support if necessary. Capacity and coverage persist. The buffer case in Lemma C performs TWO completed transfers, returning to a partition between them; it does not compound the upper bound. The spare space is in an existing bin.

When adding target duplicate occurrences, every intermediate block is contained in its target block, so its complementary support contains its target support. Hence residual transversal is at most the target level, at most three, while coverage maintains at least two. The fixing count in inherited C gives finite progress. Every residual primitive lies in {2,3}, and exact additivity lifts it to {3,4}.

## 5. Saturation forces existing three-root capacity reserves

Now suppose sum_F c_i=n. Equality in the chain in Section 3 forces:

- all M blocks are at their full capacities and partition R;
- every F minus M slot has c_i=0 and ORIGINAL floor a_i=n;
- every positive-capacity F slot belongs to M.

In the prepared tuple, positive-capacity blocks form this owner partition; zero-capacity F supports are R. The prepared full level is exactly three. Since every c_i<=n-1, choose source labels x_0,y_0 from DIFFERENT nonempty owner bins.

Return conceptually to the aligned exact-four source BEFORE preparation; do not execute a move backward. For each t in T the triple {t,x_0,y_0} cannot hit every root. Choose an actual root j_t missing it. It is not s. It is not M, because no partition block contains both x_0,y_0. It is not Z: a Z support has size at least n+1, whereas a support avoiding these three labels has size at most |P|-3=n.

Therefore j_t belongs to F minus M and has ORIGINAL floor n. Its support avoids three labels in a palette of size n+3, so the floor forces it to be EXACTLY

(R minus {x_0,y_0}) union (T minus {t}).

The three slots j_a,j_b,j_c are DISTINCT because these three forced supports differ. Thus three EXISTING zero-residual-capacity slots are derived from exact-four coverage. No slack, slot or label is invented. Their prepared supports are all R. Once derived, these same slots can be reused for EVERY subsequent owner swap, not only the source pair.

## 6. The renewing swap, with every primitive checked

Suppose a current owner partition has x in bin i and y in a DIFFERENT bin j. Define for each t in T:

B_t(x,y)=(R minus {x,y}) union (T minus {t}), of size n.

First build the three reserves at the original j_t slots through

R -> R union (T minus {t}) -> B_t(x,y),

adding the two anchor labels, then deleting x and y, one incidence at a time. Each support has size at least its ORIGINAL floor n. The unchanged T+owner partition has transversal three and protects all these primitives. Capacity is borrowed through permitted anchor attachments, not through a new residual bin.

With all three B_t installed, exchange the two owners in FOUR individual support moves:

1. add x to support i (remove x from its old block);
2. add y to support j (remove y from its old block);
3. delete y from support i (give y to block i);
4. delete x from support j (give x to block j).

At the block level the two removals free the original capacities before the two insertions. All original support floors hold. No other owner is changed. Every possible label pair remains missed somewhere:

- a pair inside R misses the fixed triple root T;
- a pair inside T misses any positive-capacity F root, all of whose support labels lie in R throughout the edits;
- a pair {t,z} with z outside {x,y} misses its unchanged owner root;
- {t,x} and {t,y} miss B_t(x,y).

This also covers hitting sets of size at most two: in the palette of size at least five, each such set extends to a pair, and a missed pair witnesses its missed subset. Thus full transversal remains at least three, including the stage when x and y have temporarily lost their residual owners. The final blocks are again a saturated partition, with x and y swapped and no other label moved.

Restore each reserve by the reverse union bridge

B_t(x,y) -> R union (T minus {t}) -> R.

The completed owner partition and T again supply the fixed lower guard three; both bridge endpoints have size n. All three ORIGINAL reserves are restored for the next exchange.

The upper bound is checked independently. Choose ANY two distinct anchor labels u,v in T. During this entire reserve-build/swap/restore word, {u,v,x,y} hits every root. T meets u,v. Every reserve bridge support contains either R or B_t; the former meets x,y and the latter meets {u,v}, since any two-element subset of a three-element T meets T minus {t}. Other zero-capacity F roots equal R, and Z roots equal P. Positive-capacity F blocks contain neither both x and y initially nor both during or after the four owner edits, so their supports meet {x,y}. Therefore every primitive has transversal at most four. Counts alone are not being used to assert exact four at reserve stages: their level is proved only to lie in {3,4}. Completed owner partitions with restored reserves are exactly three by additivity.

## 7. Available swaps and finite progress at saturation

The destination prepared blocks are also a partition with exactly c_i labels in every bin. Let a misplaced label x currently be in bin i with desired bin j. Since current and desired bin j have the SAME cardinality c_j, and j lacks x, bin j contains a label y not desired there. Choose that y. The bins are distinct and both nonempty.

Apply Section 6 using the SAME three reserve slots to swap x and y. Label x becomes correct; y was already misplaced, so no correctly placed label is displaced. Every other owner is unchanged. The number of misplaced labels decreases by at least one. After at most n swaps every owner agrees with the destination. Each swap includes reserve restoration, ensuring the next permitted swap remains available. This gives global termination at saturation, rather than merely safety of a supplied exchange.

Zero-capacity bins own no labels at either endpoint and remain R after every word. The Z roots remain P. Therefore the entire prepared destination is restored exactly, not just its cover count.

## 8. Assemble the path and state the boundary

Concatenate source compaction/alignment/preparation, the appropriate strict-slack or saturated residual route, and the REVERSE destination preparation/alignment/compaction. Every primitive has already been bounded in {3,4}. Every stage has a finite word and the middle has an explicit finite progress measure. Reversal retains every floor and band check. This proves Theorem X5 with exact original labelled endpoint restoration.

The saturated regime has NO spare residual capacity. Protection is renewed instead by three endpoint-forced roots whose original floors allow temporary anchor attachments. These roots protect the two temporarily ownerless labels against all three anchor choices, then return to their prepared supports after every swap. This is a sufficient overlapping-protection renewal mechanism; it is not universal availability of the needed actual avoiding family.

For the six-label carrier of all twenty triples, fixing any triple T leaves only the complementary triple R avoiding it, with residual transversal ONE. Thus it fails X5's guard hypothesis. This is not an obstruction to its native connectivity: accepted AC already covers that carrier, as recorded in X4. Uniform-floor-three and other all-floor-at-least-three carriers outside applicable accepted classes remain OPEN.

At target four X3/X4 still cover any carrier containing an original floor one or two; X5 adds the stated conditional triple-anchor class. No minimality, necessary floor threshold, exact-endpoint disconnection, global destination-directed scheduling, unrestricted root/nested universality or new numerical/implementation certification is claimed. Native lifting retains accepted child interfaces. No new external design dependency, physical geometry, primitive time, efficiency or originality claim is made.
