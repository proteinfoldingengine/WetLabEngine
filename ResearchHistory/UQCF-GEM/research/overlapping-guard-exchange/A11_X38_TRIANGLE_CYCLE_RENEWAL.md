# A11.X38 — reserve-free triangle-cycle renewal

Scope: a89a6b4a24727f83c367e73748dec03a9a1312e3.
Parent: 08e714565c70dc34b80710da4bc7c37a03349074.
Status: exact candidate for fresh independent whole-argument review.
No numerical execution, implementation, benchmark or numbered certification.

## 1. Statements and native domain

Fix a finite ordered palette P, labelled actual roots and their SAME positive ORIGINAL floors a_i. A primitive toggles ONE incidence in ONE root. Larger supports, temporary incidences and repeated edits are native permissions.

**X38T (single-cycle lemma).** For any exact-q tuple E, q>=3, and a palette permutation sigma consisting of ONE nontrivial cycle of length two or three, E can be repaired to sigma(E) by adding all destination-only incidences and then deleting all source-only incidences. Every primitive respects the original floors and q-1<=tau<=q. Each differing incidence toggles ONCE and common incidences remain fixed. The three-cycle case extends accepted L's transposition construction; arbitrary palette permutations already connect by L, so this is scheduling, not connectivity novelty.

**X38R (derived reserve-free repeated completion).** Supply m>=4 nonempty group roles, actual nonempty root masks Q_i of template transversal EXACT FOUR, and partitions B_j,D_j of the same palette with |B_j|=|D_j|=b_j>0. Actual endpoints are A_i=union_{j in Q_i}B_j and C_i=union_{j in Q_i}D_j, with N_i=sum_{j in Q_i}b_j and arbitrary positive ORIGINAL a_i<=N_i. Multigroup roots may be SATURATED a_i=N_i; no reserve is required.

Construct the directed misplaced-label ownership graph: label x currently in B_u and finally in D_v, u!=v, supplies an arc u->v. Require that its directed support has NO simple directed cycle of length greater than three. A readily checkable sufficient structural condition is that every strongly connected component has at most three group indices. No cycle decomposition is supplied as an input.

Then a deterministic sequence of native edits connects exact labelled A to exact labelled C, with 3<=tau<=4 at EVERY primitive. Every original destination-only incidence is added ONCE, every source-only incidence removed ONCE, common incidences are fixed, and the total primitive count is exactly sum_i |A_i symmetric_difference C_i|. This is a mathematical toggle bound, not an executed speed benchmark. Reusable eligibility is DERIVED from actual balanced ownership, not assumed.

**X38F (genuine saturated overlap control).** Section 5 gives an infinite six-group/all-twenty-triples family satisfying X38R, with no reciprocal ownership arcs, saturated or unequal original floors, no four disjoint floor-safe roots anywhere, and an unsafe whole endpoint union. Triangle handovers complete repeated repair despite these features.

**X38O (limited long-cycle obstruction).** Section 6 gives a declared four-cycle whose full-union preparation has a two-cover. It is an obstruction to this full-cycle-union construction only; X37's reserve-bearing adjacent-link mechanism and L's unrestricted native connection remain valid.

The template and balanced group representation are openly sufficient hypotheses. General overlapping endpoints, arbitrary longer cycles, unequal group cardinalities, template accessibility, unrestricted mixed-floor/directed/higher-target/nested universality are NOT asserted.

## 2. Why an entire triangle can be prepared safely

Let F_i=sigma(E_i), U_i=E_i union F_i. Floors at F equal floors at E in the same slots, because a label permutation preserves every root cardinality.

For any hitting set H of U, consider H'=H union sigma^{-1}(H). If root i is hit through an old incidence, H hits E_i. Otherwise its hit h in F_i corresponds to sigma^{-1}(h) in E_i. Thus H' hits E.

