# One remote incidence chooses a receiving branch across every traversal order

Two preparations differ by adding label 1 at one remote evidence leaf. The original v16.53 routine routes a replacement into one of two candidate branches. Reversing the preparation reverses which branch acquires a new label. The caller passes the tree, initial holdings, a profile computed from those holdings and a label enumeration. It passes no active branch, source withdrawal, receiving site or later request.

In the four-leaf version, all **65 sites** at and below the central junction have identical labelled holdings in both runs at the point when its four child roots first become full. The remote leaf is outside those sites. The currently executing call retains a different label order derived from its ancestors. The distinction is present in the encompassing state even when every bit in the local junction agrees.

| Remote evidence leaf | Priority reaching the junction | Only branch receiving a replacement below its root during junction clearance | Receiver's next visit |
| --- | --- | --- | --- |
| {2} | (0,2,1) | The width-two fork in P gains 2 and releases 1 | Three other leaves gain 2 |
| {1,2} | (0,1,2) | The width-two fork in R gains 1 and releases 2 | Three other leaves gain 1 |

P and R are names for reading the trace. The branch selected for clearance is precisely the width-two branch whose compact holdings lack the incoming marker. The identity of that branch and of its width-two fork survives all reordering of siblings and of the external palette. Which physical tip of that fork is written first can change with traversal. The two whole-tree canonical endpoints agree for each matched pair.

## How the ordered routine makes an order-independent choice here

The three upper junctions each have one pair of children whose holdings intersect. The third child carries a label disjoint from both. In the inherited ternary routine, the first label of the intersection moves to the front of the continuing child's order. This promotion applies because the child's minimum width is less than the size of the available parent palette.

1. The outer junction has a singleton witness {1}. Every external enumeration promotes 1.
2. The next junction reads the evidence leaf. When it holds only 2, the overlap forces 2. When it holds 1 and 2, the preceding promotion gives 1 precedence. Write the resulting marker as $m$.
3. The third junction has a singleton witness {0}. It promotes 0. The central junction therefore receives $(0,m,u)$, where $u$ is the other marker.

The concrete orders result from the stored witnesses. The program still uses its inherited promotion and priority rules. Changing the outer witness to {2} makes the added bit silent. Giving it the tied witness {1,2} restores external-order dependence in three of the six relative marker/base orders.

The central junction has hitting number one. Its four child roots initially hold {0,1}, {0,2}, {0}, {0}. Each has three candidate forks of identical shape. In P and R, exactly one fork has width two, determined by its terminal holdings. The two remaining branches have width one everywhere. The historical minimum table at hitting number one assigns the first $w$ labels to each child of width $w$. These nested prefixes simultaneously attain minimum palette size, satisfy the shared-label condition and maximize each row in the historical incidence ordering. Permuting the four rows leaves the assignment to each width unchanged.

Both width-two rows consequently target {0,$m$}, and the narrow rows target {0}. On the first recursive pass the restriction to the labels already held in either wide branch is always (0,its original marker). Hence their compact proper states agree between preparations. Next all four roots expand to {0,1,2}. Exactly one wide branch has to release a marker still occupied below it. The only spare at that branch is $m$. The original clearance writes $m$ to the width-two receiver and its occupied tip, removes $u$ from those sites in reverse order, then removes $u$ from the source root. The other three branches have no proper descendant edits during this lift. They can change during other phases of the full call.

## The receiver uses the marker it acquired

We used four terminal leaves at each fork in a prepared, 74-site tree. The selected receiver initially has no incidence of the incoming label at any of its five sites. After clearance it has that label at its root and one tip. On the next recursive visit the receiver's own four-child routine expands its four leaf holdings. It writes the incoming label to the other three leaves, then contracts back to the stored state. No further instruction is issued to the enclosing computation.

The complete nine-state local path matches a fresh invocation using just the receiver's five stored sites, its held labels and its locally recomputed profile. Reordering a captured receiver's four leaves in all 24 ways and enumerating its two labels in both orders still produces those three gains before the all-full state. The later contraction can depend on order.

The passive width-two receiver already held the marker and can generate the same local path. Its trace and the active receiver's trace agree in local rank coordinates. The evidence of acquisition is the actual earlier write and absence of that physical label before delivery. Later reuse alone does not identify a unique past occurrence. The historical routine does not consume a separate event journal in this construction.

