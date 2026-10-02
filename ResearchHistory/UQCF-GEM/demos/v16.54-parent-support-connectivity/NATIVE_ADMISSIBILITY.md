# Native admissibility — general parent-support connectivity

Recorded before new implementation or numerical execution. Already-developed analytical leads are disclosed in RESEARCH_SCOPE.md; they are not relabeled prospective discoveries.

Verified integrated parent: f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8 (v16.53, PR101). Independent completed closeout: bf172aabe335a8f8ce54ae7f2058dd371f2048a2 on research/v16.53-audit-receipt.

## Native category remains fixed

Use nonempty nested supports on a finite nonempty ordered palette P. The global root is P. At each internal vertex, h is the minimum number of labels hitting all immediate child supports; q is its fixed integer target. Exact endpoint admissibility means that a nested state realizes the entire target profile, not merely that each target lies in its numerical range.

One primitive adds or deletes one label incidence at one nonroot vertex, preserving nonemptiness and nesting. The repair budget is the sum over all internal vertices of |h-q|, at most one at every primitive. No new labels, vertices, simultaneous moves, weights, physical primitives or fundamental time are introduced. The inherited scalar barriers remain separate scalar minima.

## Abstract parent-support problem

Let r>=2, k=|P|>=1, and 1<=a_i<=k. The a_i are minimum exact widths supplied by child interfaces. A root tuple A=(A_1,...,A_r) has A_i subset P and |A_i|>=a_i. Let tau(A) be its transversal number. Fix 1<=q<=r and require native exact endpoints tau=q to exist; otherwise the endpoint problem is infeasible, not a failed repair.

The graph G(r,P,a;q) has these tuples with |tau-q|<=1 as vertices. An edge adds or deletes one root incidence while preserving all width floors. The primary question is whether every pair of exact-q vertices lies in one component. Connectivity of every intermediate vertex is a stronger, unnecessary claim and is not assumed.

This graph is a sufficient root-level carrier for a nested repair when child interfaces supply exact-interior clearance. Its disconnectedness alone is not automatically a native barrier: a native path could temporarily spend its one unit inside a child and use a root smaller than that child's minimum EXACT width. Any necessity claim must address that distinction.

## Complement formulation

Write B_i=P\A_i and b_i=k-a_i. These are blocks with capacities |B_i|<=b_i. A label subset H fails to hit the roots exactly when H is contained in at least one block B_i. Thus tau>=q-1 means all (q-2)-subsets are covered by the blocks (with the empty-subset convention when q=2), while tau<=q+1 means a hitting set of size at most q+1 exists. When q+1<=k, the latter is equivalent to at least one (q+1)-subset not being contained in any block. Use the direct hitting-set definition outside that size range.

For r=5,q=3, the band is tau in {2,3,4}: complements must cover every label, and five disjoint roots must be avoided. For r=5,q=4, the band is {3,4,5}: complements must cover every pair of distinct labels; the upper bound is automatic. Feasible exact targets imply k>=q. These are diagnostic boundaries for the general principle, not separate branching-number campaigns.

## Claims and stopping rules

Distinguish a proved sufficient connectivity condition, an unresolved universal conjecture, a failure of a chosen construction, a disconnected width-floor graph, and a genuine native nonunit barrier. A native barrier requires admitted exact endpoints and exclusion of every legal unit path. No finite passing search proves the universal claim.

This analytical stage has no numerical enumeration domain or execution budget: no numerical campaign is authorized by this document. Any later implementation requires a separate prospective bounded protocol and written plan, independently reconstructing the full universe and running scientific work on GitHub only. Stop proof claims at the first unproved obligation; preserve the exact gap rather than filtering difficult endpoints.
