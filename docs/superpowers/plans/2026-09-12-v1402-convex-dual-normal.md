# v14.02 Convex-Dual Boundary Normal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the full hidden global-compatibility spectrahedra for the archived `V_A` and `V_B` constructions carry an objective-independent canonical local dual ray at their PSD boundaries.

**Architecture:** Reuse the archived `UQCF_Quantum_Compatibility_Lab` exactly for the physical/mathematical compatibility construction, then add a focused v14.02 audit that works in the full Hermitian hidden kernel. The audit constructs frozen radial PSD boundaries, computes the intrinsic normal cone relative to the hidden affine fiber, certifies support identities and hidden-basis invariance, and separately verifies interior and synthetic degenerate controls. The checker adjudicates only the frozen outcomes from the design and is finally bound to `SUMMARY.json`.

**Tech Stack:** Python 3.11, NumPy 2.4.6, SciPy 1.17.1, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-12-v1402-convex-dual-normal-design.md`

## Global Constraints

- Work only on branch `research/v14.02-convex-dual-normal` until exact-SHA certification succeeds.
- Reuse `Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`; do not replace the compatibility construction with a new primary toy model.
- Use the full hidden Hermitian kernel from `hidden_basis(L)`, never the 3D visualization section, for scientific adjudication.
- Deterministic seed: `1402`.
- Survey exactly 64 radial directions for `V_A` and exactly 64 for `V_B`.
- Hermiticity residual tolerance: `1e-11`.
- Hidden-kernel/marginal residual tolerance: `1e-10`.
- Boundary PSD residual tolerance: `1e-10 * max(1, ||X_*||_2)`.
- Nullity threshold: `tau_null = 1e-9 * max(1, ||X_*||_2)`.
- A boundary is simple only when exactly one eigenvalue satisfies `abs(lambda) <= tau_null` and the second-smallest eigenvalue is at least `100*tau_null`.
- Normal-rank SVD threshold: `1e-10` relative to the largest singular value.
- Support-identity and basis-invariance certification tolerance: `2e-9` relative error.
- The archived trace-distance dual effect is a typed comparison object only: `VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE`.
- Gate outcomes are exactly `CANONICAL_DUAL_RAY`, `NONUNIQUE_NORMAL_CONE`, or `NO_BOUNDARY_SELECTOR`; `UNRESOLVED_NUMERICAL_BOUNDARY` is a verification-stop state only.
- No source law, coupling magnitude, stress-energy, spacetime, curvature, or Einstein claim may be inferred from a local dual ray.
- Pin Python 3.11, NumPy 2.4.6, and SciPy 1.17.1 in CI. SciPy 1.17.1 supports Python >=3.11.
- Pillar 3 remains OPEN regardless of gate result.

---

### Task 1: Freeze the RED certification interface

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/CHECKER.py`
- Create: `.github/workflows/uqcf-v1402-convex-dual-normal.yml`

**Interfaces:**
- Consumes: `run_audit() -> dict` from `dual_normal_audit.py`.
- Produces: deterministic assertions over construction provenance, survey counts, tolerances, control outcomes, and the scientific gate classification.

- [ ] **Step 1: Write the RED checker**

Create `CHECKER.py` with the following required assertions before `dual_normal_audit.py` exists:

```python
#!/usr/bin/env python3
import json
from dual_normal_audit import run_audit

result = run_audit()

assert result["version"] == "v14.02"
assert result["seed"] == 1402
assert result["survey"]["V_A"]["sample_count"] == 64
assert result["survey"]["V_B"]["sample_count"] == 64
assert result["primary_sample_count"] == 128
assert result["construction"]["uses_full_hidden_kernel"] is True
assert result["construction"]["uses_visualization_section"] is False
assert result["typed_dual_control"] == "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE"
assert result["interior_control"]["classification"] == "NO_BOUNDARY_SELECTOR"
assert result["interior_control"]["minimum_center_eigenvalue"] > 0.0
assert result["synthetic_degenerate_control"]["classification"] == "NONUNIQUE_NORMAL_CONE"
assert result["synthetic_degenerate_control"]["projected_normal_span_rank"] >= 2
assert result["max_boundary_psd_residual"] < 2e-9
assert result["max_support_identity_relative_error"] < 2e-9
assert result["max_basis_invariance_relative_error"] < 2e-9
assert result["zero_projected_normal_count"] == 0
assert result["gate_outcome"] in {
    "CANONICAL_DUAL_RAY",
    "NONUNIQUE_NORMAL_CONE",
    "NO_BOUNDARY_SELECTOR",
    "UNRESOLVED_NUMERICAL_BOUNDARY",
}

print("V14_02_CONVEX_DUAL_NORMAL_CHECKER_PASS")
print(json.dumps(result, indent=2, sort_keys=True))
```

