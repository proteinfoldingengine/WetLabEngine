# A11.X2: renewable protection with q-2 singleton-floor slots

Status: frozen candidate analytical proof for independent review. Scope parent: 325bb35370a69b750215ef58578fdbff4bc361a0. Fixed finite palette, labelled roots, positive original floors and individual incidence moves throughout. No enumeration, numerical campaign, implementation, tests or workflows.

## 1. Theorem and claim boundary

Let P be a finite palette of size k, let A_i,C_i be permitted supports at the same labelled slots with floors a_i>=1, and let tau(A)=tau(C)=q>=4. Suppose at least q-2 of the ORIGINAL floors equal one.

**Theorem X2 (renewable singleton anchors).** A and C have a finite primitive path with every floor respected and transversal in {q-1,q}, regardless of the other positive floors.

We first prove a constructive finite lower path with tau>=q-1, then use accepted maximum-layer removal (GENERAL_PARENT_CONNECTIVITY.md, Theorem A, integrated baseline 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f). The latter dependency is not independently recertified here.

The construction permits temporary incidences and repeated toggles. Thus it closes this NATIVE connectivity class, not A11's universal destination-directed scheduling question. It supplies its own renewing invariant and global finite progress inside the class. It does not say every safe prefix has a continuation; A11.X1's contrary result is unchanged.

Set m=q-2 and select the same m floor-one slots at both endpoints, in a fixed order. Call these the anchor slots. Feasibility gives k>=q=m+2 and r>=q, since P hits every support and one label per root also suffices. At least two nonanchor slots exist.

## 2. Normalize anchor slots without losing protection

At either endpoint contract each selected anchor support to any one of its labels, deleting the others individually. Its original floor is one; support contraction cannot decrease tau. Thus the normalized tuple has tau>=q, though it need not remain exact q.

If two selected anchors are both {p}, choose t in P outside the set of currently used anchor labels and change one of them by

    {p} -> {p,t} -> {t}.

The other singleton {p} stays fixed. Every hitting set must already contain p, so the union step does not change the hitting requirement of the tuple. Deleting p from the changed slot cannot lower tau. The number of distinct selected-anchor labels increases by one. Whenever it is below m, a duplicate selected anchor and an unused palette label exist, since k>=m+2. Repeat until the m selected anchors contain DISTINCT labels.

This process is finite, uses original palette labels, respects floors and maintains tau>=q. Normalize A and C separately, obtaining A*,C*. The nonanchor supports are unchanged by this normalization. Reversing C -> C* later supplies a legal path from C* back to C with tau>=q.

## 3. The forced-label invariant and two actual protecting roots

When the m anchor slots are singletons with distinct label set U, every hitting set of size at most m must equal U: it must contain all m singleton labels. Consequently,

    tau(X)>=m+1=q-1
        iff some NONANCHOR support X_i misses U.

This is an exact lower-guard criterion in the anchored carrier; it does not assume any additivity of the other roots or their support sizes.

At A* and C*, whose transversal is at least q=m+2, U is missed by AT LEAST TWO roots. If it missed zero roots it would be a hitting set of size m; if it missed only one root, appending any label from that positive-floor support would give a hitting set of size at most m+1. Both contradict tau>=m+2. Such missed roots are nonanchors.

Choose two distinct source protecting indices i,j. Their actual supports miss U, so

    a_i<=|A*_i|<=k-m,   a_j<=|A*_j|<=k-m.

