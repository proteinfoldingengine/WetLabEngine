# v15.51 Minimal Quantum-Origin Primitive Classification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether any preregistered pre-quantum primitive package is minimally sufficient to originate the quantum-side structure missing in v15.50, without supplying Hilbert/matrix structure as input.

**Architecture:** Freeze an explicit assumption lattice and output contract first. Evaluate packages from strict-weaker to stronger using abstract finite operational models, classify all lawful realizations including classical alternatives, test strict subpackages for minimality, independently reconstruct the classification, then mechanically adjudicate.

**Tech Stack:** CPython 3.13.5 standard library; exact finite algebra/relations and Fractions; itertools; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1551-minimal-quantum-origin-primitive.md`

## Global Constraints

- Baseline (U_0) is the certified v15.50 target-blind ordered-recoverability-incidence object.
- No Hilbert space, qubits, matrices, tensor factors, Born rule, density operators, CPTP maps, target dimensions, or node/site dictionary as primitive data.
- No curvature/source/gravity/GR/continuum target.
- No entropy/minimum-norm/spectral selector.
- Minimality means strict assumption inclusion, not a subjective complexity score.
- Classical realizations and alternative representation theories must remain visible.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.

## Candidate lattice

Freeze packages:
- `P0`: (U_0) only.
- `P1`: (P0) + composition-with-interference primitive.
- `P2`: (P0) + convex operational distinguishability.
- `P3`: (P0) + noncommutative involutive event composition.
- `P12`, `P13`, `P23`: pairwise joins.
- `P123`: join of the three weak classes.
- `P4`: `P123` + purification/local-tomography package.

No package may be inserted after exposure without a new version.

---

### Task 1: Freeze assumption lattice and output contract

**Files:** create `ResearchHistory/UQCF-GEM/demos/v15.51-minimal-quantum-origin-primitive/primitive_contract.py`, `test_primitive_contract.py`, `docs/INPUTS.json`, and `README.md`.

**Interface:** `load_contract(root: Path) -> dict`.

- [ ] RED-test exact v15.50/predecessor pins, complete package lattice, strict-subpackage relations, forbidden quantum primitives, required outputs, and downstream firewall.
- [ ] RED-test that no package contains target dimension/carrier/matrix/tensor data.
- [ ] Observe missing-module RED.
- [ ] Implement minimal hash-pinned contract and canonical input replay.
- [ ] Run inherited v15.50–v15.46 regressions; commit.

### Task 2: Enumerate lawful operational realizations package-by-package

**Files:** create `primitive_realizations.py`, `test_primitive_realizations.py`, and `docs/REALIZATIONS.json`.

**Interfaces:** `enumerate_realizations(contract, package_id) -> tuple[dict,...]`; `check_realization(contract,package_id,r) -> dict`.

- [ ] RED-test deterministic enumeration and assumption compliance for every frozen package.
- [ ] RED-test Hilbert/matrix/dimension smuggling rejection.
- [ ] RED-test that classical realizations remain classified as classical rather than “quantum.”
- [ ] RED-test noncommutativity/interference claims against explicit witnesses.
- [ ] Observe RED.
- [ ] Implement exact finite abstract realizations; no scores.
- [ ] Freeze/replay realization ledger; run full current suite; commit.

### Task 3: Quantum-origin output and representation classification

**Files:** create `quantum_origin.py`, `test_quantum_origin.py`, and `docs/ORIGIN_RESULTS.json`.

**Interfaces:** `derive_outputs(contract,package_id,realizations) -> dict`; `classify_representations(...) -> dict`.

- [ ] RED-test each required output: carrier/representation class, subsystem composition, recovery-capable operations, typed quantum leg.
- [ ] RED-test that a merely classical realization cannot satisfy quantum-origin sufficiency.
- [ ] RED-test alternative real/complex/quaternionic or other inequivalent representation classes where admitted.
- [ ] RED-test that multiple inequivalent realizations prevent uniqueness.
- [ ] Observe RED.
- [ ] Implement output derivation/classification without target dimensions.
- [ ] Freeze/replay results; commit.

### Task 4: Strict-subpackage minimality + independent verifier

**Files:** create `minimality.py`, `verify_quantum_origin.py`, `test_minimality.py`, `test_verify_quantum_origin.py`, and `docs/VERIFICATION.json`.

**Interfaces:** `minimal_packages(contract,origin_results) -> dict`; `verify(contract,realization_ledger,origin_ledger,minimality_ledger) -> dict`.

- [ ] RED-test that every claimed minimal package has all strict frozen subpackages checked and insufficient.
- [ ] RED-test incomparable successful minimal packages -> family nonunique.
- [ ] RED hostile mutations: hidden matrix data, dimension injection, classical relabelled as quantum, omitted realization, collapsed alternative representation, invented equivalence, downstream leakage.
- [ ] Observe RED.
- [ ] Independently reconstruct assumption inclusion, sufficiency and representation accounting without importing Task-2/Task-3 classifiers.
- [ ] Freeze/replay verification ledger; run full suite; commit.

### Task 5: Mechanical verdict and exact-head certification

**Files:** create `gate.py`, `test_gate.py`, `docs/RESULTS.json`, `docs/CI_RECEIPT.md`, and `.github/workflows/uqcf-v1551-quantum-origin.yml`; update README and PR #57.

**Interface:** `adjudicate(contract,verification) -> dict`.

- [ ] RED-test all four frozen verdicts and claim boundaries.
- [ ] Observe RED.
- [ ] Implement decision table:
  - candidate types ill-defined without quantum conclusions -> `QUANTUM_ORIGIN_CLASSIFICATION_ILL_TYPED`;
  - no tested package sufficient -> `TESTED_PRIMITIVES_INSUFFICIENT`;
  - >1 incomparable minimal successful packages -> `QUANTUM_ORIGIN_PRIMITIVE_FAMILY_NONUNIQUE`;
  - exactly one minimal successful package with all strict subpackages insufficient -> `MINIMAL_QUANTUM_ORIGIN_PRIMITIVE_IDENTIFIED`.
- [ ] Add exact-head CI on CPython 3.13.5: all v15.51 tests; inherited v15.50/v15.49/v15.48/v15.47/v15.46 regressions; canonical replay; compileall; predecessor preservation; clean tree; exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, commit receipt and update PR #57.

## Interpretation rule

Any identified primitive is minimal only within this frozen tested lattice. A package that permits both classical and genuinely quantum realizations without an additional selector is not sufficient to uniquely originate quantum structure.

No v15.51 result alone establishes a source law, gravity, Einstein dynamics, or continuum GR.