- [ ] **Step 2: Add branch/main CI**

Create `.github/workflows/uqcf-v1402-convex-dual-normal.yml` that:

```yaml
name: UQCF v14.02 Convex Dual Normal Audit

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - research/v14.02-convex-dual-normal
    paths:
      - 'ResearchHistory/UQCF-GEM/v14/v14.02/**'
      - 'Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py'
      - 'ResearchHistory/UQCF-GEM/README.md'
      - 'ResearchHistory/UQCF-GEM/STATUS.md'
      - 'docs/superpowers/specs/2026-09-12-v1402-convex-dual-normal-design.md'
      - 'docs/superpowers/plans/2026-09-12-v1402-convex-dual-normal.md'
      - '.github/workflows/uqcf-v1402-convex-dual-normal.yml'

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    env:
      OPENBLAS_NUM_THREADS: '1'
      OMP_NUM_THREADS: '1'
      MKL_NUM_THREADS: '1'
      PYTHONHASHSEED: '0'
    defaults:
      run:
        working-directory: ResearchHistory/UQCF-GEM/v14/v14.02
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install scientific dependencies
        run: python -m pip install numpy==2.4.6 scipy==1.17.1
      - name: Run v14.02 checker
        run: python CHECKER.py
```

- [ ] **Step 3: Push and verify RED**

Expected CI failure: `ModuleNotFoundError: No module named 'dual_normal_audit'`.

- [ ] **Step 4: Commit**

Commit message: `test: add v14.02 convex-dual RED gate`.

---

### Task 2: Implement archived-lab loader and full-hidden-fiber construction

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces: `load_archived_lab()`, `build_primary_configuration(name: str) -> dict`, `normalized_hidden_directions(dim: int, count: int, rng) -> ndarray`.
- Consumes archived functions: `build_completion`, `hidden_basis`, constants `V_A`, `V_B`, `FIXED_T`.

- [ ] **Step 1: Implement repository-root loading without copying archived science**

Use `importlib.util.spec_from_file_location` and locate the repository root from `Path(__file__).resolve().parents[5]`. Load:

```text
Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py
```

The loader must fail loudly if the path is absent.

- [ ] **Step 2: Build each actual configuration**

For each of `V_A`, `V_B`:

```python
state = lab.build_completion(V, lab.FIXED_T)
modes, hidden_report = lab.hidden_basis(state["L"])
```

Assert/check and record:

```python
np.linalg.norm(modes - np.swapaxes(modes.conj(), -1, -2)) < 1e-11
hidden_report["maximum_marginal_null_residual"] < 1e-10
np.min(np.diag(state["X0"])) > 0
```

Return the archived state, full hidden basis, and hidden report. Do not call `choose_section`.

- [ ] **Step 3: Freeze deterministic full-hidden directions**

For each configuration, use the shared RNG initialized with `np.random.default_rng(1402)`, generate 64 Gaussian vectors in hidden-coordinate dimension, and normalize each row to Euclidean norm one. Record SHA-256 of the direction array bytes for reproducibility.

- [ ] **Step 4: Commit**

Commit message: `feat: load archived full compatibility fibers for v14.02`.

---

### Task 3: Implement boundary and intrinsic normal-cone mathematics

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces:
  - `radial_boundary(X0, modes, u) -> dict`
  - `kernel_hermitian_basis(r: int) -> ndarray`
  - `project_hidden_covector(modes, Y) -> ndarray`
  - `normal_cone_audit(Xstar, modes) -> dict`

- [ ] **Step 1: Construct the exact radial boundary**

For normalized `u`, compute

```python
D = np.einsum("a,aij->ij", u, modes, optimize=True)
D = (D + D.conj().T) / 2
inv_sqrt = np.diag(1 / np.sqrt(np.diag(X0)))
G = inv_sqrt @ D @ inv_sqrt
lam = np.linalg.eigvalsh(G)
assert lam[0] < 0
r = -1.0 / lam[0]
Xstar = (X0 + r * D + (X0 + r * D).conj().T) / 2
```

Record radius, Hermiticity residual, trace of `D`, `||Xstar||_2`, minimum eigenvalue residual, second-smallest eigenvalue, `tau_null`, nullity, and simple/near-degenerate status.

- [ ] **Step 2: Implement a complete Hermitian basis on a kernel**

For kernel dimension `r`, return `r^2` Hilbert–Schmidt-orthonormal Hermitian matrices: diagonal projectors, real symmetric off-diagonal matrices divided by `sqrt(2)`, and imaginary antisymmetric Hermitian matrices divided by `sqrt(2)`.

- [ ] **Step 3: Project ambient PSD normals into hidden dual coordinates**

Implement:

```python
def project_hidden_covector(modes, Y):
    return np.real(np.einsum("aij,ji->a", modes.conj(), Y, optimize=True))
```

