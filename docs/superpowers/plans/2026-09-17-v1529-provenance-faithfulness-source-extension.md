# v15.29 Pre-Time Provenance Faithfulness / Source Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether frozen provenance certifies physically relevant distinctions inside a fixed coarse source fiber (q=B_1s), and if so whether those distinctions define a natural, representation-ready pre-time source extension without using gravity, metric, pruning, entropy, or physical time.

**Architecture:** Build a hash-pinned provenance inventory first, then construct exact (q)-fibers from the certified v15.25/v15.28 chain complex. Audit archived provenance only through typed relations actually present in the frozen evidence. A countermodel layer tests entailment before any source extension can be certified; a separate action layer tests covariance and representation readiness. The final gate adjudicates mechanically and never invokes the v15.28 coupling solver inside v15.29.

**Tech Stack:** Python 3.13.5, standard library dataclasses/hashlib/json/importlib, NumPy 2.3.5 only where inherited matrix fixtures require it, exact integer/Fraction arithmetic for fiber/action decisions, unittest, GitHub Actions, FFmpeg for the optional MP4.

**Spec:** `docs/superpowers/specs/2026-09-14-v1529-provenance-faithfulness-source-extension-design.md`

## Global Constraints

- Base scientific head is exactly `42244310b065f473c8bd459a6f065a61afbd2292`.
- All scientific implementation is additive under `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/`.
- Do not modify any v15.28-or-earlier scientific file.
- No implementation module may import or compute remote holonomy, inverse-square scores, Newton/Einstein/GR targets, physical distance, Hodge/minimum-action selectors, entropy, pruning, RCR actuality, or physical time.
- Raw microscopic incidence coordinates are not physical source semantics by default.
- Matching dimensions/cardinalities, lexical labels, sorting, PCA/SVD alignment, random isometries, and hand-selected cross-domain correspondences are forbidden selectors.
- A provenance distinction counts only if it is frozen-evidence-backed and survives every certified provenance gauge/relabeling equivalence.
- A typed/covariant extension is not automatically representation-ready.
- `PROVENANCE_SOURCE_REPRESENTATION_READY` additionally requires a finite exact linear representation or a canonical frozen-theory linearization, exact equivariant projection to (Q), and no supplied arbitrary embedding.
- v15.29 never invokes the downstream coupling solver even if representation readiness is certified; it only freezes the source carrier for a later gate.
- `signal_of_life=false`, `gravity_canary_certified=false`, `physical_gravity_derived=false`, and `Pillar_3="OPEN"` in every v15.29 outcome.
- Tests are written first and RED is recorded before each implementation task.
- GitHub Actions exact-head certification is authoritative for completion; local or ad-hoc runs are development evidence only.
- PR #25 remains draft and unmerged. No merge to `main` without explicit approval.

## Frozen Evidence Pins

Implementation must verify these Git blob IDs before using the corresponding evidence:

| Artifact | Path | Git blob |
|---|---|---|
| Genesis Pin bridge | `Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md` | `8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e` |
| V923 source-role report | `Tmp/TOE/Einstein 3/v923_full_stack_visualization/run/V923_FULL_STACK_VISUALIZATION_REPORT.md` | `f26a470720eeda324705569a519ab3a2fdc09848` |
| v13.26 source calibration | `ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md` | `9917085b211ca0e1f4737082227f55097cc72b66` |
| v14.04 provenance representation | `ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md` | `e5d9566bfc86c801d2933e63453d1800f60a675b` |
| v15.01 common parent | `ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md` | `1afbb7aebe384a1fb761f99fd2b040e595be1fa5` |
| v15.02 shared labels | `ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md` | `be1281621b0e2872e555223b2c1cdb98fe9d8011` |
| v15.03 graph/site lift | `ResearchHistory/UQCF-GEM/v15/v15.03/REPORT.md` | `6c3aed73c63c9c7554107d163e15b8fae7549c1c` |
| v15.08 source semantics | `ResearchHistory/UQCF-GEM/v15/v15.08/REPORT.md` | `23bbeaecdb81adfe1a39b3140569d23c367b8b55` |
| v15.09 carrier origin | `ResearchHistory/UQCF-GEM/v15/v15.09/REPORT.md` | `ec73ef9240dcef062c95a82c511a874d0d2923ef` |
| v15.25 chain/source fixture | `ResearchHistory/UQCF-GEM/demos/v15.25-pretime-gravity-canary/pretime_gravity_canary.py` | `99110f943550751645539c0c8a7339024d7fefd3` |
| v15.26 target coordinates | `ResearchHistory/UQCF-GEM/demos/v15.26-response-selector-rank/selector_rank.py` | `623defd0d8284e5d9cba6d8f8679de698e5202bc` |
| v15.27 target-origin theorem | `ResearchHistory/UQCF-GEM/demos/v15.27-target-origin/target_origin.py` | `1c33232050567bf3b2bf77b19570ec2b8a1fb5e0` |
| v15.28 gate | `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_gate.py` | `fd1962289627446090d9d673f70068f647171311` |
| v15.28 exact actions | `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/representation_actions.py` | `7260147cd6ca47ec21634172b44b98de726904af` |
| v15.28 exact linear core | `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/exact_linear.py` | `05cc1b8cfec70d501408377b5e44190b259a4514` |
| v15.28 coupling solver | `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/coupling_solver.py` | `de39fc726fa23b22a9d8809cd4da753756c31eb2` |
| v15.28 concise result | `ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/docs/RESULTS.json` | `6d1ed9766d89c2f66d072978a8fa4b60bedccb39` |

---

### Task 1: Freeze the Typed Provenance Evidence Inventory

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_inventory.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_inventory.py`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/PROVENANCE_INVENTORY.json`

**Interfaces:**
- Produces `EvidenceRecord`.
- Produces `frozen_inventory(repo_root: Path) -> tuple[EvidenceRecord, ...]`.
- Produces `by_key(key: str) -> EvidenceRecord`.
- Produces deterministic `inventory_digest(records) -> str`.

- [ ] **Step 1: Write failing inventory tests**

```python
class InventoryTests(unittest.TestCase):
    def test_every_record_is_blob_pinned(self):
        rows = inv.frozen_inventory(inv.REPO_ROOT)
        self.assertGreaterEqual(len(rows), 16)
        for row in rows:
            self.assertRegex(row.blob_sha, r'^[0-9a-f]{40}$')
            self.assertEqual(inv.git_blob_sha(inv.REPO_ROOT / row.path), row.blob_sha)

    def test_source_semantics_stays_irreducible(self):
        r = inv.by_key('v15.08-source-semantics')
        self.assertEqual(r.relation_to_micro_source, 'NO_TYPED_RELATION')
        self.assertEqual(r.source_semantics, 'IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY')

    def test_v1404_map_stays_conditional(self):
        r = inv.by_key('v14.04-supplied-intertwiner')
        self.assertEqual(r.representation_status, 'CONDITIONAL_ON_SUPPLIED_MAP')
```

- [ ] **Step 2: Run RED**

Run:
```bash
python -m unittest -v test_inventory.py
```

Expected: import/module failure because `provenance_inventory.py` does not yet exist.

- [ ] **Step 3: Implement the evidence model**

```python
@dataclass(frozen=True)
class EvidenceRecord:
    key: str
    path: str
    blob_sha: str
    evidence_type: str
    source_semantics: str
    relation_to_micro_source: str
    gauge_status: str
    action_status: str
    projection_status: str
    representation_status: str
    exact_claims: tuple[str, ...]
```

Use only these controlled values where applicable:

```text
CERTIFIED_PROVENANCE_RELATION
CERTIFIED_GAUGE_OR_EQUIVALENCE
CERTIFIED_ACTION
CERTIFIED_PROJECTION_TO_Q
ARCHIVE_EVIDENCE_ONLY
NO_TYPED_RELATION
CONDITIONAL_ON_SUPPLIED_MAP
IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY
```

