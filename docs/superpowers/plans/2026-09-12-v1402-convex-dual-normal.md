# v14.02 Convex-Dual Boundary Normal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the full hidden global-compatibility spectrahedra for the archived `V_A` and `V_B` constructions carry an objective-independent canonical local dual ray at their PSD boundaries.

**Architecture:** Reuse the archived `UQCF_Quantum_Compatibility_Lab` exactly for the compatibility construction, then add a focused v14.02 audit that works in the full Hermitian hidden kernel. The audit constructs frozen radial PSD boundaries, computes the intrinsic normal cone relative to the hidden affine fiber, certifies support identities and hidden-basis invariance, and separately verifies interior and synthetic degenerate controls. The checker adjudicates only the frozen outcomes from the design and is finally bound to `SUMMARY.json`.

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

Create `CHECKER.py` with the required assertions over version, seed, sample counts, full-hidden-kernel provenance, typed-dual status, interior and synthetic controls, residual tolerances, nonzero projected normals, and the frozen outcome enum.

- [ ] **Step 2: Add branch/main CI**

Create `.github/workflows/uqcf-v1402-convex-dual-normal.yml` with Python 3.11 and `python -m pip install numpy==2.4.6 scipy==1.17.1`, then run `python CHECKER.py` from `ResearchHistory/UQCF-GEM/v14/v14.02`.

Trigger on branch/main changes to the v14.02 gate, archived compatibility-lab source, canonical README/STATUS, spec/plan, and workflow file.

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

Use `importlib.util.spec_from_file_location` and locate the repository root from `Path(__file__).resolve().parents[4]`. Load `Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`. Fail loudly if absent.

- [ ] **Step 2: Build each actual configuration**

For each of `V_A`, `V_B`:

```python
state = lab.build_completion(V, lab.FIXED_T)
modes, hidden_report = lab.hidden_basis(state["L"])
```

Require Hermiticity residual `<1e-11`, hidden marginal-null residual `<1e-10`, and strictly positive diagonal `X0`. Return archived state, full hidden basis, and hidden report. Do not call `choose_section`.

- [ ] **Step 3: Freeze deterministic full-hidden directions**

Using a shared `np.random.default_rng(1402)`, generate exactly 64 Gaussian normalized coordinate directions per configuration and record SHA-256 of the direction bytes.

- [ ] **Step 4: Commit**

Commit message: `feat: load archived full compatibility fibers for v14.02`.

---

### Task 3: Implement boundary and intrinsic normal-cone mathematics

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces `radial_boundary`, `kernel_hermitian_basis`, `project_hidden_covector`, and `normal_cone_audit`.

- [ ] **Step 1: Construct the exact radial boundary**

For normalized `u`, compute `D=sum_a u_a Q_a`, Hermitian-symmetrize it, form `G=X0^{-1/2} D X0^{-1/2}`, require `lambda_min(G)<0`, set `r=-1/lambda_min(G)`, and build `Xstar=X0+rD`.

Record radius, Hermiticity residual, trace of `D`, `||Xstar||_2`, minimum eigenvalue residual, second-smallest eigenvalue, `tau_null`, nullity, and simple/near-degenerate status using the frozen thresholds.

- [ ] **Step 2: Implement a complete Hermitian basis on a kernel**

For kernel dimension `r`, return `r^2` Hilbert–Schmidt-orthonormal Hermitian matrices: diagonal projectors, real symmetric off-diagonal matrices divided by `sqrt(2)`, and imaginary antisymmetric Hermitian matrices divided by `sqrt(2)`.

- [ ] **Step 3: Project ambient PSD normals into hidden dual coordinates**

Implement `g_a = Re Tr(Q_a Y)` with `np.einsum`; map a complete kernel Hermitian basis through `Y=V0 Z V0^dagger`, project each, and compute the real-linear map rank with SVD threshold `1e-10*smax`.

- [ ] **Step 4: Distinguish PSD ray consistency from linear-span rank**

If nullity is one, use `Y=vv^dagger` and require nonzero projected `g`.

If nullity exceeds one and span rank is one, additionally test kernel rank-one projectors and deterministic superpositions. Normalize nonzero projected covectors and require pairwise dot products `>1-2e-9` for the same positive ray. Otherwise classify the point as nonunique.

- [ ] **Step 5: Commit**

Commit message: `feat: compute intrinsic compatibility normal cones`.

---

### Task 4: Implement support-identity, basis-invariance, and typed-objective controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces `support_identity_audit`, `basis_invariance_audit`, and `orthogonal_objective_control`.

- [ ] **Step 1: Verify the exact support identity on feasible points**

For each ray-valued boundary representative `g,Y`, let `xstar=r*u`. Test the center, convex points `t*xstar` for `t={0.2,0.5,0.8}`, and four independently sampled feasible interior points from other radial directions. Compare `g@(x-xstar)` with `Re Tr(Y X(x))` and enforce the inward support sign.

- [ ] **Step 2: Test eight deterministic hidden-basis rotations per actual configuration**

Use two-plane Givens rotations. Rotate affected hidden basis elements and `g` coordinates, reconstruct `NH=sum_a g_a Q_a`, and record relative Frobenius invariance error. Eight deterministic rotations per configuration are required.

