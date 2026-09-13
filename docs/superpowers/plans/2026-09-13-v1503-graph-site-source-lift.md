# v15.03 Graph-Site Factorization / Local-Gauge Source Lift Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the frozen UQCF-GEM archive already supplies a canonical graph-site quantum source representation that can feed the certified compatibility parent, and if not, localize the obstruction between graph-site identity, independent local-gauge covariance, state-dependent operator lifts, and cross-carrier compatibility.

**Architecture:** Implement a deterministic executable audit in `ResearchHistory/UQCF-GEM/v15/v15.03/` with four scientific layers matching the approved spec: archive/type audit; analytic state-independent local-gauge centrality with deterministic controls; supplied five-qubit state-dependent covariant source-family audit; and compatibility-parent relevance. Primary adjudication is upstream-only and never uses v14.02/v14.03 boundary or dual-ray quality as a selector. A frozen `SUMMARY.json`, `REPORT.md`, checker, and exact-SHA GitHub Actions run archive the result.

**Tech Stack:** Python 3.11; NumPy 2.4.6; SciPy 1.17.1; Python standard library `ast`, `hashlib`, `importlib`, `json`, `pathlib`, `itertools`; GitHub Actions; archived UQCF-GEM gate packages.

**Spec:** `docs/superpowers/specs/2026-09-13-v1503-graph-site-source-lift-design.md`

## Global Constraints

- Primitive/pre-pruning ontology remains atemporal.
- Do not use entropy, physical time, Newton/Einstein/ADM residuals, gravity observables, cosmology, or empirical targets as source selectors.
- The retained source fixture is exactly five nodes, seven directed edges, and scalar source `(-1,0,0,+1,0)` from `Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py`.
- A genuine graph-site carrier has five nontrivial factors `d_i >= 2`.
- The certified compatibility parent remains `C^5_A tensor C^5_B1 tensor C^5_B2 = C^125` with support isometry `L : C^25 -> C^125`.
- The arithmetic theorem `125 = 5^3` forbids identifying five nontrivial graph-site factors literally with the certified `C^125` parent.
- No one-dimensional padding, reshaping, factor suppression, PCA/SVD alignment, random isometry, or hand-built intertwiner may evade that theorem.
- State-independent retained scalar/current data carry no internal quantum-frame action. Under independent local unitaries the analytic commutant theorem is primary: a deterministic invariant source lift must be central.
- At v14.03 projective level `P ~ aP+bI` with `a>0`; central `P` is PGRL-null.
- State-dependent candidate functions are frozen to `f(x)=x`, `x^2`, `log x`, plus constant `1` null control. Do not add/drop candidates after observing results.
- Supplied five-qubit controls are exactly `r_A=(0.15,-0.31,0.42,0.63,-0.22)` and `r_B=(0.52,-0.18,0.27,-0.47,0.36)` with `rho_i=(I+r_i Z)/2`.
- Supplied graph-site controls are sufficiency fixtures only and must be labeled `SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION`.
- A min-norm/Hodge current is a control only unless a previously certified selected current for the exact same realization and carrier is found and hash-bound.
- No downstream v14.02/v14.03 boundary radius, hidden tangent norm, or dual-ray quality may select among source families.
- Primary gate outcome must be one of `GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY`, `NO_CERTIFIED_GRAPH_SITE_FACTORIZATION`, `GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT`, `STATE_INDEPENDENT_GRAPH_SOURCE_CENTRAL_PGRL_NULL`, `STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE`, or `UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT`.
- `scientific_breakthrough=true` only if the archive itself supplies an exact retained-node graph-site factorization, a noncentral locally covariant unique projective source law, and an earned natural map into the certified compatibility parent/support.
- Pillar 3 remains OPEN unless an independent later gate closes it.

---

