# UQCF-GEM v14.04 Provenance Representation / Intertwiner Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether the frozen Genesis/provenance stack naturally produces the positive projective Hermitian support-source ray consumed by v14.03, or whether the present ontology is blocked by support-gauge centrality and an unfixed provenance-to-support intertwiner.

**Architecture:** Add one focused executable audit module under `ResearchHistory/UQCF-GEM/v14/v14.04/`. It reuses the certified v14.03 PGRL/contact machinery, proves/controls the support-gauge centrality obstruction for gauge-trivial provenance, inventories richer frozen provenance carriers, and uses explicitly supplied intertwiners only as positive/ambiguity controls. The scientific checker is written first and later bound to a frozen `SUMMARY.json`.

**Tech Stack:** Python 3.11, NumPy 2.4.6, SciPy 1.17.1, existing v14.03/v14.02 audit modules, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-13-v1404-provenance-representation-design.md`

## Global Constraints

- Pre-pruning ontology remains atemporal; do not use entropy/time as a selector.
- Do not use ADM/Einstein residuals, gravity observables, or target downstream dual rays to choose a provenance representation.
- Source output is evaluated projectively under `P ~ a P + b I`, `a > 0`; do not attempt absolute source calibration.
- Gauge-trivial provenance may only count as a nontrivial source representation if it produces a noncentral projective class naturally under support-coordinate changes.
- An arbitrary reshape, random isometry, SVD/PCA alignment, Fourier identification, or dimension match is never evidence for a derived provenance map.
- A supplied intertwiner is a positive/ambiguity control only and must be labeled external declared structure.
- If no frozen natural representation/intertwiner exists and supplied admissible intertwiners produce inequivalent source/downstream rays, stop with `REQUIRES_NEW_REPRESENTATION_LINK`.
- No new representation axiom is introduced in this gate.
- `Pillar_3` remains `OPEN` for every allowed v14.04 outcome.

---

## File Map

- Create `ResearchHistory/UQCF-GEM/v14/v14.04/CHECKER.py` — executable scientific assertions; RED first, later summary-bound.
- Create `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py` — all theorem controls, archive inventory, intertwiner ambiguity control, and gate adjudication.
- Create `ResearchHistory/UQCF-GEM/v14/v14.04/SUMMARY.json` — frozen machine-readable result after first successful production audit.
- Create `ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md` — theorem/computation/interpretation/claim boundary.
- Create `.github/workflows/uqcf-v1404-provenance-representation.yml` — exact branch/main certification.
- Modify `ResearchHistory/UQCF-GEM/README.md` — index v14.04 only after result is frozen.
- Modify `ResearchHistory/UQCF-GEM/STATUS.md` — move frontier only after result is frozen.
- Preserve `ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py`; import it, do not fork its source/contact mathematics.

---

### Task 1: RED checker and CI contract

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.04/CHECKER.py`
- Create: `.github/workflows/uqcf-v1404-provenance-representation.yml`

**Interfaces:**
- Consumes: planned `run_audit() -> dict[str, Any]` from `provenance_representation_audit.py`.
- Produces: frozen assertion contract for all later implementation tasks.

- [ ] **Step 1: Write the failing checker**

Create `CHECKER.py` with this initial contract:

```python
#!/usr/bin/env python3
from provenance_representation_audit import run_audit

r = run_audit()
assert r["version"] == "v14.04"
assert r["seed"] == 1404
assert r["support_dimension"] == 25
assert r["Pillar_3"] == "OPEN"
assert r["class_a"]["analytic_theorem"] == "SUPPORT_GAUGE_PROJECTIVE_CENTRALITY"
assert r["class_a"]["central_only"] is True
assert r["class_a"]["identity_pgrl_null"] is True
assert r["class_a"]["max_weyl_twirl_error"] < 2e-11
assert r["class_a"]["min_noncentral_orbit_projective_residual"] > 1e-4
assert r["class_b"]["nontrivial_carrier_count"] >= 1
assert r["class_b"]["certified_natural_support_link_count"] in {0, 1}
assert r["class_c"]["declared_intertwiner_count"] >= 2
assert r["class_c"]["min_pair_projective_residual"] > 1e-4
assert r["class_c"]["max_hidden_direction_separation"] > 1e-4
assert r["class_c"]["max_boundary_separation"] > 1e-6
assert r["class_c"]["max_dual_ray_separation"] > 1e-6
assert r["gate_outcome"] in {
    "DERIVED_PROVENANCE_SOURCE_RAY",
    "CENTRAL_ONLY_PGRL_NULL",
    "REQUIRES_NEW_REPRESENTATION_LINK",
    "UNRESOLVED_REPRESENTATION_AUDIT",
}
print("V14_04_PROVENANCE_REPRESENTATION_CHECKER_PASS")
```

