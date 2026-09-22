# UQCF-GEM v15.43 Certified Response Geometry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the unchanged certified transport to all 740 frozen response cases and publish an exact finite curvature classification without source adjudication.

**Architecture:** A coordinator verifies frozen evidence and replays parent certification before invoking a separate acquisition process. Acquisition serializes a strict projection; a fresh evaluator process imports only the certified transport closure and the projection/application modules. The coordinator owns provenance and publication; pure mathematical modules have no source, target, filesystem, or process capabilities.

**Tech Stack:** CPython 3.13.5 for official CI, standard-library unittest/Fraction/JSON/subprocess/AST, NumPy 2.3.5 only for inherited acquisition and regressions, Ubuntu 24.04. Exact arithmetic governs all mathematical decisions.

**Spec:** `docs/superpowers/specs/2026-09-20-v1543-certified-response-geometry-design.md`, approved in conversation after publication at `c414d4328b206f50bacd7febe350faab30014a0f`; frozen blob `680f691538b99037b89d52b6c93742495d039d4e`.

## Global Constraints

- Scientific parent: `0f426fa28d22871ce042e39bf9704695ede8b336`; implementation starts after this plan on its v15.43 descendant branch, not on the parent branch.
- Neither a nonzero result nor a null result may select a new connection, stencil, orientation, normalization, field lift, or response family. No source-correspondence verdict is permitted.
- Sizes: `5`, `7`; scales: `1`, `7/3`; all five frozen families, all response indices, every face: 740 base cases and 148 canonical-family cases.
- All families use the canonical global-balance carrier; no control field gets a different connection or its own work geometry in this stage.
- L7 is a held-out size for this application, evaluated with an unchanged rule after L5.
- Source arrays are allowed only inside inherited acquisition. The evaluator receives operational geometry and exact scalar responses, never sources, incidence support, target results, coordinates, fitting inputs, or historical curvature.
- Reuse certified transport and holonomy byte-identically; do not rewrite their formulas or run the v15.41 closure ansatz.
- Reject booleans, floats, malformed/noncanonical fractions, unknown or duplicate JSON keys, incomplete cases, invalid ordering, pin drift, and process failures. No partial success.
- Keep all historical files and the approved specification unchanged. Add only the new v15.43 demo, its plan, and its dedicated workflow relative to the scientific parent.
- Retain the 91 inherited tests and both byte-identical v15.41/v15.42 replays.
- Source correspondence is `NOT_EVALUATED`; physical claims and scientific breakthrough remain false; Pillar 3 remains `OPEN`.
- No fundamental time, dark-matter primitive, physical normalization, source contraction, threshold, or fitted parameter is introduced.
- PR #53 stays unchanged and unmerged. PR #54 stays draft, open, and unmerged. Publish authorized changes to its existing branch.

## Review Focus

1. A syntactically valid payload with duplicate case keys or swapped vector order must fail before any curvature evaluation (Task 2).
2. An import with a familiar name but wrong origin, or an injected source/target field, must fail before mathematical construction (Tasks 1–2).
3. An evaluator failure after some cases finish must retain the actual first failure and never publish a partial nonzero verdict (Task 5).
4. A relabeling that changes a cycle's canonical start/orientation must compare the correct based endomorphisms, not raw ordered matrices (Task 4).
5. A geometrically unidentifiable response carrier must stop, even when the manufactured torus fixture would pass (Task 3).

---

## File map and frozen dependencies

Let `D = ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/`. Every relative filename in Tasks 1–5 is under D. Commands run from D unless a repository-root path is shown. This notation is a path alias, not a module or environment variable.

| New file | Responsibility |
| --- | --- |
| `evidence.py`, `dependencies.json` | Exact repository pins, ancestry and import-origin receipts |
| `projection.py` | Immutable validated projection and canonical serialization |
| `acquire.py` | Separate pinned inherited producer; no curvature calls |
| `carriers.py` | Actual response carrier and baseline validation |
| `application.py` | Pure certified-core calls and complete face records |
| `presentation_checks.py` | Independent product derivative and exact presentation identities |
| `application_controls.py` | Actual-carrier impulses/constants, response scale/shift/superposition checks |
| `firewall.py` | Reviewed import/AST boundary and runtime-origin checks |
| `evaluate.py` | Evaluator CLI: projection input and result output only |
| `response_geometry_gate.py` | Coordinator, parent replay, subprocesses, statuses, ledger CLI |
| `test_evidence.py`, `test_projection.py`, `test_carriers.py`, `test_application.py`, `test_controls.py`, `test_gate.py` | Focused behavioral tests owned by respective tasks |
| `docs/INPUTS.json`, `docs/RESULTS.json`, `README.md` | Reproducible projected inputs, complete results, claim boundary |
| `ci_verify.py` | Exact-head scope/test/replay/coverage verification |

Use the original v15.42 files in place via an explicit path in the fresh evaluator process; never mix them with v15.41 modules in one interpreter. Verify `__file__` and Git blob of every imported local module. The new controls file is `application_controls.py`; the original parent controls stay in the parent replay process only. Entry-point imports must distinguish the new evidence module from the parent evidence module by process ownership and verified path.

Executable inherited acquisition closure (all paths relative to demos):

