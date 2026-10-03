# Independent whole-argument review — A11.X14

Reviewer: /root/x14_whole_argument_review.
Verdict: ACCEPT, no mathematical corrections requested.
Candidate:9abe657a82bff30c05d6a943d379b7c5a2e4663a.
Proof:A11_X14_SATURATED_INCIDENCE_RENEWAL.md.
Reviewed proof blob:70ba07a459da08e9b6b3c5ee81fb5880eaea42d6.
Proof SHA256:107c6b9d8f814def5b8702fba6c7ecfbf0e0ab68ee41194607ab92a7d63dd3b2.
Prospective analytical scope:950c43e11579a6f2567379893d09d5daf5861ebe.

## Actual independent report

The report below preserves the reviewer's actual reasoning and decision; identifier/math formatting is normalized for the receipt.

I read the actual immutable candidate, its scope, the accepted X12 proof at1216c1007b0a91cf5e6c0a1c14d813a81dcc23b9, the X13 source at2b1bfa9cf4f6bf2189d7cc1e643263726b679225, and the exact-compaction and maximum-layer source at certified baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. I also read the applicable scientific closure requirements. No branch mutation, enumeration, test, workflow, or scientific execution was performed for this analytical review.

### Four-root actual-guard palette bound

Lemma X14G is correct.

Two vertex-disjoint intersection edges would supply at most two labels hitting all four roots, contradicting the lower guard. The remaining intersection graph is a star or lies in a triangle. In the star case three leaf supports are disjoint, requiring at least3h labels. In the triangle case the fourth root is disjoint from the other three, and those three cannot share a label. Their incidences consequently require at leastceil(3h/2) labels, with another h needed for the isolated root. This provesceil(5h/2).

The proof covers larger supports and incomplete intersection graphs. Its floor-three sharpness control123,145,245,678 does require three hitting labels and uses eight labels. It is correctly classified as a guard control rather than an exact-four endpoint.

The three-root disjointness statement is also correct. It legitimately excludes smaller avoiding families alongside the four-root bound.

### Exact avoiding families and compaction

At exact four, a two-cover of the actual roots avoiding x, together with x, would hit the full tuple with at most three labels. Thus the avoiding family has transversal at least three and uses only P minus {x}.

The resulting five-root requirement and degree bound are actual endpoint statements, not assertions about arbitrary intermediate prefixes.

Cover-retaining compaction is exact: every deletion retains the original floor and the supplied minimum cover, while deletion cannot lower transversal. The candidate openly assumes degree-bounded compactions for X14C and does not claim arbitrary compaction choices always satisfy that hypothesis. Saved reverse compactions restore the original noncompact supports.

### Progress moves and blocked-cycle existence

The pending directed graph correctly pairs present non-destination incidences with absent destination incidences within each row. Equal current and destination row sizes supply equal surplus and deficit counts.

Its balance identity is correct:
out(v)-in(v)=degree_current(v)-degree_destination(v).

A pending edge ending at a column of degree below D supplies the stated legal add-before-remove transfer.

If no such edge exists, every column with incoming pending edges is full. Since destination degrees are at most D, every such column has an outgoing pending edge. Following edges therefore supplies a directed cycle, from which a simple cycle can be extracted. Loops are excluded by disjoint surplus and deficit sets in a row.

This proves next-move existence whenever the completed-transfer boundary differs from the destination; it does not merely posit a decreasing potential.

### Saturated renewal

The cycle rotation is correct, including the two-edge case.

The first transfer creates one degree-D+1 column and one degree-D-1 column. Processing the preceding edges in reverse cyclic order moves the underfull column backward. The final removal closes the initially overfull column. At every primitive there is at most one degree-D+1 column, and every other column has degree at most D.

Each added incidence remains absent until its own transfer, and each removed incidence remains present. Distinct cycle vertices and the original surplus/deficit classification prevent conflicting incidence edits. Repeated nonadjacent row colours are harmless; adjacent colours cannot coincide because their shared label would otherwise be both surplus and deficit in that row.

Every transfer returns its row to its original floor size. Every completed cycle restores the pre-cycle label degree vector, while resolving its selected incidences. No extra label, root, spare column, or independent capacity copy is introduced.

This is a reusable handover: after a cycle, the remaining pending graph again meets the conditions supplying either a greedy transfer or another cycle. The hitting number need not return to the exact target at those boundaries.

### Actual lower witnesses, termination and endpoint restoration

For every forbidden K with |K|<=q-2, the estimate
number of roots hit by K <= sum_(x in K)degree(x) <= (q-2)D+1 < r
is valid at every preliminary primitive.

Counting repeated hits only enlarges the estimate. The strict inequality therefore guarantees an actual existing root missing K; choosing the first such root supplies the stated witness. This covers all forbidden sets, including pairs containing the overfull column, background pairs and unused palette labels.

Every primitive decreases the symmetric difference from the compact destination by one. The finite pending graph supplies the next move whenever differences remain, so termination at the exact labelled compact destination is proved.

The preliminary path retains all original floors and tau>=q-1, while its upper bound is finite because every root remains nonempty. The inherited maximum-layer theorem is applicable to this actual finite path between exact-q endpoints. The candidate correctly distinguishes its converted band path from the destination-directed preliminary schedule.

Prepending source exact compaction and appending reversed destination exact compaction restores every original labelled destination support. Mixed original floors are allowed in X14C because no row permutation is used; the proof does not infer universal mixed-floor connectivity.

### Complete eight-label consequence

For k=8,h=3, every label-avoiding family lives on at most seven labels. X14G and three-root disjointness force at least five avoiding roots. Hence every endpoint label degree is at most r-5.

For4<=r<=7, exact compaction would imply3r<=8(r-5), which is impossible. For r<4, tau<=r excludes exact four.

At r=8, all endpoint degrees are at most three and the compact incidence total is24. Therefore all eight degrees are exactly three. X14C applies with D=3, since8>2D+1=7. Indeed, the same incidence bound forces the original endpoints themselves to be compact.

The two disjoint four-label complete triple cores establish exact-four feasibility at eight roots, and duplicate padding establishes feasibility above eight. For r>=9, X12D applies within its accepted domain: the hub fits andceil(3r/8)>=4.

Thus the complete eight-label all-feasible-root-count conclusion follows.

### Scope and closure classification

The candidate correctly preserves the distinction between its analytical theorem and numbered implementation certification. It introduces no numerical campaign or run ID.

Its remaining possible uniform-floor-three carriers—nine labels with seven through nine roots—are consistent with the accepted X12 and X13 exclusions. Their feasibility or disconnection is not asserted.

Original A11 destination-directed universality, unrestricted nested universality and physical interpretation remain open. Conditional child lifting retains the baseline interfaces. Failure of X14C's sufficient degree inequality is correctly classified as a limitation of this construction, not a negative native theorem.

No mathematical corrections are requested. The exact candidate identified above is accepted for analytical publication.
