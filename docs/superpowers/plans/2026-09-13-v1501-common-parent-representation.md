# v15.01 Common-Parent Representation Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether frozen Genesis/provenance/source structure already supplies a parent-space source class or support-preserving parent tangent on the archived 125-dimensional compatibility parent whose compression canonically induces the positive projective 25-dimensional source ray consumed by v14.03.

**Architecture:** Reuse the archived quantum compatibility laboratory and v14.03/v14.04 audit code without changing their scientific contracts. The new audit has three independent layers: verify the parent/support representation and exact compression theorems; inventory frozen provenance/source candidates for lawful same-parent operators or support-preserving tangents; then run supplied-parent positive controls to prove common-parent descent is sufficient without treating the controls as provenance derivations. The final adjudication is derived only from frozen archive typing and canonicality, never from downstream gravity/ADM targets.

**Tech Stack:** Python 3.11; NumPy 2.4.6; SciPy 1.17.1; GitHub Actions; existing `Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`; existing v14.03 source-ray and v14.04 provenance-representation audits.

**Spec:** `docs/superpowers/specs/2026-09-13-v1501-common-parent-representation-design.md`

## Global Constraints

- Primitive/pre-pruning reality remains atemporal; no physical time or entropy primitive may be introduced.
- Reuse the archived compatibility parent exactly: `H_Q = C^125`, support isometry `L : C^25 -> C^125`, and `T = L X L^dagger` at frozen `FIXED_T = 21/41`.
- Do not replace `L` with another support embedding.
- Projective source equivalence remains `P ~ a P + b I`, `a > 0`.
- Parent compression is only `C_L(A) = L^dagger A L`.
- Do not construct a provenance parent source by lifting a desired support source through `L`, fitting v14.02/v14.03 dual rays, padding/reshaping the six-qubit demo, vectorizing the 6-D Genesis field, PCA/SVD/random alignment, or ADM/Einstein/gravity target fitting.
- A state, ledger, graph current, or field is not a source covector unless the frozen archive already supplies the typed source map.
- A parent-state tangent counts only if it is support-preserving and the frozen faithful PGRL/BKM tangent map determines the projective support covector class without an added selector.
- A support-changing parent tangent must be reported as `SUPPORT_CHANGING_PARENT_TANGENT_NOT_V1403_COMPATIBLE`, not projected back by hand.
- The primary outcome must be one of `COMMON_PARENT_INDUCES_SOURCE_RAY`, `COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE`, `NO_COMMON_PARENT_REPRESENTATION`, or verification-stop `UNRESOLVED_COMMON_PARENT_AUDIT`.
- Even a positive v15.01 result does not derive gravity, stress-energy, source-to-coframe coupling, spacetime, Einstein equations, or Pillar 3 closure.

---

### Task 1: Freeze RED checker and branch CI

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.01/CHECKER.py`
- Create: `.github/workflows/uqcf-v1501-common-parent-representation.yml`

**Interfaces:**
- Consumes: no v15.01 implementation module yet.
- Produces: a frozen checker contract importing `run_audit()` from `common_parent_audit.py` and branch CI that runs it under pinned Python/NumPy/SciPy.

- [ ] **Step 1: Create the failing checker**

Use this contract:

```python
#!/usr/bin/env python3
from common_parent_audit import run_audit

r = run_audit()
assert r["version"] == "v15.01"
assert r["seed"] == 1501
assert r["parent_dimension"] == 125
assert r["support_dimension"] == 25
assert r["Pillar_3"] == "OPEN"

p = r["parent_support"]
assert p["status"] == "COMPATIBILITY_PARENT_SUPPORT_VERIFIED"
assert p["max_isometry_error"] < 2e-11
assert p["max_reconstruction_error"] < 2e-11
assert p["max_projector_idempotence_error"] < 2e-11
assert p["max_compression_covariance_error"] < 2e-10
assert p["max_projective_descent_error"] < 2e-11

inv = r["archive_inventory"]
assert inv["candidate_count"] >= 5
assert inv["missing_artifact_count"] == 0
assert inv["same_parent_source_class_count"] >= 0
assert inv["support_preserving_parent_tangent_count"] >= 0

