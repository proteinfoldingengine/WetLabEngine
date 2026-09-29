# v16.25 — Pruning/refinement closure: combined findings

## Adjudicated result

For componentwise ancestral pruning of a fixed indexed family of actual retained views, provided the union carrier is unchanged, the exact v16.24 consistency order is monotone:

**h(after) >= h(before).**

General proofs P1–P5 cover the declared finite prefix-tree category. The bounded exhaustive audit independently re-enumerated every same-union refinement of every legal cover of at most four views on all 17 rooted unordered tree shapes through five vertices.

- refinements checked: **488,307**
- strict increases: **318,719**
- unchanged: **169,588**
- decreases: **0**

Transition histogram:

| before → after | count |
|---|---:|
| 1→1 | 73,047 |
| 1→2 | 219,561 |
| 1→3 | 51,790 |
| 1→4 | 1,128 |
| 2→2 | 95,706 |
| 2→3 | 44,639 |
| 2→4 | 1,529 |
| 3→3 | 834 |
| 3→4 | 72 |
| 4→4 | 1 |

Pruning can only remove child incidences from each view. Any set of refined views covering all immediate children would also have covered them before pruning; the minimum child-cover cardinality therefore cannot decrease.

## Composition closure

For nested actual retained carriers W subset Z subset Y, longest-retained-ancestor retractions and finite fiber sums compose exactly:

**r_YW = r_ZW o r_YZ** and **P_YW = P_ZW P_YZ**.

Direct and staged pruning give the same final source pushforward. Inserting legal intermediate stages changes neither the final retained family nor its child incidence, tau, or h.

## Fixed-union boundary

The same-union premise is essential. If pruning changes the union carrier, the global node inequalities change. v16.25 makes no monotonicity theorem across different final unions.

For fixed compatible subtree coordinates on the unchanged union, global feasibility is unchanged by cover refinement. What can increase is how many local views must be checked jointly to expose the same global inequality.

## Verification quality

The wiring RED failed with implementation absent. The initial strict fixture was corrected before adjudication because its first draft changed the number of indexed views and was not componentwise pruning.

Self-review then added an adversarial non-prefix intermediate carrier. The then-current verifier incorrectly accepted it. GitHub run **36612453511** preserved substantive RED: 10/11 tests passed and that new rejection test failed. The verifier was corrected to validate every intermediate as an actual retained prefix carrier.

Scientific GREEN run **36612979239**, execution SHA `a0064589cb491a68b35c575899e8fc718c41becb`, passed all 11 current tests, independently reconstructed the complete 488,307-refinement universe, and passed inherited v16.21–v16.24 and exact-parent regressions.

The bulk certificate stores per-shape counts, transition histograms and a canonical SHA-256 stream over every refinement. The independent verifier re-enumerates the complete universe and reconstructs each digest. Explicit basis-composition certificates remain in behavioral tests.

## Scope

Formal rational source spaces and actual common-Genesis prefix-tree retained morphisms only. No physical source attainability, response-law selection, quantum structure, metric, connection, curvature or gravity is derived.

Review is self-review with an algorithmically independent verifier, not separate authorship.

**Time is pruning / ordered recoverability update.**
