# A change at the fork identifies a lasting receiver record

Let the same source chart remove one of two equally graded tips. Allow either chart to make every subsequent legal deletion. In the seven-node example, the receiver's grade at the same surviving fork starts at 3. Every complete history ends with that grade either still at 3, or at **10 after the first source cut and 9 after the second**. The original deletion certificate reports a local cover increase precisely on the complete histories that change the receiver's fork grade. The receiver can keep the reading after the source is withheld from the measurement.

The historical v16.39 normalization routine gives a separate test of who actually acts. On the preceding six-node receiver-turn fixture its first edit restores the discarded source leaf before it edits the receiver. On a four-node mixed-depth tree the same routine produces receiver roots 3 and 11 at its first single-holder cleanup. This second outcome depends on chart order and on invocation of the connectivity routine. The two experiments use different allowed continuations.

## Unrestricted native pruning

Both charts S and R initially cover one finite rooted tree X with exactly two tips a and b. The unique branching vertex c is their least common ancestor. Its two descending arms, A and B, have m and n vertices respectively, excluding c and including the tips. The root-to-c path has d nonroot vertices. An extensive, positive fine grade g supplies their common starting numerical state. Write M_A and M_B for the sums of g over the respective arms. S takes the specified v16.26 source atom at a. Subsequent steps may remove any nonroot local tip from any chart provided the full family union stays fixed.

R is the last holder of a, so it always retains a and its entire ancestral path, including c. While b still has two holders, either S or R may delete b. R's full view permits no other deletion. S can trim the abandoned end of A without deciding b's owner. In a complete run someone must resolve b, since a duplicated global tip remains legally deletable.

* If S gives up b, R holds both unique tips. S may prune to the root. R keeps its full prior geometry and grade throughout.
* If R gives up b, S permanently keeps b and R permanently keeps a. Completeness now requires S to remove its remaining A vertices and R to remove all its B vertices. In either chart these removals proceed upwards within the arm. An internal tip left outside the path to the chart's owned global tip would still be deletable.

P1 on R is just nearest-retained-ancestor aggregation. Until R gives up the child of c on the B arm, that child holds any B mass removed from below it, and the value at c stays g(c). When R removes that child, c acquires the entire M_B and never changes again. Thus at **every prefix** its only possible readings are g(c) and g(c)+M_B. For the opposite source cut replace M_B with M_A. With unequal positive arm sums, a reading above the baseline identifies the source choice even on a run stopped immediately after that reading appears. With equal sums both changed readings coincide. The indexed leaf ownership still differs.

### What the actual geometric event establishes

Let the certificate's local cover number at c be the smallest number of charts required to cover the two immediate children of c. It starts at 1. During an unchanged-receiver history R covers both children throughout. During a split history S eventually loses c's A child, and R eventually loses c's B child. Whichever of those two removals finishes second changes the local cover from 1 to 2. The native `trigger` is true there because every previous one-chart cover is destroyed. The parent is c. There are no further active-subtree moves.

In a complete run the following statements are equivalent: R makes any deletion, R's grade at c changes, and the native local trigger occurs at c. The reading is available **by** that trigger. It can precede it strictly when R clears B before S finishes clearing A. A local trigger therefore certifies the write; it can be emitted by S after the write already occurred. At an incomplete prefix the presence of the trigger suffices, while its absence does not rule out an already changed reading.

For the named example the parents are (−1,0,1,1,3,2,4) and the fine grades are (5,3,4,1,4,2,2). The fork is node 1. Its A arm contains nodes 2,5 with total 6. Its B arm contains 3,4,6 with total 7. Both tip grades are 2.

| Source deletion | Fixed R fork before any continuation | At the local trigger and thereafter | Complete R-stationary alternative |
|---|---:|---:|---:|
| Tip 5 (A) | 3 | 10 | 3 |
| Tip 6 (B) | 3 | 9 | 3 |

