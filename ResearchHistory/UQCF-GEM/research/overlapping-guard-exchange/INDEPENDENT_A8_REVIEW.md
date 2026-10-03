# Independent analytical review — A8 combined completed exchange

Reviewer: independent mathematical review agent `/root/a8_combined_review`, dispatched by `/root` under the requesting-code-review workflow. Date: 2026-10-03. The reviewer did not author or modify the candidate proof.

**Decision: ACCEPT the scoped analytical negative result, with its explicit external dependency D25 and accepted maximum-layer-removal dependency.** No Critical, Important, or Minor mathematical issue was found. This answers the declared enlarged completed-method question negatively. It does not certify an implementation, locally recertify the perfect design, or establish primitive/native disconnection.

## Exact review boundary and provenance

Repository: `proteinfoldingengine/WetLabEngine`. Frozen candidate: `d4eda779dc9490e3b59c8a151e9d9b0bcf82cc85`. Parent: `83378979919501b160b51e15458b43d85990d0ea`.

The reviewer fetched the full immutable remote `ResearchHistory/UQCF-GEM/research/overlapping-guard-exchange/A8_COMBINED_EXCHANGE_OBSTRUCTION.md` and `A8_SCOPE.md`, fetched candidate commit metadata, and compared candidate against parent. The compare reports one commit ahead, zero behind, merge base equal to the declared parent, with only the proof document added. The scope document is inherited from the parent. The scope's own earlier parent field refers to its historical creation boundary and does not conflict with the candidate's scope-parent boundary.

Proof Git blob SHA: `bcf60e0d079acbfbdea719fc9af2c9c27512b7dd`. Exact fetched proof SHA-256: `7a773196b35eb0ac35d4786e0563d8ad521b3df1a2dba1ea1923261227e196db`. The remote UTF-8 content was written to a separate scratch byte copy; SHA-256, Git blob hashing, and byte comparison matched the supplied local proof. Scope Git blob SHA: `be3b58177e03536a533b281e2b90af6d52ce44bf`.

The review used manual mathematics, read-only primary-source retrieval, a visual inspection of the relevant PDF page, source reads, and byte/provenance checks. No design enumeration, numerical campaign, tests, workflows, implementation imports, or scientific computation was performed. No proof edits or remote publication were performed.

## Full relation and tight-slice check

The scope quantifies over every admissible completed tuple with tau>=q, allowing completed levels above q, with either A6 background/occupancy-preserving two-label edges or compatible whole-support root-slot transpositions. The review did not replace this relation with a narrower fixed-size or exact-level subgraph.

For q=3, h=v-3, and r=v(v-1)/6, each complementary block has at most three points. A completed tuple must cover every palette pair by complementary blocks, since an uncovered pair hits all supports. Total pair-occurrence capacity is exactly the number of palette pairs. Saturation therefore forces all blocks to be triples, all pairs to occur once, and all blocks to be distinct. Conversely a Steiner triple system excludes one- and two-label hitting sets. A palette triple that is not a block hits every support, and there are more palette triples than blocks for v>=7. Thus every completed vertex has exact tau=3. This exhausts the entire admissible completed graph: larger supports and completed levels above target offer no escape.

## Exact two-label edge equivalence and component invariant

Fixed outside-pair incidences, fixed selected-pair occupancy in the root supports, and the forced triple size fix the complement block containing both selected labels and every block containing neither. Every complement block containing exactly one selected label can only keep or swap that label. The resulting u-only and v-only outside pairs are disjoint perfect matchings on P minus {u,v,w}, where {u,v,w} is the unique both-label block. Their union is a simple degree-two graph of even alternating cycles.

At each outside point, unique coverage of {u,x} forces the two incident block-switch indicators to agree. Consequently every allowed edge switches a union of entire alternating cycles. Conversely every such union switch preserves all pairs, fixed backgrounds, occupancy, and floors, so the characterization is sufficient as well as necessary. Individual cycle switches give a finite completed decomposition when there is more than one cycle.

For a perfect design, each pair has one spanning cycle. Its only nonidentity two-label switch is the corresponding global palette transposition. Root-slot transpositions change only the ordering of blocks. Isomorphism and perfection are preserved after both kinds of moves, so induction over every finite path keeps its complement design in the starting isomorphism class. This is a component invariant, not just a restriction on the initial move. A nonperfect endpoint cannot belong to that component.

## Primary-source audit and dependency D25

