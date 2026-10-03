# Post-v16.54: Distributed Repair

Current phase: OPEN analytical research. Last completed checkpoint: A10, reachable recovery obstruction for certified saturation/root swaps, and completeness of critical-witness primitive move certificates. Global progress remains OPEN. No run is active or queued. This phase has not been assigned a numbered version. In particular, it is not unfinished v16.54 and is not yet designated v16.55.

## Closed baseline

v16.54's bounded M1-M9 implementation and native integration are CLOSED/CERTIFIED at integrated closeout 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. The present research is on the separate branch research/uqcf-overlapping-guard-exchange. Its analytical results are published and reviewed, but are not new certified implementations or merged additions to that integrated closeout.

## Track A: mathematical research

Purpose: determine when distributed relational changes admit a renewing protection certificate and a finite repair sequence with total excursion at most one. Fixed palette, labelled roots, positive floors and one-incidence moves remain mandatory. Native lifting retains its accepted child-interface conditions.

| ID | Deliverable | Status | Evidence |
| --- | --- | --- | --- |
| A1 | One-overlap guard handover | COMPLETE, analytical acceptance | GUARD_HANDOVER.md; INDEPENDENT_REVIEW.md |
| A2 | Sequential handover and exact ordering criterion | COMPLETE, analytical acceptance | SEQUENTIAL_HANDOVER.md; INDEPENDENT_SEQUENTIAL_REVIEW.md |
| A3 | Existing-root cycle buffer criterion | COMPLETE, analytical acceptance | CYCLE_BUFFER.md; INDEPENDENT_BUFFER_REVIEW.md |
| A4 | Adaptive buffer renewal interface | COMPLETE, conditional analytical acceptance | ADAPTIVE_BUFFER_RENEWAL.md; INDEPENDENT_RENEWAL_REVIEW.md |
| A5 | Universal bounded-participation method test | COMPLETE, NEGATIVE result | UNBOUNDED_REPAIR_PARTICIPATION.md; INDEPENDENT_PARTICIPATION_REVIEW.md |
| A6 | Distributed two-label exchange and exact renewal test | COMPLETE, analytical acceptance | TWO_LABEL_DISTRIBUTED_EXCHANGE.md; INDEPENDENT_TWO_LABEL_REVIEW.md |
| A7 | Global accessibility by renewing distributed exchanges | COMPLETE, NEGATIVE FOR THE SPECIFIED METHOD | A7_FANO_EXCHANGE_OBSTRUCTION.md; INDEPENDENT_A7_REVIEW.md |
| A8 | Completed two-label exchange plus compatible root swaps | COMPLETE, NEGATIVE with explicit source dependency D25 | A8_SCOPE.md; A8_COMBINED_EXCHANGE_OBSTRUCTION.md; INDEPENDENT_A8_REVIEW.md |
| A9 | Exact renewal at one-unit-defective boundaries | COMPLETE, bounded analytical interface and diagnostics | A9_SCOPE.md; A9_DEFECT_BOUNDARY_RENEWAL.md; INDEPENDENT_A9_REVIEW.md |
| A10 | Recovery completeness and primitive move expressiveness | COMPLETE: negative recovery for M; exact local completeness for W | A10_SCOPE.md; A10_RECOVERY_TRAP_AND_MOVE_COMPLETENESS.md; INDEPENDENT_A10_REVIEW.md |

A4 remains a correct sufficient interface. A5 disproves its universal completeness, not A4's theorem and not the general one-unit law. A6 supplies a correct distributed mechanism. A7 disproves its global completeness on the declared labelled completed-state graph, while constructing a primitive one-unit path for the same endpoints. Universal primitive higher-floor connectivity remains OPEN.

### A7 milestones and completion gate

| ID | Required result | Current state |
| --- | --- | --- |
| A7.1 | Fixed mathematical question and admissibility | DEFINED in RESEARCH_BRIEF.md |
| A7.2 | General accessibility proof OR rigorous obstruction to the specified exchange class | COMPLETE: tight seven-root method obstruction |
| A7.3 | Independent review of the exact candidate and claim limits | COMPLETE: see INDEPENDENT_A7_REVIEW.md |
| A7.4 | Publish accepted proof/obstruction and scoped decision; update tracker | COMPLETE in this publication |

A7 is now complete negatively for its specified method; this is not universal primitive closure. A8 states that enlarged relation explicitly and disproves its universal completeness between different unlabelled incidence structures. Its concrete starting design uses primary-source dependency D25; D25 has not been locally recertified. Both A7 and A8 endpoints nevertheless admit primitive one-unit repair. NEXT_OBLIGATION.md records the still-open broader renewal obligation.

A new local lemma can complete a checkpoint without completing a general accessibility question. A7 is complete only when A7.2-A7.4 are satisfied, or the user explicitly agrees to a revised scope. A failed construction, an unresolved proof attempt, or another passing example does not count as closure. No percentage completion is assigned to the open theorem.

