# v15.02 Shared-Label Equivariance / Natural Source Representation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the archived five-node retained source carrier and the three five-level compatibility factors share an earned permutation representation that canonically induces the projective support-source ray consumed by v14.03, without inventing a label bijection, factor placement, source operator, or downstream selector.

**Architecture:** Reuse the exact archived source graph, the v15.01 parent/support representation, the frozen v14.03 source/contact/dual machinery, and the v9.167–v9.171 compatibility lab. Enumerate all `5! = 120` permutations exactly. Separate source-side graph automorphisms, compatibility-side label gauge, node-to-quantum-label double-coset classes, source-operator equivariance, and parent-factor placement. Only the scalar source `D(s)` participates in scientific adjudication unless the audit discovers an archived certified selected-current vector; directed-current operators remain structural controls otherwise. Downstream v14.03 is used only after upstream canonicality is decided.

**Tech Stack:** Python 3.11; NumPy 2.4.6; SciPy 1.17.1; Python standard-library `itertools`, `ast`, `hashlib`; GitHub Actions; archived UQCF compatibility and source-current artifacts.

**Spec:** `docs/superpowers/specs/2026-09-13-v1502-shared-label-equivariance-design.md`

## Global Constraints

- Primitive/pre-pruning ontology remains atemporal.
- Do not use entropy, physical time, Newton/Einstein/ADM residuals, gravity observables, cosmology, or empirical targets to select a label representation or factor action.
- Do not identify the two five-element carriers merely because their cardinalities match.
- Do not reshape/vectorize the 6-D Genesis field, pad another representation to dimension five/125, or choose a label map by PCA/SVD/random alignment.
- Reuse the exact compatibility parent `C^5 tensor C^5 tensor C^5 = C^125`, frozen support `L : C^25 -> C^125`, and v14.03 projective equivalence `P ~ aP + bI`, `a > 0`.
- Enumerate finite permutations exactly; do not Monte-Carlo sample groups or identifications.
- Compare subspaces with projectors/principal-angle-equivalent quantities, never arbitrary null/SVD basis vectors.
- The source graph artifact at `Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py` supplies the frozen structural fixture `NODES=[0,1,2,3,4]`, `EDGES=[(0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4)]`, and balanced source `SOURCE=(-1,0,0,+1,0)`.
- v13.25 certifies the five-node/seven-edge/rank/cycle boundary but does not archive the selected-current vector. Therefore a current-derived operator may not adjudicate the gate unless a matching certified current artifact is discovered and hash-bound during implementation.
- Allowed parent placements are exactly central-factor `A_A`, equal-partner-symmetric `A_B`, and fully symmetric `A_all`; single-partner placements are negative controls only.
- Do not choose a relative coefficient in `D(s)+alpha iK(J)` unless the frozen ontology supplies `alpha`.
- Primary adjudication must be one of `SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY`, `SHARED_LABEL_IDENTIFICATION_NONUNIQUE`, `SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE`, `NO_CERTIFIED_SHARED_LABEL_CARRIER`, or verification-stop `UNRESOLVED_EQUIVARIANCE_AUDIT`.
- Secondary `CENTRAL_ONLY_OR_PGRL_NULL` may be recorded where appropriate.
- Even a positive gate does not derive absolute source magnitude, observer calibration, stress-energy, coframe/solder law, metric/spacetime, gravitational coupling, Einstein equations, or Pillar 3 closure.

---

### Task 1: Freeze RED checker and branch CI

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.02/CHECKER.py`
- Create: `.github/workflows/uqcf-v1502-shared-label-equivariance.yml`

**Interfaces:**
- Consumes: no `shared_label_audit.py` yet.
- Produces: the branch TDD contract and pinned CI environment.

- [ ] **Step 1: Create the failing checker**

Create a checker importing `run_audit` from `shared_label_audit` and asserting only the schema/scientific invariants that are known before execution:

```python
#!/usr/bin/env python3
from shared_label_audit import run_audit

r = run_audit()
assert r["version"] == "v15.02"
assert r["permutation_count"] == 120
assert r["source_fixture"]["node_count"] == 5
assert r["source_fixture"]["edge_count"] == 7
assert r["source_fixture"]["source_sum_abs"] < 1e-14
assert r["Pillar_3"] == "OPEN"