Implement Git-blob hashing exactly:

```python
def git_blob_sha(path):
    raw = Path(path).read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
```

- [ ] **Step 4: Generate deterministic inventory JSON**

Sort by `key`, serialize with `sort_keys=True, allow_nan=False`, and include the inventory SHA-256 over the canonical compact JSON.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_inventory.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: freeze v15.29 typed provenance evidence inventory"
```

---

### Task 2: Build Exact Coarse-Source Fibers Without Promoting Representatives to Physics

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/fiber_model.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_fibers.py`

**Interfaces:**
- Consumes frozen v15.25 chain fixture and v15.28 exact action utilities after verifying their blob hashes.
- Produces `FiberFixture`.
- Produces `q_of(s) -> tuple[int, ...]`.
- Produces `face_shift(fixture, face_index, amplitude=1) -> tuple[int, ...]`.
- Produces `cycle_shift(fixture, cycle_index, amplitude=1) -> tuple[Fraction, ...]`.
- Produces `same_q(a, b) -> bool`.

- [ ] **Step 1: Write failing fiber tests**

```python
class FiberTests(unittest.TestCase):
    def test_face_boundary_shift_preserves_q_exactly(self):
        f = fm.root_fixture()
        s2 = fm.add(f.representative, fm.face_shift(f, 0))
        self.assertNotEqual(s2, f.representative)
        self.assertEqual(fm.q_of(f, s2), f.q)

    def test_every_exact_cycle_basis_shift_preserves_q(self):
        f = fm.root_fixture()
        for i in range(f.cycle_dimension):
            z = fm.cycle_shift(f, i)
            self.assertTrue(fm.vector_is_zero(fm.B1_times(f, z)))
            self.assertEqual(fm.q_of(f, fm.add(f.representative, z)), f.q)

    def test_coordinate_difference_is_not_physical_distinction(self):
        f = fm.root_fixture()
        s2 = fm.add(f.representative, fm.face_shift(f, 0))
        self.assertEqual(fm.raw_coordinate_relation(f.representative, s2),
                         'COORDINATES_DIFFER_ONLY_NO_PHYSICAL_CLAIM')
```

- [ ] **Step 2: Run RED**

Expected: `fiber_model` absent.

- [ ] **Step 3: Implement exact fixture loading**

Hash-check v15.25 blob `99110f...` and v15.28 action blob `726014...`. Load the torus complex, cast certified integer incidence matrices to Python integers, and use the exact cycle basis from v15.28.

```python
@dataclass(frozen=True)
class FiberFixture:
    B1: tuple[tuple[int, ...], ...]
    B2: tuple[tuple[int, ...], ...]
    representative: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    cycle_basis: tuple[tuple[Fraction, ...], ...]
```

No pseudoinverse or metric appears in this module.

- [ ] **Step 4: Add orientation/relabeling fixture controls**

Use v15.28 signed cell actions to transform (s), (B_1), and (q); verify (ho_0(g)B_1=B_1ho_1(g)) exactly on selected generators and all 392 automorphisms in the dedicated action task later.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_fibers.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: construct exact pre-time coarse-source fibers"
```

---

### Task 3: Extract Only Frozen Provenance Relations and Classify Fiber Pairs

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_equivalence.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_equivalence.py`

**Interfaces:**
- Produces `ProvenanceCertificate`.
- Produces `pair_relation(s1, s2, inventory) -> PairAudit`.
- Pair statuses are exactly:
  - `PROVENANCE_IDENTICAL`
  - `PROVENANCE_DISTINCT_CERTIFIED`
  - `PROVENANCE_DISTINCTION_GAUGE_ONLY`
  - `PROVENANCE_RELATION_UNSPECIFIED`

- [ ] **Step 1: Write fail-closed RED tests**

