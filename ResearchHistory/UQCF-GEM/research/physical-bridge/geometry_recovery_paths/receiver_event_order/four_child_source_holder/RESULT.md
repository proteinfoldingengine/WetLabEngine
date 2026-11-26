# A source withdrawal can leave only reversal or a write by one receiver

On a three-tip star with two charts, a specified ordinary withdrawal leaves exactly three possible single-tip network edits. One reverses the withdrawal. In both remaining edits the same other chart acquires a previously hidden numerical distinction in its own addressed P1 state. This classification uses the incident sets themselves. It requires no canonical endpoint, saved cover target, chart priority or tip priority. Idling and reversal remain possible.

The example was constructed after inspecting the eight contrary controls in the [earlier four-child experiment](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7178885480). The new evidence consists of a general classification, exhaustive comparisons on small stars and replays of the original operations. The three-tip example is a new preparation on the arity-three topology supported by the archived producer. The eight controls below are original four-child R campaign inputs. All numerical fine-grade assignments are supplied.

## A complete next-move classification

Let every chart contain the same Pin, with each tip held by at least one chart. Allow one chart to add a missing tip or withdraw a tip while preserving the union. Each addition is the inverse of an admissible withdrawal. Let source A withdraw a tip s that chart B also holds. Let H be a specified nonempty set of other tips absent from B.

**Theorem.** Every ensuing single-tip edit either exactly reverses the source event or adds to B a tip in H if and only if there are exactly two charts, B initially holds only s apart from the Pin, and H consists of all other tips. The union then forces A to hold all tips before the event. This is a statement about the set of possible next edits. It supplies no requirement to make an edit.

For sufficiency, immediately after A's withdrawal, B holds s alone and A holds every tip in H alone. All withdrawals would lose a tip. A can add only s, which reverses the event. B can add precisely the members of H.

For necessity, consider a third chart C. If C omits s, it may add s. If C holds s, it may withdraw s since B holds it. Either operation moves the atlas without editing B or reversing A's action. For two charts consider any other tip t already on B. If A also holds t, either chart can withdraw it. If A omits t, A can add it. Finally if t is absent from B but outside H, adding it to B is a further counterexample. These cases exhaust every tip. The bounded independent holder-set enumeration checked 71,082 eligible role and hidden-set choices over the chart/tip sizes in result.json, including all seven tested size pairs. The proof applies to arbitrary finite covered stars under the stated move relation.

## An addressed grade changes under either forward choice

On the two-chart star, give A tips 1,2,3 and B only tip 3. A withdraws tip 3. Give the Pin and tip 3 grade 1. Assign tips 1,2 grades (1,3) in one preparation and (3,1) in the other. B has addressed grades (Pin:5, tip 3:1) in both, before and immediately after the source edit. Which chart could acquire a hidden tip is now determined by the two incident sets. Exactly one chart is missing tips 1 and 2.

| Next edit | Receiver grades for hidden pair (1,3) | Receiver grades for hidden pair (3,1) |
|---|---|---|
| A adds tip 3 back | Pin 5, tip 3 grade 1 | Pin 5, tip 3 grade 1 |
| B adds tip 1 | Pin 4, tip 1 grade 1, tip 3 grade 1 | Pin 2, tip 1 grade 3, tip 3 grade 1 |
| B adds tip 2 | Pin 2, tip 2 grade 3, tip 3 grade 1 | Pin 4, tip 2 grade 1, tip 3 grade 1 |

The two sets of possible acquiring outputs are disjoint even if different branches are chosen in the two preparations. Choosing the same tip distinguishes its grade. Choosing different tips distinguishes their addresses. These are inherited P1 coordinates on genuinely enlarged retained views. A physical measurement or a persistent protected copy after further moves would need additional evidence.

Before A withdraws, B can instead give up tip 3 without acquiring either hidden grade. The source disables that option immediately. The unmodified arity-three caller was also executed on both preparations of incidence (source withdrawal versus no withdrawal), over six child priorities and both chart priorities. On the post-source state its first step acquires in eight of twelve orders, reverses in two, and its invocation ends without an edit in two. On the unmodified state its first step acquires in all twelve orders. The forward acquisition therefore identifies the hidden grade, while its occurrence alone does not identify whether the source acted. Counts here are orderings, with no probability model.

## The immediate effect on a full-cover jump

For a covered star let k count its charts and let the cover number be the fewest charts that jointly hold all tips. It equals k exactly when every chart has a private tip. A chart without one can be omitted from the full cover. A chart with a private tip must belong to every cover.

