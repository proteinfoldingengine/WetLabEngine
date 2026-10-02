# v16.54 findings — the general parent-support principle

Status: independently accepted analytical results. No implementation or new numerical campaign has run. v16.54 is not CLOSED/CERTIFIED; the certified v16.53 predecessor remains unchanged.

## The general result

For any number of children, fixed palette and positive child-width floors, two exact-target-q root tuples (q>=2) have a one-unit connection if and only if they can be connected while keeping the hitting number at least q-1. Any such lower-guard connection can be rewritten so that the parent hitting number stays in {q-1,q}. Upper excursions are removable.

This is Theorem A in GENERAL_PARENT_CONNECTIVITY.md, accepted at proof SHA256 de144b98ee80c99510dc1eabb7318be11d67603f5f7337004019dc8372bc2751 by INDEPENDENT_PROOF_REVIEW.md. The submitted proof retains its candidate heading to preserve the reviewed bytes; the independent decision records its accepted status.

The structural explanation is explicit. Root supports may be expanded freely. Merging two label roles selected from a minimum hitting set lowers the hitting number exactly one. The union of two such local repairs lowers it by at most two relative to the removed high layer. Addition/deletion paths through those unions preserve width floors and the one-unit band. This argument does not depend on a branching number.

## What determines connectivity now

Write B_i=P\A_i and impose capacities |B_i|<=k-a_i. A hitting-number lower bound q-1 is exactly the requirement that every (q-2)-subset of the palette lies in some B_i. The remaining problem is therefore capacity-bounded subset-cover reconfiguration:

| Target | Required lower guard | Analytical outcome |
|---|---|---|
| q=1 or2, arbitrary arity | Elementary expansion/contraction | Connected |
| q=3, arbitrary arity | Cover every individual label | Connected; native exact admissibility supplies spare capacity |
| q=4, five children | Cover every pair of labels | Connected; degree-two incidence transfers plus an explicit saturated-hub argument |
| q>=3, arbitrary arity, saturated capacity sum b_i=(q-1)k | Cover every (q-2)-subset | Connected by the exact-endpoint normal form and partition exchanges |
| All floors 2, arbitrary feasible arity and target | Cover every (q-2)-subset | Connected by star symmetrization, canonicalization and upper-excursion removal |
| Mixed floors in {1,2}, arbitrary feasible arity and target | Singleton anchors plus residual graph | Connected |
| At least q floor-1 indices, arbitrary remaining floors | q forced anchor labels | Connected |
| Higher floors with fewer than q floor-1 indices | General residual hyperedge cover | OPEN beyond the earlier proved cases |

Five-child target3 is now a consequence of the arbitrary-arity theorem. It does not require its own passing-case campaign. Five-child target4 tests a genuinely different lower guard: ordinary label coverage is insufficient. Its proof handles both spare incidence capacity and the no-spare-capacity case, rather than silently excluding saturated exact states.

## Native consequence and limit

The accepted fixed-root clearance mechanism lifts these root paths through arbitrary children already supplying the inherited interface. Child interiors stay exact during parent reconfiguration; child normalization occurs only at an exact parent. Thus the bound is on the global sum of deviations, not separate coordinate bounds.

The parent criterion is necessary and sufficient within the stated width-floor root graph, and sufficient for native nested repair. Its failure would not alone prove a native barrier: a native path may spend a unit inside a child and temporarily leave that child's minimum-exact-width carrier. A genuine obstruction must exclude those additional native paths too.

## The next mathematical question

Establish or refute a general exchange theorem for capacity-bounded pair and higher-subset covers, restricting endpoints to complementary tuples of exact-q native states. Such endpoints cover every (q-1)-subset and leave at least one q-subset uncovered. Total complementary capacity is at least (q-1)k, but that scalar slack has not been proved sufficient to preserve all pair/higher-subset constraints during reconfiguration.

The next useful deliverable is that exchange theorem or a precisely characterized obstruction to it. Another branching-number campaign or larger passing-case count would not resolve this question. No universal arbitrary-target connectivity, native nonunit obstruction, path-length efficiency or physical interpretation is claimed.

## Publication boundary

Native scope:3932248af7bb5c64bdd3d467fcd6d78ddf7adde5. Reviewed proof:26bdda935564ba828e89bb7879400285789f2d72. Parent:f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8. Draft PR102 holds this analytical work separately from the certified predecessor. Any later implementation has its own prospective protocol, written plan, independent producer/verifier, GitHub execution and full certification gates.

