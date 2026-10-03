# A8: compatible root swaps do not make completed two-label exchange universal

Status: frozen analytical candidate for independent review. Parent scope commit: 83378979919501b160b51e15458b43d85990d0ea. Relation and completion gate: A8_SCOPE.md. Integrated implementation baseline is unchanged. No numerical campaign, enumeration, tests or workflows.

## 1. Admissibility and the added edge

The completed graph has all admissible tuples with tau>=q as vertices. Its edges are A6 two-label exchanges OR floor-compatible transpositions of two labelled root supports. Completed levels above q are allowed.

A compatible root transposition at a tuple of level p>=q has a primitive lower path with tau>=p-1>=q-1. Put the union of the two exchanged supports in both slots, expanding first and contracting to the exchanged destination. Any cover of the union tuple can be extended by at most one label to cover both originals, so its transversal is at least p-1. All intermediate tuples are contained in the union tuple and contain the appropriate endpoint tuple. Thus their levels lie in {p-1,p}; floors hold by containment of each slot's starting or permitted destination support. This repeats A7's argument at arbitrary p. All changes are finite single-incidence moves.

A6 gives the same lower guarantee for its completed edges. A finite enlarged-graph path between exact-q endpoints can therefore be converted to a primitive unit-band path using the accepted maximum-layer-removal theorem, if upward excursions occur. The issue is existence of that completed path.

## 2. Tight pair-cover slice for general order v

Take q=3, palette size v>=7, uniform floor h=v-3 and r=v(v-1)/6 roots, for integer r and feasible endpoints. Let E_i=P minus X_i. Every admissible complement has size at most three. At a completed tuple, every palette pair must be contained in some E_i, since otherwise that pair hits every support. There are binomial(v,2) pairs and at most 3r=binomial(v,2) covered pair occurrences.

Equality forces every complement to have size three, every pair to occur in exactly one complement, and all complement blocks to be distinct. Thus completed vertices are precisely labelled-slot realizations of Steiner triple systems on the fixed palette. Every such vertex has exact level three: there are more palette triples than complement blocks, and any triple not equal to a block hits all supports. The entire completed graph is in this tight slice; larger support sizes and levels above three cannot provide escape routes.

## 3. Exact characterization of the two-label edges

For distinct u,v, let {u,v,w} be their unique complement block and V=P minus {u,v,w}. Occupancy preservation fixes that both-role block. Fixed outside-pair incidences and block size fix blocks containing neither role. Every block containing exactly one role may only retain or exchange that role.

The outside-role pairs in the u-only blocks form a perfect matching on V. The v-only blocks form another perfect matching, with no shared edge by pair uniqueness. Their union is a disjoint collection of even cycles, each of length at least four. At any vertex x of this graph, preserving unique coverage of {u,x} forces the switch indicators of its incident u-block and v-block to agree. Hence indicators are constant on each cycle.

Conversely switching the role labels on all blocks of any selected collection of whole cycles preserves pair uniqueness: outside-role pairs remain fixed; pairs containing u or v remain uniquely covered at each x; pairs involving w and the pair {u,v} were fixed. Thus this characterization is both necessary and sufficient.

Completed two-label edges are exactly switches on unions of these alternating cycles. A union switch can be decomposed into a finite sequence of individual cycle switches, remaining within completed vertices. This is the classical cycle-switch operation on triple designs, derived here from the native graph conditions. It is not asserted to be a new design-theory operation.

Call a triple design perfect when the matching union is one cycle for EVERY label pair. Then every nontrivial eligible two-label edge is a global palette transposition. Every root-slot edge preserves the unlabelled block collection. Starting from a perfect design, all reachable completed tuples therefore have complement designs isomorphic to that starting design. Perfection is preserved by both operations, so this is an invariant of an entire component, not merely a first-move limitation.

## 4. Explicit 25-label endpoints and one external finite-design dependency

Use P=Z_5 x Z_5, with the fixed identification (x,y) -> 5x+y in Z_25. Set v=25, r=100, h=22 and q=3. All roots are fixed labelled slots.

### Starting complement design D

Form the 100 triples by translating each of these four base triples by every element of Z_5 x Z_5:

    {(0,0),(0,1),(1,0)}
    {(0,0),(0,2),(2,1)}
    {(0,0),(1,1),(2,3)}
    {(0,0),(1,3),(3,3)}.

This exact construction and its perfection are reported in Grannell, Griggs and Murphy, Some new perfect Steiner triple systems, Journal of Combinatorial Designs 7 (1999), 327-330, Introduction, Perfect STS(25). Author preprint: https://grannell.net/Papers/perfect.pdf, PDF page 3. The construction is attributed there to Tonchev's third translation-invariant system.

**External dependency D25:** the displayed translation construction is a Steiner triple system and every pair-derived cycle graph is a single 22-cycle. This finite-design property is used as established primary-source mathematics. It has NOT been locally enumerated, reproduced or independently recertified in this work. The review must verify the source supports the precise construction and property. The new native obstruction is derived from D25; D25 is not represented as a new UQCF result or a locally generated certificate.

Order these triples by base index, then translation (x,y) lexicographically. Define A_i=P minus D_i. D25 supplies distinct blocks and pair uniqueness, so A is an admissible exact-three endpoint.

### Destination complement design E

In Z_25 translate every one of these four triples by all residues:

    {0,1,12}, {0,2,9}, {0,3,8}, {0,4,10}.

