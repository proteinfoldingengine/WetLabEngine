# Independent analytical review: recursive binary interface

Verdict: accept the proposed induction for every finite full binary tree, with the leaf and ordering conventions below made explicit. This review is analytical only; no local scientific execution or tests were performed. It does not certify implementation or finite closure output.

## Precise interface

Let T be a finite ordered full binary tree, P a nonempty ordered palette, and q a profile assigning either 1 or 2 to every internal vertex and 0 to leaves. A state assigns a nonempty support S_v to every vertex, with S_root=P and S_child contained in S_parent. The hitting coordinate at an internal vertex is the minimum size of a label set meeting both child supports. It is 1 exactly when those supports overlap and 2 exactly when they are disjoint. Primitive moves add or delete one nonroot label incidence while retaining nonempty nested supports.

Define w(leaf)=1 and, at an internal root with child widths a,b, define w(T)=max(a,b) when q_root=1 and w(T)=a+b when q_root=2.

The induction establishes:

1. **Feasibility:** q is attained on fixed root palette P if and only if |P|>=w(T).
2. **Canonical endpoint:** there is a canonical state K(T,P,q). For an internal root, its left child receives the first a labels and its right child receives the first b labels when q_root=1; when q_root=2, the right child receives the next b labels following the left child's first a labels. Each child is filled recursively. The root support remains all of P. For a leaf, K consists only of the fixed root support P. Thus the union of proper-descendant supports is exactly the first w(T) labels for an internal T; for a leaf, it is empty.
3. **Fixed-root normalization:** every exact state with root P has a finite primitive path to K, keeping root P fixed, whose total profile L1 deviation over all vertices of T is at most 1. Every completed recursive normalization ends with the entire target profile exact.
4. **Role transport:** replacing a complete label role by a label absent from its subtree preserves every internal hitting coordinate of that subtree at every primitive step, even for arbitrary tree shape.
5. **Compact contraction:** after fixed-root normalization, when T occurs as a child of a larger tree, its root can be contracted to its first w(T) labels without changing its internal profile. For a leaf, contract directly to the first label. These are nonroot moves in the larger tree, although not moves in the fixed-root standalone interface.
6. **Ordered-palette equivariance and phase boundaries:** simultaneous relabeling of labels and of the ordered palette relabels canonical endpoints and paths. Recursive normalization and each completed cross-child exchange have exact endpoints. A numerical-order implementation need not be equivariant if labels are permuted while its palette order is reset; that implementation property must not be confused with this ordered-palette statement.

## Inductive proof

For a leaf, feasibility requires only nonempty P, its fixed-root normalization is the empty path, and its parent may contract it to P's first label. There are no hitting coordinates inside the leaf to disturb.

Suppose the interface holds for both child trees. If a state attains q, the child palettes have sizes at least a and b by the induction hypothesis. When q_root=2 these palettes are disjoint, giving |P|>=a+b. When q_root=1, |P|>=max(a,b). The recursive canonical construction above attains the profile whenever these inequalities hold, proving both directions of feasibility and defining the common endpoint.

When q_root=1, first expand each child-root support to P, one incidence at a time. Initially the child palettes share an anchor. That anchor is retained, so the parent's coordinate remains 1 throughout expansion. A child's own hitting coordinate depends on its children, not on its own support, so all inner profile coordinates remain exact. Normalize the first child on fixed palette P, then contract its root to the first a labels; normalize the second child on fixed palette P, then contract its root to the first b labels. During the first normalization the opposite root is P. During the second normalization the first child retains P's first label and the opposite root remains P. Therefore the parent's coordinate stays 1. Contraction removes only labels absent from proper descendants; its internal profile remains exact. Leaf contraction is direct. Both child palettes retain the first label. Only the currently normalizing child can deviate, and its entire excursion has total L1 at most 1 by induction. The resulting state is K(T,P,q).

