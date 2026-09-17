# UQCF-GEM v15.30 Provenance–Fiber Definability / Common-Carrier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Determine whether any already-frozen ontology-native object canonically defines a provenance relation on exact microscopic representatives inside one fixed `q = B1 x` fiber, without adding a source-semantics axiom or consulting downstream coupling/gravity criteria.

**Architecture:** v15.30 is a theorem-first typed-relation audit stacked on the certified v15.29 head. It reuses v15.29's exact q-fiber implementation by hash-pinned file-path import, extends the frozen evidence inventory with four candidate-origin artifact bundles, builds a certified carrier-relation graph, and evaluates common-carrier reachability, exact-fiber compatibility, naturality, uniqueness, and no-choice constraints. Synthetic controls exercise positive, collapsed, non-definable, multiple-natural, and unique-natural branches without promoting synthetic structures into frozen evidence.

**Tech Stack:** Python 3.13.5, standard-library `dataclasses`, `fractions`, `hashlib`, `importlib`, `json`, `unittest`; NumPy 2.3.5 and Matplotlib 3.10.8 only for inherited modules/replay; FFmpeg for optional H.264 delivery media; GitHub Actions for exact-head regression and digest-verified publication.

**Spec:** `docs/superpowers/specs/2026-09-17-v1530-provenance-fiber-definability-common-carrier-design.md`

## Global Constraints

- Stacked scientific base is exactly `6535ea69214f6661e340fe201813dfd17ddbb7e1`.
- Inherited v15.29 adjudication remains `PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED`.
- Scientific source pin inherited from v15.29 remains `42244310b065f473c8bd459a6f065a61afbd2292`.
- Candidate count is exactly four: Genesis/history lineage, minimal ternary source role, retained graph source/current, Genesis 6-D provenance carrier.
- No fifth real candidate may be added without reopening the design.
- `x` denotes the torus microscopic representative; retained graph source variables use `s_ret`.
- Exact q-fiber equalities are integer/rational statements; floating comparison must never decide same-fiber status.
- No holonomy, inverse-square, Newton, Einstein, ADM, metric/Hodge/minimum-action, entropy, pruning-performance, recoverability-performance, or physical-time quantity may select a relation.
- No PCA/SVD/alignment, learned embedding, dimension/cardinality match, name/label match, arbitrary representative, supplied intertwiner, or post-hoc lookup may certify a real relation.
- `new_source_semantics_axiom_added`, `coupling_solver_reopened`, `gravity_observables_evaluated`, `signal_of_life`, `gravity_canary_certified`, and `physical_gravity_derived` remain `false` in every v15.30 real outcome.
- No v15.30 outcome directly authorizes a coupling or gravity gate.
- Real statuses are exactly: `NO_TYPED_COMMON_CARRIER`, `PROVENANCE_FIBER_RELATION_NOT_DEFINABLE`, `MULTIPLE_NATURAL_RELATIONS_REMAIN`, `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED`.
- `scientific_breakthrough` may be true only for `CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED`.

---

## File Structure

Create one focused v15.30 demo directory:

```text
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/
  .gitignore
  README.md
  requirements.txt
  frozen_inputs.py
  typed_carrier_graph.py
  exact_fiber.py
  naturality.py
  uniqueness.py
  definability_gate.py
  replay.py
  viewer.html
  test_frozen_inputs.py
  test_common_carrier.py
  test_exact_fiber.py
  test_naturality.py
  test_uniqueness.py
  test_gate.py
  test_replay.py
  docs/
    CANDIDATE_EVIDENCE.json
    RESULTS.json
```

Responsibilities:

- `frozen_inputs.py`: hash-pinned inherited v15.29 loaders plus the exact four candidate artifact bundles.
- `typed_carrier_graph.py`: typed relation records, certified-edge filtering, path/common-parent search, Gate A.
- `exact_fiber.py`: inherited exact q-fiber fixtures and Gate B evaluation helpers only.
- `naturality.py`: finite exact invariance/equivariance checks and Gate C controls.
- `uniqueness.py`: relation signatures, pairwise inequivalence, uniqueness/countermodel logic for Gate D.
- `definability_gate.py`: Gate E, mechanical precedence, real audit, synthetic controls, deterministic ledger.
- `replay.py` / `viewer.html`: gravity-blind presentation of candidate → typed graph → q-fiber → naturality → uniqueness → final status.

The v15.30 implementation must not modify any v15.29 scientific file.

---

### Task 1: Freeze Inherited Interfaces and the Four Candidate Artifact Bundles

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/frozen_inputs.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_frozen_inputs.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/CANDIDATE_EVIDENCE.json`

**Interfaces:**
- Produces `FrozenModules`, `CandidateEvidence`, `load_v1529()`, `candidate_inventory()`, `candidate_by_key()`, `inventory_payload()`, `inventory_digest()`, `write_candidate_inventory()`.
- Later tasks consume candidate `domain`, `evidence_keys`, `artifact_pins`, `transformation_source`, and `claim_boundary` exactly as emitted here.

Exact inherited pins:

```text
v15.29/provenance_inventory.py  81a41442d2f3b26817657ebb5f3dc948e62d14b2
v15.29/fiber_model.py           e04cf0b24bbce6f908b83c9472c1f1b5639b7e8b
v15.29/source_extension_gate.py 305af411792c08906ea8eed2c9aeba3de25be1cf
v15.29/docs/RESULTS.json        0984a8238a7fd2a115ab673a3d4f23b0706c7b12
```

Exact additional artifact pins:

```text
V997 report                       8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e
V923 report                       9a1523c08d2b9b2c5ba2d298dfed3d563a750bec
V923 proof script                 90f69d5101e0ab14488d8d25da326e7b94341375
v13.26 report                     9917085b211ca0e1f4737082227f55097cc72b66
v14.04 report                     e5d9566bfc86c801d2933e63453d1800f60a675b
v14.04 provenance audit           1e75767a59a54b4fb7840ca355eb00845cf119e3
v15.01 report                     1afbb7aebe384a1fb761f99fd2b040e595be1fa5
v15.01 common-parent audit        b8b6ef14b323659eb730b33bd3d36c99e7f03957
V1172 Genesis/6-D engine          78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d
```

- [ ] **Step 1: Write four RED tests**

```python
class FrozenInputTests(unittest.TestCase):
    def test_v1529_result_pin_and_stop_object(self):
        mods = fi.load_v1529()
        ledger = mods.v1529_results
        self.assertEqual(ledger['status'], 'PROVENANCE_RELATION_TO_Q_FIBERS_NOT_ENTAILED')
        self.assertEqual(ledger['next_required_object'], 'INDEPENDENTLY_MOTIVATED_PROVENANCE_FIBER_RELATION')

    def test_inherited_module_blobs_are_exact(self):
        fi.load_v1529()  # must fail closed on any blob drift

    def test_exact_four_candidate_origins(self):
        rows = fi.candidate_inventory(fi.REPO_ROOT)
        self.assertEqual(tuple(r.key for r in rows), (
            'genesis-history-lineage', 'genesis-6d-carrier',
            'retained-source-current', 'ternary-source-role'))

    def test_candidate_artifact_pins_are_exact(self):
        for row in fi.candidate_inventory(fi.REPO_ROOT):
            fi.verify_candidate(row, fi.REPO_ROOT)
```

- [ ] **Step 2: Run RED**

Run:

```bash
cd ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability
python -m unittest -v test_frozen_inputs.py
```

Expected: `ModuleNotFoundError: No module named 'frozen_inputs'`.

- [ ] **Step 3: Implement the frozen loader and evidence dataclass**

Core type:

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
```

Use `git_blob_sha(raw)` with Git's `blob <len>\0` prefix, verify every path before loading it, and import v15.29 modules by exact file path under private module names. `load_v1529()` must also parse the pinned v15.29 `RESULTS.json` and reject a status/base mismatch.