| Path | Blob |
| --- | --- |
| `v15.40-global-balance-geometry-specificity/response_generation.py` | `afd5a68ce74f7f80f49b6fd6307ebb0681182bf5` |
| `v15.40-global-balance-geometry-specificity/response_geometry.py` | `9128c24b695c1b539ac60dc93aeaf0bd4795c57b` |
| `v15.28-coupling-space/representation_actions.py` | `7260147cd6ca47ec21634172b44b98de726904af` |
| `v15.28-coupling-space/exact_linear.py` | `05cc1b8cfec70d501408377b5e44190b259a4514` |
| `v15.27-target-origin/baseline/baseline/pretime_gravity_canary.py` | `99110f943550751645539c0c8a7339024d7fefd3` |

The last module is dynamically loaded by `load_frozen_complex`; it imports only NumPy and standard-library code. Only its existing carrier construction is used. Do not invoke its canary/scientific entry point. NumPy is pinned separately as an installed dependency, not represented as a Git blob.

Evaluator inherited closure, under `v15.42-duality-covariant-transport-repair/`:

| File | Blob |
| --- | --- |
| `exact_algebra.py` | `c67ea42b61321469f7735ce589f2e729b241666a` |
| `operational_complex.py` | `8163beba8e52bc2a3a6d0c8cf59dd1257222f65c` |
| `protocol_types.py` | `e90a98d17baa6028f0d50a165f0b9d0046de13a2` |
| `transport.py` | `df552284c16d43bc876340fbc13fe91eb9ee6a00` |
| `holonomy.py` | `bad3f06b291bb448a903b4f48344a9e54a633f68` |

Parent replay adds these executable files from that same directory:

| File | Blob |
| --- | --- |
| `protocol_gate.py` | `681c5186c523cd8eb42ea343c6e96cdcb56c476c` |
| `evidence.py` | `4662b73ec2b9724ad6ea06b3194b583c9f6ac3be` |
| `fixtures.py` | `9704660b4183f040c84a0734b52702258d1d42da` |
| `selection.py` | `c8f592eb427135896c46bd8fccd6f3ddb48f7876` |
| `controls.py` | `a31d9a97a379823763b8d8a377166d3501eb0315` |

Hash-only evidence includes every artifact in spec section 3, the approved spec itself, and all paths in the inherited producer's `EVIDENCE` dictionary. Obtain each additional blob from the immutable scientific parent, write it literally in `dependencies.json`, and verify before importing. The inherited producer does parse its own prerequisite status ledgers inside its unchanged verification functions; this is the approved inherited provenance check, not permission for the new application to read target comparisons. Only the parent v15.42 verdict may be parsed by the coordinator; other new checks hash ledger bytes only.

The regression processes may execute the following frozen repository modules, plus the three v15.28/v15.27 modules enumerated above. These paths are a separate `regression` inventory in dependencies.json; none grants evaluator access. Standard-library imports and the pinned NumPy distribution are separate from repository code. Unexpected repository module origins fail closed.

