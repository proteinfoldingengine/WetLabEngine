# Recursive repair interface: candidate proof

Status: independently accepted analytical argument; see INDEPENDENT_PROOF_REVIEW.md. No implementation, numerical validation or stage certification claimed.

## Typed statement

Let T be any finite rooted ordered tree whose internal vertices have two or three children. Let q assign an integer from 1 to the local arity at each internal vertex. Let P be any finite nonempty ordered palette. A state assigns nonempty supports S_v contained in P, with S_root=P and S_child contained in S_parent. The coordinate h_v is the minimum cardinality of a set of labels meeting every immediate child support. Legal primitives add or delete one incidence at a nonroot vertex, preserving these conditions.

Define w recursively: leaf 1; binary q=1 takes max, q=2 sum; ternary q=1 takes max, q=2 takes max(maximum child width, ceiling of half their sum), q=3 takes sum.

Claim I(T,q), quantified over EVERY ordered P. Canonical endpoints and normalization are defined only for feasible palettes |P|>=w(T,q). All excursion sums are over internal vertices (equivalently set leaf h=q=0):

1. Exact states exist iff |P|>=w(T,q).
2. There is a recursively specified exact K(T,P,q), with root P. For an internal T, the union of its proper descendant supports is exactly the first w(T,q) labels of P. For a leaf the union is empty.
3. Every exact state has a finite legal fixed-root normalization to K with sum_v |h_v-q_v|<=1 at every primitive. Each call returns with the whole subtree exact.
4. In an attached subtree, a complete role can be replaced by a subtree-absent label, if its external parent contains the old and new labels, preserving EVERY interior coordinate at every primitive. This operation may change the external parent's coordinate; callers must control it separately.
5. An attached normalized root can contract to its first w labels through exact-interior primitives. For a leaf retain its first label. The resulting state is K on that shorter ordered palette. External-parent control is again a caller obligation.
6. Simultaneously transporting labels and palette order transports K and the deterministic path. Compact K has w distinct ordered label roles.

The lemma claims that I for all children implies I for their binary or ternary parent. This is stronger than existence of a unit path for a particular joined state.

## R2: role transport is independent of arity

The vertices carrying x form an ancestor-closed set inside a subtree. For a label y absent from the subtree, add y at these vertices in preorder, then remove x in reverse preorder. Addition respects nesting because each parent already contains y; deletion respects nesting because every affected child has already lost x. An x removal never empties a support because y has been installed there.

At each interior vertex during addition, the set of immediate children carrying y is a subset of the unchanged set carrying x. Every hitting set using y can replace it with x without increasing its size; adding y cannot raise the minimum, so the minimum is unchanged. During deletion, y carries the complete original child-incidence set, while remaining x occurrences form a subset. Removing dominated x cannot change the minimum. Other labels are unchanged. This proof applies at arbitrary arity and depth, including zero affected child occurrences. It does not claim control of the external parent.

## Canonical construction and feasibility

Leaf K has root P and no descendants. For an internal vertex with child widths a_i, choose child palettes as follows, with each child palette ordered by restriction of P:

- q=1: initial segments of lengths a_i.
- q=arity: consecutive disjoint blocks of lengths a_i.
- ternary q=2: concatenate blocks of lengths a,b,c on positions 0 through a+b+c-1, reduce positions modulo M=max(a,b,c,ceil((a+b+c)/2)), and use the corresponding first M labels of P in each child.

Fill each child by its own K. Child feasibility supplies necessity of each individual width. Disjointness supplies necessity of the sum when q=arity. A ternary hitting number 2 means no triple intersection and at least one pair intersection: every label belongs to at most two child roots, so a+b+c<=2|P|. These give all stated lower bounds.

The construction attains them. In the middle ternary case each block length is <=M; total S satisfies M<S<=2M because all three widths are positive. Therefore no label occurs in all three blocks, some label occurs in two, and their union is exactly the first M labels. The other canonical unions are their stated prefixes. These conclusions depend only on child widths and interface feasibility, never on binary-only child structure.

## q=1 joining, for either arity