```python
class EquivalenceTests(unittest.TestCase):
    def test_raw_coordinate_difference_is_not_provenance(self):
        f = fm.root_fixture()
        s2 = fm.add(f.representative, fm.face_shift(f, 0))
        r = pe.pair_relation(f.representative, s2, inv.frozen_inventory(inv.REPO_ROOT))
        self.assertEqual(r.status, 'PROVENANCE_RELATION_UNSPECIFIED')

    def test_genesis_pin_is_history_legitimacy_not_incidence_identity(self):
        r = pe.archive_relation('v997-genesis-pin')
        self.assertFalse(r.references_micro_incidence)
        self.assertEqual(r.typed_role, 'HISTORY_LEGITIMACY_BOUNDARY')

    def test_source_role_does_not_map_to_edge_representative(self):
        r = pe.archive_relation('v923-source-role')
        self.assertFalse(r.references_micro_incidence)
```

- [ ] **Step 2: Run RED**

Expected: module absent.

- [ ] **Step 3: Implement typed relation extraction**

Do not NLP-infer physical meaning from prose. Each inventory entry declares the typed relation allowed by its frozen report. `pair_relation` may return a definite identity/distinction only when an inventory record explicitly has `CERTIFIED_PROVENANCE_RELATION` whose argument types include the microscopic representative type used by `fiber_model`.

If no such typed relation exists, return `PROVENANCE_RELATION_UNSPECIFIED`.

- [ ] **Step 4: Add synthetic controls in a separate namespace**

```python
synthetic_distinct = ProvenanceCertificate(
    key='synthetic-fiber-label',
    argument_type='MICRO_SOURCE_REPRESENTATIVE',
    relation='DISTINGUISH_EXACT_LABEL',
    gauge_invariant=True,
    physical_evidence=False,
)
```

The synthetic control must produce `PROVENANCE_DISTINCT_CERTIFIED` while carrying `physical_evidence=False`.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_equivalence.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: classify q-fiber provenance relations fail closed"
```

---

### Task 4: Prove or Defeat Provenance-Extension Entailment With Explicit Countermodels

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/countermodels.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_countermodels.py`

**Interfaces:**
- Produces `FrozenConstraint`.
- Produces `ProvenanceModel`.
- Produces `countermodel_audit(fixture, inventory) -> CountermodelAudit`.

- [ ] **Step 1: Write RED tests**

```python
class CountermodelTests(unittest.TestCase):
    def test_same_frozen_constraints_allow_collapsed_and_distinguished_models_when_relation_unspecified(self):
        a = cm.countermodel_audit(fm.root_fixture(), inv.frozen_inventory(inv.REPO_ROOT))
        self.assertTrue(a.collapsed_model_satisfies_all)
        self.assertTrue(a.distinguished_model_satisfies_all)
        self.assertTrue(a.models_disagree_on_fiber_relation)
        self.assertEqual(a.verdict, 'PROVENANCE_EXTENSION_NOT_ENTAILED')

    def test_explicit_typed_relation_would_kill_countermodel(self):
        a = cm.synthetic_relation_control()
        self.assertFalse(a.models_disagree_on_fiber_relation)
        self.assertEqual(a.verdict, 'RELATION_ENTAILED_IN_SYNTHETIC_CONTROL')
```

- [ ] **Step 2: Run RED**

Expected: `countermodels` absent.

- [ ] **Step 3: Implement logical constraints**

A frozen constraint is typed; it does not mention microscopic representatives unless the archive actually provides such an argument.

```python
@dataclass(frozen=True)
class FrozenConstraint:
    key: str
    argument_types: tuple[str, ...]
    predicate: str
    expected: object
```

Build two models over one (q)-fiber:
1. `collapsed`: all microscopic representatives receive the same provenance class.
2. `distinguished`: at least two representatives receive different provenance classes while all frozen constraints that lack microscopic arguments remain unchanged.

