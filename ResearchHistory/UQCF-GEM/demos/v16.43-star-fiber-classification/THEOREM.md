# Exact-fiber classification for every rooted star

Let a rooted star have m>=2 indexed leaves and k>=2 indexed labels. Its root support is K; each leaf has a nonempty subset of K. A primitive move adds or removes one leaf-label incidence while preserving nonemptiness. Let q be the minimum hitting-set size of the leaf supports, with 1<=q<=min(m,k).

**Theorem.** The exact-q graph is connected unless m=k=q. In that exception it has m! isolated states, and between distinct states B1=Binf=Bs=1; the separate LEX triple is (1,1,1). In all connected cases every within-fiber barrier is zero. This classifies stars only; nested branching interactions remain unresolved.

## Contraction to a singleton coloring
Choose a minimum hitting set H of size q. In each leaf select one member of H already in its support and remove every other label, one incidence at a time. Removing memberships cannot decrease the hitting number; H continues to hit every leaf, so it cannot increase above q. The path is exact. At its end all q members of H must be used, or fewer than q labels would hit the original supports. We have a surjective coloring of m leaves with q colors.

## Changing the palette
Set H0={0,...,q-1}. Replace each a in H\H0 by a different b in H0\H: add b to every a-colored leaf, then remove a from those leaves. During addition b's coverage is contained in a's; during deletion a's coverage is contained in b's. Replacing the dominated label in a hitting set proves the optimum stays q. All leaves remain nonempty. Repeat until the palette is H0.

## A spare leaf: m>q
We may recolor a singleton leaf from a to another already-used color b by first adding b and then deleting a whenever another singleton leaf still witnesses a. Every one of the q colors then has a singleton witness among the unchanged leaves; the mixed leaf does not change the hitting number.

Fix anchors sequentially: leaf i must receive color i for i=0,...,q-1. Earlier anchors are fixed and have distinct colors. If leaf i already has i, continue. Otherwise let its current color be a. If a occurs at least twice, recolor leaf i to i. If a occurs only once, first choose an unfixed leaf t other than i whose color occurs at least twice, and recolor t to a. Such t exists because m>q: a duplicated color either has both occurrences unfixed or has a fixed occurrence and an unfixed duplicate; fixed anchors cannot contain two occurrences of the same color. Since a is unique at i, the donor is not i. Now recolor i to i, retaining a at t. All intermediate states are exact by the singleton-witness argument. No earlier anchor moves. Finally recolor each non-anchor leaf to0; its old color is still witnessed at an anchor.

Thus every state reaches the common canonical coloring: leaf i has i for i<q, all remaining leaves have0. This also covers q=1: the surjection already uses a single color after palette replacement.

## A spare label: m=q<k
After contraction and palette replacement, each leaf has a distinct color from H0. Choose spare label c=q outside H0. To exchange colors a,b on two leaves, recolor the first a→c, the second b→a, then the first c→b. Each recoloring adds a globally absent color before deleting the old color. The modified leaf is disjoint from the other singleton leaves throughout, so the hitting number remains m=q. Transpositions yield the canonical ordering. The spare label is absent again after each exchange.

## Fully packed: m=k=q
Hitting number m means all m supports are pairwise disjoint: an intersection would let one label hit two leaves, giving a cover of size at most m-1. The m nonempty disjoint supports exhaust k=m labels, so every support is a singleton and the state is a leaf-label bijection. There are m! such states. No primitive exact move changes one bijection into another, hence they are isolated and every independent scalar barrier between distinct states is at least1.

For a transposition of labels a,b on two leaves, add a to the b-leaf, add b to the a-leaf, remove a from its original leaf, then remove b from its original leaf. The hitting number is m-1 while these two leaves overlap and m otherwise; the remaining leaves are unchanged. Composing transpositions gives a legal path with only the root's hitting number deviating by1. This proves the three matching upper bounds and the separately named LEX triple.

## Scope and interpretation
The proof holds for every m,k>=2 and every feasible q. The finite campaign is the eleven preregistered (m,k) pairs, all attained profiles. It is not exhaustive over nested trees. It shows a lone star has no nonunit obstruction and that only full packing disconnects its exact fibers. It does not prove that local normalizations can be composed across constrained internal supports of a deeper tree.
