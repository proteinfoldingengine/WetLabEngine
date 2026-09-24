# v15.51 — Minimal Quantum-Origin Primitive Classification

**Status:** DESIGN FREEZE — implementation not started  
**Predecessor:** v15.50 `COMMON_ANCESTOR_INSUFFICIENT`.

## Purpose

Determine the **minimal additional primitive structure** that must be added to the target-blind ordered-recoverability-incidence object (U) before a quantum operational representation can be derived, without assuming Hilbert space, subsystem factorization, recovery channels, or a node/site dictionary as primitives.

v15.50 isolated four missing outputs: quantum carrier, subsystem structure, recovery-channel extraction, and cross-domain morphism typing. v15.51 asks whether one weaker pre-quantum primitive can generate these jointly.

## Baseline

`U0 = ORDERED_RECOVERABILITY_INCIDENCE`

is frozen from v15.50 and remains sufficient for the retained leg but insufficient for the quantum leg.

## Candidate primitive classes

The first classification must compare, rather than immediately adopt:

1. **Composition-with-interference structure** — amplitudes/phases on alternative recovery compositions with a composition law, but no Hilbert carrier assumed.
2. **Convex operational distinguishability** — states/effects and probabilistic composition sufficient to ask whether complex-linear quantum structure is forced.
3. **Noncommutative event composition** — an abstract involutive/noncommutative composition algebra on recovery events, without declaring matrix/Hilbert realization.
4. **Purification/local tomography package** — stronger operational axioms tested only if weaker classes fail; must be recorded as a larger assumption package.

These are NEW candidate primitives. None may be described as derived from v15.50 unless independently proved.

## Minimality order

Candidate packages are partially ordered by explicit assumption inclusion. A stronger package cannot be called minimal if a strict weaker package already derives the same quantum-origin outputs.

No complexity score or subjective simplicity ranking may determine minimality.

## Required quantum-origin outputs

A candidate extension (U^+) counts as sufficient only if it derives, rather than supplies:

- a carrier/representation class;
- subsystem/composition structure;
- operational state/effect or channel structure adequate to define recovery;
- the typed map from (U^+) into that operational structure;
- uniqueness up to already-earned equivalence, or an explicit classification of remaining freedom.

## Forbidden shortcuts

- Hilbert space, qubits, complex matrices, tensor factors, Born rule, CPTP maps, or density operators inserted as primitive data;
- a node/site dictionary;
- target dimensions such as 32 or 125;
- fitting to curvature/source/gravity/GR;
- entropy/minimum-norm/spectral selectors;
- declaring a known quantum reconstruction theorem's conclusion as an input;
- post-result axiom addition without restarting the gate.

## Frozen verdicts

Exactly one:

- `MINIMAL_QUANTUM_ORIGIN_PRIMITIVE_IDENTIFIED`
- `QUANTUM_ORIGIN_PRIMITIVE_FAMILY_NONUNIQUE`
- `TESTED_PRIMITIVES_INSUFFICIENT`
- `QUANTUM_ORIGIN_CLASSIFICATION_ILL_TYPED`

## Adversarial controls

1. **Hilbert-smuggling control:** reject primitives isomorphic to explicitly supplied matrix/Hilbert data unless that equivalence is itself derived.
2. **Dimension control:** no target dimension in candidate generation.
3. **Strict-weaker control:** every claimed minimal package must be compared against all tested strict subpackages.
4. **Representation-freedom control:** multiple inequivalent quantum realizations are recorded, not tie-broken.
5. **Real/complex/quaternionic control:** where operational axioms permit multiple scalar fields/representation theories, uniqueness is not claimed.
6. **Classical control:** candidate axioms that admit a fully classical realization do not by themselves certify quantum origin.
7. **Relabeling/gauge control:** only earned equivalence collapses realizations.
8. **Downstream firewall:** no geometry/source/gravity/continuum data.
9. **Mutation control:** hidden target labels, omitted axioms, dimension injection, or post-exposure strengthening fail closed.

## Execution outline

Task 1 freezes the candidate primitive lattice, explicit assumption sets, output requirements, and predecessor pins.

Task 2 tests the weakest packages first and constructs all lawful operational realizations without Hilbert primitives.

Task 3 classifies whether any package forces genuinely nonclassical/noncommutative operational structure and whether carrier/subsystem/recovery structure is derived uniquely enough to define (F_Q).

Task 4 performs strict-subpackage minimality tests and independent reconstruction, including classical and alternative-scalar-field controls.

Task 5 emits the mechanical verdict and exact-head certification.

## Stop rules

If candidate primitive types cannot be specified without quantum conclusions, return `QUANTUM_ORIGIN_CLASSIFICATION_ILL_TYPED`.

If every tested package leaves (F_Q) underdetermined, return `TESTED_PRIMITIVES_INSUFFICIENT`.

If more than one incomparable minimal package succeeds, return `QUANTUM_ORIGIN_PRIMITIVE_FAMILY_NONUNIQUE`.

Only if exactly one tested minimal assumption class succeeds while all strict tested subpackages fail may `MINIMAL_QUANTUM_ORIGIN_PRIMITIVE_IDENTIFIED` be emitted.

## Claim boundary

Even a successful v15.51 result would identify a minimal primitive **within the tested assumption lattice**, not prove uniqueness among all conceivable reconstructions of quantum theory.

No source law, gravity, Einstein equation, or continuum limit follows from this gate. Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains **OPEN**.
