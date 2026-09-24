# v15.54 Operational Nonclassicality Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the certified v15.53 recoverability obstruction survives an exact operational nonclassicality test against a frozen finite classical comparator class.

**Architecture:** Build a new v15.54 finite operational family with exact rational probability tables, a pre-frozen operational witness, an exact bounded classical hidden-state comparator, target-blind retained reduction, structural equivalence, and an independent verifier that reimplements every semantic check. v15.53 remains an immutable predecessor/control.

**Tech Stack:** Python 3.13.5 standard library only; fractions.Fraction; finite exhaustive enumeration; unittest; GitHub Actions ubuntu-24.04.

**Spec:** `docs/superpowers/specs/2026-09-24-v1554-operational-nonclassicality-gate.md`

## Global Constraints

- Exact arithmetic only for the primary scientific verdict; no floating tolerance.
- Freeze witness, comparator class, retained reduction, and structural equivalence before candidate enumeration.
- Noncommutativity alone cannot certify nonclassicality.
- A positive gate requires an operational probability-table witness plus exact absence of a comparator in the frozen classical class.
- The ontic-state bound is explicitly scoped and cannot be promoted to all hidden-variable models.
- v15.53 scientific files remain byte-preserved.
- Independent verifier cannot call producer semantic functions.
- `source_correspondence=NOT_EVALUATED`; `Pillar_3=OPEN`; no physical source, gravity, geometry, continuum, empirical, fundamental-time, dark-matter, or universal-quantum-derivation claim.
- Inherited v15.46-v15.53 discovered suites remain regression gates.

## Review Focus

- A noncommuting permutation control must remain classically reproducible and fail the nonclassical certification gate.
- Classical comparator enumeration must be complete under the frozen ontic bound, including deterministic extremal response/transition maps needed for convex mixtures.
- Exact probability normalization must survive JSON serialization without silently converting rational values to floats.
- Operational relabelings must transform both candidate tables and witness contexts consistently rather than changing the verdict.
- Failure to find a comparator at the frozen bound must never be worded as exclusion of arbitrary-size classical models.

---