## Exact-endpoint extension: the capacity boundary is resolved

EXACT_ENDPOINT_CAPACITY.md (proof commit b1ebe5df4f534c8813797d5a3b2ccc430e757126, SHA256 37556dd879d80b1301395fbc89b8ec1ee442a0497459c659accbf776fa604ff8) is independently accepted in INDEPENDENT_CAPACITY_REVIEW.md with no findings.

At an exact-q endpoint every s-subset S, s<=q-1, lies in at least q-s complementary blocks. For s<=q-2, the capacities of precisely those blocks obey sum_{i:S subset B_i}(b_i-s)>=(q-s-1)(k-s). In particular every required lower-cover subset has at least two covering blocks. One whole block can therefore be replaced safely; this redundancy cannot be assumed to survive repeated replacements.

When total capacity attains its lower bound, every exact endpoint has r-q full-palette roots and q roots partitioning the palette. The same floor vector forces the same full-palette indices. Finite partition swaps give a one-unit path for every q>=3 and every arity, resolving pair and all higher-subset reconfiguration on this entire boundary.

For positive delta=sum b_i-(q-1)k, compaction leaves at most delta labels below maximum incidence degree r-q+1. Their deficits sum exactly to delta. This localizes the remaining structural problem without proving that these labels supply a safe exchange buffer. Universal positive-slack connectivity remains OPEN. No implementation or numerical campaign was initiated.

## Positive-slack exchange with protected roots

PROTECTED_EXCHANGE.md is accepted by INDEPENDENT_PROTECTED_REVIEW.md, with no findings, at proof commit 4825b8d5544ace5185b10ca9af7f856c1840c276 and SHA256 a76dffd9e6f9db7e590ebb89e62c4a195c27af826e84cc5c3a60005329279ee0. Candidate wording in the proof header preserves reviewed bytes; the review records acceptance.

All exact-q endpoints possessing q pairwise-disjoint roots are connected with tau in {q-1,q}, at arbitrary arity and slack. Witness indices can be moved to the q smallest-floor indices through exact states, after which finite size transfers and partition swaps reach a common canonical tuple. No spare label is needed.

Such protected endpoints exist exactly when the sum of the q smallest floors is at most k. A symbolic family of m disjoint triangles (m>=2, r=k=3m, q=2m, all floors 2) has exact target q and positive slack but violates that condition: 4m>3m. It admits no protected state anywhere in the width-floor carrier. This is a precise obstruction to the protected-root method, not evidence of disconnection or a native barrier.

The general positive-slack problem remains OPEN. When the floor condition holds, reaching the protected class from unprotected exact endpoints is unproved. When it fails, a different mechanism preserving overlapping witnesses or complementary subset covers is necessary. Deficient-label counts do not imply the protected-root condition. No numerical campaign or implementation was initiated.

## Overlapping roots: the earlier obstruction family is connected

OVERLAPPING_CLIQUE_EXCHANGE.md and INDEPENDENT_OVERLAP_REVIEW.md record the next accepted analytical result. Reviewed proof SHA256: 5515da06738778bccf0e46dc126aee358bf9c4c4446a5d8c34f07697672f6e14. The initial candidate at 9105f42b683546a039f09405234f1493dc2c65f4 received one grammatical correction; the reviewer verified the corrected hash and reaffirmed acceptance. No unresolved findings remain.

General label transpositions and floor-compatible root permutations admit one-unit paths for arbitrary overlapping supports. These symmetry moves become a complete connectivity proof on the following extremal family: all floors 2, k=ms labels, r=m*s*(s-1)/2 roots, exact q=m(s-1)>=3, and s>=3. Compaction and an independent-set averaging equality force every compact exact endpoint to be m disjoint complete graphs on s labels. Safe symmetry exchanges connect all such forms, and reversing compaction handles every original exact endpoint.

These carriers have positive slack and no q disjoint root witnesses, since 2q>k. Thus the earlier disjoint-triangle family (s=3) is now proved connected, as part of a uniform overlapping-root theorem. Its prior status as a protected-method obstruction remains correct; it is not a connectivity obstruction.

The open problem is now exchanges between different overlap structures outside the extremal equality regime. The theorem does not assert arbitrary positive-slack connectivity. No numerical campaign, implementation or certification was initiated.

