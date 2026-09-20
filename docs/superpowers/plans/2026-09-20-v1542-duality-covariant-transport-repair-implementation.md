# UQCF-GEM v15.42 Duality-Covariant Transport Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build and certify one exact, source-blind, duality-covariant linearized transport protocol on the operational square complex, including a preregistered nonflat manufactured control.

**Architecture:** Create a new additive v15.42 demo whose frozen substrate is byte-identical to the certified v15.41 exact algebra and operational-complex constructor. Separate symbolic selection, typed edge transport, based holonomy, manufactured controls, and authoritative status generation into focused modules; the gate imports no response or source module. Tangent transport is primary and cotangent transport is generated mechanically by pullback, so there is only one connection.

**Tech Stack:** Python 3.13.5; standard-library dataclasses, enum, fractions.Fraction, hashlib, json, pathlib, collections.Counter, ast, and unittest; existing dependency-free exact algebra; NumPy 2.3.5 only for inherited v15.40 regression tests; GitHub Actions on ubuntu-24.04.

**Spec:** docs/superpowers/specs/2026-09-20-v1542-duality-covariant-transport-repair-design.md

## Global Constraints

- Preserve parent head b9c5f29d8687a7dbc2af0595430aa73fbc5b8553 as the exact base of the additive v15.42 work.
- Preserve original v15.41 design blob 6d35aae0ccb6c2584d26d5a83d522b3cc7036728, erratum blob d40d03d9d2498ce54839b15dad00c1505c1a586a, corrected ledger blob 46cae26d91c709fdde4c5cc39cd3cf3908980e97, and approved v15.42 design blob 91f2c66bea982b3180a07c61ccc4bef76e9c031d byte-for-byte.
- Add files only under ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/, the v15.42 spec/plan paths, and one dedicated v15.42 workflow.
- The constructor may consume only labels, adjacency, certified direction classes, opposite-neighbor relations, baseline transport, metric, local D4 frame presentation, and an exact scalar field.
- Never import v15.40 response arrays, response generation, source targets, source labels, historical connection outputs, coordinates, spectra, observational targets, or fitting code into the v15.42 demo.
- Use Fraction arithmetic throughout; reject bools, floats, malformed dimensions, incomplete fields, and non-D4 frame presentations.
- Freeze tangent frame variation at -u/2 and cotangent coframe variation at +u/2. These signs are derived behavior, not configurable options.
- Maintain one tangent connection. Generate every cotangent action mechanically by transpose/pullback; no independent cotangent constructor is permitted.
- Evaluate evidence, type, selection, covariance, constant-null, L5 nonflat, held-out L7, scale, and superposition gates in that order.
- A passing stage may report only TRANSPORT_PROTOCOL_CERTIFIED and APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION.
- All source-correspondence, physical-curvature, stress-energy, Einstein, continuum, spacetime, and breakthrough fields remain false or null; Pillar_3 remains OPEN.
- Retain all 43 inherited v15.39-v15.41 tests, byte-identical v15.41 replay, and exact-head certification.
- PR #53 remains draft, open, and unmerged throughout implementation.

## Review Focus

1. **Local frame changes:** a different D4 frame at every vertex must transform baseline and perturbed transports covariantly, not merely pass a global-frame test. Task 3 tests every D4 action as a one-site change, plus a deterministic mixed local presentation, on every affected edge.
2. **Dual path independence:** cotangent results must be derived from tangent pullback and agree through the pairing identity; a second adjustable constructor would reintroduce the v15.41 ambiguity. Task 4 tests the pairing edge by edge and around every face.
3. **Zero-row false positive:** rank or multiset tests could pass with empty curvature data. Tasks 4 and 5 assert the exact number of faces, explicit nonzero matrices, four nonzero 1/16 faces, eight nonzero 1/64 faces, and independently expanded product derivatives.
4. **Relabeling of the marked control:** the impulse mark must move with the carrier permutation; leaving it on the old integer label would create label-dependent results. Task 5 tests every L5 root and deterministic nontrivial permutations at L5 and L7.
5. **Premature scientific access:** a passing manufactured canary must not make response or source artifacts reachable. Task 6 parses imports/names, injects raising forbidden stages, and requires null scientific fields.

---

## File Map

All demo-relative paths below are under ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/.

- Create exact_algebra.py: byte-identical certified exact matrix and rational linear algebra copied from v15.41 blob c67ea42b61321469f7735ce589f2e729b241666a.
- Create operational_complex.py: byte-identical certified operational-complex and baseline constructor copied from v15.41 blob 8163beba8e52bc2a3a6d0c8cf59dd1257222f65c.
- Create evidence.py: frozen paths/hashes and Git-blob verification with no imports from prior executable demos.
- Create fixtures.py: source-blind periodic square carrier construction and exact relabeling utilities.
- Create protocol_types.py: immutable carrier/action manifest, frame presentation, transport records, and selection-audit records.
- Create selection.py: exact uniqueness proofs for the centered derivative and endpoint average.
- Create transport.py: centered operational derivative and the single tangent transport constructor; cotangent pullback is derived here.
- Create holonomy.py: independently expanded product derivative, based curvature, reversal/basepoint operations, and invariant.
- Create controls.py: constant, impulse, scale, superposition, relabeling, gauge, and duality control records.
- Create protocol_gate.py: ordered hard gates, status mapping, evidence firewall ledger, and deterministic CLI.
- Create test_evidence.py, test_selection.py, test_transport.py, test_holonomy.py, test_controls.py, and test_gate.py: 36 planned behavior tests.
- Create docs/RESULTS.json: canonical exact ledger.
- Create README.md: result, reproduction instructions, claim boundary, and next required object.
- Create .github/workflows/uqcf-v1542-duality-covariant-transport-repair.yml: additive-scope, v15.42, inherited, replay, and compilation certification.
- Modify this plan only to append immutable execution receipts after implementation; never rewrite approved plan text.

### Task 1: Freeze evidence and the source-blind operational substrate

**Files:**
- Create: exact_algebra.py
- Create: operational_complex.py
- Create: evidence.py
- Create: fixtures.py
- Create: test_evidence.py

