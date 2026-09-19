# v15.41 Formal Connection, Curvature, and Source Correspondence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and certify the preregistered v15.41 exact gate asking whether the frozen v15.40 response geometry canonically determines a formal discrete connection and a source-specific linearized curvature response.

**Architecture:** Reuse v15.40 only through a hash-pinned input adapter, then keep the adjudicating path in three isolated layers: a response-only operational complex/connection constructor, a centered-source/`B2`-only target constructor, and a mechanical gate. The response graph first generates an orientation-free square complex and flat baseline transport up to local `D4` gauge; an exact first-order conformal metric perturbation then solves metric-compatibility and Cartan closure equations before curvature is contracted through the uniquely equivariant cycle-label incidence map.

**Tech Stack:** Python 3.13.5, standard-library `dataclasses`, `fractions.Fraction`, `collections`, `itertools`, `json`, `unittest`, NumPy 2.3.5 only inside the hash-pinned inherited v15.40 generator, GitHub Actions on `ubuntu-24.04`.

**Spec:** `docs/superpowers/specs/2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md`

## Global Constraints

- Base exactly on v15.40 certified head `84aa1c81fd86ac4d7a06015482f98572f3afc05f`.
- Preserve the reviewed v15.41 design blob `6d35aae0ccb6c2584d26d5a83d522b3cc7036728`.
- Do not modify v15.40 or any earlier artifact; all scientific implementation is additive under the v15.41 demo directory.
- Use unchanged formulas at `L=5,7,9,11`; `L=11` is the locked holdout.
- Use exact rational/integer arithmetic for graph construction, quotient ranks, transport matrices, equation ranks, holonomy, curvature, contractions, and correspondence. No floating tolerance adjudicates.
- The operational constructor receives only labels, exact work matrix `R`, response-derived neighbors `N_R`, and one exact response field when constructing its source-indexed first variation.
- The operational constructor may not import or query `B1`, `B2`, coordinates, torus displacements, inherited generators/operators, eigenspectra, candidate identity, historical connection/holonomy, or physical targets.
- The source-target constructor receives only the centered source family and signed support of `B2`; it may not import or query response work, neighbors, response fields, connection, curvature, coordinates, or candidate identity.
- Only the gate compares frozen operational and target outputs.
- Every local frame ordering, axis sign, and auxiliary orientation is gauge; no lexicographic representative may adjudicate.
- Reuse only `DIRECT_INHERITANCE`, `ONE_INCIDENCE_TRANSPORT`, `MATCHED_DIAGONAL_BALANCE`, and `MATCHED_STEP2_BALANCE`, plus the two frozen scramble controls.
- Evaluate common projective scales `1` and `7/3`, simultaneous deterministic relabeling `pi(i)=(2*i+1) mod L**2`, source superposition amplitudes `2/3` and `-5/7`, and every source at every size.
- Keep every construction-firewall counter exactly zero.
- Keep `historical_connection_used_for_adjudication=false`, `physical_connection_derived=false`, `physical_curvature_derived=false`, `stress_energy_derived=false`, `spacetime_derived=false`, `continuum_limit_derived=false`, `einstein_equations_derived=false`, `scientific_breakthrough=false`, and `Pillar_3=OPEN` for every outcome.
- Historical Retained-Atlas comparison is permitted only after the gate verdict is frozen and must be labeled `NON_ADJUDICATING_HISTORICAL_CROSS_CHECK`; it is not part of this implementation plan.
- Preserve one intended missing-implementation RED receipt and one final exact-head certification. Exploratory scientific runs do not execute in CI.

## Review Focus

1. **False uniqueness from frame fixing:** choosing one axis order or orientation can collapse multiple connection orbits; Tasks 2 and 3 enumerate all local `D4` frame actions and compare gauge-invariant quotient data.
2. **Non-square or degenerate response graphs:** irregular stars, ambiguous opposite pairs, missing/excess chordless cycles, or tangent quotient rank other than two must return `CONNECTION_NOT_IDENTIFIABLE`; Task 2 supplies explicit synthetic graphs for every branch.
3. **Underdetermined first-order connection:** metric compatibility alone leaves rotational edge freedom, while malformed closure equations can appear full-rank after a hidden gauge choice; Task 4 publishes coefficient rank, augmented rank, nullity, and exact residuals before classifying uniqueness.
4. **Tautological source recovery:** defining curvature as the inherited graph Laplacian would guarantee the desired result; Tasks 4 and 5 construct transport first, differentiate holonomy mechanically, forbid operator imports, and only then compare the independent contraction with sources.
5. **Control or relabel contamination:** a control label, unmatched scramble, or `pi`/`pi^-1` error can leak into construction while preserving counts; Tasks 5 and 6 use hostile sentinels, exact old-to-new mapping, two asymmetric scrambles, and identity-hidden family iteration.

