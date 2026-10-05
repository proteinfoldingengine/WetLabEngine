# A11.X58 — prescribed anchor permutation with coupled pair renewal

Status: frozen analytical candidate; independent review pending. Parent be93a6fef3d089a00f6311ecf2870392b98eaef9. Scope A11_X58_SCOPE.md at dacc35eee084e4f9902609b577f55626d72a1f28. No numerical execution or implementation certification.

## Theorem

Fix a labelled finite role set G, anchors A={0,1,2,3}, outside roles R=G minus A, and an ACTUAL simple graph Gamma_a on R for each anchor a. Declare precisely the actual types
Q={a} union e, e in E(Gamma_a),
with arbitrary positive numbers c_Q of ORIGINAL labelled root copies.

Assume the colored guard
(C) vc(union_(a in J) Gamma_a)>|J|
for every nonempty J subset A.

Fix IN ADVANCE an arbitrary permutation pi of G satisfying pi(A)=A. No anchor or outside relabeling is performed after pi is given.

For t>=1 let the fixed palette consist of pairwise distinct original labels x_(s,h), s in G, 1<=h<=t, and disjoint fixed padding sets Z_j, |Z_j|=p_j>=0. Source groups are
B_j=Z_j union {x_(j,h):1<=h<=t}.
Destination groups are
D_j=Z_j union {x_(pi^{-1}(j),h):1<=h<=t}.
Thus in every column the selected label x_(s,h) moves from owner s to prescribed owner pi(s). Each original copy of type Q has source E_Q=union_(j in Q)B_j and exact labelled destination C_Q=union_(j in Q)D_j. Its individual ORIGINAL floor may be any 1<=f_i<=N_Q=3t+sum_(j in Q)p_j.

There is an explicit finite native path from E to C with 3<=tau<=4 after every one-incidence primitive. It restores every exact original labelled destination support. Every endpoint-differing incidence changes once and no other incidence changes, so the path globally minimizes primitive count. The construction repeats over all t columns and permits arbitrary unequal saturated floors.

This advances X57 from an exchange chosen after compatible labeling to every PRESCRIBED anchor-preserving role permutation on the fixed labelled carrier. Several exceptional pair obligations may coexist. The theorem does not cover permutations that mix A and R.

## Colored footprint guard and exact endpoints

Condition(C) is equivalent, within this actual carrier, to both:
1. A is the unique role hitting set of size at most four;
2. every role footprint F with |F|<=4 and F!=A has an actual avoiding type.

Indeed put J=A minus F and X=F intersect R. If F!=A and |F|<=4, J is nonempty and |X|<=|J|. Condition(C) says X does not cover the actual union graph Gamma_J, so an actual edge e of some color a in J avoids X; actual {a} union e avoids F. Conversely, a cover X of Gamma_J with |X|<=|J| makes (A minus J) union X a role hitting set of size at most four different from A.

Every prepared role group is nonempty and contains t+p_j labels. A physical hitting set projects to owner roles. Thus every source, destination and completed-column state has exact transversal four. One physical label from each anchor group supplies a minimum cover. Copies and padding do not alter this result.

## Exceptional pairs for the prescribed permutation

During active column h, x_(s,h) has old owner s and required owner pi(s). Every other label has one fixed current owner in that column. A physical pair containing at most one active label has footprint size at most three and hence an actual union-avoiding type. A pair of active labels indexed by S={s,t} has footprint
F_pi(S)=S union pi(S).
It lacks the guaranteed common witness exactly when F_pi(S)=A. Because pi(A)=A, this implies S subset A, |S|=2, the four roles are distinct, and
pi(S)=A minus S.

Define the finite exceptional family
E_pi={S subset A: |S|=2 and pi(S)=A minus S}.
Every physical pair outside E_pi has an actual type avoiding its complete old/new support union. Any copy of that type stays inside this union during the edits below, so the witness remains actual even while its root changes.

