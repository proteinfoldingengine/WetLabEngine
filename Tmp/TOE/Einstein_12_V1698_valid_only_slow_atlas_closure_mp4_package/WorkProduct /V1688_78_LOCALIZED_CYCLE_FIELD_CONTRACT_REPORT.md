# V1688.78 — Localized Cycle-Field Contract

**Verdict:** `LOCALIZED_CYCLE_FIELD_CONTRACT_READY`

V1688.77 showed that a true retained field-law test needs more than weak-form node fields and edge fields. It requires the **same compatible graph identity** and a way to localize cycle holonomy back to nodes or regions.

This version freezes that missing object.

## Frozen nodewise law

```text
weak_target(p) ≈ M0(p)
              + C_corr(p)
              + H_dir(p)
              + div_R J(p)
```

where:

```text
M0(p) = source_abs(p) + access_abs(p) + div_baseline(p)
H_dir(p) = localized native directional holonomy density
div_R J(p) = retained-order incidence continuity residual
```

## Required new object

```text
cycle_node_map.csv
```

with:

```text
cycle_id
node_id
weight
```

This prevents a global cycle defect from being incorrectly used as a local field.

## Why this matters

A global holonomy defect can prove a cycle mismatch exists, but it cannot test a field equation at each node because it is constant under regression with an intercept.

A local field law requires:

```text
H_dir(p)
```

not merely:

```text
H_dir(global cycle)
```

## Files provided

- JSON contract
- executable validator harness
- report

The next execution is only valid when a compatible node/edge/cycle/cycle-node-map ledger is supplied.