Outside the single cycle all labels are fixed. Within a two/three-cycle, any subset S has at most one element in sigma^{-1}(S) minus S: check cardinalities zero/all (zero), one (at most one), or two of a three-cycle (at most one). Hence |H'|<=|H|+1 and tau(U)>=q-1.

Use literal affected-root lists: for each cycle label in increasing palette order, add it to each root where it lies in F_i minus E_i, increasing root index; then for each cycle label/root in the same order delete every E_i minus F_i incidence. Every listed addition is absent, every listed deletion present. Roots containing a label in BOTH endpoints receive no change. No simultaneous move or temporary extraction of roots is used.

During additions the physical tuple contains E and is contained in U. During deletions it contains F and is contained in U. Floors hold since each current root contains the corresponding floor-safe endpoint. Hitting-number monotonicity gives tau>=tau(U)>=q-1 and tau<=tau(E) or tau(F)=q. This proves X38T, including all prefixes. A physically silent packet is omitted, not counted as a native edit.

This is a joint argument on actual roots. An incoming replacement already present through another role cannot cause a floor loss: ALL destination-only incidences have been installed before ANY source-only incidence is removed, so each deletion prefix contains the complete next endpoint support. A reserve is unnecessary. Preparatory roots can all be unfinished simultaneously.

## 3. Actual pair witnesses and exact template endpoints

At any structural boundary each palette label has exactly one group owner and each actual root is the union specified by its SAME mask Q_i. A hitting set of actual roots induces group indices meeting every Q_i, so needs at least four labels. A supplied minimum template cover H of four group indices yields an actual four-label cover by choosing one label from each nonempty corresponding group. Thus every boundary is exact FOUR.

Select a directed two/three-cycle i_1->...->i_l->i_1 with distinct arc labels x_t. Define sigma(x_t)=x_{t-1}, cyclic indices; all other labels fixed. Since x_t is initially in group i_t, applying sigma to the actual tuple makes x_t occupy group i_{t+1}, its destination. This fixes all selected group assignments and restores each b_j. Distinct simple-cycle indices ensure the selected labels are distinct.

In its actual union U, a selected label x_t occurs through roles {i_t,i_{t+1}}; any unselected label retains its single owner. For EVERY two-label set K, its combined expanded role footprint has at most three indices: two ordinary labels use at most two; one ordinary plus one cycle label at most three; two selected labels on a two/three-cycle occupy two edges sharing an index and use at most three. This includes ordinary labels outside the cycle.

Template exactness supplies an ACTUAL root mask Q_i avoiding that footprint. The least such root index gives an explicit witness. Its union support U_i misses K, so EVERY partial physical support at that index also misses K. This proves W_E(K) nonempty for EVERY pair at every native primitive, rather than just total counts or separate capacities. No independent witness capacity is assigned to different obligations.

A source boundary four-cover remains a cover throughout addition prefixes; a next-boundary four-cover remains a cover throughout deletion prefixes. This also proves tau<=4 directly. X38T alternatively proves the band without the supplied-template pair language; the explicit template witness identifies the actual protecting root.

## 4. Eligible next cycle, renewal, termination and destination events

At a structural partition boundary with the same b_j as D, each group has equal misplaced incoming and outgoing arc multiplicities. Indeed current group count minus destination group count is zero, and cancelling correctly assigned labels leaves outgoing count minus incoming count zero.

If any arc remains, follow outgoing arcs. Any vertex just entered has positive indegree and, by balance, positive outdegree. In a finite graph a repeated vertex yields a directed simple cycle. Loops were removed because they are correct labels. By the stated cycle condition its length is two or three. Choose the lexicographically least eligible simple cycle and least available arc label on each edge. These finite choices supply the next exchange whenever unfinished.

Execute the literal X38T lists to the next structural partition. Every selected label now has its final group; no correct label is moved. Remove exactly these arcs. Balance persists because one incoming and one outgoing arc was removed at each involved group. The directed support only loses edges; it cannot gain a long simple cycle or enlarge a strongly connected component. The structural eligibility condition therefore survives.