For S in E_pi, every old root whose anchor color lies in A minus S avoids the two old physical labels. Every completed new root whose anchor lies in S avoids them at the new endpoint, since their new owners pi(S)=A minus S. The lower problem is therefore a simultaneous transfer from color set A minus S to color set S for every S in E_pi.

## Shared reserves and seed cover

Condition(C) on singleton {a} gives vc(Gamma_a)>=2. Hence Gamma_a has at least two distinct edges, and every anchor color has at least two distinct actual root types. Choose once and for all:
- one seed type q_a in each color a;
- a different reserve type r_a in the same color;
- one original labelled copy of each chosen type.
All exist because every declared type has positive multiplicity. A copy is used for only one role in this certificate.

Choose any anchor set T subset A that meets every S in E_pi. Such a transversal exists; T=A always works, and if E_pi is empty take T=empty. Process the selected seed copies q_a for a in T first, in any fixed order. Do not touch any selected reserve copy r_a during this seed phase.

Fix S in E_pi. Until the first seed whose color lies in T intersect S is complete, an old reserve in either color of A minus S remains untouched and avoids the pair. While that first seed is changing, the same old reserve protects it. Once the seed completes, its color lies in S, so it is an actual new witness for the pair and remains completed for the rest of the column. Therefore every exceptional pair is protected throughout the entire seed phase.

After all seeds finish, T meets every exceptional S, so each has a permanent completed new seed witness. Process every remaining original root copy afterward, including unselected copies of seed types and all reserve copies. The completed selected seeds stay fixed. The SAME reserves and seeds may protect many exceptional pairs; no obligation is assigned an independent copy or capacity.

This is a reusable multiple-overlap handover. It supplies an actual next seed whenever its color remains pending, and after the finite seed phase supplies an actual next remaining copy until the column is finished.

## One fixed upper cover and primitive legality

For active column h define the physical anchor-label set
K_h={x_(a,h):a in A}.
At the old endpoint its owner set is A. At the new endpoint its owner set is pi(A)=A. Hence K_h hits BOTH endpoint supports of every actual type.

Use any fixed type order that begins with the selected seeds and then lists all remaining copies. For each active original copy, add every destination incidence missing from its current support, one incidence at a time; then delete every old-only incidence, one at a time. Through additions the root contains its entire old support; through deletions it contains its entire new support. K_h hits it throughout. Every inactive root is at one of its two column endpoints and is also hit by K_h.

The active root never has fewer than N_Q labels, so it retains its own original floor, including unequal saturation. It remains within the fixed palette and its endpoint union. The common witnesses and reserve/seed witnesses above prove every physical pair misses an actual root, so tau>=3. K_h proves tau<=4. Both bounds hold after every literal primitive on the same schedule.

No extra label, slot, weakened floor, simultaneous move, role relabeling or fictitious owner primitive is used.

## Renewal, continuation, termination and exact restoration

For one column, the chosen seeds, remaining copies and their add/delete incidence lists are finite. Empty edit lists are skipped. Whenever a literal edit remains, the first pending edit is legal by the previous section, and the pending count decreases.

After the column completes, each role group again has t+p_j labels: pi permutes one selected label out of and one into every role. Every original root again has its prepared type support and size N_Q. Exact four, condition(C), the same seed/reserve choices and all individual floor bounds remain. An unresolved later column still has its labels at their source owners. Reuse the identical certificate with that column's physical labels.

After h completed columns, exactly (t-h) prescribed columns remain unresolved. This decreases by one after every finite column exchange and reaches zero. Auxiliary owner notation merely records incidence membership; a selected label whose prescribed owner change affects no root incidence requires no native edit. Every listed primitive is an actual incidence toggle.

At completion every x_(s,h) has its prescribed owner pi(s), padding stayed fixed, and every ORIGINAL labelled root copy equals C_Q exactly. For t>=2, every root with a nonzero endpoint difference is unfinished relative to both outer endpoints after the first column; zero-distance roots already equal both and require no artificial changes.

