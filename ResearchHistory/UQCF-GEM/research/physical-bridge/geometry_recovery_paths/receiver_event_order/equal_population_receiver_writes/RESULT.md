# Four source withdrawals can reach a remote chart despite identical pair measurements at the endpoints

Start twice from exactly the original 121-chart, 968-leaf orbit. Only chart 0 acts. It withdraws four of its leaves in each history. After the fourth withdrawal every one of the 7,260 pair-work values agrees between histories, and all 120 other charts still have their original addressed records. When the existing v16.43 star normalizer is run on a specified cover of 11 charts containing every original leaf, chart 15 acquires the same previously absent leaf in both histories. Its own retained count at that gain is 130 or 129. Its own P1 Pin grade is 1,677 or 1,679. Both normalizations finish with the same addressed state.

Four withdrawals per history are necessary and sufficient in this fixture to conceal a difference in the **types of leaf supports withdrawn** from pair work when only one chart withdraws. The bound identifies two leaves with exactly the same original holder set as copies of the same type. An addressed swap of such twins can be invisible to pair work after just one withdrawal.

## A common starting point and an exact minimum

Chart 0 initially holds 200 grade-2 leaves, comprising two copies of each of 100 support types. Each leaf has 25 initial holders. At any other chart j write c_j for the number of the k removed leaves it holds. Upon these withdrawals, the change in work from 0 to j is 4(2c_j−k). Other pairs are untouched. Sum the change divided by four over the 120 other charts. Each removed leaf had 24 other holders, so the sum is −72k. Thus equal endpoint work between histories forces k to agree, and then forces every c_j to agree.

Let M be the 121-by-100 membership matrix of the source-held types. Its row at chart 0 counts all removed leaves. Pair-work equivalence is exactly M d=0, where d is the difference of the two removed multiplicity vectors. Each entry is an integer between −2 and 2. Conversely every such null vector is the difference of two legal removal vectors: withdraw its positive entries in one world and its negative entries in the other. All original leaves have other holders throughout. A common removal cancels. A nonzero vector records a true difference of support types with chart addresses fixed.

The independent coordinate reconstruction gives exact rational rank 92. Its eight-dimensional rational nullspace basis has integer entries and free-coordinate identity rows. Enumerating the 5⁸ possible values of those free coordinates and imposing the 100 component bounds leaves 13,471 vectors including zero. The smallest nonzero positive-part sum is four. Exactly eight directed vectors attain it, four reversals paired. These are difference vectors at the fixed source, not numbers of named histories. Translations of the original atlas give the same bound at every source. The two obvious orientation redistributions anticipated before the run span only part of the kernel.

A second check of the lower bound dispenses with rank and nullspaces. For each removable support multiset of size one, two or three, encode its chart counts as base-four digits. There are no carries. The 100, 5,050 and 171,600 possible type multisets respectively give that many distinct signatures. Triple repetition of a type is excluded because only two copies exist. This directly rules out a smaller collision between different support multisets.

## The two histories

| Quantity | History A | History B |
| --- | --- | --- |
| Chart 0 withdraws these original leaf addresses in order | 41, 217, 278, 454 | 91, 157, 338, 404 |
| Chart 0's final leaf count | 196 | 196 |
| Pairwise shared leaves at (0,15), (15,117), (0,117) | 39, 48, 39 | 39, 48, 39 |
| Leaves shared by all three | 16 | 15 |

Measured between these two histories after their respective first, second, third and fourth withdrawals, the numbers of differing pair-work entries are 38, 68, 38 and 0. The common endpoint work differs from the initial work at 116 pairs. A continuous observer of intermediate pair work could therefore tell the histories apart. The endpoints have four 24-holder leaves and 964 25-holder leaves in each arm, with the identities of the four depending on the history. This uses the original equal-population starting state and ordinary withdrawals. It does not impose population 25 on the endpoints.

## What the writer actually does