| Regression path relative to demos | Blob |
| --- | --- |
| `v15.39-higher-incidence-source-axioms/source_axiom_canary.py` | `620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a` |
| `v15.39-higher-incidence-source-axioms/test_gate.py` | `c49612a53836ab8a1c783e233f6d741e5e515670` |
| `v15.40-global-balance-geometry-specificity/geometry_specificity_gate.py` | `2e75867e6aedb82ebe3d9c1f04733e2c0d33018a` |
| `v15.40-global-balance-geometry-specificity/incidence_target.py` | `03c1f62279865aac396ea4b85f75a8d38c1629cf` |
| `v15.40-global-balance-geometry-specificity/response_generation.py` | `afd5a68ce74f7f80f49b6fd6307ebb0681182bf5` |
| `v15.40-global-balance-geometry-specificity/response_geometry.py` | `9128c24b695c1b539ac60dc93aeaf0bd4795c57b` |
| `v15.40-global-balance-geometry-specificity/test_gate.py` | `349d500bd97178ac0e341e65699d0ce5f581b7cf` |
| `v15.41-formal-connection-curvature-source-correspondence/connection_curvature_gate.py` | `5c75f2c1d92d9eca42f2ac17a7a91a68633c3726` |
| `v15.41-formal-connection-curvature-source-correspondence/exact_algebra.py` | `c67ea42b61321469f7735ce589f2e729b241666a` |
| `v15.41-formal-connection-curvature-source-correspondence/linearized_connection.py` | `20bff9ed3addd2f1bd39cd28f9c974b7883b97b4` |
| `v15.41-formal-connection-curvature-source-correspondence/operational_complex.py` | `8163beba8e52bc2a3a6d0c8cf59dd1257222f65c` |
| `v15.41-formal-connection-curvature-source-correspondence/response_inputs.py` | `d5720dece65f4f329247d8ca07422e3814a679b6` |
| `v15.41-formal-connection-curvature-source-correspondence/source_target.py` | `7837786ef98b94d21bdd0c9d3d8c6db950379282` |
| `v15.41-formal-connection-curvature-source-correspondence/test_gate.py` | `eadffeb059b32b3057420a9e33cbba44983b8664` |
| `v15.41-formal-connection-curvature-source-correspondence/test_linearized_connection.py` | `109cd05597d7a643ab8d0010ffd6d16d6e3ead81` |
| `v15.41-formal-connection-curvature-source-correspondence/test_operational_complex.py` | `89ab2e423accd6bf3db162434f5de946ba2bbf17` |
| `v15.42-duality-covariant-transport-repair/controls.py` | `a31d9a97a379823763b8d8a377166d3501eb0315` |
| `v15.42-duality-covariant-transport-repair/evidence.py` | `4662b73ec2b9724ad6ea06b3194b583c9f6ac3be` |
| `v15.42-duality-covariant-transport-repair/exact_algebra.py` | `c67ea42b61321469f7735ce589f2e729b241666a` |
| `v15.42-duality-covariant-transport-repair/fixtures.py` | `9704660b4183f040c84a0734b52702258d1d42da` |
| `v15.42-duality-covariant-transport-repair/holonomy.py` | `bad3f06b291bb448a903b4f48344a9e54a633f68` |
| `v15.42-duality-covariant-transport-repair/operational_complex.py` | `8163beba8e52bc2a3a6d0c8cf59dd1257222f65c` |
| `v15.42-duality-covariant-transport-repair/protocol_gate.py` | `681c5186c523cd8eb42ea343c6e96cdcb56c476c` |
| `v15.42-duality-covariant-transport-repair/protocol_types.py` | `e90a98d17baa6028f0d50a165f0b9d0046de13a2` |
| `v15.42-duality-covariant-transport-repair/selection.py` | `c8f592eb427135896c46bd8fccd6f3ddb48f7876` |
| `v15.42-duality-covariant-transport-repair/test_controls.py` | `41d40ae55465c6fc4a2d26f6a31e8abf952c8c01` |
| `v15.42-duality-covariant-transport-repair/test_evidence.py` | `3f48eee09ce549cb3904d7c435412c9df4ae06da` |
| `v15.42-duality-covariant-transport-repair/test_gate.py` | `220665a27ac8acb00f7257eba3eaa7132478c078` |
| `v15.42-duality-covariant-transport-repair/test_holonomy.py` | `c7a77b1face08800f3520c73672eeb6eec369ecd` |
| `v15.42-duality-covariant-transport-repair/test_selection.py` | `3824a34a8fe9eebc1a270ae798cbe3c76c6c1822` |
| `v15.42-duality-covariant-transport-repair/test_transport.py` | `a593a2d2772544ed4decc81877b79528702f08af` |
| `v15.42-duality-covariant-transport-repair/transport.py` | `df552284c16d43bc876340fbc13fe91eb9ee6a00` |

## Shared interfaces and wire schema

`projection.py` defines frozen dataclasses, with tuples throughout:

```python
CaseKey = tuple[int, str, Fraction, int]  # L, family, scale, response index
# Payload: L:int, scale:Fraction, labels:tuple[int,...],
# work:tuple[tuple[Fraction,...],...], neighbors:tuple[tuple[int,int],...],
# fields:tuple[Field,...]
# Field: family:str, response_index:int, values:tuple[Fraction,...]
# Projection: parent:str, dependencies:tuple[tuple[str,str],...],
# payloads:tuple[Payload,...], payload_hashes:tuple[str,...]
```

Wire top-level keys are exactly `schema`, `parent`, `dependencies`, `payloads`, `payload_hashes`; schema is `uqcf-v1543-inputs-v1`. Four payloads ordered `(5,1),(5,7/3),(7,1),(7,7/3)`; payload keys exactly `L,scale,labels,work,neighbors,fields`. Each field has exactly `family,response_index,values`, in spec family order and then ascending response index. Labels must be the complete integer carrier `0..L²-1` in explicit sorted order at ingestion; transformations occur only after validation. Each work row and field vector follows this declared order. Canonical undirected edges are sorted endpoint pairs, sorted uniquely. Fractions are strings `str(Fraction(value))`, with no alternative spelling. Payload hashes are SHA256 of their canonical UTF-8 JSON bytes. Dependencies must equal the frozen manifest projection, not merely be self-consistent with supplied hashes.

Public pure interfaces:

```python
canonical_bytes(value: object) -> bytes
decode_projection(raw: bytes) -> Projection
encode_projection(value: Projection) -> bytes
build_carrier(payload: Payload) -> Carrier  # complex, baseline, receipt
evaluate_field(carrier: Carrier, values: tuple[Fraction,...]) -> FieldResult
check_presentations(carrier: Carrier, values: tuple[Fraction,...]) -> dict
check_carrier_controls(carrier: Carrier) -> dict
check_response_controls(unit: Carrier, scaled: Carrier,
                        unit_fields: tuple[Field,...], scaled_fields: tuple[Field,...]) -> dict
evaluate_projection(projection: Projection) -> dict
classify(cases: tuple[dict,...], coverage_complete: bool) -> tuple[str,str]
audit() -> dict
```

`Carrier` contains the immutable inherited `OperationalComplex`, `BaselineConnection`, L, scale, and an identification receipt. `FieldResult` contains transport, tuple of `(cycle,K,invariant)` records, and exact zero/nonzero counts/histogram/sum; numerical internal data remain Fractions. Wire conversion happens at the output boundary. No metadata chooses mathematics.

### Task 1: Freeze evidence and enforce import ownership

**Files:** Create `evidence.py`, `dependencies.json`, `firewall.py`, `test_evidence.py`.