assert r["scalar_source_controls"]["constant_source_norm"] < 1e-12
assert r["scalar_source_controls"]["max_permutation_covariance_error"] < 2e-12
assert r["scalar_source_controls"]["max_positive_scale_projective_residual"] < 2e-12

for name in ("V_A", "V_B"):
    c = r["compatibility"][name]
    assert c["support_dimension"] == 25
    assert c["parent_dimension"] == 125
    assert c["max_projector_covariance_error"] < 2e-9

assert r["positive_control"]["classification"] == "SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION"
assert r["incompatible_control"]["classification"] == "INCOMPATIBLE_LABEL_ACTION_REJECTED"

assert r["gate_outcome"] in {
    "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY",
    "SHARED_LABEL_IDENTIFICATION_NONUNIQUE",
    "SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE",
    "NO_CERTIFIED_SHARED_LABEL_CARRIER",
    "UNRESOLVED_EQUIVARIANCE_AUDIT",
}
print("V15_02_SHARED_LABEL_EQUIVARIANCE_CHECKER_PASS")
```

- [ ] **Step 2: Create CI workflow**

Use:

```yaml
name: UQCF v15.02 Shared-Label Equivariance Audit
on:
  push:
    branches:
      - main
      - research/v15.02-shared-label-equivariance
    paths:
      - 'ResearchHistory/UQCF-GEM/v15/v15.02/**'
      - 'Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py'
      - 'Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py'
      - 'ResearchHistory/UQCF-GEM/v13/v13.25/**'
      - 'ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py'
      - 'ResearchHistory/UQCF-GEM/v15/v15.01/**'
      - 'ResearchHistory/UQCF-GEM/README.md'
      - 'ResearchHistory/UQCF-GEM/STATUS.md'
      - 'docs/superpowers/specs/2026-09-13-v1502-shared-label-equivariance-design.md'
      - 'docs/superpowers/plans/2026-09-13-v1502-shared-label-equivariance.md'
      - '.github/workflows/uqcf-v1502-shared-label-equivariance.yml'
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
        working-directory: ResearchHistory/UQCF-GEM/v15/v15.02
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install numpy==2.4.6 scipy==1.17.1
      - run: python CHECKER.py
```

- [ ] **Step 3: Commit RED files**

Commit message:

```text
test: add v15.02 shared-label RED gate
```

- [ ] **Step 4: Verify intended RED**

Expected failure:

```text
ModuleNotFoundError: No module named 'shared_label_audit'
```

Any other failure must be diagnosed before production implementation.

---

### Task 2: Implement deterministic permutation and archived source-fixture layer

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`

**Interfaces:**
- Produces:
  - `all_permutations() -> tuple[tuple[int,...], ...]`
  - `compose_perm(p, q) -> tuple[int,...]`
  - `inverse_perm(p) -> tuple[int,...]`
  - `permutation_matrix(p) -> np.ndarray`
  - `parse_source_fixture() -> dict[str, Any]`
  - `incidence_matrix(nodes, edges) -> np.ndarray`
  - `source_side_audit(fixture) -> dict[str, Any]`

- [ ] **Step 1: Enumerate `S5` exactly**

Use `tuple(itertools.permutations(range(5)))`; assert length `120`, unique elements `120`, identity present, inverse/compose closure exact.

- [ ] **Step 2: Parse the archived source fixture without importing the plotting program**

Read `Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py`. Use `ast.parse` to recover literal `NODES` and `EDGES`; parse the `SOURCE[index]=value` assignments from the AST. Require exactly:

```python
nodes == (0,1,2,3,4)
edges == ((0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4))
source == (-1.0,0.0,0.0,1.0,0.0)
```

Record SHA-256 of the file and SHA-256 of the canonical JSON fixture.

- [ ] **Step 3: Reconstruct the incidence matrix**

Use the archived convention `-1` at edge tail, `+1` at head. Verify rank `4`, cycle dimension `3`, source sum zero, and the v13.25 summary dimensions `nodes=5`, `edges=7`, `cycle_dimension=3`.

- [ ] **Step 4: Enumerate source structural automorphisms**

A permutation `p` is in `G_src` iff the directed edge set maps to itself:

```python
{(p[u], p[v]) for (u,v) in edges} == set(edges)
```

Separately compute the source-state stabilizer requiring `source[p^{-1}(i)] == source[i]` in addition to graph preservation. Record both groups as sorted permutation tuples and SHA-256 hashes.

- [ ] **Step 5: Commit source/group foundation**