This destination is checked algebraically here. The unordered nonzero difference classes in Z_25, represented by 1 through 12, are partitioned by the four bases as follows:

    {1,11,12}, {2,7,9}, {3,5,8}, {4,6,10}.

Each class occurs once. Translation therefore covers every pair exactly once. No base triple has a nonzero translation stabilizer, since a three-element translation orbit cannot have size dividing 25; the difference classes also distinguish the four orbits. There are exactly 100 distinct triples. Identify their labels with P by the inverse fixed bijection, order by base index and translation residue, and define C_i=P minus E_i. This is another admissible exact-three endpoint on the same palette, floors and labelled slots.

E is NOT perfect. For the pair {0,4}, its unique block is {0,4,10}. The six vertices

    5,22,20,17,18,16

form a complete alternating cycle, using the following complement blocks:

    {0,5,22}, {4,22,20}, {0,20,17},
    {4,17,18}, {0,18,16}, {4,16,5}.

Their translations from the listed bases are, in the same order: base 3 plus 22; base 2 plus 20; base 3 plus 17; base 1 plus 17; base 2 plus 16; base 1 plus 4. All arithmetic is modulo 25. Pair uniqueness makes this a separate six-cycle component in the derived degree-two graph, leaving sixteen of its 22 vertices outside. Thus the pair graph cannot be a single 22-cycle.

The perfect design D and the nonperfect design E cannot be isomorphic. Section 3's component invariant proves A,C disconnected in the enlarged completed graph.

**Theorem A8-N, with explicit dependency D25.** Adding every floor-compatible labelled-root transposition to A6's completed two-label exchanges still does not give universal exact-endpoint accessibility. The explicit 25-label, 100-root, floor-22, target-three endpoints above are separated. This covers ALL permitted completed moves in their full admissible domain, including potential above-target completed routes.

The source-backed dependency is essential to this concrete negative instance. Without accepting D25, Sections 2-3 remain self-contained structural theorems and the explicit E construction remains verified analytically, but the perfect starting endpoint would be conditional. No locally self-contained verification of D25 is claimed.

## 5. Primitive one-unit connectivity nevertheless holds for these endpoints

A triple-design endpoint has no single-label hitting set, so the intersection of all its root supports is empty. For each of the 25 labels choose one existing root omitting it. The selected roots form a subfamily of at most 25 roots with empty intersection, hence a level-two guard. Both A and C have such guards.

There are 100 slots. Leave A's selected guard fixed and permute C's supports into a tuple C' that puts its selected guard in slots disjoint from A's guard; at least 75 slots are available. Equal floors make that permutation admissible, and slot permutation preserves exact level three.

Prepare C' at those destination guard slots through one-support union replacements, holding A's guard unchanged. Each support is first expanded by additions and then contracted toward its own destination by deletions. Floors hold. Once the destination guard is complete, hold it fixed and finish every other root. This is a finite primitive path A to C' with tau>=2. Apply the accepted v16.54 maximum-layer-removal theorem to remove upward excursions between these exact-three endpoints, obtaining tau in {2,3}. Then permute C' back to C via floor-compatible root transpositions, whose primitive paths have tau in {2,3} by Section 1.

This establishes primitive unit-band connectivity for the SAME endpoints that the enlarged completed method cannot connect. The primitive conclusion depends on the accepted maximum-layer-removal theorem; its hypotheses apply here (fixed finite palette and slots, positive floors, single-incidence lower path, exact-target endpoints). That accepted dependency is not independently recertified in this analytical unit. No explicit normalized move list or efficiency bound is claimed.

Native lifting still requires its accepted child interfaces. This proof makes no full nested obstruction claim.

## 6. Learning and next obligation

A7's failure arose from restricting labelled-slot rearrangement. A8 repairs that particular omission but finds an obstruction between different unlabelled incidence structures. Safe label-role switches plus safe slot swaps do not span every completed protected configuration.

The defect allowance is a resource for travelling between protected structures; requiring all macro completions to remain exact or above-target can obstruct the chosen mechanism even when a primitive one-unit route exists. This is not a conservation law, geometry insertion or physical claim.

The next task is to characterize a broader native-derived exchange or a renewal interface that may carry level q-1 through a macro boundary, while still proving a finite global path and avoiding a second unit. Simply adding more slot swaps cannot remove the invariant. General primitive higher-floor and full nested connectivity remain OPEN; the original q=4/floor-three diagnostic is not settled here.

This unit is an analytical negative method result, with D25 explicitly sourced and an accepted primitive normalization dependency. It is neither new implementation certification nor independent reproduction of the cited design property. No originality claim is made.

## Primary source audit

1. Grannell, Griggs, Murphy (1999), Some new perfect Steiner triple systems, https://grannell.net/Papers/perfect.pdf. Read Introduction and the exact Perfect STS(25) construction on PDF page 3. This supports D25 and attribution only; none of its search experiments was rerun.
2. Grannell, Griggs, Murphy (1999), Switching cycles in Steiner triple systems, https://grannell.net/Papers/SWITCH2.pdf. Introduction and Theorem 1 identify classical cycle switching and the global transposition for a single spanning cycle. The native edge equivalence and enlarged-relation obstruction are proved above, rather than assumed from a graph-connectivity table.

Primary-source retrieval is read-only. It is not substituted for a newly executed scientific campaign or local certificate.
