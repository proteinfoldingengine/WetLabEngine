# An archived source edit leaves a record confined to the receiver

In v16.51 campaign cases 2208 and 2209 (zero-based), enabling the historical rank-preserving preparation adds exactly one incidence, label 3 at node 1. No caller specifies that edit, the receiving branch or the leaf writes. The unchanged normalizer then selects nodes 1 and 4 as the first pair with a shared label and uses 3 as their shared label. At node 4, two leaves acquire 3 and one releases it. Later the program removes the source incidence. At frame 21 every difference from the quiet compact state lies strictly below node 4. A fresh invocation can act on that retained difference with no supplied history.

The complement clue from M9 led to this test. In M9 the parent route is constructed from the endpoint before the leaves are initialized. The earlier ternary program contains a different sequence of operations that actually generates a complement and uses it in choosing an interaction. Earlier ternary experiments traced a receiver write after preparing alternative overlaps. Here the addition is made by the original campaign preparation, and both complete comparison paths occur in the published certificate. [M9 guard result](GUARD_ONSET.md) · [Original ternary producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py)

## How the program generates the source and the receiver write

Both cases start construction from the same canonical tree U, identity palette order and stored rank profile (2,2,2,1,2,1,2). The campaign explicitly includes a compact mode and a mode that tries to enlarge each branch while preserving rank. The upper branch nodes are ordered 1, 4 and 9. Their compact supports are {0,1}, {2,3} and {0,1,2}, respectively. The root hitting number, the minimum number of labels meeting every branch, is two.

In compact mode the starting state is already the canonical endpoint, and the program emits zero edits. In expansion mode precisely two additions to the compact top-level supports individually preserve rank. Both add label 3, one at node 1 and the other at node 9. The historical scanner visits node 1 first. Once it accepts 3 there, adding it also at node 9 would put the same label in all three branches and lower rank to one. The complete expanded start differs from the compact start only at node 1. The stored starting states and the independently regenerated preparation verify that one-bit difference. The certificate stores the resulting start and normalization path; it has no separate journal of unsuccessful preparation attempts.

With compact inputs, the first overlapping pair is (1,9) and its first common label is 0. After the addition, nodes 1 and 4 overlap on 3. The routine selects them, gives their common label priority, and normalizes their descendants. The other admissible placement of the same source label, at node 9, is a new control: node 4 starts identically, the selected pair is (1,9), and the complete one-edit path clears the added bit without changing any part of node 4.

| State or boundary | Source node 1 holds 3 | Receiver node 4 | Leaves 6, 7, 8 below node 4 |
| --- | --- | --- | --- |
| Compact start and end, case 2208 | No | {2,3} | (2,2,3) |
| Expanded start, case 2209 | Yes | {2,3} | (2,2,3) |
| End of first child-normalization pass, frame 13 | Yes | {2,3} | (3,3,2) |
| After the source has returned to its compact state, frame 21 | No | {2,3} | (3,3,2) |
| End of case 2209, frame 37 | No | {2,3} | (2,2,3) |

At frames 6, 7 and 8, the stored path adds 3 to internal node 5 and then to leaves 6 and 7. At frames 9 through 11 those three nodes release 2. Leaf 8 then acquires 2 and releases 3. Even forgetting leaf order, the number of leaves holding 3 changes from one to two. Label 3 was already present elsewhere in node 4 before this acquisition. At frame 21 the only changed nodes in the entire incidence array are 5, 6, 7 and 8. All supports outside that proper subtree, node 4's own support, and the exact rank profile agree with the quiet run.

Restarting the unmodified normalizer at frame 21 generates eight primitive edits confined below node 4. Restarting at the compact state generates zero. Both end at the compact state. The uninterrupted run has sixteen edits left at frame 21 and follows its existing schedule. The fresh-start test measures what the receiver record can cause in a new call; recovering the prior execution position from those records would be a stronger claim.

## The complement follows from the historical rank rule

Let U be the full palette and S₀, S₁, S₂ the three initial supports in scan order. Suppose their hitting number is two. Adding incidences cannot raise it. An attempted addition is rejected exactly when it would make a label present in all three branches. The scan therefore fills each label to exactly two branches, in the earliest available positions, while preserving any existing holders. Different labels' acceptance decisions are independent.

Consequently the final sets of labels shared by each pair are

- branches 0 and 1 share U minus S₂;
- branches 0 and 2 share S₂ minus S₁;
- branches 1 and 2 share S₂ intersect S₁.

These three sets partition U. For instance, a label initially absent from the last branch must fill the first two before the scan reaches the last. A label already in the last branch occupies the middle branch in the final pair precisely if it was there initially. The first surviving pair in the normalizer's order selects its least label. In case 2209 the last branch lacks exactly 3. This determines the first pair's payload directly from the compact state. The formula addresses the upper branches; the original recursive normalizer supplies the subsequent leaf writes.

The stored ordering has an observable effect. Across the six sibling orders in the parent-level calculation for this case, the prepared edit always adds label 3. Two orders select 3 for the subsequent interaction, two select 0, and two select 2. The historical order selects 3. The experiment does not derive that ordering or the choice to run the expansion mode.

## Archive census and reproduction

The full 2,592-case certificate regenerated byte for byte after decompression. Both normalizations in every one of its 432 compact/expanded pairs at root rank two reproduced the archived paths and passed the independent historical verifier. In all 432 pairs the complement formula predicted the entire expanded top-level state and the selected pair and label. An independent bit-mask scan checked the formula on all 15,240 ordered rank-two triples of nonempty supports on palettes of one through five labels.

The selected pair or label changes in 284 of the 432 pairs. Within those pairs, 297 comparisons of individual receiver branches have identical complete starting subtrees. In 64 of those comparisons the leaf records differ at the end of the first pass. In 22, a leaf newly holds the selected label in the expanded arm while lacking it in its common prior and at the compact comparison boundary. Eleven of those 22 comparisons arise from a single preparation bit. Three of the eleven change the selected pair itself.

In eight of the 22 comparisons, the compact arm is stationary and an exact state after the first pass holds the new leaf distinction with every incidence outside the proper receiver subtree restored. All eight fresh starts produce edits and converge to the quiet state. The supplied evidence includes the case numbers, frames and fresh-start lengths. The census counts branch comparisons where indicated. These related archival cases come from one parameterized program.

The program supplies an ordered tree, palette, target ranks and two preparation modes. Within the expansion mode the rank test generates the source addition, the overlap routine selects the receiving branches and label, and the recipient's own descendants are modified. The receiver record survives removal of the source and is eventually erased by normalization. General initiation without a chosen preparation, persistent separation at termination, and an origin of the M9 opening remain open.

From the repository root run

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/ternary_preparation.py ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface
```

The output is the archived analysis JSON. The original compressed certificate SHA-256 is `91aac71f6e786af4a3876ee9a7ec09d78b4bbe0906eb5461e08d9be1318b93f9`. [Reproduction script](ternary_preparation.py) · [Counts and complete witness, control and restart paths](ternary_preparation_evidence.json) · [Original campaign certificate](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/evidence/science/scientific/CERTIFICATE.json.gz)
