# v14.03 Projective Source-Ray / Hidden First-Contact Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test whether a supplied positive projective PGRL source ray canonically determines a hidden tangent direction, a radial hidden-fiber first-contact point, and the v14.02 canonical local dual ray.

**Architecture:** Reuse the certified v14.02 full-hidden-fiber boundary and normal-cone machinery by loading `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py` dynamically. Add a focused v14.03 audit that computes the exact PGRL tangent in the archived coefficient-space support, projects that tangent into the exact hidden kernel, maps the normalized hidden component to radial first contact, and audits invariance under positive source rescaling, identity shifts, and support-coordinate unitary changes. Keep the provenance-to-source-ray origin as a separate archive audit so a positive supplied-source result cannot be mistaken for a derived Genesis/provenance source law.

**Tech Stack:** Python 3.11, NumPy 2.4.6, SciPy 1.17.1, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-12-v1403-projective-source-ray-design.md`

## Global Constraints

- Work only on branch `research/v14.03-projective-source-ray` until exact-SHA certification succeeds.
- Reuse the archived compatibility construction and certified v14.02 boundary/dual machinery; do not replace either with a new primary toy model.
- Use the full support coefficient state `X0`, the full Hilbert–Schmidt hidden kernel, and supplied Hermitian support-space source covectors.
- Deterministic RNG seed: `1403`.
- Survey exactly `64` primary sources for `V_A` and exactly `64` for `V_B`.
- Python `3.11`, NumPy `2.4.6`, SciPy `1.17.1`.
- Finite-difference epsilon: `1e-6`.
- Source Hermiticity tolerance: `1e-12`.
- Tangent Hermiticity tolerance: `2e-11`.
- Tangent trace tolerance: `2e-11`.
- Finite-difference relative tolerance: `2e-7`.
- Hidden-component threshold: `tau_hidden = 1e-10 * max(1, ||dotX||_HS)`.
- Boundary PSD tolerance: `2e-9`.
- Projective hidden-direction drift tolerance: `2e-9`.
- Boundary-point relative drift tolerance: `2e-9`.
- Oriented dual-ray drift tolerance: `2e-9` using `1-dot(N1_hat,N2_hat)` after the common inward orientation convention.
- Support-coordinate covariance tolerance: `2e-9`.
- Positive-scale controls: `a=[0.2,0.5,2.0,5.0,11.0]`.
- Identity-shift controls: `b=[-3.0,-0.7,0.4,2.5]`.
- Never re-center or re-normalize transformed sources `aP+bI` before invariance tests.
- Never call hidden radial first contact a physical PGRL boundary crossing.
- Provenance/Genesis must not be claimed to supply `[P]` unless an existing certified typed construction actually does so.
- Pillar 3 remains OPEN regardless of gate outcome.

---

### Task 1: Freeze the RED v14.03 certification interface

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.03/CHECKER.py`
- Create: `.github/workflows/uqcf-v1403-projective-source-ray.yml`

**Interfaces:**
- Consumes: `run_audit() -> dict` from `source_ray_audit.py`.
- Produces: deterministic assertions over survey size, source/tangent controls, projective/gauge invariance, boundary/dual status, engineered controls, provenance status, and gate outcome.

- [ ] **Step 1: Write the failing checker**

Use assertions that require:

```python
result["version"] == "v14.03"
result["seed"] == 1403
result["primary_sample_count"] == 128
result["survey"]["V_A"]["sample_count"] == 64
result["survey"]["V_B"]["sample_count"] == 64
result["max_tangent_hermiticity_residual"] < 2e-11
result["max_tangent_trace_abs"] < 2e-11
result["max_finite_difference_relative_error"] < 2e-7
result["max_projective_hidden_direction_drift"] < 2e-9
result["max_projective_boundary_relative_drift"] < 2e-9
result["max_projective_dual_ray_drift"] < 2e-9
result["max_support_coordinate_covariance_error"] < 2e-9
result["identity_source_control"]["classification"] == "ZERO_PGRL_TANGENT"
result["hidden_active_control"]["classification"] == "NONZERO_HIDDEN_COMPONENT"
result["gate_outcome"] in {
    "PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY",
    "SOURCE_TO_BOUNDARY_NONUNIQUE",
    "NO_HIDDEN_SOURCE_CONTACT",
    "UNRESOLVED_NUMERICAL_SOURCE_LIFT",
}
result["provenance_source_ray_status"] in {
    "PROVENANCE_TO_SOURCE_RAY_DERIVED",
    "PROVENANCE_TO_SOURCE_RAY_UNDERIVED",
    "PROVENANCE_SOURCE_TYPE_MISMATCH",
}
```

- [ ] **Step 2: Add branch/main CI**

Workflow `UQCF v14.03 Projective Source-Ray Audit` must trigger on `main` and `research/v14.03-projective-source-ray` for v14.03 files, the v14.02 audit file, the archived compatibility lab, canonical README/STATUS, the spec/plan, and the workflow itself. Pin the frozen Python/NumPy/SciPy versions and run `python CHECKER.py` from the v14.03 directory.

- [ ] **Step 3: Push and verify RED**

Expected failure: `ModuleNotFoundError: No module named 'source_ray_audit'`.

- [ ] **Step 4: Commit**

Commit messages: `test: add v14.03 projective-source RED gate` and `ci: add v14.03 projective-source workflow`.

---

### Task 2: Implement certified dependency loading and exact PGRL tangent

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`

**Interfaces:**
- Produces:
  - `load_v1402() -> ModuleType`
  - `build_configuration(name: str) -> dict`
  - `pgrl_tangent(X0: ndarray, P: ndarray) -> ndarray`
  - `pgrl_state(X0: ndarray, P: ndarray, s: float) -> ndarray`
  - `sample_sources(k: int, count: int, rng) -> ndarray`
- Consumes certified v14.02 functions `load_archived_lab`, `build_primary_configuration`, `radial_boundary`, `normal_cone_audit`.

- [ ] **Step 1: Dynamically load v14.02 from the repository tree**

From `Path(__file__).resolve().parents[4]`, load:

`ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

with `importlib.util.spec_from_file_location`. Fail loudly if missing.

- [ ] **Step 2: Build `V_A` and `V_B` through v14.02**

Use the certified loader and `build_primary_configuration`; record `X0`, hidden modes, support dimension, hidden dimension, and archived lab provenance.

- [ ] **Step 3: Implement exact PGRL tangent by the logarithmic-mean formula**

Diagonalize faithful `X0`; transform `P`; form the logarithmic-mean matrix stably; compute the Fréchet derivative and subtract the normalization term. Return a Hermitian, trace-zero matrix.

- [ ] **Step 4: Implement finite PGRL state only for tangent verification**

Use `scipy.linalg.logm/expm` or an eigen-decomposition equivalent to evaluate

`exp(log(X0)+sP)/Tr(exp(...))`.

This finite path is never used as the boundary selector.

- [ ] **Step 5: Freeze primary source sampling**

For each support dimension, generate 64 complex-Gaussian Hermitian sources, subtract `Tr(X0 P)I`, normalize by Frobenius norm, and record SHA-256 of the source tensor bytes.

- [ ] **Step 6: Commit**

Commit message: `feat: implement exact v14.03 PGRL source tangents`.

---

