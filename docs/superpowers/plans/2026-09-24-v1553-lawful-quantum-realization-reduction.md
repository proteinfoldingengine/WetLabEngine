# v15.53 Lawful Quantum Realization / Reduction Certification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and independently verify a finite lawful realization family whose retained reduction can be exhaustively tested for same-readout/distinct-target obstruction witnesses.

**Architecture:** v15.53 is split into a frozen contract, raw candidate family, producer-side admissibility/reduction/equivalence/search, and a fully independent verifier that recomputes every semantic premise without calling producer validity functions. The scientific outcome is one of four frozen verdicts; either a certified pair or a no-witness result in the frozen family is acceptable.

**Tech Stack:** Python 3.13.5 standard library only; exact finite integers/tuples/dicts; unittest; GitHub Actions on ubuntu-24.04.

**Spec:** `docs/superpowers/specs/2026-09-24-v1553-lawful-quantum-realization-reduction.md`

## Global Constraints

- No floating-point tolerance enters admissibility, reduction, equivalence, or verdict calculation.
- No predecessor scientific file may be modified to make v15.53 pass.
- Producer status fields never establish admissibility or inequivalence.
- The retained reduction must be recomputed from each realization and must not read candidate IDs, target classes, enumeration indices, or post-result information.
- The target equivalence relation is frozen before candidate enumeration.
- Independent verification must not call producer admissibility, reduction, equivalence, class-construction, or witness-selection functions.
- Positive certification is limited to the frozen v15.53 family.
- `source_correspondence=NOT_EVALUATED`; `Pillar_3=OPEN`; no physical source law, geometry/curvature, continuum, empirical, fundamental-time, or dark-matter claim.
- Inherited v15.46-v15.52 discovered suites remain regression gates.

## Review Focus

- Structurally duplicate candidates under different IDs must collapse to one target class and never fabricate a witness.
- An allowed isomorphism family that is incomplete or contains a non-isomorphism must be rejected rather than silently changing class counts.
- A realization whose local tables are well typed but whose composition is nonassociative must be inadmissible.
- JSON/list-vs-tuple round trips must not change admissibility, reduction, equivalence, or verdict.
- Relabeling retained objects within the registered source schema must leave the scientific verdict invariant.

---

### Task 1: Freeze the v15.53 contract and RED skeleton

**Files:**
- Create: `ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction/realization_contract.py`
- Create: `ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction/test_realization_contract.py`
- Create: `.github/workflows/uqcf-v1553-realization-reduction.yml`

**Interfaces:**
- Consumes: exact predecessor blob pins from v15.46 Stage C, v15.51 RESULTS, v15.52 VERIFICATION and v15.52 frozen spec.
- Produces: `load_contract(root: Path) -> dict`, frozen verdict list, forbidden field/input lists, retained-observable schema.

- [ ] **Step 1: Write failing contract tests**

Tests assert:
- schema is `uqcf-v1553-realization-contract-v1`;
- predecessor paths and Git blob SHAs are exact;
- primary verdicts are exactly `CERTIFIED_FAMILY_OBSTRUCTION_WITNESS`, `NO_WITNESS_IN_FROZEN_FAMILY`, `FAMILY_INVALID`, `VERIFICATION_FAILED`;
- retained observables equal the seven v15.52 readouts;
- forbidden selector/target-derived fields are explicit;
- claim firewall is frozen.

- [ ] **Step 2: Run contract tests and verify RED**

Run:
`cd ResearchHistory/UQCF-GEM/demos/v15.53-lawful-quantum-realization-reduction && python -m unittest -v test_realization_contract`

Expected: import/module failure because `realization_contract.py` is absent.

- [ ] **Step 3: Implement minimal frozen contract**

Implement only literal contract data plus predecessor-byte verification.

- [ ] **Step 4: Run contract tests and verify GREEN**

