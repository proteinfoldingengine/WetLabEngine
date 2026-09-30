# Proof-directed continuation, not a vertex-count default

The mathematical result and example were developed exploratorily after verified v16.38 merge e4de671b3e483cc82a2e240dbd6a8d4d83e6518f (audit 36757689353). No part of this already-known work is retroactively preregistered. This file is a proposed next experiment, not an executed or preregistered campaign.

## Scientific target

Can changes in an unsaturated, restricted-support branch containing nested active vertices always be scheduled with only one temporary unit deviation, possibly moving that deviation between parent and child? Or can an admitted structure force simultaneous deviations, or a deviation of size at least two? Label borrowing while preserving descendant q is one candidate mechanism; allowing the child's own one-unit excursion is another.

The local star theorem alone cannot settle this: its root-set moves must respect a descendant subtree with q>=2. Nor can the necessary obstruction be treated as a witness. The five-vertex example in OBSTRUCTION_EXAMPLE.md exhibits the obstruction but has an explicit unit path.

## Proposed discriminating checks

1. Implement the constructive proof for SC-satisfying pairs and verify every emitted incidence move, every intermediate q profile, endpoint identity and joint width-one bound independently. Use the complete existing v16.38 canonical universe, not newly selected successful records.
2. Classify that entire universe by SC, endpoint full-support condition, active nesting and restricted palettes. Independently rebuild classifications. Exact pair identities, including omitted/duplicated/substituted negatives, are required.
3. On SC-failing pairs, isolate the first restricted skeleton edge. Test explicit competing repair mechanisms: fixed-descendant-q label borrowing versus unavoidable additional q deviations. A failed chosen algorithm is not a nonunit barrier witness; corrected global threshold certification is required for any nonunit claim.
4. Seek a general repair lemma or a rigorously certified obstruction to all unit-threshold paths. Freeze any targeted construction family and resource rule prospectively before executing a new search. Do not automatically expand to seven vertices.

## Remaining numbered-stage gates

Before a v16.39 scientific campaign, commit its actual prospective protocol on the verified integrated parent, disclosing the already-known theorem and example. Then retain the established independent canonical reconstruction, rejecting controls (including direct adapted provenance controls), full inherited tests, artifact/source/run bindings, fresh publication reproduction, durable hashes, review, verified-head merge and actual-merge audit. The present mathematical work is not a substitute for that chain and does not claim numbered-stage closure.
