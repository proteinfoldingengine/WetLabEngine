# v15.40 Global-Balance Geometry Specificity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and certify the preregistered v15.40 blind exact test of whether the v15.39 global-balance response recovers the independently queried `B2` face geometry more specifically than historical local and matched covariant Green-operator controls.

**Architecture:** Add four focused modules: an exact response-generation layer that alone may use inherited operators, a blind response-geometry constructor, an incidence-support-only target constructor, and a mechanical adjudicator/orchestrator. The two constructors expose immutable exact outputs through narrow signatures; only the adjudicator compares them. A behavior-first unittest suite, deterministic JSON ledger, explanatory README, and branch-specific GitHub workflow certify separation, exhaustive finite checks, inherited regressions, and byte-identical replay.

**Tech Stack:** Python 3.13.5, standard-library `dataclasses`, `fractions.Fraction`, `collections.deque`, `itertools`, `json`, `unittest`, NumPy 2.3.5 only through hash-pinned inherited complex construction, GitHub Actions on `ubuntu-24.04`.

**Spec:** `docs/superpowers/specs/2026-09-19-v1540-global-balance-geometry-specificity-design.md`

## Global Constraints

- Base exactly on v15.39 certified head `0f3e10602929dd0a148b195f32406efa52082070`.
- Preserve the reviewed v15.40 design head `940e77adf346ad8defc01f94b3f6e7c39ff18880` and design blob `5f75f9a7ba1df5b21715f775d26bedbedc07297f`.
- Do not modify a v15.39 candidate formula, observable, result, ledger, or any earlier artifact.
- Use unchanged formulas at `L=5,7,9,11`; `L=11` is the locked holdout.
- Use exact rational arithmetic for every response, work value, comparison, solve, and scale check; no floating tolerance may adjudicate.
- The response-geometry constructor receives only labels, centered source vectors, response vectors, and exact rational arithmetic; it may not import or query inherited geometry/operator modules.
- The incidence-target constructor receives only the signed support matrix of `B2`; it may not import or query response or operator data.
- Only the adjudicator compares frozen constructor outputs, using exact set equality, booleans, integer graph distances, equality/order, and projective ratios.
- Use only the frozen controls `DIRECT_INHERITANCE`, `ONE_INCIDENCE_TRANSPORT`, `MATCHED_DIAGONAL_BALANCE`, and `MATCHED_STEP2_BALANCE`.
- Matched controls must pass connectedness, augmentation-sector invertibility, translation/D4 covariance, valence four, and the common protocol; historical controls may fail the metric protocol without invalidating the gate.
- Exhaust every source face, unordered pair, ordered triple, required source orientation, and the amplitudes `2/3`, `-5/7` and scales `1`, `7/3`.
- Apply the deterministic relabeling `pi(i)=(2*i+1) mod L**2` to labels, face-vector coordinates, and `B2` columns.
- Keep all eight construction-firewall counters exactly zero.
- Keep `physical_metric_derived=false`, `spacetime_derived=false`, `physical_gravity_derived=false`, `continuum_limit_derived=false`, `einstein_equations_derived=false`, `scientific_breakthrough=false`, and `Pillar_3=OPEN` for every outcome.
- All repository changes are additive under the v15.40 demo directory plus this plan and one branch-specific workflow.
- Exploratory calculations do not run in CI: preserve one intended missing-implementation RED receipt and one final exact-head certification unless an interface defect requires a narrowly documented intermediate run.

## Review Focus

1. **Forbidden-input leakage:** a constructor must not gain geometry through an imported operator, a rich object attribute, or a precomputed distance; Tasks 3 and 4 pin exact signatures, AST import/name allowlists, and raising sentinels.
2. **Degenerate/nonmetric response work:** zero, negative, dimension-mismatched, or triangle-violating inputs must produce either a deterministic failed metric protocol or a specified validation error rather than a crash or tuned cutoff; Task 3 adds explicit synthetic cases.
3. **Relabeling direction errors:** `pi` versus `pi^-1` can preserve counts while corrupting equivariance; Tasks 3–5 compare every relabeled pair, source coordinate, target edge, and distance under one explicit old-to-new convention.
4. **Control-status contamination:** a historical metric failure must not invalidate the protocol, while a matched-control structural failure must; Task 5 tests both branches directly through `classify_gate`.
5. **Holdout or scale special-casing:** `L=11` and `lambda=7/3` must use the same formulas and exact criteria as the controls; Tasks 2 and 5 compare frozen manifests and scaled work matrices before permitting adjudication.

