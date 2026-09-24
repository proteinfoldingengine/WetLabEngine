# v15.47 — Cross-Domain Representation Functoriality Gate

**Status:** DESIGN FREEZE — implementation not started  
**Classification:** architectural/theorem gate  
**Predecessor:** v15.46 Stage C `REPRESENTATION_NONUNIQUE`.

## Purpose

Test whether one explicitly new, pre-time cross-domain principle can reduce the representation freedom certified by v15.46 without importing source, curvature, gravity, time, entropy optimization, or a hand-written node/site dictionary.

The proposed new principle is a **retained-to-quantum representation functor**. It is explicitly a NEW ASSUMPTION, not a rediscovered consequence of the frozen ontology.

## New assumption under test

There exists a representation assignment

`F : Retained -> QuantumRepresentation`

defined on a declared finite retained category and satisfying:

1. identities map to identities;
2. composable retained morphisms map compositionally;
3. disjoint composition is represented monoidally;
4. declared refinement/quotient diagrams commute;
5. retained isomorphisms map to quantum equivalences;
6. the rule is size-family uniform and fixed before downstream exposure.

The target is typed abstractly enough to include finite-dimensional carrier/algebra, subsystem inclusions and state transport. No source amplitude or geometry observable is part of F.

## What is forbidden

F may not be selected, parameterized or repaired using:
- v15.39 source-response performance;
- v15.43-v15.45 curvature;
- Newton/ADM/Einstein/continuum targets;
- entropy or maximum-entropy completion;
- minimum norm, PCA/SVD or spectral-edge tuning;
- sorting retained invariants against quantum spectral invariants;
- a manually supplied node-to-site bijection disguised as bookkeeping;
- physical time or pruning rate.

## Primary question

Do the functoriality laws themselves reduce the v15.46 Stage-C representation family to one equivalence class under an explicitly declared target equivalence?

The test must compare the whole surviving family, not demonstrate that one chosen representation satisfies the laws.

## Frozen verdicts

Exactly one of:

- `FUNCTORIALITY_STILL_NONSELECTIVE`
- `FUNCTORIALITY_SELECTS_REPRESENTATION_CLASS`
- `FUNCTORIALITY_INCONSISTENT_WITH_FROZEN_RETAINED_STRUCTURE`
- `FUNCTORIALITY_ILL_TYPED`

No other success label is allowed.

## Adversarial controls

1. **Weak-covariance control:** mere covariance under independently supplied permutations must remain nonselective.
2. **Dictionary injection control:** a candidate whose implementation contains a privileged node/site table is rejected as `MANUAL_CROSS_DOMAIN_DICTIONARY`.
3. **Conjugate-family control:** if two functors differ only by an earned target equivalence, count them as one class.
4. **Inequivalent-family control:** if two survivors are not related by declared/earned target equivalence, selection fails.
5. **Dimension control:** no implicit 32<->125 reshape or padding.
6. **Refinement control:** a rule that works only on one fixture but fails a frozen refinement square is rejected.
7. **Composition control:** a rule that does not preserve declared composition is rejected.
8. **Downstream firewall:** the evaluator has no curvature/source-response inputs.
9. **Null firewall:** failure to select does not imply zero source or absent physics.

## Execution design

Task 1 freezes a minimal finite retained category from hash-pinned predecessor structure and a separately declared target representation category.

Task 2 implements a candidate-enumerator/checker that evaluates functor laws without geometry and includes weak-covariance/manual-dictionary hostile controls.

Task 3 enumerates surviving representation classes modulo declared target equivalence and measures whether Stage-C freedom is reduced.

Task 4 independently reconstructs the law checks and equivalence classes from frozen inputs, without importing Task-2 selection logic.

Task 5 emits the mechanical verdict, exact ledger and exact-head CI receipt.

All executable tasks use RED->observed failure->minimal GREEN, CPython 3.13.5, deterministic exact arithmetic where possible, and fail-closed source pins.

## Interpretation

A selecting result would establish only:

**Given the explicitly new functorial representation axiom and the frozen finite contract, the tested representation family collapses to one target-equivalence class.**

It would not establish that the functoriality axiom follows from earlier UQCF-GEM, nor that the selected quantum representation is physically correct, nor gravity/GR.

A nonselective result would show that even this stronger new structural principle is insufficient in the tested contract and would prevent silently treating “naturality” as the missing physics.

No source law is adopted. Source correspondence remains `NOT_EVALUATED`. Pillar 3 remains **OPEN**.