---

## File map

- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/exact_algebra.py`: dependency-free exact matrix, rank, solve, nullspace, and first-order matrix-product helpers.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/response_inputs.py`: hash-pinned v15.40 evidence verification and immutable family/work/relabel adapters; this is the only v15.41 module allowed to import v15.40 generation code.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/operational_complex.py`: response-only star validation, chordless squares, directed-edge quotient, tangent carrier, local `D4` gauges, baseline transports, and holonomy.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/linearized_connection.py`: isotropic lift, exact first-order metric-compatible transports, Cartan closure system, uniqueness audit, and differentiated holonomy.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/source_target.py`: centered-source and signed-`B2`-support-only target construction.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/connection_curvature_gate.py`: unique contraction enumeration, family/size orchestration, controls, classification, ledger, and canonical JSON CLI.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py`: exact algebra, malformed graph, tangent, gauge, baseline connection, and holonomy tests.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_linearized_connection.py`: invariant lift, compatibility, Cartan closure, uniqueness, linearity, and curvature tests.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_gate.py`: input separation, target, controls, relabeling, scale, holdout, status, firewall, and replay tests.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/docs/RESULTS.json`: byte-replayable authoritative result.
- Create `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/README.md`: result, exact construction, limitations, and reproduction commands.
- Create `.github/workflows/uqcf-v1541-formal-connection-curvature-source-correspondence.yml`: additive-scope, inherited-regression, exact replay, and exact-head certification.

### Task 1: Freeze the RED contract and CI boundary

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_linearized_connection.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_gate.py`
- Create: `.github/workflows/uqcf-v1541-formal-connection-curvature-source-correspondence.yml`
- Modify: `docs/superpowers/plans/2026-09-19-v1541-formal-connection-curvature-source-correspondence-implementation.md` only to append execution receipts.

**Interfaces:**
- Consumes: approved v15.41 specification and certified v15.40 branch.
- Produces: 15 behavior-first tests importing the planned public interfaces and a branch workflow that records the expected missing-module RED failure after inherited regressions pass.

- [ ] **Step 1: Create the operational RED tests**

Create the shared synthetic fixture and five unittest methods with these imports and public assertions:

```python
from fractions import Fraction
import unittest

from operational_complex import (
    ConnectionStatus,
    construct_operational_complex,
    enumerate_baseline_connection,
)


def periodic_square_input(L=5):
    labels = tuple(range(L * L))
    def label(x, y): return (x % L) + L * (y % L)
    edges = frozenset(
        frozenset((label(x, y), label(x + dx, y + dy)))
        for x in range(L) for y in range(L)
        for dx, dy in ((1, 0), (0, 1))
    )
    def distance(i, j):
        ix, iy = i % L, i // L
        jx, jy = j % L, j // L
        dx = min((ix - jx) % L, (jx - ix) % L)
        dy = min((iy - jy) % L, (jy - iy) % L)
        return Fraction(dx + dy)
    work = tuple(tuple(distance(i, j) for j in labels) for i in labels)
    return labels, work, edges


class OperationalComplexTests(unittest.TestCase):
    def test_exact_square_complex_and_tangent_quotient(self):
        result = construct_operational_complex(*periodic_square_input())
        self.assertEqual(result.status, ConnectionStatus.IDENTIFIABLE)
        self.assertEqual(result.complex.tangent_rank, 2)
        self.assertEqual(len(result.complex.cycles), 25)

    def test_malformed_stars_cycles_and_opposites_stop(self):
        labels = (0, 1, 2, 3)
        work = tuple(tuple(Fraction(i != j) for j in labels) for i in labels)
        path = frozenset((frozenset((0, 1)), frozenset((1, 2)), frozenset((2, 3))))
        result = construct_operational_complex(labels, work, path)
        self.assertEqual(result.status, ConnectionStatus.NOT_IDENTIFIABLE)
        self.assertIn(result.reason, {"degree_not_four", "edge_cycle_count", "opposites_ambiguous"})

    def test_local_d4_gauge_is_complete(self):
        result = construct_operational_complex(*periodic_square_input())
        self.assertEqual(len(result.complex.d4_actions), 8)
        self.assertEqual(len(set(result.complex.d4_actions)), 8)

    def test_baseline_transport_has_one_gauge_orbit(self):
        complex_ = construct_operational_complex(*periodic_square_input()).complex
        result = enumerate_baseline_connection(complex_)
        self.assertEqual(result.status, ConnectionStatus.IDENTIFIABLE)
        self.assertEqual(result.connection.gauge_orbit_count, 1)

    def test_holonomy_is_orientation_and_frame_covariant(self):
        complex_ = construct_operational_complex(*periodic_square_input()).complex
        connection = enumerate_baseline_connection(complex_).connection
        self.assertTrue(connection.flat)
        self.assertTrue(all(cls == connection.identity_class for cls in connection.holonomy_classes))