The reviewer opened [Grannell, Griggs and Murphy, Some new perfect Steiner triple systems](https://grannell.net/Papers/perfect.pdf) and inspected PDF page 3 (zero-based page index 2), both extracted text and rendered page. Its Introduction defines perfection as a single (v-3)-cycle for every pair, identifies Tonchev's third C5 x C5 invariant system as a perfect STS(25), and displays exactly the candidate's four Z5 x Z5 base triples. It specifies the two coordinate translations modulo 5. The exact construction, group action, attribution, and claimed perfection are supported by the primary source.

This is verification of source support for D25, not an independent finite-design proof or local recertification of all pair cycles. D25 is accepted as established cited mathematics. If D25 is withheld, the structural tight-slice and edge/invariant results remain self-contained and the destination remains algebraically verified, but the concrete perfect starting design and hence concrete negative witness remain conditional. This limitation is correctly declared in the candidate.

The reviewer also read [Grannell, Griggs and Murphy, Switching cycles in Steiner triple systems](https://grannell.net/Papers/SWITCH2.pdf), Introduction and Theorem 1. These passages support the classical switch definition and the fact that a spanning-cycle switch is the palette transposition. No connectivity table or experimental result from that paper was used to establish A8 graph disconnection, and no search experiment was rerun.

## Explicit destination and separation check

For the Z25 bases, the differences are respectively {1,11,12}, {2,7,9}, {3,5,8}, and {4,6,10}, partitioning all twelve nonzero unordered difference classes. Each base-pair translation covers every pair of its class once. A nonzero translation has order five or twenty-five and cannot stabilize a three-point set; different base orbits are distinguished by their difference classes. Hence there are exactly one hundred distinct blocks covering each pair once. The fixed bijection between Z5 x Z5 and Z25 is only a point identification; the argument does not assume it is a group homomorphism.

For {0,4}, {0,4,10} is its block. The six displayed blocks follow directly from the stated base translations, in order: {22,0,5}, {20,22,4}, {17,20,0}, {17,18,4}, {16,18,0}, and {4,5,16}. They alternate along the six distinct outside points 5,22,20,17,18,16. Pair uniqueness ensures degree two at each of these points, so this closed cycle is a full separate component, with sixteen other derived vertices outside it. The destination is nonperfect. Perfection is isomorphism invariant, giving the required separation from D in the full enlarged relation.

Both endpoints have the same fixed twenty-five labels, one hundred labelled slots, positive uniform floor twenty-two, and exact target three. The explicit ordering conventions specify labelled endpoint tuples rather than only abstract designs.

## Primitive path and accepted normalization dependency

For a root-support transposition from level p, saturating both affected slots to their union admits a repair of any resulting hitting set by at most one label: a hitting set meeting the union already meets at least one original support, and one additional label meets the other. The expansion and contraction halves contain the corresponding endpoint tuple, giving tau<=p, and are subsets of the union tuple, giving tau>=p-1. Compatible destination floors protect every deletion. This proves the stated finite primitive realization at arbitrary p.

Each triple-design endpoint has empty total root intersection. Choosing one root omitting each label gives at most twenty-five distinct guard slots whose fixed support subfamily excludes every singleton transversal. One hundred slots provide at least seventy-five outside the first guard, enough to embed the destination guard disjointly through a slot permutation. All floors are equal. Holding the first guard while installing the second, and then holding the second while completing all remaining slots, guarantees tau>=2. Each replacement expands to its own union and contracts to its own destination, preserving its positive floor with finite single-incidence changes. The resulting path ends at the exact-three tuple C'. Compatible transpositions restore the exact labelled C.

The reviewer read the accepted v16.54 `GENERAL_PARENT_CONNECTIVITY.md` Theorem A and its maximum-layer statement, together with `INDEPENDENT_PROOF_REVIEW.md`, from the supplied existing local dependency files. Its fixed finite palette/slots, positive floors, arbitrary incidence/union carrier, finite tau>=q-1 path, and exact-q endpoint hypotheses all apply. Thus normalization yields tau in {2,3}. The accepted dependency was used for this implication, not independently recertified or implemented here. No explicit normalized move list or efficiency bound was audited or asserted.

This proves primitive one-unit connectivity of the very same separated completed endpoints. It prevents reading the method obstruction as primitive disconnection. Native lifting remains conditional on accepted child interfaces and clearance; no full nested conclusion follows solely from the completed graph.

## Accepted completion and excluded stronger claims

The candidate meets the analytical proof obligation for the declared enlarged-method question: an explicit destination and structural invariant prove a rigorous negative answer, with D25 visibly sourced and bounded. Independent analytical review is now supplied for these exact frozen bytes. This report does not itself fulfill the separate publication/status-update gate; the coordinator must publish the reviewed bytes and update status without claiming implementation certification.

Accepted: the tight completed slice, exact cycle-switch characterization, perfect-design component invariant, explicit source-dependent A8-N witness, and same-endpoint primitive one-unit connection conditional on accepted normalization.

Not established: local recertification of D25; implementation replay/correctness; numerical validation; general primitive connectivity at arbitrary higher targets/floors; the original q=4/floor-three diagnostic; universal nested connectivity; native disconnection; efficiency; novelty; or physical-law consequences. The integrated implementation baseline remains outside this analytical change.

No revision is required for scoped analytical acceptance of the reviewed candidate.
