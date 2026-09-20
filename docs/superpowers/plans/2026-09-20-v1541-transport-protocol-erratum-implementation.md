# UQCF-GEM v15.41 Transport-Protocol Erratum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the v15.41 authoritative record so the untyped transport convention stops adjudication at `PROTOCOL_INVALID`, while retaining the prior exact execution and flatness/parity theorem only as non-adjudicating provenance.

**Architecture:** Add an explicit transport-type manifest and exact pre-adjudication audit to the existing linearized-connection layer. The gate verifies evidence, validates the manifest, runs a mandatory manufactured nonconstant-field audit, and returns immediately on the frozen literal convention's rank inconsistency. Flatness/parity calculations run only in a separately labeled diagnostic path and cannot populate downstream scientific verdicts.

**Tech Stack:** Python 3.13.5; standard-library `dataclasses`, `enum`, `fractions.Fraction`, `json`, and `unittest`; existing dependency-free exact algebra; NumPy 2.3.5 only in the inherited hash-pinned v15.40 adapter; GitHub Actions on `ubuntu-24.04`.

**Spec:** `docs/superpowers/specs/2026-09-20-v1541-transport-protocol-erratum-design.md`

## Global Constraints

- Preserve original v15.41 design blob `6d35aae0ccb6c2584d26d5a83d522b3cc7036728` and approved erratum blob `d40d03d9d2498ce54839b15dad00c1505c1a586a` byte-for-byte.
- Base correction work on PR #52 head `3f8a514b9d9dbce40b450441e6ed1d5310f8d59a`; do not modify v15.40 or earlier artifacts.
- Do not select a replacement connection, transport direction, dualization, variation sign, torsion rule, lift, or curvature observable.
- The literal audit is tangent-vector transport, reverse directed transport back to the cycle base point, and positive `delta_v_i = +(u[x_i]/2) v_i`.
- Run a mandatory nonconstant manufactured exact field before connection, curvature, correspondence, or control adjudication.
- Any manifest mismatch or rank inconsistency returns `PROTOCOL_INVALID` immediately with `REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION`.
- Under `PROTOCOL_INVALID`, `connection_identifiable`, `curvature_source_map_identifiable`, `canonical_correspondence`, and `control_all_sizes` are `null`.
- Preserve the old `CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE` record only under `superseded_execution_receipt`.
- Preserve zero-curvature and odd/even parity only under `non_adjudicating_protocol_diagnostics` labeled `NON_ADJUDICATING_PROTOCOL_DIAGNOSTIC`.
- Authoritative JSON contains no floats, retains every evidence hash and exact-head receipt, and replays byte-for-byte.
- Keep construction-firewall counters zero, physical-interpretation flags false, `scientific_breakthrough=false`, and `Pillar_3=OPEN`.
- No historical connection artifact may select a repair. Keep PR #52 draft, open, and unmerged.

## Review Focus

1. **Implicit repair during typing:** Task 2 tests every manifest field and rejects forward, transpose, inverse, or sign substitutions.
2. **Adjudication after failure:** Task 4 injects a raising adjudicator and requires all downstream verdicts to remain `null`.
3. **Constant manufactured control:** Task 2 pins a nonconstant rational field and exact ranks `50/51` at L=5 and `98/99` at L=7.
4. **Diagnostic promoted to verdict:** Tasks 3 and 5 namespace diagnostics and test that they cannot change top-level classification.
5. **Provenance/replay loss:** Task 5 pins prior result blob `5228c2754c7ea1b1da6966adcfd34135250132cb`, rejects floats recursively, and compares clean replay bytes.

---

## File Map

- Modify `linearized_connection.py`: typed manifest, literal protocol audit, isolated diagnostic helpers.
- Modify `test_linearized_connection.py`: typing, inconsistency, row-space, arbitrary-field flatness, and parity tests.
- Modify `connection_curvature_gate.py`: audit-first ordering, immediate stop, nullable verdicts, diagnostic/provenance namespaces.
- Modify `test_gate.py`: fail-fast, schema, firewall, provenance, and replay tests.
- Modify `docs/RESULTS.json`: corrected authoritative result with nested superseded receipt.
- Modify `README.md`: corrected result and theorem/computation/interpretation boundaries.
- Append an erratum receipt to the 2026-09-19 implementation plan without rewriting its history.
- Modify the v15.41 workflow to cover both erratum documents and certify exact head.
- Update PR #52 description only after the implementation commit and exact-head CI exist.

All demo paths are under `ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/`.

### Task 1: Freeze the corrected RED contract