```

Use an explicit 3-by-3 periodic square graph built only as `(labels, work, neighbors)` synthetic input. Also include a degree-three graph, `K5`, a four-regular graph with an edge in fewer than two chordless squares, and a star with tied non-opposite maxima. Each invalid scientific case must return `ConnectionStatus.NOT_IDENTIFIABLE`, not raise or silently choose.

- [ ] **Step 2: Create the linearized-connection RED tests**

Create five methods importing:

```python
from linearized_connection import (
    construct_isotropic_lift,
    solve_linearized_connection,
    differentiate_holonomy,
)


class LinearizedConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex = construct_operational_complex(*periodic_square_input()).complex
        cls.baseline = enumerate_baseline_connection(cls.complex).connection
        cls.field = tuple(Fraction(i - 12) for i in range(25))

    def test_isotropic_symmetric_tensor_space_has_rank_one(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        self.assertEqual(lift.invariant_dimension, 1)
        self.assertTrue(lift.glues_equivariantly)

    def test_metric_compatibility_is_exact_on_every_edge(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertTrue(result.metric_compatibility_exact)

    def test_cartan_closure_rank_and_residual_are_exact(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertEqual(result.coefficient_rank, result.augmented_rank)
        self.assertTrue(result.residual_zero)

    def test_solution_is_unique_and_linear_or_stops(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        self.assertEqual(result.nullity, result.gauge_dimension)
        self.assertTrue(result.unique_mod_gauge)

    def test_curvature_is_differentiated_holonomy_not_laplacian(self):
        lift = construct_isotropic_lift(self.complex, self.field)
        result = solve_linearized_connection(self.complex, self.baseline, lift)
        values = tuple(differentiate_holonomy(self.baseline, result, cycle)
                       for cycle in self.complex.cycles)
        self.assertEqual(len(values), len(self.complex.cycles))
```

The final test AST-scans `linearized_connection.py` and rejects identifiers/imports containing `B1`, `B2`, `laplacian`, `defect`, `response_generation`, `coordinates`, `numpy`, `eig`, `svd`, or `pinv`.

- [ ] **Step 3: Create the gate RED tests**

Create five methods importing:

```python
from connection_curvature_gate import (
    ALLOWED_GATE_STATUSES,
    audit,
    canonical_json,
    classify_gate,
    next_required_object_for_status,
)


class ConnectionCurvatureGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_evidence_and_input_separation(self):
        self.assertTrue(self.result["evidence_verified"])
        self.assertTrue(self.result["input_separation"]["operational_constructor_blind"])
        self.assertTrue(self.result["input_separation"]["source_target_blind"])

    def test_unique_contraction_and_independent_source_target(self):
        self.assertIn(self.result["curvature_contraction_dimension"], (None, 1))
        self.assertTrue(self.result["source_target_frozen_before_adjudication"])

    def test_controls_relabeling_scale_superposition_and_holdout(self):
        self.assertEqual(self.result["projective_scales"], ["1", "7/3"])
        self.assertTrue(self.result["all_relabeling_checks_complete"])
        self.assertTrue(self.result["all_superposition_checks_complete"])
        self.assertEqual(self.result["holdout_size"], 11)

    def test_status_firewalls_and_claim_boundary(self):
        self.assertIn(self.result["status"], ALLOWED_GATE_STATUSES)
        self.assertTrue(all(value == 0 for value in self.result["construction_firewall"].values()))
        self.assertFalse(self.result["historical_connection_used_for_adjudication"])
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)
```

Pin all five statuses from the specification and require `Pillar_3 == "OPEN"` regardless of the classified branch.

- [ ] **Step 4: Add the branch-specific workflow**

Create the workflow with this header and path filter:

```yaml
name: UQCF v15.41 Formal Connection Curvature Source Gate

on:
  push:
    branches: [research/v15.41-formal-connection-curvature-source-correspondence]
    paths:
      - 'ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/**'
      - 'docs/superpowers/specs/2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md'
      - 'docs/superpowers/plans/2026-09-19-v1541-formal-connection-curvature-source-correspondence-implementation.md'
      - '.github/workflows/uqcf-v1541-formal-connection-curvature-source-correspondence.yml'
  workflow_dispatch:

permissions:
  contents: read
```

Use Python `3.13.5`, NumPy `2.3.5`, `PYTHONHASHSEED=0`, and `timeout-minutes: 90`. Verify every diff from `84aa1c81fd86ac4d7a06015482f98572f3afc05f` is additive and lies under the new demo directory or equals the v15.41 spec, plan, or workflow. Run v15.39's 8 tests and v15.40's 9 tests before v15.41.

- [ ] **Step 5: Run and record the intended RED receipt**

Push only the spec, plan, tests, and workflow. Require additive scope and all 17 inherited tests to pass, then record the exact expected first failure:

```text
ModuleNotFoundError: No module named 'operational_complex'
```

Append the Actions run ID, job ID, exact head SHA, inherited counts, and error text under `Execution receipts`. Commit:

```text
test: preregister v15.41 formal connection gate
```

### Task 2: Build pinned inputs and the response-only operational complex

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/exact_algebra.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/response_inputs.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/operational_complex.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py`

**Interfaces:**
- Consumes: hash-pinned v15.40 family generation and work geometry through `response_inputs.py` only.
- Produces:
  - `FamilyInput(key, labels, sources, responses, work, neighbors)`
  - `family_input(L: int, key: str, scale: Fraction) -> FamilyInput`
  - `source_target_input(L: int) -> tuple[tuple[VectorQ, ...], SignedSupport]`
  - `OperationalComplex(labels, work, neighbors, adjacency, cycles, directed_edges, direction_classes, tangent_rank, local_vectors, d4_actions, metric_automorphisms)`
  - `construct_operational_complex(labels, work, neighbors) -> OperationalComplexAudit`
  - exact algebra functions `rref`, `rank`, `nullspace`, `solve_unique`, `matmul`, `matvec`, `transpose`, `add`, and `scale`.

Use one scientific-stage enum throughout the operational modules:

```python
from enum import Enum

class ConnectionStatus(str, Enum):
    IDENTIFIABLE = "IDENTIFIABLE"
    NOT_IDENTIFIABLE = "NOT_IDENTIFIABLE"
```

- [ ] **Step 1: Pin every inherited blob before import**

Set `BASE_SHA` and `EVIDENCE` exactly:

```python
BASE_SHA = "84aa1c81fd86ac4d7a06015482f98572f3afc05f"
EVIDENCE = {
    "v15.40-response-generation": (V1540 / "response_generation.py", "afd5a68ce74f7f80f49b6fd6307ebb0681182bf5"),
    "v15.40-response-geometry": (V1540 / "response_geometry.py", "9128c24b695c1b539ac60dc93aeaf0bd4795c57b"),
    "v15.40-incidence-target": (V1540 / "incidence_target.py", "03c1f62279865aac396ea4b85f75a8d38c1629cf"),
    "v15.40-gate": (V1540 / "geometry_specificity_gate.py", "2e75867e6aedb82ebe3d9c1f04733e2c0d33018a"),
    "v15.40-tests": (V1540 / "test_gate.py", "349d500bd97178ac0e341e65699d0ce5f581b7cf"),
    "v15.40-results": (V1540 / "docs/RESULTS.json", "c56ca48110b3341e2d68289be717bf1e5308a20a"),
    "v15.40-design": (V1540_SPEC, "5f75f9a7ba1df5b21715f775d26bedbedc07297f"),
    "v15.41-design": (V1541_SPEC, "6d35aae0ccb6c2584d26d5a83d522b3cc7036728"),
}
```

Verify the inherited status is `CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES`, sizes are `[5,7,9,11]`, every firewall value is zero, and Pillar 3 is open before importing v15.40 modules.

- [ ] **Step 2: Implement dependency-free exact algebra**

Copy no scientific operator. Implement Gaussian elimination over `Fraction` with explicit dimensions:

```python
MatrixQ = tuple[tuple[Fraction, ...], ...]
VectorQ = tuple[Fraction, ...]

def solve_unique(a: MatrixQ, b: VectorQ) -> VectorQ:
    augmented = tuple(row + (rhs,) for row, rhs in zip(a, b))
    rr, pivots = rref(augmented, ncols=len(a[0]) + 1)
    if pivots and pivots[-1] == len(a[0]):
        raise ValueError("inconsistent exact system")
    if tuple(pivots) != tuple(range(len(a[0]))):
        raise ValueError("nonunique exact system")
    return tuple(rr[i][-1] for i in range(len(a[0])))
```

Test empty matrices with explicit `ncols`, ragged input, dimension mismatch, inconsistent systems, nonunique systems, and exact residual `A*x=b`.

- [ ] **Step 3: Construct immutable family inputs**

`response_inputs.family_input` calls v15.40 `response_family`, then its blind `construct_response_geometry`, and copies only primitive immutable output into `FamilyInput`. It must not expose the v15.40 complex, `B2`, generator permutations, `A`, or `D`. A separate `source_target_input(L)` returns centered sources plus a primitive immutable copy of signed `B2` support; the gate may pass that pair only to `source_target.py`, never to an operational function.

For relabeling use the inherited old-to-new convention and reconstruct the work matrix by:

```python
changed_work[pi[i]][pi[j]] = original_work[i][j]
changed_neighbors = frozenset(
    frozenset(pi[label] for label in edge) for edge in original_neighbors
)
```

- [ ] **Step 4: Reconstruct chordless squares from neighbors only**

Validate exact integer labels and symmetric simple edges. Build sorted adjacency and enumerate canonical chordless four-cycles by considering all length-four closed walks with four distinct labels, rejecting either diagonal edge, and canonicalizing over eight rotations/reversals:

```python
def canonical_cycle(vertices):
    rotations = tuple(vertices[i:] + vertices[:i] for i in range(4))
    reversed_vertices = tuple(reversed(vertices))
    return min(rotations + tuple(reversed_vertices[i:] + reversed_vertices[:i] for i in range(4)))
```

Require degree four, connectedness, exactly two chordless cycles per edge, and exactly `L**2` cycles when the label count is a perfect odd square. Scientific structural failure returns `NOT_IDENTIFIABLE` with reason codes; malformed input types raise `TypeError`/`ValueError`.

- [ ] **Step 5: Build the intrinsic tangent quotient**

Generate one formal variable for every directed edge. Add exact relations:

```text
v_(y,x) + v_(x,y) = 0
v_(x0,x1) - v_(x3,x2) = 0  for each oriented chordless square
v_(x1,x2) - v_(x0,x3) = 0  for each oriented chordless square
```

Compute the quotient dimension as `directed_edge_count - rank(relations)`. Require rank two. Choose an arbitrary algebraic quotient basis only for computation, enumerate its full eight-element `D4` basis orbit, and assert every local star maps bijectively to `{+e1,-e1,+e2,-e2}` in every orbit. Store only basis-independent relations and gauge-orbit invariants in the audit.

- [ ] **Step 6: Pin opposite pairs from exact work**

For each star, compute all six `R(y,z)` values. Require exactly two disjoint maximizing pairs covering the star and require `R(x,y)=R_min` for all four radial directions. Confirm quotient negatives agree with those pairs. A tied partition, incomplete cover, or mismatch returns `NOT_IDENTIFIABLE`.

Enumerate weighted-metric automorphisms without general factorial permutation search. For every proposed image of one root and each of its eight local `D4` frame images, propagate labels through the directed-edge quotient, reject conflicts, and retain the completed permutation only if it preserves every work entry and neighbor edge exactly. This yields at most `8*len(labels)` candidates and publishes the verified automorphism count.

- [ ] **Step 7: Run focused tests and commit**

Run:

```bash
python -m unittest -v \
  test_operational_complex.OperationalComplexTests.test_exact_square_complex_and_tangent_quotient \
  test_operational_complex.OperationalComplexTests.test_malformed_stars_cycles_and_opposites_stop \
  test_operational_complex.OperationalComplexTests.test_local_d4_gauge_is_complete
```

Expected: 3 tests pass. Commit:

```text
feat: construct v15.41 response-only tangent complex
```

### Task 3: Enumerate the baseline connection and formal holonomy

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/operational_complex.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py`

**Interfaces:**
- Consumes: successful `OperationalComplexAudit` with rank-two quotient and complete local `D4` orbit.
- Produces:
  - `BaselineConnection(transports, gauge_orbit_count, holonomy_classes, flat)`
  - `enumerate_baseline_connection(complex_: OperationalComplex) -> BaselineConnectionAudit`
  - `cycle_holonomy(connection, cycle, orientation) -> MatrixQ`.

- [ ] **Step 1: Define transport candidates without a frame choice**

For edge `x->y`, a candidate maps each of the four quotient direction vectors at `x` to the equal global quotient vector at `y`. Enumerate that map in every pair of local `D4` frames; retain candidates satisfying forward continuation, reverse inverse, transverse-square preservation, and metric isometry.

Use exact signed-permutation matrices only:

```python
D4 = tuple(
    matrix
    for matrix in signed_permutation_matrices(2)
    if matmul(transpose(matrix), matrix) == identity(2)
)
assert len(D4) == 8
```

- [ ] **Step 2: Quotient global assignments by local gauge**

Gauge-fix only for orbit enumeration: select a graph spanning tree, set its transport representatives to identity by vertex `D4` actions, and enumerate residual candidates on non-tree edges. Record the total assignment count and canonical orbit signatures; never expose the chosen root/tree as scientific output. Require exactly one orbit to proceed.

Add a synthetic connection with one reflected non-tree edge and assert it produces a distinct holonomy signature rather than being erased by gauge fixing.

- [ ] **Step 3: Compute exact holonomy classes**

For each canonical cycle `(x0,x1,x2,x3)`, multiply transports in path order. Store the `D4` conjugacy class as the sorted tuple of all `G H G^-1`. Require reversal to produce the inverse class and all frame choices to produce the same class. Baseline flatness means every class contains `identity(2)`.

- [ ] **Step 4: Test relabeling and scale covariance**

Reconstruct the complex at scales `1` and `7/3` and after simultaneous `pi` relabeling. Require equal tangent rank, gauge-orbit count, and mapped holonomy multiset. Test a work perturbation that preserves `N_R` but breaks the unique opposite partition; it must stop rather than reuse cached topology.

- [ ] **Step 5: Run focused tests and commit**

Run all five `test_operational_complex.py` tests. Expected: 5 pass. Commit:

```text
feat: identify v15.41 baseline connection up to gauge
```

### Task 4: Solve the exact source-indexed linearized connection

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/linearized_connection.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_linearized_connection.py`

**Interfaces:**
- Consumes: a unique baseline connection, exact response field `u_f`, operational cycles, tangent vectors, and exact algebra.
- Produces:
  - `IsotropicLift(values, invariant_dimension, glues_equivariantly)`
  - `LinearizedConnection(delta_transports, coefficient_rank, augmented_rank, nullity, gauge_dimension, residual_zero, unique_mod_gauge)`
  - `construct_isotropic_lift(complex_, field) -> IsotropicLiftAudit`
  - `solve_linearized_connection(complex_, baseline, lift) -> LinearizedConnectionAudit`
  - `differentiate_holonomy(baseline, perturbation, cycle) -> MatrixQ`.

- [ ] **Step 1: Compute the invariant symmetric-tensor space**

Represent a symmetric 2-by-2 form by `(a,b,c)` for `[[a,b],[b,c]]`. For every `G in D4`, add linear equations for `G.T*h*G-h=0`; compute the exact nullspace and require basis `((1,0,1),)` up to nonzero scale. Construct `h_f(x)=u_f(x) I` without fixing that overall scale.

Test a reduced reflection-only gauge group whose invariant space is larger than one dimension; it must return `NOT_IDENTIFIABLE`.

- [ ] **Step 2: Parameterize every first-order edge transport**

Fix one auxiliary orientation matrix `J=((0,-1),(1,0))`; the reflected choice `-J` is run separately and must give the same projective verdict. For each canonical undirected edge `{x,y}` introduce one rational unknown `a_xy` and define:

```python
delta_P_xy = scale(Fraction(u[x] - u[y], 2), identity(2)) + scale(a_xy, J)
delta_P_yx = scale(-1, delta_P_xy)
```

Verify directly for every direction that

```text
delta_P_xy^T g + g delta_P_xy + u[y] g - u[x] g = 0.
```

- [ ] **Step 3: Assemble first-order Cartan closure equations**

For an oriented chordless cycle with baseline edge vectors `v0,v1,v2,v3`, define first-order coframe vectors `delta_v_i=(u[x_i]/2)v_i`. Transport every edge vector back to `T_x0` using prefix products. Differentiate the exact closure expression

```text
v0 + P_10 v1 + P_10 P_21 v2 + P_10 P_21 P_32 v3 = 0
```

by the product rule. The two components of the derivative are two rational linear equations in all `a_xy`. Add them for both orientations of every cycle, reverse-edge equations, and no coordinate-derived equation.

- [ ] **Step 4: Solve and publish uniqueness data before curvature**

Compute coefficient rank, augmented rank, solution nullity, and exact residual. The finite local `D4` gauge has infinitesimal dimension zero; publish `gauge_dimension=0`. Classify unique only when:

```python
consistent = coefficient_rank == augmented_rank
unique_mod_gauge = consistent and nullity == gauge_dimension
residual_zero = matvec(A, solution) == rhs
```

Zero or multiple solutions returns `CONNECTION_NOT_IDENTIFIABLE`. Do not call `solve_unique` until the rank audit passes.

- [ ] **Step 5: Differentiate holonomy mechanically**

For cycle transports `P0,P1,P2,P3` and perturbations `dP0,dP1,dP2,dP3`, compute:

```python
delta_H = add(
    add(
        matmul(dP3, matmul(P2, matmul(P1, P0))),
        matmul(P3, matmul(dP2, matmul(P1, P0))),
    ),
    add(
        matmul(P3, matmul(P2, matmul(dP1, P0))),
        matmul(P3, matmul(P2, matmul(P1, dP0))),
    ),
)
```

The helper must accept arbitrary exact matrices and must not know the response field or source. Require orientation reversal to transform by exact inverse-linearization and local frame changes by conjugation.

- [ ] **Step 6: Test exact linearity and forbidden imports**

For two distinct fields and `a=2/3`, `b=-5/7`, solve independently and require every edge perturbation and cycle curvature for `a*u_f+b*u_g` to equal the same linear combination. Run the AST forbidden-name test before any family-scale integration.

- [ ] **Step 7: Run focused tests and commit**

Run all five `test_linearized_connection.py` tests. Expected: 5 pass. Commit:

```text
feat: solve v15.41 linearized metric connection
```

### Task 5: Construct the independent target and curvature-source adjudication

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/source_target.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/connection_curvature_gate.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_gate.py`

**Interfaces:**
- Consumes: frozen `FamilyInput`, operational/linearized audits, and target output only at the adjudicator boundary.
- Produces:
  - `SourceTarget(labels, centered_sources, neighbors)`
  - `construct_source_target(centered_sources, signed_support) -> SourceTarget`
  - `ContractionAudit(orbit_count, dimension, weights, curvature_fields)`
  - `enumerate_curvature_contractions(complex_, curvature_by_source) -> ContractionAudit`
  - `classify_gate(protocol_valid, connection_identifiable, map_identifiable, correspondence, control_passes) -> str`
  - `audit() -> dict` and `canonical_json(value) -> str`.

- [ ] **Step 1: Implement the narrow source-target constructor**

Validate exact centered sources and signed support entries in `{-1,0,1}`. Reconstruct `N_B2` with the same mathematical rule as v15.40 but without importing response or connection code. Expose only labels, source vectors, and neighbors.

AST-allow only `dataclasses`, `fractions`, `itertools`, and `__future__`. A hostile object must raise on attempted access to `R`, `N_R`, responses, connection, curvature, coordinates, candidate key, or historical geometry while still constructing successfully from its permitted sequence methods.

- [ ] **Step 2: Enumerate local equivariant curvature contractions**

Create one formal weight variable for each incidence flag `(x,C)` where label `x` lies on cycle `C`. Compute flag orbits under every automorphism already derived from the weighted response metric. Locality forbids all nonincident pairs. Orientation reversal identifies the sign-adjusted cycle coefficient. The admissible weight space is the nullspace of all orbit-equality equations.

Require dimension one after quotienting common scale. Normalize the one basis vector to primitive integer weights with positive first nonzero entry; this normalization is serialization-only. Apply it by:

```python
raw[x] = sum(weight[x, cycle] * curvature[source, cycle] for cycle in incident_cycles[x])
K[source][x] = raw[x] - sum(raw.values(), Fraction(0)) / len(labels)
```

Run both auxiliary orientations and require fields to differ by at most one common nonzero sign.

- [ ] **Step 3: Compare source fields projectively and exactly**

For each size choose the first nonzero target component only to calculate a candidate `alpha_L`, then verify all components of all sources satisfy `K_f=alpha_L*s_f`. Require the same nonzero `alpha_L` for every source at that size. A zero curvature family cannot pass.

This comparison occurs only after `N_R == N_B2`; therefore matched diagonal/step-2 families may report internal connection results but cannot pass the complete gate when their recovered geometry differs from the independent target.

- [ ] **Step 4: Implement frozen controls and scrambles**

Iterate `FAMILY_KEYS` in the inherited order while passing no key to operational functions. Record the first failed stage for metric-inapplicable controls. For the canonical family:

```python
pairing_scramble[f] = curvature_by_source[pi[f]]
cycle_scramble[pi_cycle[cycle]] = curvature_by_source[f][cycle]
```

Require both asymmetric scrambles to fail while simultaneous relabeling maps sources, fields, cycles, and labels equivariantly. The cycle permutation is induced by mapping all four labels and re-canonicalizing the tuple.

- [ ] **Step 5: Implement statuses and next objects exactly**

Use this ordered classifier:

```python
ALLOWED_GATE_STATUSES = (
    "PROTOCOL_INVALID",
    "CONNECTION_NOT_IDENTIFIABLE",
    "CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE",
    "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE",
    "GENERIC_CONNECTION_CURVATURE_RESPONSE",
    "CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES",
)

def classify_gate(protocol, connection, contraction, canonical, controls):
    if not protocol:
        return "PROTOCOL_INVALID"
    if not connection:
        return "CONNECTION_NOT_IDENTIFIABLE"
    if not contraction:
        return "CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE"
    if not canonical:
        return "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE"
    if any(controls.values()):
        return "GENERIC_CONNECTION_CURVATURE_RESPONSE"
    return "CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES"
```

Map each status to the exact next object in specification Section 16.

- [ ] **Step 6: Assemble the exhaustive audit without early scientific sampling**

For all sizes, scales, relabel states, families, and sources, record structural reason codes, tangent ranks, connection orbit counts, baseline holonomy classes, invariant dimensions, equation ranks/nullities, contraction dimensions, `alpha_L`, correspondence booleans, and scramble results. A family may stop its scientific pipeline at the first inapplicable stage, but every family/scale/relabel/size cell must have a ledger row.

- [ ] **Step 7: Run gate tests and commit**

Run the first four `test_gate.py` methods; exclude the committed-ledger test until Task 6. Expected: 4 pass. Commit:

```text
feat: adjudicate v15.41 curvature source correspondence
```

### Task 6: Freeze the result, documentation, and exact-head certification

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/docs/RESULTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/README.md`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_gate.py`
- Modify: `.github/workflows/uqcf-v1541-formal-connection-curvature-source-correspondence.yml`
- Modify: `docs/superpowers/plans/2026-09-19-v1541-formal-connection-curvature-source-correspondence-implementation.md` only to append execution receipts.

**Interfaces:**
- Consumes: deterministic `audit()` output after Tasks 2–5.
- Produces: authoritative JSON, human-readable result boundary, full local verification, and one exact-head Actions certificate.

- [ ] **Step 1: Add canonical JSON CLI and generate once**

Use:

```python
def canonical_json(value):
    return json.dumps(value, sort_keys=True, indent=2, separators=(",", ": ")) + "\n"
```

Support mutually exclusive `--out PATH` and `--check PATH`. Generate:

```bash
python connection_curvature_gate.py --out docs/RESULTS.json
```

After generation, scientific formulas, statuses, thresholds, controls, and comparison rules are frozen. Only protocol defects may be repaired, with a documented receipt.

- [ ] **Step 2: Complete ledger and interpretation assertions**

Require no Python floats recursively and assert every construction firewall counter is zero. Require the new-structure ledger booleans from specification Section 15 exactly, including:

```python
expected = {
    "formal_tangent_carrier_new": True,
    "formal_connection_class_new": True,
    "formal_isotropic_lift_class_new": True,
    "formal_curvature_contraction_class_new": True,
    "historical_connection_used_for_adjudication": False,
    "physical_connection_derived": False,
    "physical_curvature_derived": False,
    "stress_energy_derived": False,
    "spacetime_derived": False,
    "continuum_limit_derived": False,
    "einstein_equations_derived": False,
    "scientific_breakthrough": False,
    "Pillar_3": "OPEN",
}
```

- [ ] **Step 3: Write the result README from the frozen ledger**

Lead with the exact mechanical status. Report connection identifiability, curvature-map identifiability, correspondence, controls, sizes, and exact-head provenance. State explicitly that this is a finite formal candidate or falsification—not a physical connection, spacetime curvature, stress-energy law, continuum result, Newtonian limit, Einstein equation, or breakthrough.

Include reproduction commands:

```bash
python -m unittest -v test_operational_complex.py test_linearized_connection.py test_gate.py
python connection_curvature_gate.py --check docs/RESULTS.json > /tmp/v1541-results.json
cmp docs/RESULTS.json /tmp/v1541-results.json
python -m compileall -q exact_algebra.py response_inputs.py operational_complex.py linearized_connection.py source_target.py connection_curvature_gate.py test_operational_complex.py test_linearized_connection.py test_gate.py
```

- [ ] **Step 4: Run the complete fresh local verification**

Run all 15 v15.41 tests, exact replay/cmp, compileall, and the inherited v15.39/v15.40 suites. Require `15/15` v15.41 tests and `17/17` inherited tests with zero failures. Run `git diff --check` and verify the diff against base contains only additive v15.41 files, the reviewed spec/plan, and workflow.

- [ ] **Step 5: Commit the frozen result**

Commit:

```text
docs: freeze v15.41 formal connection result
```

- [ ] **Step 6: Push once and verify exact-head Actions**

Push the final head through the connected GitHub credential path. Verify the branch reference equals the intended commit SHA, the remote file bytes equal local bytes, PR remains draft/open/unmerged and cleanly mergeable, and the branch workflow succeeds on that exact SHA.

Append the final run ID, job ID, exact head SHA, test counts, replay result, status, and PR state under `Execution receipts`. If appending the receipt changes the head, run one final exact-head certification for the receipt commit.

## Execution receipts

No implementation run has been executed. This section is append-only after plan approval.