**Interfaces:**
- Consumes: repository files at the four frozen evidence paths and the certified v15.41 exact/operational modules.
- Produces: verify_evidence() -> dict[str, str], periodic_square_input(L: int, labels: tuple[int, ...] | None = None), relabel_input(data, permutation), relabeled_edges(data, permutation), and byte-identical exact_algebra/operational_complex modules.

- [ ] **Step 1: Write four failing evidence/substrate tests**

~~~python
class EvidenceTests(unittest.TestCase):
    def test_parent_evidence_blobs_are_exact(self):
        self.assertEqual(
            verify_evidence(),
            {
                "v15.41-design": "6d35aae0ccb6c2584d26d5a83d522b3cc7036728",
                "v15.41-erratum": "d40d03d9d2498ce54839b15dad00c1505c1a586a",
                "v15.41-results": "46cae26d91c709fdde4c5cc39cd3cf3908980e97",
                "v15.42-design": "91f2c66bea982b3180a07c61ccc4bef76e9c031d",
            },
        )

    def test_vendored_substrate_matches_certified_blobs(self):
        self.assertEqual(git_blob_sha(Path("exact_algebra.py")),
                         "c67ea42b61321469f7735ce589f2e729b241666a")
        self.assertEqual(git_blob_sha(Path("operational_complex.py")),
                         "8163beba8e52bc2a3a6d0c8cf59dd1257222f65c")

    def test_fixture_constructs_exact_source_blind_carriers(self):
        for L in (5, 7):
            audit = construct_operational_complex(*periodic_square_input(L))
            self.assertEqual(audit.status, ConnectionStatus.IDENTIFIABLE)
            self.assertEqual(len(audit.complex.labels), L * L)
            self.assertEqual(len(audit.complex.cycles), L * L)

    def test_fixture_relabeling_carries_labels_without_changing_work(self):
        original = periodic_square_input(5)
        permutation = tuple(reversed(range(25)))
        changed = relabel_input(original, permutation)
        self.assertEqual(changed[0], permutation)
        self.assertEqual(sorted(map(sorted, changed[2])),
                         sorted(map(sorted, relabeled_edges(original, permutation))))
~~~

- [ ] **Step 2: Run RED**

Run from the new demo directory:

~~~bash
python -m unittest -v test_evidence.py
~~~

Expected: import failure for missing evidence and fixtures modules. Record the command, four test names, exit code, and head SHA.

- [ ] **Step 3: Copy the two certified substrate modules byte-for-byte**

~~~bash
cp ../v15.41-formal-connection-curvature-source-correspondence/exact_algebra.py exact_algebra.py
cp ../v15.41-formal-connection-curvature-source-correspondence/operational_complex.py operational_complex.py
~~~

Immediately compute Git blob hashes and stop if either differs from the values above.

- [ ] **Step 4: Implement exact evidence verification**

~~~python
from hashlib import sha1
from pathlib import Path

EVIDENCE = {
    "v15.41-design": (
        "../../../../docs/superpowers/specs/"
        "2026-09-19-v1541-formal-connection-curvature-source-correspondence-design.md",
        "6d35aae0ccb6c2584d26d5a83d522b3cc7036728",
    ),
    "v15.41-erratum": (
        "../../../../docs/superpowers/specs/"
        "2026-09-20-v1541-transport-protocol-erratum-design.md",
        "d40d03d9d2498ce54839b15dad00c1505c1a586a",
    ),
    "v15.41-results": (
        "../v15.41-formal-connection-curvature-source-correspondence/docs/RESULTS.json",
        "46cae26d91c709fdde4c5cc39cd3cf3908980e97",
    ),
    "v15.42-design": (
        "../../../../docs/superpowers/specs/"
        "2026-09-20-v1542-duality-covariant-transport-repair-design.md",
        "91f2c66bea982b3180a07c61ccc4bef76e9c031d",
    ),
}

def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def verify_evidence() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    observed = {}
    for key, (relative, expected) in EVIDENCE.items():
        actual = git_blob_sha((root / relative).resolve())
        if actual != expected:
            raise ValueError(f"evidence mismatch: {key}")
        observed[key] = actual
    return observed
~~~

- [ ] **Step 5: Implement source-blind periodic fixtures**

Move only the periodic square work/edge construction from the v15.41 test helper into fixtures.py. Accept arbitrary integer labels, validate a bijection, and rebuild work and edges by position so a relabeling carries all structure. Do not import response_inputs.py or source_target.py.

- [ ] **Step 6: Run GREEN and the inherited operational tests**

~~~bash
python -m unittest -v test_evidence.py
python ../v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py
~~~

Expected: 4/4 new tests pass and all inherited operational tests pass.

- [ ] **Step 7: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair
git commit -m "test(uqcf): freeze v15.42 transport substrate"
~~~

### Task 2: Prove the selection axioms and freeze typed manifests

**Files:**
- Create: protocol_types.py
- Create: selection.py
- Create: test_selection.py

**Interfaces:**
- Consumes: exact Fraction rank/solve functions.
- Produces: CarrierKind, MatrixAction, TypedMap, TransportManifest.certified(), SelectionAudit, audit_centered_stencil(), audit_endpoint_average(), and audit_selection() -> SelectionAudit.

- [ ] **Step 1: Write five failing tests**

~~~python
def test_certified_manifest_types_every_map_and_sign():
    manifest = TransportManifest.certified()
    self.assertEqual(manifest.tangent_forward,
                     TypedMap("T_x", "T_y", MatrixAction.DIRECT))
    self.assertEqual(manifest.tangent_reverse,
                     TypedMap("T_y", "T_x", MatrixAction.INVERSE))
    self.assertEqual(manifest.cotangent_pullback,
                     TypedMap("T_y*", "T_x*", MatrixAction.TRANSPOSE))
    self.assertEqual(manifest.cotangent_reverse,
                     TypedMap("T_x*", "T_y*", MatrixAction.INVERSE_TRANSPOSE))
    self.assertEqual(manifest.frame_variation_sign, -1)
    self.assertEqual(manifest.coframe_variation_sign, 1)

