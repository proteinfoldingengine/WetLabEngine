# Four-child joining interface — candidate analytical proof

This is the proof text submitted for independent analytical review; the current decision is recorded in INDEPENDENT_PROOF_REVIEW.md. Native category and research scope were recorded first in commit 8fcc46597ab7c2b83fe9dd2fd0611a07e66169cd. No new implementation or numerical campaign is claimed.

## 1. Statement

Use NATIVE_ADMISSIBILITY.md without alteration. Let four ordered child trees T_i carry profiles and the SAME six-clause interface I accepted in v16.52, with minimum widths a_i>=1. Their interior vertices may be arbitrarily deep; the argument uses their interfaces, not a restriction to particular examples. Attach them to one parent with target q in {1,2,3,4} and fixed ordered palette P of size k.

The claim is that the joined tree has that same interface: exact feasibility, a compact ordered canonical endpoint, finite fixed-root normalization with total excursion at most one, exact-interior attached role replacement, compact contraction, and transported-order equivariance. Feasibility below is constructive finite combinatorics, not a guessed closed-form recurrence.

Write tau(A_1,...,A_4) for the minimum number of labels hitting all four nonempty child-root supports. The parent coordinate is tau. Child-root supports can change; the parent's root P cannot.

## 2. Compact feasibility and canonical endpoint

Define w(a,q) as the least m for which four subsets of [m] have cardinalities exactly a_1,...,a_4 and transversal number q. This minimum exists: take disjoint private palettes of those sizes, choose one label in each of 5-q children, and identify those chosen labels into one common label. The other q-1 children have disjoint private palettes. Every hitting set needs one label for each of those isolated children and at least one for the group; the shared label attains q. This uses sum(a_i)-(4-q) labels. Thus the definition is finite and does not assume the result to be proved.

Equivalently, enumerate the 15 nonempty incidence regions C subset {1,2,3,4}. Nonnegative integer counts n_C satisfy sum_{C containing i} n_C=a_i. Their sum is the number of used labels. The transversal number is the least cardinality of a collection of region types with positive count whose union is all four indices. A repeated type contributes nothing new to a minimum cover. Minimize the sum of counts subject to that transversal number being q. This is an exact feasibility specification. In particular w(a,1)=max a_i and w(a,4)=sum a_i; no middle-target formula is presumed.

Why compact feasibility equals native feasibility: suppose an exact nested state exists on P. Choose a minimum parent hitting set H of size q and, for each child, one anchor x_i in H intersect A_i. Normalize child i on its own fixed root A_i ordered with x_i first, and contract its attached normalized root to its first a_i labels. Each child interface guarantees exact-interior contraction, and retains x_i. During normalization the parent roots are fixed, so the parent is exact. During contraction all child roots only decrease: the parent hitting number cannot decrease below q, while H continues to hit all roots, so it cannot exceed q. At the end the four roots have sizes a_i and transversal number q. This is also a finite legal path with global unit excursion, although only its existence is needed for the feasibility argument. Leaves contract to their selected single anchor.

Consequently any native exact state requires k>=w. Conversely, select a compact tuple realizing w, embed it into the first w labels of P, and fill each child using its own canonical interface. This gives an exact nested state for every k>=w. No used label can be absent from all four roots in a minimum-w tuple, since deleting that unused palette label and relabeling would contradict minimality.

Choose the lexicographically least feasible tuple of incidence bit strings on [w]: compare child 1's string first, then children 2,3,4; within each string compare palette positions increasingly, with bit 1 ordered before bit 0. Embed it into the first w labels of P; call the resulting roots A_i*. Fill child i with K(T_i,A_i*,q_i), using induced P order. This defines K for the joined tree. The union of all its proper descendant supports is exactly the first w labels: its immediate child roots already have that union and all lower supports are nested. The root itself remains all P.

## 3. Fixed-root clearance and lifting lemma

Normalize each child on its current fixed root A_i in induced P order. Since the parent is exact, sequential calls cost at most one TOTAL unit. For a nonleaf child, its proper descendant union U_i now has exactly a_i labels. A leaf has empty proper descendant union and requires separate, trivial root handling.

