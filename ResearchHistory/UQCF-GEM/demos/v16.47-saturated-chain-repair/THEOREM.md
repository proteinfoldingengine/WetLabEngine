# Saturated-chain repair by palette transport
Status: proposed general proof, subject to independent review and prospectively registered validation.

## Objects and target
Let R-U-V be the three internal vertices of a no-unary rooted tree, with degrees a,b,c>=2. R has l=a-1 outer side leaves, U has b-1 middle side leaves, and V has c bottom leaves. Root palette K has k>=2 indexed labels, every nonroot support is nonempty and nested, and moves change one label incidence. Fix an attained profile (r,s,t). v16.46 establishes a common canonical L1<=1 normalization for r<a. We address r=a here.

## Fixed outer partition and inner normalization
Saturation r=a forces supports of all a outer children to be pairwise disjoint. Let S be U's support, ordered increasingly. The subtree rooted at U is a two-internal tree on palette S. If |S|>=2, normalize it with the reviewed v16.44 construction, using the ordered palette S. U's support stays fixed, so outer hitting stays exactly a, while total deviation inside the subtree is at most1. If |S|=1, every descendant support is that singleton and the subtree is already canonical, with s=t=1.

At the canonical endpoint the union of U's child supports uses precisely the first d labels of S, where d=max(s,t) when s<b, and d=b-1+t when s=b. In the latter case pairwise disjoint middle children imply |S|>=b-1+t; otherwise |S|>=max(s,t). Remove unused labels from U, one at a time; no descendant uses them. Shrink each outer side leaf to its least label, deleting other incidences. Outer children stay nonempty and disjoint, so all three profile coordinates are exact throughout these contractions. We now have l distinct outer singleton labels and d distinct nested palette labels, disjoint from each other. Thus k>=l+d. The canonical nested pattern depends only on the ordered roles of these d labels, not their names.

## Clone-before-delete lemma
Suppose label x occurs in U's subtree and y is absent from that entire subtree. Replace x by y by first adding y at every vertex carrying x, in parent-before-child order, then removing x at those vertices in child-before-parent order. Every move is admitted: during addition y is present at a vertex's parent, and during deletion no child retains x after its parent loses x. No support empties because the replacement y is already present.

At every internal vertex during addition, the set of children carrying y is a subset of those carrying x. A hitting set using y can replace it by x, so adding these redundant incidences does not change the hitting number. During deletion the remaining x-incidences are a subset of y-incidences, giving the reverse redundancy argument. Thus q(U) and q(V) remain exactly s,t throughout. This argument also covers internal vertices whose child sets contain neither label. Root R is handled separately below.

## Role exchanges with one outer defect
Each outer leaf is one role; each of the d nested palette labels is one role, carrying its complete fixed canonical incidence pattern in U's subtree. Labels assigned to distinct roles are distinct.

1. Replace a role's label by a globally unused label. For an outer leaf add then delete; for a nested role use the clone-before-delete lemma. All outer children remain disjoint, and the whole profile stays exact.
2. Exchange a nested role x with an outer leaf y. Clone/replace x by y throughout U's subtree, then replace y by x at that outer leaf (add x, delete y). Inner profiles stay exact. Only U and this one outer leaf can overlap, and every other child remains disjoint from both. Root hitting is therefore a or a-1 throughout; after the exchange it is a.
3. Exchange two outer singleton roles x,y by adding y to the first, adding x to the second, deleting x from the first, and deleting y from the second. Only these two children overlap, so again root hitting is a or a-1, with inner profiles unchanged.
4. Exchange two nested roles x,y using any outer leaf as a temporary role z. Perform three exchanges of type2: (x,z), then (y,z), then (x,z), where these names designate fixed roles and their current assigned labels. This swaps the two nested labels and restores the outer role's original label. Every constituent exchange ends at the exact profile before the next begins, so the defects never stack. At least one outer leaf exists since a>=2.

## Common endpoint and conclusion
Order the roles as the l outer leaves first and the d nested palette roles second, retaining their fixed canonical pattern order. For role i=0,...,l+d-1, make its assigned label i: if i is unused use type1; if another role holds i exchange the two roles by types2-4. Earlier completed roles are unaffected at the end of each operation; a temporary outer pivot is restored. This finite procedure reaches labels0,...,l-1 on the ordered outer leaves and labels l,...,l+d-1 on the ordered nested pattern roles.

This is a common canonical endpoint for every state with the target profile. Before label transport, only the inner subtree could have a unit excursion while the outer root stayed exact. During transport both inner coordinates are exact and only the root can deviate by1. Hence total L1 deviation never exceeds1. Reverse one normalization and concatenate to connect any two states of the same target profile. Distinct exact components exclude zero cost for each scalar objective; integrality gives B1=Binf=Bs=1 independently, and the common path gives separately optimized LEX=(1,1,1). Same-component barriers are0.

Combined with v16.46 for r<a, this proves unit barriers between distinct exact components for ALL admitted three-internal-vertex chains of arbitrary a,b,c>=2 and k>=2. It does not prove the universal retained-tree conjecture, longer-chain normalization, or any physical energy/metric/gravity interpretation. Finite audits validate implementation; they do not establish the general quantifiers.
