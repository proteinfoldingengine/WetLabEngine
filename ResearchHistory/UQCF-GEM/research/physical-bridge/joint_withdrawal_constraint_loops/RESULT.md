# A source choice closes a loop of incompatible withdrawals among three untouched charts

Start two histories from the same state in the original v16.26 five-site campaign. Chart A makes one successful withdrawal in each. In one history the relations among B, C and D still form a path. In the other they form a triangle. All three untouched charts retain exactly the same holdings and exactly the same complete sets of individually possible future withdrawals in both histories. The source's local cover number, global height, trigger and height increment agree across the two releases. The graphs even have different numbers of edges after discarding all participant and site names.

## What an edge measures

Fix an initial state. A word at a chart is a finite ordered list of its own successful withdrawals in some legal continuation; other charts may interleave arbitrary successful moves. Two charts have an edge when each has an individually possible word but there is no continuation realizing both words together in their respective local orders. The graph is undirected and simple. For the source-choice comparison we examine the induced graph on the charts other than the common source. Repeated shared constraints between a pair count as one edge; the full joint-word counts below retain more detail.

**Edge criterion.** An edge is present precisely when some leaf of the covered union is held by exactly that pair. In that case each chart can release the leaf alone and both cannot release it together. Conversely freeze all exterior charts, and take any two individually possible words. With the two words interleaved, the local leaf checks hold since the charts have independent rows. The only possible failure is loss of the union. It is enough to check global leaves at the final endpoint: every earlier row contains its eventual row, and ancestry retains every ancestor of a covered leaf. Each singly held leaf is protected by individual feasibility. Every leaf having an exterior holder is still present. Thus a joint failure requires a global leaf originally held by exactly the two charts. This is an inference from original admissions and refusals, with no metric or chart-to-chart message supplied.

## A matched example at the smallest possible size

On the four-leaf star, the only holders of the four tips are as follows. The root belongs to everyone.

| Tip | Holders initially |
| --- | --- |
| 1 | A, B, C |
| 2 | A, C, D |
| 3 | B, C |
| 4 | B, D |

Initially B and C cannot both release tip 3. B and D cannot both release tip 4. C and D can jointly realize every pair of individually possible histories, since A still holds tip 2. All three remote pairs already share at least one tip in every preparation below; raw overlap is therefore the same complete triangle throughout.

| A's action | Edges among B, C, D | Shape | Jointly realizable C/D word pairs, out of 80 |
| --- | --- | --- | ---: |
| Before a release | BC, BD | Path | 80 |
| Release tip 1 | BC, BD | Path | 80 |
| Release tip 2 | BC, BD, CD | Triangle | 47 |

In the first arm BC acquires a second constraint at tip 1, reinforcing an existing edge. In the second arm tip 2 acquires just two holders, making CD a new edge. B, C and D each retain exactly their original individual possibilities in both arms. There is a precise sense in which an observer who only had those individual action histories would miss a change in the relations. The calculation establishes the relation without granting any local chart access to the graph. The original source receipt still identifies which leaf A released.

The original actor and both admissible cuts were found at the canonical historical starting rows with masks (7,15,21,27), where the chart order is A,C,D,B. The parent numbers for both cuts are at the root. Both have root cover 2 before and after, global height 2 before and after, false trigger and zero height increment. In the replay we enumerate all local words and all compatible pairs of words for all three remote pairs in all three states with the historical atom. All 24 chart permutations crossed with 24 tip permutations give the transported graph in all three cases. A and the underlying holdings are supplied; no receiver, edge, metric or next participant is specified by the source command.

**Minimum under the comparison tested.** A triangle among remote charts takes at least three of them plus the source. Only the newly two-holder leaf can add one remote edge per source cut. Closing a triangle therefore requires two of its edges present beforehand, which requires at least two distinct two-holder leaves. The matched alternative cuts require two more distinct three-holder leaves that include A. Hence at least four covered leaves and five covered vertices are necessary regardless of the number of additional charts. The example attains both bounds. This is a minimum for the stated matched-source test, not a claim about every possible definition of a graph on chart states.

## Census and scope

Across the full historical domain of 19,995 original source cuts, two independent implementations identify the same 1,172 unordered pairs of cuts at the same chart and same preparation satisfying the predeclared matching conditions. They agree on the identity and graphs of all 24 pairs in which exactly one release closes a triangle. These are indexed cases in a finite campaign, with no probability measure or claim of 24 inequivalent geometries. All occur at four charts and five vertices on the four-leaf star. The prospective construction was known analytically before the census and is explicitly disclosed in the scope. [Frozen comparison](SCOPE.md) · [Full qualifying cases and original-word counts](native.json) · [Independent mask verification](verification.json).

This is a change in the topology of compatibility among untouched participants. A triangle here consists of three pairwise incompatibilities. Neither a transported quantity nor a circuit of three executed events has been observed. The experiment uses supplied tree and holdings, so it demonstrates neither origin of the substrate, self-similar scaling, a receiver-side receipt, nor spacetime curvature. The [five-chart test](../joint_withdrawal_constraint/RESULT.md) separately verifies that a receiver can still be preempted. The geometric result adds an operationally defined relation that a future account of transport or scale could use.

Run with DEMOS pointing to the pinned historical demos directory at e61d5b0e827f7b412824ad46021e2ad6cc6f7875.

```bash
set -euo pipefail
python -B scan.py "$DEMOS" | cmp - native.json
python -B verify.py native.json | cmp - verification.json
```
