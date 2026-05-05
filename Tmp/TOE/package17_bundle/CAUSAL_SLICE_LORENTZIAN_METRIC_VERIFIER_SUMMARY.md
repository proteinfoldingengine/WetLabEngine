# CAUSAL_SLICE_LORENTZIAN_METRIC_VERIFIER_SUMMARY.md

# Verifier Summary
## Lorentzian metric from causal rank time and antichain spatial metric

## Status
**Executed structural verifier. Not a curvature or GR proof.**

Verifier file:

```text
causal_slice_lorentzian_metric_verifier.py
```

Execution log:

```text
causal_slice_lorentzian_metric_verifier_run.log
```

## Captured output

```text
Causal slice Lorentzian metric verifier
==================================================
Route:
longest-chain time + antichain spatial h_ab -> ADM-like block g_mu_nu

PASS: 78.75
SOFT_FAIL: 13.75
HARD_FAIL: 7.5
n_slices_used_median: 8.5
depth_time_corr_median: 0.9777411078654019
median_h_rank_median: 3.0
median_h_condition_median: 2.0462149979338617
signature_fraction_median: 1.0
median_g_condition_median: 88.24840056647994
```

## Interpretation

The verifier tests:

\[
(\tau,h_{ab})
\rightarrow
g_{\mu\nu}
=
\begin{pmatrix}
-N^2 & 0 \\
0 & h_{ab}
\end{pmatrix}.
\]

It checks:
- causal rank/time stability;
- spatial metric rank;
- spatial metric conditioning;
- Lorentzian signature;
- block metric conditioning.

It supports a local Lorentzian assembly but does not derive lapse, shift, curvature, or covariance.

**End of summary.**
