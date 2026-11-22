# Which complete pruning runs write the source address to the receiver?

A source index deletes one of two shared leaves. At exhaustion the other index must still own that address. It can also own the other address. On the existing 85-vertex fixture every shortest complete run forces the receiver to delete that other address, while every longest complete run leaves it owning both. One extra incidence of their common nonroot parent accounts for this difference. The result gives a condition on the complete run using only the native deletion graph. No endpoint, log timestamp or requested receiver output enters its definition.

## Premises

- **INHERITED.** Start from finitely many indexed prefix-closed views on a finite rooted tree. Every view contains the root. The v16.26 atom removes one nonroot view-leaf if the union is preserved. P5 factors any such componentwise refinement of the same union. The atom accepts an index and a leaf. The producer enumerates eligible calls. The factorizer accepts an endpoint.
- **SUPPLIED.** Use the two post-source families recorded in the published P1 owner-action replay. A complete run goes until it has no legal deletion. “Shortest” and “longest” compare the number of atom calls among all complete runs from the *same* post-source family. They count edits, with no physical time variable.
- **OPEN.** No unconditional occurrence of exhaustion, extremal selection or physical access is assumed. The v16.53 four-child normalizer has a documented state-dependent write in a different move system that includes additions. Its particular controller is not an implementation of shortest complete deletion here. The prior minimum-incidence example fixes a donor and a retained junction. The earlier saturation proof supplies a common lower endpoint and a budget. Neither restriction is used here.

## Characterization on any finite union tree

Write L for the nonroot leaves of the union and H(v) for the initial index set containing leaf v. Choose one j(v) in H(v) independently for every v in L. Assign to each index the root and the ancestral paths of its assigned leaves. These are precisely the reachable terminal families.

Every multiply owned union leaf admits a deletion. Once each has a unique owner, every ancestor of an assigned leaf must stay in that owner's view. Any surplus incidence outside that hull has a deepest such descendant (possibly itself). This descendant has no child in that view, and some other view covers it by retaining a union leaf below it. It can be deleted. Conversely, deleting a terminal view-leaf from a hull loses its unique global leaf from the union. All hull families form componentwise refinements of the starting family with the same union, so P5 gives a legal path to each. Each atom decreases incidence by one. In the root-only case the empty assignment gives the single all-root family.

There are exactly ∏ᵥ |H(v)| distinct terminal states. For receiver b put M = {v | H(v)={b}} and P = {v | b∈H(v)}. Its possible final leaf sets are precisely M ⊆ S ⊆ P. Any optional leaf excluded from S can be assigned to another holder. Two starting states with the same union therefore have disjoint terminal receiver views exactly when a mandatory leaf in either state is impossible in the other. Otherwise the union of the two mandatory sets gives a shared view. This statement concerns actual reachable states and assigns them no probability.

If two histories from a common family differ solely by deletions by the same source a, one can even coalesce the entire families without an intervening receiver edit. Intersect a's two surviving views, leaving every other index fixed. The intersection is prefix-closed. Any lost vertex is absent in one of the two legal families, so another unchanged index covers it. Apply P5 in each arm, editing only a, then extend the identical family to a common terminal. A receiver observing only its own successive membership changes has identical histories on these two completions.

## Shortest and longest runs on the archived family

The two terminal children of a nonroot parent p are initially shared by a,b. After a deletes s, only b holds s and both hold the other child. No further descendants exist below p. In a terminal state the remaining shared child goes either to a or to b. Putting it with a forces b to remove it and leaves both owners at p. Putting it with b leaves only b at p. Nothing outside p's subtree changes between the two terminal assignments if we hold all other leaf assignments fixed. Their common parent is a direct child of the root, whose membership is fixed for all indices. Thus the two possible terminal incidence totals differ by exactly one for **every** fixed outside assignment. The path length to a terminal is initial incidence minus terminal incidence. This proves that all shortest completions split the marked leaves and all longest completions put both with b. Under the shortest condition, b's own membership changes and its surviving marked address identifies s. At the longest endpoint, both source histories can give b the same full view.

The terminal distance d(F) = min over reachable terminals Z of (|F| − |Z|), with |F| the sum of view sizes, is defined from the unweighted transition graph. Choosing any legal step decreasing d by one realizes a shortest path. This expresses precisely what a proposed historical selection law must imply on this family. It introduces no weights or target receiver. The existence of this graph function alone does not make it a law of motion. If p is the compulsory root, both assignments have the same terminal incidence and both occur after one step in the two-leaf control. The nonroot retained junction is essential to the length advantage here.

## Bounds and witnesses on the full fixture

There are 25 roots counted with multiplicity, 25 corner leaves of multiplicity four, 50 edge-complement leaves of multiplicity 23 and two marked children. After the source edit the marked multiplicities are one and two. All 25 indices initially retain all seven internal nonroot parents. The post-source incidence is 25×8 + 25×4 + 50×23 + 3 = 1453. At terminality the 77 global leaves each contribute one incidence. The 25 roots and these leaves give a fixed total of 102.

Each of five row parents can have three to five terminal holders at the extrema. Two labels cover at most four of its five corners. The row labels at offsets 0, 2 and 4 cover the row, and choosing the label at each corner realizes five. The common edge parent requires at least two terminal holders since each index is excluded from its own incident edge leaves. Two nonadjacent indices cover all 50, so two are attainable. The certificate assigns distinct allowed edge leaves to all 25 indices and attains the upper bound of 25. The five row subtrees, edge subtree and marked subtree have independent assignments. All extremal counts in the table are attainable from either source input.

| b's final marked leaves | Holders at p | Minimum deletions | Maximum deletions |
| --- | ---: | ---: | ---: |
| Only the source-deleted address | 2 | 1299 | 1332 |
| Both addresses | 1 | 1300 | 1333 |

There are K = 4²⁵ × 23⁵⁰ ways to assign the unmarked leaves. In each arm K terminals carry just the marked source address at b and K carry both. The two arms share exactly the latter K full terminal states. These count distinct endpoints, without weighting schedules. The bounds compare extremal runs. An unspecified intermediate run length does not in general select a record.

## Reproduction

Run the checker relative to the repository root with Python 3.10 or later. It imports the original producer and independent verifier, checks the Git blob of the existing ZIP, and reads the exact archived source inputs. It enumerates the native transition graph for every rooted shape through four vertices with one, two or three ordered views, including repeated views. It compares all sinks reachable from every start with the analytic assignments, and checks disjointness on the distinct receiver intervals. On the full fixture it verifies each source atom, every extremal terminal witness as a refinement, every candidate terminal deletion refusal and the equal-length root control. Large-case reachability uses P5. The full 85-vertex path graph is not enumerated.

This answers the fixed-command challenge. A refused command can remain private to the global checker. A shortest complete run actually edits b, with opposite surviving addresses in the two source histories. A longest complete run actually admits identical final states. Finding which, if either, inherited caller enforces these alternatives on this carrier is the outstanding question.
