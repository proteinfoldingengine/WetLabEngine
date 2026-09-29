# v16.31 — Typed global factorization, G1–G8

Written before adjudication implementation. Finite general arguments; not proof-assistant formalization. No geometric target.

## Provenance/type ledger

|Object|Definition, type and assumptions|Provenance/status|
|---|---|---|
|X,Y,Z,U|Finite rooted common-Genesis lineage; indexed literal prefix subsets Z_i subset Y_i; U=union Y_i=union Z_i|.27 completion/PROOFS.md T1–T3,C1 at 134b3d6c3358d91df2e34a9bb57ac82a2f0406ce; admitted category|
|E,Pred(e)|Removed (i,node) events, strict descendant-before-ancestor relation within each indexed view|.28 PROOFS.md T2,D1 at d732a772b5c9244896e481c77658b78d7cdb9efc; derived poset|
|J(E),Y^S|Predecessor-closed event sets S; remaining views after S|.28 D1; exactly actual reachable retained states|
|tau_v(S)|Least number of remaining views covering all immediate children of v in U; zero at leaves|.24 C7,H2–H3; .29 PROOFS.md L1–L7 at 3543d37f83a9d6849a4f62796c8fd17b907992f0; integer diagnostic|
|E_v|Events whose removed node has parent v; an antichain|Definition and G1; no new state primitive|
|P_v|Union of strict predecessor sets of E_v|Derived ideal G2; actual retained predecessor deletion, not an arbitrary background|
|f_v|Boolean table f_v(A)=tau_v(P_v union A), A subset E_v|Derived G2–G3; all entries have actual retained representatives|
|mu_v(B)|Sum over A subset B of (-1)^(|B|-|A|) f_v(A)|Exact integer inclusion-exclusion; coefficients of existing function, not physical couplings|
|G_v|Edge e,f iff a second mixed difference of f_v is nonzero at some background|.30 cube definition, verified globally by G3–G4|
|g_C|f_v(A)-f_v(empty), for A subset component C with other E_v events absent|Derived normalized component function G5; not selected by fitting|

All .28/.29 relative files are under ResearchHistory/UQCF-GEM/demos. Earlier source/response carriers remain intact and are not identified with these integers. Finite additivity of physical sources is NOT used to infer arbitrary real source directions.

## G1 — Same-parent events are an antichain

Within one indexed view, two distinct nodes with the same parent are siblings, never strict ancestors. Across indexed views no predecessor relation is imposed. Hence distinct e,f in E_v are incomparable. A strict predecessor of any e in E_v is a deletion at a deeper node and cannot itself belong to E_v.

## G2 — Full Boolean projection has earned lifts

P_v=union_e Pred(e) is an ideal and disjoint from E_v. Every event of E_v is enabled after P_v. Therefore P_v union A is an ideal for EVERY A subset E_v. .28 D1 proves every such ideal gives a legal retained cover with union U; no fundamental time or missing view has been inserted.

Also the down-closure down(A) is the smallest ideal containing A and satisfies down(A) intersect E_v=A. Thus projection J(E)->2^E_v is surjective. This is not the assertion that arbitrary tuples of projections at DIFFERENT parents are jointly reachable.

## G3 — One canonical parent cube represents all histories

The child-incidence sets at v depend solely on which (i,child-of-v) incidences have been deleted. For any S in J(E), they coincide with those at P_v union (S intersect E_v), even though other parts of the retained covers differ. Therefore

    tau_v(S)=f_v(S intersect E_v),   f_v(empty)=tau_v(empty).

Any pair at different parents has zero mixed difference in every coordinate by this locality. Every local pair/background in f_v lifts by G2 to an actual enabled diamond. Conversely every global diamond in coordinate v either is such a local pair with that projection, or is zero. Consequently the full-history local-interaction graph equals the union of the parent-cube graphs. It is not merely a union of convenient test examples.

## G4 — Pairwise graph versus all interaction orders

