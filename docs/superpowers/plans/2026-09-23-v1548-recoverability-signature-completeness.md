# v15.48 Recoverability-Signature Cross-Domain Completeness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the complete preregistered recoverability signature uniquely fixes the retained↔quantum correspondence, or whether the problem is nonselective or ill typed.

**Architecture:** First freeze a typed signature schema independently on the retained and quantum sides. Then compute both signature families without any cross-domain labels, exhaustively test all 120 bijections for exact signature preservation, quotient survivors only by earned gauge, and independently reconstruct the result before final adjudication.

**Tech Stack:** CPython 3.13.5 standard library; exact integers/Fractions where applicable; deterministic tuples/dicts; unittest; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1548-recoverability-signature-completeness.md`

## Global Constraints

- No score maximization/minimization over recoverability, fidelity, CMI, entropy, or any scalar proxy.
- No sorted-rank matching.
- No post-result feature/coordinate selection.
- No manually supplied node/site dictionary.
- No curvature, holonomy, source-response, Newton/ADM/Einstein/continuum target.
- No physical time or pruning-rate selector.
- No PCA/SVD/minimum-norm/spectral-edge rule.
- Signatures are constructed independently within each sort before any bijection is evaluated.
- Only predecessor-earned gauge may quotient survivors.
- If common typing is not independently justified, verdict is `RECOVERABILITY_SIGNATURE_ILL_TYPED`.
- Source correspondence remains `NOT_EVALUATED`; Pillar 3 remains `OPEN`.

## Review Focus

1. Hidden cross-domain labels entering signature construction through fixture ordering.
2. Retained and quantum coordinates being compared despite lacking a common operational type.
3. Duplicate signatures being broken by list order rather than preserved as ambiguity.
4. A scalar summary silently replacing the complete relational signature.
5. A claimed unique mapping depending on a signature coordinate chosen only after seeing results.

---

### Task 1: Freeze typed signature schemas

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.48-recoverability-signature-completeness/signature_contract.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.48-recoverability-signature-completeness/test_signature_contract.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.48-recoverability-signature-completeness/docs/INPUTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.48-recoverability-signature-completeness/README.md`

**Interfaces:**
- Produces `load_contract(root: Path) -> dict`.
- Contract records source pins, retained signature coordinates, quantum signature coordinates, common typing map or explicit absence, earned gauge, prohibited inputs, and one preregistered holdout relation when available.

- [ ] Write RED tests for exact source pins, zero cross-domain labels, complete coordinate manifest, explicit type audit, prohibited downstream inputs, and fail-closed source drift.
- [ ] Run focused tests and require missing-module RED.
- [ ] Implement minimal contract loader from pinned predecessor evidence only.
- [ ] If no common type is certified, encode that fact explicitly rather than inventing a metric.
- [ ] Canonically generate/replay `docs/INPUTS.json`; run inherited v15.47/v15.46 regressions; commit.

### Task 2: Compute retained and quantum signatures independently

**Files:**
- Create: `retained_signatures.py`
- Create: `quantum_signatures.py`
- Create: `test_signatures.py`
- Create: `docs/RETAINED_SIGNATURES.json`
- Create: `docs/QUANTUM_SIGNATURES.json`

**Interfaces:**
- `compute_retained_signatures(contract) -> tuple[dict,...]`
- `compute_quantum_signatures(contract) -> tuple[dict,...]`

- [ ] RED-test permutation covariance within each sort, deterministic output, coordinate completeness, duplicate-signature preservation, and no foreign-sort identifiers.
- [ ] Observe RED.
- [ ] Implement retained signatures using only retained-side relations.
- [ ] Implement quantum signatures using only quantum operational relations.
- [ ] Reject scalarization unless it is provably information-equivalent to the full tuple.
- [ ] Freeze both ledgers before any matching; run full current suite; commit.

### Task 3: Exhaustive signature-preserving bijection gate

**Files:**
- Create: `signature_match.py`
- Create: `test_signature_match.py`
- Create: `docs/MATCHES.json`

**Interfaces:**
- `enumerate_matches(contract, retained, quantum) -> dict`
- Output contains all 120 candidate bijections, exact rejection reasons, survivor set, and earned-gauge quotient.

- [ ] RED-test exact enumeration of all 120 bijections.
- [ ] RED-test that duplicate signatures preserve multiple survivors.
- [ ] RED-test that missing common typing yields `ILL_TYPED` rather than arbitrary comparison.
- [ ] RED-test relabeling covariance of the survivor set.
- [ ] RED-test holdout relation prediction if the contract supplies a holdout.
- [ ] Observe RED.
- [ ] Implement exact signature equality filtering only; no distance or score.
- [ ] Freeze/replay `docs/MATCHES.json`; run current suite; commit.

### Task 4: Independent reconstruction and hostile controls

**Files:**
- Create: `verify_signatures.py`
- Create: `test_verify_signatures.py`
- Create: `docs/VERIFICATION.json`

**Interface:**
- `verify(contract, retained_ledger, quantum_ledger, match_ledger) -> dict`
- Must not import Task-2 signature constructors or Task-3 matcher.

- [ ] RED mutation tests for omitted coordinate, reordered-only tiebreak, altered signature entry, invented common type, omitted/duplicated bijection, unearned gauge, holdout leakage, and downstream selector contamination.
- [ ] Observe RED.
- [ ] Independently reconstruct coordinate completeness, typing status, exact signature preservation, survivor accounting, relabeling covariance and gauge quotient.
- [ ] Freeze/replay verification ledger; run full suite; commit.

### Task 5: Mechanical verdict and exact-head certification

**Files:**
- Create: `gate.py`
- Create: `test_gate.py`
- Create: `docs/RESULTS.json`
- Create: `docs/CI_RECEIPT.md`
- Create: `.github/workflows/uqcf-v1548-recoverability-signature.yml`
- Modify: v15.48 README and PR #57 transition documentation.

**Interface:**
- `adjudicate(contract, verification) -> dict`

- [ ] RED-test all four frozen verdicts and reject unknown verdicts.
- [ ] RED-test physical-gravity/source-correspondence promotion.
- [ ] RED-test noncanonical output and skipped/expected-failure acceptance.
- [ ] Observe RED.
- [ ] Implement frozen decision table:
  - missing common type -> `RECOVERABILITY_SIGNATURE_ILL_TYPED`
  - zero survivors despite well-typed complete signatures -> `RECOVERABILITY_SIGNATURE_INCONSISTENT`
  - one earned-gauge class -> `RECOVERABILITY_SIGNATURE_SELECTS_REPRESENTATION_CLASS`
  - more than one -> `RECOVERABILITY_SIGNATURE_STILL_NONSELECTIVE`
- [ ] Add exact-head CI: CPython 3.13.5; all v15.48 tests; inherited v15.47/v15.46 regressions; canonical replay; compileall; predecessor hash/tree preservation; clean tree; exact `GITHUB_SHA`.
- [ ] Require zero failures/errors/skips/expected failures.
- [ ] After successful CI only, commit receipt and update PR #57 with exact executed head and narrow interpretation.

## Interpretation rule

A selecting result is conditional on the explicitly new recoverability-signature preservation principle. It does not retroactively derive that bridge from earlier UQCF-GEM.

An `ILL_TYPED` result is scientifically substantive: it means even the proposed complete-invariant comparison lacks a certified cross-domain equality relation and therefore cannot lawfully select a representation.

A nonselective result means the full tested recoverability pattern still leaves representation freedom.

No result here by itself establishes a physical source law, gravity, Einstein dynamics, or continuum GR.
