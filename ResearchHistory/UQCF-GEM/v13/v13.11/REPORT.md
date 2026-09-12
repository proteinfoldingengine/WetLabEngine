# UQCF-GEM v13.11 — Metric-Affine Source Response / Nonmetricity-Torsion Dynamics Gate

**Date:** 2026-09-12

## Adjudication

The generic metric-affine parent now has a derived **first-order atemporal source-response operator**, but it still does not close into an autonomous geometric field theory.

The strongest new exact result is a trace-exactness theorem for BKM/polar nonmetricity.

## 1. Quantum-to-metric-affine source response

For the ETL/PGRL source family

`rho_s = exp(log rho + s P)/Z_s`,

the tangent `dot rho` is linear in the centered source generator P.

On a faithful state and a nonsingular polar-correlation stratum, the downstream maps are differentiable:

`rho -> K_i`,
`rho -> C_ij -> O_ij=polar(C_ij)`.

Therefore source response canonically induces:

- `dot K_i`;
- `dot O_ij`;
- a discrete nonmetricity-defect jet;
- a retained holonomy jet.

Define

`M_ij = K_j - O_ij^T K_i O_ij`

and

`Omega_ij = O_ij^T dot O_ij`.

Then the exact differential is

`dot M_ij = dot K_j - O_ij^T dot K_i O_ij + [Omega_ij, O_ij^T K_i O_ij]`.

This formula is valid away from the Q=0 sector as well.

Fresh finite-difference error:

`6.287e-10`.

For a three-edge loop

`H=O_01 O_12 O_20`,

the ordinary product rule gives the retained curvature/holonomy response.

Fresh holonomy derivative error:

`2.452e-11`.

The fixed-RESA solder response formula is also verified to

`2.402e-11`.

I call the resulting conditional first-order map the

**QMAR — Quantum Metric-Affine Response operator**.

It is kinematic, not a field equation.

## 2. Source linearity

Because the ETL/PGRL tangent is linear in the centered source and all downstream operations are differentiated at one fixed state, QMAR is linear in P.

A random nine-source combination was compared with the corresponding linear combination of the nine separately evaluated source-response columns.

Absolute error:

`2.136e-09`.

Relative error:

`7.051e-09`.

So source superposition holds at first response order.

## 3. Local-frame covariance

The full response stack was conjugated by three independent local SU(2)/SO(3) frame changes.

Maximum covariance error over:

- K;
- O;
- dot K;
- dot O;
- dot M;
- dot H;
- fixed-solder dot C

was

`5.847e-09`.

Thus QMAR is gauge covariant to numerical precision.

## 4. Exact BKM Trace-Exactness Theorem

Define the positive metric mismatch operator

`G_ij = K_j^-1/2 O_ij^T K_i O_ij K_j^-1/2`.

Since O is orthogonal,

`det G_ij = det K_i / det K_j`.

Therefore, exactly,

`tr log G_ij = log det K_i - log det K_j`.

This is a node-potential difference.

Consequently, for every closed relational cycle C,

`sum_C tr log G_ij = 0`.

No dynamics, fitting, or Q=0 assumption is needed.

Fresh controls:

- edge potential identity error: `2.526e-15`;
- baseline closed-cycle error: `2.866e-15`;
- maximum finite-source closed-cycle error: `7.211e-15`;
- maximum source-response cycle error: `1.514e-10`.

The raw linear metric defect has the corresponding identity

`sum_C tr M_ij = 0`

because orthogonal transport preserves trace.

### Continuum implication

If the logarithmic BKM nonmetricity admits the smooth continuum limit already made conditional by SMRRL/SMAVT, then its trace/Weyl one-form is locally exact, up to orientation/sign convention:

`w = d log det K`.

Therefore its closed-loop circulation vanishes.

The generic BKM/polar metric-affine parent is not an arbitrary Weyl geometry.

Its scalar/Weyl nonmetricity sector is integrable.

Any nontrivial nonmetricity circulation must live in the traceless/shear sector.

This is an exact structural theorem of the present construction.

## 5. Torsion-like response is still not determined

For the same PGRL state tangent and the same induced `dot K` and `dot O`, hold the RESA solder fixed.

The torsion-like closure response norm is

`0.0348537740497`.

Now change only the solder/coframe tangent by taking

`dot xi_0 = - dot C_fixed`

with the other local solder tangents zero.

The closure response becomes

`0.000e+00`.

So PGRL does not determine a torsion evolution law.

A source-to-solder/coframe lift remains genuinely missing.

## 6. Geometry is not an autonomous state variable

The v13.10 rigid and hidden completions begin with the same current:

- local BKM metrics;
- polar edge transports;
- loop holonomy;
- metric-compatibility defects.

Current geometric-state mismatch:

`0.000e+00`.

Apply the same source.

Their response jets differ by:

- edge-transport jet: `0.0907979585539`;
- holonomy jet: `0.272393875656`;
- fixed-solder closure jet: `0.13359956207`.

Therefore no autonomous first-order law of the form

`dot G_geometry = F(G_geometry, P)`

can exist on the current visible geometric variables alone.

The full quantum/hidden completion state is carrying response information not contained in the instantaneous geometry.

This is a source-response memory/non-autonomy theorem, not physical time evolution.

## 7. Conservation-law audit

The response vector used:

- 18 symmetric components of the three edge `dot M_ij`;
- 3 fixed-solder closure-response components;
- 3 body-frame holonomy-response components.

Across 20 generic faithful states and nine local Pauli sources each, the resulting 24 x 180 response matrix had

`rank = 23`.

There is one constant-coefficient linear null.

Its alignment with the predicted cycle-trace identity is

`1`.

Theoretical null residual:

`6.179e-16`.

The smallest nonzero singular value is

`0.138211682624`,

while the exact-null singular value is

`5.832e-16`.

Thus within this tested response class the only universal constant-linear conservation relation found is the exact trace/nonmetricity cycle identity.

This does **not** exclude nonlinear, state-dependent, higher-order, or continuum conservation laws.

## 8. What is and is not closed

### Derived

- first-order source-to-BKM metric response;
- first-order source-to-polar connection response;
- first-order nonmetricity-defect response;
- first-order holonomy/curvature response;
- source linearity;
- local-frame covariance;
- exact BKM trace/Weyl circulation closure.

### Not derived

- source-to-solder/coframe response;
- continuum torsion dynamics;
- autonomous dynamics on geometric variables alone;
- metric-affine action;
- stress-energy constitutive law;
- Einstein equations.

## Status

- QMAR: **DERIVED FIRST-ORDER / CONDITIONAL ON FULL STATE**
- BKM trace-exactness: **CLOSED EXACT THEOREM**
- trace/Weyl closed-cycle circulation: **ZERO EXACTLY**
- torsion source lift: **MISSING**
- autonomous geometry-only source dynamics: **OBSTRUCTED**
- generic metric-affine parent: **STRENGTHENED, NOT DYNAMICALLY CLOSED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major structural theorem**: in the BKM/polar parent geometry, scalar nonmetricity is integrable, while the genuinely nontrivial metric-affine content is pushed into shear nonmetricity, torsion/coframe response, and hidden-completion-dependent connection response.

## Next — v13.12

### Shear Nonmetricity / Curvature Response Coupling Gate

Remove the exact trace/Weyl sector and isolate the traceless nonmetricity response.

Test whether source-induced shear nonmetricity determines or constrains the holonomy/curvature response across generic faithful states and the hidden-completion controls.

The goal is a covariant derived coupling.

Do not introduce an action or fit a field equation unless the retained response structure itself forces one.