---

## File map

- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_generation.py`: evidence verification, centered sources, exact candidate/control responses, structural admissibility, orientations, additivity, symmetries, scale, and relabeling inputs.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py`: dependency-free blind source-response work metric and minimum-neighbor construction.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/incidence_target.py`: dependency-free signed-support validation, face adjacency, connectivity, and all-pairs graph distance.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py`: constructor isolation adapters, exhaustive per-size orchestration, exact comparison, gate classification, and canonical JSON CLI.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`: behavior-first unit, integration, ledger, and firewall tests.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/docs/RESULTS.json`: byte-replayable authoritative result.
- Create `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/README.md`: theorem/computation/interpretation report and reproduction commands.
- Create `.github/workflows/uqcf-v1540-global-balance-geometry-specificity.yml`: additive-scope, inherited-regression, deterministic-replay, and exact-head certification.

### Task 1: Freeze the RED contract and CI boundary

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`
- Create: `.github/workflows/uqcf-v1540-global-balance-geometry-specificity.yml`
- Modify: `docs/superpowers/plans/2026-09-19-v1540-global-balance-geometry-specificity-implementation.md` only to append the RED receipt after the run.

**Interfaces:**
- Consumes: the approved v15.40 design and certified v15.39 branch.
- Produces: a failing public contract importing `geometry_specificity_gate`, plus CI that proves inherited health and records the intended absent-module failure before production code exists.

- [ ] **Step 1: Add the complete failing public test skeleton**

Create `test_gate.py` with these imports, status constants, and nine test names. Each later task fills the imported implementation; do not weaken these assertions after scientific output is visible.

```python
import json
from pathlib import Path
import unittest

from geometry_specificity_gate import (
    ALLOWED_GATE_STATUSES,
    CONTROL_KEYS,
    audit,
    canonical_json,
    classify_gate,
    next_required_object_for_status,
)


class GlobalBalanceGeometrySpecificityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_evidence_and_exact_generation_protocol(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(self.result["canonical_augmentation_isomorphism_exact"])
        self.assertTrue(self.result["all_response_equations_exact"])

    def test_response_geometry_is_blind_exact_and_total(self):
        self.assertTrue(self.result["input_separation"]["response_constructor_blind"])
        self.assertTrue(self.result["all_required_pairs_evaluated"])
        self.assertTrue(self.result["all_required_ordered_triples_evaluated"])

    def test_incidence_target_is_blind_four_regular_and_connected(self):
        self.assertTrue(self.result["input_separation"]["target_constructor_blind"])
        self.assertTrue(self.result["all_targets_four_regular"])
        self.assertTrue(self.result["all_targets_connected"])

    def test_orientation_additivity_covariance_and_relabeling(self):
        self.assertTrue(self.result["all_orientation_rays_exact"])
        self.assertTrue(self.result["all_additivity_exact"])
        self.assertTrue(self.result["all_translation_D4_covariance_exact"])
        self.assertTrue(self.result["all_relabeling_equivariant"])

    def test_projective_scale_and_holdout_rules(self):
        self.assertEqual(self.result["projective_scales"], ["1", "7/3"])
        self.assertTrue(self.result["all_scale_verdicts_identical"])
        self.assertEqual(self.result["holdout_size"], 11)
        self.assertTrue(self.result["holdout_formula_unchanged"])

    def test_controls_and_mechanical_correspondence(self):
        self.assertEqual(tuple(self.result["control_keys"]), CONTROL_KEYS)
        self.assertTrue(self.result["matched_controls_structurally_admissible"])
        self.assertTrue(self.result["mechanical_correspondence_rule_applied"])

    def test_status_and_next_object_are_mechanical(self):
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        self.assertEqual(
            self.result["next_required_object"],
            next_required_object_for_status(self.result["status"]),
        )

    def test_construction_and_interpretation_firewalls(self):
        self.assertTrue(all(value == 0 for value in self.result["construction_firewall"].values()))
        self.assertFalse(self.result["physical_metric_derived"])
        self.assertFalse(self.result["scientific_breakthrough"])
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)
```

- [ ] **Step 2: Add the branch workflow**

Create a workflow triggered only by the v15.40 branch paths and manual dispatch:

```yaml
name: UQCF v15.40 Global-Balance Geometry Specificity
on:
  push:
    branches: [research/v15.40-global-balance-geometry-specificity]
    paths:
      - 'ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/**'
      - 'docs/superpowers/specs/2026-09-19-v1540-global-balance-geometry-specificity-design.md'
      - 'docs/superpowers/plans/2026-09-19-v1540-global-balance-geometry-specificity-implementation.md'
      - '.github/workflows/uqcf-v1540-global-balance-geometry-specificity.yml'
  workflow_dispatch:
