# Separating shared labels when the existing palette has room

Status: candidate analytical proof for independent review. Parent accepted head: 59f708231dd0e57548fc5931a8b0c98156ed8aa0. No implementation, enumeration or numerical execution.

## 1. Statement and native scope

Let r roots on a fixed palette P of size k have arbitrary positive floors a_1,...,a_r, and put S=sum_i a_i. All moves are single-incidence toggles, preserve floors and use only the original labels and root slots. Fix feasible exact-q endpoints, q>=3.

**Theorem AE (palette room).** If k>=S, every pair of exact-q endpoints is connected by a finite primitive path with tau in {q-1,q}.

The condition concerns available labels, not the total complementary block capacity. The proof does not infer it from the earlier inequality sum_i(k-a_i)>=(q-1)k. No label is added to the native palette.

## 2. Splitting a shared label without lowering the hitting number

Compact an endpoint exactly to its floors by retaining in each root at least one label from a minimum hitting set. The compact tuple has exactly S incidences.

If a label x occurs in at least two roots, the number of active labels is less than S. Since k>=S, some label y of P is absent from every root. In one root containing x, add y and then delete x. The root's size goes from a_i to a_i+1 and back to a_i, so its floor holds.

The addition does not lower tau. Indeed any hitting set after the addition can have y replaced by x to hit the old tuple: y occurs only in the edited root, so this replacement does not destroy coverage of another root. The other monotonic inequality follows because adding an incidence cannot increase tau. Thus tau is unchanged at the addition. Deleting x cannot decrease tau. The completed split therefore never goes below the old hitting number.

Because x still occurs in another root while y is now active, the number of active labels increases by exactly one. Repeating the operation terminates after at most S minus the initial number of active labels such splits. At termination all S incidences have distinct labels; hence the r nonempty roots are pairwise disjoint and tau=r.

This finite procedure uses fresh labels relative to the current tuple, always chosen from the existing palette. It does not add external labels or root slots, and it does not impose a complexity claim on the later path normalization.

## 3. A common disjoint tuple and removal of upper excursions

Choose a canonical tuple of pairwise disjoint roots of sizes a_1,...,a_r inside P; k>=S ensures that it exists. Any completed disjoint tuple can be sent to it by a global label permutation, extended arbitrarily on unused labels. Completed permutations preserve hitting number r and every root's floor.

The accepted label-transposition lemma provides primitive paths with hitting number in {r-1,r} for these permutations. Feasibility of an exact-q endpoint implies q<=r, since choosing one label per root is a hitting set. Thus the permutation paths remain at least q-1.

Each original endpoint reaches the canonical disjoint tuple through a lower-guard path: exact compaction, nondecreasing splits, and those label permutations. Reverse the second route and concatenate to obtain a finite path between the original exact-q endpoints with tau>=q-1. Apply the accepted maximum-layer removal theorem to obtain the required path with tau in {q-1,q}. The large values up to r in the preliminary construction are removed by that theorem; they are not claimed to satisfy the final excursion bound themselves.

All labels selected for splitting and all permutation labels belong to P, so maximum-layer replacement remains within the original carrier. This proves AE for arbitrary positive floors, without a uniform-rank or complete-module assumption.

## 4. Sharpened finite obstruction domain

Together with Theorem AC of GUARD_BUFFER_CONNECTIVITY.md, AE implies the following. Fix uniform floor h and q>=3, and let N=C(h+q-2,h). If any pair of exact-q endpoints is disconnected in the unit band, there is such a pair with compact endpoints and

    q <= r <= 2N-1,
    h+q-1 <= k <= rh-1.

The upper bound on r follows from AC. The upper bound on k follows from AE, since S=rh. The lower bound on r is the elementary tau<=r bound. For the lower bound on k, any k-h+1 labels hit every support of size at least h, so q<=k-h+1. Exact compaction preserves connected components because each compaction is itself an exact-q path.

This is sharper than the palette bound from the general finite-support simulation. The simulation theorem still has a separate use: for a specified arbitrary floor vector and a specified compact pair it identifies a small palette that preserves the connectivity answer in both directions. AE instead settles all pairs whenever k>=S.

No remaining finite domain is enumerated here. It need not be computationally tractable, and finiteness for each fixed h,q does not prove the assertion for all unbounded h,q. For mixed floors, any failure must satisfy k<S, but AC does not give the same uniform bound on r. All conclusions concern the width-floor carrier, not a necessary native nested barrier. Implementation and certification remain pending.
