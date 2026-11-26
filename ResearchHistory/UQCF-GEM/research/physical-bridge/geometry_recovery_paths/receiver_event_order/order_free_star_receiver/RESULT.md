# A receiver's first gain can distinguish the source event without knowing the chart priority

For the original v16.43 star normalizer with more leaves than its minimum cover size, a chart's **first gain of a leaf**, whenever it occurs, reveals whether the chart belonged to the initially chosen minimum cover. A first gain leaving exactly one leaf means the chart was outside that cover. A first gain leaving at least two means it belonged. This is an actual local transition during ordinary normalization. The chart can use its own retained count immediately after the gain. No phase label, remote clock, target address or reconstruction of a cover is needed for this implication.

We found a five-chart preparation where two withdrawals by the same source place the same structurally identifiable receiver inside every minimum cover in one arm and outside every minimum cover in the other. Thus the values at a first gain identify the source alternative even under unrelated chart and leaf orders. Occurrence is conditional. There are orders for which that receiver sees identical complete local histories. The contraction is a supplied invocation of a real historical algorithm; the model here does not decide to start it after a withdrawal.

## Proof for the existing algorithm

Let H be the minimum hitting set selected by the existing routine, K the first q chart labels in its supplied order, and m the number of leaves, with m>q. A cover hits every leaf. Every member of a minimum cover has at least one private witness relative to that cover: otherwise that member can be removed. Contraction deletes a leaf from every holder except its earliest holder in H. A chart in H retains at least one private witness throughout. A chart outside H becomes empty, and no chart acquires during this phase.

During palette replacement each member of H outside K transfers all its surviving leaves to a distinct member of K outside H, by adding the new holder first and deleting the old holder second. Charts in H intersect K keep at least one leaf. Charts outside K receive no leaves in replacement or final recoloring. Each new member of K receives its first leaf from an empty state. The final m>q branch maintains a surjective coloring onto K: before a sole old color is recolored it creates a spare witness, and all nonanchor recolors have a surviving anchor. Copy-before-delete preserves nonemptiness during those moves. Therefore any first gain at a chart in H occurs from a nonempty state; any first gain at a chart outside H occurs from empty. With one incidence per primitive the claimed local counts follow. The proof imposes no physical probability distribution over orders and uses no supplied readout to decide the primitive.

At the first all-singleton state the set of nonempty charts is exactly H. Conversely any chosen optimum can rank first by putting its members before the other charts. Hence a chart is nonempty for every chart order precisely when every minimum cover contains it, and empty for every order precisely when none contains it. These facts hold separately for both source cuts. A first gain provides a receiver-local alternative to observing that global phase boundary.

## Input and roles on an unlabelled preparation

Here A is the source, B the tested receiver, X and Y are interchangeable charts, and D is the remaining chart. The Pin is common to all charts, with grade 1; each of the five leaves has grade 2. The five original holder sets, in the file's leaf order, are:

| Leaf | Holders |
| --- | --- |
| 1 | A, X |
| 2 | A, Y |
| 3 | X, Y, B |
| 4 | A, X, Y, D |
| 5 | A, B, D |

A is the sole chart with four leaves. B and D each hold two; B is the degree-two chart holding the unique leaf absent at A. These descriptions survive all chart and leaf renamings. The two candidate source leaves have different holder-set sizes. The source, receiver and comparison are distinguishable even after forgetting names. This property does not initiate either event.

Initially the minimum covers are AX, AY and AB. This can be checked directly: A plus one holder of leaf 3 covers everything. Avoiding A forces X and Y to cover leaves 1 and 2, and that pair misses leaf 5. After A withdraws from leaf 5 the only minimum cover is AB. After A withdraws from leaf 4 they are AX and AY. Withdrawals can only remove covers at a fixed size. B is the only remote chart compulsory in one arm and excluded in the other. No leaf ever has fewer than two holders **immediately after either cut**. The unchanged v16.26 atomic call accepts both and reports q=h=2 before and after, delta zero and trigger false in both. B still holds leaves 3 and 5 immediately after both withdrawals. Geometry and all priors start identical; the two post-cut work matrices need not agree.

In the AB arm, B alone among the two selected charts holds leaves 3 and 5 after the cut. It keeps both throughout contraction. In the other arm B loses both. In the equal-grade v16.23 marginal the chart's Pin grade is 11 minus twice its number of held leaves. The contraction-boundary records are therefore two leaves and Pin 7 versus zero and Pin 11. The two arms finish contraction after eight primitive deletions. The conditional first-gain test is stronger because it does not need that shared index.

