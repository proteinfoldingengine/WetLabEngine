# v16.27 — Completed proof and independent verification

This report completes v16.27; it does not start a new numbered stage. The initial report and old engine/verifier are preserved. Read this report with PROOFS.md and the exact publication receipt.

| Question | Adjudicated answer |
|---|---|
| What operation is closed? | Legal atomic factorization of a fixed same-union retained refinement and telescoping of the consistency-order difference. Proofs C1–C3 specify the finite-prefix category and map types. |
| What does the tested obstruction do? | A bare removed (view,node) event can receive different actual delta h on two legal paths with identical endpoints. An admissible three-vertex witness refutes universal event-level attribution. C4. |
| Is a new splitting or response carrier introduced? | No. Retained source/response results from earlier work are neither discarded nor redefined. This step uses only actual views, events and integer h. |
| Can attribution be compared across paths? | Yes, through identical event identities in a fixed endpoint refinement or explicit parent/view-preserving bijections. Total h(Z)-h(Y) is invariant; per-event delta need not be. C3–C6. |
| What genuinely passed computation? | 170 tests; all 3,486 original endpoints and 56,498 legal paths, plus their exact relabeled/storage-reversed copies; all intermediate h/tau/delta/trigger data; independently reconstructed shape, endpoint and path coverage. |
| What remains open? | General characterizations of which endpoints have event-independent attribution, physical realization of the formal source cone, response-law selection and the operational quantum bridge. No temporal or geometric law is inferred. |

## 1. The result stands, but the old evidence was insufficient

The initial verify.py called the producer's own produce function for its enumeration comparison. It independently recomputed only part of the witness. It did not reject false stored after-states, foreign step carriers/origins, wrong recorded h, wrong local triggers, or Boolean values substituted for integer deltas.

A new contract was committed before the replacement. Run **36624403670**, attempt 1, at `1eefe98987e3a91eb2d402d280b5445c555649e4` exposed **seven genuine rejection failures out of 11 tests**, with zero test errors. The admissible witness and two already-existing rejection checks still passed. This is a substantive RED against real incorrect acceptance, not a missing-module RED.

The identical contract passed against the replacement. The completion verifier imports no producer or inherited adjudication helper. The old source files and old GREEN remain historical records and are not retroactively credited with these checks.

## 2. Explicit admissible witness

The parent array is (-1,0,0), so 0 is root with children 1 and 2. The initial and final indexed views are

    Y=({0,1},{0,2},{0,1,2}), Z=({0,1},{0,2},{0}).

The event set is E={(2,1),(2,2)}. Both orders are legal leaf deletions; the first two views preserve the common union at every stage.

| Path | First event and actual delta | Second event and actual delta | h sequence |
|---|---|---|---|
| A | (2,1): 1 | (2,2): 0 | 1,2,2 |
| B | (2,2): 1 | (2,1): 0 | 1,2,2 |

Thus the fixed event (2,1) has different actual increments on the two paths, while both totals are 1. PROOFS.md C4 gives the complete argument from child-cover incidence; WITNESS.json supplies all intermediate states and typed fields checked by the strict verifier.

At most two union vertices imply h=1 on every cover, so no smaller union-vertex counterexample exists. No claim of minimality in every other measure is made.

## 3. What is, and is not, canonical

For a fully specified current cover and event, the local minimum-cover trigger and delta h are determined. They are not generally determined by the bare event, even when the remote initial and final endpoints are fixed.

    sum(delta h along a legal path)=h(final)-h(initial)

is an exact telescoping identity. It is NOT a claim about an invariant amount of information loss, physical time, energy, or a nonzero closed-loop response. No temporal no-go follows from this counterexample. 'Canonical' here means agreement with the ACTUAL event increments on every admitted path; the result does not forbid unrelated event invariants or newly defined averaged allocations.

## 4. Independent exhaustive verification

