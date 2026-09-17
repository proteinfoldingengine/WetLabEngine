# UQCF-GEM v15.30 Provenance–Fiber Definability / Common-Carrier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether any already-frozen ontology-native object canonically defines a provenance relation on exact microscopic representatives inside one fixed `q = B1 x` fiber, without adding a source-semantics axiom or consulting downstream coupling/gravity criteria.

**Architecture:** v15.30 is a theorem-first typed-relation audit stacked on the certified v15.29 head. It reuses v15.29's exact q-fiber implementation by hash-pinned file-path import, extends the frozen evidence inventory with four candidate-origin bundles, constructs a certified carrier-relation graph, then evaluates exact-fiber compatibility, naturality, uniqueness, and no-choice constraints. Synthetic controls exercise positive and negative branches without promoting synthetic structures into frozen evidence.

**Tech Stack:** Python 3.13.5; standard-library `argparse`, `dataclasses`, `fractions`, `hashlib`, `importlib`, `json`, `pathlib`, `unittest`; NumPy 2.3.5 and Matplotlib 3.10.8 only for inherited modules and replay; FFmpeg for optional H.264 media; GitHub Actions for exact-head certification and delivery.

**Spec:** `docs/superpowers/specs/2026-09-17-v1530-provenance-fiber-definability-common-carrier-design.md`

## Global Constraints

- Stacked delivery/scientific base: `6535ea69214f6661e340fe201813dfd17ddbb7e1`.
- Inherited scientific source pin: `42244310b065f473c8bd459a6f065a61afbd2292`.
- Inherited v15.29 result: `PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED`.
- Exactly four real candidate origins are allowed: Genesis/history lineage; minimal ternary source role; retained graph source/current; Genesis 6-D provenance carrier.
- `x` denotes the torus microscopic representative. Retained graph source variables use `s_ret`.
- Same-fiber equality is exact integer/rational equality only.
- No gravity, coupling, metric, entropy, pruning-performance, recoverability-performance, physical-time, PCA/SVD, learned embedding, dimension/cardinality matching, shared vocabulary, supplied intertwiner, or preferred representative may select the real relation.
- Real statuses are exactly `NO_TYPED_COMMON_CARRIER`, `PROVENANCE_FIBER_RELATION_NOT_DEFINABLE`, `MULTIPLE_NATURAL_RELATIONS_REMAIN`, `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED`.
- `new_source_semantics_axiom_added`, `coupling_solver_reopened`, `gravity_observables_evaluated`, `signal_of_life`, `gravity_canary_certified`, and `physical_gravity_derived` remain false for every v15.30 real outcome.
- No v15.30 result directly authorizes a coupling or gravity gate.

## File Map

Create:

```text
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/.gitignore
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/README.md
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/requirements.txt
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/frozen_inputs.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/typed_carrier_graph.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/exact_fiber.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/naturality.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/uniqueness.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/definability_gate.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/replay.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/viewer.html
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_frozen_inputs.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_common_carrier.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_exact_fiber.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_naturality.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_uniqueness.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_gate.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_replay.py
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/CANDIDATE_EVIDENCE.json
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/RESULTS.json
.github/workflows/uqcf-v1530-provenance-fiber-definability.yml
```

No v15.29 scientific file is modified.

---

## Task 1: Frozen Inputs and Candidate Evidence

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/frozen_inputs.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_frozen_inputs.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/CANDIDATE_EVIDENCE.json`

**Interfaces:**

```python
@dataclass(frozen=True)
class CandidateEvidence:
    key: str
    domain: str
    evidence_keys: tuple[str, ...]
    artifact_pins: tuple[tuple[str, str], ...]
    transformation_source: str
    certified_relation_claims: tuple[str, ...]
    claim_boundary: str

@dataclass(frozen=True)
class FrozenModules:
    provenance_inventory: object
    fiber_model: object
    source_extension_gate: object
    v1529_results: dict

