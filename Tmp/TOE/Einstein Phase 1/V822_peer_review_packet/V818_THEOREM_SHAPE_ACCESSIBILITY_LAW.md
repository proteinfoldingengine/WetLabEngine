# V818 Theorem-Shape Accessibility Curvature Law

## Purpose

The branch has now compressed into a small, stable structure.

The goal of V818 is to state the irreducible theorem-shape result.

## Surviving law

```text
A = exp(C - μ + η repair)
```

so:

```text
log A = C - μ + η repair
```

The curvature law is:

```text
G_proxy = 2α Δ log(A + ε)
```

which compresses to:

```text
G_proxy ∝ Δ(C - μ + η repair)
```

## What survived

```text
1. Ω / φ conformal geometry
2. scalar curvature closure
3. ADM Hamiltonian closure
4. accessibility-density interpretation
5. compressed Laplacian recoverability-balance law
```

## What failed

```text
1. conserved local momentum current
2. ADM momentum closure
3. local transport evolution law for A
```

The failures are not noise. They define the boundary of the result.

## Theorem-shape statement

### Primitive

The primitive is not momentum.

The primitive is:

```text
reachable-state density A(x, τ)
```

### Accessibility potential

Geometry responds to accessibility through a logarithmic potential:

```text
φ = -α log(A + ε)
```

### Metric

```text
Ω = exp(φ)
g_eff = Ω² g0
```

### Curvature proxy

```text
G_proxy = -2Δφ
```

### Substitution

Substitute:

```text
φ = -α log(A + ε)
```

Then:

```text
G_proxy = -2Δ[-α log(A + ε)]
```

Therefore:

```text
G_proxy = 2α Δ log(A + ε)
```

This is the compressed law.

## Plain-language meaning

```text
Curvature emerges where reachable recovery futures compress or expand spatially.
```

Defects reduce accessibility.

Repair increases accessibility.

Surplus capacity increases accessibility.

The geometry responds to the spatial second derivative of that accessibility balance.

## Why the Laplacian appears

The Laplacian is the minimal local operator that detects spatial compression / expansion.

A first derivative only detects direction.

A zero-order term only detects amount.

Curvature needs local second-order structure:

```text
where does accessibility bend, compress, or spread?
```

That is exactly what:

```text
Δ log A
```

measures.

## Why log accessibility appears

A logarithm converts multiplicative accessibility into additive potential.

If accessible futures combine multiplicatively, then the natural potential is:

```text
log A
```

This also makes:

```text
C - μ + η repair
```

the additive recoverability balance.

## Why scalar / Hamiltonian closure works

The accessibility field is scalar.

The Hamiltonian constraint is scalar.

So scalar closure is natural:

```text
curvature density ↔ accessibility compression
```

## Why momentum closure failed

Momentum closure requires local conserved vector transport:

```text
J_i
```

But accessibility is not behaving like conserved flow.

It behaves like a state-function:

```text
A = F(C, μ, repair)
```

This explains why:

```text
transport helped partially
but conservation failed
```

## Final theorem-shape claim

Allowed:

```text
The simulation supports an accessibility-curvature law:
curvature is strongly predicted by the Laplacian of log reachable-state density.
```

Not allowed:

```text
The full tensor Einstein equations are closed.
```

## Current strongest statement

```text
Recoverability pressure creates an accessibility field A.
Spatial compression of log A generates conformal curvature.
```

## Next test

```text
V819 — perturb A directly and verify curvature response
```

Goal:

```text
If A is the true primitive, direct perturbations of A should produce predictable curvature changes.
```