Use the complete line y=3x mod 11 in the archived x+11y numbering. Its 11 charts jointly retain all 968 named leaves and the grade-1 Pin. This is a supplied set of active charts. We pass their actual original records, with the entire ambient star, to the historical routines. We do not invoke the writer on all 121 charts. Each selected chart has at least 24 private witnesses relative to this cover in both source endpoints; removing any selected chart would uncover a leaf. Its exact minimum cover size is therefore 11 in both. An exploratory full-atlas search found an 11-chart upper bound but did not certify an optimum for 121 charts. No full-atlas writer output is inferred.

Each of the eight actual v16.26 atomic calls on the selected cover preserves the union and gives (tau before, tau after, h before, h after, delta h, trigger)=(11,11,11,11,0,false). Each same incidence withdrawal is legal on the full atlas because 24 other charts retain that leaf. The expensive global cover statistic was evaluated on the selected cover only. The source and its four ordered edits, the cover, the invocation and priorities are supplied. Neither routine chooses them from the initial atlas.

Use the ordinary leaf-address order, with chart priority 0,117,15 and then the other selected charts in increasing order. During the original contraction a leaf stays with its earliest holder. Chart 15 retains exactly its original leaves absent from both earlier charts. Inclusion-exclusion gives 200−39−48+16=129 or 200−39−48+15=128. At the start of recoloring the first three anchor leaves are all held by chart 0. Anchor 1 stays at 0, anchor 2 goes to 117, and anchor 3 goes to 15. Thus the next gain at 15 is a copy of leaf 3 in both histories. The chart lacked it in its common prior. After the gain the retained counts are 130 and 129. The P1 push on the unmodified full ambient grades gives Pin=1+2(968−count). The two values occur on the same global edit index 1,231. A receiver needs only its own first gain to locate the comparison. At termination it holds just one leaf in both arms.

With the source last in the selected chart priority, every non-source chart has **the same entire sequence of addressed local records** across arms, after ignoring idle global steps. For every commonly retained leaf the two source memberships agree; every leaf treated differently between arms has a surviving non-source holder in both. The first winner is therefore identical in both worlds under any such common chart priority. Each non-source chart starts identically and loses exactly the same nonwinning addresses in any common leaf order. At the all-singleton stage the whole state has coalesced, and subsequent deterministic operations agree. One full pair of blind traces is checked directly. Supplied ordering can expose or erase the distinction even though the source really acted and receiver writes really occurred.

## The reflected preparations from #168

We also replayed the actual writer on the former static pair with fixed complete prior at chart 0. On the same line and leaf order, use chart priority 15,30,49,0 and then increasing remaining charts. The first newly acquired leaf at chart 0 is the same address 4. The retained counts are 101 and 100, giving Pin 1,735 and 1,737. These two states were separately prepared. The single-source withdrawal histories above establish the stronger common-start comparison. Both evaluations of the normalizer extend beyond its original small finite campaign; they are new direct calls to its unchanged implementation.

## Reproduce

Use Python 3.11 with NumPy 1.26.4 and SymPy 1.13.3. From this directory run the commands below. ORBIT is the sibling orbit_exchange/probe.py. DEMOS is ResearchHistory/UQCF-GEM/demos at e61d5b0e827f7b412824ad46021e2ad6cc6f7875. The replay verifies the five input Git blob identities, both complete parent work tables, every full writer path's one-incidence changes and cover preservation, the receiver's original P1 output, and the measured control.

```bash
python replay.py "$ORBIT" "$DEMOS/v16.23-overlap-descent/engine.py" \
  "$DEMOS/v16.26-consistency-increment-law/engine.py" \
  "$DEMOS/v16.43-star-fiber-classification/producer.py" \
  "$DEMOS/v16.43-star-fiber-classification/graph_producer.py" | cmp - results.json
python verify.py | cmp - verification.json
```

The second program rebuilds the atlas from 25 explicit coordinates and calculates the initial contractions and first gains using sets. It also independently certifies the minimum. The observation is a transient difference in a local extensive-grade record under an already defined writer. The model still needs an intrinsic reason to select the source actions, active cover and invocation. No physical identification is established.
