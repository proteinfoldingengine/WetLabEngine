# One opening addition determines the first M9 guard transfer

In each of the four original v16.54 M9 records, the label added in the first edit fixes the support of every receiving row at the first handoff. The historical row and leaf update rules then determine the address, label and order of all 259 remaining primitive edits across the four phases. This accounts for a previously unexplained choice. In the smallest record the program bypasses a unique three-edit repair at frame 10 and performs a unique three-edit repair at frame 19. The guard inferred at frame 1 requires both decisions.

The result is conditional on the original guard-transfer schedule, ordered palette, tree and stored ranks. The historical case generator supplies a reversed palette and a one-row shift when constructing its full endpoint. Why the initial state would initiate the transfer and select this particular opening without those choices remains open. These M9 records and the separate 1,509-byte campaign log have different provenance.

## Derivation

The hitting number of a family of rows is the fewest labels needed to meet every row. Write h for each row's minimum width and number of leaves, and q for the exact root hitting number. The first N rows protect a guard of hitting number q−1 while the next N rows install a second guard of the same rank. The argument applies to the historical starting geometry with h ≥ 2, q ≥ 3, sorted row encodings and the M9 guard schedule.

* Set d = h+q−2, k = d+h and N = binomial(d,h). The labels are 0 through k−1. The first N rows are all h-subsets of A = {0,…,d−1}. The first receiving row starts at B = {d,…,k−1}. The remaining receivers initially contain every label.
* M9 installs the new rows in lexicographic order of their target supports. Each replacement adds missing labels in increasing order and then deletes departing labels in increasing order. Until the second receiving row is visited, a minimum cover of the source guard and one label from the first receiver meet all rows. The root hitting number is at most q on that prefix, so the peak-clipping procedure preserves its edges.
* The first receiving row must acquire a label below d. Every width-h-or-larger subset containing only labels in B equals B. If B were the first sorted target row, every subsequent row would also equal B, giving guard rank one. The first addition x is therefore the smallest label of the first target row and of the whole new guard. Its support lies in the suffix beginning at x.
* Every family of rows of width at least h on s labels can be hit by any s−h+1 labels of that palette. A guard of rank q−1 thus requires at least d labels. Consequently x ≤ h. At x = h the suffix G = {h,…,k−1} has exactly d labels. For each h-subset E of G, its complement in G has size q−2 and fails to hit some guard row. That row lies in E and has width at least h, so it equals E. This accounts for every one of the N slots. Sorting now specifies the destination of every support.
* The inferred phase survives clipping. Let I = A ∩ G, of size q−2. Take all of I, one label in A outside G, and one label in G outside A. These q labels meet every source guard row and every inferred receiving guard row. They also meet B and every full initial row. Each intermediate replacement contains its starting or ending row, so the same cover works throughout. The native nested routine clears a departing occupied label by changing its holder to the least available spare before the parent withdraws it. The initial leaves and inferred row replacements determine every such write.

One can identify G directly on the receiver side after recognizing this branch. Each initially full receiving row holds the same labels {0,…,h−1} in its leaves. G is the complement of that locally stored set. At this handoff every initially full receiver has released all those labels. Requiring such a turnover in advance would add a premise. The opening observation is what warrants it in these four records.

## Reconstruction and controls

The predictor accepts exactly two nested frames (initial and just after the opening), the ordered tree and its stored rank profile. It has no access to a target row tuple, a future frame, a guard-end index or the generator's reversal and shift fields. The independent comparison regenerates the original full records byte for byte, runs the historical verifier, and compares every predicted nested vertex to the archive through the recorded handoff. All four records belong to one parameterized construction.

| Original record | h | q | First label | Parent edits | All primitive edits | Leaf replacements |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2393446 | 3 | 4 | 3 | 49 | 137 | 44 |
| 2393447 | 2 | 3 | 2 | 8 | 22 | 7 |
| 2393448 | 3 | 3 | 3 | 14 | 40 | 13 |
| 2393449 | 2 | 4 | 2 | 24 | 64 | 20 |
| Total | | | | 95 | 263 | 84 |

