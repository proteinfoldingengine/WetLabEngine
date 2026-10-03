# A7: Global accessibility through distributed two-label exchanges

Status: analytical research scope definition, not a theorem or execution protocol. Track and history: PHASE_TRACKER.md. Current accepted basis: A6 at scientific candidate 36fa636de04d9a0078a8a1adbae4877ea57eb5a8, published with its review at 92fc8465a1f60108f3956cf4e2006b0e3c53d5aa.

## Primary question

Fix a finite ordered palette P, r labelled slots, positive floors a_i and feasible exact-q endpoints A,C, q>=3. Let the completed-state graph have as vertices every admissible tuple X with tau(X)>=q. Join two vertices when, for some pair of distinct labels u,v, they have identical incidences outside that pair and the same set of roots containing at least one of u,v. All destination floors must hold.

Question: do all exact-q vertices belong to one connected component of this graph, for every feasible palette and floor vector?

The accepted two-label saturation proof turns each such edge into a primitive path with tau>=q-1. A finite completed-state path between A and C can therefore be converted by maximum-layer removal into a primitive unit-band path. This is the rationale for the question, not a proof that the graph is connected.

Completed states above q are allowed; restricting the question unnecessarily to exact-q intermediate states could miss valid routes. A negative result for an exact-q-only subgraph would not settle the primary question.

## Decisive outcomes

- POSITIVE: an analytical accessibility theorem with native-derived hypotheses covering the declared primary domain, eligible moves and finite progress, followed by independent review and publication. Conditional native lifting must preserve its stated dependencies.
- NEGATIVE FOR THIS METHOD: an explicit symbolic exact-endpoint family and a proof that no completed-state path in the graph connects the selected endpoints. A failed pair choice, failed schedule or disconnected smaller subclass is insufficient. This would limit this exchange method, not by itself disprove general one-unit connectivity.
- INCOMPLETE: narrower sufficient lemmas, candidate invariants, or unresolved attempts. Publish useful progress accurately while leaving A7 open.

## Proof obligations

Every proposed exchange must establish admissibility, its lower guard and completed renewal. An algorithmic proof must show that an eligible move exists until the destination or a proved common reachable form is reached, and must provide a well-founded progress measure. Symmetry-related endpoint connectivity does not cover different overlap structures. The bounded-participation obstruction rules out treating only finitely many root supports as temporary, independent of system size.

If another distributed mechanism is required, record the revised exchange relation and its scientific justification before claiming it solves this question. Existing conditional results remain valid even if the chosen exchange relation is incomplete. Preserve failed arguments and their exact scope.

## Authorized work and exclusions

Analytical derivations, read-only source checks, independent mathematical review and repository documentation are authorized. No new numerical campaign, implementation or test execution is included. No repeated binary/ternary campaign, arity-by-arity enumeration, extra labels, extra slots, geometry insertion or physical-law claim is part of A7.

This brief defines future analysis. It does not retrospectively preregister A1-A6, assign v16.55, reopen v16.54, or authorize merging new implementation into the certified baseline. Any numerical validation requires its own prospective bounded plan and approval.
