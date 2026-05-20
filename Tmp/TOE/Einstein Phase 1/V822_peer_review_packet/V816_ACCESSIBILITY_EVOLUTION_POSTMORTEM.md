# V816 Accessibility Evolution Failure Post-Mortem

## Verdict

```text
A predicts curvature strongly.
A_t is not predicted by local diffusion/source terms.
```

This means the accessibility field is probably not a locally evolved conserved field.

It behaves more like:

```text
a state-function / constraint solution
```

than:

```text
a dynamical transport variable
```

## Evidence

### V813

Accessibility curvature law:

```text
G_proxy = 2α Δ log(A + ε)
```

Strong held-out result:

```text
mean R² ≈ 0.879
min R² ≈ 0.860
corr ≈ 0.938
```

### V815

Accessibility evolution law:

```text
A_τ ≈ diffusion + source/sink
```

failed:

```text
mean R² ≈ 0.010
```

## First-principles interpretation

The failure is coherent.

If A is reachable-state density, it may not evolve like local matter.

Instead, each ordered update recomputes accessibility from the current recoverability state:

```text
A = F(C, μ, repair)
```

So curvature reads accessibility:

```text
G_proxy ∝ Δ log A
```

but A itself is not governed by a simple local update law.

## Corrected interpretation

Do not model:

```text
A_τ = local diffusion + source
```

Model:

```text
A = constraint state
```

Specifically:

```text
log A = C - μ + η repair
```

Then:

```text
G_proxy = 2α Δ log A
```

This collapses to:

```text
G_proxy = 2α Δ(C - μ + η repair)
```

That is a constraint curvature law.

## Why this explains prior failures

### Momentum failure

Momentum expects local vector transport.

But A is not transported locally.

### Conservation failure

Conservation expects closed flow.

But A is recomputed from accessibility constraints.

### Evolution failure

A_t is weak because A does not obey a standalone local PDE in this toy construction.

## New correct target

The next step is:

```text
V817 — accessibility constraint law validation
```

Test the compressed law:

```text
G_proxy ≈ k Δ(C - μ + η repair)
```

against the richer accessibility law:

```text
G_proxy ≈ 2α Δ log A
```

If the compressed law holds, the result becomes extremely simple:

```text
curvature = Laplacian of recoverability accessibility balance
```