### Task 1: Freeze RED checker and branch CI

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.03/CHECKER.py`
- Create: `.github/workflows/uqcf-v1503-graph-site-source-lift.yml`

**Interfaces:**
- Consumes: no `graph_site_source_audit.py` yet.
- Produces: branch TDD contract and pinned CI environment.

- [ ] **Step 1: Write the failing checker**

Create:

```python
#!/usr/bin/env python3
from graph_site_source_audit import run_audit

r = run_audit()
assert r["version"] == "v15.03"
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["dimension_theorem"]["compatibility_parent_dimension"] == 125
assert r["dimension_theorem"]["five_nontrivial_factorization_possible"] is False
assert r["centrality_theorem"]["analytic_classification"] == "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER"
assert r["centrality_controls"]["identity_invariance_error"] < 2e-12
assert r["centrality_controls"]["noncentral_independent_frame_violation"] > 1e-6
assert r["state_dependent_controls"]["classification"] == "SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION"
assert r["Pillar_3"] == "OPEN"
assert r["gate_outcome"] in {
    "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY",
    "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION",
    "GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT",
    "STATE_INDEPENDENT_GRAPH_SOURCE_CENTRAL_PGRL_NULL",
    "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE",
    "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT",
}
print("V15_03_GRAPH_SITE_SOURCE_LIFT_CHECKER_PASS")
```

- [ ] **Step 2: Create branch workflow**

Use:

```yaml
name: UQCF v15.03 Graph-Site Source Lift Audit

on:
  push:
    branches:
      - main
      - research/v15.03-graph-site-source-lift
    paths:
      - 'ResearchHistory/UQCF-GEM/v15/v15.03/**'
      - 'Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py'
      - 'Tmp/TOE/ThePhysicsParadox/uqcf_gate_a_small_network_phi_simulation_package 2/**'
      - 'ResearchHistory/UQCF-GEM/v13/v13.11/**'
      - 'ResearchHistory/UQCF-GEM/v13/v13.15/**'
      - 'ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/**'
      - 'Tmp/TOE/UQCF_Quantum_Compatibility_Lab/**'
      - 'ResearchHistory/UQCF-GEM/v14/v14.03/**'
      - 'ResearchHistory/UQCF-GEM/v14/v14.04/**'
      - 'ResearchHistory/UQCF-GEM/v15/v15.01/**'
      - 'ResearchHistory/UQCF-GEM/v15/v15.02/**'
      - 'ResearchHistory/UQCF-GEM/README.md'
      - 'ResearchHistory/UQCF-GEM/STATUS.md'
      - 'docs/superpowers/specs/2026-09-13-v1503-graph-site-source-lift-design.md'
      - 'docs/superpowers/plans/2026-09-13-v1503-graph-site-source-lift.md'
      - '.github/workflows/uqcf-v1503-graph-site-source-lift.yml'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    env:
      OPENBLAS_NUM_THREADS: '1'
      OMP_NUM_THREADS: '1'
      MKL_NUM_THREADS: '1'
      PYTHONHASHSEED: '0'
    defaults:
      run:
        working-directory: ResearchHistory/UQCF-GEM/v15/v15.03
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install scientific dependencies
        run: python -m pip install numpy==2.4.6 scipy==1.17.1
      - name: Run v15.03 checker
        run: python CHECKER.py
```

- [ ] **Step 3: Commit RED contract**

Commit message:

```text
test: add v15.03 graph-site RED gate
```

- [ ] **Step 4: Verify intended RED**

Expected CI failure:

```text
ModuleNotFoundError: No module named 'graph_site_source_audit'
```

Any other RED failure must be diagnosed before implementation.

---

### Task 2: Implement exact archive/type and dimension audit

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.03/graph_site_source_audit.py`

**Interfaces:**
- Produces:
  - `sha256_file(path: Path) -> str`
  - `parse_source_fixture() -> dict[str, Any]`
  - `archive_graph_site_audit() -> dict[str, Any]`
  - `dimension_factorization_audit() -> dict[str, Any]`
  - `run_audit() -> dict[str, Any]`

