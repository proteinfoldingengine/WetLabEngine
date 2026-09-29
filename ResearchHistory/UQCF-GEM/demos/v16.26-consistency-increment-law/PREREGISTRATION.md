# v16.26 — Atomic consistency-increment law

Parent: v16.25 publication commit `c637ac5a2c8017cf080f7d10813db07cde886045`.

## Frozen question

For one **atomic legal pruning**—remove one leaf from exactly one indexed retained view, while the union carrier remains unchanged—what can happen to the exact v16.24 consistency order h?

No new state variable is introduced. Define only the endpoint difference delta h = h(after)-h(before).

## Candidate theorem

Let the removed leaf be c with parent v.

A1. Only the child-incidence set of the modified view at v changes.
A2. For every vertex u != v, tau_u is unchanged.
A3. At v, tau_v(after) is either tau_v(before) or tau_v(before)+1.
A4. Hence h(after)-h(before) is in {0,1}.
A5. Exact local trigger: tau_v rises iff **no minimum tau_v(before)-view cover of Ch(v) remains a cover after deletion**. Equivalently, every old minimum cover is destroyed by the lost incidence.
A6. Global h rises iff the new tau_v exceeds the old global h (with the positive-order convention).
A7. Any same-union componentwise pruning can be factored into atomic leaf deletions that preserve the union at every step. Along any such factorization, each increment is 0 or 1 and the sum telescopes to h(final)-h(initial). Different legal factorizations may place the increments at different steps, but their total is endpoint invariant.

A counterexample to any item is a valid result.

## Proof obligation

If an old minimum cover at v survives, tau is unchanged. Otherwise take any old minimum cover S. It contained the modified view and relied on it for c. Because the final union is unchanged, some other view contains c after deletion; adjoining that view gives a cover of size at most tau+1. Monotonicity from v16.25 gives the lower bound tau(after)>=tau(before). Therefore the increase is exactly 0 or 1.

For A7, remove nodes from each view in leaf-first order. A node removed from one view remains in the final union, hence at least one final view retains it; that view is never removed at any stage. Thus every atomic deletion preserves the common union.

## Verification

Preregistered tests must reject: an atomic jump of 2; a false trigger label; removal of a non-leaf; changed union; multiple-view mutation mislabeled atomic; and a claimed factorization that removes an ancestor before its descendant.

Enumerate all atomic same-union refinements for every legal cover of at most four views on all rooted unordered trees through five vertices. Independently reconstruct the exact trigger and transition counts. Also enumerate legal atomic factorizations for bounded endpoint refinements on trees through four vertices and verify 0/1 increments and telescoping endpoint invariance across alternative orders.

**Time is pruning / ordered recoverability update.**