The test is logical consistency, not numerical scoring.

- [ ] **Step 4: Make non-entailment priority explicit**

If both models satisfy every frozen constraint and disagree on the fiber relation, the gate must not later certify an extension from the same evidence.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_countermodels.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: add provenance extension countermodel entailment audit"
```

---

### Task 5: Audit Covariance, Gauge Survival, and Representation Readiness Separately

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/action_audit.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_actions.py`

**Interfaces:**
- Produces `ActionAudit`.
- Produces `audit_action(candidate) -> ActionAudit`.
- Produces `representation_ready(candidate, action_audit, projection_audit) -> bool`.

- [ ] **Step 1: Write RED tests**

```python
class ActionTests(unittest.TestCase):
    def test_raw_delta_b_is_rejected_without_provenance_action(self):
        a = aa.audit_action(aa.raw_representative_control())
        self.assertFalse(a.provenance_action_certified)
        self.assertFalse(a.representation_ready)

    def test_v1404_supplied_map_stays_conditional(self):
        a = aa.audit_action(aa.v1404_supplied_map_control())
        self.assertEqual(a.status, 'CONDITIONAL_ON_SUPPLIED_MAP')
        self.assertFalse(a.representation_ready)

    def test_synthetic_linear_extension_is_recognized(self):
        a = aa.audit_action(aa.synthetic_linear_extension())
        self.assertTrue(a.provenance_action_certified)
        self.assertTrue(a.exact_linear_representation)
        self.assertTrue(a.representation_ready)
```

- [ ] **Step 2: Run RED**

Expected: `action_audit` absent.

- [ ] **Step 3: Implement action requirements**

```python
@dataclass(frozen=True)
class ActionAudit:
    status: str
    provenance_action_certified: bool
    relabeling_covariant: bool
    orientation_convention_safe: bool
    genesis_root_preserved: bool
    exact_linear_representation: bool
    canonical_linearization: bool
    arbitrary_embedding_used: bool
    representation_ready: bool
```

For physical archive candidates, `exact_linear_representation` can be true only if the frozen evidence supplies one or a canonical exact linearization is derived without target feedback.

- [ ] **Step 4: Verify the synthetic action under all 392 automorphisms**

Reuse hash-pinned v15.28 `representation_actions.py`. The synthetic extension must obey group composition and exact equivariance of its projection. The archive result cannot inherit that action unless its labels are typed to the same cells by frozen evidence.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_actions.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: separate provenance covariance from representation readiness"
```

---

### Task 6: Certify Exact Projection-to-q and Source Extension Status

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_extension.py`

**Interfaces:**
- Produces `ProjectionAudit`.
- Produces `SourceExtensionAudit`.
- Produces `audit_source_extension() -> SourceExtensionAudit`.

- [ ] **Step 1: Write RED tests for all preregistered branches**

```python
class ExtensionTests(unittest.TestCase):
    def test_collapsed_control(self):
        r = gate.collapsed_q_control()
        self.assertEqual(r.status, 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE')

    def test_synthetic_extension_certifies_but_is_not_physical_evidence(self):
        r = gate.synthetic_extension_control()
        self.assertEqual(r.status, 'PROVENANCE_SOURCE_REPRESENTATION_READY')
        self.assertTrue(r.projection_exact)
        self.assertTrue(r.representation_ready)
        self.assertFalse(r.physical_evidence)

    def test_archive_countermodels_force_non_entailment(self):
        r = gate.audit_source_extension()
        self.assertIn(r.status, {
            'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE',
            'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED',
            'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION',
            'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED',
            'PROVENANCE_SOURCE_REPRESENTATION_READY',
            'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM',
        })
        if r.countermodels_survive:
            self.assertEqual(r.status, 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')
```

- [ ] **Step 2: Run RED**

Expected: `source_extension_gate` absent.

- [ ] **Step 3: Implement exact projection audit**

