# v16.27 completion — types, proofs, and claim boundaries

Written mathematical arguments; not proof-assistant formalization. Self-reviewed, not independent authorship. All historical references below are under `ResearchHistory/UQCF-GEM/` at baseline `4a3eba5e36f49064515e4062b4cf18fcaeac5e9a`.

## Type and provenance ledger

| ID | Definition / type | Assumptions and exact provenance | Status |
|---|---|---|---|
| T1 | X: finite rooted tree of distinct common-Genesis lineage identities. Every nonroot identity has one parent; all parent chains reach the root. | demos/v16.24-consistency-order/TYPE_AND_PROOF.md C1; inherited v16.21 retained category. Integer parent arrays are coordinates only. | Inherited admitted category, not derivation of all physical states. |
| T2 | Y=(Y_i): nonempty indexed family of root-containing ancestor-closed subsets. U=union_i Y_i. Retained inclusion is literal identity inclusion. | v16.24 C1–C2; v16.25 TYPE_AND_PROOF.md R2–R5. | Actual retained objects and maps. |
| T3 | Z=(Z_i), each Z_i subseteq Y_i, same index set, union Z_i=U. | v16.25 P1,P3. Equal dimensions do not identify carriers; all inclusions are checked by identities. | Admissible endpoint refinement. |
| T4 | E={(i,c):c in Y_i minus Z_i}: fixed finite event set. A legal atomic step removes a nonroot leaf of the CURRENT i-th view and leaves union U unchanged. | v16.26 PREREGISTRATION.md A1–A7; completion proofs C1–C2 below establish legality without relying on historical validators. | Derived event/path types. |
| T5 | tau_v(Y): minimum cardinality of a subfamily covering every immediate child of v in U; tau=0 at leaves. h(Y)=max(1,max_v tau_v(Y)). Both are integers. | v16.24 C7–C8 and proofs H0–H3; v16.25 R7–R8. | Exact combinatorial invariant. Its interpretation as worst-case nonnegative feasibility order uses the inherited FORMAL rational source cone; no physical attainability assumed. |
| T6 | delta(e;Y)=h(Y with e removed)-h(Y): integer assigned to a typed STATE TRANSITION, not to a bare event. | v16.26 P2–P4; completion C2 below. | Derived endpoint difference; no new scalar field or fitted weight. |
| T7 | A_pi:E->{0,1}: per-event map for a legal path pi; D(Y,Z)=h(Z)-h(Y). | v16.26 P6; completion C3. | Attribution and endpoint total. Neither is called an information amount, energy or time. |
| T8 | Categorical identity / equivalence | Parent-preserving bijections of lineage identities and simultaneous permutations of indexed views transport Y,Z,E and paths. Origin labels must agree; storage order is not structure. | Explicit relabeling, not an unearned cross-Genesis morphism. |

No G, Q, response-codomain transport or quantum operation enters this stage. Those objects are not silently identified with these integer quantities.

## C1 — Every legal factorization uses exactly the fixed event set

Atomic deletions never restore an identity and never remove root. A path from Y to Z must remove each element of E exactly once and no element outside E. Therefore it is a permutation of E.

Within one view, a removed descendant must precede a removed ancestor: otherwise the ancestor is not a leaf at deletion. Conversely, suppose a permutation obeys all such precedence relations. At deletion of c, every descendant of c that belonged to Y_i has already been deleted, because prefix-closed Z_i cannot retain a descendant while omitting c. Thus c is a current leaf. Remaining views are prefix-closed. Every identity in U belongs to at least one FINAL Z_j, and no event removes it from that view. Therefore the union remains U at every step. The permutation is a legal atomic path.

This proves a bijection: legal paths <-> linear extensions of the within-view descendant-before-ancestor relation on E. It justifies independent verification by ALL permutations, not another call to a DFS producer. In the frozen <=5-event domain there are at most 5!=120 permutations, so no path cap is required. The historical 20,000 cap cannot have truncated this particular domain.

## C2 — State-dependent atomic trigger and the 0/1 bound

Delete c from view i; write v=parent(c). Only membership of c in the i-th view changes, hence only the child-incidence family at v changes. The other tau values are identical.

