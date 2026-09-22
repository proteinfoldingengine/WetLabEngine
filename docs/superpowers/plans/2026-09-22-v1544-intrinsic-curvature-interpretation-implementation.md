# UQCF-GEM v15.44 Intrinsic Curvature Interpretation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Derive and certify the exact finite response-to-curvature operator, its complete kernel, and all frozen canonical-control comparisons without source fitting.

**Architecture:** A coordinator verifies parent evidence, then a construction worker builds family-blind operators and kernel certificates from geometry alone. An independent frozen-core worker supplies reference columns and presentation checks. A later comparison worker reads fields and archived RESULTS only after construction certificates pass. Pure exact algebra has no filesystem or process capabilities.

**Tech Stack:** CPython 3.13.5, standard library Fraction/unittest/JSON/subprocess/hashlib/AST, Ubuntu 24.04. No new numeric dependency; production v15.44 does not import NumPy or acquisition.

**Spec:** `docs/superpowers/specs/2026-09-22-v1544-intrinsic-curvature-interpretation-design.md`, approved in conversation; commit `98ef86fc93d829e0f7da2ad31d431042b9b11f40`, blob `6df4678d903d5a841f426505abf0a5e1070436e8`.

## Global Constraints

- Scientific parent: `f121358c53ffdf88f9c0dcf351b850819ecb0298`; parent certification run `35754551391` succeeded. Preserve every parent-tracked file byte-for-byte.
- Execute only on `research/v15.44-intrinsic-curvature-interpretation`. PR #55 remains draft/open/unmerged; PR #53 and #54 remain unchanged.
- Four actual carriers: L5/L7 at scales 1 and 7/3. Full field domain Q^(L^2); archived fields remain centered.
- Every operator stores four row-major matrix entries per inherited ordered face. No scalar signed-curvature extraction.
- 740 case keys and 592 canonical-control pairs; every response index and family. No selected subset, thresholds, family winner, or p-values.
- Prior nonzero outcomes and L7 exposure are known; no fresh holdout claim.
- Source correspondence NOT_EVALUATED, Pillar 3 OPEN, physical claims, foundational uniqueness and scientific breakthrough false. Preserve inherited-axiom and scalar-lift dependence.
- No fundamental time, dark-matter primitive, physical normalization, source fitting, new carrier rule, continuum claim, or transport retuning.
- Exact rational decisions only. A mathematical null or generic response is a successful characterization if verification passes.
- Use the preserved subagent-driven preference: task implementation and scoped review, then a fresh whole-branch review. Approval of this written plan permits all listed tasks without repeated between-task confirmation.
- Put execution receipts in PR metadata. Complete source/artifact publication precedes one official certification; fix-driven reruns are permitted, documentation-only reruns are avoided.

## Review Focus

1. Rank certificates must reject a correct annihilated vector with an incomplete kernel basis (Task 3).
2. A reflected frame or changed face basepoint must not create a false family difference from raw matrix entries (Task 4).
3. Zero field, nonzero kernel field, opposite sign and proportional curvature require distinct, total comparison handling (Task 5).
4. The independent derivation must not call or alias the oracle, or use archived results to choose coefficients (Tasks 1–2).
5. Failure after partial work must retain the first failed stage and never report 740 successful cases by expectation (Task 6).

## File map and process ownership

Let D = `ResearchHistory/UQCF-GEM/demos/v15.44-intrinsic-curvature-interpretation`. All filenames below are under D unless explicitly rooted.

| Files | Owner |
| --- | --- |
| dependencies.json, evidence.py, bootstrap.py, test_evidence.py | Frozen closure, origin checks, worker loading |
| exact_matrix.py, test_exact_matrix.py | Rectangular rational algebra and certificates |
| operator_types.py, derive.py, oracle.py, test_operator.py | Geometry-only coefficient derivation and reference comparison |
| kernel.py, test_kernel.py | Rank, nullspace, image and orthogonal projector |
| presentations.py, test_presentations.py | Full basis covariance, cycle and alignment checks |
| compare.py, test_compare.py | Complete fields, invariant ratios and canonical-control pairs |
| worker.py, gate.py, test_gate.py | Process stages, failure ledger, canonical replay |
| docs/DERIVATION.md, docs/RESULTS.json, README.md | Proof narrative, deterministic complete ledger, scope |
| ci_verify.py, .github/workflows/uqcf-v1544-intrinsic-curvature-interpretation.yml | Exact-head certification |

