# v15.29 Pre-Time Provenance Faithfulness / Source Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether frozen UQCF-GEM provenance certifies nontrivial source distinctions inside a fixed coarse source fiber `q=B1 s`, and if so whether those distinctions define a natural, representation-ready pre-time source carrier without using gravity behavior.

**Architecture:** Build a fail-closed evidence registry first, then construct exact q-fibers from the already-certified v15.28 torus complex. Provenance equivalence is adjudicated only from hash-pinned typed relations; absence of a cross-domain relation produces an explicit non-entailment result rather than an inferred carrier. Synthetic controls prove the machinery can recognize collapsed, enhanced, and representation-ready extensions, while the real UQCF branch is allowed to stop before any coupling solve.

**Tech Stack:** Python 3.13.5, standard library `dataclasses`/`fractions`/`hashlib`/`json`, NumPy 2.3.5 only for inherited frozen torus arrays and presentation, v15.28 exact rational helpers, `unittest`, Matplotlib 3.10.8/FFmpeg for optional presentation, GitHub Actions for exact-head certification.

**Spec:** `docs/superpowers/specs/2026-09-14-v1529-provenance-faithfulness-source-extension-design.md`

## Global Constraints

- Base scientific head is exactly `42244310b065f473c8bd459a6f065a61afbd2292` (certified v15.28).
- All scientific implementation is additive under `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/`; do not modify v15.28 or earlier research files.
- Do not merge `main`; exact current `main` is independently checked only as a delivery boundary.
- Treat `q=B1 s` as the existing coarse source control, not as proof that `s` is physical.
- Do not infer provenance distinctness from `s1 != s2`; a distinction must be supported by a frozen typed provenance relation.
- Do not identify Genesis Pin, source-role labels, retained source grade, microscopic incidence, quantum source operators, or cycle-response coordinates by shared terminology.
- No downstream holonomy, distance/falloff, Newton/GR, cosmology, metric/Hodge/minimum-action, entropy, pruning, RCR, or physical-time quantity may appear in carrier selection or representation-readiness logic.
- No PCA/SVD alignment, random isometry, arbitrary node/site map, dimension/cardinality matching, or chosen section `Q -> S_prov` may be used.
- A typed/covariant provenance extension is not automatically representation-ready. The exact v15.28 coupling solver may be reopened only in a later gate if v15.29 certifies a finite linear representation or a canonical frozen-theory linearization.
- `signal_of_life`, `gravity_canary_certified`, and `physical_gravity_derived` remain `false` for every v15.29 outcome.
- No new source-semantics axiom is adopted in v15.29. If one is required, stop with `PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM`.
- Use TDD for every new scientific interface; preserve tests-first commits before implementation commits.
- Exact algebraic decisions use integer/Fraction arithmetic where available. Floating tolerances are permitted only when validating inherited floating arrays, never to invent provenance relations.

## Frozen Evidence Pins

The evidence inventory task must verify these exact Git blobs before any scientific adjudication:

```text
v15.28 report
  ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/README.md
  1ea6c653dd45b2c01da1bb5a09f629bd2d12e67d

v15.28 concise ledger
  ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json
  6d1ed9766d89c2f66d072978a8fa4b60bedccb39

v15.28 exact source head
  42244310b065f473c8bd459a6f065a61afbd2292

v15.27 target-origin implementation
  ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/target_origin.py
  1c33232050567bf3b2bf77b19570ec2b8a1fb5e0

v15.26 selector-rank implementation
  ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/selector_rank.py
  623defd0d8284e5d9cba6d8f8679de698e5202bc

v15.25 pre-time canary implementation
  ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py
  99110f943550751645539c0c8a7339024d7fefd3

v15.09 carrier-origin report
  ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md
  ec73ef9240dcef062c95a82c511a874d0d2923ef

v15.08 source-semantics report
  ResearchHistory/UQCF-GEM/v15/v15.08/REPORT.md
  23bbeaecdb81adfe1a39b3140569d23c367b8b55

v15.07 report (hash already frozen by v15.09)
  ResearchHistory/UQCF-GEM/v15/v15.07/REPORT.md
  c3abb3af5b5c7210fc717392d4e2cc6fc4648284

v15.03 graph-site/source-lift report
  ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md
  6c3aed73c63c9c7554107d163e15b8fae7549c1c

v15.02 shared-label-equivariance report
  ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md
  be1281621b0e2872e555223b2c1cdb98fe9d8011

v15.01 common-parent report
  ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md
  1afbb7aebe384a1fb761f99fd2b040e595be1fa5

v14.04 provenance representation report
  ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md
  e5d9566bfc86c801d2933e63453d1800f60a675b

v13.26 source-calibration/origin report
  ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md
  9917085b211ca0e1f4737082227f55097cc72b66

V997 Genesis Pin bridge report
  Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md
  8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e

V923 source-role closure report
  Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/FULL_REPORT_AND_PROOF.md
  9a1523c08d2b9b2c5ba2d298dfed3d563a750bec
```

