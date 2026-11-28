# One remote incidence redirects a retained write in M9

In a new six-row preparation, adding label 4 to row 0 changes which leaf of row 4 receives the same later write. In each fixed-target comparison, the complete initial nested states differ by exactly that one incidence, including at the source. All leaves start identically. At termination the complete states differ only at leaves 14 and 15, both owned by row 4. The underlying program is the historical, hash-pinned v16.54 M9 producer and its bound v16.53 clearance routine. The preparation was found by exploratory search and is outside the four archived campaign cases.

## How the difference reaches the receiver

At preliminary parent frame 5, the six rows in the first arm are

`{0,2}, {0,2,3,6}, {3,6}, {1,4}, {1,2,4,5,6,7}, {5,7}`.

Rows 0, 2, 3 and 5 are pairwise disjoint. Any set of labels meeting every row needs at least four labels. The least minimum cover in the historical label order is {0,1,3,5}. With the extra 4 at row 0, the cover {3,4,5} meets every row. Rows 2, 3 and 5 remain disjoint, so three is exact. The receiver has precisely the same preliminary holdings in both arms.

The parent routine enforces a ceiling of three by replacing states at the maximum layer of its proposed path. In the first arm the maximum is four. At this frame its first two cover labels are 0 and 1, so it includes 0 in every row holding 1. That condition includes row 4. In the second arm this frame already meets the ceiling. Across the affected part of the path, the first arm postpones row 4's withdrawal of 0 until after its withdrawal of 2. The second arm withdraws 0 first. Without the maximum-layer replacement, the entire sequence of preliminary local parent edits at row 4 agrees across the two arms at either fixed target. This comparison identifies the connecting operation. The preliminary path itself can exceed the allowed ceiling.

Row 4 starts with labels (0,2) at leaves (14,15). After its first two clearance writes the leaves hold (4,1) in the first arm and (1,4) in the second. The same later parent withdrawal of 4, from the same complete parent transition, makes the historical writer put 0 into the leaf that held 4. It writes to leaf 14 or 15. Two subsequent common withdrawals preserve the distinction through termination.

| Source at row 0 | Leaf that receives 0 on withdrawal of 4 | Terminal leaves (14,15) | Leaves that finish with their own starting label |
| --- | ---: | --- | ---: |
| {0,2} | 14 | (2,3) | 0 |
| {0,2,4} | 15 | (3,2) | 1 |

The last column is invariant under consistent renaming of the leaves and labels. In either arm the unordered set of terminal labels at this receiver is {2,3}. An observer with access only to that set cannot distinguish them.

## Separating the starting bit from the target

Let T₀ and T₁ be the two targets computed from the respective inputs by the historical reversal and one-row cyclic shift. They differ by label 3 at target row 1. Running all four source-target combinations makes the endpoint a controlled variable. The diagonal recomputes the target from the corresponding starting rows.

| Starting row 0 | Row 4 under T₀ | Row 4 under T₁ |
| --- | --- | --- |
| {0,2} | (2,3) | (2,3) |
| {0,2,4} | (3,2) | (3,2) |

With T₀ fixed, the last 42 complete parent frames agree. With T₁ fixed, the last 38 agree. All three later withdrawals used in the replay lie inside the respective common suffix. The global hitting number at both endpoints is three in all four runs.

Across all six cyclic shifts with palette reversal, row 4 is the only remote row whose terminal leaf tuple changes at either fixed target. Across all six shifts preserving the palette, every remote row has the same terminal tuple in the two arms at either fixed target. The twelve settings and both source-target crossings are exhaustive for this preparation. They share a single fixture and do not estimate prevalence. A separate pilot with a common supplied target gives a second example at row 5. There the common withdrawal of 6 puts 0 into leaf 18 or 17, and the terminal tuples are (5,0) and (0,5).

## Relation to the archived campaign

For the four archived M9 inputs, all 248 single-incidence flips that respect row size floors admit a set of at most q labels meeting every modified starting row and every row of the fixed original target. Of these flips, 209 also preserve the original source guard's hitting number. The cover bound gives a direct control. Each row replacement adds its new elements before deleting old ones. During reordering, the union route has the same property. Thus every row along the preliminary route contains an initial or target row, and the common cover meets it. No maximum-layer replacement occurs. Before all rows reach the prescribed intermediate tuple, other rows' local edit sequences are independent of the flipped row. The subsequent reorder starts from the same complete tuple. No remote terminal leaf changes by this intervention on the original four inputs.

The companion [fixed-plan proof](STOCK_PLAN.md) extends this control to all admissible preparations on those four fixed targets. It explains why the positive construction uses six rows with eight labels.

**Scientific scope.** The program generates the affected local operations, determines their leaf addresses from current holdings, and changes the receiver's retained state. The run uses a prepared incidence structure, a specified guard construction, a ceiling, and fixed ordering rules. The experiment identifies one causal bit under those conditions. Deriving the initiating process and its geometry from unprepared information remains open. Reconstructing the original event receipt from the earlier campaign log is a separate open test.

## Reproduction

Run from the repository root with the v16.53 binding commit available in Git history.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/remote_incidence.py ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity
```

The script hash-checks the historical source, runs the historical record verifier on all 50 new records, independently enumerates small covers, checks actual primitive nested writes at row 4, and compares the whole regenerated record stream to `remote_records.jsonl.gz`. The first four records are the source-target matrix in row-major order, the next two are the pilot, and the remaining 44 cover the other eleven settings. The uncompressed SHA-256 is `523f72aa166f8c9ef2e75920b56ff81a3bfe9493f6608bacb912962df144f38d`. The four original M9 records and their separate archive replay are in this directory.