def test_every_manifest_substitution_is_rejected():
    manifest = TransportManifest.certified()
    changes = (
        {"carrier_pair": (CarrierKind.COVECTOR, CarrierKind.COVECTOR)},
        {"frame_variation_sign": 1},
        {"coframe_variation_sign": -1},
        {"basepoint_rule": "output_selected"},
        {"orientation_rule": "forward_only"},
        {"cotangent_pullback": TypedMap("T_y*", "T_x*", MatrixAction.INVERSE_TRANSPOSE)},
        {"cotangent_reverse": TypedMap("T_x*", "T_y*", MatrixAction.TRANSPOSE)},
    )
    for change in changes:
        with self.subTest(change=change), self.assertRaises(ValueError):
            replace(manifest, **change).validate()

def test_centered_stencil_is_uniquely_selected():
    audit = audit_centered_stencil()
    self.assertTrue(audit.identifiable)
    self.assertEqual(audit.solution, (Fraction(1, 2), Fraction(0), Fraction(-1, 2)))
    self.assertEqual((audit.rank, audit.unknowns), (3, 3))

def test_endpoint_average_is_uniquely_selected():
    audit = audit_endpoint_average()
    self.assertTrue(audit.identifiable)
    self.assertEqual(audit.solution, (Fraction(1, 2), Fraction(1, 2)))
    self.assertEqual((audit.rank, audit.unknowns), (2, 2))

def test_missing_affine_or_normalization_axiom_is_not_identifiable():
    self.assertFalse(audit_centered_stencil(drop="affine_exact").identifiable)
    self.assertFalse(audit_endpoint_average(drop="constant_exact").identifiable)
~~~

- [ ] **Step 2: Run RED**

~~~bash
python -m unittest -v test_selection.py
~~~

Expected: import failure for protocol_types and selection.

- [ ] **Step 3: Implement immutable types**

~~~python
class CarrierKind(str, Enum):
    TANGENT_VECTOR = "tangent_vector"
    COVECTOR = "covector"

class MatrixAction(str, Enum):
    DIRECT = "direct"
    INVERSE = "inverse"
    TRANSPOSE = "transpose"
    INVERSE_TRANSPOSE = "inverse_transpose"

@dataclass(frozen=True)
class TypedMap:
    domain: str
    codomain: str
    action: MatrixAction

@dataclass(frozen=True)
class TransportManifest:
    carrier_pair: tuple[CarrierKind, CarrierKind]
    tangent_forward: TypedMap
    tangent_reverse: TypedMap
    cotangent_pullback: TypedMap
    cotangent_reverse: TypedMap
    frame_variation_sign: int
    coframe_variation_sign: int
    basepoint_rule: str
    orientation_rule: str

    @classmethod
    def certified(cls):
        return cls(
            (CarrierKind.TANGENT_VECTOR, CarrierKind.COVECTOR),
            TypedMap("T_x", "T_y", MatrixAction.DIRECT),
            TypedMap("T_y", "T_x", MatrixAction.INVERSE),
            TypedMap("T_y*", "T_x*", MatrixAction.TRANSPOSE),
            TypedMap("T_x*", "T_y*", MatrixAction.INVERSE_TRANSPOSE),
            -1, 1, "based_holonomy_conjugacy", "both_orientations",
        )

    def validate(self):
        if self != type(self).certified():
            raise ValueError("manifest differs from the approved v15.42 protocol")
        return True
~~~

- [ ] **Step 4: Implement exact symbolic selection audits**

Represent derivative weights as (w_plus, w_center, w_minus). Use exact equations constant: w_plus+w_center+w_minus=0, oddness: w_center=0 and w_plus+w_minus=0, affine exactness: w_plus-w_minus=1. Represent edge weights as (a,b) with a+b=1 and a-b=0. Use exact rank and solve_unique; when a named axiom is dropped, return identifiable=False rather than selecting a free parameter. audit_selection() must contain the two component audits and set identifiable to their conjunction; no later task may recompute or override that verdict.

- [ ] **Step 5: Run GREEN**

~~~bash
python -m unittest -v test_selection.py
~~~

Expected: 5/5 pass.

- [ ] **Step 6: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/protocol_types.py \
        ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/selection.py \
        ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/test_selection.py
git commit -m "feat(uqcf): freeze v15.42 transport selection"
~~~

### Task 3: Construct the exact tangent transport

**Files:**
- Create: transport.py
- Create: test_transport.py

**Interfaces:**
- Consumes: OperationalComplex, BaselineConnection, exact field tuple, TransportManifest, and optional FramePresentation.
- Produces: FramePresentation.identity(complex_), centered_derivatives(complex_: OperationalComplex, baseline: BaselineConnection, field: tuple[Fraction, ...], presentation: FramePresentation) -> tuple[tuple[int, Vector2], ...], construct_transport(complex_: OperationalComplex, baseline: BaselineConnection, field: tuple[Fraction, ...], manifest: TransportManifest | None = None, presentation: FramePresentation | None = None) -> LinearizedTransport, and cotangent_pullback_delta(matrix: Matrix2) -> Matrix2.

- [ ] **Step 1: Write seven failing transport tests**

Tests must cover:

