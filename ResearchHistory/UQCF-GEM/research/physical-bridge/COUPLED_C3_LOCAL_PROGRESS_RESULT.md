# Safe local progress with unbounded inaccessible reserve capacity

Status: OPEN analytical checkpoint; author proof below, no independent review, execution or certification yet. Parent: 3949cfd085731f29c4b6dd32e8e2938e5b49c4b5. Exploratory finding disclosed BEFORE new finite execution.

## Question and declared objects

Does kappa<|P| together with an actual uniformly safe first changing edit guarantee an absent label is reachable? No, in the following family. This continues the exact static-capacity theorem and removes isolated-source failure from its counterexample. All original hidden completions and floors stay fixed.

For n>=3 use labelled roots L_i={a,c_i}, R_i={b,c_i}, i=1..n, T={f,g,h}, U={f}. Palette P={a,b,c_1,...,c_n,f,g,h}; every label initially active. Floors are 2 on L/R, 3 on T, 1 on U, all saturated. Hidden labels are disjoint, arbitrary and nonempty; Q ranges over ALL original protected completions with full hitting number in 3..4. Operations are one core incidence toggle plus optional NOOP. Supplied core access, routing, source protection and committed progress are unchanged assumptions.

Original core tau=3: a,b,f cover; the L/R family needs at least two labels and T/U need a disjoint third. Maximal original footprints are L, R, J_i={L_i,R_i}, and K={T,U}. Footprints of g,h are {T}, strictly inside K. The addition of g at U is changing and uniformly safe: floors hold, footprints are dominated by K, and a,b,f still cover. Thus the source is not isolated.

## Exact capacity

kappa=7 for n>=2. The L/R roots require 4n incidences, and each of their maximal footprints supplies at most n incidences. At least four labels must be allocated there. T requires three distinct labels allocated to K; none of these can also cover L/R because no original footprint crosses those root groups. Hence at least seven active labels are necessary. Assign two labels to L, two to R and three to K, obtaining seven labels and a three-label cover.

A safe exact target has {a,c_1} on every L root, {b,c_2} on every R root, T={f,g,h}, U={f}. It uses seven labels; c_3,...,c_n are absent. Every footprint is dominated by an original one, floors hold and tau=3, so it is safe for every original protected Q. Static absent capacity n-2 grows without bound.

## Exact reachable component and invariant proof

The complete changing reachable component consists of exactly seven cores: all L/R roots and T stay exactly original, while U is any nonempty subset of {f,g,h}.

Proof by invariant induction, using the original-source universal core-region criterion:

1. Initially the described invariant holds, and EVERY palette label remains active at each invariant state: each c_i at its original pair, a on L, b on R, and f,g,h at T.
2. Every L/R deletion fails its original saturated floor in Q=empty. Every addition of another L/R label enlarges one of the antichain footprints L,R,J_i, and cannot be dominated by any original footprint. Every addition of a gadget label to L/R crosses disjoint maximal-footprint groups and likewise fails domination. Thus no L/R root can change.
3. T has all three gadget labels and no other label. Deleting one violates floor 3 in Q=empty. Adding a L/R label crosses the footprint groups and fails domination. Thus T cannot change.
4. At U a L/R addition crosses the footprint groups, and deletion of its last gadget label violates floor 1. All other gadget toggles at U preserve the invariant.
5. Each claimed state meets original floors, its gadget-label footprints are subsets of original f footprint K, and choosing a,b plus any label in U gives a three-label core cover. Thus ALL seven states are uniformly admissible over the SAME original protected Q. The nonempty-subset cube is connected by single toggles: add f if absent, delete g/h as needed, then reverse such a route to any target subset.

There are nine undirected or eighteen directed changing edges within this component. Optional NOOPs do not enlarge it. No absent-label state is reachable, despite safe first progress and an arbitrarily large static surplus. The prescribed seven-label target is outside this component for n>=2 (at n=2 it has no absent labels but differs at L/R).

This is more than a failed controller: it identifies EVERY allowed outgoing change at EVERY reachable core. It does not prove that progress inside the repair-relevant component would be insufficient; that stronger premise has not been tested.

## Increment and remaining obligations

The inherited antichain lemma and kappa formulation are not new. The increment is a non-isolated reachable component with safe local motion, unbounded static spare capacity, and an exact invariant excluding all reserve release. Static capacity PLUS some safe progress is still insufficient. A positive theorem needs capacity that can be transferred along the component containing the actual target, with floors and an upper cover preserved throughout.

Author argument only at this freeze. Broad C3/general C4/native observer origin remain OPEN. This is no numbered v16/full-stack closure or physical derivation.
