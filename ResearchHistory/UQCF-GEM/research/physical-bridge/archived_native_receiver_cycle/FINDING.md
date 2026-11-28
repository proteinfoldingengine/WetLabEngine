# An original M9 receiver keeps a distinction through the end of the run

In archived record **2393447**, two rows reach the same local state. Each holds the labels {2,3,4} at its root and (2,3) in its two named leaves. The running parent routine withdraws 3 at one row and 2 at the other. The inherited writer puts the unique spare 4 into whichever leaf held the withdrawn label. Later both rows undergo the exact same parent change, {0,1,4} to {0,1}. Each contains the same unordered leaf set {0,4}. The code reads where 4 is actually stored and writes the unique spare 1 there. The two ordered leaf records stay different through termination.

Both occurrences are in **one original v16.54 M9 execution**. The comparison follows two rows at their respective local events. They occupy different positions in the supplied guard construction. The archived record includes both the parent path and the nested leaf path. The historical M9 producer itself allocates one branch per input row, attaches the supplied number of leaves, initializes them from that row's first labels in sorted order, and invokes the v16.53 writer. The experimenter supplies no separate attachment or follow-on probe for these records.

## The archived write and read

Indices and frames are zero-based. Each pair of numbers in the frame column identifies the parent frame at the first write and at the later common withdrawal.

| Row | Earlier generated withdrawal | Leaf receiving 4 | Leaves before the common withdrawal of 4 | Leaf receiving 1 | Terminal leaves | Parent frames |
| ---: | ---: | ---: | --- | ---: | --- | --- |
| 4 | 3 | 15 | (0,4) | 15 | (0,1) | 5 and 36 |
| 5 | 2 | 17 | (4,0) | 17 | (1,0) | 8 and 24 |

The parent plan first moves rows 4 and 5 toward the different required guard sets {2,4} and {3,4}. That determines the earlier withdrawals. Label 4 remains in the same leaf throughout the interval until the common parent withdrawal. Immediately before that withdrawal the root, the unordered set of occupied labels, the removed label and the available spare all agree across the two rows. The physical child holding 4 differs. At the read, the raw nested path adds 1 to that child, removes 4 there, and then removes 4 at the parent. The table compares leaves by local slot and gives their original global node IDs. Row 5 ultimately regains all five parent labels. Row 4 ends with parent holdings {0,1}.

Replaying the inherited writer on the recorded pre-read leaf states chooses slots 1 and 0 in the two rows. As a separate intervention, sorting each leaf tuple before the read preserves the parent and unordered occupied set and makes both writes go to slot 1. The historical code reads current retained incidences. A journal object need not be passed back into it.

Record **2393448** repeats the comparison with three leaves. From the common parent {3,4,5,6} and common leaves (3,4,5), the two rows withdraw 5 or 3. They put 6 into the last or first slot. Later they both withdraw 6 from {0,1,2,6}, both use the sole spare 2, and send it back to the same slot that received 6. These are archived leaves 24 and 30. The terminal leaf tuples are (0,1,2) and (2,0,1).

## Terminal records after forgetting leaf order

For each of the four original M9 records, we compared every unordered pair of distinct rows within that run. A pair qualifies if the rows start with equal roots and equal ordered leaf values, end with equal roots, and have different **sets** of terminal leaf values. Separately we count single rows for which the parent returns to its full initial local holdings and the ordered leaves have changed. These are descriptive counts across overlapping row pairs.

| Global record | Leaves per row | Parent hitting target | Closed rows with changed ordered leaves | Qualifying pairs with different terminal leaf sets |
| ---: | ---: | ---: | ---: | ---: |
| 2393446 | 3 | 4 | 8 | 28 |
| 2393447 | 2 | 3 | 1 | 0 |
| 2393448 | 3 | 3 | 2 | 1 |
| 2393449 | 2 | 4 | 3 | 6 |
| **Total** | | | **14** | **35** |

For example, rows 6 and 7 of record 2393448 both begin and end with every label from 0 through 6 at the parent. Their initial leaves are (0,1,2). Row 6 ends with (3,6,5), entirely disjoint from its initial label set. Row 7 ends with (2,0,1), preserving its entire initial set. The difference between zero and three surviving original labels is invariant under permutation of the leaves or any consistent renaming of labels. This example compares different indexed histories in a single prepared run.

## Why the last receiver rotates for arbitrary leaf count

