# v15.39 Higher-Incidence Source Axioms Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Implement and certify the preregistered v15.39 typed higher-incidence source lift, three response axioms, and their common exact adversarial canary without changing any inherited theory artifact.

**Architecture:** Reuse the hash-pinned v15.28 exact chain-complex and rational-linear-algebra modules. A single new gate module owns the typed source lift, boundary-sector coordinate model, three candidate maps, exact canary observables, and deterministic ledger; a focused unittest file specifies behavior before implementation. The GitHub workflow enforces additive scope from the exact v15.38 head, inherited regressions, deterministic replay, and the claim firewall.

**Tech Stack:** Python 3.13.5, standard library `fractions.Fraction`, NumPy 2.3.5 only for inherited integer incidence arrays, `unittest`, GitHub Actions on `ubuntu-24.04`.

**Spec:** `docs/superpowers/specs/2026-09-19-v1539-higher-incidence-source-axioms-design.md`

## Global Constraints

- Base exactly on v15.38 certified head `825b47b276c6a17df35e6620f6de6630a1d729e2`.
- Preserve the preregistration commit `c71d16ead84620a9d3ac8762c3feb59e5be5c487` and design blob `edabb9837d293f49ff78f007c31c3904bf04c3e5`.
- Treat the higher-incidence source lift and all three response laws as `NEW_ASSUMPTION`; never mark them derived from the frozen ontology.
- Use unchanged formulas at `L=5,7,9,11`; `L=11` is the locked holdout.
- Candidate construction performs zero eigenspectrum queries, zero spectral-edge tuning, zero gravity fitting, and zero candidate-specific thresholding.
- All adjudicating support and commutator predicates use exact rational zero/nonzero tests.
- Preserve projective scale freedom; `lambda=1` is a ledger representative, not a derived physical coupling.
- Do not introduce a metric, Hodge/minimum-norm selector, pruning, entropy, outcome selection, or physical time.
- Keep `physical_gravity_derived=false`, `continuum_limit_derived=false`, and `Pillar_3=OPEN` for every result.
- All repository changes are additive under the v15.39 demo directory plus this plan and one branch-specific workflow.

## Review Focus

1. **Reflection/orientation signs:** a D4 reflection must transform `delta`, `q`, and `kappa` exactly, including edge and face orientation signs; Task 2 adds a generator-level covariance test.
2. **Coarse-null versus fiber-nonnull composition:** a full oriented face boundary must have `q=0` and nonzero composed `kappa`, with this ontology concession explicit in the ledger; Task 2 adds that exact test.
3. **Homology kernel leakage:** `4I-A` is singular on translation-fixed homology but must be exactly invertible on `B=im(B2)`; Task 3 tests the boundary restriction and rejects any ambient pseudoinverse shortcut.
4. **Accidental absolute-scale claim:** changing nonzero rational `lambda` must preserve closure and all projective verdicts; Task 4 tests two unequal `lambda` values.
5. **Remote-shell wraparound/duplicate edges:** exact far-shell support and perpendicular-pair sums must be invariant under source translation and must not depend on floating tolerances; Task 4 tests translated sources at all four sizes.

---

## File map

- Create `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py`: exact source model, candidate maps, canary observables, adjudication, and canonical JSON.
- Create `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`: behavior-first structural, candidate, canary, ledger, and firewall tests.
- Create `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/docs/RESULTS.json`: byte-replayable authoritative result.
- Create `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/README.md`: theorem/computation/interpretation report.
- Create `.github/workflows/uqcf-v1539-higher-incidence-source-axioms.yml`: additive-scope and exact-head certification.

### Task 1: Freeze the RED contract and CI boundary

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`
- Create: `.github/workflows/uqcf-v1539-higher-incidence-source-axioms.yml`

**Interfaces:**
- Consumes: the approved v15.39 spec and inherited v15.38 branch.
- Produces: failing tests importing `source_axiom_canary`; CI that records the intended missing-module failure and later certifies the same suite.

- [x] **Step 1: Add the failing test skeleton**

Create `test_gate.py` with these imports and test names:

```python
import json
from pathlib import Path
import unittest

