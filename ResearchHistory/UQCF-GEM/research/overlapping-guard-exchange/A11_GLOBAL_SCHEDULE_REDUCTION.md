# A11: exact global interval scheduling for destination-directed repairs

Status: candidate analytical reduction for independent review. A11's global schedule-existence question remains OPEN. Scope parent: 4e958ed23e0a8b3db2f741cf2b7ead1eae713250. No numerical campaign, enumeration, tests, implementation or workflows.

## 1. Candidate global path class

Fix finite palette P, labelled slots, positive floors and exact-four endpoints A,C. Let

    E+={(i,x): x in C_i minus A_i},
    E-={(i,x): x in A_i minus C_i},
    n=|E+|+|E-|.

A destination-directed schedule is a permutation of these n distinct events. Each addition/deletion is performed once. Every common incidence stays fixed. Different roots may interleave arbitrarily, including partially repaired roots. This class is broader than the accepted A2 whole-root, add-all-then-delete schedules, but remains a restriction of the full native graph: it excludes additional temporary incidences and repeated toggles.

The primary question is whether every admissible exact-four pair has some safe schedule in this class. No answer is proved here. A negative answer for this class would not be a primitive barrier, and a failed chosen order would not even be a class obstruction.

## 2. Exact floor constraints

Give each event its position p(e) in {1,...,n}. State s is the tuple after the first s events, for 0<=s<=n. Write N_i+(s) and N_i-(s) for the numbers of addition and deletion events at root i performed by then. The support cardinality is exactly

    |X_i(s)|=|A_i|+N_i+(s)-N_i-(s).

Hence all native floors hold exactly when, for every root i and every prefix s,

    N_i-(s)-N_i+(s) <= |A_i|-a_i.

Each event remains a genuine single-incidence toggle: an addition was initially absent and has no deletion event, and a deletion was initially present and has no addition event. No separate eligibility assumption is hidden in the permutation.

These constraints permit all intermediate sizes allowed by the original floors. Neither compact-only intermediates nor whole-root completion boundaries are imposed.

## 3. Pair protection is an exact interval at every root

For each two-label set H subset P and root i, first check common incidences. If H intersects A_i intersect C_i, root i always meets H and never protects against it. Give it an empty protection interval.

Otherwise all initial H incidences at i are deletion events and all final H incidences at i are addition events. Define

    d_i(H)=max{p(i,x): x in H intersect A_i}, default 0;
    b_i(H)=min{p(i,x): x in H intersect C_i}, default n+1.

At prefix s, root i misses H exactly when

    d_i(H)<=s<b_i(H).

Indeed all its original H labels must have been deleted, while none of its destination H labels may yet have been added. There are no other possible H incidences in a destination-directed path. Thus the protecting prefixes are the discrete interval [d_i(H), b_i(H)-1], intersected with {0,...,n}; when d_i(H)>=b_i(H), it is empty.

This interval includes four cases:

- old-only protection: initial root misses H, destination meets it; d=0;
- new-only protection: initial root meets H, destination misses it; b=n+1;
- permanent protection: both endpoints miss H; d=0,b=n+1;
- transient protection: both endpoints meet H through different labels, but all old H incidences are deleted before any new H incidence is added; 0<d<b<n+1.

A common H incidence rules out transient protection. A root that meets H at both endpoints must therefore not be discarded without checking whether its common incidence set intersects H and whether its event order/floor permits a transient gap.

For example, one root with A_i={u,z}, C_i={v,z}, floor one can delete u before adding v. It then misses H={u,v} between those events. This only illustrates the interval case; it is not an assertion of a new whole-tuple connectivity class or of an essential witness in a supplied global example.

## 4. Necessary-and-sufficient global schedule criterion

In the positive-floor carrier, tau(X)>=3 exactly when every two-label set H is missed by at least one root. If tau<=2, a hitting set can be extended to a two-label hitting set because exact-four feasibility gives |P|>=4. Conversely any two-label cover directly violates the lower guard.

**Theorem I11.** A permutation of E+ union E- is a native destination-directed lower-guard path from A to C if and only if:

1. every floor prefix inequality in Section 2 holds; and
2. for EVERY pair H, the union of its root protection intervals in Section 3 covers EVERY integer prefix 0,...,n.

Proof: the floor constraints are exactly the cardinality bounds at every prefix; event uniqueness gives incidence legality; the intervals describe exactly all roots missed by H at every prefix. Their coverage is therefore equivalent to excluding every two-label transversal at every state. Processing the n events reaches the exact labelled C. These conditions are jointly necessary as well as sufficient, not a greedy acceptance rule or a sufficient root-level approximation.

A feasible schedule terminates with the number of unperformed events decreasing by one at each primitive. This is well-founded progress AFTER schedule feasibility is established. It does not prove that a feasible permutation exists or that a local edit can be chosen to extend every partial schedule.

If a feasible schedule exists, the accepted maximum-layer-removal theorem converts its finite tau>=3 path with exact-four endpoints into a path with tau in {3,4}. That final conversion can introduce incidences or repeated toggles outside the destination-directed class; no claim is made that the normalized path remains monotone. It stays in the original palette, slots and floors. Accepted normalization is a dependency, not independently recertified here.

## 5. What exact endpoints supply

At either exact-four endpoint, every pair H misses AT LEAST TWO roots. If it missed only zero or one, add one label from the possible missed root to H; positive floors make this possible. The resulting at-most-three-label set would hit every root, contradicting exact four.

Therefore every pair has at least two protection intervals covering prefix zero and at least two covering prefix n. This is genuine boundary redundancy. It supplies neither coverage of every intermediate prefix nor a compatible simultaneous ordering for all pairs and floors. No extension lemma connecting those boundary conditions is proved here.

In complementary blocks B_i=P minus A_i and D_i=P minus C_i, the exact endpoints cover every triple and the lower path must cover every pair under capacities |B_i(s)|<=|P|-a_i. The same interval theorem describes when a pair belongs to a complementary block during its destination-directed replacement. The endpoint triple condition is stronger than just pair coverage, but its global scheduling consequence remains the missing proof.

## 6. Relation to earlier obstructions

A2's one-pass whole-root schedules impose additional ordering: all additions at a root precede its deletions, and a root is completed before another begins. I11 removes those schedule restrictions and admits transient pair protection. It therefore cannot be identified with A2's acyclic root-precedence criterion.

A7/A8 failed completed-state exchange relations do not rule out I11 schedules, since I11 permits tau=3 stages for target four and arbitrary event interleaving. A10's recovery trap excludes its fixed safe-saturation method, not this global destination-directed class. I11's exact local interval accounting also does not by itself overcome A10's global progress warning.

A feasible I11 schedule is a finite full destination path, not a single local safety certificate. However encoding feasibility exactly does not solve it. This distinction is the reason A11 remains OPEN.

## 7. Proof attempt and current blocker

The candidate attempt is to use endpoint triple-cover redundancy to construct event positions satisfying the joint floor/interval constraints. Establishing interval coverage pair by pair would be insufficient: all pairs share the SAME event positions and all floors must hold throughout. Likewise a potential counting destination incidences proves finite descent only after an eligible remaining event is guaranteed.

The precise outstanding obligation is one of:

- an extension theorem or constructive finite scheduling theorem ensuring these constraints are jointly feasible for every declared endpoint pair;
- or explicit admissible exact-four endpoints and a rigorous proof that NO permutation satisfies them, leaving unrestricted primitive connectivity separate.

Neither result has been obtained in this checkpoint. No favorable examples, finite search or heuristic order is presented as evidence for universal feasibility. No percentage completion or universal closure is assigned.

**Current result:** an exact global schedule reduction and a well-founded measure conditional on feasible scheduling. **A11 primary status: OPEN, schedule existence or class obstruction unproved.** General q>=4 primitive/nested connectivity and the q=4/floor-three diagnostic remain OPEN or conditional as before. The reduction applies to all original positive floors and permissible support sizes; it does not create a new numerical campaign, implementation result, efficiency, originality or physical-law claim.
