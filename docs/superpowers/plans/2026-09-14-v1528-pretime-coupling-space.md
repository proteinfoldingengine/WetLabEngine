# v15.28 Pre-Time Constitutive Coupling Space Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a gravity-blind exact classifier for the complete pre-time source→higher-incidence coupling space permitted by already-certified representation structure, and freeze any one-dimensional coupling form before any gravity observable is exposed.

**Architecture:** The implementation separates frozen representation inventory, exact rational linear algebra, exact combinatorial representations, the intertwiner solver, and scientific adjudication. The torus baseline is solved without metric choices by using ambient vertex/edge coordinates, exact source-quotient and cycle constraints, and signed-permutation symmetry orbits; an independent character calculation on exact source/cycle subrepresentations cross-checks the result. Archived provenance carriers are admitted only when a certified source↔target representation relationship already exists; otherwise the gate stops instead of inventing an embedding.

**Tech Stack:** Python 3.13; standard library `dataclasses`, `fractions.Fraction`, `hashlib`, `json`, `itertools`, `math`; NumPy 2.3.5 only for inherited numerical verification and presentation; Matplotlib 3.10.8/FFmpeg only for the optional replay; GitHub Actions for certification. No symbolic CAS dependency is added.

**Spec:** `docs/superpowers/specs/2026-09-14-v1528-pretime-coupling-space-design.md`

## Global Constraints

- Base scientific head is `700a4639010100a12b73882d530ac2c2bbf1f71e`; v15.28 changes are additive only.
- Do not merge or move `main`; any main-branch change requires separate user approval.
- Do not use holonomy magnitude, remote-loop behavior, inverse-square behavior, Newton/GR targets, lensing, cosmology, or any downstream gravity score in coupling selection or rank adjudication.
- Do not use a physical metric, Hodge norm, minimum action, smoothness, radiality, distance penalty, pruning, entropy, RCR, record probability, or physical time as a selector.
- Do not create arbitrary source↔target embeddings, random isometries, PCA/SVD alignments, or hand-selected label bijections.
- Exact coupling-space dimension is adjudicated with integer/rational arithmetic. Floating SVD may be logged only as a conditioning diagnostic and may not change a rank verdict.
- A carrier with no certified shared representation relationship receives `NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK` and never reaches the coupling solver.
- If an eligible physical candidate has a one-dimensional coupling space, freeze its basis-independent projective form before any gravity-like computation; v15.28 itself runs no gravity canary.
- A one-dimensional result fixes form only. Overall scale remains explicitly unresolved and nonphysical in v15.28.
- Pre-time reversible change remains allowed; no pruning/time primitive is introduced.
- RAS/RCR and earlier stopped branches remain untouched.

---

## File Structure

Create one additive package:

`ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/`

- `representation_inventory.py` — immutable frozen-carrier inventory and eligibility/status logic.
- `exact_linear.py` — exact `Fraction` matrix arithmetic, RREF/nullspace/inversion, no UQCF semantics.
- `representation_actions.py` — torus automorphisms, signed-permutation cell actions, exact augmentation/cycle representations.
- `coupling_solver.py` — exact intertwiner constraints, signed-pair orbit solver, character cross-checks, coupling basis expansion.
- `coupling_gate.py` — q baseline, archived-candidate audit, preregistered verdict, unique-form freeze, scientific ledger.
- `replay.py` / `viewer.html` — gravity-blind representation/coupling inspector.
- `test_inventory.py`, `test_exact_linear.py`, `test_actions.py`, `test_solver.py`, `test_gate.py`, `test_replay.py`.
- `requirements.txt`, `.gitignore`, `docs/REPRESENTATION_INVENTORY.json`, `docs/RESULTS.json`.

Add:

- `.github/workflows/uqcf-v1528-coupling-space.yml`

The workflow reruns the inherited 517 selected checks plus the complete v15.28 test suite, regenerates the exact ledger/presentation assets, and publishes only after exact-head success and release-asset digest checks.

---

