# One remote bit changes which receiving leaf is written under a fixed traversal

The v16.53 normalizer takes the same ordered 53-site tree and the same default label priority in two runs. A single additional incidence at a distant leaf changes the withdrawal that the program generates at a different branch. It then writes the replacement into a different named leaf of the same receiver. The source and its twelve descendants have identical stored histories, with consecutive repeats suppressed, up to the first receiver write. Every bit at all thirteen sites agrees immediately before that write. The receiver's own root still distinguishes the two runs at termination.

This resolves the traversal qualification in the [previous matched-prior experiment](RECEIVER_BRANCH_MEMORY.md). The construction is a new preparation executed by the historical producer. The caller supplies the initial holdings and invokes the inherited rule. The runner computes the target profile from those holdings and passes it to the producer. It supplies no withdrawal, replacement, receiver address or target table.

## How the bit reaches the receiver

The junction has four children. Each child contains three equally shaped forks, and each fork has three leaves. In the source branch S, the three candidate receiver roots all initially hold labels 0, 1 and 2. At one fork, W, the three leaves hold distinct singleton labels. At the other two forks, all leaves hold 0. The resulting minimum widths are 3, 1 and 1. Three other junction children have the same topology.

In a separate branch L, three sibling leaves initially hold the singleton labels 0, 1 and 3. Adding label 1 to the last leaf makes its holdings {1,3}. Before the addition a set of labels meeting all three leaves needs three members. Afterward {0,1} suffices and a singleton cannot suffice. This changes exactly one entry in the computed profile. The minimum width of L consequently falls from three to two. The arrangement and holdings in S are identical between the runs.

In the displayed configuration S is the third junction child and L is fourth. Under the same label order (0,1,2,3) the inherited positional rule computes the following target for S.

| Remote leaf initially | Four child widths | Target at S | Source withdrawal | First receiving leaf gaining 3 | Later edits inside W | W root at termination |
| --- | --- | --- | --- | --- | ---: | --- |
| {3} | (3,3,3,3) | {0,2,3} | 1 | A1, which held 1 | 4 | {0,2,3} |
| {1,3} | (3,3,3,2) | {0,1,3} | 2 | A2, which held 2 | 0 | {0,1,3} |

A1 and A2 are persistent site names in the default example. Both runs first add the unique missing label 3 at S. The target determines which remaining label S will withdraw. At the common pre-write state the withdrawn label occurs below S only at W and at the one leaf of W holding it. Label 3 is the sole spare at S. The original clearance adds 3 to W and that leaf, removes the withdrawn label from the leaf and W, then releases it at S. The recorded moves establish the destination directly. No decoding of aggregate counts is involved.

The later visit reorders two leaf holdings in the first arm and makes zero edits in the second. In the default example both eventually place 3 at A2. The identity of the surviving marker, 2 or 1, is the lasting distinction. Extracting W's final four sites and invoking the stock routine with only its held labels and its locally recomputed profile returns that same receiver state with zero edits in both arms. This measures retention through termination and one isolated local replay. The two whole-tree endpoints correspond to different remote profiles.

## What selects the source target

We independently enumerated all labelled four-child target tables with the required row widths, four available labels and exact hitting number two. Four is the minimum label count for both width tuples. With three available labels, each width-three child would use all labels and at least one label would meet every child.

| Widths | Admissible tables | Row at S in the historical preferred table |
| --- | ---: | --- |
| (3,3,3,3) | 24 | {0,2,3} |
| (3,3,3,2) | 108 | {0,1,3} |

All four possible three-label rows at S occur in both admissible families. The historical rule compares the incidence tables in positional order, preferring a present incidence at the first difference. Independent enumeration gives the same chosen tables as the producer. Feasibility permits multiple source withdrawals. The supplied law selects one, and occupancy then fixes the receiving leaf.

Two controls test the role of width. Placing the same added label 1 at a width-one fork in L preserves the profile and reproduces the baseline source and receiver outcome. Adding label 0 instead of 1 to the original remote leaf also reduces the width and reproduces the changed outcome. Across both controls the matched source histories, subsequent local paths and corresponding full endpoints agree.

## A comparison with the complete profile held fixed

A separate 56-site preparation puts one ternary junction above the same four-child structure. One external singleton leaf holds 0 or 3. The original overlap rule derives an internal priority of (0,1,2,3) or (3,0,1,2). Restricted to the three labels S holds before its gain, both induce (0,1,2). Thus the two source subtrees again reach the identical full immediate prior under a fixed traversal. S withdraws 2 or 1 and W writes to different leaves. The externally supplied order, full profile and complete canonical endpoint agree in this comparison. Its receiver distinction is temporary. For a fixed ordered tree the canonical endpoint depends on the profile and the external label order. The remote profile change in the 53-site result allows its two endpoints to differ.

A contemporaneous [M5 nested-carrier test](https://github.com/proteinfoldingengine/WetLabEngine/blob/ed09044700fa0d59f366f3a4633d480051ad6fed/ResearchHistory/UQCF-GEM/research/physical-bridge/archived_nested_balance_followup/FINDING.md) held the complete initial parent input fixed, intervened on the first source choice and later applied a common supplied probe. Its leaf distinction survived agreement of the complete parent output. Here the two initial states differ at a remote leaf, and the original v16.53 routine generates both source withdrawals and their follow-on receiver calls. A common-parent endpoint with that combined property remains open.

## Verification and limits

Each series tests 216 matched pairs. It varies the placement of the width-three receiver among three candidates, all six traversal orders at S and W, and the order of two other junction branches. The remaining subtree orders use a fixed random seed and stay identical within a pair. Each of the 18 ordered pairs of different named leaves of one receiver occurs twelve times in each series. The 53-site series has 864 verified whole paths including its controls. The 56-site series has 432. A read-only observer maps the original recursive receiver call back to the whole path and checks every returned local state against the corresponding stored bits.

An additional 48 complete runs test the remote width change in all 24 junction orders with the site names and starting holdings fixed. S writes to different leaves in both arms for **2 of the 24 orders**. In six other orders an active withdrawal becomes a withdrawal of the unused spare, leaving its descendants untouched. In the remaining sixteen orders the withdrawn label at S is the same. Looking at all three unperturbed branches, **13 of the 24 orders** give at least one branch with different active withdrawals in the two arms. The code checks the actual descendant edits against their occupied sites.

The historical verifier checks admission, one-bit steps, the bound on deviations from each profile, and the canonical endpoint. This is an executed interaction and retained distinction in an ordered finite model. The experiment takes the tree and normalization law as inputs. It does not derive an unordered selection law, a starting network, historical campaign receipt provenance or a spacetime observable.

[Historical producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Runnable verification](fixed_order_delivery.py) · [Output](fixed_order_delivery.txt) · [Raw examples, site maps and placement census](fixed_order_delivery_trace.json)

From this directory, set DEMO to the linked revision's v16.53-four-child-boundary directory. The inherited input check verifies the four pinned source blobs.

```bash
set -euo pipefail
python -B fixed_order_delivery.py "$DEMO" | diff - fixed_order_delivery.txt
python -B fixed_order_delivery.py "$DEMO" --example | diff - fixed_order_delivery_trace.json
```