- [ ] **Step 2: Add deterministic CI**

Create `.github/workflows/uqcf-v1404-provenance-representation.yml` with:

```yaml
name: UQCF v14.04 Provenance Representation Audit

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - research/v14.04-provenance-representation
    paths:
      - 'ResearchHistory/UQCF-GEM/v14/v14.04/**'
      - 'ResearchHistory/UQCF-GEM/v14/v14.03/source_ray_audit.py'
      - 'ResearchHistory/UQCF-GEM/v14/v14.02/dual_normal_audit.py'
      - 'Tmp/TOE/Einstein 6/v1172_full_stack_package/**'
      - 'ResearchHistory/UQCF-GEM/v13/v13.26/**'
      - 'ResearchHistory/UQCF-GEM/README.md'
      - 'ResearchHistory/UQCF-GEM/STATUS.md'
      - 'docs/superpowers/specs/2026-09-13-v1404-provenance-representation-design.md'
      - 'docs/superpowers/plans/2026-09-13-v1404-provenance-representation.md'
      - '.github/workflows/uqcf-v1404-provenance-representation.yml'

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    env:
      OPENBLAS_NUM_THREADS: '1'
      OMP_NUM_THREADS: '1'
      MKL_NUM_THREADS: '1'
      PYTHONHASHSEED: '0'
    defaults:
      run:
        working-directory: ResearchHistory/UQCF-GEM/v14/v14.04
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install scientific dependencies
        run: python -m pip install numpy==2.4.6 scipy==1.17.1
      - name: Run v14.04 checker
        run: python CHECKER.py
```

- [ ] **Step 3: Push and verify RED**

Expected checker failure:

```text
ModuleNotFoundError: No module named 'provenance_representation_audit'
```

Any other failure is not the intended RED gate and must be diagnosed before implementation.

- [ ] **Step 4: Commit**

Commit message:

```text
test: add v14.04 provenance representation red gate
```

---