The four real candidate records are fixed:

```python
GENESIS_HISTORY = CandidateEvidence(
    key='genesis-history-lineage',
    domain='HISTORY_PROVENANCE',
    evidence_keys=('v997-genesis-pin',),
    artifact_pins=(
      ('Tmp/TOE/Einstein 4/V997_FULL_STACK_GENESIS_PIN_BRIDGE_REPORT.md', '8f4ee48cbaf6c822b87dd5e30a5dfee4d596e26e'),
      ('Tmp/TOE/Einstein 6/v1172_full_stack_package/v1172_6d_gpu_full_stack_genesis_provenance_engine.py', '78d57450ac6a2b7fe3ab4ad42cf2f707c3e61f8d'),
    ),
    transformation_source='V997/V1172 ordered-lineage and append-only provenance certification',
    certified_relation_claims=('PINNED_REGISTRY','GENESIS_ROOT','WITNESS_QUORUM','APPEND_ONLY_CONTINUITY'),
    claim_boundary='history legitimacy is not microscopic torus incidence',
)
```

Create analogous fixed records for `ternary-source-role`, `retained-source-current`, and `genesis-6d-carrier`, using the pins above.

- [ ] **Step 4: Serialize and byte-check the inventory**

```bash
python frozen_inputs.py --out docs/CANDIDATE_EVIDENCE.json
python -m unittest -v test_frozen_inputs.py
python frozen_inputs.py --out /tmp/v1530_candidate_evidence.json
cmp docs/CANDIDATE_EVIDENCE.json /tmp/v1530_candidate_evidence.json
```

Expected: 4 tests PASS and byte comparison succeeds.

- [ ] **Step 5: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/frozen_inputs.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/test_frozen_inputs.py \
        ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/docs/CANDIDATE_EVIDENCE.json
