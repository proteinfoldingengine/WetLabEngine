# A11.X14 — actual guard palette bounds and renewable saturated incidence cycles

Scope:950c43e11579a6f2567379893d09d5daf5861ebe.
Parent analytical publication:2b1bfa9cf4f6bf2189d7cc1e643263726b679225.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Exact new claims

**Lemma X14G (four-root guard palette bound).** Four actual roots of size at least h>=1 requiring at least three hitting labels use at least ceil(5h/2) distinct labels in their support union. Three roots requiring three labels instead need at least 3h distinct labels.

At an exact-four endpoint, all roots avoiding x form an actual three-guard on P minus {x}. Thus, if k-1<ceil(5h/2), that family must have at least FIVE roots and every label degree is at most r-5. For original uniform h, exact compaction consequently satisfies hr<=k*(r-5). The condition also excludes smaller guards because 3h>=ceil(5h/2); fewer than three nonempty roots cannot require three labels.

**Theorem X14C (renewable bounded-incidence repair).** Fix r labelled roots, a finite ordered palette, arbitrary positive ORIGINAL floors a_i, exact-q endpoints q>=3, and an integer D>=1. Suppose both endpoints admit legal exact compactions to their original floors in which every label has degree at most D. If

r >= (q-2)*D + 2,

then the ORIGINAL endpoints have a finite native path with transversal in {q-1,q}, restoring every labelled/noncompact destination support.

The preliminary lower path uses directed surplus/deficit transfers and reusable cycle rotations, allowing at most ONE temporarily overfull label of degree D+1; every other label stays at degree at most D. It does not need an unused palette label, a spare incidence column, an extra root, a chosen X5 entry or a full endpoint permutation. The degree restriction is a sufficient witness condition on the construction, NOT a new native admissibility rule. Original native paths remain unrestricted.

**Corollary X14E (complete eight-label original-floor-three class).** Every exact-four endpoint pair on an eight-label palette with uniform original floor three has complete native {3,4} repair, at EVERY feasible root count. For r<=7 exact four is infeasible. At r=8, exact compaction forces every label to have degree exactly three; X14C with D=3 applies. For r>=9 accepted X12 supplies full repair.

Thus the remaining possible unresolved original-floor-three exact-four carriers, before other accepted-class exclusions, have ONLY nine labels and r=7..9. Not every such tuple is asserted feasible. General original A11 directed scheduling, universal mixed-floor repair, higher targets and unrestricted nested universality remain open.

## 2. Exact compaction and actual label-avoiding guard

For a root tuple of exact transversal q and positive floors a_i, choose a supplied minimum q-cover H. In every root retain an a_i-subset meeting H and delete the other incidences individually. Every deletion retains the original floor and H, and cannot lower transversal. Every intermediate is therefore EXACT q. An excess incidence exists whenever compaction is unfinished; total excess strictly decreases. Save its reverse to restore original noncompact supports.

For X14C the assumed degree-bounded exact compactions are these endpoints; no arbitrary choice is claimed to satisfy its hypothesis. If an exact endpoint already has maximum degree at most D, this cover-retaining compaction automatically retains that bound.

At exact four, the actual family avoiding x requires at least three labels, since a cover of it with at most two labels together with x would cover the full tuple. Its supports use only P minus {x}. This elementary restriction strengthens a whole-palette guard bound; the avoiding label is not an extra resource. No exact-endpoint implication is used at an arbitrary inexact prefix.

## 3. Four-root guard palette proof

Let the intersection graph have one vertex per actual root and an edge for each pair of intersecting roots. If it has two vertex-disjoint edges, choose one label in each corresponding intersection. Those at most two labels hit all four roots, contradicting the guard. Thus its distinct edges are pairwise intersecting.

A pairwise-intersecting edge family is a star or lies in a triangle. Indeed, from edges uv and uw, an edge avoiding u must be vw; every edge meeting all three then has both ends in that triangle. A family with fewer edges lies in a star.

In the star case the three leaves have pairwise disjoint supports, requiring at least 3h labels. In the triangle case the fourth root is disjoint from the other three. Those three cannot share a common label, since that label and any label of the isolated root would be a two-cover. Therefore each label in the three-root union belongs to at most two of them. Their at-least-3h incidences require at least ceil(3h/2) distinct labels. The isolated root contributes at least h further labels. The total is at least h+ceil(3h/2)=ceil(5h/2).

This proves X14G for larger supports too. At floor three the bound is sharp: roots 123,145,245,678 use eight labels and require three hitting labels. The first three have empty common intersection and a two-cover, and the fourth has a private palette. This example is a guard control, not an exact-four endpoint or an assumed reachable entry.

