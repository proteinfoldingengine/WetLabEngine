# Adaptive protection transfer and renewal

Analytical deliverable: complete after independent acceptance of the adaptive renewal theorem, as recorded in INDEPENDENT_RENEWAL_REVIEW.md. Implementation: not started. Universal higher-floor connectivity: OPEN. No new numbered version is assigned, and v16.54's bounded certification is unchanged.

The final result is an adaptive buffer interface. At an exact-q endpoint, any existing root may initially serve as the buffer because all other roots retain transversal at least q-1. During a chosen order of edits to the other roots, each active union has an exact safe label pool for the buffer. A repair in this method class exists exactly when every such pool meets the buffer's original floor. At completed edits the buffer can change support safely through the union of its old and next supports. This proves renewal without requiring exactness at each intermediate state or one fixed buffer support for the whole path.

The proof supplies legal single-incidence moves, eligible supports, finite termination, exact labelled endpoint restoration and conditional native lifting. It does not establish that every exact endpoint pair has a buffer and order satisfying those inequalities. RENEWAL_SCOPE_CLOSEOUT.md separates the completed analytical deliverable from this open universal existence problem.

The first advance is a reusable handover theorem: two actual protective root subfamilies at exact-q endpoints may share one labelled root slot and still provide a primitive repair path with transversal in {q-1,q}. Disjoint protection is sufficient but no longer necessary for this construction. The proof works with arbitrary positive floors and uses only the existing palette and slots.

The sequential extension handles multiple shared roots when their protection can be transferred in a compatible order. It derives an exact criterion for a fixed-preparation, one-root-at-a-time union schedule: for every small hitting-set obstruction with disjoint old and new missed-root sets, some new missed root must be installed before the last old missed root is edited. Such an order exists exactly when one can choose a precedence witness for each obstruction without creating a directed cycle. This supplies eligible operations and finite completion under an explicit certificate, not a universal claim that the certificate exists.

The existing-buffer extension now resolves cycles when an actual root outside both selected guards can temporarily protect the responsible obstructions. A buffer assigned a family of small hitting sets must choose its support from labels outside their union; that label pool must meet the buffer's original floor. Unassigned obstructions must admit acyclic precedence witnesses. These conditions are necessary and sufficient for this buffered method. The proof includes all newly exposed obstructions after reshaping the buffer, not only those blocked by its original support.

The protection is not a conserved scalar. It passes from an unchanged old guard, through a proved union-bridge certificate, to a completed destination guard. Exact endpoint redundancy is restored at completion. This permits repeated use along an eligible exact-endpoint chain without assuming redundancy survives every intermediate edit.

A symbolic example proves that sequential handover can succeed where the full union bridge fails. A second example forces contradictory precedences and excludes every order in the restricted sequential method, although a different native repair still works. These examples motivated the subsequent buffer and renewal results; they remain method limitations rather than connectivity obstructions.

A further symbolic family resolves such a forced cycle with five compact roots of arbitrary floor h>=3 on 4h labels. An existing fifth root supplies protection without adding a slot or label, despite the palette being smaller than the sum of floors. The family already belongs to a solved connectivity class; its value here is explaining how the cycle is broken and protection renewed.

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
- CYCLE_BUFFER.md: exact capacity and acyclic-residual certificate for existing buffer slots.
- CYCLE_BUFFER_EXAMPLE.md: compact higher-floor family where a buffer resolves a forced cycle.
- INDEPENDENT_BUFFER_REVIEW.md: acceptance and exact hashes of the buffer proof and example.
- ADAPTIVE_BUFFER_RENEWAL.md: arbitrary initial buffer reservation, safe support pools, exact adaptive criterion and reusable boundary handover.
- INDEPENDENT_RENEWAL_REVIEW.md: independent acceptance and exact hashes of the final proof and scope closeout.
- RENEWAL_SCOPE_CLOSEOUT.md: completed analytical deliverable, unchanged certification and unresolved universal obligation.
- STATUS.json: current phase and next authorized transition.

The next scientific question is whether exact-endpoint structure guarantees a choice of buffer and edit order meeting every local safe-pool capacity, or whether a stronger local exchange is needed to bypass a deficient stage. Initial lack of a slot outside the selected guards has been removed as an intrinsic obstacle by R1. No large arity campaign is proposed. A numerical or engineering-test campaign would need its own prospective bounded authorization.

This checkpoint is published on the separate research branch. It does not merge new work into the integrated certified branch. The performance-baseline/orchestration workstream remains separately pending.
