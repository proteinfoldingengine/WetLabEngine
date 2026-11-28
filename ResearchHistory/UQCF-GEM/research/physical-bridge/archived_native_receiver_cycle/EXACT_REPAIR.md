# The unique shortest repair predicts an observed write in all four original M9 records

There is a recognizable state in each original campaign run where the stored target profile and current incidences determine one shortest way to return to exactness. It has three primitive edits. The actual historical program performs those exact edits next. The predictor takes no receiving address, payload, parent target tuple or future trace.

| Original record | Leaves per row | Root target | Starting nested frame | Parent node | Receiving leaf | Old label | Acquired label |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2393446 | 3 | 4 | 134 | 77 | 79 | 4 | 7 |
| 2393447 | 2 | 3 | 19 | 16 | 17 | 2 | 4 |
| 2393448 | 3 | 3 | 37 | 29 | 30 | 3 | 6 |
| 2393449 | 2 | 4 | 61 | 34 | 36 | 3 | 5 |

The comparison was retrospective. The five-label record suggested the condition, which was then applied to the other three. The records belong to one parameterized historical construction. All four full archived records regenerate byte for byte and pass the original verifier.

## Why the leaf, payload and order are forced at this checkpoint

In the five-label case, frame 19 has six row supports, in order:

`{0,1}, {0,2}, {1,2}, {2,3}, {2,4}, {2,3,4}`.

The target is three labels to hit all rows. Currently two suffice. Only the last row is wider than its exact floor of two. Adding an incidence cannot raise the hitting number. Of its possible one-label deletions, only removing 2 restores the required three. At the receiver, leaf 17 holds 2 and its sibling holds 3. The parent must keep every child label until its child releases it. Each leaf must remain nonempty, and the two leaves must end with hitting number two. Thus leaf 17 must acquire 4, release 2, and only then can parent 16 release 2.

This also excludes competing three-step paths elsewhere. The pair {0,2} hits every row through labels already in its leaves. While all those retained incidences stay present, no parent changes can restore rank three. At least one initially singleton leaf must lose a label, requiring at least two leaf moves. At least one parent move is independently necessary. At the resulting lower bound of three, the parent deletion is unique, which fixes the leaf, its sole spare and the order. The historical frames 20 through 22 match exactly.

An independent breadth-first search used *all* native single-incidence moves at every nonroot node. It enforced nonempty supports, nesting and the historical one-unit total deviation budget, allowing intermediate changes at any level. Distances one, two and three reached 19, 202 and 1,564 previously unseen states. Only one was exact, reached by a single shortest path.

## General checkpoint

Let h be the leaf count per row, q the required root hitting number, and A and G two sets of size h+q−2 sharing a set I of size q−2. The source guard contains every h-subset of A. A second guard contains every h-subset of G except B = G minus I. Its last row is B plus one member m of I. Every other row is exactly at floor h. All leaves are singleton and distinct within a row. The last row holds m in one leaf, with exactly one label in its support unused by its leaves.

The complete source guard needs q−1 hits, all in A if the cover has that minimum size. I and any one member of A outside I hit the current tuple and hit every row through an already occupied leaf label. In the second guard every h-subset other than B meets I, and the last row holds m. Deleting m there completes all h-subsets of G. Any cover of size q−1 would now have to lie entirely in both A and G, whose intersection has size q−2. A q-cover is obtained by adjoining one label from each side to I. Any other one-parent deletion either violates an exact floor or leaves the old cover intact. The same independent lower bounds of one parent edit and two leaf edits apply, and the unique three-step chain follows. No ordering of the palette is needed for this argument on the measured state.

## What selects the shortest repair?

The native admissibility rules define legal moves and a one-unit budget. The guard-connectivity theorem connects given exact endpoints. Neither rule mandates immediate shortest restoration at every deficient state. The five-label run itself discriminates the two claims. At frame 23 one move could return the state to exactness. The program instead adds 3 to parent 1 and stays deficient. At frame 19 a four-move legal repair could use leaf 12 and leave leaf 17 untouched.

Across all 28 parent boundaries with root hitting number two in this record, six had no exact repair within three moves. Among the seven with a unique shortest repair in that horizon, the historical route followed it once and bypassed it six times. Among fifteen with multiple shortest repairs, it followed a shortest path four times. The four matching family checkpoints establish local determination under shortest restoration. Deriving when the dynamics select that restoration remains open. This result does not identify the separate 1,509-byte campaign receipt.

[Historical native admissibility](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/NATIVE_ADMISSIBILITY.md) · [Historical two-guard theorem](https://github.com/proteinfoldingengine/WetLabEngine/blob/7abbb1b85dc71110498c4a2998b8536c70770891/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/GUARD_BUFFER_CONNECTIVITY.md)

## Reproduction and related controlled result

Run from the repository root with the v16.53 binding commit available in Git history.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/archive_exact_search.py ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity
```

[Four archived records](original_m9.jsonl.gz) · [Unrestricted search and structural predictor](archive_exact_search.py) · [Verification output](archive_exact_results.txt) · [Exact-endpoint correction and source-bit experiment](EXACT_ENDPOINT_CORRECTION.md)
