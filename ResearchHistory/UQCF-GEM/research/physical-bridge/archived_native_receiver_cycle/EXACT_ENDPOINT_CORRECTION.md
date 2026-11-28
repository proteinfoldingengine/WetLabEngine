# Exact-endpoint correction and source-controlled leaf repair

The earlier guard-completion experiment passed the historical M9 record verifier and demonstrated a persistent receiver distinction. Its final root hitting number was two against the stored target of three. It demonstrated a legal endpoint in the one-unit band. Exact endpoints in the original analytical contract must realize the entire target profile. The receiver trace remains valid. The distinction matters when claiming restoration of exactness.

## The missing unit singles out a receiver edit

Up to row order, the constructed target consists of T, K, S, A, X, S, where K = S ∪ T, A contains T, and the crossing row X meets both S and T. The disjoint pairs S and T require two hits. Choosing one label from S that lies in X and any one from T meets every row. Hence this target always has rank two.

If the other five rows are held fixed and X is narrowed, an exact rank-three endpoint requires removing every member of K from X. Any surviving member would give a two-cover. Provided at least two labels remain in X, retaining all its labels outside K meets the floor and attains three. This determines both mandatory withdrawals on the discovery fixture. An exhaustive search over *all six* rows and all 48 incidences also makes those two withdrawals the unique minimum-distance parent correction.

There is a label-independent version for the family tested here. Suppose X meets S only at s₀ and T only at t₀. Call the other members s₁ and t₁. Assume A contains T and meets S. The disjoint two-covers {s₀,t₁} and {s₁,t₀} must both be destroyed. This requires at least two deletions, ruling out a distance-two solution involving an addition. The three pair rows are already at their exact floors. K contains both labels of both covers. If a deletion in A kills one cover, it must delete that cover's T label and A must lack its S label. Since A meets S, it contains the other S label. Killing the second cover in X now leaves {s₀,t₀} intact. Thus both deletions must occur in X, removing s₀ and t₀. X retains at least one label from each of P and Q. The correction therefore works and is the unique nearest exact parent endpoint even when every row is available for editing.

## A source bit changes the destination of every shortest nested repair

The original six-row preparation ends with leaf 14 or 15 holding label 4, depending on the extra incidence at row 0. Starting from these actual deficient terminal records, every shortest native repair must clear that leaf. Either 2 or 6 can fill it. A compact variant changes the initial crossing row to {0,3,4,7}, with the other five initial rows as in the earlier preparation. Both histories are checked with the unmodified historical producer and record verifier. Their complete starting states differ only by label 4 at row 0. Their deficient terminal states differ only by the placement of 0 and 4 in leaves 14 and 15.

In the compact example restoring rank three requires parent 13 to lose 4 and 7 at the nearest exact parent endpoint. The cover {4,5} hits every row through a label already held in its leaves, so some singleton leaf must also be emptied of its *old* label. That requires a gain and a withdrawal, giving an independent lower bound of four total primitive edits. In four moves the parent endpoint is forced, as is the leaf holding 4. The final parent is {0,3}. The sibling holds 0, forcing the payload 3. All four legal interleavings in each arm yield the same exact endpoint. A separate unrestricted breadth-first search found zero exact states at distances one through three. Of 254,645 new states at distance four, exactly one was exact in each arm. The repair routine obtains these results from the measured state, tree and target profile alone.

| Source bit | Initial compact receiver leaves | Forced repair | Final leaves |
| --- | --- | --- | --- |
| Absent | (4,0) at the deficient checkpoint | Leaf 14 gains 3 and releases 4 | (3,0) |
| Present | (0,4) at the deficient checkpoint | Leaf 15 gains 3 and releases 4 | (0,3) |

An eight-move exact repair in each arm edits a different row and leaves the receiver untouched. Independent full M9 runs to the corrected target produce the same terminal states as the compact four-move repairs. Those full runs do not visit the identical deficient checkpoint on the way there. The direct repair and the separate end-to-end executions are two distinct tests. The decision to form a complementary guard is still a proposed initiation rule. A common exact alternative target on the earlier fixture passes the same verifier in both arms and leaves the receiver with (0,2) in both.

## Sensitivity beyond the discovery fixture

Fix P = {0,2}, Q = {3,6}, S = {5,7}, T = {1,4}. Use starting rows P, P ∪ Q, Q, A, X, S. Vary A over T plus nonempty subsets of Q and S. Vary X over nonempty subsets of P and Q plus exactly one member of each of S and T. This defines 324 matched comparisons. Each has a second arm adding 4 to row 0. Each arm computes the preceding incidence-based proposal, receives the exact correction, passes the historical verifier, and ends at the full target profile.

The initial 36 comparisons used ordered row widths (|A|,|X|) in {(6,4),(6,6),(5,6)}. Fourteen had distinct ordered terminal receiver leaves. In those 36, the distinction occurred exactly when both of the receiver's starting leaf labels lay outside K. Applying the same criterion to the remaining 288 gave 112 predicted and observed distinctions and 176 predicted and observed equalities. These are exhaustive counts within one structured family. Every positive pair still had the same *unordered* terminal leaf set in both arms.

We also applied all fifteen other cyclic shifts and reflections of the palette to the first 36 comparisons and reran historical leaf initialization. Of 540 controls, 360 changed the source's initial leaves as well as its parent incidence and were excluded from the one-incidence comparison. All 180 remaining pairs passed verification and had equal terminal receiver tuples. The original-order classifier would have predicted delivery for 62 of them. The endpoint theorem is invariant under renaming. Transmission through the historical input-to-checkpoint schedule depends on the label order.

## Reproduction

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/exact_receiver.py ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity
```

The replay regenerates 1,024 entries, comprising 1,018 full stock-verified runs and six direct-repair or longer-control records. It compares each to the compressed archive. The uncompressed SHA-256 is `c962bd64c3b190adaeb7112b4cdfd9363a9b6190a5ea186754180f7158d7e9ab`. The compact witness was selected for interpretable leaf contents and an admitted route to its deficient state. Its uniqueness follows from the proof and the endpoint search. Frequencies above describe only their specified families.

[Complete records](exact_receiver_records.jsonl.xz) · [Repair search and controls](exact_receiver.py) · [Verification output](exact_receiver_results.txt) · [Archived shortest-write discovery](EXACT_REPAIR.md)
