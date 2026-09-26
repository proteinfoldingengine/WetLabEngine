# v15.69 Local-frame covariance — COMPLETE

Date: 2026-09-26.

## Verdict

\`LOCAL_FRAME_COVARIANT_NULL_CONFIRMED\`.

The v15.64/v15.68 symmetric-null construction survives deterministic local quantum-frame changes when the hidden tangent is transformed as source data.

## Frozen ensemble

- 12 asymmetric full-rank states;
- 8 deterministic independent local SU(2)^3 frames generated from seed 20260969;
- 96 total state/frame cases;
- eta=1e-4;
- t=1e-3;
- minimum-Hilbert-Schmidt-norm global lift recomputed independently after each frame transformation.

## Worst-case residuals across all 96 cases

- lift covariance relative residual: **3.5967448515958586e-15**
- edge polar covariance residual: **1.081645144627655e-14**
- transformed retained-target relative residual: **6.282592716804444e-15**
- finite source-vector-field covariance residual: **1.699839867958255e-16**
- analytic polar-skew null relative residual: **5.262601018375311e-16**
- trace error: **6.667345956270563e-16**
- minimum finite-state eigenvalue: **0.0383348989239673**

All 96 cases passed the preregistered thresholds.

## Scientific consequence

The symmetric-null existence counterexample is not an artifact of the preferred Pauli frame.

For a local frame U=U0⊗U1⊗U2, with

    rho' = U rho U†
    h'   = U h U†,

the independently recomputed minimum-norm lift obeys, numerically to machine precision,

    Y_{rho'} = U Y_rho U†.

The edge polar factors and retained symmetric targets transform with the induced SO(3) endpoint rotations, and the local affine source vector field satisfies

    T' = U T U†

on the frozen finite probe.

Therefore local-frame covariance does not eliminate the symmetric-null mechanism.

## Boundary

This does not establish a physical source law.

The construction still uses the hidden tangent h as explicit source data and remains base-point-local. v15.69 does not establish:
- a unique source selector from rho alone;
- a source law determined by an ordinary one-body source generator;
- composition/naturality across overlapping retained charts;
- semigroup/flow consistency;
- positivity for arbitrary finite source strength.

The next admissibility obstruction is composition / atlas consistency.

A covariant family of local null maps is not yet a natural source law unless the assignments agree under restriction/overlap and compose consistently.

## Reproducibility

- branch: \`research/v15.69-covariant-symmetric-null\`
- preregistration: \`3148bdcc939de9f491835b348d0f5e8873168aab\`
- RED run: \`36276674560\`
- tested implementation: \`c6cbe4eb80d4e5c93ef5cef5352dd85d99c0f378\`
- GREEN run: \`36276731957\`, job \`108500822797\`
- artifact: \`10916798400\`
- artifact SHA-256: \`019e147f6b21a83001a3251f327a04caaa035802dd409a6ba6b1d72358b1dec6\`