### Task 1: Freeze v15.54 contract and authoritative RED runner

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.54-operational-nonclassicality-gate/nonclassicality_contract.py`
- Create: `.../test_nonclassicality_contract.py`
- Create: `.github/workflows/uqcf-v1554-nonclassicality.yml`

**Interfaces:**
- Consumes exact Git blob pins for v15.53 `docs/RESULTS.json`, v15.53 contract, and v15.54 spec.
- Produces `load_contract(root: Path) -> dict`, exact primary verdicts, exact ontic bound, frozen witness definition, forbidden fields, claim firewall.

- [ ] **Step 1: Write RED contract tests**
  - schema exactly `uqcf-v1554-nonclassicality-contract-v1`;
  - v15.53 predecessor pins exact;
  - v15.53 verdict required to equal `CERTIFIED_FAMILY_OBSTRUCTION_WITNESS`;
  - comparator ontic bound is a positive fixed integer;
  - witness contexts/outcomes and exact rational threshold frozen;
  - five primary verdicts exactly match the spec;
  - forbidden `nonclassical`, `target_class`, copied retained readout, post-result gauge/selector fields;
  - claim firewall exact.

- [ ] **Step 2: Run RED**
Run: `python -m unittest -v test_nonclassicality_contract`
Expected: missing `nonclassicality_contract` import.

- [ ] **Step 3: Implement literal frozen contract and Git-blob verification**
No candidate family or witness evaluation.

- [ ] **Step 4: Run GREEN**
Expected: all Task-1 tests pass.

- [ ] **Step 5: Commit**
`feat(uqcf): freeze v15.54 operational nonclassicality contract`

### Task 2: Exact operational candidate family and admissibility

**Files:**
- Create: `.../operational_family.py`
- Create: `.../test_operational_family.py`

**Interfaces:**
- Produces `enumerate_raw_candidates(contract) -> tuple[dict,...]` and `check_admissibility(contract,candidate) -> dict`.
- Exact probabilities serialized as numerator/denominator integer pairs; internal computation uses `Fraction`.

- [ ] **Step 1: Write RED tests**
Cover deterministic enumeration; normalization; nonnegative probabilities; context/outcome completeness; composition/typing; duplicate rejection; forbidden status fields; ID invariance; JSON round trip; malformed rational denominator rejection.

- [ ] **Step 2: Run RED**
Expected: missing module/functions.

- [ ] **Step 3: Implement minimal finite family**
Include:
  - an explicit classical/permutation positive control descended from v15.53;
  - a noncommuting-but-operationally-classical control;
  - the smallest preregistered operational candidate set needed to exercise W.
Do not tune candidates after observing comparator results.

- [ ] **Step 4: Run GREEN**
Expected: all Task-2 tests pass.

- [ ] **Step 5: Commit**
`feat(uqcf): add exact v15.54 operational family`

### Task 3: Operational witness functional W

**Files:**
- Create: `.../operational_witness.py`
- Create: `.../test_operational_witness.py`

**Interfaces:**
- Produces `evaluate_witness(contract,candidate) -> dict` from registered probabilities only.

- [ ] **Step 1: Write RED tests**
Cover exact threshold behavior; candidate-ID blindness; internal-operation-label blindness; allowed preparation/outcome/context relabeling invariance; probability-table mutation closing W; noncommuting permutation control failing W; witness evaluation refusing missing contexts.

- [ ] **Step 2: Run RED**
Expected: missing witness module.

- [ ] **Step 3: Implement W exactly**
Use only the frozen registered probability cells and exact rational arithmetic.

- [ ] **Step 4: Run GREEN**
Expected: all Task-3 tests pass.

- [ ] **Step 5: Commit**
`feat(uqcf): implement exact v15.54 operational witness`

### Task 4: Exact classical comparator class

**Files:**
- Create: `.../classical_comparator.py`
- Create: `.../test_classical_comparator.py`

**Interfaces:**
- Produces:
  - `enumerate_extremal_models(contract,table_schema) -> tuple`
  - `find_classical_comparator(contract,operational_table) -> dict`
- Result exactly `CLASSICAL_COMPARATOR_FOUND` or `NO_COMPARATOR_IN_FROZEN_CLASS`, with concrete model or exact infeasibility record.

- [ ] **Step 1: Write RED tests**
Cover explicit classical positive control; v15.53 C4/V4-derived operational controls; noncommuting permutation control; known table outside frozen comparator class; normalization/negativity rejection; ontic-bound enforcement; deterministic extremal coverage; permutation invariance of ontic labels.

- [ ] **Step 2: Run RED**
Expected: missing comparator module.

- [ ] **Step 3: Implement exact finite comparator search**
Enumerate deterministic extremal preparation/transition/response assignments under the frozen bound and solve convex membership exactly using rational Gaussian elimination / finite convex-combination search appropriate to the preregistered small table.

- [ ] **Step 4: Run GREEN**
Expected: all Task-4 tests pass and classical controls return concrete comparators.

- [ ] **Step 5: Commit**
`feat(uqcf): add exact bounded classical comparator`

### Task 5: Retained reduction and structural target equivalence

**Files:**
- Create: `.../retained_reduction.py`
- Create: `.../target_equivalence.py`
- Create: `.../test_reduction_equivalence.py`

**Interfaces:**
- Produces `reduce_to_retained(contract,candidate)->dict`, `are_equivalent(contract,left,right)->bool`, `canonical_class_key(contract,candidate)->tuple`.

- [ ] **Step 1: Write RED tests**
Cover exact seven-field retained domain unless explicitly versioned by contract; copied readout ignored/rejected; target/witness blindness; source relabeling covariance; self/symmetric/transitive equivalence; allowed operational relabelings; omitted/invented isomorphism controls; JSON invariance.

- [ ] **Step 2: Run RED**
Expected: missing modules.

- [ ] **Step 3: Implement target-blind reduction and exhaustive structural maps**

- [ ] **Step 4: Run GREEN**
Expected: all Task-5 tests pass.

- [ ] **Step 5: Commit**
`feat(uqcf): derive v15.54 retained and target classes`

### Task 6: Producer adjudication

**Files:**
- Create: `.../nonclassicality_search.py`
- Create: `.../test_nonclassicality_search.py`

**Interfaces:**
- Produces `search_frozen_family(contract)->dict`.

- [ ] **Step 1: Write RED tests**
Require exactly one primary verdict; full candidate accounting; no early-stop before comparator/class accounting; positive verdict only when equal retained readout + distinct target classes + W pass + no comparator; classically reproducible obstruction gets its dedicated verdict; no-witness result fabricates no pair; enumeration/ID invariance; scoped interpretation text.

- [ ] **Step 2: Run RED**
Expected: missing search module.

- [ ] **Step 3: Implement exhaustive producer search**

- [ ] **Step 4: Run GREEN**
Record actual producer verdict without calling it certified.

- [ ] **Step 5: Commit**
`feat(uqcf): adjudicate frozen v15.54 nonclassicality family`

### Task 7: Independent semantic verifier

**Files:**
- Create: `.../verify_nonclassicality.py`
- Create: `.../test_verify_nonclassicality.py`

**Interfaces:**
- Consumes frozen contract and raw candidate literals only.
- Independently reimplements admissibility, W, comparator search, retained reduction, equivalence, and final search.

- [ ] **Step 1: Write RED adversarial tests**
Cover all 18 mandatory controls from the spec, plus monkeypatch producer functions to prove verifier independence. Explicitly assert v15.53 permutation witness/control is classically reproducible under the new gate.

- [ ] **Step 2: Run RED**
Expected: missing verifier.

- [ ] **Step 3: Implement independent verifier**
No producer semantic imports.

- [ ] **Step 4: Run GREEN**
Expected: producer/verifier agreement on frozen family and all adversarial controls pass.

- [ ] **Step 5: Commit**
`feat(uqcf): independently verify v15.54 nonclassicality gate`

### Task 8: Authoritative certification and publication

**Files:**
- Modify: `.github/workflows/uqcf-v1554-nonclassicality.yml`
- Create only after code-head GREEN: `.../docs/RESULTS.json`, `.../docs/CI_RECEIPT.md`, `.../README.md`

**Interfaces:**
- Produces exact-head evidence and scoped scientific adjudication.

- [ ] **Step 1: Extend workflow**
Require exact checkout; all v15.54 discovered tests; each inherited v15.46-v15.53 suite >0 and green; independent replay twice byte-identical; compilation; predecessor scientific-byte preservation; canonical JSON output.

- [ ] **Step 2: Push code head and inspect authoritative run**
Do not freeze result docs before SUCCESS.

- [ ] **Step 3: Debug any failure via reproducing RED test**
No symptom patches.

- [ ] **Step 4: Freeze independent verdict exactly into RESULTS.json**

- [ ] **Step 5: Write receipt and README**
Record SHA, run/job, counts, result hash, comparator bound, exact scientific scope, and all negative claim boundaries.

- [ ] **Step 6: Run final documentation head**
Stored RESULTS must compare byte-for-byte to independent replay.

- [ ] **Step 7: Update PR #57**
Keep draft unless merge separately approved.

- [ ] **Step 8: Commit**
`docs(uqcf): record v15.54 operational nonclassicality verdict`

## Plan Self-Review

- Spec coverage: operational family, W, exact comparator, retained reduction, target equivalence, independent verification, controls, CI, and claim firewall all map to explicit tasks.
- Placeholder scan: no placeholder markers or unspecified implementation steps remain.
- Type consistency: all probabilities enter semantic calculations as exact rationals; producer and verifier consume the same frozen raw schema but do not share semantic implementations.
- Review Focus: each listed failure mode is assigned to Tasks 3, 4, 5, or 7.
- Scope discipline: comparator nonexistence is explicitly limited to the frozen ontic bound unless a later theorem proves compression.