Each leaf replacement contributes two primitive edits. Subtracting the four observed openings from 263 gives 259 subsequent edits. Two additional sizes outside the frozen campaign, (h,q) = (2,5) and (4,3), gave complete phase matches over 129 and 64 edits respectively. Both used the stock generator's reversal and shift.

We ran all 116 choices of a d-label set H across the four original geometries. The supplied target guard consists of every h-subset of H, with its complement placed in one other target row and the other rows full. Both full endpoints have root rank q. Every tested target passed the native verifier. For a first label x the number of these tight support choices is binomial(k−x−1,d−1). Every x from 0 through h occurs. Exactly one such support realizes x = h. The derivation above also covers guards on more labels and rows of width greater than h.

Even specifying exact root rank at the handoff allows every opening value. A common cover of size q−1 for the two complete guards must lie inside A ∩ H. The intersection has size at least q−2. The handoff therefore has rank q precisely when the intersection has size q−2, or equivalently when B is contained in H. In that case the intersection plus one label from each side gives a q-cover. The control records exhibited 10, 3, 4 and 6 exact-handoff supports in table order. In the five-label geometry the three guards on {0,3,4}, {1,3,4} and {2,3,4} all attain the exact handoff. The archive uses the last. Twelve further runs permuted the placement of final guard rows or changed the other target rows while preserving the saturated opening. Every predicted phase still agreed.

## What selects the repair at frame 19?

The five-label archive opens by adding 2. The new guard must therefore be {2,3}, {2,4}, {3,4}, in that order. At frame 10 the middle receiving row contains {2,3,4}, with 2 and 3 held at its leaves. Immediate shortest restoration would remove 2. The inferred middle target keeps 2, so the program moves the holder of 3 to 4 and removes 3. At frame 19 the last row has the same local supports. Its inferred target is {3,4}. Leaf 17 must acquire 4, release 2, then parent 16 must release 2. Here the three edits also restore exactness.

At frame 23 the one-step repair would immediately undo the previous parent addition. In an unclipped guard route a replacement keeps its added labels, the next replacement visits a different row, and every nontrivial swap starts with an addition. Thus that immediate undo cannot be next. This accounts for five of the six bypasses. Together with the two guard predictions it accounts for all seven unique shortest repairs at distance at most three among the smallest record's 28 deficient parent boundaries. The other 21 boundaries had either several shortest repairs or no repair within three moves.

## Same observed history, opposite next action

Two additional native runs use the five-label initial state and the same shift, tree and stored profile. Their supplied exact endpoint tuples differ at a single incidence, label 2 on target row 3 (zero-based). Both open with label 0 and share every nested frame from 0 through 17. At frame 17 unrestricted native breadth-first search finds one exact state and one shortest path to it within three edits. The path adds 4 at leaf 17, withdraws 2 there, then withdraws 2 at parent 16.

With the target incidence absent, the program takes those three edits. With it present, the next action adds 2 at parent 1, and three edits later the root is still deficient. This isolates the endpoint's causal role on a less restrictive opening. It also gives a direct test for a proposed upstream origin of the interaction. The prior rank and state permit several first labels even under exact handoff. A successful native trigger must distinguish them or predict the resulting alternatives without reading the supplied target tuple.

## Evidence and reproduction

The 132 distinct controlled records comprise 116 tight supports, 12 endpoint variants, two runs in the single-incidence comparison and two new sizes. The uncompressed JSONL SHA-256 is `7641c30279b33f82e4deb3f5dcba21fa96fb3122cb46a6fd9a58455792f5019c`. From the repository root, with the v16.53 binding commit available in local Git history, run

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/guard_onset.py ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity
```

[Reconstruction and controls](guard_onset.py) · [Complete controlled records](guard_onset_records.jsonl.xz) · [Verification output](guard_onset_results.txt) · [Four original records](original_m9.jsonl.gz) · [Previous shortest-repair result](EXACT_REPAIR.md)