**Files:**
- Modify: `test_linearized_connection.py`
- Modify: `test_gate.py`
- Modify: `docs/superpowers/plans/2026-09-19-v1541-formal-connection-curvature-source-correspondence-implementation.md` only to append the RED receipt.

**Interfaces:**
- Consumes: approved erratum and existing public interfaces.
- Produces: failing tests naming the new interfaces before implementation.

- [ ] **Step 1: Add manifest and exact-defect tests**

```python
def test_literal_frozen_manifest_is_explicit_and_inconsistent(self):
    manifest = TransportManifest.literal_frozen()
    self.assertEqual(manifest.carrier, CarrierKind.TANGENT_VECTOR)
    self.assertEqual(manifest.edge_direction, TransportDirection.REVERSE)
    self.assertEqual(manifest.matrix_action, MatrixAction.DIRECT)
    self.assertEqual(manifest.variation_sign, 1)
    for L, expected in ((5, (50, 51)), (7, (98, 99))):
        complex_ = construct_operational_complex(*periodic_square_input(L)).complex
        field = tuple(Fraction((i*i + 3*i) % 11 - 5) for i in range(L*L))
        result = audit_transport_protocol(complex_, field, manifest)
        self.assertFalse(result.protocol_valid)
        self.assertEqual((result.coefficient_rank, result.augmented_rank), expected)
        self.assertEqual(result.reason, "literal_frozen_rank_inconsistency")

def test_transport_manifest_rejects_implicit_repair(self):
    manifest = TransportManifest.literal_frozen()
    with self.assertRaises(ValueError):
        replace(manifest, edge_direction=TransportDirection.FORWARD).validate_literal_frozen()
    with self.assertRaises(ValueError):
        replace(manifest, matrix_action=MatrixAction.TRANSPOSE).validate_literal_frozen()
    with self.assertRaises(ValueError):
        replace(manifest, variation_sign=-1).validate_literal_frozen()
```

- [ ] **Step 2: Add fail-fast ledger tests**

```python
def test_erratum_stops_before_scientific_adjudication(self):
    result = audit()
    self.assertFalse(result["protocol_valid"])
    self.assertEqual(result["status"], "PROTOCOL_INVALID")
    self.assertEqual(result["next_required_object"],
                     "REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION")
    for key in ("connection_identifiable",
                "curvature_source_map_identifiable",
                "canonical_correspondence", "control_all_sizes"):
        self.assertIsNone(result[key])
```

- [ ] **Step 3: Run the four focused tests**

Run the two new linearized tests plus gate tests for immediate stopping and non-authoritative provenance. Expected: FAIL only because the new interfaces and fields do not exist. Record command, failing names, exit code, and head SHA in the appended erratum receipt.

- [ ] **Step 4: Commit**

```bash
git add ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_linearized_connection.py \
        ResearchHistory/UQCF-GEM/demos/v15.41-formal-connection-curvature-source-correspondence/test_gate.py \
        docs/superpowers/plans/2026-09-19-v1541-formal-connection-curvature-source-correspondence-implementation.md
git commit -m "test(uqcf): freeze v15.41 transport erratum contract"
```

### Task 2: Implement typed transport audit

**Files:**
- Modify: `linearized_connection.py`
- Test: `test_linearized_connection.py`

**Interfaces:**
- Consumes: `OperationalComplex`, exact scalar field, explicit `TransportManifest`.
- Produces: `ProtocolAudit(protocol_valid, coefficient_rank, augmented_rank, reason, manifest)`; no connection verdict.

- [ ] **Step 1: Define exact types**

```python
class CarrierKind(str, Enum):
    TANGENT_VECTOR = "tangent_vector"
    COVECTOR = "covector"

class TransportDirection(str, Enum):
    FORWARD = "forward"
    REVERSE = "reverse"

class MatrixAction(str, Enum):
    DIRECT = "direct"
    INVERSE = "inverse"
    TRANSPOSE = "transpose"
    INVERSE_TRANSPOSE = "inverse_transpose"

@dataclass(frozen=True)
class TransportManifest:
    carrier: CarrierKind
    edge_direction: TransportDirection
    matrix_action: MatrixAction
    dualized: bool
    variation_sign: int
    basepoint_rule: str
    orientation_rule: str

    @classmethod
    def literal_frozen(cls):
        return cls(CarrierKind.TANGENT_VECTOR, TransportDirection.REVERSE,
                   MatrixAction.DIRECT, False, 1,
                   "transport_later_edges_back_to_x0",
                   "both_cycle_orientations")

    def validate_literal_frozen(self):
        if self != type(self).literal_frozen():
            raise ValueError("manifest does not encode the literal frozen convention")
        return True

@dataclass(frozen=True)
class ProtocolAudit:
    protocol_valid: bool
    coefficient_rank: int
    augmented_rank: int
    reason: str | None
    manifest: TransportManifest
```