### Task 1: Freeze the Representation Inventory Before Solving Anything

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_inventory.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_inventory.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/REPRESENTATION_INVENTORY.json`

**Interfaces:**
- Produces `CarrierRecord`.
- Produces `frozen_inventory(repo_root: Path) -> tuple[CarrierRecord, ...]`.
- Produces `by_key(key: str, records: tuple[CarrierRecord, ...] | None = None) -> CarrierRecord`.
- Produces `eligible_records(records) -> tuple[CarrierRecord, ...]`.

- [ ] **Step 1: Write failing inventory tests**

```python
import unittest
from pathlib import Path
import representation_inventory as inv

class InventoryTests(unittest.TestCase):
    def test_v1527_and_v1404_hashes_are_frozen(self):
        rows = {r.key: r for r in inv.frozen_inventory(Path(inv.REPO_ROOT))}
        self.assertEqual(rows['v15.27-target-origin'].git_blob,
                         '1c33232050567bf3b2bf77b19570ec2b8a1fb5e0')
        self.assertEqual(rows['v14.04-provenance-report'].git_blob,
                         'e5d9566bfc86c801d2933e63453d1800f60a675b')

    def test_missing_representation_links_fail_closed(self):
        self.assertEqual(inv.by_key('genesis-6d-field').eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertEqual(inv.by_key('retained-graph-source-current').eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')

    def test_q_baseline_is_control_not_physical_candidate(self):
        q = inv.by_key('source-quotient-q-control')
        self.assertTrue(q.eligible)
        self.assertEqual(q.role, 'BASELINE_CONTROL')
```

- [ ] **Step 2: Run RED**

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
python -m unittest -v test_inventory.py
```

Expected: import/module failure because `representation_inventory.py` does not exist.

- [ ] **Step 3: Implement immutable inventory types and exact Git-blob hashing**

```python
from dataclasses import dataclass
from pathlib import Path
import hashlib, json

REPO_ROOT = Path(__file__).resolve().parents[4]

@dataclass(frozen=True)
class CarrierRecord:
    key: str
    artifact_path: str
    git_blob: str
    carrier_type: str
    carrier_dimension: int | None
    action_status: str
    quotient_status: str
    composition_status: str
    label_link_status: str
    eligibility: str
    role: str

    @property
    def eligible(self) -> bool:
        return self.eligibility == 'ELIGIBLE_EXACT_COUPLING_AUDIT'


def git_blob_hash(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def by_key(key: str, records=None) -> CarrierRecord:
    rows = frozen_inventory(REPO_ROOT) if records is None else records
    hits = [r for r in rows if r.key == key]
    if len(hits) != 1:
        raise KeyError(key)
    return hits[0]
```

Required records:

```text
source-quotient-q-control
v15.27-target-origin
v15.26-response-selector-rank
v14.04-provenance-report
v14.04-supplied-intertwiner-control
genesis-ledger
genesis-6d-field
retained-scalar-source-grade
retained-graph-source-current
v15.01-common-parent
v15.02-shared-label
v15.03-graph-site-source-lift
```

Preserve archived status exactly. A nontrivial carrier is not eligible merely because it has the right dimension or because an arbitrary isometry can be supplied.

- [ ] **Step 4: Emit deterministic inventory JSON**

```python
def write_inventory(path: Path, records: tuple[CarrierRecord, ...]) -> None:
    payload = [r.__dict__ for r in sorted(records, key=lambda r: r.key)]
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
```

Tests must reject missing files, hash drift, duplicate keys, and eligibility with an uncertified action/link.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_inventory.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/REPRESENTATION_INVENTORY.json
git commit -m "test: freeze v15.28 representation inventory and eligibility boundary"
```

---

### Task 2: Build the Exact Rational Linear-Algebra Core

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_exact_linear.py`

**Interfaces:**
- Produces `MatrixQ = tuple[tuple[Fraction, ...], ...]`.
- Produces `rref`, `rank`, `nullspace`, `inverse`, `matmul`, `matvec`, `trace`, `conjugate`.
- No UQCF-specific imports are allowed.

- [ ] **Step 1: Write RED tests for exact rank/nullspace/inverse**

```python
import unittest
from fractions import Fraction
import exact_linear as ql

class ExactLinearTests(unittest.TestCase):
    def test_rank_and_nullspace_are_exact(self):
        a = ql.matrix(((1,2,3),(2,4,6)))
        self.assertEqual(ql.rank(a), 1)
        ns = ql.nullspace(a)
        self.assertEqual(len(ns), 2)
        for v in ns:
            self.assertEqual(ql.matvec(a, v), (Fraction(0), Fraction(0)))

    def test_unimodular_inverse_is_exact(self):
        u = ql.matrix(((1,1),(0,1)))
        self.assertEqual(ql.matmul(u, ql.inverse(u)), ql.identity(2))
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement exact matrices and sparse row reduction**

```python
from fractions import Fraction


def q(x):
    return x if isinstance(x, Fraction) else Fraction(x)


def matrix(rows):
    rows = tuple(tuple(q(x) for x in row) for row in rows)
    if rows and len({len(r) for r in rows}) != 1:
        raise ValueError('ragged matrix')
    return rows


def rref(rows, ncols=None):
    sparse = [dict((j, q(v)) for j, v in enumerate(row) if v)
              for row in rows]
    cols = ncols if ncols is not None else max((len(r) for r in rows), default=0)
    pivots, r = [], 0
    for c in range(cols):
        p = next((k for k in range(r, len(sparse)) if sparse[k].get(c)), None)
        if p is None:
            continue
        sparse[r], sparse[p] = sparse[p], sparse[r]
        scale = sparse[r][c]
        sparse[r] = {j: v/scale for j, v in sparse[r].items()}
        for k in range(len(sparse)):
            if k == r or not sparse[k].get(c):
                continue
            f = sparse[k][c]
            for j, v in sparse[r].items():
                sparse[k][j] = sparse[k].get(j, Fraction(0)) - f*v
                if sparse[k][j] == 0:
                    del sparse[k][j]
        pivots.append(c); r += 1
        if r == len(sparse):
            break
    return sparse, tuple(pivots)
```

Implement `nullspace` from free columns, `inverse` via augmented Gauss-Jordan, and exact matrix operations with shape checks.

- [ ] **Step 4: Add exact change-of-basis tests**

```python
def test_conjugation_preserves_trace(self):
    a = ql.matrix(((0,1),(1,0)))
    u = ql.matrix(((1,1),(0,1)))
    b = ql.conjugate(a, u)
    self.assertEqual(ql.trace(a), ql.trace(b))
```

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_exact_linear.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_exact_linear.py
git commit -m "feat: add exact rational linear algebra for v15.28"
```

---

### Task 3: Build Exact Torus Automorphisms and Source/Cycle Representations

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_actions.py`

**Interfaces:**
- Consumes `exact_linear`.
- Hash-pins `ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py` to Git blob `99110f943550751645539c0c8a7339024d7fefd3`.
- Produces `SignedPermutation`, `CellAutomorphism`, `SubspaceBasis`, `torus_automorphisms`, `vertex_action`, `edge_action`, `face_action`, `augmentation_basis`, `cycle_basis_exact`, `restricted_representation`.

- [ ] **Step 1: Write RED group/action tests**

```python
class ActionTests(unittest.TestCase):
    def setUp(self):
        self.c = actions.load_frozen_complex(7)
        self.group = actions.torus_automorphisms(7)

    def test_full_group_has_392_elements(self):
        self.assertEqual(len(self.group), 392)
        self.assertEqual(len(set(self.group)), 392)

    def test_boundary_maps_are_exact_chain_maps(self):
        b1 = self.c.B1.astype(int)
        b2 = self.c.B2.astype(int)
        for g in self.group:
            p0 = actions.vertex_action(self.c, g).matrix_int()
            p1 = actions.edge_action(self.c, g).matrix_int()
            p2 = actions.face_action(self.c, g).matrix_int()
            np.testing.assert_array_equal(p0 @ b1, b1 @ p1)
            np.testing.assert_array_equal(p1 @ b2, b2 @ p2)
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement signed-permutation convention**

```python
@dataclass(frozen=True)
class SignedPermutation:
    image: tuple[int, ...]
    sign: tuple[int, ...]

    def validate(self):
        if sorted(self.image) != list(range(len(self.image))):
            raise ValueError('not a permutation')
        if any(s not in (-1,1) for s in self.sign):
            raise ValueError('signs must be ±1')

    def matrix_int(self):
        m = np.zeros((len(self.image), len(self.image)), dtype=int)
        for i, (j, s) in enumerate(zip(self.image, self.sign)):
            m[j, i] = s
        return m
```

`CellAutomorphism` contains an integer D4 matrix and translation. Use the eight matrices

```python
D4 = (
 ((1,0),(0,1)), ((0,-1),(1,0)), ((-1,0),(0,-1)), ((0,1),(-1,0)),
 ((-1,0),(0,1)), ((1,0),(0,-1)), ((0,1),(1,0)), ((0,-1),(-1,0)),
)
```

with all 49 translations.

- [ ] **Step 4: Derive edge and face actions combinatorially**

Create a lookup mapping both orientations of every stored edge to `(index, ±1)`. Transform endpoints under the vertex automorphism and resolve the resulting oriented edge through this lookup.

Derive face action from boundaries rather than lower-left coordinates:

```python
transformed = p1 @ c.B2[:, f].astype(int)
```

find the unique face column equal to `transformed` or `-transformed`, and record the corresponding sign. This makes `P1 B2 = B2 P2` a construction invariant rather than an assumed reflection convention.

- [ ] **Step 5: Construct exact source and cycle bases**

```python
@dataclass(frozen=True)
class SubspaceBasis:
    columns: tuple[tuple[Fraction, ...], ...]
    coordinate_indices: tuple[int, ...]

    def coordinates(self, vector):
        coords = tuple(Fraction(vector[i]) for i in self.coordinate_indices)
        # reconstruct and compare exactly before returning
        if combine(self.columns, coords) != tuple(Fraction(x) for x in vector):
            raise ValueError('vector not in subspace')
        return coords
```

For source augmentation use columns `e_i-e_last` with coordinate indices `0..n-2`. For `ker(B1)`, use the canonical exact nullspace from Task 2 and its free-column indices. Assert exact dimensions 48 and 50 for `L=7`.

- [ ] **Step 6: Build restricted representations and verify group law**

For each automorphism, apply the ambient action to each basis column and re-expand exactly. Verify identity, inverse, four preregistered generators, and ten deterministic full-group products.

- [ ] **Step 7: Run GREEN and commit**

```bash
python -m unittest -v test_actions.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_actions.py
git commit -m "feat: add exact torus source and cycle representations"
```

---

### Task 4: Implement the Exact Intertwiner/Coupling Solver

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_solver.py`

**Interfaces:**
- Consumes `exact_linear` and `SignedPermutation`.
- Produces `CouplingSpace`.
- Produces `solve_exact_intertwiners`, `solve_signed_ambient`, `hom_dimension_from_characters`, `canonical_projective_matrix`.

- [ ] **Step 1: Write preregistered d=0/d=1/d>1 RED controls**

```python
class SolverTests(unittest.TestCase):
    def test_d0_sign_mismatch(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_c2_sign_mismatch()).dimension, 0)

    def test_d1_identical_sign_irrep(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_c2_identical_sign()).dimension, 1)

    def test_dgt1_multiplicity(self):
        self.assertEqual(solver.solve_exact_intertwiners(
            solver.synthetic_trivial_multiplicity(2,1)).dimension, 2)