load_v1529() -> FrozenModules
candidate_inventory(repo_root: Path) -> tuple[CandidateEvidence, ...]
candidate_by_key(key: str, rows=None) -> CandidateEvidence
verify_candidate(row: CandidateEvidence, repo_root: Path) -> None
inventory_digest(rows) -> str
write_candidate_inventory(path: Path, rows) -> None
```

Exact inherited pins:

```text
ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/provenance_inventory.py  81a41442d2f3b26817657ebb5f3dc948e62d14b2
ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/fiber_model.py           e04cf0b24bbce6f908b83c9472c1f1b5639b7e8b
ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/source_extension_gate.py 305af411792c08906ea8eed2c9aeba3de25be1cf
ResearchHistory/UQCF-GEM/demos/v15.29-provenance-faithfulness/docs/RESULTS.json        0984a8238a7fd2a115ab673a3d4f23b0706c7b12
```

Exact candidate pins:

```text
Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md                                   8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e
Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/FULL_REPORT_AND_PROOF.md             9a1523c08d2b9b2c5ba2d298dfed3d563a750bec
Tmp/TOE/Einstein 3/v923_full_stack_source_role_closure_proof/v923_full_stack_source_role_closure_proof.py 90f69d5101e0ab14488d8d25da326e7b94341375
ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md                                                      9917085b211ca0e1f4737082227f55097cc72b66
ResearchHistory/UQCF-GEM/v14/v14.04/REPORT.md                                                      e5d9566bfc86c801d2933e63453d1800f60a675b
ResearchHistory/UQCF-GEM/v14/v14.04/provenance_representation_audit.py                             1e75767a59a54b4fb7840ca355eb00845cf119e3
ResearchHistory/UQCF-GEM/v15/v15.01/REPORT.md                                                      1afbb7aebe384a1fb761f99fd2b040e595be1fa5
ResearchHistory/UQCF-GEM/v15/v15.01/common_parent_audit.py                                         b8b6ef14b323659eb730b33bd3d36c99e7f03957
Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py   78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import frozen_inputs as fi


class FrozenInputTests(unittest.TestCase):
    def test_v1529_result_pin_and_stop_object(self):
        mods = fi.load_v1529()
        self.assertEqual(mods.v1529_results['status'],
                         'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')
        self.assertEqual(mods.v1529_results['next_required_object'],
                         'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION')

    def test_inherited_module_blobs_are_exact(self):
        mods = fi.load_v1529()
        self.assertIsNotNone(mods.provenance_inventory)
        self.assertIsNotNone(mods.fiber_model)
        self.assertIsNotNone(mods.source_extension_gate)

    def test_exact_four_candidate_origins(self):
        rows = fi.candidate_inventory(fi.REPO_ROOT)
        self.assertEqual(tuple(row.key for row in rows), (
            'genesis-history-lineage',
            'genesis-6d-carrier',
            'retained-source-current',
            'ternary-source-role',
        ))

    def test_candidate_artifact_pins_are_exact(self):
        for row in fi.candidate_inventory(fi.REPO_ROOT):
            fi.verify_candidate(row, fi.REPO_ROOT)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability
python -m unittest -v test_frozen_inputs.py
```

Expected: fail because `frozen_inputs.py` is absent.

- [ ] **Step 3: Implement hash verification and exact file-path loading**

Use Git blob hashing:

```python
def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
```

`load_v1529()` must verify every inherited pin before importing by `importlib.util.spec_from_file_location`. It must parse the pinned v15.29 result and assert:

```python
ledger['version'] == 'v15.29'
ledger['status'] == 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED'
ledger['next_required_object'] == 'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION'
```

Create exactly four `CandidateEvidence` records, sorted by key. `certified_relation_claims` records only already-certified candidate-internal claims; it does not certify a q-fiber relation.

- [ ] **Step 4: Generate deterministic evidence JSON and run GREEN**

```bash
python frozen_inputs.py --out docs/CANDIDATE_EVIDENCE.json
python -m unittest -v test_frozen_inputs.py
python frozen_inputs.py --out /tmp/v1530_candidate_evidence.json
cmp docs/CANDIDATE_EVIDENCE.json /tmp/v1530_candidate_evidence.json
```

Expected: 4 tests PASS; byte comparison PASS.

- [ ] **Step 5: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/frozen_inputs.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_frozen_inputs.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/CANDIDATE_EVIDENCE.json
git commit -m "feat: freeze v15.30 candidate evidence inventory"
```

---

## Task 2: Gate A — Certified Typed Common-Carrier Graph

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/typed_carrier_graph.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_common_carrier.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class TypedEdge:
    source: str
    target: str
    relation_class: str
    evidence_key: str
    synthetic: bool = False

@dataclass(frozen=True)
class CarrierConnection:
    candidate_domain: str
    torus_domain: str
    direct_path: tuple[TypedEdge, ...]
    common_node: str | None
    common_node_kind: str | None
    real_certified: bool
    reason: str

