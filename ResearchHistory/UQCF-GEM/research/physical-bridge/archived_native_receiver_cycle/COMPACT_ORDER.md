# A compact receiver record determines the relevant traversal in a ternary archive pair

The starting holdings in v16.51 cases 912/913 and 948/949 identify which upper branch goes first under the historical compact-state constructor. Erasing every sibling order and the order of the three labels leaves sixteen compatible executions per expanded case. All sixteen add label 2 at node 1, select node 4 as its peer, and leave exactly the same record inside that peer after the source has returned to its starting state. The two case pairs exchange the positions of two subtrees and realize the same structural example.

There is also a smaller interaction whose occurrence is independent of the compact/expanded switch. The narrow fork under node 9 receives label 1 and writes it into both of its leaves in either mode, under every compatible ordering. This transfer clears completely. The distinct record under node 4 outlives its source in expanded mode.

## What information determines the order?

The input to the inverse calculation is the tree with unordered children, its full compact incidence state, and the historical compact construction. The local hitting numbers can be computed from those incidences. The inversion uses no future frame, event label, target address, supplied palette order, or candidate execution trace. The archive specifies that the same traversal and palette convention are used to construct and process the identity-palette seed. This provenance assumption matters.

Write A, B and C for the three branches, identifiable from their supports. A is the single-label branch, B is disjoint from A, and C meets both. With physical labels a = 0, b = 1 and c = 2 the supports are

| Branch | Compact support | Width required by its subtree |
| --- | --- | ---: |
| A, node 1 | {a} | 1 |
| B, node 4 | {b,c} | 2 |
| C, node 9 | {a,b} | 2 |

For root hitting number two, the historical constructor gives successive branches blocks of lengths 1, 2 and 2 in their traversal order, wrapping around a palette of length three. Testing the six branch orders against the six label orders leaves exactly two ways to reproduce the three upper supports. One orders the branches A,B,C and labels a,b,c. The other orders them C,B,A and labels b,a,c. The label names here identify stored incidences; the test compares only equality and membership.

The distinguishing record is one level down. C has local hitting number one and two children of widths one and two. The rank-one constructor gives each child an initial segment of C's palette of the required size. The width-one child holds a. Thus a precedes b, regardless of which child is visited first. Only the A,B,C upper order survives. The reconstruction also recovers the palette ordering. The narrow child is selected by its width and holdings rather than a numbered position. The formula was checked under all 2,304 renumberings of the tree and palette for each seed and its altered-memory control.

## What the program then generates

In expanded preparation, label c initially belongs to B alone. Giving it to A preserves rank two. A subsequent addition to C would lower the hitting number to one. The other labels already occur twice. The sole upper addition is therefore c at A. The first two branches A and B now share only c. Giving c priority in B exchanges its two local labels. The branch that originally stored b in two leaves now stores c there, and the other leaf takes b. The following measurements use historical node identities.

| Boundary | Leaves 6, 7, 8 under node 4 | Other incidences |
| --- | --- | --- |
| Compact start | (1,1,2) | Reference state |
| Compact-mode normalization, all six edits | (1,1,2) throughout | The edits occur under node 9 |
| Expanded-mode first pass, frame 14 | (2,2,1) | Source still differs |
| Expanded-mode frame 20 | (2,2,1) | Only nodes 5, 6, 7 and 8 differ from the compact start |
| Expanded-mode end, frame 36 | (1,1,2) | Full compact state restored |

Of the 2,304 possible sibling and label orderings, sixteen reproduce the full compact seed in each case. They give eight distinct indexed paths. Their only differences are the intermediate states of eight pairs of consecutive edits on sibling leaves. In each pair either leaf can go first. All 256 independent combinations of the eight switches pass the native verifier and yield the same complete state at frame 20. Eight paths occur among the sixteen compatible executions. The 256 combinations are a separate admissibility test.