```

- [ ] **Step 2: Write exact basis-change invariance RED tests**

Conjugate small source/target representations with

```python
S_CHANGE = ((1,1),(0,1))
T_CHANGE = ((1,0),(1,1))
```

and require unchanged dimension.

- [ ] **Step 3: Run RED**

Expected: solver absent.

- [ ] **Step 4: Implement generic exact intertwiner constraints for small representations**

For each group element impose

```text
K S_g - T_g K = 0
```

on `vec(K)`. Build exact `Fraction` rows and use `exact_linear.nullspace`. This path handles synthetic controls and low-dimensional eligible carriers.

- [ ] **Step 5: Implement signed-pair orbit reduction for the large ambient torus problem**

For source basis index `j` and target index `i`, equivariance implies

```text
K[t_image(i), s_image(j)] = t_sign(i) * s_sign(j) * K[i,j].
```

Union target/source index pairs over the full group while tracking relative sign. If an orbit closes with sign `-1`, force that orbit coefficient to zero.

Then impose exact structural rows on orbit variables:

```python
def solve_signed_ambient(source_actions, target_actions,
                         source_null_vectors, target_constraint_rows):
    ...
```

For q→cycle later, `source_null_vectors=(ones,)` and `target_constraint_rows=B1`, enforcing `K·1=0` and `B1·K=0` exactly.

- [ ] **Step 6: Implement independent character dimension**

```python
def hom_dimension_from_characters(source_rep, target_rep):
    keys = tuple(source_rep)
    if set(keys) != set(target_rep):
        raise ValueError('group keys differ')
    total = sum(ql.trace(target_rep[g]) * ql.trace(source_rep[g]) for g in keys)
    value = total / len(keys)
    if value.denominator != 1:
        raise ArithmeticError('nonintegral character inner product')
    return value.numerator