The local record uses the receiver's own P1 updates. The scalar difference reflects the retained arm masses. Replacing the fine grade by (4,3,5,1,4,2,2) holds the total fixed and makes both arm sums 7. The trigger still reports a write, while both changed readings are 10. This control distinguishes detection of a changed record from identification of the source.

### Counting complete histories

After the source cuts a, the split endpoint requires m−1 source deletions along A and n receiver deletions along B. Each is a chain; their interleaving is free. The erasing endpoint has the same A and B chains, both performed by S, followed by the forced d-step deletion of the common stem at S. Relabel the B commands from R to S and append that stem to obtain a bijection; the reverse construction strips the stem and restores the B actor. Hence each endpoint has exactly

\[
H=\binom{m+n-1}{m-1}
\]

complete labeled histories. The split history uses L=m+n−1 post-source edits and the erasing history uses L+d. The earlier [terminal-ownership argument](../forced_parent_deletion/P1_TERMINAL_OWNERSHIP.md) already earned the shortest-versus-longest effect of a common stem. Here the endpoint counts, the P1 reading at a permanently held address and its relation to the native fork trigger are explicit. The live source and receiver labels are kept in all counts.

Attach a separate limb at the original root, above a different child from the active fork (so d≥1). Another chart covers the entire new chain. A fourth chart holds its t upper nodes and must delete them in descending depth order because the first chart permanently retains the final tip. These t edits can be interleaved anywhere without changing any active move. Subtract the added unit grades from the fine root to preserve both active numerical priors exactly. Each active word of length j now has \(\binom{j+t}{t}\) extensions. In the named cases the added limb keeps the global consistency order at 2 even before the active fork changes. The local trigger and the receiver readings survive while the global order increment vanishes.

| Independent forced deletions | Split / unchanged words after cutting tip 5 | Split / unchanged after cutting tip 6 | Fraction split under uniform complete-word counts |
|---:|---:|---:|---:|
| 0 | 4 / 4 | 6 / 6 | 1/2 |
| 1 | 20 / 24 | 30 / 36 | 5/11 |
| 2 | 60 / 84 | 90 / 126 | 5/12 |

Uniformly choosing an enabled deletion at each step is a different, explicitly supplied diagnostic. At every undecided state the two commands deleting b have equal selection chances, and every other move leaves both available. Backward induction on the finite remaining rank gives split probability 1/2 with or without the extra chain. The native rule licenses transitions. Neither probability weighting is specified by that rule. Raw counts alone would let unrelated activity change the apparent signal frequency.

## Test of an inherited caller

