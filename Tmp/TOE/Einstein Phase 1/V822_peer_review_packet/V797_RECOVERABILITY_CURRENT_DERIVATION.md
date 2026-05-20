# V797 Recoverability Current Derivation

## Purpose

V796 identified the root cause:

```text
We tried to close ADM momentum constraints without first deriving a recoverability current.
```

V797 derives the missing object:

```text
J_a^recoverability
```

## First principle

```text
Scalar constraints can be closed by scalar pressure.
Vector constraints require vector transport.
```

The model already has scalar fields:

```text
μ_defect
repair
C_surplus
φ = log Ω
```

Those are enough for scalar / Hamiltonian closure.

They are not enough by themselves for momentum closure.

## Required object

We need a current:

```text
J_a = (J_τ, J_i)
```

where:

```text
J_τ = recoverability density
J_i = recoverability flux
```

## Recoverability density

A first candidate is:

```text
J_τ = C_surplus - μ_defect + η repair
```

Interpretation:

```text
retained recoverability density
= surplus capacity
- unresolved defect burden
+ active repair contribution
```

## Recoverability spatial current

A minimal vector current should contain four pieces.

### 1. Advective recoverability flux

```text
A · C · v_i
```

where `v_i` is the ordered-update displacement / transport velocity of recoverability structure.

This represents recoverability being carried across the manifold.

### 2. Gradient relaxation flux

```text
- B · ∂_i C
```

This is diffusion-like surplus equalization.

### 3. Geometry-drift flux

```text
D · repair · ∂_i φ
```

This says repair moves along Ω / geometry deformation gradients.

### 4. Defect-drag flux

```text
- E · φ · ∂_i μ
```

This says defect burden drags recoverability flow.

## Candidate current

```text
J_i =
    A C v_i
  - B ∂_i C
  + D repair ∂_i φ
  - E φ ∂_i μ
```

## Continuity equation

The current should satisfy:

```text
∂_τ J_τ + ∂_i J_i = σ_repair - σ_defect
```

where:

```text
σ_repair = local creation of recoverability by repair
σ_defect = local loss from unresolved defect growth
```

## Momentum constraint target

ADM momentum residual is:

```text
M_i = D_j(K^j_i - δ^j_i K)
```

The correct closure test is:

```text
M_i ≈ κ J_i
```

not:

```text
M_i ≈ arbitrary shear terms
```

## Why previous attempts failed

### Shear terms failed

They were local products of gradients, not a conserved current.

### Shift terms failed

They were guessed from flow gradients, not solved from a current law.

### Continuity flux failed

It used raw flux features, but not a structured current with density, drift, defect drag, and source/sink balance.

## Pass condition

```text
J_i predicts ADM momentum residuals on held-out geometries
and materially improves over V792/V793 baselines.
```

Baseline to beat:

```text
V792 best momentum mean R² ≈ 0.043
V793 best momentum R² ≈ 0.001
```

## Fail condition

```text
J_i does not improve momentum closure beyond chance.
```

## Next step

```text
V798 — implement and test recoverability current J_i
```

Test:

```text
M_x ≈ J_x
M_y ≈ J_y
```

across held-out seeds / defect counts / complexity levels.
