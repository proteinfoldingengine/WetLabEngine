# V819 Direct Accessibility Perturbation Curvature Response

## Purpose

Test the V818 law directly:

```text
G_proxy = 2α Δ log(A + ε)
```

by perturbing A itself and checking whether curvature changes as predicted.

## Method

For each synthetic accessibility field:

```text
A₂ = A · exp(amp · q(x,y))
```

Predicted curvature change:

```text
δG_pred = 2α Δ[log(A₂) - log(A)]
```

Observed curvature change:

```text
δG_obs = G(A₂) - G(A)
```

## Summary

```text
tests: 48
mean δG R²: 1.000000
min δG R²: 1.000000
mean δG corr: 1.000000
min δG corr: 1.000000
mean |δG|: 0.002026
```

## Verdict

```text
direct_accessibility_perturbation_confirmed
```

## Interpretation

This confirms that when A is perturbed directly, curvature responds according to the accessibility law.

## Next

```text
V820 — adversarial/null perturbation test
```
