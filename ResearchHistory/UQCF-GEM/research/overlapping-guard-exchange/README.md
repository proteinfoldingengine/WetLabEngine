# Distributed repair: two completed-method obstructions

**Start here:** [Phase tracker](PHASE_TRACKER.md) separates the completed v16.54 baseline, completed checkpoints A1-A8, the negative A7/A8 method results, and pending execution-efficiency track B. [A7 research brief](RESEARCH_BRIEF.md) defines the question and completion gate.

Current A8 result: completed two-label exchanges PLUS compatible root-slot swaps are still incomplete. An explicit 25-label design pair is separated by a whole-component isomorphism invariant. Both endpoints nevertheless have a primitive one-unit path using disjoint guards and accepted normalization. The perfect starting design uses the named primary-source dependency D25; no local design-property recertification is claimed. See A8_SCOPE.md, A8_COMBINED_EXCHANGE_OBSTRUCTION.md and INDEPENDENT_A8_REVIEW.md.

Current A7 result: completed two-label accessibility is DISPROVED by a tight seven-root family. The same endpoints admit an explicit eight-move primitive one-unit path. See A7_FANO_EXCHANGE_OBSTRUCTION.md and INDEPENDENT_A7_REVIEW.md. This is a method obstruction, not a primitive barrier.

Current positive result: distributed two-label exchange and an exact renewal test, independently reviewed as recorded in INDEPENDENT_TWO_LABEL_REVIEW.md. Implementation: not started. Universal higher-floor connectivity: OPEN. No new numbered version is assigned, and v16.54's bounded certification is unchanged.

Fix two labels, every other incidence, and which roots contain at least one of the two labels. Any two admissible exact-q configurations in that class are connected with excursion at most one, even if arbitrarily many roots change. Expand the two roles across all their active roots, then contract to the destination. A four-case transversal formula proves the band and gives the exact condition under which a completed role reassignment restores level q. The exchange can change overlap structure and root sizes, so it is broader than a global label permutation.

This is a reusable distributed mechanism, not a universal sequence-selection theorem. A7 now proves that these exchanges alone cannot connect arbitrary labelled endpoints. A8 assessed the explicit enlarged relation: safe root-slot transpositions repair A7's particular failure, but A8 proves that they do not yield general completeness. Saturating three labels at once is not automatically safe: a symbolic exact-endpoint example loses two units.

The universal adaptive one-buffer conjecture is now DISPROVED. On an explicit exact-endpoint family, every one-unit root path must reach a state where at least m-3 roots are away from BOTH their own endpoint supports. Yet a primitive one-unit path exists through global label transpositions. The number of required intermediate roots grows without bound, while the excursion remains at most one.

This excludes every choice of one buffer and whole-root edit order on that family. It also excludes any fixed b-buffer architecture allowing at most one further active root, once m>b+4. Buffer identities may change and roots may be revisited; the lower bound still applies whenever at most b+1 roots may be intermediate at one state. This is a necessary participation bound, not a memory/runtime bound or a barrier greater than one.

The preceding adaptive buffer interface remains valid as a conditional theorem. At an exact-q endpoint, any existing root may initially serve as the buffer because all other roots retain transversal at least q-1. During a chosen order of edits to the other roots, each active union has an exact safe label pool for the buffer. A repair in this method class exists exactly when every such pool meets the buffer's original floor. At completed edits the buffer can change support safely through the union of its old and next supports. This proves renewal without requiring exactness at each intermediate state or one fixed buffer support for the whole path.

That proof supplies legal single-incidence moves, eligible supports, finite termination, exact labelled endpoint restoration and conditional native lifting. RENEWAL_SCOPE_CLOSEOUT.md records its historical checkpoint, when universal existence for this method was still open. The subsequent participation theorem answers that method-completeness question negatively without falsifying the conditional interface or the general one-unit conjecture.

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
- NEXT_OBLIGATION.md: prospective enlarged exchange relation and remaining global obligation.
- CYCLE_BUFFER.md: exact capacity and acyclic-residual certificate for existing buffer slots.
- CYCLE_BUFFER_EXAMPLE.md: compact higher-floor family where a buffer resolves a forced cycle.
- INDEPENDENT_BUFFER_REVIEW.md: acceptance and exact hashes of the buffer proof and example.
- ADAPTIVE_BUFFER_RENEWAL.md: arbitrary initial buffer reservation, safe support pools, exact adaptive criterion and reusable boundary handover.
- INDEPENDENT_RENEWAL_REVIEW.md: independent acceptance and exact hashes of the final proof and scope closeout.
- RENEWAL_SCOPE_CLOSEOUT.md: completed analytical deliverable, unchanged certification and unresolved universal obligation.
- UNBOUNDED_REPAIR_PARTICIPATION.md: explicit family, every-path participation lower bound, unit-band construction and bounded-buffer exclusion.
- METHOD_COMPLETENESS_DECISION.md: negative resolution of the method-completeness conjecture and the resulting research direction.
- INDEPENDENT_PARTICIPATION_REVIEW.md: acceptance, hashes and limits of the participation theorem and decision.
- TWO_LABEL_DISTRIBUTED_EXCHANGE.md: exact transversal formula, renewal conditions and distributed unit-band exchange within a two-label fiber.
- TWO_LABEL_EXAMPLES_AND_LIMITS.md: higher-floor nonsymmetry exchange, occupancy/floor limitations, and three-label saturation failure.
- INDEPENDENT_TWO_LABEL_REVIEW.md: exact reviewed candidate, hashes and acceptance limits.
- A7_FANO_EXCHANGE_OBSTRUCTION.md: complete analytical obstruction to A7's exchange class and eight-move legal alternative.
- INDEPENDENT_A7_REVIEW.md: frozen candidate, exact hashes and independent review decision.
- A8_SCOPE.md: fixed enlarged relation, analytical gate and external-dependency rules.
- A8_COMBINED_EXCHANGE_OBSTRUCTION.md: cycle-switch reduction, perfect-design component invariant, explicit separated 25-label endpoints, and primitive connectivity.
- INDEPENDENT_A8_REVIEW.md: exact candidate and primary-source review with dependency limits.
- STATUS.json: current phase and next authorized transition.

The next scientific task is a broader exchange or renewal interface that can carry a level-q-1 guard across a macro boundary, with independently proved protection and finite global progress. A8's combined relation is now proved incomplete between different unlabelled incidence structures; universal primitive higher-floor connectivity remains OPEN. A numerical or engineering-test campaign would need its own prospective bounded authorization.

This checkpoint is published on the separate research branch. It does not merge new work into the integrated certified branch. The performance-baseline/orchestration workstream remains separately pending.
