# v15.47 Cross-Domain Representation Functoriality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test whether the explicitly new retained-to-quantum functoriality axiom reduces the certified v15.46 representation freedom to one target-equivalence class without downstream selection.

**Architecture:** Freeze a small finite retained category and target representation category from hash-pinned inputs, then enumerate candidate object/morphism assignments rather than choosing one. A law checker filters candidates using identity/composition/monoidal/refinement requirements; a separate quotient stage computes surviving equivalence classes, and an independent verifier reconstructs the count before final adjudication.

**Tech Stack:** CPython 3.13.5 standard library; integer/Fraction exact arithmetic; itertools; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1547-cross-domain-representation-functoriality.md`

## Global Constraints

- Functoriality is explicitly a NEW ASSUMPTION, never back-propagated as a v15.46 derivation.
- No curvature, source-response, Newton/ADM/Einstein/continuum or empirical target may enter candidate generation or selection.
- No entropy/max-entropy, minimum-norm, PCA/SVD, spectral-edge or sorted-invariant selector.
- No hard-coded privileged node/site dictionary.
- No implicit 32<->125 identification, reshape or padding.
- Surviving candidates are quotiented only by target equivalence declared before execution.
- Failure to select does not imply a zero source.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.

## Review Focus

1. Candidate enumeration accidentally omits valid permutations and manufactures apparent uniqueness.
2. A manually privileged dictionary enters through fixture ordering rather than an explicit table.
3. The quotient treats an unearned permutation as target equivalence.
4. Refinement/composition checks are vacuous because the finite category lacks a nontrivial composable/refinement diagram.
5. The evaluator imports Stage-C witness labels or downstream geometry into candidate scoring.

---

### Task 1: Freeze finite source and target categories

**Files:** create a new `ResearchHistory/UQCF-GEM/demos/v15.47-cross-domain-representation-functoriality/` directory containing `functor_contract.py`, `test_functor_contract.py`, `docs/INPUTS.json`, and `README.md`.

**Interfaces:** `load_contract(root: Path) -> dict` returns source objects/morphisms, composition table, one nontrivial refinement square, target objects/equivalences, source pins and prohibited inputs.

- [ ] Write RED tests requiring exact predecessor pins, at least one nonidentity composition, a nontrivial refinement square, explicit target-equivalence declaration, and absence of downstream fields.
- [ ] Run the focused test and require missing-module RED.
- [ ] Implement the smallest finite contract supported by pinned retained structures; do not add morphisms merely to make functoriality selective.
- [ ] Canonically generate/replay `docs/INPUTS.json`.
- [ ] Run all v15.46 predecessor tests and commit.

### Task 2: Enumerate candidates and check functor laws

**Files:** create `functor_candidates.py`, `test_functor_candidates.py`, and `docs/CANDIDATES.json`.

**Interfaces:** `enumerate_candidates(contract) -> tuple[dict,...]`; `check_laws(contract,candidate) -> dict`.

- [ ] RED-test complete permutation enumeration, identity preservation, composition preservation, refinement commutation, dimension mismatch rejection and manual-dictionary contamination.
- [ ] Observe RED.
- [ ] Implement exhaustive deterministic enumeration with no candidate score.
- [ ] Add hostile controls: weak covariance must admit more than one candidate; a hard-coded dictionary must be classified `MANUAL_CROSS_DOMAIN_DICTIONARY`.
- [ ] Freeze/replay candidate results; run predecessor suite and commit.

### Task 3: Quotient surviving functors by declared target equivalence

**Files:** create `functor_classes.py`, `test_functor_classes.py`, and `docs/CLASSES.json`.

**Interfaces:** `surviving_classes(contract,candidates) -> dict` reports survivor count, equivalence-class count, members and invariants.

- [ ] RED-test that identity-only equivalence preserves distinct Stage-C mappings, while explicitly declared conjugate controls collapse only when the contract earns that equivalence.
- [ ] Observe RED.
- [ ] Implement exact equivalence relation and class enumeration.
- [ ] Require every enumerated survivor to occur in exactly one class and reject incomplete partitions.
- [ ] Freeze/replay class ledger; run complete current suite and commit.

### Task 4: Independent verifier

**Files:** create `verify_functoriality.py` and `test_verify_functoriality.py`.

**Interface:** `verify(contract,candidate_ledger,class_ledger) -> dict`. It must not import Task-2/Task-3 enumeration functions.

- [ ] RED mutation tests for omitted candidate, duplicated class member, invented target equivalence, broken composition, broken refinement, changed dimension and injected downstream selector.
- [ ] Observe RED.
- [ ] Independently reconstruct finite law satisfaction and equivalence membership from ledgers plus contract.
- [ ] Verify all survivors/classes and emit an exact verification ledger.
- [ ] Run complete suite and commit.

### Task 5: Mechanical verdict and exact-head certification

**Files:** create `gate.py`, `test_gate.py`, `docs/RESULTS.json`, `docs/CI_RECEIPT.md`, and `.github/workflows/uqcf-v1547-functoriality.yml`; update v15.47 README and PR #57 transition documentation.

**Interface:** `adjudicate(contract,classes,verification) -> dict`.

- [ ] RED-test the four frozen verdicts and reject unknown verdicts, physical-gravity promotion, source-correspondence promotion, skipped tests and noncanonical bytes.
- [ ] Observe RED.
- [ ] Implement decision table: zero well-typed survivors with structural conflict -> `FUNCTORIALITY_INCONSISTENT_WITH_FROZEN_RETAINED_STRUCTURE`; one verified equivalence class -> `FUNCTORIALITY_SELECTS_REPRESENTATION_CLASS`; more than one -> `FUNCTORIALITY_STILL_NONSELECTIVE`; missing required typing -> `FUNCTORIALITY_ILL_TYPED`.
- [ ] Add exact-head CI on CPython 3.13.5: all v15.47 tests, required v15.46 regressions, canonical ledger replay, compileall, predecessor tree/hash preservation, clean tree and exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, commit the receipt and update PR #57 with exact executed head and narrow scientific interpretation.

## Interpretation rule

If multiple verified equivalence classes survive, functoriality is insufficient and must not be described as the missing representation law.

If exactly one survives, the claim is conditional: **the explicitly new functoriality axiom selects one representation class in the frozen finite contract.** It does not show that the axiom was derived from earlier UQCF-GEM or that the class is physically correct.

No v15.47 outcome by itself establishes a source law, gravity, Einstein dynamics or continuum GR.
