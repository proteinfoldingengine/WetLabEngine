# Protein P8 — Patch 622/624 source-mechanism certification contract

**Branch:** `research/protein-p8-patch622-624-reopen`  
**Base:** P7 closeout `0e156790b961abdebcd288b333b44c2e6df05d61`

## Purpose

P8 exists only because newly recovered Drive source satisfies the documented P7 reopen rule at the source-evidence level: an exact Patch-622/624-adjacent runner/DAG/config lineage contains mechanism wiring materially different from the StableDAGPhysics source certified by P7.

P8A asks a source-mechanism question only:

> Does the recovered bundle execute a persistent Compaction phase with coordinate-active fractal compaction, and later activate a LockIn force set that is materially richer than contact springs alone?

P8A does **not** test whether the historical folding claims were correct, whether a native structure was reached, or whether the mechanism transfers to held-out proteins.

## Provenance boundary

The recovered folders are mixed historical snapshots, not byte-pure single-patch releases.

- `GlobularFoldQIS` contains a runner labeled 622.2 / runtime Patch_623, DAG 622.1, force field/config 623.0.
- `StableGlobularQISBest` contains a runner with runtime Patch_625, DAG/force 624.1, and Patch-625 config.

Accordingly P8 will call them the **Patch-622/623 recovered bundle** and **Patch-624/625 recovered bundle**. It will not silently relabel either as a pure patch release.

No raw historical execution log has yet been recovered from these folders.

## Authoritative P8A predicates

The CI certification must evaluate the vendored recovered source, not a rewritten model.

1. **Content integrity:** every frozen source/config file used by the audit must match its recorded SHA-256.
2. **Persistent Compaction:** with Betti₁ equal to the configured threshold at every simulated step, step 0 must remain in `Compaction`.
3. **Exact idealized transition trace:** under continuously qualifying Betti history, steps 0–98 must remain `Compaction` and the first `LockIn` transition must occur at step 99, because the configured DAG lifetime threshold is 100 and the history is appended before DAG evaluation.
4. **622/623 force-set difference:** `LockIn - Compaction` must equal `{contact_springs, screened_electrostatics}`.
5. **Fractal gradient:** the recovered fractal compaction energy must have a finite, nonzero coordinate-gradient norm on a fixed nondegenerate synthetic coordinate fixture.
6. **Electrostatic gradient:** the recovered screened-electrostatics energy must have a finite, nonzero coordinate-gradient norm on a fixed charged synthetic fixture.
7. **624/625 extension:** `LockIn - Compaction` must equal `{contact_springs, screened_electrostatics, torsional_incoherence_penalty}`.
8. **Torsional-path classification:** with the recovered runner semantics in which `phi_rms` is converted to a Python scalar before force evaluation, the torsional-incoherence penalty may have a gamma gradient but must not be classified as a direct coordinate-gradient force.

## Decision rule

If predicates 1–8 all pass:

`REOPEN_RULE_SATISFIED_DISTINCT_HISTORICAL_MECHANISM_SOURCE_LEVEL`

This changes the P7 program-wide mechanism classification only as follows:

- P7 remains authoritative for its certified StableDAGPhysics source.
- P7 no longer exhausts the recovered historical DAG lineage.
- A bounded prospective P8B test of the recovered distinct mechanism is authorized.
- No historical folding claim is promoted or restored.

If any predicate fails:

`SOURCE_CERTIFICATION_INCOMPLETE`

No P8B folding measurement is authorized until the source discrepancy is resolved without changing the frozen historical source.

## Outcome-exposure note

A local exploratory dry-run was used to debug the certification harness before this contract was frozen. Therefore P8A is **not** represented as an outcome-blind preregistration. The authoritative evidence is the subsequent repository/CI run against this frozen contract. P8B, if authorized, must be freshly preregistered before structural outcome exposure.