Consider the same stock guard construction with integer leaf count $h\ge 2$, parent hitting target 3, unit shift, reversed label transformation and $2(h+1)$ rows. The palette is $U=\{0,\ldots,2h\}$. Put $D=\{0,\ldots,h-1\}$, $A=D\cup\{h\}$, $B=\{h+1,\ldots,2h\}$ and $G=B\cup\{h\}$. The initial guards are all $h$-subsets of $A$, followed by $B$ and full surplus rows. The reversed guards are the $h$-subsets of $G$, and the reversed standalone row is $D$.

The stock guard phase assigns the last full surplus row to the lexicographically last $h$-subset of $G$, namely $B$. Its first leaves are $(0,\ldots,h-1)$. The routine deletes labels $0,\ldots,h$ from the full parent in ascending order. At the first $h$ deletions it fills the vacated slots with $h,\ldots,2h-1$ in sequence. The deletion of $h$ then puts $2h$ in slot zero. The leaf record is now $(2h,h+1,\ldots,2h-1)$.

In the coexistence layout row 1 holds $D$ and the last row holds the unique $B$. Row 1 requires $B$ in the target. The original reorder exchanges the two supports by adding the incoming labels before removing the outgoing ones. The last row first gains $D$. As it releases $h+1,\ldots,2h-1$, the least available spares $0,\ldots,h-2$ fill slots 1 through $h-1$. The last release, of $2h$, puts the only remaining spare $h-1$ in slot zero. The remaining reversed guards are distinct. Reordering them leaves the unique $D$ in the last row until row $h+2$ requires it, at which point the last row acquires $U$. Those additions leave the leaves untouched.

No upper-layer clipping alters this itinerary. Every row endpoint in these guard, coexistence and permutation phases is a guard on $A$ or $G$, the set $D$ or $B$, or the full set. One element from $D$, the pivot $h$ and one element from $B$ hit all of them. During a replacement or swap each intermediate row contains its old or its new endpoint, so this same triple remains a cover.

Thus the parent returns to $U$ and the induced leaf action is
$$
(0,1,\ldots,h-1)\longmapsto(h-1,0,\ldots,h-2).
$$
The parent decisions and spare choice depend on occupied labels and respect a permutation of leaf slots. On all slot orderings of the initial set $D$, the same closed parent itinerary applies the label permutation $j\mapsto j-1\pmod h$. It has exact order $h$. Repeating that local itinerary is an algebraic test. The archived run makes one circuit. The campaign contains the $h=2,3$ examples. Additional runs of the unmodified producer at $h=4,5,6,7$ passed its verifier, and all slot orderings were checked at each tested size.

## Scientific scope

The ordered initial rows, available palette, uniform leaf count, shift, reversal and calling convention are inherited inputs. The original code constructs the nested state, computes the parent edits, selects the actual child from its holdings, and retains the result. This identifies a historical mechanism where locally identical parent endpoints allow persistent child information. The [v16.53 first-child endpoint result](../four_chart_exact_surface/ORDER_INDEPENDENT_RECEIVER.md) concerned a different map that canonicalizes the entire subtree. M9 canonicalizes the parent and transports the existing leaves along its path.

The record establishes a label acquisition, its subsequent use and a surviving receiver distinction. Recovering an arbitrary event's unique identity from the terminal leaves alone, independently generating the branching law, and delivering a receipt from the earlier 1,509-byte campaign log remain open. No spacetime or continuum interpretation is needed for the finite rotation.

## Reproduction

The four original newline-terminated JSON rows are bundled losslessly. All four regenerated rows matched their archived bytes before analysis. Every parent event was checked against the corresponding raw nested edits and the historical independent verifier accepted every complete record. The optional shard check compares the bundled rows directly to the original ZIP, verifies its published SHA-256, and checks the original case identities, ordinals and source bytes.

[Original campaign run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37059520424) · [Original shard 7](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37059520424/artifacts/11251351546) · [Historical M9 constructor and writer call](https://github.com/proteinfoldingengine/WetLabEngine/blob/0ba1284ade581267997882de2d4c723f2b9ee3a4/ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/mechanisms.py#L296) · [Bundled original rows](original_m9.jsonl.gz) · [Replay](replay.py) · [Measured output](results.txt) · [Exact paired frames and all qualifying row pairs](witnesses.json)

Run from this directory with the linked revision's v16.54 demo in a Git checkout that can resolve the inherited v16.53 parent commit. Use --shard /path/to/original.zip to verify the optional original ZIP. Ordinals are zero-based.

```bash
set -euo pipefail
python -B replay.py "$DEMO" | diff - results.txt
python -B replay.py "$DEMO" --details | diff - witnesses.json
```
