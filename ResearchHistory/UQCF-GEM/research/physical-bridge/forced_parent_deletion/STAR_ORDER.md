# What the star writer's source event determines about a blank receiver

The original v16.43 writer causally reads a donor's updated leaf set. The new question is whether the same source deletion and an intrinsically identifiable receiver determine who supplies the write. Even when all views, the unique minimum cover and the exact source deletion agree up to relabeling, they can admit silence or different first acquisitions. The complete duplicate-cleanup result does determine the possible donors by a precedence graph.

## First copy after settling duplicate leaf ownership

Use a star with (m) leaves and (k) root-containing indexed views. Its hitting number (q) is the least number of views whose union covers the star. Suppose (m>q=k-1), and B is the only initially blank view. The (q) occupied views form the unique minimum cover. Each occupied view has a private leaf. Otherwise deleting it from the cover would give (q-1) views covering everything.

The original `producer.normalize` first assigns each leaf to its least-ranked holder in the chosen minimum cover by deleting all other copies. After this cleanup, every previously occupied view has a nonempty, disjoint leaf bundle. Keep the initial holdings and these final cleanup bundles fixed as role-indexed data with the ranks forgotten. For every leaf, draw an arrow from its cleanup keeper to every other view that originally held that leaf. These arrows require the keeper to be earlier than the other holders. B has no incident arrow.

A relative order on the occupied roles yields exactly these cleanup bundles if and only if it respects every arrow. Every arrow is necessary by the keeper rule. Respecting them makes the desired keeper earliest for each leaf, so all are sufficient. Orders exist for an actual cleanup result, thus this precedence graph has no directed cycle. An occupied view can be last among the occupied views exactly when it has no outgoing arrow. Such a view can be taken out, the remaining acyclic graph ordered, and the chosen view appended at the end. Conversely an outgoing arrow prevents it from being last.

The writer migrates the occupied indices to the first (q) index positions. When B is last, all of those positions are already occupied. No migration occurs, and the subsequent (m>q) recoloring uses only the first (q) positions. B stays blank. When B is earlier, the first (q) positions omit exactly the last occupied role. The writer copies that role's entire current bundle into B in leaf order, then removes the donor's copies. Both loops are inherited. Every sink of the precedence graph can be that donor by putting B before it, and B-last is possible for every graph. The exact outcomes of the initial transfer into B are therefore silence and the bundles of the sink roles. The receiver's first acquired site, when it writes, is the least leaf of the chosen bundle. Since the bundles are disjoint and nonempty, these first sites are all distinct. With (s) sinks there are exactly (s+1) different first outcomes including silence. A single sink identifies the bundle **conditional on a write**. The cleanup alone still leaves silence possible.

The original code and scope of the rule are at `demos/v16.43-star-fiber-classification/producer.py`, lines 11–31, authoritative head e7e01bab68ba5171dacd91333f98d208d810dac3. The relative ranks are program inputs. No new dynamics or distribution over rank orders is used.

## The original three-view handoff after conditioning on the actual emission

Rows 184 and 232 from the earlier analysis have one reference, a blank B and one donor A. The only duplicated leaf belongs to the reference and A. Exactly three of the six orderings put the reference before A, so they all emit A's deletion of that duplicated leaf as the first edit. All three have the same source and receiver identities and full initial and post-event incidence after forgetting index order. A is the only sink of the cleanup precedence graph. In two qualifying orders B receives the surviving donor leaf. In the third B is ranked last and stays blank. Actual occurrence of the exact source deletion therefore still permits silence. The fractions count orderings, without assigning occurrence probabilities.

## A full matched event with different immediate acquisitions

Use four leaves and four views, with masks in B, X, R, A role order. The initial state is (1,3,13,21). X has leaf 1, R has 2 and 3, and A has 2 and 4. B has only the root. The private leaves 1, 3 and 4 force the unique minimum cover of size three. Leaf 2 is the sole duplicate.

The source deletes A's leaf 2 as the first step exactly when R precedes A. All 12 qualifying orderings give the exact same post-event state (1,3,13,17) after restoring role order. The entire cleanup is now complete. Its arrow is R to A. The sinks are A and X.

| Archived start row | Original rank order | B's next outcome | Mechanism |
| --- | --- | --- | --- |
| 103 | B, X, R, A | Gains leaf 4 on the next edit | A is last |
| 765 | B, R, A, X | Gains leaf 1 on the next edit | X is last |
| 3289 | X, R, A, B | Stays blank throughout | B is last |

Six qualifying orders give leaf 4, three give leaf 1, and three give silence. The comparison fixes the total preparation, source edit, complete post-event state, minimum cover, and initially blank receiver, all by the intrinsic roles. Both first acquisitions occur at the very next program edit. Even conditioning on a write leaves the two different outcomes. The two acquired vertices were already distinguishable by their original roles and retained identities. The copy of leaf 1 comes from X and was not carried by A. Its association with the same event arises from the selected migration column.

## Complete archive checks

The audit rebuilds the initial universe by choosing a nonempty subset of (k) owners separately at each leaf. The original archive has 74,185 starts across its eleven domains and exactly one normalization row per ordered state. The checker recomputes every starting minimum cover size, replays the unmodified normalizer to each canonical endpoint, and confirms every original edge and the archived profile band. Across the 263 initial/cleanup classes satisfying the first theorem, all predicted outcomes occur. Sixty-seven classes admit more than one copying donor.

A live event class fixes A's exact before/after mask and the multiset of all other views except B. B must be the sole blank immediately before and after A's deletion and have been blank throughout the preceding path. Leaf identities stay fixed. Across the archive all 844 such classes occur with B silent and with B acquiring a leaf. In 313 of the classes there is more than one acquired leaf across the qualifying executions.

A class with preparation records A's initial mask and pairs each of the other views' initial and event masks so roles cannot switch mid-run. B is also the unique blank at preparation. Among the 3,504 resulting classes, 1,206 always remain silent, and 2,040 allow both a write and silence. The remaining 258 always write, and each of those 258 lifts to exactly one original ordered starting row. This bounded claim preserves those positive cases. A sufficiently specific event and preparation can identify a ranked execution in the archive, while no class with multiple ordered starts in this comparison forces an acquisition.

The replay is independent of the exploratory scan's backward first-edit tracking. It uses the first edit of each index from the start and excludes every event after that index's first edit. The first audit assertion exposed a mismatch between qualifying the blank view before the event and qualifying it on both sides. The frozen result applies the both-sides condition used by the exploratory definition. Donor deletions that introduce a second blank view are outside that defined class.

**Physical scope.** The historical program supplies an actual write on some ranked executions. A structure-based identification of B and an actual source deletion leave the demonstrated ambiguity. The fixed-order handoff remains an inherited software fact. A physical rule selecting a transfer and its donor, and physical access to the resulting record, remain open.