permissions:
  contents: read
jobs:
  verify:
    runs-on: ubuntu-24.04
    timeout-minutes: 90
    env:
      PYTHONHASHSEED: '0'
```

Install Python `3.13.5` and `numpy==2.3.5`. Before the v15.40 tests, run the v15.38 and v15.39 suites and require exactly `7+8=15` inherited tests. Verify additive scope against `0f3e10602929dd0a148b195f32406efa52082070` with this exact allowlist:

```python
allowed = {
    "docs/superpowers/specs/2026-09-19-v1540-global-balance-geometry-specificity-design.md",
    "docs/superpowers/plans/2026-09-19-v1540-global-balance-geometry-specificity-implementation.md",
    ".github/workflows/uqcf-v1540-global-balance-geometry-specificity.yml",
}
demo = "ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/"
```

Require every diff entry to have status `A` and to be inside `demo` or `allowed`.

- [ ] **Step 3: Run the single intended RED workflow**

Push only the spec, plan, test, and workflow. Expected v15.40 failure:

```text
ModuleNotFoundError: No module named 'geometry_specificity_gate'
```

Confirm additive scope and all 15 inherited tests passed before the intended import failure.

- [ ] **Step 4: Record and commit the RED receipt**

Append the run ID, job ID, exact head SHA, inherited count, and exact missing-module error under `Execution receipts` at the bottom of this plan. Commit message:

```text
test: preregister v15.40 blind geometry gate
```

### Task 2: Implement exact response generation and structural controls

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_generation.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`

**Interfaces:**
- Consumes: hash-pinned v15.39 canary/results, v15.40 design, inherited `representation_actions.py`, and `exact_linear.py`.
- Produces:
  - `ResponseFamily(key: str, labels: tuple[int, ...], sources: tuple[VectorQ, ...], responses: tuple[VectorQ, ...])`
  - `StructuralAudit(key: str, connected: bool, invertible_on_augmentation: bool, translation_D4_covariant: bool, valence_four: bool, response_equations_exact: bool)`
  - `signed_support_B2(L: int) -> tuple[tuple[int, ...], ...]`
  - `response_family(L: int, key: str, scale: Fraction = Fraction(1)) -> ResponseFamily`
  - `relabel_family(family: ResponseFamily, permutation: tuple[int, ...]) -> ResponseFamily`
  - `relabel_support_columns(support, permutation) -> SignedSupport`
  - `generation_audit(L: int) -> dict`

- [ ] **Step 1: Pin inherited evidence before constructing responses**

Define and verify these blobs without importing a pinned module first:

```python
BASE_SHA = "0f3e10602929dd0a148b195f32406efa52082070"
EVIDENCE = {
    "v15.39-source": (V1539 / "source_axiom_canary.py", "620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a"),
    "v15.39-results": (V1539 / "docs/RESULTS.json", "ac8eb10ed90360fee6dcc0f170f19fffd0d74116"),
    "representation_actions.py": (V1528 / "representation_actions.py", "7260147cd6ca47ec21634172b44b98de726904af"),
    "exact_linear.py": (V1528 / "exact_linear.py", "05cc1b8cfec70d501408377b5e44190b259a4514"),
    "v15.40-design": (SPEC, "5f75f9a7ba1df5b21715f775d26bedbedc07297f"),
}
```

Require the inherited ledger status `AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL`, the global-balance verdict `PRETIME_GLOBAL_ORGANIZATION_SURVIVES`, and the two historical verdicts `STRUCTURAL_ONLY_LOCAL`.

- [ ] **Step 2: Add failing centered-source and isomorphism tests**

For every `L in (5, 7, 9, 11)` and every face `f`, assert:

```python
s = centered_source(L, f)
self.assertEqual(sum(s), 0)
self.assertEqual(s[f], Fraction(L * L - 1, L * L))
self.assertTrue(all(s[g] == Fraction(-1, L * L) for g in range(L * L) if g != f))
self.assertEqual(boundary_from_face_vector(L, s), B2_column(L, f))
```

Also require `rank(B2)=L**2-1`, `ker(B2)` on face chains is exactly the constant line, and the augmentation restriction has trivial kernel.

- [ ] **Step 3: Build the four frozen operators without spectral routines**

Use generator displacements exactly:

```python
GENERATORS = {
    "GLOBAL_BALANCE_COMPLETION": ((1, 0), (-1, 0), (0, 1), (0, -1)),
    "MATCHED_DIAGONAL_BALANCE": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
    "MATCHED_STEP2_BALANCE": ((2, 0), (-2, 0), (0, 2), (0, -2)),
}
CONTROL_KEYS = (
    "DIRECT_INHERITANCE",
    "ONE_INCIDENCE_TRANSPORT",
    "MATCHED_DIAGONAL_BALANCE",
    "MATCHED_STEP2_BALANCE",
)
```

Construct face signed-permutation representations from inherited actions. For balance families form `D=4I-A` only on `augmentation_basis(L**2)`. Prohibit `eig`, `eigh`, `svd`, `pinv`, `lstsq`, and floating conversion by a module-source test.

- [ ] **Step 4: Implement exact unique solves and all response families**

Compute and cache one exact augmentation-sector inverse per `(L, balance family)` in the response-generation layer. `ql.inverse` uses exact `rref`; verify both products before using it for all source right-hand sides:

```python
def inverse_on_augmentation(matrix):
    inverse = ql.inverse(matrix)
    identity = ql.identity(len(matrix))
    if ql.matmul(matrix, inverse) != identity or ql.matmul(inverse, matrix) != identity:
        raise ArithmeticError("exact augmentation inverse verification failed")
    return inverse

def solve_with_verified_inverse(matrix, inverse, rhs):
    solution = ql.matvec(inverse, rhs)
    if ql.matvec(matrix, solution) != tuple(rhs):
        raise ArithmeticError("exact solve verification failed")
    return solution
```

This inverse is permitted only here, never in `response_geometry.py`. Reuse keeps the exhaustive all-source audit tractable without changing a formula or sampling the source set.

Return full face vectors in `F_L^0`:

```python
DIRECT_INHERITANCE: u_f = s_f
ONE_INCIDENCE_TRANSPORT: u_f = A_ax @ s_f
GLOBAL_BALANCE_COMPLETION: (4I - A_ax) @ u_f = s_f
MATCHED_DIAGONAL_BALANCE: (4I - A_diag) @ u_f = s_f
MATCHED_STEP2_BALANCE: (4I - A_step2) @ u_f = s_f
```

Generate all `L**2` sources and responses once per family and cache immutable results.

- [ ] **Step 5: Test structural admissibility and common response protocol**

For each balance generator graph, derive neighbors from its permutations and require connectedness, valence four, exact augmentation invertibility, and covariance under the two primitive translations plus all eight D4 matrices. For all five families require response equations, every source face, four incidence-normalized source occurrences, amplitudes `2/3` and `-5/7`, and linear additivity exactly.

Use the old-to-new relabel convention:

```python
pi = tuple((2 * i + 1) % (L * L) for i in range(L * L))
new_vector[pi[old]] = old_vector[old]
new_label = pi[old_label]
new_support[row][pi[old_column]] = old_support[row][old_column]
```

Assert `pi` is bijective and round-trips under its computed inverse.

- [ ] **Step 6: Run the focused generation tests and commit**

Run only the generation/isomorphism/orientation/additivity/covariance tests; all must pass for four sizes. Commit message:

```text
feat: generate exact v15.40 response families
```