For `V0` spanning `ker(Xstar)`, map every kernel Hermitian basis element `Z_mu` to

```python
Y_mu = V0 @ Z_mu @ V0.conj().T
g_mu = project_hidden_covector(modes, Y_mu)
```

Compute the rank of the real-linear map with SVD threshold `1e-10*smax`.

- [ ] **Step 4: Distinguish PSD ray consistency from linear-span rank**

If nullity is one, use `Y=vv^dagger` and require nonzero projected `g`.

If nullity is greater than one and span rank is one, additionally test every kernel basis vector rank-one projector `v_i v_i^dagger` plus normalized deterministic superpositions `(v_i+v_j)/sqrt(2)` and `(v_i+i v_j)/sqrt(2)`. Normalize nonzero projected covectors and require pairwise dot products `> 1-2e-9` (same positive ray). If not, classify the point as nonunique.

- [ ] **Step 5: Commit**

Commit message: `feat: compute intrinsic compatibility normal cones`.

---

### Task 4: Implement support-identity, basis-invariance, and typed-objective controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces:
  - `support_identity_audit(...) -> float`
  - `basis_invariance_audit(...) -> float`
  - `orthogonal_objective_control(...) -> dict`

- [ ] **Step 1: Verify the exact support identity on feasible points**

For a simple/ray-valued boundary with representative `g`, choose the kernel-supported PSD normal `Y` used to form it. Let boundary coordinates be `xstar = r*u`.

Verify at:

- center `x=0`;
- convex points `x=t*xstar` for `t in {0.2,0.5,0.8}`;
- four independently sampled radial directions `w`, each shrunk to `0.5*rmax(w)`.

For each point:

```python
lhs = g @ (x - xstar)
rhs = np.real(np.trace(Y @ X(x)))
```

because `Tr(Y Xstar)=0`. Record maximum relative/absolute scaled mismatch and require nonnegative support sign within tolerance.

- [ ] **Step 2: Test eight deterministic hidden-basis rotations per actual configuration**

Use two-plane Givens rotations, not a dense arbitrary-basis rewrite. For each rotation on coordinate pair `(p,q)` and frozen angle `theta`, rotate only the two affected basis elements and the corresponding two coordinates of `g`. Reconstruct

```python
NH = np.einsum("a,aij->ij", g, modes)
NH_rot = np.einsum("a,aij->ij", g_rot, modes_rot)
```

and record relative Frobenius error. Use eight predeclared pairs/angles generated from seed 1402 after primary directions are frozen.

- [ ] **Step 3: Keep the archived visible-objective dual outside the hidden-fiber result**

Do not compare the archived `W`/trace-distance effect to hidden `g`. Record only:

```python
"typed_dual_control": "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE"
```

and provenance that the archived lab’s objective is stipulated.

- [ ] **Step 4: Add orthogonal-objective sensitivity at simple boundaries**

For a normalized intrinsic `g`, construct deterministic `h` by taking a frozen random vector, removing its projection onto `g`, and normalizing. Demonstrate `h` is not a supporting normal at that point by using a sufficiently small feasible tangent/interior displacement in a direction with `h·delta < 0` while remaining inside the spectrahedron. Record the maximum negative support value found as an objective-independence sensitivity control; it must not enter the primary gate classification unless the support identity itself fails.

- [ ] **Step 5: Commit**

Commit message: `test: certify v14.02 intrinsic support and basis invariance`.

---

### Task 5: Add interior and synthetic-degenerate checker controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces: `interior_control`, `synthetic_degenerate_control` in `run_audit()` output.

- [ ] **Step 1: Interior control from actual archived centers**

For both `V_A` and `V_B`, record `min eig(X0) > 0`. Since the point is strictly interior relative to the hidden fiber, set certified relative normal-cone rank `0` and classification `NO_BOUNDARY_SELECTOR` by convex-analysis theorem, not by an optimization run.

- [ ] **Step 2: Synthetic degenerate test fixture**

Use the explicitly labeled toy fiber

```python
X(x1, x2) = np.diag([x1, x2, 1.0])
```

at `X*=diag([0,0,1])`. Its kernel has dimension two. Projectors onto `e1` and `e2` give independent coordinate normals `(1,0)` and `(0,1)`, so projected normal span rank is 2 and classification is `NONUNIQUE_NORMAL_CONE`.

- [ ] **Step 3: Commit**

Commit message: `test: add v14.02 interior and degenerate controls`.

---

### Task 6: Run the 128-boundary frozen survey and adjudicate

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces final `run_audit() -> dict` used by checker and scientific archive.

- [ ] **Step 1: Execute exactly 64 boundaries per actual configuration**

For every boundary, run construction, normal-cone, support, and classification logic. Basis invariance may be aggregated per configuration but must cover at least eight orthogonal rotations.