The inventory may add further exact pins only when a cited frozen artifact is needed to support a typed relation. Adding a file is evidence collection, not permission to broaden its semantics.

---

### Task 1: Freeze the Provenance Evidence Inventory and Type Boundary

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_inventory.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_inventory.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/PROVENANCE_EVIDENCE.json`

**Interfaces:**
- Produces `EvidenceRecord`.
- Produces `frozen_inventory(repo_root: Path) -> tuple[EvidenceRecord, ...]`.
- Produces `by_key(key: str) -> EvidenceRecord`.
- Produces `inventory_digest(records) -> str`.
- No fiber or source-extension conclusion is allowed in this module.

- [ ] **Step 1: Write RED tests for exact evidence pins and typed relations**

```python
import unittest
import provenance_inventory as inv


class InventoryTests(unittest.TestCase):
    def test_required_blobs_are_exact(self):
        rows = inv.frozen_inventory(inv.REPO_ROOT)
        self.assertEqual(inv.by_key('v15.28-ledger', rows).blob,
                         '6d1ed9766d89c2f66d072978a8fa4b60bedccb39')
        self.assertEqual(inv.by_key('v15.08-source-semantics', rows).blob,
                         '23bbeaecdb81adfe1a39b3140569d23c367b8b55')
        self.assertEqual(inv.by_key('v997-genesis-pin', rows).blob,
                         '8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e')
        self.assertEqual(inv.by_key('v923-source-role', rows).blob,
                         '9a1523c08d2b9b2c5ba2d298dfed3d563a750bec')

    def test_genesis_pin_is_not_microscopic_incidence_relation(self):
        r = inv.by_key('v997-genesis-pin')
        self.assertEqual(r.domain, 'HISTORY_PROVENANCE')
        self.assertNotIn('TORUS_EDGE_REPRESENTATIVE', r.codomains)

    def test_source_role_is_discrete_legitimacy_not_edge_label(self):
        r = inv.by_key('v923-source-role')
        self.assertEqual(r.relation_class, 'CERTIFIED_PROVENANCE_RELATION')
        self.assertEqual(r.value_type, 'TERNARY_SOURCE_ROLE')
        self.assertFalse(r.certifies_q_fiber_relation)
```

- [ ] **Step 2: Run RED**

Run from the v15.29 demo directory:

```bash
python -m unittest -v test_inventory.py
```

Expected: import failure because `provenance_inventory.py` does not exist.

- [ ] **Step 3: Implement immutable evidence records and Git-blob verification**

```python
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json

REPO_ROOT = Path(__file__).resolve().parents[4]

@dataclass(frozen=True)
class EvidenceRecord:
    key: str
    path: str
    blob: str
    domain: str
    codomains: tuple[str, ...]
    relation_class: str
    value_type: str
    certifies_q_fiber_relation: bool
    certifies_action: bool
    claim_boundary: str


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def verify_record(root: Path, record: EvidenceRecord) -> None:
    raw = (root / record.path).read_bytes()
    actual = git_blob_sha(raw)
    if actual != record.blob:
        raise ValueError(f'frozen evidence changed: {record.key}: {actual}')