**Interfaces:** `verify_evidence(root: Path) -> dict`; `verify_origins(modules: tuple[object,...], allowed: dict[str,str]) -> dict`; `verify_firewall(paths: tuple[Path,...]) -> dict`. Evidence returns verified paths/blobs, parent ancestry, and spec pin. Pure modules receive no Path objects.

- [ ] **Step 1: Write RED tests for altered pins, missing ancestor, wrong import origin and forbidden evaluator capability.** Use temporary files and explicit small module objects, never modify frozen repository files.

```python
def test_origin_spoof_rejected(self):
    from types import SimpleNamespace
    from evidence import verify_origins
    with self.assertRaises(ValueError):
        verify_origins((SimpleNamespace(__name__='transport', __file__='/tmp/transport.py'),),
                       {'transport': 'df552284c16d43bc876340fbc13fe91eb9ee6a00'})

def test_forbidden_import_rejected(self):
    from firewall import verify_firewall
    from tempfile import TemporaryDirectory
    from pathlib import Path
    with TemporaryDirectory() as d:
        p = Path(d)/'application.py'
        p.write_text('import response_generation\n')
        with self.assertRaises(ValueError):
            verify_firewall((p,))
```

- [ ] **Step 2: Run RED:** `python -m unittest -v test_evidence.py`. Confirm failures name the missing behavior; record output and commit the tests.
- [ ] **Step 3: Implement pins and AST/origin checks.** Inventory the paths above and inherited evidence dictionaries without running scientific entry points. Use Git blob framing, strict path containment and exact module path+blob matches. Bootstrap entry points with `python -I`; explicitly add only D and the required original directory. Pure AST allowlist contains named symbols from fractions/dataclasses/collections/itertools and the reviewed mathematical modules; reject wildcard/dynamic imports, evaluation/reflection, I/O, process/network modules, and unapproved source/target imports. Entry-point I/O and evidence hashing have separately declared capabilities.

```python
def blob(raw):
    from hashlib import sha1
    return sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
# Use subprocess.run(['git','merge-base','--is-ancestor', PARENT, 'HEAD'],
#                    cwd=root, check=True) only inside the evidence boundary.
```

- [ ] **Step 4: Run GREEN:** `python -m unittest -v test_evidence.py`; also verify all manifest pins against the scientific parent. Record standard-library/external-package versus repository-module distinctions honestly.
- [ ] **Step 5: Commit:** `git add evidence.py dependencies.json firewall.py test_evidence.py && git commit -m 'feat(uqcf): freeze v15.43 evidence and evaluator boundary'`. Review this task before downstream work.

### Task 2: Strict projected inputs and isolated acquisition

**Files:** Create `projection.py`, `acquire.py`, `test_projection.py`.

**Interfaces:** Shared projection dataclasses and codec above; `acquire_projection() -> Projection` lives only in acquire.py. CLI `python -I acquire.py --out PATH` writes canonical bytes atomically after full validation. Coordinator invokes it only after parent replay; direct CLI still verifies evidence before imports.

- [ ] **Step 1: Write RED codec and producer tests.** Define `valid_projection_bytes()` in test_projection.py using the public dataclasses, all four canonical-size payloads, zero centered test fields, exact work diagonals zero/off-diagonals one, and a declared ring neighbor set. This is a codec fixture only, never an application carrier. Include one failure each for duplicate JSON keys, unknown source field, missing case, swapped field order, float/bool, malformed fraction, bad payload hash, wrong dependency list, and duplicate labels.

```python
def test_noncanonical_fraction_rejected(self):
    import json
    from projection import decode_projection
    wire = json.loads(valid_projection_bytes())
    wire['payloads'][0]['fields'][0]['values'][0] = '0/2'
    with self.assertRaisesRegex(ValueError, 'noncanonical_fraction'):
        decode_projection(json.dumps(wire).encode())

def test_injected_source_rejected(self):
    import json
    from projection import decode_projection
    wire = json.loads(valid_projection_bytes())
    wire['payloads'][0]['sources'] = []
    with self.assertRaisesRegex(ValueError, 'unknown_field'):
        decode_projection(json.dumps(wire).encode())
```

- [ ] **Step 2: Run RED:** `python -m unittest -v test_projection.py`; commit observed failing tests.
- [ ] **Step 3: Implement schema and projection.** Canonical JSON uses sorted keys, indent two, newline; reject duplicate keys via object_pairs_hook. Check exact keys/types, rational spelling before Fraction conversion, dimensions, zero sum, four payloads, all five families/indices, then hashes in that order. Tests must assert the specific error category (for example noncanonical_fraction, unknown_field, duplicate_case, wrong_field_order), so a stale hash cannot accidentally satisfy a malformed-input test. Acquire using only the pinned functions below; strip sources before serialization. Pin inspection occurs before import; run in a fresh process so its NumPy/inherited imports never enter the evaluator.

```python
# Inside acquisition, after evidence verification and origin checks:
for L in (5, 7):
    for amplitude in (Fraction(1), Fraction(7, 3)):
        canonical = generation.response_family(L, 'GLOBAL_BALANCE_COMPLETION', amplitude)
        geometry = geometry_module.construct_response_geometry(
            canonical.labels, canonical.sources, canonical.responses)
        fields = tuple(
            (key, r, tuple(values))
            for key in FAMILY_KEYS
            for r, values in enumerate(generation.response_family(L, key, amplitude).responses))
        # Project labels, geometry.work, sorted geometry.neighbors and fields
        # into the Payload dataclass; do not serialize canonical.sources.
```

