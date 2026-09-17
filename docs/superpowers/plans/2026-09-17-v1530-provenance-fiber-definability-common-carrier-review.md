# v15.30 Implementation Plan Self-Review / Execution Pins

This file is the required companion to:

`docs/superpowers/plans/2026-09-17-v1530-provenance-fiber-definability-common-carrier-implementation.md`

It records the implementation-plan self-review required by the writing-plans workflow and completes helper-interface pins that are referenced by tests. It contains no scientific implementation.

## Approval / execution boundary

The v15.30 concept and written design have been approved. The implementation plan is now complete and self-reviewed. Scientific implementation has not begun.

Frozen stacked base:

```text
6535ea69214f6661e340fe201813dfd17ddbb7e1
```

Inherited scientific source pin:

```text
42244310b065f473c8bd459a6f065a61afbd2292
```

The v15.29 result remains:

```text
PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED
```

## Spec-coverage review

Every design requirement has an implementation task:

```text
Spec §§1–3 purpose, frozen boundary, four candidates
  -> Task 1 frozen inputs / exact candidate inventory

Spec §4 exact microscopic q-fiber objects
  -> Task 3 exact inherited fiber model

Spec §5 Gate A typed/common carrier
  -> Task 2 certified typed-carrier graph

Spec §6 Gate B fixed-q evaluation
  -> Task 3 exact q-fiber compatibility

Spec §7 Gate C definability/naturality
  -> Task 4 exact finite-action/equivariance gate

Spec §8 Gate D uniqueness/countermodels
  -> Task 5 canonical relation signatures and countermodels

Spec §9 Gate E no-choice audit
  -> Task 6 strict per-candidate pipeline

Spec §§10–11 statuses and mechanical precedence
  -> Task 6 global adjudicator

Spec §12 six required controls
  -> Tasks 2, 4, 5, and 6 synthetic controls

Spec §13 deterministic evidence model
  -> Task 1 hash-pinned candidate inventory

Spec §§14–16 firewall, ledger, next-step mapping
  -> Task 7 deterministic result ledger and README

Spec §17 verification standard
  -> Task 9 exact-head 604-test CI and delivery

Spec §18 interpretation discipline
  -> Tasks 7–9 claim-boundary assertions and gravity-blind presentation

Offline presentation continuity
  -> Task 8 self-contained HTML and 24-second H.264 replay
```

No spec requirement is missing a task.

## Placeholder scan

The superseded shorthand draft was deleted. The authoritative implementation plan was checked for the writing-plans red flags:

```text
TODO            : 0 matches
TBD             : 0 matches
implement later : 0 matches
Similar to Task : 0 matches
fill in         : 0 matches
```

Occurrences of `...` in the authoritative plan are Python variadic type syntax such as `tuple[str, ...]`, not omitted implementation content.

## Interface/type consistency review

The authoritative interfaces are completed below. These helper names are part of the implementation contract even where the main plan first introduced them inside tests.

### Task 2 — `typed_carrier_graph.py`

In addition to the dataclasses in the plan, define:

```python
class CarrierGraph:
    def add_edge(self, edge: TypedEdge) -> None: ...
    def add_untyped_note(self, text: str) -> None: ...
    def nodes(self) -> tuple[str, ...]: ...
    def certified_paths(self, source: str, target: str,
                        real_only: bool = True) -> tuple[tuple[TypedEdge, ...], ...]: ...
    def has_certified_path(self, source: str, target: str,
                           real_only: bool = True) -> bool: ...


def synthetic_supplied_embedding_graph() -> CarrierGraph: ...
def synthetic_common_parent_graph() -> CarrierGraph: ...
```

The ellipses above are Python signature notation in this self-review, not placeholders for behavior: the main plan defines their exact semantic requirements. `certified_paths()` returns only paths whose edges use certifying relation classes and, when `real_only=True`, contain no synthetic edges.

### Task 3 — `exact_fiber.py`

The interface includes the control used by the test:

```python
def noncycle_control_preserves_q(case: FiberCase, edge_index: int) -> bool: ...
```

It changes exactly one inherited edge coefficient by `+1`, computes the resulting q through pinned v15.29 `apply_B1()`, and compares q tuples exactly.

### Task 4 — `naturality.py`

The test/control helpers are authoritative:

```python
def synthetic_swap_counterexample() -> tuple[FiniteRelation, FiniteAction]: ...
def synthetic_equivariant_control() -> tuple[FiniteRelation, FiniteAction]: ...
def break_multiplication_table(action: FiniteAction) -> FiniteAction: ...
```

The first uses a reduct-preserving representative swap that breaks a distinguishing relation. The second supplies a finite exact equivariant action. The third changes exactly one multiplication-table entry while leaving permutations unchanged, so the group-law checker must fail.

### Task 6 — `definability_gate.py`

The synthetic control helpers referenced by the tests are authoritative:

```python
def synthetic_no_common_carrier_control() -> DefinabilityAudit: ...
def synthetic_cross_candidate_multiple_control() -> DefinabilityAudit: ...
def synthetic_unique_natural_control() -> DefinabilityAudit: ...
def synthetic_supplied_embedding_control() -> DefinabilityAudit: ...
```

`synthetic_cross_candidate_multiple_control()` must contain two different candidate audits whose individually natural relation signatures are inequivalent. This is the regression that enforces global, cross-candidate multiplicity.

## Global multiplicity correction

The original planning draft incorrectly allowed a positive result when two different candidates each supplied a unique-but-inequivalent natural relation. That draft was superseded before implementation.

The authoritative rule is global:

```python
natural_signatures = {
    signature
    for candidate in natural_candidates
    for signature in candidate.relation_signatures
}

if len(natural_signatures) >= 2:
    status = 'MULTIPLE_NATURAL_RELATIONS_REMAIN'
```

Thus uniqueness must hold across the entire four-candidate frozen archive, not merely within one candidate origin.

## Exact inherited and evidence pins

v15.29 modules/ledger:

```text
provenance_inventory.py  81a41442d2f3b26817657ebb5f3dc948e62d14b2
fiber_model.py           e04cf0b24bbce6f908b83c9472c1f1b5639b7e8b
source_extension_gate.py 305af411792c08906ea8eed2c9aeba3de25be1cf
v15.29 RESULTS.json      0984a8238a7fd2a115ab673a3d4f23b0706c7b12
```

Candidate artifacts:

```text
V997 report              8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e
V923 report              9a1523c08d2b9b2c5ba2d298dfed3d563a750bec
V923 proof script        90f69d5101e0ab14488d8d25da326e7b94341375
v13.26 report            9917085b211ca0e1f4737082227f55097cc72b66
v14.04 report            e5d9566bfc86c801d2933e63453d1800f60a675b
v14.04 audit             1e75767a59a54b4fb7840ca355eb00845cf119e3
v15.01 report            1afbb7aebe384a1fb761f99fd2b040e595be1fa5
v15.01 audit             b8b6ef14b323659eb730b33bd3d36c99e7f03957
V1172 engine             78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d
```

## Test-count contract

The plan deliberately fixes counts before implementation:

```text
Task 1                                      4
Task 2                                      5
Task 3                                      4
Task 4                                      4
Task 5                                      4
Task 6/7 combined final test_gate count     5
Task 8                                      4
---------------------------------------------
v15.30 total                               30

v15.11–v15.27 inherited                   517
v15.28 inherited                           35
v15.29 inherited                           22
---------------------------------------------
inherited selected total                  574
v15.30 selected                            30
---------------------------------------------
exact-head selected total                 604
```

Task 7 replaces one earlier Gate test with the final ledger-schema/boundary test rather than adding a sixth Gate test.

## Scientific boundary review

The plan never invokes the v15.28 coupling solver as part of v15.30 adjudication. It never evaluates a gravity canary or gravity observable. The following remain false for every real v15.30 result:

```text
new_source_semantics_axiom_added
coupling_solver_reopened
gravity_observables_evaluated
uses_holonomy_selector
uses_newton_or_gr
uses_metric_selector
uses_pruning_as_selector
uses_entropy_as_selector
uses_physical_time
signal_of_life
gravity_canary_certified
physical_gravity_derived
```

Even `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED` advances only to a separate provenance-action / representation-readiness gate.

## Self-review status

```text
spec coverage            : COMPLETE
placeholder scan         : CLEAN
interface consistency    : COMPLETE WITH PINS ABOVE
global multiplicity rule : CORRECTED BEFORE IMPLEMENTATION
candidate scope           : EXACTLY FOUR
inherited pins            : COMPLETE
new-test target           : 30
selected-regression target: 604
scientific implementation: NOT STARTED
```
