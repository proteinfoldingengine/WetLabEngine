# A first write fixed by the tree, and a peer record that survives a change of order

**Original compact case 1728.** At the top of the v16.51 tree there is exactly one missing child incidence, label 1 at branch 9. The stock call adds it as its first edit. Its ordinary recursion carries 1 to every descendant of 9, including all four leaves. The same seven sites acquire the same label under all 768 orders of the labeled palette and siblings. The canonical endpoint already equals the original input under the historical order. The 16-edit path and the constant path both pass the original verifier.

**Matched peer experiment.** Using the same stock code on a constructed exact input, two genuine one-edit source prunes leave different surviving labels. After the source prune, its survivor alone determines which label a sibling fork and both its leaves retain at the end of the first pass. The receiver and all its leaves start identically in the two arms. All 288 remaining order choices per arm produce the same record for that arm. The original routine binds the shared label before it visits either participant. This experiment tests which information survives a change of order and when it can drive a fresh call.

## The original seven-site delivery

The compact certificate entry has tree U, k=2 and initial bit masks [65399,187]. Under identity order, the masks are already canonical. The immediate branch supports at nodes 1, 4 and 9 are {0,1}, {0,1} and {0}. The minimum number of labels needed to meet every one of these supports is one, witnessed by 0. This is the rank used by the historical normalizer. Within branch 9 every internal fork likewise has rank one, and every site initially holds only 0. In the checker the original verifier computes all ranks directly from the input before the ordinary normalizer is called. On the entire frozen certificate the recovered ranks equal the recorded ranks.

| Sites | First acquisition of label 1 in the original case |
|---|---|
| Branch root 9 | Edit 1 |
| Its children 10 and 13 | Edits 4 and 5 |
| Leaves 11 and 12 under 10 | Edits 6 and 7 |
| Leaves 14 and 15 under 13 | Edits 11 and 12 |

The ordinary rank-one rule first extends every immediate child to the full palette at its parent. The set of possible additions in that loop initially contains just one element, so the loop has a unique first edit. The recursive call at branch 9 then sees label 1 in its own root support. Each rank-one fork adds its entering palette to both children before descending. Induction along the tree gives every descendant the new label. Each acquisition comes after acquisition at its parent. In a wholly rank-one binary subtree the later width reduction can remove a label but supplies no further additions at a visited site. The receiver footprint and the set of descendants reached are calculated from the input tree without the canonical endpoint. The order of edits on different subtrees can vary.

As a direct input control, the actual binary subcall starts with masks [127,1] in its local coordinates. The six proper descendants initially lack the new label. The historical child routine from that input reproduces the projected segment of the unmodified archive. The same routine from [127], after withholding just the new root label and its now-empty palette column, emits zero edits. All six descendant priors and all three local ranks agree. This second subcall is a control.

The archive has 864 rank-one root cases, 57 with a single missing upper incidence, and 51 in which that incidence enters a nontrivial wholly rank-one subtree. All 51 complete paths passed the historical verifier and matched the certificate. Every descendant acquired the predicted label exactly once in each. In case 1728, we separately changed the actual tree traversal under all 6 top-level orders, all 64 lower sibling-order combinations and both palette orders. All 768 complete stock calls passed verification against their order-specific endpoints. All seven sites acquired the same physical label in every run. In 384 runs they all retained it at the global endpoint. In the other 384, including the archive order, none retained it there. The seven acquisitions take place at different frames. This calculation makes no assumption that all seven sites hold the label simultaneously.

## One uniquely legal prune switches a sibling's first pass

A separate constructed control uses the original three-binary-fork tree T and the same two labels. Its raw initial masks are [499,655]. The first fork S holds {0,1}, with both leaves holding only 1. The second fork R and both its leaves hold only 0. The last fork N holds {0,1}, with two singleton leaves carrying different labels. The whole tree admits exactly one same-union atomic pruning under the original v16.26 producer: delete label 0 at S. That label is dangling there. Every leaf has just one label, and every other nonroot holding has a descendant in that same view. The code enumerated every present incidence in both views against the original atomic routine, then verified the sole resulting record with its original independent checker.

The prune changes only source node 1. The root's local cover number rises from 1 to 2 because its children now include disjoint singletons {1} and {0}. The original trigger is true. The global maximum remains 2 because N already requires two labels. The receiver's entire prior is identical.

| Input to ordinary normalization | First pass at the same receiver R |
|---|---|
| Before the unique prune, masks [499,655] | The sole missing upper incidence is 1 at R. The first edit installs it there, and both leaves acquire it during R's ordinary visit. |
| After the unique prune, masks [497,655] | The measured root rank is 2. The upper expansion is skipped, and the receiving fork and its leaves keep only 0 through its entire first visit. |