- [ ] **Step 4: Run GREEN:** `python -m unittest -v test_projection.py`. Mock producer modules for tests of source metadata exclusion and prohibited audit calls; patch those calls to raise. With a fixed geometry/response return, changing a producer's source-only metadata must produce identical projected bytes. Real acquisition is deferred to Task 5 after parent replay; no response curvature runs in this task.
- [ ] **Step 5: Commit:** `git add projection.py acquire.py test_projection.py && git commit -m 'feat(uqcf): isolate and validate frozen response acquisition'`.

### Task 3: Identify actual carriers and apply the unchanged core

**Files:** Create `carriers.py`, `application.py`, `test_carriers.py`, `test_application.py`.

**Interfaces:** `Carrier`, `FieldResult`, `build_carrier`, `evaluate_field` as declared above. Both builders raise ValueError on invalid dimensions/types or non-identification, retaining the inherited reason. They do not call fixture constructors.

- [ ] **Step 1: Write RED tests using manufactured inputs only.** Tests build Payload objects from the frozen periodic fixture solely in test code; use all-zero fields and all impulse positions. A complete-graph neighbor input must fail. Patch the inherited operational builder to return NOT_IDENTIFIABLE and ensure no baseline/transport call follows.

```python
def test_null_and_impulse(self):
    from fractions import Fraction as Q
    from carriers import build_carrier
    from application import evaluate_field
    carrier = build_carrier(manufactured_payload(5))
    null = evaluate_field(carrier, (Q(7,3),)*25)
    self.assertEqual(null.nonzero_count, 0)
    impulse = evaluate_field(carrier, (Q(1),)+(Q(0),)*24)
    self.assertEqual(dict(impulse.histogram), {Q(0):13,Q(1,64):8,Q(1,16):4})
```

`manufactured_payload(L)` is defined in test_carriers.py: freeze `periodic_square_input(L)` into a Payload at scale one, with no response fields. Test_application.py imports that test helper explicitly. Production schema remains strict; this helper constructs internal test values only.

- [ ] **Step 2: Run RED:** `python -m unittest -v test_carriers.py test_application.py`; commit failure evidence.
- [ ] **Step 3: Implement direct application.** Validate work symmetry, diagonal zero, positive off-diagonal entries and neighbor-minimum consistency before inherited identification. Require IDENTIFIABLE complex and baseline, rank two, flatness, unique baseline orbit and the certified manifest. Preserve local module origin checks at bootstrap. Call the pinned constructor for every base case, without basis reconstruction of primary outputs.

```python
transport = construct_transport(carrier.complex, carrier.baseline, values)
records = tuple((cycle,
                 linearized_holonomy(carrier.baseline, transport, cycle))
                for cycle in carrier.complex.cycles)
invariants = tuple(curvature_invariant(K) for cycle, K in records)
if not transport.metric_compatibility_exact or not transport.reversal_exact:
    raise ValueError('transport_identity_failure')
if any(value < 0 for value in invariants):
    raise ValueError('negative_curvature_invariant')
```

Also require exact zero-matrix predicate consistency with zero invariant for the certified skew matrices. Store every face matrix and exact histogram/sum. Carrier construction has no fallback; fixture imports are forbidden in these production modules.

- [ ] **Step 4: Run GREEN:** `python -m unittest -v test_carriers.py test_application.py`. Add mismatch tests for baseline labels, field length/type, and manifest convention, using real inherited validators. Verify unchanged core blobs again.
- [ ] **Step 5: Commit:** `git add carriers.py application.py test_carriers.py test_application.py && git commit -m 'feat(uqcf): apply certified transport to validated carriers'`.

### Task 4: Presentation identities and complete control coverage

**Files:** Create `presentation_checks.py`, `application_controls.py`, `test_controls.py`; extend test_application.py only for independent-product comparisons.

**Interfaces:** `check_presentations`, `check_carrier_controls`, `check_response_controls` as above. Receipts contain actual evaluated counts, coverage keys, exact Boolean identities and transformation names. No timing values enter deterministic output.

- [ ] **Step 1: Write RED tests for all identities and real defects.** Exercise zero/impulse fields and an exact mixed centered field on L5/L7. Mutate a tangent delta, reverse a pullback product order, omit a relabel component permutation, or use the wrong scale in a test double; each must be detected. Include a relabeling that changes canonical cycle orientation/basepoint.

```python
def test_wrong_scale_is_rejected(self):
    from fractions import Fraction as Q
    from application_controls import check_response_controls
    unit, scaled, unit_fields, scaled_fields = control_inputs()
    bad = tuple(replace(f, values=tuple(Q(2)*v for v in f.values))
                for f in unit_fields)
    with self.assertRaises(ValueError):
        check_response_controls(unit, scaled, unit_fields, bad)
```

Define `control_inputs()` in test_controls.py from manufactured L5 work and its 7/3 scaling, with all five family names and every indexed centered impulse; scale the corresponding field vectors exactly. Import dataclasses.replace in the test. This synthetic family tests mechanics without measuring inherited responses.

