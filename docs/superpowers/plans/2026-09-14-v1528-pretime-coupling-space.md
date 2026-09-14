# v15.28 Pre-Time Constitutive Coupling Space Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a gravity-blind exact classifier for the complete pre-time source→higher-incidence coupling space permitted by already-certified representation structure, and freeze any one-dimensional coupling form before any gravity observable is exposed.

**Architecture:** The implementation separates frozen representation inventory, exact signed-permutation/cell actions, an exact intertwiner solver, and gate adjudication. The large torus baseline is solved without metric choices by working in ambient vertex/edge coordinates with quotient/image constraints and exact symmetry orbits; an independent character calculation on exact source/cycle subrepresentations cross-checks the coupling-space dimension. Archived provenance carriers are admitted only when a certified source↔target representation relationship exists; otherwise the gate fails closed rather than inventing an embedding.

**Tech Stack:** Python 3.13; standard library `dataclasses`, `fractions.Fraction`, `hashlib`, `json`, `itertools`; NumPy 2.3.5 only for inherited numerical regression/conditioning diagnostics and presentation; Matplotlib/FFmpeg only for the optional replay; GitHub Actions for certification.

**Spec:** `docs/superpowers/specs/2026-09-14-v1528-pretime-coupling-space-design.md`

## Global Constraints

- Base scientific head is `700a4639010100a12b73882d530ac2c2bbf1f71e`; v15.28 changes are additive only.
- Do not merge `main`; `main` must remain unchanged unless separately approved.
- Do not use holonomy magnitude, inverse-square behavior, Newton/GR targets, lensing, cosmology, or any downstream gravity score anywhere in coupling selection or rank adjudication.
- Do not use a physical metric, Hodge norm, minimum action, smoothness, radiality, pruning, entropy, RCR, record probability, or physical time as a selector.
- Do not create arbitrary source↔target embeddings, random isometries, PCA/SVD alignments, or hand-selected label bijections.
- Exact coupling-space dimension is adjudicated with integer/rational arithmetic. Floating SVD may be logged only as a conditioning diagnostic.
- A candidate with no certified shared representation relationship receives `NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK` and is not force-fit.
- If an eligible coupling space is one-dimensional, freeze its basis-independent one-dimensional subspace before any gravity-like computation; v15.28 itself runs no gravity canary.
- A one-dimensional result fixes form only. Overall scale remains explicitly unresolved and nonphysical in this gate.
- Pre-time reversible change remains allowed; no pruning/time primitive is introduced.
- RAS/RCR and earlier stopped branches remain untouched.

---

## File Structure

Create one additive package:

`ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/`

- `representation_inventory.py` — immutable inventory of frozen carriers, blob hashes, certified actions/links, quotient data, and eligibility/status.
- `representation_actions.py` — exact torus automorphisms and signed-permutation actions on vertices, edges, and faces; exact source/cycle subrepresentation construction.
- `coupling_solver.py` — exact rational row-reduction, signed-pair orbit reduction, character cross-checks, and coupling-basis expansion.
- `coupling_gate.py` — preregistered candidate evaluation, status logic, one-dimensional freeze record, and claim-boundary ledger.
- `replay.py` — data-only replay showing coupling-space dimensions/statuses; must not import gravity/holonomy scoring.
- `viewer.html` — fully offline inspector for representation multiplicities and stop reasons.
- `test_inventory.py` — frozen artifact/hash/link tests.
- `test_actions.py` — exact group/action/chain-map tests.
- `test_solver.py` — synthetic d=0/d=1/d>1 controls, basis invariance, and exact solver tests.
- `test_gate.py` — q-only baseline, archived-candidate adjudication, freeze/stop rules, forbidden-selector flags.
- `test_replay.py` — offline/presentation/claim-boundary tests.
- `requirements.txt` — pin only NumPy/Matplotlib versions already used by the v15 series; no symbolic CAS dependency.
- `.gitignore` — `__pycache__/`, `*.pyc`, `outputs/`, `evidence/ci/`.
- `docs/RESULTS.json` — committed concise expected schema only after GREEN; authoritative fresh ledger is generated in CI.
- `docs/REPRESENTATION_INVENTORY.json` — hash-pinned inventory emitted from frozen artifacts.

