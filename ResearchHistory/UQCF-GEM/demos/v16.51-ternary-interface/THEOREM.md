# Independent analytical review of the v16.51 ternary interface

Verdict: **the frozen analytical construction satisfies T1–T6**, with the ordering, full-palette exception, and phase conditions made explicit below. This is an analytical proof review, not implementation acceptance, numerical validation, or campaign certification. No numerical science or tests were executed in preparing this review.

Scope: one ternary root whose three children are arbitrary finite ordered full binary trees. This does not establish repeated ternary composition or any higher-arity theorem.

## Setup and inherited interface

Write the ordered global palette as P, its cardinality as k, the three binary child trees as A,B,C, and their positive inherited widths as a,b,c. Every binary internal target is 1 or 2. A leaf has width 1. Supports are nonempty, nested, and the global root remains P. An elementary move changes one nonroot incidence.

The v16.50 THEOREM.md supplies the following precise ingredients: width necessity and sufficiency on a fixed child root; canonical binary descendants on an ordered fixed palette; normalization from every exact state with total child excursion at most 1; exact normalization endpoints; parent-before-child addition and child-before-parent deletion for complete-role replacement by a subtree-absent label; contraction of a normalized attached root by removing unused labels; the direct leaf contraction convention; and equivariance when palette order is transported with labels.

A useful distinction is that K(D,Q), with fixed root Q, need not have a compact root. After contracting to its first w(D) labels, it is exactly the compact canonical binary state with those labels in that same order. Every compact label therefore represents one of w(D) ordered roles. Replacing complete roles changes their names while retaining that abstract ordered-role state.

## T1: three-child classification

For three nonempty supports, a singleton hits them all exactly when their triple intersection is nonempty. If every pair is disjoint, every hitting set has at least three members, and three suffice. If some pair intersects, a shared label together with any label of the remaining support is a hitting set of size at most two. Consequently hitting two is exactly the condition of empty triple intersection and at least one intersecting pair.

Every admitted ternary coordinate is in {1,2,3}. Thus when its target is 2, its deviation never exceeds 1. This fact is usable only while all child interiors are exact; it does not justify overlapping a root defect with a binary normalization defect.

## T2: widths and prescribed supports

Let S=a+b+c.

For target 1, k≥max(a,b,c) is necessary from child feasibility. Taking initial segments of lengths a,b,c gives triple intersection and attains this bound.

For target 3, the child roots must be pairwise disjoint. Child feasibility gives k≥S, and consecutive disjoint blocks attain it.

For target 2, absence of a triple intersection means each palette label belongs to at most two child roots. Hence S≤|S_A|+|S_B|+|S_C|≤2k, and separately k≥max(a,b,c). This proves necessity of

M=max(a,b,c,ceil(S/2)).

For sufficiency take the frozen consecutive blocks of lengths a,b,c in positions 0,...,S−1 modulo M. Each block has length at most M and therefore contains its required number of distinct labels. Since all three widths are positive, M<S, and since S≤2M no label occurs more than twice. There is no triple intersection and, because S>M, some label appears twice. T1 proves hitting two. The union of these roots is exactly the first M labels of P. Give each root its induced P order and the inherited binary canonical descendants. This constructs the frozen endpoint for every k≥M.

## T3: normalization and contraction with a retained pair

Start from an arbitrary admitted exact state with root target 2. T1 supplies two child roots containing a common label x, with x absent from the third. Fix this choice before normalizing any child.

For each selected child whose width is strictly less than k, order its initial root palette with x first, followed by its other labels in induced P order. For an unselected child use induced P order. There is one exception: any child of width k uses induced P order, even if selected. Such a child has initial root P, and contraction will remove nothing, so it retains x without x being first.

Normalize the children sequentially using their fixed initial roots. During each such normalization all three child-root supports are fixed, so the ternary coordinate is exactly 2. The other two child interiors are exact, and the inherited normalization has total excursion at most 1. At its endpoint all child interiors are exact.

Contract that attached child root to its first width-many labels, or to the first label when it is a leaf. For a selected nonfull child this retains x by the order choice. A selected full child retains all P. The selected pair therefore continues to share x throughout every contraction. Deletions cannot create a triple intersection. Thus the ternary coordinate stays exactly 2 throughout contraction as well. This reasoning also applies when contractions and successive normalizations are interleaved: the witness pair survives and the third continues to exclude x.

At completion every child is a compact canonical state on some ordered role list, the entire profile is exact, and the ternary coordinate remains 2.

## T4: transport and the full-palette exception

For a compact child of width w<k, its w role labels are distinct and its root contains exactly those labels. Any label in P outside that root is absent from the entire subtree. It is a usable local hole regardless of its occurrence in other children. The external parent P contains both the old and replacement labels.

To assign the w roles to their prescribed, pairwise distinct target labels, fix roles in order. If a role already has its target, continue. If its target is absent from the child, replace its complete role by that target. If its target belongs to another role, that other role is not an earlier fixed role, because prescribed targets are distinct. Evacuate that other role into any currently absent label, then replace the current role by its now-absent target. Each complete replacement preserves the child's internal profile and compactness at completion. Earlier fixed roles are never touched. There are finitely many roles and at most two replacements per newly fixed role. This proves arbitrary assignments and permutations, including a final target support with no globally unused label.

