# A source cut determines the very next chart under cover-preserving pruning

In the 24 four-leaf preparations where either source cut leaves the cover number at two and switches the fate of a receiver, the destination follows in **one deletion**. After each source cut exactly two of the four legal deletions preserve cover size. Both are at the same nonsource chart. Switching the cut switches that chart. An existing writer executes a source cut and the predicted next receiver edit in a single invocation on 16 of the 24 preparations. It binds a covering pair before either edit. The source-event alternative remains available in the native deletion graph at the common prior.

## Why both next edits have the same destination

Let S denote the source and let A and B be the other two active charts. With root holdings implicit, the four leaves have holder sets P = {S}, X = {A,S}, Y = {S,B}, Z = {A,B}. An additional chart is blank. The prior admits the two minimum covers {A,S} and {S,B}. P forces S and Z requires one of A or B. Either of the marked source cuts preserves the union and cover size two. The inherited v16.26 trigger is false for both. Their transferred counting grades are one each.

Suppose S cuts X. Leaf X is now private to A and P is private to S. Any two-chart cover must be {A,S}. The remaining duplicate leaves are Y, held by S and B, and Z, held by A and B. Deleting Y at S would also require B to cover Y. Deleting Z at A would also require B to cover Z. Either move raises the minimum to three. Removing Y or Z at B preserves the two-chart cover. The other removal at B is then the only further cover-preserving deletion. S cutting Y exchanges A with B and X with Y. This proves the one-step implication and classifies both two-deletion paths on either arm. A next deletion suffices for the first record. Running to a terminal state, binding a particular cover and ordering the two leaves are unnecessary for this implication.

After either cut the forced destination is the unique nonblank chart with no private leaf. It already has an identifiable relation to the event in the prior. Among the two active nonsource charts it is the one that did not hold the cut leaf. Before any event the pair of simultaneous swaps A ↔ B and X ↔ Y preserves the full unpointed incidence structure and fixes S, P, Z and the blank. Thus the unlabelled prior admits a pair of candidate receivers. The pointed source event distinguishes the destination equivariantly. A fixed labeled receiver has the same prior across the two histories.

## Original pre-cut invocation

Use P=1, X=2, Y=3, Z=4. Chart 0 is blank, chart 1 holds {2,4}, source chart 2 holds {1,2,3}, and chart 3 holds {3,4}. The common pre-cut state is row 1349 of the v16.43 four-chart, four-leaf archive.

| Source edit from row 1349 | Post-cut row | Both possible cover-preserving next deletions | Unrestricted second source cut |
|---|---:|---|---:|
| Chart 2 cuts leaf 2 | 1325 | Chart 3 removes leaf 3 or 4 | Row 1289, cover three |
| Chart 2 cuts leaf 3 | 1301 | Chart 1 removes leaf 2 or 4 | Row 1289, cover three |

Call the unmodified v16.43 normalizer **once**, from row 1349 at cover two. Its first-cover search chooses charts 1 and 2 using their supplied order, before any edit. Its live deletion prefix visits rows 1349, 1325, 1321, 1313. It deletes leaf 2 at the source, then leaves 3 and 4 at chart 3. The cut itself removes the other minimum cover from the visible atlas. The retained choice in the running program already excluded that same cover. The alternative cut from row 1349 is a legal exact-cover edge to row 1301. Taking it would invalidate the bound pair {1,2}. The published trace observes the same cover tuple and mutable state list at every cleanup call and matches the full archived normalization path.

This distinguishes three experimentally checkable facts. Both cut alternatives are native from the very same atlas. Each implies a different next chart if the next operation is a deletion that preserves cover. With the complete controller state and its input fixed, this deterministic historical writer executes only its chosen cut. It supplies direct software occurrence of one arm without a post-source restart. The physical origin of the restriction on the next operation and a native way of varying the source event at an identical external controller setting remain open.

## Counts and labeling

The 24 preparations assign distinct addresses to P, X, Y, Z with chart 0 blank and source 2. The complete chart/leaf relabeling action has 576 elements and 288 distinct labeled preparations. Each state occurs twice under the joint exchange above. The independent verifier recovers this class from arbitrary masks with a blank, two distinct legal flat source cuts and opposite forced receiver occupancy. It compares exact states, all neighbors, fixed-cover paths, bindings, keeper identities, change order and original archive row IDs.

| Observed role of the source during the three cleanup edits | Original 24 | All 288 distinct labelings |
|---|---:|---:|
| Source first | 8 | 64 |
| Source second | 8 | 64 |
| Source last | 8 | 64 |
| No marked source cut during cleanup | 0 | 96 |
| Source immediately followed by its predicted receiver | 16 | 128 |
| Source removes a still-visible choice of covering pair | 12 | 96 |
| Another edit had already reduced the visible family to one before the source | 12 | 96 |
| Opposite source cut still union-legal immediately before the executed source cut | 12 | 96 |
| Opposite source cut still legal at the same scalar cover at that instant | 8 | 64 |
| Opposite source cut preserves the already-bound covering pair at that instant | 0 | 0 |

For an analytical count, label the earlier of A and B in chart order L and the later R. The lexicographically first minimum cover is {S,L}. Of the two marked cuts, only the one on the leaf shared with L can be emitted, and only when L precedes S. That occurs in two thirds of the distinct chart placements. In the other third, S keeps both its shared leaves. When the cut occurs, the order of the three duplicated leaves distributes its position equally among first, second and third. The visible cover choice survives until either S discards its leaf shared with L or R discards Z. Their relative order is equally frequent. The other marked source cut is union-legal until R discards its leaf shared with S. It remains scalar-flat too only if R has discarded neither leaf. In the original chart order L=1 precedes S=2 throughout. These identities explain all rows of the table without treating counting frequencies as occurrence probabilities.

## Two erasures and the remaining physical question

Dropping the fixed-cover condition admits the second source cut on both arms and joins the histories at row 1289 before either receiver changes. Keeping the cover fixed while allowing additions also admits an immediate erasure. The inverse of each source cut is an archived exact-profile addition back to row 1349. Each post-cut state has ten cover-preserving single-leaf additions, including that inverse. The archived exact component therefore contains a common return even at cover two. The one-step receiver consequence uses both the deletion direction and preservation of cover size. The named pre-cut writer enforces these within its cleanup phase and preselects a covering pair by chart order. This evidence concerns finite atlas edits. An autonomous source choice, physical retained readout, and a gravity correspondence remain open.

[Prospective test](FLAT_COVER_NEXT_EDIT_PLAN.md) · [Certificate and named trace](flat_cover_certificate.json) · [Complete population](flat_cover_universe.json.xz) · [Original-writer replay](check_flat_cover.py) · [Independent reconstruction and rejecting controls](verify_flat_cover.py)

