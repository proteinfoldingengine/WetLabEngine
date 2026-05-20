# V794 Momentum Constraint Failure Freeze and Shift-Solve Route

## Verdict

```text
Hamiltonian/scalar ADM constraint: closed.
Momentum/off-diagonal ADM constraints: not closed.
```

This is now a stable diagnostic result.

## What succeeded

### Scalar / conformal branch

The scalar/conformal branch remains strong:

```text
G_proxy = -2Δφ
R_conf = exp(-2φ)G_proxy
```

### 2+1 tensor lift

The 2+1 recoverability metric produced a nonzero Einstein tensor.

### ADM Hamiltonian constraint

V791 showed:

```text
Hamiltonian mean R² = 1.000
```

So the scalar constraint closes.

## What failed

### Momentum constraints

V791:

```text
Momentum_x mean R² = 0.030
Momentum_y mean R² = 0.084
```

### Shift-flow attempt

V792:

```text
best momentum mean R² = 0.043
```

Shift helped slightly, but did not close.

### Continuity / flux attempt

V793:

```text
best momentum R² ≈ 0.001
```

Recoverability flux sources did not explain the momentum constraints.

## Interpretation

This is not a general failure of the bridge.

It says the system has:

```text
scalar constraint closure
```

but not:

```text
momentum constraint closure
```

That distinction matters.

The missing structure is probably not another hand-added source term.

The correct next step is to solve the shift vector from the momentum constraints.

## Correct mathematical next step

Instead of guessing β_i, solve:

```text
D_j(K^j_i - δ^j_i K) = J_i^recoverability
```

for:

```text
β_i
```

where:

```text
K_ij = -(1/2N)(∂τ h_ij - D_i β_j - D_j β_i)
```

This makes β_i an inferred recoverability-flow geometry, not a heuristic input.

## Frozen status

```text
Step 4 scalar/conformal closure: strong
2+1 tensor G_ab existence: confirmed
ADM Hamiltonian constraint: closed
ADM momentum constraints: failed
full tensor equation: not closed
```

## Correct next step

```text
V795 — solve shift vector β_i from momentum constraints
```

Goal:

```text
Given h_ij, N(C), and target J_i^recoverability,
solve elliptic/least-squares shift β_i that minimizes momentum residual.
```