~~~python
class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex = construct_operational_complex(*periodic_square_input(5)).complex
        cls.baseline = enumerate_baseline_connection(cls.complex).connection
        cls.impulse = tuple(Fraction(index == 0) for index in range(25))

    def test_constant_field_has_zero_edge_variation(self):
        result = construct_transport(
            self.complex, self.baseline, (Fraction(7, 3),) * 25
        )
        zero = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
        self.assertTrue(all(value == zero for _edge, value in result.tangent_deltas))

    def test_field_validation_rejects_float_bool_and_wrong_dimension(self):
        for field in ((Fraction(0),) * 24, (0.0,) * 25, (False,) * 25):
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                construct_transport(self.complex, self.baseline, field)

    def test_metric_compatibility_is_exact_on_every_directed_edge(self):
        result = construct_transport(self.complex, self.baseline, self.impulse)
        self.assertTrue(result.metric_compatibility_exact)
        self.assertEqual(len(result.tangent_deltas), len(self.complex.directed_edges))
        directions = dict(zip(self.complex.directed_edges,
                              self.complex.direction_classes))
        edge = next(edge for edge in self.complex.directed_edges
                    if edge[0] == 0
                    and directions[edge] == (Fraction(1), Fraction(0)))
        self.assertEqual(
            dict(result.source_endomorphisms)[edge],
            ((Fraction(1, 2), Fraction(0)),
             (Fraction(0), Fraction(1, 2))),
        )

    def test_reverse_edge_is_derivative_of_inverse_transport(self):
        result = construct_transport(self.complex, self.baseline, self.impulse)
        self.assertTrue(result.reversal_exact)
        by_edge = dict(result.source_endomorphisms)
        p = dict(result.baseline)
        for x, y in self.complex.directed_edges:
            self.assertEqual(by_edge[(y, x)],
                             scale(-1, matmul(p[(x, y)],
                                              matmul(by_edge[(x, y)], p[(y, x)]))))

    def test_frame_and_coframe_signs_are_derived_not_arguments(self):
        parameters = inspect.signature(construct_transport).parameters
        self.assertNotIn("frame_variation_sign", parameters)
        self.assertNotIn("coframe_variation_sign", parameters)
        self.assertEqual(TransportManifest.certified().frame_variation_sign, -1)
        self.assertEqual(TransportManifest.certified().coframe_variation_sign, 1)

    def test_every_local_d4_frame_change_is_covariant(self):
        identity_result = construct_transport(self.complex, self.baseline, self.impulse)
        presentations = [deterministic_mixed_presentation(self.complex)]
        presentations.extend(
            one_site_presentations(self.complex, label=0)
        )
        for presentation in presentations:
            actual = construct_transport(
                self.complex, self.baseline, self.impulse,
                presentation=presentation,
            )
            self.assertEqual(actual, gauge_transform(identity_result, presentation))

    def test_relabeling_commutes_with_transport_construction(self):
        permutation = tuple((7 * index + 3) % 25 for index in range(25))
        relabeled_complex, relabeled_baseline, relabeled_field = relabeled_problem(
            self.complex, self.baseline, self.impulse, permutation
        )
        actual = construct_transport(
            relabeled_complex, relabeled_baseline, relabeled_field
        )
        expected = relabel_transport(
            construct_transport(self.complex, self.baseline, self.impulse),
            permutation,
        )
        self.assertEqual(actual, expected)
~~~

Use literal expected matrices on a hand-checked L5 impulse edge. For root 0 with the standard fixture, assert the full 2x2 Fraction matrix rather than recomputing the expectation through construct_transport.

- [ ] **Step 2: Run RED**

~~~bash
python -m unittest -v test_transport.py
~~~

Expected: import failure for transport.

- [ ] **Step 3: Implement frame presentations and validation**

~~~python
@dataclass(frozen=True)
class FramePresentation:
    gauges: tuple[tuple[int, Matrix2], ...]

    @classmethod
    def identity(cls, complex_):
        return cls(tuple((label, identity(2)) for label in complex_.labels))

@dataclass(frozen=True)
class LinearizedTransport:
    manifest: TransportManifest
    baseline: tuple[tuple[tuple[int, int], Matrix2], ...]
    source_endomorphisms: tuple[tuple[tuple[int, int], Matrix2], ...]
    tangent_deltas: tuple[tuple[tuple[int, int], Matrix2], ...]
    cotangent_pullback_deltas: tuple[tuple[tuple[int, int], Matrix2], ...]
    metric_compatibility_exact: bool
    reversal_exact: bool
~~~

Validate that gauges contain each label exactly once and every matrix is one of complex_.d4_actions.

- [ ] **Step 4: Implement the centered operational derivative**

For each vertex, locate the unique neighbors with direction d1, -d1, d2, and -d2 in that vertex's presented frame. Solve the two metric pairings exactly for q_x. Do not infer an orientation or use label arithmetic.

- [ ] **Step 5: Implement the frozen edge formula**

~~~python
def construct_transport(complex_, baseline, field, manifest=None, presentation=None):
    manifest = manifest or TransportManifest.certified()
    manifest.validate()
    field_by_label = validate_exact_field(complex_, field)
    presentation = presentation or FramePresentation.identity(complex_)
    q = centered_derivatives(complex_, baseline, field, presentation)
    for x, y in complex_.directed_edges:
        p_xy = presented_baseline[(x, y)]
        p_yx = presented_baseline[(y, x)]
        direction = presented_direction[(x, y)]
        q_bar = scale(Fraction(1, 2), add_vector(q[x], matvec(p_yx, q[y])))
        skew = scale(
            Fraction(1, 2),
            add(outer(q_bar, lower(direction)),
                scale(-1, outer(direction, lower(q_bar)))),
        )
        b_xy = add(scale((field_by_label[x] - field_by_label[y]) / 2,
                         identity(2)), skew)
        delta_p = matmul(p_xy, b_xy)
~~~

Store the reverse and cotangent records mechanically. Verify exact differentiated metric compatibility and reversal before returning.

- [ ] **Step 6: Run GREEN and mutation checks**

~~~bash
python -m unittest -v test_transport.py
~~~

Expected: 7/7 pass. Temporarily flip either conformal sign, omit endpoint transport in q_bar, or replace one-half by one; at least one named test must fail for each mutation. Restore the code and rerun 7/7.

- [ ] **Step 7: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/transport.py \
        ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/test_transport.py
git commit -m "feat(uqcf): construct duality-covariant transport"
~~~

### Task 4: Differentiate holonomy and prove presentation covariance

**Files:**
- Create: holonomy.py
- Create: test_holonomy.py

**Interfaces:**
- Consumes: BaselineConnection, LinearizedTransport, and an oriented four-cycle.
- Produces: linearized_holonomy(baseline: BaselineConnection, transport: LinearizedTransport, cycle: tuple[int, int, int, int]) -> Matrix2, reverse_cycle(cycle) -> tuple[int, int, int, int], rotate_cycle(cycle, steps: int) -> tuple[int, int, int, int], cotangent_holonomy(baseline, transport, cycle) -> Matrix2, curvature_invariant(matrix: Matrix2) -> Fraction, and CurvatureRecord.

- [ ] **Step 1: Write six failing holonomy tests**

