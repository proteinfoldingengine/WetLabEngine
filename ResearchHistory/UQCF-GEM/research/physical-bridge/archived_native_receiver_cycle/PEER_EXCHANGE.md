# A receiver becomes the next source in an original compact run

In case 170 of the v16.51 ternary certificate, the ordinary program sends label 3 from branch 1 to branch 4, then from branch 4 to branch 7. The first recipient and both its leaves acquire 3. That locally stored role becomes the outgoing role in the second exchange. Both interactions occur in one call on a compact input. The first recipient is an intermediate destination even though the canonical endpoint assigns 3 to branch 7.

The ordered tree, palette, initial state, target ranks, choice to invoke normalization and historical normalization law are inherited inputs. No per-exchange source, recipient or payload is an argument to the normalizer. Two questions can therefore be tested separately. What does the existing law generate from the tree? What can the tree still tell us after the source has released its label?

## The two exchanges

Case indices and frame numbers are zero-based. The root has three binary branches. The inherited ranks are (3,2,1,1). Their canonical branch supports are {0,1}, {2}, {3}, respectively. A label is present at a site when its bit for that site is set. The archived compact reversal supplies the original start. The ordinary normalizer produces all 36 primitive edits.

| Frame | Branch 1 | Branch 4 | Branch 7 | Evidence in the tree |
|---|---|---|---|---|
| 14 | {0,3} | {1} | {2} | Branch 1 needs 1. Branch 4 holds it. |
| 18 | {0,1} | {1} | {2} | Branch 1 has acquired 1. Label 3 is absent everywhere below the root. |
| 24 | {0,1} | {3} | {2} | Branch 4 and leaves 5 and 6 hold 3. Branch 4 needs 2. |
| 30 | {0,1} | {2} | {2} | Branch 4 has acquired 2. Again 3 is absent below the root. |
| 36 | {0,1} | {2} | {3} | Branch 7 and leaves 8 and 9 hold 3 at the exact endpoint. |

There are two direct checks of the handoff. First, restarting the unmodified normalizer at frame 14 reproduces the remaining 22 edits. Restarting separately at frame 24 reproduces the remaining 12 edits. Each restart receives the **whole tree** and the same ranks. Second, we calculated the two exchanges independently from the retained incidences, topology and ordered canonical target. At the first branch whose support differs from its target, take its one excess label and its one missing label. The unique peer holding the missing label is the recipient. Apply the historical local edit order to the occupied sites of both branches. Reapply this calculation to its own output. Starting at frame 14, it predicts all 22 edits without reading the program counter, role array, trace, next frame or branch indices. This calculation is tested on single-mismatch states here. The historical law also handles internal permutations and more general inputs.

Fourteen original compact cases contain consecutive exchanges relaying the same outgoing label across three distinct branches under the explicit criterion in the checker. In two of the fourteen, cases 170 and 1466, a fresh normalization at the completed first handoff reproduces the entire remaining archived path. The other twelve still relay the label in their uninterrupted execution.

## When the midpoint determines the receiver write

Let the disjoint upper branches have a total of W roles in a palette of k labels. Immediately before a cross-branch exchange, the W roles have distinct labels. Write x for the outgoing source label and y for the peer's label. After the source replaces x with y and before the peer acts, exactly y is duplicated, and the union of the branch supports has size W−1. Consequently **k−W+1 labels are absent**. The outgoing x belongs to that set. Hierarchical nesting makes absence at all upper branches equivalent to absence below the root. All palette labels stay present at the root.

When k=W, x is the unique absent label. In a direct exchange the source is the canonical owner of y, because the historical outer loop is filling y's own slot. The recipient is the other current holder of y. Thus the duplicated label, the missing label, the tree and the inherited canonical assignment recover the entire next receiver operation. This orientation theorem assumes a direct exchange. The historical program can also use three exchanges via a third branch to implement a within-branch permutation.

The checker regenerated all 864 original root-rank-three paths and matched every frame against the certificate. There were 2,048 cross-branch exchanges, including 1,304 with k=W. Of 1,220 direct exchanges, 890 had k=W. For all 890, we inferred the recipient and both labels from the midpoint as above, applied the stock role edit and recovered the full recorded receiver segment. Those events covered 439 distinct midpoints when keyed by tree, ranks, palette size and full retained state. None had a competing observed source, recipient or payload in this archive. The historical code actually keeps x in a local variable. Reconstruction establishes what the incidence determines under the stated hypotheses.