- [ ] **Step 2: Aggregate the frozen telemetry**

Return at minimum:

```python
{
    "version": "v14.02",
    "seed": 1402,
    "construction": {...},
    "survey": {"V_A": {...}, "V_B": {...}},
    "primary_sample_count": 128,
    "simple_boundary_count": ...,
    "near_degenerate_boundary_count": ...,
    "zero_projected_normal_count": ...,
    "normal_cone_rank_histogram": {...},
    "minimum_simple_boundary_spectral_gap": ...,
    "max_boundary_psd_residual": ...,
    "max_support_identity_relative_error": ...,
    "max_basis_invariance_relative_error": ...,
    "typed_dual_control": "VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE",
    "source_lift_status": ...,
    "gate_outcome": ...,
    "Pillar_3": "OPEN",
}
```

- [ ] **Step 3: Apply the exact adjudication order**

1. If any frozen tolerance or sensitivity rule leaves unresolved numerical classification, return `UNRESOLVED_NUMERICAL_BOUNDARY` and stop.
2. Else if any primary boundary has genuine projected normal span rank >1 or inequivalent positive PSD normal rays, return `NONUNIQUE_NORMAL_CONE`.
3. Else if all 128 primary boundaries have certified nonzero one-ray cones, return `CANONICAL_DUAL_RAY`.
4. Else return `NO_BOUNDARY_SELECTOR`.

If `CANONICAL_DUAL_RAY`, set source status `CANONICAL_DUAL_DIRECTION_BUT_SOURCE_LIFT_UNDERIVED`; do not fabricate a source tangent.

- [ ] **Step 4: Run the RED-to-GREEN checker**

Run: `python CHECKER.py`.

Expected: `V14_02_CONVEX_DUAL_NORMAL_CHECKER_PASS` and printed deterministic JSON.

- [ ] **Step 5: Commit**

Commit message: `feat: execute v14.02 convex-dual boundary survey`.

---

### Task 7: Freeze report, summary, and bind checker to archive

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/REPORT.md`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/SUMMARY.json`
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/CHECKER.py`

**Interfaces:**
- Consumes exact fresh `run_audit()` output from Task 6.
- Produces human-readable and machine-readable scientific adjudication with executable equality binding.

- [ ] **Step 1: Write the report from actual telemetry**

Report sections must cover:

- compatibility fiber and full-hidden-kernel provenance;
- relative normal-cone theorem;
- frozen numerical conventions;
- actual `V_A` and `V_B` survey counts;
- simple/near-degenerate distribution;
- normal-rank histogram;
- support-identity and basis-invariance evidence;
- typed separation from visible trace-distance dual;
- interior and synthetic-degenerate controls;
- exact gate outcome;
- source-lift boundary and claim limits.

- [ ] **Step 2: Write `SUMMARY.json` with exact numeric values**

Include `scientific_breakthrough: false` unless the executed result independently warrants an explicit upgrade under governance. Do not change Pillar 3.

- [ ] **Step 3: Bind checker to the summary**

After all existing live assertions, load `SUMMARY.json` and compare the frozen scientific fields/numerics to `run_audit()` using exact equality for integers/strings and tight tolerance (`<=1e-15` or exact JSON-emitted floats where deterministic) for scalar telemetry. Fail if the archive drifts from executable output.

- [ ] **Step 4: Run checker again**

Expected: PASS with summary binding.

- [ ] **Step 5: Commit**

Commit message: `docs: freeze v14.02 convex-dual adjudication`.

---

### Task 8: Update canonical research status and certify exact SHA

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Consumes final v14.02 result.
- Produces canonical project frontier without rewriting historical claims.

- [ ] **Step 1: Add v14.02 to the research index**

State only the executed result and link `v14/v14.02/`.

- [ ] **Step 2: Update `STATUS.md`**

Preserve v13.28 and v14.01 branch-stop results; add the precise v14.02 boundary-dual conclusion and lawful next move. Keep Pillar 3 OPEN.

- [ ] **Step 3: Run exact-SHA branch CI**

Wait for the `UQCF v14.02 Convex Dual Normal Audit` workflow on the final branch SHA; require success.

- [ ] **Step 4: Compare branch to `main`**

Require `behind_by = 0` and intended files only.

- [ ] **Step 5: Fast-forward `main` without force**

Only after branch CI is green on the exact head SHA.

- [ ] **Step 6: Verify post-merge CI**

Require v14.02 workflow success on the exact merged SHA. Also inspect any triggered v14.01 and v13.28 regression workflows and require success before final completion claim.

- [ ] **Step 7: Report final links and claim boundary**

Report merged SHA, Actions run(s), report/summary/checker URLs, exact gate classification, what was derived, and what remains underived.
