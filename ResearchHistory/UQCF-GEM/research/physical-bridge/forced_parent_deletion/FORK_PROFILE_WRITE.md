# One stored cover decision directs a write after two fork states coincide

## Source and status

The verified v16.45 binary-fork normalizer computes a right-branch palette from the initial hitting profile. Its own output path records a change to an indexed receiver's retained tree. We isolate that dependence at an intermediate state where the competing histories have exactly the same memberships and the controller is about to normalize the same right-hand star. This gives a source-conditioned software write and an exact obstruction to predicting it from the current tree alone.

**INHERITED.** The v16.26 producer and verifier implement union-preserving deletion. The v16.45 graph stores a hitting profile for each indexed cover. Its producer calls the normalizer on one representative of each component at fixed profile and passes the component's profile. The independently implemented verifier checks each path and its endpoint. The scientific certificate and its reproduction have the same Git blob, `3ed66277766b9836804ed9ec222d9728009b2b67`. The original certificate contains the two representative trajectories used below.

**SUPPLIED.** For the paired source experiment we prepare one common tree and three fixed, ordered indices. We run one original source atom and then invoke the original normalizer on that post-source state's exact graph profile. Both inputs are legal graph members. The two experimental inputs are not among the representatives scheduled by the campaign. We compare their downstream paths directly to stored campaign rows. Actual triggering of normalization by a physical event and physical receiver access remain open.

## A matched source and receiver

Use seven vertices. Root 0 has left parent 1 with leaves 2,3 and right parent 4 with leaves 5,6. The mask of a view is the sum of 2 to the power of each retained vertex ID. Index A is the source, B the receiver and C the third holder, in that palette order. The initial masks are (31,15,113). A and B cover the left branch, A also retains the bare right parent, and C covers the right branch. B is the unique view with the left leaves and no right parent. The chosen right leaf 5 belongs only to C. Its entire vector of owners agrees across the two inputs to the normalizer.

| Source operation on A | Post-source masks | Root cover r | Left and right covers s,t |
| --- | --- | ---: | --- |
| Drop its bare right parent 4 | (15,15,113) | 2 | 1,1 |
| Drop its left leaf 2 | (27,15,113) | 1 | 1,1 |

Each is one accepted and verified deletion from the same preparation, with no edit to B or C. In the first case the owners of the two root children are disjoint. In the second case A still spans both children. The number of indices needed to cover the two children therefore changes from one to two only in the first case. This source operation never addresses either right leaf.

The normalizer gives the left star the first s palette positions. It gives the right star the first t positions if r=1, or the t positions beginning at s if r=2. Here s=t=1, so the designated right holder is A for r=1 and B for r=2. The routine prepares those palettes once from its input profile. One common preparation, both source edits, all other slots of the input profile, the controller implementation and the palette order are fixed in this comparison.

## Where the paths rejoin and separate

Both paths normalize the left star and make the right parent present in every view. Just before the local right-star calculation both reach **(31,17,113)**. A holds both left leaves and the bare right parent. B holds the root and the bare right parent. C holds the right subtree. The four preceding B edits, including their signs and addresses, have the same ordered masks in both histories. Starting with 15 they give 11, 3, 1 and 17. All earlier differences between the two source inputs have disappeared from the full indexed membership state. The initial right-palette assignment persists in the controller.

| Initial root cover | Next global edit from the common state | B's fifth own edit since normalization started | B's final right leaves |
| --- | --- | --- | --- |
| 2 | B adds leaf 5 | Adds leaf 5, mask 17 → 49 | 5 and 6 |
| 1 | A adds leaf 5 | Removes its empty right parent, mask 17 → 1 | Neither |

To see why this write occurs, at the common state only C holds the right leaves. In either arm the original star solver must choose its unique singleton cover, C. The solver then copies C's leaves to the first label of its reordered palette. That destination is the previously computed right holder. In the r=2 run the routine copies the two leaves into B, then drops C's extra copies. In the r=1 run A receives those leaves. B's empty right junction is then removed. The fifth B edit already distinguishes the branches at fixed address 5. The distinction persists to completion and every value above is a membership in B's own trajectory. No refused command, clock, geometry fit or shortest-path objective is used. The no-source comparison gives the same sequence of B masks as the left-leaf deletion.

## Two original campaign trajectories exhibit the same divergence

For the (2,2,3) campaign graph, representative IDs 0 and 6 have profiles (1,1,1) and (2,1,1) at the three internal vertices. Their initial states differ from our experimental inputs. At exactly the same zero-based positions 6 through 10, both actual campaign paths traverse the identical five full states with IDs 600, 595, 594, 1463 and 1488. The last is (31,17,113). The next state is 2657 in representative 0 and 1518 in representative 6. These masks are (63,17,113) and (31,49,113). Our respective post-source executions match both archived suffixes exactly from ID 1488 through their endpoints.

Thus a deterministic predictor of the next edit given only those last five full states and the position in the path cannot reproduce both historical rows. Its input is identical and the next edits differ. An exact controller needs at least two distinguishable internal conditions or equivalent external inputs at this point. The archived controller implements that distinction with the selected right palette. This lower bound counts two alternatives and makes no probabilistic or thermodynamic claim. Measuring the contemporaneous root cover at the meeting state gives 1 on both arms. Restarting normalization from that profile yields the same endpoint (127,1,1). The distinction belongs to what the controller retained from the source episode.

## Controls and scope

- **Previous binary-fork counterexample.** Starting from (127,127), removing site 2 or 3 from the first index leads the historical fork normalizer immediately to (115,127), with the same subsequent path and the same receiver. Both inputs have the same root cover and their first local cleanup removes the remaining redundant child. This reproduces Dot's control.
- **Palette ownership.** Across the six common orderings of the three prepared roles, sites 5 and 6 go to rank 0 for r=1 and rank 1 for r=2. The structurally identified B records different final bits in four of the six orderings. In the two cases where B has rank 2 it is silent at that address at both endpoints. At least one index other than A has a different bit in every ordering. The old rule fixes individual ownership from an ordered palette. Physical authority for that order is a separate premise.
- **Verification.** The checker imports the original two producers and independent verifiers, regenerates both (2,2,2) and (2,2,3) graph entries, compares their full data structures to the corresponding entries in the Git-pinned archived certificate and checks all matched paths. Other campaign graphs are outside this replay. The review input includes an extract with both historical rows and all matched source paths.
- **Research boundary.** We found an implemented carrier of the source distinction and a definite write on a joined historical path. This controller is an algorithm with its own stored choice. The caller that would make a native physical event start it, its physical carrier of memory, access to B's tree, and transfer to the 85-vertex deletion-only system remain unestablished.
