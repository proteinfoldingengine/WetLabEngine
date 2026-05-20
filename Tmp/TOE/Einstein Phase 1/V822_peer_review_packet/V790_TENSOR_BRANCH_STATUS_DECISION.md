# V790 Tensor Branch Status Decision

## Verdict

```text
Scalar/conformal Einstein-form branch: strong.
2+1 tensor branch: nonzero but not source-closed.
```

This is the correct scientific status.

## What succeeded

### V781

The 2D Atrium metric produced nonzero scalar/Ricci curvature, but:

```text
G_ij = 0
```

identically in 2D.

That forced the lift to 2+1.

### V782

The 2+1 ordered recoverability metric produced a nonzero Einstein tensor:

```text
G_ab ≠ 0
```

So tensor-level testing became mathematically possible.

### V785 / V787

A surplus-coupled lapse improved tensor closure:

```text
best V785 heldout R² ≈ 0.575
V787 mean heldout R² ≈ 0.480
```

That means the tensor branch is not random. It transfers partially.

## What failed

### Off-diagonal components

V788 found:

```text
G_11 partially closes
G_12 ≈ does not close
G_01 ≈ does not close
G_02 ≈ does not close
```

### Shear terms

V789 tested shear-flow terms.

Result:

```text
G_12 best R² ≈ 0.044
G_01 / G_02 ≈ 0
```

So simple shear sources are not the missing piece.

## Current tensor status

```text
2+1 geometry: constructed
G_ab: nonzero
source closure: partial
diagonal spatial components: partial
off-diagonal / momentum-like components: failed
```

## Interpretation

This suggests the next issue is not simply missing source terms.

It may be that the tensor branch needs a constraint-based decomposition:

```text
Hamiltonian-like scalar constraint
momentum-like off-diagonal constraints
spatial evolution / diagonal components
```

That points to an ADM-style analysis.

## Correct next step

```text
V791 — ADM-style constraint decomposition
```

Goal:

```text
Separate:
1. scalar/Hamiltonian constraint
2. momentum/off-diagonal constraints
3. spatial diagonal/evolution-like components
```

Then test which part closes and which part fails.