from source_axiom_canary import CANDIDATE_KEYS, audit, canonical_json

class HigherIncidenceSourceAxiomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_source_lift_typing_covariance_and_composition(self):
        p = self.result["source_protocol"]
        self.assertTrue(p["all_B1_kappa_zero"])
        self.assertTrue(p["generator_covariance_exact"])
        self.assertTrue(p["source_additivity_exact"])
        self.assertTrue(p["source_reversal_exact"])

    def test_closed_face_q_null_is_fiber_nonnull(self):
        p = self.result["source_protocol"]
        self.assertTrue(p["closed_face_coarse_q_null"])
        self.assertTrue(p["closed_face_higher_incidence_source_nonnull"])

    def test_candidate_formulas_and_balance_uniqueness(self):
        self.assertEqual(tuple(self.result["candidate_keys"]), CANDIDATE_KEYS)
        self.assertTrue(self.result["all_candidate_outputs_in_boundary_sector"])
        self.assertTrue(self.result["global_balance_boundary_inverse_exact"])

    def test_exact_remote_and_commutator_predicates(self):
        self.assertTrue(self.result["exact_zero_nonzero_predicates_only"])
        self.assertEqual(self.result["candidate_specific_thresholds"], 0)
        self.assertTrue(self.result["commuting_axis_precursor_zero"])

    def test_multisize_holdout_and_mechanical_verdicts(self):
        self.assertEqual(self.result["finite_size_controls"], [5, 7, 9, 11])
        self.assertTrue(self.result["holdout_formula_unchanged"])
        self.assertTrue(self.result["mechanical_candidate_rule_applied"])

    def test_projective_scale_and_hostile_controls(self):
        self.assertTrue(self.result["projective_scale_discipline_enforced"])
        self.assertFalse(self.result["absolute_response_scale_derived"])
        self.assertTrue(all(self.result["hostile_controls"].values()))

    def test_axiom_and_claim_firewall(self):
        self.assertTrue(self.result["new_source_semantics_axiom_added"])
        self.assertFalse(self.result["source_axiom_derived_from_frozen_ontology"])
        for key in (
            "physical_gravity_derived", "einstein_equations_derived",
            "continuum_limit_derived", "uses_pruning", "uses_entropy",
            "uses_physical_time", "scientific_breakthrough",
        ):
            self.assertFalse(self.result[key], key)
        self.assertEqual(self.result["Pillar_3"], "OPEN")

    def test_committed_ledger_is_exact(self):
        committed = Path("docs/RESULTS.json").read_text()
        self.assertEqual(committed, canonical_json(self.result))
        self.assertEqual(json.loads(committed), self.result)
```

Commit this complete RED file without adding the implementation module.

- [x] **Step 2: Add the branch workflow**

Create a workflow triggered on `research/v15.39-higher-incidence-source-axioms`. It must:

```yaml
name: UQCF v15.39 Higher-Incidence Source Axioms
on:
  push:
    branches: [research/v15.39-higher-incidence-source-axioms]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  verify:
    runs-on: ubuntu-24.04
    timeout-minutes: 60
    env:
      PYTHONHASHSEED: '0'
```

Add steps for checkout, Python `3.13.5`, `numpy==2.3.5`, additive-scope verification against `825b47b276c6a17df35e6620f6de6630a1d729e2`, inherited v15.37/v15.38 unittests, v15.39 unittests, result replay, compilation, and ledger assertions.

The additive allowlist is exactly:

```python
allowed = {
    "docs/superpowers/specs/2026-09-19-v1539-higher-incidence-source-axioms-design.md",
    "docs/superpowers/plans/2026-09-19-v1539-higher-incidence-source-axioms-implementation.md",
    ".github/workflows/uqcf-v1539-higher-incidence-source-axioms.yml",
}
demo = "ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/"
```

Require every diff entry to have status `A` and to be inside `demo` or `allowed`.

- [x] **Step 3: Run RED in GitHub Actions**

Expected failure:

```text
ModuleNotFoundError: No module named 'source_axiom_canary'
```

Confirm inherited v15.37/v15.38 suites ran before the intended failure or split the workflow so their success is visible.

- [x] **Step 4: Record the RED receipt**

Append the run ID, job ID, exact head SHA, and intended missing-module error to this plan under a `RED receipt` heading using a normal GitHub file update.

- [x] **Step 5: Commit**

Commit message:

```text
test: preregister v15.39 source-axiom canary
```

### Task 2: Implement the exact typed source lift

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`