Let t=tau_v before deletion. Removing incidence cannot create a t-1 child cover, so the new value is at least t. If an old minimum t-view child cover survives, the value stays t. Otherwise take any old t-cover S. The only lost covered identity is c. Same-union retention ensures some remaining view j still contains c. Appending j to S gives a cover of cardinality at most t+1. Consequently the local increment is 0 or 1, and it is one iff EVERY old minimum cover is destroyed.

The global increment is one iff the new local tau exceeds the old global h. Otherwise it is zero. In particular local trigger and global increment are not synonyms. This is a directly proved property of h, not a physical law.

## C3 — Canonical endpoint difference, not canonical event attribution

For any legal path Y=V_0 -> ... -> V_m=Z,

    sum_{k=1}^m [h(V_k)-h(V_{k-1})] = h(Z)-h(Y).

Cancellation proves the identity for arbitrary finite paths. It does not require treating h as a conserved physical quantity. It implies equal total for two paths with equal endpoints, not equal summands assigned to a particular bare event.

## C4 — Explicit admissible counterexample

Let X={0,1,2}, with root 0 and children 1,2. Let

    Y=({0,1},{0,2},{0,1,2}), Z=({0,1},{0,2},{0}).

Each view contains the root and is prefix-closed. Z_i subseteq Y_i and both unions equal X. E={(2,1),(2,2)}. Both events delete a leaf; the first two views retain the union throughout either order.

Initially the third view covers both children, so h(Y)=1. After deleting EITHER leaf from that view, no single view covers both children, but the first two views together do, so h=2. Deleting the remaining leaf from the third view leaves that same minimum two-view cover, hence h(Z)=2.

In path [(2,1),(2,2)], the two event attributions are 1,0. In the reversed path they are 0,1. The event (2,1), for example, cannot have a path-independent coefficient equal to its actual delta on every path. Both totals are 1. This single verified admissible counterexample refutes universal EVENT_ATTRIBUTION_CANONICAL for this h.

For at most two union vertices, every nonleaf has at most one child, so h=1 on every cover and every delta=0. Thus three is the smallest possible UNION VERTEX count for a counterexample. No other notion of minimality, such as fewest views when repeated initial views are allowed, is claimed.

## C5 — What the trigger does establish

For a fixed typed state and deleted incidence the current minimum-cover family, local trigger and delta are determined. Earlier deletions can change that family even when the future event has the same index and node identity. Thus attribution is canonical as a function of the full transition (current cover, event), not generally as a function of the bare event or the event plus the two remote endpoints.

This precisely scoped statement does not prove that all mathematical event invariants fail, and it does not rule out a physical time primitive in other frameworks. The campaign preserves the program's 'Time is pruning / ordered recoverability update' framing without promoting this counterexample into a new physical claim.

## C6 — Relabeling and storage covariance

A root/parent-preserving bijection maps ancestor chains, leaves, child-cover subfamilies and legal paths bijectively. A simultaneous view permutation maps the first component of event identities. Consequently tau profiles are permuted by node labels, h/delta/trigger values are preserved, and A_pi transports with E. Reversing storage order changes no retained set. Both the counterexample and non-attribution conclusion are invariant under these explicit identifications.

## C7 — Bounded coverage is not a universal positive claim

Producer DFS and independent permutation enumeration must agree on the COMPLETE set of raw paths for every admitted endpoint, not just their number. The verifier separately enumerates the complete endpoint universe and rooted shapes. With <=4 vertices it includes every size-1..4 family of DISTINCT initial views, all same-union componentwise endpoints removing 2..5 events, and all legal orders. Repeated final views are included, with the index correspondence preserved. Singleton paths, zero-event identity, repeated initial views and inadmissible inputs are separate checker controls, not additional enumerated physical observations.

An endpoint can be classified path-independent on its fully enumerated finite path set. A bounded lack of a counterexample over a domain would not prove global event canonicity. Here C4 supplies the universal refutation; enumeration measures its coverage in the fixed implementation domain. No empirical count is used as a theorem axiom.