### Task 2: Loader, Hermitian/projective utilities, and exact Weyl-twirl control

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py`

**Interfaces:**
- Consumes: `source_ray_audit.py` from v14.03.
- Produces: `load_v1403()`, `herm()`, `projective_fit_residual()`, `heisenberg_weyl_twirl()`, and `centrality_controls()`.

- [ ] **Step 1: Implement the module loader**

Use repository-relative loading analogous to v14.03:

```python
def load_v1403():
    repo_root = Path(__file__).resolve().parents[4]
    path = repo_root / "ResearchHistory" / "UQCF-GEM" / "v14" / "v14.03" / "source_ray_audit.py"
    spec = importlib.util.spec_from_file_location("uqcf_v1403_source_ray", path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
```

- [ ] **Step 2: Implement projective equivalence residual**

For Hermitian `P,Q`, fit real `a,b` in `Q ~= a P + b I` by least squares on stacked real/imaginary entries, then reject nonpositive `a`:

```python
def projective_fit_residual(P, Q):
    P = herm(P); Q = herm(Q)
    I = np.eye(P.shape[0], dtype=complex)
    def vec(A):
        return np.concatenate([A.real.ravel(), A.imag.ravel()])
    A = np.column_stack([vec(P), vec(I)])
    x, *_ = np.linalg.lstsq(A, vec(Q), rcond=None)
    a, b = map(float, x)
    fit = a * P + b * I
    rel = np.linalg.norm(Q - fit) / max(1.0, np.linalg.norm(Q), np.linalg.norm(fit))
    if a <= 0:
        rel = max(rel, 1.0)
    return {"a": a, "b": b, "residual": float(rel)}
```

- [ ] **Step 3: Implement the exact 25-dimensional Weyl twirl**

Use `X|j> = |j+1 mod d>` and `Z|j> = omega^j|j>` for `d=25`, then average all `625` conjugations. Do not sample a subset.

- [ ] **Step 4: Implement centrality regression controls**

Use at least two deterministic noncentral Hermitian matrices:

```python
P1 = np.diag(np.linspace(-1.0, 1.0, 25))
P2 = herm(np.diag(np.arange(25, dtype=float)) + 0.37 * (np.eye(25, k=1) + np.eye(25, k=-1)))
```

For each:
- verify the full Weyl twirl equals `Tr(P)/25 I` within `2e-11`;
- apply at least one fixed 2-plane Hadamard mixing unitary and one discrete Fourier unitary;
- verify at least one conjugated orbit representative has projective-fit residual `>1e-4`.

Also verify `lambda I` remains exactly invariant under those unitary controls.

- [ ] **Step 5: Commit**

Commit message:

```text
feat: add v14.04 support-gauge centrality controls
```

---

### Task 3: PGRL-null consequence and Class-A theorem package

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py`

**Interfaces:**
- Consumes: `load_v1403()`, v14.03 `build_configuration()` and `pgrl_tangent()`.
- Produces: `class_a_audit(v1403) -> dict[str, Any]`.

- [ ] **Step 1: Build one frozen compatibility configuration**

Use:

```python
v1402 = v1403.load_v1402()
cfg = v1403.build_configuration(v1402, "V_A")
```

- [ ] **Step 2: Verify central sources are PGRL-null**

For `lambda in (-3.5, -1.0, 0.2, 2.0, 11.0)` compute:

```python
P = lambda_ * np.eye(25, dtype=complex)
dotX = v1403.pgrl_tangent(cfg["X0"], P)
```

Record maximum Frobenius norm and require `<2e-11`.

- [ ] **Step 3: Encode the analytic theorem separately from the regression controls**

Return fields:

```python
{
  "analytic_theorem": "SUPPORT_GAUGE_PROJECTIVE_CENTRALITY",
  "theorem_statement": "If provenance has trivial U(25) support action and [UPU^dagger]_+=[P]_+ for all U, then P is central modulo the v14.03 projective equivalence; central representatives are PGRL-null.",
  "central_only": True,
  "identity_pgrl_null": True,
  "max_identity_tangent_norm": ...,
  "max_weyl_twirl_error": ...,
  "min_noncentral_orbit_projective_residual": ...,
}
```

Do not label the numerical twirl as proof; it is a deterministic regression control for the exact representation-theoretic theorem.

- [ ] **Step 4: Commit**

Commit message:

```text
feat: certify v14.04 class-a pgrl-null consequence
```

---

### Task 4: Frozen provenance carrier inventory

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py`

**Interfaces:**
- Produces: `class_b_audit() -> dict[str, Any]` with machine-readable inventory.

- [ ] **Step 1: Inventory only frozen, traceable candidates**

Record at minimum:

```python
CANDIDATES = [
  {
    "name": "genesis_ledger_identity",
    "path": "Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py",
    "domain_type": "hash/root/event/witness ledger",
    "transformation_law": "source-origin/ordered-lineage identity; no certified U(25) support action",
    "support_map_status": "NONE_CERTIFIED",
  },
  {
    "name": "genesis_6d_field",
    "path": "Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py",
    "domain_type": "real 6D field on RES^6 grid",
    "transformation_law": "model-specific grid/roll/pruning transforms",
    "support_map_status": "NONE_CERTIFIED",
  },
  {
    "name": "retained_source_grade",
    "path": "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
    "domain_type": "retained scalar/extensive source grade",
    "transformation_law": "positive retained-source scaling",
    "support_map_status": "NONE_CERTIFIED",
  },
  {
    "name": "retained_source_current",
    "path": "ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md",
    "domain_type": "graph source/current package with BJ=s",
    "transformation_law": "graph balance/covariance inside retained convention",
    "support_map_status": "NONE_CERTIFIED",
  },
]
```

- [ ] **Step 2: Verify each source file exists and hash it**

Use SHA-256 of file bytes/text to bind the type inventory to concrete archived artifacts. If a required source path is absent, return `UNRESOLVED_REPRESENTATION_AUDIT` rather than silently dropping it.

- [ ] **Step 3: Search the inventoried file text for an explicit certified support link**

The audit may recognize only explicit identifiers tied to the v14.03 carrier, such as `Herm(25)`, `support coefficient`, `source_ray_audit`, or a documented `J: K_prov -> H_supp`. A generic geometry projection or visualization mapping does not count.

Record:

```python
"nontrivial_carrier_count": <integer >= 1>,
"certified_natural_support_link_count": 0 or 1,
"candidates": [...]
```

A zero count is an archive fact for this frozen audit, not a theorem that no future link can exist.

- [ ] **Step 4: Commit**

Commit message:

```text
feat: inventory frozen v14.04 provenance carriers
```

---

### Task 5: Declared-intertwiner positive and ambiguity control

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py`

**Interfaces:**
- Consumes: v14.03 `source_contact()` on frozen `V_A` configuration.
- Produces: `class_c_audit(v1403) -> dict[str, Any]`.

- [ ] **Step 1: Build a small declared provenance-carrier fixture**

Use `k=3` and a noncentral Hermitian operator:

```python
Pprov = np.array([
    [1.0, 0.25+0.1j, 0.0],
    [0.25-0.1j, -0.6, 0.15],
    [0.0, 0.15, -0.4],
], dtype=complex)
Pprov = herm(Pprov)
```

This fixture is not claimed to be Genesis physics.

- [ ] **Step 2: Construct at least three deterministic supplied isometries**

Use seeded complex Gaussian `25x3` matrices with QR for seeds `14041, 14042, 14043`; normalize column phases deterministically. Verify `||J^dagger J-I||<2e-12`.

- [ ] **Step 3: Produce support source operators**

For each supplied `J`:

```python
Pj = herm(J @ Pprov @ J.conj().T)
Pj -= np.real(np.trace(cfg["X0"] @ Pj)) * np.eye(25)
```

The subtraction is only a v14.03 identity-shift gauge choice; comparisons still use the projective-fit residual.

- [ ] **Step 4: Establish genuine projective ambiguity**

For every pair `(Pi,Pj)`, compute `projective_fit_residual`. Require at least one pair `>1e-4` and report the minimum pair residual across all nonidentical pairs.

- [ ] **Step 5: Propagate all supplied intertwiners through v14.03**

Use:

```python
contact = v1403.source_contact(v1402, cfg, Pj, certify_base_formula=True)
```

Each valid control must have:
- `hidden.classification == "NONZERO_HIDDEN_COMPONENT"`;
- simple first-contact boundary;
- `normal.classification == "RAY"`;
- non-null oriented `dual_rep`.

If a seeded `J` accidentally yields zero hidden component, do not tune it against the target. Instead classify the fixture as numerically unsuitable and use the next predeclared seeds `14044,14045,14046`, stopping after six total candidates. Record all attempted seeds.

- [ ] **Step 6: Quantify downstream ambiguity**

For pairs of successful controls record:

```python
hidden_sep = ||u_i-u_j|| / max(1,||u_i||,||u_j||)
boundary_sep = ||X*_i-X*_j|| / max(1,||X*_i||,||X*_j||)
dual_sep = max(0, 1-ReTr(G_i^dagger G_j))
```

The checker requires nonzero separations; the exact thresholds remain conservative (`>1e-4` hidden, `>1e-6` boundary/dual).

- [ ] **Step 7: Commit**

Commit message:

```text
feat: add v14.04 declared-intertwiner ambiguity control
```

---

### Task 6: Combined adjudication and first GREEN scientific run

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py`

**Interfaces:**
- Produces: `run_audit() -> dict[str, Any]` consumed by `CHECKER.py`.

- [ ] **Step 1: Implement combined gate logic exactly**

```python
if class_b["certified_natural_support_link_count"] > 0:
    gate = "DERIVED_PROVENANCE_SOURCE_RAY"
elif class_b["nontrivial_carrier_count"] == 0:
    gate = "CENTRAL_ONLY_PGRL_NULL"
elif class_c["genuine_projective_ambiguity"]:
    gate = "REQUIRES_NEW_REPRESENTATION_LINK"
else:
    gate = "UNRESOLVED_REPRESENTATION_AUDIT"
```

Return top-level fields:

```python
{
  "version": "v14.04",
  "seed": 1404,
  "support_dimension": 25,
  "Pillar_3": "OPEN",
  "scientific_breakthrough": False,
  "class_a": ...,
  "class_b": ...,
  "class_c": ...,
  "gate_outcome": gate,
}
```

- [ ] **Step 2: Run CI without changing the checker thresholds**

Expected first GREEN possibilities are only the spec-approved outcomes. If CI fails numerically, debug the implementation; do not change scientific tolerances until the root cause is established.

- [ ] **Step 3: Commit**

Commit message:

```text
feat: adjudicate v14.04 provenance representation gate
```

---

### Task 7: Freeze summary/report and bind checker

**Files:**
- Create: `ResearchHistory/UQCF-GEM/v14/v14.04/SUMMARY.json`
- Create: `ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md`
- Modify: `ResearchHistory/UQCF-GEM/v14/v14.04/CHECKER.py`

**Interfaces:**
- Consumes: exact successful `run_audit()` telemetry from CI.
- Produces: immutable scientific archive checked against live recomputation.

- [ ] **Step 1: Freeze `SUMMARY.json` from successful telemetry**

Include discrete outcome fields, source artifact hashes, theorem classification, Weyl-twirl error, PGRL-null error, intertwiners attempted/successful, projective/downstream separations, and claim boundaries.

- [ ] **Step 2: Write `REPORT.md` in four explicit layers**

Sections must distinguish:
1. **Theorem:** support-gauge projective centrality and PGRL-null consequence.
2. **Reproducible computation:** exact Weyl 1-design control, archive type inventory, declared-intertwiner ambiguity control.
3. **Interpretation:** what representation structure is missing.
4. **Unresolved physical claims:** no derived gravity, spacetime, stress-energy, or absolute coupling.

- [ ] **Step 3: Bind the checker to the summary**

Read `SUMMARY.json`, assert all discrete scientific fields exactly, assert source hashes exactly, and compare floating telemetry using a tolerance no tighter than:

```python
tol = 1e-12 + 1e-9 * max(1.0, abs(actual), abs(frozen))
```

Keep the independent scientific thresholds from the RED checker as separate assertions.

- [ ] **Step 4: Re-run exact-SHA CI**

Expected: PASS with summary-bound checker.

- [ ] **Step 5: Commit**

Commit messages may be split as:

```text
docs: freeze v14.04 provenance representation result
test: bind v14.04 checker to frozen summary
```

---

### Task 8: Canonical status/index and release certification

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/README.md`
- Modify: `ResearchHistory/UQCF-GEM/STATUS.md`

**Interfaces:**
- Consumes: frozen v14.04 result.
- Produces: canonical project frontier.

- [ ] **Step 1: Update README**

Add v14.04 under v14 history. Preserve v14.01, v14.02, v14.03, v13.26, and v13.28 conclusions explicitly.

- [ ] **Step 2: Update STATUS**

If the expected `REQUIRES_NEW_REPRESENTATION_LINK` outcome is confirmed, frontier text must become:

```text
Genesis/provenance
    -> nontrivial provenance carriers exist
    -> gauge-trivial provenance alone is central/PGRL-null
    -> no frozen natural provenance-to-support intertwiner found
    -> supplied [P] -> hidden contact -> dual ray remains certified conditionally
```

Do not describe a supplied intertwiner as derived.

- [ ] **Step 3: Certify exact final branch head**

No edits after the exact branch SHA goes green.

- [ ] **Step 4: Compare against main**

Require:
- `behind_by == 0`;
- only v14.04 gate/workflow/spec/plan plus README/STATUS changed;
- no temporary debugging scripts.

- [ ] **Step 5: Fast-forward main and require post-merge checks**

After merge, require v14.04 success on the exact merged SHA and inspect v14.03/v14.02/v14.01/v13.28 regression workflows triggered by README/STATUS changes.

- [ ] **Step 6: Final verification**

Fetch `main` and confirm it still points at the exact certified merged SHA before declaring v14.04 complete.

---

## Self-Review Results

- **Spec coverage:** All three audit classes, the projective centrality theorem, exact Weyl 1-design control, PGRL-null consequence, richer-carrier inventory, supplied-intertwiner ambiguity control, outcome hierarchy, claim boundaries, and stop rule are mapped to tasks.
- **Placeholder scan:** No `TBD`, `TODO`, implicit implementation gaps, or unnamed tests remain.
- **Type consistency:** `run_audit()`, `class_a`, `class_b`, `class_c`, `projective_fit_residual`, and v14.03 `source_contact` usage are consistent across tasks.
- **Critical claim boundary:** A successful supplied-`J` control can only demonstrate sufficiency and ambiguity; it cannot upgrade provenance to a derived support-space source representation.