```

- [ ] **Step 7: Implement metric-free canonical projective normalization**

For a one-dimensional exact matrix, clear denominators by LCM, divide all integer entries by their GCD, and choose sign so the first nonzero row-major entry is positive. Hash the serialized integer matrix. Never normalize by an L2/Frobenius norm.

- [ ] **Step 8: Run GREEN and commit**

```bash
python -m unittest -v test_solver.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_solver.py
git commit -m "feat: add exact pre-time coupling-space solver"
```

---

### Task 5: Compute the q-Only Source Baseline Without Gravity Exposure

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py`

**Interfaces:**
- Defines `CandidateAudit`.
- Produces `q_baseline_audit() -> CandidateAudit`.
- No holonomy/Newton/GR field exists in `CandidateAudit`.

- [ ] **Step 1: Write q-baseline RED tests**

```python
class GateTests(unittest.TestCase):
    def test_q_baseline_orbit_and_character_dimensions_agree(self):
        r = gate.q_baseline_audit()
        self.assertEqual(r.dimension, r.orbit_dimension)
        self.assertEqual(r.dimension, r.character_dimension)

    def test_q_basis_maps_are_exactly_cycle_valued_and_quotient_safe(self):
        r = gate.q_baseline_audit()
        for k in r.ambient_basis:
            self.assertTrue(gate.matrix_is_zero(gate.left_multiply_B1(k)))
            self.assertTrue(gate.vector_is_zero(gate.apply_to_constant(k)))

    def test_q_baseline_schema_has_no_gravity_scores(self):
        text = json.dumps(gate.q_baseline_audit().as_dict()).lower()
        for forbidden in ('holonomy','newton','einstein','inverse_square','distance_score'):
            self.assertNotIn(forbidden, text)
```

