# When an actor's trigger survives the global height readout

The original v16.27 attribution map kept (chart, leaf) and the change in whole-tree height for each withdrawal. On all **242,936 event occurrences** in its four-site campaign, that last value equals the trigger in the original v16.26 receipt. Its 56,498 paths contain 60,305 true and 182,631 false occurrences. An occurrence counts each time an event appears in a path.

The guarantee extends to trees of any size with at most one branching vertex. Adding a second branching vertex makes it possible for an actual local trigger to change while the recorded height remains constant. For a five-vertex example we found the two relevant parent profiles in **adjacent records 1392 and 1393** of the original v16.29 archive. In both histories the same chart performs the same edit in the same position. Its complete local P1 states agree, while its trigger is true in one history and false in the other.

## Which trees permit a hidden trigger?

Work on the finite rooted tree actually covered by the charts. The legal views contain the root and all ancestors of every retained vertex. An atomic withdrawal removes a nonroot leaf of one view and preserves the union. At a parent v, let τ(v) be the minimum number of charts covering all its children, with value zero when it has no children. The height h is the maximum of 1 and these parent values. A masked event here means that the original atom returns trigger=true and Δh=0.

**Inherited local identity.** Only the withdrawn leaf's parent can change its τ. Its value rises by one exactly when no old minimum cover survives. That rise changes h precisely if the parent was at the previous maximum. A false trigger always implies Δh=0. These are the historical v16.26 P1–P4 results. That work had already counted masked atoms at five sites. v16.29 had already exhibited locally masked diamonds. The structural classification below concerns which entire tree shapes support this loss over all allowed chart holdings. [Historical proof ledger](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.26-consistency-increment-law/TYPE_AND_PROOF.md).

| Shape of the covered tree | Fewest charts permitting a masked event |
| --- | --- |
| Zero or one branching vertex (a vertex with at least two children) | Impossible for any number of charts |
| Two branching vertices in incomparable subtrees, or a branching vertex with at least three children and a branching descendant | 2 |
| All branching vertices form one ancestor chain, there are at least two, and every branching vertex above the last has exactly two children | 3 |

A leaf contributes zero and a unary vertex contributes one. With at most one branching vertex the only possible local rise sets the global height. With one chart no same-union withdrawal is possible.

For two charts to mask a rise, two distinct parents must simultaneously require both charts after the cut. At each such parent some child is exclusive to each chart. Both charts consequently contain the parent. If one parent lies above the other, the child on the path between them belongs to both charts. The upper parent then needs at least three children. This proves the two-chart necessity.

For the converse choose the target parent p and a different parent q. For incomparable parents either orientation works. In the nested two-chart case choose the lower as p. At q choose two child subtrees off the path to p. Give one exclusively to each chart. At p choose two distinct children x and y. Initially both charts hold every child of p. Give the proper descendants of x only to the second chart and the proper descendants of y only to the first. All other available vertices can be shared. This preserves ancestry and lets the first chart release x and the second release y in either order. At p the second release raises τ from one to two, while q keeps the global height at two throughout.

For the remaining nested binary case choose p above q. At p choose a child w off the path to q. A third chart holds the path to w and all its subtree. In each of the first two charts keep w with none of its proper descendants. At q split two different child subtrees, one exclusive to each of those first two charts. Elsewhere those two charts can retain every remaining vertex. Both can legally release w in either order. The third chart alone keeps w, and it lacks the child of p leading to q. The second release therefore raises τ(p) to two. The competing parent q has required two charts all along. No parent requires three. These are constructions on any finite tree of the indicated shape, not just the enumerated trees.

## Same local record, same event position

The smallest tree with two branching vertices has five vertices. In this example root 0 has children 1 and 2, and 1 has children 3 and 4. The starting charts are A={0,1,2,3}, C={0,1,2,4}, E={0,2} and D={0,1,3}. Every edit below uses the original v16.26 atom.

| Quantity | History 1 | History 2 |
| --- | --- | --- |
| Chart and leaf released in order | A−2, C−2, A−3 | A−3, C−2, A−2 |
| C's own before → after holdings | {0,1,2,4} → {0,1,4} | {0,1,2,4} → {0,1,4} |
| Root cover number on C's edit | 1 → 2 | 1 → 1 |
| C's original trigger | True | False |
| Full height word | 2, 2, 2, 2 | 2, 2, 2, 2 |

At the start either A or C covers both root children. In history 1, when C releases child 2, A has already lost it. E still holds 2, but a second chart is needed for child 1. In history 2, A still holds both root children when C acts. The children of vertex 1 need two separate charts in both histories, masking the root change.