- [ ] **Step 1: Bind exact retained source fixture**

Parse `phi lab.py` with `ast` rather than importing plotting/runtime side effects. Require:

```python
nodes == (0, 1, 2, 3, 4)
edges == ((0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4))
source == (-1.0,0.0,0.0,1.0,0.0)
```

Compute incidence matrix with `-1` at tail and `+1` at head. Record node count `5`, edge count `7`, rank `4`, cycle dimension `3`, and source sum absolute value.

- [ ] **Step 2: Hash every frozen archive artifact used for graph-site evidence**

At minimum inspect and record path/SHA-256 plus semantic evidence for:

```text
ResearchHistory/UQCF-GEM/v13/v13.15/
ResearchHistory/UQCF-GEM/v13/v13.11/
ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/
Tmp/TOE/ThePhysicsParadox/uqcf_gate_a_small_network_phi_simulation_package 2/
ResearchHistory/UQCF-GEM/v14/v14.04/
ResearchHistory/UQCF-GEM/v15/v15.01/
ResearchHistory/UQCF-GEM/v15/v15.02/
```

Use deterministic recursive file listing sorted by relative path. For each candidate classify evidence as one of:

```text
EXACT_RETAINED_GRAPH_SITE_IDENTITY
GRAPH_INDEXED_QUANTUM_MODEL_CONTROL_ONLY
LOCAL_FRAME_COVARIANCE_ONLY
NO_GRAPH_SITE_IDENTITY_STATEMENT
```

Do not infer identity from matching node counts or demonstrations.

- [ ] **Step 3: Implement the exact `125=5^3` theorem executable check**

Enumerate integer tuples `d_i >= 2` with product `125`. Because `2^5 > 125`, a finite search over `range(2,126)` is sufficient with early product cutoff. Assert no five-tuple exists. Record:

```python
{
  "compatibility_parent_dimension": 125,
  "required_site_count": 5,
  "minimum_site_dimension": 2,
  "five_nontrivial_factorization_possible": False,
  "prime_factorization": [5,5,5],
  "classification": "FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT",
}
```

- [ ] **Step 4: Determine graph-site factorization and carrier statuses only from frozen evidence**

Return exactly one factorization status:

```text
EXACT_GRAPH_SITE_FACTORIZATION_CERTIFIED
GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED
NO_GRAPH_INDEXED_QUANTUM_CARRIER_FOUND
```

Return carrier evidence fields that distinguish:

```text
FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT
NATURAL_MAP_TO_COMPATIBILITY_PARENT_CERTIFIED
GRAPH_SITE_CARRIER_DISTINCT_FROM_COMPATIBILITY_PARENT
NO_EXACT_GRAPH_SITE_CARRIER
```

A natural-map success requires an explicit archived typed map/intertwiner into the exact certified compatibility parent/support; mere dimensional embeddings do not count.

- [ ] **Step 5: Commit archive/type layer**

Commit message:

```text
feat: add v15.03 graph-site archive and dimension audit
```

---

### Task 3: Implement state-independent local-gauge centrality theorem controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.03/graph_site_source_audit.py`

**Interfaces:**
- Produces:
  - `kron_all(ops: Sequence[np.ndarray]) -> np.ndarray`
  - `embed_site(op: np.ndarray, site: int, dims: Sequence[int]) -> np.ndarray`
  - `swap_operator(dim: int) -> np.ndarray`
  - `deterministic_local_unitaries() -> tuple[np.ndarray, ...]`
  - `centrality_controls() -> dict[str, Any]`

- [ ] **Step 1: Use a five-qubit supplied carrier only as theorem/control fixture**

Set `dims=(2,2,2,2,2)`. This fixture is not archive provenance. Build independent deterministic unitaries from closed-form matrices, e.g. Hadamard, phase rotation `diag(1, exp(i*pi/5))`, and real rotations with fixed angles. Do not draw random frames.