```python
@dataclass(frozen=True)
class ProjectionAudit:
    projection_defined: bool
    projection_exact: bool
    equivariant: bool
    chosen_section_used: bool
```

A section (Q	o S_{m prov}) is forbidden and must always remain false for physical adjudication.

- [ ] **Step 4: Implement status priority**

Use this order:

```python
if requires_new_source_semantics:
    status = 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM'
elif countermodels_survive:
    status = 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED'
elif no_nontrivial_fiber_distinction:
    status = 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE'
elif not natural_action_certified:
    status = 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION'
elif not representation_ready:
    status = 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED'
else:
    status = 'PROVENANCE_SOURCE_REPRESENTATION_READY'
```

This priority ensures a convenient extension cannot override a surviving non-entailment countermodel.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_extension.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: adjudicate provenance source extension exactly"
```

---

### Task 7: Build the Preregistered Scientific Ledger and Claim Boundary

**Files:**
- Modify: `source_extension_gate.py`
- Extend: `test_extension.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/README.md`
- Create after GREEN: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/RESULTS.json`

**Interfaces:**
- Produces `audit() -> dict`.
- Produces CLI `python source_extension_gate.py --out outputs`.

- [ ] **Step 1: Add fail-closed ledger tests**

Required keys:

```python
REQUIRED = {
 'version','status','base_sha','inventory_digest','fiber_audit','provenance_relations',
 'countermodel_audit','action_audit','projection_audit','source_extension',
 'provenance_distinction_certified','countermodels_survive',
 'enhanced_source_carrier_certified','representation_ready',
 'coupling_solver_invoked','coupling_space_recomputed','gravity_observables_evaluated',
 'uses_holonomy_selector','uses_newton_or_gr','uses_metric_selector',
 'uses_pruning','uses_entropy','uses_physical_time','new_source_semantics_axiom_added',
 'scientific_breakthrough','signal_of_life','gravity_canary_certified',
 'physical_gravity_derived','Pillar_3','next_required_object'
}
```

Assert every forbidden selector flag is false.

- [ ] **Step 2: Implement breakthrough rule**

```python
scientific_breakthrough = (
    status == 'PROVENANCE_SOURCE_REPRESENTATION_READY'
    and source_extension['physical_evidence'] is True
    and countermodels_survive is False
)
```

Even then:

```python
signal_of_life = False
gravity_canary_certified = False
physical_gravity_derived = False
coupling_solver_invoked = False
coupling_space_recomputed = False
```

- [ ] **Step 3: Set next object mechanically**

```python
NEXT = {
 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED':
     'INDEPENDENTLY_MOTIVATED_SOURCE_SEMANTICS_OR_NEW_TYPED_PROVENANCE_RELATION',
 'PROVENANCE_COLLAPSES_TO_Q_EQUIVALENCE':
     'SOURCE_TO_CYCLE_CONSTITUTIVE_PRINCIPLE_BEYOND_PROVENANCE',
 'PROVENANCE_DISTINGUISHES_REPRESENTATIVES_BUT_NO_NATURAL_ACTION':
     'NATURAL_PROVENANCE_ACTION_ON_SOURCE_EXTENSION',
 'PROVENANCE_ENHANCED_SOURCE_CARRIER_CERTIFIED':
     'CANONICAL_LINEARIZATION_OR_EXACT_SOURCE_REPRESENTATION',
 'PROVENANCE_SOURCE_REPRESENTATION_READY':
     'NEW_GRAVITY_BLIND_COUPLING_SPACE_GATE_FOR_CERTIFIED_SOURCE_CARRIER',
 'PROVENANCE_EXTENSION_REQUIRES_NEW_SOURCE_SEMANTICS_AXIOM':
     'EXPLICIT_HUMAN_APPROVAL_OF_NEW_SOURCE_SEMANTICS_AXIOM',
}
```

- [ ] **Step 4: Write README from executed ledger only**

