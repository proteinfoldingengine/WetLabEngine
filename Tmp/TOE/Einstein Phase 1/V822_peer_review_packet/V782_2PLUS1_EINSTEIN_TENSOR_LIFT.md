# V782 2+1 Ordered Recoverability Einstein Tensor Lift

## Purpose

V781 showed the true 2D Einstein tensor vanishes identically.

V782 lifts the Atrium metric into a 2+1 ordered recoverability geometry:

```text
ds² = -dτ² + Ω(τ,x,y)²(dx² + dy²)
```

where τ is ordered recoverability update order.

## Tensor construction

Computed directly:

```text
Γᵃ_bc
R_ab
R
G_ab = R_ab - 1/2 g_ab R
```

## Summary

```text
mean |R_scalar|  = 1.128583
mean |G_ab|      = 0.598965

joint G/T affine R²   = 0.000
joint G/T affine corr = 0.021

component mean R² = 0.004
component min R²  = 0.000
```

## Component scores

| component | mean |G| | mean |T| | affine R² | corr | alpha |
|---|---:|---:|---:|---:|---:|
| 00 | 0.081214 | 1.111441 | 0.025 | 0.157 | 0.012943 |
| 01 | 0.098949 | 0.352682 | 0.000 | 0.003 | -0.000741 |
| 02 | 0.099941 | 0.354861 | 0.000 | 0.014 | -0.003275 |
| 11 | 0.389166 | 0.196674 | 0.001 | 0.038 | 0.093493 |
| 12 | 0.000902 | 0.121484 | 0.000 | 0.007 | -0.000062 |
| 22 | 0.389166 | 0.207163 | 0.000 | 0.017 | 0.041008 |

## Interpretation

The 2+1 lift succeeds at the first required step:

```text
G_ab is nonzero.
```

This means tensor-level testing is now mathematically possible.

The initial stress tensor here is still a candidate built from recoverability gradients.

If closure is weak, the next step is not to force the result; it is to derive T_ab by variational action with respect to g_ab.

## Correct next step

```text
V783 — derive recoverability T_ab from action variation and retest tensor closure
```