```

Populate records only from the exact pins in this plan. The V997 record is typed as history/registry/root/witness legitimacy. The V923 record is typed as ternary source-role legitimacy. v14.04 is typed as provenance representation evidence with conditional supplied intertwiners and no certified torus-edge/cycle target link. v15.08/v15.09 carry explicit irreducibility/type-boundary claims.

- [ ] **Step 4: Add deterministic inventory serialization**

```python
def inventory_digest(records):
    payload = [r.__dict__ for r in records]
    text = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(text.encode()).hexdigest()
```

Write `docs/PROVENANCE_EVIDENCE.json` with sorted keys, no timestamps, and exact blob IDs.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_inventory.py
python provenance_inventory.py --out docs/PROVENANCE_EVIDENCE.json
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_inventory.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/PROVENANCE_EVIDENCE.json
git commit -m "test: freeze v15.29 provenance evidence and type boundary"
```

---

### Task 2: Build the Exact q-Fiber Model Without Promoting Representatives to Sources

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/fiber_model.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_fiber_model.py`

**Interfaces:**
- Hash-pins the v15.28 `exact_linear.py` and `representation_actions.py` source at the v15.28 certified head before importing them by file path.
- Produces `FiberRepresentative`.
- Produces `root_fixture() -> FiberRepresentative`.
- Produces `face_shift(rep, face_index, coefficient) -> FiberRepresentative`.
- Produces `cycle_shift(rep, cycle_vector) -> FiberRepresentative`.
- Produces `same_coarse_source(a, b) -> bool` using exact integer arithmetic.
- Does not contain provenance semantics.

- [ ] **Step 1: Write RED exact-fiber tests**

```python
import unittest
import fiber_model as fm


class FiberModelTests(unittest.TestCase):
    def test_face_boundary_shift_preserves_q_exactly(self):
        rep = fm.root_fixture()
        shifted = fm.face_shift(rep, face_index=0, coefficient=3)
        self.assertTrue(fm.same_coarse_source(rep, shifted))
        self.assertNotEqual(rep.edge_vector, shifted.edge_vector)

    def test_general_cycle_shift_preserves_q_exactly(self):
        rep = fm.root_fixture()
        z = fm.canonical_cycle_basis()[7]
        shifted = fm.cycle_shift(rep, z)
        self.assertTrue(fm.same_coarse_source(rep, shifted))

    def test_noncycle_shift_changes_q(self):
        rep = fm.root_fixture()
        bad = list(rep.edge_vector)
        bad[3] += 1
        other = fm.FiberRepresentative(tuple(bad), fm.apply_B1(tuple(bad)))
        self.assertFalse(fm.same_coarse_source(rep, other))
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest -v test_fiber_model.py
```

Expected: module absent.

- [ ] **Step 3: Implement exact source representatives and inherited complex verification**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FiberRepresentative:
    edge_vector: tuple[int, ...]
    q: tuple[int, ...]


def apply_B1(edge_vector):
    c = load_frozen_complex()
    return tuple(int(sum(int(c.B1[v,e]) * edge_vector[e]
                         for e in range(c.B1.shape[1])))
                 for v in range(c.B1.shape[0]))


def same_coarse_source(a, b):
    return a.q == b.q
```

`root_fixture()` must use the same `(face=(0,0), edge_slot='bottom', amplitude=1)` incidence defect as v15.25, but only to produce integer `s` and `q`. Do not import or call any v15.25 response/holonomy function.

- [ ] **Step 4: Expose canonical exact cycle controls**

Use the exact v15.28 cycle basis derived from `ker(B1)`. `face_shift` uses integer `B2[:,f]`; `cycle_shift` verifies `B1 z = 0` exactly before constructing the shifted representative.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_fiber_model.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/fiber_model.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_fiber_model.py
git commit -m "feat: add exact q-fiber source representative model"
```

---

### Task 3: Implement Provenance Relation Adjudication and Fail-Closed Unspecified Status

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_equivalence.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_equivalence.py`