- [ ] **Step 2: Verify central invariance**

For `I_32`, compute

```python
err = np.linalg.norm(U @ I32 @ U.conj().T - I32)
```

for the deterministic product frame. Require `<2e-12`.

- [ ] **Step 3: Verify a noncentral local operator violates invariance under independent frames**

Use supplied coordinate control `Z` on site 0 only:

```python
Pz = embed_site(np.diag([1.0,-1.0]), 0, dims)
```

Apply an independent product frame whose site-0 factor does not commute with `Z`. Record a Frobenius violation and require `>1e-6`.

- [ ] **Step 4: Verify SWAP/current loophole failure under independent frames**

Embed `SWAP_01` on sites 0 and 1. Choose `U0 != U1` and verify

```python
|| (U0 tensor U1) SWAP (U0 tensor U1)^dagger - SWAP ||_F > 1e-6.
```

Also include tied-frame control `U0=U1` showing the SWAP can be invariant under a weaker diagonal action. Label that control `WEAKER_TIED_FRAME_GAUGE_NOT_ADJUDICATION_GAUGE`.

- [ ] **Step 5: Record analytic theorem as primary evidence**

Return:

```python
{
  "analytic_classification": "FULL_PRODUCT_LOCAL_UNITARY_COMMUTANT_IS_CENTER",
  "state_independent_source_classification": "CENTRAL_ONLY",
  "pgrl_classification": "CENTRAL_PGRL_NULL",
  ...controls...
}
```

The numerical controls corroborate but do not replace the representation-theoretic theorem.

- [ ] **Step 6: Commit centrality layer**

Commit message:

```text
feat: certify v15.03 local-gauge centrality controls
```

---

### Task 4: Implement frozen state-dependent covariant source-family audit

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.03/graph_site_source_audit.py`

**Interfaces:**
- Produces:
  - `qubit_state(r: float) -> np.ndarray`
  - `matrix_function_centered(rho: np.ndarray, name: str) -> np.ndarray`
  - `graph_site_source(source, local_states, function_name) -> np.ndarray`
  - `projective_residual(P: np.ndarray, Q: np.ndarray) -> float`
  - `state_dependent_family_audit() -> dict[str, Any]`

- [ ] **Step 1: Freeze supplied states exactly**

Use only:

```python
R_A = (0.15,-0.31,0.42,0.63,-0.22)
R_B = (0.52,-0.18,0.27,-0.47,0.36)
```

with `rho_i=(I+r_i Z)/2`. Verify Hermitian, trace one, and smallest eigenvalue `>0` for every local state.

- [ ] **Step 2: Implement the four predeclared functional-calculus families**

For eigen-decomposition `rho=V diag(lam) V^dagger`, use:

```python
identity: f(lam)=1
linear:   f(lam)=lam
square:   f(lam)=lam**2
log:      f(lam)=np.log(lam)
```

Trace-center each local result before embedding. Reject `log` if any eigenvalue is nonpositive; this should not occur for frozen controls.

- [ ] **Step 3: Build full five-site source operator**

For scalar source `s=(-1,0,0,+1,0)`:

```python
P_f = sum(s[i] * embed_site(centered_f_rho_i, i, dims) for i in range(5))
```

Record Hermiticity error, trace, Frobenius norm, and centered norm for every family/control.

- [ ] **Step 4: Verify constant family is null/central**

Require its centered full-source norm `<2e-12`.

- [ ] **Step 5: Verify independent local-unitary covariance**

Transform every local state with the deterministic independent frames and rebuild `P_f`. Compare with `U_G P_f U_G^dagger`. Require relative Frobenius error `<2e-10` for `linear`, `square`, and `log` on both controls.

- [ ] **Step 6: Verify positive source scaling is projectively inert**

For scales `(0.2,0.5,2.0,5.0,11.0)`, rebuild each noncentral family with scaled scalar source and compare projective ray residual to the unscaled source. Require `<2e-12`.

- [ ] **Step 7: Implement positive-ray projective residual**

Trace-center `P,Q`; normalize by Frobenius norm; because only positive scaling is quotiented, use

```python
min_positive = np.linalg.norm(Pn - Qn)
```

without identifying `Pn` with `-Qn`. Report pairwise residuals among `linear`, `square`, and `log` separately for control A and B.

- [ ] **Step 8: Adjudicate state-dependent uniqueness without adding candidates**

If at least two noncentral lawful families have projective residual `>1e-8` on either frozen control, record:

```text
STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE
```

If all predeclared noncentral families are projectively equivalent within `2e-10`, record `STATE_DEPENDENT_FROZEN_FAMILIES_PROJECTIVELY_EQUIVALENT` as a secondary status only; do not infer universal uniqueness beyond the tested family class.

- [ ] **Step 9: Keep current-based pair lifts control-only**

If a minimum-norm current `J=B^+s` is computed, store it only under `current_control` with:

```python
"scientific_evidence": False,
"classification": "MIN_NORM_CURRENT_CONTROL_NOT_PROVENANCE_SELECTED"
```

Do not allow it into primary gate adjudication.

- [ ] **Step 10: Commit state-dependent layer**

Commit message:

```text
feat: audit v15.03 state-dependent covariant source families
```

---

### Task 5: Implement hierarchical adjudication and preserved boundaries

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.03/graph_site_source_audit.py`

