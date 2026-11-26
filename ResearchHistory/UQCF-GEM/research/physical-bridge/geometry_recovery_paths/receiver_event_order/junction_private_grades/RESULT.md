# When a private grade first appears in another chart

Consider the 36 indexed preparations of the [private binary split](../junction_reachability/RESULT.md). In the existing incidence model, preserving every chart's private terminal leaves confines the atlas to two states. Any path reaching a third distinct state must copy a private leaf into a different chart. In a single family of eight positive grade preparations, that copy makes a binary distinction held initially by the leaf's owner distinguishable in the recipient's own addressed P1. The entire pair-work matrix agrees across the preparations before the copy. Every one of the 36 untouched normalizer calls makes such a copy on its **first** edit. In 33 the first recipient can still distinguish that same source bit from its current P1 at return.

## The two possible states before the copy

The rooted tree has top-level singleton leaves X,Y, a ternary branch W, and a binary branch S. Each W leaf belongs to a different sole holder. Two charts each hold one S leaf. The remaining chart O alone holds X,Y and initially lacks S. Each chart holds the Pin, and the chart rows are ancestor-closed and jointly cover the tree. A primitive edit changes one incidence, either an ordinary union-preserving terminal deletion or its inverse. Every terminal leaf is singly held before the first copy. No chart can delete one. All charts must keep W to retain their W leaf. The two S-leaf owners must keep S. The only remaining interior incidence is O at S. It can toggle in either direction. Thus before the first leaf copy one can idle, alternate between these two states any number of times, or exit by acquiring someone else's leaf. This argument requires neither a priority nor an endpoint or cover budget. If immediate reversals are excluded and two edits occur, an acquisition occurs by the second edit.

| State before the exit | Legal private-leaf copies per start | Copies within the historical total unit band |
| --- | ---: | ---: |
| Original compact state | 12 | 12 |
| O also holds S bare | 14 | 6 |

At the compact state a non-owner can copy any W leaf or root singleton. Each binary owner can copy the opposite binary leaf. With O at S all fourteen non-owner/leaf pairs are available. The root cover has fallen from two to one. Copies that further reduce the W or S cover exceed the historical band. The four copies of X or Y and O's two binary-leaf copies remain in band. The two bare-S toggles themselves are both admissible in that band.

## What the receiving chart learns

Write t(v) for the total fine grade of the subtree at v. A chart's P1 entry at a retained v equals t(v) minus the subtree totals of its retained immediate children. Summing addressed P1 entries back up its retained subtree recovers t(v). This uses the original extensive-grade pushforward. The non-Pin pair work is the sum of t(v)² over addresses present in exactly one of the two charts.

Choose three binary contrasts independently. For O assign (1,2,3) or (2,3,1) to (X,Y,O's W leaf). For the left binary owner assign (4,5) or (5,4) to (its W leaf,left). For the right binary owner use (6,7) or (7,6) at the corresponding addresses. Fix t(Pin)=80, t(W)=30 and t(S)=24. Subtracting child totals gives positive integer fine grades everywhere. The ambient fine grades at internal addresses can compensate when leaves change. Source ownership here means that initially only the named chart's **retained record** distinguishes its bit. This experiment supplies the contrasts.

Each group of private leaves contributes a constant sum of squares across that owner's cut. All interior subtree totals are constant. Consequently the complete work matrix is identical across all eight worlds at each of the two pre-copy states. Flipping one bit leaves both peers' entire P1 records unchanged. All admissible incidence operations and all original program choices are independent of these grades. At any first exit, the actual recipient's new entry at the copied leaf equals its fine grade. At each address the two values for its original owner are distinct. Holding either of the other bits fixed or varying them does not change that fact. The donor keeps its copy. The statement compares two preparations along the same incidence history and uses no separate decoder or program-selected recipient in the geometric proof.

The bare-S acquisition supplies a numerical control even for arbitrary nonnegative fine grades on this preparation. Let L,R denote the two binary owners and d the three labeled pre-edit works. Then

    (d(O,L) + d(O,R) - d(L,R))/2 = t(X)² + t(Y)² + t(O's W leaf)² + t(S)².

O already retains the three leaves on the right. Given all three initial works, O's prior fixes the nonnegative t(S) by subtraction and a square root. An observer limited to O's P1 has not been supplied those three works. In the prepared family the extra S entry distinguishes none of the other charts' bits.

## What the work change identifies

At the first private copy, let s be the original sole holder, r the acquirer, h the remaining chart, and g the leaf grade. Work on (r,s) falls by g², work on (r,h) rises by g², and work on (s,h) stays fixed. For positive g the common endpoint of the falling and rising edges identifies the recipient. The other endpoint of the falling edge identifies the sender, and the magnitude gives g. A bare-S addition decreases both incident works and its reversal increases both. Within the specified frontier these signatures distinguish all three event types.

Geometry alone can lose the leaf address and the source bit. At I=(409,681,79), D holds W leaf 4 and binary leaf 8. B can copy 4 in one preparation or 8 with D's bit flipped, receiving grade 4 in both. In pair order (D,B),(D,C),(B,C) both work changes equal (−16,0,+16). B's retained addresses distinguish the two acquisitions. In the untouched original run at I, D instead acquires singleton X from C. With only C's bit flipped, D and B start with the same respective P1 in both worlds and the initial works are (126,631,675). D's new X is 1 or 2. The work changes are respectively (+1,−1,0) and (+4,−4,0).

## Actual occurrence and duration in the original code

The original v16.53 routine starts with a supplied invocation, chart priority, child order and cover target. The 36 presentations are distinct indexed inputs of one shape. Thirty first copies occur in W, three at the binary left leaf and three at X. If W's roles need reordering, the first misplaced W leaf goes to its target chart. If W is aligned and the binary holders are reversed, the earlier holder takes left. Otherwise root expansion copies X to the first other chart. This predicts the archived first edits for all 36. It accounts for first acquisitions even in the six earlier runs with no binary leaf edit.

All 36 runs return to (31,425,713). In three the first recipient has lost every leaf carrying that first source bit. Starting at the canonical state itself gives one example. B copies X on the first move, the run executes ten edits and returns to its exact starting state. The other 33 first recipients retain the copied leaf at return. Stopping at entry and repeatedly toggling bare S remain admissible controls outside the supplied caller. The initiation of a native process, operational access to the numerical records and a physical interpretation remain open.

## Reproduction

The [scope](SCOPE.md) and [signed-work control](WORK_TEST.md) precede the new runs. With historical checkout `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`, run `python3 -B check.py HISTORICAL_CHECKOUT --raw rows.json`, then `python3 -B verify.py rows.json`. The producer calls the original atomic and independent deletion check, P1 pushforward, work constructor, normalizer and path verifier. The second computation rebuilds all possible owners from seven terminal assignments, all one-bit neighbors from union and ancestry, cover profiles by subset cover, every signed number from symmetric differences, and the first ordered move from the three priority cases. It also rejects missing, duplicated, substituted and numerically corrupted records. The full ledger includes both silent directions, every in-band and out-of-band exit, all eight preparations and all original paths.