### Task 3: Implement the blind response-geometry constructor

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/response_geometry.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`

**Interfaces:**
- Consumes: only `labels`, centered `sources`, and face-potential `responses`, all as immutable tuples containing exact integers/Fractions.
- Produces:
  - `ResponseGeometry(labels, work, minimum, neighbors, symmetric, identity, separated, triangle, pair_count, ordered_triple_count)`
  - `construct_response_geometry(labels, sources, responses) -> ResponseGeometry`
  - `metric_passes(geometry: ResponseGeometry) -> bool`

- [ ] **Step 1: Add synthetic failing tests for validation and metric behavior**

Pin exact signature names with `inspect.signature`. Reject duplicate labels, fewer than two labels, mismatched family lengths, inconsistent vector dimensions, bools, floats, and non-rational entries. Add exact cases that fail strict separation and triangle inequality, plus a valid three-point metric; separately verify that the source-response formula is symmetric and zero on the diagonal for every valid input. A metric failure returns booleans in an otherwise complete `ResponseGeometry`; malformed input raises `TypeError` or `ValueError` before work evaluation.

- [ ] **Step 2: Implement exact source-response work**

Keep this module limited to `dataclasses`, `fractions`, and `itertools`. For every ordered pair compute:

```python
def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))

R[i][j] = dot(subtract(sources[i], sources[j]),
              subtract(responses[i], responses[j]))
```

Require `R[i][i]==0`, compare `R[i][j]` and `R[j][i]` exactly, and count `n*(n-1)//2` unordered pairs.

- [ ] **Step 3: Implement exhaustive metric and minimum-neighbor checks**

Evaluate strict separation for every distinct pair and triangle inequality for every ordered triple `(i,j,k)` including repeated labels:

```python
triangle = all(R[i][k] <= R[i][j] + R[j][k]
               for i in range(n) for j in range(n) for k in range(n))
minimum = min(R[i][j] for i in range(n) for j in range(i + 1, n))
neighbors = frozenset(
    frozenset((labels[i], labels[j]))
    for i in range(n) for j in range(i + 1, n)
    if R[i][j] == minimum
)
```

Do not use a tolerance, fitted transform, supplied graph, matrix inversion, coordinate, or candidate-specific branch.

- [ ] **Step 4: Enforce the hostile input firewall**

Create a raising sentinel with forbidden properties `B1`, `B2`, `A`, `D`, `translations`, `D4`, `coordinates`, `distances`, `spectrum`, and `candidate_key`. Pass only its safe `labels`, `sources`, and `responses` properties to the constructor and require no forbidden access. Parse the module AST and require imports to be a subset of `{"dataclasses", "fractions", "itertools", "__future__"}` and loaded names to exclude the forbidden property set plus `inverse`, `solve`, and `numpy`.

- [ ] **Step 5: Test exact scale and relabel covariance**

For every generated family and size require:

```python
scaled.work[i][j] == Fraction(7, 3) * base.work[i][j]
scaled.neighbors == base.neighbors
(scaled.symmetric, scaled.identity, scaled.separated, scaled.triangle) == (
    base.symmetric, base.identity, base.separated, base.triangle,
)
relabeled.work[pi[i]][pi[j]] == base.work[i][j]
relabeled.neighbors == map_pairs(base.neighbors, pi)
```

Use an explicit pair-mapping helper rather than unpacking unordered sets in production code.

- [ ] **Step 6: Run focused constructor tests and commit**

Expected: all synthetic, generated, firewall, scale, and relabeling tests pass. Commit message:

```text
feat: add blind exact response geometry
```

### Task 4: Implement the incidence-only target constructor

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/incidence_target.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`

**Interfaces:**
- Consumes: only a rectangular immutable signed-support matrix with entries in `{-1,0,1}` and columns interpreted as opaque face labels `0..n-1`.
- Produces:
  - `IncidenceTarget(labels, neighbors, degrees, connected, distances)`
  - `construct_incidence_target(signed_support) -> IncidenceTarget`

- [ ] **Step 1: Add exact validation and graph tests**

Pin the one-argument signature. Reject empty/ragged support, bools, entries outside `{-1,0,1}`, fewer than two columns, and a face column with no support. Add small matrices producing a connected path, a disconnected graph, and an isolated face. The constructor must return structural booleans rather than assume four-regularity.

- [ ] **Step 2: Construct adjacency from shared nonzero row support**

For each row, collect nonzero columns and add every unordered pair of distinct columns. Do not inspect signs beyond validating signed support. Build immutable neighbor sets and degree tuples from this relation.

```python
for row in signed_support:
    incident = tuple(i for i, value in enumerate(row) if value != 0)
    for offset, first in enumerate(incident):
        for second in incident[offset + 1:]:
            neighbors.add(frozenset((first, second)))