Construction worker input schema contains only L, scale, labels, work and neighbors. The construction parser rejects fields, families, sources, targets and unknown keys. The coordinator validates the frozen INPUTS using the parent decoder before stripping fields. Only the comparison worker receives field tuples and archived results. The oracle receives carrier geometry and internally generated basis/control fields, never archives.

Bootstrap pins every inherited import's real resolved path and Git blob; do not trust sys.path names. Use unique v15.44 module names for new modules (the filenames above do not collide with the selected inherited closure except evidence, which is not inherited here). Load inherited paths explicitly into isolated fresh workers using `python -I -B`. No production import of any parent evidence.py or acquisition module.

Executable inherited closure, relative to demos:
- v15.42-duality-covariant-transport-repair/exact_algebra.py — c67ea42b61321469f7735ce589f2e729b241666a
- v15.42-duality-covariant-transport-repair/operational_complex.py — 8163beba8e52bc2a3a6d0c8cf59dd1257222f65c
- v15.42-duality-covariant-transport-repair/protocol_types.py — e90a98d17baa6028f0d50a165f0b9d0046de13a2
- v15.42-duality-covariant-transport-repair/transport.py — df552284c16d43bc876340fbc13fe91eb9ee6a00
- v15.42-duality-covariant-transport-repair/holonomy.py — bad3f06b291bb448a903b4f48344a9e54a633f68
- v15.43-certified-response-geometry/projection.py — f857f2cf1cd4c265c193121236af8e441b1f01dc
- v15.43-certified-response-geometry/carriers.py — 5cd286b014bb44025e16832ee91a6e6665291c8c

The application module is evidence-only, blob 30348d71d366a751932ec2d58d18a9148d81ae83. Its behavior is recovered by explicit core calls in oracle.py, not imported. Tests may load parent fixtures.py (9704660b4183f040c84a0734b52702258d1d42da) in their isolated test worker, never production. Inherited presentation_checks.py is read for conventions but not imported; independent alignment is owned by presentations.py.

