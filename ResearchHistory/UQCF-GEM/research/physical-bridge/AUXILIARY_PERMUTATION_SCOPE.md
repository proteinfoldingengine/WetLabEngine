# Auxiliary cycle breaking by one reusable buffer label — scope

Date: 2026-10-07. Status: prospective analytical scope.
Parent: JOINT_AUTO_EVENT_CYCLE_CLOSEOUT.md at 537a959126ca2ff89faf8445619064424af8809c.

## Scientific question

When can ONE temporary off-endpoint incidence break several alternating floor/lower-witness dependency cycles, without retaining it at the exact destination?

## Frozen carrier

There are n labelled roots, n in {3,4}, with original floor1. The source roots are distinct singletons S_i={a_i}. The exact target is C_i={a_{sigma(i)}} for a prescribed permutation sigma of {1,...,n}. All a_i are distinct. An auxiliary label w is in the palette, distinct from all a_i and absent at both endpoints. Native edits toggle one incidence. The protected band is 3<=tau<=4.

The permutation decomposes into c nontrivial cycles, with m moved roots total. Fixed points are never edited.

## Proposed reusable-buffer algorithm

For each nontrivial cycle (i1,...,il), with sigma(i_j)=i_(j+1) cyclically:

1. Add w to root i1; delete a_i1 from i1, creating a free label.
2. In order j=l,l-1,...,2, add the currently freed label a_i_(j+1) (cyclic, with a_i_(l+1)=a_i1) to root i_j, then delete its old a_i_j. This frees a_i_j.
3. Add the final freed a_i2 to i1, then delete w.
4. Reuse the same w for the next nontrivial cycle.

## Required proof and controls

- Prove every root remains nonempty and root supports are pairwise disjoint at every primitive state; consequently tau=n exactly, so the full band is preserved.
- Prove exact labelled target and complete cleanup of w.
- Prove 2(l+1) primitive edits per cycle and 2m+2c overall; at most one w incidence is ever present.
- Prove one buffer LABEL is sufficient for any number of disjoint permutation cycles, not one buffer per cycle.
- Prove for n=3 a nonidentity permutation has no legal endpoint-only first move (all deletions violate floor1, all additions create a shared label and tau=2).
- Give a rejecting control at n=4: some swaps are endpoint-only repairable in the band, so do NOT assert w is necessary for n=4.
- State retained input: permutation/address and available fresh label w; no need for global hidden support read in this exact singleton carrier.
- Do not claim arbitrary incidence states, n>4 in target-four band, all overlapping cycles, or a universal auxiliary bound.
- Provide author-side audit, immutable readback, and honest scoped closeout. Independent review remains separate.

No physical particle, force, geometry, energy, observer field, continuum, or fundamental time.