The actual preparation adds six incidences in total. For each compatible ordering we tested all 64 subsets, keeping the receiver's prior fixed. Twenty-five subsets preserve nesting, nonempty supports and the original exact rank profile. In all twenty that include the upper addition at node 1, the subsequent historical normalization reaches the exact frame-20 receiver-only record. In all five that omit it, the receiver misses that record. The single upper addition by itself is sufficient. The other five preparation bits by themselves cannot account for this response.

## A transfer common to both preparations

Initially the narrow child of C and its two leaves hold a alone, while C holds a and b. In the ordinary compact normalization, the rank-one routine adds b to that narrow child. The child's own rank-one routine then adds b to both leaves. It subsequently clears b from the leaves and then from their parent. The six compact edits constitute the entire path in this case. The source of the gain, its physical destination, and the label follow from the local width and holdings.

In expanded mode the original initializer produces the same three local gains during preparation. The archived normalization path clears them. The certificate stores the expanded start, not individual preparation attempts. Read-only observation of the pinned initializer during reproduction verified the gains. After suppressing idle frames, the complete local sequence of holdings of b is identical in both modes for each of the sixteen compatible orderings. Taking the number of occupied sites gives 0,1,2,3,2,1,0. This local transfer also occurs when node 4 stays quiet. It is distinct from the remote edit required for node 4's longer-lived record.

## Changing the distinguishing memory, and holding the traversal fixed

A new control changes a to b at the narrow child of C and at its two leaves. All upper supports, the receiver subtree and every rank stay fixed. If the altered state must itself be a compact seed of the historical constructor, all sixteen compatible executions now have upper order C,B,A and palette order b,a,c. The source addition of c occurs at C. Its selected peer B gives priority to b, which B already stored first. The entire receiver subtree stays fixed throughout all eight edits of the expanded normalization.

To test what the original updater reads at runtime, we crossed each of the two memories with each traversal family. For the two incompatible combinations we substituted the compact incidence state at the initializer's canonical-state input, then ran the stock expansion and normalization. With the forward traversal held fixed, either memory gives (2,2,1) at B after the first pass. With the reverse traversal held fixed, either gives (1,1,2). The narrow record therefore identifies the traversal that could have produced the compact preparation. The program itself reads its traversal from the ordered tree. A law that dynamically changes that order on reading the narrow record remains open.

## Search scope and reproducibility

The screen covered all 144 root-rank-two compact/expanded pairs with identity palette permutation, taken from the published 2,592-case certificate. Both archived paths in every pair were regenerated and independently verified. We examined 5,868 compatible presentations. The test required an unchanged receiver subtree throughout the compact run and at the expanded start, followed by the same nontrivial exact state confined to its proper descendants in every compatible presentation after the first pass. Only pairs 912/913 and 948/949 pass that specific test. Twelve compact seeds fix the upper order uniquely. In the earlier 2208/2209 example, eight presentations reproduce the compact starting state, four in each direction. The four with reverse upper order leave node 4 unchanged throughout the one-edit route.

The two preparations of 912 and 948 remain compatible with exactly the same compact data and recovered ordering. Compact mode alone generates the local transfer. Expansion also generates the longer-lived remote record. Deriving whether to initiate that expansion from those compact data remains open.

From the repository root, run the command below and compare its output with the result JSON. The script also compares each regenerated detailed record with the uncompressed evidence stream, whose SHA-256 is `4ce9e1cb7ba3a0dbc77987918a6434efb3bb21c815d991904a3a6009f5a4d5ec`.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/compact_order.py ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface
```

[Original constructor and updater](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py) · [Original certificate](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/evidence/science/scientific/CERTIFICATE.json.gz) · [Order reconstruction and controls](compact_order.py) · [Screening results](compact_order_results.json) · [1,512 detailed replay and control records](compact_order_paths.jsonl.xz) · [Prior receiver result](TERNARY_PREPARATION.md)