## Original full traces and common gains

Direct calls to v16.43 and v16.23 cover every one of the 5! chart orders times 5! leaf orders, with the same physical actors and addresses held fixed in each paired trial. The common prior includes both receiver leaf identities and all its local grades. The complete terminal state agrees at each common priority. Counts below enumerate orders, not likelihoods.

| First gain during the full routine | Orders |
| --- | ---: |
| Both source arms | 4,608 |
| Only after the withdrawal from leaf 4 | 1,152 |
| Only after the withdrawal from leaf 5 | 0 |
| Neither | 8,640 |

In all 4,608 gains after the leaf-5 withdrawal B holds either two (1,152 cases) or three leaves (3,456 cases), with Pin 7 or 5. After the leaf-4 withdrawal all 5,760 first gains leave one leaf and Pin 9. In 1,248 common-gain trials **the very same address is gained first in both arms, and B lacked it initially**. The source distinction survives matching both the kind of receiver edit and its newly acquired address. All incoming grades in this experiment equal two. The distinguishing information is in the rest of B's own retained state. The trace file gives a common example in which leaf 4 is the first gained address of both arms and the respective counts are three and one.

In the 8,640 no-gain pairs the entire addressed receiver-only histories agree when consecutive idle repetitions are removed. The identity orders give an example: B loses leaf 3 then leaf 5, with Pin 7, 9, 11 in both arms. The losses occur at different global indices; those are unavailable to the receiver. A common receiver-edit landmark during contraction is impossible in this fixture because the survival arm has no B deletions then. The first-gain result uses the full historical routine. A silent record cannot generally identify the source.

There is a general collision construction when m>q and B is compulsory in one cut and excluded in the other at the same q. Then q<k. Put B last, hence outside K in both arms. The erasure arm removes all B's prior leaves in their order during contraction. In the survival arm B deletes its nonwinners in leaf order during contraction and its remaining winners in leaf order during palette replacement. The initial cover and its winners depend only on chart order, so choose the common leaf order with nonwinners before winners. Now every addressed local state at B agrees between arms after deleting idle repetitions; no later B move is possible. This applies whenever the two post-cut B priors match. It does not equate other charts' records or make all priority choices equivalent.

## What happened to the 121-chart orbit?

For any fixed source A on the earlier transitive stripped orbit there exists a minimum cover omitting A. Any 97 charts hit every 25-holder leaf, so a minimum is proper. Translate an omitted chart to A. This cover survives any union-preserving single withdrawal at A and remains optimal, since deletions cannot improve the optimum. Give its members priority. The same cover and the same leaf winners occur under each withdrawal at A. Every remote chart performs identical local contraction deletions in the same leaf order. The full states coincide at the all-singleton stage, so all later chart records agree as well. A time-resolved global trace may differ. More generally, a source belonging to every old optimum is necessary for an order-independent compulsory/excluded distinction of this kind. The five-chart example supplies exactly this asymmetry without an index tie between B and D being broken by a name.

## Search, provenance and scope

A complete scan of the eleven historical star sizes covers 74,185 indexed states. It compares two distinct-support legal source withdrawals at the same chart with equal post-cut q. There are 286,404 indexed unordered source pairs and 13,290 admit a compulsory/excluded remote receiver. They yield 23,772 receiver witnesses; 2,808 source pairs have just one such receiver. None meet the additional condition that every post-cut support has size at least two in both arms. The archived three-leaf, four-chart example in trace.json has the specific normalized inputs with state IDs 2099 and 1243 and full path IDs for both. The workflow compares them with the original compressed certificate at the historical commit. That old campaign normalized each input separately; the matched source comparison is new to this study.

The bounded extension covers distinct initial supports of size at least two at (m,k)=(5,4),(6,4),(7,4),(3,5),(4,5),(5,5), fixing source chart 0, requiring unchanged q and at least two holders per leaf after either cut. extension.json reports all six cells, including failures; it is not a universal minimality claim. verify.py separately enumerates the full historical labeled domain, checks central counts without multiplying symmetry representatives, and tests every first gain on the original routine in all states with m>q at historical indexing. Arbitrary relabelings are represented because the historical domain already contains all indexed states.

This establishes a locally distinguishable transition conditional on running the original procedure and obtaining a gain. The star fixture and allowed source events are supplied. An intrinsic law guaranteeing a gain or initiating a source cut has not been established. No fractal limit, quantum dynamics or gravitational observable is defined in this study.