**Clearance.** Suppose a nonleaf child's root A contains x and has size greater than its width a. If x is used in its proper descendants, choose y in A outside their a-label union. Replace x by y at every proper descendant carrying x: add y in preorder, then delete x in reverse preorder, never changing the child root during this operation. Nesting and nonemptiness hold because the child root already contains both labels and each replacement installs y before removing x. At every internal coordinate, including this child's root coordinate, the partial y-incidence pattern is dominated by the original x pattern during addition; during deletion the remaining x pattern is dominated by the complete y pattern. Replacing the dominated label in any hitting set proves equality of the hitting number at every primitive. This is the inherited role argument applied below a fixed root, with the root boundary explicitly checked.

Afterward x occurs only at the child root and can be deleted there. If x was unused below the root, just delete it. Proper descendant union size remains a after a completed clearance. For a leaf, a permitted deletion simply leaves its root nonempty.

**Lifting lemma.** Any finite path of four root supports with |A_i|>=a_i, changing one root incidence per step and keeping tau within [q-1,q+1], lifts to a legal native path with all child interiors exact throughout: root additions are immediate; for a deletion, its resulting size >=a_i guarantees its previous size >a_i, so apply clearance and then delete. The outer parent's coordinate is unchanged during clearance. At the root step it stays within the prescribed band. No recursive child normalization is called while the parent is inexact.

If that root path ends at the exact canonical tuple A_i*, normalize the children again on those fixed roots in induced P order. The parent is exact throughout this final phase, so only the active child's inherited unit excursion is present. This reaches the specified K regardless of the role ordering produced by clearance. Full-width children require no deletions; leaves require no clearance. The lemma therefore includes both boundary cases.

## 4. Targets q=1 and q=2

From an exact tuple, add missing labels to child roots until every A_i=P. Along these additions the hitting number can only decrease. For q=1 it stays 1; for q=2 it is either 1 or 2. Then delete labels outside each target A_i*. Every intermediate root remains a superset of its target, so the target's hitting set still covers all roots. Thus tau is again 1 for q=1 and in {1,2} for q=2. All roots stay at least their required widths. Apply the lifting lemma.

This argument does not rely on the ternary shortcut that every possible parent coordinate is within one of the middle target. It explicitly guards the parent by a common expanded-root configuration. In fact this root argument for q=2 is independent of the number of children; only the four-child conclusion is needed here.

## 5. Cover reconfiguration lemma

Let a k-element set P be covered by sets B_1,...,B_r with capacities |B_i|<=b_i. Some capacities may be zero. Suppose sum b_i>=k+1. Any two such covers are connected by single-incidence additions/deletions that preserve coverage and capacities.

Proof: from each cover select one owner f(x) for every label x and delete its other occurrences. This produces a partition of P among bins satisfying capacities. To connect partitions f and g, keep labels already assigned to their destination bins fixed. Pick a misplaced label x and let j=g(x). If bin j has spare capacity, transfer x there by adding the new occurrence and then deleting the old one. If j is full, it contains a misplaced label y: otherwise all its b_j occupants are destined for j, and the additional label x would contradict the capacity of the target partition g. Total occupancy is k and total capacity exceeds k, so some other bin has a spare slot. Transfer y to that bin, then transfer x to j. The displaced y was not fixed. Each transfer maintains coverage, and its temporary duplicate uses a free slot. Every iteration fixes x without displacing any fixed label, so the procedure terminates. Finally add the extra occurrences required by the target cover; capacities hold because each resulting bin remains a subset of its target bin. This proves connectivity and a finite algorithm, not just a counting condition.

## 6. Target q=3: complementary supports supply the missing guard

In an EXACT four-child q=3 tuple, no label can occur in three child roots: that label plus any label from the remaining nonempty root would give a cover of size at most two. Therefore sum |A_i|<=2k, and hence S=sum a_i<=2k. Exact target 3 also requires k>=3.

Put B_i=P minus A_i and b_i=k-a_i. The forbidden parent value 1 is precisely a common label in all four A_i; equivalently, it is failure of the B_i to cover P. The permitted parent band for q=3 is {2,3,4}. Thus a capacity-bounded complementary cover is exactly a nonempty-root configuration in that permitted band with |A_i|>=a_i.

