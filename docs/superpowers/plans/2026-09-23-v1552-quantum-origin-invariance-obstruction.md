# v15.52 Quantum-Origin Invariance Obstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans task-by-task.

**Goal:** Certify or falsify an invariance obstruction to unique quantum origin within the frozen target-blind extension class E.

**Architecture:** Freeze E and its observable algebra first; compute complete finite source automorphism actions; construct explicit inequivalent quantum-origin witness pairs that are source-indistinguishable; independently prove the selector obstruction and search for separating counterexamples; mechanically adjudicate.

**Tech Stack:** CPython 3.13.5 standard library; finite permutations/relations; exact tuples/Fractions; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1552-quantum-origin-invariance-obstruction.md`

## Global constraints

- Claims only over frozen finite class E.
- No target labels/dimensions, Hilbert/matrix primitives, node/site dictionary, geometry/source/gravity/empirical selector.
- Source automorphisms must be complete for each fixture.
- Witness Q1/Q2 must be inequivalent under frozen earned quantum equivalence.
- Indistinguishability means equality on every preregistered E-observable.
- Any separating admissible observable falsifies that witness.
- Source correspondence NOT_EVALUATED; Pillar 3 OPEN.

### Task 1 — Freeze E, observables, equivalence, theorem contract

**Files:** create `ResearchHistory/UQCF-GEM/demos/v15.52-quantum-origin-invariance-obstruction/obstruction_contract.py`, `test_obstruction_contract.py`, `docs/INPUTS.json`, `README.md`.

- [ ] RED-test predecessor pins, explicit E field whitelist, observable algebra, earned equivalence, T1/T2/T3 text identifiers, forbidden selectors and downstream firewall.
- [ ] RED-test target dimension/labels/matrix fields rejected.
- [ ] Observe missing-module RED.
- [ ] Implement minimal hash-pinned contract and canonical input replay.
- [ ] Run inherited v15.51–v15.46 regressions; commit.

### Task 2 — Complete source automorphism action

**Files:** create `source_automorphisms.py`, `test_source_automorphisms.py`, `docs/AUTOMORPHISMS.json`.

- [ ] RED-test exhaustive permutation enumeration on frozen fixtures.
- [ ] RED-test relation/composition/refinement preservation.
- [ ] RED-test omitted/duplicate automorphism detection and relabeling covariance.
- [ ] Implement complete action and orbit partition.
- [ ] Freeze/replay ledger; commit.

### Task 3 — Explicit quantum-origin obstruction witness

**Files:** create `obstruction_witness.py`, `test_obstruction_witness.py`, `docs/WITNESS.json`.

- [ ] RED-test Q1/Q2 inequivalence under earned quantum equivalence.
- [ ] RED-test equality on every E-observable.
- [ ] RED-test differences in at least one required quantum-origin output.
- [ ] RED-test no target/downstream information used in witness construction.
- [ ] Search finite frozen witness family exhaustively.
- [ ] If none exists, record `OBSTRUCTION_WITNESS_NOT_FOUND`; do not manufacture one.
- [ ] Freeze/replay witness ledger; commit.

### Task 4 — Independent theorem verifier and counterexample search

**Files:** create `verify_obstruction.py`, `test_verify_obstruction.py`, `docs/VERIFICATION.json`.

- [ ] RED-test T1 mechanically: selector from E-invariant data is constant on E-indistinguishability classes.
- [ ] RED hostile mutations: omitted automorphism, altered observable, invented gauge, target label, randomized selector claimed as derivation.
- [ ] Independently enumerate all preregistered E-observables and search for one separating Q1/Q2.
- [ ] A separating observable falsifies the witness.
- [ ] Verify T2 only if witness survives.
- [ ] Record T3 narrowly as necessity of equivalence-breaking/type-enriching information.
- [ ] Freeze/replay verification; commit.

### Task 5 — Mechanical verdict and exact-head certification

**Files:** create `gate.py`, `test_gate.py`, `docs/RESULTS.json`, `docs/CI_RECEIPT.md`, `.github/workflows/uqcf-v1552-obstruction.yml`; update PR #57.

- [ ] RED-test all four frozen verdicts and claim boundaries.
- [ ] Implement decision table:
  - ill-defined E/equivalence -> `OBSTRUCTION_THEOREM_ILL_TYPED`;
  - E too weak for meaningful observable completeness -> `OBSTRUCTION_CLASS_TOO_WEAK`;
  - no valid witness -> `OBSTRUCTION_WITNESS_NOT_FOUND`;
  - complete automorphisms + valid inequivalent E-indistinguishable witness + T1/T2 verified + no separating counterexample -> `QUANTUM_ORIGIN_INVARIANCE_OBSTRUCTION_CERTIFIED`.
- [ ] Exact-head CI on CPython 3.13.5 with v15.52 and inherited v15.51–v15.46 suites, canonical replay, compileall, clean tree and predecessor preservation.
- [ ] After successful CI only, commit receipt and update PR #57.

## Interpretation

Certification would prove an obstruction only within E: source-invariant information cannot uniquely select distinctions it does not encode. It would establish that a future successful primitive must add equivalence-breaking/type-enriching information, not identify the physical primitive itself.
