# UQCF-GEM v15.45 Curvature Factorization / Spectral Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Derive and certify the exact compact factorization of the frozen v15.44 curvature-response operator on the actual archived carriers, characterize its spectral/parity boundary, and separate construction-implied consequences from independent physical evidence.

**Architecture:** Add a self-contained v15.45 demo beside v15.44. A pure exact-algebra module constructs the candidate Laplacian/face-average operator from carrier geometry only; an independent verifier compares it coefficient-by-coefficient with the frozen v15.44 operator under all declared presentations. A separate spectral module proves/checks kernel conditions and even-size falsifiers. No source archive is available to the factorization worker.

**Tech Stack:** CPython 3.13.5; standard-library Fraction, unittest, JSON, subprocess, hashlib; frozen v15.42/v15.44 exact modules; GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-23-v1545-curvature-factorization-spectral-boundary-design.md`

## Global Constraints

- Parent is certified v15.44 head `9085e4fa0bec3dbd700f759a8a9629b230d226ff`; run `35814970929` succeeded.
- Work only on `research/v15.45-curvature-factorization-spectral-boundary`; PR #56 remains draft/open/unmerged during execution.
- Preserve parent-tracked scientific files byte-for-byte; v15.45 changes are additive.
- No fundamental time, dark-matter primitive, downstream gravity fit, source fitting, transport retuning, or post-result carrier redefinition.
- Actual archived L5/L7 carriers are authoritative for factorization certification.
- L6/L8 are preregistered falsifier carriers; an obstruction is a valid scientific result and must not be repaired after exposure.
- Source correspondence is not evaluated in this gate. Physical curvature, gravity, spacetime, stress-energy, Einstein equations, continuum limit, foundational uniqueness, and breakthrough claims remain false; Pillar 3 remains OPEN.
- Exact decisions use rational/integer algebra wherever possible. Any numerical conditioning diagnostic is descriptive only and may not tune the operator.

## Review Focus

1. A compact formula that matches identity presentation but fails D4/orientation/basepoint transformation must fail certification.
2. Even-size L6/L8 null modes must be reported, not filtered, regularized, or used to redefine admissibility.
3. Scale 7/3 must follow the frozen response scaling exactly; no hidden normalization may erase scale dependence.
4. Pair-separation claims implied by centered injectivity plus input nonproportionality must be labeled dependent consequences.
5. Any source-curvature relation algebraically guaranteed by composing frozen source generation with the factorization must be identified before a later physical source test.

---

### Task 1: Freeze evidence and exact compact operator

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/evidence.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/factorization.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_factorization.py`

**Interfaces:**
- Consumes: v15.44 `build_actual_carrier`, `derive_operator`, frozen carrier geometry.
- Produces: `compact_operator(carrier, presentation=None) -> Operator`; `verify_factorization(carrier, presentation=None) -> dict`.

- [ ] Write RED tests that import `compact_operator`, compare all entries to `derive_operator` for one actual L5 carrier, reject a damaged coefficient, and assert constants map to zero.
- [ ] Run `python -m unittest -v test_factorization`; expected RED because v15.45 implementation is absent.
- [ ] Implement exact `Delta` and face averaging from carrier adjacency/direction/cycles, returning the full four-entry-per-face Operator in the same codomain convention as v15.44. Do not call `derive_operator` inside construction.
- [ ] Run the focused test GREEN and then all four actual carriers.
- [ ] Commit: `feat(uqcf): derive compact curvature factorization`.

### Task 2: Presentation-covariant equality

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/presentations.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_presentations.py`

**Interfaces:**
- Consumes: Task 1 compact operator and v15.44 presentation conventions.
- Produces: `check_all_presentations(carrier) -> dict`.

- [ ] Write RED tests for D4 frame changes, reversed orientation, changed basepoint, deterministic relabeling, and both scales; include one intentionally mismatched raw-entry comparison that must be rejected.
- [ ] Run focused tests RED.
- [ ] Implement presentation alignment using only declared transformations and compare exact full matrices after alignment.
- [ ] Run GREEN on all actual carriers.
- [ ] Commit: `feat(uqcf): certify factorization presentation covariance`.

### Task 3: Kernel theorem and frozen even-size falsifiers

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/spectral.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_spectral.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/docs/DERIVATION.md`