git commit -m "feat: freeze v15.30 candidate evidence inventory"
```

---

### Task 2: Implement Gate A as a Certified Typed-Carrier Graph

**Files:**
- Create: `.../typed_carrier_graph.py`
- Create: `.../test_common_carrier.py`

**Interfaces:**
- Consumes `CandidateEvidence` and inherited v15.29 `EvidenceRecord` rows.
- Produces `TypedEdge`, `CarrierConnection`, `build_real_graph()`, `find_typed_connection()`, `audit_candidate_common_carrier()`.

Only these relation classes create real graph edges:

```text
CERTIFIED_PROVENANCE_RELATION
CERTIFIED_GAUGE_OR_EQUIVALENCE
CERTIFIED_PROJECTION_TO_Q
CERTIFIED_ACTION  (only when the record explicitly certifies the typed source/target relation)
```

`ARCHIVE_EVIDENCE_ONLY`, `NO_TYPED_RELATION`, and `CONDITIONAL_ON_SUPPLIED_MAP` never create real carrier edges.

The inherited exact q projection is registered explicitly as:

```python
TypedEdge(
    source='TORUS_EDGE_REPRESENTATIVE',
    target='Q_SOURCE_QUOTIENT',
    relation_class='CERTIFIED_PROJECTION_TO_Q',
    evidence_key='v15.29-fiber-model:B1',
    synthetic=False,
)
```

- [ ] **Step 1: Write five RED tests**

```python
class CommonCarrierTests(unittest.TestCase):
    def test_common_words_create_no_edge(self):
        g = tc.CarrierGraph()
        g.add_untyped_note('source provenance site origin')
        self.assertFalse(g.has_certified_path('A', 'B'))

    def test_supplied_embedding_is_not_real_evidence(self):
        g = tc.synthetic_supplied_embedding_graph()
        r = tc.find_typed_connection(g, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE')
        self.assertFalse(r.real_certified)

    def test_synthetic_common_parent_is_detected(self):
        g = tc.synthetic_common_parent_graph()
        r = tc.find_typed_connection(g, 'SYNTHETIC_PROVENANCE', 'TORUS_EDGE_REPRESENTATIVE')
        self.assertTrue(r.common_parent_certified)

    def test_real_graph_has_exactly_four_candidate_roots(self):
        graph, candidates = tc.build_real_graph()
        self.assertEqual(len(candidates), 4)

    def test_untyped_relation_classes_never_promote(self):
        self.assertFalse(tc.relation_class_is_certifying('NO_TYPED_RELATION'))
        self.assertFalse(tc.relation_class_is_certifying('ARCHIVE_EVIDENCE_ONLY'))
        self.assertFalse(tc.relation_class_is_certifying('CONDITIONAL_ON_SUPPLIED_MAP'))
```

- [ ] **Step 2: Run RED**

Expected: missing `typed_carrier_graph`.

- [ ] **Step 3: Implement certified graph search**

Core types:

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
    common_parent: str | None
    common_parent_paths: tuple[tuple[TypedEdge, ...], tuple[TypedEdge, ...]] | None
    real_certified: bool
    common_parent_certified: bool
    reason: str
```

`find_typed_connection()` must search:

1. certified path candidate → torus;
2. certified path torus → candidate;
3. certified common parent `K` with `K → candidate` and `K → torus` paths;
4. certified common quotient `K` with candidate → `K` and torus → `K` paths.

Every returned path must reject any synthetic or non-certifying edge when `real_only=True`.

- [ ] **Step 4: Add the real candidate audit**

```python
def audit_candidate_common_carrier(candidate, graph):
    connection = find_typed_connection(
        graph, candidate.domain, 'TORUS_EDGE_REPRESENTATIVE', real_only=True)
    return {
        'candidate': candidate.key,
        'typed_common_carrier': connection.real_certified,
        'connection': asdict(connection),
    }
```

Do not hard-code the final v15.30 status here. Task 6 adjudicates after all gates.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest -v test_frozen_inputs.py test_common_carrier.py
git add .../typed_carrier_graph.py .../test_common_carrier.py
git commit -m "feat: add v15.30 typed common-carrier gate"
```

Expected cumulative test count: 9.

---

### Task 3: Reuse v15.29 Exact q-Fibers for Gate B

**Files:**
- Create: `.../exact_fiber.py`
- Create: `.../test_exact_fiber.py`

**Interfaces:**
- Consumes the pinned v15.29 `fiber_model` only through `frozen_inputs.load_v1529()`.
- Produces `FiberCase`, `canonical_fiber_cases()`, `same_q_exact()`, `evaluate_labeling_on_fiber()`.

- [ ] **Step 1: Write four RED tests**

```python
class ExactFiberTests(unittest.TestCase):
    def test_face_shift_is_distinct_and_same_q(self): ...
    def test_cycle_shift_is_distinct_and_same_q(self): ...
    def test_noncycle_shift_changes_q(self): ...
    def test_q_only_label_collapses_entire_fiber(self): ...
```

The fourth test uses a synthetic `label_fn=lambda rep: rep.q` and requires all canonical cases to receive the same label.

- [ ] **Step 2: Run RED**

Expected: missing `exact_fiber`.

- [ ] **Step 3: Implement exact fixtures**

```python
@dataclass(frozen=True)
class FiberCase:
    key: str
    edge_vector: tuple[int, ...]
    q: tuple[int, ...]


def canonical_fiber_cases():
    fm = fi.load_v1529().fiber_model
    root = fm.root_fixture()
    face = fm.face_shift(root, 0, 1)
    cycle = fm.cycle_shift(root, fm.canonical_cycle_basis()[7])
    return tuple(FiberCase(k, r.edge_vector, r.q) for k, r in (
        ('root', root), ('face-boundary-shift', face), ('cycle-shift', cycle)))
```

Never recompute the torus incidence matrices independently in v15.30.

- [ ] **Step 4: Run GREEN and commit**

Expected cumulative test count: 13.

---

### Task 4: Implement Gate C Naturality / Automorphism Tests

**Files:**
- Create: `.../naturality.py`
- Create: `.../test_naturality.py`

**Interfaces:**
- Produces `FiniteRelation`, `FiniteAction`, `NaturalityResult`, `check_equivariance()`, `audit_relation_naturality()`.
- A real relation can pass only if its action/transformation law is supplied by pinned evidence, not generated by v15.30 for convenience.

- [ ] **Step 1: Write four RED tests**

```python
class NaturalityTests(unittest.TestCase):
    def test_swap_preserving_reduct_rejects_noninvariant_relation(self): ...
    def test_equivariant_synthetic_relation_passes(self): ...
    def test_missing_certified_action_fails_closed(self): ...
    def test_group_law_checked_exactly_for_finite_control(self): ...
```

- [ ] **Step 2: Run RED**

- [ ] **Step 3: Implement exact finite action model**

```python
@dataclass(frozen=True)
class FiniteAction:
    elements: tuple[str, ...]
    rep_permutations: dict[str, tuple[int, ...]]
    label_permutations: dict[str, tuple[int, ...]]
    multiplication: dict[tuple[str, str], str]

@dataclass(frozen=True)
class FiniteRelation:
    rep_keys: tuple[str, ...]
    labels: tuple[str, ...]
```

`check_equivariance()` must test every finite group element and every representative, plus every multiplication-table pair. No sampling.

- [ ] **Step 4: Implement fail-closed real wrapper**

```python
def audit_relation_naturality(relation, certified_action):
    if certified_action is None:
        return NaturalityResult(False, 'NO_CERTIFIED_ACTION_FOR_DEFINABILITY', ...)
    return check_equivariance(relation, certified_action)
```

- [ ] **Step 5: Run GREEN and commit**

Expected cumulative test count: 17.

---

### Task 5: Implement Gate D Uniqueness / Countermodel Classification

**Files:**
- Create: `.../uniqueness.py`
- Create: `.../test_uniqueness.py`

**Interfaces:**
- Produces `canonical_partition_signature()`, `relations_inequivalent()`, `UniquenessResult`, `classify_relation_family()`, synthetic unique/multiple controls.

- [ ] **Step 1: Write four RED tests**

```python
class UniquenessTests(unittest.TestCase):
    def test_label_renaming_does_not_create_new_relation(self): ...
    def test_two_distinct_partitions_prove_nonuniqueness(self): ...
    def test_single_survivor_is_unique(self): ...
    def test_empty_family_cannot_certify_uniqueness(self): ...
```

- [ ] **Step 2: Run RED**

- [ ] **Step 3: Implement canonical equivalence signature**

For labels `(A, A, B)`, canonicalize to `(0, 0, 1)`; `(X, X, Y)` must yield the same signature. Pairwise inequality of canonical signatures is the exact nonuniqueness witness.

```python
def canonical_partition_signature(labels):
    ids, next_id, out = {}, 0, []
    for label in labels:
        if label not in ids:
            ids[label] = next_id
            next_id += 1
        out.append(ids[label])
    return tuple(out)
```

`classify_relation_family()` returns exactly one of `NONE`, `UNIQUE`, `MULTIPLE` and carries two explicit witness signatures when `MULTIPLE`.

- [ ] **Step 4: Run GREEN and commit**

Expected cumulative test count: 21.

---

### Task 6: Implement Gate E and the Mechanical v15.30 Adjudicator

**Files:**
- Create: `.../definability_gate.py`
- Create: `.../test_gate.py`

**Interfaces:**
- Produces `CandidateAudit`, `DefinabilityAudit`, `audit_candidate()`, `audit_real_archive()`, `audit_synthetic_controls()`, `adjudicate()`.
- Task 7 extends this file with deterministic ledger serialization but does not change adjudication semantics.

- [ ] **Step 1: Write five RED tests**

```python
ALLOWED = {
 'NO_TYPED_COMMON_CARRIER',
 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE',
 'MULTIPLE_NATURAL_RELATIONS_REMAIN',
 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED',
}

class GateTests(unittest.TestCase):
    def test_real_status_is_preregistered_and_candidate_count_is_four(self): ...
    def test_no_common_carrier_has_highest_precedence(self): ...
    def test_multiple_natural_relations_outrank_positive_candidate(self): ...
    def test_unique_synthetic_control_can_reach_positive_status(self): ...
    def test_supplied_embedding_control_never_certifies_real_relation(self): ...
```

- [ ] **Step 2: Run RED**

- [ ] **Step 3: Implement per-candidate pipeline**

`audit_candidate()` executes strictly:

```text
A typed common-carrier
B exact q-fiber compatibility
C naturality/definability
D uniqueness/countermodels
E no-choice dependency audit
```

If a gate fails, later gates for that candidate are marked `NOT_REACHED`, never silently treated as pass.

Core result:

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
```

- [ ] **Step 4: Implement mechanical precedence**

```python
def adjudicate(results):
    typed = [r for r in results if r.gate_a_common_carrier]
    if not typed:
        return 'NO_TYPED_COMMON_CARRIER'
    natural = [r for r in typed if r.gate_b_exact_fiber and r.gate_c_natural]
    if not natural:
        return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'
    if any(r.gate_d_unique is False for r in natural):
        return 'MULTIPLE_NATURAL_RELATIONS_REMAIN'
    positive = [r for r in natural if r.gate_d_unique and r.gate_e_no_choice]
    if len(positive) == 1:
        return 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED'
    return 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE'
```

Do not assert which real outcome will occur before the audit runs.

- [ ] **Step 5: Implement all six required synthetic controls**

Controls must cover: common-word null, supplied embedding, q-collapsed relation, explicit distinguishing relation, automorphism rejection, unique-natural positive control.

- [ ] **Step 6: Run GREEN and commit**

Expected cumulative v15.30 test count: 26.

---

### Task 7: Freeze the Deterministic Ledger and Human Claim Boundary

**Files:**
- Modify: `.../definability_gate.py`
- Modify: `.../test_gate.py`
- Create: `.../docs/RESULTS.json`
- Create: `.../README.md`

**Interfaces:**
- Adds `audit() -> dict`, `write_audit(out_dir: Path) -> Path`, CLI `--out`.
- `replay.py` and CI consume only the serialized public audit contract, not internal candidate objects.

- [ ] **Step 1: Extend `test_gate.py` to five total tests, replacing overlap rather than increasing count**

The final five tests must include schema/boundary assertions:

```python
REQUIRED = {
 'version','base_sha','status','candidate_count','candidate_results',
 'common_carrier_count','exact_fiber_relation_count','natural_relation_count',
 'countermodels_survive','canonical_relation_certified',
 'new_source_semantics_axiom_added','coupling_solver_reopened',
 'gravity_observables_evaluated','uses_holonomy_selector','uses_newton_or_gr',
 'uses_metric_selector','uses_pruning_as_selector','uses_entropy_as_selector',
 'uses_physical_time','scientific_breakthrough','signal_of_life',
 'gravity_canary_certified','physical_gravity_derived','Pillar_3','next_required_object'
}
```

Require every firewall flag false and `Pillar_3 == 'OPEN'`. Require `scientific_breakthrough == (status == 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED')`.

- [ ] **Step 2: Implement deterministic ledger**

`base_sha` must be `6535ea69214f6661e340fe201813dfd17ddbb7e1`.

Use exact next-object mapping:

```python
NEXT = {
 'NO_TYPED_COMMON_CARRIER': 'GENUINELY_TYPED_COMMON_CARRIER_OR_EXPLICIT_NEW_AXIOM',
 'PROVENANCE_FIBER_RELATION_NOT_DEFINABLE': 'LOCALIZED_SYMMETRY_OR_DEFINABILITY_OBSTRUCTION',
 'MULTIPLE_NATURAL_RELATIONS_REMAIN': 'ADDITIONAL_PRIMITIVE_SELECTING_AMONG_NATURAL_RELATIONS',
 'CANONICAL_PROVENANCE_FIBER_RELATION_CERTIFIED': 'SEPARATE_PROVENANCE_ACTION_REPRESENTATION_READINESS_GATE',
}
```

- [ ] **Step 3: Generate the result, then commit exactly what the executable produces**

```bash
python definability_gate.py --out outputs
cp outputs/verification.json docs/RESULTS.json
python definability_gate.py --out /tmp/v1530_out
cmp docs/RESULTS.json /tmp/v1530_out/verification.json
```

The README must state the actual result after execution and distinguish theorem/proof controls from interpretation. Do not write the result in advance.

- [ ] **Step 4: Run the full current v15.30 unit surface**

```bash
python -m unittest -v \
  test_frozen_inputs.py test_common_carrier.py test_exact_fiber.py \
  test_naturality.py test_uniqueness.py test_gate.py
```

Expected: 26 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .../definability_gate.py .../test_gate.py .../docs/RESULTS.json .../README.md
git commit -m "feat: freeze v15.30 definability adjudication"
```

---

### Task 8: Build the Gravity-Blind Offline Inspector and 24-Second Replay

**Files:**
- Create: `.../replay.py`
- Create: `.../viewer.html`
- Create: `.../test_replay.py`
- Create: `.../requirements.txt`
- Create: `.../.gitignore`

**Interfaces:**
- `payload()` consumes `definability_gate.audit()` plus candidate/common-carrier summaries and exact q-fiber examples.
- `write_html()` embeds JSON and makes no network requests.
- `movie()` displays only definability/common-carrier state, never coupling/gravity scores.

- [ ] **Step 1: Write four RED tests**

```python
class ReplayTests(unittest.TestCase):
    def test_payload_has_candidates_graph_fiber_and_audit(self): ...
    def test_payload_contains_no_gravity_or_coupling_scores(self): ...
    def test_html_is_self_contained_and_declares_nonphysical_playback(self): ...
    def test_movie_guard_rejects_nonpositive_fps(self): ...
```

Forbidden payload tokens include:

```text
holonomy_score
newton_score
einstein_score
inverse_square_score
preferred_coupling
```

- [ ] **Step 2: Implement exactly six scenes**

```text
1  four frozen candidate origins
2  certified typed-carrier graph / Gate A
3  one exact q-fiber with multiple microscopic representatives
4  frozen-data automorphism / definability boundary
5  uniqueness or countermodel adjudication
6  final v15.30 status and next required object
```

Footer on every scene:

```text
Microscopic difference is not automatically provenance difference.
Playback is not physical time.
No coupling member or gravity observable is evaluated.
```

- [ ] **Step 3: Pin requirements and generated-artifact exclusions**

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

- [ ] **Step 4: Run GREEN and media verification**

```bash
python -m unittest -v test_replay.py
python replay.py --out outputs --video
ffmpeg -v error -i outputs/provenance_fiber_definability.mp4 -f null -
ffprobe -v error -show_entries stream=codec_name,width,height -show_entries format=duration -of json outputs/provenance_fiber_definability.mp4
```

Require H.264, 1280×720, 24.0 seconds ±0.1 s.

- [ ] **Step 5: Run all v15.30 tests and commit**

Expected exact new-test count: **30**.

```bash
python -m unittest -v test_frozen_inputs.py test_common_carrier.py test_exact_fiber.py \
  test_naturality.py test_uniqueness.py test_gate.py test_replay.py
git add ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability
git commit -m "feat: add gravity-blind v15.30 definability replay"
```

---

### Task 9: Exact-Head CI, 604-Test Regression, and Digest-Verified Delivery

**Files:**
- Create: `.github/workflows/uqcf-v1530-provenance-fiber-definability.yml`
- Update only the v15.30 draft PR with evidence after exact-head success.

**Interfaces:**
- Delivery base: exact v15.29 branch head `6535ea69214f6661e340fe201813dfd17ddbb7e1`.
- Scientific source pin remains `42244310b065f473c8bd459a6f065a61afbd2292` and must be present through the archive reference created during v15.29 certification.
- Inherited selected tests: 574.
- v15.30 tests: 30.
- Required selected total: **604**.

- [ ] **Step 1: Create additive-scope exact-head workflow**

The diff from the delivery base may contain additions only under:

```text
ResearchHistory/UQCF-GEM/demos/v15.30-provenance-fiber-definability/
docs/superpowers/specs/2026-09-17-v1530-provenance-fiber-definability-common-carrier-design.md
docs/superpowers/plans/2026-09-17-v1530-provenance-fiber-definability-common-carrier.md
docs/superpowers/plans/2026-09-17-v1530-provenance-fiber-definability-common-carrier-review.md
.github/workflows/uqcf-v1530-provenance-fiber-definability.yml
```

Any modification/deletion outside those paths fails certification.

- [ ] **Step 2: Replay inherited selected regressions unchanged**

Copy the exact v15.29 inherited suite list and require:

```text
v15.11–v15.28 selected = 552
v15.29 selected        = 22
inherited total        = 574
```

Then run the seven v15.30 test files and require exactly 30 tests, total 604.

- [ ] **Step 3: Reproduce deterministic artifacts**

```bash
python frozen_inputs.py --out /tmp/CANDIDATE_EVIDENCE.json
cmp docs/CANDIDATE_EVIDENCE.json /tmp/CANDIDATE_EVIDENCE.json
python definability_gate.py --out outputs
cmp docs/RESULTS.json outputs/verification.json
python replay.py --out outputs --video
```

Decode and probe MP4 again.

- [ ] **Step 4: Assert the scientific firewall after regeneration**

Regardless of the real status:

```python
assert r['status'] in ALLOWED
assert r['candidate_count'] == 4
assert r['new_source_semantics_axiom_added'] is False
assert r['coupling_solver_reopened'] is False
assert r['gravity_observables_evaluated'] is False
assert r['signal_of_life'] is False
assert r['gravity_canary_certified'] is False
assert r['physical_gravity_derived'] is False
assert r['Pillar_3'] == 'OPEN'
assert not any(r[k] for k in (
  'uses_holonomy_selector','uses_newton_or_gr','uses_metric_selector',
  'uses_pruning_as_selector','uses_entropy_as_selector','uses_physical_time'))
```

- [ ] **Step 5: Package eight verified release assets**

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

The ZIP includes the complete v15.30 demo folder, fresh CI logs, approved spec, plan, plan self-review, and workflow. Verify every ZIP member by size and SHA-256 before publication.

- [ ] **Step 6: Publish uniquely and verify remote bytes**

Tag:

```text
uqcf-gem-v15.30-${GITHUB_RUN_ID}-a${GITHUB_RUN_ATTEMPT}
```

Create draft → upload 8 assets → verify remote size and `sha256:` digest → publish. Then download published HTML/MP4, exercise all viewer selectors at widths 1280/820/390 with zero JS errors, external requests, and horizontal overflow; fully decode published MP4 again.

- [ ] **Step 7: Record final PR receipt without merging**

The receipt must include:

```text
source SHA
run ID
v15.29 delivery base SHA
scientific source pin
574 inherited + 30 v15.30 = 604 selected tests
actual v15.30 verdict
release URL
8/8 asset digest verification
browser/video PASS
claim boundary
```

The v15.30 PR remains open/draft/unmerged at certification, matching the stacked research workflow. No post-certification scientific edits are allowed.

---

## Final Stop Rule

After v15.30 certification:

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

No v15.30 result itself may choose one of v15.28's three q-only coupling controls or authorize a gravity canary.