### Task 3: Implement hidden projection, radial first contact, and canonical dual representative

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`

**Interfaces:**
- Produces:
  - `project_hidden(modes, dotX) -> dict`
  - `source_contact(cfg, P) -> dict`
  - `oriented_dual_representative(cfg, boundary, normal) -> ndarray`

- [ ] **Step 1: Project the tangent into the exact hidden kernel**

Compute real HS coordinates

```python
coords = np.real(np.einsum("aij,ij->a", modes.conj(), dotX, optimize=True))
V = np.einsum("a,aij->ij", coords, modes, optimize=True)
```

and verify projection reconstruction/idempotence to numerical precision.

- [ ] **Step 2: Apply the frozen zero-hidden threshold**

If `||V|| <= 1e-10*max(1,||dotX||)`, classify `ZERO_HIDDEN_SOURCE_COMPONENT`; do not normalize it.

- [ ] **Step 3: For nonzero hidden response, compute radial first contact with v14.02**

Set `u=V/||V||`, use HS coordinates `coords/||coords||`, and call the certified v14.02 `radial_boundary(X0,modes,u_coords)` followed by `normal_cone_audit`.

- [ ] **Step 4: Construct a coordinate-free inward dual representative**

From `representative_g`, reconstruct

```python
NH = np.einsum("a,aij->ij", g, modes, optimize=True)
```

orient it so the center displacement has positive support pairing, normalize by Frobenius norm, and return the representative. Reject zero or non-ray normal results as unresolved/nonunique according to the frozen gate logic.

- [ ] **Step 5: Commit**

Commit message: `feat: map supplied source rays to hidden first contact`.

---

### Task 4: Audit projective invariance and support-coordinate gauge covariance

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`

**Interfaces:**
- Produces:
  - `projective_invariance_audit(cfg, P, base_contact) -> dict`
  - `support_coordinate_covariance_audit(cfg, P, base_contact, rng) -> dict`

- [ ] **Step 1: Verify analytic tangent against central finite differences**

For every primary source compare `pgrl_tangent(X0,P)` to

`(X(+eps)-X(-eps))/(2eps)` with `eps=1e-6`; record maximum relative error.

- [ ] **Step 2: Test raw `aP+bI` without preprocessing**

For every nonzero-hidden primary source and every frozen `a,b`, recompute the tangent/contact directly from `aP+bI`. Verify:

- `dotX_transformed ~= a*dotX`;
- normalized hidden direction is unchanged;
- boundary matrix is unchanged;
- inward normalized dual representative is unchanged.

Record maxima separately.

- [ ] **Step 3: Add deterministic support-coordinate unitaries**

Construct eight deterministic unitary matrices by QR decomposition of complex Gaussian matrices. Transform

`L'=L U†`, `X0'=U X0 U†`, `P'=U P U†`, `Q'_a=U Q_a U†`.

Recompute the complete source-contact pipeline in transformed coordinates and verify conjugation covariance of `dotX`, hidden projection, boundary, and dual representative.

- [ ] **Step 4: Commit**

Commit message: `test: certify v14.03 projective and gauge invariance`.

---

### Task 5: Add engineered controls and provenance/source-ray audit

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`

**Interfaces:**
- Produces `identity_source_control`, `visible_only_tangent_control`, `hidden_active_control`, and `provenance_source_ray_status`.

- [ ] **Step 1: Identity source control**

Set `P=I`; certify tangent norm below `2e-11`; classify `ZERO_PGRL_TANGENT`.

- [ ] **Step 2: Hidden-active control**

Use a deterministic hidden mode `Q_0` as a tangent target and solve the BKM/PGRL inverse linear map in the eigenbasis of `X0` for a Hermitian source `P_hidden`; verify its actual PGRL tangent has nonzero hidden projection. This is a checker control, not provenance evidence.

- [ ] **Step 3: Visible-only control only if canonical construction is available**

Attempt a deterministic source whose PGRL tangent lies in the HS orthogonal complement of the hidden kernel by selecting a tangent from the visible-range projector and inverting the faithful BKM map. If the chosen visible tangent is incompatible with trace-zero Hermitian tangent constraints or numerical conditioning, report `NOT_CONSTRUCTED`; do not tune post hoc.

- [ ] **Step 4: Audit provenance typing from frozen archive**

Record the existing certified facts rather than inventing code: Genesis/source provenance gives origin identity, source-flow compatibility, and grading; v13.26 proves it does not provide an observer calibration; no certified frozen artifact returns the required support-coefficient Hermitian operator ray for the v14.03 compatibility support. Unless an exact typed source is found in archive inspection, classify `PROVENANCE_SOURCE_TYPE_MISMATCH` (preferred if spaces differ) or `PROVENANCE_TO_SOURCE_RAY_UNDERIVED`.

- [ ] **Step 5: Commit**

Commit message: `test: add v14.03 source controls and provenance audit`.

---

### Task 6: Execute the 128-source gate, freeze archive, and bind checker

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.03/CHECKER.py`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.03/SUMMARY.json`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.03/REPORT.md`