Both the initial exact tuple and the exact canonical tuple supply such covers. Moreover sum b_i=4k-S>=2k>=k+1. The cover lemma therefore supplies a path between them preserving capacities and coverage. A complement addition is a child-root deletion; a complement deletion is a child-root addition. Throughout, the parent cannot have hitting number 1, and four nonempty roots have hitting number at most 4. Apply the lifting lemma and final exact-parent normalizations.

This addresses the genuinely new overlap problem. The surplus complementary capacity is DERIVED from native exact q=3 admissibility. It is not an extra admissibility restriction, an added palette label, or an assumed free label shared by all children. A full-width child corresponds to capacity zero and is handled by the same proof.

## 7. Target q=4

An exact tuple has pairwise disjoint roots. Normalize each child on its fixed root and contract it to width a_i; roots remain disjoint, so the parent stays exact. Necessarily k>=S=sum a_i. Target exactly the disjoint tuple A_i* selected in Section 2; the role-assignment argument works for that tuple without needing any additional block convention.

The inherited disjoint-role assignment proof applies with four children. Replace a complete role by a globally absent desired label when possible. If a desired label is occupied in another child, exchange the two roles through two complete-role replacements. At every primitive the only possible shared label is between those two children; the other two roots remain disjoint from them and each other. Thus the parent hitting number is 3 or 4, and every child interior is exact. Each complete exchange restores disjointness. A same-child role swap uses three cross-child exchanges with a role in another nonempty child as pivot, restoring the pivot at the end. Fix target roles successively, preserving previously fixed roles at the end of each exchange. This finite procedure realizes the canonical disjoint assignment, including ordered child roles, with total excursion <=1.

## 8. The SAME interface is returned

Exact feasibility and canonical compactness were proved in Section 2. Normalization is supplied by Sections 3–7. Complete-role replacement of an ATTACHED joined subtree is still the arity-independent domination argument, including its root; its external parent's coordinate remains a caller obligation. Compact contraction deletes root-only labels beyond the canonical w-prefix, preserving every interior coordinate; the result is exactly K on that shorter palette. Leaves retain their one role.

All choices can be fixed by tree order and palette order: least feasible positional tuple, first minimum cover, first eligible anchor, first unused proper-descendant label, first misplaced cover label, first misplaced occupant, first bin with capacity, and ordered role targets. None depends on numerical names apart from the supplied order. Simultaneously relabeling and transporting that order transports the canonical endpoint and every primitive. Finite child calls and the finite cover/role procedures prove termination.

The four-child joining theorem consumes and returns I without weakening any clause. The already proved binary and ternary joins also consume only I, rather than assumptions about descendant arity. Together with the leaf base case, structural induction consequently extends I to every finite ordered tree with internal arities in {2,3,4}, PROVIDED this four-child argument is independently accepted. This is a theorem consequence, not a new collection of deeper binary/ternary examples.

## 9. What fails in the old shortcut, and what this does not claim

For four leaf children on P={a,b,c,d}, target 2, roots ({a},{a},{b},{b}) are exact. Replacing the second a by c and then the fourth b by d, each through add-before-delete primitives, ends at four disjoint singleton roots with hitting number 4. Child interiors are exact, yet parent excursion is 2.

For target 3, roots ({a},{a},{b},{c}) are exact. Replacing b by a and c by a reaches four copies of {a}, with hitting number 1 and excursion 2. These admitted move sequences precisely refute unrestricted middle-target transport as a proof shortcut. They do NOT exhibit endpoints that require a nonunit path. The guarded constructions above avoid the forbidden extremes.

After acceptance, reverse and concatenate normalization paths to connect exact endpoints on the same fixed root/profile within total excursion one. Each independently minimized inherited scalar barrier is zero within an exact component and one between distinct exact components, using the integer lower bound; existence of multiple components is not asserted. No minimal path length or physical interpretation follows. Arity>=5 remains outside this theorem, except for explicitly identified sublemmas. Analytical acceptance is separate from implementation validation and full execution certification.