**Interfaces:**
- Produces stable `run_audit() -> dict[str, Any]` schema consumed by checker and frozen summary.

- [ ] **Step 1: Adjudicate upstream statuses before any optional downstream sufficiency control**

Use this order:

```python
if numerical_failure:
    gate_outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"
elif exact_factorization_not_certified:
    gate_outcome = "NO_CERTIFIED_GRAPH_SITE_FACTORIZATION"
elif exact_graph_site_carrier_exists and not natural_map_to_compatibility_parent:
    gate_outcome = "GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT"
elif only_state_independent_retained_data_available:
    gate_outcome = "STATE_INDEPENDENT_GRAPH_SOURCE_CENTRAL_PGRL_NULL"
elif state_dependent_families_nonunique:
    gate_outcome = "STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE"
elif exact_factorization_certified and natural_map_certified and unique_noncentral_covariant_ray:
    gate_outcome = "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY"
else:
    gate_outcome = "UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT"
```

When the archive factorization fails first, preserve the centrality and state-dependent family results as independent secondary theorems/controls rather than letting them override the hierarchical primary outcome.

- [ ] **Step 2: Set breakthrough flag narrowly**

Only:

```python
scientific_breakthrough = (
    gate_outcome == "GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY"
)
```

- [ ] **Step 3: Preserve claim boundaries explicitly**

Return `not_derived` containing at least:

```text
a certified exact retained-node-to-quantum-site factorization, unless Gate A proves it
a natural graph-site-to-C125 compatibility-parent map, unless Gate D proves it
absolute source magnitude
stress-energy
coframe or solder law
physical metric or spacetime
gravity coupling
Einstein equations
physical time primitive
Pillar 3 closure
```

- [ ] **Step 4: Emit deterministic JSON**

When run as a script, print `json.dumps(run_audit(), indent=2, sort_keys=True)`.

- [ ] **Step 5: Commit adjudication layer**

Commit message:

```text
feat: adjudicate v15.03 graph-site source lift gate
```

---