**Interfaces:**
- Produces final `run_audit()` output and scientific adjudication.

- [ ] **Step 1: Aggregate the frozen survey**

For each configuration record sample count, source hash, support/hidden dimensions, zero-hidden count, nonzero-contact count, simple/ray boundary count, projective/gauge maxima, tangent finite-difference maxima, and sample-level records sufficient for audit.

- [ ] **Step 2: Adjudicate mechanically**

Use:

- `UNRESOLVED_NUMERICAL_SOURCE_LIFT` if any required numerical certification fails;
- else `SOURCE_TO_BOUNDARY_NONUNIQUE` if an equivalent projective source representation produces inequivalent hidden direction/boundary/dual result;
- else `NO_HIDDEN_SOURCE_CONTACT` if every primary source has zero hidden component;
- else `PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY` if every nonzero-hidden primary source passes all frozen projective and gauge checks and lands on a certified v14.02 ray-valued boundary.

Do not require every random source to have a hidden component; zero-hidden sources are valid scoped cases.

- [ ] **Step 3: Freeze `SUMMARY.json` from actual CI output**

Do not invent telemetry. Include the provenance-source-ray sub-status separately from the supplied-source gate result.

- [ ] **Step 4: Write `REPORT.md`**

Lead with the exact claim boundary: supplied projective source ray to hidden-tangent radial contact/dual ray if positive; actual PGRL trajectory does not cross the boundary; provenance-to-source ray remains separate; no gravity/coupling claim.

- [ ] **Step 5: Bind `CHECKER.py` to `SUMMARY.json`**

Compare discrete fields exactly and floating telemetry with scale-aware tolerances (`1e-12 + 1e-9*max(1,abs(actual),abs(expected))`). Preserve the scientific thresholds independently of summary matching.

- [ ] **Step 6: Run remote GREEN certification**

Require the summary-bound checker to pass on the exact branch SHA.

- [ ] **Step 7: Commit**

Commit messages: `docs: freeze v14.03 projective-source result` and `test: bind v14.03 checker to frozen summary`.

---

### Task 7: Canonical status integration and release verification

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Consumes frozen v14.03 result.
- Produces canonical program frontier without retracting v13.28, v14.01, or v14.02.

- [ ] **Step 1: Update v14 history and frontier**

Record the v14.03 outcome, explicitly distinguishing the supplied-source map from provenance origin.

- [ ] **Step 2: Verify branch diff**

Require `behind_by == 0`; changed files must be limited to v14.03, workflow, spec, plan, README, and STATUS.

- [ ] **Step 3: Exact-SHA branch certification**

Wait for the final v14.03 workflow to pass on the exact release SHA after the last documentation change.

- [ ] **Step 4: Fast-forward `main` only after certification**

Use non-force ref update.

- [ ] **Step 5: Post-merge verification**

Require v14.03 on exact merged SHA and inspect v14.02, v14.01, and v13.28 regression workflows triggered by canonical status/index changes.

- [ ] **Step 6: Final report-out**

Report exact `main` SHA, workflow run IDs, archive links, primary scientific claim, provenance status, preserved no-go results, and next lawful question. Set `scientific_breakthrough=true` only if the executed result independently warrants that classification under program governance.