- [ ] **Step 2: Run RED:** `python -m unittest -v test_controls.py`; commit the tests and mutation observations.
- [ ] **Step 3: Implement independent product expansion and presentation checks.** The independent oracle sums four ordered terms, with the derivative in each possible slot; it must not call the production recurrence.

```python
expanded = ZERO
for slot in range(4):
    term = identity(2)
    for i, edge in enumerate(edges):
        term = matmul(deltas[edge] if i == slot else baseline[edge], term)
    expanded = add(expanded, term)
```

For every face check all rotations and their reversals, using intervening baseline transport for conjugation; compare cotangent with transpose. Build the relabeled work, edges and field together under pi, reconstruct its operational carrier, and derive frame alignment from direction classes at each vertex. Require one D4 map satisfying both independent directions; never solve alignment from K. Use that map plus cycle rotation/reversal to compare based matrices. Check scale carriers by the same structural method.

Local D4 coverage: at every vertex use all eight sorted actions, plus the fixed mixed assignment. For every input field verify centered-gradient covariance and edge endpoint identities directly, then verify the resulting conjugation for every face. The inherited formula may be applied once per transformed field for initial validation; optimization may cache immutable topology, gradients and unaffected edge results, but must compare every declared edge/face identity with the independent endpoint formula. It may not reuse a pass flag from a different field. Verify this incremental evaluator against full certified `construct_transport` for every D4 action at every site on both constant and every-root impulse fields. Since both are exact linear maps, these basis checks certify the optimization for all fields. Primary 740 outputs still call the unchanged core directly.

- [ ] **Step 4: Implement actual-carrier controls and response identities.** Every one of four actual carriers gets constants 0 and 7/3 plus every-root unit impulses, with L5 counts 13/8/4 and L7 counts 37/8/4 at invariants 0,1/64,1/16. Response controls: compare all indexed scale pairs; add 7/3 to each field and require unchanged B/K; for each family/size at unit scale compare `2/3*u0 - 5/7*u1` against the linear combination of B/K, and repeat for scaled fields. Never assert linearity of the quadratic invariant under superposition; it is checked only under common scaling.

```python
combined = tuple(Q(2,3)*x-Q(5,7)*y for x,y in zip(left,right))
# Compare every B and K with the same linear combination; compare scale
# invariant with Q(49,9)*unit_invariant; shift invariant stays identical.
```

- [ ] **Step 5: Run GREEN:** `python -m unittest -v test_controls.py test_application.py`. Record exactly which mutations fail and measured control coverage. Cache only immutable mathematical values, keyed by full carrier/field/presentation; do not cache evidence or failure verdicts.
- [ ] **Step 6: Commit:** `git add presentation_checks.py application_controls.py test_controls.py test_application.py && git commit -m 'feat(uqcf): verify response application covariance and controls'`.

### Task 5: Ordered gate, full ledger and one local application

**Files:** Create `evaluate.py`, `response_geometry_gate.py`, `test_gate.py`, `docs/INPUTS.json`, `docs/RESULTS.json`, `README.md`.

**Interfaces:** `evaluate_projection`, `classify`, `audit` as above. CLI `python -I response_geometry_gate.py --out PATH` emits canonical ledger; `--check PATH` writes reproduced ledger to stdout, compares bytes and returns nonzero on mismatch/invalid outcome. Acquisition and evaluator are each `subprocess.run` children, with checked exit codes, explicit timeouts, controlled paths and no inherited PYTHONPATH. No shell command interpolation.

- [ ] **Step 1: Write RED gate tests with dependency-injected private executors.** Test each ordered failure position, missing/duplicate cases, failed child process and malformed child output. A private `_audit(executors)` may support tests; public audit takes no override arguments. Test all four outcome mappings from the approved spec using complete synthetic case records.

```python
def test_failure_stops_before_acquisition(self):
    calls=[]
    def fail():
        calls.append('parent')
        raise ValueError('parent_replay_mismatch')
    def forbidden():
        self.fail('acquisition ran after parent failure')
    result = run_test_gate(parent=fail, acquire=forbidden)
    self.assertEqual(result['status'], 'RESPONSE_APPLICATION_INVALID')
    self.assertEqual(result['first_failed_gate'], 'parent_replay')
    self.assertEqual(calls, ['parent'])
```

Define run_test_gate in test_gate.py as a wrapper around private `_audit` with deterministic success doubles for all other stages; first-failure tests replace each stage in turn and make every later stage raise if called. These are stage-order tests, not substitutes for real end-to-end verification.

- [ ] **Step 2: Run RED:** `python -m unittest -v test_gate.py`; commit test evidence.
- [ ] **Step 3: Implement ordering, coverage and result mapping.** Exact stage order: evidence, parent replay, acquisition/projection, all four carrier identifications, actual-carrier controls, complete response cases/identities, ledger. Within sizes always L5 before L7. Run parent protocol_gate.py --check in its original directory before acquisition and compare stdout to its pinned RESULTS bytes. Do not re-execute this expensive replay inside each unit test.