~~~python
class HolonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complex, cls.baseline, cls.transport = impulse_problem(5, root=0)
        cls.cycle = cls.complex.cycles[0]

    def test_product_derivative_matches_independent_four_term_expansion(self):
        p, d = dict(self.baseline.transports), dict(self.transport.tangent_deltas)
        edges = tuple((self.cycle[i], self.cycle[(i + 1) % 4]) for i in range(4))
        p0, p1, p2, p3 = (p[edge] for edge in edges)
        d0, d1, d2, d3 = (d[edge] for edge in edges)
        expected = add(
            add(matmul(d3, matmul(p2, matmul(p1, p0))),
                matmul(p3, matmul(d2, matmul(p1, p0)))),
            add(matmul(p3, matmul(p2, matmul(d1, p0))),
                matmul(p3, matmul(p2, matmul(p1, d0)))),
        )
        self.assertEqual(
            linearized_holonomy(self.baseline, self.transport, self.cycle),
            expected,
        )

    def test_cyclic_basepoints_are_baseline_conjugate(self):
        first = linearized_holonomy(self.baseline, self.transport, self.cycle)
        p = dict(self.baseline.transports)
        for steps in (1, 2, 3):
            changed = rotate_cycle(self.cycle, steps)
            bridge = path_transport(p, self.cycle, steps)
            self.assertEqual(
                linearized_holonomy(self.baseline, self.transport, changed),
                matmul(bridge, matmul(first, transpose(bridge))),
            )

    def test_reversal_is_negative_at_flat_baseline(self):
        forward = linearized_holonomy(self.baseline, self.transport, self.cycle)
        reverse = linearized_holonomy(
            self.baseline, self.transport, reverse_cycle(self.cycle)
        )
        self.assertEqual(reverse, scale(-1, forward))

    def test_local_d4_gauge_conjugates_based_curvature(self):
        presentation = deterministic_mixed_presentation(self.complex)
        changed = construct_transport(
            self.complex, self.baseline, impulse_field(5, 0),
            presentation=presentation,
        )
        gauge = dict(presentation.gauges)[self.cycle[0]]
        expected = matmul(
            gauge,
            matmul(
                linearized_holonomy(self.baseline, self.transport, self.cycle),
                transpose(gauge),
            ),
        )
        self.assertEqual(
            linearized_holonomy(presented_baseline(self.baseline, presentation),
                                changed, self.cycle),
            expected,
        )

    def test_tangent_and_cotangent_paths_preserve_pairing(self):
        tangent = linearized_holonomy(self.baseline, self.transport, self.cycle)
        cotangent = cotangent_holonomy(
            self.baseline, self.transport, self.cycle
        )
        for vector in ((Fraction(1), Fraction(0)), (Fraction(2), Fraction(-3))):
            for covector in ((Fraction(0), Fraction(1)), (Fraction(5), Fraction(7))):
                self.assertEqual(pair(matvec(tangent, vector), covector),
                                 pair(vector, matvec(cotangent, covector)))

    def test_curvature_invariant_is_exact_and_presentation_independent(self):
        value = ((Fraction(0), Fraction(-1, 4)),
                 (Fraction(1, 4), Fraction(0)))
        self.assertEqual(curvature_invariant(value), Fraction(1, 16))
        for action in self.complex.d4_actions:
            changed = matmul(action, matmul(value, transpose(action)))
            self.assertEqual(curvature_invariant(changed), Fraction(1, 16))
~~~

The first test must build the four terms directly in the test from literal baseline/delta dictionaries. It must not call a helper from holonomy.py to compute the expected value.

- [ ] **Step 2: Run RED**

~~~bash
python -m unittest -v test_holonomy.py
~~~

Expected: import failure for holonomy.

- [ ] **Step 3: Implement the product derivative**

~~~python
def linearized_holonomy(baseline, transport, cycle):
    p = dict(baseline.transports)
    d = dict(transport.tangent_deltas)
    edges = tuple((cycle[i], cycle[(i + 1) % 4]) for i in range(4))
    p0, p1, p2, p3 = (p[e] for e in edges)
    d0, d1, d2, d3 = (d[e] for e in edges)
    return add(
        add(matmul(d3, matmul(p2, matmul(p1, p0))),
            matmul(p3, matmul(d2, matmul(p1, p0)))),
        add(matmul(p3, matmul(p2, matmul(d1, p0))),
            matmul(p3, matmul(p2, matmul(p1, d0)))),
    )
~~~

Validate four distinct vertices and all required directed edges.

- [ ] **Step 4: Implement dual and invariant operations**

Cotangent holonomy must be obtained from pullbacks, not a second formula with adjustable choices. For a based tangent loop H, verify the covector loop acts by H transpose on the dual and that the bilinear pairing derivative agrees. Define:

~~~python
def curvature_invariant(value):
    square = matmul(value, value)
    return -(square[0][0] + square[1][1]) / 2
~~~

Reject a curvature matrix whose symmetric part is nonzero; do not hide it behind the invariant.

- [ ] **Step 5: Run GREEN and all transport tests**

~~~bash
python -m unittest -v test_transport.py test_holonomy.py
~~~

Expected: 13/13 pass.

- [ ] **Step 6: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/holonomy.py \
        ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/test_holonomy.py
git commit -m "feat(uqcf): certify typed linearized holonomy"
~~~

### Task 5: Execute the manufactured nonflat control family

**Files:**
- Create: controls.py
- Create: test_controls.py

**Interfaces:**
- Consumes: source-blind fixtures, construct_transport, linearized_holonomy, and curvature_invariant.
- Produces: constant_control(L: int, value: Fraction) -> ControlResult, impulse_control(L: int, root: int, amplitude: Fraction, presentation: FramePresentation | None = None) -> ControlResult, superposition_control(L: int, left: tuple[Fraction, ...], right: tuple[Fraction, ...], a: Fraction, b: Fraction) -> bool, ControlStage, ControlExecutors.default(), and run_control_family(executors: ControlExecutors | None = None) -> ControlFamily.

- [ ] **Step 1: Write seven failing control tests**

