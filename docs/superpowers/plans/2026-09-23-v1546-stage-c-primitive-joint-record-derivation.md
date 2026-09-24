# v15.46 Stage C Primitive Joint-Record Derivation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine mechanically whether the audited frozen retained/pruning ontology uniquely derives a quantum joint-record representation up to already-earned gauge.

**Architecture:** Build a read-only, hash-pinned primitive contract first. Represent only information actually present in that contract, then construct exact alternative realizations when permitted. A separate verifier checks constraint satisfaction and earned-gauge equivalence before a final adjudicator emits one of the four preregistered verdicts.

**Tech Stack:** CPython 3.13.5 standard library; exact integer/Fraction arithmetic; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1546-stage-c-primitive-joint-record-derivation.md`

## Global Constraints

- No v15.39 assumed incidence source may be used as evidence for quantum-carrier derivation.
- No v15.43-v15.45 curvature output, gravity target, continuum target or empirical fit may select a representation.
- No maximum-entropy, minimum-norm, spectral-edge or convenient-completion selector.
- Quantum-site relabeling is gauge only when the frozen retained ontology earns the cross-domain identification.
- Missing representation data never imply a zero source.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.
- All predecessor evidence is read-only and hash-pinned.
- Every implementation task follows RED -> observed failure -> minimal GREEN -> complete current-suite verification.

## Review Focus

1. A changed predecessor byte must fail before semantic adjudication.
2. A neutral density operator must not be allowed to select a tensor factorization.
3. Two rigid sorts must not be identified merely because each has trivial internal automorphism.
4. An isomorphism introduced only by the Stage-C implementation must not count as earned gauge.
5. A nonuniqueness witness must satisfy every frozen constraint under the same contract, rather than weakening constraints between realizations.

---

### Task C1: Freeze the primitive contract

**Files:** create `stage_c_contract.py`, `test_stage_c_contract.py`, and `docs/STAGE_C_INPUTS.json` inside the v15.46 demo.

**Interfaces:** `load_contract(root: Path) -> dict`, with retained sort, quantum sort, cross-domain relations, earned gauge, constraints and source receipts.

- [ ] Write RED tests for exact source pins, source drift, the v15.09 cross-domain boundary, and exclusion of later curvature/source assumptions.
- [ ] Run `python -m unittest -v test_stage_c_contract`; require missing-module RED.
- [ ] Implement the minimal byte-pinned contract loader using only predecessor statements.
- [ ] Generate and byte-replay canonical `STAGE_C_INPUTS.json`.
- [ ] Run all current v15.46 tests and commit only when prior Stage A/B/B2 remains green.

### Task C2: Exact representation family

**Files:** create `stage_c_representations.py` and `test_stage_c_representations.py`.

**Interfaces:** `candidate_family(contract) -> tuple[dict,...]`; each candidate records carrier dimension, factorization/inclusions, state descriptor, overlaps, provenance and assumptions.

- [ ] RED-test neutral-state factorization blindness, absence of an unearned factorization selector, and strict separation of dimension 32 from 125.
- [ ] Observe missing-module RED.
- [ ] Implement exact integer factorization enumeration and symbolic neutral-state descriptors; no floating fit.
- [ ] Add the v15.09 rigid-two-sort control: internal rigidity does not create a node-site dictionary.
- [ ] Run C1+C2 and all prior v15.46 tests; commit.

### Task C3: Nonuniqueness witness search

**Files:** create `stage_c_nonuniqueness.py`, `test_stage_c_nonuniqueness.py`, and on a valid witness `docs/STAGE_C_WITNESS.json`.

**Interfaces:** `find_witness(contract) -> dict` with left/right realizations, shared constraints, gauge test and status.

- [ ] RED-test that both sides satisfy the identical frozen constraints and that candidate-specific added selectors invalidate a witness.
- [ ] Observe RED.
- [ ] Search first for the smallest exact structural witness: two inequivalent node-site bijection expansions of the same rigid two-sort reduct, or two compatible factorizations when no selector exists.
- [ ] Require an explicit demonstration that the relation between sides is not in earned gauge.
- [ ] Freeze/replay the witness, run the complete current suite, and commit.

### Task C4: Independent constraint/gauge verifier

**Files:** create `stage_c_verify.py` and `test_stage_c_verify.py`.

**Interfaces:** `verify_witness(contract, witness) -> dict`. It must not call the search implementation.

- [ ] RED mutation tests for changed pin, changed dimension, omitted constraint, invented cross-domain relation, newly declared gauge, and identical left/right realization.
- [ ] Observe RED.
- [ ] Implement independent exact contract/constraint/distinction/gauge checks.
- [ ] Verify the frozen witness without importing search internals.
- [ ] Run the complete v15.46 suite and commit.

### Task C5: Mechanical adjudication and exact-head CI

**Files:** create `stage_c_gate.py`, `test_stage_c_gate.py`, `docs/STAGE_C_RESULTS.json`, and `.github/workflows/uqcf-v1546-stage-c-derivation.yml`; update the v15.46 README.

**Interface:** `adjudicate(contract, witness, verification) -> dict`. Allowed verdicts only: `UNIQUE_UP_TO_EARNED_GAUGE`, `REPRESENTATION_NONUNIQUE`, `NO_REPRESENTATION_DERIVED`, `ILL_TYPED`.

- [ ] RED-test unknown verdict rejection, physical-gravity/source-correspondence promotion, skipped tests and noncanonical output.
- [ ] Observe RED.
- [ ] Implement the minimal frozen decision table. A verified inequivalent pair yields `REPRESENTATION_NONUNIQUE`; do not invent a fallback.
- [ ] Add exact-head CI: CPython 3.13.5; every v15.46 test; Stage A/B/B2/C replay; compile; v15.44/v15.45 tree hashes; clean tree; exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, add a receipt commit and PR #57 comment identifying the exact executed head; do not call the receipt commit scientifically certified.

## Final interpretation rule

If Stage C returns `REPRESENTATION_NONUNIQUE`, the permissible claim is: **the audited frozen ontology does not uniquely derive the joint quantum record up to its earned gauge**. The next scientific action is a genuinely new primitive principle capable of breaking that representation freedom, preregistered as a new assumption before downstream geometry.

If Stage C returns `UNIQUE_UP_TO_EARNED_GAUGE`, only then may v15.46 proceed to overlap/support/occurrence/coupling admission. Neither result is itself a gravity result.