These are ORIGINAL floor-compatible slots. Expand each to G(U)=P minus U, individually adding its missing labels. It remains disjoint from U during its own expansion. At least one root, indeed that same root, therefore protects the forced set throughout. At the end both i,j have support G(U). Their floors fit EVERY future set G(U') with |U'|=m, because all such sets have cardinality k-m.

The invariant to be renewed is: m distinct singleton anchors plus TWO retained root slots i,j each equal G(U). One protecting root blocks the only forbidden m-label cover; the second permits a change of that constraint and is renewed afterwards. The palette labels used for the roots were already in P, and no root slot is added.

## 4. Six primitive moves change an anchor and restore the invariant

Suppose the invariant holds, the changed anchor currently has label p in U, and t is an existing palette label outside U. Put

    W=U minus {p},  U'=W union {t},
    G=P minus U,   G'=P minus U'.

Then t belongs to G, p does not, and G'=G union {p} minus {t}. Keep all other roots fixed. Perform the following SIX individual moves, with displayed supports referring to the changed anchor, guard i and guard j:

| Stage | Move | Anchor | Guard i | Guard j |
| --- | --- | --- | --- | --- |
| 0 | Initial | {p} | G | G |
| 1 | Add p at j | {p} | G | G union {p} |
| 2 | Delete t at j | {p} | G | G' |
| 3 | Add t at anchor | {p,t} | G | G' |
| 4 | Delete p at anchor | {t} | G | G' |
| 5 | Add p at i | {t} | G union {p} | G' |
| 6 | Delete t at i | {t} | G' | G' |

Every toggle has the stated incidence present or absent. Both guard supports always have at least k-m labels, meeting a_i,a_j. The anchor always has at least one label. All other floors are unchanged.

Through stage 2 the anchors force U, and guard i misses U. At stage 3 the other m-1 singleton anchors force W; a hitting set with at most m labels must then be either U or U', to hit the two-label anchor {p,t}. Guard i misses U and guard j misses U', so neither hits the tuple. After stage 4 the anchors force U' and guard j misses U' through stages 5 and 6. This proves tau>=q-1 at EVERY primitive, including the union stage.

At stage 6 both retained guards equal G(U') again. The protection has been renewed, not consumed: the same six-move exchange is available for another distinct-anchor label change. No inactive-family saturation certificate or exact-q restoration is presumed at the stage boundaries. The path may be at q-1 or above q; maximum-layer removal is applied only at the final exact-q endpoints.

## 5. A finite anchor-label schedule always exists

The anchor labels form an ordered injection of m slots into P. The target is the ordered distinct label tuple in C*. We can change one coordinate at a time while keeping all labels distinct, using existing unused palette labels.

First, whenever a wrong coordinate's target label is not currently used, replace its label by that target. This fixes that coordinate and releases its old label; repeat while possible. Correct coordinates are never disturbed.

If wrong coordinates remain but none has a free target, ALL m destination labels are already used: the current and destination label sets coincide. The remaining mismatch is a disjoint union of nontrivial permutation cycles. Take one cycle, choose a helper label h outside the current set, and change one cycle coordinate to h. Its old label becomes free. Follow the cycle, moving each newly free label to the coordinate requiring it, and finish by replacing h at the first coordinate with its target. A cycle of length ell is resolved in ell+1 single-coordinate changes. h is outside the destination set at the start of this cycle, since the current and destination sets coincide; it becomes unused again when the cycle ends.

Each direct change fixes a coordinate. Each cycle transaction fixes all its coordinates and then terminates. There are at most m initially wrong coordinates and at most m nontrivial cycles, hence at most 2m coordinate changes suffice. At every individual change its new label is outside the then-current anchor set, so Section 4 applies. Helpers exist because k>=m+2. No added label or assumed room to separate all root incidences is involved.

Replacing each coordinate change with its six-move exchange gives a finite native lower path that matches ALL anchor labels of C*, with both guards renewed after every change. This stage has at most 12m primitives, a mathematical path-length bound, not an empirical performance or runtime claim.

## 6. Repair all remaining roots and reach the labelled destination

Now the singleton anchors agree with C*, with label set V, and the retained source slots i,j both equal G(V). At C*, at least two nonanchor roots miss V by Section 3. Choose one destination protecting index b different from i; this is always possible. It may equal j.

Hold root i fixed while repairing b to C*_b through

    X_b -> X_b union C*_b -> C*_b,

adding each missing destination incidence individually and then deleting each source-only incidence individually. Root i still misses V, so the anchored lower guard survives every move. Expansion preserves the source floor, and contraction to the permitted C*_b preserves the same original floor.

Keep the completed C*_b fixed; it misses V. Repair every other nonanchor root to its exact labelled C* support with the same single-incidence union replacement, including the two retained guard slots when applicable. At each primitive C*_b protects the only forbidden m-label set V. Each completed root is processed once in this final stage; the number of unprocessed roots decreases by one. Each root has finitely many remaining incidence additions/deletions, so those replacements terminate as well.

The anchors already agree with C*, so this reaches C* exactly. Reverse the separately constructed normalization C -> C*. Every state on that reverse segment has tau>=q, and every original floor holds. Concatenating A -> A*, guard preparation, anchor exchanges, remaining-root repairs and C* -> C yields a FINITE primitive A -> C path with tau>=q-1 throughout.

All labelled slots are restored; the original palette and floors are unchanged. There is no unproved next-exchange existence assumption: source guards exist by redundancy; their floors permit every renewed G(U); anchor changes have an explicit finite assignment schedule; destination guard choice exists by redundancy; and each final root repair has a fixed protecting root.

Applying accepted maximum-layer removal ONCE to this full finite lower path, whose original endpoints have tau=q, gives tau in {q-1,q}. This completes Theorem X2. The accepted conversion does not have to retain the anchor invariant or the temporary-support sequence; the proof only needs its stated fixed-carrier conclusion.

## 7. New sufficient class and remaining scientific boundaries

**Corollary X2.4.** For target four, two original floor-one slots suffice for one-unit native connectivity of ALL feasible exact-four endpoints on that carrier, with arbitrary positive floors elsewhere. A11.X1's 15-root carrier (two floors one and thirteen floors 6006) therefore belongs to this proved class, not merely its displayed endpoint pair.

For general q>=4, Theorem X2 improves the accepted arbitrary-other-floor condition from q singleton-capable slots (SINGLETON_ANCHOR_REDUCTION.md, Theorem P) to q-2. Theorem Q in that source still concerns the separate class where EVERY floor is one or two. Historical baseline sources and their certification remain unchanged; this is a separately reviewed analytical extension. Arbitrary-arity target three was already closed and is not claimed as new work.

The theorem proves sufficiency, not a minimal necessary number of floor-one slots. It does not close carriers with fewer than q-2 such slots unless another accepted theorem applies. In particular, the original target-four uniform-floor-three diagnostic has no singleton-floor slots and stays OPEN. General q>=4 unrestricted root/nested universality stays OPEN; lifting requires the accepted child-interface conditions.

This is not an answer to universal A11 destination-directed scheduling. Guard supports P minus U can introduce incidences outside the endpoints' unions; helper labels and reverse endpoint normalizations can require repeated toggles or temporary deletion of destination incidences. No monotone-path claim is made for the general theorem. A11.X1's failure of arbitrary safe-prefix extension is retained.

The scientific mechanism is explicit renewal: hold one existing avoiding root while the other acquires avoidance of the new forced set, change the anchor constraint with both alternatives protected, then restore the second root so the next exchange remains available. The floor conditions guaranteeing the next exchange are derived from endpoint protection and unchanged support cardinality. No additional physical geometry, primitive time, alignment rule, original-design property, numerical evidence, implementation certification or efficiency claim is used.