When q_root=2, normalize each child on its own fixed initial palette and contract it to its required width. Throughout these two phases the child palettes remain disjoint and the parent's coordinate stays exactly 2. Each recursive phase has total L1 at most 1 and finishes exact. The remaining a+b child labels are distinct complete roles. They can then be transported to the prescribed consecutive labels of P using the operations proved below. During transport every internal child coordinate stays exact and only the parent's coordinate may drop from 2 to 1. Every completed role operation restores disjointness. Thus the overall path still has total L1 deviation at most 1 and finishes at K.

## Complete-role transport

Let x be a role and y absent from the entire destination subtree. Add y at every vertex carrying x in parent-before-child order, then delete x at those vertices in child-before-parent order. Every addition has y already present at the parent, including the subtree-root parent outside the destination subtree. Every deletion has already removed x from the relevant children. Supports remain nested and nonempty.

At every inner vertex during the addition phase, the immediate-child incidence set of y is contained in that of x, and x's incidence set is unchanged. Adding a dominated incidence set cannot improve the minimum hitting size: any hitting set using y can replace y by x without increasing its size. During the deletion phase, y has x's complete original incidence set and the remaining x-incidence set is contained in y's. The same replacement argument proves the hitting size is unchanged. The argument is local to each vertex and does not depend on subtree shape or depth. It also covers a leaf, vacuously.

For a cross-child exchange of x in the left child and y in the right child, replace x by y throughout the left child and then y by x throughout the right child. Both absence conditions hold. Initially y is absent on the left. After the first replacement x is absent in both subtrees. At completion, palettes are again disjoint with roles exchanged. Inner coordinates stay exact; only the binary parent's hitting coordinate can temporarily equal 1. A same-child swap is the three cross-child exchanges (i,p),(j,p),(i,p), where p is any opposite-child role. Both widths are positive, so p exists. These operations restore p and exchange i,j, and each constituent operation has an exact endpoint.

Enumerate left roles followed by right roles. At each position, replace by its prescribed label if that label is globally unused below the parent; otherwise swap with the role currently carrying it. Earlier completed positions are restored by any pivot use. This finite assignment procedure reaches the prescribed labels. Replacing by a globally unused label preserves the parent's disjointness throughout. Sequential exact endpoints prevent deviations in separate phases from accumulating.

## Consequence

Reversing one normalization and concatenating it with another connects any two states of the same attained profile within total L1 deviation 1. For pairs in distinct exact-profile components, every path must have a nonzero integer profile deviation somewhere. Therefore the separately minimized scalar barriers B1, Binf, and Bs are each exactly 1; within one exact component they are 0. A separately defined joint lexicographic objective has value (1,1,1) between distinct exact components, provided its coordinates are the corresponding maximum path deviations. This does not make a claim about general higher-arity interfaces.

## Frozen directed corpus

With C=(L,L), F=(C,C), N=(F,C), and D=(F,F), N has five internal vertices and eleven total vertices; D has seven internal vertices and fifteen total vertices. Assign every internal profile in {1,2}^5 and {1,2}^7 respectively. For each profile let M=w(T); use k=M and M+1, each of identity/reversal/cyclic global label permutations, and compact/overlap_inflated start modes. The number of specification records is (32+128)*2*3*2=1920. Coinciding starts under small palettes are allowed and should not be deduplicated if the protocol promises 1920 specification records.

The compact start is canonical, followed by the selected global relabeling. For overlap_inflated, traverse internal vertices in preorder; at every target-1 vertex expand both immediate child roots to that vertex's current palette. Every expansion respects nesting. The two child supports already overlap and retain a common label, so the vertex remains at hitting 1; the changed child root's own hitting coordinate is unaffected. Preorder ensures that palettes enlarged by an earlier ancestor are correctly available at later vertices. All profile coordinates therefore remain exact. The root palette remains fixed.

An independent path verifier must check every recorded primitive, nonempty nested supports, the fixed global root palette, exact initial/final profile, the canonical endpoint, and total L1 over all vertices at every state. Finite directed success is implementation evidence only. Failed construction is not a certified nonunit obstruction; a negative scientific verdict needs an independently verified unit-neighborhood cut or equivalent proof.
