# An existing clone loop selects different peers without row or label ordering at the endpoint

**Scope.** Constructed exact inputs to the unchanged v16.54 M4 clone producer and independent checker, not original archived catalog occurrences. This is an enacted program transition, not just a legal choice. It is not a derivation of a native trigger, a historical source receipt, receiver-owned access, or physical interpretation.

## Matched route and extension

Bit j is label j. There are eight rows. Row 0 is the source, row 1 peer A, row 2 peer B. The two calls begin with identical complete holdings and floors. Run label commands (1,5) or (1,7), followed **in the same existing call** by the identical (0,1). The caller supplies both commands; it supplies neither a receiving row nor any target holdings.

The compact input is [342,169,169,170,356,464,139,43], k=9, floors [2,2,3,1,1,1,1]. The first command cuts only source 342→326 or 342→338. In the next command, A and B are the only slots. Its sorted demands are [325,169] versus [169,337]. One new demand comes from the source; the other equals the prior at both peers. The normalizer thus writes A=325 or B=337 and preserves the other peer. This compact example is row-order invariant at fixed label order, not invariant to label renaming.

Remove the role of lexicographic labels by using [3414,681,681,682,356,3536,651,555], k=12, floors [2,2,3,1,1,1,3,1]. Relative to the compact input, put new label 9 on rows 1,2,3,6,7; put 10 and 11 on rows 0,5; raise the floor of row 6 from 1 to 3.

| Call | First command: sorted slots, sorted demands | Second command: sorted slots, sorted demands | End (source,A,B) |
| --- | --- | --- | --- |
| (1,5), (0,1) | [0,6], [326,651] | [1,2], [325,681] | (326,325,681) |
| (1,7), (0,1) | [7,0], [555,3410] | [1,2], [681,3409] | (3410,681,3409) |
| Only (0,1) | none | [1,2], [681,3413] | (3414,681,3413) |

Only the source changes in the first command; the first branch releases three labels from it and the other releases one. No neutral row changes. In the second command's output exactly A shrinks 5→4 or exactly B grows 5→6, respectively. These differences persist in the stored endpoint of the routine. The other peer is unchanged. No label readout is needed for this own-state width contrast, but the program exports a global record; separate participant access is not established.

## Why row and label names do not determine the endpoint

The historical M4 producer computes slots (holding u without v) and sorts them by floor, using row index only for ties. It computes distinct demands by replacing v with u in each row holding v without u, and sorts by width, using label ordering only for ties. Then the existing producer edits each slot to its paired demand by adding before removing. The membership tests commute with relabelings that carry the command labels. The extended experiment has no ties in each of the slot-floor or demand-width lists: first commands have widths (4,5) and (5,6); second commands (4,5) and (5,6); the no-source control (5,7). Each slot's floor meets the demand size. This proves agreement of command endpoints for every simultaneous row enumeration and label bijection (with floors and commands transported), not agreement of intra-command primitive order after label renaming.

Labels {3,6} hit every row after renaming back, throughout each path. All sites either remain untouched or move by adding the new labels before removing old ones; both endpoints of every such replacement keep this cover, so every intermediate holds it. Rows 4 and 6 are disjoint and unchanged; no single label can cover the state. Thus every primitive has exact cover two and the historical clipping mechanism need not alter one frame. The actual stock verifier checks the clone interval, order, endpoint, wide-band semantics, and hitting formulas. The additional independent cover witness enforces exact two, not merely the wide band.

## Irreducible supplied inputs and controls

The floors are a real asymmetry, not bookkeeping. If A and B instead had equal floors, exchanging their enumeration would exchange which receives the nonneutral demand; two identical eligible holdings with identical floors cannot be uniquely distinguished by the ordering-free input.

The common prior already permits the second command, which writes B with width 5→7 rather than 5→6 or leaving B unchanged. Starting fresh from either exact post-first-command state and supplying the second command reproduces the entire associated receiver suffix. The result is therefore a source-state-dependent write, not a certificate of occurrence or evidence that a source receipt crosses into the peer. Each extended post-first-command state admits 69 exact commands of the 132 distinct ordered label pairs. Fifty-eight make a nonempty write; (3,9) is an exact no-op. The inherited loop does not select its label commands or invoke itself. Its floor distinctions, preparations, shared access and call are supplied. Varying the first command is an intervention; the sign and content of the source cuts are computed by the producer, not defined as input changes to row 0. No new trigger was added and the result does not meet the complete native constructive milestone.

## Verification

Run `python -B replay_clone.py /absolute/path/to/demos/v16.54-parent-support-connectivity`. It pins three Git blobs, uses the original immutable producer and checker, verifies all 40,320 row permutations of both arms in each fixture, checks representative label bijections for the extended fixture, checks no-source and fresh-post-state aliases, counts exact one-command alternatives, and verifies rejection after reversing the saved demand order (no changes to scientific bytes are used to make the direct cases pass). Counts and raw fixture paths are in expected.json. The name-independent endpoint theorem uses the strict inequalities, not a finite no-counterexample inference. The catalog's exhaustive enrollment contract is not asserted for these new eight-row cases.