All b_j and actual N_i are restored, even when original roots are still unfinished relative to A,C. Floors remain the SAME, including saturated floors; no reserve has been spent or replenished. The next exchange derives from the residual actual graph. Inside a handover its next literal incidence is present/absent and floor safe by Section 2, including at tau3. This proves continuation for the constructed prefixes, not for an arbitrary safe prefix.

The count of incorrectly assigned labels strictly decreases by l across each finite exchange. It is a nonnegative integer, so repetition terminates. At zero every group is D_j and each actual root is precisely its full original labelled destination C_i. No compactness or destination size change is imposed.

Each label participates in one resolving cycle. Its actual incidence changes only at masks containing exactly one of its old and final group. Such source-only/destination-only incidences are precisely the original differing endpoint events and toggle once. Masks containing both retain the common incidence; masks containing neither stay absent. Correct labels are untouched. The exact count stated in X38R follows. Identical group incidence patterns can make a resolving cycle partly or wholly physically silent; the finite ownership measure still terminates, and zero-change native steps are omitted.

For a finite specified chain of group partitions on the same template/cardinalities/floors, apply the theorem when each adjacent actual ownership graph satisfies the structural condition. Each complete endpoint restores the representation for the next leg. No fresh minimum cover or protecting reserve is assumed after an unfinished step: the literal finite handover proves it. Both band bounds are direct; accepted A's complete-lower-path conversion is unnecessary.

## 5. Infinite nonprotected control requiring directed triangles

Let t>=1. Partition P into TWELVE distinct cells of t labels each: B_jj for j=1,...,6, plus B_12,B_23,B_31,B_45,B_56,B_64. These are supplied existing labels, not added during repair. Source group j is its row; destination group j its column. Each has size b_j=2t and k=12t.

Actual root masks are all twenty three-subsets of six indices, ordered lexicographically. N_i=6t. Template transversal is four: every three-index set is avoided by its complementary triple; H={1,2,3,4} meets all triples. Source and destination actual endpoints are exact FOUR.

Two openly declared ORIGINAL floor vectors are valid:
- fully saturated: all a_i=6t;
- unequal: first ten floors6t, last ten floors6t-1.
The proof covers both without weakening any floor. Their minimum floors are at least6t-1>=5. Four floor-safe disjoint roots anywhere would require at least4(6t-1)>12t labels, impossible. Actual roots overlap heavily across group triples.

Misplaced arcs are t copies of 1->2->3->1 and t copies of 4->5->6->4. No reverse arc exists. Thus no destination-directed two-cycle can start, and the structural theorem derives a three-cycle whenever either component remains unfinished. This is NOT a claim that every arbitrary native palette-transposition path is impossible: L still applies and may use non-destination events.

For one first-component triangle choose x_1 in B_12, x_2 in B_23, x_3 in B_31. Expand all its required actual incidences before contracting. Every affected root gains exactly one incidence: a triple mask meeting {1,2,3} in one or two indices has exactly one crossing incoming cycle label, while masks {1,2,3} and {4,5,6} do not change. There are eighteen affected actual roots. Each of these roots also has a pending source-only incidence, so after the complete addition stage each is away from BOTH its original source and original destination, even at t=1.

At that union prefix the ACTUAL transversal is exactly three: pair witnesses follow Section 3, while x_1,x_2 and any unchanged label z in group4 cover all templates because their combined group footprint {1,2,3,4} meets every triple. This covers simultaneous unfinished roots without holding an entire old or new three-guard separately fixed.

The contraction restores every N_i, including roots where a nominal incoming label already existed via another role. There is no dip below N_i: all new incidences were installed before deletions. Repeat t triangles in each component. There are 2t completed exchanges and all exact labelled destination roots are restored.