### A8 completion and source boundary

| ID | Required result | Current state |
| --- | --- | --- |
| A8.1 | Fixed enlarged relation and completion gate | COMPLETE: A8_SCOPE.md |
| A8.2 | General proof or rigorous method obstruction | COMPLETE NEGATIVE: tight triple-design cycle-switch invariant; explicit 25-label endpoints |
| A8.3 | Independent exact-candidate and primary-source review | COMPLETE: INDEPENDENT_A8_REVIEW.md |
| A8.4 | Publication and exact byte verification | COMPLETE in this publication |

D25 is the established perfection property of the displayed translated STS(25), checked against its primary source, not a new local enumeration or certificate. The native obstruction and explicit nonperfect destination are analytical derivations. Primitive connectivity for the same endpoints uses the accepted maximum-layer-removal dependency. Universal primitive/nested connectivity and the q=4/floor-three diagnostic remain OPEN. No numbered version or implementation certification is assigned.

### A9 checkpoint and remaining general obligation

A9 proves the common two-label saturation route from tau>=q-1 is safe exactly when its inactive roots have transversal at least q-2. This allows a supplied finite chain to carry defect across macro boundaries, and the residual lower tests then follow automatically from inactive-family containment. Every admissible tuple within that certified fiber is lower-safe; changing fiber requires a fresh inactive-family certificate. At the critical inactive level q-3, saturation reaches q-2, exact q is impossible within that fiber, and lower renewal needs both pure-role witnesses for every minimum inactive cover. A four-root example proves fiber disconnection but provides a full-carrier one-unit escape; a five-root example proves saturation failure can coexist with a legal fiber path.

A9 is a bounded completed checkpoint, NOT general sequence-existence closure. It supplies no guarantee that the next eligible exchange exists or makes global progress. Target-three arbitrary-arity connectivity was already proved in v16.54 and is not new A9 work. No new external design property is used; A8's D25 remains confined to A8. General q>=4 primitive/nested connectivity and q=4/floor-three diagnostics remain OPEN. Native lifting is conditional on its accepted child interfaces.

### A10 completion and global frontier

The certified saturation/root-swap recovery method M fails from a legal defect state: a 35-root, seven-label, floor-four, q=4 repeated-triple configuration is primitive-reachable from exact four but every label pair has inactive transversal one. Its entire M-component consists of root reorderings at level three. A self-contained finite primitive route recovers exact four. This is method-recovery incompleteness, not a primitive barrier or exact-endpoint-only connectivity counterexample.

The separately defined critical-witness single-incidence relation W covers ALL and ONLY legal lower primitive edges: retain a companion label at the edited root to obtain its two-label certificate. This settles local expressiveness but does not choose improving moves. General progress must now be proved at the complementary-pair-cover level, rather than inferred from more local safety certificates. A10 uses no new external design dependency; A8's D25 remains A8-specific. Universal q>=4 primitive/nested connectivity and the q=4/floor-three diagnostic remain OPEN.

## Track B: execution efficiency

This track is independent of A7 and is not a dependency of v16.54 certification.

| ID | Deliverable | Status / authorization |
| --- | --- | --- |
| B1 | Source-backed timing baseline from existing runs, attempts, logs and job dependencies | NOT STARTED; read-only analysis authorized |
| B2 | Bounded orchestration design and tiny end-to-end validation proposal | NOT STARTED; design authorized |
| B3 | Written implementation/execution scope, independent design review and user approval | NOT STARTED; needed before new tests or implementation |
| B4 | Approved implementation and focused equivalence/performance validation | NOT AUTHORIZED by current analytical scope |

Start with automated mechanical transitions and justified dependency parallelism. Consider preparation/chunking only after measurements and accepted design justify it. Preserve independent verification, exact scientific bytes or approved correspondence, inherited checks, resource limits, rejecting controls, reproduction and audit. No speedup percentage is claimed without measurements.

## Reporting and ownership

The primary executor maintains this tracker, RESEARCH_BRIEF.md and STATUS.json. Independent reviewers assess frozen candidates; their acceptance scope and hashes are recorded separately. Future updates must say which track and milestone changed.

Use this reporting template:

- Phase/version: Post-v16.54 Distributed Repair; unnumbered.
- Completed checkpoint: ID, result, exact reviewed source and publication link.
- Current objective: ID and remaining proof or engineering obligation.
- Execution: actual active run ID and attempt, or NONE. Do not use RUNNING for merely planned research.
- Claim boundary: accepted theorem, method obstruction, unresolved proposition, or certified implementation.
- Next authorized action and any genuine approval gate.

STATUS.json distinguishes checkpoint completion from the overall OPEN research objective. A completed checkpoint must never be reported as unfinished v16.54 or as universal closure. Version designation can be agreed separately; no prior exploratory result will be retrospectively called preregistered.