- [ ] **Step 2: Run RED**

Expected: `coupling_gate.py` absent.

- [ ] **Step 3: Implement `CandidateAudit` and exact q baseline**

```python
@dataclass(frozen=True)
class CandidateAudit:
    key: str
    role: str
    eligibility: str
    status: str
    dimension: int | None
    orbit_dimension: int | None = None
    character_dimension: int | None = None
    ambient_basis: tuple = ()
    basis_hashes: tuple[str, ...] = ()
    stop_reason: str | None = None

    @property
    def eligible_physical_candidate(self):
        return self.role == 'PHYSICAL_CANDIDATE' and self.eligibility == 'ELIGIBLE_EXACT_COUPLING_AUDIT'
```

Solve the ambient map with all 392 exact vertex/edge actions, constant source null vector, and rows of `B1` as target constraints. Independently compute the 48-D augmentation→50-D cycle character inner product and require exact equality.

- [ ] **Step 4: Cross-check v15.26 response coordinates only as verification**

Hash-pin v15.27 baseline `selector_rank.py` at blob `623defd0d8284e5d9cba6d8f8679de698e5202bc`. For deterministic balanced source basis vectors, apply each coupling basis map, then pass the resulting cycle through inherited `R` and `reconstruct` and confirm recovery to inherited numerical tolerance. `R` never enters the exact coupling constraints.

- [ ] **Step 5: Assign baseline status mechanically**