Hash-only evidence includes the spec, parent INPUTS (f6435267950cde0985889056a67d5427f60f637f), parent RESULTS (937024b3f90570c9b177bfb2eee7cdab25a13985), and parent tree. Verify parent ancestry and `git diff --name-status PARENT HEAD`: only added D/**, this exact spec and plan, and the exact v15.44 workflow are allowed. Any parent deletion or modification fails. Runtime code must not dynamically extend the dependency allowlist.

## Shared types and contracts

Use immutable dataclasses and tuples. Q means Fraction, Matrix means tuple of tuple of Q. Reject bool and float at boundaries.

- Geometry: L:int, scale:Q, labels:tuple[int,...], work:Matrix, neighbors:tuple[tuple[int,int],...].
- Operator: labels:tuple[int,...], cycles:tuple[tuple[int,int,int,int],...], entries:Matrix of shape (4F,N).
- Reduction: reduced:Matrix, pivots:tuple[int,...], operations:tuple of exact elementary row operations.
- KernelResult: rank:int, nullity:int, pivots:tuple[int,...], null_basis:Matrix (N by nullity), image_basis:Matrix (4F by rank), projector:Matrix (N by N), centered_basis:Matrix, reduction:Reduction.
- `derive_operator(carrier) -> Operator`; `reference_operator(carrier, presentation=None) -> Operator`.
- `analyze_kernel(operator: Operator) -> KernelResult`; `verify_kernel(operator, result) -> bool` raises ValueError on invalid certificates.
- `check_presentations(carrier, operator: Operator) -> dict`, containing observed counts and exact checks.
- `analyze_field(operator, kernel, values:tuple[Q,...]) -> dict`; `compare_pair(canonical:dict, control:dict) -> dict`.
- `audit() -> dict` has no injectable public overrides. A private `_audit(executors)` supports failure tests.
- CLI: `python -I gate.py --out docs/RESULTS.json` or `--check docs/RESULTS.json`. The CLI must bootstrap its own pinned module paths under isolation.
- Canonical wire format: sorted object keys, indent=2, ASCII, trailing newline; Fraction as canonical str; tuple as list; duplicate keys rejected. All data arrays preserve prescribed order. No timing or machine fields in scientific bytes.

## Task 1: Evidence, isolation and strict geometry interface

**Files:** dependencies.json, evidence.py, bootstrap.py, operator_types.py, test_evidence.py.

**Consumes:** exact parent/spec/closure pins above. **Produces:** `verify_evidence(root:Path)->dict`, `load_geometry(raw:bytes)->Geometry`, `build_actual_carrier(geometry:Geometry)->Carrier`, and Operator type.

- [ ] Write failing tests for pin drift, wrong module origin, duplicate JSON keys, floats/bools, source/target injection, fields in construction input, swapped label ordering, incomplete four-carrier inventory and parent mutation. Patch file readers in tests to assert derive/kernel cannot open archives.
```python
def test_construction_rejects_response_data(self):
    wire = geometry_wire_from_fixture(5)
    wire["fields"] = []
    with self.assertRaisesRegex(ValueError, "unknown_field"):
        load_geometry(canonical_bytes(wire))
```
Define geometry_wire_from_fixture in test_evidence.py from the pinned periodic fixture, excluding response data. Define canonical_bytes in operator_types.py for serialization; RED failure must reach missing implementation or the specified validation, not a typo/import in the test.
- [ ] Run `python -m unittest -v test_evidence`; observe RED.
- [ ] Implement explicit-key strict parsers and the fixed pin manifest. Build an empty-fields parent Payload internally from Geometry and call pinned build_carrier; never fabricate production geometry from test fixtures. Assert exactly N=L^2, 2N undirected edges and F=N after identification; unexpected actual inventory fails instead of modifying coverage.
```python
allowed = {"L", "scale", "labels", "work", "neighbors"}
if set(wire) != allowed:
    raise ValueError("unknown_field" if set(wire)-allowed else "missing_field")
```
Origin checks use Path(module.__file__).resolve() against the manifest before accepting imported symbols. AST-check derive/kernel to prohibit oracle/core/compare/gate imports and filesystem/process access. Runtime tests deny those capabilities after bootstrap.
- [ ] Re-run the test module GREEN. Check the frozen parent/spec blobs from Git.
- [ ] Commit only this task's named files; message `feat(uqcf): freeze intrinsic interpretation inputs and isolation`.

## Task 2: Independent coefficient operator and proof narrative

**Files:** exact_matrix.py, derive.py, oracle.py, test_exact_matrix.py, test_operator.py; begin docs/DERIVATION.md.

**Consumes:** Geometry -> Carrier; Operator. **Produces:** derive_operator, reference_operator and exact rectangular matmul, transpose, add, identity, zeros, apply_matrix. Shapes including zero-column matrices are explicit; no zip truncation.

- [ ] Write RED algebra tests (rectangular shape rejection, exact products) and operator tests. Use actual parent carriers only for integration; manufactured geometry tests only establish mechanics.
```python
def test_complete_basis_agreement(self):
    c = fixture_carrier(5)
    self.assertEqual(derive_operator(c), reference_operator(c))

def test_reject_changed_coefficient(self):
    a = derive_operator(fixture_carrier(5))
    damaged = replace_entry(a, row=1, column=0, increment=Q(1))
    with self.assertRaisesRegex(ValueError, "operator_mismatch"):
        require_equal(damaged, reference_operator(fixture_carrier(5)))
```
Define fixture_carrier in test_operator.py using the pinned fixture and parent identification; replace_entry is a test-only immutable constructor; require_equal belongs to derive.py and compares metadata and every entry.
- [ ] Run `python -m unittest -v test_exact_matrix test_operator`; observe RED.
- [ ] Derive coefficients directly, carrying a length-N coefficient vector at each scalar. For local gradient component i, assign +1/2 to the positive neighbor and -1/2 to the negative neighbor. Let G_x be its 2 by N matrix. For edge x->y, define H=(G_x+P_yx G_y)/2. Form each coefficient B_j exactly:
```python
B_j[a][b] = ((Q(x==j)-Q(y==j))/2)*Q(a==b) + (
    H[a][j]*direction[b] - direction[a]*H[b][j]
)/2
D_j = P_xy @ B_j
```
Here j denotes the label at the selected column, not an assumed integer position. Implement @ using exact_matrix.matmul. For edge sequence e0..e3, K_j is the sum of four ordered products P3...D_slot...P0. Do not call the inherited recurrence or constructor from derive.py. In oracle.py alone, call construct_transport and linearized_holonomy on every e_j, then flatten four matrix entries per inherited face.
- [ ] Write the algebraic derivation of linearity and the ordered product in DERIVATION.md. Derive cancellation of the scalar identity contribution under the flat baseline, explicitly retaining all skew contributions. Any stencil simplification must be proved and compared with every coefficient; the unsimplified coefficient formula is sufficient and no Laplacian identification is presumed.
- [ ] Run GREEN tests. Require equality on all columns of all four actual carriers in integration before committing. Verify oracle access is prohibited from derive.py.
- [ ] Commit named files; message `feat(uqcf): derive exact response curvature operator independently`.

## Task 3: Complete rational kernel and independently verified certificates

**Files:** extend exact_matrix.py and test_exact_matrix.py; kernel.py, test_kernel.py.

**Consumes:** Operator. **Produces:** Reduction, KernelResult, analyze_kernel, verify_kernel.

- [ ] Write RED tests using matrices with known ranks, zero matrices, full column rank and nontrivial centered kernel:
```python
def test_kernel_completeness(self):
    a = operator_from_matrix(((Q(1),Q(-1),Q(0)),))
    k = analyze_kernel(a)
    self.assertEqual((k.rank,k.nullity),(1,2))
    self.assertEqual(k.projector, (
        (Q(1,2),Q(1,2),Q(0)),
        (Q(1,2),Q(1,2),Q(0)),
        (Q(0),Q(0),Q(1))))
    with self.assertRaises(ValueError):
        verify_kernel(a, omit_last_null_column(k))
```
operator_from_matrix is a test-only adapter for algebraic kernel tests (production Operator schema still enforces 4F rows); omit_last_null_column constructs a corrupted certificate. Also test a forged rank with valid null vectors and a dependent image basis.
- [ ] Run `python -m unittest -v test_exact_matrix test_kernel`; observe RED.
- [ ] Implement deterministic Gauss-Jordan: scan columns ascending; select first nonzero remaining row; record swap, nonzero rational row scaling, and row additions; eliminate above and below pivots. Replay the operations in a verifier that does not invoke the reducer. Check RREF conditions independently. Invertibility of each recorded operation plus verified RREF certifies rank; no tolerance or singular-value cutoff.
```python
for free in free_columns:
    z = [Q(0)] * n
    z[free] = Q(1)
    for row, pivot in enumerate(pivots):
        z[pivot] = -R[row][free]
    basis_columns.append(tuple(z))
```
Image basis comprises original A columns at pivot indices. Verify spanning by reducing each column in this basis, independence via rank, and rank-nullity. Compute centered kernel as nullspace of A augmented by one all-ones row, not by discarding a conveniently named constant basis vector.
- [ ] Implement exact P=Z inverse(Z^T Z) Z^T; zero-column case returns N by N zeros. Verify P^T=P, P^2=P, AP=0 and PZ=Z. Verify constants and every reported kernel vector through the frozen oracle in the control worker. The projector uses the spec's fixed unweighted vertex inner product only.
- [ ] Run GREEN tests and actual four-carrier certificates, reporting observed ranks without expected scientific ranks in tests.
- [ ] Commit named files; message `feat(uqcf): certify complete response curvature kernels`.

## Task 4: Presentation, basis and scale controls

**Files:** presentations.py, test_presentations.py; extend oracle.py only for exact presented reference calls.

**Consumes:** Operator, Carrier, kernel certificates. **Produces:** check_presentations and exact alignment receipts.

- [ ] Write RED tests for wrong derivative slot, basepoint rotation, reversed cycle sign, reflected D4 action, label reversal without column permutation, and geometry chosen from results. Example:
```python
def test_column_permutation_required(self):
    c = fixture_carrier(5)
    a = derive_operator(c)
    relabeled, names = relabel_geometry(c, tuple(reversed(c.complex.labels)))
    b = derive_operator(relabeled)
    with self.assertRaisesRegex(ValueError, "aligned_operator"):
        verify_alignment(c, relabeled, a, b, names, permute_columns=False)
```
The test-only false switch belongs to a helper wrapper; production verify_alignment always permutes columns. relabel_geometry reconstructs work/neighbors and calls inherited identification, then returns Carrier and the old->new label map.
- [ ] Run `python -m unittest -v test_presentations`; observe RED.
- [ ] Implement transformations from geometry: P'_xy=g_y P_xy g_x^T and d'_xy=g_x d_xy. Re-derive the coefficient map from those presented arrays; do not generate the transformed map by conjugating the expected answer. Compare against transformed columns of A after recomputation. Validate full frozen-core reference columns under these presentations.
- [ ] Enumerate all eight uniform D4 assignments and 8N single-site assignments per carrier. For each, check every column and every face. Deduplication of identical mathematics may cache immutable values but must not remove declared receipts. Baseline carrier sum N=148 implies 1,216 declared gauge assignments; record observed assignment, column and face counts, not only pass booleans.
- [ ] Check all four cycle rotations and both orientations with baseline path conjugation on every basis column. Label reversal j->N-1-j moves field/work/neighbors together. Establish unique frame alignment from direction classes alone. Match faces by vertex sets, then explicitly align canonical cycle orientation/basepoint before comparing matrices. Fail on nonunique face matches or alignment.
- [ ] Align scale carriers through the same geometry rules; verify unit-scale A against aligned 7/3 carrier A on the same abstract field, then verify every archived response pair's scalar factor 7/3 and squared-invariant factor 49/9 in Task 5. Check constants, all impulses, kernel vectors and the fixed mixed field u_j=j+1 through the core. No additional all-pairs core calls are needed: exact linearity and complete basis equality certify sums of all unit-field pairs.
- [ ] Run GREEN tests. Execute controls on four actual carriers before committing. Bound the control-worker subprocess to 7,200 seconds; a timeout is incomplete verification, never a null result. Optimize only exact topology/coefficient reuse with unchanged complete coverage.
- [ ] Commit named files; message `feat(uqcf): verify intrinsic operator presentation controls`.

## Task 5: Complete archived-field and canonical-control comparison

**Files:** compare.py, test_compare.py.

**Consumes:** sealed four-operator/kernel receipts, strict parent projection, archived result wire in a separate worker. **Produces:** analyze_field, compare_pair, complete case/pair arrays.

- [ ] Write RED tests for zero field, nonzero kernel field, opposite sign, proportional fields and unequal profiles:
```python
def test_proportionality_preserves_sign(self):
    left = synthetic_case(curvature=(Q(1),Q(-1)), field=(Q(1),Q(-1)))
    right = synthetic_case(curvature=(Q(-2),Q(2)), field=(Q(-2),Q(2)))
    result = compare_pair(left, right)
    self.assertEqual(result["proportionality"], "NONZERO_PROPORTIONAL")
    self.assertEqual(result["factor_control_over_canonical"], Q(-2))
    self.assertFalse(result["matrix_equal"])
    self.assertTrue(result["normalized_profile_equal"])
```
synthetic_case is a test-only builder producing valid skew 2 by 2 matrices from each scalar, exact E/S/profile and visible-norm fields. Test two zero curvatures with distinct nonzero fields; one-zero curvature; malformed archived face order and missing pair.
- [ ] Run `python -m unittest -v test_compare`; observe RED.
- [ ] Implement x=Au; split into 2 by 2 K_f; require skewness and I_f>=0. Compute S=u^T u, z=Pu, v=u-z, E=sum I_f and all spec ratios with null reasons. Verify orthogonality, norm decomposition and A z=0. Preserve all full components and matrices. Archived-result comparison checks strict complete case/face order and exact entries, invariants, histograms and total before acceptance.
```python
if all(x == 0 for x in canonical_K):
    category = "BOTH_ZERO" if all(y == 0 for y in control_K) else "CANONICAL_ZERO_ONLY"
    factor = None
elif all(y == 0 for y in control_K):
    category, factor = "CONTROL_ZERO_ONLY", None
else:
    i = next(i for i,x in enumerate(canonical_K) if x != 0)
    factor = control_K[i] / canonical_K[i]
    ok = factor != 0 and all(y == factor*x for x,y in zip(canonical_K,control_K))
    category = "NONZERO_PROPORTIONAL" if ok else "NONZERO_NONPROPORTIONAL"
    if not ok: factor = None
```
Require equal vector lengths before zip. When E=0, normalized-profile equality is null with reason UNDEFINED_ZERO_CURVATURE, even if both curvature arrays are zero; matrix equality is still well-defined. Ratio differences are control minus canonical; undefined operands produce null with named reason. Do not classify by family label.
- [ ] Build cases ordered by payload L/scale, family order from parent FAMILY_KEYS, then response index. Build pairs in L, scale, response-index order, then the four controls in inherited order. Require exact key sets and cardinalities (740,592); reject duplicates. Publish descriptive counts per control (148 pairs each) and carrier.
- [ ] Run GREEN tests plus all archived-field comparisons. Verify complete 370 matched scale pairs across five families and both sizes, including core-matrix and invariant scaling under Task 4 alignment. No statistical independence claim for scale pairs.
- [ ] Commit named files; message `feat(uqcf): characterize all frozen response families`.

## Task 6: Fail-closed coordinator, deterministic artifacts and proof review

**Files:** worker.py, gate.py, test_gate.py, docs/DERIVATION.md, docs/RESULTS.json, README.md.

**Consumes:** all previous interfaces. **Produces:** audit and strict --out/--check CLI.

- [ ] Write RED failure-order tests for every stage, malformed child JSON, timeout, nonzero worker exit and failure after partial case completion:
```python
def test_partial_comparison_never_succeeds(self):
    result = _audit(executors_with_failure("all_archived_field_comparisons", completed=12))
    self.assertEqual(result["status"], "INTRINSIC_CURVATURE_INTERPRETATION_INVALID")
    self.assertEqual(result["first_failed_stage"], "all_archived_field_comparisons")
    self.assertEqual(result["completed_counts"]["cases"], 12)
    self.assertIsNone(result["scientific_verdict"])
```
executors_with_failure is a private test factory supplying deterministic stage doubles; production audit cannot receive overrides.
- [ ] Run `python -m unittest -v test_gate`; observe RED.
- [ ] Implement ordered stages exactly: evidence, projection/carriers, operator derivation/equality, kernel/image certificates, controls, all archived-field comparisons, ledger. Each subprocess uses argument lists, isolated Python, controlled paths, capture to temporary files, timeout and checked return code. Evidence timeout 60s, algebra and compare workers 1,800s each, controls 7,200s. Preserve first failure and actual completed counts.
- [ ] Seal construction output before archived RESULTS are loaded. Record operator/certificate canonical SHA-256s. The ledger contains parent/spec/pins, theorem statements with assumptions, proof/certificate status, four complete carrier objects, 740 field receipts, 592 pair receipts, control coverage, failure fields and claims. Successful status INTRINSIC_CURVATURE_CHARACTERIZED; invalid status as above. No time/cost/host metadata in deterministic bytes.
- [ ] Complete DERIVATION.md: exact linearity, coefficient/product derivation, cancellation, rational rank/kernel proof by certificates, projector proof, and interpretation limited to observed finite results. Separate analytic proof from finite computation. No named differential-operator identity without all constants/domain/boundary conventions proved.
- [ ] Run all focused new tests once GREEN and record actual count. Execute one full local audit and one --check replay in a durable Git-backed workspace with pinned Python. Required CLI commands:
```bash
python -I gate.py --out docs/RESULTS.json
python -I gate.py --check docs/RESULTS.json
python -m compileall -q .
```
Expected: audit/replay exit zero, deterministic bytes identical, complete coverage. An invalid result stops publication of a successful ledger; preserve the failure and repair only implementation defects, never expected scientific ranks/results.
- [ ] README states actual characterization, exact reproduction commands, known-data disclosure, interpretation limits, common-carrier limitation and next unresolved question. Commit only named files; message `feat(uqcf): publish certified intrinsic curvature characterization`.

## Task 7: Review, complete publication and one official certification

**Files:** ci_verify.py; repository-root .github/workflows/uqcf-v1544-intrinsic-curvature-interpretation.yml; test_ci.py.

- [ ] Write RED tests for additive-scope rejection, moved parent head, approved-spec drift, incomplete ledger, false physical claims, wrong runtime, skipped/expected-failure tests, and wrong final head. Test CI functions with injected subprocess records, never mock a scientific successful audit.
- [ ] Implement the CI runner in this order: exact HEAD and clean tracked tree; parent ancestry and frozen tree/spec/dependency checks; focused suite with actual recorded test count and no skips; one complete --check replay; complete coverage/certificate/claim checks; compilation; unchanged tracked tree and final HEAD; print V1544_CERTIFIED_HEAD plus SHA.
- [ ] Run `python -m unittest -v test_ci` RED then GREEN. Workflow configuration:
```yaml
name: UQCF v15.44 intrinsic curvature interpretation
on:
  push:
    branches: [research/v15.44-intrinsic-curvature-interpretation]
    paths:
      - 'ResearchHistory/UQCF-GEM/demos/v15.44-intrinsic-curvature-interpretation/**'
      - 'docs/superpowers/specs/2026-09-22-v1544-intrinsic-curvature-interpretation-design.md'
      - 'docs/superpowers/plans/2026-09-22-v1544-intrinsic-curvature-interpretation-implementation.md'
      - '.github/workflows/uqcf-v1544-intrinsic-curvature-interpretation.yml'
permissions:
  contents: read
jobs:
  certify:
    runs-on: ubuntu-24.04
    timeout-minutes: 180
    env:
      PYTHONHASHSEED: '0'
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13.5'
      - run: python ResearchHistory/UQCF-GEM/demos/v15.44-intrinsic-curvature-interpretation/ci_verify.py
```
No pull_request trigger, schedule, broad branch filter, installation step or matrix. Parent certification and frozen parent tree are inherited evidence; do not rerun the entire v15.43 acquisition pipeline. New complete basis/core checks verify the bridge actually consumed by v15.44.
- [ ] Finish scoped reviews, then fresh whole-branch review of source isolation, derivation independence, kernel completeness, transformed codomain comparisons, undefined ratios, complete counts and truthful claims. Resolve substantive defects with targeted failing tests and rerun affected gates only.
- [ ] Verify complete publication inventory includes README, proof document, ledger and workflow before pushing the reviewed commit series once to PR #55. Do not publish the workflow against a known incomplete artifact tree.
- [ ] Observe official run/head/job/conclusion. Success requires matching current PR head and all steps successful. Record receipts, actual test/control counts, output blobs, reviewers and execution rulings in PR metadata without another scientific commit. No merge.
- [ ] Report finite outcome and what it means for the information-to-geometry stack; distinguish novelty hypothesis and unresolved physical claims. End this stage without beginning a new scientific experiment.

## Plan self-review and handoff

Coverage: spec 1–3 -> constraints and Task 1; spec 4 -> Task 2; spec 5 -> Task 3; spec 6 -> Task 5; spec 7 -> Tasks 1–5; spec 8 -> Task 6; spec 9 -> Tasks 6–7. Review Focus items have explicit adversarial tests in their owning tasks. Executable inherited closure is enumerated above; archive-reading and coefficient construction are separately owned.

The matrix representation uses full entries, eliminating an unregistered signed-scalar convention. Rank verification does not accept annihilation alone. Undefined ratios retain reasons. Relabeling and gauge tests transform both domain and codomain. No scientific expected rank, kernel dimension, family preference or numerical result is baked into tests.

Approval boundary: the written specification is approved. This plan is the next reviewable deliverable and contains no executed v15.44 scientific result. Approve this written plan before implementation. The prior task-scoped subagent review method is preserved; no fresh execution-method choice is required unless the user wants to change it.
