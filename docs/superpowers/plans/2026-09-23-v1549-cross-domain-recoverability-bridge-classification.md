# v15.49 Cross-Domain Recoverability Bridge Classification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Classify all cross-domain recoverability bridges admitted by the frozen v15.49 axiom package and determine whether the bridge is unique up to earned gauge.

**Architecture:** Freeze explicit finite retained and quantum recoverability types first, then enumerate/derive bridge candidates without downstream information. Classify candidates modulo only earned gauge, independently verify the family and hostile mutations, then emit one preregistered verdict.

**Tech Stack:** CPython 3.13.5 standard library; exact finite relations/permutations; itertools; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1549-cross-domain-recoverability-bridge-classification.md`

## Global Constraints

- No implicit retained↔quantum coercion.
- No sorted-invariant matching, entropy/max-entropy/minimum norm, PCA/SVD, or spectral-edge selection.
- No manual node/site dictionary.
- No curvature, holonomy, source-response, Newton/ADM/Einstein/continuum or empirical target.
- No physical time or pruning-rate fitting.
- No post-result axiom weakening.
- Only predecessor-earned gauge may quotient bridges.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.

## Review Focus

1. Source/target structures that remain ill typed despite being represented by same-size finite sets.
2. A zero bridge passing covariance but violating the intended typed structure.
3. Target endomorphisms generating distinct bridges that are accidentally collapsed as gauge.
4. Candidate enumeration depending on fixture ordering.
5. Composition/refinement constraints being vacuous rather than genuinely exercised.

---

### Task 1: Freeze bridge domain, codomain and axiom contract

**Files:** create `ResearchHistory/UQCF-GEM/demos/v15.49-cross-domain-recoverability-bridge-classification/bridge_contract.py`, `test_bridge_contract.py`, `docs/INPUTS.json`, and `README.md`.

**Interface:** `load_contract(root: Path) -> dict`.

- [ ] RED-test exact predecessor pins, explicit source/codomain types, nontrivial composition and refinement relations, earned gauge, prohibited inputs, and absence of a privileged bridge.
- [ ] RED-test that mere equal cardinality does not certify common typing.
- [ ] Observe missing-module RED.
- [ ] Implement minimal hash-pinned contract.
- [ ] Canonically freeze/replay inputs; run inherited v15.48/v15.47/v15.46 regressions; commit.

### Task 2: Enumerate/derive complete admissible bridge family

**Files:** create `bridge_family.py`, `test_bridge_family.py`, and `docs/BRIDGES.json`.

**Interfaces:** `enumerate_bridges(contract) -> tuple[dict,...]`; `check_axioms(contract, bridge) -> dict`.

- [ ] RED-test complete finite enumeration where well typed, deterministic ordering, covariance, composition/order, neutrality, refinement, locality and disjoint-composition checks.
- [ ] RED-test rejection of zero bridge when it fails typed preservation.
- [ ] RED-test manual dictionary and downstream-selector contamination.
- [ ] Observe RED.
- [ ] Implement exact candidate generation with no scores.
- [ ] Freeze/replay bridge ledger; run full current suite; commit.

### Task 3: Classify modulo earned gauge and expose endomorphism freedom

**Files:** create `bridge_classes.py`, `test_bridge_classes.py`, and `docs/CLASSES.json`.

**Interface:** `classify(contract, bridges) -> dict`.

- [ ] RED-test that distinct target endomorphism compositions remain distinct unless the contract earns their equivalence.
- [ ] RED-test complete partition, no omitted/duplicated bridges, and no fixture-order tiebreak.
- [ ] RED-test invented gauge rejection.
- [ ] Observe RED.
- [ ] Implement exact quotient/class enumeration.
- [ ] Emit an explicit pair witness if more than one class survives.
- [ ] Freeze/replay class ledger; run full suite; commit.

### Task 4: Independent verifier

**Files:** create `verify_bridges.py`, `test_verify_bridges.py`, and `docs/VERIFICATION.json`.

**Interface:** `verify(contract, bridge_ledger, class_ledger) -> dict`. It must not import Task-2/Task-3 enumeration functions.

- [ ] RED mutations: changed pin/type, omitted axiom, broken composition, broken refinement, zero-map substitution, invented gauge, omitted bridge, duplicated class, downstream leakage.
- [ ] Observe RED.
- [ ] Independently reconstruct admissibility and quotient accounting.
- [ ] Verify any explicit nonuniqueness witness.
- [ ] Freeze/replay verification ledger; run complete suite; commit.

### Task 5: Mechanical verdict and exact-head certification

**Files:** create `gate.py`, `test_gate.py`, `docs/RESULTS.json`, `docs/CI_RECEIPT.md`, and `.github/workflows/uqcf-v1549-bridge-classification.yml`; update README and PR #57.

**Interface:** `adjudicate(contract, verification) -> dict`.

- [ ] RED-test all four frozen verdicts and claim boundaries.
- [ ] Observe RED.
- [ ] Implement decision table: missing typing -> `BRIDGE_ILL_TYPED`; zero admissible bridges with complete typing -> `BRIDGE_INCONSISTENT`; one earned-gauge class -> `BRIDGE_UNIQUE_UP_TO_EARNED_GAUGE`; more than one -> `BRIDGE_FAMILY_NONUNIQUE`.
- [ ] Add exact-head CI on CPython 3.13.5: all v15.49 tests, inherited v15.48/v15.47/v15.46 regressions, canonical replay, compileall, predecessor preservation, clean tree and exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, commit receipt and update PR #57 with exact executed head and narrow interpretation.

## Interpretation rule

Uniqueness is conditional on the explicitly new v15.49 bridge axiom package. Nonuniqueness identifies residual freedom in the bridge itself. Ill-typing stops enumeration rather than authoring a coercion.

No v15.49 outcome alone establishes a physical source law, gravity, Einstein dynamics or continuum GR.