```python
expected = {(L,key,a,r) for L in (5,7) for key in FAMILY_KEYS
            for a in (Q(1),Q(7,3)) for r in range(L*L)}
if len(cases) != 740 or {case_key(c) for c in cases} != expected:
    raise ValueError('incomplete_or_duplicate_case_coverage')
primary = [c for c in cases if c['family']=='GLOBAL_BALANCE_COMPLETION']
if len(primary) != 148:
    raise ValueError('canonical_coverage')
nonflat = sum(c['nonzero_count'] > 0 for c in primary)
outcomes = {
    'NULL': ('CANONICAL_RESPONSE_CURVATURE_NULL', 'CHARACTERIZE_CERTIFIED_TRANSPORT_KERNEL'),
    'NONZERO': ('CANONICAL_RESPONSE_CURVATURE_NONZERO',
                'PREREGISTER_INTRINSIC_CURVATURE_INTERPRETATION_WITHOUT_SOURCE_FITTING'),
    'MIXED': ('CANONICAL_RESPONSE_CURVATURE_MIXED',
              'CHARACTERIZE_FINITE_SIZE_OR_RESPONSE_DEPENDENCE'),
}
status, next_object = outcomes['NULL' if nonflat == 0 else
                               'NONZERO' if nonflat == 148 else 'MIXED']
# Gate exceptions instead emit RESPONSE_APPLICATION_INVALID and
# REPAIR_APPLICATION_WITHOUT_RETUNING_TRANSPORT.
```

`case_key(c)` is defined in response_geometry_gate.py and parses exactly L, family, Fraction scale and response index. Public failure ledger carries error category, sanitized message, actual first stage/case, completed case/face counts, null unfinished results, false physical claims and source correspondence NOT_EVALUATED. Nonzero/Mixed/Null outcomes exit zero only if all gates pass. Unhandled exceptions are caught once at the stage boundary, with chained causes retained in stderr, never relabeled as another stage.

Schema ledger: `version,parent,spec_blob,dependency_pins,input_hashes,manifest,gate_receipts,carrier_receipts,control_receipts,cases,family_classifications,status,next_required_object,first_failed_gate,failure,completed_counts,claims`. Claims include every prohibition in spec section 11, plus inherited-axiom dependence. Keep acquisition permissions distinct from evaluator prohibitions. Each case has its four-part key, full face matrices/invariants, face counts, histogram/sum, presentation receipts, and `carrier_family=GLOBAL_BALANCE_COMPLETION`. Arrays use the declared order; fractions serialize canonically.

- [ ] **Step 4: Run focused GREEN and the new suite once.** `python -m unittest -v test_evidence.py test_projection.py test_carriers.py test_application.py test_controls.py test_gate.py`. Report actual test count; do not invent a target number or add tests solely to match it. Check dynamic repository import origins and execute pure math with file/process operations denied after bootstrap. Ensure evaluator imports no NumPy or acquisition module.
- [ ] **Step 5: Execute one full local audit and verify deterministic output.** After prerequisite tests pass, run `python -I response_geometry_gate.py --out docs/RESULTS.json`; coordinator also publishes verified canonical `docs/INPUTS.json`. A second `--check docs/RESULTS.json` is the required replay, not an opportunity to change interpretation. Record full 740 cases, 148 canonical cases and 30,260 face records (`10*(25*25+49*49)`) if valid. On invalid result stop at its actual gate, preserve failure evidence, and fix only implementation defects within the approved rule. Any mathematical protocol change requires a separate design, never a patched expected output.
- [ ] **Step 6: Write README and commit.** State actual status, command lines, finite scope, common-carrier control limitation, input permissions and unchanged scientific boundaries. Run `python -m compileall -q .`; commit only named new files and deterministic artifacts using `git add evaluate.py response_geometry_gate.py test_gate.py docs/INPUTS.json docs/RESULTS.json README.md` followed by `git commit -m 'feat(uqcf): publish exact response geometry application ledger'`. If acquisition failed, do not fabricate INPUTS or successful case records; commit only existing truthful artifacts and report the stop.

### Task 6: Exact-head certification, review and GitHub receipt

**Files:** Create D/`ci_verify.py` and `.github/workflows/uqcf-v1543-certified-response-geometry.yml`; append only execution receipts to this plan. No approved spec edits.

**Interfaces:** `python D/ci_verify.py` verifies additive scope, runs the suites, performs replays and prints an exact-head completion marker. It does not regenerate committed files in place.