Expected: all Task-1 tests pass with zero skips/expected failures.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): freeze v15.53 realization reduction contract`

### Task 2: Define exact raw realization family and admissibility

**Files:**
- Create: `.../realization_family.py`
- Create: `.../test_realization_family.py`

**Interfaces:**
- Consumes: `load_contract(root)`.
- Produces:
  - `enumerate_raw_realizations(contract: dict) -> tuple[dict, ...]`
  - `check_admissibility(contract: dict, realization: dict) -> dict`

Each raw realization contains exact:
- carrier sites with dimensions/types;
- operation symbols and exact operation table;
- identity element;
- recovery-capable operation subset;
- typed incidence/refinement assignments;
- no target class, retained readout, node-site selector, or post-result gauge.

- [ ] **Step 1: Write failing family/admissibility tests**

Tests pin:
- deterministic nonempty finite enumeration;
- no duplicate canonical realization records;
- IDs are metadata only and can be changed without changing admissibility;
- valid baseline candidates pass;
- one changed composition entry fails closure or associativity;
- broken identity fails;
- recovery operation outside operation domain fails;
- malformed typed incidence fails;
- forbidden `target_class`, retained readout, or selector field fails;
- JSON round-trip preserves admissibility.

- [ ] **Step 2: Run and verify RED**

Expected: missing module/functions.

- [ ] **Step 3: Implement minimal exact family and exhaustive admissibility checks**

Associativity must check every triple in the finite operation domain.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Task-2 tests pass.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): add exact v15.53 realization family`

### Task 3: Implement target-blind retained reduction

**Files:**
- Create: `.../reduction.py`
- Create: `.../test_reduction.py`

**Interfaces:**
- Consumes: admissible raw realization dict.
- Produces: `reduce_to_retained(contract: dict, realization: dict) -> dict` with exactly seven readouts.

- [ ] **Step 1: Write failing reduction tests**

Tests assert:
- output key set exactly matches frozen seven readouts;
- two calls are byte/canonical equal;
- changing candidate ID leaves reduction unchanged;
- injecting target-class metadata is rejected upstream and cannot affect reduction;
- mutating one realization-side relation changes the corresponding recomputed readout;
- a copied external `E_observables` field is ignored/rejected, never trusted;
- every produced readout passes the retained schema;
- retained relabeling produces canonically relabeled output, not a hidden selector effect.

- [ ] **Step 2: Run and verify RED**

Expected: missing `reduction.py`.

- [ ] **Step 3: Implement minimal target-blind reduction**

Derive every retained field from realization structure only.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Task-3 tests pass.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): derive retained readout from realizations`

### Task 4: Freeze and compute structural equivalence classes

**Files:**
- Create: `.../equivalence.py`
- Create: `.../test_equivalence.py`

**Interfaces:**
- Consumes: two admissible realizations.
- Produces:
  - `enumerate_isomorphisms(contract: dict, left: dict, right: dict) -> tuple[tuple[int, ...], ...]`
  - `are_equivalent(contract: dict, left: dict, right: dict) -> bool`
  - `canonical_class_key(contract: dict, realization: dict) -> tuple`

- [ ] **Step 1: Write failing equivalence tests**

Tests assert:
- self-equivalence;
- symmetry and transitivity on the frozen family;
- label/ID swaps do not alter equivalence;
- structurally isomorphic relabelings are equivalent;
- one operation-table invariant change makes candidates inequivalent;
- omitted valid isomorphism is detected by an independent brute-force test helper;
- invented non-preserving bijection is rejected;
- JSON round-trip preserves class key;
- enumeration order does not alter class partition.

- [ ] **Step 2: Run and verify RED**

Expected: missing module/functions.

- [ ] **Step 3: Implement complete finite bijection enumeration**

Preserve carrier dimensions/types, operation table, recovery subset, and typed incidence/refinement assignments.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Task-4 tests pass.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): classify v15.53 realizations by exact isomorphism`

### Task 5: Producer-side witness search and frozen-family verdict

**Files:**
- Create: `.../witness_search.py`
- Create: `.../test_witness_search.py`

**Interfaces:**
- Consumes: contract, raw family, admissibility, reduction, equivalence.
- Produces: `search_frozen_family(contract: dict) -> dict`

Result fields include:
- candidate_count;
- admissible_count;
- retained_fiber_count;
- target_class_count;
- witness pair if present;
- primary verdict;
- claim firewall.

- [ ] **Step 1: Write failing search tests**

Tests assert:
- deterministic result;
- enumeration-order invariance;
- duplicate candidate injection rejected or canonicalized without changing verdict;
- candidate ID relabeling leaves verdict invariant;
- result is exactly one allowed primary verdict;
- positive witness, if present, contains admissible candidates with equal recomputed readout and distinct structural class keys;
- no-witness verdict contains no fabricated pair;
- producer never emits universal/no-go language beyond the frozen family.

- [ ] **Step 2: Run and verify RED**

Expected: missing `witness_search.py`.

- [ ] **Step 3: Implement exhaustive finite partition/search**

