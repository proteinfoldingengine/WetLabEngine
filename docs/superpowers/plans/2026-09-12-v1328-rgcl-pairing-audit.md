# v13.28 RGCL Pairing Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close v13.28 by testing whether any frozen ontology-native source→geometry pairing can fix a nonzero absolute coupled-source magnitude without Einstein/ADM target fitting or an inserted free scale.

**Architecture:** Use a theorem-first gate with deterministic numerical controls. `CHECKER.py` reproduces only the algebraic scale-weight witnesses; `REPORT.md` carries the ontology audit and cites upstream certified premises; `SUMMARY.json` freezes the adjudication. No new physical model or fitted field equation is introduced.

**Tech Stack:** Python 3 + NumPy for deterministic controls; Markdown/JSON gate artifacts; GitHub history structure already used by v13.01–v13.27.

**Spec:** `docs/superpowers/specs/2026-09-12-v1328-rgcl-pairing-audit-design.md`

## Global Constraints

- Audit only four frozen candidate classes: Genesis/source grade + retained measure/support; PGRL/BKM pairing; RESA solder/coframe; QMAR response/covariance.
- Never consult an ADM/Einstein residual as a selector.
- Never fit or insert a coupling scale.
- Allowed final outcomes: `DERIVED`, `OBSTRUCTED`, `REQUIRES_NEW_AXIOM`.
- If all frozen candidates fail, stop the source-to-GR coupling branch and do not introduce another missing-law label.
- Numerical controls are algebraic witnesses only; they are not physical validation.

---

### Task 1: RED checker contract

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v13/v13.28/CHECKER.py`

**Interfaces:**
- Consumes: NumPy only.
- Produces: deterministic JSON-like summary printed to stdout and assertions for the scale-weight controls.

- [ ] **Step 1:** Write checker expectations before helper implementation: 256 trials, scales `[0.2,0.5,2,5,11]`, four source-linear candidate maps, BKM quadratic scaling, direction invariance, and inverse-weight positive control.
- [ ] **Step 2:** Run the checker locally and confirm it fails because the audit helper functions are absent.
- [ ] **Step 3:** Add the minimal helper functions inside `CHECKER.py`.
- [ ] **Step 4:** Run again and require relative errors below `2e-12` and a nonzero minimum baseline candidate norm.
- [ ] **Step 5:** Record the exact fresh numbers for `SUMMARY.json` and `REPORT.md`.

### Task 2: Freeze candidate-by-candidate theorem audit

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v13/v13.28/REPORT.md`
- Create: `ResearchHistory/UQCF-GEM/v13/v13.28/SUMMARY.json`

**Interfaces:**
- Consumes: upstream v13.11, v13.26, v13.27 certified premises and Task 1 numerical controls.
- Produces: final v13.28 adjudication.

- [ ] **Step 1:** State the source-scale weight action and the scale-weight pairing obstruction theorem.
- [ ] **Step 2:** Audit Genesis/measure-support: weight-one source amount + weight-zero geometry cannot fix an invariant extensive magnitude or coframe type.
- [ ] **Step 3:** Audit PGRL/BKM: BKM dual/norm inherits source scale; normalized quantities are projective; quadratic relative-entropy/BKM response scales as degree two.
- [ ] **Step 4:** Audit RESA: supplied solder can provide a type map only conditionally; v13.11 nonunique solder lift prevents a canonical source→coframe law; no magnitude calibration appears.
- [ ] **Step 5:** Audit QMAR: linear/covariant response remains weight one; covariance/trace identities do not select a coefficient; geometry-only autonomy is already obstructed.
- [ ] **Step 6:** Adjudicate each candidate `OBSTRUCTED` and overall gate `REQUIRES_NEW_AXIOM` if no negative-weight calibrated object is found.
- [ ] **Step 7:** Freeze the branch stop: one explicit new axiom or independently calibrated physical observable is required before this coupling branch can continue.

### Task 3: Repository status integration

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/CHANGELOG.md`

**Interfaces:**
- Consumes: final v13.28 adjudication.
- Produces: canonical research-history status.

- [ ] **Step 1:** Update latest completed gate to v13.28 and record the source-scale pairing obstruction.
- [ ] **Step 2:** State that the source-to-GR coupling branch is stopped pending a new axiom or independent calibration.
- [ ] **Step 3:** Preserve Pillar 3 as OPEN; do not claim physical GR failure in general.
- [ ] **Step 4:** Add v13.28 to the research index and append a changelog entry.

### Task 4: Verification and merge gate

**Files:**
- No new files unless verification reveals a defect.

- [ ] **Step 1:** Run `python ResearchHistory/UQCF-GEM/v13/v13.28/CHECKER.py` and require exit 0.
- [ ] **Step 2:** Re-read `REPORT.md` and `SUMMARY.json` line-by-line against the design constraints.
- [ ] **Step 3:** Compare branch to `main`; require `behind_by=0` and only intended v13.28/spec/plan/status-history files.
- [ ] **Step 4:** Fast-forward `main` only after the checker and diff audit pass.
- [ ] **Step 5:** Verify the files resolve on `main` and report the exact merge SHA and scientific adjudication.