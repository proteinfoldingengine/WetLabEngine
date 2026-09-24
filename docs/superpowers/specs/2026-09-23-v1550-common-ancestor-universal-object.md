# v15.50 — Common-Ancestor / Universal-Object Gate

**Status:** DESIGN FREEZE — implementation not started  
**Predecessors:** v15.46 `REPRESENTATION_NONUNIQUE`; v15.47 `FUNCTORIALITY_STILL_NONSELECTIVE`; v15.48 `RECOVERABILITY_SIGNATURE_ILL_TYPED`; v15.49 `BRIDGE_ILL_TYPED`.

## Purpose

Test whether retained recoverability and quantum operational recoverability can be obtained as two representations/projections of one deeper primitive object (U), rather than by postulating a direct cross-domain bridge.

Target architecture:

`R_retained <-F_R- U -F_Q-> R_quantum`

The common ancestor, not a direct retained↔quantum map, is the object under study.

## Candidate primitive object

The first candidate class for (U) is a minimal **ordered recoverability incidence object** containing only:

- primitive record/event occurrences;
- lineage/dependency incidence;
- admissible recovery composition;
- ordered recoverability/pruning-compatible refinement;
- disjoint composition where already meaningful.

No geometry, Hilbert-space factorization, entropy extremum, source law, physical time, or empirical target is primitive in (U).

## Central requirement

Both legs (F_R) and (F_Q) must be determined from the same declared (U)-structure and the same preregistered universal laws.

Supplying (F_Q), a node/site dictionary, a Hilbert carrier, or a target-specific selector by hand fails the gate as a disguised v15.49 bridge.

## Universal-property test

A candidate (U) is admissible only if:

1. its type is defined independently of either target;
2. (F_R) and (F_Q) are lawful morphisms in independently declared target categories;
3. identities/composition/refinement are preserved where typed;
4. any claimed universal property is stated before candidate exposure;
5. factorization through (U) is unique up to earned automorphism/gauge;
6. target endomorphisms cannot generate inequivalent factorizations unless recorded as nonuniqueness;
7. neither leg can inspect downstream geometry/source-response data.

## Forbidden constructions

- defining (U) as the ordered pair ((R_retained,R_quantum));
- embedding the desired node/site dictionary in labels of (U);
- defining (F_Q) by lookup table;
- entropy/max-entropy/minimum-norm/spectral selectors;
- sorted invariant matching;
- curvature, holonomy, source-response or GR selection;
- physical-time/pruning-rate fitting;
- declaring target automorphisms gauge after exposure.

## Frozen verdicts

Exactly one:

- `COMMON_ANCESTOR_UNIQUE_UP_TO_EARNED_GAUGE`
- `COMMON_ANCESTOR_NONUNIQUE`
- `COMMON_ANCESTOR_INSUFFICIENT`
- `COMMON_ANCESTOR_ILL_TYPED`

## Adversarial controls

1. **Pair-object control:** (U=(R,Q)) or an isomorphic disguised product is rejected.
2. **Target-blindness:** constructing (U) cannot inspect quantum labels or geometry.
3. **Leg independence:** (F_Q) may not call/use (F_R^{-1}) plus a supplied dictionary.
4. **Automorphism control:** nontrivial automorphisms of (U) and target endomorphisms are explicitly classified.
5. **Factorization control:** two inequivalent (F_Q) legs from the same (U) imply nonuniqueness.
6. **Refinement control:** at least one nontrivial frozen refinement diagram must commute.
7. **Composition control:** at least one nonidentity composition must be exercised.
8. **Degeneracy control:** fixture order cannot break equal structural signatures.
9. **Dimension control:** no implicit 32↔125 reshape/padding.
10. **Downstream firewall:** no curvature/source/gravity/continuum inputs.
11. **Mutation control:** changed pins, hidden target labels, omitted laws, invented gauge, or target-specific fields fail closed.

## Execution outline

Task 1 freezes the type/signature of (U), the two target categories, predecessor pins, and the universal-property contract.

Task 2 constructs/enumerates the smallest complete family of target-blind (U) candidates admitted by that contract and rejects pair-object/dictionary contamination.

Task 3 derives/enumerates both legs (F_R,F_Q) from each surviving (U), then classifies factorizations modulo earned automorphism/gauge.

Task 4 independently reconstructs candidate and factorization accounting and attacks it with automorphism, target-endomorphism, refinement, composition and mutation controls.

Task 5 emits the mechanical verdict and exact-head certification.

## Stop rules

If (U) itself cannot be typed without importing one target, return `COMMON_ANCESTOR_ILL_TYPED`.

If (U) is well typed but does not determine a lawful quantum leg without additional cross-domain information, return `COMMON_ANCESTOR_INSUFFICIENT`.

If multiple inequivalent common-ancestor factorizations survive, return `COMMON_ANCESTOR_NONUNIQUE`.

Only one factorization class under already-earned gauge permits `COMMON_ANCESTOR_UNIQUE_UP_TO_EARNED_GAUGE`.

## Claim boundary

A successful result would establish only that the explicitly new universal-object principle selects a common factorization in the frozen finite contract. It would not prove that the principle follows from earlier UQCF-GEM or establish gravity.

An insufficiency result would be especially informative: it would show that a common retained primitive structure alone still does not originate the quantum projection.

No source law, physical gravity, Einstein equation, or continuum limit follows from v15.50. Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains **OPEN**.
