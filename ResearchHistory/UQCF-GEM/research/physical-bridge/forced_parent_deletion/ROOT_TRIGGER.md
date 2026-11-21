# An original event field distinguishes the two sources at the root

A change of reference in the five-vertex example makes a pre-existing output of the v16.26 event producer distinguish the first leaf deletion. The output is the Boolean `trigger` that `engine.atomic` already returns for the immediate parent of the deleted incidence. Neither this Boolean nor the rule computing it was designed for this test.

## Premises

- **INHERITED.** The fixed nested-support carrier and its permitted one-incidence edits are specified in the frozen sibling note `DERIVATION.md`. The v16.26 same-union view deletion is implemented by `engine.atomic` and checked independently by `verify.verify_atomic`. In view language, an incidence at v is removable from a view if it is a nonroot leaf of that view and other views still cover v. This is equivalent to deleting an uncovered-by-children label from a valid row while keeping that row nonempty. Sources are `demos/v16.26-consistency-increment-law/{engine.py,verify.py,TYPE_AND_PROOF.md}` at integrated revision `e7e01bab68ba5171dacd91333f98d208d810dac3`. The original P1–P4 in that proof ledger concern this increment law.
- **SUPPLIED.** Keep the root o with children p and d, and p with children l and w. Use o=p=ABC, l=AB, w=C. In the primary comparison fix the other root child d=A in advance and compare the two possible source labels removed at l. Controls replace d with B or C and make the same comparison within each preparation.
- **SUPPLIED.** The episode realizes two consecutive same-union atomic deletions from the common preparation. Locations, indices, rates and a destination are absent from this hypothesis. Operational access by an actual retained owner and physical realization of this event type remain open.

## What v16.26 already computes

For a vertex v, the local hitting number tau(v) is the minimum number of indexed views that together contain all its children. The defining event field is true precisely if all previously minimum covers of the affected parent's children fail after the edit. For a same-union atomic deletion, the original proof shows that the Boolean is true exactly when the affected parent's local hitting number increases by one. The global h is the largest local hitting number, floored at one. The atomic record includes the affected parent, both local numbers, the Boolean and both global values. In the campaign caller `engine.produce`, the returned `trigger` contributes to the trigger count and to the per-shape digest.

## Why the bit appears

1. With any of the three singleton anchors at d, d and w cannot be deleted. The children of p cover every label at p. Hence initially the only deletions are A or B at l. After removing x all leaves are singletons and precisely x is missing from the union of the supports of p's children. The sole legal next deletion is x at p. In both histories the root and its three incidences survive unchanged.
2. On the first edit the affected parent is p. Since l and w have disjoint supports before and after, its hitting number stays two. At least one of the previous minimum covers survives and the original trigger is false on both branches.
3. On the second edit the affected parent is o. Before that edit p has all three labels, so the unique minimum cover of the two root children uses the label at d. If the leaf source removed that label, the forced deletion removes it from p. The children p and d now have disjoint supports, two views are necessary and the old minimum cover has failed. For either other removed label the anchor still covers both children and the local number stays one. This establishes trigger = (removed label equals fixed anchor).
4. Vertex p continues to have hitting number two. Thus global h is two before and after the second edit in all six comparisons. A global-increment readout would be blind. Root membership itself is also unchanged. The distinguishing output is an actual field of the mathematical event certificate computed from the root's child supports.

| Fixed label at d | Remove A at l | Remove B at l |
| --- | --- | --- |
| A | root tau 2, trigger true | root tau 1, trigger false |
| B | root tau 1, trigger false | root tau 2, trigger true |
| C | root tau 1, trigger false | root tau 1, trigger false |

The positive-reference comparison uses the bare v16.26 incidence grammar. Relative to the starting profile (1,2), both branches stay within total deviation one. The branch with a true trigger ends at (2,2), so requiring the same exact terminal hitting profile in both branches would exclude it.

The two alternatives within a row have identical starting views. Swapping the reference reverses the Boolean. Choosing a reference absent from both source alternatives makes it blind. The tree grammar admits both first events and makes no prediction of their relative frequencies.

Two earlier protected-record examples help identify what moved. The positive two-deletion path in pruning_record_bridge/ACCEPTED_DRAFT.md §4 keeps its root hitting number at two. The two outputs in view_local_pruning/REVIEWED_DRAFT.md §4 also keep their root hitting number at two. In both examples the old record is a membership projection at an internal vertex. Here the sibling reference makes the original root-level event field itself responsive. This is an application of the existing v16.26 P3 trigger law, with no claim of a new general increment law.

## Source replay and physical boundary

`replay_root_trigger.py` calls the blob-checked original v16.26 producer on every index and nonroot site from each relevant state, and checks every successful record with its independently written original verifier. It also computes the two-child hitting number directly from their intersection. Flipping the reported Boolean makes the original verifier reject each of the six changed certificates. `replay_original_atomic.py` tests the two historical endpoint choices and the competing hull interpretation on the neutral anchor. Calling `factor` with the post-source state as its supplied endpoint stops after one deletion. Supplying the final state gives two. A proposed certificate that bundles the two into a single atom is rejected. The original function's output after the first edit contains the surviving parent incidence.

The finite campaign uses distinct views. With d=A or B our three initial views are distinct and appear as an unordered cover in its enumeration on the stated tree. With d=C the initial A and B views coincide. The v16.26 atomic function accepts all three cases. The neutral fixture is a direct function replay and a v16.53 grammar fixture; no historical v16.26 production-coverage credit is claimed for its duplicate-view initialization.

The normal v16.26 campaign was replayed with its returned atomic events observed. The original production file reproduced byte for byte. Its independent verifier counted 19,995 atomic events, 4,111 local triggers, 4,090 global increases and 17 shapes. The six labelled second events map to three distinct inputs in the campaign's view ordering. Each was observed, including the neutral-reference post-source state where the views have become distinct. An initial exploratory assertion counted six distinct canonical keys. Exchanging A and B identifies each pair, and the corrected trace retains every alias. These numbers reproduce the old campaign. They are not six independent physical experiments.

The software caller uses the trigger. Its campaign totals and digests do not expose an individually accessible physical record at o. The reference at d is chosen as part of the preparation and is held fixed within the comparison. The source is the identity of the first event. The comparison does not establish a response to two independent physical preparations under one fixed source event. A physical application would have to bind two such successful operations to an actual episode and identify a retained system that can use the root's recorded distinction. A state may stop after the first edit and the broader signed grammar admits the coalescing branches in the first note. No gravity, physical duration, detection statistic, autonomous selector or new stage closure follows.

The primary paths, original outputs and controls were worked out and replayed during exploration before this follow-up was frozen. This is an unnumbered conditional argument. The earlier Gemini verdict was for `DERIVATION.md` at its own freeze.