The producer enumerates ancestor-first rooted trees and leaf-first DFS paths with no cap. The verifier separately enumerates shapes via Prüfer sequences and all event permutations, retaining exactly those obeying descendant-before-ancestor precedence. C1 proves that these permutations are exactly the legal same-union paths.

The original universe is unchanged: all eight rooted unordered shapes through four vertices, up to four distinct INITIAL views covering the tree, same-index final retained views (duplicates permitted), and 2–5 removed incidences. At most 5!=120 permutations exist per endpoint. The historical cap of 20,000 therefore could not truncate this domain; no fictitious truncation is reported.

| Original-coordinate coverage | Count |
|---|---:|
| Rooted shapes | 8 |
| Endpoint refinements | 3,486 |
| Endpoints with multiple legal paths | 3,446 |
| Path-dependent endpoints | 1,091 |
| Complete legal atomic paths | 56,498 |
| Maximum paths at an endpoint | 120 |

Every endpoint and every path is repeated under the declared actual lineage relabeling, reversed indexed-view order and reversed vertex storage. Both copies have identical counts. Across both copies **485,872 atomic step occurrences** are checked. Copies are equivalence controls, not independent physical observations.

Every raw path, event sequence, full local profile, h sequence, delta and trigger is published in FULL_CERTIFICATES.json.xz. This replaces the old counts-plus-digest-only delivery. The uncompressed certificate is **22,500,736 bytes**, losslessly compressed to **203,300 bytes**. Raw SHA-256:

`1397e6d798c73126fc547afffb4bb7f681645bd83665af9b7ae6a66e472c866d`

The independently reconstructed counts exactly match the old 3,486/3,446/1,091/56,498 figures. That comparison is an additional recorded check; the new verifier did not use those numbers as acceptance axioms.

## 5. Rejecting checks and execution

The new suites contain 11 strict witness-contract tests and 23 full-verification tests. They reject corrupted deltas/profiles/triggers, Boolean deltas, foreign origins/carriers, missing/duplicate paths and events, false attribution flags, missing endpoints/shapes, non-prefix endpoints, wrong unions, ancestor-first illegal deletions and false metamorphic copies. Positive controls include identity, one-path endpoints, an admissible counterexample, and reordered valid path records. Nineteen named corrupted-certificate rejection reasons are logged, with further domain/coverage controls in the test logs.

The 136 inherited tests include the original v16.27 five-test suite, v16.26, v16.25, v16.24, v16.23, v16.22, v16.21 and the exact pruning parent. These regressions are useful but do not replace the new independent checks. Total: **170 tests passed**, all 15 campaign commands returned exit code zero.

Corrected scientific GREEN: **36625099103**, job **109599923952**, attempt **1**, execution SHA **a89f4cabc484612ed2924247245a0a8a2adab6d2**. Python **3.11.16**, SymPy **1.13.3**, mpmath **1.3.0**. The new primary producer/verifier themselves use only the standard library; the pinned third-party packages support inherited regressions.

Scientific artifact **11060250742**, 244,947 bytes, SHA-256 `1db9c67818ac0a4e5520b615e818bfaecc8ac0843ef23480fceb17d17a28909c`, was downloaded and its ZIP CRC and every member checksum verified. The publication stage separately reruns all commands and checks full scientific-byte equality before durable commit. See PUBLICATION_EVIDENCE.json for its actual run/commit provenance; do not equate this report's documentation commit with the scientific execution.

## 6. Review and limitations

Review is **self-review**, with an algorithmically independent verifier—not an independently authored person/agent review. The mathematical proof is written, not proof-assistant formalized. The general refutation is supported by C4; exhaustive code establishes the declared finite coverage, not a universal positive classification.

No new physical source family, coupling, response law, fundamental time primitive, metric, connection or curvature was introduced. The original 'time' interpretation is retained as program framing, not inferred from this finite combinatorial result.

**Time is pruning / ordered recoverability update.**