Commit message:

```text
feat: add v15.02 exact source permutation audit
```

---

### Task 3: Implement compatibility-side label gauge without basis-vector dependence

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`

**Interfaces:**
- Consumes: v15.01 parent configuration helper and archived compatibility lab.
- Produces:
  - `load_v1501() -> ModuleType`
  - `build_configs() -> dict[str, dict[str, Any]]`
  - `parent_perm_unitary(p) -> np.ndarray`
  - `support_projector(L) -> np.ndarray`
  - `compatibility_side_audit(cfg, p) -> dict[str, Any]`
  - `compatibility_groups(configs) -> dict[str, Any]`

- [ ] **Step 1: Load `V_A` and `V_B` at frozen `FIXED_T=21/41`**

Reuse v15.01/v14.03 loaders. Do not recompute a different support selection.

- [ ] **Step 2: Define parent permutation action**

For `U_p = permutation_matrix(p)`, define

```python
U3 = np.kron(np.kron(U_p, U_p), U_p)
```

and transformed support projector `Pi_p = U3 @ Pi @ U3.conj().T`.

- [ ] **Step 3: Enumerate fixed-construction label stabilizers**

For each `p in S5`, test whether the transformed frozen compatibility construction is gauge-equivalent by projector/state invariants rather than support basis columns. At minimum record:

```python
projector_error = ||Pi_p - Pi||_F
state_error = ||U3 T U3^dagger - T||_F
```

and typed arrangement checks separating row/central-label, partner-label, and arrangement-value actions. Only permutations satisfying the typed frozen construction at tolerance `2e-9` enter the fixed-configuration group.

- [ ] **Step 4: Distinguish family covariance from fixed-state symmetry**

Also record whether a permutation merely relabels the model to an isomorphic transformed arrangement. Such covariance is a family property, not automatically a gauge stabilizer for the frozen `V_A`/`V_B` instance. Do not use family covariance alone to collapse identification classes.

- [ ] **Step 5: Define the compatibility group used in the cross-model identification audit**

Because the scientific stack relies on both frozen families, use the intersection of the correctly typed `V_A` and `V_B` fixed-construction groups for the common adjudication group. Record per-family groups and the intersection separately.

- [ ] **Step 6: Add projector-covariance diagnostics**

For every certified group element verify support-projector and compressed-operator covariance below `2e-9`. Do not compare SVD hidden-basis vectors.

- [ ] **Step 7: Commit compatibility symmetry layer**

Commit message:

```text
feat: enumerate v15.02 compatibility label gauge
```

---

### Task 4: Implement exact identification-orbit / double-coset audit

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`

**Interfaces:**
- Produces:
  - `double_cosets(G_comp, G_src) -> list[dict[str, Any]]`
  - `identification_audit(...) -> dict[str, Any]`

- [ ] **Step 1: Implement exact equivalence action**

Represent each node-to-quantum-label bijection by `phi in S5`. Its equivalence orbit is

```python
{compose_perm(gc, compose_perm(phi, inverse_perm(gs)))
 for gc in G_comp for gs in G_src}
```

- [ ] **Step 2: Partition all 120 bijections into disjoint double cosets**

Choose the lexicographically smallest permutation as representative. Assert union size `120`, pairwise disjointness, and that every orbit size divides the finite action count as expected.

- [ ] **Step 3: Record semantic status separately**

The existence of one or more double-coset classes does not itself prove the two carriers share physical semantics. Record whether the archive contains an explicit common functor/semantic identification. If none exists, the only possible positive route is gauge canonicality plus representation covariance exactly as allowed by the approved spec.

- [ ] **Step 4: Commit exact orbit audit**

Commit message:

```text
feat: add v15.02 label identification double-coset audit
```

---

### Task 5: Implement scalar source representation and factor placements

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`

**Interfaces:**
- Produces:
  - `centered_source_operator(s) -> np.ndarray`
  - `current_operator(edges, J) -> np.ndarray`
  - `parent_action(Q, placement) -> np.ndarray`
  - `compress(L, A) -> np.ndarray`
  - `projective_affine_residual(P, Q) -> float`
  - `source_representation_audit(...) -> dict[str, Any]`

- [ ] **Step 1: Implement `D(s)`**

```python
def centered_source_operator(s):
    s = np.asarray(s, dtype=float)
    return np.diag(s) - np.mean(s) * np.eye(5)