ctrl = r["positive_control"]
assert ctrl["classification"] == "SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION"
assert ctrl["noncentral_compressed_source"] is True
assert ctrl["nonzero_hidden_component"] is True
assert ctrl["boundary_simple"] is True
assert ctrl["normal_classification"] == "RAY"
assert ctrl["max_parent_support_covariance_error"] < 2e-9
assert ctrl["max_projective_descent_error"] < 2e-11

assert r["gate_outcome"] in {
    "COMMON_PARENT_INDUCES_SOURCE_RAY",
    "COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE",
    "NO_COMMON_PARENT_REPRESENTATION",
    "UNRESOLVED_COMMON_PARENT_AUDIT",
}
print("V15_01_COMMON_PARENT_REPRESENTATION_CHECKER_PASS")
```

- [ ] **Step 2: Create branch workflow**

Use Python 3.11, install exactly `numpy==2.4.6 scipy==1.17.1`, set `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `PYTHONHASHSEED=0`, and run `python CHECKER.py` from `ResearchHistory/UQCF-GEM/v15/v15.01`.

- [ ] **Step 3: Commit RED files**

Commit message:

```text
test: add v15.01 common-parent representation RED gate
```

- [ ] **Step 4: Verify intended RED**

Expected CI failure:

```text
ModuleNotFoundError: No module named 'common_parent_audit'
```

Any different failure must be diagnosed before implementation.

---

### Task 2: Implement parent/support representation and exact compression theorems

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py`

**Interfaces:**
- Consumes: archived `build_completion(V, FIXED_T)` from `uqcf_quantum_lab.py`; v14.03 loader/configuration helpers where useful.
- Produces:
  - `load_archived_lab() -> ModuleType`
  - `load_v1403() -> ModuleType`
  - `build_parent_configuration(name: str) -> dict[str, Any]`
  - `compress_parent_operator(L: np.ndarray, A: np.ndarray) -> np.ndarray`
  - `parent_support_audit(configs: dict[str, dict[str, Any]]) -> dict[str, Any]`
  - `run_audit() -> dict[str, Any]`

- [ ] **Step 1: Load frozen compatibility states**

For `V_A` and `V_B`, load the archived lab at `FIXED_T`, record `L`, `X0`, `T`, parent dimension 125, support dimension 25, and support projector `Pi = L @ L.conj().T`.

- [ ] **Step 2: Verify parent/support identities**

For each family compute:

```python
isometry_error = ||L^dagger L - I_25||_F
reconstruction_error = ||T - L X0 L^dagger||_F
projector_hermiticity_error = ||Pi - Pi^dagger||_F
projector_idempotence_error = ||Pi^2 - Pi||_F
```

Require all below `2e-11`.

- [ ] **Step 3: Implement exact parent compression**

```python
def compress_parent_operator(L, A):
    A = (A + A.conj().T) / 2
    return (L.conj().T @ A @ L + (L.conj().T @ A @ L).conj().T) / 2
```

Reject matrices whose shape is not `(125, 125)` for the frozen parent.

- [ ] **Step 4: Verify positive-projective descent numerically**

For deterministic Hermitian parent probes and `a in (0.2, 0.5, 2.0, 5.0, 11.0)`, `b in (-3.0, -0.7, 0.4, 2.5)`, verify

```text
C_L(aA + b I_125) = a C_L(A) + b I_25
```

with relative error below `2e-11`.

- [ ] **Step 5: Verify parent/support covariance**

For deterministic parent unitaries `U` and support unitaries `V`, define

```text
L' = U L V^dagger
A' = U A U^dagger
```

and verify

```text
C_L'(A') = V C_L(A) V^dagger
```

with relative error below `2e-10`.

- [ ] **Step 6: Run checker GREEN candidate**

At this stage `run_audit()` may return `UNRESOLVED_COMMON_PARENT_AUDIT` until inventory/control tasks are implemented, but parent/support telemetry must already satisfy the frozen checker fields that exist.

- [ ] **Step 7: Commit parent/support implementation**

Commit message:

```text
feat: verify v15.01 compatibility parent and compression
```

---

### Task 3: Audit frozen provenance candidates for same-parent source objects and tangents

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py`

