# A11.X64 — exact cycle-breaking slack law for unit witness handovers

Date: 2026-10-06 UTC.
Status: analytical candidate for fresh independent whole-argument review.
Corrected prospective scope: A11_X64_SCOPE.md after commit 6bd94daa6d22f7ade70ff13aece755a54b4ecb87. The earlier scope commit 935304c7a9201e972d752b8286233ad894a74bdc incorrectly said an endpoint-union hit alone made an upper cover static; it was corrected BEFORE this proof candidate.

Accepted parent: A11.X61 candidate f8b96d1fabb4cd15b87cb943a8d87f0f470a9463.
Pending X62/X63 are not assumed accepted.

## 1. Unit native domain

Fix ORIGINAL labelled exact-four endpoints E=(E_i), C=(C_i) on finite palette P with same original positive floors f_i.

Every changing root i has exactly one destination-only incidence a_i and exactly one source-only incidence d_i. Thus
C_i=(E_i minus {d_i}) union {a_i}.
All other roots are unchanged. Common incidences never move.

Call i SATURATED when |E_i|=f_i. Otherwise |E_i|>=f_i+1 and i has at least one unit of initial slack.

Assume a fixed physical set H, |H|<=4, such that

    H intersect E_i intersect C_i != empty

for EVERY root i. Hence one common H incidence in each root never moves; H is a genuine static upper cover through every endpoint-only event order.

For every physical pair K choose either:

COMMON: an actual root w with (E_w union C_w) intersect K empty; or

TRANSFER: actual roots v_K,u_K with
    C_v intersect K=empty,
    E_u intersect K=empty,
and neither is a common witness.

In this unit domain a transfer has:
- d_v in K and a_v notin K, so deleting d_v creates the new witness v;
- a_u in K and d_u notin K, so adding a_u destroys the old witness u.

Declare dependency edge v->u. Let T be the resulting directed root multigraph; duplicate edges are harmless.

The declared certificate asks for a minimum endpoint-only path using each a_i addition and d_i deletion once, preserving the chosen lower witnesses and fixed H.

## 2. Exact event graph

Create native events A_i=add a_i and D_i=delete d_i for every changing root.

Floor edges:
- if i is saturated, add A_i -> D_i;
- if i has slack, add no floor edge.

Transfer edges:
- for every declared dependency v->u, add D_v -> A_u.

Call the resulting digraph G_unit.

### Floor exactness

If i is saturated, D_i cannot occur before A_i: it would lower size from f_i to f_i-1. After A_i, D_i is legal.

If i has at least one slack unit, either order is floor-legal because the root has only one deletion. D_i first leaves size |E_i|-1>=f_i; A_i first only enlarges it.

Thus the floor edges are exactly the mandatory floor precedences in this unit domain.

### Lower exactness for the declared witnesses

For transfer v->u, old witness u avoids K until A_u occurs. New witness v avoids K from D_v onward. Therefore D_v -> A_u is sufficient for overlap: before D_v, u remains actual; after D_v, v is actual.

It is also necessary for THIS chosen two-witness handoff if no common witness is being used: if A_u occurs before D_v, then immediately after A_u and before D_v neither chosen root avoids K.

COMMON pairs need no precedence edge because their actual union witness avoids K throughout.

All pair obligations share the same event graph. No independent root capacity is allocated.

## 3. Cycle projection theorem

**X64C.** G_unit is acyclic if and only if the subgraph of T induced by saturated roots is acyclic.

### Proof: event cycle implies saturated root cycle

Every edge leaving an A_i vertex is a floor edge A_i->D_i, and such an edge exists only for saturated i. Every edge leaving a D_i vertex is a transfer edge D_i->A_j.

Hence any directed cycle in G_unit must alternate

    A_i -> D_i -> A_j -> D_j -> ...

Every root whose A_i->D_i edge occurs is saturated. Projecting each segment D_i->A_j to dependency i->j yields a directed cycle of T using only saturated roots.

### Proof: saturated root cycle implies event cycle