- [ ] **Step 3: Keep the archived visible-objective dual outside the hidden-fiber result**

Record only `VISIBLE_OBJECTIVE_DUAL_WITNESS_DIFFERENT_DUAL_SPACE`; do not compare the old trace-distance dual effect for collinearity with hidden `g`.

- [ ] **Step 4: Add orthogonal-objective sensitivity at simple boundaries**

Construct deterministic `h` orthogonal to normalized `g` and exhibit a sufficiently small feasible interior displacement with `h·delta<0`, showing an arbitrary orthogonal objective is not an intrinsic normal at that smooth boundary.

- [ ] **Step 5: Commit**

Commit message: `test: certify v14.02 intrinsic support and basis invariance`.

---

### Task 5: Add interior and synthetic-degenerate checker controls

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

- [ ] **Step 1: Interior control from actual archived centers**

For both archived centers, record positive minimum eigenvalue and theorem-level relative normal-cone rank zero. Aggregate as `NO_BOUNDARY_SELECTOR`.

- [ ] **Step 2: Synthetic degenerate test fixture**

Use the explicitly labeled toy fiber `X(x1,x2)=diag([x1,x2,1])` at `diag([0,0,1])`. The two kernel projectors produce independent projected normals `(1,0)` and `(0,1)`, so span rank is 2 and classification is `NONUNIQUE_NORMAL_CONE`.

- [ ] **Step 3: Commit**

Commit message: `test: add v14.02 interior and degenerate controls`.

---

### Task 6: Run the 128-boundary frozen survey and adjudicate

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py`

**Interfaces:**
- Produces final `run_audit() -> dict`.

- [ ] **Step 1: Execute exactly 64 boundaries per actual configuration**

For every boundary, run construction, normal-cone, support, and classification logic. Basis invariance may be aggregated per configuration but must cover at least eight orthogonal rotations.

- [ ] **Step 2: Aggregate frozen telemetry**

Return construction provenance, per-configuration sample counts, simple/near-degenerate counts, zero-normal count, rank histogram, minimum simple spectral gap, maximum PSD residual, maximum support-identity error, maximum basis-invariance error, typed-dual status, source-lift status, gate outcome, and Pillar 3 status.

- [ ] **Step 3: Apply exact adjudication order**

1. Unresolved frozen numerical classification -> `UNRESOLVED_NUMERICAL_BOUNDARY` and stop.
2. Any primary boundary with genuine projected normal span rank >1 or inequivalent positive PSD normal rays -> `NONUNIQUE_NORMAL_CONE`.
3. All 128 boundaries certified nonzero one-ray -> `CANONICAL_DUAL_RAY`.
4. Otherwise -> `NO_BOUNDARY_SELECTOR`.

If a canonical ray is found, source status is `CANONICAL_DUAL_DIRECTION_BUT_SOURCE_LIFT_UNDERIVED`; do not fabricate a source tangent.

- [ ] **Step 4: Run checker**

Expected: `V14_02_CONVEX_DUAL_NORMAL_CHECKER_PASS`.

- [ ] **Step 5: Commit**

Commit message: `feat: execute v14.02 convex-dual boundary survey`.

---

### Task 7: Freeze report, summary, and bind checker to archive

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/REPORT.md`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.02/SUMMARY.json`
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.02/CHECKER.py`

- [ ] **Step 1: Write report from actual telemetry**

Cover compatibility-fiber provenance, normal-cone theorem, frozen tolerances, actual `V_A/V_B` survey, rank/gap distribution, support/basis evidence, typed dual separation, controls, gate outcome, source-lift boundary, and claim limits.

- [ ] **Step 2: Write machine-readable summary**

Include exact structural outcomes and executed telemetry. `scientific_breakthrough` remains false unless governance explicitly warrants an upgrade after execution. Pillar 3 stays OPEN.

- [ ] **Step 3: Bind checker to summary**

Load `SUMMARY.json`; require exact equality for structural strings/integers/booleans and `math.isclose(..., rel_tol=5e-12, abs_tol=5e-12)` for floating telemetry. This is tight enough to detect drift while avoiding false failures from BLAS-level last-bit differences.

- [ ] **Step 4: Run checker again**

Expected: PASS with summary binding.

- [ ] **Step 5: Commit**

Commit message: `docs: freeze v14.02 convex-dual adjudication`.

---

### Task 8: Update canonical research status and certify exact SHA

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

- [ ] **Step 1: Add v14.02 to research index**

State only the executed result and link `v14/v14.02/`.

- [ ] **Step 2: Update status**

Preserve v13.28 and v14.01 branch stops; add the precise v14.02 boundary-dual conclusion and lawful next move. Pillar 3 remains OPEN.

- [ ] **Step 3: Run exact-SHA branch CI**

Require success on the final branch head.

- [ ] **Step 4: Compare to main**

Require `behind_by=0` and intended files only.

- [ ] **Step 5: Fast-forward main without force**

Only after exact-SHA branch CI success.

- [ ] **Step 6: Verify post-merge CI and regressions**

Require v14.02 success on exact merged SHA. Inspect any triggered v14.01 and v13.28 regression workflows and require success before completion claim.

- [ ] **Step 7: Report final links and claim boundary**

Report merged SHA, Actions run(s), report/summary/checker URLs, gate classification, what was derived, and what remains underived.