**Interfaces:**
- Produces:
  - `archive_inventory() -> dict[str, Any]`
  - `classify_parent_candidate(record: dict[str, Any]) -> dict[str, Any]`
  - machine-readable candidate records with path, SHA-256, carrier type/dimension, source status, parent-map status, tangent status, and adjudication.

- [ ] **Step 1: Freeze candidate inventory**

Audit at least these exact artifacts:

```text
Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py
ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md
Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py
ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md
ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/uqcf_demo/quantum.py
```

Record SHA-256 of the exact file bytes/text used by the audit.

- [ ] **Step 2: Classify compatibility parent objects**

Record that `L`, `X0`, and `T` establish the `125 <- 25` parent/support representation but do not by themselves constitute a provenance/source operator.

- [ ] **Step 3: Classify Genesis ledger/scalar provenance**

Record these as identity/scalar provenance with no certified same-parent Hermitian source map.

- [ ] **Step 4: Classify 6-D Genesis/pruning field**

Record its own 6-D grid carrier and transformation law; explicitly mark that no frozen map to `Herm(C^125)` is certified. Do not vectorize it.

- [ ] **Step 5: Classify retained graph source/current package**

Record graph balance/current structure and its retained convention; mark no frozen same-parent `Herm(C^125)` representation unless an exact archived map is found.

- [ ] **Step 6: Classify six-qubit source demonstration**

Record dimension 64 and that its `P` is explicitly chosen within that demo. It is not the 125-D compatibility parent and no frozen natural functor to that parent may be invented.

- [ ] **Step 7: Audit support-preserving tangent route**

For every candidate tangent-like object found, require an already-frozen parent tangent `deltaT` satisfying both:

```text
||(I-Pi) deltaT||_F < tol
||deltaT (I-Pi)||_F < tol
```

before compressing it to `deltaX = L^dagger deltaT L`.

If support-preserving and trace-zero, use the inverse faithful PGRL/BKM tangent map already encoded in v14.03 `_source_from_tangent(X0, target)` only to recover the support projective source class. If support-changing, record `SUPPORT_CHANGING_PARENT_TANGENT_NOT_V1403_COMPATIBLE` and do not project it back by hand.

- [ ] **Step 8: Derive inventory counts**

Return at minimum:

```text
candidate_count
missing_artifact_count
same_parent_source_class_count
support_preserving_parent_tangent_count
support_changing_parent_tangent_count
```

- [ ] **Step 9: Commit archive inventory**

Commit message:

```text
feat: audit v15.01 frozen common-parent source candidates
```

---

### Task 4: Prove common-parent sufficiency with supplied-parent controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py`

**Interfaces:**
- Produces: `positive_control(v1403, cfg) -> dict[str, Any]` and downstream v14.03 telemetry.

- [ ] **Step 1: Build target-blind parent controls**

Construct deterministic parent-space Hermitian controls from fixed parent basis indices and coefficients only; do not use v14.02/v14.03 boundary/dual outputs to choose them. Example family:

```python
A = np.zeros((125, 125), dtype=complex)
A[0, 0] = 1.0
A[1, 1] = -0.7
A[2, 5] = A[5, 2] = 0.31
A[7, 11] = 0.22j
A[11, 7] = -0.22j
```

Try a frozen finite list of such controls declared in source. Select the first one whose compressed source is noncentral and v14.03-active; record every attempt. This is a positive control, not a provenance selector.

- [ ] **Step 2: Compress the parent control**

For each `V_A`/`V_B` configuration compute

```text
P_ctrl = L^dagger A_ctrl L
```

and test noncentrality after removing the identity component.

- [ ] **Step 3: Feed the compressed source through frozen v14.03**

Use `source_contact()` from v14.03 without modifying it. Require at least one control/configuration pair with:

```text
hidden_classification = NONZERO_HIDDEN_COMPONENT
boundary.simple = True
normal.classification = RAY
```

