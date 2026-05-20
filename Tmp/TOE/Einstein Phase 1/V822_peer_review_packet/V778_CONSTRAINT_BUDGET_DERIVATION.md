# V778 First-Principles Constraint-Budget Derivation

## Purpose

V777 froze the correct coefficient status:

```text
operator form derived
coefficients = recoverable Lagrange multipliers
coefficient-free theorem not supported yet
```

V778 asks the next first-principles question:

```text
What measurable constraint budget sets each multiplier?
```

## Guardrail

```text
Ordered recoverability updates, not physical time.
```

## Core principle

If coefficients are Lagrange multipliers, they are not arbitrary constants.

They are shadow prices of constraints.

So each coefficient should correspond to a measurable budget.

## Budget 1 — defect pressure budget

Multiplier:

```text
a
```

Source term:

```text
log_mu
```

Constraint budget:

```text
B_defect = ∫ φ log(1+μ) dA
```

Interpretation:

```text
a is the shadow price of unresolved defect burden.
```

## Budget 2 — repair-geometry coupling budget

Multiplier:

```text
b
```

Source term:

```text
repair_phi
```

Constraint budget:

```text
B_repair_geom = ∫ repair φ² dA
```

Interpretation:

```text
b is the shadow price of coupling retained repair pressure to Ω geometry.
```

## Budget 3 — surplus-gradient exchange budget

Multiplier:

```text
c
```

Source term:

```text
lap_C
```

Constraint budget:

```text
B_surplus_grad = ∫ ∇C · ∇φ dA
```

Variation:

```text
δ/δφ ∫ ∇C · ∇φ dA = -ΔC
```

Interpretation:

```text
c is the shadow price of surplus spatial alignment with geometry.
```

## Budget 4 — repair-gradient exchange budget

Multiplier:

```text
d
```

Source term:

```text
lap_repair
```

Constraint budget:

```text
B_repair_grad = ∫ ∇repair · ∇φ dA
```

Variation:

```text
δ/δφ ∫ ∇repair · ∇φ dA = -Δrepair
```

Interpretation:

```text
d is the shadow price of repair spatial alignment with geometry.
```

## Budget 5 — conformal consistency budget

R-side identity:

```text
R_conf = exp(-2φ)G_proxy
```

Constraint:

```text
B_conf(ψ) = ∫ ψ [R_conf - exp(-2φ)G_proxy] dA
```

Source terms:

```text
exp_phi_lap_C
exp_phi_lap_repair
grad_phi_energy
phi_lap_C
C_grad_phi
```

Interpretation:

```text
R-side multipliers enforce conformal curvature consistency.
```

## Budget 6 — boundary residue

Boundary budget:

```text
B_boundary = ∮ weak-form boundary residue
```

Source term:

```text
boundary_proxy
```

Interpretation:

```text
boundary coefficient is a finite-domain correction,
not necessarily a fundamental law term.
```

## First-principles status

```text
The coefficients now have measurable budget identities.
```

Still open:

```text
Do the measured budgets predict the recovered multipliers?
```

That is the next real test.

## Correct next step

```text
V779 — budget/multiplier prediction audit
```

Test:

```text
λ_i ≈ function(B_i)
```

If yes, coefficients are no longer just calibrated.  
They are budget-determined.
