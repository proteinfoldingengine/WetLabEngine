# V817 Accessibility Constraint Law Validation

## Purpose
Compress the V813 accessibility law into the simplest constraint form.

Since:

```text
A = exp(C - μ + η repair)
```

then:

```text
log A = C - μ + η repair
```

and:

```text
G_proxy = 2α Δ log A
        = k Δ(C - μ + η repair)
```

## Summary

```text
best model: separate_terms
mean heldout R²: 0.917
min heldout R²: 0.865
mean corr: 0.958
```

## Model scores

| model | mean R² | min R² | mean corr |
|---|---:|---:|---:|
| separate_terms | 0.917 | 0.865 | 0.958 |
| balance_plus_level | 0.897 | 0.874 | 0.948 |
| compressed_balance | 0.880 | 0.856 | 0.938 |

## Coefficients

| model | term | coef |
|---|---|---:|
| compressed_balance | intercept | 0.000316 |
| compressed_balance | lap_balance | 0.250386 |
| separate_terms | intercept | 0.000210 |
| separate_terms | lap_C | 0.131626 |
| separate_terms | lap_mu | -0.378666 |
| separate_terms | lap_repair | 0.105600 |
| balance_plus_level | intercept | -0.020146 |
| balance_plus_level | lap_balance | 0.214880 |
| balance_plus_level | balance | -0.090446 |

## Interpretation

If the compressed law holds, the curvature result becomes:

```text
curvature = Laplacian of recoverability accessibility balance
```

## Verdict

```text
compressed_accessibility_constraint_supported
```

## Next

```text
V818 — final accessibility law theorem-shape memo
```