**Interfaces:**
- Consumes: Task 1 exact factorization.
- Produces: `spectral_certificate(L) -> dict`; exact finite kernel characterization and theorem narrative.

- [ ] Write RED tests reproducing L5 rank/nullity 24/1 and L7 48/1, plus preregistered L6/L8 checks requiring explicit nonconstant centered null modes when present.
- [ ] Run RED before implementation.
- [ ] Implement exact Fourier/polynomial or shift-operator reasoning sufficient to certify kernel membership without floating thresholds. Explicitly test `X=-1` and `Y=-1` modes for even L.
- [ ] State the general finite condition in DERIVATION.md only to the extent proved; separate theorem from finite checks.
- [ ] Run GREEN and compare odd-size certificates with v15.44.
- [ ] Commit: `feat(uqcf): characterize curvature spectral boundary`.

### Task 4: Conditioning and evidence-dependency audit

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/dependency_audit.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_dependency_audit.py`

**Interfaces:**
- Consumes: v15.44 archived centered fields/pairs, Task 1 operator, Task 3 kernel result.
- Produces: dependency classifications for pair separation; descriptive conditioning records.

- [ ] Write RED tests proving that on a centered-injective carrier, proportional output implies proportional input, and that this implication is not asserted on a carrier with a nonconstant kernel.
- [ ] Add a RED test that conditioning data cannot change any scientific gate threshold or operator coefficient.
- [ ] Implement exact dependency classification and a descriptive nonzero-response-scale diagnostic.
- [ ] Run GREEN over all 592 archived pairs and all four carriers.
- [ ] Commit: `feat(uqcf): audit curvature evidence dependencies`.

### Task 5: Source-correspondence firewall

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/source_firewall.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_source_firewall.py`

**Interfaces:**
- Consumes: frozen v15.40 response-generation formulas as evidence, not as factorization input.
- Produces: symbolic/exact list of source-curvature relations already implied by construction.

- [ ] Write RED tests for the canonical global-balance composition and controls, requiring construction-implied identities to be labeled `DEPENDENT_BY_CONSTRUCTION`.
- [ ] Run RED.
- [ ] Implement composition audit in a later isolated stage that cannot alter Tasks 1–4 results.
- [ ] Verify no physical-source verdict is emitted.
- [ ] Run GREEN.
- [ ] Commit: `feat(uqcf): separate construction implied source relations`.

### Task 6: Deterministic gate, result ledger, and documentation

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/docs/RESULTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/README.md`

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: deterministic fail-closed v15.45 scientific ledger and adjudication.

- [ ] Write RED tests for partial-stage failure, missing actual carrier, missing L6/L8 falsifier, altered factorization coefficient, forbidden source claim, and noncanonical result bytes.
- [ ] Run RED.
- [ ] Implement ordered fail-closed coordinator and canonical JSON.
- [ ] Generate RESULTS once; replay with `--check` and require byte identity.
- [ ] README records the actual result, theorem/computation boundary, parity/spectral boundary, dependency audit, and next unresolved scientific object.
- [ ] Commit: `feat(uqcf): publish curvature factorization spectral boundary`.

### Task 7: Exact-head GitHub certification and closeout

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/ci_verify.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.45-curvature-factorization-spectral-boundary/test_ci.py`
- Create: `.github/workflows/uqcf-v1545-curvature-factorization-spectral-boundary.yml`

**Interfaces:**
- Consumes: complete v15.45 tree and deterministic ledger.
- Produces: exact-head certification receipt.

- [ ] Write RED tests for parent drift, spec/plan drift, nonadditive scope, wrong Python runtime, skipped tests, incomplete ledger, false physical claims, and head mismatch.
- [ ] Run RED.
- [ ] Implement exact-head runner pinned to CPython 3.13.5; no dependency installation or broad workflow matrix.
- [ ] Run complete local/isolated suite and canonical replay before publication.
- [ ] Fresh whole-branch review against spec, especially the five Review Focus items; repair only verified defects with RED→GREEN tests.
- [ ] Push reviewed commits to PR #56 and observe one official Actions certification. Record run/job/head/result and scientific adjudication in PR metadata; no merge.
- [ ] End without starting source correspondence. Commit: `ci(uqcf): certify v15.45 spectral boundary`.
