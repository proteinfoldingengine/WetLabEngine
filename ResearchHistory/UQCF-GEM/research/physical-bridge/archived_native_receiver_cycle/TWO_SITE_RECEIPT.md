# When a receiver's own transition identifies the whole source atom

In 58 of the 226 guarded peer transfers in the v16.53 four-leaf archive, the receiver's own change of holding, its address, and the inherited ordered transfer rule suffice to reconstruct the complete v16.26 source-deletion record. Reconstruction reproduces the before and after views of *every label*, the source site and index, parent, local and global ranks, trigger, and remaining fields of the original atomic producer. Each candidate was compared as a complete record against the original atom constructed independently from the whole archived predecessor and checked with the historical verifier.

This conclusion is about information in the local transition of a known stock transfer. It assumes access to the receiver's before and after holding and the ordered palette and tree. The program does not install an explicit serialized receipt at the receiver. None of the 58 keeps its gained label continuously through the canonical endpoint.

## A concrete reconstruction

In original case 1368, branch 2 goes from holding {0,1} to {0,1,2} at edit 9. It acquired label 2. Under the stock rule the source for that label is branch 1. Because 2 is last in the palette, both lower labels have already reached their assigned missing sites: 0 is missing at branch 3 and 1 at branch 1. Just before the source released 2, its only missing site was the receiver, branch 2. These three facts determine the complete physical tree via one missing-site bit per label.

| Boundary | Entire tree, masks indexed by label |
|---|---|
| Before source release | [23,29,27] |
| After source release | [23,29,25] |
| After receiver write | [23,29,29] |

The original atomic record is the first transition in the table. The reconstruction used the receiver transition, with no access to the source holding, planner stack or campaign lookup table.

## Why the rule works

Use physical branches 1–4 in traversal order and labels 0,…,k−1 in processing order. In a rank-three four-leaf start a single label cannot hit three branches. If it did, one label at the remaining nonempty branch would give a cover of at most two. Thus every label is initially missing from at least two branches. The complementary-cover cleanup leaves one missing site per label, the first site where it was missing. That site is always among branches 1–3.

At rank three the canonical physical singletons are {0},{0},{1},{2}. Consequently the first missing site in the target is **3 for label 0 and 1 for every other label**. The transfer loop moves a missing label from its old site (the physical receiver) to its assigned site (the physical source).

No capacity detour is necessary in this flat rank-three family. When 0 is processed first, branch 3 cannot already own k−1 missing labels after cleanup. If it did, it would initially be a singleton holding some u, and both preceding branches would contain every label except possibly u. Then u together with a suitable second label covers all four branches, contradicting rank three. After the step for 0, branch 1 no longer owns missing label 0. If it still needs some nonzero j, it therefore has at most k−2 missing labels, below its capacity k−1. Each actual transfer fixes its label's assignment permanently during this loop. This describes the complement-transfer phase; later physical edits complete the target.

## Exactly which extra data the decoder uses

Let x be the newly acquired label, determined from the receiver's change. Immediately after that transfer half completes, x is missing at its calculated source. Every label below x is missing at its target site. Every higher label absent from the receiver is missing at the receiver. The only remaining questions concern higher labels that the receiver *already held*. For each such label, read whether the sender still holds it. If it does, the missing site is the third site among branches 1–3 other than sender and receiver. If it does not, the missing site is the sender. Branch 4 holds every label during this phase.

This recovers the completed whole tree. Undo the two known edits to get both sides of the actual source release. If the receiver previously held no label higher than x, the procedure makes zero remote reads. This covers 54 transfers of label 2 and four of label 1 in the original archive. Under the original three-label ordering, the 226 transfers present eleven distinct (receiver, prior holding, gained label) combinations. The three combinations satisfying the zero-read condition each give a unique whole source receipt. Each of the other eight admits multiple actual receipts. The conditional side read is an analytical decoder; an original receiver-local caller taking that read is still open.

The stock verifier and decoder also ran on all 2,952 rank-three starts among the 50,625 possible ordered nonempty four-branch configurations with four labels. All 6,012 transfers reconstructed exactly, including 1,304 requiring zero remote reads. These are new controls beyond the frozen campaign. The zero-read condition is proved sufficient for any supported palette and established necessary for uniqueness of the immediate receiver data within the original three-label corpus.

## Controls on history and the supplied order

Original cases 684 and 733 deliver label 0 from node 3 to node 1 at the same frame. Node 1 has an identical holding at every frame of the entire two runs, including their common endpoint. Yet immediately before the source cut the arrays are [29,27,29] and [29,23,29]. The difference is in the holding of label 1 outside node 1. No deterministic function of that entire local history, even with frame numbers, can produce both correct receipts. Seven of the 66 archived keys formed by receiver, payload, transfer frame and entire indexed local history have this ambiguity.

The source address result also depends on the historical ordering. In case 733 swap traversal positions 1 and 2 while keeping the physical receiving branch 3 fixed. The two exchanged sites have identical supports in the initial state and at the endpoint, so both complete physical initial and final trees agree. At edits 8 and 9, the original order releases label 1 from physical site 1 and delivers it to 3. The alternative order releases the same label from physical site 2 and delivers it to 3. The whole physical receiver trace agrees frame for frame. This is a controlled order substitution, not a second frozen case.

The result sharpens the genesis question: the stock rule can make an event's identity inferable locally, and the inherited ordering supplies some of the information used in that inference. The full record here is specifically the v16.26 atomic receipt. The separate historical campaign journal and the extensive P1 grade have no established identification with it.

[Earlier guarded transfer](GUARDED_PEER_TRANSFER.md) · [Checker](two_site_receipt.py) · [Numerical results and example paths](two_site_receipt_results.json) · [Original transfer code](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/cover.py)

From the repository root, run with Python assertions enabled.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/two_site_receipt.py ResearchHistory/UQCF-GEM/demos
```