Add one workflow:

- `.github/workflows/uqcf-v1528-coupling-space.yml`

The workflow reruns the inherited 517 selected checks plus all v15.28 tests, generates the exact ledger and optional presentation assets, verifies byte digests, and publishes a prerelease only after exact-head success.

---

### Task 1: Freeze the Representation Inventory Before Solving Anything

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_inventory.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_inventory.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/REPRESENTATION_INVENTORY.json`

**Interfaces:**
- Produces `CarrierRecord` and `frozen_inventory(repo_root: Path) -> tuple[CarrierRecord, ...]`.
- Produces `eligible_records(records) -> tuple[CarrierRecord, ...]`.
- Later tasks consume exact artifact paths, Git-blob hashes, carrier types, action/link status, quotient status, and composition status only from this module.

- [ ] **Step 1: Write failing inventory tests**

```python
from pathlib import Path
import representation_inventory as inv

class InventoryTests(unittest.TestCase):
    def test_v1527_and_v1404_hashes_are_frozen(self):
        rows = {r.key: r for r in inv.frozen_inventory(Path(inv.REPO_ROOT))}
        self.assertEqual(rows['v15.27-target-origin'].git_blob,
                         '1c33232050567bf3b2bf77b19570ec2b8a1fb5e0')
        self.assertEqual(rows['v14.04-provenance-report'].git_blob,
                         'e5d9566bfc86c801d2933e63453d1800f60a675b')

    def test_missing_representation_link_fails_closed(self):
        rows = {r.key: r for r in inv.frozen_inventory(Path(inv.REPO_ROOT))}
        self.assertEqual(rows['genesis-6d-field'].eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
        self.assertEqual(rows['retained-graph-source-current'].eligibility,
                         'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')

    def test_q_baseline_is_control_not_physical_derivation(self):
        q = next(r for r in inv.frozen_inventory(Path(inv.REPO_ROOT))
                 if r.key == 'source-quotient-q-control')
        self.assertTrue(q.eligible)
        self.assertEqual(q.role, 'BASELINE_CONTROL')
```

- [ ] **Step 2: Run RED**

Run:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
python -m unittest -v test_inventory.py
```

Expected: import/module failures because `representation_inventory.py` does not exist.

- [ ] **Step 3: Implement immutable inventory types and blob hashing**

```python
from dataclasses import dataclass
from pathlib import Path
import hashlib

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
```

Populate records only from frozen evidence. Required records at minimum:

```python
(
    'source-quotient-q-control',
    'v15.27-target-origin',
    'v15.26-response-selector-rank',
    'v14.04-provenance-report',
    'genesis-ledger',
    'genesis-6d-field',
    'retained-scalar-source-grade',
    'retained-graph-source-current',
    'v15.01-common-parent',
    'v15.02-shared-label',
    'v15.03-graph-site-source-lift',
)
```

The v14.04 report must preserve its archived conclusion that nontrivial provenance carriers exist but no certified natural link into the prior support carrier was earned. The v15.03 record must preserve the distinction between graph-site factorization and the certified compatibility parent rather than treating matching dimensions/labels as a bridge.

- [ ] **Step 4: Generate and compare a deterministic inventory JSON**

```python
def write_inventory(path: Path, records: tuple[CarrierRecord, ...]) -> None:
    payload = [r.__dict__ for r in records]
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
```

Test exact stable ordering by `key` and reject unknown/unhashed artifacts.

- [ ] **Step 5: Run GREEN**

Run `python -m unittest -v test_inventory.py`.

Expected: all inventory tests PASS.

- [ ] **Step 6: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/REPRESENTATION_INVENTORY.json
git commit -m "test: freeze v15.28 representation inventory and eligibility boundary"
```

---

### Task 2: Build Exact Torus Automorphisms and Chain Actions

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_actions.py`

**Interfaces:**
- Consumes frozen `torus_complex(7)` from `v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py` through an explicit hash-checked import helper.
- Produces `SignedPermutation`, `CellAutomorphism`, `torus_automorphisms(L)`, `vertex_action`, `edge_action`, `face_action`, `augmentation_basis`, `cycle_basis_exact`, and exact restricted representation matrices.

- [ ] **Step 1: Write RED tests for exact group size and chain covariance**

```python
class ActionTests(unittest.TestCase):
    def setUp(self):
        self.c = actions.load_frozen_complex(7)
        self.group = actions.torus_automorphisms(7)

    def test_full_translation_d4_group_has_392_elements(self):
        self.assertEqual(len(self.group), 7 * 7 * 8)
        self.assertEqual(len(set(self.group)), 392)

    def test_each_action_is_signed_permutation(self):
        for g in self.group:
            actions.vertex_action(self.c, g).validate()
            actions.edge_action(self.c, g).validate()
            actions.face_action(self.c, g).validate()

    def test_boundary_maps_are_exactly_equivariant(self):
        for g in self.group:
            p0 = actions.vertex_action(self.c, g).matrix_int()
            p1 = actions.edge_action(self.c, g).matrix_int()
            p2 = actions.face_action(self.c, g).matrix_int()
            np.testing.assert_array_equal(p0 @ self.c.B1.astype(int),
                                          self.c.B1.astype(int) @ p1)
            np.testing.assert_array_equal(p1 @ self.c.B2.astype(int),
                                          self.c.B2.astype(int) @ p2)
```

- [ ] **Step 2: Run RED**

Expected: module/function absence failures.

- [ ] **Step 3: Implement signed-permutation convention**

```python
@dataclass(frozen=True)
class SignedPermutation:
    image: tuple[int, ...]
    sign: tuple[int, ...]

    def validate(self) -> None:
        if sorted(self.image) != list(range(len(self.image))):
            raise ValueError('image is not a permutation')
        if any(s not in (-1, 1) for s in self.sign):
            raise ValueError('signs must be ±1')

    def apply_basis_index(self, i: int) -> tuple[int, int]:
        return self.image[i], self.sign[i]

    def compose(self, other: 'SignedPermutation') -> 'SignedPermutation':
        # self ∘ other
        image = tuple(self.image[other.image[i]] for i in range(len(self.image)))
        sign = tuple(other.sign[i] * self.sign[other.image[i]]
                     for i in range(len(self.image)))
        return SignedPermutation(image, sign)
```

- [ ] **Step 4: Implement the 392 exact combinatorial automorphisms**

Use the eight integer D4 matrices:

```python
D4 = (
    ((1,0),(0,1)), ((0,-1),(1,0)), ((-1,0),(0,-1)), ((0,1),(-1,0)),
    ((-1,0),(0,1)), ((1,0),(0,-1)), ((0,1),(1,0)), ((0,-1),(-1,0)),
)
```

For each matrix and translation `(tx, ty)`, map vertices modulo `L`. Map every canonical horizontal/vertical directed edge by its transformed endpoints; if the transformed direction is opposite to the canonical stored edge, use sign `-1`. Face orientation sign is the determinant of the D4 matrix.

- [ ] **Step 5: Implement exact augmentation and cycle bases**

Source augmentation basis for 49 vertices:

```python
def augmentation_basis(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((1 if r == c else -1 if r == n-1 else 0)
                       for r in range(n))
                 for c in range(n-1))
```

Implement fraction-free RREF/nullspace for integer `B1` and return a canonical basis with identified free columns. Verify for `L=7`:

```python
rank(B1) == 48
len(cycle_basis_exact(B1).vectors) == 50
```

- [ ] **Step 6: Build exact restricted source/cycle representations**

For each group element, apply ambient signed permutations to every basis vector and re-express exactly in the canonical augmentation/cycle basis using integer/Fraction coordinates. Assert representation composition on a preregistered generator subset and on ten deterministic full-group pairs.

- [ ] **Step 7: Run GREEN and commit**

```bash
python -m unittest -v test_actions.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_actions.py
git commit -m "feat: add exact torus automorphism and cycle representations"
```

---

### Task 3: Implement the Exact Coupling Solver with Synthetic d=0/d=1/d>1 Controls

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_solver.py`

**Interfaces:**
- Consumes `SignedPermutation` actions or exact representation matrices.
- Produces `CouplingSpace(dimension, basis, constraint_rank, orbit_count, metadata)`.
- Produces `solve_signed_ambient(...)`, `hom_dimension_from_characters(...)`, and `conjugate_exact_representation(...)`.

- [ ] **Step 1: Write the three preregistered solver controls**

```python
class SolverTests(unittest.TestCase):
    def test_d0_sign_mismatch(self):
        c2 = solver.synthetic_c2_sign_mismatch()
        self.assertEqual(solver.solve_exact(c2).dimension, 0)

    def test_d1_identical_irrep(self):
        pair = solver.synthetic_c2_identical_sign()
        self.assertEqual(solver.solve_exact(pair).dimension, 1)

    def test_dgt1_multiplicity(self):
        pair = solver.synthetic_trivial_multiplicity(source_dim=2, target_dim=1)
        self.assertEqual(solver.solve_exact(pair).dimension, 2)
```

- [ ] **Step 2: Write basis-change invariance tests before implementation**

Use exact unimodular changes:

```python
S_CHANGE = ((1,1),(0,1))
T_CHANGE = ((1,0),(1,1))
```

Conjugate every representation matrix by these exact changes and assert unchanged `d_eta`.

- [ ] **Step 3: Run RED**

Expected: solver module absent.

- [ ] **Step 4: Implement exact sparse RREF over `Fraction`**

Rows are dictionaries `dict[int, Fraction]`; eliminate pivot columns without converting to float.

```python
def exact_rref(rows: list[dict[int, Fraction]], ncols: int):
    rows = [dict(r) for r in rows if r]
    pivots = []
    r = 0
    for c in range(ncols):
        p = next((k for k in range(r, len(rows)) if rows[k].get(c)), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        scale = rows[r][c]
        rows[r] = {j: v/scale for j, v in rows[r].items()}
        for k in range(len(rows)):
            if k == r or not rows[k].get(c):
                continue
            f = rows[k][c]
            for j, v in rows[r].items():
                rows[k][j] = rows[k].get(j, Fraction(0)) - f*v
                if rows[k][j] == 0:
                    del rows[k][j]
        pivots.append(c)
        r += 1
        if r == len(rows):
            break
    return rows, tuple(pivots)
```

Implement exact nullspace basis from free columns.

- [ ] **Step 5: Implement signed-pair orbit reduction**

For a source basis index `j` and target basis index `i`, the equivariance relation is

```text
K[t_image(i), s_image(j)] = t_sign(i) * s_sign(j) * K[i,j].
```

Union pair indices under the full group while tracking relative sign. If an orbit returns to itself with sign `-1`, force that orbit variable to zero.

- [ ] **Step 6: Convert target/source constraints into orbit-variable equations**

`solve_signed_ambient(...)` receives:

```python
def solve_signed_ambient(
    source_actions: dict[str, SignedPermutation],
    target_actions: dict[str, SignedPermutation],
    source_null_vectors: tuple[tuple[int, ...], ...],
    target_constraint_rows: tuple[tuple[int, ...], ...],
) -> CouplingSpace:
    ...
```

For the q→cycle baseline later:

```text
source_null_vectors = (all-ones vertex vector,)
target_constraint_rows = rows of B1
```

so every returned ambient matrix `K:C0→C1` satisfies both `K·1=0` and `B1·K=0` exactly.

- [ ] **Step 7: Implement independent character formula**

On exact restricted representations:

```python
def hom_dimension_from_characters(source_rep, target_rep) -> int:
    total = sum(trace_exact(target_rep[g]) * trace_exact(source_rep[g])
                for g in source_rep)
    if total % len(source_rep):
        raise ArithmeticError('character inner product is not integral')
    return total // len(source_rep)
```

For real signed-permutation representations the characters are integers, so complex conjugation is trivial.

- [ ] **Step 8: Run GREEN and commit**

```bash
python -m unittest -v test_solver.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_solver.py
git commit -m "feat: add exact pre-time coupling-space solver"
```

---

### Task 4: Compute the Source-Quotient Baseline Without Gravity Exposure

**Files:**
- Modify: `coupling_solver.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py` (initial baseline tests)
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py`

**Interfaces:**
- Produces `q_baseline_audit() -> CandidateAudit`.
- `CandidateAudit` contains only exact representation/coupling facts: `dimension`, `basis_hashes`, `character_dimension`, `orbit_dimension`, constraint counts, and status. No holonomy/GR fields exist in this type.

- [ ] **Step 1: Write the baseline RED tests**

```python
class GateTests(unittest.TestCase):
    def test_q_baseline_orbit_and_character_dimensions_agree(self):
        r = gate.q_baseline_audit()
        self.assertEqual(r.dimension, r.character_dimension)
        self.assertEqual(r.dimension, r.orbit_dimension)

    def test_every_q_baseline_basis_map_is_exactly_cycle_valued(self):
        r = gate.q_baseline_audit()
        for k in r.ambient_basis:
            self.assertTrue(gate.exact_zero(gate.B1_times(k)))
            self.assertTrue(gate.exact_zero(gate.K_times_constant(k)))

    def test_q_baseline_contains_no_gravity_observable(self):
        r = gate.q_baseline_audit().as_dict()
        forbidden = {'holonomy','newton','einstein','inverse_square','distance_score'}
        self.assertTrue(forbidden.isdisjoint(r))
```

- [ ] **Step 2: Run RED**

Expected: `coupling_gate.py` absent.

- [ ] **Step 3: Implement q baseline construction**

Use the exact full 392-element vertex and edge action dictionaries. Solve ambient equivariant maps with:

```python
space = solve_signed_ambient(
    source_actions=vertex_actions,
    target_actions=edge_actions,
    source_null_vectors=(tuple([1] * len(c.vertices)),),
    target_constraint_rows=tuple(tuple(int(x) for x in row) for row in c.B1.astype(int)),
)
```

Independently construct exact 48-D augmentation and 50-D cycle representations and compute the character inner product. Require exact equality of dimensions.

- [ ] **Step 4: Add target-coordinate cross-check without using target coordinates as physics**

For every ambient coupling basis map `K`, apply it to a deterministic set of balanced source basis vectors, map resulting cycles through v15.26 `R`, then invert only as a verification layer and confirm the same cycle is recovered to the inherited numerical tolerance. Do not use `R` to reduce the coupling space.

- [ ] **Step 5: Freeze the q-control status mechanically**

```python
status = (
    'EQUIVARIANT_COUPLING_SPACE_ZERO' if dimension == 0 else
    'EQUIVARIANT_COUPLING_UNIQUE_UP_TO_SCALE' if dimension == 1 else
    'EQUIVARIANT_COUPLING_MULTI_DIMENSIONAL'
)
```

The q baseline remains `role='BASELINE_CONTROL'` regardless of dimension and cannot by itself trigger the gate-level breakthrough.

- [ ] **Step 6: Run tests and commit**

```bash
python -m unittest -v test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py
git commit -m "feat: classify q-only pre-time coupling baseline exactly"
```

---

### Task 5: Audit Provenance-Enhanced Candidates and Representation-Link Stops

**Files:**
- Modify: `representation_inventory.py`
- Modify: `coupling_gate.py`
- Extend: `test_inventory.py`
- Extend: `test_gate.py`

**Interfaces:**
- Produces `audit_candidate(record: CarrierRecord) -> CandidateAudit`.
- Produces `audit_all_candidates() -> tuple[CandidateAudit, ...]`.
- No candidate may enter `coupling_solver` unless `record.eligible` is true.

- [ ] **Step 1: Write fail-closed RED tests for archived carriers**

```python
def test_genesis_field_does_not_get_arbitrary_embedding(self):
    r = gate.audit_candidate(inv.by_key('genesis-6d-field'))
    self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')
    self.assertIsNone(r.dimension)

def test_retained_graph_source_current_stays_blocked_without_label_bridge(self):
    r = gate.audit_candidate(inv.by_key('retained-graph-source-current'))
    self.assertEqual(r.status, 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK')

def test_v1404_supplied_intertwiner_is_control_not_eligibility_upgrade(self):
    r = gate.audit_candidate(inv.by_key('v14.04-supplied-intertwiner-control'))
    self.assertEqual(r.status, 'CONDITIONAL_ON_SUPPLIED_INTERTWINER')
```

- [ ] **Step 2: Run RED**

Expected: missing candidate adjudicator/status failures.

- [ ] **Step 3: Implement eligibility gate before solver dispatch**

```python
def audit_candidate(record: CarrierRecord) -> CandidateAudit:
    if record.eligibility == 'NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK':
        return CandidateAudit.blocked(record.key, record.eligibility)
    if record.eligibility == 'CONDITIONAL_ON_SUPPLIED_INTERTWINER':
        return CandidateAudit.blocked(record.key, record.eligibility)
    return solve_eligible_record(record)
```

No branch of this function may synthesize a map when `label_link_status` is not certified.

- [ ] **Step 4: Implement the v14.04 ambiguity regression**

Read the frozen v14.04 report and verify the supplied-isometry control remains inequivalent across its three archived seeds. The test need only preserve the reported conclusion/hashes; do not rerun the old random-isometry construction as an allowed v15.28 candidate.

Required status:

```text
CONDITIONAL_ON_SUPPLIED_INTERTWINER
```

- [ ] **Step 5: Add any truly eligible archived carrier discovered by the inventory**

This step is conditional only on frozen evidence, not analyst preference. The code path is exact:

```python
if record.eligible:
    if not record.action_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified action')
    if not record.label_link_status.startswith('CERTIFIED'):
        raise AssertionError('eligible record lacks certified target link')
    return solve_eligible_record(record)
```

If the inventory finds no provenance-enhanced eligible carrier, that absence is itself the executed result; do not add a toy carrier to improve the outcome.

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest -v test_inventory.py test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
git commit -m "feat: enforce provenance representation-link gate before coupling solve"
```

---

### Task 6: Implement Gate-Level Adjudication and Freeze Any Unique Form Before Gravity

**Files:**
- Modify: `coupling_gate.py`
- Extend: `test_gate.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json`

**Interfaces:**
- Produces `audit() -> dict` with the frozen schema below.
- Produces `freeze_unique_form(candidate: CandidateAudit) -> FrozenCouplingForm` only for eligible physical candidates with `dimension == 1`.

- [ ] **Step 1: Write schema and claim-boundary tests**

Required ledger keys:

```python
REQUIRED = {
    'version', 'status', 'base_sha', 'inventory_hash',
    'q_control', 'candidates', 'eligible_candidate_count',
    'one_dimensional_candidate_count', 'multi_dimensional_candidate_count',
    'zero_dimensional_candidate_count', 'blocked_candidate_count',
    'unique_form_frozen', 'frozen_form', 'scale_resolved',
    'gravity_observables_evaluated', 'uses_holonomy_selector',
    'uses_newton_or_gr', 'uses_metric_selector', 'uses_pruning',
    'uses_entropy', 'uses_physical_time', 'signal_of_life',
    'gravity_canary_certified', 'Pillar_3', 'next_required_object'
}
```

Hard assertions:

```python
self.assertFalse(r['gravity_observables_evaluated'])
self.assertFalse(r['uses_holonomy_selector'])
self.assertFalse(r['uses_newton_or_gr'])
self.assertFalse(r['uses_metric_selector'])
self.assertFalse(r['uses_pruning'])
self.assertFalse(r['uses_entropy'])
self.assertFalse(r['uses_physical_time'])
self.assertFalse(r['gravity_canary_certified'])
```

- [ ] **Step 2: Implement exact preregistered verdict logic**

```python
def adjudicate(candidates: tuple[CandidateAudit, ...]) -> str:
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

If multiple inequivalent one-dimensional candidates survive, force `PRETIME_COUPLING_REMAINS_UNDERDETERMINED`.

- [ ] **Step 3: Freeze a unique form basis-independently if and only if allowed**

`FrozenCouplingForm` stores:

```python
@dataclass(frozen=True)
class FrozenCouplingForm:
    candidate_key: str
    projective_basis_hash: str
    ambient_shape: tuple[int, int]
    exact_nonzero_entries: tuple[tuple[int, int, int, int], ...]
    scale_status: str = 'UNRESOLVED_NONPHYSICAL_IN_V15_28'
```

Each exact entry is `(row, col, numerator, denominator)` after canonical projective normalization: multiply by the LCM of denominators, divide by the GCD of integer entries, and choose the first nonzero entry positive. This freezes the one-dimensional subspace without using a norm.

- [ ] **Step 4: Add breakthrough flag logic exactly as specified**

```python
breakthrough = (
    status == 'PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE'
    and frozen_form is not None
    and not gravity_observables_evaluated
)
```

Record `signal_of_life=False` and `gravity_canary_certified=False` even if `breakthrough=True`; this is an upstream constitutive-form breakthrough only.

- [ ] **Step 5: Write deterministic JSON and run GREEN**

```bash
python coupling_gate.py --out outputs
python -m unittest -v test_gate.py
```

Require `json.dumps(..., allow_nan=False, sort_keys=True)` and no timestamps inside the scientific ledger.

- [ ] **Step 6: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json
git commit -m "feat: add preregistered v15.28 coupling-space adjudication"
```

---

### Task 7: Build the Gravity-Blind Offline Inspector and Replay

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/viewer.html`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/test_replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/requirements.txt`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/.gitignore`

**Interfaces:**
- `payload() -> dict` consumes only `coupling_gate.audit()`.
- `write_html(payload, path)` embeds all data and makes no network requests.
- `movie(path, fps=10)` visualizes dimensions/status only; no physical field map or holonomy curve.

- [ ] **Step 1: Write RED presentation tests**

```python
class ReplayTests(unittest.TestCase):
    def test_payload_contains_candidate_dimensions_not_gravity_scores(self):
        p = replay.payload()
        self.assertIn('candidates', p)
        self.assertNotIn('holonomy', json.dumps(p).lower())
        self.assertNotIn('newton', json.dumps(p).lower())

    def test_html_is_offline_and_states_claim_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('No gravity observable was used to choose the coupling', text)
            self.assertIn('Scale unresolved', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_fps_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)
```

- [ ] **Step 2: Run RED**

Expected: replay module/viewer absent.

- [ ] **Step 3: Implement data-only presentation**

The HTML may show:

```text
carrier → eligibility → d_eta → verdict
```

and, if a one-dimensional form exists, a sparse matrix support diagram with entries normalized projectively. It must not show distance-from-source, radial curves, remote loops, Newton residuals, or GR comparisons.

- [ ] **Step 4: Implement optional 24-second MP4**

Use six four-second scenes:

```text
1. frozen representation inventory
2. exact symmetry constraints
3. synthetic d=0/d=1/d>1 controls
4. q baseline dimension
5. provenance candidate stop/solve statuses
6. final preregistered verdict and gravity boundary
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

### Task 8: Add Exact-Head CI, Full Regression, and Digest-Verified GitHub Release

**Files:**
- Create: `.github/workflows/uqcf-v1528-coupling-space.yml`
- Modify only documentation metadata on PR #24 after exact-head results; do not alter scientific files after certification.

**Interfaces:**
- Workflow verifies additive scope against base `700a4639010100a12b73882d530ac2c2bbf1f71e`.
- Workflow runs prior 517 selected checks plus the complete v15.28 suite in separate processes.
- Workflow publishes eight release assets only after SHA-256/size/state verification.

- [ ] **Step 1: Write workflow with RED→GREEN evidence preservation**

The test step must run all prior suites exactly as v15.27 did and then:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space
python -m unittest -v \
  test_inventory.py test_actions.py test_solver.py test_gate.py test_replay.py
```

Do not hard-code the final v15.28 test count until the tests-first commits are frozen; the workflow must parse and record the actual `Ran N tests` line from this exact command, then assert prior total `517` separately and record `517 + N` in `evidence/ci/SUMMARY.json`.

- [ ] **Step 2: Enforce additive scope**

```python
base = '700a4639010100a12b73882d530ac2c2bbf1f71e'
for line in subprocess.check_output(['git','diff','--name-status',base,'HEAD'], text=True).splitlines():
    status, name = line.split('\t', 1)
    assert status == 'A'
    assert (name.startswith('ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/')
            or name.startswith('docs/superpowers/')
            or name == '.github/workflows/uqcf-v1528-coupling-space.yml')
```

- [ ] **Step 3: Recompute scientific result from source, not committed docs**

```bash
python coupling_gate.py --out outputs > evidence/ci/model.log
python replay.py --out outputs --video > evidence/ci/render.log
```

CI must assert the exact status is one of the four preregistered gate verdicts and that all forbidden-selector flags are false.

- [ ] **Step 4: Package source and evidence**

Release assets:

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

The bundle must include the design spec, implementation plan, source, tests, exact inventory, scientific ledger, and fresh CI logs.

- [ ] **Step 5: Verify every release asset before publication**

Use the same GitHub CLI pattern already proven in v15.24–v15.27: create a unique draft prerelease, enumerate uploaded assets, require eight assets, compare remote `digest` and `size` to local bytes, then patch `draft=false`.

- [ ] **Step 6: Verify post-publication state and `main`**

Check:

```text
release draft == false
verify job == success
publish job == success
PR remains draft/unmerged
main == 8cf86768313eac837f904175b6d7b47e8e5460b0 unless user separately approved a main merge
```

If `main` has legitimately changed for unrelated user-approved work, report the observed SHA rather than forcing the historical one; never move `main` from this gate.

- [ ] **Step 7: Add final PR comment with exact-head evidence**

The comment must separate:

```text
THEOREM / EXACT COMPUTATION
INTERPRETATION
NOT CLAIMED
CI / RELEASE EVIDENCE
```

If `d_eta=1`, use the frozen breakthrough wording from the design spec. Otherwise explicitly state no breakthrough alert.

- [ ] **Step 8: Commit workflow before triggering final branch push**

```bash
git add .github/workflows/uqcf-v1528-coupling-space.yml
git commit -m "ci: certify and publish v15.28 coupling-space gate"
```

---

## Self-Review Checklist

Before execution, verify these mappings against the approved design:

- Spec §§3–5 frozen inputs/prohibited selectors/eligibility → Tasks 1 and 5.
- Spec §4 abstract target and basis independence → Tasks 2–4.
- Spec §6 symmetry/naturality/quotient/composition → Tasks 2, 3, and 5.
- Spec §7 exact solver/rank/basis invariance → Task 3.
- Spec §8 Gates A–E → Tasks 1–6.
- Spec §9 preregistered verdicts → Task 6.
- Spec §10 breakthrough rule → Task 6 and Task 8 final reporting.
- Spec §§11–12 isolation/fail-closed architecture → all tasks, especially 1, 5, and 8.
- Spec §13 tests/evidence → Tasks 1–8.
- Spec §14 no gravity conclusion → Task 6 schema, Task 7 presentation, Task 8 CI assertions.

No placeholder/TODO/TBD language is permitted in implementation. Any newly discovered missing representation link must stop that candidate rather than expanding scope mid-gate. Hidden complexity that requires a genuinely new carrier or physical axiom ends v15.28 and returns to design review instead of being patched into this plan.