**Interfaces:**
- Consumes `EvidenceRecord` and `FiberRepresentative`.
- Produces `RelationResult`.
- Produces `classify_pair(a, b, evidence) -> RelationResult`.
- Produces exact synthetic controls separately from UQCF evidence.

- [ ] **Step 1: Write RED classification tests**

```python
class EquivalenceTests(unittest.TestCase):
    def test_raw_edge_difference_is_not_provenance_evidence(self):
        a = fm.root_fixture()
        b = fm.face_shift(a, 0, 1)
        r = pe.classify_pair(a, b, inv.frozen_inventory(inv.REPO_ROOT))
        self.assertEqual(r.status, 'PROVENANCE_RELATION_UNSPECIFIED')
        self.assertFalse(r.physical_distinction_certified)

    def test_synthetic_collapsed_control_is_identical(self):
        a, b, evidence = pe.synthetic_collapsed_control()
        r = pe.classify_pair(a, b, evidence)
        self.assertEqual(r.status, 'PROVENANCE_IDENTICAL')

    def test_synthetic_distinct_control_is_certified(self):
        a, b, evidence = pe.synthetic_distinct_control()
        r = pe.classify_pair(a, b, evidence)
        self.assertEqual(r.status, 'PROVENANCE_DISTINCT_CERTIFIED')
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement typed relation results**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RelationResult:
    status: str
    physical_distinction_certified: bool
    supporting_keys: tuple[str, ...]
    reason: str


def classify_pair(a, b, evidence):
    if a.q != b.q:
        raise ValueError('pair is not in one q-fiber')
    links = [r for r in evidence if r.certifies_q_fiber_relation]
    if not links:
        return RelationResult(
            'PROVENANCE_RELATION_UNSPECIFIED', False, (),
            'NO_FROZEN_TYPED_RELATION_FROM_TORUS_REPRESENTATIVE_TO_PROVENANCE')
    return classify_from_certified_links(a, b, links)
```

Do not fall back to edge-vector equality, file-path equality, dimension matches, string matching, or source-role labels.

- [ ] **Step 4: Implement synthetic controls with explicit `SYNTHETIC_CONTROL` evidence class**

The positive synthetic record must declare a fiber tag and its exact equivalence relation. The collapsed record must declare its provenance value as a deterministic function of `q`. Synthetic evidence cannot be returned by `frozen_inventory()`.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_equivalence.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_equivalence.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_equivalence.py
git commit -m "feat: add fail-closed provenance fiber relation adjudication"
```

---

### Task 4: Add Explicit Countermodels for Non-Entailment

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/countermodels.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_countermodels.py`

**Interfaces:**
- Produces `FrozenReduct` and `ProvenanceExpansion`.
- Produces `fiber_countermodels() -> tuple[ProvenanceExpansion, ProvenanceExpansion]`.
- Produces `same_frozen_reduct(a, b) -> bool`.
- Produces `relation_disagrees(a, b) -> bool`.

- [ ] **Step 1: Write RED non-entailment tests**

```python
class CountermodelTests(unittest.TestCase):
    def test_same_reduct_allows_collapsed_and_distinguishing_expansions(self):
        collapsed, distinguishing = cm.fiber_countermodels()
        self.assertTrue(cm.same_frozen_reduct(collapsed, distinguishing))
        self.assertTrue(cm.relation_disagrees(collapsed, distinguishing))

    def test_countermodels_keep_same_q_and_source_role(self):
        collapsed, distinguishing = cm.fiber_countermodels()
        self.assertEqual(collapsed.reduct.q, distinguishing.reduct.q)
        self.assertEqual(collapsed.reduct.source_role,
                         distinguishing.reduct.source_role)
        self.assertEqual(collapsed.reduct.genesis_status,
                         distinguishing.reduct.genesis_status)
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement reduct versus expansion explicitly**

```python
@dataclass(frozen=True)
class FrozenReduct:
    q: tuple[int, ...]
    source_role: str
    genesis_status: str
    retained_source_grade: str