~~~python
class ControlTests(unittest.TestCase):
    def test_constant_fields_are_flat_at_l5_and_l7(self):
        for L in (5, 7):
            for value in (Fraction(0), Fraction(7, 3)):
                result = constant_control(L, value)
                self.assertEqual(result.invariant_counts,
                                 ((Fraction(0), L * L),))
                self.assertTrue(all(matrix == ZERO for matrix in result.curvatures))

    def test_l5_impulse_has_frozen_nonflat_multiset(self):
        result = impulse_control(5, root=0, amplitude=Fraction(1))
        self.assertEqual(dict(result.invariant_counts), {
            Fraction(1, 16): 4, Fraction(1, 64): 8, Fraction(0): 13,
        })
        self.assertEqual(sum(matrix != ZERO for matrix in result.curvatures), 12)

    def test_l7_holdout_has_frozen_nonflat_multiset(self):
        result = impulse_control(7, root=0, amplitude=Fraction(1))
        self.assertEqual(dict(result.invariant_counts), {
            Fraction(1, 16): 4, Fraction(1, 64): 8, Fraction(0): 37,
        })
        self.assertEqual(sum(matrix != ZERO for matrix in result.curvatures), 12)

    def test_every_l5_marked_vertex_has_the_same_multiset(self):
        expected = impulse_control(5, 0, Fraction(1)).invariant_counts
        self.assertEqual(
            {impulse_control(5, root, Fraction(1)).invariant_counts
             for root in range(25)},
            {expected},
        )

    def test_exact_scale_law_at_one_and_seven_thirds(self):
        unit = impulse_control(5, 0, Fraction(1))
        scaled = impulse_control(5, 0, Fraction(7, 3))
        self.assertEqual(
            scaled.curvatures,
            tuple(scale(Fraction(7, 3), value) for value in unit.curvatures),
        )
        self.assertEqual(
            dict(scaled.invariant_counts),
            {key * Fraction(49, 9): count
             for key, count in unit.invariant_counts},
        )

    def test_transport_and_curvature_are_linear_under_superposition(self):
        left = impulse_field(5, 0)
        right = impulse_field(5, 7)
        self.assertTrue(superposition_control(
            5, left, right, Fraction(2, 3), Fraction(-5, 7)
        ))

    def test_relabel_gauge_basepoint_orientation_and_dual_controls_all_pass(self):
        family = run_control_family()
        self.assertTrue(family.covariance_exact)
        self.assertTrue(family.every_root_equivalent)
        self.assertEqual(len(family.results), 29)
~~~

Use exact expected Counters:

~~~python
self.assertEqual(result.invariant_counts, {
    Fraction(1, 16): 4,
    Fraction(1, 64): 8,
    Fraction(0): L * L - 12,
})
self.assertEqual(len(result.curvatures), L * L)
self.assertEqual(sum(value != ZERO for value in result.curvatures), 12)
~~~

The nonzero matrix count prevents an empty/zero-row implementation from passing the multiset assertion.

- [ ] **Step 2: Run RED**

~~~bash
python -m unittest -v test_controls.py
~~~

Expected: import failure for controls.

- [ ] **Step 3: Implement immutable control records**

~~~python
@dataclass(frozen=True)
class ControlResult:
    L: int
    root: int | None
    amplitude: Fraction
    curvatures: tuple[Matrix2, ...]
    invariant_counts: tuple[tuple[Fraction, int], ...]
    all_covariances_exact: bool

@dataclass(frozen=True)
class ControlStage:
    passed: bool
    results: tuple[ControlResult, ...] = ()

@dataclass(frozen=True)
class ControlExecutors:
    covariance: Callable[[], ControlStage]
    constant_null: Callable[[], ControlStage]
    l5_nonflat: Callable[[], ControlStage]
    l7_holdout_nonflat: Callable[[], ControlStage]
    scale_exact: Callable[[], ControlStage]
    superposition_exact: Callable[[], ControlStage]

    @classmethod
    def default(cls):
        # Bind the six production stage functions in certified order.
        ...

@dataclass(frozen=True)
class ControlFamily:
    covariance_exact: bool | None
    constant_null: bool | None
    l5_nonflat: bool | None
    l7_holdout_nonflat: bool | None
    every_root_equivalent: bool | None
    scale_exact: bool | None
    superposition_exact: bool | None
    results: tuple[ControlResult, ...]
    failed_stage: str | None

    @property
    def all_required_pass(self):
        return all(value is True for value in (
            self.covariance_exact, self.constant_null, self.l5_nonflat,
            self.l7_holdout_nonflat, self.every_root_equivalent,
            self.scale_exact, self.superposition_exact,
        ))
~~~

Serialize Counters as sorted tuples to preserve deterministic JSON order.

- [ ] **Step 4: Implement the controls without source terminology**

The impulse field helper accepts only a carrier and a marked control vertex. Names, docstrings, ledger keys, and imports must use control_root or marked_vertex, never source, mass, stress, or target. Carry the marked vertex through relabeling. run_control_family() invokes ControlExecutors stages strictly in this order: covariance, constant-null, L5 nonflat/every-root, held-out L7, scale, superposition. It returns immediately on the first failed stage; later status fields are None and later callables are never invoked. A successful default run stores results in this exact order: constant L5 at 7/3, constant L7 at 7/3, all 25 unit L5 roots in label order, the unit L7 root 0 holdout, and the L5 root 0 amplitude-7/3 scale case. The tuple therefore contains exactly 29 records.

- [ ] **Step 5: Run GREEN and the complete mathematical suite**

~~~bash
python -m unittest -v test_evidence.py test_selection.py test_transport.py \
  test_holonomy.py test_controls.py
~~~

Expected: 29/29 pass.

- [ ] **Step 6: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/controls.py \
        ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair/test_controls.py
git commit -m "test(uqcf): add exact nonflat transport canary"
~~~

### Task 6: Build the ordered gate and canonical ledger

**Files:**
- Create: protocol_gate.py
- Create: test_gate.py
- Create: docs/RESULTS.json
- Create: README.md

**Interfaces:**
- Consumes: verify_evidence, manifest validation, selection audits, transport identities, and ControlFamily.
- Produces: audit() -> dict, _audit(evidence_verifier: Callable = verify_evidence, manifest_factory: Callable = TransportManifest.certified, selection_auditor: Callable = audit_selection, control_runner: Callable = run_control_family) -> dict, write_result(path: Path) -> None, and CLI flags --out and --check.