## General all-floor-two theorem: overlap structure may change

FLOOR_TWO_CONNECTIVITY.md (ab27c05ee225c28d2a1fcd517d03eb406693d2c0, SHA256 cdfd4f9550c4787b2c21e3b2de2d7b2d48b584e2b516c52db2ea7691d9214840) is independently accepted by INDEPENDENT_FLOOR_TWO_REVIEW.md with no findings.

For every feasible r,k,q>=3 with all root floors equal to 2, all exact-q endpoints are connected with tau in {q-1,q}. Existing q=1,2 arguments complete the feasible targets for this floor class. This needs neither disjoint root witnesses nor extremal clique parameters nor common endpoint symmetry type.

Exact compaction gives a graph. A star edit retains the G-u constraints, losing at most one hitting unit, and fits the fixed root slots whenever the new degree does not exceed the old. Closed-neighborhood class symmetrization does not increase independence number or distinct edge count and strictly reduces class count. Clique splitting, balancing, duplicate normalization and safe symmetry exchanges yield one canonical tuple. The preceding maximum-layer theorem removes upper excursions only after this complete lower-guard path has been established.

This supersedes the clique-boundary limitation for floors 2 while preserving that earlier proof. It is a structural exchange theorem, not an arity campaign. Mixed or higher floors remain the general unresolved case: compact roots may be hyperedges and the graph cloning/slot argument does not automatically apply. No implementation, numerical campaign or certification was initiated.

## Singleton anchors: mixed floors and arbitrary higher floors with enough anchors

SINGLETON_ANCHOR_REDUCTION.md (60a1b1da426858926dc6022f78de1f1d46e95a62; SHA256 93eda3cc5c6f7904c5d88e6d99576d70892e638cda04e2414ad9bb2ea4fb932c) is independently accepted in INDEPENDENT_SINGLETON_REVIEW.md with no findings.

Theorem P connects all exact-q endpoints when at least q root indices have floor 1, regardless of the other floors. Exact compaction and duplicate-anchor separation establish q distinct forced labels; they protect the lower bound while every other root expands, reaching the previously proved protected class.

Theorem Q connects all exact-q endpoints whenever every floor lies in {1,2}. With fewer than q singleton-capable roots, canonical distinct singleton labels contribute a fixed p units. Pair roots touching those labels are redundant; the remaining graph lies on the complementary palette. The proof handles residual target 1 separately and explicitly extends graph normalization to target 2 and starting cover number above target. Final maximum-layer replacement restores the one-unit band globally.

These structural reductions cover arbitrary feasible arity and target. The general remaining case involves floors at least 3 and fewer than q singleton-capable indices, outside earlier saturated/protected/low-target results. Hyperedge connectivity there remains OPEN. No implementation or numerical campaign ran.

## Higher-floor clone boundary: safe criterion and failed unguarded iteration

HYPEREDGE_CLONE_BOUNDARY.md (0da7319bef2f58d6c43489c6a8cfb78aded9fbcc, SHA256 05bedf4d486c41c07191315866fed9ff8036f660c0f111614022dc17994bcd6f) is independently accepted by INDEPENDENT_HYPEREDGE_REVIEW.md with no findings.

The arbitrary-floor star lemma permits replacement of roots containing one label while untouched roots protect tau>=q-1. To iterate, completed exchanges need a renewed tau>=q guard. A new theorem provides it for hyperedge clones protected by an EXISTING pair root, with an exact sorted floor/size matching test assigning copied supports to existing root slots. No root or palette label is added.

The direct unguarded graph generalization fails. A symbolic four-root floor-three example has tau=3; a slot-compatible clone retaining a shared triple and equal clone-label degrees reduces tau to 2. Two disjoint copies give successive completed values 6,5,4, violating the target-6 lower bound. This refutes that iteration rule, not exact-endpoint connectivity: the prescribed final tuple is not exact-6.

The graph proof's structural protection is now explicit: a pair root forbids an independent set from containing both clone labels. A larger shared hyperedge does not. General higher-floor connectivity still needs another completed-exchange invariant or a way to restore exactness before another unit is spent. No universal existence/termination theorem is inferred from the local rule, and no native barrier or numerical campaign is claimed.

## Contraction guard replaces the pair-root assumption for a clone