Three-root guard disjointness is elementary: a label shared by two roots plus one label of the third gives a two-cover. Hence three-root guards use at least 3h labels. Together these facts prove every claimed exact avoiding-family degree bound.

## 4. Surplus/deficit transfers and existence of progress

Write B,C for the degree-bounded compact exact-q endpoints. They have identical row sizes a_i, though their label degree vectors need NOT agree.

At each current completed-transfer boundary, pair the surplus labels B_i minus C_i with the equally many deficit labels C_i minus B_i in each row i. Make a directed edge x->y coloured i for each such pair. Its source incidence is present and not in C_i; its destination incidence is absent and in C_i. Choose the pairings by the fixed palette order. When a transfer is completed remove that paired edge; pairings need not be recomputed.

If an edge x->y ends at a label y of current degree less than D, add y in row i and then remove x in row i. The row first grows from a_i to a_i+1, then returns to a_i. Degrees stay at most D, and both primitives reduce symmetric difference from C by one.

Suppose edges remain and none ends at a label of degree less than D. Every label with an incoming pending edge is full, of degree D. At any label v,

outgoing pending count - incoming pending count
= current degree(v) - destination degree(v).

Since destination degree(v)<=D, a full label with an incoming edge also has an outgoing edge. Following directed edges therefore yields a directed cycle; extract a simple cycle with distinct label vertices. Each cycle label is full. There are no loops, because a label cannot be both surplus and deficit in one row. This supplies an eligible cycle whenever the greedy move is unavailable. It requires NO spare column.

The finite directed graph and its degree balance are based on the actual pending incidences, not a conjectured order or a claim that any safe prefix can finish.

## 5. Reusable cycle handover without spare capacity

Let a chosen simple cycle be

x_1->x_2, x_2->x_3, ..., x_m->x_1,

with m>=2. Keep all background roots and incidences unchanged during this particular rotation; the theorem does not restrict the final native graph to such schedules.

First transfer x_1->x_2 in its coloured row: add x_2, then remove x_1. This makes x_2 temporarily degree D+1 and x_1 degree D-1.

Now process the preceding cycle edges in reverse order:

x_m->x_1, x_(m-1)->x_m, ..., x_2->x_3.

For each, add its destination in its coloured row, then remove its source. The destination is the currently underfull label, so adding restores degree D. Removing the source makes that source underfull. The last removal is x_2, which instead closes the initial overfull column back to D.

Throughout the rotation at most ONE label, x_2, has degree D+1. Every other label has degree at most D. At some within-transfer instants no label is underfull, but the single-overfull property remains valid; no spare-capacity claim is made about those instants.

Every added incidence was a pending deficit and remains absent until its own transfer; every removed incidence was a pending surplus and remains present until its own transfer. Distinct cycle labels ensure no earlier cycle transfer alters the same directed incidence. Repeated nonadjacent row colours cause no problem: surplus and deficit sets are disjoint within a row, and earlier completed transfers in that row return its size to a_i. Adjacent cycle edges cannot have the same colour because their shared label would then be both surplus and deficit in that row.

Thus every primitive is legally supplied, one incidence in one existing root. Add-before-remove retains floor a_i. A completed cycle returns EVERY row to its original compact size and EVERY label degree to its value before that cycle. No reserve root or new label is borrowed.

All processed transfers add a destination incidence and delete a non-destination incidence. The total symmetric difference from C decreases by one at EVERY primitive. After a completed cycle the remaining pending graph again satisfies the degree balance of Section 4, and all columns have degree at most D. Therefore greedy moves or another eligible cycle are again available. The structure is genuinely renewed, even if the hitting number is only q-1.

This also covers complete incidence saturation: if sum a_i=D*k, no unused column capacity exists at any completed boundary, but every unfinished balanced pending graph supplies a cycle and the same handover restores saturation. A completed cycle fixes its incidences without displacing a correctly placed incidence. There are finitely many differences, so the process ends at the EXACT compact labelled C. Its preliminary length equals the initial symmetric difference; no bound is claimed for later upper conversion.

## 6. All forbidden-cover witnesses and the converted band

For ANY palette set K with at most q-2 labels, at every preliminary intermediate state the number of roots it meets is bounded by

sum_(x in K) degree(x)
<= |K|*D+1
<= (q-2)*D+1
< r.

The estimate deliberately counts possible shared incidences more than once; this preserves the upper bound. The single-overfull certificate concerns the SAME actual columns, not independent capacities or hypothetical clones.

Consequently at least one ACTUAL existing root misses K. Select the first such root in slot order for an explicit witness W(K). This treats every forbidden pair at q4, including the temporarily overfull label, the travelling underfull label, entirely background pairs and labels unused in the endpoints. At smaller K the same bound holds; the empty set misses all nonempty roots. Hence transversal is at least q-1 at EVERY primitive.

