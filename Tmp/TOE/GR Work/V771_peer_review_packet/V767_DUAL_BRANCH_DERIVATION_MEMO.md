# V767 Formal Dual-Branch Derivation Memo

## Purpose

V767 consolidates V764–V766 into a formal dual-branch derivation memo.

The goal is to explain why Step 4 does not use one universal source branch for both curvature observables.

## Guardrail

```text
All structure is across ordered recoverability updates.
The ordering parameter is not assumed to be physical time.
```

## Core identities

Let:

```text
φ = log Ω
```

Then the two curvature-side observables used in the bridge are:

```text
G_proxy = -2 Δφ
R_conf  = -2 exp(-2φ) Δφ
```

Therefore:

```text
R_conf = exp(-2φ) G_proxy
```

This identity explains the dual-branch split.

## Branch 1 — G-side Laplacian-dominant closure

### Observable

```text
G_proxy = -2 Δφ
```

This is a second-order spatial observable.

### Source requirement

By locality and isotropy, the lowest-order nontrivial scalar spatial operator is the Laplacian.

Recoverability pressure enters through:

```text
repair
C = recoverability surplus
```

Therefore the necessary spatial source terms are:

```text
Δrepair
ΔC
```

which correspond to:

```text
lap_repair
lap_C
```

### Frozen G-side law

```text
J_G = F(log_mu, lap_repair, lap_C, repair_phi)
```

### Evidence

V765 showed:

```text
zero-order R²:        0.241
first-derivative R²:  0.514
zero + first R²:      0.371

lap repair/surplus R²: 0.993
minimal G R²:          0.993
```

Conclusion:

```text
G-side closure requires second-order spatial recoverability variation.
```

## Branch 2 — R-side conformal-weighted closure

### Observable

```text
R_conf = -2 exp(-2φ) Δφ
```

Equivalently:

```text
R_conf = exp(-2φ) G_proxy
```

### Source requirement

Because R_conf includes the conformal factor:

```text
exp(-2φ)
```

the R-side source must include conformal weighting and curvature-energy correction terms.

### Frozen R-side law

```text
J_R = F(
  log_mu,
  lap_repair,
  lap_C,
  repair_phi,
  exp_phi_lap_C,
  exp_phi_lap_repair,
  grad_phi_energy,
  phi_lap_C,
  C_grad_phi,
  boundary_proxy
)
```

### Evidence

V766 showed:

```text
unweighted G_proxy → R_conf R²: -0.188
conformal-weighted G R²:        1.000
base 4-term R²:                 0.959
full refined R²:                0.999
```

Conclusion:

```text
R-side closure necessarily requires conformal weighting.
```

## Why one branch failed

V759 showed that forcing the refined 10-term R-side law onto G-side degraded G scaling.

That was not a failure of closure.

It showed:

```text
G_proxy and R_conf are different observables.
```

They share a base structure but require different closures.

## Why dual-branch succeeded

V759.1 froze:

```text
G-side: minimal spatial source law
R-side: conformal refined source law
```

and obtained:

```text
mean G R²: 0.996
min G R²:  0.991

mean R R²: 1.000
min R R²:  0.999

continuum G R² estimate: 0.995
continuum R R² estimate: 1.000
```

## The dual-branch theorem-shaped statement

```text
Given bounded Ω=exp(φ), local recoverability pressure, and ordered update slices:

1. G_proxy = -2Δφ is closed by the lowest-order isotropic spatial source terms
   Δrepair and ΔC, with bounded defect/geometry coupling.

2. R_conf = exp(-2φ)G_proxy requires the same base source structure plus
   conformal weighting and curvature-energy correction terms.

Therefore the recoverability-to-curvature bridge is dual-branch:
Laplacian-dominant for G_proxy and conformal-weighted for R_conf.
```

## What is now supported

```text
G-side Laplacian necessity: analytically motivated and empirically supported
R-side conformal correction necessity: analytically motivated and empirically supported
dual-branch structural closure: supported under scaling
```

## What is not claimed

```text
physical GR
physical time
full coordinate-covariant Einstein tensor
formal continuum theorem
coefficient-free first-principles law
```

## Correct next step

```text
V768 — coefficient interpretation / invariant normalization derivation
```

We now know the terms.  
Next we ask whether their coefficients follow from normalization, units, or invariant ratios.
