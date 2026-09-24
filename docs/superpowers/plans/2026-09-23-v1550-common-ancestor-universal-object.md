# v15.50 Common-Ancestor / Universal-Object Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test whether one target-blind primitive ordered-recoverability object (U) can lawfully and uniquely determine both retained and quantum recoverability representations.

**Architecture:** Freeze the type and universal-property contract for (U) before constructing examples. Enumerate only target-blind (U) candidates, derive both legs independently, classify all factorizations modulo earned automorphism/gauge, and independently verify the result before mechanical adjudication.

**Tech Stack:** CPython 3.13.5 standard library; finite exact relations; itertools; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1550-common-ancestor-universal-object.md`

## Global Constraints

- (U) may contain only primitive occurrences, lineage/dependency incidence, admissible recovery composition, pruning-compatible refinement, and typed disjoint composition.
- No target labels, Hilbert carrier, node/site dictionary, geometry, source response, entropy extremum, physical time, or empirical target in (U).
- (F_R) and (F_Q) must be derived independently from the same (U).
- No lookup-table (F_Q), no (F_R^{-1}) plus supplied dictionary.
- Only earned automorphism/gauge may quotient factorizations.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.

## Review Focus

1. (U) secretly encoding the quantum target through labels/order.
2. Pair-object/product constructions disguised as universal objects.
3. (F_Q) requiring extra information absent from (U).
4. Target endomorphisms or (U)-automorphisms generating inequivalent factorizations.
5. Fixture ordering breaking structural degeneracy.

---

### Task 1: Freeze U type and universal-property contract

**Files:** create `ResearchHistory/UQCF-GEM/demos/v15.50-common-ancestor-universal-object/common_contract.py`, `test_common_contract.py`, `docs/INPUTS.json`, and `README.md`.

**Interface:** `load_contract(root: Path) -> dict`.

- [ ] RED-test exact predecessor pins, target-blind U schema, nonidentity composition, nontrivial refinement, disjoint composition, two independently typed targets, earned automorphisms/gauge, and prohibited fields.
- [ ] RED-test pair-object and target-label contamination.
- [ ] Observe missing-module RED.
- [ ] Implement minimal hash-pinned contract.
- [ ] Freeze/replay canonical inputs; run inherited v15.49–v15.46 regressions; commit.

### Task 2: Construct complete target-blind U candidate family

**Files:** create `common_candidates.py`, `test_common_candidates.py`, and `docs/CANDIDATES.json`.

**Interfaces:** `enumerate_candidates(contract) -> tuple[dict,...]`; `check_target_blindness(contract,u) -> dict`.

- [ ] RED-test deterministic complete enumeration within the frozen finite schema.
- [ ] RED-test rejection of pair-object, quantum labels, node/site dictionaries, target-specific dimensions, and downstream fields.
- [ ] RED-test relabeling covariance and degeneracy preservation.
- [ ] Observe RED.
- [ ] Implement exact enumeration with no scores.
- [ ] Freeze/replay candidate ledger; run full current suite; commit.

### Task 3: Derive both legs and classify factorizations

**Files:** create `common_factorizations.py`, `test_common_factorizations.py`, and `docs/FACTORIZATIONS.json`.

**Interfaces:** `derive_retained_leg(contract,u) -> dict`; `derive_quantum_legs(contract,u) -> tuple[dict,...]`; `classify_factorizations(contract,u,fr,fqs) -> dict`.

- [ ] RED-test that (F_R) and (F_Q) cannot inspect each other's target labels.
- [ ] RED-test that missing quantum typing yields INSUFFICIENT evidence, not a lookup repair.
- [ ] RED-test composition/refinement commutation on both legs where typed.
- [ ] RED-test target-endomorphism and U-automorphism freedom.
- [ ] Observe RED.
- [ ] Implement exact derivation/classification.
- [ ] Emit explicit inequivalent factorization witnesses when present.
- [ ] Freeze/replay factorization ledger; run full suite; commit.

### Task 4: Independent verifier

**Files:** create `verify_common_ancestor.py`, `test_verify_common_ancestor.py`, and `docs/VERIFICATION.json`.

**Interface:** `verify(contract,candidate_ledger,factorization_ledger) -> dict`; must not import Task-2/Task-3 enumerators.

- [ ] RED mutations for hidden target label, pair-object injection, altered composition/refinement, lookup-table quantum leg, invented gauge, omitted candidate/factorization, target-endomorphism collapse, and downstream leakage.
- [ ] Observe RED.
- [ ] Independently reconstruct target blindness, leg lawfulness and quotient accounting.
- [ ] Verify explicit insufficiency/nonuniqueness witness if present.
- [ ] Freeze/replay verification ledger; run full suite; commit.

### Task 5: Mechanical verdict and exact-head certification

**Files:** create `gate.py`, `test_gate.py`, `docs/RESULTS.json`, `docs/CI_RECEIPT.md`, and `.github/workflows/uqcf-v1550-common-ancestor.yml`; update README and PR #57.

**Interface:** `adjudicate(contract,verification) -> dict`.

- [ ] RED-test all four frozen verdicts and claim boundaries.
- [ ] Observe RED.
- [ ] Implement decision table: U not independently typed -> `COMMON_ANCESTOR_ILL_TYPED`; U typed but no lawful F_Q without extra information -> `COMMON_ANCESTOR_INSUFFICIENT`; multiple inequivalent factorizations -> `COMMON_ANCESTOR_NONUNIQUE`; exactly one earned-gauge class -> `COMMON_ANCESTOR_UNIQUE_UP_TO_EARNED_GAUGE`.
- [ ] Add exact-head CI on CPython 3.13.5: all v15.50 tests, inherited v15.49/v15.48/v15.47/v15.46 regressions, canonical replay, compileall, predecessor preservation, clean tree and exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, commit receipt and update PR #57 with exact executed head and narrow interpretation.

## Interpretation rule

The strongest negative result is `COMMON_ANCESTOR_INSUFFICIENT`: a lawful target-blind retained primitive (U) exists, but it does not contain enough information to originate the quantum leg. That would distinguish missing primitive quantum information from a mere missing direct bridge.

No v15.50 result alone establishes a physical source law, gravity, Einstein dynamics, or continuum GR.
