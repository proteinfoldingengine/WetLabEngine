# A forced cycle resolved within a compact higher-floor carrier

This symbolic family checks the buffer mechanism analytically. It is not a numerical campaign or a new classification of the already solved five-root target-four class.

Fix any h>=3. Partition the fixed palette into four disjoint sets X_1,X_2,X_3,X_4, each of size h. Thus k=4h. Use five labelled root slots, all with floor h. Choose E subset X_1 union X_2 of size h that meets both X_1 and X_2. Such E exists, for example one label from X_1 and h-1 from X_2.

Let

    A=(X_1,X_2,X_3,X_4,E),
    C=(X_2,X_1,X_4,X_3,E).

Both endpoints are compact at their floors and have transversal exactly q=4. The four disjoint block roots force four labels; choose the label from X_1 inside E intersect X_1 and one from each other block to obtain a four-label transversal of all five roots. The same argument applies after permutation of the four block roots.

The carrier has k=4h<5h=sum_i a_i, so the global palette-room theorem does not apply. No spare native label or extra root is used. This family still lies in the earlier five-root target-four connectivity theorem; the advance here is explanation and repair of its selected forced cycle, not a new endpoint-class result.

## 1. Unbuffered fixed preparation forces opposite orders

Take I={1,2,3}, J={1,2,4}, K={1,2}, t=3. Both endpoint guards consist of three disjoint block supports and have transversal three. Prepare root 4 to X_3. Without changing root 5, the fixed roots are X_3,X_3,E.

Choose x in E intersect X_1, y in E intersect X_2, and z in X_3. The set {x,z} hits the fixed roots and has L={2}, R={1}, forcing 1->2. The set {y,z} hits the fixed roots and has L={1}, R={2}, forcing 2->1. These singleton miss sets offer no alternative witness choices. The unbuffered sequential method is therefore impossible after this preparation.

The full shared union bridge also fails: roots 1 and 2 both become X_1 union X_2, while roots 3 and 4 equal X_3 and root 5 equals E. A label in E plus a label in X_3 hits all roots, giving transversal two.

## 2. Existing root 5 supplies the missing protection

Use T={5}. Now F_0 consists of roots 3 and 4, both X_3; root 5 is deliberately omitted when deriving obstructions. Any H of size at most two hitting F_0 contains a label from X_3. Its old/new miss sets are disjoint exactly when its other label belongs to X_1 or X_2. Otherwise both miss sets contain both shared indices. Hence every H in Q lies in X_1 union X_2 union X_3, and collectively these H use every label of that union.

Assign all Q to buffer 5. Then W_5=X_4 and |W_5|=h=a_5. Install Z_5=X_4 while the old guard I remains unchanged: expand E to E union X_4 and contract to X_4. This is a legal floor-safe replacement in the original fifth slot. No new support is treated as an additional root.

Prepare root 4 to X_3, then replace shared roots 1 and 2 in either order through their unions. Throughout this shared stage, root 5 is X_4, roots 3 and 4 are X_3, and the two shared roots are nonempty subsets of X_1 union X_2. These three disjoint label regions force at least three hitting labels, and four suffice. Thus tau is three or four at every primitive step. Every support contains its old or destination h-element support during its individual replacement.

The completed destination guard J is (X_2,X_1,X_3). Hold it fixed while restoring root 3 to X_4 and buffer 5 to E, through their unions. This returns exactly to C and renews exact-q redundancy. In fact the full path has transversal three or four directly: preparation retains four disjoint block constraints or three such regions, and restoration first regains the four disjoint block roots before removing the buffer support. The general B2 result does not depend on this example-specific upper bound.

The buffer works because it is missed by EVERY obstruction responsible for the forced cycle, and it fits its original floor exactly. Total capacity alone did not select this role. The label pool X_4 and the existing fifth slot provide a concrete admissible certificate.
