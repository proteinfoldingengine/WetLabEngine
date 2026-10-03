# Adaptive buffer renewal without an outside-guard slot assumption

Status: candidate analytical proof for independent review. Parent: 064c4ca1581eebe54a850c23adf420b8d9d3a2b1. Native carrier, analytical authorization and certified baseline are unchanged from SCOPE.md. No implementation, scientific enumeration or workflow execution.

## 1. Any root can initially be reserved

Let A,C be exact-q endpoints in the same fixed palette P, labelled slots and positive floor vector, with q>=3 and t=q-1. Fix ANY existing slot b as the buffer. Write A_{-b} for all other roots.

**Lemma R1.** Both tau(A_{-b}) and tau(C_{-b}) are at least q-1.

A transversal of A_{-b}, together with one label from the nonempty A_b, hits A. Thus q<=tau(A_{-b})+1; the destination argument is identical. This is the already accepted one-root-removal consequence of exactness, not a new endpoint classification.

Consequently the guards I=J=all indices except b are always available at the two endpoints. A lack of a slot outside two previously selected guards is not an intrinsic obstruction at exact endpoints: select these larger guards instead. This does NOT prove that their highly overlapping handover is possible. It moves the remaining question from initial slot availability to renewal of protection during the handover.

One cannot automatically reserve two roots, or repeat R1 after reaching only level q-1. For example q pairwise disjoint roots require q hitting labels; removing two leaves q-2. No extra native slot is assumed here.

## 2. Exact supports that make a fixed residual family safe

For a family F of all nonbuffer roots, define

    D_t(F) = {H subset P : |H|<=t-1 and H hits every root of F},
    W_t(F) = P minus union_{H in D_t(F)} H.

If D_t(F) is empty, its union is empty and W_t(F)=P. All sets are mathematical proof objects; no enumeration is executed or claimed efficient.

**Lemma R2 (safe support pool).** A buffer support Z is admissible and makes tau(F plus Z)>=t exactly when

    Z subset W_t(F),   |Z|>=a_b.

Indeed a small set H hitting F is prevented from hitting the whole tuple exactly when it misses Z. Requiring this for every such H is precisely Z subset W_t(F). The buffer's floor supplies the size condition.

Thus the safe supports of the buffer at fixed F are closed under union. If Z and Z' are both safe and meet the floor, the primitive path Z -> Z union Z' -> Z' stays safe and respects the floor. This holds even if the whole tuple is only at level t: it does not require restored exact-q redundancy.

The pool can be characterized by the residual transversal number:

- If tau(F)>=t, then W_t(F)=P.
- If tau(F)=t-1, then W_t(F) consists of labels occurring in NO minimum transversal of F.
- If tau(F)<=t-2, then W_t(F) is empty. To prove this, take a transversal H of size at most t-2. For any label x, H union {x} is a transversal of size at most t-1, so x is in the forbidden union.

In the middle case, W_t(F) is also the intersection of all maximum independent label sets of the hypergraph F, by complementing transversals. This is an elementary identity, not an originality claim or an efficient algorithm.

## 3. A chosen sequence of nonbuffer root edits

Choose any permutation i_1,...,i_m of the nonbuffer slots, where m=r-1. Let G_s be their hybrid family after the first s slots have changed to C and the others still equal A. Let U_s, 1<=s<=m, agree with G_{s-1} except that slot i_s is expanded to A_{i_s} union C_{i_s}.

Thus G_{s-1} and G_s are both componentwise contained in U_s. The intended nonbuffer edit is a single-root union replacement, whose intermediate families are also contained in U_s. Put W_s=W_t(U_s).

The buffer may be reset between completed nonbuffer edits, but is held fixed during each individual nonbuffer union replacement. Its support must always meet the original floor a_b. This describes a method class, not an extra native restriction.

**Theorem R3 (adaptive buffer criterion).** For this fixed buffer slot and fixed nonbuffer order, a path in this method class preserving tau>=t exists if and only if

    |W_s|>=a_b for every s=1,...,m.

No common intersection of all W_s is required.

Necessity: the path visits U_s while holding some support Z_s in the buffer. R2 forces Z_s subset W_s and |Z_s|>=a_b, hence the inequality.

Sufficiency: choose any Z_s subset W_s of size a_b. Initially G_0=A_{-b} has transversal at least t by R1, so replace A_b with Z_1 through their union safely. Hold Z_1 while editing root i_1. R2 makes U_1 plus Z_1 safe, and shrinking nonbuffer supports cannot reduce transversal number, so every primitive of that edit is safe.

At the boundary G_s between successive edits, both Z_s and Z_{s+1} are safe. Indeed G_s is contained in both U_s and U_{s+1}. Any small transversal of G_s therefore hits both larger families, and must miss both Z_s and Z_{s+1}. It misses their union as well. Equivalently,

    W_t(G_s) contains W_s union W_{s+1}.

Change the buffer Z_s -> Z_s union Z_{s+1} -> Z_{s+1} at fixed G_s. R2 proves safety and the floor throughout. Then perform the next nonbuffer edit. After the last edit, G_m=C_{-b} has transversal at least t, so restore the buffer exactly to C_b through its union. Every labelled root now equals its destination.

This constructs a finite lower-guard path between exact-q endpoints. Apply the accepted maximum-layer-removal theorem to obtain tau in {q-1,q}. The normalized path need not retain the same edit order or buffer supports. Native lifting is conditional on the accepted child interfaces as stated in GUARD_HANDOVER.md Section 6.

## 4. Why this is a renewal theorem

The editable root and the buffer never change simultaneously. During a nonbuffer edit, U_s certifies its fixed buffer support. At the completed boundary, the residual family admits both old and next buffer supports and their union, allowing a floor-safe handover. This is a proved renewal point even if the complete tuple has not returned to exact q.

Eligible supports exist by the inequalities. Choose their a_b least labels under the supplied palette order if a deterministic choice is desired. Each union replacement has finitely many toggles. There are m nonbuffer replacements and m+1 buffer replacements, including installation/restoration. Advancing along this finite list proves termination; the tie-break alone is not the argument. There is no claim that computing the pools or finding a qualifying order is efficient.

For a buffer held fixed throughout, R2 would instead require a support of size a_b in the intersection of all W_s. R3 removes this joint-support requirement by proving compatible changes at the boundaries. The inequality comparison alone does not claim that a strict separation is realized by a particular native endpoint family; no such example is needed for the theorem and none is asserted here.

## 5. Precisely characterized method obstruction

For a prescribed b and order, failure is exact: some stage has |W_t(U_s)|<a_b. This means either the nonbuffer transversal has fallen below t-1, or at level t-1 there are too few labels excluded from all minimum transversals to support the buffer floor. No choice of buffer support can repair THAT active-union stage while the other roots are frozen there.

A different order or different buffer may avoid that stage. R3 does not prove that every exact endpoint pair has a qualifying choice. Ruling out one order, or even all such orders, is not a native barrier: an unrestricted path may interleave partial nonbuffer edits, use temporary supports outside endpoint unions, or exploit other native child freedoms.

The remaining universal obligation is now explicit: establish that exact-endpoint structure guarantees a buffer/order satisfying every local safe-pool capacity, or provide a new renewing move that bypasses a deficient stage. Total endpoint capacity and local redundancy have not yet supplied that existence theorem.