## Global endpoint minimum

In one column, x_(s,h) belongs to source root Q iff s in Q and to destination root Q iff pi(s) in Q, equivalently s in pi^{-1}(Q). The construction toggles exactly those differing incidences once and leaves common, absent and padding incidences untouched. Its length is
L=t sum_Q c_Q |Q symmetric-difference pi^{-1}(Q)|.
This is precisely the outer endpoint Hamming distance. Every native primitive changes one incidence, so no path between the exact endpoints can be shorter.

The seed/reserve ordering therefore adds no incidence overhead despite simultaneously renewing several obligations. L is an analytical identity, not a performance benchmark.

## Four-obligation private-edge control

For every m>=20 use the fixed labelled private-edge carrier
Gamma_0={{8,10},{9,12}},
Gamma_1={{4,6},{11,14}},
Gamma_2={{5,7},{13,16}},
Gamma_3={{15,18},{17,m-1}}.
The eight outside edges are pairwise disjoint and private to their colors. For every nonempty J, Gamma_J is a matching of 2|J| edges, so vc(Gamma_J)=2|J|>|J|. There are exactly eight actual types and no cross-anchor edge intersection.

Prescribe pi=(0 1)(2 3) on A and fix every outside role. No relabeling follows this declaration. Then
E_pi={{0,2},{0,3},{1,2},{1,3}}.
These are four simultaneous exceptional physical pairs. No single anchor color lies in all four sets, so no single completed root color is a new witness for all. Their complements also have empty total intersection, so no single old root color protects all four. The obligations are genuinely distributed.

The seed color set T={0,1} meets all four exceptional sets. Choose one seed and one distinct reserve root in each color as above. During the two seed completions, the four obligations use overlapping old reserves; afterward the two completed seeds jointly protect all four. All eight roots then reach their destinations. This is repeated for every column.

Because pi fixes every outside role and moves every anchor, each one-anchor type differs from its image only in its anchor role. Thus |Q symmetric-difference pi^{-1}(Q)|=2 for every type. With one copy each, L=16t exactly. Arbitrary copies give L=2t sum_Q c_Q. Eight types are minimal within condition(C), because every singleton color graph needs at least two distinct edges. This is not a universal native root minimum.

The full outer endpoint-union tuple has transversal exactly two. Any S in E_pi, for example physical {x_(0,1),x_(2,1)}, has footprint A and hits every root union. Every singleton has a footprint of size at most two other than A and therefore has an actual avoiding union root. No permanent one-label guard or single witness color explains the repair.

The physical set K_h is the unique four-label cover at both singleton one-column endpoints, since A is the unique role cover and each group is a singleton. One upper-cover identity therefore suffices and is necessary in that control. This concerns upper coverage, while four lower pair obligations still require the shared seed/reserve handover.

## Limits and next obligation

The theorem handles every prescribed pi with pi(A)=A on a fixed labelled colored carrier satisfying(C). It uses complete root-copy blocks after a finite seed phase; it does not prove that every arbitrary root order works or that whole-root scheduling is impossible.

Permutations mixing anchors with outside roles can destroy the fixed physical anchor cover and can create a different exceptional-footprint system. Failure of(C), arbitrary exact endpoint accessibility, multiple exchanged anchor blocks, higher target, arbitrary mixed/directed/nested repair and unrestricted native universality remain open. Applicable connectivity was already accepted; this adds a prescribed-order reusable certificate and exact path minimum.

The next analytical question is whether the colored footprint and seed/reserve method extends when pi(A)!=A, requiring a moving upper cover while several lower obligations transfer, or whether a precise compatibility obstruction appears. Unbounded upper-cover stages coupled to several moving lower witnesses remains open.

No numerical execution, enumeration, implementation, efficiency benchmark, integration merge, numbered certification or physical claim is made. Completed v16.54/v16.55, historical failed constructions and all original evidence remain preserved. Separate efficiency runner/fixture/benchmark work remains unstarted.