@dataclass(frozen=True)
class ProvenanceExpansion:
    reduct: FrozenReduct
    representative_labels: tuple[tuple[int, ...], ...]
    provenance_classes: tuple[str, ...]
```

Construct both expansions over the same two q-equivalent representatives. The collapsed expansion assigns one provenance class to both; the distinguishing expansion assigns two. The frozen reduct contains only fields actually certified independently of the torus representative.

- [ ] **Step 4: Make the theorem fail closed**

`same_frozen_reduct=True` plus differing fiber equivalence means frozen evidence does not entail one relation. Record the theorem status `PROVENANCE_EXTENSION_NOT_ENTAILED`. Do not claim the distinguishing expansion is physically valid; its role is logical independence.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_countermodels.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/countermodels.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_countermodels.py
git commit -m "feat: add provenance fiber non-entailment countermodels"
```

---

### Task 5: Audit Covariance, Gauge Survival, and Natural Action Readiness

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/action_audit.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_action_audit.py`

**Interfaces:**
- Consumes relation results plus exact v15.28 torus automorphisms.
- Produces `ActionAudit`.
- Produces `audit_real_provenance_action(...) -> ActionAudit`.
- Produces `audit_synthetic_extension_action(...) -> ActionAudit`.
- Does not manufacture a map between provenance and torus cells.

- [ ] **Step 1: Write RED naturality tests**

```python
class ActionAuditTests(unittest.TestCase):
    def test_real_archive_has_no_certified_torus_provenance_action(self):
        r = aa.audit_real_provenance_action(inv.frozen_inventory(inv.REPO_ROOT))
        self.assertFalse(r.action_certified)
        self.assertEqual(r.status,
                         'PROVENANCE_DISTINCTION_EXISTS_BUT_ACTION_NOT_CERTIFIED'
                         if r.distinction_certified else
                         'NO_CERTIFIED_PROVENANCE_ACTION_ON_Q_FIBER')

    def test_synthetic_extension_has_exact_group_action(self):
        r = aa.audit_synthetic_extension_action()
        self.assertTrue(r.action_certified)
        self.assertTrue(r.group_law_exact)
        self.assertTrue(r.projection_equivariant)
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement action audit without cross-domain inference**

```python
@dataclass(frozen=True)
class ActionAudit:
    status: str
    distinction_certified: bool
    action_certified: bool
    group_law_exact: bool
    projection_equivariant: bool
    representation_ready: bool
    reason: str
```

For real frozen evidence, search only records explicitly marked `CERTIFIED_ACTION` whose domain is the candidate provenance carrier and whose label relation reaches the torus source representation. V997 history-registry invariance does not count as an action on torus edge representatives. V923 role labels do not count as an action on the 392-element torus group.

- [ ] **Step 4: Implement representation-readiness rule**

A candidate is representation-ready only if it has:

```text
1. nontrivial certified q-fiber distinction,
2. exact projection to Q,
3. certified natural action,
4. finite linear representation matrices OR a canonical frozen-theory linearization,
5. exact equivariance of the projection,
6. no arbitrary embedding or selector.
```

The synthetic positive control supplies these by construction. The real branch must not infer them.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_action_audit.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/action_audit.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_action_audit.py
git commit -m "feat: audit provenance covariance and representation readiness"
```

---

### Task 6: Implement the Source-Extension Gate and Mechanical Outcome Logic

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_gate.py`

**Interfaces:**
- Produces `ExtensionAudit`.
- Produces `audit_real_archive() -> ExtensionAudit`.
- Produces `audit_synthetic_controls() -> tuple[ExtensionAudit, ...]`.
- Produces `adjudicate(...) -> str`.
- Never calls the v15.28 coupling solver.

- [ ] **Step 1: Write RED primary-outcome tests**

