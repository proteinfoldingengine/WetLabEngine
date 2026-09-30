# A unit-barrier theorem for fully packed partition profiles

## Definitions and claim
Let T be any finite rooted tree with k>=2 leaves and no unary internal vertices. There are k indexed labels, nonempty supports S_v subset K, S_root=K, and S_child subset S_parent. Primitive moves change one label incidence at a nonroot vertex while preserving these conditions. At an internal vertex v with d_v children, q_v is the minimum cardinality of a label set meeting every child support; leaves have q_v=0. Freeze q0_v=d_v at internal vertices. For a state, the three costs are sum_v|q_v-q0_v|, max_v|q_v-q0_v| and the number of nonzero deviations; a path cost is the maximum of the corresponding state cost.

**Theorem.** Every pair of distinct states in this exact profile has B1=Binf=Bs=1 under the three independent scalar minimax objectives. The separate nested LEX triple is also(1,1,1). A finite explicitly legal path exists with at most one unit deviation at any moment. No assertion about other profiles follows from this theorem.

## Exact-profile characterization
For d nonempty sets, their minimum hitting number is d if and only if they are pairwise disjoint. Disjointness requires one distinct hitting label per set. Conversely, if two sets intersect, one label hits both and one label from each of the remaining d-2 sets gives a hitting set of size at most d-1.
Thus sibling supports are disjoint at every internal vertex. Any two leaves separate below their lowest common ancestor, so their supports are disjoint. There are k nonempty leaf supports drawn from k labels; every leaf is a singleton and their labels form a bijection. Prefix closure forces each vertex to contain the labels of all its descendant leaves. It cannot contain a label whose leaf lies elsewhere: at the lowest common ancestor of that vertex and the other leaf, sibling supports would intersect. Hence S_v is exactly the set of labels of its descendant leaves.
Every leaf-label bijection conversely defines an admitted exact-profile state. There are k! such indexed states, each isolated in the exact-profile primitive graph: changing a leaf bijection changes at least two leaf incidences, whereas changing an internal incidence alone contradicts the forced characterization. Therefore every scalar objective has lower bound1 between distinct states.

## Transposition construction
Choose two different leaves x,y, currently labelled a,b. Let v be their lowest common ancestor, P_x the downward path from the child of v toward x through x, and P_y similarly. These paths lie in different child branches. The starting state is a partition-profile state.
1. Add a along P_y in top-down order.
2. Add b along P_x in top-down order.
3. Remove a along P_x in bottom-up order.
4. Remove b along P_y in bottom-up order.
No operation touches v itself or any ancestor of v.

All additions are legal: the parent already contains the added label, and adding membership preserves every other prefix constraint and nonemptiness. Initially a is absent from the entire y branch and b is absent from the entire x branch. Along either branch a newly introduced label occurs in only one child at every internal vertex, so the child supports there remain pairwise disjoint. During removals, every child requiring the removed label has already lost it; off-path children never contained that label. Every on-path vertex remains nonempty because it has the replacement label, in addition to any labels of unaffected descendant leaves. Thus removals also preserve admission.

At v only its two selected child supports can intersect. Their intersection contains a, b, or both while an exchange is incomplete, and no other child support meets those labels. Its hitting number is therefore d_v-1 while they overlap, and d_v otherwise. All other internal vertices retain pairwise disjoint child supports and their original hitting numbers. Coordinates at ancestors of v are unchanged because S_v itself is unchanged. The final state is precisely the partition-profile state with leaf labels a,b exchanged.
Thus every intermediate profile has L1,Linf and support-size deviation at most1. Any leaf permutation is a finite product of transpositions; compose these paths, returning to the exact profile between exchanges. This proves all three independent upper bounds1, matching their lower bounds. Since the same path attains all three bounds, the separate nested LEX optimum is(1,1,1) as well.

This proof allows the deviation coordinate to move between lowest common ancestors during successive transpositions. It makes no universal fixed-coordinate claim and is consistent with the v16.40 compositional obstruction.

## A safe full-support gluing lemma
Suppose a root's child subtrees have endpoint root supports K and endpoint parent profile1. If each subtree has a unit path with its own root held at K and with its own fixed endpoint profile, executing those paths serially is globally admitted. The common parent stays at profile1, and only the currently changing branch can contribute deviation. Thus the global independent scalar barriers have upper bounds equal to the maximum of the supplied branch-path bounds. This is a sufficient path construction; it does not assert equality with unrestricted branch minima, because a global path may change branch-root supports. Failure of this sufficient criterion is not a proof of intrinsic indecomposability. The numerical campaign excludes no cases using it.

## Remaining obstruction and bounded test
Outside the partition profile, some internal q_v is smaller than d_v and sibling supports need not be disjoint. The fresh-label propagation argument above can then fail: a propagated label might already occupy a different child branch. Whether suitable alternative repairs always avoid overlapping deviations is unresolved. The finite campaign covers every attained profile on every four-leaf no-unary rooted tree with four labels, including these overlapping-support profiles. It is a test of that remaining obstruction, not a proof of a universal result from bounded enumeration.

The prospective ADDENDUM.md additionally tests one specified nested five-leaf/four-label overlapping-support profile. That directed case is outside this theorem; it is not an expansion of the theorem claim.
