# V815 Accessibility Field Evolution Law Test

## Purpose
V814 froze the accessibility-curvature law:

```text
G_proxy = 2α Δ log(A + ε)
```

V815 asks what governs A itself.

## Accessibility field

```text
A = exp(C - μ + η repair)
```

## Candidate evolution forms

Tested:

```text
A_τ ≈ diffusion + repair gain - defect loss + surplus gain
```

and log-accessibility evolution:

```text
(log A)_τ ≈ Δ log A + source/sink terms
```

## Summary

```text
best target: A_t
best feature set: full_accessibility
mean heldout R²: 0.010
min heldout R²: -0.001
mean corr: 0.104
```

## Scores

| target | feature set | mean R² | min R² | mean corr |
|---|---|---:|---:|---:|
| A_t | full_accessibility | 0.010 | -0.001 | 0.104 |
| A_t | diffusion_plus_sources | 0.004 | 0.002 | 0.062 |
| A_t | diffusion_only | 0.001 | 0.000 | 0.024 |
| A_t | logdiff_plus_phi | 0.000 | -0.000 | 0.022 |
| A_t | log_diffusion_only | 0.000 | -0.001 | 0.014 |
| A_t | phi_sources | 0.000 | -0.001 | 0.010 |
| A_t | source_sink | -0.000 | -0.000 | 0.007 |
| logA_t | full_accessibility | 0.008 | -0.010 | 0.096 |
| logA_t | diffusion_plus_sources | 0.003 | -0.002 | 0.056 |
| logA_t | logdiff_plus_phi | 0.001 | -0.002 | 0.038 |
| logA_t | phi_sources | 0.001 | -0.002 | 0.029 |
| logA_t | diffusion_only | 0.000 | -0.001 | 0.020 |
| logA_t | log_diffusion_only | 0.000 | -0.000 | 0.011 |
| logA_t | source_sink | 0.000 | -0.000 | 0.009 |

## Verdict

```text
accessibility_evolution_law_partial_or_weak
```

## Next

```text
V816 — prune accessibility evolution law or freeze if weak
```