If one ordinary withdrawal raises the cover from k−1 to k, exactly one other chart gains its first private tip. Only the withdrawn tip can change holders, so its other holder must be unique and must previously have had no private tip. All remaining charts already had private tips. Among the other charts exactly one legal withdrawal command disappears, namely that new sole holder’s withdrawal of the same tip. Its mask and P1 stay fixed across the source edit. This consequence belongs to the global admissibility rule. Detecting its response locally would require a way for the chart to invoke or observe that rule.

The checker replayed all 12,564 legal withdrawals on the original 2,507 R rows and compared remote command catalogues on all 776 full-cover jumps (56 with two charts, 720 with three). Among the 72 previously published positive hidden-grade comparisons with a full-cover jump, the chart identified by this immediate effect was the eventual designated grade receiver in 52 and another chart in 20. In the eight deferred cases the split is six and two. The earlier [active-holder proof](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/research/physical-bridge/forced_parent_deletion/ACTIVE_HOLDER_WRITE.md) already used private tips to identify the receiver on a specific matched family. Here the boundary follows for any star on a jump to full cover, with an explicit comparison to later address acquisition.

## Why the eight archived repairs defer restoration

In **all eight**, the first sourced call to the original complementary-cover editor puts back the incidence removed by the source. The two histories thus meet at the exact pre-source atlas. From that state the *only* single-tip edit restoring cover 3 repeats the original source command and revisits the immediately preceding sourced state. The next sourced move instead adds a different incidence. The trace places both additions in the original loop that removes duplicate complementary memberships in child/chart order. The archival program first recovers cover 3 at its endpoint, after 12 or 14 edits counted from the source-prepared input.

That excursion is optional under the archived union, primitive-move, unit-excursion and canonical-endpoint conditions. An independent breadth-first search recovered all 132 three-chart four-tip states of cover 3 from the common sourced endpoint. In each of the eight cases it found a path to the identical **labeled** endpoint that keeps cover exactly 3 on every step. Four such shortest paths require four edits, four require eight. Each attains the Hamming lower bound because one primitive changes one membership bit. The predecessor search supplies one witness, without assigning its ordering physical meaning. All 52 remaining positive cover-3 comparisons with disjoint original paths also attain their Hamming bounds in the exact-cover graph.

For example, the pre-source masks are [11,5,21]. Chart 2 withdraws tip 2 and the atlas becomes [11,5,17]. The archived run adds tip 2 back on chart 2 and ends after 12 moves. A shortest alternative visits [11,5,17], [11,13,17], [3,13,17], [7,13,17], [7,9,17]. It exposes a hidden tip on chart 1 at the first move and has the same endpoint as the archive. A separate check one step beyond the common fork found two forward ways to recover cover 3, and the original program still deferred. Avoiding an immediate reversal alone does not recover its general scheduling rule.

## Child order and the four-child endpoint witness

We held all physical tip labels, chart labels, grades and the source fixed. We reran the original producer with each of the 24 child priorities by reindexing inputs and mapping each output back. The chart priority stayed fixed. Each comparison designates two initially hidden tips with identical holders. The counted effect is that the sourced endpoint contains at least one and the unmodified endpoint contains neither.

| Matched comparisons | Source alone exposes | Neither exposes | Both expose | Unmodified alone exposes |
|---:|---:|---:|---:|---:|
| 288 | 12 orders | 12 orders | 0 | 0 |
| 24 | 8 orders | 4 orders | 4 orders | 8 orders |

Every comparison was positive under the original ordering. In all 312, changing child priority can remove this particular sourced-only endpoint distinction. The two-chart theorem above asks a different question about **any immediate primitive change** in a specified preparation. Its receiver identity and disjoint addressed outputs follow under either choice of hidden tip.

## Reproduction and premises

Run `python3 -B check.py HISTORICAL_CHECKOUT --raw actual.json > summary.json` from this directory. The historical sources are pinned at `e61d5b0e827f7b412824ad46021e2ad6cc6f7875`. The neighboring four_child_retained_grade_fork directory supplies the reviewed positive comparison ledger. Compare summary.json to result.json and actual.json to the decompressed raw.json.xz. The raw archive records every full jump, every order-control comparison, both three-tip caller arms, and the eight path witnesses.

The inherited inputs are the fixed rooted incidence, original union-preserving withdrawal, its inverse as an allowed expansion, the extensive P1 projection, and the original ordered normalization caller for the replay tests. The star, grade swaps and source intervention are supplied. The complete next-move alternatives and immediate loss of admissibility are derived. What selects an occurrence, makes reversal or rest avoidable, or lets a physical receiver read the grade remains open.