```

- [ ] **Step 3: Compute exact unweighted all-pairs distances internally**

Run deterministic BFS from every label using `collections.deque`. Store `None` for unreachable ordered pairs so disconnected input remains representable. Set `connected` only if every ordered pair has an integer distance. For each required torus require every degree is four, the graph is connected, and there are exactly `2*L**2` unordered target edges.

- [ ] **Step 4: Enforce the hostile target firewall**

Wrap valid support in a sequence sentinel whose properties `A`, `D`, `responses`, `response_pairings`, `translations`, `D4`, `coordinates`, and `precomputed_distances` raise on access. Require construction succeeds through sequence access alone. Parse the module AST and permit only `collections`, `dataclasses`, `itertools`, and `__future__`; reject the forbidden names and imports.

- [ ] **Step 5: Test relabeling equivariance with the explicit convention**

After column relabeling, require target edges and every distance transform old-to-new:

```python
relabeled.distances[pi[i]][pi[j]] == original.distances[i][j]
relabeled.neighbors == map_pairs(original.neighbors, pi)
```

Do not pass a precomputed distance or inverse permutation into the constructor.

- [ ] **Step 6: Run focused target tests and commit**

Expected: validation, synthetic graphs, all four exact targets, firewall, and relabeling tests pass. Commit message:

```text
feat: derive blind incidence geometry target
```

### Task 5: Implement isolated comparison, exhaustive audits, and mechanical status

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`

**Interfaces:**
- Consumes: `ResponseFamily` objects from generation and frozen `ResponseGeometry`/`IncidenceTarget` values from the two constructors.
- Produces:
  - `GeometryComparison(metric_passes: bool, neighbors_equal: bool, distances_equal: bool)`
  - `compare_geometry(response: ResponseGeometry, target: IncidenceTarget) -> GeometryComparison`
  - `classify_gate(protocol_valid: bool, canonical_all_sizes: bool, control_all_sizes: dict[str, bool]) -> str`
  - `exact_size_audit(L: int) -> dict`
  - `next_required_object_for_status(status: str) -> str`
  - `audit() -> dict`

- [ ] **Step 1: Add failing comparison and status-precedence tests**

Build synthetic frozen outputs and require `compare_geometry` uses only output fields. Reconstruct distances from `response.neighbors` inside the adjudication module and compare them to `target.distances` exactly. Pin classification precedence:

```python
if not protocol_valid:
    return "RESPONSE_GEOMETRY_PROTOCOL_INVALID"
if not canonical_all_sizes:
    return "NO_RESPONSE_DERIVED_GEOMETRY"
if any(control_all_sizes.values()):
    return "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY"
return "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES"
```

Add one test where a historical control is nonmetric but protocol validity remains true, and one where a matched-control structural flag is false and protocol validity becomes false.

- [ ] **Step 2: Keep candidate identity outside the response constructor**

The orchestration adapter calls:

```python
geometry = construct_response_geometry(family.labels, family.sources, family.responses)
```

Store the family key only after the constructor returns. The incidence adapter passes only `signed_support_B2(L)` into `construct_incidence_target`. Tests monkeypatch each adapter with raising-rich objects to prove no raw operator crosses either boundary.

- [ ] **Step 3: Implement exact correspondence and distance consistency**

For each size/family/scale/relabel state record metric booleans, exact work values serialized as reduced fraction text, `R_min`, pair/triple counts, response neighbor pairs, target neighbor pairs, exact set equality, and reconstructed-distance equality. Distance equality is checked only when neighbor equality holds and is recorded as a consistency check rather than extra evidence.

- [ ] **Step 4: Exhaust the frozen audit matrix**

For `L=(5,7,9,11)`, all five families, scales `(1,7/3)`, and original/relabelled states:

- generate every one of the `L**2` labeled sources/responses;
- evaluate `L**2*(L**2-1)//2` unordered pairs;
- evaluate `(L**2)**3` ordered triples;
- verify four normalized edge occurrences at one face and their translation/D4 images;
- verify two-source additivity with `2/3` and `-5/7`;
- verify exact old-to-new equivariance of constructor outputs and final comparison;
- ensure the holdout row was produced from the same family manifest and code path.