relation_class_is_certifying(name: str) -> bool
build_real_graph() -> tuple[CarrierGraph, tuple[CandidateEvidence, ...]]
find_typed_connection(graph, candidate_domain, torus_domain, real_only=True) -> CarrierConnection
audit_candidate_common_carrier(candidate, graph) -> dict
```

Only these relation classes create real graph edges:

```text
CERTIFIED_PROVENANCE_RELATION
CERTIFIED_GAUGE_OR_EQUIVALENCE
CERTIFIED_PROJECTION_TO_Q
CERTIFIED_ACTION
```

`ARCHIVE_EVIDENCE_ONLY`, `NO_TYPED_RELATION`, and `CONDITIONAL_ON_SUPPLIED_MAP` never create a real edge.

Register the inherited exact projection explicitly:

```python
TypedEdge(
    source='TORUS_EDGE_REPRESENTATIVE',
    target='Q_SOURCE_QUOTIENT',
    relation_class='CERTIFIED_PROJECTION_TO_Q',
    evidence_key='v15.29-fiber-model:B1',
    synthetic=False,
)
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import typed_carrier_graph as tc


class CommonCarrierTests(unittest.TestCase):
    def test_common_words_create_no_edge(self):
        graph = tc.CarrierGraph()
        graph.add_untyped_note('source provenance site origin')
        self.assertFalse(graph.has_certified_path('A', 'B'))

    def test_supplied_embedding_is_not_real_evidence(self):
        graph = tc.synthetic_supplied_embedding_graph()
        result = tc.find_typed_connection(
            graph, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE', real_only=True)
        self.assertFalse(result.real_certified)

    def test_synthetic_common_parent_is_detected(self):
        graph = tc.synthetic_common_parent_graph()
        result = tc.find_typed_connection(
            graph, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE', real_only=False)
        self.assertEqual(result.common_node, 'SYNTHETIC_PARENT')
        self.assertEqual(result.common_node_kind, 'PARENT')

    def test_real_graph_has_exactly_four_candidate_roots(self):
        graph, candidates = tc.build_real_graph()
        self.assertEqual(len(candidates), 4)
        self.assertIn('TORUS_EDGE_REPRESENTATIVE', graph.nodes())

    def test_untyped_relation_classes_never_promote(self):
        for name in ('NO_TYPED_RELATION', 'ARCHIVE_EVIDENCE_ONLY',
                     'CONDITIONAL_ON_SUPPLIED_MAP'):
            self.assertFalse(tc.relation_class_is_certifying(name))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest -v test_common_carrier.py
```

Expected: fail because `typed_carrier_graph.py` is absent.

- [ ] **Step 3: Implement graph search**

Search in this exact order:

1. candidate → torus certified path;
2. torus → candidate certified path;
3. common parent `K` with `K → candidate` and `K → torus` certified paths;
4. common quotient `K` with `candidate → K` and `torus → K` certified paths.

When `real_only=True`, any path containing `synthetic=True` is rejected. The graph may record untyped notes for diagnostics but those notes never participate in reachability.

- [ ] **Step 4: Run GREEN and commit**

```bash
python -m unittest -v test_frozen_inputs.py test_common_carrier.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/typed_carrier_graph.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_common_carrier.py
git commit -m "feat: add v15.30 typed common-carrier gate"
```

Expected cumulative count: 9 tests.

---

## Task 3: Gate B — Exact q-Fiber Compatibility

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/exact_fiber.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_exact_fiber.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class FiberCase:
    key: str
    edge_vector: tuple[int, ...]
    q: tuple[int, ...]

canonical_fiber_cases() -> tuple[FiberCase, ...]
same_q_exact(a: FiberCase, b: FiberCase) -> bool
evaluate_labeling_on_fiber(label_fn) -> tuple[object, ...]
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import exact_fiber as ef


class ExactFiberTests(unittest.TestCase):
    def test_face_shift_is_distinct_and_same_q(self):
        root, face, cycle = ef.canonical_fiber_cases()
        self.assertNotEqual(root.edge_vector, face.edge_vector)
        self.assertTrue(ef.same_q_exact(root, face))

    def test_cycle_shift_is_distinct_and_same_q(self):
        root, face, cycle = ef.canonical_fiber_cases()
        self.assertNotEqual(root.edge_vector, cycle.edge_vector)
        self.assertTrue(ef.same_q_exact(root, cycle))

    def test_noncycle_shift_changes_q(self):
        root = ef.canonical_fiber_cases()[0]
        self.assertFalse(ef.noncycle_control_preserves_q(root, edge_index=3))

    def test_q_only_label_collapses_entire_fiber(self):
        labels = ef.evaluate_labeling_on_fiber(lambda case: case.q)
        self.assertEqual(len(set(labels)), 1)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

Expected: missing `exact_fiber.py`.

- [ ] **Step 3: Implement by reusing the pinned v15.29 fiber model**

```python
def canonical_fiber_cases():
    fm = fi.load_v1529().fiber_model
    root = fm.root_fixture()
    face = fm.face_shift(root, face_index=0, coefficient=1)
    cycle = fm.cycle_shift(root, fm.canonical_cycle_basis()[7])
    return (
        FiberCase('root', root.edge_vector, root.q),
        FiberCase('face-boundary-shift', face.edge_vector, face.q),
        FiberCase('cycle-shift', cycle.edge_vector, cycle.q),
    )
```

`noncycle_control_preserves_q()` changes one edge coordinate by `+1`, recomputes `q` through the inherited `apply_B1()`, and returns exact tuple equality. v15.30 must not rebuild incidence matrices independently.

- [ ] **Step 4: Run GREEN and commit**

```bash
python -m unittest -v test_exact_fiber.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/exact_fiber.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_exact_fiber.py
git commit -m "feat: add exact v15.30 q-fiber compatibility gate"
```

Expected cumulative count: 13 tests.

---

## Task 4: Gate C — Naturality / Automorphism Definability

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/naturality.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_naturality.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class FiniteRelation:
    rep_keys: tuple[str, ...]
    labels: tuple[str, ...]

@dataclass(frozen=True)
class FiniteAction:
    elements: tuple[str, ...]
    rep_permutations: dict[str, tuple[int, ...]]
    label_permutations: dict[str, tuple[int, ...]]
    multiplication: dict[tuple[str, str], str]

@dataclass(frozen=True)
class NaturalityResult:
    certified: bool
    group_law_exact: bool
    equivariant: bool
    reason: str

check_group_law(action: FiniteAction) -> bool
check_equivariance(relation: FiniteRelation, action: FiniteAction) -> bool
audit_relation_naturality(relation, certified_action) -> NaturalityResult
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import naturality as nat


class NaturalityTests(unittest.TestCase):
    def test_swap_preserving_reduct_rejects_noninvariant_relation(self):
        relation, action = nat.synthetic_swap_counterexample()
        result = nat.audit_relation_naturality(relation, action)
        self.assertFalse(result.certified)
        self.assertFalse(result.equivariant)

    def test_equivariant_synthetic_relation_passes(self):
        relation, action = nat.synthetic_equivariant_control()
        result = nat.audit_relation_naturality(relation, action)
        self.assertTrue(result.certified)
        self.assertTrue(result.group_law_exact)
        self.assertTrue(result.equivariant)

    def test_missing_certified_action_fails_closed(self):
        relation, action = nat.synthetic_equivariant_control()
        result = nat.audit_relation_naturality(relation, None)
        self.assertFalse(result.certified)
        self.assertEqual(result.reason, 'NO_CERTIFIED_ACTION_FOR_DEFINABILITY')

    def test_group_law_checked_exactly_for_finite_control(self):
        relation, action = nat.synthetic_equivariant_control()
        self.assertTrue(nat.check_group_law(action))
        broken = nat.break_multiplication_table(action)
        self.assertFalse(nat.check_group_law(broken))


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

Expected: missing `naturality.py`.

- [ ] **Step 3: Implement exact finite checks**

For each `g` and `h`, require the stored permutation for `g*h` to equal permutation composition exactly. For equivariance, for every representative index `i`, require:

```text
label(g · i) = g · label(i)
```

No numerical tolerance is used.

A real candidate relation with no pinned action/transformation witness returns `NO_CERTIFIED_ACTION_FOR_DEFINABILITY`; v15.30 must not borrow the torus action and declare that it acts on an unrelated provenance carrier.

- [ ] **Step 4: Run GREEN and commit**

```bash
python -m unittest -v test_naturality.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/naturality.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_naturality.py
git commit -m "feat: add v15.30 naturality gate"
```

Expected cumulative count: 17 tests.

---

## Task 5: Gate D — Uniqueness / Countermodels

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/uniqueness.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_uniqueness.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class UniquenessResult:
    status: str
    signatures: tuple[tuple[int, ...], ...]
    witness_pair: tuple[tuple[int, ...], tuple[int, ...]] | None

canonical_partition_signature(labels) -> tuple[int, ...]
relations_inequivalent(a, b) -> bool
classify_relation_family(labelings) -> UniquenessResult
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import uniqueness as uq


class UniquenessTests(unittest.TestCase):
    def test_label_renaming_does_not_create_new_relation(self):
        self.assertEqual(uq.canonical_partition_signature(('A','A','B')),
                         uq.canonical_partition_signature(('X','X','Y')))

    def test_two_distinct_partitions_prove_nonuniqueness(self):
        result = uq.classify_relation_family((('A','A','B'), ('A','B','B')))
        self.assertEqual(result.status, 'MULTIPLE')
        self.assertIsNotNone(result.witness_pair)

    def test_single_survivor_is_unique(self):
        result = uq.classify_relation_family((('A','A','B'), ('X','X','Y')))
        self.assertEqual(result.status, 'UNIQUE')
        self.assertEqual(len(result.signatures), 1)

    def test_empty_family_cannot_certify_uniqueness(self):
        result = uq.classify_relation_family(())
        self.assertEqual(result.status, 'NONE')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

Expected: missing `uniqueness.py`.

- [ ] **Step 3: Implement canonical signatures**

```python
def canonical_partition_signature(labels):
    ids = {}
    next_id = 0
    out = []
    for label in labels:
        if label not in ids:
            ids[label] = next_id
            next_id += 1
        out.append(ids[label])
    return tuple(out)
```

`classify_relation_family()` deduplicates signatures. Zero signatures → `NONE`; one → `UNIQUE`; two or more → `MULTIPLE` and stores the first two distinct signatures as the countermodel witness. Infinite analytic families do not require enumeration: supplying any two exact inequivalent admissible signatures is sufficient to return `MULTIPLE`.

- [ ] **Step 4: Run GREEN and commit**

```bash
python -m unittest -v test_uniqueness.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/uniqueness.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_uniqueness.py
git commit -m "feat: add v15.30 uniqueness and countermodel gate"
```

Expected cumulative count: 21 tests.

---

## Task 6: Gate E and Mechanical Adjudication

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/definability_gate.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_gate.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class CandidateAudit:
    key: str
    gate_a_common_carrier: bool
    gate_b_exact_fiber: bool | None
    gate_c_natural: bool | None
    gate_d_unique: bool | None
    gate_e_no_choice: bool | None
    relation_signatures: tuple[tuple[int, ...], ...]
    stop_reason: str

@dataclass(frozen=True)
class DefinabilityAudit:
    status: str
    candidates: tuple[CandidateAudit, ...]
    countermodels_survive: bool
    canonical_relation_certified: bool

audit_candidate(candidate) -> CandidateAudit
audit_real_archive() -> DefinabilityAudit
audit_synthetic_controls() -> tuple[DefinabilityAudit, ...]
adjudicate(results: tuple[CandidateAudit, ...]) -> str
```

- [ ] **Step 1: Write the failing tests**

```python
import unittest
import definability_gate as gate

ALLOWED = {
    'NO_TYPED_COMMON_CARRIER',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}


class GateTests(unittest.TestCase):
    def test_real_status_is_preregistered_and_candidate_count_is_four(self):
        result = gate.audit_real_archive()
        self.assertIn(result.status, ALLOWED)
        self.assertEqual(len(result.candidates), 4)

    def test_no_common_carrier_has_highest_precedence(self):
        result = gate.synthetic_no_common_carrier_control()
        self.assertEqual(result.status, 'NO_TYPED_COMMON_CARRIER')

    def test_global_multiple_relations_outrank_positive_candidate(self):
        result = gate.synthetic_cross_candidate_multiple_control()
        self.assertEqual(result.status, 'MULTIPLE_NATURAL_RELATIONS_REMAIN')

    def test_unique_synthetic_control_can_reach_positive_status(self):
        result = gate.synthetic_unique_natural_control()
        self.assertEqual(result.status, 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')
        self.assertTrue(result.canonical_relation_certified)

    def test_supplied_embedding_control_never_certifies_real_relation(self):
        result = gate.synthetic_supplied_embedding_control()
        self.assertNotEqual(result.status, 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run RED**

Expected: missing `definability_gate.py`.

- [ ] **Step 3: Implement strict per-candidate gate order**

Execute A → B → C → D → E. When a gate fails, all later gates for that candidate are `None`, and the stop reason names the first failed gate.

Gate E passes only when the surviving relation dependency path contains no supplied embedding, fitted selector, arbitrary basis map, preferred representative, new semantic declaration, or downstream score.

- [ ] **Step 4: Implement global precedence correctly**

The multiplicity decision is global, not merely per candidate:

```python
def adjudicate(results):
    typed = [r for r in results if r.gate_a_common_carrier]
    if not typed:
        return 'NO_TYPED_COMMON_CARRIER'

    natural = [r for r in typed if r.gate_b_exact_fiber and r.gate_c_natural]
    if not natural:
        return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'

    signatures = {
        sig
        for result in natural
        for sig in result.relation_signatures
    }
    if len(signatures) >= 2:
        return 'MULTIPLE_NATURAL_RELATIONS_REMAIN'

    if any(result.gate_d_unique is False for result in natural):
        return 'MULTIPLE_NATURAL_RELATIONS_REMAIN'

    positive = [
        result for result in natural
        if result.gate_d_unique is True and result.gate_e_no_choice is True
    ]
    if len(signatures) == 1 and positive:
        return 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'

    return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'
```

This handles two different candidate origins selecting inequivalent natural relations.

- [ ] **Step 5: Implement the six required synthetic controls**

The controls are: common-word null; supplied embedding; q-collapsed relation; explicit distinguishing relation; automorphism rejection; unique-natural positive. `synthetic_cross_candidate_multiple_control()` additionally combines two individually natural but inequivalent candidate relations to test global multiplicity.

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest -v test_gate.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/definability_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_gate.py
git commit -m "feat: add v15.30 definability adjudicator"
```

Expected cumulative count: 26 tests.

---

## Task 7: Deterministic Ledger and Claim Boundary

**Files:**
- Modify `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/definability_gate.py`
- Modify `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_gate.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/RESULTS.json`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/README.md`

**Interfaces:**

```python
audit() -> dict
write_audit(out_dir: Path) -> Path
```

The public ledger keys are exactly:

```python
REQUIRED = {
    'version', 'base_sha', 'status', 'candidate_count', 'candidate_results',
    'common_carrier_count', 'exact_fiber_relation_count', 'natural_relation_count',
    'countermodels_survive', 'canonical_relation_certified',
    'new_source_semantics_axiom_added', 'coupling_solver_reopened',
    'gravity_observables_evaluated', 'uses_holonomy_selector', 'uses_newton_or_gr',
    'uses_metric_selector', 'uses_pruning_as_selector', 'uses_entropy_as_selector',
    'uses_physical_time', 'scientific_breakthrough', 'signal_of_life',
    'gravity_canary_certified', 'physical_gravity_derived', 'Pillar_3',
    'next_required_object',
}
```

- [ ] **Step 1: Replace one Task-6 test with a ledger-schema test so `test_gate.py` remains five tests total**

The schema test requires `set(gate.audit()) == REQUIRED`, all firewall flags false, and:

```python
self.assertEqual(result['Pillar_3'], 'OPEN')
self.assertEqual(result['scientific_breakthrough'],
                 result['status'] == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')
```

- [ ] **Step 2: Implement deterministic next-object mapping**

```python
NEXT = {
    'NO_TYPED_COMMON_CARRIER':
        'GENUINELY_TYPED_COMMON_CARRIER_OR_EXPLICIT_NEW_AXIOM',
    'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE':
        'LOCALIZED_SYMMETRY_OR_DEFINABILITY_OBSTRUCTION',
    'MULTIPLE_NATURAL_RELATIONS_REMAIN':
        'ADDITIONAL_PRIMITIVE_SELECTING_AMONG_NATURAL_RELATIONS',
    'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED':
        'SEPARATE_PROVENANCE_ACTION_REPRESENTATION_READINESS_GATE',
}
```

`base_sha` is exactly `6535ea69214f6661e340fe201813dfd17ddbb7e1`. `candidate_count` is exactly 4.

- [ ] **Step 3: Generate and freeze the actual result**

```bash
python definability_gate.py --out outputs
cp outputs/verification.json docs/RESULTS.json
python definability_gate.py --out /tmp/v1530_out
cmp docs/RESULTS.json /tmp/v1530_out/verification.json
```

README wording is written from the generated result, not before it. It must state that no v15.30 result chooses a coupling member or certifies gravity.

- [ ] **Step 4: Run the complete non-presentation unit surface**

```bash
python -m unittest -v \
  test_frozen_inputs.py test_common_carrier.py test_exact_fiber.py \
  test_naturality.py test_uniqueness.py test_gate.py
```

Expected: exactly 26 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/definability_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_gate.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/RESULTS.json \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/README.md
git commit -m "feat: freeze v15.30 definability adjudication"
```

---

## Task 8: Gravity-Blind Offline Inspector and Replay

**Files:**
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/replay.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/viewer.html`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_replay.py`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/requirements.txt`
- Create `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/.gitignore`

**Interfaces:**

```python
payload() -> dict
write_html(data: dict, path: Path) -> None
movie(path: Path, fps: int = 10) -> None
```

- [ ] **Step 1: Write the failing tests**

```python
import json
import tempfile
import unittest
from pathlib import Path
import replay


class ReplayTests(unittest.TestCase):
    def test_payload_has_candidates_graph_fiber_and_audit(self):
        data = replay.payload()
        self.assertEqual(data['version'], 'v15.30')
        self.assertEqual(len(data['candidates']), 4)
        self.assertIn('typed_graph', data)
        self.assertIn('fibers', data)
        self.assertIn('audit', data)

    def test_payload_contains_no_gravity_or_coupling_scores(self):
        text = json.dumps(replay.payload()).lower()
        for forbidden in ('holonomy_score', 'newton_score', 'einstein_score',
                          'inverse_square_score', 'preferred_coupling'):
            self.assertNotIn(forbidden, text)

    def test_html_is_self_contained_and_declares_nonphysical_playback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'index.html'
            replay.write_html(replay.payload(), path)
            text = path.read_text()
            self.assertIn('Playback is not physical time', text)
            self.assertIn('No coupling member or gravity observable is evaluated', text)
            self.assertNotIn('<script src=', text)
            self.assertNotIn('fetch(', text)

    def test_movie_guard_rejects_nonpositive_fps(self):
        with self.assertRaises(ValueError):
            replay.movie(Path('unused.mp4'), fps=0)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Implement exactly six scenes**

```text
1  FOUR FROZEN CANDIDATE ORIGINS
2  TYPED COMMON-CARRIER GRAPH / GATE A
3  ONE EXACT q-FIBER / MULTIPLE MICROSCOPIC REPRESENTATIVES
4  FROZEN-DATA AUTOMORPHISM / DEFINABILITY BOUNDARY
5  UNIQUENESS OR COUNTERMODEL ADJUDICATION
6  FINAL v15.30 STATUS / NEXT REQUIRED OBJECT
```

Every scene footer includes:

```text
Microscopic difference is not automatically provenance difference.
Playback is not physical time.
No coupling member or gravity observable is evaluated.
```

- [ ] **Step 3: Pin requirements and exclusions**

`requirements.txt`:

```text
numpy==2.3.5
matplotlib==3.10.8
```

`.gitignore`:

```text
__pycache__/
*.pyc
outputs/
evidence/ci/
```

- [ ] **Step 4: Run GREEN and media checks**

```bash
python -m unittest -v test_replay.py
python replay.py --out outputs --video
ffmpeg -v error -i outputs/provenance_fiber_definability.mp4 -f null -
ffprobe -v error -show_entries stream=codec_name,width,height -show_entries format=duration -of json outputs/provenance_fiber_definability.mp4
```

Require codec `h264`, width 1280, height 720, duration 24.0 seconds ±0.1 seconds.

- [ ] **Step 5: Run all v15.30 tests and commit**

```bash
python -m unittest -v \
  test_frozen_inputs.py test_common_carrier.py test_exact_fiber.py \
  test_naturality.py test_uniqueness.py test_gate.py test_replay.py
```

Expected: exactly 30 tests PASS.

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability
git commit -m "feat: add gravity-blind v15.30 definability replay"
```

---

## Task 9: Exact-Head CI, 604-Test Regression, and Digest-Verified Delivery

**Files:**
- Create `.github/workflows/uqcf-v1530-provenance-fiber-definability.yml`
- Update the v15.30 draft PR only with certification evidence after success.

**Interfaces:**
- Delivery base: `6535ea69214f6661e340fe201813dfd17ddbb7e1`.
- Scientific source pin: `42244310b065f473c8bd459a6f065a61afbd2292`.
- Inherited selected tests: 574.
- v15.30 tests: 30.
- Required selected total: 604.

- [ ] **Step 1: Create additive-scope enforcement**

Only additions under these paths are allowed relative to the delivery base:

```text
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/
docs/superpowers/specs/2026-09-17-v1530-provenance-fiber-definability-common-carrier-design.md
docs/superpowers/plans/2026-09-17-v1530-provenance-fiber-definability-common-carrier-implementation.md
docs/superpowers/plans/2026-09-17-v1530-provenance-fiber-definability-common-carrier-review.md
.github/workflows/uqcf-v1530-provenance-fiber-definability.yml
```

The workflow must reject modifications or deletions outside these paths.

- [ ] **Step 2: Run the inherited selected suite exactly**

Use this v15.11–v15.27 table exactly:

```python
suites = [
 ('v15/v15.11', ['test_continuity.py'], 20),
 ('demos/v15.12-pretime-to-history', ['test_simulation.py','test_presentation.py'], 30),
 ('demos/v15.13-independent-events', ['test_model.py','test_replay.py'], 27),
 ('demos/v15.14-record-dependencies', ['test_adaptive.py','test_replay.py'], 30),
 ('demos/v15.15-coherent-records', ['test_coherent.py','test_replay.py'], 30),
 ('demos/v15.16-partial-pruning', ['test_recoverability.py','test_replay.py'], 33),
 ('demos/v15.17-retained-motion', ['test_motion.py','test_replay.py'], 32),
 ('demos/v15.18-invariant-completion', ['test_completion.py','test_replay.py'], 34),
 ('demos/v15.19-linear-prediction', ['test_linear.py','test_replay.py'], 36),
 ('demos/v15.20-physical-predictor', ['test_channel.py','test_replay.py'], 38),
 ('demos/v15.21-record-readout', ['test_record_readout.py','test_readout_presentation.py'], 32),
 ('demos/v15.22-event-sufficient-retention', ['test_event_sufficiency.py','test_sufficiency_presentation.py'], 32),
 ('demos/v15.23-sufficient-channel-family', ['test_family.py','test_family_view.py'], 32),
 ('demos/v15.24-composition-gate', ['test_composition.py','test_composition_view.py'], 30),
 ('demos/v15.25-pretime-gravity-canary', ['test_canary.py','test_replay.py'], 28),
 ('demos/v15.26-response-selector-rank', ['test_selector.py','test_replay.py'], 26),
 ('demos/v15.27-target-origin', ['test_origin.py','test_replay.py'], 27),
]
```

Require 517 tests from this table, 35 v15.28 tests, and 22 v15.29 tests = 574 inherited.

The v15.30 test files are exactly:

```python
new_files = [
 'test_frozen_inputs.py',
 'test_common_carrier.py',
 'test_exact_fiber.py',
 'test_naturality.py',
 'test_uniqueness.py',
 'test_gate.py',
 'test_replay.py',
]
```

Require exactly 30 new tests and 604 selected tests total.

- [ ] **Step 3: Regenerate and byte-check artifacts**

```bash
python frozen_inputs.py --out /tmp/CANDIDATE_EVIDENCE.json
cmp docs/CANDIDATE_EVIDENCE.json /tmp/CANDIDATE_EVIDENCE.json
python definability_gate.py --out outputs
cmp docs/RESULTS.json outputs/verification.json
python replay.py --out outputs --video
ffmpeg -v error -i outputs/provenance_fiber_definability.mp4 -f null -
```

- [ ] **Step 4: Assert the firewall after regeneration**

```python
assert r['status'] in {
 'NO_TYPED_COMMON_CARRIER',
 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
 'MULTIPLE_NATURAL_RELATIONS_REMAIN',
 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}
assert r['candidate_count'] == 4
assert r['new_source_semantics_axiom_added'] is False
assert r['coupling_solver_reopened'] is False
assert r['gravity_observables_evaluated'] is False
assert r['uses_holonomy_selector'] is False
assert r['uses_newton_or_gr'] is False
assert r['uses_metric_selector'] is False
assert r['uses_pruning_as_selector'] is False
assert r['uses_entropy_as_selector'] is False
assert r['uses_physical_time'] is False
assert r['signal_of_life'] is False
assert r['gravity_canary_certified'] is False
assert r['physical_gravity_derived'] is False
assert r['Pillar_3'] == 'OPEN'
```

- [ ] **Step 5: Package eight assets**

```text
provenance_fiber_definability.mp4
provenance_fiber_definability.html
verification.json
replay_data.json
REPORT.md
PROVENANCE.json
UQCF_GEM_v15_30_bundle.zip
SHA256SUMS.txt
```

The ZIP contains the complete v15.30 demo directory, fresh CI logs, the approved spec, this implementation plan, the plan self-review, and the workflow. Verify every ZIP member by size and SHA-256 before upload.

- [ ] **Step 6: Publish and verify remote bytes**

Use tag:

```text
uqcf-gem-v15.30-${GITHUB_RUN_ID}-a${GITHUB_RUN_ATTEMPT}
```

Create the release as draft, upload all eight assets, verify every remote size and `sha256:` digest, then publish. Download the published HTML/MP4, exercise all viewer selectors at widths 1280, 820, and 390 with zero JavaScript errors, zero external requests, and zero horizontal overflow, and fully decode the published MP4 again.

- [ ] **Step 7: Record the final PR receipt and stop**

The receipt contains source SHA, run ID, delivery base SHA, scientific source pin, `574 + 30 = 604` selected test count, actual v15.30 verdict, release URL, 8/8 digest verification, browser/video PASS, and the claim boundary.

The v15.30 PR remains open/draft/unmerged at certification. There are no post-certification scientific edits.

## Final Stop Rule

```text
NO_TYPED_COMMON_CARRIER
  -> stop archive derivation; do not invent a bridge.

PROVENANCE_FIBER_RELATION_NOT_DEFINABLE
  -> isolate the exact symmetry/definability obstruction; do not fit around it.

MULTIPLE_NATURAL_RELATIONS_REMAIN
  -> identify the minimal additional primitive required to choose among them; no coupling solve.

CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED
  -> open a separate provenance-action / representation-readiness gate only.
```

No v15.30 result itself may select one of v15.28's three q-only coupling controls or authorize a gravity canary.