```python
status = ('EQUIVARIANT_COUPLING_SPACE_ZERO' if dimension == 0 else
          'EQUIVARIANT_COUPLING_UNIQUE_UP_TO_SCALE' if dimension == 1 else
          'EQUIVARIANT_COUPLING_MULTI_DIMENSIONAL')
```

The q baseline always remains `role='BASELINE_CONTROL'`; it cannot trigger a physical breakthrough by itself.

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest -v test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py
git commit -m "feat: classify q-only pre-time coupling baseline exactly"
```

---

### Task 6: Audit Provenance-Enhanced Candidates and Representation-Link Stops

**Files:**
- Modify: `representation_inventory.py`
- Modify: `coupling_gate.py`
- Extend: `test_inventory.py`
- Extend: `test_gate.py`

**Interfaces:**
- Produces `audit_candidate(record: CarrierRecord) -> CandidateAudit`.
- Produces `audit_all_candidates() -> tuple[CandidateAudit, ...]`.

- [ ] **Step 1: Write fail-closed RED tests**

```python
def test_genesis_field_does_not_get_arbitrary_embedding(self):
    r = gate.audit_candidate(inv.by_key('genesis-6d-field'))
    self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
    self.assertIsNone(r.dimension)

def test_retained_graph_source_current_stays_blocked_without_label_bridge(self):
    r = gate.audit_candidate(inv.by_key('retained-graph-source-current'))
    self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')

def test_v1404_supplied_intertwiner_remains_conditional(self):
    r = gate.audit_candidate(inv.by_key('v14.04-supplied-intertwiner-control'))
    self.assertEqual(r.status, 'CONDITIONAL_ON_SUPPLIED_INTERTWINER')
```

- [ ] **Step 2: Run RED**

Expected: candidate adjudicator absent.

- [ ] **Step 3: Implement eligibility gate before solver dispatch**

```python
def audit_candidate(record):
    if record.eligibility in {
        'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK',
        'CONDITIONAL_ON_SUPPLIED_INTERTWINER',
    }:
        return CandidateAudit(record.key, record.role, record.eligibility,
                              record.eligibility, None,
                              stop_reason=record.label_link_status)
    if not record.action_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified action')
    if not record.label_link_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified target link')
    return solve_eligible_record(record)
```

- [ ] **Step 4: Preserve the v14.04 supplied-intertwiner ambiguity as a negative control**

Verify the frozen report still records three inequivalent supplied links and downstream projective/source-direction differences. Do not rerun or adopt those isometries as v15.28 physical candidates.

- [ ] **Step 5: Solve only genuinely eligible archived carriers**

If the inventory contains none beyond the q baseline, record that absence. Do not add a demonstration carrier. If an eligible carrier exists and its exact representation dimension is small, use `solve_exact_intertwiners`; if it is a signed-permutation ambient carrier, use `solve_signed_ambient`. Apply only composition constraints explicitly certified in its frozen record.

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest -v test_inventory.py test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
git commit -m "feat: enforce provenance representation-link gate before coupling solve"
```

---

### Task 7: Implement Preregistered Gate Adjudication and Unique-Form Freeze

**Files:**
- Modify: `coupling_gate.py`
- Extend: `test_gate.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json`

**Interfaces:**
- Produces `audit() -> dict`.
- Produces `FrozenCouplingForm` only for one-dimensional eligible physical candidates.

- [ ] **Step 1: Write ledger/claim-boundary tests**

Required keys:

```python
REQUIRED = {
 'version','status','base_sha','inventory_hash','q_control','candidates',
 'eligible_candidate_count','one_dimensional_candidate_count',
 'multi_dimensional_candidate_count','zero_dimensional_candidate_count',
 'blocked_candidate_count','unique_form_frozen','frozen_form','scale_resolved',
 'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
 'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
 'scientific_breakthrough','signal_of_life','gravity_canary_certified',
 'Pillar_3','next_required_object'
}
```

Hard assertions keep all gravity/pruning/time selectors false and keep `signal_of_life=False`, `gravity_canary_certified=False` even if an upstream constitutive-form breakthrough occurs.

- [ ] **Step 2: Implement exact preregistered verdict logic**