The full starting states, full final states, acting-chart sequence, and the entire v16.27 addressed Δh map coincide. The receiver acts second in both. Running the original v16.23 P1 push on each of the five independent ambient basis vectors confirms identical before and after linear maps at C. Thus the local record agrees for **every common choice of ambient additive grades**. The unchanged v16.27 witness selector returns no witness for this pair because its selection rule only reads the addressed Δh map.

On this minimal tree three charts suffice when event position may change. For the stronger comparison above, four are necessary. Independent enumeration from all 109 unordered three-chart starting covers, allowing duplicate rows and keeping the charts indexed during histories, reached 238,760 nonempty histories and checked 1,505,910 marked occurrences. The collision key fixes the full start and end, actor word, height word, full addressed height map, marked position and event, and that actor's local before and after. No pair sharing the key differed in the marked trigger. Index permutations cover other initial orderings. The two-chart exclusion follows from the structural theorem. The four-chart example supplies the upper bound.

## What the historical files actually retained

The genuine v16.26 receipt contains both the local trigger and Δh. The v16.27 first-witness file stores full receipts for its selected example. Its event_map projection and selection procedure are narrower. The four-site campaign exercised only trees with at most one branching vertex. Agreement of its two bits across every path follows from its domain. In v16.26's five-site census the historical totals were 19,995 legal atoms, 4,111 local triggers and 4,090 height rises. The difference is 21 masked atoms, all on the minimal nested binary tree. Five use three distinct charts and sixteen use four. [Original height-map reader](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.27-increment-attribution-closure/engine.py#L32).

The v16.29 extension serializes the four complete states and parent-cover profiles of each tested two-event square. Its original chart indexing in this example is E=0, D=1, A=2, C=3. In the original five-site group with code `((()())())`, zero-based record 1392 contains A−2 followed by C−2 and record 1393 contains A−3 followed by C−2 (each certificate includes both event orders). The first gives root profiles 1 → 2 on that C edit and is classified LOCAL_MASKED. The second gives 1 → 1 and is classified ZERO. The source recalculates the profiles from the chart holdings. Both complete records match pinned archive bytes and both pairs of intermediate states match fresh original v16.26 returns. They are evidence of an archived, addressed distinction at fixed local P1 input/output. The three-step control joins their common two-event prefixes to their respective remaining A cut. Archive membership is asserted for the two squares separately. [Historical profile producer](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/producer.py#L53) · [Original archive](https://github.com/proteinfoldingengine/WetLabEngine/blob/e61d5b0e827f7b412824ad46021e2ad6cc6f7875/ResearchHistory/UQCF-GEM/demos/v16.29-local-profile-closure/evidence/FULL_CERTIFICATES.json.xz).

The archive producer receives chart holdings and two specified events and writes global certificates. C's own P1 state is unchanged between the two histories at each matching point. No receipt is delivered to a participant-owned object by this trace. The chart-indexed information available centrally is now located to two exact records. [Prior custody result](../geometry_recovery_paths/receiver_event_order/receipt_provenance_log/RESULT.md).

## Verification and replay

The native calculation reproduces the historical v16.26 per-instance document and the exact archived v16.27 stdout. Direct original atomic calls validate the constructive witnesses on all eligible shapes through seven vertices. Of 85 rooted shapes through seven vertices, 54 permit no masking, eight permit it with two charts and 23 require three. The independent program enumerates every legal two-chart full-union preparation on these shapes. It independently regenerates the five-site native campaign's 17 per-shape receipt digests and every addressed trigger word on all four-site paths. Its hash covers ordered event identities and bits for each path at each complete endpoint. Counts alone would not detect substituted histories.

Use a historical checkout at e61d5b0e827f7b412824ad46021e2ad6cc6f7875 with Python 3.11 and SymPy 1.13.3. Set DEMOS to its absolute ResearchHistory/UQCF-GEM/demos directory, including the original evidence files. Run from this directory.

```bash
set -euo pipefail
python -B replay.py "$DEMOS" | cmp - results.json
python -B verify.py "$DEMOS/v16.26-consistency-increment-law/evidence/PRODUCTION.json" | cmp - verification.json
python -B archived_profiles.py "$DEMOS" | cmp - profiles.json
```

The [initial scope](SCOPE.md), [two-chart refinement](TWO_CHART_SCOPE.md) and [historical archive test](ARCHIVE_SCOPE.md) disclose the earlier analytic leads and the results known before each check.
