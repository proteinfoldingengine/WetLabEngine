# Cyclic overlap can be reconfigured without complete modules

Status: candidate analytical proof for independent review. Parent head: 59f708231dd0e57548fc5931a8b0c98156ed8aa0. No implementation, enumeration or numerical execution.

## 1. Native scope and theorem

Fix an ordered palette P of size k>=6 and r root slots, all with floor 3. Partition P into three nonempty labelled parts A,B,C, with sizes a,b,c and orientation A->B->C->A. The cyclic core consists of all triples inside a part, together with all triples of types AAB, BBC and CCA. Every distinct core triple must occupy an actual root slot. Additional roots must contain a core triple and are therefore redundant. All primitive moves toggle one incidence, preserve the palette and every floor, and retain all r slots.

**Theorem AA.** Any two such cyclic-core tuples with the same k and r are connected by a finite primitive path with hitting number in {q-1,q}, where q=k-3. Their part sizes, labels, orientation descriptions and redundant multiplicities need not agree.

This connects endpoints in the cyclic class; primitive intermediate tuples need not belong to that class. It is not a classification of every exact-q endpoint. It directly covers the cyclic family in MODULE_CAPACITY_OBSTRUCTION.md without introducing its unavailable complete-module destination.

## 2. Exactness and preliminary normalization

A transversal triple, one label from each part, is independent. Every four-set contains a core root: three labels in one part suffice, and otherwise the distributions are (2,2,0) or (2,1,1). A directed cycle edge between occupied parts supplies a root in the first case; the successor of the doubled part supplies one in the second. Thus the core has independence number 3 and hitting number k-3. Redundant extra roots do not change it.

Keep one representative of each core triple fixed. Expand every extra root to P, one incidence at a time. The fixed core enforces q, and every intermediate extra root still contains its original core triple, so this normalization stays exact-q. P fillers may be retained throughout the argument. They are constraints on the existing palette, not additional root slots.

The core root count is

    R(a,b,c) = C(a,3)+C(b,3)+C(c,3)
               +C(a,2)b+C(b,2)c+C(c,2)a.

Here C(s,t)=0 for nonnegative s<t.

## 3. A directed relocation with exact slot accounting

Suppose a>=b+1 and move one label u from A to its successor B. The part A remains nonempty, since b>=1. All core roots avoiding u are unchanged. On P without u they form the same cyclic core on nonempty parts of sizes a-1,b,c. The four-set proof still applies, including when a part has size one. Since k-1>=5, this fixed family is nonempty and has hitting number (k-1)-3=q-1.

The old and desired numbers of distinct core roots containing u are

    D_old = C(a-1,2)+(a-1)b+C(c,2),
    D_new = C(b,2)+bc+C(a-1,2).

Set e=c-b. Subtraction gives

    D_old-D_new = b(a-b-1)+e(e-1)/2 >= 0.

The last inequality holds because a>=b+1, b>=1 and e is an integer. Thus the existing old-star slots suffice for all desired new-star roots. Assign one desired triple to each of D_new slots and P to the remaining old-star slots. Retain all non-u core representatives unchanged. The previously normalized P fillers can be regarded as editable supports that stay P; they also contain u.

Every editable support contains u at both ends and meets floor 3. Replace each through old support -> union -> new support. The fixed family enforces tau>=q-1; one of its minimum hitting sets together with u hits every intermediate root, giving tau<=q. This is Lemma X, with its hypotheses explicitly checked. The completed state is the cyclic core on sizes a-1,b+1,c with P fillers, and is exact-q.

No clone safety assumption or temporary additional root is used. The core count changes by D_new-D_old and therefore does not increase.

## 4. Balancing terminates, including the directed exceptional case

At completed states define the integer potential as the lexicographically ordered pair

    (a^2+b^2+c^2, R(a,b,c)).

If any directed cycle edge has source size at least two greater than its destination, perform that relocation. The first coordinate decreases by 2(source-destination-1)>0; the core count also does not increase.

Suppose the sizes are not balanced, meaning max-min>=2, but no directed edge has a drop of two or more. A maximum part cannot have a minimum successor. Its successor must be the third part, and the other directed edge on the path to the minimum also has drop at most one. It follows that, up to cyclic rotation, the sizes are exactly (m+2,m+1,m), with m>=1. Move a label from the maximum to its successor. The first coordinate is unchanged (the two sizes swap). In the slot formula a=b+1 and e=c-b=-1, so the second coordinate decreases by exactly one. The new sizes are (m+1,m+2,m), with an available directed drop of two for the next step.

Thus every chosen step is legal, keeps the parts nonempty, does not increase root demand, and strictly decreases a nonnegative integer lexicographic potential. Alternatively, every exceptional step is immediately followed by a step strictly reducing the sum of squares. The process terminates with sizes differing by at most one.

## 5. Common endpoint and full path

The balanced size multiset is determined by k. Its ordered cyclic arrangements are related by cyclic rotations: there is either one size, or two equal sizes and one different size. Consequently a global label permutation sends every balanced cyclic core to one fixed canonical cyclic core on the ordered palette. An orientation described oppositely is handled by naming its parts in its own directed cyclic order before applying the same argument; the resulting balanced core is again isomorphic to the canonical one.

Use the previously accepted label-transposition paths to perform that permutation. Completed states remain exact-q and the primitive paths have tau in {q-1,q}. Normalize every P filler to one chosen core triple while holding the complete core fixed. This remains exact-q. All slots have the same floor, so the accepted root-permutation paths arrange the resulting tuple in canonical root order, again in the unit band.

Both endpoints reach the same ordered tuple; reverse one path and concatenate. All intermediate supports meet their floors. Every completed balancing, normalization or permutation step is exact-q, so one-unit deficits do not accumulate between steps. This proves Theorem AA.

## 6. Interpretation and limits

The normal-form obstruction from Theorem Z remains valid. It coexists with connectivity of the entire cyclic class, now proved directly. Positive slack was not used as a proxy for an exchange path: the proof uses an actual fixed q-1 root guard, an explicit slot inequality and finite progress.

This supplies a reusable cyclic-overlap interface, not another arity-by-arity campaign. It does not prove that arbitrary higher-floor endpoints reach a cyclic core, nor does it establish connectivity between the cyclic class and every other exact-q class. Earlier conditional native lifting applies under its previously stated child-interface assumptions; it is not recertified here. No universal higher-floor theorem, numerical result, efficiency bound, novelty claim or physical implication is asserted.