**Interfaces:**
- Consumes: hash-pinned `representation_actions.py`, `exact_linear.py`, v15.38 `RESULTS.json`, and the design spec.
- Produces:
  - `SourceOccurrence(face_index: int, edge_index: int, amplitude: Fraction)`
  - `LiftedSource(delta, q, kappa, incidence_sign)`
  - `source_lift(c, face_index, edge_index, amplitude) -> LiftedSource`
  - `compose_sources(sources) -> LiftedSource`
  - `transform_occurrence(actions, c, occurrence, g) -> SourceOccurrence`

- [x] **Step 1: Pin and load inherited evidence**

Define:

```python
BASE_SHA = "825b47b276c6a17df35e6620f6de6630a1d729e2"
EVIDENCE = {
    "representation_actions.py": (..., "7260147cd6ca47ec21634172b44b98de726904af"),
    "exact_linear.py": (..., "05cc1b8cfec70d501408377b5e44190b259a4514"),
    "v15.38-results": (..., "9caa94fe6e700a6684fa9c899b37503a2736bece"),
    "v15.39-design": (..., "edabb9837d293f49ff78f007c31c3904bf04c3e5"),
}
```

`verify_evidence()` must compute git-blob hashes and require the v15.38 status
`PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE`.

- [x] **Step 2: Write exact lift tests**

Use one face and each of its four loop entries. Assert:

```python
self.assertTrue(all(x == 0 for x in matvec(B1, lifted.kappa)))
self.assertEqual(lifted.q, matvec(B1, lifted.delta))
self.assertIn(lifted.incidence_sign, (-1, 1))
```

For translation, quarter-turn, and reflection generators, assert transformed `delta`, `q`, and `kappa` equal the signed-permutation actions exactly.

- [x] **Step 3: Implement `source_lift`**

Use edge-amplitude convention exactly:

```python
delta[e] = Fraction(amplitude)
q = B1 @ delta
sigma = int(B2[e, f])
kappa = Fraction(amplitude) * sigma * B2[:, f]
```

Reject an edge not incident on the face and reject non-rational/non-finite inputs rather than coercing floats.

- [x] **Step 4: Implement composition and the closed-face concession**

Compose four occurrences on one face with edge amplitudes equal to their boundary signs. Assert:

```python
delta_total == B2[:, f]
q_total == 0
kappa_total == 4 * B2[:, f]
```

Record `closed_face_coarse_q_null=true` and
`closed_face_higher_incidence_source_nonnull=true`.

- [x] **Step 5: Run the source tests**

Run:

```bash
python -m unittest -v   test_gate.HigherIncidenceSourceAxiomTests.test_source_lift_typing_covariance_and_composition   test_gate.HigherIncidenceSourceAxiomTests.test_closed_face_q_null_is_fiber_nonnull
```

Expected: PASS.

- [x] **Step 6: Commit**

Commit message:

```text
feat: add typed higher-incidence source lift
```