- [ ] **Step 1: Implement the narrow workflow and verification runner.** Trigger on push only to `research/v15.43-certified-response-geometry`, restricted to D/**, this plan, the approved v15.43 spec and its workflow. No broad pull_request trigger, schedule or matrix. Read-only contents; Ubuntu 24.04; CPython 3.13.5; PYTHONHASHSEED=0; 180-minute job limit. Check out `${{ github.sha }}`, full history, persist-credentials false. Install `numpy==2.3.5` only after the dependency-free parent suite. Each subprocess has a finite timeout, reports its stage, and fails closed.

```yaml
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
      - run: python ResearchHistory/UQCF-GEM/demos/v15.43-certified-response-geometry/ci_verify.py
```

Runner order: scope/pins, v15.42 suite (48), install pinned NumPy, v15.43 focused suite with its observed frozen count, inherited v15.39 (8), v15.40 (9), v15.41 (26), unchanged v15.41 replay, one full v15.43 `--check` (which performs the required unchanged v15.42 replay before acquisition), projected INPUTS byte comparison, compilation, coverage/claim checks, final marker. This retains both parent replays without executing v15.42 twice in the same certification run. Reject skipped/expected-failure tests in official output.

Scope algorithm:

```python
for line in git_diff_name_status(PARENT, 'HEAD'):
    status, path = line.split('\t',1)
    if status != 'A' or not allowed_v1543_path(path):
        raise ValueError('nonadditive_scope')
```

Define both helpers in ci_verify.py: git_diff_name_status invokes Git with an argument list; allowed_v1543_path permits D/ plus the two exact v15.43 document paths and one workflow. Verify approved spec blob and plan prefix independently. No secret writes or force pushes.

- [ ] **Step 2: Verify locally at the complete tree.** Run the inherited 91 tests once if no already-recorded evidence covers this exact source tree; run v15.41 replay once, reuse Task 5's completed v15.43 replay for unchanged code. Validate workflow scope and observed test counts. A timeout is incomplete verification, not a mathematical null; report it and improve exact caching only if behavior-preserving and covered by targeted tests. Do not enlarge the job indefinitely or launch parallel duplicate runs.
- [ ] **Step 3: Review and publish.** Use the preserved subagent-driven execution preference: task-scoped reviews, then one fresh whole-branch reviewer. Review focus is source leakage, interface alignment, canonical-cycle comparisons, actual-carrier failures, complete coverage and honest claims. Resolve findings and rerun only affected tests. Publish reviewed commits to PR #54 and run official exact-head CI once.
- [ ] **Step 4: Append the actual receipt and certify the final head.** Record run/job/head/conclusion, counts, replay byte equality, artifact blobs and reviewer verdict. If this append changes the head, publish once and run the required final exact-head certification. Record that final run in PR metadata, not another plan commit. Keep all old artifacts unchanged, PR #54 draft/open/unmerged/mergeable and PR #53 untouched.
- [ ] **Step 5: Final report.** State the actual mechanical outcome and exact evidence; separate finite computation from interpretation and unassessed physics. Include the next object from the fixed outcome table. Report all execution rulings with costs if the chosen execution skill requires them. Do not begin a subsequent scientific stage automatically.

## Plan self-review and approval boundary

Coverage: spec 1–3 -> global constraints/Task 1; spec 4 -> Tasks 1–2; spec 5 -> Task 3 and scale checks in Task 4; spec 6–7 -> Tasks 3–5; spec 8–9 -> Tasks 4–5; spec 10 -> Tasks 1–6; spec 11 -> Tasks 5–6. Each of the five Review Focus items has an owning task and failure test. No primary case or family is selected after output. No numerical response-curvature result is assumed.

This plan is the deliverable of written-spec approval. It contains no executed response-curvature result and authorizes no merge. The previously selected subagent-driven method is preserved; written-plan review is the next gate before implementation. Approval of this concrete plan permits its six tasks to be executed without repeated between-task confirmation, within the existing publication and claim boundaries.

## Execution receipt — 2026-09-22

Published application commit `4741959e812f541f954b4d5f3f3cf97456b2f6c2` passed [GitHub Actions run 35685635987](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/35685635987), attempt 1, job `106611723946` (`certify`). GitHub reports the run and every job step completed successfully. Run creation: 2026-09-22T04:06:52Z; final run update: 2026-09-22T05:49:30Z.

The successful fail-closed `ci_verify.py` invocation enforces 170 tests (48 v15.42, 79 v15.43, 8 v15.39, 9 v15.40, 26 v15.41), unchanged v15.41 replay, full v15.43 replay including its v15.42 parent replay, byte-identical projected INPUTS and RESULTS, scope/pins, compilation, complete coverage, claim boundaries, and unchanged tracked tree/head. These checks are established by the successful runner and its reviewed mandatory assertions. The full job log exceeded the connector response limit; its final printed marker was not separately retrieved for this receipt.

Published artifact blobs:
- INPUTS: `f6435267950cde0985889056a67d5427f60f637f`.
- RESULTS: `937024b3f90570c9b177bfb2eee7cdab25a13985` (29,996,672 bytes).
- Outcome: `CANONICAL_RESPONSE_CURVATURE_NONZERO`.
- Coverage: 740 cases, 148 canonical cases, 30,260 faces; no failed audit gate.
- The recovery audit exited zero in 4,140 seconds and reproduced both previously reviewed artifact blobs exactly.

Prior scoped rereview and final review were recorded in execution history as reporting no outstanding findings. This receipt does not claim a new review or recreate the lost transient review files.

Ruling: retain the reviewed scientific source and exact recovered artifacts; restore the missing README as documentation only — the transient checkout was lost, while recovered JSON blobs match exactly — the remaining documentation provenance difference is recorded and does not change the mathematical computation.

This is reproducible progress in the UQCF-GEM information-to-geometry construction under its frozen assumptions. Uniqueness from foundational axioms and literature novelty remain unestablished. All five response families are nonflat on the common carrier; canonical specificity remains unresolved. Source correspondence stays NOT_EVALUATED; physical claims and scientific breakthrough stay false; Pillar 3 stays OPEN.

This append preserves the approved plan prefix byte-for-byte and requires final certification of the resulting commit. Record that final run in PR metadata without another plan append. PR #54 remains draft/open/unmerged; PR #53 is untouched. The next scientific object after closeout is PREREGISTER_INTRINSIC_CURVATURE_INTERPRETATION_WITHOUT_SOURCE_FITTING; no subsequent scientific stage is executed by this receipt.
