# A11.X13 — narrow-palette guard completion and six-root feasibility

Scope commit: 4bd9d85475b4070731b985c8d1099941872d7379.
Parent analytical publication: 1216c1007b0a91cf5e6c0a1c14d813a81dcc23b9.
Certified integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Exact new statements

**Lemma X13B (exhausted-palette disjoint-guard completion bound).** Fix t>=2 and original uniform floor h>=1. Suppose the palette is the disjoint union of t actual guard supports U_1,...,U_t, each of size h. If a family containing these roots and b additional floor-safe roots has transversal at least t+1, then

b >= ceil((t/(t-1))^t).

More precisely, if b*(1-1/t)^t < 1, an actual t-label hitting set exists, selecting one label from each block. This is a necessary completion bound, not a sufficient construction or a disconnection theorem. At t=3 it requires at least FOUR additional roots. The result concerns actual supports, not independent invented capacities.

**Theorem X13F (six-root floor-three exact-four feasibility threshold).** On six labelled slots with original uniform floor three, exact-four endpoints exist if and only if k>=10. Thus every feasible exact-four endpoint pair on six slots has complete native repair with tau in {3,4}, by X12W. Every original labelled/noncompact destination support is restored.

The new work proves infeasibility below ten by structural protection/completion and an elementary six-vertex incidence argument. The positive hub and repair route are inherited X12, not a new multiple-overlap construction or a claim of universal floor-three closure.

**Additional necessary protection constraint.** On a palette of k<3h labels with floor h, an exact-four endpoint cannot have a three-root three-guard. Every actual three-guard needs at least four roots. At any exact endpoint, the family avoiding an actual label is a three-guard, so every label has degree at most r-4. After uniform exact compaction this gives

hr <= k*(r-4).

This is a derived feasibility bound only. It supplies no editable buffer and is not asserted at an arbitrary inexact prefix.

## 2. Native rules and exact compaction

Keep fixed the ordered palette, all existing labelled slots and original floors. A primitive changes ONE incidence in ONE root, retaining its floor. Larger intermediate supports, temporary incidences and repeated toggles remain permitted. Endpoints have hitting number exactly four.

Choose a minimum four-label cover H. In every root choose an h-subset meeting H; remove other incidences individually. Each removal retains H, keeps the floor, and cannot lower transversal. Thus every primitive remains EXACT FOUR. Total excess strictly decreases; an excess incidence is available whenever compaction is unfinished. The reverse restores the full original tuple.

At an exact-four state, ALL roots avoiding any label x form an actual three-guard: a cover of them with at most two labels, together with x, would hit the whole tuple with at most three labels. If three nonempty roots require three hitting labels, they are pairwise disjoint: any intersection lets one label hit two roots and one more hit the third. Such roots at floor h require at least 3h distinct labels.

Therefore k<3h forces every avoiding family to have at least four roots. This proves the degree and incidence constraints in Section 1. Three disjoint supports cannot be inferred from a larger three-guard, nor is the exact endpoint degree statement reused after arbitrary edits.

## 3. Exhausted-palette completion proof

For Lemma X13B, select independently and uniformly one label x_j from each ACTUAL block U_j. This defines a finite set of h^t possible t-label covers of the disjoint guard. Probability here is a finite counting proof; no sampling, numerical execution or heuristic is used.

For an additional actual support A, put a_j=|A intersect U_j|. Since the blocks exhaust P and |A|>=h,

sum a_j >= h,  0<=a_j<=h.

The fraction of these colourful t-sets missing A is exactly

product_j (1-a_j/h).

Arithmetic-geometric mean bounds it by (1-1/t)^t: the factors are nonnegative and their sum is at most t-1. This accounts for the SAME support across all blocks, including supports entirely within a block and larger supports. No independent protection capacities are assumed.

A t-set fails to hit the full family only if it misses an additional root; the guard blocks themselves are always hit. The union bound therefore gives a failed fraction at most b*(1-1/t)^t. If that quantity is less than one, at least one of the actual colourful t-sets hits EVERY actual root. Hence transversal is at most t, contradicting the proposed lower bound t+1. This proves the stated necessary bound. Equality of the counting bound alone does not prove completion exists.

For t=3,h=3, each additional root misses at most 8 of the 27 colourful triples. Three such roots miss at most 24 in total, so at least three colourful triples still hit the complete family. Consequently six roots containing three disjoint triples on a nine-label palette cannot have transversal four. Additional roots, temporary supports or other endpoints outside this hypothesis are not excluded.

## 4. An elementary six-vertex incidence lemma

**Lemma X13M.** Every loopless cubic multigraph on six vertices has a perfect matching. Parallel edges are allowed; loops are not.

Pick an edge ab. If the induced graph on the other four vertices has two disjoint edges, those edges and ab are a perfect matching.

Otherwise its distinct edges are pairwise intersecting. Such an edge family is a star or lies in a triangle: given edges uv and uw, an edge avoiding u must be vw; any edge intersecting all three then has both ends in that triangle. A family with fewer distinct edges fits the star case.

At most four edges, counted with multiplicity, join the remaining four vertices to a,b: their combined degree is six and ab already uses two degree units. If the induced graph is a star, its three leaf vertices have combined full degree nine. At most three of those degree units can go to the centre, whose full degree is three, and at most four can go to a,b. Nine cannot be at most seven. Thus the star case is impossible.

In the triangle case the fourth vertex w has no induced neighbour, so its three edges go to a,b. The three triangle vertices have combined degree nine; their number of external edges is positive and odd, since their internal edges contribute an even number of degree units. Only one external edge remains available, so there is exactly one such edge, say from triangle vertex z to a (rename a,b if needed).