Initially all child roots have a common label. Expand each child root to P, retaining that anchor. These moves change no child interior coordinate. Normalize children sequentially on ordered fixed P, then contract each normalized child to its width prefix. Unprocessed child roots are P; processed roots contain the first label of P. The active root is fixed at P during its normalization and retains the first label during contraction. Thus the parent stays exactly 1. Only the active child may deviate, with total excursion <=1 by its interface. At completion every child is the prescribed K. No assumption on its descendants' arities was used.

## q=arity joining, for either arity

Child roots initially are pairwise disjoint. Normalize each on its own root in induced P order, then contract. Roots remain disjoint and each normalization starts and ends exact. The remaining compact roles are distinct across children.

Assign those roles to the canonical disjoint blocks. If a desired label is absent from all child roots, use R2 replacement. If occupied, exchange roles. A cross-child exchange x,y first replaces x by y in the first child, then y by x in the second. Both subtree-absence conditions hold. A same-child swap uses three cross-child exchanges with any role in another nonempty child as pivot; the pivot returns to its initial role.

At a binary parent the only possible defect is 2 to 1. At a ternary parent an exchange touches only two children; the untouched third contains neither exchanged label. No triple intersection arises, so the only possible defect is 3 to 2. All child interiors remain exact by R2. Each complete exchange restores pairwise disjointness. Process target roles in order; earlier roles are unchanged at the end of each exchange, including a previously fixed pivot. The finite procedure reaches K.

## Ternary q=2 joining

Select the first overlapping pair of child roots and their first common label x in P order. The third excludes x. Normalize children sequentially with roots fixed. For selected children of width <k=|P|, use x-first order followed by induced P order. All other children use induced P order, including any selected width-k child. Contract each exact normalized child to its width prefix.

The selected pair retains x: an ordinary selected prefix includes x, while a width-k root is P and loses nothing. Deletion cannot create a triple intersection, so the parent stays exactly 2 throughout these contractions and recursive normalizations. The child interface bounds the TOTAL interior deviation, even if its own active defect occurs deep below another ternary vertex.

After this phase every child is compact and all coordinates are exact. A compact child of width <k has a label in P absent from its whole subtree. Assign its ordered roles to the canonical target labels: replace a role directly if its target is absent, otherwise evacuate the occupying role into a currently absent label before assigning the target. Earlier fixed roles cannot occupy a later distinct target. Each replacement uses R2 and preserves all child interiors. Local holes may occur in other children; global absence is unnecessary.

There is at most one width-k child: two roots equal P would intersect the nonempty third. Such a child already has the canonical induced-P role order because it was normalized that way, and its canonical cyclic block equals all P. Do not transport it. All other children can be assigned by local holes. At every transport primitive the sole possible deviation is the parent, whose value is 1,2 or3 and target2. No recursive normalization is invoked in this phase. Complete target assignment restores parent2 and gives K.

## Compactness, equivariance and induction

The canonical union property shows unused labels occur only at the root. Delete them in an attached context to obtain K on the width prefix without changing any interior coordinate. For the leaf, direct contraction gives its single role. Restricting the palette to the prefix does not change any canonical child palette or descendant order.

Fix every discretionary choice by tree order and the supplied palette order: first shared pair, first common anchor, first unused hole, first eligible pivot, and ordered target positions. Under simultaneous relabeling and order transport, these choices and primitive sequences transport identically. This is not invariance under resetting numerical sort after relabeling.

The leaf satisfies all six interface clauses. The joining arguments use only those clauses for strictly smaller children and establish the identical clauses at their parent, with finite recursion and finite role assignments. Structural induction therefore yields I for every finite tree of internal arity2 or3, including arbitrary mixed and repeated ternary composition. An external ancestor stays exact during a child's fixed-root call; during an ancestor's transport, all child interiors stay exact. No part of the argument licenses concurrent defects at different levels.

## Barrier consequence and limits

Reverse one normalization and concatenate with another to connect two exact states on the same fixed root/profile within total excursion1. Within an exact-profile component all independent scalar barriers are0. Between distinct components every path must leave that integer-valued exact profile; each inherited scalar objective has lower bound1. The constructed path attains upper bound1 for each. This does not assert that every profile has multiple components.

The argument concerns existence of legal paths, not their minimal length, unique selection, dynamics, energy, action, metric or gravity. It does not cover arity>=4. Independent proof review, implementation controls, frozen validation and full closure remain necessary before stage certification.