```python
def adjudicate(candidates):
    eligible = [c for c in candidates if c.eligible_physical_candidate]
    ones = [c for c in eligible if c.dimension == 1]
    if not eligible:
        return 'PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK'
    if not ones and all(c.dimension == 0 for c in eligible):
        return 'PRETIME_COUPLING_SPACE_ZERO'
    if len(ones) == 1:
        return 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE'
    return 'PRETIME_COUPLING_REMAINS_UNDERDETERMINED'
```

If two inequivalent one-dimensional physical candidates survive, force underdetermined.

- [ ] **Step 3: Freeze one-dimensional form without a metric**

```python
@dataclass(frozen=True)
class FrozenCouplingForm:
    candidate_key: str
    projective_basis_hash: str
    ambient_shape: tuple[int, int]
    exact_nonzero_entries: tuple[tuple[int,int,int,int], ...]
    scale_status: str = 'UNRESOLVED_NONPHYSICAL_IN_V15_28'
```

Serialize the canonical projective integer matrix from Task 4. No Frobenius/unit norm appears.

- [ ] **Step 4: Implement breakthrough rule exactly**

```python
scientific_breakthrough = (
    status == 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE'
    and frozen_form is not None
    and gravity_observables_evaluated is False
)
```

This flag means only the design-spec upstream theorem. It never sets `signal_of_life` or `gravity_canary_certified` true.

- [ ] **Step 5: Write deterministic ledger and run GREEN**

```bash
python coupling_gate.py --out outputs
python -m unittest -v test_gate.py
```

Use `allow_nan=False`, sorted JSON keys, and no scientific timestamps.

- [ ] **Step 6: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json
git commit -m "feat: add preregistered v15.28 coupling-space adjudication"
```

---

### Task 8: Build the Gravity-Blind Offline Inspector and Replay

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/viewer.html`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/requirements.txt`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/.gitignore`

**Interfaces:**
- `payload()` consumes only `coupling_gate.audit()`.
- `write_html()` embeds all data; no network calls.
- `movie()` visualizes dimensions/status only.

- [ ] **Step 1: Write RED presentation tests**

```python
class ReplayTests(unittest.TestCase):
    def test_payload_has_dimensions_not_gravity_scores(self):
        text = json.dumps(replay.payload()).lower()
        self.assertIn('candidates', text)
        self.assertNotIn('holonomy', text)
        self.assertNotIn('newton', text)

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'index.html'
            replay.write_html(replay.payload(), p)
            text = p.read_text()
            self.assertIn('No gravity observable was used to choose the coupling', text)
            self.assertIn('Scale unresolved', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_fps_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)
```

- [ ] **Step 2: Run RED**

Expected: replay/viewer absent.

- [ ] **Step 3: Implement offline presentation**

Show only:

```text
carrier → representation-link eligibility → d_eta → gate status
```

If a one-dimensional form exists, show sparse projective support, not a field/geometry plot.

- [ ] **Step 4: Implement optional 24-second MP4**

Six four-second scenes:

```text
1 inventory
2 exact automorphism constraints
3 synthetic d=0/d=1/d>1 controls
4 q baseline
5 provenance candidate stop/solve statuses
6 final verdict + gravity boundary
```

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_replay.py
python replay.py --out outputs --video
ffmpeg -v error -i outputs/coupling_space.mp4 -f null -
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
git commit -m "feat: add gravity-blind v15.28 coupling-space replay"
```

---

### Task 9: Add Exact-Head CI, Full Regression, and Digest-Verified Release

**Files:**
- Create: `.github/workflows/uqcf-v1528-coupling-space.yml`
- Update PR #24 only with evidence/comments after exact-head results; do not rewrite scientific files after certification.

**Interfaces:**
- CI compares additive scope to `700a4639010100a12b73882d530ac2c2bbf1f71e`.
- Runs inherited 517 selected checks plus all v15.28 tests.
- Publishes eight release assets only after size/SHA-256/uploaded-state verification.

- [ ] **Step 1: Add exact-head test workflow**

Run prior v15.11–v15.27 suites exactly as the successful v15.27 workflow did, separately from:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
python -m unittest -v \
  test_inventory.py test_exact_linear.py test_actions.py \
  test_solver.py test_gate.py test_replay.py
```