There are exactly four external edges overall. Hence a and b each have exactly two external edges and ab is their only mutual edge. The three w-edges reach both a and b, so wb exists. If u,v are the other triangle vertices, their internal degrees are three,three and z's internal degree is two. Solving the three degree equations gives two parallel uv edges and one edge from z to each of u,v. In particular uv exists.

The edges az, bw, uv give a perfect matching. These cases are exhaustive and prove X13M without importing a graph matching theorem.

## 5. Six-root infeasibility below ten labels

Compact any hypothetical exact-four six-root floor-three endpoint to six triples as in Section 2. It has 18 incidences.

For k<=8, every avoiding family must contain at least four roots, since a three-root guard needs nine labels. Therefore every label has degree at most two. The compact incidence count would give 18<=2k<=16, impossible. Floor infeasibility at k<3 is already included.

For k=9, exact four implies degree at most three: a label of degree d together with one label from each of its 6-d avoiding roots supplies a cover of size at most 7-d. If any label has degree three, its three avoiding roots require three hitting labels. Thus they are pairwise disjoint triples and exhaust the nine-label palette. The other three roots cannot complete them to exact four by X13B. This is a contradiction.

Hence EVERY label has degree at most two. Since there are 18 incidences on nine palette labels, every label occurs in EXACTLY TWO roots. Make a loopless multigraph whose vertices are the six labelled root slots and whose edge for a palette label joins its two actual incident roots. Distinct labels can give parallel edges. Each compact root contains exactly three labels, so this graph is cubic.

By X13M a perfect matching exists. Its three distinct edge labels meet all six roots. That is an actual three-label hitting set, contradicting exact four. No classification of intermediate repair states or finite graph enumeration is used.

This proves infeasibility at every k<10, including noncompact endpoints because their exact compaction would retain exact four.

## 6. Positive feasibility and complete restoration

For k>=10 choose ten existing labels. Put all four triples of S={1,2,3,4} in four existing root slots, and put U={5,6,7}, V={8,9,10} in the other two. Unused original palette labels are allowed.

The complete triple core on S has transversal two, and each private block requires one label. Since S,U,V are disjoint, the hub has transversal exactly four; {1,2,5,8} is a supplied minimum four-cover. ONE core root together with U,V is an ACTUAL three-root three-guard. Every support has its original floor three.

X12W applies with h=3,r=6,k>=10. To make the complete route explicit, for 10<=k<18 exact compaction has 18 incidences, so some label degree is at least two. Its avoiding roots are an actual three-guard. The exact hub's three-root guard can be placed using at least two slots outside that source guard and at most one shared slot. X12A's full endpoint permutation, O1 bridge, lower-path primitive schedule and maximum-layer conversion therefore supply complete access to the ORIGINAL exact labelled hub.

In O1 any at-most-two-label set hitting both exclusive families must miss BOTH supports in the sole shared slot, hence their union. This witnesses every forbidden pair; the old guard protects initial preparation, the bridge protects handover, and the installed destination guard protects all remaining edits. A root's missing destination incidence is the next legal addition; once destination is present, each old-only incidence is a legal deletion. Floors hold by retained endpoint supports, and symmetric difference decreases in finitely many scheduled phases. The preliminary path keeps tau>=3; inherited maximum-layer Theorem A supplies the converted {3,4} path between the exact endpoints.

For k>=18 inherited palette-room AE applies because k>=sum floors=18; X12W already checks that domain and its finite splitting/progress argument. No new label or slot is introduced.

For any original endpoints A,C, the two complete paths A->Q and C->Q return to the SAME full original labelled exact-four hub Q, after reversing saved full token permutations and hub compactions. Reverse the second leg and concatenate. Source exact compaction is reversed at the destination, so EVERY original destination support, including its excess incidences, is restored. Renewal need not reset exact four inside a handover; the complete hub join IS exact four and can be reused for any finite chain of endpoints in this class.

This proof inherits no path-length or runtime efficiency claim. The inherited sources remain frozen: X12_MODULE_HUB_ACCESS Sections 2-6; GUARD_HANDOVER O1; OVERLAPPING_CLIQUE_EXCHANGE M; GENERAL_PARENT_CONNECTIVITY A; PALETTE_SLACK_CONNECTIVITY AE. Uniform floors license full endpoint permutations; arbitrary mixed floors do not. X5's triple/cover/actual avoiding-family qualification is not used.

## 7. Exact remaining scope and obstruction classification

X13B removes the assumption that three actual disjoint guard roots can always be completed to an exact-four entry using only three further roots when their supports exhaust the palette. That particular six-slot/nine-label entry class is EMPTY. It is not an unreachable existing target, a disconnected pair, or a necessary higher native barrier. No exact-four endpoints exist on that carrier at all, by the additional incidence argument.

The complete six-slot repair conclusion removes an unresolved feasibility possibility from the previous ledger. It does NOT furnish universal multiple-overlap renewal. The scientific gain is an actual coupled protection/completion bound explaining why an apparently sufficient lower guard can fail to admit an exact entry, plus a full feasibility/repair consequence.

Combining accepted X12 and the new feasibility exclusions leaves possible unresolved original-floor-three exact-four carriers only at k=8,r=7..8 and k=9,r=7..9, before other accepted-class checks. Not every tuple is asserted feasible. These are domain bounds, not isolated campaigns.

Continue seeking stronger actual protection or reusable necessary multiple-overlap handovers. Full native lower paths allow temporary incidences, larger supports, background edits and repeated toggles. Original A11 destination-directed scheduling, mixed-floor generality, unrestricted nested universality and physical interpretation remain outside this result. Conditional child lifting retains the certified baseline's required interfaces.

No numerical job, run ID, implementation, benchmark, workflow, numbered v16.55 certification or integration merge exists for this checkpoint. The separate accepted efficiency design remains unchanged; runner implementation and measured speedup remain unstarted.