- [ ] **Step 2: Separate closure assembly from convention choice**

Add `_transport_factor(cycle, prefix, manifest)`; for the literal manifest it selects the reverse directed edge `(cycle[prefix + 1], cycle[prefix])` and applies that edge matrix directly. Thread edge direction, matrix action, dualization, and the integer variation sign through closure assembly. Reject carrier/action mismatches; never convert one convention into another.

- [ ] **Step 3: Implement the exact rank audit**

```python
def audit_transport_protocol(complex_, field, manifest):
    manifest.validate_literal_frozen()
    lift = construct_isotropic_lift(complex_, field)
    edges = tuple(sorted(tuple(sorted(edge)) for edge in complex_.neighbors))
    rows, rhs = _closure_system(complex_, lift, edges, manifest)
    coefficient_rank = rank(rows, ncols=len(edges))
    augmented_rank = rank(tuple(row + (value,) for row, value in zip(rows, rhs)),
                          ncols=len(edges) + 1)
    valid = coefficient_rank == augmented_rank
    return ProtocolAudit(valid, coefficient_rank, augmented_rank,
                         None if valid else "literal_frozen_rank_inconsistency",
                         manifest)
```

Do not call `solve_unique` when ranks differ.

- [ ] **Step 4: Verify and commit**

Run the two Task 1 linearized tests; require PASS with `50/51` and `98/99`. Commit as `fix(uqcf): add typed v15.41 transport audit`.

### Task 3: Isolate diagnostic theorems

**Files:**
- Modify: `linearized_connection.py`
- Modify: `test_linearized_connection.py`

**Interfaces:**
- Consumes: operational complex and exact field.
- Produces: diagnostic records only; no `ConnectionStatus` and no scientific verdict.

- [ ] **Step 1: Add exact tests**

Test that appending the face-circulation row does not increase the local closure rank. Test the executed forward/positive diagnostic on the existing field, `((7*i+2)%13)-6`, and a standard-basis field at L=5. Test parity witnesses exactly:

```python
expected = {
    5: (50, 50, 0), 6: (71, 72, 1), 7: (98, 98, 0),
    8: (127, 128, 1), 9: (162, 162, 0),
}
```

Every witness must also report zero face curvature.

- [ ] **Step 2: Implement diagnostic-only helpers**

Add frozen `FlatnessDiagnostic` and `ParityWitness` dataclasses. Implement `local_circulation_rowspace_witness()`, `executed_flatness_diagnostic()`, and `parity_witness()` using exact ranks and the already executed forward/positive ansatz. None may call the scientific classifier.

- [ ] **Step 3: Verify and commit**

Run `python -m unittest -v test_linearized_connection.py`; require PASS. Commit as `test(uqcf): isolate v15.41 flatness parity diagnostics`.

### Task 4: Enforce audit-before-adjudication

**Files:**
- Modify: `connection_curvature_gate.py`
- Modify: `test_gate.py`

**Interfaces:**
- Consumes: verified evidence, literal manifest, manufactured fields at L=5 and L=7.
- Produces: authoritative `PROTOCOL_INVALID` ledger; downstream adjudicator is unreachable.

- [ ] **Step 1: Add an injectable boundary**

Have cached `audit()` delegate to `_audit(adjudicator=_run_scientific_adjudication)`. In `_audit`, verify evidence, build the literal manifest, run both manufactured-field audits, and return `_protocol_invalid_ledger(...)` when either fails. Do not compute size audits, cell rows, targets, contractions, correspondence, or controls before this branch.

- [ ] **Step 2: Prove unreachability**

```python
def test_failed_protocol_never_calls_scientific_adjudicator(self):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("scientific adjudicator called after protocol failure")
    self.assertEqual(_audit(adjudicator=forbidden)["status"], "PROTOCOL_INVALID")
```

- [ ] **Step 3: Emit nullable verdicts**

The corrected dictionary must set `protocol_valid=False`, the required status/next object, and all four downstream verdict fields to `None`. Retain firewall zeroes, `Pillar_3="OPEN"`, and all physical derivation flags false.

- [ ] **Step 4: Verify and commit**

Run the focused fail-fast tests; require PASS. Commit as `fix(uqcf): stop v15.41 adjudication on protocol defect`.

