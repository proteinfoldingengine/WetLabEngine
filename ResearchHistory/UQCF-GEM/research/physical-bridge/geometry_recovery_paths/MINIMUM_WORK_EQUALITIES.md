# Minimum exact-work conservation on the prepared 25-chart fixture

Status: frozen analytical addendum to PR #156 for independent review. The calculations were explored before this freeze. This is not a new prospectively registered stage or native interaction claim. [First derivation](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7154939560) · [Second minimal set](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7155015365) · [Blind controls](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-7154434692).

## Premises

Use the exact historical fixture and carrier at e61d5b0e827f7b412824ad46021e2ad6cc6f7875, and the common 134-delete preparation of geometry_selected_record_certificate.json. In each arm chart 0 first deletes one of 718 and 719, and then deletes 1355, restoring the original work table. Both addresses remain at chart 12; the address deleted by 0 has its last copy in chart 12. These preparations, the completed source update and the occurrence of a nonempty completed one-chart deletion refinement are supplied. Tip deletion must preserve the global union at every step; the completed aligned geometry must pass the historical carrier gate. The refinement length and eligible editor are not supplied. There is no physical time, outcome law, or receiver-owned measurement assumed here.

Write S for the 13 entries (0,j) with j in {6,7,8,9,11,13,16,17,18,19,21,23,24}. For every subset C of the 300 possible exact-work checks, the carrier gate plus the checks in C force a permanent, source-dependent indexed record at chart 12 for either completed source arm iff
1. C contains S and (0,12); or
2. C contains S and both (0,14), (0,22).

Thus the minimum cardinality is 14 with a unique size-14 set. The other inclusion-minimal set has size 15. The all-work return witnesses remain valid under every weaker restriction above, so the theorem is not vacuous.

## Eight equalities internal to the geometric test

A one-chart edit changes only work incident to its own chart i. The old global minimum 1984 remains present away from i. A lower minimum would have every minimum edge incident to i, which cannot satisfy degree four. At the same minimum, the degree condition for each noneditor forces its adjacency to i to agree with the original table, since its other adjacencies are unchanged. Thus the four radial weights at i are unchanged.

At a neighbor k of i, the old maximizing opposite pair not containing i is unchanged. Among the three pairs not containing i this is the unique maximum. If the new maximum were higher, every maximizing pair would contain i, so two maximizers could not be disjoint. Hence the old fixed pair stays maximal and the other maximizing pair must be its unique disjoint complement, with the old value. As k runs over the four neighbors, these are exactly the four axial distance-two work entries incident to i. Distances here are paths on the 5-by-5 torus, not an external clock. The proof uses necessary implications of the gate; a general vector satisfying these implications need not pass the whole gate.

## Exact upper certificate

For each proposed editor collect those eight coordinates and every explicitly conserved coordinate incident to the editor. If an address at the editor has no other holder, it and each of its ancestors are protected. The remaining eligible nonroot addresses include every legal deletion set. Each contributes a vector with entries +w at other holders and −w at other nonholders, where w is the squared ambient descendant subtotal, independent of intermediate tip order. A conserved projection requires a nonempty subset of distinct-address columns summing to zero. We solve a relaxation: some zero sums might not give legal or admitted endpoints. Exclusion and the mandatory choice at chart 12 are proved in this larger class.

Partition columns by whether their coordinate sum is negative, zero, or positive. Every candidate must select a nonempty subset of nonpositive columns. For each such subset let t be its negated sum, let W be total positive-column weight, and let k be the smallest positive coordinate sum divided by column weight. Then max_j |t_j| ≤ W ≤ floor(sum_j t_j/k). For each integer W the exact missing-weight target in coordinate j is (W−t_j)/2; reject wrong parity. Group positive columns by signed vector and enumerate counts subject to each group's address multiplicity and the nonnegative weight budget and target. This needs no a priori length cap and is exact because a positive group contributes its full weight to every coordinate where it is missing, zero to the other missing totals, and W determines all complementary contributions. The degree and maximal-opposite conditions are necessary, so an exhaustive no-solution certificate excludes any admitted refinement.

Both arms and both inclusion-minimal routes exclude all editors other than 12. For route 14, every projected solution at 12 consists of the other distinguished address and one of 60 unit mates (not all are asserted to pass the whole gate). In route 15, omitting the other distinguished address at chart 12 leaves all column sums positive except address 2, whose vector has zero sum but is nonzero, so it cannot furnish a zero cancellation. The exact checker lists the route-15 relaxation as well. Route 15's alternate projection has no other editor: the original arguments are unchanged or strengthened outside 0 and 12; at 0 the extra two entries rule out the projected source-only zero-sum alternatives. Full-table mate 1301 and 1302 controls are run against the inherited gate and establish occurrence is admissible, not that it must happen. Once the complementary address is deleted at 12, the retained distinguished address remains as its sole copy and the other cannot reappear at 12 under deletion.

## Lower certificate

The earlier work table gives one blind carrier-admitted chart-0 continuation whose only changed entry is (0,j), for each j in S. The new exact replay checks all 13 again in both arms. Each must be monitored: any C omitting one such entry misses its witness, in which 12 never changes.

The same chart 0 can, in either source arm, delete the remaining shared distinguished unit leaf and mate 1362 or 1399, missing chart 14 or 22 respectively. Each pair is legal and leaves chart 12 untouched. The first changes exactly (0,12), (0,14), and the second exactly (0,12), (0,22). In both cases (0,12) changes 1998→2000, and the second entry changes 2004→2002. The original carrier admits all four cases. Mate 1046 changes the union of those supports and supplies an additional admitted control. Thus a subset must hit both two-element sets. Since neither intersects S, the stated two minimal inclusion choices exhaust the possibilities.

## Limits and review targets

Exact enumeration plus a separately run individual binary-feasibility solver confirmed the actor and shared-address requirement in both arms for both minimal routes. The frozen replay uses pinned original sources and archives exact integer columns' solutions, lower controls and two positive controls per arm. The inherited comparator and foundation have their own prior reviewed verification. No physical correspondence, local access to pairwise work, or derived law enforcing either minimal set or requiring the event has been shown. Labels distinguish the retained record, not the shape or an externally chosen detector.

Independent review should reconstruct the single-editor geometry implication, validate the completeness and signs of the projected enumeration including zero-sum columns, replay or analyze all lower-control patterns, and test the direction and limits of the source-to-indexed-record inference.
