# Independent analytical review: reserve activation

Verdict: **ACCEPT for the declared saturated-neighbor monotone activation template**, with one nonblocking domain clarification below. No mathematical counterexample found. This is a raw analytical review, not a numerical or implementation verification and not an unrestricted native-reachability result.

Reviewed `RESULT.md` against the source-escape result and closeout retained in `source_readbacks.json`, parent `c31f5313486be2be25ff1d32d01b507d2de2e313`. No enumeration was run; no proof or implementation file was modified.

## Criterion, assignment, and order

The finite Horn closure is well defined and independent of fair exhaustive rule order. In a run adding one new receiver w at a time, a firing donor i becomes a member of Z immediately. That donor cannot fire again: its entire saturated neighborhood stays activated. Consequently each added receiver has a distinct donor, and a full run constructs the claimed injection J -> R* with |J|=|R*|. The assigned objects can be actual preselected original labels, not merely type counts.

Each activation adds at least its firing donor to Z while adding one receiver, so |Z(R)|-|R| never decreases. The difference is nonnegative along a realizable closure run and counts exactly the unused releasable donors at its macro boundaries. Thus positive terminal surplus is sufficient; an earlier release-eligible donor implies the same positive terminal surplus. This also excludes dependence on an unlucky firing choice: every exhaustive order has the same final sets and leaves a donor available exactly under the stated strict inequality. The existence of saturated-degree-zero donors is handled correctly by Z(empty).

## Floor, cover, and label safety

Independence of I in G is substantive: a saturated root incident to a donor has its other endpoint outside I, so another donor never independently removes an original incidence at that same saturated root. At a transfer, every saturated edge lost before the pivot has an already retained full receiver label, and the pivot itself retains the moving label. A release uses the same compensation on all saturated neighbors. Original C anchors cover every H root throughout, giving both floor one for nonsaturated roots and an actual cover of at most four labels. Multiplicity at I intersect C supplies the distinct donor and anchor. Multiple choices of original copy yield the same argument without identifying distinct actual labels.

At every deletion slice the donor stays inside M_i; after the pivot it stays inside M_w. Other moving labels already occupy original full stars. Original-star domination therefore supports the inherited substitution proof of lower-three protection for every fixed original protected hidden completion. This establishes uniform admissibility, not an observation, enforcement, selection, or progress mechanism.

## Native edits, reversal, and equal stars

For distinct adjacent stars in a simple graph, their intersection is precisely the pivot edge. The transfer requires deg_H(i)-1 actual deletions and deg_H(w)-1 actual additions. The donor never becomes empty during such a transfer. A final release costs deg_H(t) and reaches its first vacancy on its last deletion. Reversing the actual edit sequence traverses exactly the safe forward states and restores the original labelled source when no intervening operation has changed it. No exchange theorem follows for use of the reserve between the two routes.

A saturated K2 component permits a zero-edit container reassignment because the two endpoint stars are equal. This does not introduce native motion or source escape. Since G-independence permits at most one donor endpoint on that saturated edge, that isolated component can contribute only one used donor and one receiver, hence no positive surplus. With singleton endpoints, C eligibility also prevents selecting the anchored endpoint as the donor. The bookkeeping event is safe, but should remain explicitly separate from actual committed edit records, as the candidate requires. Positive constructions elsewhere do not turn this isolated zero-edit event into an extra source escape.

## Hand-derived chain and novelty

The K_{4,3} fixture is sound. Its saturated subgraph is the alternating path 0-4-1-5-2-6-3. Its initial degree-one donor endpoints have distinct saturated neighbors, so it has no initial two-donor common-neighbor cherry. Donor 0 activates 4, enabling donor 1 to activate 5, enabling donor 2 to activate 6, after which donor 3 releases. Each donor star has degree three and each receiver star degree four. Each of the three transfers costs five actual edits and release costs three, for exactly eighteen constructed edits. The unchanged labels at 4, 5, and 6 give the fixed three-cover. All three transfers include genuine outside-original-star additions.

This is a substantive extension from the inherited one-step cherry: a closure of successive compensation events and an exact order-independent criterion for that specified template. It is not a new theorem about all native paths, shortest reserves, repair after reserve use, or native record origin. The G=H control has empty closure and no release; its failure is also independently explained by the inherited saturated-degree source lock. Empty G and the cherry specialization are correctly identified as inherited/simple controls rather than new classifications.

## Nonblocking clarification

State directly in Domain that a transfer i -> w uses **w in N_G(i) minus R** (a saturated pivot), if that is the intended template. The construction later says the pivot exists because it is saturated, but Domain currently only says receivers belong to N_G(I) and a donor shrinks to {iw}.

The broader literal reading could permit a nonsaturated H-edge pivot to a new receiver. Such a transfer can be safe only after all saturated neighbors of its donor are already in R, so a release is already available at its start. Therefore this ambiguity does not furnish a counterexample to the vacancy-existence criterion. However, a proof for that broader template should stop at the first release-eligible boundary: before it, every legal transfer necessarily uses a unique missing saturated neighbor and follows the closure. It should not imply that every permitted transfer in the broader reading is itself a closure firing. Tightening the domain is the cleaner choice for the candidate's stated scope.

## Remaining limits

This acceptance is analytical and scoped. It does not certify future enumeration completeness, canonical certificate construction, test coverage, publication provenance, native acquisition/access, enforcement, actual-successor choice, progress despite NOOPs, arbitrary repair/restoration, or broad C3/C4-C6 claims. The current candidate preserves these boundaries appropriately.