CONTRACTION_CLONE_GUARD.md (118829a29f39e3642e48b3d9e8f43d9c74df8ede; SHA256 86a894e88fd36d62f551a2e23d3f9afa292a6e9070cb8bdac717f8cfce615e9f) is independently accepted in INDEPENDENT_CONTRACTION_REVIEW.md with no findings.

For the slot-compatible clone, let F be old roots avoiding u and L be retained roots with u,v contracted away. Then tau(new)=min(1+tau(F),tau(L)), using infinity for an un-hittable empty contracted support. If old tau=t, the completed clone is safe exactly when tau(L)>=t; it stays exactly at t exactly when additionally tau(F)=t-1 or tau(L)=t. A (t-1)-cover of L is a concrete unsafe-clone certificate. These are auxiliary proof objects, not native moves lowering root floors.

The criterion handles genuinely higher-floor cases with no native pair/singleton root. An arbitrary-target symbolic all-floor-three family gives an exact exchange from an endpoint with q disjoint root witnesses to one with maximum disjoint-root family size q-1. This supplies a connection into the protected component for those destinations while keeping the one-unit budget; it does not establish accessibility for all unprotected endpoints.

The remaining obligation is global: find a finite sufficient sequence of guarded exchanges or an exactness-restoring move when the guard fails. No universal higher-floor connectivity, efficiency or termination theorem is inferred. No numerical campaign or implementation certification occurred.

## Guarded clones are incomplete; star relocation supplies a new progress mechanism

HYPEREDGE_STAR_RELOCATION.md (8a63b59c5104eab214052dbbc6e7a8a944a72f9a; SHA256 70cc9abe8e63f48820b656b95cb1a4a6a359bea4360090ceb1028ff05ce12251) is independently accepted in INDEPENDENT_RELOCATION_REVIEW.md with no findings.

A fixed family of hitting number q-1, avoiding u, permits arbitrary floor-safe replacements of other roots as long as they retain u. This directly preserves tau in {q-1,q}. Applied to complete uniform hyperedge modules, moving a label from a larger to a smaller module fits the existing slots by a binomial count. Completed moves remain exact-q, and the sum of squared module sizes strictly decreases. Canonical balancing therefore connects all such module tuples with the same r,k,h,q, including different overlap structures and redundant root multiplicities.

Guarded completed clones alone are not complete for connectivity, even with label/root permutations. Pure complete modules are fixed by within-module clones, while across-module clones have f=lambda=q-1 and are unsafe. Yet the same-floor exact-q endpoints with h=3,k=8,r=11,q=4 and module sizes (3,5) versus (4,4) plus three duplicates are connected by one star relocation and redundancy normalization. The restricted clone progression cannot connect them. This is a proved method limitation accompanied by a successful native one-unit replacement, not a native barrier.

The remaining global issue is reaching module forms or another common class from arbitrary higher-floor endpoints. No such theorem or universal progress measure is claimed. No numerical campaign or implementation certification occurred.

## Accepted complete-module capacity obstruction

MODULE_CAPACITY_OBSTRUCTION.md (proof bc9ce299e76886f38b159618739e1f6184d42242; SHA256 d4664fcd76e39d9c885e301c876b23f49424a48b1649a74505b56d673c644fda) is independently accepted in INDEPENDENT_MODULE_CAPACITY_REVIEW.md, with no findings.

Theorem Z supplies an infinite all-floor-three cyclic family: k=3a, r=a(a-1)(2a-1), exact q=k-3, a>=2, with strictly positive derived capacity slack. Every four-label set contains a root, while a transversal triple is independent. Any disjoint complete-triple-module state at that exact target would require one module on k-1 labels, even allowing labels outside the core and redundant extra roots. Its required slot count exceeds r by (a-1)^2(5a-2)/2. The terminal form is therefore unavailable anywhere in the same carrier.

The unequal-part (3,2,2) illustration has k=7, r=12 and q=4, whereas its hypothetical exact-target module core requires twenty slots. These are symbolic proof values, not a numerical campaign.

This supersedes the prior suggestion that every higher-floor endpoint might reach the complete-module class. Theorem Y remains valid for endpoints already of that type. A universal argument must accommodate other overlap structures within the fixed slot budget. General higher-floor connectivity remains OPEN; this is neither a disconnected pair nor a native barrier. No implementation, numerical campaign or certification occurred.