- [ ] **Step 4: Verify projective descent and parent/support covariance end-to-end**

Transform parent source and support coordinates consistently and verify the compressed source and v14.03 downstream contact/dual objects covary within frozen tolerances.

- [ ] **Step 5: Add support-preserving tangent positive control**

Take the same supplied parent operator `A_ctrl`, compute its support source `P_ctrl`, obtain the exact support PGRL tangent `deltaX`, lift only that tangent via

```text
deltaT_ctrl = L deltaX L^dagger
```

and verify the tangent route recovers the same projective support source class. Label this strictly as a mathematical round-trip control, not provenance evidence.

- [ ] **Step 6: Commit positive controls**

Commit message:

```text
test: add v15.01 common-parent sufficiency controls
```

---

### Task 5: Adjudicate v15.01 and freeze archive artifacts

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py`
- Create: `ResearchHistory/UQCF-GEM/v15/v15.01/SUMMARY.json`
- Create: `ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md`
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.01/CHECKER.py`

**Interfaces:**
- Produces the frozen v15.01 scientific result and summary-bound checker.

- [ ] **Step 1: Implement exact adjudication hierarchy**

Use:

```python
if certified_unique_same_parent_source_class:
    gate_outcome = "COMMON_PARENT_INDUCES_SOURCE_RAY"
elif certified_multiple_inequivalent_same_parent_source_classes:
    gate_outcome = "COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE"
elif no_frozen_same_parent_source_class_or_support_preserving_parent_tangent:
    gate_outcome = "NO_COMMON_PARENT_REPRESENTATION"
else:
    gate_outcome = "UNRESOLVED_COMMON_PARENT_AUDIT"
```

The compatibility parent itself being verified does not count as provenance source selection.

- [ ] **Step 2: Run production checker and capture JSON telemetry**

Print the full `run_audit()` result after the pass marker. Use that exact successful run as the source for `SUMMARY.json` and report numbers.

- [ ] **Step 3: Write `SUMMARY.json`**

Include version, seed, parent/support dimensions, gate outcome, secondary parent-support status, archive candidate inventory and hashes, positive-control telemetry, claim boundaries, scientific breakthrough flag, Pillar 3 status, and stop rule.

- [ ] **Step 4: Write `REPORT.md`**

Separate:

```text
THEOREM
EXECUTED COMPUTATION
ARCHIVE TYPE AUDIT
INTERPRETATION
UNRESOLVED PHYSICAL CLAIMS
```

If positive, do not say gravity is derived. If negative, preserve the verified `125 <- 25` parent/support representation explicitly.

- [ ] **Step 5: Bind checker to frozen summary**

Load `SUMMARY.json` and assert the live result agrees on gate outcome, exact inventory hashes, parent/support status, and frozen telemetry within numerical tolerances.

- [ ] **Step 6: Re-run exact summary-bound CI**

Require success on the exact branch SHA.

- [ ] **Step 7: Commit frozen package**

Commit message:

```text
docs: freeze v15.01 common-parent representation result
```

---

### Task 6: Advance canonical research status and integrate only after exact-SHA certification

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Produces canonical project frontier after v15.01.

- [ ] **Step 1: Update README**

Add v15 history and preserve v14.01-v14.04 and v13.28 claim boundaries.

- [ ] **Step 2: Update STATUS**

Set latest completed gate to v15.01 and state the exact new frontier implied by the measured outcome.

- [ ] **Step 3: Certify exact final branch head**

Run v15.01 workflow on the exact final SHA; make no post-certification edits.

- [ ] **Step 4: Compare against `main`**

Require `behind_by == 0` and only the intended workflow/spec/plan/v15.01/README/STATUS files.

- [ ] **Step 5: Fast-forward `main` under the established completed-gate workflow**

Move `main` only to the exact certified SHA.

- [ ] **Step 6: Require post-merge safeguards on the same SHA**

Require success for:

```text
v15.01
v14.04
v14.03
v14.02
v14.01
v13.28
```

- [ ] **Step 7: Verify `main` ref**

Confirm `main` still equals the exact certified v15.01 SHA before claiming completion.