Parse the actual v15.28 `Ran N tests` line after tests-first commits are frozen; record `prior_selected_tests=517`, `v1528_tests=N`, and `selected_tests_passed=517+N` in `evidence/ci/SUMMARY.json`.

- [ ] **Step 2: Enforce additive-only diff**

```python
base='700a4639010100a12b73882d530ac2c2bbf1f71e'
for line in subprocess.check_output(['git','diff','--name-status',base,'HEAD'],text=True).splitlines():
    status,name=line.split('\t',1)
    assert status=='A'
    assert (name.startswith('ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/')
            or name.startswith('docs/superpowers/')
            or name=='.github/workflows/uqcf-v1528-coupling-space.yml')
```

- [ ] **Step 3: Recompute ledger and media from exact source**

```bash
python coupling_gate.py --out outputs > evidence/ci/model.log
python replay.py --out outputs --video > evidence/ci/render.log
ffmpeg -v error -i outputs/coupling_space.mp4 -f null - 2> evidence/ci/video_decode.log
```

Assert status is one of the four preregistered verdicts and every forbidden-selector flag is false.

- [ ] **Step 4: Package release evidence**

Eight assets:

```text
coupling_space.mp4
coupling_space.html
verification.json
replay_data.json
REPORT.md
PROVENANCE.json
UQCF_GEM_v15_28_bundle.zip
SHA256SUMS.txt
```

Bundle design spec, implementation plan, source, tests, exact inventory, ledger, and fresh CI logs.

- [ ] **Step 5: Verify release bytes before publishing**

Create a unique draft prerelease; require exactly eight remote assets; compare remote digest/size/state against local bytes; only then patch `draft=false`.

- [ ] **Step 6: Verify final repository state**

Require verify/publish jobs success, release non-draft, PR #24 draft/unmerged, and confirm observed `main` SHA without modifying it. If `main` differs due unrelated approved work, report the observation rather than forcing the historical SHA.

- [ ] **Step 7: Add final evidence comment to PR #24**

Use four headings:

```text
THEOREM / EXACT COMPUTATION
INTERPRETATION
NOT CLAIMED
CI / RELEASE EVIDENCE
```

If and only if an eligible physical candidate has `d_eta=1`, use the exact breakthrough wording from the design spec. Otherwise state explicitly that no breakthrough alert is issued.

- [ ] **Step 8: Commit workflow before final certification push**

```bash
git add .github/workflows/uqcf-v1528-coupling-space.yml
git commit -m "ci: certify and publish v15.28 coupling-space gate"
```

---

## Self-Review Checklist

- Spec §§3–5 frozen inputs/prohibited selectors/eligibility → Tasks 1 and 6.
- Spec §4 abstract cycle target/basis independence → Tasks 2–5.
- Spec §6 symmetry/naturality/quotient/composition → Tasks 3, 4, and 6.
- Spec §7 exact solver/rank/basis invariance → Tasks 2 and 4.
- Spec §8 Gates A–E → Tasks 1–7.
- Spec §9 verdicts → Task 7.
- Spec §10 breakthrough rule → Tasks 7 and 9.
- Spec §§11–12 isolation/fail-closed architecture → all tasks, especially 1, 6, and 9.
- Spec §13 tests/evidence → Tasks 1–9.
- Spec §14 no gravity conclusion → Tasks 7–9.

Self-review requirements before execution:

1. Search the plan/source for `TODO`, `TBD`, or undefined neighboring interfaces; none may remain.
2. Verify every later function/type used above is introduced in an earlier task or the same task.
3. Re-check the pinned v15.27 scientific blob `1c33232050567bf3b2bf77b19570ec2b8a1fb5e0`, v15.26 baseline blob `623defd0d8284e5d9cba6d8f8679de698e5202bc`, and v15.25 baseline blob `99110f943550751645539c0c8a7339024d7fefd3` before writing production code.
4. If hidden complexity requires a genuinely new carrier, physical axiom, or representation link, stop v15.28 and return to design review rather than patching it into implementation.
