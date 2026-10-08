# C3 three-singleton-anchor obstruction theorem

Date: 2026-10-07.
Status: ANALYTICAL CANDIDATE / AUTHOR-SIDE PROOF, not independently accepted.
Frozen scope: COUPLED_C3_ANCHOR_SCOPE.md at f12d6775214b827ede8e5a5248e9b8f92721c048.

## Theorem

Let four original labelled roots have source supports
    r1={a}, r2={b}, r3={c}, r4=S,
with a,b,c distinct and S nonempty. All original floors are positive and compatible with the source. Let the exact target for r4 be T, nonempty, with |T|>=f4 and |S|>=f4.

Keep r1,r2,r3 unchanged while r4 is edited.

Then for EVERY intermediate r4 support U that is nonempty:
    3<=tau({a},{b},{c},U)<=4.

Proof. The three singleton roots require a,b,c in every transversal, hence tau>=3. Choosing a,b,c and one label u in nonempty U hits all four roots, hence tau<=4. No geometric or numerical assumption is used.

## Constructive endpoint-only fourth-root repair

Given S and T, perform:
1. Add every incidence in T minus S to r4 (in a fixed retained label order).
2. Delete every incidence in S minus T from r4 (in a fixed retained label order).

Every addition increases the support and preserves its floor. After all additions the support contains T. During deletions it continues to contain T, so its size remains at least |T|>=f4 and it stays nonempty.

All intermediate states satisfy 3<=tau<=4 by the theorem. At the end r4=T exactly.

If S!=T, at least one endpoint-differing primitive is performed, and the FIRST such primitive is legal. Therefore a four-root source with three distinct frozen singleton roots and an active fourth-root endpoint obligation cannot be completely endpoint-only stuck at its source.

## Corollary and limitation

For the C2 source ({a},{b},{c},{a,d}) and fourth-root target {b,c}, a protected M4-first route exists automatically, even though finishing M4 first later blocks the particular complete M1 and M2 macros.

This distinction is essential:
    one legal first move
does NOT imply
    a complete protected endpoint-only path to every prescribed full target.

The C2 example does possess another complete endpoint-only path, but that fact is separate from this structural theorem.

## Rejecting boundaries

1. If the source does not contain three distinct singleton roots kept unchanged during the fourth-root edits, the lower-bound proof no longer applies.
2. If r4 is allowed to become empty, the upper-bound argument fails and floor legality fails for positive floors.
3. If |T|<f4, the declared endpoint itself violates the original floor and is outside the theorem.
4. If a fourth root has no endpoint difference, this theorem does not assert an endpoint-only first move.
5. This does not prove that all four-root coupled carriers admit endpoint-only full completion, or that temporary auxiliaries are never needed.

## C3 consequence

A prospective four-root C3 counterexample with no legal endpoint-only first move and an active fourth root cannot use three distinct singleton roots as a frozen source scaffold.

The next candidate should use a genuine overlapping protection system without three frozen singleton anchors. Any proposed auxiliary-necessity claim must still rule out ALL endpoint-only legal paths, not merely a chosen macro schedule.

No numerical campaign, independent acceptance, physical force, geometry, observer field, or fundamental time is inferred.
