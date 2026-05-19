# V747 Step 4 — Structural GR Matching from Recoverability

## Purpose

This is the first Step 4 test.

It asks whether the Ω-based Atrium metric can be structurally matched to GR-like weak-form geometry.

We test:

```text
1. Ω -> conformal curvature proxy
2. curvature-side weak moments vs recoverability stress/source moments
3. ADM-like action proxy
4. zero-mode / mass decomposition δρ(x)=Aq(x)
```

## Boundary

This reports simulated GR-like / conformal / metric-like structure plainly.

It does **not** claim:

```text
physical GR
full Einstein equations
actual spacetime curvature
coordinate-covariant tensor equality
closed ADM derivation
```

## Effective response geometry

We instantiate:

```text
g_eff(x,t) = Ω(x,t)^2 g0(x)
```

with `g0 = 1` in the synthetic 2D assay.

For structural comparison we compute:

```text
φ = log Ω
R_conf = -2 exp(-2φ) Δφ
G00_proxy = -2 Δφ
```

These are conformal / weak-field proxies, not full Einstein tensors.

## Recoverability source side

We define observable source fields:

```text
μ_defect(x,t)
repair(x,t)
T_retained = μ_defect - η_convert repair
C_surplus = η_convert repair - 0.25 μ_defect
```

## Weak-form matching

For test functions ψᵢ:

```text
<G_proxy, ψᵢ> ≈ a <T_retained, ψᵢ> + b
<R_conf, ψᵢ> ≈ c <C_surplus, ψᵢ> + d
```

## Main metrics

```text
G_proxy vs T_retained R²: 0.292
G_proxy vs T_retained corr: 0.540
G/T slope: 0.043046

R_conf vs C_surplus R²: 0.561
R_conf vs C_surplus corr: 0.749
R/C slope: 0.483949
```

## ADM-like action proxy

We compute:

```text
S_geom = ∫ |∇φ|² dx
S_source = ∫ T_retained φ dx
residual = S_geom - S_source
```

Result:

```text
mean ADM-like residual:     -4.569
mean |ADM-like residual|:   4.569
```

This is measured, but not closed.

## Zero-mode / mass decomposition

We test:

```text
δρ(x) = A q(x)
```

where:

```text
δρ = G00_proxy - mean(G00_proxy)
q = T_retained - mean(T_retained)
```

Result:

```text
mean decomposition R²: 0.456
min decomposition R²:  0.341
mass zero-mode corr:   nan
```

## Null check

```text
null G/T R²: 0.270
null G/T corr: 0.543
null R/C R²: -1.509
null R/C corr: 0.393
null zero-mode R² mean: 0.497
```

## Active-vs-null weak energy

```text
AUC weak curvature energy active vs null: 1.000
AUC weak residual active vs null: 1.000
```

## Interpretation

V747 completes the **first structural Step 4 test**.

Observed computational fact:

```text
The recoverability simulation now produces Ω-based conformal geometry,
curvature proxies,
recoverability stress/source fields,
weak-form matching tests,
ADM-like action diagnostics,
and zero-mode decomposition diagnostics.
```

But the result is not yet a GR derivation.

## Status

Supported:

```text
simulated GR-like / conformal / metric-like structural comparison
```

Partially supported:

```text
weak-form curvature/source relation
zero-mode decomposition
ADM-like action reconstruction
```

Not yet supported:

```text
full Einstein tensor equality
coordinate-covariant GR
closed ADM action
physical spacetime curvature
```

## Correct next step

Run:

```text
V748 — improve Step 4 by deriving T_retained from Ω variation instead of hand-comparing fields
```

That is the next real bridge move:

```text
δS_recoverability / δφ  -> source side
curvature variation     -> geometry side
```