```python
class GateTests(unittest.TestCase):
    def test_real_archive_fails_closed_without_fiber_entailment(self):
        r = gate.audit_real_archive()
        self.assertIn(r.status, {
            'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE',
            'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED',
            'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION',
            'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED',
            'PROVENANCE_SOURCE_REPRESENTATION_READY',
            'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
        })
        self.assertFalse(r.gravity_observables_evaluated)

    def test_current_frozen_evidence_prefers_non_entailment_if_countermodels_survive(self):
        r = gate.audit_real_archive()
        if r.countermodels_survive:
            self.assertEqual(r.status,
                             'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')

    def test_representation_ready_is_stronger_than_carrier_certified(self):
        carrier, ready = gate.synthetic_carrier_vs_ready_controls()
        self.assertEqual(carrier.status,
                         'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED')
        self.assertFalse(carrier.representation_ready)
        self.assertEqual(ready.status,
                         'PROVENANCE_SOURCE_REPRESENTATION_READY')
        self.assertTrue(ready.representation_ready)
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement typed gate result**

```python
@dataclass(frozen=True)
class ExtensionAudit:
    status: str
    fiber_relation_status: str
    countermodels_survive: bool
    nontrivial_kernel_certified: bool
    projection_to_q_certified: bool
    natural_action_certified: bool
    representation_ready: bool
    requires_new_source_semantics_axiom: bool
    gravity_observables_evaluated: bool = False
    stop_reason: str | None = None
```

- [ ] **Step 4: Implement mechanical precedence rules**

```python
def adjudicate(fiber_relation, countermodels_survive, action, source_semantics_required):
    if source_semantics_required:
        return 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM'
    if countermodels_survive or fiber_relation == 'PROVENANCE_RELATION_UNSPECIFIED':
        return 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED'
    if fiber_relation == 'PROVENANCE_IDENTICAL':
        return 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE'
    if fiber_relation == 'PROVENANCE_DISTINCT_CERTIFIED' and not action.action_certified:
        return 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION'
    if action.action_certified and not action.representation_ready:
        return 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED'
    if action.representation_ready:
        return 'PROVENANCE_SOURCE_REPRESENTATION_READY'
    raise AssertionError('unreachable provenance gate state')
```

The countermodel/non-entailment precedence is intentional: a computationally convenient distinguishing assignment cannot outrank a frozen-theory independence result.

- [ ] **Step 5: Assert that raw microscopic incidence is never auto-promoted**

```python
def test_raw_representative_control_never_certifies_real_carrier(self):
    r = gate.audit_raw_representative_control()
    self.assertEqual(r.status,
                     'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM')
    self.assertFalse(r.nontrivial_kernel_certified)
```

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest -v test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_gate.py
git commit -m "feat: add preregistered v15.29 source-extension gate"
```

---

### Task 7: Add the Exact Ledger and Claim-Boundary Assertions

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py`
- Extend: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_gate.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/RESULTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/README.md`

**Interfaces:**
- Produces `audit() -> dict`.
- Ledger is deterministic, sorted, and contains no timestamps or gravity scores.

- [ ] **Step 1: Write RED schema and claim-boundary tests**

```python
REQUIRED = {
    'version','status','base_sha','inventory_hash','fiber_fixture_count',
    'fiber_relation_counts','countermodels_survive','extension_kernel_status',
    'projection_to_q_certified','natural_action_certified','representation_ready',
    'coupling_solver_reopened','new_source_semantics_axiom_added',
    'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
    'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time',
    'scientific_breakthrough','signal_of_life','gravity_canary_certified',
    'physical_gravity_derived','Pillar_3','next_required_object'
}


def test_ledger_schema_and_boundaries(self):
    r = gate.audit()
    self.assertEqual(set(r), REQUIRED)
    for key in ('gravity_observables_evaluated','uses_holonomy_selector',
                'uses_newton_or_gr','uses_metric_selector','uses_pruning',
                'uses_entropy','uses_physical_time','signal_of_life',
                'gravity_canary_certified','physical_gravity_derived'):
        self.assertFalse(r[key])
    self.assertEqual(r['Pillar_3'], 'OPEN')
```