## A spare label changes the answer

Original cases 176 and 177 share tree T, rank profile (3,2,1,1), palette size 5 and reversal order. Case 176 starts compact. The other original preparation adds precisely one incidence, label 0 at node 1, to the first initial state. Both runs make branch 1 gain label 1. Immediately afterward their complete raw trees are identical, with palette-indexed site masks [7,907,113,1,1]. Branch 7 and its leaves have the same prior. Both 3 and 4 are missing below the root.

The next archived edit puts 4 at node 7 in case 176 and 3 there in case 177. Both labels subsequently reach leaves 8 and 9 in their respective histories. At completion of the exchange, all differences lie inside that receiver subtree. The worker's current roles, physical owners and two slot indices also agreed immediately before the second half. The enclosing exchange retained the different outgoing x. Replaying the receiver worker from the same midpoint with each captured x reproduced its six original edits. A fresh ordinary normalization at the completed handoff took six more edits in case 176 and zero in case 177 and reached the same canonical endpoint.

Across all rank-three paths, 73 of 1,154 midpoint keys admitted more than one observed outgoing label even after fixing source, gain and recipient. None of those keys had two different payloads within the frozen compact preparations alone. The following controlled compact inputs test the same effect without changing the mode.

- Two independent relabelings of the compact case-176 seed vary the outgoing label (3 or 4) and the branch holding the desired 1 (4 or 7). The unchanged normalizer realizes all four combinations. With branch 4 first, that receiver forwards the same x to branch 7. The ordering used to process the palette stays fixed.
- More generally, use k labels, fork 1 with roles 0 and x, and singleton forks with 1 and 2. For either placement of 1, every x in {3,…,k−1} produces the same whole midpoint at fixed k and placement. The first receiver edit then adds x. Thus the k−3 candidates are all realized in this four-role family. A deterministic replay from this midpoint needs at least k−3 distinguishable pending states if it must match every historical continuation. Retaining x suffices for the next exchange half. All 870 compact runs for k=4 through 32 passed the historical path verifier. The independent incidence calculation also reproduced every first exchange and every immediate forwarding exchange in the branch-4 arm.
- As a control on intermediate absence, all 210 order-preserving interleavings of the four source edits with the six receiver edits pass the historical validity and endpoint checks for each of the four compact controls. Only the all-source-first order removes x from every nonroot site at once. In 208 orders, both exchanged labels retain a nonroot holder throughout. The certificate implements the all-source-first order.

## Relation to the earlier rank-two question

In compact cases 912 and 948 the historical rank-two anchor is fixed at entry. Node 1 has width one and canonical target {0}. Normalizing a binary child preserves its root support, child compression only deletes, and transporting one remaining role can add only its canonical label. An ordinary rank-two run with this setup therefore cannot first add the absent label 2 at node 1. Across all 864 archived rank-two paths we checked 816 width-one upper branches and all 452 positive incidences there. Every gain was in the relevant branch's canonical singleton. The rank-three construction answers a different question about actual peer delivery available elsewhere in the same historical producer.

The receipt traced here is the source's actual outgoing **role label**. The archive does not identify it with the four event receipts in the separate campaign log. The tree, canonical target and priority order are still inputs. Whether the retained information generates those choices, or a geometry with a measurable scaling or curvature, remains open.

## Reproduction

From the repository root, the command verifies the four historical code hashes, the original compressed certificate hash, the archived paths, the new controls and the included evidence stream. Python assertions must be enabled.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/peer_exchange.py \
  ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface
```

The evidence stream has 890 JSON lines. Its uncompressed SHA-256 is `7196c0c89ccf1c8a744e5ed76342f41769282c88f015e4716d666a292002e3be`. These 890 lines contain the 14 archived relay cases, 2 archived collision cases, 4 compact controls and 870 family runs. The count of 890 direct saturated exchanges is a separate census over the frozen archive.

[Historical producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py) · [Historical certificate](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/evidence/science/scientific/CERTIFICATE.json.gz) · [Checker](peer_exchange.py) · [Numerical results](peer_exchange_results.json) · [Complete paths for the cited examples and controls](peer_exchange_paths.jsonl.xz) · [Earlier rank-two result](COMPACT_ORDER.md)
