# One reusable auxiliary label breaks permutation cycles

Date: 2026-10-07.
Status: ANALYTICAL CANDIDATE; author-side argument, not independent certification.
Frozen scope: AUXILIARY_PERMUTATION_SCOPE.md at 51bb75d3ca71f35c62b480eee21e6f9afcdd6fbb.

## 1. Exact class

Fix n in {3,4}, original labelled roots r_1,...,r_n, all floors1. Let a_1,...,a_n,w be distinct labels. Source E_i={a_i}; target C_i={a_{sigma(i)}} for a prescribed permutation sigma. w is absent at both endpoints.

The native primitive toggles one root-label incidence. A state is protected when all floors hold and 3<=tau<=4.

The source and target have n nonempty, pairwise disjoint singleton roots. Consequently tau(E)=tau(C)=n.

Write sigma as disjoint cycles. Let c be the number of cycles of length at least2, and m the number of indices in those cycles.

## 2. One-buffer construction for one cycle

Take a nontrivial cycle (i_1,...,i_l), where sigma(i_j)=i_(j+1) and i_(l+1)=i_1.

Initially r_(i_j)={a_(i_j)}.

A. Buffer the first root:
   Add(i_1,w), then Del(i_1,a_(i_1)).
   Root i_1 now equals {w}, and a_(i_1) is free (absent from all roots).

B. For j=l,l-1,...,2:
   Add(i_j,a_(i_(j+1))) where i_(l+1)=i_1.
   Del(i_j,a_(i_j)).
   The newly freed label is a_(i_j).

   At the moment root i_j is processed, the free label is exactly a_(i_(j+1)), which is its prescribed target label.

C. Finish the buffered root:
   Add(i_1,a_(i_2)), then Del(i_1,w).

All roots in this cycle now have their exact prescribed targets. w is absent again.

The number of native events is
    2 + 2(l-1) + 2 = 2(l+1).

## 3. Disjoint-support invariant

**Theorem A (protected buffer cycle).** Every primitive state in Section2 has n nonempty pairwise disjoint root supports.

Proof. Initially the supports are disjoint singleton sets.

- Add w: w is absent globally; adding it only to i_1 preserves disjointness. That root becomes a two-element support and remains nonempty.
- Delete its old label: i_1 still has w, so remains nonempty. Its old label becomes globally absent.
- In each middle iteration, the added label is the currently globally absent freed label. Hence the addition preserves pairwise disjointness. The root contains its old label and the new target label, so deleting its old label leaves a nonempty singleton and makes that old label globally absent.
- Finally a_(i_2) is globally absent. Adding it to buffered i_1 preserves disjointness; deleting w leaves its prescribed singleton and frees w.

Roots outside the cycle are unchanged and their labels are distinct from the labels in the cycle and w. Thus the invariant holds across the whole system. QED.

For n nonempty pairwise disjoint supports, any hitting set needs at least one different label for each root, while choosing one label per root hits all roots. Therefore tau=n exactly.

Since n is3 or4, every state lies in 3<=tau<=4. All floors1 hold by nonemptiness.

## 4. Reuse across several cycles

**Theorem B (one reusable label).** Process the nontrivial cycles of sigma in any deterministic order using Section2. After each cycle, w has been removed and all processed roots have their exact targets. Their labels remain pairwise distinct from those of unprocessed cycles.

Therefore the same single label w can be reused on the next cycle. At most one incidence containing w is present at any moment.

Summing the event counts gives

    L = sum_cycles 2(l+1) = 2m+2c.

After exactly L native edits, every moved root is at its exact labelled target, every fixed point is unchanged, and w is absent. Every intermediate state has tau=n and floors1.

This is a constructive sufficient theorem. The count is the length of THIS schedule, not a universal minimum over all native paths.

For n=4, sigma=(1 2)(3 4) has two cycles: the same w is used twice, giving 12 edits and tau=4 throughout.