- [ ] **Step 2: Implement exact breakthrough rule**

Only `PROVENANCE_SOURCE_REPRESENTATION_READY` may set `scientific_breakthrough=True`, and that flag means only an upstream typed-representation breakthrough. It must not set any gravity signal flag.

```python
scientific_breakthrough = (status == 'PROVENANCE_SOURCE_REPRESENTATION_READY')
```

- [ ] **Step 3: Implement deterministic next-step rule**

```python
NEXT = {
 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE': 'NEW_SOURCE_SEMANTICS_OR_INDEPENDENT_CARRIER_PRIMITIVE',
 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED': 'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION',
 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION': 'CERTIFIED_PROVENANCE_RELABELING_ACTION',
 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED': 'CANONICAL_LINEARIZATION_OR_FINITE_REPRESENTATION',
 'PROVENANCE_SOURCE_REPRESENTATION_READY': 'SEPARATE_COUPLING_SPACE_GATE_FOR_S_PROV',
 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM': 'EXPLICIT_AXIOM_APPROVAL_REQUIRED',
}
```

- [ ] **Step 4: Write deterministic outputs and README**

`source_extension_gate.py --out outputs` writes `outputs/verification.json`. Copy a concise committed adjudication to `docs/RESULTS.json`; README explains theorem/computation/interpretation and explicitly states that no coupling member or gravity observable was evaluated.

- [ ] **Step 5: Run GREEN and commit**

```bash
python source_extension_gate.py --out outputs
python -m unittest -v test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/RESULTS.json \
        ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/README.md
git commit -m "feat: freeze v15.29 provenance-extension adjudication"
```

---

### Task 8: Build the Gravity-Blind Offline Inspector and Replay

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/viewer.html`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/requirements.txt`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/.gitignore`

**Interfaces:**
- `payload()` consumes only `source_extension_gate.audit()` plus exact fiber examples.
- `write_html()` embeds data; no external requests.
- `movie()` shows provenance/fiber statuses only.

- [ ] **Step 1: Write RED replay tests**

```python
class ReplayTests(unittest.TestCase):
    def test_payload_has_fibers_and_provenance_not_gravity_scores(self):
        p = replay.payload()
        self.assertIn('fibers', p)
        self.assertIn('audit', p)
        text = json.dumps(p).lower()
        for forbidden in ('holonomy_score','newton_score','einstein_score','inverse_square_score'):
            self.assertNotIn(forbidden, text)

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('Microscopic difference is not automatically physical source difference', text)
            self.assertIn('Playback is not physical time', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)
```

- [ ] **Step 2: Run RED**

Expected: replay/viewer absent.

- [ ] **Step 3: Implement six-scene gravity-blind narrative**

Use these scenes exactly:

```text
1 coarse q quotient
2 multiple microscopic representatives in one q-fiber
3 frozen provenance relation status
4 gauge/relabeling/action boundary
5 countermodel / extension adjudication
6 final status and next required object
```

No spatial field map, remote-loop visualization, distance axis, coupling dimension selector, or preferred microscopic representative is shown.

- [ ] **Step 4: Run GREEN, generate and decode media**

```bash
python -m unittest -v test_replay.py
python replay.py --out outputs --video
ffmpeg -v error -i outputs/provenance_faithfulness.mp4 -f null -
ffprobe -v error -show_entries stream=codec_name,width,height -show_entries format=duration -of json outputs/provenance_faithfulness.mp4
```

Require H.264, 1280x720, 24 seconds ±0.1 s.

- [ ] **Step 5: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: add gravity-blind v15.29 provenance replay"
```

---

### Task 9: Add Exact-Head CI, Inherited Regression, and Digest-Verified Release

**Files:**
- Create: `.github/workflows/uqcf-v1529-provenance-faithfulness.yml`
- Update PR #25 only with evidence after exact-head success; no post-certification scientific file edits.

