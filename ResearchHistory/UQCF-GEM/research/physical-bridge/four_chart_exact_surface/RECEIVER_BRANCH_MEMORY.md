# A source withdrawal writes a label into a particular leaf, and the receiver uses the resulting state

In a prepared 53-site tree, the original v16.53 normalization routine generates a gain at a source and then withdraws one of two markers. It writes the replacement into the unique receiving branch and down to the particular leaf that held the withdrawn marker. The receiver subsequently edits its own records differently depending on whether the source had to gain the replacement or already held it. The two histories have identical sequences of distinct holdings at the receiver root. Their child records distinguish them until the receiver's next visit.

## What fixes the destination

The preparation supplies the tree, initial label holdings and an invocation of the original ordered normalization rule. The target profile is computed from the initial state. The caller supplies no event instruction, destination address or callback. Every candidate receiver has the same 13-site shape and the same initial root holdings. The distribution of labels below one candidate gives it width three. Its two peers have width one. Within the width-three receiver, one child has width three and two have width one. Here width is the minimum label count computed by the historical recursion.

As in the [preceding experiment](INITIATING_GAIN.md), a remote evidence leaf holds marker $m$ in $\{0,1\}$. Three upstream overlaps put the four labels into the order $(3,2,m,u)$, where $u=1-m$. The four-child junction plans a gain of 3 at the source followed by withdrawal of $u$. Its descendants still holding $u$ consist of the width-three receiver, its width-three child and a single leaf under that child. The writer adds 3 at those three sites, releases $u$ in reverse order, and completes the withdrawal at the source. Only the branch holding $u$ can require this replacement under the nesting rule. The other two candidate receivers have no incidence of 3 through this part of the run.

We compared the entire four-site state of the wide child immediately before delivery, retaining the names of its three leaves. In each of six matched states, switching the source withdrawal changed which named leaf gained 3. For example, suppose the named leaves hold 0, 1 and 2, respectively. Withdrawal of 1 puts 3 at the second leaf. Withdrawal of 0 puts 3 at the first. Matching this close to delivery required different earlier enumerations of the three leaves across the two histories. All twelve paths start from the same named holdings except for the remote evidence marker. The output of the actual clearance on this branch is computed by replacing $u$ with 3 at every site holding $u$. This formula is independent of leaf enumeration.

## What the receiver retains and does

The matched control switches only the initial source bit for label 3. The receiver starts identically. The comparison point can be found from its root alone. It is the first state at which the root holds 3 and exactly two other labels. The complete sequence of distinct root holdings agrees between the arms at fixed marker and order, including the later moves. The number of intervening edits elsewhere can differ.

| At this local comparison point | Source gains 3 during the run | Source already holds 3 |
| --- | --- | --- |
| Receiver root | $\{3,2,m\}$ | $\{3,2,m\}$ |
| Width-three child | $\{3,2,m\}$ | $\{3,2,m\}$ |
| Two width-one children, as an unordered pair | $\{2\},\{m\}$ | $\{3\},\{2\}$ |
| Children holding 3 | 1 | 2 |
| Receiver edits during its second recursive visit in the same run | 24 | 0 |
| Width-one child releasing $m$ on that visit | The unique child holding $m$ | None |

The first normalization of the receiver uses the priority $(2,m,u)$ when 3 is absent at the source. In the prefilled control the top three are $(3,2,m)$. In the historical assignment rule, a child of width three uses all three positions in a cycle. The other two children take the first and second positions, whatever their locations relative to the wide child. Clearance then replaces $u$ only where it is present. This yields the two rows of singleton holdings in the table.

The next recursive visit has the same local priority $(3,2,m)$ and the same target profile in both arms. In the generated-gain arm, one width-one child gains 3 and the other releases $m$. In the prefilled arm the receiver is already in its target state. The child holding $m$ had it before the source gain. The direct source write was the replacement of $u$ by 3 in the width-three branch. These are two distinct edits in the stored path.

## Interventions on the stored receiver

We replayed the original receiver routine with the wide child from one history and the two narrow children from either history. The receiver root, priority and target profile were identical. Every combined state passed the admission check.

| Wide child taken from | Narrow children taken from | Edits within wide child | Edits within narrow children |
| --- | --- | ---: | ---: |
| Generated gain | Generated gain | 8 | 16 |
| Generated gain | Prefilled | 8 | 0 |
| Prefilled | Generated gain | 0 | 16 |
| Prefilled | Prefilled | 0 | 0 |

We also froze each receiver at the second visit, preserved all 13 named site holdings and tried all six orders of its three child subtrees. The unique narrow child holding $m$ released it in every generated-gain replay. No narrow child released $m$ in any prefilled replay. With this deliberate change of order, a prefilled receiver can make other edits. The total edit count is therefore specific to uninterrupted runs. The marker withdrawal and its destination survive the order intervention. The three child records also retain their differing holdings from the local comparison point through entry to this visit. The resulting canonical endpoints coincide.

## Verification and scope

The main series covered 648 matched pairs, or 1,296 complete paths. It crossed both markers, all three placements of the wide receiver, all three placements of its wide child, and all six orders at each of the two wide nodes. The remaining sibling orders and the external label enumeration were sampled reproducibly. The four combinations of stored subtrees gave 2,592 local replays, and changing the order of frozen snapshots gave another 7,776. The historical verifier checked every path against its target and canonical endpoint, including the one-bit edit constraint. The 12 additional complete paths match the four-site state immediately before delivery. The example file includes the preparation, site map, raw clearance window, extracted second visit, mixed controls and named immediate priors.

This is a constructive result inside a specified finite dynamics. The distinction identifies the two preparations compared here. Its lifetime ends at canonicalization. The 53-site starting tree, the choice to invoke the normalizer and its ordered rule are inputs. Delivery of an original archived event receipt into its receiver, autonomous production of the starting network, and any connection to fractal scaling or spacetime curvature remain open questions.

[Historical producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Runnable experiment](receiver_branch_memory.py) · [Measured output](receiver_branch_memory.txt) · [Raw examples](receiver_branch_memory_trace.json)

From this directory, set DEMO to the v16.53-four-child-boundary directory at the linked historical revision. The imported preceding check validates its four source blobs before running.

```bash
set -euo pipefail
python -B receiver_branch_memory.py "$DEMO" | diff - receiver_branch_memory.txt
python -B receiver_branch_memory.py "$DEMO" --example | diff - receiver_branch_memory_trace.json
```
