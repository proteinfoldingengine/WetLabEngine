# Measured rank selects a live writer in the four-child campaign

In the v16.53 R campaign an input specification contains the palette and four child supports. The producer encodes them as a full four-leaf tree, computes its root cover number, and passes that value into the original normalizer. At rank two the normalizer expands supports and contracts to its canonical assignment. At rank three it reconfigures sets of missing labels. Both branches pass their generated paths to the original tree writer, which sets and clears the child incidences. Neither the rank, the first receiving site nor its edit is an R-case input. The ordered palette, ordered children, canonicalization law and entry into the campaign are inherited.

## A source-dependent destination at identical measured rank

In original case 1173 the four child supports are {0,1}, {2}, {0}, {0,1}. The middle two sites are potential receivers. Each of the following is a valid same-union v16.26 deletion from that one prior. Each removes label 0, has the same root parent, and raises the cover number from two to three. Both resulting whole trees are also original v16.53 inputs. The original normalization from each was reproduced in full.

| Source edit from 1173 | Original post-edit case | Receiver's first write |
|---|---:|---|
| Remove 0 at site 1 | 830 | Site 2 changes from {2} to {0,2} |
| Remove 0 at site 4 | 1172 | Site 3 changes from {0} to {0,1} |

Both receiver priors agree between arms. Both runs use the same rank-three routine and end at the same canonical tree. Their physical first writes differ because the routine reads which branch first holds each *missing* label and removes redundant occurrences from later branches. That deletion from a missing-label set becomes an addition to the corresponding physical branch. In case 830, label 0 is already missing at site 1 and then missing again at site 2. In case 1172 the first repeated missing label occurs at site 3, for label 1. The original lift commits each edit to the tree in its returned trajectory.

There are 144 unordered pairs of rank-raising cuts from common three-label priors. In 48 pairs the two post-cut runs have different first receivers. In 12 pairs both receivers are outside both source sites. These are enumerated pairs in the historical row order. In a separate test on the displayed pair, 48 of 144 simultaneous changes of sibling and palette order preserved a difference of first destination; 12 kept both destinations remote from both source sites. The two source sites initially have exactly equal supports. Swapping them fixes both receiver sites and exchanges the two histories. Consequently a law respecting that symmetry after forgetting sibling order could not assign these two different fixed receivers to those exchanged histories. The historical order is doing identifiable work here.

## The measured rank can change which writer runs

A second comparison isolates the choice of routine. Case 643 has supports {0}, {0,1,2}, {1}, {0,2}. Deleting 0 at site 4 produces case 642, with a singleton {2} at that site. The measured rank goes from two to three. Case 643 first installs 1 at site 1; case 642 first installs 2 at site 3. Replaying these two complete paths under all 144 sibling and palette orders changed the first destination in every paired run. In 48 it was remote from site 4 in both arms.

This rank-switch result extends to all 720 qualifying cuts from 576 distinct states in the three-label R corpus. In the historical order every cut changes the first destination; 324 change it between two sites both distinct from the cut site. In 432 of the 576 source states only one legal cut raises the rank. Other legal cuts can still exist.

For the general order argument, rank three with three labels requires singleton branches for all three labels: if the singleton for label j were absent, the other two labels would meet every branch. A rank-raising deletion therefore turns a two-label branch into a singleton. It leaves the set of non-full branches unchanged. Rank-two expansion first edits the earliest non-full branch. In the rank-three routine that same branch is the first owner of each label missing there, so the initial cleanup cannot write there. A later branch must contain a repeated missing label because two distinct singleton branches lack a common third label. Cleanup writes at such a later branch. This explains the change in first destination under any common ordering. The individual physical destinations can vary.

## Connection to the layer repair and the remaining gap

In original two-label case 328 the computed rank is one. Its first three full masks are [27,31] → [31,31] → [31,29]. This is precisely the receiver-first route of the preceding layer calculation with four rows, oriented to begin at this prior. A direct release first would instead reach [27,29]. That very state occurs as original case 274: the historical caller measures rank two there and its next edit returns to [27,31]. Thus a matching route in an original writer is compatible with two different programs. The v16.53 R caller uses its own rank-dependent planner. The five direct calls to v16.54 clip in mechanisms.py take q from the case parameters. This establishes no caller connection from R to clip.

The comparisons use original paths from independently enumerated starting states. The v16.26 verifier validates the connecting deletion, but these separate invocations do not establish live dispatch after that event. Across all 2,401 three-label R paths, every one of the 132 internal primitive transitions from rank two to rank three was the final edit of its run. There was no next edit in those runs to attribute to a fresh choice of writer. The source-sensitive receiver writes are genuine; these records leave open who initiates the connecting prune and calls normalization again. No claim about a P1 grade or physical geometry follows from this test.

The checker regenerated the 2,863-record certificate, matched its compressed Git blob 9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e, and checked every complete three-label R path with the historical verifier. The comparisons and order controls are exploratory. From the repository root run:

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/rank_dispatch.py ResearchHistory/UQCF-GEM/demos
```

[Historical caller and tree writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Missing-label reconfiguration](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py) · [Checker](rank_dispatch.py) · [Results](rank_dispatch_results.json) · [Layer repair](LAYER_HANDOFF.md)