Conversely suppose T has a directed cycle

    i_1 -> i_2 -> ... -> i_l -> i_1

with every i_j saturated. Transfer edges give

    D_(i_j) -> A_(i_(j+1)),

and saturation gives

    A_(i_(j+1)) -> D_(i_(j+1)).

Alternating these edges around the root cycle produces a directed cycle in G_unit.

Thus the two acyclicity statements are equivalent.

Multiple pair obligations or parallel dependency edges do not alter the argument.

## 4. Direct minimum repair theorem

**X64U.** The declared unit witness-handover certificate admits a native direct-band minimum repair if and only if the saturated induced dependency graph T_sat is acyclic.

When acyclic, execute the lexicographically least topological order of G_unit.

Every addition is absent and every deletion present because each endpoint-differing incidence occurs once. Section2 proves every original floor.

For every physical pair, either its common actual witness persists or its transfer edge ensures the old actual witness survives until the new actual witness is created. Therefore no two-label set hits every root and tau>=3 after every primitive.

The common incidence H intersect E_i intersect C_i remains in every root, so H hits every state and tau<=4.

The finite event list terminates with every changing root exactly at C_i and every unchanged root untouched. Every endpoint-differing incidence changes once and no common incidence changes, so path length is

    sum_i |E_i symmetric-difference C_i|,

the global endpoint Hamming minimum.

If T_sat has a directed cycle, Section3 proves the chosen floor plus witness-transfer precedence constraints are inconsistent. This is impossibility of THIS DECLARED CERTIFICATE, not native disconnection and not impossibility under different witnesses, transient witnesses, moving covers, or nonminimum temporary incidences.

## 5. Feedback-vertex corollary

Consider the abstract design question where T and all endpoint/witness incidences are fixed, but one is free to designate selected changing roots as having one unit of initial slack instead of saturation.

A root with slack removes its mandatory A_i->D_i floor edge. By X64C, feasibility is equivalent to the slack-root set intersecting every directed cycle of T.

Therefore the minimum number of roots that must receive one slack unit is exactly

    fvs(T),

the minimum directed feedback-vertex-set cardinality of T.

More generally, a chosen slack set works exactly when deleting those vertices from the saturated dependency graph makes it acyclic.

This is a combinatorial resource theorem. It is NOT physical energy, action, cost, time, or a permission to alter floors in an already fixed native problem.

## 6. What the theorem teaches

Slack is not required throughout an acyclic dependency region. It is needed by this unit certificate only to break closed chains of mutual precedence.

Equivalently, the obstruction is not 'too little total room.' It is circular ordering:

    replacement needed before deletion
    -> witness deletion needed before another addition
    -> ...
    -> returns to the first replacement.

One slack root cuts the floor edge at one point on such a cycle and opens a topological order. Several overlapping cycles require a slack set hitting all of them; the exact minimum is the directed feedback-vertex number.

This identifies a precise distinction between local capacity and global dependency topology.

## 7. Relation to accepted and pending work

X61 permits general root batches and moving covers; X64 instead freezes a common upper cover and solves an exact unit lower-handover obstruction. Neither subsumes the other.

Pending X62/X63 aim at more general event certificates. X64 does not rely on their acceptance.

Accepted X36 demonstrates why X64 must remain scoped. X36 repairs floor-saturated cyclic ownership dependencies by a richer multi-unfinished-root mechanism with incoming-before-outgoing additions and actual transient protection. Thus a saturated cycle in X64's chosen endpoint-witness dependency graph is a method obstruction, not a universal repair obstruction.

The next question after review is to generalize the exact cycle law when a root has several additions/deletions and several slack units. The natural object is then a capacitated feedback problem: determine whether local slack/matching capacity can break every alternating floor-witness-cover cycle without assuming independent capacity for shared obligations.

No numerical execution, workflow, implementation, benchmark, integration merge, numbered certification or physical claim. v16.54/v16.55 and all original evidence remain unchanged. Separate efficiency implementation remains unstarted.