- [ ] **Step 1: Write seven failing gate tests**

~~~python
class GateTests(unittest.TestCase):
    def test_all_exact_gates_produce_protocol_certified(self):
        result = audit()
        self.assertEqual(result["status"], "TRANSPORT_PROTOCOL_CERTIFIED")
        self.assertEqual(
            result["next_required_object"],
            "APPLY_CERTIFIED_TRANSPORT_TO_RESPONSE_GEOMETRY_WITHOUT_SOURCE_ADJUDICATION",
        )

    def test_type_or_covariance_failure_returns_protocol_invalid(self):
        def bad_manifest():
            raise ValueError("manifest mismatch")
        failed = replace(run_control_family(), covariance_exact=False)
        for arguments in (
            {"manifest_factory": bad_manifest},
            {"control_runner": lambda: failed},
        ):
            with self.subTest(arguments=tuple(arguments)):
                result = _audit(**arguments)
                self.assertEqual(result["status"], "PROTOCOL_INVALID")
                self.assertEqual(result["next_required_object"],
                                 "REPAIR_PROTOCOL_BEFORE_ANY_APPLICATION")

    def test_nonunique_selection_returns_protocol_not_identifiable(self):
        ambiguous = replace(audit_selection(), identifiable=False)
        result = _audit(
            selection_auditor=lambda: ambiguous,
            control_runner=lambda: self.fail("controls ran after ambiguity"),
        )
        self.assertEqual(result["status"], "PROTOCOL_NOT_IDENTIFIABLE")

    def test_failed_nonflat_canary_stops_before_later_stages(self):
        calls = []
        def stage(name, passed):
            return lambda: (calls.append(name) or ControlStage(passed))
        def forbidden(name):
            return lambda: self.fail(f"{name} ran after L5 failure")
        executors = ControlExecutors(
            covariance=stage("covariance", True),
            constant_null=stage("constant-null", True),
            l5_nonflat=stage("L5", False),
            l7_holdout_nonflat=forbidden("L7"),
            scale_exact=forbidden("scale"),
            superposition_exact=forbidden("superposition"),
        )
        result = _audit(
            control_runner=lambda: run_control_family(executors=executors)
        )
        self.assertEqual(calls, ["covariance", "constant-null", "L5"])
        self.assertEqual(result["failed_gate"], "l5_nonflat")
        self.assertFalse(result["response_geometry_applied"])
        self.assertFalse(result["source_target_constructed"])
        self.assertFalse(result["source_correspondence_evaluated"])

    def test_import_and_name_firewall_excludes_response_source_and_physics(self):
        forbidden = {
            "response_inputs", "response_generation", "source_target",
            "coordinates", "spectrum", "numpy", "newton", "einstein",
            "observational", "fit", "svd", "eig", "pinv",
        }
        observed = production_imports_and_names(PRODUCTION_FILES)
        self.assertTrue(observed.isdisjoint(forbidden), observed)

    def test_evidence_failure_stops_before_protocol_construction(self):
        def bad_evidence():
            raise ValueError("evidence mismatch")
        result = _audit(
            evidence_verifier=bad_evidence,
            manifest_factory=lambda: self.fail("manifest ran"),
            selection_auditor=lambda: self.fail("selection ran"),
            control_runner=lambda: self.fail("controls ran"),
        )
        self.assertEqual(result["status"], "PROTOCOL_INVALID")
        self.assertEqual(result["failed_gate"], "evidence")

    def test_committed_ledger_is_exact_float_free_and_byte_stable(self):
        expected = json.loads(Path("docs/RESULTS.json").read_text())
        actual = audit()
        self.assertEqual(actual, expected)
        self.assertFalse(contains_float(actual))
        rendered = render_result(actual)
        self.assertEqual(rendered, Path("docs/RESULTS.json").read_text())
~~~

For fail-fast tests, inject callables that raise AssertionError if a later stage is reached. Recursively reject float values. Parse evidence.py, protocol_types.py, selection.py, transport.py, holonomy.py, controls.py, and protocol_gate.py with ast and reject imports/names containing response_inputs, response_generation, source_target, coordinates, spectrum, numpy, newton, einstein, observational, fit, svd, eig, or pinv.

- [ ] **Step 2: Run RED**

~~~bash
python -m unittest -v test_gate.py
~~~

Expected: import failure for protocol_gate.

- [ ] **Step 3: Implement strict gate ordering**

~~~python
def _audit(evidence_verifier=verify_evidence,
           manifest_factory=TransportManifest.certified,
           selection_auditor=audit_selection,
           control_runner=run_control_family):
    try:
        evidence = evidence_verifier()
    except (OSError, ValueError) as error:
        return invalid_ledger("evidence", str(error))
    try:
        manifest = manifest_factory()
        manifest.validate()
    except (TypeError, ValueError) as error:
        return invalid_ledger("manifest", str(error), evidence=evidence)
    selection = selection_auditor()
    if not selection.identifiable:
        return stopped_ledger(
            "PROTOCOL_NOT_IDENTIFIABLE",
            "ADD_FIRST_PRINCIPLES_SELECTION_AXIOM",
            evidence, selection,
        )
    controls = control_runner()
    if not controls.all_required_pass:
        return stopped_ledger(
            "PROTOCOL_INVALID",
            "REPAIR_PROTOCOL_BEFORE_ANY_APPLICATION",
            evidence, selection, controls,
            failed_gate=controls.failed_stage,
        )
    return certified_ledger(evidence, manifest, selection, controls)
~~~

`run_control_family` is the only control entrypoint used by the gate. It must enforce covariance, constant-null, L5, L7, scale, and superposition order internally and expose the first failed stage; `_audit` must not reconstruct, reorder, or continue those stages. Do not define or import a response-application or scientific-adjudication function in this stage.

- [ ] **Step 4: Freeze the ledger schema**

The certified ledger must include exact evidence pins, typed manifest, selection ranks/weights, L5/L7 invariant counts, every-root/scale/superposition/covariance booleans, construction-firewall zeroes, status TRANSPORT_PROTOCOL_CERTIFIED, and the next required object. It must also contain:

