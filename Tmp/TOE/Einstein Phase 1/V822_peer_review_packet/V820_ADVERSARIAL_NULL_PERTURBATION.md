# V820 Adversarial / Null Perturbation Test

## Purpose

V819 confirmed that direct perturbations of accessibility A produce predicted curvature changes.

V820 asks whether this is specific to the law:

```text
δG = 2α Δδlog(A)
```

or whether any perturbation-like pattern can predict the response.

## Predictors tested

```text
correct Δlog(A) Laplacian
zero predictor
wrong sign
zero-order perturbation
gradient-like perturbation
shuffled correct predictor
unrelated Laplacian
```

## Summary

```text
correct predictor mean R²: 1.000
correct predictor min R²:  1.000
correct predictor corr:    1.000

next best predictor:       null_zero
next best mean R²:         0.000

margin vs next best:       1.000
```

## Predictor scores

| predictor | mean R² | min R² | mean corr |
|---|---:|---:|---:|
| correct_delta_lap_logA | 1.000 | 1.000 | 1.000 |
| null_zero | 0.000 | 0.000 | nan |
| shuffled_correct | -1.000 | -1.047 | -0.000 |
| wrong_sign | -3.000 | -3.000 | -1.000 |
| gradient_like_q | -12.634 | -19.461 | -0.000 |
| zero_order_q | -30.352 | -59.440 | -0.738 |
| unrelated_lap | -37.072 | -124.131 | 0.019 |

## Verdict

```text
adversarial_null_test_passed
```

## Interpretation

The curvature response is specifically tied to:

```text
Δ log(A)
```

not to generic perturbation, gradient, shuffled, or unrelated structures.

## Next

```text
V821 — final accessibility curvature validation freeze
```