Cache generation and constructor results by immutable `(L, family, scale, relabeled)` keys. Do not cache or shortcut away the recorded exhaustive triple count.

- [ ] **Step 5: Aggregate protocol validity before scientific classification**

Set `protocol_valid` to the conjunction of evidence pins, constructor firewalls, canonical augmentation isomorphism, exact response equations, all target structural checks, both matched-control structural audits, orientation/additivity/covariance, scale/relabel equivalence, unchanged holdout manifest, exact-count checks, and all eight zero construction counters. Historical metric failures do not enter this conjunction.

If false, return the protocol-invalid status without publishing canonical/control correspondence booleans. If true, define:

```python
canonical_all_sizes = all(
    row.metric_passes and row.neighbors_equal
    for row in canonical_original_scale_one_rows
)
control_all_sizes[key] = all(
    row.metric_passes and row.neighbors_equal
    for row in original_scale_one_rows_for_key
)
```

Scale and relabel rows certify invariance but do not multiply scientific evidence.

- [ ] **Step 6: Add the complete construction firewall and next-object map**

Require this exact dictionary:

```python
construction_firewall = {
    "spectrum_queries": 0,
    "spectral_edge_parameters": 0,
    "geometry_fit_parameters": 0,
    "candidate_specific_thresholds": 0,
    "coordinate_queries_in_response_geometry": 0,
    "B2_queries_in_response_geometry": 0,
    "response_queries_in_incidence_target": 0,
    "operator_inversions_in_response_geometry": 0,
}
```

Map statuses exactly:

```python
{
    "RESPONSE_GEOMETRY_PROTOCOL_INVALID":
        "REPAIR_BLIND_GEOMETRY_PROTOCOL_BEFORE_ANY_ADJUDICATION",
    "NO_RESPONSE_DERIVED_GEOMETRY":
        "CLOSE_GLOBAL_BALANCE_GEOMETRY_INTERPRETATION_WITHOUT_TUNING",
    "GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY":
        "DOWNGRADE_V1539_TO_GENERIC_INVERSE_OPERATOR_GLOBALITY",
    "CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES":
        "PREREGISTER_FORMAL_CONNECTION_CURVATURE_AND_SOURCE_CORRESPONDENCE_GATE",
}
```

- [ ] **Step 7: Run the complete in-memory gate tests and commit**

Expected: all nine tests except the committed-ledger test pass; the scientific status itself is data and must only be asserted to equal the mechanical rule. Commit message:

```text
feat: adjudicate v15.40 geometry specificity
```

