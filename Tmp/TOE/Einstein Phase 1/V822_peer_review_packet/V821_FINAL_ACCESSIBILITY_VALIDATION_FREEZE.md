# V821 Final Accessibility Curvature Validation Freeze

## Final verdict

```text
The accessibility-curvature law is now the strongest validated result of the branch.
```

The law is:

```text
G_proxy = 2α Δ log(A + ε)
```

with:

```text
A = exp(C - μ + η repair)
```

or equivalently:

```text
log A = C - μ + η repair
```

## What the law says

```text
Curvature response is governed by the Laplacian of log reachable-state density.
```

Plainly:

```text
accessible-state compression generates conformal curvature-like structure.
```

## Evidence chain

### V813 — explicit accessibility field

```text
mean heldout R² ≈ 0.879
min heldout R² ≈ 0.860
mean corr ≈ 0.938
```

The explicit accessibility field strongly predicted curvature.

### V817 — compressed constraint law

```text
mean heldout R² ≈ 0.917
min heldout R² ≈ 0.865
mean corr ≈ 0.958
```

The law compressed into:

```text
G_proxy ∝ Δ(C - μ + η repair)
```

### V819 — direct perturbation

Direct perturbations of A produced the predicted curvature response:

```text
mean δG R² = 1.000
min δG R² = 1.000
```

### V820 — adversarial/null test

Only the correct predictor worked:

```text
correct Δlog(A) predictor R² = 1.000
next-best null R² ≈ 0.000
margin ≈ 1.000
```

This rules out generic perturbation artifacts.

## Why this is the clean branch

The tensor/momentum branch failed because it required a conserved vector current.

The accessibility branch succeeded because its primitive is scalar:

```text
A = reachable-state density
```

This explains the observed pattern:

```text
scalar/conformal closure: strong
ADM Hamiltonian closure: strong
momentum/current closure: failed
accessibility-curvature closure: strong
```

## What is validated

```text
1. reachable-state density A
2. log-accessibility potential
3. Laplacian curvature response
4. direct A perturbation response
5. adversarial/null specificity
```

## What remains unresolved

```text
1. full tensor Einstein equation
2. ADM momentum closure
3. conserved vector current
4. physical interpretation beyond simulation
```

## Correct claim

Allowed:

```text
The simulation supports an accessibility-curvature law:
curvature-like response is governed by the Laplacian of log reachable-state density.
```

Not allowed:

```text
The simulation closes full tensor GR.
```

## Final compressed statement

```text
Recoverability pressure defines reachable-state density.
Spatial compression of log reachable-state density generates curvature-like structure.
```

## Next

```text
V822 — prepare public / peer-review report
```