The arithmetic inequality proves existence of the actual missed root; it is not a total coverage heuristic. Roots are floor-safe and every intermediate incidence is specified. The preliminary path may exceed q. Its finite upper bound is r because all r roots are nonempty.

Apply inherited maximum-layer Theorem A to this actual finite lower path between the EXACT-q compact endpoints. The native root carrier permits arbitrary additions and unions and retains all original positive floors. Theorem A converts it to a finite path with transversal in {q-1,q}. It can change the schedule and introduce temporary/repeated incidences; no destination-directed or efficiency property of the preliminary path is claimed for the converted path.

Prepend saved exact compaction of the original source and append reversed saved exact compaction of the original destination. Both joins are exact q. The complete path reaches EVERY original labelled destination support and incidence. No root permutation, hub alignment, X5 qualification or fixed reserve budget is needed.

The same argument can be used for every adjacent pair in any finite chain of exact endpoints admitting the stated compactions. Each complete path restores its exact original endpoint; within a lower path cycle renewal may remain at level q-1. This establishes X14C's reusable COMPLETE repair in its explicit class. It does not establish completion from arbitrary safe inexact prefixes.

## 7. Eight-label consequence from forced regularity

Fix k=8, uniform original floor h=3 and exact target four. For any label x, its actual avoiding family uses at most seven labels. X14G says four roots requiring three labels need at least eight labels, while three roots need nine. Thus every avoiding family has at least FIVE roots. Every label degree is at most r-5, even before compaction.

At r<=7, legal exact compaction would have 3r incidences, bounded by 8*(r-5). For r between four and seven, 3r<=8(r-5) is impossible, equivalently r>=8 is necessary. At r<4, transversal is at most r and exact four is impossible. Thus no exact-four endpoint exists below eight roots.

At r=8 each label degree is at most three. Exact compaction has 24 incidences, so ALL EIGHT label degrees are exactly three. Every endpoint's compaction therefore satisfies X14C with D=3; the inequality is r=8>2D+1=7. The saturated renewal handles every pair directly, with no exact-hub accessibility hypothesis. It restores all original destination supports after upper conversion and reverse compaction.

In fact the original endpoint itself must already be compact: its supports contain at least 24 incidences in total, while the original degree bound permits at most 24. This observation is not imposed as an intermediate path restriction; larger supports remain legal and are used in each add-before-remove transfer.

Feasibility at r8 is supplied by the existing two-core hub: all four triples on {1,2,3,4} and all four triples on {5,6,7,8}. Each complete core has transversal two, so their disjoint union has EXACT four, with supplied four-cover {1,2,5,6}. Padding with duplicate roots gives feasibility for every r>=8. For r>=9, accepted X12D applies: the two-core guard has five roots and ceil(3r/8)>=4. That result restores every original labelled/noncompact endpoint, not just the hub shape.

These branches prove X14E on EVERY feasible eight-label carrier. This is a consequence of a general guard palette theorem plus a general coupled incidence renewal lemma, not an isolated finite campaign.

## 8. Scientific scope, dependencies and next obligation

X14 removes the need for a spare incidence column or separate guard placement in the bounded-incidence class. The renewal structure is one temporary overfull label and a travelling underfull label; every forbidden small cover still misses an actual root, every subsequent move is supplied, and saturation is restored after each cycle. This is a reusable multiple-root/multiple-label handover with complete exact destination restoration.

It does not claim universal arbitrary-guard multiple-overlap connectivity. The original-floor/degree hypotheses are explicit. Mixed floors are permitted in X14C because row sizes/floors stay in their original slots and no permutation is used; no universal mixed-floor conclusion follows. The final converted path need not be directed toward original destinations.

Previously accepted X12/X13 classes remain valid. Only nine-label floor-three target-four carriers r7..9 can still be outside all accepted classes, before any further feasibility exclusion. This is a mathematical domain bound, not a campaign checklist. Seek stronger protection or renewal below X14C's sufficient incidence inequality. Failure of that inequality is not disconnection; empty exact-entry classes and inaccessible existing classes retain different proof obligations.

Dependencies: exact compaction and maximum-layer Theorem A at frozen baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f; X12D for k8r>=9 only. The cycle construction is related to inherited Lemma E, but it removes that lemma's spare-column requirement by allowing a single overfull actual label and proving sufficient lower protection. No source is rewritten or recertified, no classical graph/design theorem is imported.

Original A11 destination-directed universality, unrestricted nested universality and physical interpretation remain open. Conditional child lifting retains the baseline Section7 interfaces; no new nested necessity claim is made.

No numerical enumeration, scientific execution, test/workflow, run ID, implementation, benchmark, new numbered v16.55 certification or integration merge. Separate accepted efficiency baseline/design and certified v16.54 remain unchanged.
