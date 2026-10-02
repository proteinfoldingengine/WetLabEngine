# v16.54 general parent-support connectivity

Status: independently accepted analytical results; no implementation or new numerical execution; not CLOSED/CERTIFIED.

Start with FINDINGS.md for the result, GENERAL_PARENT_CONNECTIVITY.md for the exact reviewed proof, and INDEPENDENT_PROOF_REVIEW.md for its independent acceptance. NATIVE_ADMISSIBILITY.md and RESEARCH_SCOPE.md preserve the original category, question and disclosed prior leads.

The general theorem removes upper excursions and reduces parent unit connectivity to lower subset-cover connectivity. Target3 is connected for arbitrary arity; five-child target4 is connected including saturation. General higher-target subset-cover connectivity remains OPEN. The certified predecessor is v16.53 at integrated commit f6d4d792aa6ec1d7c058eeb21fa3a4de267dacb8.

The exact-endpoint extension is in EXACT_ENDPOINT_CAPACITY.md, accepted by INDEPENDENT_CAPACITY_REVIEW.md. It proves local redundancy and capacity inequalities, and resolves the entire saturated capacity boundary sum b_i=(q-1)k for every q>=3 and every arity. Positive-slack pair/higher-subset connectivity remains OPEN. The extension retains its candidate header to preserve reviewed bytes; its review records acceptance.

PROTECTED_EXCHANGE.md and INDEPENDENT_PROTECTED_REVIEW.md add an accepted arbitrary-arity positive-slack theorem for endpoints with q disjoint root witnesses, plus an exact floor criterion for this class to exist. A symbolic exact-q family shows the class may be absent; this is only a method obstruction. Universal positive-slack connectivity remains OPEN.

OVERLAPPING_CLIQUE_EXCHANGE.md and INDEPENDENT_OVERLAP_REVIEW.md resolve an entire overlapping-root parameter family, including the earlier triangle method obstruction: all exact endpoints are connected despite the impossibility of disjoint root witnesses. The mechanism is extremal endpoint classification plus general safe symmetry exchanges. Universal positive-slack connectivity remains OPEN.

Latest: FLOOR_TWO_CONNECTIVITY.md and INDEPENDENT_FLOOR_TWO_REVIEW.md prove all exact endpoints connected for every feasible arity/palette/target with every root floor equal to 2. The new star-symmetrization mechanism changes overlap structure and subsumes the clique-boundary family. General mixed/higher-floor connectivity remains OPEN; no numerical campaign or implementation certification.

Latest: SINGLETON_ANCHOR_REDUCTION.md and INDEPENDENT_SINGLETON_REVIEW.md prove connectivity for all mixed floors in {1,2}, and for arbitrary remaining floors whenever at least q indices have floor 1. Residual hyperedge cases with fewer singleton-capable roots remain OPEN beyond the earlier scoped results. No implementation certification.
