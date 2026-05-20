# V796 Post-Mortem Root Cause Audit: Tensor Momentum Failure

## Purpose

The last sequence did the right thing scientifically:

```text
measure twice
find the failure
do not force closure
```

This post-mortem explains why the tensor momentum branch failed.

## Executive verdict

```text
The branch failed because we promoted a scalar/conformal recoverability geometry
into a tensor ADM system without deriving an independent momentum-carrying degree of freedom.
```

That is the root cause.

## What was solid

### 1. Scalar/conformal branch

This remains strong:

```text
G_proxy = -2Δφ
R_conf = exp(-2φ)G_proxy
```

This is a scalar/conformal curvature-source closure.

### 2. 2D correction

V781 found an important mathematical fact:

```text
2D Einstein tensor is identically zero.
```

So moving to 2+1 was necessary.

### 3. 2+1 tensor existence

V782 showed:

```text
G_ab ≠ 0
```

So tensor testing became possible.

### 4. ADM decomposition

V791 found the key split:

```text
Hamiltonian constraint R² = 1.000
Momentum constraints ≈ failed
```

This is the most important diagnostic.

## What failed

### Failed branch 1 — hand-built stress

The original gradient stress tensor did not close:

```text
joint G/T R² ≈ 0.0004
```

### Failed branch 2 — action-style stress

V783 improved but remained partial:

```text
joint action-library R² ≈ 0.379
```

### Failed branch 3 — surplus lapse

V785/V787 improved transfer:

```text
best heldout R² ≈ 0.575
scaling mean R² ≈ 0.480
```

Good signal, but still not tensor closure.

### Failed branch 4 — shear terms

V789:

```text
G_12 best R² ≈ 0.044
G_01 / G_02 ≈ 0
```

### Failed branch 5 — continuity flux

V793:

```text
best momentum R² ≈ 0.001
```

### Failed branch 6 — shift solve

V795:

```text
mean momentum reduction = -0.021
```

The solve made the residual slightly worse.

## Root cause

### RC1 — scalar geometry promoted too far

The original discovery was scalar/conformal:

```text
Ω = exp(φ)
g_eff = Ω²g0
```

That naturally creates:

```text
scalar curvature
Ricci-like scalar structure
Hamiltonian-like scalar constraint
```

It does not automatically create:

```text
momentum flow
off-diagonal stress
vector current
```

### RC2 — ADM momentum requires a real vector/current degree of freedom

ADM momentum constraints are not scalar constraints.

They require something like:

```text
J_i
```

a momentum/current density.

But the model currently has only scalar fields:

```text
μ
repair
C
φ
```

Their gradients can imitate directions, but they are not a conserved current.

### RC3 — shift was guessed, not derived

We tried:

```text
C-flow shift
repair-flow shift
mixed shift
Poisson-like β solve
```

But none were derived from a true recoverability-current law.

So they were underdetermined.

### RC4 — Hamiltonian closure does not imply Einstein tensor closure

This is crucial.

The model can truthfully have:

```text
scalar Einstein-form closure
```

without having:

```text
full tensor Einstein closure
```

That is exactly what the data shows.

### RC5 — missing conservation equation

The real missing object is probably:

```text
∇_a J^a_recoverability = source/sink
```

or a related retained-current law.

Without that, there is no principled momentum source.

## First-principles correction

Do not continue by adding terms.

The next object must be derived first:

```text
J_a^recoverability
```

A recoverability current should be built from:

```text
ordered update flow
defect transport
repair transport
surplus transport
Ω deformation flow
```

Then momentum closure becomes:

```text
M_i ≈ J_i
```

not:

```text
M_i ≈ random shear terms
```

## Correct status after post-mortem

```text
Scalar/conformal Einstein-form closure: strong
ADM Hamiltonian closure: strong
Tensor momentum closure: failed
Root cause: no derived recoverability current
```

## Correct next step

```text
V797 — derive recoverability current J_a
```

Goal:

```text
derive a vector/current law before retrying the momentum constraints
```

Pass condition:

```text
J_i predicts ADM momentum residuals on held-out geometries.
```

Fail condition:

```text
J_i does not improve momentum closure beyond chance.
```
