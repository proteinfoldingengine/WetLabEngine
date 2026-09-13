# v14.01 Global Admissibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the frozen global-consistency architecture canonically selects a nonzero source-dependent admissibility deformation or only an inequivalent family.

**Architecture:** Implement a basis-independent graph/cochain audit. The native incidence map is tested against the cycle projector exactly. Several covariant state/relational-weighted incidence maps are then compared as candidate source→global-defect deformations. Global positivity is independently audited in the faithful interior and at a PSD boundary so it cannot be silently treated as a selector. A positive control explicitly inserts a selected functional and coefficient to prove the gate recognizes uniqueness when a new law is supplied.

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

- [x] **Step 1:** Create a checker that imports `run_audit`; verify RED before the implementation file exists.
- [x] **Step 2:** Assert seed `1401`, 256 trials, graph cycle dimension `3`, incidence leakage `<1e-12`, covariance/scaling errors `<2e-12`, at least two inequivalent weighted operators, and positive-control error `<2e-12`.
- [x] **Step 3:** Require the gate outcome to be one of the three frozen outcomes and require branch-stop status for a non-derived result.
- [x] **Step 4:** Commit the RED checker and preserve the failing CI evidence.

### Task 2: Implement basis-independent incidence and weighted-deformation audit

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.01/admissibility_audit.py`

**Interfaces:**
- Produces `run_audit() -> dict`.

- [x] **Step 1:** Build the fixed 5-node / 7-edge oriented incidence matrix `B` and cycle projector `Pcyc = I - B.T @ pinv(B @ B.T) @ B`.
- [x] **Step 2:** Verify the exact incidence-only identity numerically through `||Pcyc @ B.T||`.
- [x] **Step 3:** Generate deterministic edge invariants `chi` and candidate weights `W1=diag(1+chi)`, `W2=diag(exp(chi))`, `W3=diag(1+chi**2)` with all weights positive.
- [x] **Step 4:** Define candidate operator `Eta(W)=Pcyc @ W @ B.T @ C`, where `C=I-11^T/n` centers arbitrary node sources into the balanced subspace.
- [x] **Step 5:** Measure candidate operator norms and rank of the flattened operator family.
- [x] **Step 6:** Across 256 random node-source trials and frozen positive scales, verify `Eta(c s)=c Eta(s)` and record normalized output-direction separations between the three candidate maps.
- [x] **Step 7:** Test covariance algebraically under random vertex permutation matrices and signed edge permutation/orientation matrices using `B' = V B E.T`, `W' = E W E.T`, and `s'=V s`.
- [x] **Step 8:** Add a declared-law positive control `eta*=c* Eta(W*)` and verify exact reconstruction when `W*` and `c*` are supplied.
- [x] **Step 9:** Adjudicate provisionally: incidence-only zero plus two or more inequivalent lawful nonzero weighted operators => `NONUNIQUE`; no nonzero weighted operators => `NO_NATIVE_DEFORMATION`; only one uniquely selected operator with no added choice => `DERIVED`.
- [x] **Step 10:** Run `python CHECKER.py` and preserve the first GREEN evidence.

### Task 2B: Audit global positivity as a possible hidden selector

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.01/CHECKER.py`
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.01/admissibility_audit.py`

- [x] **Step 1:** Add RED assertions requiring a `positivity_audit` object; verify failure because the implementation is absent.
- [x] **Step 2:** Embed the seven edge-defect control coordinates injectively into `Sym(4)` only for the positivity test; explicitly label this as a control rather than a physical tensor map.
- [x] **Step 3:** At the faithful center `X0=I4`, compute one common epsilon for all 768 bounded candidate perturbations and verify every `X0 + epsilon Delta` remains positive definite.
- [x] **Step 4:** At `Xb=diag(0,1,1,1)`, record the first-order PSD condition `e0^T Delta e0 >= 0` and the 9-dimensional equality lineality subspace inside `Sym(4)`.
- [x] **Step 5:** Classify positivity as `INEQUALITY_FILTER_NOT_CANONICAL_SOURCE_MAP` when both the open-interior and boundary-cone controls show non-selection.
- [x] **Step 6:** Re-run CI and require GREEN before scientific adjudication.

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
- [ ] **Step 4:** Record the positivity interior/boundary result and explain why feasibility does not select the deformation.
- [ ] **Step 5:** Record the scalar-family ambiguity separately.
- [ ] **Step 6:** Record all fresh controls exactly from the authoritative checker.
- [ ] **Step 7:** Preserve v13.28 branch stop: no downstream coupling work is reopened.
- [ ] **Step 8:** State restart condition: explicit new source→higher-incidence axiom or independent physical cross-domain calibration.
- [ ] **Step 9:** Bind the checker to the frozen `SUMMARY.json` values.

### Task 4: Repository status and CI

**Files:**
- Create: `.github/workflows/uqcf-v1401-global-admissibility.yml`
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

- [x] **Step 1:** Add CI for branch and `main`, pinned Python 3.11 / NumPy 2.4.6, running `CHECKER.py`.
- [ ] **Step 2:** Add v14.01 to the research index without rewriting prior v13 claims.
- [ ] **Step 3:** Update status with the exact v14.01 adjudication and preserve Pillar 3 open.
- [ ] **Step 4:** Run CI on the exact final branch SHA.
- [ ] **Step 5:** Compare branch against `main`; require 0 behind and only intended files.
- [ ] **Step 6:** Fast-forward `main` only after exact-SHA CI succeeds, then require post-merge CI success.