```

Verify constant-source null, Hermiticity, exact trace zero, permutation equivariance, and positive-scale projective invariance.

- [ ] **Step 2: Implement directed-current operator as a control-only path by default**

Construct antisymmetric `K(J)` over the archived directed edges and `P_J = 1j*K`. Mark `scientific_evidence=False` unless a certified selected-current artifact is discovered and its hash/type match the v13.25 control. Never use the educational `J_true` to adjudicate provenance physics.

- [ ] **Step 3: Implement exactly three admissible parent placements**

```python
A_A(Q)   = kron(Q, I, I)
A_B(Q)   = (kron(I,Q,I) + kron(I,I,Q))/2
A_all(Q) = (kron(Q,I,I) + kron(I,Q,I) + kron(I,I,Q))/3
```

Also build `B1_only` and `B2_only` negative controls and verify partner exchange swaps them while leaving `A_B` invariant.

- [ ] **Step 4: Verify exact placement equivariance**

For every `p in S5` and every allowed placement, require

```text
A_*(U_p Q U_p^dagger) = U3 A_*(Q) U3^dagger
```

within `2e-12`.

- [ ] **Step 5: Implement projective-affine residual**

Center both Hermitian matrices by trace. Solve positive least-squares scale `a`; identity shift is thereby removed. If `a <= 0`, return inequivalent. Use Frobenius normalization and tolerance `2e-9`.

- [ ] **Step 6: Compress every double-coset representative / placement into both frozen supports**

For each identification representative `phi`, transform `s` into the quantum label order, build `Q=D(phi*s)`, each parent placement, and

```python
P = L.conj().T @ A @ L
```

for `V_A` and `V_B`. Record centered norm and all pairwise projective residuals.

- [ ] **Step 7: Determine whether identification ambiguity is downstream-inert**

Multiple double-coset classes count as harmless only if, for every eligible scalar-source fixture, every class gives the same positive projective compressed source class in both `V_A` and `V_B` under every surviving lawful placement. Otherwise classify identification nonuniqueness.

- [ ] **Step 8: Determine factor-placement uniqueness**

If the label identification is canonical/inert, compare `A_A`, `A_B`, `A_all`. If frozen structure independently selects no one placement and compressed classes differ by more than `2e-9`, classify factor-action nonuniqueness.

- [ ] **Step 9: Commit source/placement implementation**

Commit message:

```text
feat: audit v15.02 source representation and factor placement
```

---

### Task 6: Add downstream v14.03 controls without allowing circular selection

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`

**Interfaces:**
- Consumes: `source_contact()` from v14.03.
- Produces:
  - `downstream_control(...) -> dict[str, Any]`
  - `supplied_positive_control(...) -> dict[str, Any]`
  - `incompatible_label_control(...) -> dict[str, Any]`

- [ ] **Step 1: Run v14.03 only for upstream-selected or explicit-control rays**

For each source ray allowed by the upstream adjudication, call `v1403.source_contact(...)`. Record hidden classification, boundary simplicity, normal classification, boundary radius, and oriented dual representative. These values may not feed back into choice of label class or placement.

- [ ] **Step 2: Supplied shared-label positive control**

Explicitly choose identity bijection and `A_A` as a declared control regardless of scientific result. Verify permutation/source representation covariance, noncentral compression where available, and successful v14.03 contact for at least one frozen configuration. Label:

```text
SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION
```

- [ ] **Step 3: Incompatible action negative control**

Choose a permutation outside the certified compatibility fixed-construction group, verify its projector/state error exceeds the gauge tolerance, and label:

```text
INCOMPATIBLE_LABEL_ACTION_REJECTED
```

- [ ] **Step 4: Commit controls**

Commit message:

```text
test: add v15.02 downstream and incompatible controls
```

---

### Task 7: Implement final adjudication and first GREEN scientific run

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/CHECKER.py`

**Interfaces:**
- Produces `run_audit() -> dict[str, Any]` with complete scientific record.

- [ ] **Step 1: Freeze adjudication hierarchy**

Use this order:

```python
if numerical_or_archive_verification_failure:
    gate_outcome = "UNRESOLVED_EQUIVARIANCE_AUDIT"
elif no_certified_common_label_action:
    gate_outcome = "NO_CERTIFIED_SHARED_LABEL_CARRIER"
