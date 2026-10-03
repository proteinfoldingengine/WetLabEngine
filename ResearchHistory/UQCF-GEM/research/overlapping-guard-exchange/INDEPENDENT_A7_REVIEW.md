# Independent A7 mathematical review

Decision: **ACCEPT for negative closure of the completed two-label accessibility question declared in RESEARCH_BRIEF.md.** No critical or important mathematical issue was found. No source change is required for this decision.

Review date: 2026-10-03. This review independently fetched the remote frozen candidate and its scope brief, checked file identity, and assessed the derivations analytically. It did not rely on numerical evidence or a classification of seven-point designs.

## Exact reviewed object

- Repository: proteinfoldingengine/WetLabEngine.
- Candidate commit: `b0c281f991860f8f9cb04467ef1bed835def7717`.
- Declared parent/base: `36a82844a5ef83fc8386c37a9427064519043511`.
- Remote comparison reports candidate ahead by one commit, behind by zero, with the declared parent as merge base; its only changed file is the added candidate below.
- Candidate path: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A7_FANO_EXCHANGE_OBSTRUCTION.md`.
- Candidate Git blob SHA-1: `32fbe09548daf0c812352849f2ade72ca8d7ef2b`.
- Candidate UTF-8 byte SHA-256: `88711c917aae1fd8dbd547d2092bdf48939d45b486a5af3d6e9f4146f72f33cd`.
- Independently fetched remote content is byte-identical to `/workspace/scratch/fc9919d2c2dd/A7_FANO_EXCHANGE_OBSTRUCTION.md`; recomputing its Git blob identifier also matches the remote blob identifier.
- Scope brief fetched at the same candidate commit: `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/RESEARCH_BRIEF.md`, Git blob SHA-1 `9cc451146da38621d78c7ddfa9d7a0e1f1e003f1`.

The reviewed graph has all admissible tuples with tau at least q as vertices, with fixed palette and labelled root slots. Its edges preserve incidences outside a chosen label pair and the set of slots occupied by at least one label of that pair. The primary question quantifies over positive floors and q at least three. Thus the candidate's seven-label, seven-slot, floor-four, q=3 instance lies in the declared domain.

## Analytical findings

1. **Exact endpoints and full vertex rigidity are sound.** The displayed triples cover each palette pair exactly once. Their complementary supports have size four and transversal number three. For every admissible completed tuple in this instance, complements have size at most three. Covering all 21 pairs with seven such complements forces every complement to be a triple and every pair occurrence to be unique. A nonblock triple hits all supports, so every completed vertex has tau exactly three. The obstruction consequently includes the entire declared graph, with no omitted route through larger supports or above-target completed vertices.

2. **The edge characterization is sound.** Occupancy preservation fixes the complement block containing both selected labels. Fixed outside-pair incidences and triple size fix blocks containing neither. The remaining four blocks can only retain or swap their single selected label. For the four points outside the unique both-label block, the two single-label classes define disjoint perfect matchings. Pair uniqueness excludes a shared matching edge; their union is a four-cycle. Unique coverage of each pair consisting of a selected label and an outside point forces equal switch indicators on incident blocks, hence on the connected cycle. Every nontrivial eligible edge is the whole-tuple palette transposition. Conversely each palette transposition satisfies the declared edge conditions. Components therefore are precisely palette-permutation orbits.

3. **The labelled slot interchange is outside the orbit.** Every point occurs in three blocks and every two points share exactly one block. Distinct points' seven-block signatures differ in four positions. Removing the two exchanged positions leaves distinct signatures on the five individually fixed blocks. Any permutation preserving those five blocks fixes each point, so cannot interchange the remaining two distinct blocks. This establishes separation for every choice of two distinct labelled slots, without an automorphism-group enumeration.

4. **The primitive construction is sound.** Replacing the two exchanged supports by their union yields S. Any hitting set for S extends by at most one palette label to hit both original supports, proving tau(S) at least two. Coordinatewise inclusion in S supplies this lower bound for every intermediate tuple. Expansion intermediates contain A and contraction intermediates contain C, supplying tau at most three. The same inclusions preserve floors. In the displayed design two distinct blocks intersect in exactly one point: each of a block's three points lies in two other blocks, and pair uniqueness makes these six other blocks distinct. Hence the two supports have union size six, requiring two additions per exchanged slot followed by two deletions per slot: eight single-incidence moves to the exact labelled destination. No extra label or slot is used.

## Issues and limits

There are no blocking issues. The wording that S is “generally outside” the completed graph is weaker than the established result: in every displayed exchanged-slot instance S is outside it, and its transversal number is exactly two. This is an optional precision improvement, not a proof defect.

The accepted result is a negative answer for the stated completed two-label method, together with a primitive unit-band path for these particular endpoints. It does not establish or refute universal primitive connectivity, full nested accessibility, native lifting, implementation certification, originality, or a physical interpretation. It does not settle the earlier q=4, floor-three diagnostic. A graph enlarged by root-slot transpositions is a different question and is not proved connected here. Fixed labelled slots are essential to this particular counterexample.

No numerical campaign, state enumeration, implementation tests, workflow execution, source edits, or remote publication were performed during this review. The only local written artifact is this receipt.

## Executor ruling

Accept the scoped negative result. The reviewed proof remains byte-for-byte unchanged. The review's precision observation is acknowledged: in the displayed instances the union tuple S has tau exactly two. This publication updates executor-authored status and next-obligation records; those records are not represented as independently reviewed source.