No early stopping before full family/class accounting.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Task-5 tests pass; record the actual producer verdict but do not yet call it certified.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): exhaust v15.53 frozen realization family`

### Task 6: Independent verifier and semantic certification gate

**Files:**
- Create: `.../verify_realization_obstruction.py`
- Create: `.../test_verify_realization_obstruction.py`

**Interfaces:**
- Consumes: frozen contract and raw realization data only.
- Produces:
  - independent admissibility recomputation;
  - independent retained reduction;
  - independent isomorphism/class partition;
  - independent exhaustive witness search;
  - canonical verification report.

The verifier must not import producer functions from `realization_family.py` except raw literal candidate data if needed, and must not call producer functions from `reduction.py`, `equivalence.py`, or `witness_search.py`.

- [ ] **Step 1: Write failing independent-verifier tests**

Tests assert:
- producer/verifier verdict agreement on untampered frozen family;
- monkeypatching producer admissibility/reduction/equivalence/search cannot change verifier result;
- changed composition entry -> FAMILY_INVALID or candidate rejection;
- associativity break detected;
- recovery typing break detected;
- injected target class rejected;
- copied readout corruption detected by recomputation;
- omitted allowed isomorphism packet detected;
- invented isomorphism rejected;
- malformed/duplicate candidate rejected;
- retained relabelings preserve scientific verdict;
- JSON round-trip preserves verdict;
- double replay is byte-identical;
- all claim-firewall fields remain unchanged.

- [ ] **Step 2: Run and verify RED**

Expected: missing verifier.

- [ ] **Step 3: Implement independent logic from frozen definitions**

Duplicate necessary finite logic rather than delegating semantic checks to producer modules.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Task-6 tests pass.

- [ ] **Step 5: Commit**

Commit message:
`feat(uqcf): independently verify v15.53 realization obstruction`

### Task 7: Authoritative CI, inherited regressions, and result publication

**Files:**
- Modify: `.github/workflows/uqcf-v1553-realization-reduction.yml`
- Create after exact-head GREEN only: `.../docs/RESULTS.json`
- Create after exact-head GREEN only: `.../docs/CI_RECEIPT.md`
- Create after exact-head GREEN only: `.../README.md`

**Interfaces:**
- Consumes: complete v15.53 implementation and inherited v15.46-v15.52 test directories.
- Produces: exact-head execution evidence and scoped scientific adjudication.

- [ ] **Step 1: Extend workflow assertions**

Workflow must:
- exact-checkout current SHA;
- run all v15.53 discovered tests with a minimum count;
- run discovered suites v15.46 through v15.52 separately and require >0 tests each;
- run independent verifier twice and compare byte-for-byte;
- compile v15.53;
- verify no predecessor scientific file changed from the pinned pre-v15.53 head;
- print canonical verification JSON.

- [ ] **Step 2: Push executable head and inspect authoritative run**

Expected: workflow SUCCESS or a concrete failing gate to debug. Do not write RESULT/receipt before success.

- [ ] **Step 3: If CI fails, use systematic debugging and TDD**

Every behavioral fix gets a reproducing RED test before code change.

- [ ] **Step 4: Freeze authoritative scientific verdict**

Write `docs/RESULTS.json` from the independent verifier output exactly.

Allowed interpretation:
- if positive: obstruction certified only for the frozen family;
- if no witness: no witness found in the frozen family only;
- if invalid/failure: no scientific promotion.

- [ ] **Step 5: Write CI receipt and README**

Record exact executed SHA, run/job IDs, suite counts, canonical result hash, and claim boundary.

- [ ] **Step 6: Run documentation-head workflow again**

Require exact-head SUCCESS with stored `RESULTS.json` byte-identical to replay.

- [ ] **Step 7: Update PR #57**

Add concise status, exact verdict, links, run IDs, and next scientific dependency. Keep PR draft unless separately approved for merge.

- [ ] **Step 8: Commit documentation**

Commit message:
`docs(uqcf): record v15.53 lawful realization verdict`

## Plan Self-Review

- Spec coverage: all realization, admissibility, reduction, equivalence, witness, independence, TDD, CI, and claim-firewall requirements are assigned to tasks.
- Placeholder scan: no placeholder markers or implicit implementation steps remain.
- Type consistency: producer and verifier interfaces use contract + exact realization dicts; no target labels enter reduction.
- Review Focus items are each covered by Tasks 2, 4, or 6.
- Scientific asymmetry avoided: both certified-witness and no-witness outcomes are valid endpoints.