elif identification_classes_are_structurally_inequivalent:
    gate_outcome = "SHARED_LABEL_IDENTIFICATION_NONUNIQUE"
elif factor_placements_are_equally_lawful_and_projectively_inequivalent:
    gate_outcome = "SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE"
elif unique_or_projectively_inert_identification_and_factor_action_and_noncentral_source:
    gate_outcome = "SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY"
else:
    gate_outcome = "NO_CERTIFIED_SHARED_LABEL_CARRIER"
```

Record `CENTRAL_ONLY_OR_PGRL_NULL` as secondary if the only surviving source classes center to zero.

- [ ] **Step 2: Require all structural controls before GREEN**

Scientific thresholds include:

```text
permutation count = 120
fixture hash present
source graph rank = 4
cycle dimension = 3
source sum abs < 1e-14
scalar permutation covariance < 2e-12
factor-placement equivariance < 2e-12
certified compatibility projector covariance < 2e-9
double-coset partition covers exactly 120 bijections
positive control succeeds independently of adjudication
incompatible control is rejected
Pillar 3 = OPEN
```

- [ ] **Step 3: Commit the first production audit**

Commit message:

```text
feat: implement v15.02 shared-label equivariance audit
```

- [ ] **Step 4: Run exact-SHA GREEN candidate**

Do not interpret a failed run scientifically until distinguishing implementation/numerical error from structural result. Do not relax tolerances to obtain a preferred outcome.

---

### Task 8: Freeze `SUMMARY.json`, `REPORT.md`, and bind the checker

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v15/v15.02/SUMMARY.json`
- Create: `ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md`
- Modify: `ResearchHistory/UQCF-GEM/v15/v15.02/CHECKER.py`

**Interfaces:**
- Produces the immutable archived adjudication for exact-SHA certification.

- [ ] **Step 1: Copy telemetry only from an exact successful production run**

Do not reconstruct floating values manually. Freeze group orders/hashes, double-coset count/sizes/representatives, projective-residual extrema, factor-action status, control classifications, and downstream control telemetry.

- [ ] **Step 2: Write claim-boundary report**

Separate:

```text
THEOREM / EXACT FINITE GROUP RESULT
EXECUTED NUMERICAL COMPUTATION
INTERPRETATION
NOT DERIVED
```

A positive v15.02 result is a candidate architectural breakthrough only; do not call it gravity or Pillar 3 closure.

- [ ] **Step 3: Bind checker to frozen discrete record and hashes**

Keep scientific thresholds independent. Bind exact discrete fields and artifact hashes. Floating telemetry uses an explicit tolerance such as:

```python
def close(actual, frozen):
    tol = 1e-12 + 1e-9 * max(1.0, abs(float(actual)), abs(float(frozen)))
    assert abs(float(actual)-float(frozen)) <= tol
```

Do not use v14.02-style exact equality on basis-sensitive floating survey statistics.

- [ ] **Step 4: Certify summary-bound exact branch SHA**

Require CI success before documentation/status changes.

---

### Task 9: Publish canonical status, final-certify, merge, and regress

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Produces canonical repository frontier only after the scientific package is frozen.

- [ ] **Step 1: Update README/STATUS with exact claim boundary**

Preserve v13.26/v13.28 scale/coupling obstructions, v14.01 nonuniqueness, v14.02 dual-ray result, v14.03 conditional `[P] -> X* -> [g]`, v14.04 representation-link obstruction, and v15.01 common-parent result.

- [ ] **Step 2: Exact-head branch certification**

Run v15.02 on the final documentation head. No scientific or documentation edits after the release-candidate SHA goes green.

- [ ] **Step 3: Compare branch to `main`**

Require `0 behind` and only the intended workflow/spec/plan/v15.02 gate plus README/STATUS files.

- [ ] **Step 4: Fast-forward `main` only after clean diff**

Use non-force ref update.

- [ ] **Step 5: Post-merge safeguards on the exact merged SHA**

Require:

```text
v15.02
v15.01
v14.04
v14.03
v14.02
v14.01
v13.28
```

If v14.02 shows the already-known basis-sensitive frozen-telemetry flake while its scientific classification is intact, diagnose and rerun unchanged; do not alter v14.02 inside v15.02 unless a deterministic code regression is demonstrated.

- [ ] **Step 6: Final main-ref verification**

Confirm `main` points to the exact certified merged SHA before declaring v15.02 complete.