### Task 6: Obtain first GREEN measurement and freeze the archive

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.03/CHECKER.py`
- Create: `ResearchHistory/UQCF-GEM/v15/v15.03/SUMMARY.json`
- Create: `ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md`
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Consumes live `run_audit()` result.
- Produces immutable scientific archive bindings.

- [ ] **Step 1: Run CI on the exact implementation SHA**

Require the branch workflow to complete successfully. If it fails numerically, diagnose the exact invariant before changing thresholds or scientific logic. Do not alter frozen source-state controls to make it pass.

- [ ] **Step 2: Capture the complete live JSON**

Use the checker/job log or a dedicated deterministic run and copy the exact sorted result into `SUMMARY.json`. Do not manually round scientific telemetry beyond JSON serialization.

- [ ] **Step 3: Write `REPORT.md` from the measured result**

The report must separately state:

```text
THEOREM
- five-nontrivial-site carrier cannot literally equal C^125
- state-independent independent-local-gauge source lift is central/PGRL-null

REPRODUCIBLE COMPUTATION
- archive graph-site evidence classification
- deterministic covariance controls
- frozen source-family projective residuals for A/B
- carrier-map archive status

INTERPRETATION
- what missing representation law is localized

UNRESOLVED PHYSICS
- no gravity/stress-energy/Einstein/time primitive claim
- Pillar 3 remains OPEN
```

- [ ] **Step 4: Bind checker to frozen summary without replacing independent thresholds**

Keep the pre-summary structural/scientific asserts, then load `SUMMARY.json` and verify exact categorical fields plus tolerant numeric equality:

```python
def close(actual, frozen):
    tol = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(float(frozen)))
    assert abs(float(actual)-float(frozen)) <= tol
```

Require the frozen primary outcome, breakthrough flag, factorization status, carrier status, centrality classification, state-dependent classification, and all artifact hashes to match live execution.

- [ ] **Step 5: Update research index/status**

Add a concise v15.03 entry to `ResearchHistory/UQCF-GEM/README.md` and `STATUS.md` preserving the hierarchical primary outcome and independent secondary theorem results.

- [ ] **Step 6: Commit frozen archive**

Commit message:

```text
docs: freeze v15.03 graph-site source lift result
```

---

### Task 7: Final exact-SHA certification, review, merge, and regressions

**Files:**
- No scientific code changes after the final certification SHA.

**Interfaces:**
- Produces exact GitHub evidence that the archived result is reproducible and does not regress prior gates.

- [ ] **Step 1: Run verification-before-completion checklist**

Inspect branch diff against `main`; require only intended v15.03 spec/plan/audit/archive/workflow/index/status changes. Ensure no debug-only files or accidental generated artifacts remain.

- [ ] **Step 2: Certify final branch exact SHA**

Require `UQCF v15.03 Graph-Site Source Lift Audit` SUCCESS on the exact final branch SHA after the final documentation/checker commit.

- [ ] **Step 3: Compare with main**

Require the branch to be based on the intended v15.02-certified main head with no unexplained divergence. If main advanced independently, rebase/refresh logically before merge and rerun exact-SHA certification.

- [ ] **Step 4: Merge without force**

Advance `main` using a normal merge/fast-forward path; do not force-update history.

- [ ] **Step 5: Run post-merge exact-SHA v15.03 certification**

Require SUCCESS on the merged main SHA.

- [ ] **Step 6: Run prior-gate regressions on the exact merged SHA**

At minimum certify:

```text
v15.02 shared-label equivariance
v15.01 common-parent representation
v14.04 provenance representation link
v14.03 projective source ray
```

If an older workflow cannot be triggered automatically by unchanged paths, use its `workflow_dispatch` path on the merged main SHA or execute its checker in an equivalent pinned job.

- [ ] **Step 7: Final scientific report-out**

Report primary outcome, exact merge SHA, post-merge CI evidence, theorem/computation/interpretation/unresolved-physics separation, breakthrough flag, and the next lawful research move. If the gate is negative, obey the v15.03 stop rule: do not invent a Pauli axis, choose `log rho`, tie local frames, create a cross-carrier isometry, promote a min-norm current, or use ADM/Einstein/gravity residuals.