Nevertheless the whole original endpoint union has a two-cover. Pick x in B_12 and y in B_45; their expanded footprints {1,2} and {4,5} have four distinct indices, and every triple mask meets that four-set. Thus {x,y} hits all source/destination union roots. No subfamily of those actual union roots is a three-guard. Arbitrary contracted auxiliary supports are NOT excluded.

All endpoints are symmetry-related and already connected by L. The new gain is incidence-minimal, reserve-free directed triangle completion and derived repeated eligibility in genuine actual overlap. A fixed single-triangle input also defeats X37's saturated adjacent-link list: any initial recipient c on {1,2,3} leaves a cycle edge {u,v} avoiding c; Q={u,v,4} incurs X37's N_Q-1 loss. The full triangle preparation replaces that handover. It does not retrofit floors into X37's reserve-bearing theorem.

## 6. Exact limitation of full-union preparation beyond triangles

In the all-twenty-triples/six-group template, consider a structural boundary with a directed four-cycle 1->2->3->4->1 on distinct labels x_1,...,x_4. Its intended next partition is still exact FOUR and has the same original sizes/floors. Its full actual source/next union contains x_1 through {1,2} and x_3 through {3,4}. Every triple mask meets their combined four indices, so these TWO actual labels hit every union root. The full union has tau<=2.

Consequently the prescribed expand-ALL-then-contract handover reaches a forbidden state, irrespective of the order of its additions; the fully expanded boundary itself fails. This is a rigorously characterized obstruction to the full-union construction, not an inference from a failed sufficient test. It is NOT a no-path certificate, not impossibility of all destination-directed schedules, and not a nested barrier.

X37's one-reserve adjacent-link lift can instead handle such cycles on its stated carrier. Accepted L connects even saturated symmetry-related endpoints using its own allowed incidences. The whole-cycle condition is not claimed necessary: particular longer cycles/templates might retain suitable actual witnesses. Nor does failing the graph condition prove lack of a short-cycle decomposition or lack of native connection.

## 7. Dependencies and exact remaining obligation

L at certified466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, demos/v16.54-parent-support-connectivity/OVERLAPPING_CLIQUE_EXCHANGE.md, already proves arbitrary palette symmetry connection by transpositions with original floors. X38T uses the same union/cover argument but the independently checked three-cycle subset bound supplies a different incidence-minimal handover. No frozen proof or certificate is rewritten or re-certified.

X37 at parent08e714565c70dc34b80710da4bc7c37a03349074 supplies balanced owner-cycle reasoning, actual role witness language and the sharp limited adjacent-link cardinality obstruction. X38 replaces its preparation schedule and removes its one-incidence reserve under the stated shorter-cycle graph condition. X36/I11 supply context for interleaving and unique destination events, not a reserve-free overlapping proof.

There is no claim of a new connectivity classification, a literature-original triangle exchange, all whole-root orders failing on Section 5, universal mixed floors or nested/physical closure. Earlier X37 controls remain distinct and unchanged.

The next mathematical obligation is repeated repair for longer coupled ownership cycles when original roots are saturated, or derived replacement protection beyond the short-cycle certificate; unequal group cardinalities and template accessibility also remain OPEN. Stronger compatible-grade bounds remain parallel. This is analytical ordered repair/retained recoverability, without fundamental time, physical energy/metric/gravity, heuristics, numerical execution, workflow, implementation, benchmark or a new numbered version. v16.55/v16.54 and all referenced original evidence remain unchanged; separately promised efficiency work remains unstarted and independently scoped.

Fresh review must check X38T and X38R/F/O together, every actual pair through partial packets, supplied minimum covers, original floors, shared capacities, reverse permutation orientation, balanced eligible-cycle existence, deletion-stable graph condition, renewed progress, silent edits, endpoint events/restoration, both control floor vectors, eighteen unfinished roots, exact tau3 prefix, unsafe global/four-cycle union, and inherited novelty limits.