~~~python
{
    "Pillar_3": "OPEN",
    "scientific_breakthrough": False,
    "response_geometry_applied": False,
    "source_target_constructed": False,
    "source_correspondence_evaluated": False,
    "physical_connection_derived": False,
    "physical_curvature_derived": False,
    "stress_energy_derived": False,
    "einstein_equations_derived": False,
    "continuum_limit_derived": False,
    "spacetime_derived": False,
}
~~~

Represent every Fraction as a canonical string. Emit sorted, indented JSON with one trailing newline.

- [ ] **Step 5: Generate, replay, and document**

~~~bash
python protocol_gate.py --out docs/RESULTS.json
python protocol_gate.py --check docs/RESULTS.json > /tmp/v1542-results.json
cmp docs/RESULTS.json /tmp/v1542-results.json
~~~

README.md must lead with the mechanical status, distinguish protocol certification from response/scientific results, list the exact canary counts, describe the evidence firewall, give reproduction commands, and state that the next stage applies the certified transport to response geometry without source adjudication.

- [ ] **Step 6: Run GREEN and compile**

~~~bash
python -m unittest -v test_evidence.py test_selection.py test_transport.py \
  test_holonomy.py test_controls.py test_gate.py
python -m compileall -q exact_algebra.py operational_complex.py evidence.py fixtures.py \
  protocol_types.py selection.py transport.py holonomy.py controls.py protocol_gate.py \
  test_evidence.py test_selection.py test_transport.py test_holonomy.py \
  test_controls.py test_gate.py
~~~

Expected: 36/36 pass and compileall exits 0.

- [ ] **Step 7: Commit**

~~~bash
git add ResearchHistory/UQCF-GEM/demos/v15.42-duality-covariant-transport-repair
git commit -m "docs(uqcf): publish v15.42 transport certification ledger"
~~~

### Task 7: Add CI, run inherited regressions, and certify the exact head

**Files:**
- Create: .github/workflows/uqcf-v1542-duality-covariant-transport-repair.yml
- Modify: docs/superpowers/plans/2026-09-20-v1542-duality-covariant-transport-repair-implementation.md only by appending execution receipts.
- Update: PR #53 description after the exact-head run succeeds.

**Interfaces:**
- Consumes: the complete v15.42 artifact set and certified inherited suites.
- Produces: an exact-head workflow receipt tied to the final branch SHA; no merge.

- [ ] **Step 1: Create the dedicated workflow**

Trigger only on research/v15.42-duality-covariant-transport-repair and these paths: the new demo directory, v15.42 spec, v15.42 plan, and the workflow itself. Use Python 3.13.5, PYTHONHASHSEED=0, ubuntu-24.04, timeout 90 minutes, checkout fetch-depth 0 with credentials disabled, and NumPy 2.3.5 only for inherited tests.

- [ ] **Step 2: Enforce additive scope**

Use base b9c5f29d8687a7dbc2af0595430aa73fbc5b8553. Require every diff entry to have status A and to be inside the new demo directory or equal one of:

~~~text
docs/superpowers/specs/2026-09-20-v1542-duality-covariant-transport-repair-design.md
docs/superpowers/plans/2026-09-20-v1542-duality-covariant-transport-repair-implementation.md
.github/workflows/uqcf-v1542-duality-covariant-transport-repair.yml
~~~

- [ ] **Step 3: Run v15.42 and inherited suites**

Run the 36-test v15.42 suite first. Then run and assert exact counts for v15.39 (8), v15.40 (9), and v15.41 (26), for 43 inherited tests total. Print the tail of each suite, assert return code 0, the exact count, and a standalone OK line.

- [ ] **Step 4: Verify deterministic replay and compilation**

Run protocol_gate.py --check, compare bytes with docs/RESULTS.json, compile every v15.42 Python file, and rerun the v15.41 ledger check against its unchanged RESULTS.json.

- [ ] **Step 5: Commit workflow and pre-receipt plan state**

~~~bash
git add .github/workflows/uqcf-v1542-duality-covariant-transport-repair.yml \
        docs/superpowers/plans/2026-09-20-v1542-duality-covariant-transport-repair-implementation.md
git commit -m "ci(uqcf): certify v15.42 transport protocol"
~~~

Push and require the workflow to succeed at that exact head.

- [ ] **Step 6: Append immutable execution receipts**

Append, without rewriting prior plan text: RED commit/run/job for each task boundary; implementation commit SHAs; four parent/design/result blobs; canonical v15.42 result blob; v15.42 test count; inherited counts; replay/compile results; workflow URL/run/job; tested head; and PR state. If this receipt changes the head, require one final workflow run on the receipt commit itself.

- [ ] **Step 7: Obtain a fresh whole-branch review**

Dispatch one read-only reviewer with the approved spec, this plan, base SHA, final SHA, workflow evidence, and explicit focus on the Koszul sign, local D4 covariance, tangent/cotangent duality, nonflat oracle independence, evidence firewall, and claim boundary. Fix every Critical or Important issue test-first; record Minor issues without broadening scope.

- [ ] **Step 8: Update PR #53 without merging**

Report exact status, evidence pins, canary counts, result blob, final head, workflow URL/job, review verdict, and scientific boundary. Leave the PR draft, open, mergeable, and unmerged.

## Implementation Completion Gate

Implementation is complete only when:

- all four frozen evidence blobs and both vendored substrate blobs match exactly;
- the selection audits uniquely return centered weights (1/2, 0, -1/2) and endpoint weights (1/2, 1/2);
- every typed map, sign, domain, codomain, reversal, basepoint, orientation, relabeling, local D4, and tangent/cotangent identity passes exactly;
- constants are flat;
- L5 and held-out L7 impulse controls reproduce the frozen invariant counts for every marked root;
- scale and superposition are exact;
- response/source/physics firewall queries remain zero;
- status is TRANSPORT_PROTOCOL_CERTIFIED with all scientific fields false or null;
- the 36 new and 43 inherited tests pass;
- both v15.42 and unchanged v15.41 ledgers replay byte-for-byte;
- compilation succeeds;
- exact-head CI and fresh review are recorded;
- PR #53 remains draft, open, unmerged, and mergeable.
