# v14.01 Global Admissibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the frozen global-consistency architecture canonically selects a nonzero source-dependent admissibility deformation or only an inequivalent family.

**Architecture:** Implement a small basis-independent graph/cochain audit. The native incidence map is tested against the cycle projector exactly. Then several covariant state/relational-weighted incidence maps are compared as candidate source→global-defect deformations. A separate positive control explicitly inserts a selected functional and coefficient to prove the gate can recognize uniqueness when it is added.

**Tech Stack:** Python 3.11, NumPy 2.4.6, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-12-v1401-global-admissibility-design.md`

## Global Constraints

- Pre-pruning only: no entropy/time primitive.
- No Newtonian or Einstein/ADM target enters construction or scoring.
- Do not use downstream residuals to select a deformation.
- Gate outcomes are exactly `DERIVED`, `NONUNIQUE`, or `NO_NATIVE_DEFORMATION`.
- Positive control must be labeled as added law, never as derivation.
- Scope all no-go claims to the audited frozen construction class.

---

### Task 1: Freeze RED checker

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.01/CHECKER.py`

**Interfaces:**
- Consumes: `run_audit()` from `admissibility_audit.py`.
- Produces: deterministic certification assertions and printed JSON.

- [ ] **Step 1:** Create a checker that imports `run_audit`; it must fail before the implementation file exists.
- [ ] **Step 2:** Assert seed `1401`, 256 trials, graph cycle dimension `3`, incidence leakage `<1e-12`, covariance/scaling errors `<2e-12`, at least two inequivalent weighted operators, and positive-control error `<2e-12`.
- [ ] **Step 3:** Require the gate outcome to be one of the three frozen outcomes and require branch-stop status for a non-derived result.
- [ ] **Step 4:** Commit the RED checker.

### Task 2: Implement basis-independent incidence and weighted-deformation audit

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.01/admissibility_audit.py`

**Interfaces:**
- Produces `run_audit() -> dict`.

- [ ] **Step 1:** Build the fixed 5-node / 7-edge oriented incidence matrix `B` and cycle projector `Pcyc = I - B.T @ pinv(B @ B.T) @ B`.
- [ ] **Step 2:** Verify the exact incidence-only identity numerically through `||Pcyc @ B.T||`.
- [ ] **Step 3:** Generate deterministic edge invariants `chi` and candidate weights `W1=diag(1+chi)`, `W2=diag(exp(chi))`, `W3=diag(1+chi**2)` with `chi` chosen so all weights are positive.
- [ ] **Step 4:** Define candidate operator `Eta(W)=Pcyc @ W @ B.T @ C`, where `C=I-11^T/n` centers arbitrary node sources into the balanced subspace.
- [ ] **Step 5:** Measure candidate operator norms and rank of the flattened operator family.
- [ ] **Step 6:** Across 256 random node-source trials and frozen positive scales, verify `Eta(c s)=c Eta(s)` and record normalized output-direction separations between the three candidate maps.
- [ ] **Step 7:** Test covariance algebraically under random vertex permutation matrices and signed edge permutation/orientation matrices using `B' = V B E.T`, `W' = E W E.T`, and `s'=V s`.
- [ ] **Step 8:** Add a declared-law positive control `eta*=c* Eta(W*)` and verify exact reconstruction when `W*` and `c*` are supplied.
- [ ] **Step 9:** Adjudicate: incidence-only zero plus two or more inequivalent lawful nonzero weighted operators => `NONUNIQUE`; no nonzero weighted operators => `NO_NATIVE_DEFORMATION`; only one uniquely selected operator with no added choice => `DERIVED`.
- [ ] **Step 10:** Run `python CHECKER.py` and make it pass.

### Task 3: Freeze scientific report and summary

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.01/REPORT.md`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.01/SUMMARY.json`

**Interfaces:**
- Consumes exact printed values from `CHECKER.py`.
- Produces human- and machine-readable adjudication.

- [ ] **Step 1:** State the source-action-versus-law-deformation distinction.
- [ ] **Step 2:** Prove `Pcyc B^T=0` as the incidence-only theorem.
- [ ] **Step 3:** Document the weighted family and explain why multiple covariant state-weighted choices establish nonuniqueness rather than a derived source law.
- [ ] **Step 4:** Record the scalar-family ambiguity separately.
- [ ] **Step 5:** Record all fresh controls exactly from the checker.
- [ ] **Step 6:** Preserve v13.28 branch stop: no downstream coupling work is reopened.
- [ ] **Step 7:** State restart condition: explicit new source→higher-incidence axiom or independent physical cross-domain calibration.

### Task 4: Repository status and CI

**Files:**
- Create: `.github/workflows/uqcf-v1401-global-admissibility.yml`
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

- [ ] **Step 1:** Add CI for branch and `main`, pinned Python 3.11 / NumPy 2.4.6, running `CHECKER.py`.
- [ ] **Step 2:** Add v14.01 to the research index without rewriting prior v13 claims.
- [ ] **Step 3:** Update status with the exact v14.01 adjudication and preserve Pillar 3 open.
- [ ] **Step 4:** Run CI on the exact final branch SHA.
- [ ] **Step 5:** Compare branch against `main`; require 0 behind and only intended files.
- [ ] **Step 6:** Fast-forward `main` only after exact-SHA CI succeeds, then require post-merge CI success.
