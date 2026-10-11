# Independent reserve-activation code review

Verdict: one required negative-control coverage correction before scoped completion. No mathematical or implementation defect found in the reviewed producer/checker algorithms. This is a fresh review of the supplied files, not an attestation of pending full production, fresh reproduction, inherited suites, CI, publication, or immutable readback.

Reviewed: RESULT.md, VERIFICATION_SCOPE.md, PLAN.md, producer.py, independent.py, test_activation.py, red.log, tests_attempt2.log. Declared prospective freeze: bf40d757b903256f66f9f809b767db7d9ab0826f; declared parent: c31f5313486be2be25ff1d32d01b507d2de2e313. Those Git bindings were supplied by the implementer and were not independently fetched in this review.

## Required correction

**Medium — the named source-profile omission control removes the K2 fixture instead.** In `Activation.test_source_profile_omission`, `d['records'].pop()` removes the last record of `P.build(fixture=True)`. That record is the separately declared `name='k2'` fixture, outside the 8192 native source universe. Thus the passing test establishes rejection of a missing fixture, not the frozen scope's explicitly required native source-profile omission control. Replace the mutation with removal of a native multiplicity-profile record selected explicitly by its source multiplicities, or omission of the complete selected profile. A cheap fixture test may remove the `full` all-two profile record explicitly, while the positive source-universe test continues to check both full declarations. Preserve the original test/log evidence. This is a control-identity gap, not evidence that `verify` would accept a genuinely omitted source profile: its independent ordered reconstruction should reject that omission.

## Scientific implementation assessment

- Abstract declarations enumerate all 5054 `(p,q,m)` identities, including q=0 and empty receiver columns. Producer traverses from the initial assignment, records every unused-donor release candidate and every unused-donor/unused-receiver transfer candidate, keeps rejection verdicts, and retains all valid edges and first-vacancy terminal assignments. The checker independently generates the product universe of partial injective assignments with at most one vacancy, constructs transitions over that universe, and filters by source reachability. It neither imports the producer nor derives its universe from producer output.
- Closure implementations differ appropriately: producer iterates bitwise singleton remainders; checker applies simultaneous set implications. Both compare terminal existence to positive surplus. Every reachable nonterminal state without a transfer is checked against the final closure; the complete graph retains alternative rule orders, including choices available before early release. Canonical routes prefer the least releasable donor, then the least eligible transfer donor. Full-record comparison occurs before record digest comparison.
- Native declarations cover 4096 saturated subgraphs of the twelve labelled K4,3 roots and both uniform positive multiplicity profiles, for 8192 sources. Floors are derived from the original source, labels retain fixed positions, anchors are actual original labels, and donor/anchor disjointness is enforced. Original cover eligibility and G-independence are checked before construction.
- Transfer reconstruction preserves the actual common root, deletes other donor incidences before additions, and never reuses a donor or receiver. Source star containment, original floors, core cover number 3 through 4, anchor footprint immutability, edit cost, no early vacancy, and final vacancy classification are checked at each source-local distinct state or at the appropriate ordered route boundary. The exact labelled reverse route is reconstructed and compared to the forward states in reverse order.
- The complete protected one-hidden family is correctly characterized by a nonempty exposed-root set not contained in any original star. The per-footprint hidden check rules out a hidden-plus-current-label two-cover; the separately checked core lower bound rules out two-core-label covers, and the fixed anchors supply the upper bound. Consequently this factorization checks the one-hidden full-system band without looping over every state/mask pair independently. Explicit source/state records and complete mask lists recover those Cartesian identities, and `hidden_checks` is their logical pair count, not a count of independent uncached evaluations. Arbitrary hidden completions remain an analytical domination argument, not a finite-enumeration claim.
- The hand chain, forced cherry, fully saturated lock, empty graph, and K2 control are declared separately. The K2 reassignment retains its macro/boundary but has no operation and only the original actual state. It therefore makes no false committed-edit, escape, or vacancy claim. The ineligible singleton-anchor test exercises rejection before construction.
- The analytical exactness claim stays within the fixed-anchor monotone template. Nothing reviewed asserts normalization of arbitrary native paths, permission for intervening repair before reversal, new acquisition/sensing, or guaranteed progress.

## Evidence examined and limited spot checks

`red.log` contains a genuine missing-producer import failure. `tests_attempt2.log` reports 30 passing tests. Reading that log does not establish execution of any later suite or full campaign.

This reviewer independently ran a bounded spot check, with successful process exit:

1. Compared all 81 abstract records for `(p,q)=(1,0),(2,2),(3,2)` between the two implementations.
2. Recomputed the chain source's protected one-hidden family using direct cover-number enumeration rather than the exposed-set predicate. All 4034 masks matched.
3. Directly checked full-system cover number 3 through 4 for every one of those 4034 masks at four chain slices: the original, first edit, first completed transfer, and final vacancy.

These spot checks are supplemental and are not new counted scientific unit tests. No full campaign, fresh reproduction, or inherited suite was rerun by this reviewer. All such outcomes remain pending for purposes of this review.

## Nonblocking limitations to preserve in reporting

The finite native campaign uses one fixed donor/anchor selection, two uniform profiles, and canonical routes on K4,3; arbitrary eligible selections, mixed positive multiplicities, other carriers, and arbitrary hidden systems rely on the theorem's proof. Many negative controls intentionally mutate serialized records and are rejected by complete equality against reconstruction; they establish detection of those certificate corruptions, not independent semantic adversarial-path experiments. The native checker is independently coded with sets but necessarily follows the same specified canonical construction; its strongest structural independence is the abstract product-assignment enumeration versus forward traversal.

After the named profile-omission control is corrected and rerun, this review has no remaining code-level blocker. Scientific completion must still be based on actual successful full outputs and the subsequent evidence gates.