All 96 combinations of sibling and palette order gave this paired contrast. On both arms the receiver's own rank is 1. The root ranks used on entry are the ones independently measured in the two inputs. Later transport can still write at R. This comparison runs the original atom and then starts a fresh original normalization. The atomic API takes an indexed site as an argument. Exhaustive admission gives exactly one valid argument pair on this state, so the harness has no choice among outcomes once a pruning is required. The normalization routine receives no receiver address or message label. The experiment still chooses whether to invoke pruning before normalization. The two original modules have not been shown to make that scheduling decision themselves.

## What survives a stock source prune

Take a ternary root over a source leaf S, a receiving binary fork R and a bystander leaf N. The root palette is {0,1,2,3}. Initially S holds {0,1}, R holds {0,1,2}, its two leaves each hold only 2 and N holds only 3. The raw start is [7,7,29,33] in preorder S,R,N. Both before and after either source prune the exact ranks, measured from incidence, are (2,1). Only S and R overlap. The stock rank-two procedure selects that pair. On the common initial state it takes the earlier of 0 and 1 as the anchor. Both are structural possibilities, related by the label symmetry of the entire input.

When the program visits S first, it keeps the chosen anchor there and deletes the other source label. This is the first primitive edit even if N was visited first. The only two resulting complete states in the original indexing are [7,5,29,33] and [5,7,29,33]. They differ exclusively at S. The stock runtime generates both states on the very same initial incidence under its supported orders.

After either prune there is exactly one triple consisting of an overlapping pair and a shared label. Its label is the singleton survivor y at S. The stock anchor selection must therefore return y for every root scan and palette priority. At R the original worker places the anchor first, since the branch width is one and the global palette size is four. The binary routine expands its leaves, then shrinks each to its first role. The upper routine shrinks R to the same singleton. At the end of the first pass **R and both its leaves hold exactly y**. This is an exclusive record. Both candidates can appear transiently while the leaves expand.

| Survivor at S before a fresh call | Initial leaves of R | Leaves of R after the first pass | Orders tested |
|---|---|---|---:|
| 0 | {2}, {2} | {0}, {0} | 288 |
| 1 | {2}, {2} | {1}, {1} | 288 |

All 576 post-prune runs change only the receiving subtree during the first pass. Each test ran the full original normalizer and verified its final endpoint. The 288 orders comprise six root traversals, two receiver leaf orders and 24 palette priorities. In the additional 288 runs from the symmetric common start, 144 visit S before R. They generate each post-prune state 72 times. Restarting on the resulting whole state with the original order reproduces the full suffix in every one. Changing order at this cut still preserves the first-pass receiver record. The other 144 runs finish the receiver's first pass while S still holds both candidates. This control locates the live common cause in the stock parent anchor. The actual unchanged execution does not wait for a prune notification. The first-pass record may be overwritten by the later parent transport.

## Scope and provenance

The first example removes order and an externally chosen endpoint from the mathematical prediction of a particular original first edit and its downstream footprint. The original normalizer is still an inherited update law acting on a supplied finite tree. The verified constant path from case 1728 shows that mere legality and endpoint agreement do not require that law to act. The second example gives an explicit class where a previously generated choice is available to a fresh stock call in ordinary incidence. That choice is still tied on the symmetric common state. These are incidence labels. The correspondence to a P1 grade or a separate campaign event receipt remains open. The observed branching comes from the input tree. No scaling dimension or curvature has been inferred.

The historical normalization producer, binary dependency, coverage helper, normalization verifier, atom producer, atom verifier and frozen certificate are pinned by SHA-256. The 51 archive cases are historical. The 768 alternative orders and the peer and unique-prune comparisons are controlled runs. The original certificate SHA-256 is `91aac71f6e786af4a3876ee9a7ec09d78b4bbe0906eb5461e08d9be1318b93f9`. Fresh deterministic production matched its Git blob `571d38f08006b7023a65ec64cac77fe23e0db52a`. The evidence stream contains 1,875 full paths with identifying orders and site maps, with uncompressed SHA-256 `86bfa0d9ca05d11a4a451865601a0660a151d243f1c80a36ee0d9dc553e71874`.

From the repository root run the command below with Python assertions enabled. It checks the evidence stream in order and prints the numerical receipt.

```sh
python ResearchHistory/UQCF-GEM/research/physical-bridge/archived_native_receiver_cycle/order_free_delivery.py \
  ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface
```

[Original producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/producer.py) · [Historical certificate](https://github.com/proteinfoldingengine/WetLabEngine/blob/76f373c8940433efc463762e675daf3e231f8cb5/ResearchHistory/UQCF-GEM/demos/v16.51-ternary-interface/evidence/science/scientific/CERTIFICATE.json.gz) · [Checker](order_free_delivery.py) · [Results](order_free_delivery_results.json) · [Full paths](order_free_delivery_paths.jsonl.xz) · [Preceding two-handoff result](PEER_EXCHANGE.md)
