# A receiver selected by its internal holdings survives reordering

In this constructed family of exact inputs to the original v16.53 normalizer, a source site distinguishes label 0 from label 1. The algorithm writes the distinguished label to exactly one of three candidate subtrees during the local operation. Each candidate has exactly the same shape. The receiver is the one whose three leaves require three distinct labels to cover them. Moving this condition among A, B and C moves the write while all three candidate root supports stay fixed. Changing the source changes the actual label written at the same receiver.

The caller supplies the starting tree and holdings, the profile measured from those holdings, a global palette order and the normalization invocation. It supplies no receiver index, desired local label, local priority list or sequence of edits. The shared labels at the three upper junctions are part of the preparation. This is a new experiment using the original implementation.

## Where the choice comes from

The three upper junctions each have three children. Their sole intersecting child pair has a single common label. From the outermost junction inward those labels are x, 2 and 3. At the first junction the source leaf holds {x,11} with x either 0 or 1. The continuing child holds labels 0 through 9, and the third child holds 10. At the next junction the continuing child holds 0 through 8 and its two siblings hold 2 and 9 respectively. At the third the continuing child holds 0 through 7 and its siblings hold 3 and 8. Each junction has hitting number two. Restricting to the continuing child's holdings preserves the labels needed further down.

At each of these junctions the original algorithm moves its common label to the front of the continuing child's palette while preserving the relative order of the remaining labels. The child has width three, below its enclosing palette size, so this rule applies at all three steps. The resulting prefixes are (x), then (2,x), then (3,2,x). The global enumeration cannot put another label in one of these positions. The code finds the unique child pair from holdings, so permuting siblings cannot change the prefix either.

At their common parent, A, B and C start with root supports {2,3,4}, {4,5,6} and {2,6,7}. The overall intersection is empty and the hitting number is two. None of the candidate roots or leaves initially holds either 0 or 1. Each candidate has three leaves. In the selected candidate those leaves start with three distinct singletons from its own root support. In either other candidate all three leaves initially hold the same singleton. The exact subtree widths computed by the original recursion are consequently 3, 1 and 1 in the order determined by the holdings.

For these widths the local palette used for the assignment has length three. The stock assignment lays out consecutive blocks cyclically. The width-three block uses all three positions and leaves the pointer where it started. The two width-one blocks therefore use positions one and two in whichever order they occur. Only the width-three block contains the third label x. More generally, if a width w exceeds the sum u+v of the other two widths, positions u+v+1 through w belong exclusively to the wide branch for every ordering of the three blocks.

## The actual receiver edit

Local child normalization initially sees only labels already held in the respective subtrees. The two narrow candidates then each have one role, and transporting that role to its destination can use only one of the first two labels. Neither candidate needs a temporary spare for a one-role replacement. At the wide candidate an operation may require a spare. Before either marker has arrived, x precedes the alternate marker in the local palette, so x is always used first if a marker is required as a spare. The final wide assignment requires x. The replacement routine adds a label at the branch root before adding it below. Consequently the first appearance of either marker anywhere among the candidates is an actual gain of x at the wide root. Through the local return no competing subtree ever contains either marker, even transiently.

At return the wide root holds {2,3,x}, and one of its leaves holds x. The other two roots hold the singletons {2} and {3}. The particular leaf inside the wide branch can depend on ordering. The observer tests read the existing raw mask path. The code does not install an observer or give a physical participant access to that path.

## Matched runs and interventions

| Change | Observed result |
| --- | --- |
| Change only the source from {0,11} to {1,11} | The same candidate receives 1 in place of 0. All candidate priors and the measured profile agree. |
| Move the three distinct leaf supports from A to B or C | The destination follows the width. Only tip holdings change in the starting masks. The profile is recomputed from those holdings. |
| Vary the branch traversal and global palette | The calculated prefix, exclusive receiver, first marker write and local retained label agree with the derivation. |
| Keep the receiving subtree fixed and directly supply label 0 at ranks one, three and four | The default layout retains 0 at A and B, at A alone, and at no candidate, respectively. These isolated calls test what the upstream rank contributes. |
| Start instead with the source holding {0,1,11} | The entire common starting state is symmetric under exchanging 0 and 1. With both candidates available, reversing the global palette switches which one the program delivers. |

The common starting state has identical raw rows for labels 0 and 1. Either alternative source release is a single exact bit change leading to a main input. An unordered state invariant under exchanging the two labels cannot by itself specify just one of them equivariantly. The paired source releases are supplied interventions. The experiment establishes downstream selection for an existing source distinction.

We verified 543 matched pairs (1,086 complete paths) over 181 enumeration settings and three placements of the wide condition. This includes all individual permutations at each of the seven internal vertices with the others held fixed, the reversed palette, and all six candidate orders crossed with all 24 relative orders of labels 0,1,2,3 while varying other positions with a fixed seed. Separately, 4,320 isolated receiving calls checked every possible order of the five labels after the generated three-label prefix, crossed with both source values, all six candidate orders and all three wide placements, holding tip order fixed. Each checked the first gain, exclusion from both narrow subtrees throughout, and the wide root at return. The ordering statement for the local assignment follows from the prefix and block arguments above. Every whole path passed the independent historical admission and endpoint checker. The source distinction was lost at the final canonical endpoint in every matched pair. Within the local operation it was visible at the receiver from its first marker gain onward as a first-event observation, and in its stored holdings at the local return.

[Original writer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Executable and pinned dependencies](structural_receiver.py) · [Recorded results](structural_receiver.txt) · [Raw matched masks through local return and full-path digests](structural_receiver_trace.json) · [Earlier ordering control](GENERATED_OVERLAP.md)

```bash
set -euo pipefail
python -B structural_receiver.py "$DEMOS/v16.53-four-child-boundary" | diff - structural_receiver.txt
python -B structural_receiver.py "$DEMOS/v16.53-four-child-boundary" --trace | diff - structural_receiver_trace.json
```
