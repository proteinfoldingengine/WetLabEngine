# Protection can transfer through shared roots in a safe order

Analytical checkpoint: independently ACCEPTED. Implementation: not started. Universal higher-floor connectivity: OPEN. No new numbered version is assigned, and v16.54's bounded certification is unchanged.

The first advance is a reusable handover theorem: two actual protective root subfamilies at exact-q endpoints may share one labelled root slot and still provide a primitive repair path with transversal in {q-1,q}. Disjoint protection is sufficient but no longer necessary for this construction. The proof works with arbitrary positive floors and uses only the existing palette and slots.

The sequential extension handles multiple shared roots when their protection can be transferred in a compatible order. It derives an exact criterion for a fixed-preparation, one-root-at-a-time union schedule: for every small hitting-set obstruction with disjoint old and new missed-root sets, some new missed root must be installed before the last old missed root is edited. Such an order exists exactly when one can choose a precedence witness for each obstruction without creating a directed cycle. This supplies eligible operations and finite completion under an explicit certificate, not a universal claim that the certificate exists.

The protection is not a conserved scalar. It passes from an unchanged old guard, through a proved union-bridge certificate, to a completed destination guard. Exact endpoint redundancy is restored at completion. This permits repeated use along an eligible exact-endpoint chain without assuming redundancy survives every intermediate edit.

A symbolic example proves that sequential handover can succeed where the full union bridge fails. A second example forces contradictory precedences and excludes every order in the restricted sequential method, although a different native repair still works. The precise next problem is protected resolution of these forced cycles through another preparation or partial exchange.

Files:

- SCOPE.md: native admissibility and analytical authorization.
- GUARD_HANDOVER.md: bridge criterion, one-overlap theorem, renewal and uniform slot-bound consequence.
- METHOD_LIMITS.md: exact symbolic failure of the two-overlap bridge and its alternative valid path.
- KNOWN_RESULTS.md: accepted starting classes and their boundaries.
- PROOF_OBLIGATIONS.md: review checklist and next open exchange obligation.
- INDEPENDENT_REVIEW.md: exact reviewed commit, file hashes and acceptance limits.
- SEQUENTIAL_HANDOVER.md: exact local safety and ordering criteria, acyclic certificates, renewal and termination.
- SEQUENTIAL_EXAMPLES.md: a successful sequential extension and a forced-cycle method obstruction.
- INDEPENDENT_SEQUENTIAL_REVIEW.md: independent acceptance of the frozen sequential proof and examples.
- NEXT_OBLIGATION.md: remaining cycle-resolution problem and limits of greedy choices.
- STATUS.json: current phase and next authorized transition.

The next scientific task is a protected exchange that breaks a forced cycle, renews the relevant certificate, and admits a progress argument. No large arity campaign is proposed. A numerical or engineering-test campaign would need its own prospective bounded authorization.

This checkpoint is published on the separate research branch. It does not merge new work into the integrated certified branch. The performance-baseline/orchestration workstream remains separately pending.