Each complete replacement is realized by the inherited legal incidence sequence. Its temporary root may have w+1 labels, which is allowed because w<k. All child interior coordinates remain exact at every primitive. For target 2 the sole possible defect is at the ternary root, and T1 bounds it by 1. Consecutive role replacements need not restore the ternary target individually; this is harmless because there is no child normalization during this phase. The completed transport to all prescribed supports restores the whole profile exactly.

A child with width k needs separate treatment. Its initial root must be P. Since the initial triple intersection is empty, the other two child roots are disjoint. There cannot be two width-k children: their roots would both equal P and the nonempty third root would create a triple intersection. For the unique possible full child, the T3 normalization used induced P order, so its compact state already has exactly the desired ordered canonical descendants. It is never transported. Indeed its prescribed cyclic block has length k: feasibility gives w=k≤M≤k, so M=k, and any length-k block modulo k is P. Sorting its prescribed support by P therefore gives exactly the order used in T3. The other two children have widths below k and use the local-hole construction. Their supports may overlap transiently, but with exact interiors this causes at most the permitted root-only defect.

The distributed triangle A={a,b}, B={b,c}, C={a,c} is included: choose any shared pair and its shared label, which the third excludes. No assumption of a globally unique overlap, global spare, or simultaneous shared anchor is used. During subsequent transport triple sharing is allowed because the target is 2 and the child interiors are exact.

## T5: admission, endpoint, contraction, equivariance, and consequence

The inherited binary normalization is finite and legal. Root contractions delete only labels absent from proper descendants; for leaves there are no descendant restrictions. Retaining the specified prefix ensures a nonempty root. Complete-role additions proceed parent before child, and deletions child before parent, preserving nesting and nonemptiness. Their external parent is the fixed global P. No step changes that root.

The two classes of phases obey different and sufficient global bounds. During child normalization, the ternary root and other child interiors are exact, so the sum of all internal absolute deviations is at most 1. During contractions the whole profile stays exact. During target-2 role transport all interiors remain exact, so only the ternary root may deviate, by at most 1. The boundary between normalization and transport is exact, and the final state is the prescribed common canonical endpoint, including sorted-P internal role order. There is no stacking of defects.

The canonical immediate-child roots cover exactly the first M labels for each ternary target, and every proper descendant lies within that union. If this whole single-ternary object is itself attached to an external parent containing P, its root may therefore be contracted from P to the first M labels by deleting unused labels. This preserves its own entire profile. This attached contraction alone is not a normalization theorem for a larger tree containing multiple ternary vertices: its external parent's coordinate would require a separate argument.

To obtain an equivariant deterministic path, select a shared pair by child order and its label by the given P order, order all remaining labels by P, and select holes by P order. Relabel both labels and palette order together. All selections, inherited normalizations, complete-role moves, and endpoints then relabel identically. Permuting labels while resetting their numerical sort order is a different operation and is not the claimed equivariance.

Reversing one normalization and concatenating it with another joins any two exact states of this same scoped profile with total excursion at most 1. Within an exact-profile connected component, each inherited scalar barrier is 0. Between distinct exact-profile components, every connecting path has a nonzero integer defect somewhere; combining the inherited integer lower bound with this path gives barrier 1 for each of the three independently minimized scalar objectives. This is a combinatorial conclusion only, with no selected physical evolution, path-length, or uniqueness claim.

## T6: boundary targets

For target 1, initially retain any common anchor while expanding all three child roots to P. The expansions change no child interior and preserve the triple anchor. Then normalize each child on induced ordered P and contract it to its first width-many labels, sequentially. During the first normalization the other two roots equal P. During later normalizations every previously contracted child contains the first label of P and every unprocessed child root equals P. Contractions also retain that first label. Thus the root stays exactly 1 while at most the active binary child contributes a unit excursion. The endpoint is the prescribed initial-segment endpoint. Expansion need not retain the original anchor after all roots have become P.

For target 3, start with disjoint child roots. Normalize each on its induced P order and contract; disjointness persists. This yields distinct roles across all three children. To assign canonical labels, use globally unused-label replacements or cross-child exchanges as in the binary interface. In a cross-child exchange of x in one branch and y in another, first replace x by y throughout the first, then y by x throughout the second. Only these two branches are touched and the third contains neither x nor y. At every primitive any shared root label is absent from the third branch, so no triple intersection occurs. The ternary coordinate can decrease from 3 to 2, but never to 1. Every completed exchange restores pairwise disjointness. A same-child swap is three such exchanges using a role in either other child as pivot; both other children are nonempty. Globally unused-label replacements preserve pairwise disjointness throughout. The finite binary-style role assignment argument therefore reaches the prescribed three disjoint blocks with all child interiors exact and total excursion at most 1. Exact endpoints between exchanges prevent separate defects from accumulating.

## Review conditions for implementation

The proof accepts the mathematics, contingent on faithfully implementing the stated distinctions. In particular: x-first must be used where contraction could lose x; a width-k child must use sorted P from its initial normalization and never be transported; target-2 transport may use a child-local hole even when it is occupied elsewhere; role position, not merely root support, must be assigned to the canonical sorted-P order; and no binary normalization may run while the ternary root is defective. Every primitive must be checked against the global sum, not just a maximum coordinate or separate subtree budgets.

Finite cases cannot replace this proof, and this proof cannot certify finite coverage, implementation, manifests, workflow provenance, reproduction, or publication. Those campaign gates remain separate.