README must distinguish theorem/logical non-entailment, finite computation, and physical interpretation. It must state explicitly that no v15.28 coupling member was selected.

- [ ] **Step 5: Run GREEN and commit**

```bash
python source_extension_gate.py --out outputs
python -m unittest -v test_inventory.py test_fibers.py test_equivalence.py test_countermodels.py test_actions.py test_extension.py
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: freeze v15.29 provenance faithfulness adjudication"
```

---

### Task 8: Add Gravity-Blind Offline Inspector and 24-Second Replay

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/viewer.html`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/test_replay.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/requirements.txt`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/.gitignore`

**Interfaces:**
- `payload()` consumes only `source_extension_gate.audit()`.
- `write_html(payload, path)` is self-contained/offline.
- `movie(path, fps=10)` shows classification state only.

- [ ] **Step 1: Write RED presentation tests**

```python
class ReplayTests(unittest.TestCase):
    def test_payload_has_fiber_and_provenance_not_gravity_scores(self):
        p = replay.payload()
        self.assertIn('fiber_audit', p['audit'])
        self.assertIn('countermodel_audit', p['audit'])
        text = json.dumps(p).lower()
        for forbidden in ('holonomy_value','inverse_square_score','newton_score','einstein_score'):
            self.assertNotIn(forbidden, text)

    def test_html_is_offline_and_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('Microscopic difference is not physical sourcehood by itself', text)
            self.assertIn('Playback is not physical time', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_fps_guard(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)
```

- [ ] **Step 2: Run RED**

Expected: replay/viewer absent.

- [ ] **Step 3: Implement six-scene replay**

Scenes are exactly:
1. (q=B_1s) as coarse source quotient.
2. Several representatives in one exact fiber.
3. Frozen provenance relation status.
4. Gauge/relabeling/action audit.
5. Countermodel/extension adjudication.
6. Final status + explicit gravity boundary.

No field/geometry/holonomy plot is allowed.

- [ ] **Step 4: Run GREEN, render and decode**

```bash
python -m unittest -v test_replay.py
python replay.py --out outputs --video
ffmpeg -v error -i outputs/provenance_faithfulness.mp4 -f null -
```

- [ ] **Step 5: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness
git commit -m "feat: add gravity-blind v15.29 provenance replay"
```

---

### Task 9: Exact-Head CI, Full Selected Regression, and Digest-Verified Release

**Files:**
- Create: `.github/workflows/uqcf-v1529-provenance-faithfulness.yml`
- Update PR #25 only with executed evidence after successful exact-head certification.

**Interfaces:**
- Exact-head additive comparison base is `42244310b065f473c8bd459a6f065a61afbd2292`.
- Inherited selected suite count is exactly 552: 517 v15.11–v15.27 checks + 35 v15.28 checks.
- New v15.29 count is discovered from its unittest output and added to 552.
- Publication creates eight release assets only after remote size/SHA-256 checks.

- [ ] **Step 1: Add exact-head workflow**

Allow changes only under:
- `ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/**`
- `docs/superpowers/specs/2026-09-14-v1529-provenance-faithfulness-source-extension-design.md`
- this implementation plan
- `.github/workflows/uqcf-v1529-provenance-faithfulness.yml`

Run the same v15.11–v15.27 suites used by successful v15.28 CI, then v15.28:

```python
('demos/v15.28-coupling-space',
 ['test_inventory.py','test_exact_linear.py','test_actions.py',
  'test_solver.py','test_gate.py','test_replay.py'], 35)
```

Assert inherited total `552`.

Run v15.29 tests:

```python
NEW = [
 'test_inventory.py','test_fibers.py','test_equivalence.py',
 'test_countermodels.py','test_actions.py','test_extension.py','test_replay.py'
]
```

Capture exact new count from `Ran N tests`.

- [ ] **Step 2: Regenerate authoritative deliverables**

```bash
python source_extension_gate.py --out outputs > evidence/ci/model.log
python replay.py --out outputs --video > evidence/ci/render.log
ffmpeg -v error -i outputs/provenance_faithfulness.mp4 -f null -   2> evidence/ci/video_decode.log
ffprobe -v error   -show_entries stream=codec_name,width,height   -show_entries format=duration   -of json outputs/provenance_faithfulness.mp4   > evidence/ci/video_info.json
```

Require H.264 1280×720 and 24.0±0.1 seconds.

- [ ] **Step 3: Assert claim boundary from generated ledger**

```python
r = json.load(open('outputs/verification.json'))
assert r['base_sha'] == '42244310b065f473c8bd459a6f065a61afbd2292'
assert r['coupling_solver_invoked'] is False
assert r['coupling_space_recomputed'] is False
assert r['signal_of_life'] is False
assert r['gravity_canary_certified'] is False
assert r['physical_gravity_derived'] is False
assert r['Pillar_3'] == 'OPEN'
assert not any(r[k] for k in (
    'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
    'uses_metric_selector','uses_pruning','uses_entropy','uses_physical_time'))
```

- [ ] **Step 4: Package eight release assets**

Publish exactly:
1. `provenance_faithfulness.mp4`
2. `provenance_faithfulness.html`
3. `verification.json`
4. `replay_data.json`
5. `REPORT.md`
6. `PROVENANCE.json`
7. `UQCF_GEM_v15_29_bundle.zip`
8. `SHA256SUMS.txt`

Bundle must include source, design spec, this plan, generated data, and fresh CI logs. Verify every bundle-member SHA-256 and then every uploaded release asset size/digest before changing the release from draft to public prerelease.

- [ ] **Step 5: Post-publication presentation checks**

Download the verified delivery artifact/release bytes. Execute the HTML in system Chromium with:
- every declared view/control,
- widths 1280, 820, 390,
- zero JavaScript errors,
- zero external requests,
- document scroll width equal to viewport width.

Fully decode the downloaded MP4 again and visually inspect all six scene frames. Record native Safari/iPad as untested unless actually exercised.

- [ ] **Step 6: Record exact-head receipt on PR #25**

Comment with:
- exact SHA,
- workflow/run/job IDs,
- inherited/new/total selected test counts,
- final scientific status,
- release URL,
- eight asset names,
- artifact SHA-256 digests,
- browser/video evidence,
- explicit statement that `main` was not changed,
- explicit statement that the PR remains draft/unmerged,
- explicit statement that this is selected regression/self-review, not independent scientific peer review.

- [ ] **Step 7: Verify `main` and stop**

Fetch `refs/heads/main` and confirm it is still `8cf86768313eac837f904175b6d7b47e8e5460b0` unless the user separately approved a merge. Do not merge PR #25.

---

## Plan Self-Review Checklist

Before execution begins, verify:

1. **Spec coverage:** Tasks 1–9 cover evidence inventory, exact fibers, typed provenance relation, countermodel non-entailment, gauge/covariance, projection, representation readiness, adjudication, gravity-blind presentation, regression and release.
2. **No source-semantics leak:** no task declares (delta b), Genesis Pin, source role, or a supplied intertwiner to be the physical source.
3. **No downstream selector:** no gravity observable or target appears in any adjudication input.
4. **No hidden section:** projection (S_{m prov}	o Q) may be certified; no chosen section (Q	o S_{m prov}) is allowed.
5. **Representation readiness separated:** covariant extension alone cannot reopen the v15.28 solver.
6. **Countermodels take priority:** surviving collapsed/distinguished models force non-entailment even if a convenient implementation exists.
7. **Synthetic controls stay synthetic:** they validate the machinery but can never count as UQCF physical evidence.
8. **Type consistency:** the exact status strings and dataclass field names are identical across tasks.
9. **No placeholders:** no TODO/TBD/future implementation language remains.
10. **Delivery boundary:** exact-head GitHub CI is required before completion or publication claims.