### Task 3: Implement the three exact response candidates

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`

**Interfaces:**
- Consumes: `LiftedSource.kappa`, inherited cell actions, and exact rational linear algebra.
- Produces:
  - `CANDIDATE_KEYS = ("DIRECT_INHERITANCE", "ONE_INCIDENCE_TRANSPORT", "GLOBAL_BALANCE_COMPLETION")`
  - `face_augmentation_coordinates(c, face_index) -> tuple[Fraction, ...]`
  - `solve_unique(ql, matrix, rhs) -> tuple[Fraction, ...]`
  - `candidate_response(actions, ql, c, lifted, key) -> CandidateResponse`

- [x] **Step 1: Build primitive adjacency without a dense ambient matrix**

Define the four translations from `L`:

```python
((1, 0), (L - 1, 0), (0, 1), (0, L - 1))
```

For an edge vector, sum the four exact signed-permutation actions. For face augmentation, sum their restricted face representations.

- [x] **Step 2: Build canonical boundary coordinates**

Use `actions.augmentation_basis(L*L)` for sum-zero face coefficients. For face `f`, use the canonical lift

```python
phi_f = e_f - (1 / L**2) * 1
```

so `B2 phi_f = B2 e_f`. Map augmentation coordinates back to an edge boundary with exact multiplication by integer `B2`.

- [x] **Step 3: Add failing candidate tests**

For every `L in (5,7,9,11)` and every candidate, assert:

- output is nonzero and in `im(B2)`;
- `B1 y=0`;
- direct response equals `kappa`;
- one-step response equals the four-translation sum;
- global balance satisfies `(4I-A)y=kappa` exactly;
- `D_face` has a unique solution in all `L**2-1` augmentation coordinates;
- no function named `pinv`, `lstsq`, `eig`, or `eigh` occurs in the module source.

- [x] **Step 4: Implement exact unique solving**

Construct the augmented matrix `[D_face | rhs]`, call inherited `ql.rref`, require coefficient pivots `0..n-1`, extract the final column, and verify `D_face @ x == rhs`. Do not invert on ambient `Z` and do not project with a metric.

- [x] **Step 5: Implement C0, C1, and C2**

C0 returns `kappa`. C1 applies edge adjacency once. C2 solves on face augmentation, maps back through `B2`, and verifies the ambient balance equation exactly.

Each `CandidateResponse` records:

```python
key
response
boundary_sector = True
unique_response_ray = True
spectrum_queries = 0
spectral_edge_parameters = 0
gravity_fit_parameters = 0
candidate_specific_thresholds = 0
classification = "NEW_RESPONSE_AXIOM_CANDIDATE"
```

- [x] **Step 6: Run candidate tests**

Expected: PASS for all four sizes. If C2 is singular on any boundary sector, record
`STRUCTURALLY_REJECTED`; do not regularize it.

- [x] **Step 7: Commit**

Commit message:

```text
feat: implement preregistered response candidates
```

### Task 4: Implement the exact common adversarial canary

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`

**Interfaces:**
- Consumes: candidate response rays.
- Produces:
  - `remote_shell(c, source_face) -> tuple[face, ...]`
  - `remote_support_square(c, y, source_face) -> Fraction`
  - `remote_commutator_precursor(c, y, source_face) -> Fraction`
  - `exact_size_audit(L: int) -> dict`

- [x] **Step 1: Add exact remote-shell tests**

Use cyclic Manhattan face distance and require the shell distance to be `L-1` for odd `L`. Translate the source from `(0,0)` to `(1,2)` and require identical candidate metrics.

- [x] **Step 2: Implement exact support**

Collect every oriented edge incident on maximally distant faces and sum `y_e**2` in `Fraction` arithmetic. Duplicates must be removed with a set before summing support.

- [x] **Step 3: Implement exact commutator precursor**

For each remote face, separate loop edges by inherited edge kind `h` or `v`. Sum

```python
(y[h] * y[v]) ** 2
```

over all horizontal/vertical pairs. The commuting-axis control is represented by a separate exact `0`, because its Lie bracket vanishes identically.

- [x] **Step 4: Test orientation, reversal, additivity, and scale**

For all four source slots, require the same projective verdict. For rational amplitudes
`2/3` and `-5/7`, require response linearity. For `lambda=1` and `lambda=7/3`, require exact closure of

```python
j_lambda = -delta + lambda * y
```

and unchanged zero/nonzero support and commutator verdicts. Require the commutator precursor to scale as `lambda**4` because it is a sum of squared quadratic products.