### Task 5: Preserve provenance and rewrite canonical artifacts

**Files:**
- Modify: `connection_curvature_gate.py`
- Modify: `test_gate.py`
- Modify: `docs/RESULTS.json`
- Modify: `README.md`

**Interfaces:**
- Consumes: prior result blob `5228c2754c7ea1b1da6966adcfd34135250132cb` and exact diagnostic helpers.
- Produces: byte-stable corrected ledger and human-readable claim boundary.

- [ ] **Step 1: Add lossless superseded receipt**

```python
"superseded_execution_receipt": {
    "authoritative": False,
    "status": "CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE",
    "result_blob": "5228c2754c7ea1b1da6966adcfd34135250132cb",
    "reason_superseded": "transport_protocol_not_typed_precisely_enough",
    "prior_exact_head_receipts": prior_exact_head_receipts,
}
```

Copy receipt constants from the historical plan or prior ledger source; do not regenerate them.

- [ ] **Step 2: Add one diagnostic namespace**

Generate exact fields for label, executed convention, standard-basis L=5 flatness, local row-space identity, arbitrary-field flatness, and parity rows `(5,50,50,0)`, `(6,71,72,1)`, `(7,98,98,0)`, `(8,127,128,1)`, `(9,162,162,0)`. Compare generated values to these frozen witnesses before serialization.

- [ ] **Step 3: Strengthen tests**

Recursively reject floats; verify evidence hashes, physical flags, and Pillar 3; verify removing diagnostics cannot change authoritative classification; verify the old status appears only inside the superseded receipt.

- [ ] **Step 4: Generate and replay**

```bash
python connection_curvature_gate.py --out docs/RESULTS.json
python connection_curvature_gate.py --check docs/RESULTS.json > /tmp/v1541-erratum-results.json
cmp docs/RESULTS.json /tmp/v1541-erratum-results.json
```

Require `cmp` exit 0.

- [ ] **Step 5: Rewrite README and run full local verification**

Lead with `PROTOCOL_INVALID`. Include sections `Protocol defect`, `Non-adjudicating theorem`, `Superseded execution receipt`, `Claim boundary`, and `Reproduce`. State that there is no adjudicating connection, curvature, or source correspondence and no evidence for or against physical gravity.

Run all three v15.41 test files, canonical replay, `cmp`, and compileall. Commit as `docs(uqcf): publish corrected v15.41 protocol-invalid ledger`.

### Task 6: Expand CI and certify exact head

**Files:**
- Modify: `.github/workflows/uqcf-v1541-formal-connection-curvature-source-correspondence.yml`
- Append receipts to the 2026-09-19 plan and this plan.
- Update: PR #52 description after successful exact-head CI.

**Interfaces:**
- Consumes: corrected artifact set.
- Produces: final exact-head GitHub Actions success and auditable draft PR.

- [ ] **Step 1: Extend workflow coverage**

Add both erratum spec and plan paths to `on.push.paths` and the additive-scope `allowed` set. Retain original document paths and the base SHA `84aa1c81fd86ac4d7a06015482f98572f3afc05f`.

- [ ] **Step 2: Verify inherited and corrected suites**

Retain the 17 inherited v15.39/v15.40 tests. Rename the current step to `Run corrected v15.41 transport erratum gate`; run all v15.41 tests, replay, `cmp`, and compilation.

- [ ] **Step 3: Append exact receipts**

Append without rewriting historical text: RED SHA, correction SHAs, both design blobs, prior/corrected result blobs, workflow run URL/ID, job ID, exact tested head SHA, inherited and corrected test counts, replay result, and PR state.

- [ ] **Step 4: Commit and certify**

Commit as `ci(uqcf): certify v15.41 transport erratum`. Push, require workflow success at the exact branch head, and rerun after any receipt-only commit so the final head itself is certified.

- [ ] **Step 5: Update PR #52 without merging**

Link both approved erratum documents; report `PROTOCOL_INVALID`; distinguish the superseded receipt and diagnostic theorem; include exact workflow URL/head; retain draft/open/unmerged state.

## Implementation Completion Gate

Implementation is complete only when both design blobs are unchanged; exact rank witnesses are `50/51` and `98/99`; adjudication is unreachable after failure; authoritative status is `PROTOCOL_INVALID`; downstream verdicts are `null`; prior result and diagnostics are non-authoritative; JSON has no floats and replays byte-for-byte; inherited and corrected tests pass at exact head; and PR #52 remains draft, open, unmerged, and mergeable.

No implementation work begins until this plan is reviewed and approved.