**Interfaces:**
- Base comparison: exact certified v15.28 head `42244310b065f473c8bd459a6f065a61afbd2292`.
- Runs all 552 selected v15.11–v15.28 tests plus every v15.29 test.
- Publishes eight release assets only after exact size/SHA-256 verification.

- [ ] **Step 1: Create additive-scope workflow and inherited regression list**

Start from `.github/workflows/uqcf-v1528-coupling-space.yml`. Keep the inherited v15.11–v15.27 suites unchanged, add the v15.28 six-test-file group exactly as certified, then add:

```python
new_files = [
  'test_inventory.py','test_fiber_model.py','test_equivalence.py',
  'test_countermodels.py','test_action_audit.py','test_gate.py','test_replay.py'
]
```

Require inherited selected count `552` before adding v15.29 tests.

- [ ] **Step 2: Add exact scientific assertions after regeneration**

```python
r = json.load(open('outputs/verification.json'))
assert r['status'] in {
 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE',
 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED',
 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION',
 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED',
 'PROVENANCE_SOURCE_REPRESENTATION_READY',
 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
}
assert r['signal_of_life'] is False
assert r['gravity_canary_certified'] is False
assert r['physical_gravity_derived'] is False
assert not any(r[k] for k in (
 'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
 'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time'))
```

- [ ] **Step 3: Package exact source, data, logs, design and plan**

Release assets:

```text
provenance_faithfulness.mp4
provenance_faithfulness.html
verification.json
replay_data.json
REPORT.md
PROVENANCE.json
UQCF_GEM_v15_29_bundle.zip
SHA256SUMS.txt
```

The ZIP includes the complete v15.29 source folder, fresh CI logs, this plan, and the approved design spec. Verify every ZIP member digest before upload.

- [ ] **Step 4: Publish only after remote asset digest checks**

Use a unique prerelease tag:

```text
uqcf-gem-v15.29-${GITHUB_RUN_ID}-a${GITHUB_RUN_ATTEMPT}
```

Create as draft, verify all eight remote assets have expected size and `sha256:` digest, then publish. Upload a publication receipt artifact.

- [ ] **Step 5: Inspect exact-head jobs and record PR receipt**

Required evidence before claiming completion:

```text
verify job conclusion = success
publish job conclusion = success
all inherited + v15.29 tests = pass
movie decode = clean
release draft = false
8 release assets = uploaded and digest matched
PR #25 = open/draft/unmerged
main unchanged
```

Add a PR #25 comment containing exact source SHA, run ID, test counts, release URL, verdict, claim boundary, and the fact that no coupling solver or gravity canary was run.

- [ ] **Step 6: Post-publication offline-browser verification**

Download the published HTML/MP4 bytes from the verified delivery artifact or release. In system Chromium/Playwright exercise every q-fiber example/status selector at widths 1280, 820, and 390; require zero JavaScript errors, zero external requests, and no horizontal overflow. Fully decode the downloaded MP4 again. Record browser/video evidence as a PR comment; native iPad/Safari remains untested unless explicitly exercised.

---

## Final Stop Rule

Do not proceed to a coupling or gravity gate merely because v15.29 finds a nontrivial microscopic fiber. Continue only according to the exact v15.29 status:

```text
PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE
  -> source quotient remains q; do not choose among v15.28's three control couplings.

PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED
  -> seek an independently motivated provenance-fiber relation or explicit new axiom; no coupling solve.

PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION
  -> derive/certify the provenance relabeling action; no coupling solve.

PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED
  -> derive a canonical linearization/finite representation in a separate gate; no coupling solve yet.

PROVENANCE_SOURCE_REPRESENTATION_READY
  -> open a NEW coupling-space gate for S_prov; freeze its form before any gravity observable.

PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM
  -> stop for explicit user approval of any new axiom.
```

No v15.29 outcome itself certifies a pre-time gravity signal.
