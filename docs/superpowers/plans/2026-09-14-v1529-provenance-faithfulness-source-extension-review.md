# v15.29 Implementation Plan Self-Review / Execution Pins

This file is a required companion to:

`docs/superpowers/plans/2026-09-14-v1529-provenance-faithfulness-source-extension.md`

It records the implementation-plan self-review required by the writing-plans workflow. It contains no scientific implementation.

## Exact inherited implementation pins

Task 2 of the plan must verify these two v15.28 modules before importing them by file path:

```text
ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py
Git blob: 05cc1b8cfec70d501408377b5e44190b259a4514

ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py
Git blob: 7260147cd6ca47ec21634172b44b98de726904af
```

The v15.29 `fiber_model.py` implementation must fail closed if either blob differs. These pins supplement the evidence pins already embedded in the main implementation plan.

## Spec-coverage review

The implementation plan covers the approved design as follows:

```text
Spec §§3,6,9  typed source quotient/fibers/projection
  -> Task 2 exact q-fiber model

Spec §5 frozen evidence inventory
  -> Task 1 hash-pinned typed evidence registry

Spec §§6-7 provenance relation + countermodel requirement
  -> Tasks 3-4 provenance-equivalence and non-entailment countermodels

Spec §8 covariance/naturality
  -> Task 5 action audit and projection equivariance

Spec §10 preregistered outcomes
  -> Task 6 mechanical extension-gate adjudication

Spec §11 breakthrough rule + §12 forbidden selectors
  -> Task 7 ledger/claim-boundary assertions

Spec §13 positive/negative controls
  -> Tasks 3, 5, and 6 synthetic collapsed/distinct/representation-ready controls

Spec §14 implementation architecture
  -> Tasks 1-8 module decomposition

Spec §15 presentation boundary
  -> Task 8 gravity-blind HTML/MP4 replay

Spec §16 preservation of v15.08/v15.09/v14.04 and earlier boundaries
  -> Task 1 evidence pins + Tasks 3-7 fail-closed adjudication

Exact-head regression/publication requirement
  -> Task 9 GitHub Actions and digest-verified release
```

No spec requirement was found without a task.

## Placeholder scan

The saved plan was searched for the writing-plans red flags:

```text
TODO            : 0 matches
TBD             : 0 matches
implement later : 0 matches
Similar to Task : 0 matches
```

No placeholder remains.

## Interface/type consistency review

The later tasks use the same interfaces defined earlier:

```text
EvidenceRecord
  defined Task 1
  consumed Tasks 3 and 5

FiberRepresentative
  defined Task 2
  consumed Tasks 3, 4, and 8

RelationResult
  defined Task 3
  consumed Tasks 5 and 6

FrozenReduct / ProvenanceExpansion
  defined Task 4
  consumed Task 6 through countermodel status

ActionAudit
  defined Task 5
  consumed Task 6

ExtensionAudit
  defined Task 6
  consumed Tasks 7 and 8

audit() ledger
  defined Task 7
  consumed Tasks 8 and 9
```

No naming/signature mismatch was found.

## Boundary correction confirmed

A typed/covariant provenance carrier is not automatically a coupling-solver representation. The plan preserves the design's stronger rule:

```text
PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED
  -> no coupling solve; next object is canonical linearization/finite representation

PROVENANCE_SOURCE_REPRESENTATION_READY
  -> may open a separate future coupling-space gate
```

v15.29 itself never calls the v15.28 coupling solver and never evaluates a gravity observable.

## Plan review status

```text
spec coverage       : COMPLETE
placeholder scan    : CLEAN
interface consistency: CLEAN
inherited module pins: COMPLETE IN THIS COMPANION FILE
implementation begun : NO
```