- [x] **Step 5: Add hostile-control assertions**

Require:

```python
zero_source_response == 0
coarse_only_erasure_response == 0
bare_local_cancellation_closure == 0
bare_local_cancellation_remote_support == 0
commuting_axis_precursor == 0
accepted_candidate_spectrum_queries == 0
accepted_candidate_specific_thresholds == 0
```

- [x] **Step 6: Implement mechanical candidate verdicts**

Use only:

```python
if not structural_checks:
    verdict = "STRUCTURALLY_REJECTED"
elif remote_support == 0 or remote_commutator == 0:
    verdict = "STRUCTURAL_ONLY_LOCAL"
else:
    verdict = "PRETIME_GLOBAL_ORGANIZATION_SURVIVES"
```

Apply the all-sizes/all-orientations conjunction after individual size audits. Do not special-case a candidate.

- [x] **Step 7: Run the common canary tests**

Expected: every exact identity passes. The scientific candidate verdicts are data, not prewritten expectations; tests require only that they follow the frozen decision rule.

- [x] **Step 8: Commit**

Commit message:

```text
feat: run exact common source-axiom canary
```

### Task 5: Freeze the adjudication ledger and scientific report

**Files:**
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/source_axiom_canary.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/docs/RESULTS.json`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/README.md`
- Modify: `ResearchHistory/UQCF-GEM/demos/v15.39-higher-incidence-source-axioms/test_gate.py`

**Interfaces:**
- Consumes: all four exact size audits.
- Produces: `audit() -> dict`, `canonical_json(dict) -> str`, authoritative ledger and human-readable interpretation.

- [x] **Step 1: Implement overall adjudication**

Use:

```python
if common_source_protocol_invalid:
    status = "SOURCE_AXIOM_PROTOCOL_INVALID"
elif admissible_candidate_count == 0:
    status = "NO_ADMISSIBLE_RESPONSE_CANDIDATE"
elif global_survivor_count == 0:
    status = "ADMISSIBLE_CANDIDATES_NO_GLOBAL_SIGNAL"
else:
    status = "AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL"
```

Set `pretime_global_organization_signal = (global_survivor_count > 0)`. Keep
`gravity_canary_certified=false`, `physical_gravity_derived=false`, and
`scientific_breakthrough=false`; interpretation may separately identify an important negative or conditional result.

- [x] **Step 2: Add mandatory ledger fields**

Include exact source/candidate manifests, size/orientation metrics serialized as integers or `"numerator/denominator"`, evidence pins, RED receipt, construction-query counts, closed-face concession fields, projective-scale fields, candidate verdicts, hostile controls, and the complete claim firewall.

Set the next object mechanically:

- positive signal: `INDEPENDENT_GEOMETRY_AND_CORRESPONDENCE_TESTS_FOR_FROZEN_AXIOM_SURVIVOR`;
- no global signal: `REVISE_OR_REJECT_EXPLICIT_SOURCE_RESPONSE_AXIOMS_WITHOUT_TUNING`;
- protocol invalid: `REPAIR_TYPED_SOURCE_PROTOCOL_BEFORE_ANY_CANARY`.

- [x] **Step 3: Generate and lock the ledger**

Run:

```bash
python source_axiom_canary.py --out docs/RESULTS.json
python source_axiom_canary.py --check docs/RESULTS.json
```

Then rerun the command and require byte-identical output.

- [x] **Step 4: Write the README**

Report four separate layers:

1. theorem/exact algebra;
2. reproducible computation;
3. interpretation conditional on the new axioms;
4. unresolved physical claims.