### Task 6: Freeze the deterministic ledger and scientific report

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/test_gate.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/docs/RESULTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.40-global-balance-geometry-specificity/README.md`

**Interfaces:**
- Consumes: all four exact size audits and their mechanically derived status.
- Produces: `canonical_json(result: dict) -> str`, CLI `--out`/`--check`, authoritative result ledger, and human-readable boundary report.

- [ ] **Step 1: Complete the top-level ledger schema**

Include version/base/design identities, evidence pins, source/control formula manifests, required sizes, scale/relabel manifests, constructor-interface audit, structural audits, exhaustive counts, per-size geometry rows, exact correspondence booleans, status derivation inputs, next object, and all firewall fields.

Serialize each Fraction as an integer string or reduced `"numerator/denominator"`; never serialize a float. Recursively test that the ledger contains no Python/JSON float.

- [ ] **Step 2: Add the interpretation firewall verbatim**

Require:

```python
{
    "new_source_semantics_axiom_inherited": True,
    "new_global_balance_response_axiom_inherited": True,
    "source_axiom_derived_from_frozen_ontology": False,
    "response_axiom_derived_from_frozen_ontology": False,
    "physical_metric_derived": False,
    "spacetime_derived": False,
    "physical_gravity_derived": False,
    "continuum_limit_derived": False,
    "einstein_equations_derived": False,
    "uses_pruning": False,
    "uses_entropy": False,
    "uses_physical_time": False,
    "scientific_breakthrough": False,
    "Pillar_3": "OPEN",
}
```

If the status is generic, add a monotonic v15.39 interpretation downgrade field without modifying the v15.39 artifact. If specificity survives, describe it only as a finite internal Level-1 correspondence candidate conditional on inherited axioms.

- [ ] **Step 3: Generate and prove byte-identical replay**

Run:

```bash
python geometry_specificity_gate.py --out docs/RESULTS.json
cp docs/RESULTS.json /tmp/v1540-results-first.json
python geometry_specificity_gate.py --check docs/RESULTS.json > /tmp/v1540-results-second.json
cmp docs/RESULTS.json /tmp/v1540-results-first.json
cmp docs/RESULTS.json /tmp/v1540-results-second.json
```

The CLI prints only canonical JSON to stdout so the second comparison is meaningful.

- [ ] **Step 4: Write the README from the computed status**

Report separately: frozen assumptions, exact construction, computed finite result, control comparison, theorem/computation boundary, interpretation boundary, stop rule, and reproduction. State the actual status prominently but never call any outcome physical geometry, spacetime, gravity, a continuum result, Einstein dynamics, or a breakthrough.

- [ ] **Step 5: Complete all nine tests**

Derive expected status from committed row booleans inside the test. Require `docs/RESULTS.json == canonical_json(audit())`, every firewall counter/claim, all four status-to-next-object mappings, exact source/target counts, and no float anywhere.

- [ ] **Step 6: Run local-equivalent verification and commit**

Run:

```bash
python -m unittest -v test_gate.py
python geometry_specificity_gate.py --check docs/RESULTS.json > /tmp/v1540-results.json
cmp docs/RESULTS.json /tmp/v1540-results.json
python -m compileall -q response_generation.py response_geometry.py incidence_target.py geometry_specificity_gate.py test_gate.py
```

Commit message:

```text
docs: freeze v15.40 geometry specificity result
```

### Task 7: Exact-head certification, review, and PR receipt

**Files:**
- Modify only if a verification defect is found: `.github/workflows/uqcf-v1540-global-balance-geometry-specificity.yml`
- Update draft PR #51 description/comment; do not merge.

**Interfaces:**
- Consumes: the complete exact-head branch and immutable ledger.
- Produces: exact-head Actions success, whole-branch review findings, and a durable draft-PR receipt.

- [ ] **Step 1: Run the final workflow once at the exact implementation head**

Require additive scope, inherited suites `7+8`, v15.40 exactly `9` tests, canonical replay, `cmp`, compileall, all construction counters zero, exact holdout presence, the computed mechanical status, and the complete claim firewall.

- [ ] **Step 2: Perform whole-branch review against the frozen spec**

Use `superpowers:requesting-code-review` if the approved execution method permits a reviewer; otherwise perform the same checklist in the active context. Review every spec section, forbidden dependency, status branch, control treatment, exact-count invariant, and README claim against the diff from `0f3e10602929dd0a148b195f32406efa52082070`.

- [ ] **Step 3: Fix only verified implementation or certification defects**

Do not change a formula, control, scale, size, criterion, or interpretation boundary after output inspection. Any defect fix gets a focused regression test and reruns the complete exact-head workflow. Use commit message:

```text
ci: certify v15.40 geometry specificity gate
```

- [ ] **Step 4: Update draft PR #51**

Record design head/blob, plan commit, RED run/job/head, final GREEN run/job/head, test counts, byte-replay result, exact status, per-control correspondence table, claim boundary, and next required object. Leave PR #51 draft/open/unmerged.

- [ ] **Step 5: Report scientific significance honestly**

Explicitly flag a positive specificity result as scientifically important but axiom-dependent and not a breakthrough. Explicitly flag a generic or absent geometry result as a meaningful negative/downgrade. Keep Pillar 3 OPEN in every report.

## Execution receipts

- Plan identity: `docs/superpowers/plans/2026-09-19-v1540-global-balance-geometry-specificity-implementation.md`.
- Execution base: `0f3e10602929dd0a148b195f32406efa52082070`.
- Reviewed design head: `940e77adf346ad8defc01f94b3f6e7c39ff18880`.
- RED receipt: Actions run `35464098454`, job `105953033212`, exact head
  `b0b8116b7dc9455cef98ce8578c5c3c5afe37e57`; additive scope passed, all `7+8=15`
  inherited tests passed, and the v15.40 gate then failed exactly with
  `ModuleNotFoundError: No module named 'geometry_specificity_gate'`.
- Final exact-head receipt: record in draft PR #51 after Task 7; do not create an infinite receipt-only commit chain.