Boolean inclusion-exclusion gives, for every A subset E_v,

    f_v(A)=sum_{B subset A} mu_v(B).

For e,f outside A, their second difference at A equals sum_{R subset A} mu_v(R union {e,f}). This function of A is identically zero iff all the coefficients mu_v(R union {e,f}) vanish: apply the same invertible inclusion-exclusion. Thus e,f are adjacent iff some nonzero mu_v(B) contains both.

It follows that the nonempty support of every nonzero coefficient lies entirely within ONE connected component (and any support of size >=2 induces a clique). Nonzero terms of order three or greater CAN exist within a component. They cannot hide across disconnected all-background pairwise components.

The synthetic product x1*x2*x3 illustrates a correction to .30's preregistration: second differences vanish at the empty context but become one with the third variable present. The all-background graph is complete, not edgeless. 'Pairwise at baseline' and 'pairwise at every background' must never be interchanged.

## G5 — Global normalized component factorization and uniqueness

Let components of G_v include isolated events. Define g_C(A)=sum_{nonempty B subset A}mu_v(B)=f_v(A)-f_v(empty) for A subset C. Then g_C(empty)=0, and for EVERY reachable S,

    tau_v(S)=tau_v(empty)+sum_{C component of G_v}g_C(S intersect C).

Proof: substitute G3 in the expansion G4, and group nonempty supports by their unique component. All component coefficients are evaluated from actual canonical retained lifts, not arbitrary extensions of a partially known function.

Uniqueness follows by restricting to A subset C with all other E_v events absent, a legitimate local projection by G2. Every other normalized component is zero there, fixing g_C(A) exactly. Across all vertices the vector identity is the coordinatewise assembly of these formulas. It is not a statement that scalar h=max(1,max tau_v) is additive; .29 refutes that extrapolation.

Finest-block statement: any normalized additive partition of the parent coordinates must place the ends of every witnessed nonzero mixed-difference edge in the same block (otherwise that pair's second difference is zero). It therefore coarsens the graph-component partition. The graph is a canonical finest partition of the EVENT LABELS for this interval; inactive labels may be isolated zero factors. Do not infer a unique decomposition of physical subsystems.

## G6 — Functional factorization does not erase order constraints

On X=(-1,0,0,1), choose Y=({0,1,2,3},{0,1,3}), Z=({0,2},{0,1,3}). Events (0,3) before (0,1) form a chain and affect different parents. Each parent's projection is a two-point cube; their candidate Cartesian product has four points but J(E) has only three. The point 'delete 1 while retaining 3' is illegal. The root coordinate changes from one to two after deleting 1; the local count at 1 stays one. Thus a nonconstant function factors while the state domain is NOT a Cartesian product.

Comparable events therefore remain explicit predecessor constraints. They are not silently replaced by interaction edges or erased by the factorization.

## G7 — Higher order, naturality and interval boundaries

On a root with three children, take one full initial view plus the three singleton-child views, and prune only the full view to the root. At that root, f_v(A)=min(|A|+1,3); its top third-order coefficient is -1. Its graph is connected. This is an admissible retained higher-order example, not only a synthetic checker.

Parent-preserving lineage bijections and simultaneous indexed-view permutations transport E, Pred, P_v, all projections, local values, coefficients, graph components and g_C. Minimum-cover cardinality is unchanged. Computational order for printing witnesses does not select a physical order.

All factors are relative to a fixed endpoint interval. Restricting that interval restricts available contexts; edges may disappear and components split. No event coefficient is claimed invariant across unrelated endpoints, source carriers, or re-rooting operations.

## G8 — Scope of the conclusion

The strengthened theorem closes the full-history LOCAL PROFILE factorization left outside .30's single-cube proof. It supplies no physical response law or geometry. The background Boolean inclusion-exclusion is standard mathematics; the substantive application is showing all relevant Boolean contexts have canonical representatives inside the earned retained category. Computing local truth tables may be exponential in |E_v|. No general polynomial algorithm is claimed.

**Time is pruning / ordered recoverability update.**