The archived v16.39 [campaign](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/campaign.py#L37) chooses endpoint representatives from stored profile pairs and passes them to [construct.build](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.39-theorem-validation/construct.py). We called that unchanged builder on the actual post-source views with their v16.33 profile, and on each of three common targets. The targets were both charts full, chart 0 alone full with chart 1 root-only, and the opposite. This is a direct execution on controlled inputs. A v16.26 cut by itself returns a certificate; an automatic call to the separate connectivity routine remains unestablished.

The starting profile is 1 at each internal node. The builder first fills missing descendants of occupied root-child blocks. For a deep source tip the parent block remains occupied at S. Exactly one addition restores that same tip at S, giving the full/full family before any receiver move. For a tip directly below the root, S no longer occupies that block and the expansion phase makes zero edits.

Next the builder's one-chart cover reduction keeps the first chart that covers every immediate root child. After a shallow cut only R qualifies. After a deep cut both charts qualify and chart 0 wins the tie. Cleanup removes all nonroot holdings from the other chart. The first returned state with a single holder at every root child is therefore determined by the preparation, source cut and chart order; the three targets have identical prefixes up to this state. The chart holding all blocks keeps its prior root grade. The chart pruned to root only has its total local grade there. All numerical receiver reads through this checkpoint use actual P1 composition on the receiver's own old grade. The builder itself carries incidence masks. It can subsequently use additions and returns the specified endpoint.

| Preparation | Source index | Source choices | R root at the first single-holder checkpoint |
|---|---:|---|---|
| Four nodes, one shallow tip and one deep tip | 0 | Shallow 2 / deep 3 | **3 / 11** |
| Same four nodes, reverse chart positions | 1 | Shallow 2 / deep 3 | 3 / 3 |
| Prior six-node receiver-turn tree, both tips deep | 0 | Tip 4 / tip 5 | 16 / 16 |
| Same six nodes, reverse chart positions | 1 | Tip 4 / tip 5 | 3 / 3 |
| Seven-node common-stem tree, both tips deep | 0 | Tip 5 / tip 6 | 21 / 21 |
| Same seven nodes, reverse chart positions | 1 | Tip 5 / tip 6 | 5 / 5 |

In the four-node example the parents are (−1,0,0,1), the initial grade is (3,4,2,2), and the source removes grade 2 in either arm. The receiver remains full after the shallow cut or is pruned to its root after the deep cut when S is chart 0. At the same final target the source distinction is gone. On the six- and seven-node deep/deep examples with S first, this builder does make R act in both arms, but only after it has undone the source event. Its execution consequently fails the test of forcing the earlier source-specific receiver record on those inputs.

## Exact scope and verification

| Bare two-tip census through six vertices | Count |
|---|---:|
| Topologically ordered parent arrays / labeled source comparisons | 42 / 84 |
| Post-source arms / reachable states / legal continuation edges, counted per arm | 168 / 1,620 / 1,988 |
| Complete ordered histories | 912 |
| Changed R fork grade and positive local trigger / unchanged and no trigger | 456 / 456 |
| Histories with the changed reading strictly before the trigger | 184 |
| Source comparisons with distinct changed readings / equal changed readings | 64 / 20 |
| Changed histories in the distinct-reading / equal-reading comparisons | 368 / 88 |
| Archived builder executions for the three targets on the census arms | 504 |
| Source comparisons distinguished at the builder checkpoint | 12 / 84 |

The full census stores every reachable state, labeled edge, grade at each retained receiver address, historical cover fields and complete command word. The producer verifies native moves with the v16.26 historical checker and compares each endpoint's order count with the v16.28 predecessor poset. v16.26 `factor` produces a witness for each supplied endpoint; the experiment retains that witness and both possible outcomes. An independent implementation rebuilds every graph from the two chains, exact interleavings and subtree grades. It also reconstructs every step of the v16.39 paths independently. The v16.39 historical checker validates all paths, and each deletion or inverse addition was checked with the native v16.26 atom. The four-, six- and seven-node named controls add 36 builder calls. The separate rejecting suites exercise eleven and five kinds of corruption.

The first local independent-checker invocation stopped before comparing results because cached subtree sums received a list. It was corrected to supply immutable tuples. The [original checker and traceback](fork_trigger_evidence/initial/) are retained. The native output for the full primary universe was unchanged.

**INHERITED** — prefix views, same-union deletion, P1 ancestral pushforward, local cover diagnostic, fixed-endpoint precedence and the specified normalization code. **SUPPLIED** — preparation and source intervention; completion for statements quantified over complete runs; separate invocation and targets for the caller experiment. **DERIVED** — stable readings, their equivalence with the fork event on complete runs, exact word counts, and the builder's conditional selection or erasure. **OPEN** — what prompts a source-sensitive operation in the physical model and how the relevant support is physically available. This stage establishes a finite information/geometry relation.

[Primary registration](FORK_TRIGGER_PLAN.md) · [Caller registration](FORK_TRIGGER_CALLER_PLAN.md) · [Native producer](check_fork_trigger.py) · [Independent reconstruction](verify_fork_trigger.py) · [Caller replay](check_fork_trigger_caller.py) · [Independent path comparison](verify_fork_trigger_caller.py)