## 5. Sharp endpoint-only obstruction for n=3

**Theorem C.** If n=3 and sigma is nonidentity, no protected endpoint-only native path can leave E.

At E every root is a floor-saturated singleton. Any endpoint-only deletion empties its root and violates floor1.

Any endpoint-only addition adds a target label a_j (j != i) to a root r_i. That label is already present in the distinct singleton root r_j. Hence after the addition two roots share a_j, while the third singleton root retains a distinct label a_k. The pair {a_j,a_k} hits all three roots, so tau<=2, violating tau>=3.

Therefore no endpoint-only first event is legal. An off-endpoint temporary incidence is necessary for any protected native repair in this restricted palette/event model.

When the palette consists of the three endpoint labels plus w, the construction uses exactly one temporary w addition and one eventual w deletion. For one nontrivial cycle of length l, the 2l endpoint-differing incidences must each toggle at least once, and any successful path must use at least two off-endpoint toggles (one to depart the endpoint-only deadlock, one to restore the endpoint). Thus the displayed 2l+2 length is optimal in native incidence edits for the n=3 single-cycle case.

This lower bound is restricted to the stated source, target and palette; it is not a general auxiliary optimality claim.

## 6. Rejecting control: n=4 does not always need w

Take n=4 with source
    {a},{b},{c},{d}
and target
    {b},{a},{c},{d}.

An endpoint-only path is:

    Add b to root1: {a,b},{b},{c},{d}, tau=3;
    Del a from root1: {b},{b},{c},{d}, tau=3;
    Add a to root2: {b},{a,b},{c},{d}, tau=3;
    Del b from root2: {b},{a},{c},{d}, tau=4.

Every root remains nonempty and every state stays in 3<=tau<=4.

So the auxiliary buffer is SUFFICIENT for n=4, not necessary in every n=4 instance. The disjoint-support buffer schedule deliberately preserves the stronger invariant tau=4.

## 7. Retained-information interface

The controller needs only:
- the labelled cycle decomposition of the prescribed permutation;
- the initial singleton-label assignment and floors1;
- the fact that w is globally absent at the source and is reserved as an auxiliary;
- the active cycle position and one freed-label identifier.

It does not require a fresh full-state read after initialization. At every step, the next native edit is determined by the retained cycle/phase record.

The proof is uniform over every permissible permutation in this carrier. It does not require witness-by-witness lookup during execution because disjointness is a global structural certificate.

This is not a universal compression theorem: the labelled permutation and initial singleton assignment are explicit retained inputs.

## 8. Scientific interpretation and boundaries

The auxiliary w acts as a renewable buffer. During a cycle it gives the first saturated root a temporary nonempty support and serves as a distinct relational witness while endpoint labels are reassigned. Once the cycle closes, w is removed and can be reused for another cycle.

This generalizes the previously closed two-root singleton swap to all permutations on three or four singleton roots, and proves that one auxiliary LABEL suffices for multiple disjoint cycles in this class.

It does not cover arbitrary overlapping root supports, higher floors, arbitrary directed dependency graphs, simultaneous coupled cycles that cannot be decomposed as a permutation, or universal target-four repair.

The same combinatorial construction works for any n and keeps tau=n, but for n>4 that is OUTSIDE the target-four protected band. No physical force, particle, energy, geometry, continuum, or fundamental time is inferred.

## 9. Next theorem-first frontier

Seek a bounded carrier with overlapping root supports and coupled alternating dependency cycles, rather than disjoint singleton permutations.

Test whether one temporary incidence can simultaneously protect more than one cycle without forcing tau below3 or above4. Require:
1. an exact retained-data host-selection rule;
2. a reusable witness/capacity certificate;
3. a terminating event rank;
4. exact cleanup at the labelled destination;
5. a rejecting case showing where one buffer is insufficient.

The present result is a sufficient structural family, not a solution to that broader question.
