# v15.71 Minimal extension memory and rebased null integrability — COMPLETE

Date: 2026-09-26. Branch: `research/v15.71-minimal-extension-memory`.

## Scientific verdicts

**MINIMAL_EXTENSION_MEMORY_DESCENT_NOT_CONFIRMED** — the frozen full-state float64 descent comparison narrowly missed its preregistered relative-error gate.

**REBASED_NULL_INTEGRABILITY_CONFIRMED** — independently recomputing the symmetric-null lift after finite base-point shifts preserved the lift, hidden memory, edge polar rotations, null sector, and sequential composition throughout the frozen regular neighborhood.

These conclusions are separate. The primary NO is preserved exactly as preregistered.

## Memory structure

The exact-weight-three Pauli fiber has dimension 27. Its HS Gram matrix had:

- rank: **27**
- maximum deviation from identity: **2.220446049250313e-16**
- all singular values: **0.9999999999999998**

The derivation proves that 27 real coordinates are minimal among **linear memories that must support the full 27-dimensional source-label family**. For one already-fixed source label, only its single pairing scalar is required.

The frozen 26-coordinate compression control behaved as required:

- compressed-memory gap: **0**
- retained-output gap for the omitted source coordinate: **9.999999998992918e-8**

So ordinary two-body marginal data plus a 26-dimensional truncation still cannot represent the complete source family.

## Enriched descent measurement

All 12 asymmetric states, 27 hidden input directions, 27 source labels, both hidden signs, and all three edges were evaluated:

**52,488 enriched descent witnesses.**

The independently reconstructed local retained lift agreed with the restricted global lift to:

- maximum relative residual: **7.571427111245362e-16**

Hidden-memory coordinate recovery agreed to:

- maximum absolute error: **1.214306433183765e-17**

The regional/global output comparison had:

- maximum absolute residual: **8.780832845415946e-17**
- maximum relative residual: **1.7561665690834018e-9**
- frozen relative threshold: **1e-9**

Therefore the formal primary verdict is NOT CONFIRMED.

The failure shape is diagnostic: the absolute mismatch is at the float64 state-addition/subtraction floor, while the physical update being normalized against is only about 5e-8 in norm. v15.71 does not retune or waive the preregistered relative criterion.

All finite states remained valid; the minimum eigenvalue was **0.03831618449748307**.

## Rebasing / integrability

For every state the lift was independently recomputed after strengths

`[-1e-2,-3e-3,-1e-3,1e-3,3e-3,1e-2]`.

Worst cases across all states:

- recomputed lift relative change: **1.9303370132210866e-15**
- hidden-memory drift: **9.812029660993815e-18**
- edge polar-rotation change: **5.628661131238174e-15**
- local lift relative residual: **1.0596079507672389e-15**
- polar-skew null relative residual: **3.5385471366852256e-16**
- connected-correlation path residual: **1.1236938283130691e-16**
- sequential order residual: **3.930976791863501e-17**
- sequential-versus-combined residual: **5.464678175690276e-17**
- edge sequential order residual: **5.557548845194775e-17**
- edge sequential-versus-combined residual: **1.2645646313846623e-16**
- minimum density eigenvalue: **0.035505113044579165**
- minimum positive-polar eigenvalue: **0.01508754084987075**

Thus the base-point-local null assignment extends consistently over this frozen regular neighborhood: the recomputed Y is effectively constant, source memory is conserved, and rebased ordered repairs commute and add.

## Scientific consequence

v15.70 showed that marginal state data alone are insufficient.

v15.71 establishes two sharper facts:

1. the missing linear information is exactly the 27-dimensional hidden Pauli fiber for the complete historical source-label family, with an explicit compression obstruction below dimension 27;
2. carrying that source/extension memory does not by itself destroy the symmetric-null sector under finite rebasing.

The full-state float64 descent certification remains formally unresolved because of the frozen relative numerical criterion. A separate numerical-method adjudication is required; this result is not changed post hoc.

## Reproducibility

- parent: `0d90d48da6c121ae2e808930a9c5d10198abe437`
- preregistration: `3a3479db2ba96ba7628458d485dcfa1ef3ae267b`
- derivation: `17018f1f3e3da2d854bc79be48142d3eae0179d8`
- RED head: `db41113efebe17e8703c255efe6774a5f2359395`
- RED run: `36292971472`, job `108546449393`
- tested implementation: `14dc33e9932c67dd5457b1652c24521a4bea921a`
- GREEN run: `36293091565`, job `108546782061`
- artifact: `10922538891`
- artifact SHA-256: `eafdd3ddf74d2fd2f3736225d8a2e31747b7ff138abd1549c99cdf4a9f27fff3`

## Next

Do not relax the v15.71 relative threshold.

The immediate numerical adjudication should compare **source increments before they are added to the O(1) marginal state**, where the exact identity is

    R_e Δ_global = strength (s·m) R_e Y

versus the independently reconstructed regional increment

    Δ_regional = strength (s·m) Y_e.

If increment-space residuals satisfy the frozen v15.71 relative scale while full-state subtraction does not, the failure is cancellation from adding/subtracting the small update to the state. That must be a new preregistered gate.
