# v15.49 — Cross-Domain Recoverability Bridge Classification

**Status:** DESIGN FREEZE — implementation not started  
**Predecessors:** v15.46 `REPRESENTATION_NONUNIQUE`; v15.47 `FUNCTORIALITY_STILL_NONSELECTIVE`; v15.48 `RECOVERABILITY_SIGNATURE_ILL_TYPED`.

## Purpose

Classify the admissible cross-domain maps

`B : R_retained -> R_quantum`

that could lawfully identify retained recoverability structure with quantum operational recoverability structure, without importing geometry, source-response, physical time, or empirical targets.

The bridge itself is the object under study. v15.49 does not assume one convenient bridge and test its downstream consequences.

## New object under classification

A candidate bridge (B) maps the frozen retained recoverability object to the frozen quantum recoverability object. The exact source/target types must be declared before classification.

The following axioms are admissibility constraints, not derived facts unless predecessor evidence explicitly certifies them.

## Frozen admissibility axioms

1. **Type preservation:** domain/codomain sorts are explicit and no implicit coercion is allowed.
2. **Covariance:** retained relabelings and quantum relabelings act compatibly with (B).
3. **Order/composition preservation:** recoverability composition/order relations are preserved where both sides expose corresponding structure.
4. **Neutrality:** neutral/null recoverability structure maps to neutral/null quantum recoverability structure, if such neutral objects are independently defined on both sides.
5. **Refinement compatibility:** declared retained refinements commute with the corresponding quantum refinement image.
6. **Lineage locality:** the image of a retained relation may depend only on the declared lineage/recoverability data in its causal domain, not downstream geometry.
7. **Disjoint composition:** independent/disjoint retained components map compositionally to independent/disjoint quantum components where typed.
8. **Gauge respect:** bridges related only by already-earned gauge are identified; no new gauge is invented after exposure.
9. **No downstream selection:** no curvature, source-response, gravity, continuum, empirical fit, or physical-time target is visible to the classifier.

## Forbidden repair mechanisms

- sorted invariant matching;
- entropy/max-entropy/minimum-norm selectors;
- PCA/SVD/spectral-edge selectors;
- manually supplied node/site dictionary;
- curvature/holonomy/source-response optimization;
- physical time or pruning-rate fitting;
- post-result axiom weakening;
- introducing a metric merely to compare otherwise ill-typed objects.

## Primary mathematical question

Given the frozen finite source and target structures and the admissibility axioms above, what is the exact classification of (B)?

## Frozen verdicts

Exactly one of:

- `BRIDGE_UNIQUE_UP_TO_EARNED_GAUGE`
- `BRIDGE_FAMILY_NONUNIQUE`
- `BRIDGE_INCONSISTENT`
- `BRIDGE_ILL_TYPED`

No other success label is allowed.

## Adversarial controls

1. **Automorphism control:** candidate bridges related by independent relabelings are not collapsed unless that equivalence is earned.
2. **Null control:** a zero/neutral bridge is not accepted solely because it satisfies covariance.
3. **Endomorphism control:** if nontrivial self-maps of the target preserve all axioms, they generate distinct admissible bridges unless quotienting is earned.
4. **Composition control:** a candidate satisfying pointwise constraints but breaking composition is rejected.
5. **Refinement control:** one-fixture success is insufficient; a frozen commuting square must also pass.
6. **Locality control:** a bridge may not inspect downstream geometry or source-response artifacts.
7. **Dimension/type control:** no implicit 32<->125 or retained<->quantum coercion.
8. **Degeneracy control:** multiple admissible bridges are recorded as nonuniqueness, not tie-broken by fixture order.
9. **Mutation control:** changed pins, omitted axioms, invented gauge, or altered typing fail closed.

## Execution outline

Task 1 freezes explicit source/target recoverability types, predecessor pins, and the exact finite axiom contract.

Task 2 derives/enumerates the smallest complete bridge family satisfying only the frozen typed constraints.

Task 3 classifies the family modulo earned gauge and searches for explicit nonuniqueness witnesses, especially target endomorphism freedom.

Task 4 independently verifies every admissible bridge, quotient relation, and hostile mutation without importing Task-2 enumeration logic.

Task 5 emits the mechanical verdict and exact-head certification.

## Interpretation

A uniqueness result would mean only that the **explicitly new bridge axiom package** selects one bridge class in the frozen finite contract. It would not retroactively derive the bridge from earlier UQCF-GEM.

A nonuniqueness result would identify remaining freedom in the bridge itself and therefore the exact class of additional primitive principle still missing.

An ill-typed result would mean even the proposed bridge domain/codomain are not yet sufficiently specified to classify lawfully.

No source law, physical gravity, Einstein equation, or continuum limit follows from v15.49 alone. Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains **OPEN**.