## How far the receiving address is determined

In the binary version we replaced every candidate fork with a complete binary tree. One exceptional terminal holding in each wide branch gives its bottom sibling pair hitting number two. Each internal ancestor above that pair has hitting number one, so its width is the maximum of its child widths. Induction gives precisely one chain of width-two nodes under that branch. At the end of the first pass only that chain and one terminal tip carry the old marker. Clearance therefore performs $2(d+1)$ proper edits for a receiver fork of depth $d$. It adds the replacement on occupied sites and removes the old marker in reverse order. This is a subtree scan in the original code. Tree topology and depth are prepared inputs.

The internal receiving chain is independent of sibling order. Swapping just the two children of its last fork exchanges the named tip written first. We checked all binary seed addresses through depth three and four further depth-four addresses. The whole trees range from 50 to 386 sites. This proves a routing property for the prepared recursive family. It supplies no growth rule or measured fractal dimension.

## Why a fixed receiver can forget at the canonical endpoint

For the historical canonical map, the first child of width $w$ always receives the first $w$ labels of its parent's palette, in that order. The two- and three-child rules give this directly from their prefix, disjoint-block and cyclic-block assignments. For four children the feasibility routine sorts incidence columns by membership in the first child before the other rows. All columns contributing to that first row are therefore an initial segment.

Consider two successful normalizations with the same topology and external root palette. Fix any proper receiver subtree with the same internal target profile in both. Place the child leading to that receiver first at every ancestor and use the same order within the receiver in both runs. Child widths never exceed parent widths. Successive prefixes therefore give the receiver the same first $w$ root labels in both runs. Its own fixed profile and child order then determine identical canonical holdings at every site beneath it. Thus, within this canonical map, a remote change alone cannot give a specified receiver distinct final records under **every** sibling ordering. This statement concerns the endpoint and permits different paths on the way there.

As a direct control we reran the [previous 53-site width-change experiment](FIXED_ORDER_DELIVERY.md). In its earlier layout the four-site receiver ended with masks (3,0,5,9) or (3,5,0,9). Placing the receiver first along its ancestral path made both endpoints (3,5,9,0). The local width rule was also checked in 846 cases across arities two through four.

## Verification and provenance

The binary series crosses every junction permutation with every relative order of the three active labels (144 matched pairs). A separate series covers all 216 combinations of upper scan orders. A direct priority check exhausts all 720 external palette permutations per arm. The four-leaf series crosses the 24 junction orders with the 24 receiving-fork orders (576 matched pairs), with additional frozen-receiver checks. Each complete program path is checked by the historical verifier for admission, one-bit edits, its profile-excursion bound and the canonical endpoint. The raw examples include site names, the shared local state, the actual plan, the delivery window and the later receiver path.

The [stock M5 pair reported on the agent thread](https://github.com/proteinfoldingengine/WetLabEngine/blob/5fb398cabe752e7341e2307f4d93436a033ce188/ResearchHistory/UQCF-GEM/research/physical-bridge/archived_stock_tail_pair/FINDING.md) gives two genuine archived parent histories with the same final parent operation and different leaf outputs under a supplied nested attachment. Here a single v16.53 invocation generates the source and the follow-on receiver action in one prepared tree. The new tests address temporary acquisition and use under reordering. A native origin for the tree, a separate receiver-owned historical receipt and a physical interpretation remain open.

[Historical producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.53-four-child-boundary/producer.py) · [Experiment](unordered_receiver_choice.py) · [Measured output](unordered_receiver_choice.txt) · [Raw examples](unordered_receiver_choice_trace.json) · [Endpoint check](receiver_terminal_prefix.py) · [Endpoint output](receiver_terminal_prefix.txt)

From this directory set DEMO to the v16.53-four-child-boundary directory at the linked historical revision.

```bash
set -euo pipefail
python -B unordered_receiver_choice.py "$DEMO" | diff - unordered_receiver_choice.txt
python -B unordered_receiver_choice.py "$DEMO" --example | diff - unordered_receiver_choice_trace.json
python -B receiver_terminal_prefix.py "$DEMO" | diff - receiver_terminal_prefix.txt
```