State prominently that the closed-face `q)-null was promoted to a nonnull higher-incidence source only by the approved new axiom.

- [x] **Step 5: Complete the tests**

Require exactly eight v15.39 tests. The committed-ledger test is:

```python
committed = Path("docs/RESULTS.json").read_text()
self.assertEqual(committed, canonical_json(self.result))
self.assertEqual(json.loads(committed), self.result)
```

The firewall test must assert every prohibited physical claim remains false and
`Pillar_3 == "OPEN"`.

- [x] **Step 6: Commit**

Commit message:

```text
docs: freeze v15.39 source-axiom result
```

### Task 6: Exact-head certification and PR receipt

**Files:**
- Modify only if necessary: `.github/workflows/uqcf-v1539-higher-incidence-source-axioms.yml`
- Update PR #50 description/comment; do not merge.

**Interfaces:**
- Consumes: complete exact-head branch.
- Produces: successful Actions run and immutable certification receipt.

- [x] **Step 1: Run full local-equivalent commands in Actions**

The final workflow must run:

```bash
python -m unittest -v test_gate.py
python source_axiom_canary.py --check docs/RESULTS.json
python -m compileall -q source_axiom_canary.py test_gate.py
```

and inherited v15.37/v15.38 suites for a total of `7 + 7 + 8 = 22` selected tests.

- [x] **Step 2: Verify additive scope**

Require the exact v15.38 head to be an ancestor and every changed file to be newly added in the preregistered allowlist.

- [x] **Step 3: Inspect the final run**

Fetch job steps/logs. Confirm the exact head SHA, test counts, replay, compilation, ledger status, holdout presence, and claim-firewall assertions.

- [x] **Step 4: Update draft PR #50**

Replace the design-only “implementation not started” note with:

- exact head SHA;
- RED run/job receipt;
- GREEN run/job receipt;
- test counts;
- exact adjudication;
- candidate verdict table;
- claim boundary;
- next required object.

Leave the PR draft/open/unmerged.

- [x] **Step 5: Final verification commit only if required**

If a workflow/checker defect is found, fix only that defect, rerun the complete exact-head suite, and use:

```text
ci: certify v15.39 source-axiom canary
```

No candidate formula or canary criterion may change after the preregistration commit.


## Execution ledger

- Plan identity: `docs/superpowers/plans/2026-09-19-v1539-higher-incidence-source-axioms-implementation.md`
- Execution base: `e4cf11c03d4a510ea1f709755843d903ec4040ef`
- Ruling: The connector-only workspace contains no local git checkout, so the packaged SDD workspace/brief scripts cannot run. Use this plan section as the progress ledger, GitHub branch commits as task boundaries, and GitHub Actions as the executable test runner. Cost if wrong: recovery relies on Git history and PR receipts rather than a local ignored workspace.
- Pre-flight Task 1 -> Tasks 2-5: the RED test schema and workflow consume the exact public ledger keys later tasks produce; names match.
- Pre-flight Task 2 -> Task 3: `LiftedSource.kappa` is the boundary-sector input consumed by every candidate; types match.
- Pre-flight Task 3 -> Task 4: `CandidateResponse.response` is the exact edge vector consumed by the canary observables; types match.
- Pre-flight Task 4 -> Task 5: `exact_size_audit(L)` produces the per-size rows consumed by overall adjudication; types match.
- Pre-flight Task 5 -> Task 6: canonical ledger, README, test count, and workflow assertions match the certification task.
- Pre-flight result: no interface conflicts found.

- Task 1 RED receipt: run `35452558930`, job `105922134054`, exact head `f5548eb73991705d36349ebe1afa550c4eb207d1`; additive scope and 14 inherited tests passed; v15.39 failed with the intended `ModuleNotFoundError: No module named 'source_axiom_canary'`.
- Task 1: complete (commits `39e174a..f5548eb`; RED contract and workflow frozen before production code).
- Ruling: The final test fixture computes one cached full audit, so Tasks 2–4 will expose progressively larger audit schemas: source tests first, then candidate tests, then canary tests. The full workflow may remain red between these task commits. Cost if wrong: per-task evidence comes from named test outcomes in Actions rather than an all-green suite until Task 5.

- Task 2 evidence: run `35452749802`, job `105922643474`, exact head `777198e991fbfb8a730f1482e1df3408b7d2518f`; 14 inherited tests passed; `test_source_lift_typing_covariance_and_composition` and `test_closed_face_q_null_is_fiber_nonnull` passed; the six not-yet-implemented candidate/canary/ledger tests failed on their missing fields.
- Task 2: complete (commit `777198e`; source tests 2/2 pass on all four sizes).

- Task 3 evidence: run `35452940966`, job `105923147292`, exact head `630813fce408a7d48724adb532e329ee5ddf37e0`; 14 inherited tests passed; the source tests and `test_candidate_formulas_and_balance_uniqueness` passed; five not-yet-implemented canary/ledger tests remained red. Exact four-size candidate audit completed in 22.560 s.
- Task 3: complete (commit `630813f`; candidate tests 1/1 plus source regressions 2/2 pass).

- Task 4 evidence: run `35453225390`, job `105923895337`, exact head `1db00b56df6cd8dbb6f46326615bca5be18d4e68`; 14 inherited tests passed; the first six v15.39 tests passed; only the deliberately absent claim-firewall fields and committed ledger remained red. Exact common canary completed in 27.024 s.
- Task 4: complete (commit `1db00b5`; source, candidate, remote, holdout, scale, and hostile-control tests 6/6 pass).


- Task 5 evidence: result artifact from run `35453488826` was committed byte-for-byte, then strengthened after whole-branch review; final ledger status is `AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL`. Candidate verdicts are direct/local, one-incidence/local, and global-balance/survives. The claim firewall keeps physical gravity, continuum, Einstein dynamics, and breakthrough false; Pillar 3 remains OPEN.
- Task 5: complete (commits `50faa76..1102b1e`; deterministic ledger, README, and complete firewall committed).
- Ruling: The user chose native execution, and the active multi-agent constraint does not authorize a reviewer subagent. Perform a read-only whole-branch self-review against the frozen spec and reviewer checklist instead. Cost if wrong: the review lacks a second independent model context; compensate with behavior-first review tests and exact Actions receipts.
- Whole-branch review finding 1 (Important): the initial implementation did not directly certify fresh `B1 B2=0`, `Z=H direct_sum B`, or `A(B) subset B` at every required size, and scale checks were not members of `structural_checks_pass`. Review RED run `35453901526`, job `105925709686`, head `041913b4bf4d3c32b1ccb373504b72dcd830a3cd` exposed the missing fields. Fixed without changing a candidate formula or canary criterion; run `35454159289`, job `105926388383`, proved the new checks and failed only because the old ledger had not yet been regenerated.
- Whole-branch review finding 2 (Important): `NO_ADMISSIBLE_RESPONSE_CANDIDATE` incorrectly mapped to source-protocol repair rather than axiom revision/rejection. Review RED run `35454415938`, job `105927058494`, head `848e1afe512f07c9943e6e81c02fa43973bbdd49` exposed the absent complete mapping. Fixed in `ef8ae146ee296622417863dd17369e9291412524`.
- Whole-branch review result: no Critical or remaining Important findings. Minor operational note: the deterministic artifact and replay intentionally recompute the exact audit, trading CI time for an independent byte-replay check.
- Declined to judge: merging/integration, because the user requires the PR to remain draft/open/unmerged.
- Declined to judge: continuum, Newton/GR, and independent geometry correspondence, because the ledger names those as the next research object rather than v15.39 claims.
- Declined to judge: protein work, because the user explicitly excluded it.
- Reviewed GREEN receipt before the final ledger-only commit: run `35454591149`, job `105927530602`, exact head `ef8ae146ee296622417863dd17369e9291412524`; additive scope passed; inherited suites passed `7+7`; v15.39 passed exactly `8`; deterministic result replay and compilation passed; status and all candidate verdicts matched the frozen rules.
- Task 6 PR receipt: draft PR #50 updated with the RED/GREEN receipts, exact adjudication, claim boundary, and next required object; PR remains open, draft, and unmerged.
- Task 6 final-write rule: this execution-ledger update is the sole remaining branch-content write. Its exact-head Actions receipt is recorded in PR #50 after the run completes, avoiding an infinite sequence of receipt-only commits.
